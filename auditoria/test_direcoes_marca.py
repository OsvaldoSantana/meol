# -*- coding: utf-8 -*-
"""Os estimulos das direcoes: mesmo conteudo, so o visual muda, e nada que nao deva (P-163)."""
from __future__ import annotations

import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import direcoes_marca as DM  # noqa: E402

DIRS = DM.direcoes()
TOK = DM.tokens()


def test_vacuidade_um_estimulo_por_direcao_da_resposta_16b():
    """Sem os arquivos, os testes abaixo passariam sem medir nada."""
    assert set(DIRS) == set(TOK["direcoes"]) == {"E", "C", "D"}
    for nome, path in DIRS.items():
        fonte = DM.ler(path)
        assert f'data-direcao="{nome}"' in fonte
        assert set(DM.texto_por_estado(fonte)) == {"normal", "parcial"}, nome


def test_i_o_texto_visivel_e_identico_entre_as_direcoes():
    textos = {n: DM.texto_por_estado(DM.ler(p)) for n, p in DIRS.items()}
    ref = textos["E"]
    for n, t in textos.items():
        for estado in ("normal", "parcial"):
            assert t[estado] == ref[estado], f"{n}/{estado} difere de E"


def test_i_o_texto_contem_o_que_o_motor_deu():
    obrig = DM.textos_obrigatorios(DM.conteudo(), TOK["rotulos_de_estado"])
    for n, p in DIRS.items():
        t = DM.texto_por_estado(DM.ler(p))
        for estado, lista in obrig.items():
            faltam = [x for x in lista if x not in t[estado]]
            assert not faltam, f"{n}/{estado}: falta {faltam}"


def test_ii_toda_cor_esta_no_yaml_da_direcao():
    for n, p in DIRS.items():
        assert DM.cores_fora_do_yaml(DM.ler(p), TOK["direcoes"][n]["cores"]) == [], n


def test_iii_nenhuma_url_nem_recurso_remoto():
    for n, p in DIRS.items():
        assert DM.remotos(DM.ler(p)) == [], n


def test_iv_todo_valor_em_reais_no_formato_brasileiro():
    for n, p in DIRS.items():
        for estado, t in DM.texto_por_estado(DM.ler(p)).items():
            assert "R$" in t
            assert DM.moeda_fora_do_formato(t) == [], f"{n}/{estado}"


def test_v_a_camada_1_tem_no_maximo_15_palavras():
    for n, p in DIRS.items():
        fonte = DM.ler(p)
        assert DM.analisar(fonte).camada1, f"{n}: nenhum elemento data-camada=1"
        assert DM.camada1_longa(fonte) == [], n


def test_sem_imagem_emoji_gradiente_nem_botao_sem_texto():
    for n, p in DIRS.items():
        assert DM.proibidos(DM.ler(p)) == [], n


# --- a guarda falha quando deveria (regua 5-B, pergunta 4) --------------------------------

@pytest.fixture
def e_fonte():
    return DM.ler(DIRS["E"])


def test_mutacao_i_uma_palavra_trocada_numa_direcao_reprova(e_fonte):
    ref = DM.texto_por_estado(e_fonte)
    mut = DM.texto_por_estado(e_fonte.replace("Executei", "Feito", 1))
    assert mut["normal"] != ref["normal"]


def test_mutacao_ii_cor_fora_do_yaml_reprova(e_fonte):
    cores = TOK["direcoes"]["E"]["cores"]
    assert DM.cores_fora_do_yaml(e_fonte.replace("#F5F3EE", "#F5F3EF", 1), cores) == ["#F5F3EF"]
    assert DM.cores_fora_do_yaml(e_fonte + "<style>a{color:rgb(1,2,3)}</style>", cores) == ["rgb("]
    assert DM.cores_fora_do_yaml(e_fonte + "<style>a{color:#fff}</style>", cores) == ["#FFF"]


def test_mutacao_ii_id_que_nao_e_cor_nao_conta():
    """`#tela-normal` nao e cor; `#face` seria, e o teste usa ids que nao sao hexadecimais."""
    assert DM.cores_fora_do_yaml("<a href='#tela-normal'>", {}) == []


def test_mutacao_iii_recurso_remoto_reprova(e_fonte):
    f = e_fonte.replace("<style>", "<link rel='stylesheet' href='https://fonts.x/y.css'><style>")
    assert DM.remotos(f)
    assert DM.remotos("<style>@font-face{src:url(x.woff2)}</style>")


@pytest.mark.parametrize("ruim", ["R$ 800,00", "R$ 800.00", "R$ 16,900",
                                  "R$ 70.000.00", "R$800,00"])
def test_mutacao_iv_formatos_errados_reprovam(ruim):
    """Os erros observados na rodada 1 (RI-02): Versace "R$ 16,900", XP "R$ 70.000.00"."""
    assert DM.moeda_fora_do_formato(f"Este mes, aporte {ruim} em X.")


def test_iv_o_formato_certo_passa():
    assert DM.moeda_fora_do_formato("entre R$ 0,22 e R$ 1.213,33") == []


def test_mutacao_v_frase_longa_reprova():
    longa = " ".join(["palavra"] * 16)
    assert DM.camada1_longa(f'<h1 data-camada="1">{longa}</h1>') == [longa]


def test_mutacao_proibidos_reprovam():
    assert DM.proibidos("<img alt='x'>")
    assert DM.proibidos("<style>a{background:linear-gradient(#000,#fff)}</style>")
    assert DM.proibidos("<p>\U0001F680</p>")
    assert DM.proibidos("<button><span aria-hidden='true'></span></button>")


def test_elemento_de_linha_nao_parte_a_palavra():
    """Defeito do proprio instrumento em 27/09: juntar os pedacos com espaco fazia de
    `peso-<span>alvo</span>.` o texto "peso-alvo ." e reprovava o estimulo certo."""
    f = ('<section data-estado="normal"><p>do <span>peso-alvo</span>.</p>'
         '<dl><dt>Valor</dt><dd>R$ 1</dd></dl></section>')
    assert DM.texto_por_estado(f)["normal"] == "do peso-alvo. Valor R$ 1"
