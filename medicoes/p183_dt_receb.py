#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P-183: quanto o modo `conhecimento="dt_receb"` do leitor as-of esconde, de 2010 a 2025.

A PERGUNTA. O modo dt_receb (fase0/leitor_cvm.py) responde um documento so quando a versao
PRESENTE no demonstrativo ja tinha sido recebida em D, porque o demonstrativo traz so a ultima
versao. Entre a 1a versao e a ultima o mercado conhecia um documento que o leitor nao mostra.
Esta medicao conta quanto: documento-meses ocultos, por ano e por demonstrativo.

AS DEFINICOES, fixadas antes de rodar:
  - documento: (CD_CVM, DT_REFER) no indice do ZIP do ano ({recurso}_cia_aberta_{ano}.csv);
  - r1: o menor DT_RECEB do documento (a 1a versao conhecida); rp: o DT_RECEB da versao
    PRESENTE (a do demonstrativo; no recorte por ano, a maior VERSAO do indice, e a
    diferenca entre as duas e contada por demonstrativo);
  - documento-mes: cada fim de mes D com r1 <= D <= HORIZONTE. HORIZONTE = 31/08/2026, o
    ultimo fim de mes antes da primeira captura (24/09/2026): o periodo que so a segunda data
    alcanca;
  - oculto: o documento-mes com D < rp (a versao presente ainda nao tinha chegado), que ja
    existia em D porque r1 <= D;
  - versao com dois DT_RECEB no indice: contada a parte (o leitor a recusa) e fora das somas.

OS INSUMOS: as versoes VIGENTES de dfp_cia_aberta_2010-2025 e itr_cia_aberta_2011-2025, pelo
`acervo.abrir` (no `medir/`, com o token de leitura) ou de uma pasta local (`--pasta`), com o
sha256 de cada arquivo conferido contra o registro e impresso na saida (P1). Em 16/10/2026 a
pasta foi a release publica cvm-acervo-2026 (degrau 2: copia publica do acervo).

O QUE A SAIDA NAO TEM: valor de conta nenhum. So contagens e rotulos (n de cada numero, 5-B.14).

