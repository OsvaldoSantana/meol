# -*- coding: utf-8 -*-
"""A paginacao do servico OData do BCB (P-170), sem rede: o `pegar` e falso."""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r3_baixar_bcb as B  # noqa: E402

BASE = "https://exemplo/odata/R"


def _servico(total):
    """Um servico falso com o defeito do real: 500 a `$skip=0`. Guarda as URLs pedidas."""
    pedidas = []

    def pegar(url):
        pedidas.append(url)
        assert "$skip=0" not in url, "o servico responde 500 a $skip=0"
        pulo = int(url.split("$skip=")[1]) if "$skip=" in url else 0
        topo = int(url.split("$top=")[1].split("&")[0])
        return [{"i": i} for i in range(pulo, min(pulo + topo, total))]
    return pegar, pedidas


def test_a_primeira_pagina_vai_sem_skip_e_as_outras_pulam_de_passo_em_passo():
    pegar, pedidas = _servico(25)
    assert [r["i"] for r in B.paginar(pegar, BASE, passo=10)] == list(range(25))
    assert [u.split("?")[1] for u in pedidas] == [
        "$format=json&$top=10", "$format=json&$top=10&$skip=10", "$format=json&$top=10&$skip=20"]


def test_total_multiplo_do_passo_pede_uma_pagina_a_mais_e_nao_perde_linha():
    """Se o total e exato, a pagina cheia nao diz que acabou: a seguinte vem vazia."""
    pegar, pedidas = _servico(20)
    assert len(B.paginar(pegar, BASE, passo=10)) == 20
    assert len(pedidas) == 3


def test_recurso_vazio_devolve_lista_vazia():
    pegar, _ = _servico(0)
    assert B.paginar(pegar, BASE, passo=10) == []
