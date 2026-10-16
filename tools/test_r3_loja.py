# -*- coding: utf-8 -*-
"""A rota da App Store da R3 (P-170): as funcoes puras. Nada aqui toca rede."""
from __future__ import annotations

import io
import os
import sys
import urllib.error

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import r3_loja as L  # noqa: E402


def test_dominio_base_tira_www_e_sufixo_publico():
    assert L.dominio_base("https://www.sofisa.com.br/") == "sofisa"
    assert L.dominio_base("https://wealth.highpar.com.br/x?y=1") == "highpar"
    assert L.dominio_base("http://www.xpi.com.br") == "xpi"
    assert L.dominio_base("https://www.morganstanley.com.br/") == "morganstanley"
    assert L.dominio_base("https://brei.com.br/") == "brei"
    assert L.dominio_base("caixa.gov.br") == "caixa"
    assert L.dominio_base("https://www.bancointer.com/") == "bancointer"


def test_termos_na_ordem_do_plano_sem_repetir():
    assert L.termos_da_linha("Banco Sofisa", "https://www.sofisa.com.br/") == ["Banco Sofisa",
                                                                              "sofisa"]
    assert L.termos_da_linha("Sofisa", "https://www.sofisa.com.br/") == ["Sofisa"]
    assert L.termos_da_linha("BREI", "") == ["BREI"]


def test_url_busca_preenche_o_modelo_do_plano():
    plano = L.ler_plano()["loja"]
    u = L.url_busca(plano["busca"], "Mercado Pago", plano["limite"])
    assert u.startswith("https://itunes.apple.com/search?term=Mercado+Pago&country=br")
    assert "entity=software" in u and "limit=15" in u


class _Relogio:
    def __init__(self):
        self.t = 0.0
        self.dormiu: list[float] = []

    def agora(self):
        return self.t

    def dormir(self, s):
        self.dormiu.append(s)
        self.t += s


def _403():
    return urllib.error.HTTPError("u", 403, "Forbidden", {}, io.BytesIO(b""))


def test_espacador_respeita_o_intervalo_minimo():
    r = _Relogio()
    e = L.Espacador(4, [30], dormir=r.dormir, relogio=r.agora)
    assert e.consultar(lambda: 1) == 1
    r.t += 1.5                       # a consulta seguinte vem 1,5 s depois
    e.consultar(lambda: 2)
    assert r.dormiu == [pytest.approx(2.5)]


def test_espacador_espera_crescente_no_403_e_depois_responde():
    r = _Relogio()
    e = L.Espacador(4, [30, 60, 120], dormir=r.dormir, relogio=r.agora)
    falhas = iter([_403(), _403()])

    def fazer():
        f = next(falhas, None)
        if f:
            raise f
        return "ok"
    assert e.consultar(fazer) == "ok"
    assert e.n_403 == 2
    assert [d for d in r.dormiu if d >= 30] == [30, 60]


def test_espacador_esgotado_o_403_sobe_e_nunca_vira_sem_app():
    """A mutacao do 5-B.16: com a lista de esperas acabada, a busca falha alto."""
    r = _Relogio()
    e = L.Espacador(4, [30, 60], dormir=r.dormir, relogio=r.agora)

    def sempre_403():
        raise _403()
    with pytest.raises(urllib.error.HTTPError):
        e.consultar(sempre_403)
    assert e.n_403 == 2


def test_espacador_outro_erro_http_nao_espera():
    r = _Relogio()
    e = L.Espacador(4, [30], dormir=r.dormir, relogio=r.agora)

    def erro_500():
        raise urllib.error.HTTPError("u", 500, "x", {}, io.BytesIO(b""))
    with pytest.raises(urllib.error.HTTPError):
        e.consultar(erro_500)
    assert r.dormiu == []


def test_pendentes_so_aguarda_e_na_ordem_do_sorteio():
    linhas = [
        {"categoria_sorteada": "bancos", "ordem_no_sorteio": "12", "motivo": "x AGUARDA DEGRAU 4"},
        {"categoria_sorteada": "bancos", "ordem_no_sorteio": "5", "motivo": "AGUARDA DEGRAU 4"},
        {"categoria_sorteada": "bancos", "ordem_no_sorteio": "7", "motivo": "sem_marca: x"},
        {"categoria_sorteada": "assessor", "ordem_no_sorteio": "9", "motivo": "AGUARDA DEGRAU 4"},
    ]
    assert [(r["categoria_sorteada"], r["ordem_no_sorteio"]) for r in L.pendentes(linhas)] == [
        ("assessor", "9"), ("bancos", "5"), ("bancos", "12")]
    assert [r["ordem_no_sorteio"] for r in L.pendentes(linhas, ["bancos:12"])] == ["12"]


def _entrada(i, nome, vendedor="V", resumo="r"):
    return {"id": {"attributes": {"im:id": str(i)}}, "im:name": {"label": nome},
            "im:artist": {"label": vendedor}, "summary": {"label": resumo}}


def test_entradas_do_quadro_e_quadro_de_um_app_so():
    dados = {"feed": {"entry": [_entrada(10, "A"), _entrada(20, "B")]}}
    e = L.entradas_do_quadro(dados)
    assert [(x["posicao"], x["trackId"], x["nome"]) for x in e] == [(1, 10, "A"), (2, 20, "B")]
    assert len(L.entradas_do_quadro({"feed": {"entry": _entrada(30, "C")}})) == 1
    assert L.entradas_do_quadro({"feed": {}}) == []


def test_uniao_um_app_uma_vez_na_ordem_dos_quadros():
    q = {"topfree": [{"trackId": 1}, {"trackId": 2}],
         "topgrossing": [{"trackId": 2}, {"trackId": 3}],
         "toppaid": [{"trackId": 4}]}
    u = L.uniao_dos_quadros(q, ["topfree", "topgrossing", "toppaid"])
    assert [(x["trackId"], x["quadro"]) for x in u] == [
        (1, "topfree"), (2, "topfree"), (3, "topgrossing"), (4, "toppaid")]


def test_o_plano_v3_traz_o_que_o_script_le():
    p = L.ler_plano()
    assert p["versao"] >= 3
    assert p["loja"]["intervalo_minimo_s"] >= 4
    assert p["loja"]["espera_no_403_s"] == sorted(p["loja"]["espera_no_403_s"])
    assert set(p["universos_da_loja"]["quadros"]) == {"topfree", "topgrossing", "toppaid"}
    assert set(p["universos_da_loja"]["categorias"]) == {"robo", "consolidador"}
