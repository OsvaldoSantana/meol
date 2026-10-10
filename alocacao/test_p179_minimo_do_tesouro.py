# -*- coding: utf-8 -*-
"""P-179: o investimento minimo do Tesouro entra no "caber" do primeiro aporte, como lote.

Decisao dele, 04/10/2026, pelo formulario: "Entra, como lote" (fila, bloco 26). A regra lida na
fonte primaria em 10/10/2026 (tesourodireto.com.br, "Regras e regulamento", item 9): "As
aplicacoes tradicionais no Tesouro Direto devem ser multiplas de 0,01 titulo ou 1% (um por
cento) do valor de um titulo". Entao o lote do Tesouro e 0,01 titulo, e o preco do lote e 1%
do preco unitario (PU) do dia. Com o PU de compra do Tesouro Selic em ~R$ 20 mil (CSV do
Tesouro Transparente, 02/10/2026), o minimo fica em ~R$ 200, e a ordem de R$ 40 do
instantaneo da P-164 seria recusada pela corretora.

Nenhum numero de ninguem (D-01): os aportes e PU daqui sao sinteticos.
"""
from __future__ import annotations
import os
import sys

import pytest

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from motor import carregar as carregar_custos  # noqa: E402
from alocacao import (Estado, carregar_catalogo, carregar_politica, catalogo,  # noqa: E402
                      motor_aporte, preco_do_lote)

C, P = carregar_custos(), carregar_politica()
R = {r.id: r for r in catalogo(C)}
PU = 19943.12          # sintetico, na ordem de grandeza do Tesouro Selic de 10/2026
BASE = dict(despesa_mensal=3000, reserva_atual=18000, horizonte_anos=25)


def _alvo(pesos):
    return {"pesos": pesos}


def test_o_tesouro_negocia_em_fracoes_de_0_01_titulo():
    for rid in ("td_selic", "td_ipca"):
        r = R[rid]
        assert r.negocia_em_lote is True, f"{rid}: o lote do Tesouro e 0,01 titulo"
        assert r.lote_fracao == 0.01


def test_a_regra_vem_do_catalogo_com_a_fonte():
    """P2 e P1: a fracao e dado, e o dado diz de onde veio."""
    cru = carregar_catalogo()["rotas"]
    for rid in ("td_selic", "td_ipca"):
        base = cru[rid]["procedencia"]["base"]
        assert "multiplas de 0,01 titulo" in base and "tesourodireto.com.br" in base


def test_o_tesouro_reserva_fica_sem_lote_e_isso_esta_declarado():
    """O Tesouro Reserva e outro produto, com regra de minimo propria que nao foi lida (a
    pagina inicial do Tesouro fala em minimo "a partir de R$ 2"). Sem a regra lida, o
    catalogo nao inventa uma."""
    assert R["td_reserva"].lote_fracao is None
    assert "NAO_CONFIRMADO" in carregar_catalogo()["rotas"]["td_reserva"]["procedencia"]["base"]


def test_preco_do_lote_e_a_fracao_do_pu():
    assert preco_do_lote(R["td_selic"], PU) == pytest.approx(199.4312)
    assert preco_do_lote(R["bova11"], 128.43) == 128.43, "rota sem fracao: o lote e a unidade"


def test_quarenta_reais_nao_compram_tesouro_selic():
    """O caso que abriu a P-179. Antes, a ordem saia: R$ 40 em Tesouro Selic."""
    e = Estado(**BASE, aporte_mensal=40)
    r = motor_aporte(e, _alvo({"td_selic": 1.0}), C, P,
                     precos={"td_selic": preco_do_lote(R["td_selic"], PU)}, rotas_por_id=R)
    assert r["status"] == "NENHUMA_ROTA_CABE" and r["ordens"] == []
    assert r["nao_couberam"][0]["verificacao"] == "lote"
    assert r["caixa"] == 40


def test_quinhentos_reais_compram_dois_centesimos_e_o_resto_vai_para_o_caixa():
    e = Estado(**BASE, aporte_mensal=500)
    r = motor_aporte(e, _alvo({"td_selic": 1.0}), C, P,
                     precos={"td_selic": preco_do_lote(R["td_selic"], PU)}, rotas_por_id=R)
    o = r["ordens"][0]
    assert (o["rota"], o["quantidade"]) == ("td_selic", 2)
    assert o["valor"] == pytest.approx(398.86, abs=0.01)
    assert r["caixa"] == pytest.approx(101.14, abs=0.01)


def test_o_primeiro_aporte_cede_ao_proximo_que_cabe():
    """A regra (c) da P-164 com o lote novo: a rota de maior peso nao cabe, e o aporte vai
    inteiro para a proxima que cabe."""
    e = Estado(**BASE, aporte_mensal=150)
    r = motor_aporte(e, _alvo({"td_selic": 0.6, "rdb_100": 0.4}), C, P,
                     precos={"td_selic": preco_do_lote(R["td_selic"], PU)}, rotas_por_id=R)
    assert [o["rota"] for o in r["ordens"]] == ["rdb_100"]
    assert [d["rota"] for d in r["nao_couberam"]] == ["td_selic"]
