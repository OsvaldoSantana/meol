#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A porta de leitura do acervo: uma versao de um arquivo, venha de onde vier.

POR QUE ELE EXISTE (P-57). Com a captura na nuvem, a versao mais nova da CVM pode existir
so no armazem -- a maquina dele estava desligada quando ela chegou. Quem precisa do arquivo
nao deveria saber onde ele mora: pede `abrir("dfp", "dfp_cia_aberta_2024.zip")` e recebe
um caminho local, conferido.

DE ONDE SAI A LISTA DE VERSOES. Do que esta VERSIONADO, nunca do armazem: o registro da
captura (`docs/acervo/cvm/capturas.csv`) e o inventario da carga inicial
(`docs/acervo/<fonte>/inventario-armazem.csv`). A chave no armazem se deriva de
(fonte, recurso, arquivo, sha256), entao o git diz O QUE existe e o armazem so guarda o
byte. Um armazem que sumisse deixaria a lista inteira de pe, e cada `abrir` diria qual
byte falta.

A ORDEM DE BUSCA de `abrir`, e cada passo confere o sha256:
  1. o cache (`data/armazem/<chave>`), que so recebe byte conferido;
  2. o acervo local (`data/bronze/<fonte>/<recurso>/<arquivo>`), se o sha256 dele e o pedido;
  3. o armazem, baixando para o cache.

FRESCOR. `frescor(recurso)` devolve ha quantos dias a captura observou o recurso pela
ultima vez, e AVISA (`CapturaParada`) acima de `FRESCOR_MAXIMO_DIAS`. E a defesa contra a
falha mais silenciosa desta rotina: o GitHub desliga cron de repositorio sem atividade ha
60 dias, sem erro nenhum -- a serie so para de crescer. `abrir` chama o frescor para todo
recurso que tem rotina, de modo que quem usa o dado ouve o aviso.

O QUE ELE NAO FAZ (P5):
  - o frescor sem armazem mede so o registro versionado. Como o `inalterado` pelo portao
    HEAD vai para o log do armazem e nao para o git, um recurso que a CVM nao muda ha mais
    de 8 dias aparece velho sem estar. Os recursos de hoje mudam toda semana (a janela de
    reapresentacao da CVM), e o cad muda quase todo dia -- mas isso e propriedade da fonte,
    nao garantia. Com armazem, o log fecha o buraco;
  - nao confere o byte do cache a cada leitura: o cache so recebe byte conferido, e
    reconferir 1 GB a cada `abrir` seria o custo errado. `conferir=True` forca.
