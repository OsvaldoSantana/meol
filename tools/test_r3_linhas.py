# -*- coding: utf-8 -*-
"""As partes puras de tools/r3_linhas.py (P-170): a cor do botao principal e o botao lido."""
from __future__ import annotations

import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import r3_linhas as L  # noqa: E402


def _b(**kw):
    base = {"texto": "Fale conosco", "fundo": "rgba(0, 0, 0, 0)", "cor": "rgb(255, 255, 255)",
            "borda_cor": "rgb(0, 0, 0)", "borda_px": "0px", "borda_estilo": "none"}
    base.update(kw)
    return base


def test_cheio_usa_o_fundo_computado():
    assert L.destaque_do_botao(_b(fundo="rgb(255, 102, 0)"), "cheio") == "#ff6600"


def test_cheio_por_degrade_usa_a_mediana_sem_o_texto():
    """Portfel, 04/10: a moda da caixa de um degrade e o texto branco; a mediana sem ele e a cor."""
    px = [(255, 255, 255)] * 50 + [(20, 90, 210), (22, 94, 212), (24, 98, 214)]
    assert L.destaque_do_botao(_b(), "cheio", px) == "#165ed4"


def test_cheio_sem_fundo_e_sem_pixels_recusa():
    with pytest.raises(ValueError):
        L.destaque_do_botao(_b(), "cheio")


def test_vazado_usa_a_borda_e_sem_borda_o_texto():
    com = _b(borda_cor="rgb(31, 166, 122)", borda_px="1px", borda_estilo="solid")
    assert L.destaque_do_botao(com, "vazado") == "#1fa67a"
    assert L.destaque_do_botao(_b(cor="rgb(10, 20, 30)"), "vazado") == "#0a141e"


def test_achar_botao_pelo_comeco_do_texto():
    bs = [_b(texto="Menu"), _b(texto="FALE COM UM CONSULTOR CERTIFIC")]
    assert L.achar_botao(bs, "FALE COM UM CONSULTOR")["texto"].startswith("FALE")
    with pytest.raises(ValueError):
        L.achar_botao(bs, "Abra sua conta")
