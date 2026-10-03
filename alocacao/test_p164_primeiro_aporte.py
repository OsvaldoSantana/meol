# -*- coding: utf-8 -*-
"""P-164: o primeiro aporte, com patrimonio zero e a reserva cheia.

Decisao dele (03/10/2026, bloco 19 da fila, opcao c): o primeiro aporte vai INTEIRO para a
rota de maior peso-alvo. Se ela nao couber no valor, vai inteiro para a proxima, em ordem
decrescente de peso, que caiba; se nenhuma couber, nao ha ordem e o motivo e dito. Empate
no maior peso: a primeira rota na ordem declarada do catalogo (decisao tecnica do
claude.ai). "Caber" usa as verificacoes que o motor ja tem: lote inteiro e G3 (atrito).

Ate a versao 1.36.0 da politica, `motor_aporte()` devolvia `SEM_POSICAO` com patrimonio
zero e nenhuma ordem: quem tinha a reserva cheia e nada investido ficava sem "quanto e
onde" (F0-contrato, secao 2, item 2). Todo teste daqui falha naquela versao.
"""
import copy
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pytest

from alocacao import (Estado, alocar, carregar_catalogo, carregar_politica, catalogo,
                      g3_atrito, motor_aporte)
from motor import carregar as carregar_custos

C, P = carregar_custos(), carregar_politica()
R = {r.id: r for r in catalogo(C)}
BASE = dict(despesa_mensal=4500, reserva_atual=27000, aporte_mensal=500, horizonte_anos=25)
ORDEM_DO_CATALOGO = list(carregar_catalogo()["rotas"])


def _alvo(pesos):
    return {"pesos": pesos}


def test_patrimonio_zero_e_reserva_cheia_recebem_uma_ordem_na_rota_de_maior_peso():
    """O teste que prende o conserto: o alvo REAL do pipeline, nao um alvo montado."""
    e = Estado(**BASE)
    saida = alocar(e, C, P, teses={}, carregos={})
    assert "diretiva" not in saida, "a reserva precisa estar cheia para o caso existir"
    pesos = saida["alvo"]["pesos"]
    maior = max(pesos.values())
    esperada = min((rid for rid, w in pesos.items() if w == maior),
                   key=ORDEM_DO_CATALOGO.index)

    r = motor_aporte(e, saida["alvo"], C, P, rotas_por_id=R)

    assert r["status"] == "OK", r.get("status")
    assert len(r["ordens"]) == 1
    o = r["ordens"][0]
    assert o["rota"] == esperada
    assert o["valor"] == e.aporte_mensal
    assert r["caixa"] == e.caixa


def test_o_porque_diz_que_vai_inteiro_e_que_os_proximos_meses_espalham():
    e = Estado(**BASE)
    r = motor_aporte(e, alocar(e, C, P, teses={}, carregos={})["alvo"], C, P,
                     rotas_por_id=R)
    porque = r["ordens"][0]["porque"]
    assert "inteiro" in porque and "maior parte" in porque
    assert "proximos meses" in porque and "espalha" in porque
    assert R[r["ordens"][0]["rota"]].nome in porque


def test_empate_no_maior_peso_vale_a_primeira_rota_na_ordem_do_catalogo():
    """pibb11 vem antes de divo11 no catalogo; na ordem alfabetica e na ordem do dict
    de pesos, divo11 vem antes. So o criterio declarado escolhe pibb11."""
    assert ORDEM_DO_CATALOGO.index("pibb11") < ORDEM_DO_CATALOGO.index("divo11")
    pesos = {"divo11": 0.4, "pibb11": 0.4, "td_selic": 0.2}
    r = motor_aporte(Estado(**BASE), _alvo(pesos), C, P,
                     precos={"divo11": 10.0, "pibb11": 10.0}, rotas_por_id=R)
    assert [o["rota"] for o in r["ordens"]] == ["pibb11"]
    assert r["ordens"][0]["valor"] == 500.0


