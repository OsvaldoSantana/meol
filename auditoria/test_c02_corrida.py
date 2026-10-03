# -*- coding: utf-8 -*-
"""A corrida do C-02 (auditoria/c02_corrida.py), so com dado SINTETICO de resposta conhecida.

Nenhum preco real de 2013-2020 e lido aqui (secao 9, quarentena). O gerador monta precos e
eventos e os passa pelas MESMAS funcoes do ajustar.py (fatores, ajustar_tudo, degraus): o que
muda entre os cenarios e so quanto o preco cai no dia ex por real pago (k).

  k = 1    queda igual ao bruto    -> PASSA na janela
  k = 0,85 queda igual ao liquido  -> K2 REPROVA (IC cruza a borda, sigma <= sigma_max)
  k = 0    sem queda               -> K2 e K3 REPROVA (IC disjunto, E-K1)

Cada criterio tem a sua prova por mutacao: a versao errada do criterio e montada no teste e
da outra resposta no mesmo dado.
"""
from __future__ import annotations

import collections
import datetime as dt
import json
import os
import subprocess
import sys
from decimal import Decimal

import numpy as np
import pytest

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import c02_corrida as C  # noqa: E402

ajustar = C.ajustar
M = collections.namedtuple("M", "acervo casados fat ajustadas degraus")
ANOS = range(2016, 2021)


def fabricar(k_jcp=1.0, k_div=1.0, semente=7, ruido=0.002, crash_no_desdobramento=False):
    """Uma medicao sintetica de 2016-2020: 40 papeis, 60 pregoes por ano, 16 JCP, 16
    dividendos e 3 desdobramentos (fator 0,5) por ano. No dia ex de um provento de valor v,
    o preco cai k*v; o ajuste usa sempre o fator do bruto, (P - v) / P."""
    rng = np.random.default_rng(semente)
    tks = ["T%02d3" % i for i in range(40)]
    datas = [dt.date(a, 1, 2) + dt.timedelta(days=5 * i) for a in ANOS for i in range(60)]
    merc = rng.normal(0, 0.01, len(datas))
    ev = {}
    for a in range(5):
        base = a * 60
        for j in range(8):                           # JCP em 8 pregoes, 2 papeis cada
            for t in (j % 20, j % 20 + 20):
                ev[(tks[t], base + 5 + 6 * j)] = ("JRS CAP PROPRIO", rng.uniform(0.01, 0.03))
        for j in range(8):                           # dividendo em outros 8 pregoes
            for t in ((j + 7) % 20, (j + 7) % 20 + 20):
                ev[(tks[t], base + 8 + 6 * j)] = ("DIVIDENDO", rng.uniform(0.01, 0.03))
        for j in range(3):                           # 3 desdobramentos por ano
            d = base + 20 + 7 * j
            ev[(tks[30 + j], d)] = ("DESDOBRAMENTO", 0.5)
            if crash_no_desdobramento and j == 0:
                merc[d] = -0.20
    precos = {}
    casados = []
    for t, tk in enumerate(tks):
        p = Decimal(str(round(rng.uniform(20, 50), 2)))
        s = {}
        for i, d in enumerate(datas):
            mov = Decimal(str(round(1 + merc[i] + rng.normal(0, ruido), 8)))
            e = ev.get((tk, i))
            if i and e:
                tipo, x = e
                if tipo == "DESDOBRAMENTO":
                    f = Decimal("0.5")
                    novo = p * f * mov
                    v = None
                else:
                    k = k_jcp if tipo == "JRS CAP PROPRIO" else k_div
                    v = (p * Decimal(str(round(x, 6)))).quantize(Decimal("0.000001"))
                    f = (p - v) / p
                    novo = (p - Decimal(str(k)) * v) * mov
                casados.append(dict(_ticker=tk, data_ex=d.isoformat(), tipo=tipo,
                                    data_ex_status=ajustar.DERIVADA, fator_status=ajustar.CALCULADO,
                                    fator=format(f, "f"), valor="" if v is None else format(v, "f"),
                                    preco_vespera=format(p, "f"), _origem_preco="B3"))
                p = novo
            elif i:
                p = p * mov
            p = p.quantize(Decimal("0.000001"))
            s[d] = p
        precos[tk] = s
    acervo = ajustar.Acervo(precos, {tk: {} for tk in tks}, {}, {}, {})
    fat = ajustar.fatores(casados)
    aj = ajustar.ajustar_tudo(acervo, fat)
    return M(acervo, casados, fat, aj, ajustar.degraus(acervo, aj, fat, casados))


