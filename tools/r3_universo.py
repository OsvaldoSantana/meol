# -*- coding: utf-8 -*-
"""O universo e o sorteio da rodada 3 de marcas, a partir dos cadastros oficiais da CVM (P-170).

POR QUE EXISTE. A R3 audita categorias que as rodadas 1 e 2 nao viram, e a amostra que entra no
veto de distincao (livro de codigos, af-a) nao pode ser escolhida a mao: quem escolhe as marcas
depois de ver a classificacao de E, C e D poderia escolher o veto. Aqui o universo sai do
cadastro oficial, filtrado pelo `docs/marca/rodada3/plano.yaml`, e a ORDEM DE VISITA sai de uma
permutacao com semente fixa. A ordem vai para `docs/marca/rodada3/sorteio-<categoria>.csv` e e
empurrada antes da primeira marca classificada.

AS FONTES (10/10/2026 acrescentou duas ao ZIP da CVM). `tipo: cvm` (padrao) e o ZIP da CVM;
`tipo: json` e um recurso OData do Banco Central baixado inteiro; `tipo: planilha` e o .xlsx da
APIMEC, a entidade que a CVM autoriza a credenciar analistas (Resolucao CVM 20). Cada uma tem o
sha256 do arquivo no plano. A coluna `cnpj` do sorteio guarda o IDENTIFICADOR da fonte: o CNPJ
completo (CVM), a raiz de 8 digitos (BCB) ou `APIMEC-<registro>` (a APIMEC nao publica CNPJ).

UM UNIVERSO, DUAS CATEGORIAS. O cadastro de bancos do BCB nao separa banco de varejo de banco
digital: quem separa e o que o livro diz (agencia fisica x app), que so se ve na visita. O
universo `bancos` alimenta as duas (`categorias` no plano), e a categoria de cada marca sai da
leitura. Filtrar uma permutacao sorteada por uma propriedade e tomar as primeiras k e uma amostra
simples dessa propriedade; por isso a visita segue pela mesma lista ate as duas fecharem 10.

O QUE ELE NAO FAZ (P5). Nao baixa nada: le os arquivos de `data/r3/` (fora do git) e recusa
arquivo com sha256 diferente do plano. Nao visita site nem classifica marca. Nao copia e-mail,
telefone nem endereco do cadastro: so identificador, nome e o site declarado. Os arquivos
brutos so existem na maquina que os baixou; `--ordem` confere o que fica no git (cada
sorteio-*.csv e a permutacao da semente sobre as proprias linhas), sem eles.

    python tools/r3_universo.py                 # grava os sorteio-*.csv
    python tools/r3_universo.py --so bancos     # so esses universos (os outros arquivos ficam)
    python tools/r3_universo.py --conferir      # sai 1 se algum gravado divergir do cadastro
    python tools/r3_universo.py --ordem         # sai 1 se algum sorteio nao for a permutacao
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
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


def _conferido(fonte: dict[str, Any]) -> bytes:
    """Os bytes do arquivo local, depois de conferir o sha256 do plano (P1)."""
    path = os.path.join(RAIZ, *fonte["arquivo_local"].split("/"))
    with open(path, "rb") as f:
        dados = f.read()
    if hashlib.sha256(dados).hexdigest() != fonte["sha256"]:
        raise SystemExit(f"{fonte['arquivo_local']}: sha256 diferente do plano; outro arquivo e "
                         "outro sorteio")
    return dados


def _membro(fonte: dict[str, Any], membro: str) -> list[dict[str, str]]:
    """As linhas de um CSV dentro do ZIP oficial, depois de conferir o sha256 do ZIP (P1)."""
    texto = zipfile.ZipFile(io.BytesIO(_conferido(fonte))).read(membro).decode("latin-1")
    return list(csv.DictReader(io.StringIO(texto), delimiter=";"))


def _json(fonte: dict[str, Any]) -> list[dict[str, Any]]:
    """Um recurso OData do BCB baixado inteiro: uma lista de registros."""
    d: list[dict[str, Any]] = json.loads(_conferido(fonte).decode("utf-8"))
    return d


def ler_planilha(dados: bytes) -> list[dict[str, str]]:
    """A primeira aba de um .xlsx como uma lista de {letra da coluna: texto}, sem biblioteca.

    O .xlsx e um ZIP de XML. So o que o sorteio precisa: texto das celulas (compartilhado ou
    em linha). O cabecalho vem como a primeira linha; quem le escolhe as colunas pela LETRA,
    porque o rotulo do cabecalho da APIMEC nao acompanha o conteudo (10/10/2026: a coluna
    'Solicitacao' traz o numero de registro, e 'Vencimento' e 'Credenciamento' estao trocadas)."""
    ns = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    z = zipfile.ZipFile(io.BytesIO(dados))
    textos: list[str] = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", ns):
            textos.append("".join(x.text or "" for x in si.iter(f"{{{ns['m']}}}t")))
    linhas: list[dict[str, str]] = []
    for row in ET.fromstring(z.read("xl/worksheets/sheet1.xml")).iter(f"{{{ns['m']}}}row"):
        celulas: dict[str, str] = {}
        for c in row.findall("m:c", ns):
            letra = re.match(r"[A-Z]+", c.get("r") or "")
            if not letra:
                continue
            v = c.find("m:v", ns)
            if v is not None:
                celulas[letra.group(0)] = textos[int(v.text or 0)] if c.get("t") == "s" else (
                    v.text or "")
            else:
                inline = c.find("m:is", ns)
                celulas[letra.group(0)] = "" if inline is None else "".join(
                    x.text or "" for x in inline.iter(f"{{{ns['m']}}}t"))
        linhas.append(celulas)
    return linhas


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


def universo_registros(linhas: list[dict[str, Any]], u: dict[str, Any]) -> list[dict[str, str]]:
    """Um universo de registros (JSON do BCB ou planilha): filtra por `onde`, tira o site de
    `coluna_site` se o plano a declara, e guarda um identificador uma vez so.

    `onde` e {campo: valor exato}. `coluna_site: null` e uma fonte que NAO declara site (a
    planilha da APIMEC): o universo entra inteiro, com o site vazio, e quem nao tem site que se
    ache pela escada sai na visita (site_inacessivel), nao do sorteio."""
    coluna = u.get("coluna_site")
    prefixo = u.get("prefixo_chave", "")
    out: dict[str, dict[str, str]] = {}
    for r in linhas:
        if any(str(r.get(k) or "").strip() != v for k, v in (u.get("onde") or {}).items()):
            continue
        site = site_valido(r.get(coluna)) if coluna else ""
        if coluna and not site:
            continue
        bruto = str(r.get(u["chave"]) or "").strip()
        if not bruto:
            continue
        # `zeros`: numero de registro sem zeros a esquerda ordena "11" antes de "7" como texto
        ident = prefixo + bruto.zfill(int(u.get("zeros", 0)))
        nome = (str(r.get(u["nome"]) or "").strip()
                or str(r.get(u.get("nome_alternativo", "")) or "").strip())
        out.setdefault(ident, {"cnpj": ident, "nome": nome, "site_declarado": site or ""})
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


def universos(plano: dict[str, Any],
              so: list[str] | None = None) -> dict[str, list[dict[str, str]]]:
    f = plano["fontes"]
    out = {}
    for cat, u in plano["universos"].items():
        if so is not None and cat not in so:
            continue
        tipo = u.get("tipo", "cvm")
        if tipo == "json":
            out[cat] = universo_registros(_json(f[u["fonte"]]), u)
        elif tipo == "planilha":
            linhas = ler_planilha(_conferido(f[u["fonte"]]))
            out[cat] = universo_registros(linhas[1:], u)   # a linha 1 e o cabecalho
        elif cat == "gestora_e_private":
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


def alvos(plano: dict[str, Any] | None = None,
          so: list[str] | None = None) -> dict[str, str]:
    plano = ler_plano() if plano is None else plano
    return {os.path.join(PASTA, f"sorteio-{cat}.csv"): texto_csv(sortear(u, plano["semente"]))
            for cat, u in universos(plano, so).items()}


def ordem_confere(texto: str, semente: int) -> bool:
    """O sorteio gravado e a permutacao da semente sobre as PROPRIAS linhas dele?

    Nao precisa do cadastro bruto (que so existe na maquina que o baixou): reordena as linhas por
    identificador crescente, que e a base do `sortear`, e compara com o arquivo. Pega arquivo
    editado a mao e semente trocada; nao pega universo errado (isso e o `--conferir`)."""
    linhas = list(csv.DictReader(io.StringIO(texto)))
    base = [{c: r[c] for c in COLUNAS if c != "ordem"} for r in linhas]
    return texto_csv(sortear(base, semente)) == texto.replace("\r\n", "\n")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=(__doc__ or "").split("\n")[0])
    ap.add_argument("--conferir", action="store_true")
    ap.add_argument("--ordem", action="store_true")
    ap.add_argument("--so", nargs="+", metavar="UNIVERSO")
    a = ap.parse_args(argv)
    ruins = 0
    if a.ordem:
        semente = ler_plano()["semente"]
        for nome in sorted(os.listdir(PASTA)):
            if nome.startswith("sorteio-") and nome.endswith(".csv"):
                with open(os.path.join(PASTA, nome), encoding="utf-8") as f:
                    ok = ordem_confere(f.read(), semente)
                print(f"{nome}: {'ok' if ok else 'NAO e a permutacao da semente'}")
                ruins += not ok
        return 1 if ruins else 0
    for path, texto in alvos(so=a.so).items():
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
