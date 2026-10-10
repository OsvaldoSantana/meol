# -*- coding: utf-8 -*-
"""P-17 -- C-04 e C-05 com nome, fase e fonte, lidos no escopo; nenhum limiar inventado.

POR QUE ESTE TESTE EXISTE (10/10/2026). De 05/09 a 10/10 o `bloco_C_solvencia` citava C-04
e C-05 como existentes e nunca os nomeava (`lacuna_declarada`): o escopo estava fora de
alcance quando o bloco foi escrito. A lista mora em docs/auditoria/escopo-campos-de-analise.md
e foi lida. Tres coisas nao podem voltar:

  1. a lacuna -- o bloco C de novo sem saber o que sao os dois campos;
  2. o C-04 aplicado como EXCLUSAO antes de existir o dado dele. A moeda da divida esta na
     nota de instrumentos financeiros, que so a segunda esteira (P-65) le; ate la, cortar
     por C-04 seria excluir por falta de dado (P6);
  3. um limiar do C-05 no YAML sem a decisao dele (fila, bloco 27). O escopo nao da limiar
     nenhum como regra (secao 7); o "caixa < divida CP" dele e o exemplo do bloco L.

ALCANCE (P5): confere o YAML contra o escopo e contra o estado da P-65 e do bloco 27. NAO
confere comportamento do motor: nenhum modulo aplica o bloco C ainda (P-30). Quando aplicar,
o teste do C-04 tem de ganhar a irma comportamental (uma empresa sem C-04 continua no
universo), como o F-01 pediu duas simulacoes em vez de um atributo.
"""
from __future__ import annotations

import io
import os
import re
import sys
import unicodedata

import pytest
import yaml

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)
import test_limitacoes_tipo as L  # noqa: E402

ESCOPO = os.path.join(RAIZ, "docs", "auditoria", "escopo-campos-de-analise.md")
FILA = os.path.join(RAIZ, "docs", "decisoes", "fila-do-osvaldo.md")


def _ler(caminho):
    with io.open(caminho, encoding="utf-8") as f:
        return f.read()


def _bloco_c():
    with io.open(os.path.join(AQUI, "politica.yaml"), encoding="utf-8") as f:
        return yaml.safe_load(f)["bloco_C_solvencia"]


def _norm(s):
    s = unicodedata.normalize("NFKD", s.replace("×", "x"))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s).strip().lower()


def _escopo_bloco_c():
    """{"C-04": nome} da tabela do bloco C e {"A": linha, "B": linha} da secao 8."""
    texto = _ler(ESCOPO)
    nomes = {m.group(1): m.group(2) for m in
             re.finditer(r"(?m)^\| (C-\d{2}) \| ([^|]+?) \|", texto)}
    fases = {m.group(1): m.group(2) for m in
             re.finditer(r"(?m)^\*\*Fase ([A-D]) — (.*)$", texto)}
    return nomes, fases


def defeitos_c04(c04, pendencias):
    """[o que esta errado] na entrada do C-04 -- vazio e o unico resultado aceito.

    Enquanto a P-65 estiver aberta, o C-04 nao se aplica e nao exclui; a entrada passa pelo
    mesmo portao das limitacoes (`tipo`, `o_que_resolveria`, `pendencia` aberta)."""
    falta = list(L.defeitos({"C-04": c04}, pendencias).get("C-04", []))
    if c04.get("pendencia") != "P-65":
        falta.append(f"pendencia {c04.get('pendencia')!r}: o caminho do C-04 e a P-65")
    if pendencias.get("P-65"):
        if c04.get("aplica_hoje") is not False:
            falta.append("aplica_hoje deveria ser false com a P-65 aberta")
        texto = _norm(str(c04.get("enquanto_falta", "")))
        if "admitir com marcacao" not in texto or "nao tira ninguem do universo" not in texto:
            falta.append("enquanto_falta nao diz que admite com marcacao e nao exclui")
        if "limiar" in c04 or "corte" in c04:
            falta.append("corte do C-04 declarado antes de existir o dado dele")
    return falta


