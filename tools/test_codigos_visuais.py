# -*- coding: utf-8 -*-
"""O livro de codigos visuais do veto (P-162): fechado, sem buraco, e as direcoes classificadas
antes da R3 pela mesma regra que vai classificar as marcas."""
from __future__ import annotations

import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import codigos_visuais as V  # noqa: E402

LIVRO = V.ler_livro()

# A classificacao gravada no pre-registro final (27/09/2026, antes da R3).
ESPERADO = {
    "E": {"fundo": "claro", "matiz": "laranja", "familia_do_titulo": "serifa", "raio": "reto",
          "densidade": "media", "botao": "vazado"},
    "C": {"fundo": "claro", "matiz": "rosa", "familia_do_titulo": "sem_serifa",
          "raio": "grande", "densidade": "media", "botao": "cheio"},
    "D": {"fundo": "escuro", "matiz": "laranja", "familia_do_titulo": "serifa", "raio": "reto",
          "densidade": "media", "botao": "cheio"},
}


def test_classificacao_de_e_c_d_e_a_gravada_no_preregistro():
    assert V.classificar_direcoes(LIVRO) == ESPERADO


def test_titulo_e_o_texto_de_maior_corpo_nao_o_token_chamado_titulo():
    """Na E o token `fontes.titulo` e sem serifa (rotulos em caixa alta), mas o h1 da decisao
    herda a serifa do corpo: e o que a pessoa ve como titulo."""
    assert V.medidas_da_direcao("E", LIVRO)["familia_generica"] == "serif"


def test_as_faixas_de_matiz_cobrem_o_circulo_sem_buraco_nem_sobreposicao():
    faixas = LIVRO["variaveis"]["matiz"]["faixas"]
    for grau in range(360):
        g = grau + 0.5
        n = sum((f["de"] <= g < f["ate"]) if f["de"] < f["ate"] else (g >= f["de"] or g < f["ate"])
                for f in faixas)
        assert n == 1, grau


@pytest.mark.parametrize("hexa,faixa", [
    ("#FF0000", "vermelho"), ("#FF4000", "laranja"), ("#FFFF00", "amarelo"),
    ("#00FF00", "verde"), ("#0000FF", "azul"), ("#FF00FF", "magenta"),
    ("#808080", "neutro"), ("#1B1A17", "neutro"),
    # ag-b (livro v3): quase-branco e quase-preto sao neutros, por mais "saturados" que o HSL diga
    ("#FFFEFE", "neutro"), ("#ECE6E4", "neutro"), ("#F2F5F6", "neutro"), ("#0F1116", "neutro"),
    ("#021226", "neutro"), ("#F5F3EE", "neutro"), ("#1E3A8A", "celeste"),
])
def test_faixas_nos_pontos_conhecidos(hexa, faixa):
    assert V.faixa_de_matiz(hexa, LIVRO) == faixa


def test_fronteiras_do_fundo_e_do_raio():
    base = {"destaque_hex": "#FF0000", "familia_generica": "serif", "densidade_blocos": 1,
            "botao": "cheio"}
    # 0.179 e o ponto de contraste igual com preto e branco; #757575 (0.1779) fica abaixo,
    # #767676 (0.1812) acima
    assert V.classificar({**base, "fundo_hex": "#757575", "raio_px": 2}, LIVRO)["fundo"] == "escuro"
    assert V.classificar({**base, "fundo_hex": "#767676", "raio_px": 2}, LIVRO)["fundo"] == "claro"
    raios = {r: V.classificar({**base, "fundo_hex": "#FFFFFF", "raio_px": r}, LIVRO)["raio"]
             for r in (0, 2, 3, 8, 9, 999)}
    assert raios == {0: "reto", 2: "reto", 3: "pequeno", 8: "pequeno", 9: "grande",
                     999: "grande"}


def test_valor_fora_do_livro_reprova():
    with pytest.raises(ValueError):
        V.classificar({"fundo_hex": "#FFFFFF", "destaque_hex": "#FF0000",
                       "familia_generica": "serif", "raio_px": 0, "densidade_blocos": 1,
                       "botao": "gradiente"}, LIVRO)


def _marca(fundo, matiz, familia, raio, densidade="media", botao="cheio"):
    return {"fundo": fundo, "matiz": matiz, "familia_do_titulo": familia, "raio": raio,
            "densidade": densidade, "botao": botao}


def test_codigo_dominante_exige_metade_e_cinco_marcas():
    roxo = _marca("claro", "violeta", "sem_serifa", "grande")
    outra = _marca("escuro", "azul", "sem_serifa", "pequeno")
    assert V.codigos_dominantes([roxo] * 4, LIVRO) == []                  # n = 4 < 5
    dom = V.codigos_dominantes([roxo] * 3 + [outra] * 2, LIVRO)           # 3 de 5
    assert dom == [("claro", "violeta", "sem_serifa", "grande")]
    assert V.codigos_dominantes([roxo] * 2 + [outra] * 2 + [_marca("claro", "verde", "serifa",
                                                                   "reto")], LIVRO) == []


def test_imitar_e_partilhar_as_quatro_centrais():
    c = ESPERADO["C"]
    cat = [_marca("claro", "rosa", "sem_serifa", "grande", densidade=d, botao=b)
           for d, b in (("alta", "vazado"), ("baixa", "cheio"), ("alta", "cheio"))]
    cat += [_marca("escuro", "azul", "serifa", "reto")] * 2
    dom = V.codigos_dominantes(cat, LIVRO)
    assert V.imita(c, dom) and not V.imita(ESPERADO["E"], dom) and not V.imita(ESPERADO["D"], dom)


