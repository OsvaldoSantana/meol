# -*- coding: utf-8 -*-
"""CX-01: a guarda de segredo vale para TODO workflow, e reprova toda forma que nao seja
`secrets.NOME` no env de um passo autorizado. Mutacao (regua 5-B.4): cada forma, em cada
lugar, em cada workflow guardado."""
from __future__ import annotations

import copy
import os

import pytest

from guarda_segredos import PERMITIDOS_POR_WORKFLOW, defeitos_de_segredo, referencias
from test_workflows import WF, _wf

FORMAS = {
    "indice literal": "${{ secrets['R2_ESCRITA_TOKEN'] }}",
    "indice literal de nome permitido": "${{ secrets['R2_BUCKET'] }}",
    "toJSON": "${{ toJSON(secrets) }}",
    "indice dinamico": "${{ secrets[format('R2_{0}', 'ESCRITA')] }}",
    "maiuscula": "${{ SECRETS.R2_ESCRITA_TOKEN }}",
    "composta": "${{ secrets.R2_BUCKET || secrets.R2_ESCRITA_TOKEN }}",
    "espaco": "${{secrets .R2_ESCRITA_TOKEN}}",
    "dentro de funcao": "${{ format('{0}', secrets.R2_BUCKET) }}",
    "nome fora da lista": "${{ secrets.R2_ESCRITA_TOKEN }}",
    "sem fechamento": "${{ secrets.R2_BUCKET ",
}
ARQUIVOS = sorted(PERMITIDOS_POR_WORKFLOW)


def _job_e_passo(nome):
    d = _wf(nome)
    # um job sem passo autorizado (mutacao.yml) usa o primeiro job/passo
    for (j, p) in PERMITIDOS_POR_WORKFLOW[nome]:
        return j, p
    j = next(iter(d["jobs"]))
    return j, d["jobs"][j]["steps"][0].get("name")


def _lugares(nome):
    j, p = _job_e_passo(nome)

    def passo(d):
        return next(s for s in d["jobs"][j]["steps"] if s.get("name") == p)

    def outro_passo(d):
        # um passo que NAO esta na lista (ou, se todos estao, o autorizado sem env proprio)
        livres = [s for s in d["jobs"][j]["steps"]
                  if (j, s.get("name")) not in PERMITIDOS_POR_WORKFLOW[nome]]
        assert livres, nome
        return livres[0]

    return {
        "env do workflow": lambda d, v: d.setdefault("env", {}).__setitem__("X", v),
        "env do job": lambda d, v: d["jobs"][j].setdefault("env", {}).__setitem__("X", v),
        "env do passo autorizado": lambda d, v: passo(d).setdefault("env", {}).__setitem__("X", v),
        "env de outro passo": lambda d, v: outro_passo(d).setdefault("env", {}).__setitem__("X", v),
        "with": lambda d, v: outro_passo(d).__setitem__("with", {"x": v}),
        "run": lambda d, v: outro_passo(d).__setitem__("run", f"echo {v}"),
        "if": lambda d, v: outro_passo(d).__setitem__("if", v),
        "env inteiro como expressao": lambda d, v: outro_passo(d).__setitem__("env", v),
    }


@pytest.mark.parametrize("nome", ARQUIVOS)
def test_o_yaml_vigente_passa_em_cada_workflow(nome):
    assert defeitos_de_segredo(_wf(nome), PERMITIDOS_POR_WORKFLOW[nome]) == []


@pytest.mark.parametrize("nome", ARQUIVOS)
def test_vacuidade_o_passo_autorizado_tem_o_segredo(nome):
    esperado = PERMITIDOS_POR_WORKFLOW[nome]
    achados = {(j, p) for j, p, _, _ in referencias(_wf(nome))}
    assert achados == set(esperado), "a lista permite um passo que nao usa, ou ha uso sem lista"
    for chave, nomes in esperado.items():
        usados = {e.split(".", 1)[1] for j, p, _, e in referencias(_wf(nome)) if (j, p) == chave}
        assert usados == set(nomes), (chave, usados)


def test_todo_workflow_do_repositorio_tem_entrada_na_lista():
    assert sorted(f for f in os.listdir(WF) if f.endswith((".yml", ".yaml"))) == ARQUIVOS


@pytest.mark.parametrize("nome", ARQUIVOS)
@pytest.mark.parametrize("forma", sorted(FORMAS))
@pytest.mark.parametrize("onde", sorted(_lugares("medir.yml")))
def test_mutacao_toda_forma_em_todo_lugar_reprova(nome, forma, onde):
    d = copy.deepcopy(_wf(nome))
    _lugares(nome)[onde](d, FORMAS[forma])
    assert defeitos_de_segredo(d, PERMITIDOS_POR_WORKFLOW[nome]), (nome, forma, onde)


@pytest.mark.parametrize("nome", ARQUIVOS)
def test_mutacao_secrets_inherit_e_chave_secrets_reprovam(nome):
    d = copy.deepcopy(_wf(nome))
    j = next(iter(d["jobs"]))
    d["jobs"][j]["secrets"] = "inherit"
    assert defeitos_de_segredo(d, PERMITIDOS_POR_WORKFLOW[nome])


def test_mutacao_o_passo_autorizado_nao_le_segredo_de_outro_workflow():
    """Os nomes permitidos sao por passo: o R2 de escrita no passo de leitura reprova."""
    d = copy.deepcopy(_wf("medir.yml"))
    p = next(s for s in d["jobs"]["medir"]["steps"]
             if s.get("name") == "Medir (token de leitura)")
    p["env"]["R2_BUCKET"] = "${{ secrets.R2_BUCKET }}"
    achados = defeitos_de_segredo(d, PERMITIDOS_POR_WORKFLOW["medir.yml"])
    assert any("nao permitido" in x for x in achados)


def test_controle_a_forma_com_ponto_no_passo_autorizado_passa():
    d = copy.deepcopy(_wf("testes.yml"))
    p = next(s for s in d["jobs"]["completo"]["steps"]
             if s.get("name") == "Materializar o acervo do armazem")
    p["env"]["R2_BUCKET"] = "${{secrets.R2_BUCKET}}"       # sem espaco: ainda e a forma permitida
    assert defeitos_de_segredo(d, PERMITIDOS_POR_WORKFLOW["testes.yml"]) == []
