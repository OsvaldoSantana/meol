# -*- coding: utf-8 -*-
"""Regua 5-B.16 -- ausencia de dado por problema tecnico e pendencia de conserto, nunca
limitacao declarada.

POR QUE ESTE PORTAO EXISTE (23/09/2026). O `COTAHIST_A2026.ZIP` chegou cortado em 18/09.
Era defeito de transporte, e o conserto era baixar de novo. Eu o tratei como limitacao
e cortei o periodo da familia ML em dez/2025 -- e o arquivo integro esteve no disco 44 h
antes do commit que declarou 2026 indisponivel (P-100). `limitacoes_declaradas` e a
secao em que o leitor confia por construcao; uma falha tecnica escrita ali encerra a
investigacao e fica com cara de rigor.

O portao: toda entrada operante diz se o limite e do MUNDO (`FISICA`) ou NOSSO
(`NAO_CONSERTADA`). A segunda so entra com o que a desfaz (`o_que_resolveria`) e com o
endereco da divida (`pendencia`, aberta em PENDENCIAS.md ou na reserva). Pendencia fechada com
limitacao de pe e a P-118: declaracao que o repositorio ja contradiz.

ALCANCE (P5 aplicada ao instrumento): mede que os campos EXISTEM e que a pendencia esta
aberta. NAO mede que a classificacao esteja certa -- chamar de FISICA o que e conserto
passa aqui. O que segura isso e o `por_que_fisica` escrito e a leitura de quem revisa.
"""
from __future__ import annotations
import io
import pytest
import os
import re

import yaml

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
TIPOS = ("FISICA", "NAO_CONSERTADA")
HISTORICO = ("RETIRADA", "RESOLVIDA")
PEND = re.compile(r"^P-\d+$")


def _limitacoes():
    with io.open(os.path.join(AQUI, "politica.yaml"), encoding="utf-8") as f:
        return yaml.safe_load(f)["limitacoes_declaradas"]


def _pendencias():
    """{"P-57": aberta?} lido dos cabecalhos `## P-NN` do PENDENCIAS.md. Fechada e a que
    tem o numero riscado (`~~P-NN~~`) ou FECHADA/CONSERTADA no titulo -- as duas
    convencoes que o arquivo usa."""
    # 26/09: as fechadas moram no historico; as duas pontas contam (sem a segunda, toda
    # pendencia fechada viraria "inexistente", e a ancora P-57/P-100 deixaria de medir).
    texto = ""
    # 03/10: o PENDENCIAS.md virou so as ativas; a reserva tambem e aberta, e conta.
    for nome in ("PENDENCIAS.md", os.path.join("docs", "pendencias-reserva.md"),
                 os.path.join("docs", "historico", "pendencias-fechadas.md")):
        with io.open(os.path.join(RAIZ, nome), encoding="utf-8") as f:
            texto += f.read() + "\n"
    estado = {}
    for linha in texto.splitlines():
        if not linha.startswith("## "):
            continue
        for num in re.findall(r"P-\d+", linha.split("·")[0]):
            fechada = f"~~{num}~~" in linha or "FECHADA" in linha or "CONSERTADA" in linha
            estado[num] = not fechada
    return estado


def defeitos(lims, pendencias):
    """{nome: [o que falta]} -- vazio e o unico resultado aceito."""
    out = {}
    for nome, lim in lims.items():
        falta = []
        if isinstance(lim, dict) and any(lim.get(h) for h in HISTORICO):
            continue
        if not isinstance(lim, dict):
            out[nome] = ["texto solto: sem `tipo` (vire dicionario)"]
            continue
        tipo = lim.get("tipo")
        if tipo not in TIPOS:
            falta.append(f"tipo {tipo!r} fora de {TIPOS}")
        if tipo == "NAO_CONSERTADA":
            if not str(lim.get("o_que_resolveria") or "").strip():
                falta.append("sem `o_que_resolveria`")
            p = str(lim.get("pendencia") or "")
            if not PEND.match(p):
                falta.append(f"`pendencia` {p!r} nao e P-NN")
            elif p not in pendencias:
                falta.append(f"{p} nao existe nas pendencias (ativas, reserva ou fechadas)")
            elif not pendencias[p]:
                falta.append(f"{p} esta FECHADA -- ou a limitacao saiu, ou a pendencia reabre")
        if falta:
            out[nome] = falta
    return out


