# -*- coding: utf-8 -*-
"""tools/testar.py: o mesmo recorte do CI, e o resumo que nao esconde falha."""
from __future__ import annotations

import os
import re
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import testar as T  # noqa: E402

SAIDA_VERMELHA = """\
....F..s
FAILED alocacao/test_x.py::test_a - AssertionError: 1 != 2
ERROR fase0/test_y.py - ImportError
=========== 1 failed, 6 passed, 1 skipped, 1 error in 3.21s ===========
"""


def test_resumo_pega_a_contagem_final_com_e_sem_moldura():
    assert T.resumo(SAIDA_VERMELHA) == "1 failed, 6 passed, 1 skipped, 1 error in 3.21s"
    quieto = "....\n812 passed, 3 deselected in 41.0s\n"
    assert T.resumo(quieto) == "812 passed, 3 deselected in 41.0s"


def test_mutacao_sem_linha_de_resumo_nao_vira_verde():
    """Coleta quebrada nao tem contagem: o resumo diz isso em vez de ficar em branco."""
    assert "sem linha de resumo" in T.resumo("ImportError: no module named x\n")


def test_falhas_traz_so_failed_e_error():
    assert T.falhas(SAIDA_VERMELHA) == [
        "FAILED alocacao/test_x.py::test_a - AssertionError: 1 != 2",
        "ERROR fase0/test_y.py - ImportError"]


def test_o_comando_e_o_do_ci():
    cmd = T.comando_pytest("fase0")
    assert cmd[cmd.index("-m", 3) + 1] == "not slow and not privado and not acervo"
    assert "--dist" in cmd and cmd[cmd.index("--dist") + 1] == "loadgroup"   # P-141


@pytest.mark.repositorio
def test_as_suites_e_o_marcador_sao_os_do_testes_yml():
    """Se o CI ganhar uma suite e o testar.py nao, o "verde" local passa a medir menos."""
    with open(os.path.join(T.RAIZ, ".github", "workflows", "testes.yml"), encoding="utf-8") as f:
        wf = f.read()
    rapido = wf.split("Suites sem slow", 1)[1].split("ruff e mypy", 1)[0]
    assert tuple(re.search(r"for s in ([\w ]+);", rapido).group(1).split()) == T.SUITES
    assert f'-m "{T.MARCADOR}"' in rapido


def test_tudo_tira_o_recorte_e_mantem_o_loadgroup():
    cmd = T.comando_pytest("fase0", None)
    assert "-m" not in cmd[3:] and "loadgroup" in cmd


def test_sem_q_extra_porque_o_addopts_ja_tem_um():
    """03/10: com `-q` aqui e no pyproject, o pytest roda em `-qq` e nao imprime a contagem."""
    assert "-q" not in T.comando_pytest("fase0")
