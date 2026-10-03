# -*- coding: utf-8 -*-
"""O `medir.yml` nao ganha poder: so `contents: write`, e o token de LEITURA em um passo so.

Por que (decisao dele, 26/09/2026): um script de medicao roda codigo da branch com o token
do armazem no ambiente. Se ele tivesse o token de escrita, poderia apagar uma versao da CVM
que a CVM nao guarda mais (CV-01); se tivesse mais permissao no GitHub, o disparo por push
viraria atalho para agir no repositorio. `defeitos()` e funcao pura para poder ser provada
por mutacao (regua 5-B, pergunta 4)."""
from __future__ import annotations

import copy
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from guarda_segredos import PERMITIDOS_POR_WORKFLOW, defeitos_de_segredo, referencias  # noqa: E402
from test_workflows import _wf  # noqa: E402

PASSO_QUE_MEDE = ("medir", "Medir (token de leitura)")
PERMITIDOS = PERMITIDOS_POR_WORKFLOW["medir.yml"]


def defeitos(d):
    """[o que o workflow faz alem do permitido] -- vazio e o unico resultado aceito.

    O segredo e conferido por lista de permissao (CX-01, `guarda_segredos`), nao por regex."""
    out = []
    if d.get("permissions") != {"contents": "write"}:
        out.append(f"permissions do workflow = {d.get('permissions')!r}; so contents: write")
    if d.get("on") != {"push": {"branches": ["medir/**"]}}:
        out.append(f"gatilho = {d.get('on')!r}; so push em medir/**")
    for nome_job, job in d.get("jobs", {}).items():
        if "permissions" in job:
            out.append(f"job {nome_job} declara permissions proprias: {job['permissions']!r}")
    return out + defeitos_de_segredo(d, PERMITIDOS)


def test_o_medir_yml_so_tem_contents_write_e_o_token_de_leitura_num_passo():
    d = _wf("medir.yml")
    assert defeitos(d) == []
    com = {(j, p) for j, p, _, _ in referencias(d)}
    assert com == {PASSO_QUE_MEDE}, "vacuidade: o passo que mede tem de ter o token"
    assert len(referencias(d)) == 4


def _mutante(f):
    d = copy.deepcopy(_wf("medir.yml"))
    f(d)
    return defeitos(d)


def _passo(d, nome):
    return next(p for p in d["jobs"]["medir"]["steps"] if p.get("name") == nome)


def test_mutacao_permissao_a_mais_reprova():
    assert _mutante(lambda d: d["permissions"].update({"actions": "write"}))
    assert _mutante(lambda d: d.update(permissions="write-all"))
    assert _mutante(lambda d: d["jobs"]["medir"].update(permissions={"issues": "write"}))


def test_mutacao_token_de_escrita_reprova():
    def troca(d):
        _passo(d, "Medir (token de leitura)")["env"]["R2_ACCESS_KEY_ID"] = \
            "${{ secrets.R2_ACCESS_KEY_ID }}"
    assert any("nao permitido" in x for x in _mutante(troca))


def test_mutacao_segredo_fora_do_passo_reprova():
    assert _mutante(lambda d: d["jobs"]["medir"].update(
        env={"R2_BUCKET": "${{ secrets.R2_LEITURA_BUCKET }}"}))
    assert _mutante(lambda d: d.update(env={"X": "${{ secrets.R2_LEITURA_BUCKET }}"}))
    assert _mutante(lambda d: _passo(d, "Conferir insumos").update(
        env={"R2_BUCKET": "${{ secrets.R2_LEITURA_BUCKET }}"}))
    assert _mutante(lambda d: _passo(d, "Resumo").update(
        run="echo ${{ secrets.R2_LEITURA_BUCKET }}"))


def test_mutacao_outro_gatilho_reprova():
    assert _mutante(lambda d: d["on"].update(workflow_dispatch=None))
    assert _mutante(lambda d: d["on"]["push"].update(branches=["**"]))


# CX-01: as formas que o regex `secrets\.NOME` nao enxergava. Cada uma, em cada lugar onde um
# segredo poderia vazar, tem de reprovar. `_ONDE` e a lista dos lugares (do mais largo ao passo).
_FORMAS_QUE_ESCAPAVAM = {
    "indice literal": "${{ secrets['R2_ESCRITA_TOKEN'] }}",
    "indice literal leitura": "${{ secrets['R2_LEITURA_BUCKET'] }}",
    "toJSON": "${{ toJSON(secrets) }}",
    "indice dinamico": "${{ secrets[format('R2_{0}', 'ESCRITA')] }}",
    "maiuscula": "${{ SECRETS.R2_ESCRITA_TOKEN }}",
    "composta": "${{ secrets.R2_LEITURA_BUCKET || secrets.R2_ESCRITA_TOKEN }}",
    "espaco": "${{secrets .R2_ESCRITA_TOKEN}}",
}


def _onde():
    def workflow(d, v):
        d.setdefault("env", {})["X"] = v

    def job(d, v):
        d["jobs"]["medir"].setdefault("env", {})["X"] = v

    def passo_sem_segredo_env(d, v):
        _passo(d, "Conferir insumos")["env"] = {"X": v}

    def passo_autorizado_env(d, v):
        _passo(d, "Medir (token de leitura)")["env"]["X"] = v

    def passo_with(d, v):
        _passo(d, "Conferir insumos")["with"] = {"x": v}

    def passo_run(d, v):
        _passo(d, "Resumo")["run"] = f"echo {v}"

    return {f.__name__: f for f in (workflow, job, passo_sem_segredo_env, passo_autorizado_env,
                                    passo_with, passo_run)}


@pytest.mark.parametrize("forma", sorted(_FORMAS_QUE_ESCAPAVAM))
@pytest.mark.parametrize("onde", sorted(_onde()))
def test_cx01_forma_de_segredo_que_escapava_do_regex_reprova(forma, onde):
    v = _FORMAS_QUE_ESCAPAVAM[forma]
    assert _mutante(lambda d: _onde()[onde](d, v)), (forma, onde)
