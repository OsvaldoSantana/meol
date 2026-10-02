# -*- coding: utf-8 -*-
"""O universo e o sorteio da rodada 3 de marcas, a partir dos cadastros oficiais da CVM (P-170).

POR QUE EXISTE. A R3 audita categorias que as rodadas 1 e 2 nao viram, e a amostra que entra no
veto de distincao (livro de codigos, af-a) nao pode ser escolhida a mao: quem escolhe as marcas
depois de ver a classificacao de E, C e D poderia escolher o veto. Aqui o universo sai do
cadastro oficial, filtrado pelo `docs/marca/rodada3/plano.yaml`, e a ORDEM DE VISITA sai de uma
permutacao com semente fixa. A ordem vai para `docs/marca/rodada3/sorteio-<categoria>.csv` e e
empurrada antes da primeira marca classificada.

O QUE ELE NAO FAZ (P5). Nao baixa nada: le os arquivos de `data/r3/` (fora do git) e recusa
arquivo com sha256 diferente do plano. Nao visita site nem classifica marca. Nao copia e-mail,
telefone nem endereco do cadastro: so CNPJ, nome e o site declarado.

    python tools/r3_universo.py            # grava os sorteio-*.csv
    python tools/r3_universo.py --conferir  # sai 1 se algum gravado divergir
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import os
import re
import sys
import zipfile
from typing import Any

import numpy as np
import yaml

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA = os.path.join(RAIZ, "docs", "marca", "rodada3")
PLANO = os.path.join(PASTA, "plano.yaml")
EM_FUNCIONAMENTO = "EM FUNCIONAMENTO NORMAL"
COLUNAS = ["ordem", "cnpj", "nome", "site_declarado"]


def ler_plano(path: str = PLANO) -> dict[str, Any]:
    with open(path, encoding="utf-8") as f:
        d: dict[str, Any] = yaml.safe_load(f)
    return d


def _membro(fonte: dict[str, Any], membro: str) -> list[dict[str, str]]:
    """As linhas de um CSV dentro do ZIP oficial, depois de conferir o sha256 do ZIP (P1)."""
    path = os.path.join(RAIZ, *fonte["arquivo_local"].split("/"))
    with open(path, "rb") as f:
        dados = f.read()
    if hashlib.sha256(dados).hexdigest() != fonte["sha256"]:
        raise SystemExit(f"{fonte['arquivo_local']}: sha256 diferente do plano; outro arquivo e "
                         "outro sorteio")
    texto = zipfile.ZipFile(io.BytesIO(dados)).read(membro).decode("latin-1")
    return list(csv.DictReader(io.StringIO(texto), delimiter=";"))


def site_valido(texto: str | None) -> str | None:
    """O site declarado, ou None se o campo nao for um endereco de site."""
    s = (texto or "").strip()
    baixo = s.lower()
    if "@" in baixo or "cvm.gov.br" in baixo or not re.search(r"[a-z0-9-]+\.[a-z]{2,}", baixo):
        return None
    return s


def _digitos(s: str) -> str:
    return re.sub(r"\D", "", s or "")


def _nome(r: dict[str, str]) -> str:
    return (r.get("DENOM_COMERC") or "").strip() or (r.get("DENOM_SOCIAL") or "").strip()


def universo_cadastro(linhas: list[dict[str, str]], coluna_site: str,
                      tipos: list[str] | None = None) -> list[dict[str, str]]:
    """PJ em funcionamento, com site, um CNPJ uma vez (a primeira linha que tiver site)."""
    out: dict[str, dict[str, str]] = {}
    for r in linhas:
        if r.get("SIT") != EM_FUNCIONAMENTO:
            continue
        if tipos is not None and r.get("TP_PARTIC") not in tipos:
            continue
        site = site_valido(r.get(coluna_site))
        if site and r["CNPJ"] not in out:
            out[r["CNPJ"]] = {"cnpj": r["CNPJ"], "nome": _nome(r), "site_declarado": site}
    return list(out.values())


def universo_gestoras(fundos: list[dict[str, str]], situacao: str,
                      administradores: list[dict[str, str]],
                      coluna_site: str) -> list[dict[str, str]]:
    """Os gestores PJ de fundos na situacao dada, com o site do cadastro de administradores."""
    # o cadastro de fundos grava o CNPJ so com digitos; o de administradores, com pontuacao
    gestores = {_digitos(r["CPF_CNPJ_Gestor"]) for r in fundos
                if r.get("Situacao") == situacao and r.get("Tipo_Pessoa_Gestor") == "PJ"
                and r.get("CPF_CNPJ_Gestor")}
    adm = [r for r in administradores if _digitos(r["CNPJ"]) in gestores]
    return universo_cadastro(adm, coluna_site)


def sortear(universo: list[dict[str, str]], semente: int) -> list[dict[str, str]]:
    """A ordem de visita: permutacao com semente fixa sobre o universo em CNPJ crescente."""
    base = sorted(universo, key=lambda r: r["cnpj"])
    perm = np.random.default_rng(semente).permutation(len(base))
    return [{"ordem": str(i + 1), **base[j]} for i, j in enumerate(perm)]


def universos(plano: dict[str, Any]) -> dict[str, list[dict[str, str]]]:
    f = plano["fontes"]
    out = {}
    for cat, u in plano["universos"].items():
        if cat == "gestora_e_private":
            fundos = _membro(f[u["fonte"]], u["membro"])
            adm = _membro(f[u["site_de"]], u["membro_site"])
            out[cat] = universo_gestoras(fundos, u["situacao_do_fundo"], adm, u["coluna_site"])
        else:
            linhas = _membro(f[u["fonte"]], u["membro"])
            out[cat] = universo_cadastro(linhas, u["coluna_site"], u.get("tipos"))
    return out


def texto_csv(linhas: list[dict[str, str]]) -> str:
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=COLUNAS, lineterminator="\n")
    w.writeheader()
    w.writerows(linhas)
    return buf.getvalue()


def alvos(plano: dict[str, Any] | None = None) -> dict[str, str]:
    plano = ler_plano() if plano is None else plano
    return {os.path.join(PASTA, f"sorteio-{cat}.csv"): texto_csv(sortear(u, plano["semente"]))
            for cat, u in universos(plano).items()}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=(__doc__ or "").split("\n")[0])
    ap.add_argument("--conferir", action="store_true")
    a = ap.parse_args(argv)
    ruins = 0
    for path, texto in alvos().items():
        rel = os.path.relpath(path, RAIZ)
        n = texto.count("\n") - 1
        if a.conferir:
            with open(path, encoding="utf-8") as f:
                igual = f.read().replace("\r\n", "\n") == texto
            print(f"{rel}: {'ok' if igual else 'DIVERGE'} (n={n})")
            ruins += not igual
        else:
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(texto)
            print(f"gravado {rel} (n={n})")
    return 1 if ruins else 0


if __name__ == "__main__":
    sys.exit(main())
