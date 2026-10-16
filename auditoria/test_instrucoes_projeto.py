# -*- coding: utf-8 -*-
"""O changelog das instrucoes do Projeto no claude.ai (docs/ia/instrucoes-projeto-claude.md).

POR QUE EXISTE. Em 16/10/2026 a linha da ordem do degrau 4 entrou como versao "3", acima da 3 de
03/10, e o cabecalho dizia "Versao 3". Quem cola a copia no claude.ai confere pela versao: com
duas "3", nao ha como saber se a copia colada e a ultima. A guarda: numeros unicos, em sequencia
a partir de 1, na ordem do arquivo, e o cabecalho igual ao ultimo.

O QUE NAO VE (P5): se a copia no claude.ai foi de fato atualizada (isso e dele, fora do git).
"""
from __future__ import annotations

import os
import re

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARQ = os.path.join(RAIZ, "docs", "ia", "instrucoes-projeto-claude.md")


def versoes(texto):
    """(versao do cabecalho, [numeros das linhas do changelog na ordem do arquivo])."""
    cab = re.search(r"^\*Versão (\d+), ", texto, re.MULTILINE)
    linhas = [int(m.group(1)) for m in re.finditer(r"^\| (\d+) \| \d{2}/\d{2}/\d{4} \|", texto,
                                                     re.MULTILINE)]
    return (int(cab.group(1)) if cab else None), linhas


def problemas(texto):
    cab, linhas = versoes(texto)
    out = []
    if linhas != list(range(1, len(linhas) + 1)):
        out.append(f"changelog fora de sequencia: {linhas}")
    if not linhas or cab != linhas[-1]:
        out.append(f"cabecalho diz versao {cab}, o changelog termina em {linhas[-1:]}")
    return out


def test_o_changelog_das_instrucoes_e_uma_sequencia_e_o_cabecalho_e_o_ultimo():
    with open(ARQ, encoding="utf-8") as f:
        assert problemas(f.read()) == []


def test_mutacao_duas_linhas_3_e_o_cabecalho_velho_reprovam():
    """O estado de 16/10, antes do conserto, reprova nas duas pontas."""
    velho = ("*Versão 3, 16/10/2026.*\n\n| 1 | 26/09/2026 | a |\n| 2 | 27/09/2026 | b |\n"
             "| 3 | 16/10/2026 | d |\n| 3 | 03/10/2026 | c |\n")
    assert len(problemas(velho)) == 1                 # a sequencia [1, 2, 3, 3] reprova
    assert problemas(velho.replace("| 3 | 16/10", "| 4 | 16/10")) != []   # 4 antes da 3
    certo = ("*Versão 4, 16/10/2026.*\n\n| 1 | 26/09/2026 | a |\n| 2 | 27/09/2026 | b |\n"
             "| 3 | 03/10/2026 | c |\n| 4 | 16/10/2026 | d |\n")
    assert problemas(certo) == []
