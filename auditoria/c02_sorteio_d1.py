#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""O sorteio do D1 (secao 3.1 do pre-registro do C-02): 30 posicoes, sem abrir documento.

POR QUE (P-115, passo 6 da secao 9; N-D1c: o sorteio e empurrado ANTES de qualquer documento).
O universo e o da secao 3.1: todo evento do silver fixado cujo tipo e exatamente
`JRS CAP PROPRIO`, com data ex de 01/01/2016 a 31/12/2020 e valor > 0; um par (ticker, data
ex) conta uma vez; ordem canonica (data ex, ticker, valor) crescente; permutacao de
`numpy.random.default_rng(20260927)`. O ticker e o do `ajustar.casar`, sobre a PRESENCA do
COTAHIST de 2016-2020 (a mesma da contagem; nenhum preco, volume ou quantidade e lido).

DECISOES QUE O TEXTO NAO TOMAVA (declaradas aqui, antes de ver o resultado):
  - par (ticker, data ex) com mais de um `valor`: conta uma vez, pelo MENOR valor (a ordem
    canonica poe esse primeiro); a saida diz quantos pares tem mais de um valor;
  - data ex: a do silver rederivada pelo calendario da janela 2016-2020, como na corrida.

O QUE NAO FAZ (P5): nao procura documento nenhum; so ordena. O `valor` da B3 e dado do
provento, nao preco de mercado.

  py -3.11 auditoria/c02_sorteio_d1.py <silver.csv> [--cotahist data/bronze/b3/cotahist]
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import os
import sys
from typing import Iterable, Sequence

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(os.path.dirname(AQUI), "fase0"))
import ajustar  # noqa: E402
import c02_contar_n as N  # noqa: E402

SEMENTE = 20260927
POSICOES = 30
ANOS = range(2016, 2021)
JANELA = (dt.date(2016, 1, 1), dt.date(2020, 12, 31))
COLUNAS = N.LIDAS_SILVER + ("valor",)


def ler_silver(caminho: str) -> Iterable[dict[str, str]]:
    with open(caminho, encoding="utf-8", newline="") as f:
        r = csv.reader(f)
        cab = next(r)
        idx = [cab.index(c) for c in COLUNAS]
        for row in r:
            yield {c: row[i] for c, i in zip(COLUNAS, idx)}


def universo(casados: Iterable[dict[str, str]]) -> tuple[list[tuple[dt.date, str, str]], int]:
    """([(data ex, ticker, valor)] na ordem canonica, pares com mais de um valor)."""
    por_par: dict[tuple[dt.date, str], list[str]] = {}
    for r in casados:
        if r["tipo"] != N.JCP or r["data_ex_status"] != N.DERIVADA or not r["data_ex"]:
            continue
        d = dt.date.fromisoformat(r["data_ex"])
        try:
            v = float(r["valor"])
        except ValueError:
            continue
        if JANELA[0] <= d <= JANELA[1] and v > 0:
            por_par.setdefault((d, r["_ticker"]), []).append(r["valor"])
    multi = sum(1 for vs in por_par.values() if len({float(x) for x in vs}) > 1)
    linhas = sorted((d, tk, min(vs, key=float)) for (d, tk), vs in por_par.items())
    return sorted(linhas, key=lambda t: (t[0], t[1], float(t[2]))), multi


def sortear(linhas: Sequence[tuple[dt.date, str, str]], semente: int = SEMENTE,
            posicoes: int = POSICOES) -> list[tuple[int, int, dt.date, str, str]]:
    """[(posicao, indice na ordem canonica, data ex, ticker, valor)] das primeiras `posicoes`."""
    perm = np.random.default_rng(semente).permutation(len(linhas))
    return [(k + 1, int(i), *linhas[int(i)]) for k, i in enumerate(perm[:posicoes])]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    ap.add_argument("silver")
    ap.add_argument("--cotahist", default=os.path.join("data", "bronze", "b3", "cotahist"))
    a = ap.parse_args(argv)
    with open(a.silver, "rb") as f:
        print(f"silver {os.path.basename(a.silver)} sha256 {hashlib.sha256(f.read()).hexdigest()}")
    cot = N.ler_cotahist(a.cotahist, ANOS)
    datas = {d for d in cot.datas if d.year in ANOS}
    cobertura = (min(datas), max(datas))
    dias = {tk: sorted(d for d in ds if d.year in ANOS) for tk, ds in cot.dias.items()}
    dias = {tk: ds for tk, ds in dias.items() if ds}
    papeis = {tk: ajustar.Papel(tk, (cot.especi[tk][ds[0]].split() or [""])[0],
                                cot.isin[tk][ds[0]], "") for tk, ds in dias.items()}
    pres = {tk: dict.fromkeys(ds, 1) for tk, ds in dias.items()}
    redev, _ = ajustar.rederivar_data_ex([dict(e) for e in ler_silver(a.silver)], datas, cobertura)
    casados, _ = ajustar.casar(redev, papeis, pres)
    linhas, multi = universo(casados)
    print(f"universo: {len(linhas)} pares (ticker, data ex) JCP 2016-2020 com valor > 0; "
          f"{multi} par(es) com mais de um valor (fica o menor)")
    print(f"permutacao: numpy.random.default_rng({SEMENTE}).permutation({len(linhas)}), "
          f"primeiras {POSICOES}")
    print("pos  indice  data_ex     ticker   valor_B3")
    for k, i, d, tk, v in sortear(linhas):
        print(f"{k:3d}  {i:6d}  {d}  {tk:<8} {v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