def test_rota_de_maior_peso_que_nao_cabe_no_lote_cede_para_a_proxima():
    pesos = {"ivvb11": 0.5, "td_selic": 0.3, "bova11": 0.2}
    r = motor_aporte(Estado(**BASE), _alvo(pesos), C, P,
                     precos={"ivvb11": 600.0, "bova11": 100.0}, rotas_por_id=R)
    assert [o["rota"] for o in r["ordens"]] == ["td_selic"]
    assert r["ordens"][0]["valor"] == 500.0
    assert [d["rota"] for d in r["nao_couberam"]] == ["ivvb11"]
    assert r["nao_couberam"][0]["verificacao"] == "lote"
    assert R["ivvb11"].nome in r["ordens"][0]["porque"]   # diz quem ficou de fora


def test_rota_de_maior_peso_barrada_pelo_g3_no_valor_do_mes_cede_para_a_proxima():
    """O G3 do pipeline barra pelo aporte BASE; aqui o mes trouxe menos, e a corretagem
    fixa de acao_450 passa do teto. O controle prova que e o valor, nao a rota."""
    pesos = {"acao_450": 0.6, "td_selic": 0.4}
    precos = {"acao_450": 30.0}
    assert g3_atrito([R["acao_450"]], C, P, 500.0)[0], "controle: a 500 ela cabe"
    assert not g3_atrito([R["acao_450"]], C, P, 300.0)[0]

    cabe = motor_aporte(Estado(**BASE), _alvo(pesos), C, P, precos=precos, rotas_por_id=R)
    assert [o["rota"] for o in cabe["ordens"]] == ["acao_450"]

    r = motor_aporte(Estado(**BASE), _alvo(pesos), C, P, precos=precos, rotas_por_id=R,
                     aporte_do_mes=300)
    assert [o["rota"] for o in r["ordens"]] == ["td_selic"]
    assert r["ordens"][0]["valor"] == 300.0
    assert r["nao_couberam"][0]["verificacao"] == "G3_atrito"


def test_nenhuma_rota_cabe_recusa_com_o_motivo_e_guarda_o_dinheiro():
    """RI-10: nunca um zero, nunca um SEM_POSICAO mudo."""
    pesos = {"ivvb11": 0.6, "bova11": 0.4}
    e = Estado(**BASE)
    r = motor_aporte(e, _alvo(pesos), C, P,
                     precos={"ivvb11": 600.0, "bova11": 700.0}, rotas_por_id=R)
    assert r["status"] == "NENHUMA_ROTA_CABE"
    assert r["ordens"] == []
    assert r["motivo"] == P["motor_aporte"]["primeiro_aporte"]["motivo_sem_rota"]
    assert "guardado para o proximo" in r["motivo"]
    assert r["caixa"] == e.caixa + 500.0
    assert [d["rota"] for d in r["nao_couberam"]] == ["ivvb11", "bova11"]


def test_a_regra_e_dado_e_criterio_desconhecido_recusa():
    """P2: trocar a regra e um commit no YAML; um valor que o motor nao conhece nao vira
    default silencioso."""
    for chave in ("regra", "desempate"):
        P2 = copy.deepcopy(P)
        P2["motor_aporte"]["primeiro_aporte"][chave] = "outra_coisa"
        with pytest.raises(ValueError, match=chave):
            motor_aporte(Estado(**BASE), _alvo({"td_selic": 1.0}), C, P2, rotas_por_id=R)


def test_com_patrimonio_a_regra_do_primeiro_aporte_nao_entra():
    e = Estado(**{**BASE, "posicoes": {"bova11": 5000, "td_selic": 100}})
    r = motor_aporte(e, alocar(e, C, P, teses={}, carregos={})["alvo"], C, P)
    assert r["status"] == "OK"
    assert all("porque" not in o for o in r["ordens"])
    assert "nao_couberam" not in r
