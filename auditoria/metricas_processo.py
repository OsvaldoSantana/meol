#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""metricas_processo.py -- o processo medido por semana (25/09/2026).

Duas fontes:
  docs/metricas/eventos.csv          uma linha por erro (achado, retratacao, reincidencia),
                                     versionado. Todo achado ou retratacao novo ganha a sua
                                     linha no MESMO commit que o registra.
  data/analise-sessoes/turnos.csv    tempo e tokens por pedido, de tools/analisar_sessoes.py.
                                     So existe na maquina que tem as sessoes (~/.claude); fora
                                     dela a secao sai vazia e DIZ que saiu vazia.

Por semana ISO: retratacoes por autor; reincidencias; % dos erros achados pelo Osvaldo (com o
n ao lado -- regua 5-B.14); pedidos, minutos por pedido, chamadas ao modelo e tokens de saida.

`validar()` reprova evento sem codigo, com tipo/autor/quem_achou fora das listas, ou com data
que nao e data. Valor desconhecido se escreve `desconhecido`, nunca vazio: vazio nao distingue
"nao sei" de "esqueci".
"""
from __future__ import annotations

import argparse
import collections
import csv
import datetime as dt
import os
import re
import sys

import yaml

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVENTOS = os.path.join(RAIZ, "docs", "metricas", "eventos.csv")
TURNOS = os.path.join(RAIZ, "data", "analise-sessoes", "turnos.csv")
COLUNAS = ("data", "codigo", "tipo", "autor", "quem_achou", "regua", "commit_introduziu",
           "commit_corrigiu", "descricao")
TIPOS = ("achado", "retratacao", "reincidencia")
PESSOAS = ("claude-chat", "claude-code", "osvaldo", "outra-ia", "fonte", "desconhecido")
MODELOS = os.path.join(RAIZ, "docs", "metricas", "modelos-por-tarefa.yaml")
# 02/10/2026: sem o modelo no evento, a regra de volta nao tem o que contar. A etiqueta abre a
# descricao: "[modelo=sonnet classe=registro] texto".
ETIQUETA = re.compile(r"^\[modelo=([\w-]+) classe=([\w-]+)\]")


def ler_modelos(caminho=MODELOS):
    with open(caminho, encoding="utf-8") as f:
        return yaml.safe_load(f)


class EventoInvalido(ValueError):
    pass


def ler(caminho=EVENTOS):
    with open(caminho, encoding="utf-8", newline="") as f:
        r = csv.DictReader(f, delimiter=";")
        if tuple(r.fieldnames or ()) != COLUNAS:
            raise EventoInvalido(f"colunas {r.fieldnames}, esperado {COLUNAS}")
        return list(r)


def etiqueta(e):
    """(modelo, classe) da etiqueta, ou None."""
    m = ETIQUETA.match(e.get("descricao") or "")
    return (m.group(1), m.group(2)) if m else None


def validar(eventos, modelos=None):
    modelos = modelos or ler_modelos()
    desde = modelos["vigente_desde"]
    for i, e in enumerate(eventos, start=2):
        if not (e.get("codigo") or "").strip():
            raise EventoInvalido(f"linha {i}: evento sem codigo -- {e}")
        if e["tipo"] not in TIPOS:
            raise EventoInvalido(f"linha {i}: tipo {e['tipo']!r} fora de {TIPOS}")
        for campo in ("autor", "quem_achou"):
            if e[campo] not in PESSOAS:
                raise EventoInvalido(f"linha {i}: {campo} {e[campo]!r} fora de {PESSOAS}")
        try:
            dt.date.fromisoformat(e["data"])
        except ValueError as ex:
            raise EventoInvalido(f"linha {i}: data {e['data']!r}") from ex
        vazios = [c for c in COLUNAS if not (e.get(c) or "").strip()]
        if vazios:
            raise EventoInvalido(f"linha {i}: {vazios} vazio -- escreva 'desconhecido'")
        if e["autor"].startswith("claude") and dt.date.fromisoformat(e["data"]) >= desde:
            et = etiqueta(e)
            if et is None:
                raise EventoInvalido(f"linha {i}: evento de autoria Claude desde {desde} abre a "
                                     "descricao com [modelo=<m> classe=<c>]")
            if et[0] not in modelos["ordem"] + ["desconhecido"] or et[1] not in modelos["classes"]:
                raise EventoInvalido(f"linha {i}: etiqueta {et} fora de "
                                     "docs/metricas/modelos-por-tarefa.yaml")
    return eventos


def regra_de_volta(eventos, hoje, modelos=None):
    """Classes que devem voltar ao modelo de cima: {classe: n de eventos na janela}.

    Conta so evento de autoria Claude, etiquetado, dentro de `janela_dias`, com um modelo
    abaixo do topo da `ordem` -- o que rodava tudo antes de 02/10. `desconhecido` nao conta,
    e nao absolve: aparece no relatorio como etiqueta sem modelo."""
    modelos = modelos or ler_modelos()
    ordem, rv = modelos["ordem"], modelos["regra_de_volta"]
    inicio = hoje - dt.timedelta(days=rv["janela_dias"])
    n = collections.Counter()
    for e in eventos:
        et = etiqueta(e)
        if not et or not e["autor"].startswith("claude") or et[0] not in ordem:
            continue
        if not inicio < dt.date.fromisoformat(e["data"]) <= hoje:
            continue
        # Antes de 02/10 tudo rodava no de cima: erro com modelo abaixo dele e o custo do corte.
        if et[0] != ordem[-1]:
            n[et[1]] += 1
    return {c: k for c, k in n.items() if k >= rv["limiar"]}


def semana(data):
    a, s, _ = dt.date.fromisoformat(data[:10]).isocalendar()
    return f"{a}-S{s:02d}"


def por_semana(eventos):
    out = collections.defaultdict(lambda: dict(n=0, retratacoes=collections.Counter(),
                                               reincidencias=0, achados_osvaldo=0,
                                               quem_desconhecido=0))
    for e in eventos:
        s = out[semana(e["data"])]
        s["n"] += 1
        if e["tipo"] == "retratacao":
            s["retratacoes"][e["autor"]] += 1
        if e["tipo"] == "reincidencia":
            s["reincidencias"] += 1
        if e["quem_achou"] == "osvaldo":
            s["achados_osvaldo"] += 1
        if e["quem_achou"] == "desconhecido":
            s["quem_desconhecido"] += 1
    return dict(out)


def sessoes_por_semana(caminho=TURNOS):
    if not os.path.exists(caminho):
        return None
    out = collections.defaultdict(lambda: dict(pedidos=0, s=0.0, chamadas=0, saida_tok=0))
    with open(caminho, encoding="utf-8", newline="") as f:
        for t in csv.DictReader(f, delimiter=";"):
            s = out[semana(t["ini"])]
            s["pedidos"] += 1
            s["s"] += float(t["dur_s"])
            s["chamadas"] += int(t["chamadas"])
            s["saida_tok"] += int(t["saida_tok"])
    return dict(out)


def relatorio(eventos, sessoes):
    R = ["| semana | erros (n) | retratacoes por autor | reincidencias | achados pelo Osvaldo "
         "| quem achou: desconhecido |", "|---|---|---|---|---|---|"]
    for sem, s in sorted(por_semana(eventos).items()):
        ret = ", ".join(f"{k} {v}" for k, v in sorted(s["retratacoes"].items())) or "0"
        pct = 100.0 * s["achados_osvaldo"] / s["n"]
        R.append(f"| {sem} | {s['n']} | {ret} | {s['reincidencias']} | "
                 f"{pct:.0f}% ({s['achados_osvaldo']} de {s['n']}) | {s['quem_desconhecido']} |")
    R.append("")
    if sessoes is None:
        R.append("Sessoes: sem `data/analise-sessoes/turnos.csv` nesta maquina -- rode "
                 "`py -3.11 tools/analisar_sessoes.py`. Secao NAO medida aqui.")
    else:
        R += ["| semana | pedidos | min por pedido | chamadas ao modelo "
              "| tokens de saida por pedido |", "|---|---|---|---|---|"]
        for sem, s in sorted(sessoes.items()):
            n = max(s["pedidos"], 1)
            R.append(f"| {sem} | {s['pedidos']} | {s['s'] / 60 / n:.1f} | {s['chamadas']} | "
                     f"{s['saida_tok'] // n} |")
    return "\n".join(R) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--eventos", default=EVENTOS)
    ap.add_argument("--turnos", default=TURNOS)
    a = ap.parse_args(argv)
    ev = validar(ler(a.eventos))
    print(relatorio(ev, sessoes_por_semana(a.turnos)), end="")
    volta = regra_de_volta(ev, dt.date.today())
    print("\nRegra de volta (docs/metricas/modelos-por-tarefa.yaml): " + (
        ", ".join(f"{c} volta um degrau ({k} eventos)" for c, k in sorted(volta.items()))
        or "nenhuma classe disparou"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
