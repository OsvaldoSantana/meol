# -*- coding: utf-8 -*-
"""Arquiva no Wayback Machine as paginas da R3 que ficaram PENDENTE_LOCAL (P-170, degrau 4).

POR QUE EXISTE. A R3 grava, por marca, o link do arquivamento publico da pagina capturada: as
capturas sao de terceiros e nao entram no repositorio, entao o Wayback e o que deixa outra
pessoa ver o que foi classificado. Em 04/10/2026 a sessao na nuvem nao alcancou
web.archive.org (conexao derrubada no proxy, nas URLs /save, /web e no archive.ph; a API
archive.org/wayback/available responde, mas so le arquivamento antigo). Este script e o degrau 4
da escada (CLAUDE.md 5-B.18): roda na maquina dele, sem conta e sem login (o Save Page Now
anonimo), e escreve o link de volta no CSV.

O QUE ELE NAO FAZ (P5). Nao usa conta do archive.org nem cookie de navegador (5-A.7). Nao
reclassifica nada. Nao garante que o arquivamento e igual a captura: e a mesma URL no mesmo dia,
nao o mesmo byte (a captura e do Chromium sem interface; o Wayback guarda o HTML).

    py -3.11 tools/r3_arquivar.py            # arquiva as PENDENTE_LOCAL e regrava o CSV
    py -3.11 tools/r3_arquivar.py --plano    # so lista o que arquivaria
"""
from __future__ import annotations

import argparse
import csv
import os
import sys
import time
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r3_dominante as R  # noqa: E402

SPN = "https://web.archive.org/save/"
PAUSA_S = 12          # o Save Page Now anonimo limita a frequencia; uma pagina a cada 12 s


def pendentes(linhas: list[dict[str, str]]) -> list[int]:
    """Os indices das linhas com PENDENTE_LOCAL e url (puladas sem url ficam de fora)."""
    return [i for i, r in enumerate(linhas) if r["arquivo_wayback"] == R.PENDENTE and r["url"]]


def link_do_arquivamento(resposta_url: str, location: str | None) -> str | None:
    """O SPN responde com o snapshot no cabecalho Content-Location ou redireciona para ele."""
    for cand in (location, resposta_url):
        if cand and "/web/" in cand:
            return cand if cand.startswith("http") else "https://web.archive.org" + cand
    return None


def gravar(linhas: list[dict[str, str]], path: str = R.CSV) -> None:
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=R.COLUNAS, lineterminator="\n")
        w.writeheader()
        w.writerows(linhas)


def arquivar(url: str) -> str | None:
    req = urllib.request.Request(SPN + url, headers={"User-Agent": "meol-r3-arquivar/1"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return link_do_arquivamento(r.geturl(), r.headers.get("Content-Location"))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=(__doc__ or "").split("\n")[0])
    ap.add_argument("--plano", action="store_true")
    a = ap.parse_args(argv)
    linhas = R.ler()
    alvo = pendentes(linhas)
    print(f"{len(alvo)} pagina(s) com {R.PENDENTE}")
    if a.plano:
        for i in alvo:
            print(" ", linhas[i]["marca"], linhas[i]["url"])
        return 0
    falhas = 0
    for n, i in enumerate(alvo):
        try:
            link = arquivar(linhas[i]["url"])
        except Exception as e:  # registra e segue: a proxima rodada tenta de novo
            link, msg = None, f"{type(e).__name__}: {e}"
        else:
            msg = "sem link na resposta"
        if link:
            linhas[i]["arquivo_wayback"] = link
            gravar(linhas)                 # grava a cada uma: parar no meio nao perde nada
            print("ok  ", linhas[i]["marca"], link)
        else:
            falhas += 1
            print("FALHA", linhas[i]["marca"], msg)
        if n + 1 < len(alvo):
            time.sleep(PAUSA_S)
    print(f"{len(alvo) - falhas} arquivada(s), {falhas} falha(s). Depois: "
          "python tools/r3_dominante.py e o commit do CSV e do veto.md")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
