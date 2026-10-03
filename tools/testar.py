#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A rodada do fim no modo do CI: uma linha por suite e so as falhas (decisao de 02/10/2026).

POR QUE ELE EXISTE. A rodada do CLAUDE.md 9 roda cinco suites e devolve milhares de linhas
de saida, que a sessao paga inteiras no contexto -- para saber, quase sempre, "verde". Este
script roda o mesmo que o `testes.yml` (job `rapido`) e imprime so o resumo de cada suite e
as linhas FAILED/ERROR.

    python tools/testar.py              # cinco suites + ruff + mypy, como o CI
    python tools/testar.py --sem-lint   # so as suites
    py -3.11 tools/testar.py --tudo     # no desktop: sem recorte, slow/acervo/privado inclusive

O QUE ELE NAO FAZ (P5):
  1. Sem `--tudo`, NAO e a rodada do CLAUDE.md 9 no desktop: fica fora `slow`, `acervo` e
     `privado`, como no push. O resumo sai com o recorte escrito ao lado (5-B.15).
  2. NAO substitui o CI. Verde aqui e verde nesta arvore, neste interpretador.
  3. Quando uma suite falha, a saida inteira dela fica em `.testar/<suite>.txt` (ignorado
     pelo git) -- a falha se le la, nao no contexto.
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import time

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Os mesmos do `.github/workflows/testes.yml`; `test_testar.py` reprova se divergirem.
SUITES = ("alocacao", "fase0", "auditoria", "tools", "medicoes")
MARCADOR = "not slow and not privado and not acervo"
SAIDAS = os.path.join(RAIZ, ".testar")


# Sem `-q`: o `addopts` do pyproject ja tem um, e `-qq` apaga a linha de resumo (medido em 03/10).
def comando_pytest(suite: str, marcador: str | None = MARCADOR) -> list[str]:
    filtro = ["-m", marcador] if marcador else []
    return [sys.executable, "-m", "pytest", suite, *filtro, "-n", "auto",
            "--dist", "loadgroup", "-p", "no:cacheprovider", "-rfE"]


def resumo(saida: str) -> str:
    """A ultima linha de contagem do pytest ("3 failed, 812 passed in 41.2s")."""
    for linha in reversed(saida.splitlines()):
        limpa = linha.strip().strip("=").strip()
        if re.search(r"\b(passed|failed|error|errors|skipped|deselected|no tests ran)\b", limpa) \
                and re.search(r"\bin [\d.]+s\b", limpa):
            return limpa
    return "sem linha de resumo (a coleta quebrou?)"


def falhas(saida: str) -> list[str]:
    return [x for x in saida.splitlines() if re.match(r"(FAILED|ERROR) ", x)]


def _rodar(nome: str, cmd: list[str], cwd: str, aceitos=(0,)) -> tuple[bool, str, str]:
    """(ok, saida, tempo). A saida de quem falhou vai inteira para .testar/<nome>.txt."""
    t0 = time.monotonic()
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    saida = r.stdout + r.stderr
    ok = r.returncode in aceitos
    if not ok:
        os.makedirs(SAIDAS, exist_ok=True)
        with open(os.path.join(SAIDAS, f"{nome}.txt"), "w", encoding="utf-8") as f:
            f.write(saida)
    return ok, saida, f"{time.monotonic() - t0:.0f}s"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--sem-lint", action="store_true", help="nao roda ruff nem mypy")
    ap.add_argument("--tudo", action="store_true",
                    help="sem recorte: slow, acervo e privado inclusive (a rodada do desktop)")
    a = ap.parse_args(argv)
    marcador = None if a.tudo else MARCADOR
    print("recorte: nenhum (--tudo)" if a.tudo else f'recorte: -m "{MARCADOR}" (o do push; 5-B.15)')
    tudo_ok = True
    for s in SUITES:
        # pytest sai 5 quando o marcador nao deixa teste nenhum: nao e falha.
        ok, saida, t = _rodar(s, comando_pytest(s, marcador), RAIZ, aceitos=(0, 5))
        tudo_ok &= ok
        print(f"{s:<14} {'OK   ' if ok else 'FALHA'} {resumo(saida)} [{t}]")
        for linha in falhas(saida):
            print(f"    {linha}")
    if not a.sem_lint:
        lint = [("ruff", [sys.executable, "-m", "ruff", "check", *SUITES], RAIZ)]
        lint += [(f"mypy {s}", [sys.executable, "-m", "mypy", "."], os.path.join(RAIZ, s))
                 for s in SUITES]
        for nome, cmd, cwd in lint:
            ok, _, t = _rodar(nome.replace(" ", "_"), cmd, cwd)
            tudo_ok &= ok
            print(f"{nome:<14} {'OK   ' if ok else 'FALHA'} [{t}]")
    if not tudo_ok:
        print(f"saida inteira do que falhou: {os.path.relpath(SAIDAS, RAIZ)}/")
    return 0 if tudo_ok else 1


if __name__ == "__main__":
    sys.exit(main())
