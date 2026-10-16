# -*- coding: utf-8 -*-
"""A medicao da P-183 sobre dado SINTETICO: a contagem de documento-meses ocultos."""
from __future__ import annotations

import datetime as dt
import os
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p183_dt_receb as M  # noqa: E402

D = dt.date.fromisoformat


def test_fins_de_mes_inclui_as_pontas():
    assert M.fins_de_mes(D("2024-05-10"), D("2024-08-31")) == [
        D("2024-05-31"), D("2024-06-30"), D("2024-07-31"), D("2024-08-31")]
    assert M.fins_de_mes(D("2024-05-31"), D("2024-05-31")) == [D("2024-05-31")]
    assert M.fins_de_mes(D("2024-12-15"), D("2025-01-31")) == [D("2024-12-31"), D("2025-01-31")]
    assert M.fins_de_mes(D("2024-06-01"), D("2024-06-29")) == []


def test_documento_de_duas_versoes_oculta_os_meses_entre_a_1a_e_a_presente():
    """1a versao em 10/05, 2a (presente) em 12/08: maio, junho e julho ocultos; agosto ja ve."""
    v = {"1": {D("2024-05-10")}, "2": {D("2024-08-12")}}
    assert M.meses_do_documento(v, "2", D("2024-09-30")) == (5, 3)
    # se a presente fosse a 1a, nada oculto (a mutacao do 'presente' sai aqui)
    assert M.meses_do_documento(v, "1", D("2024-09-30")) == (5, 0)


def test_versao_de_uma_so_nunca_oculta_e_duas_datas_fica_fora():
    assert M.meses_do_documento({"1": {D("2024-05-10")}}, "1", D("2024-06-30")) == (2, 0)
    assert M.meses_do_documento({"1": {D("2024-05-10"), D("2024-05-20")}}, "1") is None
    assert M.meses_do_documento({"1": {D("2024-05-10")}}, "2") is None


def _zip(tmp_path):
    cab_i = "CNPJ_CIA;DT_REFER;VERSAO;DENOM_CIA;CD_CVM;CATEG_DOC;ID_DOC;DT_RECEB;LINK_DOC\n"
    ind = cab_i + "".join(f"x;{r};{v};S;{cd};ITR;1;{d};\n" for cd, r, v, d in (
        ("000001", "2024-03-31", "1", "2024-05-10"), ("000001", "2024-03-31", "2", "2024-08-12"),
        ("000002", "2024-03-31", "1", "2024-05-15")))
    cab = "CNPJ_CIA;DT_REFER;VERSAO;CD_CVM;ORDEM_EXERC;CD_CONTA;VL_CONTA\n"
    dre = cab + "x;2024-03-31;2;000001;U;3.01;1\nx;2024-03-31;1;000002;U;3.01;1\n"
    p = tmp_path / "itr_cia_aberta_2024.zip"
    with zipfile.ZipFile(p, "w") as z:
        z.writestr("itr_cia_aberta_2024.csv", ind.encode("latin-1"))
        z.writestr("itr_cia_aberta_DRE_con_2024.csv", dre.encode("latin-1"))
    return str(p)


def test_medir_arquivo_conta_por_ano_e_por_demonstrativo(tmp_path, monkeypatch):
    """Dois documentos; o de duas versoes oculta mai/jun/jul de 2024. Horizonte 30/09/2024:
    5 + 5 documento-meses, 3 ocultos. O membro ausente e contado, nao ignorado."""
    monkeypatch.setattr(M, "HORIZONTE", D("2024-09-30"))
    ano, ocultos, dem = M.medir_arquivo(_zip(tmp_path), "itr", 2024)
    assert (ano["documentos"], ano["com_mais_de_uma_versao"], ano["documentos_com_mes_oculto"],
            ano["documento_meses"], ano["documento_meses_ocultos"]) == (2, 1, 1, 10, 3)
    assert ocultos == [3]
    assert (dem["DRE_con"]["documentos"], dem["DRE_con"]["documento_meses_ocultos"]) == (2, 3)
    assert dem["BPA_con"]["membro_ausente"] == 1


def test_relatorio_so_tem_contagem_e_rotulo(tmp_path, monkeypatch):
    """5-B.14: todo numero sai com o n; e nada de valor de conta na saida."""
    monkeypatch.setattr(M, "HORIZONTE", D("2024-09-30"))
    por = {("itr", 2024): M.medir_arquivo(_zip(tmp_path), "itr", 2024)}
    txt = M.relatorio(por, {("itr", 2024): "ab" * 32})
    assert "RESUMO: itr 2010-2025:" in txt and "| DRE_con | 2 |" in txt
    assert "3.01" not in txt
