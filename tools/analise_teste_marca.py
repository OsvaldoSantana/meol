# -*- coding: utf-8 -*-
"""A analise do teste de marca, gravada ANTES de existir qualquer resposta (P-162, P4, P-116).

POR QUE ELE EXISTE. A regra que escolhe a direcao visual foi decidida por ele (17a, q-a, r-a,
t-a) antes de o teste rodar. Um script escrito depois de ver os dados escolheria, sem querer,
a regra que da o resultado mais bonito. Este arquivo tem o sha256 gravado no pre-registro
final (`docs/marca/preregistro-teste-de-marca-final.md`); mudar uma linha depois do merge e
analise nova, e o pre-registro deixa de cobri-la.

O QUE ELE FAZ. Le as seis exportacoes do Google Forms (`data/teste-marca/versao-N.csv`, fora do
git), fica so com quem consentiu, passou no filtro e respondeu dentro da janela de 21 dias
(h-A), e aplica:
  - a REGRA (17a + q-a): por pessoa, o indice = media de "confiavel" e "e para mim" nas telas
    base. Sai da disputa a direcao com a PIOR media em "honesto". Entre as que ficam, a de
    maior media de indice vence se o intervalo de 95% (bootstrap pareado) da diferenca para a
    segunda NAO contem zero; se contem, e EMPATE e a escolha e dele, com criterio escrito.
  - H1 (16b): E supera D em "confiavel" e em "honesto" (as duas diferencas com IC > 0).
  - H2 (t-a): D pior que E e pior que C, em "confiavel" ou em "honesto".
  - H3 (j-A), EXPLORATORIA: a versao com rota bloqueada contra a base, em "confiavel".
  - H4: fora do teste (s-a), vai para a P-156.
Tudo sai duas vezes: SEM quem conhece pessoalmente quem faz a pesquisa (u-a), que DECIDE
(r-a), e com todos, como sensibilidade. Imprime so o agregado: contagens, medias e
intervalos. Nunca uma linha, nunca o texto aberto (que o script nem le). A analise so roda
depois de 23:59:59 do dia 21 (h-A: nunca encerrar olhando o resultado).

O QUE ELE NAO FAZ (P5). Nao le a pergunta aberta nem a de pronuncia. Nao pondera o
desequilibrio do rodizio (imprime quantas respostas cada versao teve). Nao corrige
multiplicidade entre H1, H2 e H3: a regra e uma so, e as hipoteses sao relatadas. Com menos
de 2 pessoas nao ha intervalo (reamostrar uma pessoa e ela mesma): sai SEM_DADOS, e a regra
nao escolhe nada.

    python tools/analise_teste_marca.py --inicio AAAA-MM-DD   # a analise, so depois do dia 21
    python tools/analise_teste_marca.py --conferir-cabecalho            # so os cabecalhos
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import io
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from typing import Any

import numpy as np

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA_PADRAO = os.path.join(RAIZ, "data", "teste-marca")

# ---- DECLARADO ANTES DOS DADOS: nao ha opcao de linha de comando para mudar nada disto ----
REAMOSTRAGENS = 10_000
SEMENTE = 20260927
NIVEL = 0.95
JANELA_DIAS = 21                      # h-A: do dia do primeiro convite ao 21o dia, inclusive
DIRECOES = ("E", "C", "D")
ORDENS = {1: "ECD", 2: "EDC", 3: "CED", 4: "CDE", 5: "DEC", 6: "DCE"}   # g-B
# Titulo exato de cada escala no Forms (docs/marca/teste-de-marca-questionario.md, secao 5),
# depois do prefixo "[Tela k] ". 7 e sempre o polo do nome.
ESCALAS = {
    "Pelo jeito da tela (cores, letras, desenho), este app passa inseguran\u00e7a ou "
    "seguran\u00e7a?": "seguro",
    "Pelo visual, esta tela parece feita para algu\u00e9m como voc\u00ea?": "para_mim",
    "Esta tela parece querer te vender algo ou parece honesta?": "honesto",
    "Esta tela parece golpe ou parece confi\u00e1vel?": "confiavel",
    "O visual desta tela lembra mais um app popular ou um app de luxo?": "luxo",
}
CONSENTIMENTO = "Concordo em participar"
FILTRO = ("H\u00e1 pelo menos 6 meses, voc\u00ea coloca dinheiro todo m\u00eas em a\u00e7\u00f5es, "
          "fundos de \u00edndice (ETF) ou fundos imobili\u00e1rios?")                  # v-a
AMIGO = ("Voc\u00ea conhece pessoalmente a pessoa que est\u00e1 fazendo esta pesquisa "
         "(\u00e9 amigo, parente ou colega dela)?")                                        # u-a
TELA = re.compile(r"^\[Tela ([1-6])\] (.+)$")
FORMATOS_DATA = ("%d/%m/%Y %H:%M:%S", "%Y/%m/%d %I:%M:%S %p", "%m/%d/%Y %H:%M:%S")


@dataclass
class Resposta:
    versao: int
    amigo: bool
    # notas[(direcao, "base" | "rota")][escala] = 1..7
    notas: dict[tuple[str, str], dict[str, int]] = field(default_factory=dict)


# ---------------------------------------------------------------- leitura do Forms ------

def _versao_do_arquivo(nome: str) -> int:
    m = re.fullmatch(r"versao-([1-6])\.csv", nome)
    if not m:
        raise SystemExit(f"{nome}: o arquivo de cada versao se chama versao-N.csv, N de 1 a 6")
    return int(m.group(1))


def _dentro_do_git_sem_ignorar(path: str) -> bool:
    """True se o arquivo esta dentro do repositorio E o git NAO o ignora (resposta real
    nunca entra no git). Fora do repositorio, ou sem git, devolve False."""
    alvo = os.path.abspath(path)
    if not alvo.startswith(RAIZ + os.sep):
        return False
    r = subprocess.run(["git", "-C", RAIZ, "check-ignore", "-q", alvo],
                       capture_output=True, check=False)
    return r.returncode == 1


def colunas_esperadas() -> list[str]:
    cols = [CONSENTIMENTO, FILTRO, AMIGO]
    cols += [f"[Tela {k}] {t}" for k in range(1, 7) for t in ESCALAS]
    return cols


def conferir_cabecalho(cabecalho: list[str]) -> list[str]:
    """As colunas que o script precisa e o CSV nao tem (lista vazia = cabecalho bom)."""
    return [c for c in colunas_esperadas() if c not in cabecalho]


def _data(texto: str) -> dt.datetime:
    for fmt in FORMATOS_DATA:
        try:
            return dt.datetime.strptime(texto.strip(), fmt)
        except ValueError:
            continue
    raise SystemExit(f"carimbo de data em formato desconhecido: {texto!r}")


def janela(inicio: dt.date) -> tuple[dt.datetime, dt.datetime]:
    """h-A: de 00:00 do dia do primeiro convite a 23:59:59 do 21o dia (horario de Brasilia,
    que e o fuso do formulario)."""
    fim = inicio + dt.timedelta(days=JANELA_DIAS - 1)
    return (dt.datetime.combine(inicio, dt.time(0, 0, 0)),
            dt.datetime.combine(fim, dt.time(23, 59, 59)))


def ler_versao(path: str, inicio: dt.date | None) -> tuple[list[Resposta], dict[str, int]]:
    versao = _versao_do_arquivo(os.path.basename(path))
    if _dentro_do_git_sem_ignorar(path):
        raise SystemExit(f"{path} esta dentro do repositorio e o git nao o ignora: resposta "
                         "real nunca entra no git. Use data/teste-marca/.")
    ordem = ORDENS[versao]
    cont = {"linhas": 0, "sem_consentimento": 0, "fora_do_filtro": 0, "fora_da_janela": 0,
            "validas": 0}
    out: list[Resposta] = []
    with io.open(path, encoding="utf-8-sig", newline="") as f:
        rd = csv.reader(f)
        cab = next(rd, [])
        falta = conferir_cabecalho(cab)
        if falta:
            raise SystemExit(f"{path}: faltam colunas {falta}")
        idx = {c: i for i, c in enumerate(cab)}
        ini, fim = janela(inicio) if inicio else (None, None)
        for linha in rd:
            cont["linhas"] += 1
            if linha[idx[CONSENTIMENTO]].strip() != "Concordo":
                cont["sem_consentimento"] += 1
                continue
            if linha[idx[FILTRO]].strip() != "Sim":
                cont["fora_do_filtro"] += 1
                continue
            if ini is not None and fim is not None:
                quando = _data(linha[0])
                if not (ini <= quando <= fim):
                    cont["fora_da_janela"] += 1       # guardada no CSV, fora da analise
                    continue
            r = Resposta(versao=versao, amigo=linha[idx[AMIGO]].strip() == "Sim")
            for k in range(1, 7):
                direcao = ordem[(k - 1) % 3]
                versao_estimulo = "base" if k <= 3 else "rota"
                r.notas[(direcao, versao_estimulo)] = {
                    nome: int(linha[idx[f"[Tela {k}] {titulo}"]])
                    for titulo, nome in ESCALAS.items()}
            out.append(r)
            cont["validas"] += 1
    return out, cont


# ---------------------------------------------------------------- estatistica -----------

def _matriz(respostas: list[Resposta], versao_estimulo: str, medida: str) -> np.ndarray:
    """(n, 3): a medida de cada pessoa em E, C e D. `indice` = media de confiavel e para_mim."""
    def valor(r: Resposta, d: str) -> float:
        n = r.notas[(d, versao_estimulo)]
        if medida == "indice":
            return (n["confiavel"] + n["para_mim"]) / 2
        return float(n[medida])
    return np.array([[valor(r, d) for d in DIRECOES] for r in respostas], dtype=float)


def ic_diferenca(a: np.ndarray, b: np.ndarray) -> tuple[float, float, float]:
    """Media e IC percentil (NIVEL) da diferenca pareada a - b, por bootstrap de pessoas."""
    d = a - b
    n = len(d)
    rng = np.random.default_rng(SEMENTE)
    idx = rng.integers(0, n, size=(REAMOSTRAGENS, n))
    medias = d[idx].mean(axis=1)
    alfa = (1 - NIVEL) / 2
    return float(d.mean()), float(np.quantile(medias, alfa)), float(np.quantile(medias, 1 - alfa))


def _pior_em_honesto(medias_honesto: dict[str, float]) -> list[str]:
    """17a: "nao ficar abaixo da mediana em honesto" = nao ser a PIOR direcao em honesto."""
    minimo = min(medias_honesto.values())
    return [d for d, m in medias_honesto.items() if m == minimo]


def decidir(respostas: list[Resposta]) -> dict[str, Any]:
    """A regra 17a + q-a sobre as telas base. Devolve so agregado."""
    if len(respostas) < 2:
        return {"resultado": "SEM_DADOS", "n": len(respostas)}
    ind = _matriz(respostas, "base", "indice")
    hon = _matriz(respostas, "base", "honesto")
    med_ind = {d: float(ind[:, i].mean()) for i, d in enumerate(DIRECOES)}
    med_hon = {d: float(hon[:, i].mean()) for i, d in enumerate(DIRECOES)}
    fora = _pior_em_honesto(med_hon)
    elegiveis = sorted((d for d in DIRECOES if d not in fora), key=lambda d: -med_ind[d])
    base = {"n": len(respostas), "media_indice": med_ind, "media_honesto": med_hon,
            "fora_por_honesto": fora, "elegiveis": elegiveis}
    if not elegiveis:
        return {**base, "resultado": "EMPATE", "motivo": "todas empatadas na pior media de honesto"}
    if len(elegiveis) == 1:
        return {**base, "resultado": "VENCE", "vencedora": elegiveis[0],
                "motivo": "unica elegivel pela regra do honesto"}
    a, b = elegiveis[0], elegiveis[1]
    media, lo, hi = ic_diferenca(ind[:, DIRECOES.index(a)], ind[:, DIRECOES.index(b)])
    ic = {"entre": [a, b], "diferenca": media, "ic": [lo, hi]}
    if lo <= 0 <= hi:
        return {**base, **ic, "resultado": "EMPATE", "motivo": "o IC da diferenca contem zero"}
    return {**base, **ic, "resultado": "VENCE", "vencedora": a if media > 0 else b}


def _classifica(lo: float, hi: float) -> str:
    if lo > 0:
        return "POSITIVA"
    if hi < 0:
        return "NEGATIVA"
    return "INCONCLUSIVA"


def hipoteses(respostas: list[Resposta]) -> dict[str, Any]:
    if len(respostas) < 2:
        return {"H1": "SEM_DADOS", "H2": "SEM_DADOS", "H3": "SEM_DADOS"}
    col = {d: i for i, d in enumerate(DIRECOES)}
    out: dict[str, Any] = {}
    # H1 (16b): E supera D em confiavel E em honesto.
    h1 = {}
    for esc in ("confiavel", "honesto"):
        m = _matriz(respostas, "base", esc)
        media, lo, hi = ic_diferenca(m[:, col["E"]], m[:, col["D"]])
        h1[esc] = {"E_menos_D": media, "ic": [lo, hi], "sinal": _classifica(lo, hi)}
    out["H1"] = {"escalas": h1,
                 "resultado": "CONFIRMADA" if all(v["sinal"] == "POSITIVA" for v in h1.values())
                 else "NAO_CONFIRMADA"}
    # H2 (t-a): D pior que E E pior que C, em confiavel OU em honesto.
    h2 = {}
    for esc in ("confiavel", "honesto"):
        m = _matriz(respostas, "base", esc)
        comp: dict[str, Any] = {}
        for outra in ("E", "C"):
            media, lo, hi = ic_diferenca(m[:, col[outra]], m[:, col["D"]])
            comp[f"{outra}_menos_D"] = {"media": media, "ic": [lo, hi],
                                        "sinal": _classifica(lo, hi)}
        comp["D_pior_que_as_duas"] = all(v["sinal"] == "POSITIVA" for v in comp.values())
        h2[esc] = comp
    out["H2"] = {"escalas": h2,
                 "resultado": "CONFIRMADA" if any(v["D_pior_que_as_duas"] for v in h2.values())
                 else "NAO_CONFIRMADA"}
    # H3 (j-A), EXPLORATORIA: com rota bloqueada menos base, em confiavel.
    h3 = {}
    base = _matriz(respostas, "base", "confiavel")
    rota = _matriz(respostas, "rota", "confiavel")
    for d in DIRECOES:
        media, lo, hi = ic_diferenca(rota[:, col[d]], base[:, col[d]])
        h3[d] = {"rota_menos_base": media, "ic": [lo, hi],
                 "leitura": {"NEGATIVA": "reduz", "POSITIVA": "aumenta",
                             "INCONCLUSIVA": "sem evidencia de reducao"}[_classifica(lo, hi)]}
    out["H3"] = {"exploratoria": True, "ordem_fixa": "base antes", "direcoes": h3}
    out["H4"] = "fora do teste (s-a, P-156)"
    return out


def descritivas(respostas: list[Resposta]) -> dict[str, Any]:
    """Media de cada escala por direcao e versao do estimulo. Nao decide nada: `seguro` e
    `luxo` so aparecem aqui."""
    if not respostas:
        return {}
    return {f"{d}-{v}": {e: float(np.mean([r.notas[(d, v)][e] for r in respostas]))
                         for e in ESCALAS.values()}
            for v in ("base", "rota") for d in DIRECOES}


def _amostra(respostas: list[Resposta]) -> dict[str, Any]:
    return {"n": len(respostas), "regra": decidir(respostas),
            "hipoteses": hipoteses(respostas), "descritivas": descritivas(respostas)}


def analisar(respostas: list[Resposta]) -> dict[str, Any]:
    """As duas amostras: a sem amigos DECIDE (r-a); a com todos e sensibilidade."""
    sem = [r for r in respostas if not r.amigo]
    por_versao = {v: sum(1 for r in respostas if r.versao == v) for v in ORDENS}
    return {
        "declarado": {"reamostragens": REAMOSTRAGENS, "semente": SEMENTE, "nivel": NIVEL},
        "n_total": len(respostas), "n_amigos": len(respostas) - len(sem),
        "por_versao": por_versao,
        "sem_amigos_DECIDE": _amostra(sem),
        "com_todos_SENSIBILIDADE": _amostra(respostas),
    }


# ---------------------------------------------------------------- saida ------------------

def _fmt(x: Any) -> str:
    if isinstance(x, float):
        return f"{x:.3f}"
    if isinstance(x, dict):
        return "{" + ", ".join(f"{k}: {_fmt(v)}" for k, v in x.items()) + "}"
    if isinstance(x, list):
        return "[" + ", ".join(_fmt(v) for v in x) + "]"
    return str(x)


def imprimir(rel: dict[str, Any], contagens: dict[str, int]) -> None:
    print("ANALISE DO TESTE DE MARCA -- so agregado (P-162)")
    print(f"declarado: {_fmt(rel['declarado'])}")
    print(f"linhas lidas e descartes: {_fmt(contagens)}")
    print(f"validas: {rel['n_total']} (n); conhecem quem faz a pesquisa: {rel['n_amigos']}")
    print(f"por versao do formulario (rodizio g-B): {_fmt(rel['por_versao'])}")
    for chave in ("sem_amigos_DECIDE", "com_todos_SENSIBILIDADE"):
        print(f"\n== {chave} (n={rel[chave]['n']})")
        print(f"regra: {_fmt(rel[chave]['regra'])}")
        for h, v in rel[chave]["hipoteses"].items():
            print(f"{h}: {_fmt(v)}")
        for k, v in rel[chave]["descritivas"].items():
            print(f"medias {k}: {_fmt(v)}")


def agora_em_brasilia() -> dt.datetime:
    """Brasilia e UTC-3 o ano todo desde 2019 (sem horario de verao)."""
    return dt.datetime.now(dt.timezone(dt.timedelta(hours=-3))).replace(tzinfo=None)


def main(argv: list[str] | None = None, agora: dt.datetime | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--pasta", default=PASTA_PADRAO)
    ap.add_argument("--inicio", help="dia do primeiro convite (AAAA-MM-DD), do commit das datas")
    ap.add_argument("--conferir-cabecalho", action="store_true")
    a = ap.parse_args(argv)
    arquivos = sorted(os.path.join(a.pasta, n) for n in os.listdir(a.pasta)
                      if n.endswith(".csv")) if os.path.isdir(a.pasta) else []
    if not arquivos:
        print(f"nenhum versao-N.csv em {a.pasta}")
        return 1
    if a.conferir_cabecalho:
        ruins = 0
        for p in arquivos:
            _versao_do_arquivo(os.path.basename(p))
            with io.open(p, encoding="utf-8-sig", newline="") as f:
                rd = csv.reader(f)
                falta = conferir_cabecalho(next(rd, []))
                # O formato do carimbo do Forms em pt-BR e NAO_CONFIRMADO: toda linha que
                # existir (a resposta de teste com "Nao concordo", no roteiro) o confere.
                datas = [_data(linha[0]) for linha in rd if linha]
            print(f"{os.path.basename(p)}: {'ok' if not falta else f'faltam {falta}'}; "
                  f"carimbos lidos: {len(datas)}")
            ruins += bool(falta)
        return 1 if ruins else 0
    if not a.inicio:
        print("--inicio e obrigatorio: sem a data do primeiro convite nao ha janela (h-A)")
        return 2
    inicio = dt.date.fromisoformat(a.inicio)
    ini, fim = janela(inicio)
    # h-A: "nunca encerrar olhando o resultado". Antes do fim da janela nao ha analise, so
    # --conferir-cabecalho, que nao calcula nada. Regra que depende de lembrar nao e regra (P7).
    if (agora or agora_em_brasilia()) <= fim:
        print(f"a janela so fecha em {fim} (Brasilia): antes disso nao ha analise (h-A)")
        return 3
    todas: list[Resposta] = []
    total: dict[str, int] = {}
    for p in arquivos:
        rs, c = ler_versao(p, inicio)
        todas += rs
        for k, v in c.items():
            total[k] = total.get(k, 0) + v
    print(f"janela (h-A, Brasilia): {ini} a {fim}")
    imprimir(analisar(todas), total)
    return 0


if __name__ == "__main__":
    sys.exit(main())
