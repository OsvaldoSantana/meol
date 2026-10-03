#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""O estado do projeto em menos de 2 mil tokens, lido ao abrir a sessao (decisao de 02/10/2026).

POR QUE ELE EXISTE. A abertura de sessao lia o `PENDENCIAS.md` inteiro (~40 mil tokens medidos
por `auditoria/tamanho_do_contexto.py` em 03/10) para saber o que esta aberto -- e quase toda
tarefa so precisa da secao de UMA pendencia. Este gerador tira dos dois registros vivos so o
indice: as pendencias abertas (codigo, titulo, dono, gatilho, classe) e os blocos da fila do
Osvaldo que ainda nao tem resposta. O hook SessionStart (`.claude/settings.json`) injeta o
resultado; a secao inteira se le sob demanda.

    python tools/estado.py             # regenera docs/estado.md
    python tools/estado.py --conferir  # sai 1 se o arquivo estiver velho ou passar do teto

O QUE ELE NAO FAZ (P5):
  1. NAO resume a pendencia. Titulo e campos saem cortados no limite de cada coluna, com
     reticencias; quem decide le a secao (`grep -n "^## P-115" PENDENCIAS.md`).
  2. NAO inventa campo. Pendencia sem `**Dono:**`, `**Gatilho:**` ou classe declarada sai com
     `?` no campo -- e isso e uma violacao da 5-A.1 visivel, nao um defeito deste gerador.
  3. NAO mede o tokenizador do Claude. O teto usa a razao de chars/token do
     `auditoria/tamanho_do_contexto.py` (proxy, +-15%), a mesma regua das medicoes de contexto.
  4. "Sem resposta" na fila e uma regra de texto, nao leitura: um bloco numerado esta
     respondido se o cabecalho diz "respondido" ou se um dos codigos de opcao dele (`**115a**`)
     aparece nas secoes de resposta, acima do bloco 1. Bloco sem codigo proprio (opcoes `(a)`)
     so sai da lista pelo cabecalho.