@pytest.fixture(scope="module")
def C_():
    return C.custos()


@pytest.fixture(scope="module")
def evs():
    return C.ler_d1()


@pytest.fixture(scope="module")
def bruto(C_, evs):
    m = fabricar(1.0, 1.0)
    return m, C.julgar(m, evs, C_)


# ───────────────────────────────────────────────────── as tres respostas conhecidas

def test_queda_igual_ao_bruto_passa_a_janela(bruto):
    _m, r = bruto
    assert abs(r["K2"]["razao"] - 1) < 0.02 and abs(r["K3"]["razao"] - 1) < 0.02
    assert (r["K2"]["veredito"], r["K3"]["veredito"]) == (C.PASSA, C.PASSA)
    assert r["K2"]["n"] == 80 and r["K2"]["pregoes"] == 40      # 16 por ano, 8 pregoes por ano
    assert set(r["anos"].values()) == {C.PASSA}
    assert r["K5_janela"] == dict(n=15, minimo=10, veredito=C.PASSA)
    assert r["K6"]["veredito"] == C.PASSA
    assert r["veredito"] == C.PASSA


def test_queda_igual_ao_liquido_reprova_o_k2(C_, evs):
    r = C.julgar(fabricar(0.85, 1.0), evs, C_)
    k2 = r["K2"]
    assert abs(k2["razao"] - 0.85) < 0.02
    assert k2["lo"] < 0.85 < k2["hi"] and k2["sigma"] <= 0.0416      # cruza a borda inferior
    assert k2["veredito"] == C.REPROVA and r["K3"]["veredito"] == C.PASSA
    assert r["veredito"] == C.REPROVA


def test_sem_queda_reprova_k2_e_k3_por_ic_disjunto(C_, evs):
    r = C.julgar(fabricar(0.0, 0.0), evs, C_)
    for k in ("K2", "K3"):
        assert abs(r[k]["razao"]) < 0.05 and r[k]["hi"] < 0.85
        assert r[k]["veredito"] == C.REPROVA
    # Secao 4.3: CRITERIO_SEM_PODER ganha de tudo. Sem queda (k = 0), a M5 (provento
    # ignorado) da razao 1 - c + k = 1 e cabe na faixa: ignorar o provento VIRA o ajuste
    # certo, e o K6 nao tem como reprova-la. O poder do K6 depende de o mercado cair.
    assert not r["K6"]["M5"]["reprovou"] and r["K6"]["M5"]["K2"] == C.PASSA
    assert r["veredito"] == C.SEM_PODER


# ─────────────────────────────────────────────── E-K1: o veredito de K2/K3, e a mutacao

F = C.FAIXAS["K2"]


@pytest.mark.parametrize("b, esperado", [
    (dict(n=29, pregoes=25, lo=0.9, hi=1.1, sigma=0.01), C.NAO_CONFIRMADO),   # n < 30
    (dict(n=40, pregoes=19, lo=0.9, hi=1.1, sigma=0.01), C.NAO_CONFIRMADO),   # pregoes < 20
    (dict(n=40, pregoes=25, lo=0.85, hi=1.15, sigma=0.05), C.PASSA),          # bordas fechadas
    (dict(n=40, pregoes=25, lo=1.6, hi=2.4, sigma=0.20), C.REPROVA),          # disjunto, sigma alto
    (dict(n=40, pregoes=25, lo=0.80, hi=0.90, sigma=0.03), C.REPROVA),        # cruza, sigma <= max
    (dict(n=40, pregoes=25, lo=0.80, hi=0.90, sigma=0.05), C.NAO_CONFIRMADO), # cruza, sigma > max
])
def test_veredito_e_k1(b, esperado):
    assert C.veredito_razao(b, F) == esperado


