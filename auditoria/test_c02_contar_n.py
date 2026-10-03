# -*- coding: utf-8 -*-
"""O n do JCP sai do silver e da PRESENCA no COTAHIST, sem ler preco (P-115, n-c).

O QUE MEDE (P5):
  (a) com toda posicao do registro de cotacao fora dos campos de identidade ENVENENADA
      (preco, volume, fator de cotacao -- qualquer leitura levanta erro), a presenca e a
      contagem saem certas;
  (b) mutacao: o mesmo leitor com PREULT na lista de campos e pego;
  (c) a unidade e a dos 807 (819 ate 03/10): degrau com negocio no dia ex e na vespera DO
      PAPEL, que ganhou
      fator, em dia limpo (sem evento de quantidade, sem marca B/G, sem evento sem fator),
      com mercado do dia (>= 20 papeis), so JCP;
  (d) a calibracao: 2021-2025 da 807 (segue), 808-823 (segue, n x 807/n_cal para baixo)
      ou outro valor (PARA, mostra a diferenca, sem candidatas);
  (e) a regra da janela e o texto citam os mesmos numeros.
NAO mede o dado real: o silver e o COTAHIST moram no disco dele, e o script nao roda aqui.
"""
from __future__ import annotations

import datetime as dt
import os
import sys

import pytest

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import c02_contar_n as N  # noqa: E402

TEXTO = os.path.join(os.path.dirname(AQUI), "docs", "auditoria",
                     "C02-CRITERIO-V2-PREREGISTRO.md")
JCP, DIV = "JRS CAP PROPRIO", "DIVIDENDO"


class PrecoLido(AssertionError):
    pass


def _permitidas():
    ok = set()
    for campo in ("TIPREG",) + N.CAMPOS_COTAHIST:
        a, b = N.calendario.pos(campo)
        ok.update(range(a, b))
    return ok


class Envenenada(str):
    """Uma linha de cotacao em que so as posicoes dos campos de identidade se deixam ler."""

    PERMITIDAS: set[int] = set()

    def __getitem__(self, k):
        idx = range(*k.indices(len(self))) if isinstance(k, slice) else [k]
        if any(i not in self.PERMITIDAS for i in idx):
            raise PrecoLido(k)
        return str.__getitem__(self, k)


def _raw(data, codneg, especi="ON      NM", isin="BRXXXXACNOR0", codbdi="02",
         tpmerc="010"):
    campos = dict(TIPREG="01", DATA=data.replace("-", ""), CODBDI=codbdi, CODNEG=codneg,
                  TPMERC=tpmerc, ESPECI=especi, CODISI=isin)
    linha = ["9"] * 245                      # o "preco" e tudo o mais: noves
    for nome, valor in campos.items():
        a, b = N.calendario.pos(nome)
        linha[a:b] = list(valor.ljust(b - a)[: b - a])
    return "".join(linha)


@pytest.fixture
def veneno():
    Envenenada.PERMITIDAS = _permitidas()
    return lambda s: Envenenada(s)


def test_o_veneno_funciona(veneno):
    """Vacuidade: se a linha envenenada deixasse ler o preco, (a) nao provaria nada."""
    raw = veneno(_raw("2021-01-04", "PETR4"))
    a, b = N.calendario.pos("PREULT")
    with pytest.raises(PrecoLido):
        raw[a:b]
    assert raw[slice(*N.calendario.pos("CODNEG"))].strip() == "PETR4"


def test_a_campos_so_de_identidade_nenhum_de_preco():
    assert set(N.CAMPOS_COTAHIST) == {"DATA", "CODBDI", "CODNEG", "TPMERC", "ESPECI",
                                      "CODISI"}


def test_a_presenca_sai_certa_com_o_preco_envenenado(veneno):
    linhas = [veneno(_raw("2021-01-04", "PETR4", "PN      N2", "BRPETRACNPR6")),
              veneno(_raw("2021-01-05", "PETR4", "PN  EJ  N2", "BRPETRACNPR6")),
              veneno(_raw("2021-01-05", "PETR4F", "PN      N2", "BRPETRACNPR6", "96", "020")),
              veneno(_raw("2021-01-06", "VALE3"))]
    c = N.presenca(linhas)
    assert c.datas == {dt.date(2021, 1, 4), dt.date(2021, 1, 5), dt.date(2021, 1, 6)}
    assert set(c.dias) == {"PETR4", "VALE3"}, "o fracionario nao e o papel (CODBDI/TPMERC)"
    assert c.especi["PETR4"][dt.date(2021, 1, 5)] == "PN  EJ  N2"
    assert c.primeiro["PETR4"] == (dt.date(2021, 1, 4), "PN", "BRPETRACNPR6")


def test_b_mutacao_leitor_com_PREULT_e_pego(veneno, monkeypatch):
    monkeypatch.setattr(N, "CAMPOS_COTAHIST", N.CAMPOS_COTAHIST + ("PREULT",))
    with pytest.raises(PrecoLido):
        N.presenca([veneno(_raw("2021-01-04", "PETR4"))])