"""
from __future__ import annotations

import csv
import datetime as dt
import os
import sys
import tempfile
import warnings

AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)
import armazem as armazem_mod  # noqa: E402
import manifesto_cvm  # noqa: E402

# A captura roda todo dia (cron do workflow). Oito dias sem observacao sao sete rodadas
# perdidas seguidas -- uma semana inteira de reapresentacoes da CVM (a cadencia dela e
# semanal) mais um dia de folga para um feriado do runner.
FRESCOR_MAXIMO_DIAS = 8
# Os recursos com rotina automatica e o registro que ela escreve. Recurso fora daqui nao
# tem frescor a medir. O da B3 entra em 24/09/2026 com a captura do COTAHIST (P-135).
REGISTROS = {"cvm": os.path.join("docs", "acervo", "cvm", "capturas.csv"),
             "b3": os.path.join("docs", "acervo", "b3", "capturas.csv"),
             # 25/09/2026: o CSV do NEFIN saiu do git e entrou no armazem (fase0/capturar_nefin.py)
             "nefin": os.path.join("docs", "acervo", "nefin", "capturas.csv")}
INVENTARIO = "inventario-armazem.csv"
COLUNAS_INVENTARIO = ("fonte", "recurso", "arquivo", "sha256", "bytes", "chave", "papel",
                      "versao", "origem", "dt_envio")
CACHE_RELATIVO = os.path.join("data", "armazem")
# linhas do registro que descrevem a versao que ficou no lugar (as outras sao eventos)
VIGENTES = ("novo", "atualizado", "inalterado")


class VersaoDesconhecida(KeyError):
    """O arquivo, ou a versao pedida, nao aparece em registro nem inventario nenhum."""


class CapturaParada(UserWarning):
    """A ultima observacao de um recurso com rotina passou do limite."""


def raiz_repo():
    base = manifesto_cvm.raiz_do_repositorio(AQUI)
    if base is None:
        raise SystemExit("sem pyproject.toml acima de fase0/")
    return base


def _ler(caminho):
    if not os.path.exists(caminho):
        return []
    with open(caminho, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter=";"))


def _inventarios(repo):
    base = os.path.join(repo, "docs", "acervo")
    out = []
    if os.path.isdir(base):
        for fonte in sorted(os.listdir(base)):
            out.extend(_ler(os.path.join(base, fonte, INVENTARIO)))
    return out


def versoes(recurso, arquivo, repo=None):
    """Toda versao conhecida de (recurso, arquivo), da mais antiga para a mais nova, com
    `vigente` marcando a que a fonte serve hoje. Um sha256 aparece uma vez so."""
    repo = repo or raiz_repo()
    vistas = {}                                   # sha256 -> versao
    vigente = None
    for fonte, rel in sorted(REGISTROS.items()):
        for ln in _ler(os.path.join(repo, rel)):
            if ln.get("recurso") != recurso or ln.get("arquivo") != arquivo:
                continue
            if ln.get("sha256"):
                vistas.setdefault(ln["sha256"], dict(
                    fonte=fonte, sha256=ln["sha256"], bytes=ln.get("bytes", ""),
                    visto_em=ln.get("dt_captura", ""), origem="registro"))
            if ln.get("situacao") in VIGENTES and ln.get("sha256"):
                vigente = ln["sha256"]
    canonico_inventariado = None
    for ln in _inventarios(repo):
        if ln.get("recurso") != recurso or ln.get("arquivo") != arquivo:
            continue
        vistas.setdefault(ln["sha256"], dict(
            fonte=ln["fonte"], sha256=ln["sha256"], bytes=ln.get("bytes", ""),
            visto_em=ln.get("versao", ""), origem="inventario"))
        if ln.get("papel") == "canonico":
            canonico_inventariado = ln["sha256"]
    # o registro e observacao da fonte; o inventario e o que havia no disco dele. Quando
    # os dois existem, a observacao ganha.
    vigente = vigente or canonico_inventariado
    out = list(vistas.values())
    for v in out:
        v["vigente"] = v["sha256"] == vigente
    return out


def _escolher(vs, recurso, arquivo, versao):
    if not vs:
        raise VersaoDesconhecida(f"{recurso}/{arquivo}: nenhum registro nem inventario")
    if versao is None:
        ok = [v for v in vs if v["vigente"]]
        if not ok:
            raise VersaoDesconhecida(f"{recurso}/{arquivo}: nenhuma versao vigente")
        return ok[0]
    if len(versao) < 8:
        raise ValueError("versao e um prefixo de sha256 com 8 caracteres ou mais")
    ok = [v for v in vs if v["sha256"].startswith(versao.lower())]
    if len(ok) != 1:
        raise VersaoDesconhecida(f"{recurso}/{arquivo}@{versao}: "
                                 f"{'ambigua' if ok else 'nao existe'}")
    return ok[0]


def abrir(recurso, arquivo, versao=None, *, armazem=None, cache=None, repo=None,
          conferir=False):
    """Caminho local de uma versao conferida. `versao` e prefixo de sha256; sem ela, a
    vigente. So toca a rede no passo 3, e so se o byte nao estiver em disco."""
    repo = repo or raiz_repo()
    v = _escolher(versoes(recurso, arquivo, repo), recurso, arquivo, versao)
    if recurso in _recursos_com_rotina(repo):
        frescor(recurso, armazem=armazem, repo=repo)
    k = armazem_mod.chave(v["fonte"], recurso, arquivo, v["sha256"])
    cache = cache or os.path.join(repo, CACHE_RELATIVO)
    no_cache = os.path.join(cache, *k.split("/"))
    if os.path.exists(no_cache):
        if conferir and armazem_mod.sha256(no_cache) != v["sha256"]:
            raise armazem_mod.ConteudoDivergente(f"{no_cache} nao tem o sha256 da chave")
        return no_cache
    local = os.path.join(repo, "data", "bronze", v["fonte"], recurso, arquivo)
    if os.path.exists(local) and armazem_mod.sha256(local) == v["sha256"]:
        return local
    armazem = armazem or armazem_mod.do_ambiente()
    return armazem.baixar(k, no_cache)


def regimes_sem_registro(repo=None, registros=None):
    """Os acervos de `politica.yaml -> regimes_de_captura` cujo `registro` nao esta em
    `REGISTROS`, em ordem.

    P-150 (26/09/2026), a lacuna do #32: `frescor()` e `versoes()` so leem os registros
    daqui. Um acervo automatico fora desta lista e captura sem vigia -- se o cron parar,
    `CapturaParada` nao dispara, e o que o cron registrar nao se abre pelo registro (P7).
    O `b3_eventos` entra aqui no mesmo commit em que entrar em `regimes_de_captura`."""
    repo = repo or raiz_repo()
    registros = REGISTROS if registros is None else registros
    conhecidos = {os.path.normpath(r) for r in registros.values()}
    out = []
    for nome, r in (manifesto_cvm._politica(repo).get("regimes_de_captura") or {}).items():
        reg = (r or {}).get("registro") if isinstance(r, dict) else None
        if not reg or os.path.normpath(reg) not in conhecidos:
            out.append(nome)
    return sorted(out)


def _recursos_com_rotina(repo):
    out = set()
    for rel in REGISTROS.values():
        out.update(ln.get("recurso", "") for ln in _ler(os.path.join(repo, rel)))
    return out - {""}


def _instante(texto):
    try:
        return dt.datetime.strptime(texto, "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=dt.timezone.utc)
    except (TypeError, ValueError):
        return None


def frescor(recurso, *, armazem=None, repo=None, agora=None,
            limite_dias=FRESCOR_MAXIMO_DIAS, avisar=True):
    """{recurso, ultima, dias, status, consultado}. `status` e OK, CAPTURA_PARADA ou
    NUNCA_OBSERVADO; os dois ultimos avisam com `CapturaParada`. `consultado` diz se o
    log do armazem entrou na conta -- sem ele, a medida e so do registro (P5)."""
    repo = repo or raiz_repo()
    agora = agora or dt.datetime.now(dt.timezone.utc)
    instantes = []
    for rel in REGISTROS.values():
        instantes += [_instante(ln.get("dt_captura")) for ln in _ler(os.path.join(repo, rel))
                      if ln.get("recurso") == recurso]
    consultado = ["registro"]
    if armazem is not None:
        logs = armazem.listar("logs/capturas/")
        if logs:
            with tempfile.TemporaryDirectory(prefix="frescor_") as tmp:
                p = armazem.baixar(logs[-1], os.path.join(tmp, "log.csv"))
                instantes += [_instante(ln.get("dt_captura")) for ln in _ler(p)
                              if ln.get("recurso") == recurso]
        consultado.append("log do armazem")
    instantes = [i for i in instantes if i is not None]
    if not instantes:
        out = dict(recurso=recurso, ultima=None, dias=None, status="NUNCA_OBSERVADO",
                   consultado=consultado)
    else:
        ultima = max(instantes)
        dias = (agora - ultima).total_seconds() / 86400
        out = dict(recurso=recurso, ultima=ultima.strftime("%Y-%m-%dT%H:%M:%SZ"),
                   dias=round(dias, 1),
                   status="OK" if dias <= limite_dias else "CAPTURA_PARADA",
                   consultado=consultado)
    if avisar and out["status"] != "OK":
        warnings.warn(CapturaParada(
            f"{out['status']}: {recurso} -- ultima observacao {out['ultima']} "
            f"({out['dias']} dias; limite {limite_dias}; medido em "
            f"{' + '.join(consultado)}). O GitHub desliga cron apos 60 dias sem atividade "
            f"no repositorio: veja a aba Actions do workflow captura_cvm."), stacklevel=2)
    return out


def main(argv=None):
    import argparse
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--frescor", nargs="*", metavar="RECURSO",
                   help="frescor dos recursos (padrao: todos com rotina)")
    p.add_argument("--armazem", choices=["s3"], help="consulta tambem o log do armazem")
    a = p.parse_args(argv)
    repo = raiz_repo()
    arm = armazem_mod.do_ambiente(a.armazem) if a.armazem else None
    parado = False
    for r in (a.frescor or sorted(_recursos_com_rotina(repo))):
        f = frescor(r, armazem=arm, repo=repo, avisar=False)
        parado |= f["status"] != "OK"
        print(f"{r:6s} {f['status']:16s} ultima {f['ultima']}  ({f['dias']} dias; "
              f"{' + '.join(f['consultado'])})")
    return 1 if parado else 0


if __name__ == "__main__":
    raise SystemExit(main())
