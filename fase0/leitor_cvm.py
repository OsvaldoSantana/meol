#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Leitor as-of de DFP/ITR: o valor de uma conta sabendo so o que se tinha capturado ate D.

A PERGUNTA, uma so (P-51, P-53; desenho em docs/decisoes/2026-10-10-leitor-asof-cvm.md):
"qual era o valor da CONTA para o CD_CVM no DT_REFER, sabendo so o que tinha sido capturado
ate a data D". Tres regras a respondem:

  1. QUAL ARQUIVO: o do ano do DT_REFER, e so ele (P-51: a particao e o ano do ARQUIVO,
     nunca o do dado). O DFP de 2025 que corrige 2023 nao e lido para 2023, nem depois de
     capturado: a correcao de 2023 entra quando o proprio dfp_cia_aberta_2023 for regerado
     com a VERSAO nova.
  2. QUAL VERSAO DO ARQUIVO: a ultima vigencia do registro de captura com instante <= D
     (`acervo.vigencias`). Uma reapresentacao so vale a partir da dt_captura em que
     apareceu. Antes da primeira captura nao ha resposta (`SemCaptura`), nunca a versao de
     hoje no lugar.
  3. QUAIS LINHAS: so ORDEM_EXERC = ULTIMO (P-51); PENULTIMO e o ano anterior ja
     reapresentado.

O QUE ELE RECUSA EM VEZ DE ADIVINHAR (P1), cada um medido no ITR 2024 real em 10/10/2026:
  - `PeriodoAmbiguo`: mais de um periodo ULTIMO para a conta (trimestre e acumulado na DRE
    do ITR; uma linha por coluna na DMPL). Quem pergunta escolhe `dt_ini_exerc`/`coluna_df`;
  - `ValorAmbiguo`: a mesma chave com valores diferentes (13 chaves no BPP consolidado). A
    duplicata EXATA, que e comum, conta como uma linha;
  - `EnumeracaoDesconhecida`: ORDEM_EXERC, ESCALA_MOEDA ou MOEDA fora da lista OBSERVADO do
    docs/schemas/cvm-dfp-itr-v1.yaml, em qualquer linha do membro lido;
  - `LimitacaoNaoDeclarada`: a resposta carrega o nome da limitacao
    `dt_captura_nao_e_data_de_conhecimento_do_mercado`; sem ela no politica.yaml, nao ha
    resposta.

O QUE ELE NAO FAZ (P5):
  - nao responde o que o MERCADO sabia em D, e sim o que ESTE SISTEMA tinha capturado. A
    captura chega depois (ENET -> regeracao semanal da CVM -> cron diario). Antes de
    24/09/2026, a primeira linha do registro, nao responde nada. Limitacao NAO_CONSERTADA,
    pendencia P-183;
  - nao liga papel a empresa: a ponte ticker -> CD_CVM, que tambem precisa ser bitemporal,
    e a P-53b, depois da P-145;
  - nao usa DuckDB nem Parquet. O acervo e o ZIP da CVM, chaveado por sha256 no armazem, e
    ja nao depende de engine; o indice em memoria daqui e reconstruivel a cada leitura. O
    custo em escala (400 empresas x 17 anos) NAO foi medido: o memo guarda as linhas ULTIMO
    de ate 8 membros por processo, e o maior membro do ITR 2024 (BPP_ind) tem 487.974 linhas.