# ── (c) a unidade dos 819, num acervo sintetico ──────────────────────────────

def _ev(cod, ts, tipo, ultimo, fator_status="CALCULADO", isin=""):
    return dict(cod=cod, type_stock=ts, isin=isin, tipo=tipo, ultimo_dia_com_direito=ultimo,
                data_ex="", data_ex_status="FORA_DA_COBERTURA", fator_status=fator_status)


def _acervo(dias_por_papel, especi_ex=None):
    """{ticker: [dias]} -> linhas de cotacao. Os tickers `Mnn` so fazem o mercado do dia."""
    linhas = []
    for tk, dias in dias_por_papel.items():
        esp = {"PETR4": "PN      N2", "VALE3": "ON      NM", "ITUB4": "PN      N1"}.get(
            tk, "ON      NM")
        for d in dias:
            e = (especi_ex or {}).get((tk, d), esp)
            linhas.append(_raw(d, tk, e, isin="BR" + tk.ljust(10, "X")))
    return N.presenca(sorted(linhas, key=lambda s: s[2:10]))


DIAS = ["2021-01-04", "2021-01-05", "2021-01-06", "2021-01-07"]
MERCADO = {f"M{i:02d}3": DIAS for i in range(20)}
# `mercado_do_dia` so conta papeis casados com algum evento: cada papel do "mercado" tem um
# dividendo com data ex em 07/01, longe do dia medido (06/01)
EV_MERCADO = [_ev(tk, "ON", DIV, "2021-01-06") for tk in MERCADO]


def test_c_so_JCP_limpo_com_vespera_e_mercado_conta(veneno):
    cot = _acervo(dict(MERCADO, PETR4=DIAS, VALE3=DIAS, ITUB4=DIAS))
    evs = [_ev("PETR", "PN", JCP, "2021-01-05"),                   # ex 06: conta
           _ev("VALE", "ON", JCP, "2021-01-05"),                   # JCP + dividendo: nao
           _ev("VALE", "ON", DIV, "2021-01-05"),
           _ev("ITUB", "PN", JCP, "2021-01-05"),                   # + evento sem fator
           _ev("ITUB", "PN", "SUBSCRICAO", "2021-01-05", "SEM_FATOR")]
    c = N.medir_n(evs + EV_MERCADO, cot, range(2021, 2022))
    assert c[2021]["so_jcp"] == 1


def test_c_sem_negocio_na_vespera_do_papel_nao_conta():
    cot = _acervo(dict(MERCADO, PETR4=["2021-01-06"]))            # so negociou no dia ex
    c = N.medir_n([_ev("PETR", "PN", JCP, "2021-01-05")] + EV_MERCADO, cot, range(2021, 2022))
    assert c.get(2021, {}).get("so_jcp", 0) == 0


def test_c_dia_sem_mercado_nao_conta():
    poucos = {f"M{i:02d}3": DIAS for i in range(5)}                 # 5 papeis: nao e mercado
    cot = _acervo(dict(poucos, PETR4=DIAS))
    c = N.medir_n([_ev("PETR", "PN", JCP, "2021-01-05")] + EV_MERCADO, cot, range(2021, 2022))
    assert c.get(2021, {}).get("so_jcp", 0) == 0


def test_c_marca_de_bonificacao_no_ESPECI_tira_o_dia():
    cot = _acervo(dict(MERCADO, PETR4=DIAS),
                  especi_ex={("PETR4", "2021-01-06"): "PN  EJB N2"})
    c = N.medir_n([_ev("PETR", "PN", JCP, "2021-01-05")] + EV_MERCADO, cot, range(2021, 2022))
    assert c.get(2021, {}).get("so_jcp", 0) == 0


def test_c_SEM_PRECO_ganha_fator_pela_presenca_e_a_copia_da_outra_esteira_contamina():
    """A-13 sem `valor`: o SEM_PRECO sozinho ganha fator (negocio na vespera); a copia de um
    JCP que o paginado ja trouxe CALCULADO fica sem fator e contamina o dia, como no
    `ajustar.completar_preco_de_vespera`."""
    cot = _acervo(dict(MERCADO, PETR4=DIAS, VALE3=DIAS))
    so = N.medir_n([_ev("PETR", "PN", JCP, "2021-01-05", "SEM_PRECO")] + EV_MERCADO, cot,
                   range(2021, 2022))
    assert so[2021]["so_jcp"] == 1
    dup = N.medir_n([_ev("VALE", "ON", JCP, "2021-01-05"),
                     _ev("VALE", "ON", JCP, "2021-01-05", "SEM_PRECO")] + EV_MERCADO, cot,
                    range(2021, 2022))
    assert dup.get(2021, {}).get("so_jcp", 0) == 0


def test_c_o_primeiro_dia_da_janela_nao_tem_vespera():
    cot = _acervo(dict(MERCADO, PETR4=DIAS))
    c = N.medir_n([_ev("PETR", "PN", JCP, "2020-12-30")] + EV_MERCADO, cot, range(2021, 2022))
    assert c.get(2021, {}).get("so_jcp", 0) == 0


