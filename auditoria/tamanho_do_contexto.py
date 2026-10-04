#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Quanto custa LER este projeto -- medido, nunca estimado de cabeca.

POR QUE ELE EXISTE, e a resposta e uma retratacao. A secao 11.4 do `CLAUDE.md` declarou
em 06/09/2026 que o corte daquele dia levou a leitura inicial de "~26 mil" para "~13 mil"
tokens. **Os dois numeros estao errados, e nunca houve uma conta escrita.** Medidos em
19/09 com a razao real deste repositorio:

    declarado 06/09    1.112 + 911 linhas = "~26 mil"  ->  real ~38.400
    declarado 06/09      482 + 565 linhas = "~13 mil"  ->  real ~19.900

Treze dias depois, um plano de otimizacao de tokens **calibrou a propria regua** nos
"~13 mil" da 11.4 -- e errou a leitura inicial por 90% por causa disso. Numero plausivel
em prosa, sem procedencia, citado por terceiro como fonte: e o C-01 na camada do token.

    O `CLAUDE.md` tem a regra contra isso desde 12/09 -- *achado so entra com a conta
    escrita ou com o NAO_CONFIRMADO explicito*. A 11.4 e mais velha que a regra, e
    ninguem voltou para reconferi-la. **Regra nova nao audita o passado sozinha.**

O QUE ESTE MODULO NAO FAZ (P5, e sao tres limites duros):

  1. Ele NAO mede o tokenizador do Claude. Mede `cl100k_base` (OpenAI) quando o
     `tiktoken` esta instalado, e uma razao CHARS/TOKEN calibrada neste repositorio
     quando nao esta. Os dois sao PROXY. O que sobrevive e erro relativo e ordem de
     grandeza, nunca o valor absoluto.
  2. Ele NAO e dependencia do projeto. `tiktoken` nao entra no `pyproject.toml`: a P-15
     fecha a faixa de versoes e a impressao do ambiente e `7565df1381e2c1ed`. Foi por
     isso que a `multiplicidade.py` implementou a t de Student a mao em vez de trazer o
     scipy, e a mesma regra vale aqui. Sem `tiktoken`, o modulo usa a razao e DIZ que
     usou.
  3. Ele NAO mede o custo de uma sessao. Nao ve cache, nao ve resposta, nao ve saida de
     ferramenta -- e a auditoria de 19/09 concluiu que, com cache de prefixo, o custo
     dominante e justamente o que VARIA por turno. Este modulo mede o ESTAVEL, que e a
     parte que ele consegue ver. Chamar isso de "custo por sessao" seria a 11.4 outra vez.
