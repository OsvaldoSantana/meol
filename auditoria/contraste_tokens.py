#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Razao de contraste da WCAG sobre os tokens das direcoes visuais (P-163, RI-22 a RI-24).

POR QUE ELE EXISTE. O documento tecnico do motor (Quanto-e-Onde.html) usava `--ink-3` a
3,84:1 em texto de 10,5 a 12 px (docs/decisoes/rosto-v1.md, item d): ninguem mediu antes de
desenhar. Aqui a cor e dado (`docs/marca/tokens/direcoes.yaml`) e cada par declarado passa
por esta conta antes de virar estimulo.

O QUE ELE MEDE (P5). A razao `(L1 + 0.05) / (L2 + 0.05)` com a luminancia relativa sRGB da
definicao da WCAG 2.2 (docs/fontes/wcag-22-w3c.md), SEM arredondar, contra o limiar do tipo
do par (`texto_pequeno`, `texto_grande`, `componente`), lido do YAML. NAO mede: cor sobre
imagem ou gradiente, transparencia, o par que ninguem declarou, nem se o tamanho real da
fonte na tela bate com o tipo declarado -- isso e do teste de navegador da etapa 4.

    python auditoria/contraste_tokens.py      # tabela de todos os pares; sai 1 se algum reprova
"""
from __future__ import annotations

import io
import os
import re
import sys
from typing import Any

import yaml

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
TOKENS = os.path.join(RAIZ, "docs", "marca", "tokens", "direcoes.yaml")
HEX = re.compile(r"^#[0-9A-Fa-f]{6}$")


def luminancia(hexcor: str) -> float:
    """Luminancia relativa sRGB, com o 0.04045 da definicao atual (WCAG 2.2)."""
    if not HEX.match(hexcor):
        raise ValueError(f"cor fora do formato #RRGGBB: {hexcor!r}")
    canais = []
    for i in (1, 3, 5):
        c = int(hexcor[i:i + 2], 16) / 255
        canais.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    r, g, b = canais
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def razao(a: str, b: str) -> float:
    la, lb = sorted((luminancia(a), luminancia(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def carregar(path: str = TOKENS) -> dict[str, Any]:
    with io.open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def avaliar(tok: dict[str, Any]) -> list[dict[str, Any]]:
    """Uma linha por par declarado, com a razao, o limiar e se passa. Sem arredondar."""
    lim = tok["limiares"]
    out = []
    for nome, d in tok["direcoes"].items():
        cores = d["cores"]
        for p in d["pares"]:
            tipo = p["tipo"]
            if tipo not in lim:
                raise ValueError(f"{nome}: tipo de par desconhecido {tipo!r}")
            for papel in (p["frente"], p["fundo"]):
                if papel not in cores:
                    raise ValueError(f"{nome}: par cita o papel {papel!r}, que nao tem cor")
            x = razao(cores[p["frente"]], cores[p["fundo"]])
            minimo = float(lim[tipo]["razao"])
            out.append(dict(direcao=nome, frente=p["frente"], fundo=p["fundo"], tipo=tipo,
                            cor_frente=cores[p["frente"]], cor_fundo=cores[p["fundo"]],
                            razao=x, limiar=minimo, passa=x >= minimo,
                            criterio=lim[tipo]["criterio"], par=p))
    return out


def grande_sem_tamanho(tok: dict[str, Any]) -> list[str]:
    """Par marcado `texto_grande` tem de declarar o tamanho que o faz grande.

    Sem isto, marcar um texto de 12 px como grande baixava o limiar de 4,5 para 3 em
    silencio -- o mesmo erro do Quanto-e-Onde, com um rotulo por cima."""
    g = tok["limiares"]["texto_grande"]
    ruins = []
    for nome, d in tok["direcoes"].items():
        for p in d["pares"]:
            if p["tipo"] != "texto_grande":
                continue
            px = p.get("tamanho_px")
            negrito = bool(p.get("negrito"))
            minimo = g["tamanho_min_px_negrito"] if negrito else g["tamanho_min_px"]
            if px is None or float(px) < float(minimo):
                ruins.append(f"{nome}: {p['frente']} sobre {p['fundo']} ({px} px)")
    return ruins


def status_sem_rotulo(tok: dict[str, Any]) -> list[str]:
    """RI-24 (WCAG 1.4.1): toda cor de estado tem rotulo de texto declarado."""
    rot = tok.get("rotulos_de_estado", {})
    ruins = []
    for nome, d in tok["direcoes"].items():
        for papel in d["cores"]:
            if papel.startswith("status_") and not rot.get(papel[len("status_"):]):
                ruins.append(f"{nome}: {papel}")
    return ruins


def main(argv: list[str] | None = None) -> int:
    tok = carregar()
    linhas = avaliar(tok)
    for x in linhas:
        marca = "ok " if x["passa"] else "REPROVA"
        print(f"{marca:7} {x['direcao']}  {x['frente']:>20} / {x['fundo']:<11} "
              f"{x['cor_frente']} / {x['cor_fundo']}  {x['razao']:.4f} >= {x['limiar']}  "
              f"({x['tipo']})")
    ruins = [x for x in linhas if not x["passa"]]
    print(f"{len(linhas)} pares; {len(ruins)} reprovados (n={len(linhas)})")
    return 1 if ruins or grande_sem_tamanho(tok) or status_sem_rotulo(tok) else 0


if __name__ == "__main__":
    sys.exit(main())
