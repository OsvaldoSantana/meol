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
import json
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


# 03/10/2026: Brasilia sem horario de verao desde 2019. O `mergedAt` do GitHub vem em UTC, e um
# merge as 22h de Brasilia cairia no dia seguinte.
BRASILIA = dt.timezone(dt.timedelta(hours=-3))


def ler_referencia(modelos=None):
    """As linhas da classificacao de 16/09 a 02/10 (fila 21d): tipo, id, data, classe, trecho."""
    modelos = modelos or ler_modelos()
    caminho = os.path.join(RAIZ, modelos["regra_de_volta"]["referencia"]["arquivo"])
    with open(caminho, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter=";"))


def referencia(linhas, modelos=None):
    """{classe: (eventos, prs)} entre `desde` e `ate` da referencia, para toda classe da tabela.

    Tudo rodava em Opus: e a taxa do modelo de cima, contra a qual o de baixo se compara."""
    modelos = modelos or ler_modelos()
    ref = modelos["regra_de_volta"]["referencia"]
    n = {c: [0, 0] for c in modelos["classes"]}
    for r in linhas:
        if ref["desde"] <= dt.date.fromisoformat(r["data"]) <= ref["ate"]:
            n[r["classe"]][0 if r["tipo"] == "evento" else 1] += 1
    return {c: (e, p) for c, (e, p) in n.items()}


def prs_do_gh(caminho):
    """A saida de `gh pr list --state merged --json number,title,mergedAt,author`, como
    [{numero, titulo, autor, data}], com a data em Brasilia."""
    with open(caminho, encoding="utf-8") as f:
        brutos = json.load(f)
    return [dict(numero=p["number"], titulo=p["title"],
                 autor=(p.get("author") or {}).get("login", ""),
                 data=dt.datetime.fromisoformat(p["mergedAt"].replace("Z", "+00:00"))
                 .astimezone(BRASILIA).date().isoformat())
            for p in brutos]


def validar_titulo(titulo, modelos=None):
    """O titulo do PR abre com a etiqueta dos eventos: e o denominador da regra de volta."""
    modelos = modelos or ler_modelos()
    m = ETIQUETA.match(titulo or "")
    if m is None:
        raise EventoInvalido(f"titulo {titulo!r}: o PR abre com [modelo=<m> classe=<c>] "
                             "(docs/metricas/modelos-por-tarefa.yaml)")
    modelo, classe = m.groups()
    if modelo not in modelos["ordem"] + ["desconhecido"] or classe not in modelos["classes"]:
        raise EventoInvalido(f"titulo {titulo!r}: etiqueta {m.groups()} fora de "
                             "docs/metricas/modelos-por-tarefa.yaml")
    return m.groups()


def regra_de_volta(eventos, prs, hoje, ref, modelos=None):
    """Por classe: {eventos, prs, taxa, ref, ref_n, volta} na janela que termina em `hoje`.

    Conta so o que esta etiquetado com um modelo abaixo do topo da `ordem`: o evento de autoria
    Claude no numerador, o PR mergeado no denominador. `desconhecido` nao conta e nao absolve.
    `ref` e a saida de referencia(); classe sem PR na referencia nao tem taxa com que comparar
    e nunca volta -- o relatorio so mostra os numeros (decisao 21d)."""
    modelos = modelos or ler_modelos()
    ordem, rv = modelos["ordem"], modelos["regra_de_volta"]
    abaixo = set(ordem[:-1])
    inicio = hoje - dt.timedelta(days=rv["janela_dias"])

    def na_janela(data):
        return inicio < dt.date.fromisoformat(data) <= hoje

    ne, npr = collections.Counter(), collections.Counter()
    for e in eventos:
        et = etiqueta(e)
        if et and e["autor"].startswith("claude") and et[0] in abaixo and na_janela(e["data"]):
            ne[et[1]] += 1
    for p in prs:
        m = ETIQUETA.match(p["titulo"] or "")
        if m and m.group(1) in abaixo and na_janela(p["data"]):
            npr[m.group(2)] += 1
    out = {}
    for c in modelos["classes"]:
        e_ref, p_ref = ref.get(c, (0, 0))
        taxa_ref = e_ref / p_ref if p_ref else None
        taxa = ne[c] / npr[c] if npr[c] else None
        volta = (taxa_ref is not None and taxa is not None and npr[c] >= rv["min_prs"]
                 and taxa > rv["fator"] * taxa_ref)
        out[c] = dict(eventos=ne[c], prs=npr[c], taxa=taxa, ref=taxa_ref, ref_n=(e_ref, p_ref),
                      volta=volta)
    return out