def _literal(b, f):
    """A secao 4.1 ao pe da letra, antes da E-K1: IC fora e sigma > max e sempre sem poder."""
    if b["n"] < C.N_MIN_PONTOS or b["pregoes"] < C.N_MIN_PREGOES:
        return C.NAO_CONFIRMADO
    if b["lo"] >= f.inferior and b["hi"] <= f.superior:
        return C.PASSA
    return C.REPROVA if b["sigma"] <= f.sigma_max else C.NAO_CONFIRMADO


def test_mutacao_a_leitura_literal_faz_o_k6_falhar_por_construcao(bruto, evs, C_, monkeypatch):
    """A razao da E-K1: com a regra literal, a M3 (sigma enorme) vira NAO_CONFIRMADO e o K6
    falha no MESMO dado em que, com a E-K1, ele passa."""
    m, r = bruto
    assert r["K6"]["M3"]["reprovou"]
    monkeypatch.setattr(C, "veredito_razao", _literal)
    k6 = C.k6(m, evs, C_)
    assert k6["M3"]["K2"] == C.NAO_CONFIRMADO and k6["veredito"] == C.REPROVA


# ───────────────────────────────────────────────────────── o bootstrap por pregao

def _pts(semente=3, n_datas=30, por_data=4, comum=0.02):
    rng = np.random.default_rng(semente)
    fora = []
    for i in range(n_datas):
        d = dt.date(2017, 1, 1) + dt.timedelta(days=i)
        choque = rng.normal(0, comum)               # comum a todos os pontos da data
        for _ in range(por_data):
            y = rng.uniform(0.01, 0.03)
            fora.append((d, choque + rng.normal(0, 0.002), y))
    return fora


def test_bootstrap_reproduz_e_nao_depende_da_ordem():
    p = _pts()
    a = C.bootstrap_por_pregao(p)
    b = C.bootstrap_por_pregao(list(reversed(p)))
    assert a == b and a["pregoes"] == 30 and a["n"] == 120


def test_bootstrap_dourado_prende_a_semente_e_o_procedimento():
    """Instantaneo dourado: semente 20260926, 2.000 reamostras, percentil linear e ddof=1. Uma
    semente trocada, outro gerador ou outro percentil mudam estes numeros."""
    b = C.bootstrap_por_pregao(_pts())
    assert (C.SEMENTE, C.REAMOSTRAS) == (20260926, 2000)
    assert b["razao"] == pytest.approx(0.7839631329108457, abs=1e-12)
    assert b["lo"] == pytest.approx(0.4028742636329373, abs=1e-12)
    assert b["hi"] == pytest.approx(1.1149616405918832, abs=1e-12)
    assert b["sigma"] == pytest.approx(0.18147664289484816, abs=1e-12)


def test_bootstrap_e_a_concatenacao_dos_pontos_das_datas_sorteadas():
    """Somar k vezes os totais de uma data = concatenar k vezes os pontos dela (secao 3.1)."""
    p = _pts()
    b = C.bootstrap_por_pregao(p, reamostras=50)
    datas = sorted({d for d, _e, _y in p})
    rng = np.random.default_rng(C.SEMENTE)
    rs = []
    for _ in range(50):
        sel = [datas[i] for i in C.p88.indices(rng, len(datas), 1)]
        rs.append(C.razao([q for d in sel for q in p if q[0] == d]))
    assert b["lo"] == pytest.approx(np.percentile(rs, 2.5), abs=1e-12)
    assert b["sigma"] == pytest.approx(np.std(rs, ddof=1), abs=1e-12)


