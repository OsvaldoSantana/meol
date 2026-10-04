#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Os marcos auditaveis como tags anotadas (25/09/2026), e a guarda de que o texto e a tag
dizem a mesma coisa.

Um pre-registro vale pelo commit em que foi empurrado (P-116). A tag da nome a esse commit, e
a mensagem dela traz o sha256 do arquivo. Tres coisas podem se separar em silencio, e cada
uma tem um teste:
  - o PENDENCIAS cita uma tag que nao existe (escrita e nunca criada, ou apagada);
  - a tag existe e e leve (sem mensagem, portanto sem o sha256);
  - a mensagem da um sha256 que nao e o do arquivo no commit da tag.

ALCANCE (P5): so os nomes `prereg-*` sao reconhecidos como tag no texto. Um marco com outro
prefixo passa despercebido ate entrar aqui. No CI, as tags so existem porque o checkout do
workflow Testes usa `fetch-depth: 0`.
"""
from __future__ import annotations
import hashlib
import os
import re
import subprocess

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CITACAO = re.compile(r"\bprereg-[a-z0-9]+(?:-[a-z0-9]+)*\b")
SHA_NA_MENSAGEM = re.compile(r"^sha256: ([0-9a-f]{64})$", re.M)
ARQUIVO_NA_MENSAGEM = re.compile(r"^arquivo: (\S+)$", re.M)


def _git(*args):
    return subprocess.run(["git", *args], cwd=RAIZ, capture_output=True, text=True,
                          check=True, encoding="utf-8").stdout


def citadas(texto):
    return sorted(set(CITACAO.findall(texto)))


def faltando(texto, existentes):
    return [t for t in citadas(texto) if t not in set(existentes)]


def _existentes():
    return _git("tag", "-l", "prereg-*").split()


def test_faltando_acusa_a_tag_citada_e_nao_criada():
    texto = "marco `prereg-ml-v2` e `prereg-ml-v9-inexistente`."
    assert faltando(texto, ["prereg-ml-v2"]) == ["prereg-ml-v9-inexistente"]
    assert faltando("nenhuma tag aqui", []) == []


def test_toda_tag_citada_no_PENDENCIAS_existe():
    # 26/09: os marcos sairam para o historico com as pendencias fechadas; os dois contam.
    texto = ""
    for nome in ("PENDENCIAS.md", os.path.join("docs", "pendencias-reserva.md"),
                 os.path.join("docs", "historico", "pendencias-fechadas.md")):
        with open(os.path.join(RAIZ, nome), encoding="utf-8") as f:
            texto += f.read()
    assert citadas(texto), "o PENDENCIAS deixou de citar os marcos -- a guarda ficou muda"
    falta = faltando(texto, _existentes())
    assert not falta, f"citadas no PENDENCIAS e ausentes do repositorio: {falta}"


def test_toda_tag_de_marco_e_anotada_e_o_sha256_bate_com_o_arquivo():
    tags = _existentes()
    assert tags, "nenhuma tag prereg-* (no CI: o checkout precisa de fetch-depth: 0)"
    for t in tags:
        assert _git("cat-file", "-t", t).strip() == "tag", f"{t} e tag leve, sem mensagem"
        msg = _git("tag", "-l", "--format=%(contents)", t)
        arq, sha = ARQUIVO_NA_MENSAGEM.search(msg), SHA_NA_MENSAGEM.search(msg)
        assert arq and sha, f"{t}: a mensagem nao traz `arquivo:` e `sha256:`"
        conteudo = subprocess.run(["git", "show", f"{t}:{arq.group(1)}"], cwd=RAIZ,
                                  capture_output=True, check=True).stdout
        assert hashlib.sha256(conteudo).hexdigest() == sha.group(1), \
            f"{t}: o sha256 da mensagem nao e o de {arq.group(1)} no commit da tag"
