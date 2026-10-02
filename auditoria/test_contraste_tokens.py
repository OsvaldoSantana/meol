# -*- coding: utf-8 -*-
"""Todo par de cor declarado das direcoes passa no limiar da WCAG do seu tipo (P-163)."""
from __future__ import annotations

import os
import sys

import pytest
import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import contraste_tokens as CT  # noqa: E402


def test_vacuidade_as_tres_direcoes_da_resposta_16b_tem_pares():
    """Sem direcoes ou sem pares, o teste de baixo passaria sem medir nada."""
    tok = CT.carregar()
    assert set(tok["direcoes"]) == {"E", "C", "D"}, "resposta 16b: E, C e D"
    assert all(len(d["pares"]) >= 8 for d in tok["direcoes"].values())


def test_todo_par_declarado_passa_no_limiar_do_seu_tipo():
    ruins = [f"{x['direcao']} {x['frente']}/{x['fundo']} {x['razao']:.4f} < {x['limiar']} "
             f"({x['tipo']}, {x['criterio']})" for x in CT.avaliar(CT.carregar())
             if not x["passa"]]
    assert not ruins, ruins


def test_os_limiares_sao_os_da_wcag_transcrita():
    """P1: o numero do YAML e o da fonte. Se alguem afrouxar o limiar, reprova."""
    lim = CT.carregar()["limiares"]
    assert lim["texto_pequeno"]["razao"] == 4.5 and "1.4.3" in lim["texto_pequeno"]["criterio"]
    assert lim["texto_grande"]["razao"] == 3.0 and "1.4.3" in lim["texto_grande"]["criterio"]
    assert lim["componente"]["razao"] == 3.0 and "1.4.11" in lim["componente"]["criterio"]


def test_texto_grande_declara_o_tamanho_que_o_faz_grande():
    assert CT.grande_sem_tamanho(CT.carregar()) == []


def test_toda_cor_de_estado_tem_rotulo():
    assert CT.status_sem_rotulo(CT.carregar()) == []


def test_a_conta_bate_com_a_medicao_do_rosto_v1():
    """As tres razoes medidas em 26/09 sobre o Quanto-e-Onde (docs/decisoes/rosto-v1.md)."""
    assert round(CT.razao("#6D7C8B", "#EFF3F7"), 2) == 3.84
    assert round(CT.razao("#6D7C8B", "#E3EAF1"), 2) == 3.53
    assert round(CT.razao("#C4D0DD", "#EFF3F7"), 2) == 1.40
    assert CT.razao("#000000", "#FFFFFF") == pytest.approx(21.0)


def _tok_com(tmp_path, par, cores):
    tok = CT.carregar()
    tok["direcoes"] = {"X": {"cores": cores, "pares": [par]}}
    p = tmp_path / "t.yaml"
    p.write_text(yaml.safe_dump(tok), encoding="utf-8")
    return CT.carregar(str(p))


def test_mutacao_o_par_do_quanto_e_onde_reprova_como_texto_pequeno(tmp_path):
    """A guarda falha quando deveria (regua 5-B, pergunta 4): #6D7C8B sobre #EFF3F7 e
    3,84:1 e reprova como texto pequeno; o mesmo par passa como componente (3:1)."""
    cores = {"a": "#6D7C8B", "b": "#EFF3F7"}
    tok = _tok_com(tmp_path, {"frente": "a", "fundo": "b", "tipo": "texto_pequeno"}, cores)
    (linha,) = CT.avaliar(tok)
    assert not linha["passa"] and 3.83 < linha["razao"] < 3.85
    tok = _tok_com(tmp_path, {"frente": "a", "fundo": "b", "tipo": "componente"}, cores)
    assert CT.avaliar(tok)[0]["passa"]


def test_mutacao_sem_arredondar(tmp_path):
    """4,499:1 nao passa em 4,5:1 (Understanding 1.4.3). #767676 sobre branco da 4,54;
    procura-se um cinza logo abaixo e confere-se que a comparacao e estrita."""
    cinza = next(f"#{v:02X}{v:02X}{v:02X}" for v in range(0x76, 0x80)
                 if CT.razao(f"#{v:02X}{v:02X}{v:02X}", "#FFFFFF") < 4.5)
    tok = _tok_com(tmp_path, {"frente": "a", "fundo": "b", "tipo": "texto_pequeno"},
                   {"a": cinza, "b": "#FFFFFF"})
    x = CT.avaliar(tok)[0]
    assert x["razao"] > 4.4 and not x["passa"]


def test_mutacao_texto_pequeno_rotulado_como_grande_reprova(tmp_path):
    tok = _tok_com(tmp_path, {"frente": "a", "fundo": "b", "tipo": "texto_grande",
                              "tamanho_px": 12}, {"a": "#6D7C8B", "b": "#EFF3F7"})
    assert CT.grande_sem_tamanho(tok) == ["X: a sobre b (12 px)"]


def test_mutacao_cor_de_estado_sem_rotulo_reprova(tmp_path):
    tok = _tok_com(tmp_path, {"frente": "a", "fundo": "b", "tipo": "componente"},
                   {"a": "#000000", "b": "#FFFFFF", "status_alerta": "#AA0000"})
    assert CT.status_sem_rotulo(tok) == ["X: status_alerta"]