def test_mutacao_reamostrar_o_ponto_estreita_o_ic_quando_o_choque_e_da_data():
    """O motivo da secao 3.1: com choque comum na data, o bootstrap por ponto trata como
    independentes residuos que nao sao, e o sigma sai menor."""
    p = _pts()
    por_pregao = C.bootstrap_por_pregao(p)["sigma"]
    rng = np.random.default_rng(C.SEMENTE)
    rs = [C.razao([p[i] for i in rng.integers(0, len(p), len(p))]) for _ in range(2000)]
    assert por_pregao > 1.5 * float(np.std(rs, ddof=1))


# ─────────────────────────────────────────────────────────────── K1 relativo

def _acervo(precos):
    return ajustar.Acervo(precos, {}, {}, {}, {})


def test_k1_passa_com_o_ajuste_certo(bruto):
    m, r = bruto
    assert all(v["veredito"] == C.PASSA and v["pares"] > 0 for v in r["K1"].values())


def test_mutacao_k1_pega_o_ajuste_que_mexe_onde_nao_ha_evento():
    d = [dt.date(2017, 1, 2), dt.date(2017, 1, 3), dt.date(2017, 1, 4)]
    s = {d[0]: Decimal(10), d[1]: Decimal(11), d[2]: Decimal(12)}
    certo = {"X": {x: (v * Decimal(2), 2) for x, v in s.items()}}
    errado = {"X": {**certo["X"], d[2]: (Decimal(12) * Decimal("2.0001"), 2)}}
    assert C.k1_por_ano(_acervo({"X": s}), certo, {})[2017]["veredito"] == C.PASSA
    assert C.k1_por_ano(_acervo({"X": s}), errado, {})[2017]["veredito"] == C.REPROVA


def test_mutacao_k1_e_relativo_e_nao_absoluto():
    """Secao 4.2: o relativo. Num retorno de 1/1000, um desvio de 5e-12 relativo e 5e-15
    absoluto: o absoluto passaria, o relativo reprova."""
    d0, d1 = dt.date(2017, 1, 2), dt.date(2017, 1, 3)
    s = {d0: Decimal(1000), d1: Decimal(1)}
    aj = {"X": {d0: (Decimal(1000), 1), d1: (Decimal(1) * (1 + Decimal("5e-12")), 1)}}
    r = C.k1_por_ano(_acervo({"X": s}), aj, {})[2017]
    assert r["veredito"] == C.REPROVA
    absoluto = abs(float(aj["X"][d1][0] / aj["X"][d0][0] - s[d1] / s[d0]))
    assert absoluto <= C.K1_TOLERANCIA                     # a versao absoluta passaria


# ──────────────────────────────────────────────────────────────────────── K5

Gq = collections.namedtuple("Gq", "ticker data_ex tipos fator")


def _ln(ano, excesso, fator=0.5, i=0):
    g = Gq("Q%d" % i, dt.date(ano, 3, 1) + dt.timedelta(days=i), "DESDOBRAMENTO",
           Decimal(str(fator)))
    return C.Linha(g, C.QUANTIDADE, g.data_ex, excesso, 0.5)


def test_k5_um_fora_passa_dois_reprovam_sem_evento_nao_aplica():
    ls = ([_ln(2016, 0.01, i=i) for i in range(3)] + [_ln(2017, 0.30), _ln(2017, 0.0, i=1)]
          + [_ln(2018, 0.30), _ln(2018, -0.40, i=1)])
    k5 = C.k5_por_ano(ls)
    assert [k5[a]["veredito"] for a in ANOS] == [C.PASSA, C.PASSA, C.REPROVA, C.NAO_APLICA,
                                                  C.NAO_APLICA]
    assert k5[2018]["fora"][0]["ticker"] == "Q0"           # sai listado
    assert C.k5_janela(k5)["veredito"] == C.NAO_CONFIRMADO  # 7 < 10


def test_k5_borda_de_15_por_cento():
    """+-15% fechado: 0,15 fica dentro, 0,16 fica fora (secao 4.2)."""
    k5 = C.k5_por_ano([_ln(2016, 0.15), _ln(2016, -0.15, i=1),
                       _ln(2017, 0.16), _ln(2017, -0.16, i=1)])
    assert (k5[2016]["veredito"], k5[2017]["veredito"]) == (C.PASSA, C.REPROVA)


