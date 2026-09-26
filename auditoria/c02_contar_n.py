#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Conta o n do JCP por janela sem ler preco, calibra em 2021-2025 e aplica a regra.

POR QUE (P-115, secao 9 do `docs/auditoria/C02-CRITERIO-V2-PREREGISTRO.md`, decisao n-c de
26/09/2026). O K2 do JCP provavelmente sai sem poder em 2016-2020, e a janela pode crescer
para tras (2013-2020 no maximo). O tamanho so pode ser escolhido pelo n, nunca pelo preco.
E o n tem de estar na MESMA unidade dos 819 de 2021-2025: a primeira versao desta regra
comparava a contagem do silver com os 819 sem conferir isso.

A UNIDADE (a de `ajustar.medir` -> `residuo_de_mercado` -> "so JCP", dias LIMPOS): o degrau
(papel, data ex) com negocio no COTAHIST no dia ex e num pregao anterior DO PAPEL, que ganhou
fator, sem evento de quantidade, sem marca de bonificacao/grupamento no ESPECI, sem evento
sem fator no mesmo dia, num dia com mercado (>= 20 papeis), e cujos tipos sao so JCP.
O casamento evento -> papel e a data ex sao os do proprio `ajustar.py` (`casar`,
`rederivar_data_ex`): uma regra so (N-01). Onde o `ajustar` olha preco, aqui entra PRESENCA:
  - "tem preco no dia e na vespera" -> tem registro a vista em lote padrao nos dois dias;
  - "o SEM_PRECO ganha preco de vespera do COTAHIST" -> o papel negociou antes da data ex;
  - A-13 sem `valor`: a copia de um provento ja CALCULADO e o mesmo (papel, dia, tipo).

O QUE LE, e so isto:
  - do COTAHIST, pelas posicoes do `docs/schemas/cotahist-v02.yaml` (P-105/P-130), os campos
    de `CAMPOS_COTAHIST` -- DATA, CODBDI, CODNEG, TPMERC, ESPECI, CODISI. Nenhum campo de
    preco, volume, quantidade ou fator de cotacao; o teste envenena todas essas posicoes;
  - do silver, as colunas de `LIDAS_SILVER`: identidade, tipo, as duas datas e os dois
    status. Nem `valor`, nem `preco_vespera`, nem `fator`.

A CALIBRACAO e condicao, nao ajuste: rodado sobre 2021-2025, o script tem de dar 819. Outro
valor quer dizer que a presenca nao reproduz a unidade, e a regra NAO escolhe janela: o
script para, mostra a diferenca e sai 2.

O QUE NAO MEDE (P5): os casos em que o `ajustar` descarta por VALOR do preco (preco zero,
fechamento ilegivel, dois proventos de mesmo tipo e dia com valores diferentes). A calibracao
e quem diz se eles pesam.

A SAIDA e so contagem (P-136).

  py -3.11 auditoria/c02_contar_n.py <silver.csv> [--cotahist data/bronze/b3/cotahist]
