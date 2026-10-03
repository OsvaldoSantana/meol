# -*- coding: utf-8 -*-
"""O universo e o sorteio da R3 sobre cadastros SINTETICOS, e a conferencia com os reais quando
estao nesta maquina (data/r3/, fora do git)."""
from __future__ import annotations

import io
import os
import sys
import zipfile

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r3_universo as U  # noqa: E402

EF = U.EM_FUNCIONAMENTO


def _linha(cnpj, sit=EF, site="www.exemplo.com.br", **kw):
    return {"CNPJ": cnpj, "SIT": sit, "SITE_ADMIN": site, "DENOM_COMERC": f"M{cnpj}",
            "DENOM_SOCIAL": "", **kw}


def test_universo_so_em_funcionamento_com_site_e_um_cnpj_uma_vez():
    linhas = [_linha("1"), _linha("1"), _linha("2", sit="CANCELADA"), _linha("3", site=""),
              _linha("4", site="contato@empresa.com.br"), _linha("5", site="www.cvm.gov.br"),
              _linha("6", site="nao possui"), _linha("7", site="https://marca.com")]
    u = U.universo_cadastro(linhas, "SITE_ADMIN")
    assert [r["cnpj"] for r in u] == ["1", "7"]


def test_universo_filtra_tipo_de_intermediario():
    linhas = [_linha("1", TP_PARTIC="CORRETORAS"), _linha("2", TP_PARTIC="CUSTODIANTES")]
    assert [r["cnpj"] for r in U.universo_cadastro(linhas, "SITE_ADMIN", ["CORRETORAS"])] == ["1"]


def test_gestoras_cruzam_cnpj_com_e_sem_pontuacao():
    """O cadastro de fundos grava so digitos; o de administradores, com pontuacao. Sem a
    normalizacao o universo dava zero (achado na propria S-R3, 02/10)."""
    fundos = [{"Situacao": "Em Funcionamento Normal", "Tipo_Pessoa_Gestor": "PJ",
               "CPF_CNPJ_Gestor": "12345678000190"},
              {"Situacao": "Cancelado", "Tipo_Pessoa_Gestor": "PJ",
               "CPF_CNPJ_Gestor": "99999999000199"}]
    adm = [_linha("12.345.678/0001-90"), _linha("99.999.999/0001-99")]
    u = U.universo_gestoras(fundos, "Em Funcionamento Normal", adm, "SITE_ADMIN")
    assert [r["cnpj"] for r in u] == ["12.345.678/0001-90"]


def test_sorteio_deterministico_e_independente_da_ordem_de_entrada():
    u = [{"cnpj": str(i), "nome": f"n{i}", "site_declarado": "x.com"} for i in range(30)]
    a = U.sortear(u, 20261002)
    b = U.sortear(list(reversed(u)), 20261002)
    assert a == b and [r["ordem"] for r in a] == [str(i) for i in range(1, 31)]
    assert U.sortear(u, 1) != a
    assert sorted(r["cnpj"] for r in a) == sorted(r["cnpj"] for r in u)


def test_arquivo_com_sha256_diferente_e_recusado(tmp_path, monkeypatch):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("x.csv", "CNPJ;SIT\n1;EM FUNCIONAMENTO NORMAL\n")
    (tmp_path / "x.zip").write_bytes(buf.getvalue())
    monkeypatch.setattr(U, "RAIZ", str(tmp_path))
    with pytest.raises(SystemExit, match="sha256"):
        U._membro({"arquivo_local": "x.zip", "sha256": "0" * 64}, "x.csv")


def test_plano_le_a_amostra_e_a_semente_e_nao_copia_contato():
    p = U.ler_plano()
    assert isinstance(p["semente"], int)
    assert set(p["universos"]) <= set(__import__("codigos_visuais").ler_livro()["veto"]
                                      ["categorias_concorrentes"])
    assert U.COLUNAS == ["ordem", "cnpj", "nome", "site_declarado"]


def test_sorteios_gravados_conferem_com_os_cadastros_reais():
    """So nesta maquina: com os ZIP de data/r3/ (sha256 do plano), o gravado e o que sai."""
    p = U.ler_plano()
    faltam = [f["arquivo_local"] for f in p["fontes"].values()
              if not os.path.isfile(os.path.join(U.RAIZ, *f["arquivo_local"].split("/")))]
    if faltam:
        pytest.skip(f"cadastros da CVM fora desta maquina: {faltam}")
    assert U.main(["--conferir"]) == 0
