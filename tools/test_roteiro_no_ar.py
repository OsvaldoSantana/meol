# -*- coding: utf-8 -*-
"""O roteiro de por no ar e o commit das datas do teste de marca (P-162).

POR QUE EXISTE. Em 02/10 a y-a trocou o sha256 do `questionario.yaml` (73936c74 -> 02773d8b),
e o roteiro seguiu mandando conferir o antigo no banco: quem seguisse o passo 5 veria
"diverge" numa pagina certa, ou aceitaria o prefixo errado (retratacao de 04/10, eventos.csv).
E o commit das datas da janela (pre-registro final, sec. 6) e uma edicao a mao de duas linhas,
feita por ele, possivelmente pelo celular: um dia 21 contado errado passaria calado ate a analise.

O que se prende aqui:
1. todo prefixo de sha256 do questionario citado no roteiro e o do arquivo de hoje;
2. as duas linhas da janela ou estao "a preencher", ou trazem duas datas ISO com o dia 21
   exatamente 20 dias depois do dia 1 (21 dias corridos, os dois inclusive).
"""
from __future__ import annotations

import datetime as dt
import hashlib
import os
import re

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA = os.path.join(RAIZ, "docs", "marca", "teste-de-marca")
YAML = os.path.join(PASTA, "questionario.yaml")
ROTEIRO = os.path.join(PASTA, "roteiro-no-ar.md")
PRE = os.path.join(PASTA, "preregistro-final.md")

LINHA_DIA1 = re.compile(r"^\s*- dia 1 \(primeiro convite\): \*\*(?P<v>[^*]+)\*\*", re.M)
LINHA_DIA21 = re.compile(r"^\s*- dia 21 \(" "\u00faltimo" r" dia\): \*\*(?P<v>[^*]+)\*\*", re.M)
A_PREENCHER = "a preencher no commit das datas"


def _sha_do_questionario() -> str:
    with open(YAML, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def prefixos_citados(texto: str) -> list[str]:
    """Os prefixos que o passo 5 manda conferir: comeca com **`abcd1234`** (com cedilha)."""
    return re.findall("come\u00e7a com" r" \*\*`([0-9a-f]{8,64})`\*\*", texto)


def janela(texto_pre: str) -> tuple[str, str]:
    m1, m21 = LINHA_DIA1.search(texto_pre), LINHA_DIA21.search(texto_pre)
    if not m1 or not m21:
        raise AssertionError("as duas linhas da janela (sec. 6) sumiram ou mudaram de forma")
    return m1.group("v").strip(), m21.group("v").strip()


def problemas_da_janela(dia1: str, dia21: str) -> list[str]:
    if dia1 == A_PREENCHER and dia21 == A_PREENCHER:
        return []
    probs = []
    try:
        d1 = dt.date.fromisoformat(dia1)
        d21 = dt.date.fromisoformat(dia21.split(" ")[0])
    except ValueError:
        return [f"datas fora de AAAA-MM-DD: dia 1 {dia1!r}, dia 21 {dia21!r}"]
    if (d21 - d1).days != 20:
        probs.append(f"o dia 21 ({d21}) nao e o dia 1 ({d1}) + 20 dias: sao {(d21 - d1).days}")
    return probs


def test_o_roteiro_cita_o_sha256_do_questionario_de_hoje():
    with open(ROTEIRO, encoding="utf-8") as f:
        citados = prefixos_citados(f.read())
    assert citados, "o roteiro deixou de citar o sha256 do questionario no passo de conferencia"
    sha = _sha_do_questionario()
    for p in citados:
        assert sha.startswith(p), f"roteiro: {p}...; questionario: {sha[:8]}..."


def test_mutacao_prefixo_antigo_da_y_b_reprova():
    """O defeito de 02/10: o prefixo de antes da y-a."""
    texto = "a coluna `questionario_sha256` come\u00e7a com **`73936c74`**"
    assert prefixos_citados(texto) == ["73936c74"]
    assert not _sha_do_questionario().startswith("73936c74")


def test_a_janela_do_preregistro_esta_vazia_ou_coerente():
    with open(PRE, encoding="utf-8") as f:
        dia1, dia21 = janela(f.read())
    assert problemas_da_janela(dia1, dia21) == []


def test_mutacoes_da_janela():
    assert problemas_da_janela(A_PREENCHER, A_PREENCHER) == []
    assert problemas_da_janela("2026-10-08", "2026-10-28") == []
    assert problemas_da_janela("2026-10-08", "2026-10-28 (ate 23:59 de Brasilia)") == []
    assert problemas_da_janela("2026-10-08", "2026-10-29")       # contou 21 dias depois
    assert problemas_da_janela("2026-10-08", "2026-10-27")
    assert problemas_da_janela("08/10/2026", "28/10/2026")       # formato brasileiro
    assert problemas_da_janela("2026-10-08", A_PREENCHER)        # so uma das duas
