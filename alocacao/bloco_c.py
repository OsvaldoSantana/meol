# -*- coding: utf-8 -*-
"""bloco_c.py -- o bloco C (solvencia) como codigo: o portao de exclusao, com cinco saidas.

P-30 parte 1 e P-64 (24/10/2026). Desenho: docs/decisoes/2026-10-24-saidas-do-portao-bloco-c.md.
Tudo o que decide mora em `politica.yaml -> bloco_C_solvencia` (P2): os cortes, as grades de
contagem, a ordem, as metricas, o sentido de cada corte, o modo nivel/tendencia (63a), as contas
do plano da CVM e a enumeracao do SETOR_ATIV. Este arquivo so interpreta. Nenhum literal de corte
aqui: `test_bloco_c.py` o confere por AST e planta um para provar que a guarda o ve.

AS CINCO SAIDAS (a unica que tira empresa do universo e REPROVA):
  APROVA          passou em todo corte ativo;
  REPROVA         traz o codigo, o valor medido, o corte escolhido e o N do universo. So existe
                  com limiar gravado;
  MARCA           sinal sem veto: corte sem limiar, tendencia em AGUARDA_SERIE, "C-04 nao
                  medido", empresa sem dado (P-16b);
  RECUSA_REGIME   banco ou seguradora vai para `regime_instituicao_financeira` (P-31), sem
                  numero (F-02: metrica que nao se aplica mas nao falha);
  EXIGE_DOSSIE    regime sem dado estruturado, ou que o cadastro nao identifica. Fica no
                  universo, sem peso deste bloco.

O documento so e visto pelo LEITOR (`fase0/leitor_cvm.py`), no modo da captura ou no dt_receb:
a decisao de um documento ser conhecido na data e dele. Este modulo nunca compara DT_REFER com a
data para decidir o que se sabia.

O QUE ELE NAO FAZ (P5):
  - NAO esta ligado ao `alocar()` nem ao `motor_aporte()`. Nenhum corte esta ativo: todo limiar
    e PENDENTE, e o bloco calcula e marca;
  - o C-02 e NAO_IMPLEMENTADA (o escopo diz "Padrao" e EBITDA nao e conta do plano), o C-04 e
    "nao medido" (P-65) e a tendencia e AGUARDA_SERIE (63a): nenhum dos tres produz numero;
  - o regime de banco (P-31) e os regimes de N saidas (P-58 a P-61) nao existem aqui;
  - o setor vem do cadastro de HOJE, nao as-of (`setor_ativ.alcance`).
"""
from __future__ import annotations

import csv
import datetime as dt
import functools
import os
import sys
from decimal import Decimal

import yaml

AQUI = os.path.dirname(os.path.abspath(__file__))
FASE0 = os.path.join(os.path.dirname(AQUI), "fase0")
if FASE0 not in sys.path:
    sys.path.insert(0, FASE0)
import leitor_cvm as L  # noqa: E402

POLITICA = os.path.join(AQUI, "politica.yaml")
PENDENTE = "PENDENTE"
FINANCEIRA, A_DECIDIR, GERAL = "FINANCEIRA", "A_DECIDIR", "GERAL"


class SetorForaDaEnumeracao(ValueError):
    """SETOR_ATIV fora da lista OBSERVADO (P1): falha em vez de virar um dos conhecidos."""


class CadastroAmbiguo(ValueError):
    """O mesmo CD_CVM com dois SETOR_ATIV diferentes: escolher seria inventar (P1)."""


class MetricaNaoImplementada(NotImplementedError):
    """O YAML diz que a metrica se aplica hoje e o modulo nao tem como calcula-la."""


def _ler_yaml(caminho):
    with open(caminho, encoding="utf-8") as f:
        return yaml.safe_load(f)["bloco_C_solvencia"]


def _conferir_enumeracao(P):
    """A lista de SETOR_ATIV tem de somar o que diz ter contado: lista que nao fecha com o
    proprio total foi editada a mao (P1)."""
    s = P["setor_ativ"]
    if len(s["valores"]) != s["distintos"] or sum(s["valores"].values()) != s["linhas"]:
        raise ValueError(f"setor_ativ: {len(s['valores'])} valores e {sum(s['valores'].values())}"
                         f" linhas, mas o YAML declara {s['distintos']} e {s['linhas']}")
    return P


@functools.lru_cache(maxsize=None)
def _vigente():
    return _conferir_enumeracao(_ler_yaml(POLITICA))


