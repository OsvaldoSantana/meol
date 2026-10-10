# -*- coding: utf-8 -*-
"""CX-06: a guarda de politica fixa aceitava `7e+1` e `7_0`, e recusava `70.0`.

Achado externo (auditoria do Codex, 03/10/2026, `A-03` no original; registro em
`docs/auditoria/AUDITORIA-CODEX-2026-10-03.md`). `test_nenhum_literal_de_politica_fixo_no_modulo`
recortava o texto de `alocacao.py` no marcador `# ══ PORTOES ══` e procurava numeros por
regex. Tres escritas do mesmo 70 no lugar de `P["motor_aporte"]["k_max"]`: a guarda pegava uma.
E o padrao F-05: a guarda prometia "nenhuma constante de politica no Python" e media "nenhuma
constante escrita do jeito que a regex conhece".

As tres escritas e o controle viram testes permanentes. Cada fonte mutante e COMPILADA antes
de ir a guarda: a prova e sobre Python valido, nao sobre texto que nenhum interpretador leria.
"""
from __future__ import annotations
import io
import os
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import test_alocacao as T  # noqa: E402

ALVO = Path(AQUI) / "alocacao.py"
TRECHO = 'if k_max is None: k_max = P["motor_aporte"]["k_max"]'


def _guarda_sobre(fonte):
    """Roda a guarda de verdade com `fonte` no lugar de alocacao.py."""
    compile(fonte, str(ALVO), "exec")
    abrir = open

    def abrir_mutante(path, *args, **kwargs):
        return io.StringIO(fonte) if Path(path) == ALVO else abrir(path, *args, **kwargs)

    with patch("builtins.open", side_effect=abrir_mutante):
        T.test_nenhum_literal_de_politica_fixo_no_modulo()


@pytest.mark.repositorio   # 146b: le o fonte, que a mutacao instrumenta
@pytest.mark.parametrize("literal", ["70.0", "7e+1", "7_0"],
                         ids=["controle-70.0", "expoente-7e+1", "separador-7_0"])
def test_guarda_recusa_politica_fixa_em_notacoes_validas(literal):
    fonte = ALVO.read_text(encoding="utf-8")
    assert fonte.count(TRECHO) == 1, "o ponto de injecao mudou; a prova perdeu o alvo"
    with pytest.raises(AssertionError, match="literais numericos"):
        _guarda_sobre(fonte.replace(TRECHO, "if k_max is None: k_max = " + literal))


@pytest.mark.repositorio
def test_controle_a_guarda_passa_no_modulo_de_verdade():
    """Sem este, os tres acima passariam com uma guarda que reprova tudo."""
    _guarda_sobre(ALVO.read_text(encoding="utf-8"))


@pytest.mark.repositorio
def test_literal_antes_do_marcador_fica_fora_e_isso_esta_declarado():
    """O alcance (P5): o recorte e depois do marcador, como era. Um literal antes dele nao
    reprova -- o teste prende o alcance para que ele nao mude calado."""
    fonte = ALVO.read_text(encoding="utf-8")
    linha = next(x for x in fonte.splitlines() if x.startswith("# ══ PORTOES ══"))
    antes, depois = fonte.split(linha + "\n", 1)
    _guarda_sobre(antes + "_SEM_ALCANCE = 7e+1\n" + linha + "\n" + depois)
