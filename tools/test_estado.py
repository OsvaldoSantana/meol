# -*- coding: utf-8 -*-
"""O docs/estado.md que o hook injeta: em dia, abaixo do teto, e sem inventar campo.

A guarda do CI e `test_o_estado_commitado_esta_em_dia`. As mutacoes provam que ela falha
quando deveria: pendencia nova sem regenerar, resposta apagada da fila, arquivo que
estoura o teto (CLAUDE.md 5-B.4).
"""
from __future__ import annotations

import json
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import estado as E  # noqa: E402

PEND = """# Pendencias

## P-44 · Regra sem campos

Texto.

---

## P-48 · Vies de sobrevivencia

**Classe:** `BLOQUEIA_O_SISTEMA`. **Dono:** Claude. **Gatilho:** antes de rodar o backtest. O
porque vem aqui.

---

## P-115 · O criterio do degrau

**Dono:** Osvaldo decide · **Gatilho:** antes de medir qualquer janela nova ·
**Classe:** `DECISAO_DE_DESENHO`

Corpo que cita **Dono:** outra pessoa, mais abaixo.

---

## ~~P-12~~ · Fechada e esquecida aqui — **FECHADA em 01/10/2026**

**Dono:** Claude · **Gatilho:** nenhum · **Classe:** `DECISAO_DE_DESENHO`

---

## Ao voltar ao desktop

## P-46 · Nao e pendencia, e roteiro
"""

FILA = """# A fila

## Respostas dele

`115a 63b`

## 1 · Criterio da serie · P-115

- **115a** — sim
- **115b** — nao

## 2 · Nivel ou tendencia · P-63

- **63a** — por metrica
- **63b** — hibrido

## 3 · Ja respondido no cabecalho · P-162 · **respondido em 27/09: 16b**

- **(a)** um

## 4 · Onde o motor roda · P-165

- **(A)** no aparelho
"""


def _por_codigo(texto):
    return {p["codigo"]: p for p in E.pendencias(texto)}


def test_campos_lidos_nos_dois_formatos_do_registro():
    ps = _por_codigo(PEND)
    assert ps["P-48"] == {"codigo": "P-48", "titulo": "Vies de sobrevivencia", "dono": "Claude",
                          "gatilho": "antes de rodar o backtest", "classe": "BLOQUEIA"}
    assert ps["P-115"]["dono"] == "Osvaldo decide"
    assert ps["P-115"]["gatilho"] == "antes de medir qualquer janela nova"
    assert ps["P-115"]["classe"] == "DESENHO"


def test_campo_ausente_sai_vazio_e_aparece_como_interrogacao():
    """P5: o gerador nao inventa dono para quem nao declarou."""
    assert _por_codigo(PEND)["P-44"]["dono"] == ""
    texto = E.gerar(PEND, FILA)
    assert "### sem classe (1)" in texto and "P-44 · Regra sem campos" in texto


def test_riscada_e_o_roteiro_do_desktop_ficam_de_fora():
    ps = _por_codigo(PEND)
    assert "~~P-12~~" not in ps and "P-12" not in ps
    assert "P-46" not in ps
    assert list(ps) == ["P-44", "P-48", "P-115"]


def test_fila_lista_so_o_bloco_sem_resposta():
    assert [f["bloco"] for f in E.fila_sem_resposta(FILA)] == ["4"]
    assert E.fila_sem_resposta(FILA)[0]["ref"] == "P-165"


def test_mutacao_apagar_a_resposta_devolve_o_bloco_para_a_fila():
    sem = FILA.replace("`115a 63b`", "`63b`")
    assert [f["bloco"] for f in E.fila_sem_resposta(sem)] == ["1", "4"]


def test_mutacao_pendencia_nova_sem_regenerar_reprova():
    antes = E.gerar(PEND, FILA)
    nova = PEND.replace("## Ao voltar ao desktop",
                        "## P-171 · Nova\n\n**Dono:** Claude · **Gatilho:** ja · "
                        "**Classe:** `BLOQUEIA_O_SISTEMA`\n\n---\n\n## Ao voltar ao desktop")
    depois = E.gerar(nova, FILA)
    assert "P-171 · Nova · Claude · ja" in depois
    assert E.problemas(depois, antes, 2.96) and not E.problemas(antes, antes, 2.96)


def test_mutacao_arquivo_acima_do_teto_reprova():
    grande = PEND.replace("## Ao voltar ao desktop", "".join(
        f"## P-{n} · Titulo {n}\n\n**Dono:** Claude · **Gatilho:** x · "
        "**Classe:** `DECISAO_DE_DESENHO`\n\n---\n\n" for n in range(300, 600))
        + "## Ao voltar ao desktop")
    texto = E.gerar(grande, FILA)
    erros = E.problemas(texto, texto, 2.96)
    assert any("teto" in e for e in erros), erros


def test_corte_marca_o_que_cortou():
    assert E._corta("curto", 10) == "curto"
    c = E._corta("uma frase bem mais longa que o limite", 15)
    assert c.endswith("…") and len(c) <= 15


@pytest.mark.repositorio
def test_o_estado_commitado_esta_em_dia(capsys):
    """A guarda do CI: PENDENCIAS.md ou a fila mudou e o docs/estado.md nao."""
    rc = E.main(["--conferir"])
    assert rc == 0, capsys.readouterr().err


@pytest.mark.repositorio
def test_o_hook_injeta_o_estado_e_o_modelo_padrao_e_sonnet():
    """Decisao de 02/10: sem o hook, a sessao volta a abrir o PENDENCIAS.md inteiro."""
    with open(os.path.join(E.RAIZ, ".claude", "settings.json"), encoding="utf-8") as f:
        cfg = json.load(f)
    comandos = [h["command"] for g in cfg["hooks"]["SessionStart"] for h in g["hooks"]]
    assert any("docs/estado.md" in c for c in comandos), comandos
    assert cfg.get("model") == "sonnet"
