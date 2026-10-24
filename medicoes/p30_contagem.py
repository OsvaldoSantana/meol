#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P-30 parte 1 / P-17 (27c): quantas empresas SAIRIAM em cada ponto da grade do bloco C.

A PERGUNTA. Para cada corte do bloco C (C-01, C-03, C-05; o C-02 e NAO_IMPLEMENTADA) e
cada ponto da grade que o `politica.yaml` declara, quantas empresas do universo reprovariam.
So o numero: ele escolhe o corte vendo a contagem (27c), e o limiar so e gravado depois,
com impressao digital (P4). Nenhum limiar esta ativo; esta medicao nao grava nenhum.

AS DEFINICOES, fixadas antes de rodar:
  - universo: CD_CVM do cadastro (`cad_cia_aberta.csv`, versao vigente do acervo) com SIT ATIVO e
    CATEG_REG "Categoria A" (emissor de acoes). Escolha de Claude, 24/10/2026, para o N: nao ha
    ponte papel -> CD_CVM ainda (P-145), entao nao e "as acoes do indice";
  - data: `--ate` (padrao 2026-10-24), nos dois modos do leitor (captura e dt_receb);
  - o documento e o EXERCICIO mais recente conhecido em `ate`, ate `janela_de_exercicios` anos
    para tras, escolhido pelo leitor (fase0/leitor_cvm.py), nunca pelo DT_REFER;
  - banco e seguradora (RECUSA_REGIME), setor financeiro-adjacente ou vazio e CD_CVM fora do
    cadastro (EXIGE_DOSSIE) e empresa sem dado entram em linhas SEPARADAS, nunca no numero.

O QUE A SAIDA NAO TEM: nome, CD_CVM, valor de conta, preco ou retorno (P-136). So contagens e
rotulos de codigo (n de cada numero, 5-B.14).

O QUE ELA NAO MEDE (P5): o universo e o do cadastro de HOJE (nao as-of); nao liga papel a empresa
(P-145); o C-02 e o C-04 nao entram; a composicao do caixa e da divida e a de
`politica.yaml -> bloco_C_solvencia.operandos` (escolha de Claude, a ser vista por ele); 17 de
467 emissores do DFP 2024 trazem outro plano de contas e saem como PLANO_DE_CONTAS_DIFERENTE.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for pasta in (os.path.join(RAIZ, "fase0"), os.path.join(RAIZ, "alocacao")):
    if pasta not in sys.path:
        sys.path.insert(0, pasta)
import acervo  # noqa: E402
import bloco_c as B  # noqa: E402
import leitor_cvm as L  # noqa: E402

ATE_PADRAO = dt.date(2026, 10, 24)
MODOS = ("captura", "dt_receb")
SIT_DO_UNIVERSO, CATEGORIA_DO_UNIVERSO = "ATIVO", "Categoria A"


def universo_do_cadastro(caminho):
    """{CD_CVM} com SIT ATIVO e Categoria A: o universo da contagem."""
    with open(caminho, encoding="latin-1", newline="") as f:
        return {int(ln["CD_CVM"]) for ln in csv.DictReader(f, delimiter=";")
                if ln["SIT"] == SIT_DO_UNIVERSO and ln["CATEG_REG"] == CATEGORIA_DO_UNIVERSO}


def contar_modo(universo, cadastro, ate, modo, P, **kw):
    n = len(universo)
    return B.contar([B.avaliar(cd, ate, cadastro, P, n_universo=n, conhecimento=modo, **kw)
                     for cd in sorted(universo)], P)


def relatorio(contagens, meta):
    """Texto so com contagens. `contagens` = {modo: saida de bloco_c.contar}."""
    li = ["# P-30: quantas empresas sairiam em cada ponto da grade (27c)", ""]
    for k, v in meta.items():
        li.append(f"{k}: {v}")
    li.append("")
    for modo, c in contagens.items():
        li += [f"## modo {modo}", "",
               f"universo: {c['universo_total']}; regime: "
               + ", ".join(f"{s}={n}" for s, n in c["regime"].items())
               + f"; sem dado: {c['sem_dado']}; nao implementadas: "
               + (", ".join(c["nao_implementadas"]) or "nenhuma"), ""]
        li += ["| corte | ponto | sairiam | com valor | indefinido | plano diferente | sem dado |",
               "|---|---|---|---|---|---|---|"]
        for cod, m in c["cortes"].items():
            for ponto, n in m["grade"].items():
                li.append(f"| {cod} | {ponto} | {n} | {m['com_valor']} | {m['indefinido']} | "
                          f"{m['plano_diferente']} | {m['sem_dado']} |")
                li.append(f"RESUMO: modo={modo} {cod} ponto={ponto} sairiam={n} "
                          f"(n={m['com_valor']} com valor, universo={c['universo_total']})")
        li.append("")
    return "\n".join(li) + "\n"


def _insumos(P, ate):
    ano = ate.year
    anos = [ano - k for k in range(1, P["janela_de_exercicios"] + 1)]
    return [("cad", "cad_cia_aberta.csv")] + [("dfp", f"dfp_cia_aberta_{a}.zip") for a in anos]


def conferir_insumos(ate=ATE_PADRAO, repo=None):
    faltas = []
    for recurso, arquivo in _insumos(B.carregar(), ate):
        try:
            L.versao_mais_recente(recurso, arquivo, repo)
        except L.SemCaptura as e:
            faltas.append(str(e))
    return faltas


def main(argv=None):
    ap = argparse.ArgumentParser(description=(__doc__ or "").split("\n")[0])
    ap.add_argument("--conferir-insumos", action="store_true")
    ap.add_argument("--ate", type=dt.date.fromisoformat, default=ATE_PADRAO)
    a = ap.parse_args(argv)
    faltas = conferir_insumos(a.ate)
    for f in faltas:
        print("FALTA", f)
    if a.conferir_insumos or faltas:
        return 1 if faltas else 0
    P = B.carregar()
    vig = {arq: L.versao_mais_recente(rec, arq)["sha256"] for rec, arq in _insumos(P, a.ate)}
    caminho = acervo.abrir("cad", "cad_cia_aberta.csv", vig["cad_cia_aberta.csv"], conferir=True)
    cadastro = B.ler_cadastro(caminho, P)
    universo = universo_do_cadastro(caminho)
    meta = {"data": a.ate.isoformat(), "politica": "alocacao/politica.yaml bloco_C_solvencia",
            "universo": f"{len(universo)} CD_CVM, SIT {SIT_DO_UNIVERSO}, {CATEGORIA_DO_UNIVERSO}",
            **{f"sha256 {arq}": sha for arq, sha in vig.items()}}
    contagens = {m: contar_modo(universo, cadastro, a.ate, m, P) for m in MODOS}
    sys.stdout.write(relatorio(contagens, meta))
    return 0


if __name__ == "__main__":
    sys.exit(main())
