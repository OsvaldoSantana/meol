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
    c["normal"]["valor"] = c["normal"]["valor"] + 100
    alvo = tmp_path / "conteudo.yaml"
    CE.gravar(c, str(alvo))
    assert "normal.valor" in CE.conferir(str(alvo))


def test_brl_no_formato_brasileiro():
    assert CE.brl(800) == "R$ 800,00"
    assert CE.brl(1213.33) == "R$ 1.213,33"
    assert CE.brl(0.22) == "R$ 0,22"


def test_a_faixa_do_parcial_sai_dos_dois_valores_declarados():
    """A faixa nao e inventada: min e max vem da tarifa e da divergencia do custos.yaml."""
    c = CE.gerar()
    p = c["parcial"]
    assert p["custo_compra_min"] < p["custo_compra_max"]
    assert "valor_alternativo" in p["faixa_origem"]


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
    c = CE.gerar()["normal"]
    assert len(c["frase_decisao"].split()) <= 15
    assert len(c["porque"].split()) <= 15
