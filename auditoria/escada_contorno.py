#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""escada_contorno.py -- NAO_CONFIRMADO por falta de acesso so com a escada (CLAUDE.md 5-B.18).

POR QUE EXISTE. As regras 5-B.13 ("nao da" so depois de tentar) e 5-B.17 (limitacao da
ferramenta nao e da tarefa) se cumpriam com "tentei, deu 403, parei". Em 27/09/2026, tres
NAO_CONFIRMADO do repositorio cairam no primeiro degrau da escada: a API PTAX do BCB
respondeu 200 ao curl, o cabecalho do cad_fi da CVM veio num curl com Range, e o JSON do PyPI
disse que o tabpfn traz torch. A regra virou escada; esta e a guarda dela.

O QUE REPROVA. Uma linha de .md que tenha NAO_CONFIRMADO (ou NAO CONFIRMADO, com ou sem til)
junto de um motivo de acesso (403, bloqueado/a, bloqueia robo, robots, recusou, sem acesso,
nao acessivel, PERMISSIONS_ERROR, EGRESS_BLOCKED) e que nao traga `escada:` nem um codigo
P-nnn de pendencia. Texto riscado (~~...~~) nao conta: e retratacao (5-A.4).

A LINHA DE BASE. `auditoria/escada_linha_de_base.txt`: as linhas antigas legitimas, uma por
linha, `caminho | sha256[:12] da linha | motivo`. A chave e o CONTEUDO da linha, nao o numero:
editar a linha a tira da base, e ela precisa de escada ou de motivo novo. Item da base que nao
casa com mais nenhuma linha tambem reprova: a base so encolhe.

ALCANCE (o que NAO ve):
  - so .md rastreados ou nao ignorados pelo git. YAML e .py ficam fora: em 27/09 havia 21
    linhas de YAML com o mesmo padrao (12 em docs/marca/tokens/direcoes.yaml, da S4: os 11
    bancos e o comentario do metodo), contadas com uma janela de 3 linhas -- ver a P-169;
  - so a MESMA linha: NAO_CONFIRMADO numa linha e "403" na seguinte passam;
  - "nao confirmado" em minuscula (prosa) passa; a guarda olha o status, nao a prosa;
  - motivo de acesso fora da lista (500, timeout, CAPTCHA) passa.

    python auditoria/escada_contorno.py            # lista o que reprova; sai 1 se houver
"""
from __future__ import annotations

import hashlib
import os
import re
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(RAIZ, "auditoria", "escada_linha_de_base.txt")

NAO_CONFIRMADO = re.compile(r"N[A\u00c3]O[_ ]CONFIRMADO")
MOTIVO_DE_ACESSO = re.compile(
    r"\b403\b|bloquead|bloqueia rob|robots|recusou|sem acesso|n[a\u00e3]o acess[i\u00ed]vel"
    r"|permissions_error|egress_blocked", re.IGNORECASE)
TEM_ESCADA = re.compile(r"escada:|\bP-\d{2,4}\b")
RISCADO = re.compile(r"~~.*?~~", re.DOTALL)


def arquivos_md(raiz: str = RAIZ) -> list[str]:
    """Os .md que o git rastreia ou que ainda nao foram adicionados mas nao sao ignorados."""
    r = subprocess.run(["git", "-C", raiz, "ls-files", "--cached", "--others",
                        "--exclude-standard", "*.md"], capture_output=True, text=True, check=True)
    return sorted(set(r.stdout.split()))


def sem_riscado(texto: str) -> str:
    """Troca o texto riscado por espacos, mantendo as quebras (os numeros de linha nao mudam)."""
    return RISCADO.sub(lambda m: re.sub(r"[^\n]", " ", m.group(0)), texto)


def chave(linha: str) -> str:
    return hashlib.sha256(linha.strip().encode("utf-8")).hexdigest()[:12]


def violacoes_no_texto(texto: str) -> list[tuple[int, str]]:
    """(numero da linha, linha) de cada NAO_CONFIRMADO por acesso sem escada nem P-nnn."""
    out = []
    for i, linha in enumerate(sem_riscado(texto).splitlines(), start=1):
        if (NAO_CONFIRMADO.search(linha) and MOTIVO_DE_ACESSO.search(linha)
                and not TEM_ESCADA.search(linha)):
            out.append((i, linha))
    return out


def ler_base(caminho: str = BASE) -> dict[tuple[str, str], str]:
    base = {}
    with open(caminho, encoding="utf-8") as f:
        for n, bruta in enumerate(f, start=1):
            if not bruta.strip() or bruta.startswith("#"):
                continue
            partes = [p.strip() for p in bruta.split("|", 2)]
            if len(partes) != 3 or not partes[2]:
                raise ValueError(f"{caminho}:{n}: esperado 'caminho | chave | motivo'")
            base[(partes[0], partes[1])] = partes[2]
    return base


def varrer(raiz: str = RAIZ, base: dict[tuple[str, str], str] | None = None
           ) -> tuple[list[str], list[str]]:
    """(novas, obsoletas): linhas que reprovam, e itens da base que nao casam com nada."""
    base = ler_base() if base is None else base
    vistas = set()
    novas = []
    for rel in arquivos_md(raiz):
        with open(os.path.join(raiz, rel), encoding="utf-8", errors="replace") as f:
            texto = f.read()
        for n, linha in violacoes_no_texto(texto):
            k = (rel, chave(linha))
            if k in base:
                vistas.add(k)
            else:
                novas.append(f"{rel}:{n}: {linha.strip()[:160]}")
    obsoletas = [f"{c} | {h} | {m}" for (c, h), m in base.items() if (c, h) not in vistas]
    return novas, obsoletas


def main() -> int:
    novas, obsoletas = varrer()
    for v in novas:
        print(f"SEM ESCADA  {v}")
    for o in obsoletas:
        print(f"BASE VELHA  {o}")
    print(f"{len(novas)} linha(s) sem escada; {len(obsoletas)} item(ns) velho(s) na base "
          f"({len(ler_base())} na base)")
    return 1 if novas or obsoletas else 0


if __name__ == "__main__":
    sys.exit(main())