def test_k5_so_julga_quantidade_grande():
    assert not C.grande(Gq("A", dt.date(2017, 1, 1), "DESDOBRAMENTO", Decimal("0.8")))
    assert C.grande(Gq("A", dt.date(2017, 1, 1), "GRUPAMENTO", Decimal("1.5")))
    assert C.grande(Gq("A", dt.date(2017, 1, 1), "BONIFICACAO", Decimal("0.67")))
    assert not C.grande(Gq("A", dt.date(2017, 1, 1), "DIVIDENDO", Decimal("0.5")))


def test_mutacao_k5_julga_o_excesso_e_nao_o_retorno(C_, evs):
    """Desdobramento no dia de um crash de -20%: o excesso fica perto de zero e o K5 passa; o
    retorno ajustado, sem descontar o mercado, cairia fora de +-15%."""
    m = fabricar(crash_no_desdobramento=True)
    ls = C.medidas(m, m.ajustadas)
    k5 = C.k5_por_ano(ls)
    assert all(k5[a]["veredito"] == C.PASSA for a in ANOS)
    pelo_retorno = [ln for ln in ls if C.grande(ln.g) and abs(ln.g.retorno_ajustado) > 0.15]
    assert len(pelo_retorno) == 5                           # um por ano: a versao errada reprovaria


# ──────────────────────────────────────────────────────────────── completude (E-K3)

Gc = collections.namedtuple("Gc", "ticker data_ex tipos fator especi_ex")


def test_completude_nao_conta_quantidade_e_conta_o_contaminado():
    d = dt.date(2017, 5, 2)
    prov = [Gc("P%d" % i, d, "DIVIDENDO", Decimal("0.98"), "ON") for i in range(3)]
    qtd = [Gc("Q%d" % i, d, "DESDOBRAMENTO", Decimal("0.5"), "ON") for i in range(4)]
    ok = C.completude_por_ano([], prov + qtd, set(), {d: 0.0})
    assert ok[2017]["veredito"] == C.PASSA
    # mutacao do E-K3: contar a QUANTIDADE como fora do limpo daria 4/7 > 1/3
    assert sum(1 for g in prov + qtd if ajustar.classe_do_degrau(g, set()) != C.LIMPO) / 7 > 1 / 3
    contaminado = {("P0", d), ("P1", d)}
    r = C.completude_por_ano([], prov, contaminado, {d: 0.0})
    assert r[2017]["veredito"] == C.NAO_CONFIRMADO


def test_completude_de_quantidade_sem_mercado():
    d = dt.date(2017, 5, 2)
    qtd = [Gc("Q%d" % i, d, "DESDOBRAMENTO", Decimal("0.5"), "ON") for i in range(3)]
    assert C.completude_por_ano([], qtd, set(), {})[2017]["veredito"] == C.NAO_CONFIRMADO
    assert C.completude_por_ano([], qtd, set(), {d: 0.0})[2017]["veredito"] == C.PASSA


# ──────────────────────────────────────────────────────────────────────── K6

def test_k6_cada_mutacao_reprova_a_sua_linha(bruto):
    _m, r = bruto
    k6 = r["K6"]
    assert abs(k6["M1"]["razao_K2"]) < 0.2                  # E-K2: dia deslocado, razao ~ 0
    assert k6["M5"]["razao_K2"] == pytest.approx(2, abs=0.05)
    assert k6["M3"]["razao_K2"] > 10                        # muito longe da faixa
    assert k6["M2"]["anos_reprovados"] == 5
    assert k6["M4"]["classes"] == ["LIQUIDO"] * 10
    assert all(k6[k]["reprovou"] for k in ("M1", "M2", "M3", "M4", "M5"))


