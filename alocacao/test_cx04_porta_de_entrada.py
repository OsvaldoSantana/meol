# -*- coding: utf-8 -*-
"""CX-04: a porta de entrada aceitava NaN, infinito e booleano como dinheiro.

Achado externo (auditoria do Codex, 03/10/2026, `docs/auditoria/AUDITORIA-CODEX-2026-10-03.md`,
la como A-01 do original). `_num()` testava `isinstance(v, (int, float))`, e `bool` e subclasse
de `int`: `despesa_mensal: true` virava R$ 1,00. `float("nan")` e `float("inf")` passavam por
`float(s)`. E `posicoes` e `dependentes` nem passavam por `_num()`.

O YAML 1.1, que o PyYAML implementa, le `yes`, `no`, `on` e `off` sem aspas como booleano:
`caixa: no` (de "nao tenho") chega ao motor como `False`, isto e, zero. Por isso as grafias
entram aqui escritas como TEXTO de YAML, e nao como `True` do Python -- a prova tem de passar
pelo carregador que a pessoa usa.

O que este arquivo NAO cobre (P5): intervalos economicos (despesa negativa, taxa de 900% ao
mes), rota desconhecida em `posicoes`, e campos que o `validar()` nao le.
"""
from __future__ import annotations
import copy
import dataclasses
import os
import sys
import typing
from pathlib import Path

import pytest
import yaml

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import estado_io  # noqa: E402
from alocacao import Divida, MatchEmpregador, Objetivo  # noqa: E402

MODELO = Path(AQUI) / "estado.exemplo.yaml"


def _base():
    """Um estado sintetico VALIDO, com todo campo numerico preenchido: o controle. Nenhum
    numero de ninguem (D-01)."""
    d = yaml.safe_load(MODELO.read_text(encoding="utf-8"))
    d.update(
        despesa_mensal=3000, estabilidade_renda="media", horizonte_anos=30, aporte_mensal=500,
        dependentes=1, caixa=10.0, reserva_atual=900.0, reserva_disponivel=900.0,
        reserva_empenhada=0.0, reserva_por_rota={"td_selic": 900.0},
        posicoes={"bova11": 100.0},
        dividas=[{"nome": "cartao", "saldo": 1000.0, "taxa_am": 0.02}],
        objetivos=[{"nome": "carro", "valor": 30000.0, "prazo_anos": 3}],
        match_empregador={"taxa": 0.5, "teto_pct_salario": 0.08,
                          "salario_bruto_mensal": 8000.0},
        match_verificado=True)
    d["meta"]["status"] = "REAL"
    d["meta"]["preenchido_em"] = "2026-10-04"
    return d


def _numericos(classe):
    return [f.name for f in dataclasses.fields(classe)
            if typing.get_type_hints(classe)[f.name] is not str]


# Todo campo numerico que o validar() le, com o caminho no dicionario e o rotulo que a
# mensagem tem de nomear. As listas de dataclass saem da propria classe: campo numerico novo
# em Divida entra aqui sem ninguem lembrar.
CAMPOS = (
    [((c,), c) for c in estado_io.NUMERICOS]
    + [(("reserva_disponivel",), "reserva_disponivel"),
       (("reserva_empenhada",), "reserva_empenhada"),
       (("dependentes",), "dependentes"),
       (("reserva_por_rota", "td_selic"), "reserva_por_rota.td_selic"),
       (("posicoes", "bova11"), "posicoes.bova11")]
    + [(("dividas", 0, f), f"dividas[0].{f}") for f in _numericos(Divida)]
    + [(("objetivos", 0, f), f"objetivos[0].{f}") for f in _numericos(Objetivo)]
    + [(("match_empregador", f), f"match_empregador.{f}") for f in _numericos(MatchEmpregador)]
)
IDS = [rot for _, rot in CAMPOS]


def _pondo(d, caminho, valor):
    d = copy.deepcopy(d)
    alvo = d
    for k in caminho[:-1]:
        alvo = alvo[k]
    alvo[caminho[-1]] = valor
    return d


def _pelo_yaml(caminho, grafia):
    """O estado com `grafia` escrita CRUA no YAML, no lugar do campo, e lido de volta pelo
    mesmo `safe_load` do `carregar()`."""
    texto = yaml.safe_dump(_pondo(_base(), caminho, "MARCADOR_CX04"), allow_unicode=True)
    assert texto.count("MARCADOR_CX04") == 1
    return yaml.safe_load(texto.replace("MARCADOR_CX04", grafia))


def test_controle_o_estado_sintetico_e_valido():
    """Sem isto, toda recusa abaixo podia vir de outro campo."""
    _d, problemas, _avisos = estado_io.validar(_base())
    assert problemas == []


