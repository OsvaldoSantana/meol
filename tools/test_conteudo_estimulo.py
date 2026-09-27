# -*- coding: utf-8 -*-
"""O conteudo dos estimulos e o que o motor da, nao o que alguem escreveu (P-163, P1)."""
from __future__ import annotations

import os
import sys

import pytest
import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import conteudo_estimulo as CE  # noqa: E402


def test_o_conteudo_gravado_e_o_que_o_motor_da_hoje():
    """Se a politica ou os custos mudarem o numero, o estimulo fica velho em voz alta."""
    assert CE.conferir() == []


def test_mutacao_um_valor_editado_a_mao_reprova(tmp_path):
    """A guarda falha quando deveria (regua 5-B, pergunta 4)."""
    with open(CE.CONTEUDO, encoding="utf-8") as f:
        c = yaml.safe_load(f)
    c["base"]["valor"] = c["base"]["valor"] + 100
    alvo = tmp_path / "conteudo.yaml"
    CE.gravar(c, str(alvo))
    assert "base.valor" in CE.conferir(str(alvo))


def test_brl_no_formato_brasileiro():
    assert CE.brl(800) == "R$\u00a0800,00"
    assert CE.brl(1213.33) == "R$\u00a01.213,33"
    assert CE.brl(0.22) == "R$\u00a00,22"


def test_a_faixa_do_parcial_sai_dos_dois_valores_declarados():
    """A faixa nao e inventada: min e max vem da tarifa e da divergencia do custos.yaml."""
    c = CE.gerar()
    p = c["base"]
    assert p["custo_compra_min"] < p["custo_compra_max"]
    assert "valor_alternativo" in p["custo_origem"]
    assert p["status"] == "PARCIAL", "S4: o selo e o do insumo, sem estado contrafactual"


def test_nenhum_numero_do_estado_yaml(monkeypatch):
    """D-01: o gerador nao le o estado.yaml. Se ele tentar abrir o arquivo, o teste quebra."""
    real = open

    def guarda(path, *a, **k):
        if str(path).endswith("estado.yaml"):
            pytest.fail("o gerador abriu o estado.yaml")
        return real(path, *a, **k)

    monkeypatch.setattr("builtins.open", guarda)
    import io as _io
    monkeypatch.setattr(_io, "open", guarda)
    CE.gerar()


def test_frases_da_camada_1_cabem_no_ri01():
    c = CE.gerar()
    for t in (c["base"]["frase_decisao"], c["base"]["porque"], c["com_rota_bloqueada"]["linha"]):
        assert len(t.split()) <= 15, t


def test_nenhum_ticker_do_catalogo_no_texto_gerado():
    """l-B: destino e rota bloqueada saem com rotulo generico, nunca com o ticker."""
    import re
    c = CE.gerar()
    textos = " ".join(str(v) for sec in ("base", "com_rota_bloqueada")
                      for k, v in c[sec].items() if k in ("frase_decisao", "destino", "linha"))
    tickers = {t for r in CE.catalogo(CE.carregar_custos())
               for t in re.findall(r"\b[A-Z]{4}\d{1,2}\b", r.nome)}
    assert tickers, "vacuidade: o catalogo tem de ter tickers"
    assert not [t for t in tickers if t in textos]


class _Rota:
    def __init__(self, i):
        self.id, self.bloqueios = i, [f"motivo de {i}"]


def _politica(ordens):
    return {"portoes": {g: {"fase": "universo", "ordem": o} for g, o in ordens.items()}}


def test_rota_bloqueada_segue_a_ordem_dos_portoes():
    saida = {"universo": {"fora_status": [_Rota("a")],
                          "fora_atrito": [(_Rota("b"), 0.02, "PERCENTUAL", None)]}}
    assert CE.rota_bloqueada(saida, _politica({"G5_status": 5, "G3_atrito": 6}))["rota_id"] == "a"


def test_mutacao_ordem_trocada_escolhe_outra_rota():
    """A guarda falha quando deveria: invertida a ordem no YAML, a rota escolhida muda."""
    saida = {"universo": {"fora_status": [_Rota("a")],
                          "fora_atrito": [(_Rota("b"), 0.02, "PERCENTUAL", None)]}}
    assert CE.rota_bloqueada(saida, _politica({"G5_status": 7, "G3_atrito": 6}))["rota_id"] == "b"


def test_sem_rota_eliminada_o_gerador_para():
    """j-A: se o motor nao rejeita nada, nao se inventa rota bloqueada."""
    with pytest.raises(SystemExit):
        CE.rota_bloqueada({"universo": {}}, _politica({"G5_status": 5}))