def carregar(caminho=None):
    """O `bloco_C_solvencia` do politica.yaml, ou o de um YAML de teste (lido sempre de novo,
    pelo mesmo caminho: um cache por nome serviria o arquivo velho a quem o reescreve)."""
    return _vigente() if caminho is None else _conferir_enumeracao(_ler_yaml(caminho))


def limiar(P, cod):
    """O limiar gravado da metrica, ou None se PENDENTE. Aceita o numero, `{valor: n}` e o
    ponteiro `{lido_de: caminho.no.yaml}` (o C-05 guarda o seu em `campos_C04_C05`)."""
    bruto = P["metricas"][cod]["limiar"]
    if isinstance(bruto, dict) and "lido_de" in bruto:
        bruto = functools.reduce(lambda no, k: no[k], bruto["lido_de"].split("."), P)
    if isinstance(bruto, dict):
        bruto = bruto.get("valor", PENDENTE)
    return None if bruto == PENDENTE else bruto


def sai_do_universo(saida, P):
    return saida in P["saidas_do_portao"]["tiram_do_universo"]


def universo(avaliacoes, P):
    """As empresas que continuam: so REPROVA tira (P6: ausencia de criterio nao e criterio)."""
    return [a for a in avaliacoes if not sai_do_universo(a["saida"], P)]


# ── o cadastro: SETOR_ATIV (P-18) ────────────────────────────────────────────

def regime_do_setor(setor, P):
    s = P["setor_ativ"]
    if setor not in s["valores"]:
        raise SetorForaDaEnumeracao(
            f"SETOR_ATIV {setor!r} fora da enumeracao OBSERVADA em {s['data']} "
            f"({s['distintos']} valores, sha256 {s['sha256']}). Conte o valor novo no dado "
            f"e declare-o em politica.yaml antes de ler (P1).")
    if setor in s["financeira"]:
        return FINANCEIRA
    return A_DECIDIR if setor in s["a_decidir"] else GERAL


def ler_cadastro(caminho, P):
    """{CD_CVM: SETOR_ATIV} do cad_cia_aberta.csv. Falha fora da enumeracao e com dois setores
    para o mesmo emissor; a duplicata EXATA (varias linhas do mesmo CD_CVM) e uma so."""
    out = {}
    with open(caminho, encoding="latin-1", newline="") as f:
        for ln in csv.DictReader(f, delimiter=";"):
            cd, setor = int(ln["CD_CVM"]), ln["SETOR_ATIV"]
            regime_do_setor(setor, P)
            if out.setdefault(cd, setor) != setor:
                raise CadastroAmbiguo(f"CD_CVM {cd}: {out[cd]!r} e {setor!r} no mesmo cadastro")
    return out


# ── as formulas (a ESCOLHA esta no YAML; aqui so a aritmetica do escopo) ─────

def _cobertura_de_juros(v):
    despesa = -v["resultado_financeiro"]            # despesa financeira LIQUIDA
    return None if despesa <= 0 else v["ebit"] / despesa


def _perfil_de_vencimento(v):
    total = v["divida_cp"] + v["divida_lp"]
    return None if total <= 0 else v["divida_cp"] / total


def _caixa_sobre_divida_cp(v):
    return None if v["divida_cp"] <= 0 else v["caixa"] / v["divida_cp"]


FORMULAS = {"cobertura_de_juros": _cobertura_de_juros,
            "perfil_de_vencimento": _perfil_de_vencimento,
            "caixa_sobre_divida_cp": _caixa_sobre_divida_cp}


# ── a leitura do documento CONHECIDO na data, pelo leitor ────────────────────

_RECUSADOS = (L.PeriodoAmbiguo, L.ValorAmbiguo, L.DataDeConhecimentoAusente,
              L.DataDeConhecimentoAmbigua, L.EnumeracaoDesconhecida, L.LeiauteDesconhecido)


def _ler_operando(op, cd, dt_refer, ate, conhecimento, kw):
    """(valor, linha, causa): a soma das contas do operando, so se TODAS existem e trazem a
    descricao do plano; ausencia nunca vira zero."""
    total, primeira = Decimal(0), None
    for conta in op["contas"]:
        try:
            r = L.valor(op["recurso"], cd, dt_refer, conta["cd_conta"], op["demonstrativo"],
                        ate, conhecimento=conhecimento, **kw)
        except _RECUSADOS as e:
            return None, None, ("DADO_RECUSADO", str(e))
        except LookupError as e:
            return None, None, ("SEM_DADO", str(e))
        primeira = primeira or r
        if r["ds_conta"] != conta["ds_esperada"]:
            return None, r, ("PLANO_DE_CONTAS_DIFERENTE",
                             f"conta {conta['cd_conta']} traz {r['ds_conta']!r}, o plano "
                             f"esperado diz {conta['ds_esperada']!r}")
        total += r["valor_em_reais"]
    return total, primeira, None


