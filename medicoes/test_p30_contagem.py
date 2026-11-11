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
    "por_variante": {"con": 2, "ind": 1},
    "uniao": {"C-01=1.25 C-03=0.75 C-05=0.5": {"avaliadas": 3, "pelo_menos_um": 1,
                                                "por_todos": 0}},
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
    assert texto.count("RESUMO: ") == 8                 # 3 pontos + 1 linha da uniao, por modo


def test_a_uniao_e_a_variante_lida_saem_no_relatorio_so_com_numero():
    """10/11/2026: os cortes se somam, e a contagem por corte nao mostrava. E 59 empresas eram
    lidas como "sem dado" por nao consolidarem: o relatorio passa a dizer quantas foram lidas
    em cada demonstrativo."""
    texto = M.relatorio({"dt_receb": CONTAGEM}, {})
    assert "lidas pelo demonstrativo: con=2, ind=1" in texto
    assert ("RESUMO: modo=dt_receb uniao C-01=1.25 C-03=0.75 C-05=0.5 pelo_menos_um=1 "
            "por_todos=0 (n=3 avaliadas, universo=5)") in texto


def test_o_cabecalho_diz_a_versao_que_cada_modo_leu(monkeypatch):
    """Rodada em 10/11 com data 24/10, a medicao imprimia para os dois modos o sha256 da versao
    MAIS RECENTE, e o modo da captura tinha lido a de 18/10. O cadastro e o mais recente nos
    dois (o universo e o de hoje)."""
    monkeypatch.setattr(M.L, "versao_em", lambda r, a, ate, repo=None: {"sha256": "data-" + a})
    monkeypatch.setattr(M.L, "versao_mais_recente", lambda r, a, repo=None: {"sha256": "hoje-" + a})
    P, ate = {"janela_de_exercicios": 1}, dt.date(2026, 10, 24)
    lidas = M.versoes_lidas(P, ate)
    assert lidas["captura"] == {"cad_cia_aberta.csv": "hoje-cad_cia_aberta.csv",
                                "dfp_cia_aberta_2025.zip": "data-dfp_cia_aberta_2025.zip"}
    assert lidas["dt_receb"]["dfp_cia_aberta_2025.zip"] == "hoje-dfp_cia_aberta_2025.zip"
    # o cache traz as duas versoes do DFP e o cadastro uma vez
    assert M.itens_do_cache(P, ate) == [
        ("cad", "cad_cia_aberta.csv", "hoje-cad_cia_aberta.csv"),
        ("dfp", "dfp_cia_aberta_2025.zip", "data-dfp_cia_aberta_2025.zip"),
        ("dfp", "dfp_cia_aberta_2025.zip", "hoje-dfp_cia_aberta_2025.zip")]


def test_os_insumos_sao_o_cadastro_e_a_janela_de_exercicios():
    ins = M._insumos({"janela_de_exercicios": 3}, dt.date(2026, 10, 24))
    assert ins == [("cad", "cad_cia_aberta.csv"), ("dfp", "dfp_cia_aberta_2025.zip"),
                   ("dfp", "dfp_cia_aberta_2024.zip"), ("dfp", "dfp_cia_aberta_2023.zip")]