O QUE ELA NAO MEDE (P5): quantas versoes substituidas ainda podem ser lidas no ENET ou na
Wayback (isso e o resolve da limitacao, nao o tamanho dela); e o peso economico do oculto
(um documento-mes oculto de uma empresa grande vale o mesmo que o de uma pequena).
"""
from __future__ import annotations

import argparse
import collections
import csv
import datetime as dt
import glob
import hashlib
import io
import os
import statistics
import sys
import zipfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FASE0 = os.path.join(RAIZ, "fase0")
if FASE0 not in sys.path:
    sys.path.insert(0, FASE0)
import acervo  # noqa: E402
import leitor_cvm as L  # noqa: E402

HORIZONTE = dt.date(2026, 8, 31)
ANOS = tuple(range(2010, 2026))
INSUMOS = ([("dfp", a) for a in ANOS] + [("itr", a) for a in ANOS if a >= 2011])


# ------------------------------------------------------------------ funcoes puras (testadas) ---

def fins_de_mes(de, ate):
    """Os fins de mes D com de <= D <= ate, em ordem."""
    out = []
    a, m = de.year, de.month
    while True:
        prox = dt.date(a + (m == 12), m % 12 + 1, 1)
        fim = prox - dt.timedelta(days=1)
        if fim > ate:
            return out
        if fim >= de:
            out.append(fim)
        a, m = prox.year, prox.month


def meses_do_documento(versoes, presente, horizonte=None):
    """(existentes, ocultos) em documento-meses. `versoes`: {VERSAO: {DT_RECEB}}; `presente`:
    a VERSAO do demonstrativo. None se a presente nao tem data unica (fora das somas)."""
    datas = versoes.get(presente)
    if not datas or len(datas) != 1:
        return None
    rp = next(iter(datas))
    r1 = min(min(ds) for ds in versoes.values())
    meses = fins_de_mes(r1, HORIZONTE if horizonte is None else horizonte)
    return len(meses), sum(1 for d in meses if d < rp)


def maior_versao(versoes):
    return max(versoes, key=int)


# ------------------------------------------------------------------------ leitura dos ZIPs ---

def _indice(z, recurso, ano):
    nome = L.leiaute()["indice"]["membro"].format(recurso=recurso, ano=ano)
    lei = L.leiaute()["arquivo"]
    docs = collections.defaultdict(lambda: collections.defaultdict(set))
    with z.open(nome) as f:
        for ln in csv.DictReader(io.TextIOWrapper(f, encoding=lei["codificacao"]),
                                 delimiter=lei["separador"]):
            docs[(int(ln["CD_CVM"]), ln["DT_REFER"])][ln["VERSAO"]].add(
                dt.date.fromisoformat(ln["DT_RECEB"]))
    return docs


def _presentes(z, recurso, ano, demonstrativo):
    """{(CD_CVM, DT_REFER): {VERSAO}} das linhas do membro (todas as ORDEM_EXERC: a VERSAO e
    do documento, nao da linha)."""
    lei = L.leiaute()["arquivo"]
    nome = lei["membro"].format(recurso=recurso, demonstrativo=demonstrativo, ano=ano)
    if nome not in z.namelist():
        return None
    out = collections.defaultdict(set)
    with z.open(nome) as f:
        r = csv.reader(io.TextIOWrapper(f, encoding=lei["codificacao"]), delimiter=lei["separador"])
        cab = next(r)
        i_cd, i_ref, i_ver = cab.index("CD_CVM"), cab.index("DT_REFER"), cab.index("VERSAO")
        for ln in r:
            out[(int(ln[i_cd]), ln[i_ref])].add(ln[i_ver])
    return out


def medir_arquivo(caminho, recurso, ano):
    """Os contadores de um ZIP: por ano (indice) e por demonstrativo (indice x membro)."""
    lei = L.leiaute()
    dems = [f"{d}_{v}" for d in lei["demonstrativos"] for v in lei["variantes"]]
    with zipfile.ZipFile(caminho) as z:
        docs = _indice(z, recurso, ano)
        ano_c = collections.Counter()
        ocultos_por_doc = []
        for versoes in docs.values():
            ano_c["documentos"] += 1
            ano_c["com_mais_de_uma_versao"] += len(versoes) > 1
            m = meses_do_documento(versoes, maior_versao(versoes))
            if m is None:
                ano_c["versao_presente_com_duas_datas"] += 1
                continue
            ano_c["documento_meses"] += m[0]
            ano_c["documento_meses_ocultos"] += m[1]
            if m[1]:
                ano_c["documentos_com_mes_oculto"] += 1
                ocultos_por_doc.append(m[1])
        por_dem = {}
        for dem in dems:
            pres = _presentes(z, recurso, ano, dem)
            c = collections.Counter()
            if pres is None:
                c["membro_ausente"] = 1
                por_dem[dem] = c
                continue
            for chave, vs in pres.items():
                c["documentos"] += 1
                if len(vs) > 1:
                    c["mais_de_uma_versao_no_membro"] += 1
                    continue
                vp = next(iter(vs))
                versoes = docs.get(chave)
                if not versoes or vp not in versoes:
                    c["versao_presente_fora_do_indice"] += 1
                    continue
                if vp != maior_versao(versoes):
                    c["presente_nao_e_a_maior_do_indice"] += 1
                m = meses_do_documento(versoes, vp)
                if m is None:
                    c["versao_presente_com_duas_datas"] += 1
                    continue
                c["documento_meses"] += m[0]
                c["documento_meses_ocultos"] += m[1]
                c["documentos_com_mes_oculto"] += bool(m[1])
            por_dem[dem] = c
    return ano_c, ocultos_por_doc, por_dem


# ------------------------------------------------------------------------------- insumos ---

def _sha(caminho):
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def caminhos(pasta=None, repo=None):
    """{(recurso, ano): (caminho, sha256)} das versoes vigentes, conferidas contra o registro."""
    out = {}
    for recurso, ano in INSUMOS:
        arquivo = f"{recurso}_cia_aberta_{ano}.zip"
        vig = L.versao_mais_recente(recurso, arquivo, repo)["sha256"]
        if pasta:
            achados = glob.glob(os.path.join(pasta, f"{recurso}_cia_aberta_{ano}__{vig[:12]}.zip"))
            if not achados:
                raise SystemExit(f"{arquivo}: a versao vigente {vig[:12]} nao esta em {pasta}")
            c = achados[0]
            if _sha(c) != vig:
                raise SystemExit(f"{c}: sha256 diverge do registro ({vig[:12]})")
        else:
            c = acervo.abrir(recurso, arquivo, vig, conferir=True)
        out[(recurso, ano)] = (c, vig)
    return out


def conferir_insumos(repo=None):
    faltas = []
    for recurso, ano in INSUMOS:
        arquivo = f"{recurso}_cia_aberta_{ano}.zip"
        try:
            L.versao_mais_recente(recurso, arquivo, repo)
        except L.SemCaptura as e:
            faltas.append(str(e))
    return faltas


# ------------------------------------------------------------------------------ relatorio ---

def _pct(a, b):
    return f"{100 * a / b:.1f}%" if b else "-"


def relatorio(por_arquivo, shas):
    li = ["# P-183: o que o modo dt_receb esconde (documento-meses, 2010-2025)", "",
          f"horizonte: {HORIZONTE.isoformat()} (o ultimo fim de mes antes da 1a captura)", ""]
    li += ["## por ano do arquivo (dfp + itr; n = documentos do indice)", "",
           "| ano | documentos | com >1 versao | com mes oculto | documento-meses | ocultos | % | "
           "meses ocultos por doc oculto (mediana, max) | versao com 2 datas |",
           "|---|---|---|---|---|---|---|---|---|"]
    tot = collections.Counter()
    tot_ocultos = []
    for ano in ANOS:
        c = collections.Counter()
        oc = []
        for (rec, a), (ac, ocd, _) in por_arquivo.items():
            if a == ano:
                c.update(ac)
                oc += ocd
        tot.update(c)
        tot_ocultos += oc
        med = f"{statistics.median(oc):g}, {max(oc)}" if oc else "-"
        li.append(f"| {ano} | {c['documentos']} | {c['com_mais_de_uma_versao']} | "
                  f"{c['documentos_com_mes_oculto']} | {c['documento_meses']} | "
                  f"{c['documento_meses_ocultos']} | "
                  f"{_pct(c['documento_meses_ocultos'], c['documento_meses'])} | {med} | "
                  f"{c['versao_presente_com_duas_datas']} |")
    med = f"{statistics.median(tot_ocultos):g}, {max(tot_ocultos)}" if tot_ocultos else "-"
    li.append(f"| **total** | {tot['documentos']} | {tot['com_mais_de_uma_versao']} | "
              f"{tot['documentos_com_mes_oculto']} | {tot['documento_meses']} | "
              f"{tot['documento_meses_ocultos']} | "
              f"{_pct(tot['documento_meses_ocultos'], tot['documento_meses'])} | {med} | "
              f"{tot['versao_presente_com_duas_datas']} |")
    for rec in ("dfp", "itr"):
        c = collections.Counter()
        for (r, _a), (ac, _o, _d) in por_arquivo.items():
            if r == rec:
                c.update(ac)
        li.append(f"\nRESUMO: {rec} 2010-2025: {c['documento_meses_ocultos']} de "
                  f"{c['documento_meses']} documento-meses ocultos "
                  f"({_pct(c['documento_meses_ocultos'], c['documento_meses'])}), "
                  f"{c['documentos_com_mes_oculto']} de {c['documentos']} documentos")
    li += ["", "## por demonstrativo (dfp + itr, todos os anos; n = documentos no membro)",
           "", "| demonstrativo | documentos | com mes oculto | documento-meses | ocultos | % | "
           "presente != maior do indice | presente fora do indice | >1 versao no membro | "
           "2 datas | arquivos sem o membro |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    dems = sorted({d for (_a, _o, pd) in por_arquivo.values() for d in pd})
    for dem in dems:
        c = collections.Counter()
        for (_a, _o, pd) in por_arquivo.values():
            c.update(pd.get(dem, {}))
        li.append(f"| {dem} | {c['documentos']} | {c['documentos_com_mes_oculto']} | "
                  f"{c['documento_meses']} | {c['documento_meses_ocultos']} | "
                  f"{_pct(c['documento_meses_ocultos'], c['documento_meses'])} | "
                  f"{c['presente_nao_e_a_maior_do_indice']} | "
                  f"{c['versao_presente_fora_do_indice']} | "
                  f"{c['mais_de_uma_versao_no_membro']} | {c['versao_presente_com_duas_datas']} | "
                  f"{c['membro_ausente']} |")
    li += ["", "## insumos (sha256 conferido contra docs/acervo/cvm/)", ""]
    li += [f"- {rec}_cia_aberta_{ano}.zip {sha}" for (rec, ano), sha in sorted(shas.items())]
    return "\n".join(li) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=(__doc__ or "").split("\n")[0])
    ap.add_argument("--conferir-insumos", action="store_true")
    ap.add_argument("--pasta", help="ZIPs locais <recurso>_cia_aberta_<ano>__<sha12>.zip")
    a = ap.parse_args(argv)
    faltas = conferir_insumos()
    for f in faltas:
        print("FALTA", f)
    if a.conferir_insumos or faltas:
        return 1 if faltas else 0
    cam = caminhos(a.pasta)
    por_arquivo = {k: medir_arquivo(c, k[0], k[1]) for k, (c, _s) in cam.items()}
    sys.stdout.write(relatorio(por_arquivo, {k: s for k, (_c, s) in cam.items()}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
