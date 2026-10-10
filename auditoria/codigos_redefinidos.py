#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Um codigo de achado tem UM endereco -- o que o `achados_ancorados` nao mede.

POR QUE ELE EXISTE. Em 04/10/2026 a auditoria do Codex chegou com tres achados chamados `A-01`,
`A-02` e `A-03`. Esses nomes ja eram achados deste projeto desde 11/09 (B3SA3 virou BSA, o
endpoint registrado errado, a emissora que muda de codigo). Registrar o documento como veio
dava a cada um DUAS definicoes, com sentidos diferentes, e o `achados_ancorados` fechava
verde: ele mede que o codigo citado tem endereco, e passou a ter dois. A citacao `# A-01` no
codigo deixava de dizer qual achado motivou a linha. A auditoria foi registrada com os nomes
trocados (CX-04 a CX-06, `docs/auditoria/AUDITORIA-CODEX-2026-10-03.md`), e esta guarda
impede a proxima colisao.

O QUE ELE MEDE (P5): os pares (codigo, arquivo) em que o codigo tem definicao -- cabecalho ou
linha de indice, as mesmas regex do `achados_ancorados` (N-01) -- em MAIS DE UM arquivo `.md`.
Todo par assim que nao esta na linha de base reprova. A linha de base so decresce: par
resolvido sai dela (`test_a_linha_de_base_nao_guarda_par_resolvido`).

O QUE ELE NAO MEDE, declarado:
  - SENTIDO. A guarda nao sabe se duas definicoes falam do mesmo achado. Copia legitima (o
    historico que guarda o texto de um achado que mudou de casa) e colisao (outro achado com o
    mesmo nome) reprovam igual, e quem separa e a leitura: copia legitima entra na linha de
    base com o motivo no PR; colisao ganha nome novo. Comparar titulos foi medido e descartado
    (04/10): titulos do mesmo achado divergem demais entre o ACHADOS.md e o historico (A-06, C-03,
    P-99), e um limiar de semelhanca seria pontuacao no lugar de portao (P3).
  - O prefixo `P` (pendencia). O numero de pendencia e sequencial e unico por construcao, e a
    pendencia muda de casa por rotina (ativas -> reserva -> fechadas, com instantaneo no
    historico). Colisao de `P-` nao foi observada; se aparecer, este corte esta errado.
  - Os pares que ja existiam em 04/10. Sao os escopos e laudos que numeram itens com o mesmo
    formato (`escopo-campos-de-analise.md`: A-01 a K-07; `laudo-auditoria-consolidado.md`:
    A-01 a R-05) -- a maior parte da linha de base. Estao la por existirem, nao por estarem
    certos: e a contagem que decai (familia do `sem_origem`).
  - Citacao sem definicao: e o trabalho do `achados_ancorados`.
"""
from __future__ import annotations
import argparse
import collections
import io
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)
import achados_ancorados as A  # noqa: E402 -- mesmas regex, mesmas pastas ignoradas (N-01)

LINHA_DE_BASE = os.path.join(AQUI, "redefinicoes_linha_de_base.txt")
PREFIXOS_FORA = {"P": "pendencia: numero sequencial e unico, muda de casa por rotina"}


def definicoes(raiz=RAIZ):
    """{codigo: {arquivo relativo}} das definicoes em `.md`, sem os prefixos de PREFIXOS_FORA."""
    out = collections.defaultdict(set)
    for caminho in A.arquivos(raiz):
        if not caminho.endswith(".md"):
            continue
        rel = os.path.relpath(caminho, raiz).replace("\\", "/")
        with io.open(caminho, encoding="utf-8", errors="replace") as f:
            for cod in definidos_no_texto(f.read()):
                out[cod].add(rel)
    return out


def definidos_no_texto(s):
    """Os codigos que um texto `.md` DEFINE (cabecalho ou linha de indice), sem os de
    PREFIXOS_FORA. Separado de `definicoes()` para a prova sobre um texto que nao esta na
    arvore (a auditoria com os nomes originais)."""
    out = set()
    for padrao in (A.DEF_CABECALHO, A.DEF_INDICE):
        for m in padrao.finditer(s):
            cod = f"{m.group(1)}-{m.group(2)}"
            if A.conta_como_codigo(cod) and m.group(1) not in PREFIXOS_FORA:
                out.add(cod)
    return out


def pares_em_colisao(defs):
    """{(codigo, arquivo)} dos codigos definidos em mais de um arquivo."""
    return {(c, f) for c, arqs in defs.items() if len(arqs) > 1 for f in arqs}


def ler_base(caminho=LINHA_DE_BASE):
    with io.open(caminho, encoding="utf-8") as f:
        linhas = [x.strip() for x in f if x.strip() and not x.startswith("#")]
    return {tuple(x.split(";", 1)) for x in linhas}


def novos(base, atuais):
    return sorted(atuais - base)


def resolvidos(base, atuais):
    return sorted(base - atuais)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--raiz", default=RAIZ)
    ap.add_argument("--gravar", action="store_true",
                    help="regrava a linha de base com os pares de hoje (so no PR que explica)")
    a = ap.parse_args(argv)
    atuais = pares_em_colisao(definicoes(a.raiz))
    base = ler_base() if os.path.exists(LINHA_DE_BASE) else set()
    nov, res = novos(base, atuais), resolvidos(base, atuais)
    print(f"{len(atuais)} pares em {len({c for c, _ in atuais})} codigos com mais de uma "
          f"definicao; linha de base {len(base)}; novos {len(nov)}; resolvidos {len(res)}")
    for c, f in nov:
        print(f"  NOVO: {c} definido tambem em {f}")
    if a.gravar:
        with io.open(LINHA_DE_BASE, "w", encoding="utf-8", newline="\n") as f:
            f.write("# codigo;arquivo com definicao de um codigo definido em mais de um arquivo.\n"
                    "# So decresce -- ver auditoria/codigos_redefinidos.py\n")
            for c, arq in sorted(atuais):
                f.write(f"{c};{arq}\n")
    return 1 if nov else 0


if __name__ == "__main__":
    raise SystemExit(main())
