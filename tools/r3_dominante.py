# -*- coding: utf-8 -*-
"""O codigo dominante de cada categoria da R3 e a tabela do veto, a partir do CSV (P-170).

POR QUE EXISTE. O veto de distincao do teste de marca compara a direcao vencedora com o codigo
dominante das categorias concorrentes (livro de codigos, P-162). A vencedora so e conhecida
depois da janela de 21 dias; a tabela "direcao x codigo dominante de cada categoria" fica
pronta antes, para que o veto seja uma consulta e nao uma leitura. Tudo sai de
`docs/marca/rodada3/classificacao.csv`, pelas funcoes de `tools/codigos_visuais.py` (o
classificador congelado no pre-registro final): nada de regra escrita duas vezes.

O QUE ELE NAO FAZ (P5). Nao classifica marca (isso e da visita, com captura e procedencia);
nao decide o veto (a vencedora sai da analise, depois da janela).

    python tools/r3_dominante.py            # grava docs/marca/rodada3/veto.md
    python tools/r3_dominante.py --conferir  # sai 1 se o gravado divergir do CSV
"""
from __future__ import annotations

import argparse
import csv
import os
import sys
from typing import Any

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import codigos_visuais as V  # noqa: E402

RAIZ = os.path.dirname(AQUI)
PASTA = os.path.join(RAIZ, "docs", "marca", "rodada3")
CSV = os.path.join(PASTA, "classificacao.csv")
VETO = os.path.join(PASTA, "veto.md")
VARIAVEIS = ("fundo", "matiz", "familia_do_titulo", "raio", "densidade", "botao")
COLUNAS = ["marca", "categoria", "categoria_sorteada", "ordem_no_sorteio", "cnpj", "situacao",
           "motivo", "unidade", *VARIAVEIS, "fundo_hex", "destaque_hex", "familia_generica",
           "raio_px", "densidade_blocos", "url", "data", "sha256_captura", "arquivo_wayback",
           "escada"]
SITUACOES = ("classificada", "pulada", "fora_do_livro")


def ler(path: str = CSV) -> list[dict[str, str]]:
    with open(path, encoding="utf-8", newline="") as f:
        rd = csv.DictReader(f)
        if rd.fieldnames != COLUNAS:
            raise SystemExit(f"{path}: cabecalho fora do formato da R3: {rd.fieldnames}")
        return list(rd)


def validar(linhas: list[dict[str, str]], livro: dict[str, Any]) -> list[str]:
    """Os problemas do CSV (lista vazia = cada linha classificada cabe no livro)."""
    probs = []
    v = livro["veto"]
    cats = set(v["categorias_concorrentes"]) | set(v["categorias_fora_do_veto"])
    for i, r in enumerate(linhas, start=2):
        if r["situacao"] not in SITUACOES:
            probs.append(f"linha {i}: situacao {r['situacao']!r}")
            continue
        if r["situacao"] != "classificada":
            if not r["motivo"]:
                probs.append(f"linha {i}: {r['situacao']} sem motivo")
            continue
        if r["categoria"] not in cats:
            probs.append(f"linha {i}: categoria fora do livro {r['categoria']!r}")
        if r["unidade"] not in ("app", "site"):
            probs.append(f"linha {i}: unidade {r['unidade']!r} (ae-a: app ou site)")
        for var in VARIAVEIS:
            if r[var] not in livro["variaveis"][var]["valores"]:
                probs.append(f"linha {i}: {var}={r[var]!r} fora dos valores do livro")
        for campo in ("url", "data", "sha256_captura", "arquivo_wayback"):
            if not r[campo]:
                probs.append(f"linha {i}: sem {campo} (procedencia da captura)")
    return probs


def tabela(linhas: list[dict[str, str]], livro: dict[str, Any]) -> dict[str, Any]:
    """Por categoria: n, dominantes (todas as unidades e so app) e quem das direcoes imita."""
    classificadas = [r for r in linhas if r["situacao"] == "classificada"]
    direcoes = V.classificar_direcoes(livro)
    out: dict[str, Any] = {}
    for cat in livro["veto"]["categorias_concorrentes"]:
        grupo = [r for r in classificadas if r["categoria"] == cat]
        so_app = [r for r in grupo if r["unidade"] == "app"]
        dom = V.codigos_dominantes(grupo, livro)
        dom_app = V.codigos_dominantes(so_app, livro)
        out[cat] = {"n": len(grupo), "n_app": len(so_app), "dominantes": dom,
                    "dominantes_so_app": dom_app,
                    "imita": {d: V.imita(c, dom) for d, c in direcoes.items()},
                    "imita_so_app": {d: V.imita(c, dom_app) for d, c in direcoes.items()}}
    return out


def _codigo(doms: list[tuple[str, ...]]) -> str:
    return " ou ".join("/".join(d) for d in doms) if doms else "sem dominante"


def texto_veto(linhas: list[dict[str, str]], livro: dict[str, Any]) -> str:
    t = tabela(linhas, livro)
    n_min = livro["veto"]["n_minimo_de_marcas"]
    cab = ("# R3: a tabela do veto (direcao x codigo dominante de cada categoria)\n\n"
           "*GERADO por `python tools/r3_dominante.py` a partir de `classificacao.csv`; nao editar "
           "a mao. O codigo e fundo/matiz/familia do titulo/raio (as quatro centrais, aa-a). "
           f"Categoria com menos de {n_min} marcas classificadas nao tem dominante e nao veta. "
           "\"imita\" = a direcao partilha os quatro valores centrais com um dominante (livro de "
           "codigos). A vencedora so sai depois da janela; o veto se le na linha dela.*\n\n")
    linhas_md = ["| categoria | n (so app) | codigo dominante | E | C | D | so app: E | C | D |",
                 "|---|---|---|---|---|---|---|---|---|"]
    for cat, c in t.items():
        im = ["imita" if c["imita"][d] else "-" for d in ("E", "C", "D")]
        ima = ["imita" if c["imita_so_app"][d] else "-" for d in ("E", "C", "D")]
        linhas_md.append(f"| {cat} | {c['n']} ({c['n_app']}) | {_codigo(c['dominantes'])} | "
                         + " | ".join(im) + " | " + " | ".join(ima) + " |")
    return cab + "\n".join(linhas_md) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=(__doc__ or "").split("\n")[0])
    ap.add_argument("--conferir", action="store_true")
    a = ap.parse_args(argv)
    livro = V.ler_livro()
    linhas = ler()
    probs = validar(linhas, livro)
    for p in probs:
        print(p)
    if probs:
        return 1
    texto = texto_veto(linhas, livro)
    if a.conferir:
        with open(VETO, encoding="utf-8") as f:
            igual = f.read().replace("\r\n", "\n") == texto
        print("veto.md: " + ("ok" if igual else "DIVERGE do CSV"))
        return 0 if igual else 1
    with open(VETO, "w", encoding="utf-8", newline="\n") as f:
        f.write(texto)
    print("gravado docs/marca/rodada3/veto.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
