# -*- coding: utf-8 -*-
"""O servidor local da pesquisa: o contador simulado gira como o do banco, e so serve a pagina."""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import servir_pesquisa as S  # noqa: E402


def test_contador_simulado_gira_pelas_versoes_como_o_do_banco():
    """(contador mod n) + 1, comecando em 0: a mesma regra de public.abrir_resposta()."""
    sim = S.Simulador()
    vs = [sim.abrir()["versao"] for _ in range(sim.n_versoes + 1)]
    assert vs == list(range(1, sim.n_versoes + 1)) + [1]
    assert len({a["id_resposta"] for a in sim.aberturas}) == len(vs)


def test_nao_serve_api_nem_supabase_nem_fora_da_pasta():
    sim = S.Simulador()
    assert sim.conteudo("/") is not None and sim.conteudo("/questionario.json") is not None
    for proibido in ("/api/_comum.js", "/supabase/esquema.sql", "/../pyproject.toml",
                     "/../tools/servir_pesquisa.py", "/vercel.json.bak"):
        assert sim.conteudo(proibido) is None, proibido


def test_ganchos_de_teste_so_quando_pedidos():
    limpo = S.Simulador()
    assert b"_auto.js" not in (limpo.conteudo("/") or b"")
    sim = S.Simulador(exposicao_segundos=2, script_injetado="// x")
    assert b"_auto.js" in (sim.conteudo("/") or b"")
    j = json.loads(sim.conteudo("/questionario.json") or b"{}")
    assert j["questionario"]["telas"]["exposicao_segundos"] == 2


def test_api_pelo_http():
    sim = S.Simulador()
    httpd, url = S.servir(sim)
    try:
        req = urllib.request.Request(url + "api/abrir", data=b"{}", method="POST")
        with urllib.request.urlopen(req, timeout=10) as r:
            assert json.loads(r.read())["versao"] == 1
        corpo = json.dumps({"id_resposta": "x"}).encode()
        req = urllib.request.Request(url + "api/enviar", data=corpo, method="POST")
        with urllib.request.urlopen(req, timeout=10) as r:
            assert r.status == 204
        assert sim.envios == [{"id_resposta": "x"}]
        with pytest.raises(urllib.error.HTTPError):
            urllib.request.urlopen(url + "supabase/esquema.sql", timeout=10)
    finally:
        httpd.shutdown()
