#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Carga inicial do armazem: o acervo que so existe no disco dele sobe uma vez (P-57).

O QUE SOBE. Tudo o que o acervo bruto tem de versao:
  - CVM: `data/bronze/cvm/<recurso>/<arquivo>` (a versao vigente) e
    `data/bronze/cvm/<recurso>/_snapshots/<stem>__v<AAAAMMDD>__<sha12>.<ext>` (as
    deslocadas -- inclusive as duas de 2024 de 13/09, que vieram dos `(1).zip` do
    navegador e sao a UNICA copia daquela versao, CV-01);
  - B3: `data/bronze/b3/cotahist/COTAHIST_A<ANO>.ZIP` e o banco de ISIN,
    `data/bronze/b3/isin/dt_captura=<AAAA-MM-DD>/isinp.zip` (P-145, 26/09: a ponte
    ticker -> CD_CVM le o EMISSOR.TXT dele, e sem ele no armazem a medicao da P-145 so
    rodaria no desktop). A captura mais recente e a canonica; as outras, snapshot;
  - eventos da B3 (P-150, 26/09): `data/bronze/b3/{indices,eventos,proventos}/
    dt_captura=<AAAA-MM-DD>/...`, o que o `coletar_b3.py` gravou em 11/09. Recurso, nome e
    chave saem das MESMAS funcoes do passo `captura_eventos_b3` (`capturar_eventos_b3.
    RECURSOS` e `nome_no_armazem`): o 11/09 e a primeira segunda do cron sao versoes do
    mesmo arquivo, nao dois arquivos. O inventario vai para `docs/acervo/b3_eventos/`, o
    acervo do passo, e o `manifesto.jsonl` do coletor (a procedencia de cada pedido) sobe
    como log, fora do teto, como o passo faz. Nada disso entra na release (P-136): a
    publicacao le so o acervo da CVM.
Cada uma vira `<fonte>/<recurso>/<arquivo>/<sha256>.<ext>`, e o snapshot volta ao nome
canonico: a versao e o sha256, o nome do disco era so onde ele cabia.

PLANO POR PADRAO (como o `nomear_extracoes.py` e o `--arrumar`). Sem `--aplicar` nada sai
da maquina: o plano diz o que subiria, com o sha256 de cada arquivo. Com `--aplicar`, sobe
com `enviar_se_ausente` -- rodar duas vezes nao muda nada -- e grava o inventario em
`docs/acervo/<fonte>/inventario-armazem.csv` (versionado, so metadado). O inventario so e
escrito depois do envio: inventario de objeto que nao subiu seria o registro mentindo.

PARAR. Snapshot cujo nome promete um sha12 que os bytes nao tem para o plano inteiro --
o nome e procedencia, e procedencia que nao bate nao sobe. Arquivo fora das convencoes sai
DESCONHECIDO e nao e tocado: decidir o que e lixo e de quem olhou o arquivo.

USO (na maquina dele, com as credenciais R2_* no ambiente):
  py -3.11 fase0/subir_acervo_local.py            # plano
  py -3.11 fase0/subir_acervo_local.py --aplicar  # sobe e grava o inventario
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)
import acervo as acervo_mod  # noqa: E402
import armazem as armazem_mod  # noqa: E402
import capturar_eventos_b3 as eventos_b3  # noqa: E402
import manifesto_cvm  # noqa: E402

SUBIR, PARAR, DESCONHECIDO = "SUBIR", "PARAR", "DESCONHECIDO"
SNAPSHOT = re.compile(r"^(?P<stem>.+)__v(?P<versao>\d{8}|DESCONHECIDA)__(?P<sha12>[0-9a-f]{12})"
                      r"(?P<ext>\.\w+)$")
COTAHIST = re.compile(r"^COTAHIST_A\d{4}\.ZIP$", re.IGNORECASE)
RECURSOS_CVM = ("dfp", "itr", "fca", "cad")   # fca: P-132, 25/09
ISIN_CAPTURA = re.compile(r"^dt_captura=(?P<data>\d{4}-\d{2}-\d{2})$")


def _item(fonte, recurso, arquivo, caminho, papel, versao=""):
    return dict(acao=SUBIR, fonte=fonte, recurso=recurso, arquivo=arquivo, caminho=caminho,
                papel=papel, versao=versao, sha256="", bytes=0, chave="", motivo="")


