# -*- coding: utf-8 -*-
"""P-181: a porta de uso, provada sobre estados SINTETICOS.

Nenhum teste daqui le o estado.yaml de ninguem (D-01): todo estado nasce do
`estado.exemplo.yaml` com numeros inventados, e a rede e substituida por um CSV sintetico.
"""
from __future__ import annotations
import copy
import datetime as dt
import io
import os
import sys

import pytest
import yaml

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import aporte_do_mes as M  # noqa: E402
from motor import carregar as carregar_custos  # noqa: E402
from alocacao import carregar_politica  # noqa: E402

C, P = carregar_custos(), carregar_politica()
PU = 19943.12
CSV = ("Tipo Titulo;Data Vencimento;Data Base;Taxa Compra Manha;Taxa Venda Manha;"
       "PU Compra Manha;PU Venda Manha;PU Base Manha\n"
       "Tesouro Selic;01/03/2027;01/10/2026;0,01;0,02;99999,00;1;1\n"     # dia anterior
       "Tesouro Selic;01/03/2029;02/10/2026;0,05;0,06;19800,00;19790,00;19790,00\n"
       "Tesouro Selic;01/03/2031;02/10/2026;0,09;0,10;19943,12;19924,17;19924,17\n"
       "Tesouro Selic;01/03/2026;02/10/2026;0,00;0,00;0,00;18000,00;18000,00\n"  # fora de venda
       "Tesouro IPCA+;15/05/2035;02/10/2026;7,0;7,1;2000,00;1990,00;1990,00\n")


def _estado(**mudar):
    with open(os.path.join(AQUI, "estado.exemplo.yaml"), encoding="utf-8") as f:
        d = yaml.safe_load(f)
    d.update(despesa_mensal=3000, estabilidade_renda="media", horizonte_anos=25,
             aporte_mensal=500, reserva_atual=30000.0, reserva_por_rota={"td_reserva": 30000.0})
    d["meta"].update(status="REAL", preenchido_em=dt.date(2026, 10, 10))
    d.update(mudar)
    return copy.deepcopy(d)


def _lote(rid, unit):
    rotas = {r.id: r for r in M.catalogo(C)}
    return M.preco_do_lote(rotas[rid], unit)


def _texto(linhas):
    return "\n".join(linhas)


# ── O caminho de quem ainda forma a reserva ──────────────────────────────────────────────
def test_reserva_incompleta_manda_o_aporte_para_a_reserva_e_diz_por_que():
    cod, linhas = M.responder(_estado(reserva_atual=1000.0, reserva_por_rota=None), C, P)
    t = _texto(linhas)
    assert cod == 0
    assert "O QUE FAZER: TODO O APORTE PARA A RESERVA" in t
    assert "R$ 1.000,00" in t and "R$ 18.000,00" in t, "o atual e o alvo, em reais"
    assert "G2_reserva" in t and "nao e recomendacao de investimento" in t


# ── O primeiro aporte, com a reserva cheia (P-164 + P-179) ──────────────────────────────
def test_primeiro_aporte_com_o_pu_diz_quanto_para_onde_e_por_que():
    cod, linhas = M.responder(_estado(), C, P, precos_lote={"td_selic": _lote("td_selic", PU)},
                              origem_precos={"td_selic": "PU sintetico"})
    t = _texto(linhas)
    assert cod == 0
    assert "Tesouro Selic acima de R$10k: R$ 398,86 (0,02 titulo)" in t
    assert "fica no caixa: R$ 101,14" in t
    assert "Primeiro aporte: o valor vai inteiro para Tesouro Selic" in t
    assert "preco de Tesouro Selic acima de R$10k: PU sintetico" in t, "procedencia do preco"
    assert "politica.yaml versao" in t and "custos.yaml (impressao" in t


def test_quem_ficou_de_fora_sai_com_o_portao_que_eliminou():
    _cod, linhas = M.responder(_estado(), C, P, precos_lote={"td_selic": _lote("td_selic", PU)})
    fora = [x for x in linhas if x.startswith("  - ") and "[G" in x]
    portoes = {x.rsplit("[", 1)[1].rstrip("]") for x in fora}
    assert {"G3_atrito", "G4_dominancia", "G5_status", "G8_compromisso_de_carrego"} <= portoes
    assert any("BOVA11 — corretora zero" in x for x in fora if "G4_dominancia" in x), \
        "o dominado diz QUEM o domina"


def test_sem_preco_o_comando_recusa_em_vez_de_calcular_a_um_real():
    """O motor usa 1.0 quando falta preco. Sem esta guarda, a ordem sairia com quantidade
    errada e aparencia perfeita."""
    cod, linhas = M.responder(_estado(), C, P)
    assert cod == 3
    assert "falta o preco de hoje de: Tesouro Selic acima de R$10k (td_selic)" in linhas[0]


def test_pede_so_o_preco_que_o_motor_consultou():
    """R$ 150 nao alcancam 0,01 titulo de Selic (~R$ 199): o motor passa para a proxima rota,
    um ETF, e e o preco DELE que falta -- nao o de todos os ETFs da carteira."""
    cod, linhas = M.responder(_estado(aporte_mensal=150), C, P,
                              precos_lote={"td_selic": _lote("td_selic", PU)})
    assert cod == 3
    pedidos = linhas[0].split("falta o preco de hoje de: ")[1].split(". Veja")[0]
    assert pedidos == "PIBB11 — corretora zero (pibb11)"


