# -*- coding: utf-8 -*-
"""As funcoes puras da captura da R3 (P-170): nada aqui toca rede, navegador nem imagem."""
from __future__ import annotations

import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import r3_capturar as C  # noqa: E402


def test_css_para_hex():
    assert C.css_para_hex("rgb(255, 102, 0)") == "#ff6600"
    assert C.css_para_hex("rgba(0, 0, 0, 0)") is None           # transparente: nao e cor
    assert C.css_para_hex("rgba(10, 20, 30, 0.5)") == "#0a141e"
    assert C.css_para_hex("rgb(1 2 3 / 0%)") is None
    assert C.css_para_hex("transparent") is None


def test_raio_em_px_e_porcentagem_pela_altura():
    assert C.raio_px("4px", 44) == 4
    assert C.raio_px("50%", 44) == 22                          # pilula de 44 px
    assert C.raio_px("9999px", 44) == 9999
    assert C.raio_px("8px 8px", 40) == 8                       # so o primeiro valor
    assert C.raio_px("0", 40) == 0


def test_moda_e_a_cor_de_maior_area():
    px = [(255, 255, 255)] * 6 + [(0, 0, 0)] * 4
    assert C.moda(px) == ("#ffffff", 0.6)
    with pytest.raises(ValueError):
        C.moda([])


def test_moda_cromatica_ignora_cinza_e_conta_sobre_o_total():
    px = [(255, 255, 255)] * 6 + [(255, 102, 0)] * 3 + [(0, 0, 255)] * 1
    cor, fr = C.moda_cromatica(px) or ("", 0.0)
    assert cor == "#ff6600" and fr == pytest.approx(0.3)
    assert C.moda_cromatica([(10, 10, 10)] * 5) is None


def test_moda_cromatica_segue_o_livro_v3_perto_do_branco():
    """ag-b (04/10): o branco azulado da 1a captura (#f2f5f6) era 'cromatico' pela saturacao HSL
    sozinha. A captura le a regra do livro, entao ele agora e neutro, e a cor de verdade ganha."""
    px = [(242, 245, 246)] * 6 + [(30, 58, 138)] * 2
    assert C.moda_cromatica(px) == ("#1e3a8a", 0.25)
    assert C.moda_cromatica([(242, 245, 246)] * 3) is None


def test_rgb_hex():
    assert C.rgb_hex((0, 128, 255)) == "#0080ff"


def test_em_alta_troca_so_o_tamanho():
    u = "https://is1-ssl.mzstatic.com/image/thumb/a/b/x_1242x2208.png/392x696bb.png"
    assert C.em_alta(u) == "https://is1-ssl.mzstatic.com/image/thumb/a/b/x_1242x2208.png/1242x0w.png"
    assert C.em_alta("https://x/y.png") == "https://x/y.png"


def test_o_chromium_da_maquina_so_entra_quando_a_variavel_existe():
    """10/10/2026: o Playwright 1.63.0 espera o Chromium 1243 e a nuvem tem o 1194, o das 51
    primeiras visitas. Sem `R3_CHROMIUM` o lancamento e o padrao do Playwright (nada muda para
    quem instalou o navegador); com ela, o executavel vai no lancamento."""
    assert C.chromium_do_ambiente({}) is None
    assert C.chromium_do_ambiente({"R3_CHROMIUM": "  "}) is None
    assert C.chromium_do_ambiente({"R3_CHROMIUM": " /opt/chromium "}) == "/opt/chromium"