def _eventos_b3(b3):
    """Os itens do acervo de eventos (P-150). O dia mais recente de cada arquivo e o
    canonico; os outros, snapshot -- a mesma regra do ISIN."""
    out = []
    for pasta, recurso in eventos_b3.RECURSOS.items():
        base = os.path.join(b3, pasta)
        for dirpath, _dirs, nomes in os.walk(base):
            for n in sorted(nomes):
                cam = os.path.join(dirpath, n)
                partes = os.path.relpath(cam, base).replace("\\", "/").split("/")
                m = ISIN_CAPTURA.match(partes[0])
                if not (m and len(partes) > 1 and n.endswith(".json")):
                    out.append(dict(_item("b3", recurso, n, cam, ""), acao=DESCONHECIDO,
                                    acervo=eventos_b3.ACERVO,
                                    motivo="nao e dt_captura=<AAAA-MM-DD>/.../*.json"))
                    continue
                out.append(dict(_item("b3", recurso, eventos_b3.nome_no_armazem(partes), cam,
                                      "", m["data"].replace("-", "")),
                                acervo=eventos_b3.ACERVO))
    ultimo = {}
    for x in out:
        if x["acao"] == SUBIR:
            k = (x["recurso"], x["arquivo"])
            ultimo[k] = max(ultimo.get(k, ""), x["versao"])
    for x in out:
        if x["acao"] == SUBIR:
            x["papel"] = ("canonico" if x["versao"] == ultimo[(x["recurso"], x["arquivo"])]
                          else "snapshot")
    man = os.path.join(b3, "manifesto.jsonl")
    if os.path.isfile(man):
        out.append(dict(_item("b3", "manifesto_coletor", "manifesto.jsonl", man, "log"),
                        acervo=eventos_b3.ACERVO, log=True))
    return out


def plano(repo):
    """Lista do que subiria. Calcula o sha256 de cada arquivo -- e o custo de a chave
    ser o conteudo, e o plano nao pode prometer uma chave sem ter medido."""
    out = []
    base = os.path.join(repo, "data", "bronze")
    for recurso in RECURSOS_CVM:
        pasta = os.path.join(base, "cvm", recurso)
        if not os.path.isdir(pasta):
            continue
        for a in sorted(os.listdir(pasta)):
            p = os.path.join(pasta, a)
            if a == "_snapshots" and os.path.isdir(p):
                for s in sorted(os.listdir(p)):
                    m = SNAPSHOT.match(s)
                    it = _item("cvm", recurso, (m["stem"] + m["ext"]) if m else s,
                               os.path.join(p, s), "snapshot", m["versao"] if m else "")
                    if not m:
                        it.update(acao=DESCONHECIDO, motivo="nome fora da convencao 2.6")
                    else:
                        it["sha12"] = m["sha12"]
                    out.append(it)
            elif os.path.isfile(p) and a.lower().endswith((".zip", ".csv")):
                out.append(_item("cvm", recurso, a, p, "canonico"))
            else:
                out.append(dict(_item("cvm", recurso, a, p, ""), acao=DESCONHECIDO,
                                motivo="nao e ZIP, CSV nem _snapshots"))
    pasta = os.path.join(base, "b3", "cotahist")
    if os.path.isdir(pasta):
        for a in sorted(os.listdir(pasta)):
            p = os.path.join(pasta, a)
            if os.path.isfile(p) and COTAHIST.match(a):
                out.append(_item("b3", "cotahist", a, p, "canonico"))
            else:
                out.append(dict(_item("b3", "cotahist", a, p, ""), acao=DESCONHECIDO,
                                motivo="nao e COTAHIST_A<ANO>.ZIP"))
    pasta = os.path.join(base, "b3", "isin")
    if os.path.isdir(pasta):
        capturas = sorted(d for d in os.listdir(pasta) if ISIN_CAPTURA.match(d)
                          and os.path.isfile(os.path.join(pasta, d, "isinp.zip")))
        for d in capturas:
            out.append(_item("b3", "isin", "isinp.zip", os.path.join(pasta, d, "isinp.zip"),
                             "canonico" if d == capturas[-1] else "snapshot",
                             ISIN_CAPTURA.match(d)["data"].replace("-", "")))
        for d in sorted(set(os.listdir(pasta)) - set(capturas)):
            out.append(dict(_item("b3", "isin", d, os.path.join(pasta, d), ""),
                            acao=DESCONHECIDO,
                            motivo="nao e dt_captura=<AAAA-MM-DD>/isinp.zip"))
    out += _eventos_b3(os.path.join(base, "b3"))
    for it in out:
        if it["acao"] != SUBIR:
            continue
        it["sha256"] = armazem_mod.sha256(it["caminho"])
        it["bytes"] = os.path.getsize(it["caminho"])
        if it.get("sha12") and not it["sha256"].startswith(it["sha12"]):
            it.update(acao=PARAR, motivo=f"o nome promete sha12 {it['sha12']} e os bytes "
                                         f"dao {it['sha256'][:12]}")
            continue
        if it.get("log"):
            # o log nao e versao de arquivo: vai para a pasta de logs do passo, com o sha12
            # no nome para que rodar de novo nao suba outra copia
            it["chave"] = (f"{eventos_b3.LOGS}/carga-inicial__manifesto__"
                           f"{it['sha256'][:12]}.jsonl")
            continue
        it["chave"] = armazem_mod.chave(it["fonte"], it["recurso"], it["arquivo"],
                                        it["sha256"])
    return out


