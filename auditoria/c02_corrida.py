#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A corrida do C-02 em 2016-2020: os criterios da secao 4 do pre-registro, e so eles.

POR QUE (P-115, docs/auditoria/C02-CRITERIO-V2-PREREGISTRO.md, secao 3.1 passo 3). O D1 deu
PASSA (docs/fontes/jcp-amostra-2016-2020.md) e a secao 9 escolheu a janela 2016-2020. Este
script aplica a secao 4 como esta escrita, com a emenda E-K (secao 4.4), e a secao 5 (K6).
Nenhum limiar nasce aqui: cada constante abaixo cita a linha do pre-registro de onde veio.

O QUE MEDE, por criterio:
  K2/K3 (janela)  razao queda/provento so-JCP e so-dividendo, dias LIMPOS com mercado, IC 95%
                  do bootstrap POR PREGAO (semente 20260926), julgada pela E-K1;
  K1 (ano)        controle RELATIVO max |r_aj / r_bruto - 1| <= 1e-12 (secao 4.2);
  K5 (ano)        evento grande de quantidade com excesso em +-15%, no maximo 1 fora por ano;
  completude      1/3 dos degraus de provento fora dos dias limpos; 1/3 dos eventos grandes de
                  quantidade sem mercado do dia (E-K3);
  K6 (secao 5)    M1, M2, M3 e M5 no mesmo dado, M4 sobre a amostra transcrita do D1.

TRAVA (P7): o script RECUSA ler preco da quarentena (2013-2020, secao 9) se o commit atual nao
estiver no origin, ou se a arvore tiver mudanca que o commit nao carrega. "Empurrado antes de
rodar" passa a ser condicao do codigo, nao de memoria.

O QUE NAO MEDE (P5): a razao de cada ano sai so como descricao (secao 4.1). O H-FISCAL
(secao 6) e previsao e nao julga nada; nao esta aqui. A saida nao traz preco: so contagens,
razoes, ICs e, nos eventos de quantidade fora do K5, ticker, data, fator e excesso.

  py -3.11 auditoria/c02_corrida.py <silver.csv> [--cotahist data/bronze/b3/cotahist]