# ── o portao sobre o arquivo real ─────────────────────────────────────────────

@pytest.mark.repositorio   # 146b: le o repositorio, a mutacao exclui
def test_5B16_toda_limitacao_diz_se_e_do_mundo_ou_nossa():
    assert defeitos(_limitacoes(), _pendencias()) == {}


def test_5B16_os_dois_tipos_estao_em_uso():
    """Vacuidade: se todas virassem RESOLVIDA, o portao passaria sem ter visto nada."""
    tipos = {lim.get("tipo") for lim in _limitacoes().values() if isinstance(lim, dict)}
    assert set(TIPOS) <= tipos


@pytest.mark.repositorio   # 146b: le o repositorio, a mutacao exclui
def test_5B16_a_leitura_das_pendencias_ve_aberta_e_fechada():
    """O portao depende de ler PENDENCIAS.md; se o formato do cabecalho mudar e ninguem
    for achado, toda pendencia vira 'nao existe' -- e o teste acima falharia pelo motivo
    errado. Falhar aqui explica."""
    p = _pendencias()
    # A ancora aberta era a P-57, que fechou em 25/09, e depois a P-44, que fechou em 03/10
    # ao virar regra (CLAUDE.md 5-A.5). A P-48 (vies de sobrevivencia) mora na reserva e so
    # fecha com a composicao historica do indice; se fechar, troque a ancora, nao o teste.
    assert p.get("P-48") is True, "P-48 deveria estar aberta (na reserva)"
    assert p.get("P-145") is True, "P-145 deveria estar aberta (nas ativas)"
    assert p.get("P-44") is False, "P-44 fechou em 03/10"
    assert p.get("P-100") is False, "P-100 fechou em 23/09"
    assert p.get("P-57") is False, "P-57 fechou em 25/09"


# ── prova por mutacao (regra 4 da 5-B) ────────────────────────────────────────

# Universo de pendencias da mutacao: codigos REAIS (o `achados_ancorados` le este
# arquivo, e codigo inventado vira orfao). O estado aqui e o da fixture, nao o do disco.
_ABERTAS = {"P-57": True, "P-100": False}


def _nc(**kw):
    base = {"tipo": "NAO_CONSERTADA", "o_que_resolveria": "baixar de novo",
            "pendencia": "P-57"}
    base.update(kw)
    return {k: v for k, v in base.items() if v is not None}


def test_mutacao_entrada_sem_tipo_e_ACUSADA():
    assert "x" in defeitos({"x": {"o_que_falta": "algo"}}, _ABERTAS)


def test_mutacao_tipo_inventado_e_ACUSADO():
    assert "x" in defeitos({"x": _nc(tipo="LIMITACAO")}, _ABERTAS)


def test_mutacao_texto_solto_e_ACUSADO():
    assert "x" in defeitos({"x": "uma frase qualquer"}, _ABERTAS)


def test_mutacao_NAO_CONSERTADA_sem_o_que_resolveria_e_ACUSADA():
    assert defeitos({"x": _nc(o_que_resolveria=None)}, _ABERTAS) == {
        "x": ["sem `o_que_resolveria`"]}


def test_mutacao_NAO_CONSERTADA_sem_pendencia_e_ACUSADA():
    assert "x" in defeitos({"x": _nc(pendencia=None)}, _ABERTAS)


def test_mutacao_pendencia_inexistente_e_ACUSADA():
    assert "x" in defeitos({"x": _nc(pendencia="P-12")}, _ABERTAS)


def test_mutacao_pendencia_FECHADA_com_limitacao_de_pe_e_ACUSADA():
    """A P-118 na forma de portao."""
    assert "x" in defeitos({"x": _nc(pendencia="P-100")}, _ABERTAS)


def test_FISICA_nao_exige_pendencia_e_historico_nao_passa_pelo_portao():
    lims = {"a": {"tipo": "FISICA"}, "b": {"RETIRADA": "motivo"},
            "c": {"RESOLVIDA": "motivo"}}
    assert defeitos(lims, _ABERTAS) == {}


def test_a_entrada_bem_formada_passa():
    assert defeitos({"x": _nc()}, _ABERTAS) == {}
