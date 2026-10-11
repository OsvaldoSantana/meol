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


# ── 10/10/2026: acrescentar sem regravar as linhas que a maquina nao tem como refazer ───────────

def test_chaves_novas_sao_as_entradas_que_o_csv_ainda_nao_tem():
    """A sessao na nuvem de 10/10 nao tem as capturas das 51 linhas de 04/10 (fora do git, de
    terceiros). Regravar tudo as perderia; acrescentar so toca o que falta."""
    existentes = [{"categoria_sorteada": "assessor", "ordem_no_sorteio": "1"},
                  {"categoria_sorteada": "assessor", "ordem_no_sorteio": "2"}]
    leituras = {"assessor": {1: {}, 2: {}, 3: {}}, "bancos": {2: {}, 1: {}}}
    assert L.chaves_novas(existentes, leituras) == [("assessor", 3), ("bancos", 1), ("bancos", 2)]
    assert L.chaves_novas([], {}) == []


def test_classificada_sem_captura_e_erro_nomeado_e_nao_nameerror(tmp_path, monkeypatch):
    """Antes, `linha` chegava a `a = m["390"]` com `m` nunca definido: um NameError que nao diz
    qual marca nem onde faltou a captura. A captura e a procedencia: sem ela, nao ha linha."""
    monkeypatch.setattr(L, "CAPTURAS", str(tmp_path))
    leitura = {"marca": "X", "situacao": "classificada", "data": "2026-10-10"}
    with pytest.raises(ValueError, match="bancos-07.*sem captura"):
        L.linha("bancos", 7, leitura, {"cnpj": "1"}, {})


def test_marca_pulada_sem_captura_continua_valendo(tmp_path, monkeypatch):
    """Pulada por site que nao abre nao tem captura, e a linha existe com o motivo (R3, sec. 3)."""
    monkeypatch.setattr(L, "CAPTURAS", str(tmp_path))
    leitura = {"marca": "X", "situacao": "pulada", "motivo": "site_inacessivel: DNS",
               "data": "2026-10-10", "url": "https://x.com.br/"}
    r = L.linha("bancos", 7, leitura, {"cnpj": "00000001"}, {})
    assert (r["situacao"], r["url"], r["categoria_sorteada"]) == ("pulada", "https://x.com.br/",
                                                                   "bancos")


def test_botao_vazado_de_app_le_a_cor_do_texto_e_nao_o_fundo():
    """10/10/2026, BMG: 'VER SIMULACAO' e laranja sobre branco e nao tem caixa nem borda. O
    caminho do botao cheio (mediana dos pixels sem o texto) devolveria o BRANCO do fundo e o
    matiz sairia neutro; o livro manda a cor do texto."""
    fundo, laranja, borda = (255, 255, 255), (242, 106, 27), (240, 150, 100)
    px = [fundo] * 600 + [laranja] * 50 + [borda] * 20 + [(250, 245, 240)] * 30
    assert L.cor_do_texto_por_pixels(px) == "#f26a1b"
    assert L.cor_do_texto_por_pixels([fundo] * 10) == "#ffffff"
    # o cheio continua como era: o fundo, sem os pixels do texto
    assert L.preenchimento_por_pixels(px, "#f26a1b") == "#ffffff"


def test_sem_chaves_tira_so_as_pedidas_e_recusa_chave_inexistente():
    """10/10/2026: o Banco Cedula foi lido como banco_tradicional e relido como fora_do_livro
    (uma agencia no BCB, sem app) antes do commit; `--acrescentar` sozinho nao troca linha ja
    gravada, e deixar as duas na tabela do veto contaria a marca duas vezes."""
    linhas = [{"categoria_sorteada": "bancos", "ordem_no_sorteio": "16"},
              {"categoria_sorteada": "bancos", "ordem_no_sorteio": "20"},
              {"categoria_sorteada": "assessor", "ordem_no_sorteio": "16"}]
    resto = L.sem_chaves(linhas, ["bancos:16"])
    assert [(r["categoria_sorteada"], r["ordem_no_sorteio"]) for r in resto] == [
        ("bancos", "20"), ("assessor", "16")]
    with pytest.raises(ValueError, match="bancos.*17"):
        L.sem_chaves(linhas, ["bancos:17"])

def test_app_classificado_nao_exige_o_site_aberto(tmp_path, monkeypatch):
    """10/10/2026, BV: o site recusou todas as variantes, mas o app da loja tem captura. Na
    unidade app a prova e a captura da loja (app_390.json); exigir o medidas.json do site
    derrubaria uma marca que o livro manda classificar pelo app (ae-a)."""
    monkeypatch.setattr(L, "CAPTURAS", str(tmp_path))
    pasta = tmp_path / "bancos-87"
    pasta.mkdir()
    leitura = {"marca": "X", "situacao": "classificada", "unidade": "app", "data": "2026-10-10"}
    # sem a captura da loja, o erro e nomeado e diz qual arquivo falta
    with pytest.raises(ValueError, match=r"bancos-87.*app_390\.json"):
        L.linha("bancos", 87, leitura, {"cnpj": "1"}, {})
    # na unidade site, a prova continua sendo o medidas.json
    with pytest.raises(ValueError, match=r"bancos-87.*medidas\.json"):
        L.linha("bancos", 87, {**leitura, "unidade": "site"}, {"cnpj": "1"}, {})


def test_cor_do_texto_ignora_o_suavizado_quando_o_miolo_da_letra_e_pouco():
    """10/10/2026, Credishop: 'Ver todas' vermelho em uma caixa de 63x18 px com ruido. A moda dos
    pixels fora do fundo era o rosa palido do suavizado (#f9d5d9, matiz neutro); o texto, que o
    livro manda ler, e o vermelho do miolo, que tem poucos pixels e distancia maior do fundo."""
    fundo, rosa, vermelho = (255, 255, 255), (249, 213, 217), (214, 43, 43)
    suave = (246, 211, 209)
    px = [fundo] * 700 + [rosa] * 120 + [suave] * 60 + [vermelho] * 25 + [(200, 60, 60)] * 10
    cor = L.cor_do_texto_por_pixels(px)
    r, g, b = (int(cor[i:i + 2], 16) for i in (1, 3, 5))
    assert r > 190 and g < 80 and b < 80, cor
