# -*- coding: utf-8 -*-
"""O questionario do teste de marca como DADO (P-162, P2): a versao de leitura sai do YAML, a
duracao e a posicao nunca sao literais, e os textos decididos por ele estao la como decididos."""
from __future__ import annotations

import itertools
import os
import sys

import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import questionario_teste_marca as QT  # noqa: E402

Q = QT.ler()


def test_versao_de_leitura_confere_com_o_yaml():
    assert QT.conferir(Q)


def test_mutacao_md_editado_a_mao_reprova(tmp_path):
    md = tmp_path / "questionario.md"
    md.write_text(QT.gerar(Q).replace("5 segundos", "10 segundos"), encoding="utf-8")
    assert not QT.conferir(Q, str(md))


def test_duracao_e_total_nunca_sao_literais_nos_textos():
    """A duracao e um campo (telas.exposicao_segundos); os textos usam {segundos} e {n}."""
    t = Q["telas"]
    assert isinstance(t["exposicao_segundos"], int) and t["exposicao_segundos"] > 0
    for chave in ("instrucao", "instrucao_curta"):
        assert "{segundos}" in t[chave] and "{n}" in t[chave]
        assert str(t["exposicao_segundos"]) not in t[chave]
        assert str(t["quantidade"]) not in t[chave]
    mudado = {**Q, "telas": {**t, "exposicao_segundos": 7}}
    assert "7 segundos" in QT.gerar(mudado) and "5 segundos" not in QT.gerar(mudado)


def test_as_seis_ordens_sao_as_seis_permutacoes_de_e_c_d():
    versoes = Q["ordens"]["versoes"]
    assert sorted(versoes) == [1, 2, 3, 4, 5, 6]
    assert sorted(tuple(v) for v in versoes.values()) == sorted(itertools.permutations("ECD"))
    assert "mod 6" in Q["ordens"]["atribuicao"] and "aberturas" in Q["ordens"]["atribuicao"]


def test_textos_decididos_por_ele():
    """y-b (27/09): filtro e amigos com o texto de 20/09; w-a e x-a nas escalas."""
    assert Q["filtro"]["texto"] == ("Voc\u00ea aporta todo m\u00eas em renda vari\u00e1vel "
                                    "h\u00e1 pelo menos 6 meses?")
    assert Q["amigo"]["texto"] == "Voc\u00ea conhece quem criou este app?"
    polos = {e["id"]: (e["polo_1"], e["polo_7"]) for e in Q["telas"]["escalas"]}
    assert polos == {
        "seguro": ("Inseguran\u00e7a", "Seguran\u00e7a"),
        "para_mim": ("N\u00e3o \u00e9 para mim", "\u00c9 para mim"),
        "honesto": ("Quer me vender algo", "Honesta"),
        "confiavel": ("Parece golpe", "Confi\u00e1vel"),
        "luxo": ("Popular", "De luxo"),
    }


def test_escala_e_de_1_a_7_e_obrigatoria():
    t = Q["telas"]
    assert (t["escala_min"], t["escala_max"], t["escalas_obrigatorias"]) == (1, 7, True)


def test_estimulos_sao_os_seis_png_aprovados():
    est = Q["telas"]["estimulos"]
    assert set(est) == {"E", "C", "D"}
    for d, par in est.items():
        assert par == {"base": f"docs/marca/direcoes/png/{d}-base.png",
                       "rota": f"docs/marca/direcoes/png/{d}-rota-bloqueada.png"}
        assert all(os.path.isfile(os.path.join(QT.RAIZ, p)) for p in par.values())


def test_contrato_de_privacidade_e_de_datas_sem_hora():
    assert any("navegador nunca chama o Supabase" in r for r in Q["privacidade"])
    assert "sem hora" in QT.gerar(Q)
    assert Q["janela"] == {"dias": 21, "fuso": "America/Sao_Paulo",
                           "instante_que_conta": "concluida_em"}


def test_yaml_em_ascii_e_valido():
    with open(QT.YAML, "rb") as f:
        bruto = f.read()
    assert all(b < 128 for b in bruto)
    assert yaml.safe_load(bruto)["versao"] == 2
