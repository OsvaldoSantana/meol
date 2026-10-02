# -*- coding: utf-8 -*-
"""A analise do teste de marca, gravada ANTES de existir qualquer resposta (P-162, P4, P-116).

POR QUE EXISTE. A regra que escolhe a direcao visual foi decidida por ele (17a, q-a, r-a,
t-a) antes de o teste rodar. Um script escrito depois de ver os dados escolheria, sem querer,
a regra que da o resultado mais bonito. Este arquivo tem o sha256 gravado no pre-registro
final (`docs/marca/teste-de-marca/preregistro-final.md`); mudar uma linha depois do merge e
analise nova, e o pre-registro deixa de cobri-la.

O QUE ELE FAZ. Le a exportacao da pagina da S6 (`data/teste-marca/respostas.csv`, fora do
git), pelo contrato de `docs/marca/teste-de-marca/questionario.yaml` (colunas, ordens, escalas,
janela: P2, nada disso e literal aqui). Fica so com quem concluiu, consentiu, passou no filtro
e concluiu dentro da janela de 21 dias (h-A), e aplica:
  - a REGRA (17a + q-a): por pessoa, o indice = media de "confiavel" e "e para mim" nas telas
    base. Sai da disputa a direcao com a PIOR media em "honesto". Entre as que ficam, a de
    maior media de indice vence se o intervalo de 95% (bootstrap pareado) da diferenca para a
    segunda NAO contem zero; se contem, e EMPATE e a escolha e dele, com criterio escrito.
  - H1 (16b): E supera D em "confiavel" e em "honesto" (as duas diferencas com IC > 0).
  - H2 (t-a): D pior que E e pior que C, em "confiavel" ou em "honesto".
  - H3 (j-A), EXPLORATORIA: a versao com rota bloqueada contra a base, em "confiavel".
  - H4: fora do teste (s-a), vai para a P-156.
Tudo sai duas vezes: SEM quem responde "sim" a pergunta dos amigos, que DECIDE (r-a), e com
todos, como sensibilidade. Sai tambem o abandono por versao (ab-a). Imprime so o agregado:
contagens, medias e intervalos. Nunca uma linha, nunca o texto aberto (que o script nem le).
A analise so roda depois do dia 21 da janela, no fuso de Brasilia (h-A: nunca encerrar
olhando o resultado). O veto de distincao (R3) nao e deste script: tools/codigos_visuais.py.

O QUE ELE NAO FAZ (P5). Nao le a pergunta aberta nem a de pronuncia. Nao pondera
desequilibrio entre as versoes (imprime aberturas, conclusoes e abandono de cada uma). Nao
corrige multiplicidade entre H1, H2 e H3: a regra e uma so, e as hipoteses sao relatadas. Com
menos de 2 pessoas nao ha intervalo (reamostrar uma pessoa e ela mesma): sai SEM_DADOS, e a
regra nao escolhe nada.

    python tools/analise_teste_marca.py --inicio AAAA-MM-DD   # a analise, so depois do dia 21
    python tools/analise_teste_marca.py --conferir-cabecalho   # so o cabecalho e as datas
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import io
import os
import subprocess
import sys
from dataclasses import dataclass, field
from typing import Any

import numpy as np
import yaml

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUESTIONARIO = os.path.join(RAIZ, "docs", "marca", "teste-de-marca", "questionario.yaml")

# ---- DECLARADO ANTES DOS DADOS: nao ha opcao de linha de comando para mudar nada disto ----
REAMOSTRAGENS = 10_000
SEMENTE = 20260927
NIVEL = 0.95
DIRECOES = ("E", "C", "D")
BRASILIA = dt.timezone(dt.timedelta(hours=-3))   # America/Sao_Paulo: UTC-3 desde 2019


def ler_questionario(path: str = QUESTIONARIO) -> dict[str, Any]:
    with open(path, encoding="utf-8") as f:
        q: dict[str, Any] = yaml.safe_load(f)
    return q


Q = ler_questionario()
ORDENS: dict[int, tuple[str, ...]] = {int(v): tuple(o) for v, o in Q["ordens"]["versoes"].items()}
ESCALAS = tuple(e["id"] for e in Q["telas"]["escalas"])
N_TELAS = int(Q["telas"]["quantidade"])
JANELA_DIAS = int(Q["janela"]["dias"])


@dataclass
class Resposta:
    versao: int
    amigo: bool
    # notas[(direcao, "base" | "rota")][escala] = 1..7
    notas: dict[tuple[str, str], dict[str, int]] = field(default_factory=dict)


# ---------------------------------------------------------------- leitura ----------------

def colunas_esperadas(q: dict[str, Any] = Q) -> list[str]:
    """As colunas do contrato da exportacao, na ordem (questionario.yaml -> exportacao)."""
    t = q["telas"]
    ids = [t["lembranca"]["id"]] + [e["id"] for e in t["escalas"]]
    x = q["exportacao"]
    return (list(x["colunas_fixas"])
            + [f"t{k}_{i}" for k in range(1, t["quantidade"] + 1) for i in ids]
            + list(x["colunas_finais"]))


def conferir_cabecalho(cabecalho: list[str]) -> list[str]:
    """As diferencas entre o cabecalho e o contrato (lista vazia = cabecalho bom)."""
    esperado = colunas_esperadas()
    if cabecalho == esperado:
        return []
    faltam = [c for c in esperado if c not in cabecalho]
    sobram = [c for c in cabecalho if c not in esperado]
    return [f"falta {c}" for c in faltam] + [f"sobra {c}" for c in sobram] + (
        [] if faltam or sobram else ["colunas fora da ordem do contrato"])


def _dentro_do_git_sem_ignorar(path: str) -> bool:
    """True se o arquivo esta dentro do repositorio E o git NAO o ignora (resposta real
    nunca entra no git). Fora do repositorio, ou sem git, devolve False."""
    alvo = os.path.abspath(path)
    if not alvo.startswith(RAIZ + os.sep):
        return False
    r = subprocess.run(["git", "-C", RAIZ, "check-ignore", "-q", alvo],
                       capture_output=True, check=False)
    return r.returncode == 1


def _dia(texto: str) -> dt.date:
    """O contrato grava so o dia, AAAA-MM-DD, no fuso de Brasilia (sem hora)."""
    try:
        return dt.date.fromisoformat(texto.strip())
    except ValueError:
        raise SystemExit(f"data fora do contrato (AAAA-MM-DD): {texto!r}") from None


def janela(inicio: dt.date) -> tuple[dt.date, dt.date]:
    """h-A: do dia do primeiro convite ao 21o dia, inclusive (Brasilia)."""
    return inicio, inicio + dt.timedelta(days=JANELA_DIAS - 1)


def ler(path: str, inicio: dt.date | None) -> tuple[list[Resposta], dict[str, Any]]:
    if _dentro_do_git_sem_ignorar(path):
        raise SystemExit(f"{path} esta dentro do repositorio e o git nao o ignora: resposta "
                         "real nunca entra no git. Use data/teste-marca/.")
    cont: dict[str, Any] = {"aberturas": 0, "abandonos": 0, "sem_consentimento": 0,
                            "fora_do_filtro": 0, "fora_da_janela": 0, "validas": 0,
                            "aberturas_por_versao": {v: 0 for v in ORDENS},
                            "abandonos_por_versao": {v: 0 for v in ORDENS}}
    out: list[Resposta] = []
    with io.open(path, encoding="utf-8-sig", newline="") as f:
        rd = csv.reader(f, delimiter=Q["exportacao"]["separador"])
        cab = next(rd, [])
        erro = conferir_cabecalho(cab)
        if erro:
            raise SystemExit(f"{path}: cabecalho fora do contrato: {erro}")
        idx = {c: i for i, c in enumerate(cab)}
        ini, fim = janela(inicio) if inicio else (None, None)
        for linha in rd:
            if not linha:
                continue
            versao = int(linha[idx["versao"]])
            if versao not in ORDENS:
                raise SystemExit(f"versao {versao} fora das {len(ORDENS)} do contrato")
            cont["aberturas"] += 1
            cont["aberturas_por_versao"][versao] += 1
            if not linha[idx["concluida_em"]].strip():
                cont["abandonos"] += 1                 # ab-a: so a versao e o dia ficaram
                cont["abandonos_por_versao"][versao] += 1
                continue
            if linha[idx["consentimento"]].strip() != "sim":
                cont["sem_consentimento"] += 1
                continue
            if linha[idx["filtro"]].strip() != "sim":
                cont["fora_do_filtro"] += 1
                continue
            if ini is not None and fim is not None:
                if not (ini <= _dia(linha[idx["concluida_em"]]) <= fim):
                    cont["fora_da_janela"] += 1       # guardada no CSV, fora da analise
                    continue
            r = Resposta(versao=versao, amigo=linha[idx["amigo"]].strip() == "sim")
            ordem = ORDENS[versao]
            for k in range(1, N_TELAS + 1):
                direcao = ordem[(k - 1) % len(ordem)]
                versao_estimulo = "base" if k <= len(ordem) else "rota"
                r.notas[(direcao, versao_estimulo)] = {
                    e: int(linha[idx[f"t{k}_{e}"]]) for e in ESCALAS}
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
        return {"H1": "SEM_DADOS", "H2": "SEM_DADOS", "H3": "SEM_DADOS",
                "H4": "fora do teste (s-a, P-156)"}
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
                         for e in ESCALAS}
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
        "validas_por_versao": por_versao,
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


def imprimir(rel: dict[str, Any], contagens: dict[str, Any]) -> None:
    print("ANALISE DO TESTE DE MARCA -- so agregado (P-162)")
    print(f"declarado: {_fmt(rel['declarado'])}")
    print(f"aberturas e descartes: {_fmt(contagens)}")
    print(f"validas: {rel['n_total']} (n); conhecem quem criou o app: {rel['n_amigos']}")
    print(f"validas por versao (g-B): {_fmt(rel['validas_por_versao'])}")
    for chave in ("sem_amigos_DECIDE", "com_todos_SENSIBILIDADE"):
        print(f"\n== {chave} (n={rel[chave]['n']})")
        print(f"regra: {_fmt(rel[chave]['regra'])}")
        for h, v in rel[chave]["hipoteses"].items():
            print(f"{h}: {_fmt(v)}")
        for k, v in rel[chave]["descritivas"].items():
            print(f"medias {k}: {_fmt(v)}")


def hoje_em_brasilia() -> dt.date:
    return dt.datetime.now(BRASILIA).date()


def main(argv: list[str] | None = None, hoje: dt.date | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--arquivo", default=os.path.join(RAIZ, Q["exportacao"]["arquivo"]))
    ap.add_argument("--inicio", help="dia do primeiro convite (AAAA-MM-DD), do commit das datas")
    ap.add_argument("--conferir-cabecalho", action="store_true")
    a = ap.parse_args(argv)
    if not os.path.isfile(a.arquivo):
        print(f"sem exportacao em {a.arquivo}")
        return 1
    if a.conferir_cabecalho:
        with io.open(a.arquivo, encoding="utf-8-sig", newline="") as f:
            rd = csv.reader(f, delimiter=Q["exportacao"]["separador"])
            erro = conferir_cabecalho(next(rd, []))
            ix = colunas_esperadas().index
            dias = [_dia(c) for linha in rd if linha
                    for c in (linha[ix("aberta_em")], linha[ix("concluida_em")]) if c.strip()]
        print(f"cabecalho: {'ok' if not erro else erro}; datas lidas: {len(dias)}")
        return 1 if erro else 0
    if not a.inicio:
        print("--inicio e obrigatorio: sem a data do primeiro convite nao ha janela (h-A)")
        return 2
    inicio = dt.date.fromisoformat(a.inicio)
    ini, fim = janela(inicio)
    # h-A: "nunca encerrar olhando o resultado". Antes do fim da janela nao ha analise, so
    # --conferir-cabecalho, que nao calcula nada. Regra que depende de lembrar nao e regra (P7).
    if (hoje or hoje_em_brasilia()) <= fim:
        print(f"a janela so fecha no fim de {fim} (Brasilia): antes disso nao ha analise (h-A)")
        return 3
    respostas, cont = ler(a.arquivo, inicio)
    print(f"janela (h-A, Brasilia): {ini} a {fim}, inclusive")
    imprimir(analisar(respostas), cont)
    return 0


if __name__ == "__main__":
    sys.exit(main())
