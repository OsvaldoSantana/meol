# -*- coding: utf-8 -*-
"""O PLANO nao repete limitacao retirada, e as pendencias ativas cabem no que se le inteiro.

POR QUE EXISTE (03/10/2026, decisao dele: dieta completa do processo).
  1. O PLANO.md afirmou por duas semanas "um CAPTCHA por ano" no anual do COTAHIST. A entrada
     `limitacoes_declaradas.captura_do_cotahist_passa_por_captcha` foi RETIRADA em 18/09, no dia
     em que foi escrita: os 41 anuais vieram por GET simples. O plano e lido em toda sessao, e
     uma limitacao falsa ali decide o que a sessao acha que nao da para fazer (5-B.13).
  2. O PENDENCIAS.md foi dividido: ate 20 ATIVAS, lidas inteiras em toda sessao, e a reserva em
     docs/pendencias-reserva.md, lida por busca. Sem teto, as ativas voltam a crescer ate
     ninguem as ler -- foi o que fez o arquivo unico chegar a ~40 mil tokens.
  3. P-171: pendencia aberta sem dono, gatilho ou classe e desabafo (5-A.1), nos dois arquivos.
  4. Uma pendencia nao pode estar aberta e fechada ao mesmo tempo: fila desatualizada ja reabriu
     tarefa pronta tres vezes.

O QUE NAO COBRE (P5): nao le o PLANO procurando OUTRA limitacao retirada -- so a do CAPTCHA,
que e a que aconteceu; nao julga se uma ativa deveria estar na reserva (isso e a triagem).
"""
from __future__ import annotations

import importlib.util
import io
import os
import re

import pytest
import yaml

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_spec = importlib.util.spec_from_file_location("estado", os.path.join(RAIZ, "tools", "estado.py"))
assert _spec and _spec.loader
E = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(E)

RETIRADA_DO_CAPTCHA = "captura_do_cotahist_passa_por_captcha"


def _ler(*partes):
    with io.open(os.path.join(RAIZ, *partes), encoding="utf-8") as f:
        return f.read()


def afirma_captcha(plano: str) -> list[str]:
    """As linhas do plano que falam de CAPTCHA. O plano nao tem motivo para citar uma
    limitacao retirada: a historia dela mora no politica.yaml e no historico."""
    return [linha.strip() for linha in plano.splitlines() if re.search(r"captcha", linha, re.I)]


def excesso_de_ativas(texto_ativas: str) -> int:
    """Quantas ativas passam do teto (0 = cabe)."""
    return max(0, len(E.pendencias(texto_ativas)) - E.LIMITE_ATIVAS)


def abertas_e_fechadas(abertas: set[str], texto_fechadas: str) -> set[str]:
    """Codigos que estao abertos e tambem riscados como fechados."""
    riscados = set(re.findall(r"(?m)^## ~~(P-\d+)~~", texto_fechadas))
    return abertas & riscados


# ── sobre o repositorio ──────────────────────────────────────────────────────────

@pytest.mark.repositorio   # 146b: le o repositorio, a mutacao exclui
def test_o_PLANO_nao_afirma_captcha_no_cotahist():
    lims = yaml.safe_load(_ler("alocacao", "politica.yaml"))["limitacoes_declaradas"]
    # Vacuidade: se a entrada deixar de ser RETIRADA, o teste perde o fundamento e avisa.
    assert lims[RETIRADA_DO_CAPTCHA].get("RETIRADA"), (
        f"{RETIRADA_DO_CAPTCHA} deixou de ser RETIRADA: reveja este teste antes de mexer no plano")
    linhas = afirma_captcha(_ler("PLANO.md"))
    assert not linhas, (
        f"o PLANO.md fala de CAPTCHA, e a limitacao foi RETIRADA em 18/09 "
        f"(politica.yaml -> {RETIRADA_DO_CAPTCHA}): {linhas}")


@pytest.mark.repositorio
def test_as_ativas_cabem_no_teto():
    ativas = E.pendencias(_ler("PENDENCIAS.md"))
    assert ativas, "nenhuma ativa lida -- o formato do cabecalho mudou e a guarda ficou muda"
    assert len(ativas) <= E.LIMITE_ATIVAS, (
        f"{len(ativas)} ativas; o teto e {E.LIMITE_ATIVAS} (decisao de 03/10). Mova para "
        f"docs/pendencias-reserva.md ou feche, antes de abrir outra")


@pytest.mark.repositorio
def test_toda_pendencia_aberta_tem_dono_gatilho_e_classe():
    abertas = (E.pendencias(_ler("PENDENCIAS.md"))
               + E.pendencias(_ler("docs", "pendencias-reserva.md")))
    assert len(abertas) > 20, "a reserva nao foi lida -- a guarda ficou muda"
    assert E.sem_campos(abertas) == [], "5-A.1 e P-171: " + ", ".join(E.sem_campos(abertas))


@pytest.mark.repositorio
def test_nenhuma_pendencia_esta_em_dois_lugares():
    ativas = {p["codigo"] for p in E.pendencias(_ler("PENDENCIAS.md"))}
    reserva = {p["codigo"] for p in E.pendencias(_ler("docs", "pendencias-reserva.md"))}
    assert not ativas & reserva, f"ativa e reserva ao mesmo tempo: {sorted(ativas & reserva)}"
    fechadas = _ler("docs", "historico", "pendencias-fechadas.md")
    dupla = abertas_e_fechadas(ativas | reserva, fechadas)
    assert not dupla, f"abertas e riscadas como fechadas: {sorted(dupla)}"


# ── prova por mutacao (5-B.4): a guarda falha quando deveria ──────────────────────

def test_mutacao_a_frase_do_plano_antigo_e_pega():
    """A linha do PLANO de ate 03/10, como estava."""
    antigo = "**O que impede hoje:** nada além de estar na máquina — e **um CAPTCHA por ano**."
    assert afirma_captcha(antigo) and not afirma_captcha("O anual roda no cron uma vez por mes.")


def _ativas(n: int) -> str:
    return "".join(f"## P-{i} · T\n\n**Dono:** C · **Gatilho:** g · **Classe:** "
                   "`DECISAO_DE_DESENHO`\n\n---\n\n" for i in range(9001, 9001 + n))


def test_mutacao_a_vigesima_primeira_ativa_reprova():
    assert excesso_de_ativas(_ativas(20)) == 0
    assert excesso_de_ativas(_ativas(21)) == 1


def test_mutacao_pendencia_sem_classe_reprova():
    texto = _ativas(2).replace("**Classe:** `DECISAO_DE_DESENHO`", "", 1)
    assert E.sem_campos(E.pendencias(texto)) == ["P-9001 (classe)"]


def test_mutacao_aberta_e_riscada_ao_mesmo_tempo_reprova():
    fechadas = "## ~~P-9002~~ · T — **FECHADA em 03/10/2026**\n"
    assert abertas_e_fechadas({"P-9001", "P-9002"}, fechadas) == {"P-9002"}
    assert abertas_e_fechadas({"P-9001"}, fechadas) == set()