def test_com_o_preco_do_etf_o_aporte_cede_e_a_ordem_sai_em_cotas():
    precos = {"td_selic": _lote("td_selic", PU), "pibb11": _lote("pibb11", 30.0)}
    cod, linhas = M.responder(_estado(aporte_mensal=150), C, P, precos_lote=precos)
    t = _texto(linhas)
    assert cod == 0
    assert "R$ 150,00 (5 cota(s))" in t
    assert "ainda nao cabe" in t and "Tesouro Selic" in t


# ── Carteira que ja existe ──────────────────────────────────────────────────────────────
def test_com_patrimonio_as_ordens_vao_para_quem_esta_mais_longe_do_alvo():
    pos = {"bova11": 900.0, "pibb11": 900.0, "divo11": 900.0, "smal11": 900.0,
           "ivvb11": 900.0, "acao_zero": 900.0}
    precos = {"td_selic": _lote("td_selic", PU), "hash11": 48.0}
    precos.update({r: 100.0 for r in pos})
    cod, linhas = M.responder(_estado(posicoes=pos, aporte_mensal=1000), C, P, precos_lote=precos)
    t = _texto(linhas)
    assert cod == 0
    assert "1. Tesouro Selic acima de R$10k" in t, "td_selic e o maior deficit"
    assert "alvo 26" in t and "hoje 0.0% da carteira" in t


# ── A porta de entrada continua a mesma (CX-04) ─────────────────────────────────────────
def test_estado_invalido_para_antes_de_responder():
    cod, linhas = M.responder(_estado(caixa=True), C, P)
    assert cod == 2
    assert any(x.startswith("  - caixa:") for x in linhas)


# ── O PU do Tesouro, do CSV oficial ─────────────────────────────────────────────────────
def test_pu_do_tesouro_e_o_maior_do_dia_mais_recente_entre_os_a_venda():
    pu = M.pu_do_tesouro(CSV, "Tesouro Selic")
    assert pu["pu"] == PU and pu["vencimento"] == "01/03/2031"
    assert pu["data_base"].isoformat() == "2026-10-02"
    assert M.pu_do_tesouro(CSV, "Tesouro Inexistente") is None


def test_numero_como_a_pessoa_digita():
    assert M.numero_br("19.943,12") == 19943.12
    assert M.numero_br("19943,12") == 19943.12
    assert M.numero_br("19943.12") == 19943.12
    assert M.numero_br("1.500") == 1500.0, "ponto em grupo de tres e milhar"
    assert M.reais(1234.5) == "R$ 1.234,50"


def test_preco_informado_e_o_pu_e_a_conversao_e_do_lote():
    rotas = {r.id: r for r in M.catalogo(C)}
    precos, origem, erros = M.precos_informados(["td_selic=19.943,12", "bova11=128,43",
                                                 "naoexiste=1", "bova11=abc"], rotas)
    assert precos == {"td_selic": pytest.approx(199.4312), "bova11": 128.43}
    assert "informado por voce" in origem["td_selic"]
    assert len(erros) == 2


# ── O comando inteiro, com arquivo e rede de mentira ────────────────────────────────────
def _arquivo(tmp_path, d):
    p = tmp_path / "estado.yaml"
    p.write_text(yaml.safe_dump(d, allow_unicode=True), encoding="utf-8")
    return str(p)


def test_main_baixa_o_pu_e_cita_a_fonte_com_o_hash(tmp_path):
    out = io.StringIO()
    cod = M.main(["--estado", _arquivo(tmp_path, _estado())], saida=out,
                 baixar=lambda: (CSV, "ab" * 32))
    t = out.getvalue()
    assert cod == 0
    assert "PU de compra R$ 19.943,12 em 02/10/2026" in t and "sha256 abababababab" in t
    assert "R$ 398,86 (0,02 titulo)" in t


def test_main_sem_rede_pede_o_pu(tmp_path):
    def falha():
        raise OSError("sem rede")
    out = io.StringIO()
    cod = M.main(["--estado", _arquivo(tmp_path, _estado())], saida=out, baixar=falha)
    assert cod == 3 and "(td_selic)" in out.getvalue()


def test_main_com_aporte_de_bonus_mostra_os_dois_valores(tmp_path):
    out = io.StringIO()
    cod = M.main(["--estado", _arquivo(tmp_path, _estado()), "--aporte", "1.000",
                  "--preco", "td_selic=19943,12", "--sem-rede"], saida=out)
    t = out.getvalue()
    assert cod == 0
    assert "APORTE DE" in t and "R$ 1.000,00" in t
    assert "o alvo continua calculado sobre R$ 500,00" in t


def test_main_sem_o_arquivo_explica_o_que_fazer(tmp_path):
    out = io.StringIO()
    cod = M.main(["--estado", str(tmp_path / "nao_existe.yaml"), "--sem-rede"], saida=out)
    assert cod == 2 and "estado.exemplo.yaml" in out.getvalue()


def test_nenhum_teste_daqui_le_o_estado_de_ninguem():
    """A mesma garantia do test_usuario_novo: o caminho padrao do comando e o estado.yaml
    dele, e nenhum teste deste arquivo pode chama-lo sem `--estado`."""
    fonte = open(__file__, encoding="utf-8").read()
    chamadas = [x for x in fonte.splitlines() if "M.main([" in x and "chamadas" not in x]
    assert chamadas and all("--estado" in x for x in chamadas)
