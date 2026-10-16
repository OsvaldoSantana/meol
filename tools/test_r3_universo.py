# -*- coding: utf-8 -*-
"""O universo e o sorteio da R3 sobre cadastros SINTETICOS, e a conferencia com os reais quando
estao nesta maquina (data/r3/, fora do git)."""
from __future__ import annotations

import hashlib
import io
import json
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
    livro = set(__import__("codigos_visuais").ler_livro()["veto"]["categorias_concorrentes"])
    # 10/10/2026: um universo pode alimentar mais de uma categoria (`bancos` -> tradicional e
    # digital); o que tem de estar no livro e cada categoria que ele alimenta
    alimentadas = {c for nome, u in p["universos"].items() for c in u.get("categorias", [nome])}
    assert alimentadas <= livro
    assert U.COLUNAS == ["ordem", "cnpj", "nome", "site_declarado"]


def test_sorteios_gravados_conferem_com_os_cadastros_reais():
    """So nesta maquina: com os ZIP de data/r3/ (sha256 do plano), o gravado e o que sai."""
    p = U.ler_plano()
    faltam = [f["arquivo_local"] for f in p["fontes"].values()
              if not os.path.isfile(os.path.join(U.RAIZ, *f["arquivo_local"].split("/")))]
    if faltam:
        pytest.skip(f"cadastros da CVM fora desta maquina: {faltam}")
    assert U.main(["--conferir"]) == 0


# ── as fontes de 10/10/2026: JSON do BCB e planilha da APIMEC ───────────────────────────────

def _xlsx(linhas):
    """Um .xlsx minimo, SINTETICO: texto em sharedStrings, numero em <v>. `linhas` e uma lista
    de {letra: valor}; valor str vai para sharedStrings, int/float vai direto."""
    textos, xml_linhas = [], []
    for n, ln in enumerate(linhas, start=1):
        cel = []
        for letra, v in ln.items():
            if isinstance(v, str):
                textos.append(v)
                cel.append(f'<c r="{letra}{n}" t="s"><v>{len(textos) - 1}</v></c>')
            else:
                cel.append(f'<c r="{letra}{n}"><v>{v}</v></c>')
        xml_linhas.append(f'<row r="{n}">{"".join(cel)}</row>')
    ns = 'xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"'
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("xl/sharedStrings.xml",
                   f'<sst {ns}>' + "".join(f"<si><t>{x}</t></si>" for x in textos) + "</sst>")
        z.writestr("xl/worksheets/sheet1.xml",
                   f'<worksheet {ns}><sheetData>{"".join(xml_linhas)}</sheetData></worksheet>')
    return buf.getvalue()


def test_planilha_le_texto_numero_e_celula_vazia_pela_letra():
    dados = _xlsx([{"A": "Razao", "B": "Fantasia", "C": "Registro"},
                   {"A": "ACME LTDA", "B": "Acme", "C": 7}, {"A": "SO RAZAO", "C": 11}])
    linhas = U.ler_planilha(dados)
    assert linhas[0] == {"A": "Razao", "B": "Fantasia", "C": "Registro"}
    assert linhas[1] == {"A": "ACME LTDA", "B": "Acme", "C": "7"}
    assert "B" not in linhas[2]


def test_registros_filtram_por_onde_exigem_site_e_guardam_um_identificador_uma_vez():
    u = {"chave": "CNPJ", "nome": "NOME", "coluna_site": "SITIO", "onde": {"CART": "Sim"}}
    linhas = [{"CNPJ": "1", "NOME": "A", "SITIO": "www.a.com", "CART": "Sim"},
              {"CNPJ": "1", "NOME": "A2", "SITIO": "www.a2.com", "CART": "Sim"},
              {"CNPJ": "2", "NOME": "B", "SITIO": "www.b.com", "CART": "Nao"},
              {"CNPJ": "3", "NOME": "C", "SITIO": None, "CART": "Sim"},
              {"CNPJ": "4", "NOME": "D", "SITIO": "ouv@d.com", "CART": "Sim"},
              {"CNPJ": "", "NOME": "E", "SITIO": "www.e.com", "CART": "Sim"}]
    assert U.universo_registros(linhas, u) == [
        {"cnpj": "1", "nome": "A", "site_declarado": "www.a.com"}]


