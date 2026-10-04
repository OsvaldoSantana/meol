# -*- coding: utf-8 -*-
"""O arquivamento local da R3 (P-170): o que entra na fila e como o link sai da resposta."""
from __future__ import annotations

import csv
import os
import sys

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
