# -*- coding: utf-8 -*-
"""(i) O que a pagina e o banco leem sai do questionario pre-registrado, e o sha256 confere (S6)."""
from __future__ import annotations

import hashlib
import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import questionario_json as G  # noqa: E402
from analise_teste_marca import colunas_esperadas  # noqa: E402

PREREGISTRO = os.path.join(G.RAIZ, "docs", "marca", "teste-de-marca", "preregistro-final.md")


def _gravados_no_preregistro() -> dict[str, str]:
    par = re.compile(r"`((?:docs|tools)/[^`]+)`.*?`([0-9a-f]{64})`")
    with io.open(PREREGISTRO, encoding="utf-8") as f:
        return {m.group(1): m.group(2) for m in map(par.search, f.read().splitlines()) if m}


def _json() -> dict:
    with open(G.JSON, encoding="utf-8") as f:
        d: dict = json.load(f)
    return d


def test_gerados_batem_com_o_gerador():
    """--conferir: JSON, PNG, esquema e exportacao iguais ao que o YAML produz hoje."""
    assert G.conferir() == []
    assert G.main(["--conferir"]) == 0


def test_sha256_do_questionario_e_o_do_preregistro():
    gravado = _gravados_no_preregistro()["docs/marca/teste-de-marca/questionario.yaml"]
    with open(G.YAML, "rb") as f:
        assert hashlib.sha256(f.read()).hexdigest() == gravado
    assert _json()["questionario_sha256"] == gravado


def test_estimulos_copiados_sao_os_png_aprovados():
    """As copias em pesquisa/estimulos/ tem o sha256 que o pre-registro congela (i-A)."""
    gravados = _gravados_no_preregistro()
    j = _json()
    for destino, origem in j["estimulos_origem"].items():
        with open(os.path.join(G.PESQUISA, *destino.split("/")), "rb") as f:
            assert hashlib.sha256(f.read()).hexdigest() == gravados[origem], destino
        assert j["estimulos_sha256"][destino] == gravados[origem]


def test_o_json_e_o_yaml_com_so_os_caminhos_dos_estimulos_trocados():
    q = G.ler_yaml()
    j = _json()["questionario"]
    assert j["telas"]["estimulos"]["E"]["base"] == "estimulos/E-base.png"
    j["telas"]["estimulos"] = q["telas"]["estimulos"]
    assert j == json.loads(json.dumps(q, default=str))


def test_mutacao_yaml_mudado_o_json_gravado_diverge(tmp_path):
    """Uma virgula a mais numa pergunta muda o JSON e o sha256: a pagina nao fica com a antiga."""
    with open(G.YAML, encoding="utf-8") as f:
        texto = f.read()
    outro = tmp_path / "q.yaml"
    outro.write_text(texto.replace("parece honesta?", "parece, honesta?"), encoding="utf-8")
    novo = G.gerar_json(str(outro))
    assert novo["questionario_sha256"] != _json()["questionario_sha256"]
    assert G.texto_json(novo) != G.texto_json(G.gerar_json())


def test_exportacao_tem_exatamente_as_colunas_da_analise():
    """O select do exportar.sql devolve as colunas do contrato, na ordem que a analise exige."""
    with open(G.EXPORTAR, encoding="utf-8") as f:
        sql = f.read()
    corpo = sql.split("select", 1)[1].split("from public.aberturas", 1)[0]
    nomes = [re.split(r"\s+as\s+|\.", linha.strip().rstrip(","))[-1]
             for linha in corpo.strip().splitlines()]
    assert nomes == colunas_esperadas(G.ler_yaml())


def test_envio_e_o_contrato_menos_o_que_o_banco_preenche():
    envio = G.colunas_de_envio(G.ler_yaml())
    assert "questionario_sha256" in envio and "id_resposta" in envio
    assert not {"versao", "aberta_em", "concluida_em"} & set(envio)