def _exercicio(cd, ate, P, conhecimento, kw):
    """O exercicio mais recente CONHECIDO em `ate`, procurando `janela_de_exercicios` anos para
    tras: ({operando: (valor, causa)}, {proveniencia}) ou ({}, None). Quem decide se o documento
    era conhecido e o leitor; o DT_REFER so nomeia o exercicio."""
    for k in range(1, P["janela_de_exercicios"] + 1):
        dt_refer = dt.date(ate.year - k + 1, 1, 1) - dt.timedelta(days=1)
        lidos, prov = {}, None
        for nome, op in P["operandos"].items():
            valor, linha, causa = _ler_operando(op, cd, dt_refer, ate, conhecimento, kw)
            lidos[nome] = (valor, causa)
            if linha is not None and prov is None:
                prov = dict(dt_refer=dt_refer.isoformat(), dt_receb=linha.get("dt_receb"),
                            sha256=linha["sha256"], arquivo=linha["arquivo"],
                            desde=str(linha["desde"]), conhecimento=conhecimento)
        if prov is not None:
            return lidos, prov
    return {}, None


# ── uma metrica ──────────────────────────────────────────────────────────────

def _tendencia(P, m):
    if m["leitura"]["tendencia"] == "MARCA":
        return {"saida": "MARCA", "causa": P["nivel_ou_tendencia"]["tendencia_estado"]}
    raise MetricaNaoImplementada(f"leitura.tendencia {m['leitura']['tendencia']!r}: so MARCA "
                                 f"existe enquanto a serie nao existe (63a)")


def _marca(cod, m, causa, motivo, **mais):
    return dict(codigo=cod, nome=m.get("nome"), saida="MARCA", causa=causa, motivo=motivo, **mais)


def _metrica(cod, P, lidos, n_universo):
    if cod not in P["metricas"]:                          # C-04: mora em campos_C04_C05
        c04 = P["campos_C04_C05"][cod]
        if c04["aplica_hoje"]:
            raise MetricaNaoImplementada(f"{cod} diz aplica_hoje e o modulo nao o calcula")
        return dict(codigo=cod, nome=c04["nome"], saida="MARCA", causa="C-04_NAO_MEDIDO",
                    motivo=f"{cod} nao medido ({c04['pendencia']}): marca e nunca exclui (P6)")
    m = P["metricas"][cod]
    if m["status"] != "IMPLEMENTADA":
        return _marca(cod, m, m["status"], m["motivo"].strip(), pendencia=m["pendencia"])
    faltam = {n: lidos.get(n, (None, ("SEM_DADO", "exercicio nao encontrado")))[1]
              for n in m["operandos"] if lidos.get(n, (None, None))[0] is None}
    if faltam:
        causa, detalhe = next(iter(faltam.values()))
        return _marca(cod, m, causa, f"{cod}: {detalhe}")
    valor = FORMULAS[m["formula_id"]]({n: lidos[n][0] for n in m["operandos"]})
    if valor is None:
        return _marca(cod, m, "INDEFINIDA",
                      f"{cod}: denominador nao positivo -- indefinida, nunca zero")
    corte = limiar(P, cod)
    base = dict(codigo=cod, nome=m["nome"], valor=valor, tendencia=_tendencia(P, m))
    if m["leitura"]["nivel"] != "CORTA":
        return dict(base, saida="MARCA", causa="NIVEL_SO_MARCA",
                    motivo=f"{cod} = {valor}: o YAML manda so marcar o nivel")
    if corte is None:
        return dict(base, saida="MARCA", causa="LIMIAR_PENDENTE",
                    motivo=f"{cod} = {valor}: limiar PENDENTE, calcula e marca sem cortar (P6)")
    abaixo = m["sentido"] == "reprova_abaixo"
    cai = valor < Decimal(str(corte)) if abaixo else valor > Decimal(str(corte))
    if not cai:
        return dict(base, saida="APROVA", corte=corte)
    return dict(base, saida="REPROVA", corte=corte, n_universo=n_universo,
                motivo=(f"{cod} ({m['nome']}) = {valor}, {'abaixo' if abaixo else 'acima'} do "
                        f"corte {corte} que voce escolheu; universo avaliado: {n_universo} "
                        f"empresas. Reprovar muda o universo, e o corte e escolha declarada, "
                        f"sem ancora legal (natureza_dos_cortes)"))


