#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Eventos societarios da B3 no armazem -- o mesmo armazem, teto e registro da CVM (P-150).

POR QUE ELE EXISTE (26/09/2026). O `coletar_b3.py` captura o dado que o V-01 chamou de mais
perecivel do projeto -- endpoint nao documentado, sem SLA, sem espelho --, mas grava so em
disco local. A captura de 11/09 mora no disco dele; num executor do Actions, que e apagado
no fim do job, o `coletar_b3.py` sozinho baixaria e perderia tudo. Este modulo roda o mesmo
coletor numa pasta temporaria e sobe cada arquivo ao armazem, pela chave de conteudo.

O QUE ELE NAO FAZ, DE PROPOSITO:
  - nao reimplementa a coleta: chama `coletar_b3` (N-01, uma leitura do endpoint so);
  - nao publica: os eventos vao para o armazem privado e NUNCA para a release da CVM
    (P-136; `publicar_cvm.publicavel()` recusa qualquer fonte que nao seja `cvm`);
  - nao contorna bloqueio: se a B3 responder erro ou CAPTCHA, o passo fica vermelho e o
    motivo vai para o registro.

O PORTAO. O endpoint nao tem Last-Modified nem ETag (JSON montado a cada pedido), entao nao
ha HEAD que decida. O portao e o do armazem: a chave e o sha256 do conteudo, e
`enviar_se_ausente` nao sobe o que ja existe. Dia sem mudanca custa os pedidos e zero byte
de armazem. A CADENCIA vem de `politica.yaml -> cadencias_de_captura.b3_eventos`.

  python fase0/capturar_eventos_b3.py --armazem s3          # o que o workflow roda