def test_mutacao_k6_um_criterio_que_sempre_passa_nao_tem_poder(bruto, evs, C_):
    m, _r = bruto
    cego = lambda ls: {k: dict(veredito=C.PASSA, razao=1.0) for k in ("K2", "K3")}  # noqa: E731
    k6 = C.k6(m, evs, C_, julgar=cego)
    assert k6["veredito"] == C.REPROVA and not k6["M1"]["reprovou"]


def test_m1_no_dia_ex_verdadeiro_daria_dois_e_nao_zero(bruto):
    """E-K2 fixou o dia deslocado; medir no dia ex verdadeiro daria ~2 -- as duas reprovam,
    e o teste prende qual das duas o script mede."""
    m, _r = bruto
    datas = C._Datas(m.acervo.precos)
    aj = ajustar.ajustar_tudo(m.acervo, C.mutar_m1(m, datas))
    no_dia_ex = C.razao(C.pontos(C.medidas(m, aj), C.JCP))
    assert no_dia_ex == pytest.approx(2, abs=0.05)


def test_mutar_valor_e_fator_de_provento():
    r = dict(_ticker="A", data_ex="2017-01-02", tipo="DIVIDENDO", fator="0.98",
             fator_status=ajustar.CALCULADO, data_ex_status=ajustar.DERIVADA)
    q = dict(r, tipo="DESDOBRAMENTO", fator="0.5")
    m3, mq = C.mutar_valor([r, q], Decimal(1000))
    assert Decimal(m3["fator"]) == Decimal("-19.00") and mq["fator"] == "0.5"
    assert Decimal(C.mutar_valor([r], Decimal(0))[0]["fator"]) == 1


# ───────────────────────────────────────────────────────────────── D1 e a janela

def test_d1_da_transcricao_e_passa_e_a_m4_da_dez_liquidos(evs, C_):
    assert len(evs) == 10 and [e.pos for e in evs] == list(range(1, 11))
    d = C.d1(evs, C_)
    assert d["veredito"] == C.PASSA and d["classes"] == d["gravadas"]
    assert C.m4(evs, C_)["reprovou"]


def test_veredito_d1():
    assert C.veredito_d1(["BRUTO"] * 9 + ["NENHUM"]) == C.NAO_CONFIRMADO
    assert C.veredito_d1(["BRUTO"] * 9 + ["LIQUIDO"]) == C.REPROVA
    assert C.veredito_d1(["BRUTO"] * 9) == C.NAO_CONFIRMADO


@pytest.mark.parametrize("args, esperado", [
    ((C.PASSA, {a: C.PASSA for a in ANOS}, C.PASSA, C.PASSA, C.PASSA, C.PASSA), C.PASSA),
    ((C.PASSA, {a: C.PASSA for a in ANOS}, C.PASSA, C.PASSA, C.PASSA, C.REPROVA), C.SEM_PODER),
    ((C.PASSA, {a: C.REPROVA for a in ANOS}, C.PASSA, C.PASSA, C.PASSA, C.REPROVA), C.SEM_PODER),
    ((C.PASSA, {a: (C.NAO_CONFIRMADO if a == 2018 else C.PASSA) for a in ANOS}, C.PASSA, C.REPROVA,
      C.PASSA, C.PASSA), C.REPROVA),
    ((C.PASSA, {a: C.PASSA for a in ANOS}, C.NAO_CONFIRMADO, C.PASSA, C.PASSA, C.PASSA),
     C.NAO_CONFIRMADA),
    ((C.PASSA, {a: C.PASSA for a in ANOS}, C.PASSA, C.PASSA, C.NAO_CONFIRMADO, C.PASSA),
     C.NAO_CONFIRMADA),
])
def test_veredito_da_janela(args, esperado):
    assert C.veredito_janela(*args) == esperado


def test_sem_d1_passa_a_corrida_nao_roda():
    with pytest.raises(ValueError):
        C.veredito_janela(C.NAO_CONFIRMADO, {}, C.PASSA, C.PASSA, C.PASSA, C.PASSA)


# ───────────────────────────────────────────────────────────── a trava (P7)

def _git(cwd, *a):
    subprocess.run(["git", "-C", str(cwd), *a], check=True, capture_output=True)