def inventario(repo, fonte):
    return os.path.join(repo, "docs", "acervo", fonte, acervo_mod.INVENTARIO)


def aplicar(itens, armazem, repo, agora=None):
    """Sobe e grava o inventario. Com um PARAR no plano, nada sobe."""
    if any(x["acao"] == PARAR for x in itens):
        raise SystemExit("ha PARAR no plano: nada foi enviado")
    agora = agora or dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    enviados = 0
    por_fonte = {}                  # pasta do acervo (a fonte, ou b3_eventos) -> linhas
    for x in itens:
        if x["acao"] != SUBIR:
            continue
        enviados += armazem.enviar_se_ausente(x["chave"], x["caminho"],
                                              isento_do_teto=bool(x.get("log")))
        por_fonte.setdefault(x.get("acervo", x["fonte"]), []).append(dict(
            fonte=x["fonte"], recurso=x["recurso"], arquivo=x["arquivo"],
            sha256=x["sha256"], bytes=x["bytes"], chave=x["chave"], papel=x["papel"],
            versao=x["versao"], origem=os.path.relpath(x["caminho"], repo).replace("\\", "/"),
            dt_envio=agora))
    for fonte, linhas in por_fonte.items():
        _gravar_inventario(inventario(repo, fonte), linhas)
    return enviados


def _gravar_inventario(caminho, novas):
    """Acrescenta sem repetir chave: rodar de novo nao duplica linha, e a data do primeiro
    envio de cada chave fica."""
    existentes = acervo_mod._ler(caminho)
    vistas = {ln["chave"] for ln in existentes}
    linhas = existentes + [ln for ln in novas if ln["chave"] not in vistas]
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=acervo_mod.COLUNAS_INVENTARIO, delimiter=";")
        w.writeheader()
        for ln in sorted(linhas, key=lambda ln: ln["chave"]):
            w.writerow({c: ln.get(c, "") for c in acervo_mod.COLUNAS_INVENTARIO})


def main(argv=None, armazem=None, repo=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--aplicar", action="store_true", help="sobe e grava o inventario")
    p.add_argument("--armazem", choices=["s3"], default="s3")
    a = p.parse_args(argv)
    repo = repo or manifesto_cvm.raiz_do_repositorio(AQUI)
    itens = plano(repo)
    for x in itens:
        print(f"{x['acao']:12s} {os.path.relpath(x['caminho'], repo)}"
              + (f"\n{'':12s} -> {x['chave']}" if x["chave"] else "")
              + (f"\n{'':12s} {x['motivo']}" if x["motivo"] else ""))
    cont = {k: sum(x["acao"] == k for x in itens) for k in (SUBIR, PARAR, DESCONHECIDO)}
    total = sum(x["bytes"] for x in itens if x["acao"] == SUBIR)
    print("  ".join(f"{k} {v}" for k, v in cont.items()) + f"  ({total / 2**20:,.0f} MiB)")
    if cont[PARAR]:
        return 1
    if not a.aplicar:
        print("plano apenas: nada saiu da maquina. --aplicar para enviar.")
        return 0
    n = aplicar(itens, armazem or armazem_mod.do_ambiente(a.armazem), repo)
    print(f"enviados {n}; ja estavam no armazem {cont[SUBIR] - n}. Inventario gravado.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
