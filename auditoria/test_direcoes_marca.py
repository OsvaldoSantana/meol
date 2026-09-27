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
        assert set(DM.texto_por_versao(fonte)) == set(DM.VERSOES), nome


def test_i_o_texto_visivel_e_identico_entre_as_direcoes():
    textos = {n: DM.texto_por_versao(DM.ler(p)) for n, p in DIRS.items()}
    for n, t in textos.items():
        for v in DM.VERSOES:
            assert t[v] == textos["E"][v], f"{n}/{v} difere de E"


def test_i_o_texto_contem_o_que_o_motor_deu():
    obrig = DM.textos_obrigatorios(DM.conteudo(), TOK["rotulos_de_estado"])
    for n, p in DIRS.items():
        t = DM.texto_por_versao(DM.ler(p))
        for v, lista in obrig.items():
            faltam = [x for x in lista if x not in t[v]]
            assert not faltam, f"{n}/{v}: falta {faltam}"


def test_s4_i_as_versoes_diferem_so_na_linha_da_rota_bloqueada():
    """j-A: a H3 compara a mesma tela com e sem UMA linha; qualquer outra diferenca a suja."""
    linha = DM.conteudo()["com_rota_bloqueada"]["linha"]
    for n, p in DIRS.items():
        d = DM.diferenca_entre_versoes(DM.ler(p))
        assert d["base_sem"] == d["rota_sem"], f"{n}: as versoes diferem fora da linha"
        assert d["dif_base"] == "", f"{n}: a base nao pode ter elemento de diferenca"
        assert d["dif_rota"] == linha, f"{n}: a linha nao e a do conteudo.yaml"


def test_s4_ii_nenhum_ticker_do_catalogo_no_texto():
    tickers = DM.tickers_do_catalogo()
    assert len(tickers) >= 5, "vacuidade: o catalogo tem de nomear tickers"
    for n, p in DIRS.items():
        for v, t in DM.texto_por_versao(DM.ler(p)).items():
            assert DM.tickers_no_texto(t, tickers) == [], f"{n}/{v}"


def test_s4_iii_toda_ilustracao_tem_data_provisorio():
    achou_svg = False
    for n, p in DIRS.items():
        fonte = DM.ler(p)
        achou_svg |= "<svg" in fonte
        assert [x for x in DM.proibidos(fonte) if "svg" in x or "provisorio" in x] == [], n
    assert achou_svg, "vacuidade: a D tem a ilustracao provisoria (k-A)"


def test_ii_toda_cor_esta_no_yaml_da_direcao():
    for n, p in DIRS.items():
        assert DM.cores_fora_do_yaml(DM.ler(p), TOK["direcoes"][n]["cores"]) == [], n


def test_iii_nenhuma_url_nem_recurso_remoto():
    for n, p in DIRS.items():
        assert DM.remotos(DM.ler(p)) == [], n


def test_i_a_toda_fonte_usada_esta_embutida_com_licenca():
    """i-A: cada direcao carrega as suas fontes OFL, e o YAML declara as mesmas."""
    for n, p in DIRS.items():
        fonte = DM.ler(p)
        familias = DM.fontes_declaradas(fonte)
        assert familias, f"{n}: nenhuma @font-face"
        pilhas = " ".join(v for k, v in TOK["direcoes"][n]["fontes"].items() if k != "arquivos")
        for f in familias:
            assert f in pilhas, f"{n}: {f} embutida e fora do YAML"
        for arq in TOK["direcoes"][n]["fontes"]["arquivos"]:
            assert os.path.isfile(os.path.join(DM.TIPOGRAFIA, arq)), arq
            assert f"../tipografia/{arq}" in fonte, f"{n}: {arq} declarada e nao usada"


def test_m_b_o_matiz_da_c_fica_longe_das_marcas_observadas():
    """m-B: a regra escrita no YAML, aplicada: >= 30 graus de toda cor OBSERVADA."""
    c = TOK["direcoes"]["C"]
    esc = c["escolha_de_cor"]
    h = DM.matiz(c["cores"]["destaque"])
    assert abs(h - esc["matiz_escolhido_graus"]) < 2
    obs = [m for m in esc["marcas_conferidas"] if m["status"] == "OBSERVADO"]
    assert len(obs) >= 5, "vacuidade"
    perto = [(m["marca"], round(DM.distancia_de_matiz(h, DM.matiz(m["cor"]))))
             for m in obs if DM.distancia_de_matiz(h, DM.matiz(m["cor"])) < 30]
    assert not perto, perto


def test_iv_todo_valor_em_reais_no_formato_brasileiro():
    for n, p in DIRS.items():
        for v, t in DM.texto_por_versao(DM.ler(p)).items():
            assert "R$" in t
            assert DM.moeda_fora_do_formato(t) == [], f"{n}/{v}"


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


@pytest.fixture
def d_fonte():
    return DM.ler(DIRS["D"])


def test_mutacao_i_uma_palavra_trocada_numa_direcao_reprova(e_fonte):
    ref = DM.texto_por_versao(e_fonte)
    mut = DM.texto_por_versao(e_fonte.replace("Executei", "Feito", 1))
    assert mut["base"] != ref["base"]


