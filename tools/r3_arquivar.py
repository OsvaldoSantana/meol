# -*- coding: utf-8 -*-
"""Arquiva no Wayback Machine as paginas da R3 que ficaram PENDENTE_LOCAL (P-170, degrau 4).

POR QUE EXISTE. A R3 grava, por marca, o link do arquivamento publico da pagina capturada: as
capturas sao de terceiros e nao entram no repositorio, entao o Wayback e o que deixa outra
pessoa ver o que foi classificado. Em 04/10/2026 a sessao na nuvem nao alcancou
web.archive.org (conexao derrubada no proxy, nas URLs /save, /web e no archive.ph; a API
archive.org/wayback/available responde, mas so le arquivamento antigo). O Save Page Now e
anonimo: sem conta e sem login.

O DEGRAU 4 EM ORDEM (CLAUDE.md 5-B.18, 16/10/2026). 4a: o workflow `.github/workflows/
arquivar_r3.yml` roda este script no servidor do GitHub com `--saida`, que escreve o resultado
num JSON (o artefato do run) e nao toca o CSV: o workflow so le o repositorio. A sessao baixa o
artefato e grava pelo `--aplicar`: o link vai para `arquivo_wayback`, e a pagina que recusou
ganha na `escada` o degrau tentado, o erro e o proximo executor. 4b: o runner br-sp, quando
existir. 4c: a sessao local, com o mesmo `--saida` e o mesmo `--aplicar`.

O QUE ELE NAO FAZ (P5). Nao usa conta do archive.org nem cookie de navegador (5-A.7). Nao
reclassifica nada. Nao garante que o arquivamento e igual a captura: e a mesma URL no mesmo dia,
nao o mesmo byte (a captura e do Chromium sem interface; o Wayback guarda o HTML).

    python tools/r3_arquivar.py --plano                    # so lista o que arquivaria
    python tools/r3_arquivar.py --saida resultado.json     # arquiva e escreve o resultado
    python tools/r3_arquivar.py --aplicar resultado.json --degrau "4a) ..." --proximo "4c) ..."
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import sys
import time
import urllib.request
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r3_dominante as R  # noqa: E402

SPN = "https://web.archive.org/save/"
PAUSA_S = 12          # o Save Page Now anonimo limita a frequencia; uma pagina a cada 12 s


def chave(r: dict[str, str]) -> str:
    """A linha da R3 pela categoria sorteada e a ordem: e o que o resultado leva de volta."""
    return f"{r['categoria_sorteada']}:{r['ordem_no_sorteio']}"


def pendentes(linhas: list[dict[str, str]]) -> list[int]:
    """Os indices das linhas com PENDENTE_LOCAL e url (puladas sem url ficam de fora)."""
    return [i for i, r in enumerate(linhas) if r["arquivo_wayback"] == R.PENDENTE and r["url"]]


def link_do_arquivamento(resposta_url: str, location: str | None) -> str | None:
    """O SPN responde com o snapshot no cabecalho Content-Location ou redireciona para ele."""
    for cand in (location, resposta_url):
        if cand and "/web/" in cand:
            return cand if cand.startswith("http") else "https://web.archive.org" + cand
    return None


def aplicar(linhas: list[dict[str, str]], resultado: dict[str, dict[str, Any]], degrau: str,
            proximo: str) -> tuple[int, int]:
    """Grava o resultado de um executor nas linhas: o link em `arquivo_wayback`; a recusa na
    `escada`, com o degrau, o erro e o proximo executor. So mexe em linha ainda PENDENTE_LOCAL
    (um resultado velho nao desfaz um link ja gravado). Devolve (arquivadas, recusadas)."""
    por_chave = {chave(r): r for r in linhas}
    ok = recusas = 0
    for k, res in resultado.items():
        r = por_chave.get(k)
        if r is None:
            raise KeyError(f"{k}: o resultado traz uma linha que o CSV nao tem")
        if r["arquivo_wayback"] != R.PENDENTE:
            continue
        if res.get("link"):
            if not res["link"].startswith(R.WAYBACK):
                raise ValueError(f"{k}: link {res['link']!r} nao e do Wayback")
            r["arquivo_wayback"] = res["link"]
            ok += 1
        else:
            nota = f"wayback {degrau}: {res.get('erro') or 'sem link na resposta'}; {proximo}"
            r["escada"] = f"{r['escada']}; {nota}" if r["escada"] else nota
            recusas += 1
    return ok, recusas


def gravar(linhas: list[dict[str, str]], path: str = R.CSV) -> None:
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=R.COLUNAS, lineterminator="\n")
        w.writeheader()
        w.writerows(linhas)


def arquivar(url: str) -> str | None:
    req = urllib.request.Request(SPN + url, headers={"User-Agent": "meol-r3-arquivar/1"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return link_do_arquivamento(r.geturl(), r.headers.get("Content-Location"))


def _gravar_saida(path: str, resultado: dict[str, dict[str, Any]]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=1)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=(__doc__ or "").split("\n")[0])
    ap.add_argument("--plano", action="store_true")
    ap.add_argument("--saida", help="escreve o resultado num JSON e nao toca o CSV")
    ap.add_argument("--aplicar", help="le o JSON de um executor e grava no CSV")
    ap.add_argument("--degrau", default="", help="com --aplicar: o executor, transcrito")
    ap.add_argument("--proximo", default="", help="com --aplicar: o proximo executor")
    a = ap.parse_args(argv)
    linhas = R.ler()
    if a.aplicar:
        if not (a.degrau and a.proximo):
            ap.error("--aplicar exige --degrau e --proximo (5-B.18: a recusa leva os dois)")
        with open(a.aplicar, encoding="utf-8") as f:
            ok, rec = aplicar(linhas, json.load(f), a.degrau, a.proximo)
        gravar(linhas)
        print(f"{ok} link(s) gravado(s), {rec} recusa(s) com a escada; "
              f"{len(pendentes(linhas))} ainda {R.PENDENTE}")
        return 0
    alvo = pendentes(linhas)
    print(f"{len(alvo)} pagina(s) com {R.PENDENTE}", flush=True)
    if a.plano or not a.saida:
        for i in alvo:
            print(" ", chave(linhas[i]), linhas[i]["marca"], linhas[i]["url"])
        if not a.plano:
            print("sem --saida nada e arquivado (o CSV se grava pelo --aplicar)")
        return 0
    resultado: dict[str, dict[str, Any]] = {}
    for n, i in enumerate(alvo):
        r = linhas[i]
        quando = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
        try:
            link = arquivar(r["url"])
            erro = None if link else "sem link na resposta"
        except Exception as e:  # registra e segue: a recusa vai para a escada
            link, erro = None, f"{type(e).__name__}: {e}"[:200]
        resultado[chave(r)] = {"url": r["url"], "link": link, "erro": erro, "quando": quando}
        _gravar_saida(a.saida, resultado)      # grava a cada uma: parar no meio nao perde nada
        print(("ok   " if link else "FALHA"), chave(r), link or erro, flush=True)
        if n + 1 < len(alvo):
            time.sleep(PAUSA_S)
    falhas = sum(1 for v in resultado.values() if not v["link"])
    print(f"RESUMO: {len(alvo) - falhas} arquivada(s), {falhas} falha(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
