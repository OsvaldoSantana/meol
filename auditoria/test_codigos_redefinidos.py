# -*- coding: utf-8 -*-
"""Um codigo, um endereco: a auditoria do Codex de 03/10 com os nomes originais reprova.

Os testes de mutacao provam a guarda nos dois sentidos (regua 5-B, pergunta 4): a auditoria
com `A-01` a `A-03` reprova, e a mesma auditoria com CX-04 a CX-06 passa. E provam por que a
guarda e nova: o `achados_ancorados` fecha verde nos dois casos.
"""
from __future__ import annotations
import hashlib
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import achados_ancorados as A  # noqa: E402
import codigos_redefinidos as R  # noqa: E402

RAIZ = R.RAIZ
REGISTRO = "docs/auditoria/AUDITORIA-CODEX-2026-10-03.md"
DE_PARA = {"CX-04": "A-01", "CX-05": "A-02", "CX-06": "A-03"}


def _original():
    """O corpo registrado com a troca de nomes desfeita: o texto que chegou do Codex."""
    with open(os.path.join(RAIZ, REGISTRO), encoding="utf-8") as f:
        s = f.read()
    corpo = s.split("\n---\n\n", 1)[1]
    return s, re.sub(r"\bCX-0[456]\b", lambda m: DE_PARA[m.group(0)], corpo)


def test_nenhum_codigo_ganhou_definicao_num_arquivo_novo():
    base = R.ler_base()
    assert len(base) > 100, "vacuidade: a linha de base tem de existir"
    novos = R.novos(base, R.pares_em_colisao(R.definicoes()))
    assert not novos, (
        f"codigo(s) definido(s) num arquivo novo enquanto ja tinham definicao noutro: {novos}. "
        "Se e outro achado, de outro nome a ele; se e copia do mesmo, rode "
        "`python auditoria/codigos_redefinidos.py --gravar` e explique no PR.")


def test_a_linha_de_base_nao_guarda_par_resolvido():
    """So decresce: par que deixou de colidir sai, para a contagem nao esconder o proximo."""
    resolvidos = R.resolvidos(R.ler_base(), R.pares_em_colisao(R.definicoes()))
    assert not resolvidos, f"pares resolvidos ainda na linha de base: {resolvidos}"


def test_a_troca_de_nomes_e_reversivel_byte_a_byte():
    """O cabecalho do registro promete que desfazer a troca devolve o original. O sha256 dele
    esta no proprio cabecalho; o teste confere em vez de acreditar."""
    s, original = _original()
    sha = re.search(r"sha256 `([0-9a-f]{64})`", s).group(1)
    assert hashlib.sha256(original.encode("utf-8")).hexdigest() == sha
    assert not re.search(r"\bA-0[123]\b", s.split("\n---\n\n", 1)[1])


def test_mutacao_a_auditoria_com_os_nomes_originais_reprova():
    """O caso que criou a guarda, sobre a arvore real: os tres pares novos, e so eles."""
    _s, original = _original()
    defs = R.definicoes()
    for cod in R.definidos_no_texto(original):
        defs[cod].add(REGISTRO)
    novos = R.novos(R.ler_base(), R.pares_em_colisao(defs))
    assert novos == [("A-01", REGISTRO), ("A-02", REGISTRO), ("A-03", REGISTRO)]


def test_controle_a_auditoria_registrada_nao_colide():
    """Com CX, o codigo mora no registro da auditoria e, depois do conserto, no ACHADOS.md: a
    mesma coisa em dois lugares, gravada na linha de base no PR de cada conserto. Em lugar
    nenhum mais."""
    defs = R.definicoes()
    assert {"CX-04", "CX-05", "CX-06"} <= set(defs)
    for cod in ("CX-04", "CX-05", "CX-06"):
        assert REGISTRO in defs[cod] and defs[cod] <= {REGISTRO, "ACHADOS.md"}, (
            f"{cod} fora do registro e do ACHADOS.md: {defs[cod]}")


def test_o_achados_ancorados_nao_via_a_colisao(tmp_path):
    """Por que a guarda e nova: com os dois A-01, todo codigo citado tem endereco e o instrumento
    antigo fecha verde. O novo acusa o par."""
    (tmp_path / "ACHADOS.md").write_text("## A-01 · B3SA3 virou BSA\n", encoding="utf-8")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "AUDITORIA-X.md").write_text(
        "### A-01 — Valores que nao sao dinheiro\n", encoding="utf-8")
    (tmp_path / "x.py").write_text("# A-01: o motivo desta linha\n", encoding="utf-8")
    refs, defs, _ = A.varrer(str(tmp_path))
    assert A.orfaos(refs, defs) == {}
    assert R.novos(set(), R.pares_em_colisao(R.definicoes(str(tmp_path)))) == [
        ("A-01", "ACHADOS.md"), ("A-01", "docs/AUDITORIA-X.md")]


def test_pendencia_fica_fora_e_o_corte_esta_declarado(tmp_path):
    """P- muda de casa por rotina (ativas, reserva, fechadas): fora por prefixo, com motivo."""
    (tmp_path / "PENDENCIAS.md").write_text("## P-900 · algo\n", encoding="utf-8")
    (tmp_path / "historico.md").write_text("## ~~P-900~~ · algo, fechada\n", encoding="utf-8")
    assert R.pares_em_colisao(R.definicoes(str(tmp_path))) == set()
    assert "P" in R.PREFIXOS_FORA and R.PREFIXOS_FORA["P"]