"""
from __future__ import annotations

import argparse
import importlib.util
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PENDENCIAS = os.path.join(RAIZ, "PENDENCIAS.md")
FILA = os.path.join(RAIZ, "docs", "decisoes", "fila-do-osvaldo.md")
SAIDA = os.path.join(RAIZ, "docs", "estado.md")

# Decisao dele, 02/10/2026: a abertura cabe em menos de 2 mil tokens.
LIMITE_TOKENS = 2000
# Teto do texto que um hook injeta no contexto (documentacao oficial de hooks, conferida em
# 03/10/2026): acima de 10.000 caracteres a saida vira arquivo e so uma previa de 2.000 entra.
LIMITE_CHARS_HOOK = 10_000

CLASSES = {"BLOQUEIA_O_SISTEMA": "BLOQUEIA", "DECISAO_DE_DESENHO": "DESENHO",
           "DADO_DE_UM_USUARIO": "DADO"}
# Larguras por coluna: o que cabe em 2 mil tokens com 80 pendencias (03/10/2026). Medido no primeiro
# gerado; quem passar do teto ajusta aqui, e o --conferir reprova antes do CI.
LARGURA = {"titulo": 28, "dono": 16, "gatilho": 24}


def _chars_por_token() -> float:
    """A mesma razao do instrumento de contexto (P2: uma regua so)."""
    caminho = os.path.join(RAIZ, "auditoria", "tamanho_do_contexto.py")
    spec = importlib.util.spec_from_file_location("tamanho_do_contexto", caminho)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return float(mod.CHARS_POR_TOKEN)


def _limpo(s: str) -> str:
    """Tira a marcacao do markdown e o texto riscado (decisao vencida nao e o estado)."""
    s = re.sub(r"~~.*?~~", "", s)
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    s = s.replace("**", "").replace("`", "").replace("*", "")
    return re.sub(r"\s+", " ", s).strip(" .·—-")


def _corta(s: str, n: int) -> str:
    if len(s) <= n:
        return s
    corte = s[: n - 1].rsplit(" ", 1)[0] if " " in s[: n - 1] else s[: n - 1]
    return corte.rstrip(" ,;:·—(") + "…"


def _blocos(texto: str, cabecalho: str) -> list[tuple[str, str]]:
    """(linha do cabecalho, corpo) de cada `## ` que casa com o padrao."""
    partes = re.split(r"(?m)^(## .*)$", texto)
    return [(partes[i], partes[i + 1]) for i in range(1, len(partes) - 1, 2)
            if re.match(cabecalho, partes[i])]


def _campo(corpo: str, nome: str) -> str:
    plano = re.sub(r"\s+", " ", corpo)
    m = re.search(r"\*\*" + nome + r":\*\*\s*(.*?)(?=\s·\s|\*\*[A-Z][\w ]*:\*\*|\. \*\*|$)", plano)
    # So a primeira frase: o resto do paragrafo e o porque, que mora na secao.
    return _limpo(re.split(r"\.\s", m.group(1), maxsplit=1)[0]) if m else ""


def pendencias(texto: str) -> list[dict[str, str]]:
    """As abertas: todo `## P-` antes de `## Ao voltar ao desktop`, menos o codigo riscado."""
    texto = texto.split("\n## Ao voltar ao desktop", 1)[0]
    saida = []
    for cab, corpo in _blocos(texto, r"## P-\d"):
        codigo, _, titulo = cab[3:].partition(" · ")
        # So os campos do topo: o corpo pode citar "**Dono:**" de outra pendencia mais abaixo.
        topo = corpo.split("\n\n---", 1)[0][:1500]
        classe = ""
        m = re.search(r"\*\*Classe:\*\*\s*(?:~~[^~]*~~\s*)?`?([A-Z_]+)", re.sub(r"\s+", " ", topo))
        if m and m.group(1) in CLASSES:
            classe = CLASSES[m.group(1)]
        saida.append({"codigo": codigo.strip(), "titulo": _limpo(titulo),
                      "dono": _campo(topo, "Dono"), "gatilho": _campo(topo, "Gatilho"),
                      "classe": classe})
    return saida


def fila_sem_resposta(texto: str) -> list[dict[str, str]]:
    i = re.search(r"(?m)^## 1 · ", texto)
    respostas = texto[: i.start()] if i else ""
    vistos = set(re.findall(r"[\w-]+", respostas.lower()))
    saida = []
    for cab, corpo in _blocos(texto, r"## \d+ · "):
        if "respondido" in cab.lower():
            continue
        opcoes = re.findall(r"(?m)^- \*\*([\w-]+)\*\*", corpo)
        opcoes = [o for o in opcoes if re.search(r"\d|-", o)]   # 115a, dep-a; nunca "(a)"
        if any(o.lower() in vistos for o in opcoes):
            continue
        num, _, resto = cab[3:].partition(" · ")
        partes = [_limpo(p) for p in resto.split(" · ")]
        saida.append({"bloco": num, "titulo": partes[0],
                      "ref": " · ".join(p for p in partes[1:] if p)})
    return saida


def _linha(p: dict[str, str]) -> str:
    L = LARGURA
    campos = [p["codigo"], _corta(p["titulo"], L["titulo"])]
    if p["dono"] or p["gatilho"]:
        # O parentese do dono diz QUE parte e de quem; a secao tem o resto.
        dono = re.split(r" \(| ·", p["dono"], maxsplit=1)[0]
        campos += [_corta(dono, L["dono"]) or "?", _corta(p["gatilho"], L["gatilho"]) or "?"]
    return " · ".join(campos)


def gerar(texto_pend: str, texto_fila: str) -> str:
    ps = pendencias(texto_pend)
    fs = fila_sem_resposta(texto_fila)
    linhas = [
        "# Estado do projeto",
        "",
        "*Gerado por `tools/estado.py` de `PENDENCIAS.md` e da fila; não editar à mão. "
        "Cada linha: código · título · dono · gatilho, cortados (…); a seção inteira: "
        "`grep -n \"^## P-NN\" PENDENCIAS.md`. `?` = campo não declarado (5-A.1).*",
        "",
        f"## Pendências abertas: {len(ps)}",
    ]
    # Agrupar pela classe tira uma coluna de 80 linhas: e o que faz caber nos 2 mil tokens.
    grupos = [(c, [p for p in ps if p["classe"] == c]) for c in CLASSES.values()]
    grupos.append(("sem classe", [p for p in ps if not p["classe"]]))
    for nome, membros in grupos:
        if membros:
            linhas += ["", f"### {nome} ({len(membros)})", *(_linha(p) for p in membros)]
    linhas += ["", f"## Fila do Osvaldo, sem resposta: {len(fs)}", ""]
    for f in fs:
        linhas.append(f"- {f['bloco']} · {f['titulo']}" + (f" · {f['ref']}" if f["ref"] else ""))
    return "\n".join(linhas) + "\n"


def _ler(caminho: str) -> str:
    with open(caminho, encoding="utf-8") as f:
        return f.read()


def problemas(gerado: str, atual: str | None, chars_por_token: float) -> list[str]:
    erros = []
    if atual != gerado:
        erros.append("docs/estado.md esta velho: rode `python tools/estado.py` e commite")
    tokens = len(gerado) / chars_por_token
    if tokens >= LIMITE_TOKENS:
        erros.append(f"docs/estado.md tem ~{tokens:.0f} tokens; o teto e {LIMITE_TOKENS} "
                     f"(decisao de 02/10). Estreite LARGURA ou feche pendencias")
    if len(gerado) > LIMITE_CHARS_HOOK:
        erros.append(f"{len(gerado)} caracteres: o hook so injeta {LIMITE_CHARS_HOOK}")
    return erros


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--conferir", action="store_true",
                    help="nao grava; sai 1 se docs/estado.md estiver velho ou passar do teto")
    a = ap.parse_args(argv)
    gerado = gerar(_ler(PENDENCIAS), _ler(FILA))
    cpt = _chars_por_token()
    if a.conferir:
        atual = _ler(SAIDA) if os.path.exists(SAIDA) else None
        erros = problemas(gerado, atual, cpt)
        for e in erros:
            print(e, file=sys.stderr)
        if not erros:
            print(f"docs/estado.md em dia: {len(gerado)} caracteres, "
                  f"~{len(gerado) / cpt:.0f} tokens (razao {cpt} chars/token, proxy)")
        return 1 if erros else 0
    with open(SAIDA, "w", encoding="utf-8", newline="\n") as f:
        f.write(gerado)
    erros = problemas(gerado, gerado, cpt)
    for e in erros:
        print(e, file=sys.stderr)
    print(f"gravado {os.path.relpath(SAIDA, RAIZ)}: {len(gerado)} caracteres, "
          f"~{len(gerado) / cpt:.0f} tokens")
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main())