def test_fonte_sem_site_entra_inteira_com_o_site_vazio_e_o_prefixo_no_identificador():
    """A APIMEC nao publica site nem CNPJ: o filtro 'so quem declara site' nao se aplica ao
    cadastro, e quem nao tem site que se ache cai na visita, nao no sorteio."""
    u = {"chave": "C", "prefixo_chave": "APIMEC-", "zeros": 3, "nome": "B",
         "nome_alternativo": "A", "coluna_site": None, "onde": {"F": "CREDENCIADO"}}
    linhas = [{"A": "ACME LTDA", "B": "Acme", "C": "7", "F": "CREDENCIADO"},
              {"A": "SO RAZAO LTDA", "B": "", "C": "11", "F": "CREDENCIADO"},
              {"A": "PARADA", "B": "Parada", "C": "12", "F": "LICENCIADO"}]
    # `zeros` faz "7" e "11" ordenarem como numero quando o identificador e comparado como texto
    assert U.universo_registros(linhas, u) == [
        {"cnpj": "APIMEC-007", "nome": "Acme", "site_declarado": ""},
        {"cnpj": "APIMEC-011", "nome": "SO RAZAO LTDA", "site_declarado": ""}]


def test_universos_despacha_pelo_tipo_e_so_le_o_que_foi_pedido(tmp_path, monkeypatch):
    dados = json.dumps([{"CNPJ": "9", "NOME": "Z", "SITIO": "www.z.com"}]).encode()
    (tmp_path / "x.json").write_bytes(dados)
    monkeypatch.setattr(U, "RAIZ", str(tmp_path))
    plano = {"fontes": {"f": {"arquivo_local": "x.json",
                              "sha256": hashlib.sha256(dados).hexdigest()},
                        "g": {"arquivo_local": "nao_existe.json", "sha256": "0" * 64}},
             "universos": {"a": {"tipo": "json", "fonte": "f", "chave": "CNPJ", "nome": "NOME",
                                 "coluna_site": "SITIO"},
                           "b": {"tipo": "json", "fonte": "g", "chave": "CNPJ", "nome": "NOME",
                                 "coluna_site": "SITIO"}}}
    assert U.universos(plano, so=["a"]) == {
        "a": [{"cnpj": "9", "nome": "Z", "site_declarado": "www.z.com"}]}
    with pytest.raises(FileNotFoundError):       # sem `so`, o arquivo que falta aparece
        U.universos(plano)


def test_json_com_sha256_diferente_e_recusado(tmp_path, monkeypatch):
    (tmp_path / "x.json").write_text("[]")
    monkeypatch.setattr(U, "RAIZ", str(tmp_path))
    with pytest.raises(SystemExit, match="sha256"):
        U._json({"arquivo_local": "x.json", "sha256": "0" * 64})


def test_ordem_confere_pega_arquivo_editado_e_semente_trocada():
    u = [{"cnpj": f"{i:03d}", "nome": f"n{i}", "site_declarado": "x.com"} for i in range(30)]
    texto = U.texto_csv(U.sortear(u, 20261002))
    assert U.ordem_confere(texto, 20261002)
    assert not U.ordem_confere(texto, 1)
    linhas = texto.splitlines()
    trocado = "\n".join([linhas[0], linhas[2], linhas[1], *linhas[3:]]) + "\n"
    assert not U.ordem_confere(trocado, 20261002)


@pytest.mark.repositorio   # 146b: le o repositorio, a mutacao exclui
def test_todo_sorteio_gravado_e_a_permutacao_da_semente():
    """Sem precisar do cadastro bruto: vale nesta maquina, no CI e em qualquer clone. O sorteio
    e o pre-registro da amostra (P-170); um arquivo editado a mao ou gravado com outra semente
    muda quem e visitado primeiro."""
    nomes = [n for n in os.listdir(U.PASTA) if n.startswith("sorteio-") and n.endswith(".csv")]
    assert len(nomes) >= 4, "os quatro sorteios de 02/10 deveriam existir"
    semente = U.ler_plano()["semente"]
    for nome in nomes:
        with open(os.path.join(U.PASTA, nome), encoding="utf-8") as f:
            assert U.ordem_confere(f.read(), semente), nome
