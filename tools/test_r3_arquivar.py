# -*- coding: utf-8 -*-
"""O arquivamento local da R3 (P-170): o que entra na fila e como o link sai da resposta."""
from __future__ import annotations

import csv
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import r3_arquivar as A  # noqa: E402
import r3_dominante as R  # noqa: E402


def _linha(**kw):
    base = {c: "" for c in R.COLUNAS}
    base.update(kw)
    return base


def test_so_entram_as_pendentes_com_url():
    linhas = [_linha(marca="a", url="https://a", arquivo_wayback=R.PENDENTE),
              _linha(marca="b", url="https://b", arquivo_wayback="https://web.archive.org/web/1/b"),
              _linha(marca="c", url="", arquivo_wayback=R.PENDENTE),
              _linha(marca="d", url="https://d", arquivo_wayback="")]
    assert A.pendentes(linhas) == [0]


def test_link_do_arquivamento():
    assert A.link_do_arquivamento("https://web.archive.org/save/x", "/web/20261004/https://x") == \
        "https://web.archive.org/web/20261004/https://x"
    assert A.link_do_arquivamento("https://web.archive.org/web/20261004/https://x", None) == \
        "https://web.archive.org/web/20261004/https://x"
    assert A.link_do_arquivamento("https://web.archive.org/save/x", None) is None


def test_gravar_mantem_o_cabecalho_da_r3(tmp_path):
    p = tmp_path / "c.csv"
    A.gravar([_linha(marca="a", situacao="pulada", motivo="x")], str(p))
    with open(p, encoding="utf-8", newline="") as f:
        assert csv.DictReader(f).fieldnames == R.COLUNAS


# ── 16/10/2026: o degrau 4a grava pelo resultado do executor (5-B.18) ────────────────────────

def _quatro():
    return [_linha(categoria_sorteada="bancos", ordem_no_sorteio="5", url="https://a",
                   arquivo_wayback=R.PENDENTE),
            _linha(categoria_sorteada="bancos", ordem_no_sorteio="6", url="https://b",
                   arquivo_wayback=R.PENDENTE, escada="1) curl 403"),
            _linha(categoria_sorteada="bancos", ordem_no_sorteio="7", url="https://c",
                   arquivo_wayback="https://web.archive.org/web/1/c")]


def test_aplicar_grava_o_link_e_a_recusa_leva_degrau_erro_e_proximo():
    linhas = _quatro()
    res = {"bancos:5": {"link": "https://web.archive.org/web/2/a", "erro": None},
           "bancos:6": {"link": None, "erro": "HTTPError: 429"},
           "bancos:7": {"link": None, "erro": "HTTPError: 520"}}
    assert A.aplicar(linhas, res, "4a) workflow (run 9)", "4c) sessao local") == (1, 1)
    assert linhas[0]["arquivo_wayback"] == "https://web.archive.org/web/2/a"
    assert linhas[1]["arquivo_wayback"] == R.PENDENTE
    assert linhas[1]["escada"] == ("1) curl 403; wayback 4a) workflow (run 9): HTTPError: 429; "
                                   "4c) sessao local")
    # um resultado velho nao desfaz o link ja gravado
    assert linhas[2]["arquivo_wayback"] == "https://web.archive.org/web/1/c"


def test_aplicar_recusa_link_que_nao_e_do_wayback_e_linha_que_nao_existe():
    with pytest.raises(ValueError):
        A.aplicar(_quatro(), {"bancos:5": {"link": "https://x.com/y"}}, "4a)", "4c)")
    with pytest.raises(KeyError):
        A.aplicar(_quatro(), {"bancos:99": {"link": None}}, "4a)", "4c)")


def test_aplicar_sem_degrau_ou_proximo_e_recusado(tmp_path):
    p = tmp_path / "r.json"
    p.write_text("{}", encoding="utf-8")
    with pytest.raises(SystemExit):
        A.main(["--aplicar", str(p), "--degrau", "4a)"])