def test_mutacao_s4_i_diferenca_fora_da_linha_reprova(e_fonte):
    """Mudar a versao com rota bloqueada em outro ponto que nao a linha reprova."""
    i = e_fonte.index('data-versao="com_rota_bloqueada"')
    mut = e_fonte[:i] + e_fonte[i:].replace("Executei", "Confirmei", 1)
    d = DM.diferenca_entre_versoes(mut)
    assert d["base_sem"] != d["rota_sem"]


def test_mutacao_s4_i_linha_na_base_reprova(e_fonte):
    mut = e_fonte.replace('<p class="nota"', '<p data-diferenca="x">extra</p><p class="nota"', 1)
    assert DM.diferenca_entre_versoes(mut)["dif_base"] == "extra"


def test_mutacao_s4_ii_ticker_real_reprova(e_fonte):
    tickers = DM.tickers_do_catalogo()
    mut = e_fonte.replace("fundo de \u00edndice de a\u00e7\u00f5es brasileiras", "PIBB11", 1)
    assert DM.tickers_no_texto(DM.texto_por_versao(mut)["base"], tickers) == ["PIBB11"]


def test_mutacao_s4_iii_svg_sem_provisorio_reprova(d_fonte):
    mut = d_fonte.replace(' data-provisorio="P-168"', "")
    assert "svg fora de data-provisorio" in DM.proibidos(mut)
    assert DM.proibidos('<div data-provisorio="P-168"><svg><text>X</text></svg></div>')
    assert DM.proibidos('<div data-provisorio="sim"><svg></svg></div>')


def test_mutacao_ii_cor_fora_do_yaml_reprova(e_fonte):
    cores = TOK["direcoes"]["E"]["cores"]
    assert DM.cores_fora_do_yaml(e_fonte.replace("#F5F3EE", "#F5F3EF", 1), cores) == ["#F5F3EF"]
    assert DM.cores_fora_do_yaml(e_fonte + "<style>a{color:rgb(1,2,3)}</style>", cores) == ["rgb("]
    assert DM.cores_fora_do_yaml(e_fonte + "<style>a{color:#fff}</style>", cores) == ["#FFF"]


def test_mutacao_ii_id_que_nao_e_cor_nao_conta():
    """`#tela-base` nao e cor; `#face` seria, e o teste usa ids que nao sao hexadecimais."""
    assert DM.cores_fora_do_yaml("<a href='#tela-base'>", {}) == []


def test_mutacao_iii_recurso_remoto_reprova(e_fonte):
    f = e_fonte.replace("<style>", "<link rel='stylesheet' href='https://fonts.x/y.css'><style>")
    assert DM.remotos(f)
    assert DM.remotos("<style>@font-face{src:url('https://x/y.woff2')}</style>")
    assert DM.remotos("<style>@font-face{src:url('../tipografia/nao-existe.woff2')}</style>")
    assert DM.remotos("<style>a{background:url('../direcoes/cenario.yaml')}</style>")


@pytest.mark.parametrize("ruim", ["R$ 800,00", "R$\u00a0800.00", "R$\u00a016,900",
                                  "R$\u00a070.000.00", "R$800,00"])
def test_mutacao_iv_formatos_errados_reprovam(ruim):
    """Os erros observados na rodada 1 (RI-02): Versace "R$ 16,900", XP "R$ 70.000.00"."""
    assert DM.moeda_fora_do_formato(f"Este mes, aporte {ruim} em X.")


def test_iv_o_formato_certo_passa():
    assert DM.moeda_fora_do_formato("entre R$\u00a00,22 e R$\u00a01.213,33") == []


def test_mutacao_v_frase_longa_reprova():
    longa = " ".join(["palavra"] * 16)
    assert DM.camada1_longa(f'<h1 data-camada="1">{longa}</h1>') == [longa]


def test_mutacao_proibidos_reprovam():
    assert DM.proibidos("<img alt='x'>")
    assert DM.proibidos("<style>a{background:linear-gradient(#000,#fff)}</style>")
    assert DM.proibidos("<p>\U0001F680</p>")
    assert DM.proibidos("<button><span aria-hidden='true'></span></button>")


def test_mutacao_m_b_o_roxo_antigo_reprova():
    """O roxo da S3 (#6A2BD9) fica a menos de 30 graus do Nubank observado (276)."""
    assert DM.distancia_de_matiz(DM.matiz("#6A2BD9"), DM.matiz("#5D0599")) < 30


def test_elemento_de_linha_nao_parte_a_palavra():
    """Defeito do proprio instrumento em 27/09: juntar os pedacos com espaco fazia de
    `peso-<span>alvo</span>.` o texto "peso-alvo ." e reprovava o estimulo certo."""
    f = ('<section data-versao="base"><p>do <span>peso-alvo</span>.</p>'
         '<dl><dt>Valor</dt><dd>R$ 1</dd></dl></section>')
    assert DM.texto_por_versao(f)["base"] == "do peso-alvo. Valor R$ 1"
