# -*- coding: utf-8 -*-
"""CX-05: a guarda do modelo em branco conferia o dicionario de dados, nao os problemas.

Achado externo (auditoria do Codex, 03/10/2026, `A-02` no original; registro em
`docs/auditoria/AUDITORIA-CODEX-2026-10-03.md`). `validar()` devolve `(dados, problemas,
avisos)`, e `test_o_modelo_nao_carrega_ate_alguem_preencher` desempacotava
`problemas, _avisos, _ = validar(d)`: `problemas` recebia o DICIONARIO de dados. Como o modelo
tem as chaves obrigatorias (com valor nulo), `assert problemas` e o laco que procura o nome de
cada campo passavam por acaso. E o padrao F-05/N-01/R-01/S-02: o teste declarava um
comportamento e media outro, e os dois concordavam por acidente.

Os dois mutantes da auditoria (secao 9.9) viram testes permanentes: com o validador sem
recusa nenhuma, ou so com a do status MODELO, a guarda TEM de falhar.
"""
from __future__ import annotations
import os
import sys
from unittest.mock import patch

import pytest
import yaml

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import estado_io  # noqa: E402
import test_usuario_novo as T  # noqa: E402


def _modelo():
    with open(os.path.join(AQUI, "estado.exemplo.yaml"), encoding="utf-8") as f:
        return yaml.safe_load(f)


@pytest.mark.parametrize("mutacao", ["nenhum_problema", "so_status"])
def test_guarda_rejeita_validador_sem_problemas_obrigatorios(mutacao):
    dados, _, avisos = estado_io.validar(_modelo())
    problemas = [] if mutacao == "nenhum_problema" else ["meta.status: MODELO"]
    with patch.object(estado_io, "validar", return_value=(dados, problemas, avisos)):
        with pytest.raises(AssertionError):
            T.test_o_modelo_nao_carrega_ate_alguem_preencher()


def test_controle_a_guarda_passa_com_o_validador_de_verdade():
    """Sem o controle, os mutantes acima passariam tambem com uma guarda que sempre falha."""
    T.test_o_modelo_nao_carrega_ate_alguem_preencher()


def test_o_contrato_do_validar_e_dados_problemas_avisos():
    """O contrato que o desempacotamento errado ignorava, medido: o segundo elemento e a lista
    de problemas, e o primeiro e o dicionario de dados."""
    dados, problemas, avisos = estado_io.validar(_modelo())
    assert isinstance(dados, dict) and isinstance(problemas, list) and isinstance(avisos, list)
    assert all(isinstance(p, str) for p in problemas)
