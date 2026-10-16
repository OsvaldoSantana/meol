#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""degrau4.py -- a maquina dele so e proximo executor depois dos executores de nuvem (5-B.18).

POR QUE EXISTE. Em 16/10/2026 a R3 de marcas tinha 83 linhas `AGUARDA DEGRAU 4`: o site recusou
o IP da nuvem, e a linha parou esperando a maquina dele. Nenhuma tentou o executor que nao
depende dele (o workflow no servidor do GitHub), e a maioria das marcas tinha app, que e a
unidade do livro (ae-a) -- o site nem era o que se classificava (EX-01, EX-02). A regra nova poe o
degrau 4 em ordem: 4a o workflow de captura, 4b o runner br-sp quando existir, 4c a sessao local.
Esta e a guarda dela.

O QUE REPROVA.
  1. `AGUARDA DEGRAU 4` em qualquer linha do classificacao.csv ou do leituras.yaml da R3: o
     status que estaciona sem dizer em qual executor.
  2. Linha da R3 que poe a maquina dele no degrau 4 (`4c)`, "maquina dele", "sessao local", "IP
     dele") sem `4a)` e `4b)` transcritos na `escada`.
  3. Linha da R3 com `AGUARDA_EXECUTOR_NUVEM` sem `proximo executor:` na `escada`.
  4. Item da secao "Ao voltar ao desktop" do PENDENCIAS.md que manda a sessao local subir o
     degrau 4 (degrau 4, IP residencial, IP dele) sem `4a` e `4b`. A linha de base
     (`auditoria/degrau4_linha_de_base.txt`) guarda os itens anteriores a regra, pela chave do
     conteudo; ela so encolhe, como a da escada_contorno.

ALCANCE (o que NAO ve):
  - so a R3 (classificacao.csv e leituras.yaml) e a secao "Ao voltar ao desktop"; uma pendencia
    que estaciona na maquina dele em outro arquivo (ACHADOS, pesquisa) passa;
  - nao confere que o 4a foi de fato tentado: confere que esta transcrito. O run do workflow e a
    prova, e o numero dele vai na linha;
  - "maquina dele" escrito de outro jeito ("desktop", "PC do Osvaldo") passa.

    python auditoria/degrau4.py            # lista o que reprova; sai 1 se houver
"""
from __future__ import annotations

import csv
import hashlib
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R3 = os.path.join(RAIZ, "docs", "marca", "rodada3")
CSV = os.path.join(R3, "classificacao.csv")
LEITURAS = os.path.join(R3, "leituras.yaml")
PENDENCIAS = os.path.join(RAIZ, "PENDENCIAS.md")
BASE = os.path.join(RAIZ, "auditoria", "degrau4_linha_de_base.txt")

ESTACIONA = "AGUARDA DEGRAU 4"
AGUARDA_NUVEM = "AGUARDA_EXECUTOR_NUVEM"
LOCAL = re.compile(r"4c\)|m[aá]quina dele|sess[aã]o local|\bIP dele\b|IP residencial",
                   re.IGNORECASE)
TEM_4A = re.compile(r"\b4a\)")
TEM_4B = re.compile(r"\b4b\)")
PROXIMO = re.compile(r"pr[oó]ximo executor:", re.IGNORECASE)
SECAO_DESKTOP = "## Ao voltar ao desktop"
ITEM_LOCAL = re.compile(r"degrau 4|IP residencial|\bIP dele\b", re.IGNORECASE)
TEM_4A_4B_TEXTO = re.compile(r"\b4a\b.*\b4b\b", re.IGNORECASE | re.DOTALL)


def chave(linha: str) -> str:
    return hashlib.sha256(linha.strip().encode("utf-8")).hexdigest()[:12]


def problemas_da_linha(r: dict[str, str]) -> list[str]:
    """Os problemas de uma linha do classificacao.csv (regras 1 a 3)."""
    texto = f"{r.get('motivo', '')} {r.get('escada', '')}"
    escada = r.get("escada", "")
    out = []
    if ESTACIONA in texto:
        out.append("AGUARDA DEGRAU 4: diga em qual executor (4a, 4b, 4c) a linha parou")
    if LOCAL.search(escada) and not (TEM_4A.search(escada) and TEM_4B.search(escada)):
        out.append("a maquina dele no degrau 4 sem 4a) e 4b) transcritos na escada")
    if AGUARDA_NUVEM in texto and not PROXIMO.search(escada):
        out.append(f"{AGUARDA_NUVEM} sem 'proximo executor:' na escada")
    return out


def varrer_csv(caminho: str = CSV) -> list[str]:
    with open(caminho, encoding="utf-8", newline="") as f:
        linhas = list(csv.DictReader(f))
    out = []
    for i, r in enumerate(linhas, start=2):
        for p in problemas_da_linha(r):
            out.append(f"classificacao.csv:{i} ({r['categoria_sorteada']}:"
                       f"{r['ordem_no_sorteio']} {r['marca']}): {p}")
    return out


def varrer_texto_estaciona(caminho: str, rotulo: str) -> list[str]:
    with open(caminho, encoding="utf-8") as f:
        return [f"{rotulo}:{n}: {ESTACIONA}" for n, linha in enumerate(f, start=1)
                if ESTACIONA in linha]


def itens_da_secao_desktop(texto: str) -> list[tuple[int, str]]:
    """(linha, texto do item) de cada item numerado da secao 'Ao voltar ao desktop'."""
    linhas = texto.splitlines()
    try:
        ini = next(i for i, x in enumerate(linhas) if x.startswith(SECAO_DESKTOP))
    except StopIteration:
        return []
    itens: list[tuple[int, str]] = []
    for i in range(ini + 1, len(linhas)):
        x = linhas[i]
        if x.startswith("## "):
            break
        if re.match(r"^\d+\. ", x):
            itens.append((i + 1, x))
        elif itens and x.startswith("   ") and x.strip():
            n, t = itens[-1]
            itens[-1] = (n, t + " " + x.strip())
    return itens


def violacoes_desktop(texto: str) -> list[tuple[int, str]]:
    return [(n, t) for n, t in itens_da_secao_desktop(texto)
            if ITEM_LOCAL.search(t) and not TEM_4A_4B_TEXTO.search(t)]


def ler_base(caminho: str = BASE) -> dict[str, str]:
    base = {}
    with open(caminho, encoding="utf-8") as f:
        for n, bruta in enumerate(f, start=1):
            if not bruta.strip() or bruta.startswith("#"):
                continue
            partes = [p.strip() for p in bruta.split("|", 1)]
            if len(partes) != 2 or not partes[1]:
                raise ValueError(f"{caminho}:{n}: esperado 'chave | motivo'")
            base[partes[0]] = partes[1]
    return base


def varrer_pendencias(caminho: str = PENDENCIAS, base: dict[str, str] | None = None
                      ) -> tuple[list[str], list[str]]:
    base = ler_base() if base is None else base
    with open(caminho, encoding="utf-8") as f:
        texto = f.read()
    vistas, novas = set(), []
    for n, t in violacoes_desktop(texto):
        k = chave(t)
        if k in base:
            vistas.add(k)
        else:
            novas.append(f"PENDENCIAS.md:{n} ({k}): {t[:140]}")
    velhas = [f"{k} | {m}" for k, m in base.items() if k not in vistas]
    return novas, velhas


def varrer() -> list[str]:
    novas, velhas = varrer_pendencias()
    return (varrer_csv() + varrer_texto_estaciona(LEITURAS, "leituras.yaml") + novas
            + [f"BASE VELHA {v}" for v in velhas])


def main() -> int:
    probs = varrer()
    for p in probs:
        print(p)
    print(f"{len(probs)} problema(s) no degrau 4")
    return 1 if probs else 0


if __name__ == "__main__":
    sys.exit(main())