def test_mutacao_dominante_sobre_seis_variaveis_perde_o_veto(monkeypatch):
    """aa-a: o dominante e contado sobre as QUATRO centrais. Contado sobre as seis, a categoria
    acima (densidade e botao variando) deixa de ter codigo dominante e o veto nao dispara."""
    cat = [_marca("claro", "rosa", "sem_serifa", "grande", densidade=d, botao=b)
           for d, b in (("alta", "vazado"), ("baixa", "cheio"), ("alta", "cheio"))]
    cat += [_marca("escuro", "azul", "serifa", "reto")] * 2
    assert V.imita(ESPERADO["C"], V.codigos_dominantes(cat, LIVRO))
    monkeypatch.setattr(V, "CENTRAIS", tuple(LIVRO["variaveis"]))
    assert not V.imita(ESPERADO["C"], V.codigos_dominantes(cat, LIVRO))


def _na_categoria(cat, marcas):
    return [{**m, "categoria": cat} for m in marcas]


def test_veto_so_dispara_em_categoria_concorrente_do_livro():
    """ac-a: o mesmo grupo de marcas veta a C como banco digital e nao veta como referencia de
    sentimento, que o livro deixa fora do veto."""
    grupo = [_marca("claro", "rosa", "sem_serifa", "grande")] * 3
    grupo += [_marca("escuro", "azul", "serifa", "reto")] * 2
    como_banco = V.veto(ESPERADO["C"], _na_categoria("banco_digital", grupo), LIVRO)
    assert como_banco["veta"] and como_banco["por_categoria"]["banco_digital"]["imita"]
    como_ref = V.veto(ESPERADO["C"], _na_categoria("referencia_de_sentimento", grupo), LIVRO)
    assert not como_ref["veta"]
    assert not V.veto(ESPERADO["E"], _na_categoria("banco_digital", grupo), LIVRO)["veta"]


def test_veto_recusa_categoria_fora_do_livro():
    """ac-a: categoria escrita na hora (ou com outra grafia) nao entra nem sai do veto calada."""
    grupo = _na_categoria("fintech", [_marca("claro", "rosa", "sem_serifa", "grande")] * 5)
    with pytest.raises(ValueError, match="fintech"):
        V.veto(ESPERADO["C"], grupo, LIVRO)


def test_mutacao_categorias_da_r3_em_vez_do_livro_deixam_o_veto_passar(monkeypatch):
    """Se a lista viesse de quem classifica (a R3 renomeando "banco_digital" para "fintech" e
    declarando-a fora), o mesmo grupo deixaria de vetar: a guarda tem de reprovar antes."""
    livro = {**LIVRO, "veto": {**LIVRO["veto"], "categorias_fora_do_veto": ["fintech"]}}
    grupo = _na_categoria("fintech", [_marca("claro", "rosa", "sem_serifa", "grande")] * 5)
    assert not V.veto(ESPERADO["C"], grupo, livro)["veta"]
    with pytest.raises(ValueError):
        V.veto(ESPERADO["C"], grupo, LIVRO)


def test_as_onze_categorias_concorrentes_de_ac_a_e_ad_a():
    """ac-a deu sete; ad-a (02/10, antes da primeira marca da R3) acrescentou quatro."""
    assert list(LIVRO["veto"]["categorias_concorrentes"]) == [
        "banco_tradicional", "banco_digital", "corretora", "gestora_e_private", "pagamentos",
        "consolidador", "casa_de_analise_e_educacao",
        "consultoria_cvm", "assessor", "robo", "planejador"]
    assert LIVRO["veto"]["categorias_fora_do_veto"] == ["referencia_de_sentimento"]


def test_precedencia_cobre_exatamente_as_categorias_concorrentes():
    """ad-a: marca que cabe em duas categorias fica com a primeira da precedencia; uma
    categoria fora da precedencia deixaria o desempate sem regra."""
    v = LIVRO["veto"]
    assert sorted(v["precedencia"]) == sorted(v["categorias_concorrentes"])
    assert len(v["precedencia"]) == len(set(v["precedencia"]))


def test_unidade_e_amostra_da_r3_declaradas():
    """ae-a e af-a: a unidade (app ou site) e a amostra minima sao dado do livro."""
    u = LIVRO["unidade_na_r3"]
    assert set(u) == {"com_app", "sem_app", "registro", "sensibilidade"}
    assert LIVRO["veto"]["amostra_sorteada_por_categoria"] >= LIVRO["veto"]["n_minimo_de_marcas"]


def test_centrais_do_codigo_e_do_livro_sao_as_mesmas():
    assert V.CENTRAIS == tuple(k for k, v in LIVRO["variaveis"].items() if v["central"])


def test_livro_em_ascii():
    with open(V.LIVRO, "rb") as f:
        assert all(b < 128 for b in f.read())


def test_mutacao_sem_a_faixa_de_luminosidade_o_quase_branco_vira_cor():
    """ag-b, 04/10/2026: sem a faixa, #F5F3EE (o creme do fundo da propria E) cai em laranja, o
    matiz de E e D, e #FFFEFE (branco aos olhos) em vermelho. Prova que a faixa os torna neutros."""
    import copy
    sem = copy.deepcopy(LIVRO)
    sem["variaveis"]["matiz"]["luminosidade_cromatica"] = {"min": 0.0, "max": 1.0}
    assert V.faixa_de_matiz("#F5F3EE", sem) == "laranja"
    assert V.faixa_de_matiz("#FFFEFE", sem) == "vermelho"
    assert V.faixa_de_matiz("#F5F3EE", LIVRO) == "neutro"


def test_a_emenda_ag_b_nao_muda_e_c_d():
    for d, esperado in ESPERADO.items():
        assert V.classificar_direcoes(LIVRO)[d] == esperado