@pytest.fixture
def repo(tmp_path):
    remoto, local = tmp_path / "remoto.git", tmp_path / "local"
    _git(tmp_path, "init", "-q", "--bare", str(remoto))
    _git(tmp_path, "init", "-q", str(local))
    for k, v in (("user.email", "t@t"), ("user.name", "t"), ("commit.gpgsign", "false")):
        _git(local, "config", k, v)
    (local / "a.py").write_text("x = 1\n")
    _git(local, "add", "a.py")
    _git(local, "commit", "-q", "-m", "um")
    _git(local, "remote", "add", "origin", str(remoto))
    return local


def test_trava_recusa_commit_que_nao_foi_empurrado(repo):
    with pytest.raises(C.NaoPublicado, match="nao esta em nenhum ramo do origin"):
        C.conferir_publicado(str(repo))


def test_trava_aceita_o_commit_empurrado(repo):
    _git(repo, "push", "-q", "origin", "HEAD:refs/heads/ramo")
    sha = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"], capture_output=True,
                         text=True).stdout.strip()
    assert C.conferir_publicado(str(repo)) == sha


def test_trava_recusa_arvore_mudada_e_codigo_novo_fora_do_git(repo):
    _git(repo, "push", "-q", "origin", "HEAD:refs/heads/ramo")
    (repo / "b.py").write_text("y = 2\n")
    with pytest.raises(C.NaoPublicado, match="fora do git"):
        C.conferir_publicado(str(repo))
    os.remove(repo / "b.py")
    (repo / "a.py").write_text("x = 2\n")
    with pytest.raises(C.NaoPublicado, match="mudanca que o commit"):
        C.conferir_publicado(str(repo))


def test_trava_fora_de_um_repositorio(tmp_path):
    with pytest.raises(C.NaoPublicado):
        C.conferir_publicado(str(tmp_path))


def test_main_recusa_antes_de_ler_qualquer_preco(tmp_path):
    def medir(*_a, **_k):
        raise AssertionError("leu preco sem a trava")

    def publicado():
        raise C.NaoPublicado("teste")

    assert C.main([str(tmp_path / "s.csv"), "--saida", str(tmp_path / "r.json")],
                  medir=medir, publicado=publicado) == 3
    assert not (tmp_path / "r.json").exists()


def test_main_grava_o_sha256_de_cada_insumo(tmp_path, monkeypatch, bruto):
    m, _r = bruto
    raiz = tmp_path / "cotahist"
    raiz.mkdir()
    for a in ANOS:
        (raiz / ("COTAHIST_A%d.TXT" % a)).write_bytes(b"sintetico %d\n" % a)
    (raiz / "COTAHIST_A2015.TXT").write_bytes(b"fora da janela\n")
    silver = tmp_path / "eventos_silver_sintetico.csv"
    silver.write_bytes(b"cod;tipo\n")
    lidos = []

    def medir(raiz_, silver_, anos):
        lidos.append(tuple(anos))
        return m

    saida = tmp_path / "r.json"
    assert C.main([str(silver), "--cotahist", str(raiz), "--saida", str(saida)],
                  medir=medir, publicado=lambda: "abc123") == 0
    r = json.loads(saida.read_text())
    assert lidos == [tuple(ANOS)] and r["commit"] == "abc123"
    assert r["insumos"]["silver"]["sha256"] == C.sha256(str(silver))
    nomes = [c["arquivo"] for c in r["insumos"]["cotahist"]]
    assert nomes == ["COTAHIST_A%d.TXT" % a for a in ANOS]
    assert all(c["sha256"] == C.sha256(str(raiz / c["arquivo"])) for c in r["insumos"]["cotahist"])
    assert r["resultado"]["veredito"] == C.PASSA
    texto = saida.read_text()
    assert "fechamento" not in texto and "preco" not in texto      # P-136: nada de preco


def test_quarentena():
    assert C.toca_a_quarentena(range(2016, 2021)) and C.toca_a_quarentena([2013])
    assert not C.toca_a_quarentena([2021, 2025])
