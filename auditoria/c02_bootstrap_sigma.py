#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""O sigma do JCP em 2021-2025: bootstrap da razao queda/provento, com semente e n declarados.

POR QUE (P-115, secao 9, "O resultado: n = 807", 03/10/2026). O 0,0472 de setembro saiu de um
bootstrap cujo script nao esta no repositorio. O 0,0482 que a regra usa hoje sai DESTE script,
e reproduz-se com o comando abaixo (P1: o numero tem procedencia; 5-B.14: sai com o n).

O QUE MEDE: sobre os degraus so-JCP em dia LIMPO de `ajustar.residuo_de_mercado`, reamostra
os pares (excesso, rendimento) com reposicao, recalcula a razao de `ajustar.queda_por_provento`
e devolve o IC 95% pelos percentis 2,5 e 97,5; sigma = (hi - lo) / 2 / 1,959963985 -- a
convencao de setembro (`c02_criterio_v2_poder.S21`).

O QUE NAO MEDE (P5): o gerador de numeros aleatorios de setembro e desconhecido; com
`random.Random(20260921)` a razao e o sigma misturam a mudanca do silver com a do sorteio.
Le preco: so de 2021-2025, fora da quarentena. Nao aceita outra janela.

  py -3.11 auditoria/c02_bootstrap_sigma.py <silver.csv> [--cotahist data/bronze/b3/cotahist]
"""
from __future__ import annotations

import argparse
import hashlib
import os
import random
import sys
from typing import Sequence

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(AQUI), "fase0"))
import ajustar  # noqa: E402

SEMENTE = 20260921
REAMOSTRAS = 2000
Z95 = 1.959963985
JANELA = "2021-2025"


def bootstrap(pontos: Sequence[tuple[float, float]], semente: int = SEMENTE,
              reamostras: int = REAMOSTRAS) -> dict[str, float]:
    """{n, razao, lo, hi, sigma} de `pontos` = [(excesso, rendimento)]."""
    n = len(pontos)
    rng = random.Random(semente)
    razoes = sorted(
        ajustar.queda_por_provento([pontos[rng.randrange(n)] for _ in range(n)])[1]
        for _ in range(reamostras))
    lo = razoes[round(0.025 * reamostras) - 1]
    hi = razoes[round(0.975 * reamostras) - 1]
    return dict(n=n, razao=ajustar.queda_por_provento(pontos)[1], lo=lo, hi=hi,
                sigma=(hi - lo) / 2 / Z95)


def pontos_do_rotulo(residuo, rotulo: str) -> list[tuple[float, float]]:
    return [(e, y) for g, c, e, y in residuo
            if c == "LIMPO" and ajustar._so(g.tipos, rotulo)]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    ap.add_argument("silver")
    ap.add_argument("--cotahist", default=os.path.join("data", "bronze", "b3", "cotahist"))
    a = ap.parse_args(argv)
    with open(a.silver, "rb") as f:
        print(f"silver {os.path.basename(a.silver)} sha256 {hashlib.sha256(f.read()).hexdigest()}")
    m = ajustar.medir(a.cotahist, a.silver, ajustar.janela(JANELA))
    res = ajustar.residuo_de_mercado(m)
    for rotulo in ("JRS CAP PROPRIO", "DIVIDENDO"):
        b = bootstrap(pontos_do_rotulo(res, rotulo))
        print(f"{rotulo}: n={b['n']:.0f} razao={b['razao']:.4f} IC95 [{b['lo']:.4f} ; "
              f"{b['hi']:.4f}] sigma={b['sigma']:.4f} (semente {SEMENTE}, {REAMOSTRAS} reamostras)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