def relatorio_volta(volta, prs, hoje, modelos=None):
    modelos = modelos or ler_modelos()
    rv = modelos["regra_de_volta"]
    ref = rv["referencia"]
    R = [f"Regra de volta (fila 21d): janela de {rv['janela_dias']} dias; volta se taxa > "
         f"{rv['fator']} x referencia com >= {rv['min_prs']} PRs da classe. Referencia de "
         f"{ref['desde']} a {ref['ate']}, em Opus, classe {ref['status']} (inferida).", "",
         "| classe | modelo | eventos / PRs na janela | taxa | referencia (eventos / PRs) "
         "| volta |", "|---|---|---|---|---|---|"]

    def num(x):
        return "-" if x is None else f"{x:.2f}"
    for c, v in volta.items():
        e_ref, p_ref = v["ref_n"]
        r = (f"{num(v['ref'])} ({e_ref} / {p_ref})" if v["ref"] is not None
             else f"sem referencia ({e_ref} / {p_ref}): so os numeros")
        R.append(f"| {c} | {modelos['classes'][c]} | {v['eventos']} / {v['prs']} "
                 f"| {num(v['taxa'])} | {r} | {'**SIM**' if v['volta'] else 'nao'} |")
    inicio = hoje - dt.timedelta(days=rv["janela_dias"])
    sem = [p for p in prs if inicio < dt.date.fromisoformat(p["data"]) <= hoje
           and not ETIQUETA.match(p["titulo"] or "") and "dependabot" not in p["autor"]]
    R += ["", f"PRs mergeados na janela sem etiqueta, fora da conta (Dependabot excluido): "
          f"{len(sem)}"]
    return "\n".join(R) + "\n"


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
    ap.add_argument("--prs", help="saida de `gh pr list --state merged --json "
                    "number,title,mergedAt,author`; sem ela a regra de volta nao roda")
    ap.add_argument("--titulo-pr", help="so valida a etiqueta do titulo de um PR e sai")
    ap.add_argument("--disparou", action="store_true",
                    help="com --prs: imprime so as classes que voltam (nada se nenhuma)")
    a = ap.parse_args(argv)
    if a.titulo_pr is not None:
        try:
            validar_titulo(a.titulo_pr)
        except EventoInvalido as ex:
            print(f"{ex}. Corrija o titulo do PR e empurre de novo.", file=sys.stderr)
            return 1
        return 0
    ev = validar(ler(a.eventos))
    if a.prs is None:
        if a.disparou:
            ap.error("--disparou precisa de --prs")
        print(relatorio(ev, sessoes_por_semana(a.turnos)), end="")
        print("\nRegra de volta: sem --prs os PRs nao foram lidos -- secao NAO medida aqui. "
              "No semanal o workflow passa a lista do GitHub.")
        return 0
    prs = prs_do_gh(a.prs)
    modelos = ler_modelos()
    hoje = dt.datetime.now(BRASILIA).date()
    volta = regra_de_volta(ev, prs, hoje, referencia(ler_referencia(modelos), modelos), modelos)
    if a.disparou:
        for c, v in volta.items():
            if v["volta"]:
                print(f"- {c}: {v['eventos']} eventos em {v['prs']} PRs (taxa {v['taxa']:.2f}, "
                      f"referencia {v['ref']:.2f}); sai de {modelos['classes'][c]} e sobe "
                      "um degrau")
        return 0
    print(relatorio(ev, sessoes_por_semana(a.turnos)), end="")
    print()
    print(relatorio_volta(volta, prs, hoje, modelos), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
