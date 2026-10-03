# -*- coding: utf-8 -*-
"""Os numeros que o criterio v2 da P-115 cita saem do calculo, nao da memoria.

A secao 4.1 de `docs/auditoria/C02-CRITERIO-V2-PREREGISTRO.md` escreve sigma_max e as
probabilidades de reprovar um ajuste perfeito. Se alguem mudar a faixa no texto sem
recalcular, ou o calculo sem o texto, um dos dois lados reprova aqui."""
from __future__ import annotations

import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import c02_criterio_v2_poder as C  # noqa: E402

TEXTO = os.path.join(os.path.dirname(AQUI), "docs", "auditoria",
                     "C02-CRITERIO-V2-PREREGISTRO.md")


def test_sigma_max_das_duas_faixas_escolhidas():
    assert round(C.sigma_max([1.0], 0.85, 1.15), 4) == 0.0416
    assert round(C.sigma_max([1.0, 1.176], 0.85, 1.35), 4) == 0.0463


def test_a_faixa_estreita_nao_caberia_com_o_sigma_de_2021_2025():
    """A razao de ter recusado [0,90; 1,10]: 87,4% de nao caber com um ajuste perfeito."""
    assert round(C.nao_cabe(1.0, C.S21["jcp"], 0.90, 1.10), 3) == 0.874


def test_o_texto_cita_os_mesmos_numeros():
    with open(TEXTO, encoding="utf-8") as f:
        s = f.read()
    for n in ("0,0416", "0,0463", "87,4%"):
        assert n in s, f"o criterio nao cita {n}; texto e calculo divergiram"


def test_mutacao_faixa_mais_larga_muda_o_sigma():
    """A guarda falha quando deveria: outra faixa da outro sigma_max."""
    assert round(C.sigma_max([1.0], 0.80, 1.20), 4) != 0.0416