"""
from __future__ import annotations

import argparse
import bisect
import collections
import dataclasses
import datetime as dt
import hashlib
import json
import os
import platform
import re
import subprocess
import sys
from decimal import Decimal
from typing import Any, Callable, Iterable, Mapping, Sequence

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ_REPO = os.path.dirname(AQUI)
for _p in (os.path.join(RAIZ_REPO, "fase0"), os.path.join(RAIZ_REPO, "alocacao"), AQUI):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import ajustar  # noqa: E402  -- a medicao e uma so: a da corrida e a da suite
import calendario  # noqa: E402  -- o unico leitor de COTAHIST
import jcp  # noqa: E402  -- a aliquota do JCP por data (M4)
import motor  # noqa: E402  -- custos.yaml so por val() (P1)
import p88_block_bootstrap as p88  # noqa: E402  -- `indices(rng, n, L=1)`, secao 3.1

# ───────────────────────────────────────────── as constantes, com a linha de onde vieram

JANELA = (2016, 2020)                 # secao 9: nenhuma candidata atendeu
QUARENTENA = (2013, 2020)             # secao 9: nenhum retorno de dia ex desses anos antes
SEMENTE = 20260926                    # secao 3.1, "Intervalo: bootstrap por pregao"
REAMOSTRAS = 2000                     # idem
PERCENTIS = (2.5, 97.5)               # E-K4 (2): numpy.percentile, interpolacao linear
DDOF = 1                              # E-K4 (3)
N_MIN_PONTOS = 30                     # secao 4.1, ultima linha do veredito
N_MIN_PREGOES = 20                    # idem
MERCADO_MINIMO = 20                   # secao 3.1, `mercado_do_dia`
JCP = "JRS CAP PROPRIO"
DIVIDENDO = "DIVIDENDO"


@dataclasses.dataclass(frozen=True)
class Faixa:
    rotulo: str
    inferior: float
    superior: float
    sigma_max: float


FAIXAS = {                            # secao 4.1, tabela K2/K3
    "K2": Faixa(JCP, 0.85, 1.15, 0.0416),
    "K3": Faixa(DIVIDENDO, 0.85, 1.35, 0.0463),
}
K1_TOLERANCIA = 1e-12                 # secao 4.2, K1 (relativo)
K5_FATOR = (0.67, 1.5)                # secao 4.2, K5: fator <= 0,67 ou >= 1,5 (E-K4 (5))
K5_EXCESSO = 0.15                     # +-15%
K5_FORA_POR_ANO = 1                   # "no maximo 1 evento por ano fora"
K5_MIN_JANELA = 10                    # "K5 exige ao menos 10 eventos grandes somados"
COMPLETUDE = 1 / 3                    # secao 4.2, completude
K6_M2_ANOS = 3                        # secao 5: M2 "REPROVA em K5 em >= 3 dos 5 anos"
FONTE_D1 = os.path.join(RAIZ_REPO, "docs", "fontes", "jcp-amostra-2016-2020.md")
SAIDA_PADRAO = os.path.join(RAIZ_REPO, "docs", "auditoria", "C02-JANELA-2016-2020-resultado.json")

PASSA, REPROVA, NAO_CONFIRMADO, NAO_APLICA = "PASSA", "REPROVA", "NAO_CONFIRMADO", "NAO_APLICA"
NAO_CONFIRMADA, SEM_PODER = "NAO_CONFIRMADA", "CRITERIO_SEM_PODER"
LIMPO, QUANTIDADE = "LIMPO", "QUANTIDADE"
FORA_DO_LIMPO = ("CONTAMINADO", "MARCA_SEM_EVENTO")   # E-K3: o que mede o acervo


# ─────────────────────────────────────────────────────────────── a trava (P7)

class NaoPublicado(RuntimeError):
    """O commit atual nao esta no origin, ou a arvore difere dele."""


def _git(repo: str, *args: str) -> str:
    r = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True)
    if r.returncode != 0:
        raise NaoPublicado("git %s falhou: %s" % (" ".join(args), r.stderr.strip()))
    return r.stdout


def conferir_publicado(repo: str = RAIZ_REPO) -> str:
    """O sha do HEAD, se ele estiver em algum ramo do origin e a arvore for a dele.

    Tres recusas, cada uma com o motivo: arquivo rastreado mudado (o codigo que roda nao e o
    do commit); .py/.yaml novo fora do git (um modulo novo seria importado sem estar em
    commit nenhum); e HEAD fora de todo `origin/*` (o commit nunca foi empurrado). Os refs
    `origin/*` so mudam por fetch ou push, entao HEAD contido num deles foi publicado."""
    head = _git(repo, "rev-parse", "HEAD").strip()
    mudados = [ln for ln in _git(repo, "status", "--porcelain", "--untracked-files=no").splitlines()
               if ln.strip()]
    if mudados:
        raise NaoPublicado("a arvore tem mudanca que o commit %s nao carrega: %s"
                           % (head[:12], "; ".join(mudados[:5])))
    novos = [ln[3:] for ln in _git(repo, "status", "--porcelain").splitlines()
             if ln.startswith("??") and ln.rstrip().endswith((".py", ".yaml", ".yml"))]
    if novos:
        raise NaoPublicado("arquivo de codigo fora do git: %s" % "; ".join(novos[:5]))
    remotos = [ln.strip() for ln in _git(repo, "branch", "-r", "--contains", head).splitlines()
               if ln.strip()]
    if not remotos:
        raise NaoPublicado("o commit %s nao esta em nenhum ramo do origin: empurre antes de "
                           "rodar (secao 3.1, passo 3)" % head[:12])
    return head


def toca_a_quarentena(anos: Iterable[int]) -> bool:
    return any(QUARENTENA[0] <= a <= QUARENTENA[1] for a in anos)


# ───────────────────────────────────────────── o bootstrap por pregao e o veredito (K2/K3)

Ponto = tuple[dt.date, float, float]      # (pregao da medida, excesso, rendimento)


def razao(pontos: Sequence[Ponto]) -> float:
    """`ajustar.queda_por_provento` sobre os pares (excesso, rendimento): a formula e uma so.
    Ordenados, pelo mesmo motivo do bootstrap."""
    return float(ajustar.queda_por_provento([(e, y) for _d, e, y in sorted(pontos)])[1])


def bootstrap_por_pregao(pontos: Sequence[Ponto], semente: int = SEMENTE,
                         reamostras: int = REAMOSTRAS) -> dict[str, Any]:
    """{n, pregoes, razao, lo, hi, sigma}. A unidade sorteada e o PREGAO (secao 3.1): todos os
    pontos de uma data entram ou saem juntos. Sortear `k` vezes uma data e somar `k` vezes os
    seus Sum(e*y) e Sum(y^2) -- o mesmo que concatenar os pontos dela `k` vezes. Gerador NOVO
    por chamada (E-K4 (1)): o resultado nao depende da ordem dos testes. Os pontos sao
    ORDENADOS antes de somar: em ponto flutuante a soma depende da ordem (na 16a casa), e o
    resultado nao pode depender da ordem das linhas do silver."""
    pontos = sorted(pontos)
    datas = sorted({d for d, _e, _y in pontos})
    pos = {d: i for i, d in enumerate(datas)}
    sey = np.zeros(len(datas))
    syy = np.zeros(len(datas))
    for d, e, y in pontos:
        sey[pos[d]] += e * y
        syy[pos[d]] += y * y
    fora: dict[str, Any] = dict(n=len(pontos), pregoes=len(datas),
                                razao=razao(pontos) if pontos else float("nan"),
                                lo=float("nan"), hi=float("nan"), sigma=float("nan"))
    if len(datas) < 2:
        return fora
    rng = np.random.default_rng(semente)
    rs = np.empty(reamostras)
    for i in range(reamostras):
        c = np.bincount(p88.indices(rng, len(datas), 1), minlength=len(datas))
        rs[i] = 1.0 - float(c @ sey) / float(c @ syy)
    lo, hi = np.percentile(rs, PERCENTIS)
    fora.update(lo=float(lo), hi=float(hi), sigma=float(np.std(rs, ddof=DDOF)))
    return fora


def veredito_razao(b: Mapping[str, Any], f: Faixa) -> str:
    """A ordem da E-K1 (secao 4.4). Um IC que nao toca a faixa reprova com qualquer sigma: o
    sigma_max so decide quando o IC cruza uma borda."""
    if b["n"] < N_MIN_PONTOS or b["pregoes"] < N_MIN_PREGOES:
        return NAO_CONFIRMADO
    lo, hi = b["lo"], b["hi"]
    if lo >= f.inferior and hi <= f.superior:           # E-K4 (4): bordas fechadas
        return PASSA
    if hi < f.inferior or lo > f.superior:              # E-K1: disjunto
        return REPROVA
    return REPROVA if b["sigma"] <= f.sigma_max else NAO_CONFIRMADO


# ──────────────────────────────────────────────────────────── as linhas medidas

@dataclasses.dataclass(frozen=True)
class Linha:
    g: Any                    # o Degrau VERDADEIRO (ajustar.Degrau)
    classe: str               # do silver nao mutado (secao 5; E-K2)
    dia: dt.date              # o pregao em que o retorno e medido
    excesso: float | None     # retorno ajustado no `dia` menos o mercado do dia; None sem mercado
    y: float                  # 1 - fator do degrau verdadeiro


def sem_fator(m: Any) -> set[tuple[str, dt.date]]:
    """O mesmo conjunto de `ajustar.residuo_de_mercado`: evento com data ex e sem fator."""
    return {(r["_ticker"], ajustar._data(r["data_ex"])) for r in m.casados
            if r["data_ex_status"] == ajustar.DERIVADA and r["fator_status"] != ajustar.CALCULADO}


def mercado(m: Any) -> dict[dt.date, float]:
    return ajustar.mercado_do_dia(m.acervo, m.fat, {r["_ticker"] for r in m.casados},
                                  minimo=MERCADO_MINIMO)


class _Datas:
    """O pregao anterior de cada papel, por bisect: a serie de um papel e a da propria B3."""

    def __init__(self, precos: Mapping[str, Mapping[dt.date, Any]]):
        self.d = {tk: sorted(s) for tk, s in precos.items()}

    def anterior(self, tk: str, dia: dt.date) -> dt.date | None:
        ds = self.d.get(tk, [])
        i = bisect.bisect_left(ds, dia)
        return ds[i - 1] if i > 0 else None


def medidas(m: Any, ajustadas: Mapping[str, Mapping[dt.date, Any]],
            dia_de: Callable[[Any], dt.date | None] | None = None,
            merc: Mapping[dt.date, float] | None = None,
            sf: set[tuple[str, dt.date]] | None = None,
            datas: _Datas | None = None) -> list[Linha]:
    """Uma `Linha` por degrau VERDADEIRO. `ajustadas` pode vir de um ajuste mutado (K6): o
    rendimento, os tipos, a classe e o mercado sao sempre os do silver nao mutado (secao 5).
    `dia_de` diz em que pregao medir; a corrida mede no dia ex, a M1 no dia deslocado (E-K2)."""
    merc = mercado(m) if merc is None else merc
    sf = sem_fator(m) if sf is None else sf
    datas = _Datas(m.acervo.precos) if datas is None else datas
    fora = []
    for g in m.degraus:
        dia = g.data_ex if dia_de is None else dia_de(g)
        if dia is None:
            continue
        ant = datas.anterior(g.ticker, dia)
        aj = ajustadas.get(g.ticker, {})
        if ant is None or dia not in aj or ant not in aj or aj[ant][0] == 0:
            continue
        r = float(aj[dia][0] / aj[ant][0] - 1)
        e = r - merc[dia] if dia in merc else None
        fora.append(Linha(g, ajustar.classe_do_degrau(g, sf), dia, e, float(1 - g.fator)))
    return fora


def pontos(linhas: Iterable[Linha], rotulo: str) -> list[Ponto]:
    """Dias LIMPOS com mercado cujo evento e SO `rotulo` (secao 3.1)."""
    return [(ln.dia, ln.excesso, ln.y) for ln in linhas
            if ln.classe == LIMPO and ln.excesso is not None and ajustar._so(ln.g.tipos, rotulo)]


def k2_k3(linhas: Sequence[Linha]) -> dict[str, dict[str, Any]]:
    fora = {}
    for k, f in FAIXAS.items():
        b = bootstrap_por_pregao(pontos(linhas, f.rotulo))
        fora[k] = dict(b, faixa=[f.inferior, f.superior], sigma_max=f.sigma_max,
                       veredito=veredito_razao(b, f))
    return fora


def razao_por_ano(linhas: Sequence[Linha]) -> dict[int, dict[str, Any]]:
    """Secao 4.1: a razao de cada ano sai SO como descricao; nao julga nada."""
    fora: dict[int, dict[str, Any]] = collections.defaultdict(dict)
    for f in FAIXAS.values():
        por = collections.defaultdict(list)
        for p in pontos(linhas, f.rotulo):
            por[p[0].year].append(p)
        for ano, ps in por.items():
            fora[ano][f.rotulo] = dict(n=len(ps), razao=razao(ps))
    return dict(fora)


# ─────────────────────────────────────────────────────────── os criterios por ano

def k1_por_ano(acervo: Any, ajustadas: Mapping[str, Mapping[dt.date, Any]],
               fat: Mapping[tuple[str, dt.date], Any]) -> dict[int, dict[str, Any]]:
    """{ano: pares, pior, veredito}. Secao 4.2: o RELATIVO, max |r_aj / r_bruto - 1|. O
    `ajustar.controle_por_ano` mede o absoluto; o pre-registro fixou o relativo."""
    por: dict[int, list[Any]] = {}
    for tk, serie in acervo.precos.items():
        dias = sorted(serie)
        aj = ajustadas[tk]
        for d0, d1 in zip(dias, dias[1:]):
            if (tk, d1) in fat:
                continue
            if serie[d0] <= 0 or serie[d1] <= 0 or aj[d0][0] <= 0:
                continue
            r0 = serie[d1] / serie[d0]
            r1 = aj[d1][0] / aj[d0][0]
            p = por.setdefault(d1.year, [0, Decimal(0)])
            p[0] += 1
            p[1] = max(p[1], abs(r1 / r0 - 1))
    return {ano: dict(pares=n, pior=float(pior),
                      veredito=PASSA if pior <= Decimal(K1_TOLERANCIA) else REPROVA)
            for ano, (n, pior) in sorted(por.items())}


def grande(g: Any) -> bool:
    """Evento de quantidade grande (secao 4.2, K5), pelo fator do DEGRAU (E-K4 (5))."""
    return ajustar.e_de_quantidade(g.tipos) and not (K5_FATOR[0] < float(g.fator) < K5_FATOR[1])


def k5_por_ano(linhas: Sequence[Linha]) -> dict[int, dict[str, Any]]:
    """{ano: n, fora, veredito}. Julga o EXCESSO (ajustado - mercado do dia), nao o retorno:
    o crash de marco de 2020 nao pode reprovar um desdobramento certo (secao 4.2)."""
    por: dict[int, list[Linha]] = collections.defaultdict(list)
    for ln in linhas:
        if grande(ln.g) and ln.excesso is not None:
            por[ln.g.data_ex.year].append(ln)
    fora = {}
    for ano in range(JANELA[0], JANELA[1] + 1):
        ls = por.get(ano, [])
        out = [dict(ticker=ln.g.ticker, data=ln.g.data_ex.isoformat(), fator=float(ln.g.fator),
                    excesso=round(float(ln.excesso), 4))
               for ln in ls if ln.excesso is not None and abs(ln.excesso) > K5_EXCESSO]
        v = NAO_APLICA if not ls else (PASSA if len(out) <= K5_FORA_POR_ANO else REPROVA)
        fora[ano] = dict(n=len(ls), fora=out, veredito=v)
    return fora


def k5_janela(por_ano: Mapping[int, Mapping[str, Any]]) -> dict[str, Any]:
    n = sum(v["n"] for v in por_ano.values())
    return dict(n=n, minimo=K5_MIN_JANELA, veredito=PASSA if n >= K5_MIN_JANELA else NAO_CONFIRMADO)


def completude_por_ano(linhas: Sequence[Linha], degraus: Iterable[Any],
                       sf: set[tuple[str, dt.date]],
                       merc: Mapping[dt.date, float]) -> dict[int, dict[str, Any]]:
    """E-K3: o 1/3 de fora dos dias limpos e so sobre os degraus de PROVENTO (CONTAMINADO e
    MARCA_SEM_EVENTO medem o acervo); os de quantidade grandes tem a linha de mercado."""
    prov: dict[int, list[int]] = collections.defaultdict(lambda: [0, 0])
    qtd: dict[int, list[int]] = collections.defaultdict(lambda: [0, 0])
    for g in degraus:
        ano = g.data_ex.year
        if ajustar.e_de_quantidade(g.tipos):
            if grande(g):
                qtd[ano][0] += 1
                qtd[ano][1] += g.data_ex not in merc
            continue
        prov[ano][0] += 1
        prov[ano][1] += ajustar.classe_do_degrau(g, sf) in FORA_DO_LIMPO
    fora = {}
    for ano in range(JANELA[0], JANELA[1] + 1):
        (pn, pf), (qn, qf) = prov[ano], qtd[ano]
        ok = (pn == 0 or pf / pn <= COMPLETUDE) and (qn == 0 or qf / qn <= COMPLETUDE)
        fora[ano] = dict(degraus_provento=pn, fora_do_limpo=pf, grandes_quantidade=qn,
                         sem_mercado=qf, veredito=PASSA if ok else NAO_CONFIRMADO)
    return fora


def anos(k1: Mapping[int, Mapping[str, Any]], k5: Mapping[int, Mapping[str, Any]],
         comp: Mapping[int, Mapping[str, Any]]) -> dict[int, str]:
    """O veredito de cada ano (secao 4.3): REPROVA por K1 ou K5; NAO_CONFIRMADO por
    completude ou por K1 sem par nenhum; PASSA no resto."""
    fora = {}
    for ano in range(JANELA[0], JANELA[1] + 1):
        vs = [k1.get(ano, {}).get("veredito", NAO_CONFIRMADO), k5[ano]["veredito"],
              comp[ano]["veredito"]]
        fora[ano] = (REPROVA if REPROVA in vs else NAO_CONFIRMADO if NAO_CONFIRMADO in vs
                     else PASSA)
    return fora


# ─────────────────────────────────────────────────────────────────── o D1 (e a M4)

@dataclasses.dataclass(frozen=True)
class EventoD1:
    pos: int
    data_ex: dt.date
    ticker: str
    bruto: str                # como impresso no documento, virgula decimal
    liquido: str | None
    aliquota: float | None    # declarada; None = a da lei (E-D1a)
    b3: str
    classe: str               # a gravada na transcricao


_NUM = re.compile(r"\d+,\d+")
_PCT = re.compile(r"(\d+(?:,\d+)?)\s*%")


def ler_d1(caminho: str = FONTE_D1) -> list[EventoD1]:
    """A primeira tabela da transcricao do D1: as 10 posicoes que o veredito julga."""
    fora: list[EventoD1] = []
    dentro = False
    with open(caminho, encoding="utf-8") as f:
        for ln in f:
            if ln.startswith("| pos | data ex | ticker | data com |"):
                dentro = True
                continue
            if not dentro:
                continue
            if not ln.startswith("|"):
                if fora:
                    break
                continue
            c = [x.strip() for x in ln.strip().strip("|").split("|")]
            if not c[0].isdigit():
                continue
            liq = _NUM.search(c[6])
            pct = _PCT.search(c[7])
            fora.append(EventoD1(int(c[0]), dt.date.fromisoformat(c[1]), c[2],
                                 _NUM.search(c[5]).group(0),  # type: ignore[union-attr]
                                 liq.group(0) if liq else None,
                                 float(pct.group(1).replace(",", ".")) / 100 if pct else None,
                                 c[8], c[9].strip("`")))
    return fora


def _dec(txt: str) -> Decimal:
    return Decimal(txt.replace(",", "."))


def _meia_unidade(txt: str) -> Decimal:
    casas = len(txt.split(",")[1]) if "," in txt else len(txt.split(".")[1]) if "." in txt else 0
    return Decimal(5) * Decimal(10) ** -(casas + 1)


def classe_d1(ev: EventoD1, b3: Decimal, C: Any) -> str:
    """Secao 3.1: "igual" e diferenca <= meia unidade da ultima casa impressa. O liquido e o do
    documento ou bruto x (1 - aliquota); sem aliquota declarada, a da lei pela data (E-D1a)."""
    bruto, tol_b = _dec(ev.bruto), _meia_unidade(ev.bruto)
    if ev.liquido is not None:
        liq, tol_l = _dec(ev.liquido), _meia_unidade(ev.liquido)
    else:
        a = ev.aliquota if ev.aliquota is not None else jcp.aliquota_jcp(ev.data_ex, C)[0]
        liq, tol_l = bruto * (1 - Decimal(str(a))), tol_b
    ib, il = abs(b3 - bruto) <= tol_b, abs(b3 - liq) <= tol_l
    return "BRUTO" if ib and not il else "LIQUIDO" if il and not ib else "NENHUM"


def veredito_d1(classes: Sequence[str]) -> str:
    """Secao 3.1: PASSA se as 10 forem BRUTO; REPROVA se alguma for LIQUIDO; senao
    NAO_CONFIRMADO."""
    if "LIQUIDO" in classes:
        return REPROVA
    return PASSA if len(classes) == 10 and all(c == "BRUTO" for c in classes) else NAO_CONFIRMADO


def custos() -> Any:
    C = motor.carregar()
    motor.val(C["tributacao"]["ir_jcp_fonte"], contexto="tributacao.ir_jcp_fonte")  # P1
    return C


def d1(evs: Sequence[EventoD1], C: Any) -> dict[str, Any]:
    cls = [classe_d1(e, _dec(e.b3), C) for e in evs]
    return dict(classes=cls, gravadas=[e.classe for e in evs], veredito=veredito_d1(cls))


def m4(evs: Sequence[EventoD1], C: Any) -> dict[str, Any]:
    """Secao 5, M4: o valor da B3 trocado por `jcp_liquido(bruto, data, C)`. Tem de dar D1
    REPROVA com os 10 LIQUIDO. A data e a ex: 15% em toda a amostra (nenhum evento cai entre
    01/01 e 08/03/2016, onde a aliquota seria 18%)."""
    cls = [classe_d1(e, Decimal(repr(jcp.jcp_liquido(float(_dec(e.bruto)), e.data_ex, C))), C)
           for e in evs]
    ok = veredito_d1(cls) == REPROVA and cls.count("LIQUIDO") == len(evs) == 10
    return dict(classes=cls, veredito=veredito_d1(cls), reprovou=ok)


# ───────────────────────────────────────────────────────────────────── o K6 (secao 5)

def _so_provento(r: Mapping[str, Any]) -> bool:
    return (r["fator_status"] == ajustar.CALCULADO and r["data_ex_status"] == ajustar.DERIVADA
            and not ajustar.e_de_quantidade(r["tipo"]) and r.get("fator") not in (None, ""))


def mutar_valor(casados: Sequence[Mapping[str, Any]], c: Decimal) -> list[dict[str, Any]]:
    """M3 (c = 1000) e M5 (c = 0): o valor do provento vezes c. Com f = (P - v) / P, o fator
    de c*v e 1 - c*(1 - f) -- a mesma `fator_de_provento` sem precisar do preco de vespera.
    So o insumo do ajuste muda; o `y` da estatistica continua o verdadeiro (secao 5)."""
    fora = []
    for r in casados:
        if _so_provento(r):
            f = Decimal(r["fator"])
            r = dict(r, fator=format(1 - c * (1 - f), "f"))
        fora.append(dict(r))
    return fora


def mutar_m1(m: Any, datas: _Datas) -> dict[tuple[str, dt.date], Any]:
    """M1: o fator entra no ultimo dia com direito -- o pregao anterior do papel, a vespera do
    degrau. Dois eventos que caiam no mesmo dia deslocado multiplicam, como em `fatores`."""
    fora: dict[tuple[str, dt.date], Any] = {}
    for (tk, d), (f, tipos) in m.fat.items():
        ant = datas.anterior(tk, d)
        if ant is None:
            continue
        f0, t0 = fora.get((tk, ant), (Decimal(1), []))
        fora[(tk, ant)] = (f0 * f, t0 + list(tipos))
    return fora


def mutar_m2(fat: Mapping[tuple[str, dt.date], Any]) -> dict[tuple[str, dt.date], Any]:
    """M2: 1/f em todo evento."""
    return {k: (1 / f, tipos) for k, (f, tipos) in fat.items() if f != 0}


def k6(m: Any, evs_d1: Sequence[EventoD1], C: Any,
       julgar: Callable[[Sequence[Linha]], dict[str, dict[str, Any]]] = k2_k3) -> dict[str, Any]:
    """Secao 5: cada mutacao altera so a entrada do ajuste; y, tipos, classe e mercado vem do
    silver nao mutado. K6 passa se cada uma produzir a reprovacao da sua linha; um
    NAO_CONFIRMADO conta como falha."""
    merc, sf, datas = mercado(m), sem_fator(m), _Datas(m.acervo.precos)

    def linhas(fat_mut: Any, dia_de: Callable[[Any], dt.date | None] | None = None) -> list[Linha]:
        return medidas(m, ajustar.ajustar_tudo(m.acervo, fat_mut), dia_de, merc, sf, datas)

    def dupla(ls: Sequence[Linha]) -> dict[str, Any]:
        j = julgar(ls)
        return dict(K2=j["K2"]["veredito"], K3=j["K3"]["veredito"],
                    razao_K2=j["K2"]["razao"], razao_K3=j["K3"]["razao"],
                    reprovou=j["K2"]["veredito"] == REPROVA and j["K3"]["veredito"] == REPROVA)

    out: dict[str, Any] = {}
    out["M1"] = dupla(linhas(mutar_m1(m, datas), lambda g: g.data_vespera))   # E-K2
    k5m = k5_por_ano(linhas(mutar_m2(m.fat)))
    nr = sum(1 for v in k5m.values() if v["veredito"] == REPROVA)
    out["M2"] = dict(anos_reprovados=nr, reprovou=nr >= K6_M2_ANOS)
    out["M3"] = dupla(linhas(ajustar.fatores(mutar_valor(m.casados, Decimal(1000)))))
    out["M4"] = m4(evs_d1, C)
    out["M5"] = dupla(linhas(ajustar.fatores(mutar_valor(m.casados, Decimal(0)))))
    out["veredito"] = PASSA if all(out[k]["reprovou"] for k in ("M1", "M2", "M3", "M4", "M5")) \
        else REPROVA
    return out


# ──────────────────────────────────────────────────────────────── a janela (secao 4.3)

def veredito_janela(d1_v: str, anos_v: Mapping[int, str], k2: str, k3: str, k5j: str,
                    k6_v: str) -> str:
    if d1_v != PASSA:
        raise ValueError("secao 4.3: sem D1 = PASSA a corrida nao roda (D1 = %s)" % d1_v)
    if k6_v != PASSA:
        return SEM_PODER
    if REPROVA in anos_v.values() or REPROVA in (k2, k3):
        return REPROVA
    if NAO_CONFIRMADO in list(anos_v.values()) + [k2, k3, k5j]:
        return NAO_CONFIRMADA
    return PASSA


def julgar(m: Any, evs_d1: Sequence[EventoD1], C: Any) -> dict[str, Any]:
    """A secao 4 inteira sobre uma medicao (a real, ou a sintetica dos testes)."""
    dd = d1(evs_d1, C)
    if dd["veredito"] != PASSA:
        raise ValueError("secao 4.3: D1 = %s na transcricao; a corrida nao roda" % dd["veredito"])
    merc, sf = mercado(m), sem_fator(m)
    ls = medidas(m, m.ajustadas, None, merc, sf)
    kk = k2_k3(ls)
    k1 = k1_por_ano(m.acervo, m.ajustadas, m.fat)
    k5 = k5_por_ano(ls)
    k5j = k5_janela(k5)
    comp = completude_por_ano(ls, m.degraus, sf, merc)
    av = anos(k1, k5, comp)
    kk6 = k6(m, evs_d1, C)
    return dict(D1=dd, K2=kk["K2"], K3=kk["K3"], K1=k1, K5=k5, K5_janela=k5j,
                completude=comp, anos=av, razao_por_ano_descritiva=razao_por_ano(ls),
                K6=kk6, veredito=veredito_janela(dd["veredito"], av, kk["K2"]["veredito"],
                                                 kk["K3"]["veredito"], k5j["veredito"],
                                                 kk6["veredito"]))


# ─────────────────────────────────────────────────────────────── os insumos (sha256)

def sha256(caminho: str) -> str:
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def insumos(silver: str, raiz: str, anos_lidos: Iterable[int]) -> dict[str, Any]:
    """O sha256 de cada arquivo lido, gravado junto do resultado: o silver e cada COTAHIST que
    `calendario.arquivos` escolhe -- a mesma descoberta que a medicao usa."""
    cot = calendario.arquivos(raiz, set(anos_lidos))
    return dict(
        silver=dict(arquivo=os.path.basename(silver), sha256=sha256(silver),
                    bytes=os.path.getsize(silver)),
        cotahist=[dict(arquivo=os.path.basename(p), sha256=sha256(p), bytes=os.path.getsize(p))
                  for _k, p in sorted(cot.items())])


# ──────────────────────────────────────────────────────────────────────────── main

def _json(o: Any) -> Any:
    if isinstance(o, (dt.date, Decimal)):
        return str(o)
    if isinstance(o, dict):
        return {str(k): _json(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_json(v) for v in o]
    if isinstance(o, float) and o != o:
        return None
    return o


def main(argv: list[str] | None = None, medir: Callable[..., Any] = ajustar.medir,
         publicado: Callable[[], str] = conferir_publicado) -> int:
    ap = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    ap.add_argument("silver")
    ap.add_argument("--cotahist", default=ajustar.RAIZ_PADRAO)
    ap.add_argument("--saida", default=SAIDA_PADRAO)
    a = ap.parse_args(argv)
    lidos = ajustar.janela("%d-%d" % JANELA)
    commit = None
    if toca_a_quarentena(lidos):
        try:
            commit = publicado()
        except NaoPublicado as ex:
            print("RECUSADO (P7): %s. Nenhum preco foi lido." % ex, file=sys.stderr)
            return 3
    C = custos()
    evs = ler_d1()
    ins = insumos(a.silver, a.cotahist, lidos)
    m = medir(a.cotahist, a.silver, lidos)
    r = julgar(m, evs, C)
    r = dict(janela=list(JANELA), commit=commit, insumos=ins,
             ambiente=dict(python=platform.python_version(), numpy=np.__version__),
             semente=SEMENTE, reamostras=REAMOSTRAS, resultado=r)
    with open(a.saida, "w", encoding="utf-8") as f:
        json.dump(_json(r), f, ensure_ascii=True, indent=1, sort_keys=True)
        f.write("\n")
    res = r["resultado"]
    print("silver %s sha256 %s" % (ins["silver"]["arquivo"], ins["silver"]["sha256"]))
    for c in ins["cotahist"]:
        print("cotahist %s sha256 %s" % (c["arquivo"], c["sha256"]))
    for k in ("K2", "K3"):
        b = res[k]
        print("%s n=%d pregoes=%d razao=%.4f IC95 [%.4f ; %.4f] sigma=%.4f -> %s"
              % (k, b["n"], b["pregoes"], b["razao"], b["lo"], b["hi"], b["sigma"], b["veredito"]))
    print("anos: %s" % ", ".join("%d %s" % kv for kv in sorted(res["anos"].items())))
    print("K6: %s" % res["K6"]["veredito"])
    print("RESULTADO DA JANELA 2016-2020: %s (gravado em %s)" % (res["veredito"], a.saida))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