"""
from __future__ import annotations

import argparse
import collections
import csv
import dataclasses
import datetime as dt
import hashlib
import math
import os
import sys
from typing import Iterable, Iterator, Mapping

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(AQUI), "fase0"))
import ajustar  # noqa: E402  -- casar, rederivar_data_ex, marca_de_ex: a regra e uma so
import calendario  # noqa: E402  -- o unico leitor de COTAHIST e o leiaute como dado
import refinar  # noqa: E402

CAMPOS_COTAHIST: tuple[str, ...] = ("DATA", "CODBDI", "CODNEG", "TPMERC", "ESPECI", "CODISI")
LIDAS_SILVER = ("cod", "type_stock", "isin", "tipo", "ultimo_dia_com_direito", "data_ex",
                "data_ex_status", "fator_status")
JCP = "JRS CAP PROPRIO"
DIVIDENDO = "DIVIDENDO"
QUANTIDADE = frozenset(refinar.TIPOS_DE_QUANTIDADE)
CALCULADO, SEM_PRECO, DERIVADA = refinar.CALCULADO, refinar.SEM_PRECO, refinar.DERIVADA
MERCADO_MINIMO = 20          # o `minimo` de `ajustar.mercado_do_dia`

# a regra da secao 9: os numeros sao os da secao 4 (2021-2025 e sigma_max do K2)
SIGMA_2021_2025 = 0.0472
CALIBRACAO_N = 819
CALIBRACAO_ANOS = (2021, 2025)
SIGMA_MAX_K2 = 0.0416
FOLGA = 0.8
N_MIN = math.ceil(CALIBRACAO_N * (SIGMA_2021_2025 / (FOLGA * SIGMA_MAX_K2)) ** 2)
CANDIDATAS = ((2016, 2020), (2015, 2020), (2014, 2020), (2013, 2020))
PADRAO = CANDIDATAS[0]


class SilverIncompleto(ValueError):
    pass


class CalibracaoFalhou(RuntimeError):
    pass


@dataclasses.dataclass
class Presenca:
    """O que o COTAHIST diz sem preco: os pregoes, e em que dias cada papel negociou."""
    datas: set[dt.date]
    dias: dict[str, set[dt.date]]
    especi: dict[str, dict[dt.date, str]]
    isin: dict[str, dict[dt.date, str]]
    primeiro: dict[str, tuple[dt.date, str, str]]


def _campo(raw: str, nome: str) -> str:
    a, b = calendario.pos(nome)
    return raw[a:b]


def presenca(linhas: Iterable[str]) -> Presenca:
    """Linhas de cotacao (TIPREG 01) -> `Presenca`. So fatia os campos de
    `CAMPOS_COTAHIST`, e o filtro de mercado e o do `ajustar.cotacoes`."""
    p = Presenca(set(), collections.defaultdict(set), collections.defaultdict(dict),
                 collections.defaultdict(dict), {})
    for raw in linhas:
        v = {c: _campo(raw, c) for c in CAMPOS_COTAHIST}
        t = v["DATA"]
        try:
            d = dt.date(int(t[:4]), int(t[4:6]), int(t[6:8]))
        except ValueError:
            continue
        p.datas.add(d)                     # o calendario conta todo registro (pregoes)
        if v["CODBDI"] != ajustar.CODBDI_LOTE_PADRAO or v["TPMERC"] != ajustar.TPMERC_A_VISTA:
            continue
        tk, esp, isin = v["CODNEG"].strip(), v["ESPECI"].strip(), v["CODISI"].strip()
        p.dias[tk].add(d)
        p.especi[tk][d] = esp
        p.isin[tk][d] = isin
        if tk not in p.primeiro:
            p.primeiro[tk] = (d, esp.split()[0] if esp else "", isin)
    p.dias, p.especi, p.isin = dict(p.dias), dict(p.especi), dict(p.isin)
    return p


def ler_cotahist(raiz: str, anos: Iterable[int]) -> Presenca:
    anos = set(anos)

    def linhas() -> Iterator[str]:
        for _base, caminho in sorted(calendario.arquivos(raiz, anos).items()):
            yield from calendario.registros(caminho)
    return presenca(linhas())


def ler_silver(caminho: str) -> Iterator[dict[str, str]]:
    """Cada linha do silver projetada em `LIDAS_SILVER`, e so nelas."""
    with open(caminho, encoding="utf-8", newline="") as f:
        r = csv.reader(f)
        cab = next(r)
        falta = [c for c in LIDAS_SILVER if c not in cab]
        if falta:
            raise SilverIncompleto(f"{caminho}: faltam as colunas {falta}")
        idx = [cab.index(c) for c in LIDAS_SILVER]
        for row in r:
            yield {c: row[i] for c, i in zip(LIDAS_SILVER, idx)}


def medir_n(evs: Iterable[Mapping[str, str]], cot: Presenca,
            anos: Iterable[int]) -> dict[int, dict[str, int]]:
    """{ano: {so_jcp, so_div, degraus}} da janela `anos`, na unidade dos 819."""
    anos = set(anos)
    datas = {d for d in cot.datas if d.year in anos}
    cobertura = (min(datas), max(datas)) if datas else (None, None)
    dias = {tk: sorted(d for d in ds if d.year in anos) for tk, ds in cot.dias.items()}
    dias = {tk: ds for tk, ds in dias.items() if ds}
    # o Papel do `ajustar.cotacoes`: a primeira ocorrencia DENTRO da janela
    papeis = {tk: ajustar.Papel(tk, (cot.especi[tk][ds[0]].split() or [""])[0],
                                cot.isin[tk][ds[0]], "") for tk, ds in dias.items()}
    pres = {tk: dict.fromkeys(ds, 1) for tk, ds in dias.items()}
    redev, _ = ajustar.rederivar_data_ex([dict(e) for e in evs], datas, cobertura)
    casados, _ = ajustar.casar(redev, papeis, pres)

    def dia(r):
        return ajustar._data(r["data_ex"])

    # completar_preco_de_vespera, por presenca
    contados = {(r["_ticker"], r["data_ex"], r["tipo"]) for r in casados
                if r["fator_status"] == CALCULADO and r["data_ex_status"] == DERIVADA}
    for r in casados:
        if r["fator_status"] != SEM_PRECO or r["data_ex_status"] != DERIVADA:
            continue
        k = (r["_ticker"], r["data_ex"], r["tipo"])
        d = dia(r)
        if k in contados or d is None:
            continue
        if any(x < d for x in dias.get(r["_ticker"], ())):
            r["fator_status"] = CALCULADO
            contados.add(k)
    fat: dict[tuple[str, dt.date], list[str]] = {}
    for r in casados:
        d = dia(r)
        if r["fator_status"] == CALCULADO and r["data_ex_status"] == DERIVADA and d:
            fat.setdefault((r["_ticker"], d), []).append(r["tipo"])
    sem_fator = {(r["_ticker"], dia(r)) for r in casados
                 if r["data_ex_status"] == DERIVADA and r["fator_status"] != CALCULADO}
    # mercado_do_dia: papeis com negocio no dia e no anterior, sem evento no dia
    por_dia: collections.Counter[dt.date] = collections.Counter()
    for tk in {r["_ticker"] for r in casados}:
        ds = dias.get(tk, [])
        for d1 in ds[1:]:
            if (tk, d1) not in fat:
                por_dia[d1] += 1
    mercado = {d for d, n in por_dia.items() if n >= MERCADO_MINIMO}
    out: dict[int, dict[str, int]] = {}
    for (tk, d), tipos in sorted(fat.items()):
        ds = dias.get(tk, [])
        if d not in pres.get(tk, {}) or not ds or ds[0] >= d:
            continue                                   # sem negocio no dia ou na vespera
        c = out.setdefault(d.year, dict(so_jcp=0, so_div=0, degraus=0))
        c["degraus"] += 1
        if d not in mercado or QUANTIDADE & set(tipos) or (tk, d) in sem_fator:
            continue
        mk = ajustar.marca_de_ex(cot.especi[tk].get(d, ""))
        if "B" in mk[1:] or "G" in mk[1:]:
            continue
        c["so_jcp"] += int(set(tipos) == {JCP})
        c["so_div"] += int(set(tipos) == {DIVIDENDO})
    return out


def n_da_janela(evs: list[dict[str, str]], cot: Presenca, ini: int, fim: int) -> int:
    return sum(c["so_jcp"] for c in medir_n(evs, cot, range(ini, fim + 1)).values())


def calibrar(n: int) -> None:
    if n != CALIBRACAO_N:
        raise CalibracaoFalhou(
            f"calibracao {CALIBRACAO_ANOS[0]}-{CALIBRACAO_ANOS[1]}: contou {n}, a unidade "
            f"dos {CALIBRACAO_N} pede {CALIBRACAO_N}; diferenca {n - CALIBRACAO_N:+d}. "
            f"A regra NAO escolhe janela (secao 9).")


def janela(ns: Mapping[tuple[int, int], int]) -> dict[str, object]:
    """A menor candidata com n >= N_MIN; sem nenhuma, 2016-2020 com `atende=False`."""
    for ini, fim in CANDIDATAS:
        if ns[(ini, fim)] >= N_MIN:
            return dict(ini=ini, fim=fim, n=ns[(ini, fim)], atende=True)
    return dict(ini=PADRAO[0], fim=PADRAO[1], n=ns[PADRAO], atende=False)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    ap.add_argument("silver")
    ap.add_argument("--cotahist", default=os.path.join("data", "bronze", "b3", "cotahist"))
    a = ap.parse_args(argv)
    with open(a.silver, "rb") as f:
        print(f"silver {os.path.basename(a.silver)} sha256 {hashlib.sha256(f.read()).hexdigest()}")
    evs = list(ler_silver(a.silver))
    cot = ler_cotahist(a.cotahist, range(CANDIDATAS[-1][0], CALIBRACAO_ANOS[1] + 1))
    n_cal = n_da_janela(evs, cot, *CALIBRACAO_ANOS)
    try:
        calibrar(n_cal)
    except CalibracaoFalhou as e:
        print(f"RESUMO PARADO: {e}")
        return 2
    print(f"calibracao {CALIBRACAO_ANOS[0]}-{CALIBRACAO_ANOS[1]}: {n_cal} (confere)")
    ns = {w: n_da_janela(evs, cot, *w) for w in CANDIDATAS}
    for (ini, fim), n in ns.items():
        print(f"  {ini}-{fim}: n_JCP {n}")
    j = janela(ns)
    print(f"RESUMO regra da secao 9: n_min {N_MIN}; janela {j['ini']}-{j['fim']}, n {j['n']}, "
          + ("atende" if j["atende"] else
             "NENHUMA atende: NAO_CONFIRMADO provavel no K2, declarado"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
