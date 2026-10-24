# -*- coding: utf-8 -*-
"""Testes das funcoes puras de medicoes/p30_contagem.py (o acervo real nao entra: P-136)."""
from __future__ import annotations

import datetime as dt
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import p30_contagem as M  # noqa: E402

CONTAGEM = {
    "universo_total": 5,
    "regime": {"RECUSA_REGIME": 1, "EXIGE_DOSSIE": 0},
    "sem_dado": 1,
    "nao_implementadas": ["C-02"],
    "cortes": {"C-01": {"grade": {"1.25": 0, "2.0": 1, "3.0": 2}, "com_valor": 3,
                        "indefinido": 0, "plano_diferente": 0, "sem_dado": 1}},
}


def test_o_universo_e_ativo_e_categoria_A(tmp_path):
    p = tmp_path / "cad.csv"
    p.write_bytes(("CD_CVM;SIT;CATEG_REG\n1;ATIVO;Categoria A\n2;ATIVO;Categoria B\n"
                   "3;CANCELADA;Categoria A\n4;ATIVO;\n5;ATIVO;Categoria A\n").encode("latin-1"))
    assert M.universo_do_cadastro(str(p)) == {1, 5}


def test_o_relatorio_so_tem_contagem_e_rotulo():
    texto = M.relatorio({"captura": CONTAGEM}, {"data": "2026-10-24"})
    assert "RESUMO: modo=captura C-01 ponto=2.0 sairiam=1 (n=3 com valor, universo=5)" in texto
    assert "C-02" in texto and "nao implementadas: C-02" in texto
    for proibido in ("cd_cvm", "CD_CVM ", "preco", "Bancos"):
        assert proibido not in texto


def test_cada_ponto_da_grade_vira_uma_linha_RESUMO():
    texto = M.relatorio({"captura": CONTAGEM, "dt_receb": CONTAGEM}, {})
    assert texto.count("RESUMO: ") == 6


def test_os_insumos_sao_o_cadastro_e_a_janela_de_exercicios():
    ins = M._insumos({"janela_de_exercicios": 3}, dt.date(2026, 10, 24))
    assert ins == [("cad", "cad_cia_aberta.csv"), ("dfp", "dfp_cia_aberta_2025.zip"),
                   ("dfp", "dfp_cia_aberta_2024.zip"), ("dfp", "dfp_cia_aberta_2023.zip")]