"""
from __future__ import annotations
import argparse
import io
import os
import sys

# Razao medida em 19/09/2026 sobre os sete arquivos maiores do repositorio (CLAUDE.md,
# PENDENCIAS.md, PLANO.md, SEGUNDA-21.md, ACHADOS-19-09, politica.yaml, custos.yaml):
# 2,96 chars/token, desvio de 0,14 -- min 2,77, max 3,16.
#
# NAO use 14 tokens/linha. Essa razao vem de markdown em INGLES; medido aqui, markdown
# em portugues com tabelas e acentuacao da **19,0 tokens/linha**. O erro de 36% na razao
# foi o que produziu o erro de 90% na leitura inicial.
CHARS_POR_TOKEN = 2.96
TOKENS_POR_LINHA_MEDIDO = 19.0

# ── Quem entra na leitura de sessao, e o PORQUE ao lado ──────────────────────
# Sem esta lista, "leitura inicial = N tokens" e a suposicao de quem mediu, nao um fato
# do projeto -- e esse buraco foi achado na auditoria de 19/09: **o projeto nunca
# declarou qual e o conjunto de leitura inicial**. A lista e a declaracao.
SEMPRE = {
    "CLAUDE.md": ("so o que muda o que alguem faz -- lido inteiro em toda sessao; a "
                  "historia saiu para docs/historico/ em 26/09"),
    # 02/10/2026 (decisao dele): o PENDENCIAS.md saiu da abertura. O hook SessionStart injeta
    # o indice gerado por tools/estado.py, e a sessao le so a secao da P da tarefa.
    "docs/estado.md": "pendencias abertas e fila sem resposta, em menos de 2 mil tokens; injetado",
    "PLANO.md": "onde queremos chegar e a ordem do que falta",
    # 03/10/2026 (decisao dele, dieta completa): o PENDENCIAS.md volta, so com as ATIVAS (ate 20,
    # guardado por test_plano_e_pendencias.py). O resto aberto foi para docs/pendencias-reserva.md,
    # que e lido por busca e por isso nao entra aqui.
    "PENDENCIAS.md": "as pendencias ativas, ate 20 -- lidas inteiras desde 03/10",
    # 25/09/2026: o secao 2 do CLAUDE.md virou este arquivo (fonte unica, P2). Fora daqui ele
    # deixaria de ser lido, e as doutrinas sao o projeto.
    "docs/doutrinas.md": "as sete doutrinas -- sairam do CLAUDE.md e seguem lidas em toda sessao",
}
SOB_DEMANDA = {
    "ACHADOS.md": "historia dos achados -- so quando a tarefa toca a area",
    "README.md": "porta de entrada para humanos; repete o CLAUDE.md em resumo, nao instrui sessao",
    # 25/09/2026: os arquivos-padrao do GitHub. Sao para quem chega de fora, nao para a sessao.
    "CONTRIBUTING.md": "para contribuidor humano; a sessao segue o CLAUDE.md, secao 9",
    "SECURITY.md": "canal de relato privado; nao instrui sessao",
    "CODE_OF_CONDUCT.md": "texto padrao de conduta; nao instrui sessao",
    # 24/09/2026: a raiz foi limpa. Os bilhetes de entrega (LEIA-*, SEGUNDA-21, ENTREGA-19-09,
    # PROMPTS-*, RECRIAR-REPOSITORIO, DEPENDE-DE-VOCE) foram para docs/historico/entregas/, e
    # os laudos e desenhos para docs/referencia/. Quem pode morar na raiz e dado:
    # auditoria/raiz_viva.yaml, guardado por test_raiz_viva.py. As treze linhas da P-110
    # que estavam aqui descreviam arquivos que nao estao mais na raiz.
}


def instrumento():
    """(nome, funcao). Diz qual proxy esta em uso -- ferramenta que anuncia o proprio
    limite e ferramenta; ferramenta que so imprime numero e opiniao com sotaque."""
    try:
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        return "tiktoken cl100k_base (proxy: NAO e o tokenizador do Claude)", \
            lambda s: len(enc.encode(s))
    except Exception:
        return (f"razao medida {CHARS_POR_TOKEN} chars/token (tiktoken ausente; "
                f"proxy mais grosseiro, +-15%)"), \
            lambda s: round(len(s) / CHARS_POR_TOKEN)


def medir(raiz, contar):
    """[(nome, papel, linhas, chars, tokens, motivo)] para todo `.md` da raiz."""
    fora = []
    for nome in sorted(os.listdir(raiz)):
        if not nome.endswith(".md"):
            continue
        caminho = os.path.join(raiz, nome)
        if not os.path.isfile(caminho):
            continue
        with io.open(caminho, encoding="utf-8", errors="replace") as f:
            s = f.read()
        if nome in SEMPRE:
            papel, motivo = "SEMPRE", SEMPRE[nome]
        elif nome in SOB_DEMANDA:
            papel, motivo = "sob demanda", SOB_DEMANDA[nome]
        else:
            papel, motivo = "NAO CLASSIFICADO", ""
        fora.append((nome, papel, s.count("\n") + 1, len(s), contar(s), motivo))
    # O que e SEMPRE e mora fora da raiz tambem e leitura de sessao, e entra na conta.
    for nome in sorted(n for n in SEMPRE if "/" in n):
        caminho = os.path.join(raiz, *nome.split("/"))
        if os.path.isfile(caminho):
            with io.open(caminho, encoding="utf-8", errors="replace") as f:
                s = f.read()
            fora.append((nome, "SEMPRE", s.count("\n") + 1, len(s), contar(s), SEMPRE[nome]))
    return fora


def nao_classificados(linhas):
    """A contagem que DECAI (familia do `sem_origem`). Arquivo `.md` novo na raiz nasce
    sem papel, e ninguem sabe se ele entra na leitura de sessao. Classificar e escrever
    uma linha; nao classificar e deixar a proxima medicao errada."""
    return [x[0] for x in linhas if x[1] == "NAO CLASSIFICADO"]


def relatorio(raiz=".", saida=sys.stdout):
    nome_inst, contar = instrumento()
    linhas = medir(raiz, contar)
    print(f"instrumento: {nome_inst}\n", file=saida)
    print(f"{'arquivo':32} {'papel':16} {'linhas':>7} {'tokens':>8} {'tok/lin':>8}",
          file=saida)
    for n, papel, li, _ch, tk, _m in linhas:
        print(f"{n:32} {papel:16} {li:>7,} {tk:>8,} {tk/max(li,1):>8.1f}", file=saida)
    sempre = [x for x in linhas if x[1] == "SEMPRE"]
    total = sum(x[4] for x in sempre)
    print(f"\nLEITURA DE SESSAO ({len(sempre)} arquivos declarados SEMPRE): "
          f"{sum(x[2] for x in sempre):,} linhas, {total:,} tokens", file=saida)
    print("  Isto e o ESTAVEL. Com cache de prefixo ele e pago integral uma vez e a uma\n"
          "  fracao depois; o que custa integral em todo turno e o que MUDA -- resposta,\n"
          "  saida de ferramenta, arquivo reescrito -- e nada disso e medido aqui.",
          file=saida)
    orfaos = nao_classificados(linhas)
    if orfaos:
        print(f"\nAVISO: {len(orfaos)} arquivo(s) .md sem papel declarado: "
              f"{', '.join(orfaos)}\n  Classifique em SEMPRE ou SOB_DEMANDA, com o motivo "
              f"ao lado. Enquanto nao\n  estiver classificado, a linha de LEITURA DE "
              f"SESSAO acima esta incompleta.", file=saida)
    return total, orfaos


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--raiz", default=os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))))
    a = p.parse_args(argv)
    _total, orfaos = relatorio(a.raiz)
    return 1 if orfaos else 0


if __name__ == "__main__":
    raise SystemExit(main())