"""
from __future__ import annotations

import csv
import datetime as dt
import decimal
import functools
import io
import os
import sys
import zipfile

AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)
import acervo  # noqa: E402
import manifesto_cvm  # noqa: E402

SCHEMA = os.path.join("docs", "schemas", "cvm-dfp-itr-v1.yaml")
LIMITACAO = "dt_captura_nao_e_data_de_conhecimento_do_mercado"
UTC = dt.timezone.utc


class SemCaptura(LookupError):
    """Nada deste arquivo tinha sido capturado ate D."""


class ContaAusente(LookupError):
    """A versao vigente em D nao tem a conta pedida em ULTIMO. Ausencia nao e zero."""


class MembroAusente(LookupError):
    """A versao vigente em D nao tem o demonstrativo pedido."""


class PeriodoAmbiguo(LookupError):
    """Mais de um periodo ULTIMO para a mesma conta; quem pergunta escolhe qual."""


class ValorAmbiguo(ValueError):
    """A mesma chave, no mesmo periodo, com valores diferentes no dado da CVM."""


class EnumeracaoDesconhecida(ValueError):
    """Valor fora da lista OBSERVADO (P1): falha em vez de virar um dos conhecidos."""


class LeiauteDesconhecido(ValueError):
    """O cabecalho do membro nao tem as colunas que o leitor le."""


class LimitacaoNaoDeclarada(KeyError):
    """A limitacao que toda resposta carrega nao esta vigente no politica.yaml."""


@functools.lru_cache(maxsize=1)
def leiaute():
    import yaml
    with io.open(os.path.join(acervo.raiz_repo(), SCHEMA), encoding="utf-8") as f:
        return yaml.safe_load(f)


@functools.lru_cache(maxsize=1)
def _politica_limitacoes():
    return manifesto_cvm._politica(acervo.raiz_repo()).get("limitacoes_declaradas") or {}


def _limitacoes():
    return _politica_limitacoes()


def limitacao_declarada():
    """A entrada vigente de `limitacoes_declaradas` que diz o que este leitor nao sabe.
    Lida do politica.yaml do REPOSITORIO, nunca do `repo` do acervo: a limitacao e do
    leitor, nao do dado."""
    lim = _limitacoes().get(LIMITACAO)
    if not isinstance(lim, dict) or any(h in lim for h in manifesto_cvm.HISTORICO):
        raise LimitacaoNaoDeclarada(
            f"politica.yaml -> limitacoes_declaradas.{LIMITACAO} ausente ou fora de vigor. "
            f"O leitor responde o que se CAPTUROU ate D, nao o que o mercado sabia; sem a "
            f"declaracao, o numero sairia sem o aviso (P5).")
    return lim


def _limite(ate):
    """`ate` como data inclui o dia inteiro em UTC; como instante, exige fuso -- a
    dt_captura e UTC, e um instante ingenuo seria lido no relogio da maquina (CV-03)."""
    if isinstance(ate, dt.datetime):
        if ate.tzinfo is None:
            raise ValueError(f"`ate` {ate!r} sem fuso: a dt_captura e UTC; passe tzinfo")
        return ate.astimezone(UTC)
    if isinstance(ate, dt.date):
        return dt.datetime.combine(ate, dt.time.max, tzinfo=UTC)
    raise TypeError(f"`ate` e data ou instante, nao {type(ate).__name__}")


def versao_em(recurso, arquivo, ate, repo=None):
    """{sha256, desde}: a versao do arquivo que estava capturada em D."""
    limite = _limite(ate)
    antes = [(q, s) for q, s in acervo.vigencias(recurso, arquivo, repo) if q <= limite]
    if not antes:
        raise SemCaptura(f"{recurso}/{arquivo}: nenhuma captura ate {limite:%Y-%m-%dT%H:%M:%SZ}"
                         f". Nao ha observacao anterior a primeira captura; a versao de "
                         f"hoje no lugar dela seria look-ahead (P-183).")
    return {"sha256": antes[-1][1], "desde": antes[-1][0]}


def _cd(cd_cvm):
    """'001023', '1023' e 1023 sao o mesmo emissor: o CSV da CVM traz o zero a esquerda."""
    return int(str(cd_cvm).strip())


def _validar(recurso, demonstrativo):
    lei = leiaute()
    if recurso not in lei["arquivo"]["recursos"]:
        raise ValueError(f"recurso {recurso!r} fora de {lei['arquivo']['recursos']}")
    validos = [f"{d}_{v}" for d in lei["demonstrativos"] for v in lei["variantes"]]
    if demonstrativo not in validos:
        raise ValueError(f"demonstrativo {demonstrativo!r} fora do leiaute: {validos}")


@functools.lru_cache(maxsize=8)
def _ultimo_por_emissor(caminho, sha256, membro):
    """{cd_cvm: [linha ULTIMO]} de um membro. `sha256` entra na chave do memo porque o
    caminho sozinho nao identifica o conteudo. Cada linha e uma tupla de texto: o valor so
    vira Decimal quando pedido (0 ilegiveis em 3.786.457 linhas do ITR 2024, n = 1
    arquivo; um ilegivel derruba a pergunta sobre ele, nao as dos outros emissores)."""
    lei = leiaute()
    enum = lei["enumeracoes"]
    with zipfile.ZipFile(caminho) as z:
        if membro not in z.namelist():
            raise MembroAusente(f"{membro} nao esta na versao {sha256[:12]} "
                                f"({os.path.basename(caminho)})")
        with z.open(membro) as f:
            r = csv.DictReader(io.TextIOWrapper(f, encoding=lei["arquivo"]["codificacao"],
                                                newline=""),
                               delimiter=lei["arquivo"]["separador"])
            campos = r.fieldnames or []
            falta = [c for c in lei["colunas_obrigatorias"] if c not in campos]
            if falta:
                raise LeiauteDesconhecido(f"{membro}: sem as colunas {falta}")
            periodo = [c for c in lei["colunas_de_periodo"] if c in campos]
            out: dict[int, list[tuple]] = {}
            for n, ln in enumerate(r, start=2):
                for campo in ("ORDEM_EXERC", "ESCALA_MOEDA", "MOEDA"):
                    if ln[campo] not in enum[campo]["valores"]:
                        raise EnumeracaoDesconhecida(
                            f"{membro}, linha {n}: {campo} = {ln[campo]!r} fora da lista "
                            f"OBSERVADO {list(enum[campo]['valores'])} ({SCHEMA}). Conte o "
                            f"valor novo no dado e declare-o antes de ler (P1).")
                if ln["ORDEM_EXERC"] != enum["ORDEM_EXERC"]["usado"]:
                    continue                         # P-51: PENULTIMO e look-ahead
                out.setdefault(_cd(ln["CD_CVM"]), []).append((
                    ln["DT_REFER"], ln["CD_CONTA"], ln.get("DS_CONTA", ""), ln["VERSAO"],
                    ln.get("DT_INI_EXERC", "") if "DT_INI_EXERC" in periodo else "",
                    ln["DT_FIM_EXERC"],
                    ln.get("COLUNA_DF", "") if "COLUNA_DF" in periodo else "",
                    ln["VL_CONTA"], ln["ESCALA_MOEDA"], n))
    return out


def _resposta(t, ctx):
    (dt_refer, conta, ds, versao, ini, fim, coluna, vl, escala, n) = t
    try:
        vl_conta = decimal.Decimal(vl)
    except decimal.InvalidOperation:
        raise ValueError(f"{ctx['membro']}, linha {n}: VL_CONTA ilegivel {vl!r}") from None
    mult = leiaute()["enumeracoes"]["ESCALA_MOEDA"]["valores"][escala]
    return dict(ctx, dt_refer=dt_refer, cd_conta=conta, ds_conta=ds, versao=versao,
                dt_ini_exerc=ini, dt_fim_exerc=fim, coluna_df=coluna, vl_conta=vl_conta,
                escala_moeda=escala, valor_em_reais=vl_conta * mult, linha=n)


def linhas(recurso, ano, cd_cvm, demonstrativo, ate, *, repo=None, armazem=None, cache=None):
    """Toda linha ULTIMO do emissor no demonstrativo, na versao do arquivo de `ano` que
    estava capturada em D. E a serie de um emissor dentro de uma particao."""
    _validar(recurso, demonstrativo)
    lim = limitacao_declarada()
    lei = leiaute()["arquivo"]
    arquivo = lei["nome"].format(recurso=recurso, ano=ano)
    membro = lei["membro"].format(recurso=recurso, demonstrativo=demonstrativo, ano=ano)
    v = versao_em(recurso, arquivo, ate, repo)
    caminho = acervo.abrir(recurso, arquivo, v["sha256"], armazem=armazem, cache=cache,
                           repo=repo)
    ctx = dict(recurso=recurso, arquivo=arquivo, membro=membro, sha256=v["sha256"],
               desde=v["desde"], cd_cvm=_cd(cd_cvm), limitacao=LIMITACAO,
               tipo_da_limitacao=lim.get("tipo"))
    return [_resposta(t, ctx)
            for t in _ultimo_por_emissor(caminho, v["sha256"], membro).get(_cd(cd_cvm), ())]


def valor(recurso, cd_cvm, dt_refer, cd_conta, demonstrativo, ate, *, dt_ini_exerc=None,
          coluna_df=None, repo=None, armazem=None, cache=None):
    """O valor da conta para o CD_CVM no DT_REFER, sabendo so o capturado ate D. O arquivo
    e o do ano do DT_REFER (P-51). Devolve a linha inteira: `vl_conta` como a CVM escreve,
    `valor_em_reais` com a escala aplicada, e de onde veio (`arquivo`, `sha256`, `desde`)."""
    cands = [r for r in linhas(recurso, dt_refer.year, cd_cvm, demonstrativo, ate, repo=repo,
                               armazem=armazem, cache=cache)
             if r["dt_refer"] == dt_refer.isoformat() and r["cd_conta"] == cd_conta]
    if dt_ini_exerc is not None:
        cands = [r for r in cands if r["dt_ini_exerc"] == dt_ini_exerc.isoformat()]
    if coluna_df is not None:
        cands = [r for r in cands if r["coluna_df"] == coluna_df]
    onde = f"{recurso} {demonstrativo} CD_CVM {_cd(cd_cvm)} DT_REFER {dt_refer} conta {cd_conta}"
    if not cands:
        raise ContaAusente(f"{onde}: nenhuma linha ULTIMO na versao vigente em {ate}")
    periodos = sorted({(r["dt_ini_exerc"], r["dt_fim_exerc"], r["coluna_df"]) for r in cands})
    if len(periodos) > 1:
        raise PeriodoAmbiguo(f"{onde}: {len(periodos)} periodos ULTIMO (dt_ini_exerc, "
                             f"dt_fim_exerc, coluna_df) = {periodos}. Escolha com "
                             f"`dt_ini_exerc` ou `coluna_df`.")
    distintos = sorted({(r["vl_conta"], r["escala_moeda"], r["versao"]) for r in cands})
    if len(distintos) > 1:
        raise ValorAmbiguo(f"{onde}: a mesma chave com valores diferentes "
                           f"{[(str(v), e, ver) for v, e, ver in distintos]} nas linhas "
                           f"{[r['linha'] for r in cands]} de {cands[0]['membro']}. O dado "
                           f"da CVM nao diz qual vale; escolher seria inventar (P1).")
    return cands[0]