# ── a empresa ────────────────────────────────────────────────────────────────

def _empresa(cd, setor, saida, motivo, metricas=None, exercicio=None):
    return dict(cd_cvm=cd, setor=setor, saida=saida, motivo=motivo, metricas=metricas or {},
                exercicio=exercicio)


def avaliar(cd_cvm, ate, cadastro, P, *, n_universo, conhecimento="captura", **kw):
    """O portao para UMA empresa na data `ate`. `cadastro` = {CD_CVM: SETOR_ATIV}
    (`ler_cadastro`). `kw` (repo, armazem, cache) vai ao leitor."""
    cd = int(str(cd_cvm).strip())
    setor = cadastro.get(cd)
    if setor is None:
        return _empresa(cd, None, "EXIGE_DOSSIE",
                        "CD_CVM fora do cadastro: nao se sabe se e instituicao financeira, e "
                        "o portao nao assume GERAL. Fica no universo, sem peso deste bloco")
    regime = regime_do_setor(setor, P)
    if regime == FINANCEIRA:
        return _empresa(cd, setor, "RECUSA_REGIME",
                        f"SETOR_ATIV {setor!r}: instituicao financeira ou seguradora; o bloco C "
                        f"recusa e encaminha para regime_instituicao_financeira (P-31), sem numero")
    if regime == A_DECIDIR:
        return _empresa(cd, setor, "EXIGE_DOSSIE",
                        f"SETOR_ATIV {setor!r}: financeiro-adjacente ou vazio, regime da P-31 "
                        f"ainda nao decidido. Fica no universo, sem peso deste bloco")
    lidos, prov = _exercicio(cd, ate, P, conhecimento, kw)
    mets = {cod: _metrica(cod, P, lidos, n_universo) for cod in P["ordem_de_avaliacao"]}
    presentes = {m["saida"] for m in mets.values()}
    saida = next(s for s in P["saidas_do_portao"]["precedencia_na_empresa"] if s in presentes)
    motivo = "; ".join(m["motivo"] for m in mets.values() if m["saida"] == saida)
    return _empresa(cd, setor, saida, motivo, mets, prov)


# ── a contagem: quantas empresas sairiam em cada ponto da grade (27c) ────────

def _cai(valor, ponto, sentido):
    ponto = Decimal(str(ponto))
    return valor < ponto if sentido == "reprova_abaixo" else valor > ponto


def contar_em(avaliacoes, P, cod, ponto):
    sentido = P["metricas"][cod]["sentido"]
    return sum(1 for a in avaliacoes
               if "valor" in a["metricas"].get(cod, {}) and _cai(a["metricas"][cod]["valor"],
                                                                 ponto, sentido))


def contar(avaliacoes, P):
    """So numeros: sem nome, sem CD_CVM, sem preco (P-136). Empresa sem dado e contada a parte."""
    cortes, nao_impl = {}, []
    for cod in P["ordem_de_avaliacao"]:
        m = P["metricas"].get(cod)
        if m is None:
            continue
        if m["status"] != "IMPLEMENTADA":
            nao_impl.append(cod)
            continue
        causas = [a["metricas"].get(cod, {}).get("causa") for a in avaliacoes]
        cortes[cod] = dict(
            grade={str(p["valor"]): contar_em(avaliacoes, P, cod, p["valor"]) for p in m["grade"]},
            com_valor=sum(1 for a in avaliacoes if "valor" in a["metricas"].get(cod, {})),
            indefinido=causas.count("INDEFINIDA"),
            plano_diferente=causas.count("PLANO_DE_CONTAS_DIFERENTE"),
            sem_dado=causas.count("SEM_DADO"))
    return dict(
        universo_total=len(avaliacoes), cortes=cortes, nao_implementadas=nao_impl,
        regime={s: sum(1 for a in avaliacoes if a["saida"] == s)
                for s in P["saidas_do_portao"]["saidas_de_regime"]},
        sem_dado=sum(1 for a in avaliacoes if a["metricas"] and a["exercicio"] is None))