"""
from __future__ import annotations

import argparse
import datetime as dt
import io
import os
import sys
import tempfile

import yaml

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import armazem as armazem_mod  # noqa: E402
import capturar_cvm as C  # noqa: E402
import coletar_b3 as B  # noqa: E402

FONTE = "b3"
ACERVO = "b3_eventos"
LOGS = "logs/capturas_b3_eventos"   # separado: o frescor le o ultimo log de cada fonte
REGISTRO_RELATIVO = os.path.join("docs", "acervo", ACERVO, "capturas.csv")
INDICE = "IBOV"
RESSALVA = "ressalva"
# pasta do coletor -> recurso no armazem
RECURSOS = {"indices": "indice_carteira", "eventos": "eventos_suplemento",
            "proventos": "proventos"}
DIAS = ("segunda", "terca", "quarta", "quinta", "sexta", "sabado", "domingo")


class CadenciaAusente(RuntimeError):
    pass


def cadencia(raiz_repo):
    """(dia da semana, 0 = segunda; motivo) de `politica.yaml`. Sem a entrada, recusa:
    cadencia inventada no codigo seria regra fora do dado (P2)."""
    with io.open(os.path.join(raiz_repo, "alocacao", "politica.yaml"), encoding="utf-8") as f:
        P = yaml.safe_load(f) or {}
    c = (P.get("cadencias_de_captura") or {}).get(ACERVO) or {}
    dia = c.get("dia_da_semana")
    if dia not in DIAS or not c.get("motivo"):
        raise CadenciaAusente(
            f"politica.yaml -> cadencias_de_captura.{ACERVO} precisa de `dia_da_semana` "
            f"(um de {DIAS}) e `motivo`")
    return DIAS.index(dia), c["motivo"]


def nome_no_armazem(partes):
    """O nome do arquivo no armazem a partir do caminho relativo a pasta do recurso,
    `[dt_captura=DIA, ...]`. A chave nao aceita barra no nome: `PETR/pagina-001.json`
    vira `PETR__pagina-001.json`, e o dia sai -- a versao e o sha256. E a UNICA regra de
    nome: a carga inicial (`subir_acervo_local.py`) usa esta mesma funcao (N-01)."""
    return "__".join(partes[1:])


def arquivos_do_coletor(raiz):
    """[(recurso, nome no armazem, caminho)] do que o `coletar_b3` gravou. O
    `manifesto.jsonl` nao entra aqui: ele e log."""
    out = []
    for pasta, recurso in RECURSOS.items():
        base = os.path.join(raiz, pasta)
        for dirpath, _dirs, nomes in os.walk(base):
            for n in sorted(nomes):
                if not n.endswith(".json"):
                    continue
                cam = os.path.join(dirpath, n)
                partes = os.path.relpath(cam, base).replace("\\", "/").split("/")
                out.append((recurso, nome_no_armazem(partes), cam))
    return sorted(out)


def enviar(arquivos, armazem, registro, diario, estado):
    """Sobe cada arquivo pela chave de conteudo. Devolve (novos, inalterados, recusado)."""
    novos = inalterados = 0
    for recurso, nome, cam in arquivos:
        digest, n = armazem_mod.sha256(cam), os.path.getsize(cam)
        k = armazem_mod.chave(FONTE, recurso, nome, digest)
        base = dict(dt_captura=C.agora(), recurso=recurso, arquivo=nome, sha256=digest,
                    bytes=n, caminho=k)
        try:
            enviado = armazem.enviar_se_ausente(k, cam)
        except armazem_mod.TetoExcedido as e:
            linha = dict(base, situacao=C.RECUSADO_POR_TETO, motivo=str(e))
            C.anotar(registro, linha)
            diario.append(linha)
            print(f"[!] {k}  RECUSADO POR TETO: {e}")
            return novos, inalterados, True
        chave_logica = f"{recurso}/{nome}"
        if enviado or estado.get(chave_logica) != digest:
            situacao = C.NOVO if chave_logica not in estado else C.ATUALIZADO
            linha = dict(base, situacao=situacao,
                         motivo="" if enviado else "versao ja estava no armazem")
            C.anotar(registro, linha)
            estado[chave_logica] = digest
            novos += 1
        else:
            linha = dict(base, situacao=C.INALTERADO, motivo="sha256 ja no armazem")
            inalterados += 1
        diario.append(linha)
    return novos, inalterados, False


def estado_do_registro(registro):
    """{recurso/arquivo: sha256} da ultima versao registrada de cada arquivo."""
    out = {}
    for ln in C.ler_registro(registro):
        if ln.get("sha256") and ln.get("situacao") in (C.NOVO, C.ATUALIZADO):
            out[f"{ln['recurso']}/{ln['arquivo']}"] = ln["sha256"]
    return out


def main(argv=None, armazem=None, hoje=None, coletor=B, pausa=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--armazem", choices=["s3", "local"], required=True,
                   help="s3: o R2 do projeto, credenciais so por R2_*; "
                        "local: uma pasta (ARMAZEM_LOCAL)")
    p.add_argument("--registro", default=None, help=f"padrao: {REGISTRO_RELATIVO}")
    p.add_argument("--qualquer-dia", action="store_true",
                   help="roda fora do dia da cadencia (execucao manual)")
    p.add_argument("--raiz-repo", default=None, help=argparse.SUPPRESS)  # testes
    a = p.parse_args(argv)
    base = a.raiz_repo or C.raiz_repo()
    registro = a.registro or os.path.join(base, REGISTRO_RELATIVO)
    hoje = hoje or dt.date.today()

    dia_da_semana, motivo = cadencia(base)
    if hoje.weekday() != dia_da_semana and not a.qualquer_dia:
        print(f"fora da cadencia: hoje e {DIAS[hoje.weekday()]}, a captura dos eventos roda "
              f"na {DIAS[dia_da_semana]} ({motivo.strip()}). Nada foi pedido a B3.")
        return 0

    armazem = armazem or armazem_mod.do_ambiente(a.armazem, raiz_repo=base)
    C.relatar_ocupacao(armazem, raiz=base)
    diario: list[dict] = []
    dia = hoje.isoformat()
    ressalvas, falha = [], None
    with tempfile.TemporaryDirectory(prefix="eventos_b3_") as raiz:
        try:
            codigos = coletor.coletar_indice(raiz, INDICE, dia, False)
            if coletor.coletar_eventos(raiz, codigos, dia, False):
                ressalvas.append("eventos: emissora vazia, fora do formato ou sem evento "
                                 "(ver o log do coletor)")
            kw = {} if pausa is None else {"pausa": pausa}
            rc = coletor.coletar_proventos(raiz, dia, **kw)
            if rc == 2:
                falha = "proventos: nenhum tradingName no acervo de eventos da rodada"
            elif rc:
                ressalvas.append("proventos: emissora com paginacao invalida ou sem nome")
        except Exception as e:  # noqa: BLE001 -- o nome do erro vai para o registro
            falha = f"{type(e).__name__}: {str(e)[:200]}"
        arquivos = arquivos_do_coletor(raiz)
        novos, inalterados, recusado = enviar(arquivos, armazem, registro, diario,
                                              estado_do_registro(registro))
        man = os.path.join(raiz, "manifesto.jsonl")
        if os.path.exists(man):
            armazem.enviar_se_ausente(f"{LOGS}/{dia}__manifesto__{C.agora()[11:19]}.jsonl"
                                      .replace(":", ""), man, isento_do_teto=True)
    if not arquivos and not falha:
        falha = "o coletor terminou sem gravar arquivo nenhum"
    fim = dict(dt_captura=C.agora(), recurso="rodada", arquivo=f"{INDICE}.rodada",
               situacao=C.ERRO if falha else (RESSALVA if ressalvas else C.INALTERADO),
               motivo=falha or "; ".join(ressalvas))
    if falha or ressalvas:
        C.anotar(registro, fim)
    diario.append(fim)
    print(f"{len(arquivos)} arquivos: {novos} novos, {inalterados} inalterados"
          + (f"; FALHA: {falha}" if falha else "")
          + (f"; ressalvas: {'; '.join(ressalvas)}" if ressalvas else ""))
    print(f"log: {C.enviar_diario(armazem, diario, prefixo=LOGS)}")
    return 1 if (falha or recusado) else 0


if __name__ == "__main__":
    raise SystemExit(main())
