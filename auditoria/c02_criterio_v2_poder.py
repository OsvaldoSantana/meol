# -*- coding: utf-8 -*-
"""P-115: probabilidade de o IC 95% NAO caber na faixa de equivalencia (aproximacao normal).

Da o sigma_max de cada faixa -- o maior desvio com que um ajuste perfeito ainda reprova em
no maximo 10% das vezes -- e a tabela da secao 4.1 de
`docs/auditoria/C02-CRITERIO-V2-PREREGISTRO.md`. `test_c02_criterio_v2_poder.py` prende os
numeros que o texto cita: se o texto e o calculo divergirem, a suite reprova.

ALCANCE (P5): aproximacao normal, IC simetrico `est +- 1,96 sigma`. O bootstrap real pode ser
assimetrico; o sigma_max e regra declarada, nao garantia exata.
"""
from __future__ import annotations

from math import erf, sqrt

Z = 1.959963985

# O sigma iid de 2021-2025, tirado do IC 95% publicado em C02-JANELA-2021-2025.md.
S21 = {"jcp": (1.044 - 0.859) / 2 / Z, "div": (1.240 - 1.092) / 2 / Z}

# (nome, razoes verdadeiras de um ajuste perfeito, faixa, sigma de 2021-2025)
FAIXAS = [("JCP [0.90,1.10]", [1.0], 0.90, 1.10, S21["jcp"]),
          ("JCP [0.85,1.15]", [1.0], 0.85, 1.15, S21["jcp"]),
          ("DIV [0.85,1.35]", [1.0, 1.176], 0.85, 1.35, S21["div"])]


def phi(x: float) -> float:
    return 0.5 * (1 + erf(x / sqrt(2)))


def nao_cabe(k: float, s: float, lo: float, hi: float) -> float:
    """P(o IC `est +- Z s` nao caber em [lo, hi]) com a razao verdadeira `k`."""
    a, b = lo + Z * s, hi - Z * s
    return 1.0 if a > b else 1 - (phi((b - k) / s) - phi((a - k) / s))


def sigma_max(ks: list[float], lo: float, hi: float, alvo: float = 0.10) -> float:
    """O maior sigma com que nenhuma razao de `ks` deixa de caber em mais de `alvo`."""
    baixo, alto = 1e-6, 1.0
    for _ in range(200):
        m = (baixo + alto) / 2
        if max(nao_cabe(k, m, lo, hi) for k in ks) <= alvo:
            baixo = m
        else:
            alto = m
    return baixo


def main() -> None:
    for nome, ks, lo, hi, s in FAIXAS:
        sm = sigma_max(ks, lo, hi)
        print(nome, "sigma_max=%.4f" % sm,
              "| nao cabe @s21:", ["%.4f" % nao_cabe(k, s, lo, hi) for k in ks],
              "| @sigma_max:", ["%.4f" % nao_cabe(k, sm, lo, hi) for k in ks])


if __name__ == "__main__":
    main()
