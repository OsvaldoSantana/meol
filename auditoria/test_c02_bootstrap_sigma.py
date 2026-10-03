# -*- coding: utf-8 -*-
"""O bootstrap do sigma e deterministico, usa a semente declarada e acha o sigma analitico."""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c02_bootstrap_sigma as B  # noqa: E402
import c02_contar_n as N  # noqa: E402


def _pontos(n=300, razao=0.95, ruido=0.002):
    rng = random.Random(1)
    out = []
    for _ in range(n):
        y = rng.uniform(0.005, 0.03)
        out.append(((razao - 1) * y + rng.gauss(0, ruido), y))
    return out


def test_semente_e_reamostras_declaradas():
    assert B.SEMENTE == 20260921 and B.REAMOSTRAS == 2000


def test_mesma_semente_mesmo_resultado_e_outra_semente_outro():
    p = _pontos()
    assert B.bootstrap(p) == B.bootstrap(p)
    assert B.bootstrap(p)["sigma"] != B.bootstrap(p, semente=1)["sigma"]


def test_sigma_bate_com_o_erro_padrao_analitico():
    # razao = 1 - sum(e y)/sum(y^2): erro padrao ~ sd(resid)/sqrt(sum y^2)
    rng = random.Random(7)
    pts = []
    for _ in range(800):
        y = rng.uniform(0.005, 0.03)
        pts.append((-0.05 * y + rng.gauss(0, 0.01), y))
    esperado = 0.01 / math.sqrt(sum(y * y for _e, y in pts))
    b = B.bootstrap(pts)
    assert abs(b["sigma"] - esperado) / esperado < 0.1
    assert b["lo"] < b["razao"] < b["hi"] and b["n"] == 800


def test_o_sigma_do_contador_e_o_do_bootstrap_documentado():
    assert N.SIGMA_2021_2025 == 0.0482