# ── As provas da auditoria (secao 9.9), como chegaram ─────────────────────────────────────
@pytest.mark.parametrize("campo, valor", [("aporte_mensal", float("nan")),
                                          ("caixa", float("inf")),
                                          ("despesa_mensal", True)])
def test_carregar_recusa_numero_invalido(tmp_path, campo, valor):
    modelo = yaml.safe_load(MODELO.read_text(encoding="utf-8"))
    modelo.update(despesa_mensal=3000, estabilidade_renda="media", horizonte_anos=30,
                  aporte_mensal=500)
    modelo["meta"]["status"] = "REAL"
    modelo[campo] = valor
    arquivo = tmp_path / "sintetico.yaml"
    arquivo.write_text(yaml.safe_dump(modelo), encoding="utf-8")
    with pytest.raises(estado_io.EstadoInvalido, match=campo):
        estado_io.carregar(path=str(arquivo))


# ── A ampliacao: todo campo, todo valor que nao e numero finito ─────────────────────────────
@pytest.mark.parametrize("valor", [float("nan"), float("inf"), float("-inf"), True, False,
                                   "nan", "inf", "-Infinity"],
                         ids=["nan", "inf", "-inf", "True", "False", "'nan'", "'inf'",
                              "'-Infinity'"])
@pytest.mark.parametrize("caminho, rotulo", CAMPOS, ids=IDS)
def test_todo_campo_numerico_recusa_o_que_nao_e_numero_finito(caminho, rotulo, valor):
    _d, problemas, _ = estado_io.validar(_pondo(_base(), caminho, valor))
    assert any(p.startswith(rotulo + ":") for p in problemas), (
        f"{rotulo} = {valor!r} passou pela porta de entrada. Problemas: {problemas}")


@pytest.mark.parametrize("grafia", ["yes", "no", "on", "off", "Yes", "OFF", "true", ".nan",
                                    ".inf", "-.inf"])
@pytest.mark.parametrize("caminho, rotulo", CAMPOS, ids=IDS)
def test_as_grafias_que_o_yaml_le_como_booleano_ou_nao_finito(caminho, rotulo, grafia):
    d = _pelo_yaml(caminho, grafia)
    _d, problemas, _ = estado_io.validar(d)
    assert any(p.startswith(rotulo + ":") for p in problemas), (
        f"{rotulo}: {grafia} (YAML) passou pela porta de entrada. Problemas: {problemas}")


def test_a_mensagem_do_booleano_diz_por_que():
    """Quem escreveu `caixa: no` nao escreveu um booleano. A mensagem tem de dizer o que o YAML
    fez com o texto, senao a correcao vira adivinhacao."""
    _d, problemas, _ = estado_io.validar(_pelo_yaml(("caixa",), "no"))
    msg = next(p for p in problemas if p.startswith("caixa:"))
    assert "yes/no/on/off" in msg and "numero" in msg


def test_o_yaml_le_mesmo_estas_grafias_como_booleano():
    """A premissa dos testes acima, medida e nao lembrada: se o PyYAML mudar, eles perdem o
    sentido em silencio."""
    for g in ("yes", "no", "on", "off", "Yes", "OFF"):
        assert isinstance(yaml.safe_load(f"x: {g}")["x"], bool), g


def test_o_que_era_valido_continua_valido_e_com_o_mesmo_tipo():
    """O conserto nao pode mudar o que a porta devolvia para entrada boa: `dependentes` e
    `int` no Estado, e os valores de `posicoes` saem iguais."""
    d, problemas, _ = estado_io.validar(_base())
    assert problemas == []
    assert d["dependentes"] == 1 and type(d["dependentes"]) is int
    assert d["posicoes"] == {"bova11": 100.0}
    d2, _, _ = estado_io.validar(_pondo(_base(), ("dependentes",), None))
    assert d2["dependentes"] == 0, "ausente continua sendo zero dependentes"


def test_cobertura_todo_campo_numerico_do_modelo_esta_em_CAMPOS():
    """Campo numerico novo no `estado.exemplo.yaml` sem prova aqui reprova. Os nao numericos
    estao listados com o motivo."""
    nao_numericos = {"meta": "metadado", "estabilidade_renda": "texto",
                     "match_verificado": "booleano de verdade",
                     "dividas": "lista; campos via Divida", "objetivos": "lista; via Objetivo",
                     "match_empregador": "mapa; via MatchEmpregador",
                     "reserva_por_rota": "mapa; valores cobertos", "posicoes": "idem"}
    modelo = yaml.safe_load(MODELO.read_text(encoding="utf-8"))
    cobertos = {c[0] for c, _ in CAMPOS}
    faltam = set(modelo) - set(nao_numericos) - cobertos
    assert not faltam, f"campo(s) do modelo sem prova de porta de entrada: {sorted(faltam)}"
