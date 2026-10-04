# -*- coding: utf-8 -*-
"""O dominante e a tabela do veto da R3, sobre marcas SINTETICAS (nenhuma marca real aqui)."""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import codigos_visuais as V  # noqa: E402
import r3_dominante as R  # noqa: E402

LIVRO = V.ler_livro()


def _m(cat, fundo, matiz, fam, raio, unidade="app", situacao="classificada", **kw):
    r = dict.fromkeys(R.COLUNAS, "")
    r.update({"marca": "x", "categoria": cat, "situacao": situacao, "unidade": unidade,
              "fundo": fundo, "matiz": matiz, "familia_do_titulo": fam, "raio": raio,
              "densidade": "media", "botao": "cheio", "url": "https://x", "data": "2026-10-02",
              "sha256_captura": "a" * 64, "arquivo_wayback": "https://web.archive.org/web/x", **kw})
    return r


E_CODIGO = ("claro", "laranja", "serifa", "reto")   # a classificacao de E no pre-registro


def test_categoria_que_imita_e_veta_a_e_e_so_ela():
    linhas = [_m("consultoria_cvm", *E_CODIGO) for _ in range(3)]
    linhas += [_m("consultoria_cvm", "escuro", "azul", "sem_serifa", "grande") for _ in range(2)]
    t = R.tabela(linhas, LIVRO)
    c = t["consultoria_cvm"]
    assert c["n"] == 5 and c["dominantes"] == [E_CODIGO]
    assert c["imita"] == {"E": True, "C": False, "D": False}
    assert all(not v["dominantes"] for k, v in t.items() if k != "consultoria_cvm")


def test_menos_de_cinco_nao_tem_dominante_e_puladas_nao_contam():
    linhas = [_m("robo", *E_CODIGO) for _ in range(4)]
    linhas += [_m("robo", *E_CODIGO, situacao="pulada", motivo="nao_atende_pf")]
    assert R.tabela(linhas, LIVRO)["robo"]["dominantes"] == []


def test_sensibilidade_so_app():
    """ae-a: com os sites, a categoria tem dominante; so com as de app (n=3), nao."""
    linhas = [_m("planejador", *E_CODIGO, unidade="site") for _ in range(3)]
    linhas += [_m("planejador", *E_CODIGO) for _ in range(3)]
    c = R.tabela(linhas, LIVRO)["planejador"]
    assert c["imita"]["E"] and not c["imita_so_app"]["E"] and c["n_app"] == 3


def test_validacao_recusa_linha_sem_procedencia_ou_fora_do_livro():
    boa = _m("assessor", *E_CODIGO)
    ruins = [_m("fintech", *E_CODIGO), _m("assessor", *E_CODIGO, unidade="print"),
             _m("assessor", "claro", "dourado", "serifa", "reto"),
             _m("assessor", *E_CODIGO, sha256_captura=""),
             _m("assessor", *E_CODIGO, arquivo_wayback=""),
             _m("assessor", *E_CODIGO, situacao="pulada")]
    assert R.validar([boa], LIVRO) == []
    for r in ruins:
        assert R.validar([r], LIVRO) != [], r


def test_mutacao_dominante_sem_o_limite_de_cinco_dispararia_o_veto(monkeypatch):
    """Com n_minimo 1, quatro marcas imitando E vetariam: o limite e o que impede."""
    linhas = [_m("robo", *E_CODIGO) for _ in range(4)]
    assert not R.tabela(linhas, LIVRO)["robo"]["imita"]["E"]
    livro = {**LIVRO, "veto": {**LIVRO["veto"], "n_minimo_de_marcas": 1}}
    assert R.tabela(linhas, livro)["robo"]["imita"]["E"]


def test_csv_gravado_valido_e_veto_md_confere():
    assert R.validar(R.ler(), LIVRO) == []
    assert R.main(["--conferir"]) == 0


def test_arquivo_wayback_so_link_do_wayback_ou_pendente_declarado():
    """04/10: a nuvem nao alcanca o Wayback; a linha diz PENDENTE_LOCAL, e nada mais passa."""
    livro = V.ler_livro()
    ok = [_m("assessor", *E_CODIGO, arquivo_wayback="https://web.archive.org/web/2026/x"),
          _m("assessor", *E_CODIGO, arquivo_wayback=R.PENDENTE)]
    assert R.validar(ok, livro) == []
    ruim = [_m("assessor", *E_CODIGO, arquivo_wayback="arquivar depois")]
    assert R.validar(ruim, livro)
    assert "PENDENTE_LOCAL" in R.texto_veto(ok, livro)
