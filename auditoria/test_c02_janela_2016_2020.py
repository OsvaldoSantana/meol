# -*- coding: utf-8 -*-
"""O C-02 v2 contra o acervo real de 2016-2020, como o pre-registro o escreveu (secao 7).

A corrida de 03/10/2026 (b331172, docs/auditoria/C02-JANELA-2016-2020-resultado.json) deu
NAO_CONFIRMADA. Decisao dele, 03/10/2026 (opcao A): a P-115 fecha com o resultado como saiu.
A secao 7 manda o teste entrar como foi escrito, em xfail(strict=True) com a causa medida no
motivo -- a mesma decisao de 21/09 para o v1 (fase0/test_ajustar_janela.py). Se a janela
passar a dar PASSA, a suite avisa: o motivo abaixo deixou de ser verdade.

A quarentena da secao 9 acabou com o resultado empurrado; este arquivo le preco de 2016-2020
e por isso e separado do test_c02_corrida.py, que promete so dado sintetico.

O xfail vale so para AssertionError (o veredito). Insumo com sha256 diferente da secao 2 nao e
o teste do pre-registro, e sai como falha, nunca como xfail.
"""
from __future__ import annotations

import os
import sys

import pytest

AQUI = os.path.dirname(os.path.abspath(__file__))
for _p in (AQUI, os.path.join(os.path.dirname(AQUI), "fase0")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import c02_corrida as C  # noqa: E402
from acervo_de_teste import exigir_acervo  # noqa: E402

RAIZ_COTAHIST = os.path.join(C.RAIZ_REPO, "data", "bronze", "b3", "cotahist")
SILVER = os.path.join(C.RAIZ_REPO, "data", "silver",
                      "eventos_silver_2026-09-11_cal-19860102-20260918.csv")
# Secao 2 do pre-registro: os sha256 que a corrida tem de ler.
SHA_SILVER = "ec6b50dae59dd30e5ec48c66ab9849c5c000ea02d07ab1072904eab2dfe98143"
SHA_COTAHIST = {
    "COTAHIST_A2016.ZIP": "ffc82a9b973cb5901e68dc11bea1bbc9bf0a2c46749e0efe5a7a89229bc0d81f",
    "COTAHIST_A2017.ZIP": "af6aaa85187c1d58ec6565522644066da573a7dc5b579c1d4c906ae95a2dea86",
    "COTAHIST_A2018.ZIP": "9d66136179d9822476c6035000167aecf2665f4396619e4d74c0011745a0c507",
    "COTAHIST_A2019.ZIP": "5170d3f8f079c3306424b36c2fae9b467391f8fa37d16d389f487b4c5c28edb9",
    "COTAHIST_A2020.ZIP": "86442168939b9da7b3cc1ec1662c333ee5ab4c75f2be1865b5bf55ba4c52168f",
}

# A causa MEDIDA (o JSON de b331172), nao uma explicacao escrita depois.
MOTIVO = ("C-02 v2 em 2016-2020 deu NAO_CONFIRMADA (b331172): K2 do JCP razao 0,878, IC "
          "[0,680 ; 1,060], sigma 0,0971 > sigma_max 0,0416, n=555 em 271 pregoes; K3 do "
          "dividendo razao 0,934, IC [0,770 ; 1,075], sigma 0,0778 > 0,0463, n=416. Falta de "
          "poder (PO-01), nao reprovacao: K1, K5, completude e K6 PASSA")

pytestmark = pytest.mark.xdist_group("c02_janela_2016_2020")


class InsumoDiferente(RuntimeError):
    """O acervo nao e o da secao 2: o veredito nao seria o do pre-registro."""


@pytest.fixture(scope="module")
def resultado():
    exigir_acervo(SILVER, *[os.path.join(RAIZ_COTAHIST, a) for a in SHA_COTAHIST])
    lidos = C.ajustar.janela("%d-%d" % C.JANELA)
    ins = C.insumos(SILVER, RAIZ_COTAHIST, lidos)
    lido = {c["arquivo"]: c["sha256"] for c in ins["cotahist"]}
    if ins["silver"]["sha256"] != SHA_SILVER or lido != SHA_COTAHIST:
        raise InsumoDiferente("secao 2: silver %s, cotahist %s"
                              % (ins["silver"]["sha256"], lido))
    m = C.ajustar.medir(RAIZ_COTAHIST, SILVER, lidos)
    return C.julgar(m, C.ler_d1(), C.custos())


@pytest.mark.slow
@pytest.mark.xfail(strict=True, raises=AssertionError, reason=MOTIVO)
def test_REAL_C02_V2_a_janela_2016_2020_passa(resultado):
    """Secao 4.3: a janela PASSA. Escrito como o pre-registro manda; reprovou por poder."""
    assert resultado["veredito"] == C.PASSA, (resultado["veredito"], resultado["K2"],
                                              resultado["K3"])