def test_a_lacuna_de_c04_c05_nao_volta():
    """Falha na 1.39.0: la havia `lacuna_declarada`, e a ordem dizia "VER LACUNA DECLARADA"."""
    b = _bloco_c()
    assert "lacuna_declarada" not in b, "a lacuna de C-04/C-05 voltou ao bloco C"
    ordem = " ".join(b["ordem"])
    assert "LACUNA DECLARADA" not in ordem
    assert "C-04" in ordem and "C-05" in ordem and "campos_C04_C05" in ordem
    campos = b["campos_C04_C05"]
    assert {"C-04", "C-05"} <= set(campos)


@pytest.mark.repositorio   # 146b: le o repositorio, a mutacao exclui
def test_c04_e_c05_tem_o_nome_e_a_fase_do_escopo():
    """O YAML cita o escopo, nao o reescreve: nome e fase batem com a tabela e a secao 8."""
    nomes, fases = _escopo_bloco_c()
    campos = _bloco_c()["campos_C04_C05"]
    assert set(nomes) >= {"C-04", "C-05"}, f"tabela do bloco C nao lida no escopo: {nomes}"
    for cod in ("C-04", "C-05"):
        assert _norm(campos[cod]["nome"]) == _norm(nomes[cod]), cod
        fase = campos[cod]["fase"]
        assert cod in fases[fase], f"{cod} na fase {fase} do YAML, nao na do escopo"
        assert all(cod not in v for k, v in fases.items() if k != fase), cod


@pytest.mark.repositorio   # 146b: le o repositorio, a mutacao exclui
def test_c04_nao_e_exclusao_enquanto_a_p65_nao_existir():
    """Falha na 1.39.0 (o C-04 nem existia como entrada). Com a P-65 aberta, o C-04 e
    lacuna com caminho e marca 'nao medido'; quando ela fechar, este teste obriga a revisar."""
    pend = L._pendencias()
    assert "P-65" in pend, "a P-65 sumiu dos tres arquivos de pendencias"
    c04 = _bloco_c()["campos_C04_C05"]["C-04"]
    assert defeitos_c04(c04, pend) == []
    item = next(i for i in _bloco_c()["ordem"] if "C-04" in i)
    assert "NAO SE APLICA" in item and "nunca exclui" in item


def test_a_guarda_do_c04_falha_quando_deveria():
    """5-B.4: reintroduzir o defeito tem de reprovar. Tres mutacoes, cada uma sozinha."""
    pend = {"P-65": True}
    boa = dict(_bloco_c()["campos_C04_C05"]["C-04"])
    assert defeitos_c04(boa, pend) == []
    for mutacao in ({"aplica_hoje": True},
                    {"limiar": 0.5},
                    {"enquanto_falta": "exclui a empresa sem o dado"},
                    {"pendencia": "P-30"}):
        assert defeitos_c04({**boa, **mutacao}, pend), f"a guarda deixou passar {mutacao}"


@pytest.mark.repositorio   # 146b: le o repositorio, a mutacao exclui
def test_limiar_do_c05_so_entra_com_o_bloco_27_respondido():
    """O escopo nao escolhe limiar (secao 7). Ate ele responder o bloco 27, o YAML diz
    PENDENTE; um numero ali com o bloco sem resposta e criterio inventado."""
    c05 = _bloco_c()["campos_C04_C05"]["C-05"]
    assert c05["limiar_decide"] == "usuario"
    assert "bloco 27" in c05["limiar_onde"]
    m = re.search(r"(?m)^## 27 · .*$", _ler(FILA))
    assert m, "o bloco 27 da fila (o limiar do C-05) nao existe"
    assert "C-05" in m.group(0)
    if "respondido" not in m.group(0):
        assert c05["limiar"] == "PENDENTE", "limiar do C-05 sem a decisao dele"
        assert "nao corta" in _norm(c05["enquanto_o_limiar_falta"])
