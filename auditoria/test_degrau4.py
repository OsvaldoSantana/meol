# -*- coding: utf-8 -*-
"""A guarda do degrau 4 (CLAUDE.md 5-B.18, 16/10/2026): a maquina dele so e proximo executor
depois do workflow no servidor do GitHub e do runner br-sp. Ver auditoria/degrau4.py."""
from __future__ import annotations

import csv
import io
import os
import subprocess
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import degrau4 as D  # noqa: E402

# O head do PR #81 (16/10/2026), com as 83 linhas que criaram a regra.
HEAD_DO_81 = "ff13309"


def _linha(motivo="", escada=""):
    return {"motivo": motivo, "escada": escada}


def test_o_repositorio_nao_tem_degrau_4_estacionado():
    probs = D.varrer()
    assert probs == [], "degrau 4 (5-B.18):\n" + "\n".join(probs)


def test_o_csv_do_pr_81_reprova_nas_83_linhas():
    """A guarda falha onde deveria: o CSV que criou a regra (head do #81) reprova linha a linha.
    Precisa do historico do git; no clone raso do CI o commit nao existe e o teste pula."""
    r = subprocess.run(["git", "-C", D.RAIZ, "show",
                        f"{HEAD_DO_81}:docs/marca/rodada3/classificacao.csv"],
                       capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        pytest.skip(f"{HEAD_DO_81} fora deste clone (CI raso): {r.stderr.strip()[:80]}")
    linhas = list(csv.DictReader(io.StringIO(r.stdout)))
    reprovadas = [x for x in linhas if D.problemas_da_linha(x)]
    estacionadas = [x for x in reprovadas if D.ESTACIONA in x["motivo"]]
    assert len(estacionadas) == 83
    # 16/10: a regra da escada pegou mais 6 que o status nao mostrava: pulada como
    # site_inacessivel, com "4) pendente: maquina dele" (Featbank e cinco casas da APIMEC)
    assert len(reprovadas) == 89
    sem_nuvem = [x for x in reprovadas
                 if any("4a) e 4b)" in p for p in D.problemas_da_linha(x))]
    assert len(sem_nuvem) == 89


def test_mutacao_aguarda_degrau_4_reprova():
    assert D.problemas_da_linha(_linha("site_inacessivel: 403. AGUARDA DEGRAU 4"))


def test_maquina_dele_sem_os_executores_de_nuvem_reprova():
    """A frase das 83 linhas, sem o status, ainda reprova pela escada."""
    probs = D.problemas_da_linha(_linha(
        "site_inacessivel: 403", "1) Chromium: 403; 4) pendente: maquina dele"))
    assert probs == ["a maquina dele no degrau 4 sem 4a) e 4b) transcritos na escada"]
    assert D.problemas_da_linha(_linha("x", "1) curl 403; 4c) sessao local: 200"))


def test_a_ordem_transcrita_passa():
    escada = ("1) Chromium: 403 Akamai; 4a) workflow captura_r3 no servidor do GitHub (run 1): "
              "403; 4b) runner br-sp: nao existe (16/10); 4c) sessao local (IP BR): 200")
    assert D.problemas_da_linha(_linha("", escada)) == []


def test_aguarda_executor_nuvem_exige_o_proximo_nomeado():
    assert D.problemas_da_linha(_linha("site_inacessivel: AGUARDA_EXECUTOR_NUVEM", "1) 403"))
    assert not D.problemas_da_linha(_linha(
        "site_inacessivel: AGUARDA_EXECUTOR_NUVEM",
        "1) 403; 4a) workflow (run 1): 403; 4b) br-sp: nao existe; proximo executor: runner br-sp"))


_PEND = """# x

## Ao voltar ao desktop

1. **Um:** rodar o script do envio.
2. **Dois, o degrau 4:** `curl` de IP residencial no site do gestor
   e nas paginas dos bancos.
3. **Tres, o degrau 4:** 4a) workflow (run 9): 403; 4b) br-sp: nao existe; entao a sessao local.

## Outra secao

4. degrau 4 aqui nao e da secao.
"""


def test_secao_desktop_item_que_manda_a_maquina_subir_o_degrau_4_reprova():
    v = D.violacoes_desktop(_PEND)
    assert [n for n, _ in v] == [6]
    assert "paginas dos bancos" in v[0][1]           # a continuacao entra no item


def test_linha_de_base_casa_pelo_conteudo_e_so_encolhe(tmp_path):
    p = tmp_path / "PENDENCIAS.md"
    p.write_text(_PEND, encoding="utf-8")
    item = D.violacoes_desktop(_PEND)[0][1]
    assert D.varrer_pendencias(str(p), base={D.chave(item): "anterior a regra"}) == ([], [])
    novas, velhas = D.varrer_pendencias(str(p), base={"000000000000": "motivo"})
    assert len(novas) == 1 and len(velhas) == 1


def test_linha_de_base_exige_motivo(tmp_path):
    b = tmp_path / "base.txt"
    b.write_text("abcdef012345 |\n", encoding="utf-8")
    with pytest.raises(ValueError):
        D.ler_base(str(b))