# ── (d) calibracao e (e) regra ────────────────────────────────────────────────

# Decisao dele, 27/09/2026, na referencia remedida em 03/10: tolerancia de 2% SO PARA CIMA.
# 807 segue sem correcao; de 808 a 823 (807 x 1,02 = 823,14) segue, com o n de cada candidata
# x 807/n_cal arredondado para BAIXO; 806 ou 824 PARA.

def test_d_tolerancia_e_constante_declarada():
    assert N.TOLERANCIA_CALIBRACAO == 0.02


@pytest.mark.parametrize("n_cal", [807, 808, 823])
def test_d_dentro_da_tolerancia_segue(n_cal):
    assert N.calibrar(n_cal) == (N.CALIBRACAO_N, n_cal)


@pytest.mark.parametrize("n_cal", [806, 824])
def test_d_fora_da_tolerancia_para_e_mostra_a_diferenca(n_cal):
    with pytest.raises(N.CalibracaoFalhou) as e:
        N.calibrar(n_cal)
    assert str(n_cal) in str(e.value) and "807" in str(e.value)
    assert f"{n_cal - 807:+d}" in str(e.value)


def test_d_correcao_arredonda_para_baixo_e_so_diminui():
    assert N.corrigir(1650, 807) == 1650
    assert N.corrigir(1650, 808) == 1647          # 1650 x 807 / 808 = 1647,76 -> 1647
    assert N.corrigir(2000, 823) == 1961
    for n_cal in range(807, 824):
        assert N.corrigir(1650, n_cal) <= 1650


NS = {(2016, 2020): 1300, (2015, 2020): 1600, (2014, 2020): 1700, (2013, 2020): 2000}


def _main(monkeypatch, tmp_path, capsys, n_cal):
    silver = tmp_path / "silver.csv"
    silver.write_text("x\n", encoding="utf-8")
    monkeypatch.setattr(N, "ler_silver", lambda caminho: iter(()))
    monkeypatch.setattr(N, "ler_cotahist", lambda raiz, anos: None)
    tabela = dict(NS)
    tabela[N.CALIBRACAO_ANOS] = n_cal
    monkeypatch.setattr(N, "n_da_janela", lambda evs, cot, ini, fim: tabela[(ini, fim)])
    rc = N.main([str(silver)])
    return rc, capsys.readouterr().out


def test_d_main_807_segue_sem_correcao(monkeypatch, tmp_path, capsys):
    rc, out = _main(monkeypatch, tmp_path, capsys, 807)
    assert rc == 0 and "fator 1 (807/807)" in out
    assert "janela 2014-2020, n 1700" in out


@pytest.mark.parametrize("n_cal,janela", [(808, "janela 2014-2020, n 1697"),
                                          (823, "janela 2013-2020, n 1961")])
def test_d_main_dentro_da_tolerancia_corrige_e_imprime_o_fator(monkeypatch, tmp_path,
                                                               capsys, n_cal, janela):
    rc, out = _main(monkeypatch, tmp_path, capsys, n_cal)
    assert rc == 0 and f"fator 807/{n_cal}" in out
    assert "2014-2020: n_JCP 1700 -> corrigido" in out
    assert janela in out


@pytest.mark.parametrize("n_cal", [806, 824])
def test_d_main_fora_da_tolerancia_para_sem_candidatas(monkeypatch, tmp_path, capsys,
                                                       n_cal):
    rc, out = _main(monkeypatch, tmp_path, capsys, n_cal)
    assert rc == 2 and "PARADO" in out
    assert "n_JCP" not in out and "janela 20" not in out


def test_e_limiar_e_candidatas():
    assert N.N_MIN == 1693 and N.CALIBRACAO_N == 807 and N.SIGMA_2021_2025 == 0.0482
    assert N.CALIBRACAO_ANOS == (2021, 2025)
    assert N.CANDIDATAS == ((2016, 2020), (2015, 2020), (2014, 2020), (2013, 2020))


def test_e_regra_escolhe_a_menor_que_atende():
    ns = {(2016, 2020): 1200, (2015, 2020): 1500, (2014, 2020): 1700, (2013, 2020): 2000}
    assert N.janela(ns) == dict(ini=2014, fim=2020, n=1700, atende=True)


def test_e_regra_sem_candidata_cai_em_2016_2020():
    ns = {w: 900 for w in N.CANDIDATAS}
    assert N.janela(ns) == dict(ini=2016, fim=2020, n=900, atende=False)


def test_e_o_texto_cita_os_mesmos_numeros():
    with open(TEXTO, encoding="utf-8") as f:
        s = f.read()
    assert "n ≥ 1.693" in s and "2016–2020, 2015–2020, 2014–2020 e 2013–2020" in s
    assert "n_cal de 820 a 835" in s and "n_cal de 808 a 823" in s and "sai com código 2" in s
    assert "**arredondado para baixo**" in s and "Alternativa rejeitada: parar sempre" in s
