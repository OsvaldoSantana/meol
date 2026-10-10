# -*- coding: utf-8 -*-
"""Testes do leitor as-of de DFP/ITR (P-51, P-53). DADO SINTETICO, todo ele.

Cada ZIP daqui e fabricado por `_zip_sintetico`: emissor `SINTETICA S.A.`, CNPJ
`00.000.000/0001-00`, valores redondos escolhidos para que um erro de linha apareca como
outro numero. O que vem do mundo real e so a FORMA: o cabecalho de cada demonstrativo, a
codificacao latin-1, o separador `;` e os nomes dos membros, medidos no
`itr_cia_aberta_2024.zip` baixado da CVM em 10/10/2026
(docs/decisoes/2026-10-10-leitor-asof-cvm.md). Nenhum numero de empresa real entra aqui.

Os quatro testes pedidos estao marcados (a) a (d) no nome. Os outros sao as armadilhas que
a medicao de 10/10 achou no dado real e que o desenho tem de recusar ruidosamente (P1).
"""
from __future__ import annotations

import csv
import datetime as dt
import decimal
import hashlib
import io
import os
import sys
import zipfile

import pytest

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import acervo as V  # noqa: E402
import armazem as A  # noqa: E402
import leitor_cvm as L  # noqa: E402

UTC = dt.timezone.utc
ULTIMO, PENULTIMO = "ÚLTIMO", "PENÚLTIMO"
CD = "099999"                      # CD_CVM sintetico, com o zero a esquerda do dado real
COLS_REG = ("dt_captura", "recurso", "arquivo", "url", "http_last_modified", "etag",
            "sha256", "bytes", "caminho", "situacao", "motivo")
# Os cabecalhos medidos em 10/10/2026 (ITR 2024): balanco sem DT_INI_EXERC, fluxo com ele,
# DMPL com COLUNA_DF.
CAB_FLUXO = ("CNPJ_CIA", "DT_REFER", "VERSAO", "DENOM_CIA", "CD_CVM", "GRUPO_DFP", "MOEDA",
             "ESCALA_MOEDA", "ORDEM_EXERC", "DT_INI_EXERC", "DT_FIM_EXERC", "CD_CONTA",
             "DS_CONTA", "VL_CONTA", "ST_CONTA_FIXA")
CAB_BALANCO = tuple(c for c in CAB_FLUXO if c != "DT_INI_EXERC")
CAB_DMPL = CAB_FLUXO[:11] + ("COLUNA_DF",) + CAB_FLUXO[11:]
CAB_INDICE = ("CNPJ_CIA", "DT_REFER", "VERSAO", "DENOM_CIA", "CD_CVM", "CATEG_DOC", "ID_DOC",
              "DT_RECEB", "LINK_DOC")


def _ln(dt_refer, conta, valor, *, ordem=ULTIMO, ini=None, fim=None, versao="1",
        escala="MIL", moeda="REAL", cd=CD, coluna=None):
    """Uma linha de demonstrativo SINTETICA."""
    return {"CNPJ_CIA": "00.000.000/0001-00", "DT_REFER": dt_refer, "VERSAO": versao,
            "DENOM_CIA": "SINTETICA S.A.", "CD_CVM": cd, "GRUPO_DFP": "SINTETICO",
            "MOEDA": moeda, "ESCALA_MOEDA": escala, "ORDEM_EXERC": ordem,
            "DT_INI_EXERC": ini or dt_refer[:4] + "-01-01", "DT_FIM_EXERC": fim or dt_refer,
            "COLUNA_DF": coluna or "", "CD_CONTA": conta, "DS_CONTA": "Conta sintetica",
            "VL_CONTA": valor, "ST_CONTA_FIXA": "S"}


def _csv_latin1(cabecalho, linhas):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=cabecalho, delimiter=";", extrasaction="ignore",
                       lineterminator="\n")
    w.writeheader()
    w.writerows(linhas)
    return buf.getvalue().encode("latin-1")


def _zip_sintetico(recurso, ano, demonstrativos):
    """Bytes de um ZIP com a forma do da CVM. `demonstrativos`: {"DRE_con": [linhas]}."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr(f"{recurso}_cia_aberta_{ano}.csv", _csv_latin1(CAB_INDICE, []))
        for dem, linhas in demonstrativos.items():
            cab = (CAB_DMPL if dem.startswith("DMPL") else
                   CAB_BALANCO if dem[:3] in ("BPA", "BPP") else CAB_FLUXO)
            z.writestr(f"{recurso}_cia_aberta_{dem}_{ano}.csv", _csv_latin1(cab, linhas))
    return buf.getvalue()


class Acervo:
    """Um repositorio falso (registro de captura) e um armazem em memoria, SINTETICOS."""

    def __init__(self, tmp_path):
        self.repo = str(tmp_path / "repo")
        os.makedirs(os.path.join(self.repo, "docs", "acervo", "cvm"))
        with open(os.path.join(self.repo, "pyproject.toml"), "w") as f:
            f.write("[project]\nname='sintetico'\n")
        self.cache = str(tmp_path / "cache")
        self.armazem = A.ArmazemMemoria()
        self.linhas = []
        self.abertos = []

    def capturar(self, quando, recurso, ano, demonstrativos, situacao="novo"):
        byte = _zip_sintetico(recurso, ano, demonstrativos)
        sha = hashlib.sha256(byte).hexdigest()
        arquivo = f"{recurso}_cia_aberta_{ano}.zip"
        self.armazem.objetos[A.chave("cvm", recurso, arquivo, sha)] = byte
        self.linhas.append(dict(dt_captura=quando, recurso=recurso, arquivo=arquivo,
                                sha256=sha, bytes=str(len(byte)), situacao=situacao))
        with open(os.path.join(self.repo, "docs", "acervo", "cvm", "capturas.csv"), "w",
                  encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=COLS_REG, delimiter=";", extrasaction="ignore")
            w.writeheader()
            w.writerows(self.linhas)
        return sha

    def kw(self):
        return dict(repo=self.repo, armazem=self.armazem, cache=self.cache)


@pytest.fixture
def acv(tmp_path, monkeypatch):
    a = Acervo(tmp_path)
    # o frescor mede o relogio real, e as capturas daqui sao de 2024-2026 de proposito
    monkeypatch.setattr(V, "frescor", lambda *x, **k: None)
    abrir = V.abrir

    def espiao(recurso, arquivo, versao=None, **k):
        a.abertos.append(arquivo)
        return abrir(recurso, arquivo, versao, **k)
    monkeypatch.setattr(V, "abrir", espiao)
    return a


def _d(texto):
    return dt.date.fromisoformat(texto)


# ── (a) PENULTIMO nao entra na serie ─────────────────────────────────────────────

def test_a_linha_PENULTIMO_nao_entra_na_serie(acv):
    """P-51. O arquivo de 2024 traz o 2023 JA REAPRESENTADO como PENULTIMO, com o mesmo
    DT_REFER do documento. Usar essa linha para 2023 e look-ahead.

    Mutacao: tire o filtro de ORDEM_EXERC e (1) a serie ganha a linha 999, (2) a conta
    3.01 passa a ter dois periodos e `valor` sobe PeriodoAmbiguo, (3) a conta 3.99, que so
    existe como PENULTIMO, devolve 999 em vez de ContaAusente."""
    acv.capturar("2025-03-31T09:15:00Z", "dfp", 2024, {"DRE_con": [
        _ln("2024-12-31", "3.01", "100"),
        _ln("2024-12-31", "3.01", "999", ordem=PENULTIMO, ini="2023-01-01", fim="2023-12-31"),
        _ln("2024-12-31", "3.99", "999", ordem=PENULTIMO, ini="2023-01-01", fim="2023-12-31"),
    ]})
    serie = L.linhas("dfp", 2024, CD, "DRE_con", _d("2025-04-01"), **acv.kw())
    assert [ln["vl_conta"] for ln in serie] == [decimal.Decimal("100")]
    assert {ln["dt_fim_exerc"] for ln in serie} == {"2024-12-31"}
    r = L.valor("dfp", CD, _d("2024-12-31"), "3.01", "DRE_con", _d("2025-04-01"), **acv.kw())
    assert r["vl_conta"] == decimal.Decimal("100")
    with pytest.raises(L.ContaAusente):
        L.valor("dfp", CD, _d("2024-12-31"), "3.99", "DRE_con", _d("2025-04-01"), **acv.kw())


# ── (b) duas versoes do mesmo DT_REFER, capturadas em dias diferentes ────────────

def test_b_consulta_antes_da_segunda_captura_devolve_a_primeira(acv):
    """P-53. A reapresentacao (VERSAO 2) so vale a partir da dt_captura em que apareceu.
    `ate` como data inclui o dia inteiro (UTC); como instante, vale o instante.

    Mutacao: troque `max(dt_captura <= D)` pela versao vigente hoje e a consulta de 19/08
    devolve 120."""
    s1 = acv.capturar("2024-05-15T09:15:00Z", "itr", 2024, {"DRE_con": [
        _ln("2024-03-31", "3.01", "100", versao="1")]})
    s2 = acv.capturar("2024-08-20T09:15:00Z", "itr", 2024, {"DRE_con": [
        _ln("2024-03-31", "3.01", "120", versao="2")]}, situacao="atualizado")

    def em(ate):
        return L.valor("itr", CD, _d("2024-03-31"), "3.01", "DRE_con", ate, **acv.kw())

    antes = em(_d("2024-08-19"))
    assert (antes["vl_conta"], antes["versao"], antes["sha256"]) == (100, "1", s1)
    assert antes["desde"] == dt.datetime(2024, 5, 15, 9, 15, tzinfo=UTC)
    assert em(dt.datetime(2024, 8, 20, 9, 14, 59, tzinfo=UTC))["sha256"] == s1
    depois = em(_d("2024-08-20"))
    assert (depois["vl_conta"], depois["versao"], depois["sha256"]) == (120, "2", s2)
    with pytest.raises(L.SemCaptura):
        em(_d("2024-05-14"))


def test_instante_sem_fuso_e_recusado(acv):
    """Um datetime ingenuo seria lido no fuso da maquina, e a dt_captura e UTC (CV-03)."""
    acv.capturar("2024-05-15T09:15:00Z", "itr", 2024, {"DRE_con": [
        _ln("2024-03-31", "3.01", "100")]})
    with pytest.raises(ValueError, match="fuso"):
        L.valor("itr", CD, _d("2024-03-31"), "3.01", "DRE_con",
                dt.datetime(2024, 6, 1, 12, 0), **acv.kw())


# ── (c) o DFP de 2025 nao reescreve o que se sabia de 2023 ───────────────────────

def test_c_DFP_de_2025_que_corrige_2023_nao_altera_o_que_se_sabia(acv):
    """P-51: a particao e o ANO DO ARQUIVO. O DFP de 2025 traz o 2024 reapresentado como
    PENULTIMO (o caso real) e, de proposito, uma linha ULTIMO com DT_REFER de 2023 (o caso
    adversario: uma correcao de 2023 dentro de outro arquivo). Nenhuma das duas alcanca a
    pergunta sobre 2023, nem antes nem DEPOIS da captura de 2025: quem fala de 2023 e o
    arquivo de 2023. A correcao entra quando o proprio dfp_cia_aberta_2023 for regerado
    com a VERSAO nova (o teste (b)).

    Mutacao: procure o DT_REFER em todo arquivo capturado ate D e a consulta de 30/04/2026
    devolve 777; e o espiao ve o arquivo de 2025 aberto."""
    acv.capturar("2024-03-28T09:15:00Z", "dfp", 2023, {"BPA_con": [
        _ln("2023-12-31", "1", "500")]})
    acv.capturar("2026-03-30T09:15:00Z", "dfp", 2025, {"BPA_con": [
        _ln("2025-12-31", "1", "650"),
        _ln("2025-12-31", "1", "610", ordem=PENULTIMO, fim="2024-12-31"),
        _ln("2023-12-31", "1", "777"),                         # adversario, sintetico
    ]})
    for ate in (_d("2026-03-29"), _d("2026-04-30")):
        acv.abertos.clear()
        r = L.valor("dfp", CD, _d("2023-12-31"), "1", "BPA_con", ate, **acv.kw())
        assert r["vl_conta"] == 500 and r["arquivo"] == "dfp_cia_aberta_2023.zip"
        assert acv.abertos == ["dfp_cia_aberta_2023.zip"]


# ── (d) dt_captura nao e data de conhecimento do mercado ─────────────────────────

@pytest.mark.repositorio   # le o politica.yaml e o PENDENCIAS.md
def test_d_dt_captura_nao_e_data_de_conhecimento_esta_declarada(acv):
    """P5 e 5-B.16. O leitor responde "o que ESTE SISTEMA tinha capturado ate D", e a
    captura chega depois do mercado (ENET -> regeracao semanal da CVM -> cron). O dado
    para corrigir existe na fonte (DT_RECEB por VERSAO, no indice), entao o limite e NOSSO:
    NAO_CONSERTADA, com o que resolve e a pendencia aberta. Toda resposta carrega o nome
    da limitacao, para que quem usa o numero nao precise lembrar dela (P7)."""
    lim = L.limitacao_declarada()
    assert lim["tipo"] == "NAO_CONSERTADA"
    assert "DT_RECEB" in lim["o_que_resolveria"]
    with open(os.path.join(os.path.dirname(AQUI), "PENDENCIAS.md"), encoding="utf-8") as f:
        assert f"\n## {lim['pendencia']} · " in f.read()
    acv.capturar("2024-05-15T09:15:00Z", "itr", 2024, {"DRE_con": [
        _ln("2024-03-31", "3.01", "100")]})
    r = L.valor("itr", CD, _d("2024-03-31"), "3.01", "DRE_con", _d("2024-06-01"), **acv.kw())
    assert r["limitacao"] == L.LIMITACAO


def test_d_sem_a_limitacao_declarada_o_leitor_recusa(acv, monkeypatch):
    """Mutacao da (d): apague a entrada do politica.yaml e o leitor para de responder, em
    vez de devolver numero sem o aviso."""
    monkeypatch.setattr(L, "_limitacoes", lambda: {})
    acv.capturar("2024-05-15T09:15:00Z", "itr", 2024, {"DRE_con": [
        _ln("2024-03-31", "3.01", "100")]})
    with pytest.raises(L.LimitacaoNaoDeclarada):
        L.valor("itr", CD, _d("2024-03-31"), "3.01", "DRE_con", _d("2024-06-01"), **acv.kw())


# ── as armadilhas medidas no ITR 2024 real, em 10/10/2026 ────────────────────────

def test_trimestre_e_acumulado_sao_dois_periodos_ULTIMO_e_o_leitor_nao_escolhe(acv):
    """Medido: na DRE consolidada do ITR 2024, 32.901 de 48.907 chaves (CD_CVM, DT_REFER,
    CD_CONTA) em ULTIMO tem mais de uma linha -- o trimestre e o acumulado do ano, que so
    o DT_INI_EXERC separa. Sem o periodo, devolver uma delas seria sorteio."""
    acv.capturar("2024-08-20T09:15:00Z", "itr", 2024, {"DRE_con": [
        _ln("2024-06-30", "3.01", "200", ini="2024-01-01"),
        _ln("2024-06-30", "3.01", "110", ini="2024-04-01"),
    ]})
    kw = acv.kw()
    with pytest.raises(L.PeriodoAmbiguo, match="2024-04-01"):
        L.valor("itr", CD, _d("2024-06-30"), "3.01", "DRE_con", _d("2024-09-01"), **kw)
    tri = L.valor("itr", CD, _d("2024-06-30"), "3.01", "DRE_con", _d("2024-09-01"),
                  dt_ini_exerc=_d("2024-04-01"), **kw)
    assert tri["vl_conta"] == 110 and tri["dt_ini_exerc"] == "2024-04-01"


def test_duplicata_exata_e_uma_linha_e_valor_divergente_e_recusado(acv):
    """Medido: 572 chaves duplicadas na DRE consolidada, todas com o mesmo valor; e 13 no
    BPP consolidado com valores DIFERENTES na mesma chave, todas de um so emissor. A
    primeira se junta; a segunda nao tem resposta certa, e escolher seria inventar (P1)."""
    acv.capturar("2024-05-15T09:15:00Z", "itr", 2024, {"BPP_con": [
        _ln("2024-03-31", "2.01", "444"), _ln("2024-03-31", "2.01", "444"),
        _ln("2024-03-31", "2.02", "444"), _ln("2024-03-31", "2.02", "1351"),
    ]})
    kw = acv.kw()
    assert L.valor("itr", CD, _d("2024-03-31"), "2.01", "BPP_con", _d("2024-06-01"),
                   **kw)["vl_conta"] == 444
    with pytest.raises(L.ValorAmbiguo, match="1351"):
        L.valor("itr", CD, _d("2024-03-31"), "2.02", "BPP_con", _d("2024-06-01"), **kw)


def test_DMPL_separa_a_coluna_do_patrimonio(acv):
    """Medido: na DMPL toda chave sem COLUNA_DF se repete (40.080 de 40.080)."""
    acv.capturar("2024-05-15T09:15:00Z", "itr", 2024, {"DMPL_con": [
        _ln("2024-03-31", "5.01", "10", coluna="Capital Social Integralizado"),
        _ln("2024-03-31", "5.01", "20", coluna="Reservas de Lucro"),
    ]})
    kw = acv.kw()
    with pytest.raises(L.PeriodoAmbiguo):
        L.valor("itr", CD, _d("2024-03-31"), "5.01", "DMPL_con", _d("2024-06-01"), **kw)
    assert L.valor("itr", CD, _d("2024-03-31"), "5.01", "DMPL_con", _d("2024-06-01"),
                   coluna_df="Reservas de Lucro", **kw)["vl_conta"] == 20


def test_escala_vira_reais_em_decimal_nunca_float(acv):
    """ESCALA_MOEDA mistura MIL e UNIDADE no mesmo arquivo (medido: as duas em todo
    demonstrativo do ITR 2024). O valor em reais e VL_CONTA x escala, em Decimal."""
    acv.capturar("2024-05-15T09:15:00Z", "itr", 2024, {"DRE_con": [
        _ln("2024-03-31", "3.01", "1.5000000000", escala="MIL"),
        _ln("2024-03-31", "3.02", "7.0000000000", escala="UNIDADE"),
    ]})
    kw = acv.kw()
    mil = L.valor("itr", CD, _d("2024-03-31"), "3.01", "DRE_con", _d("2024-06-01"), **kw)
    assert mil["valor_em_reais"] == decimal.Decimal("1500")
    assert isinstance(mil["valor_em_reais"], decimal.Decimal)
    assert L.valor("itr", CD, _d("2024-03-31"), "3.02", "DRE_con", _d("2024-06-01"),
                   **kw)["valor_em_reais"] == decimal.Decimal("7")


@pytest.mark.parametrize("campo,valor", [("ORDEM_EXERC", "ANTEPENÚLTIMO"),
                                         ("ESCALA_MOEDA", "MILHAO"), ("MOEDA", "DOLAR")])
def test_enumeracao_fora_da_lista_OBSERVADO_falha_ruidosamente(acv, campo, valor):
    """P1: as tres enumeracoes sao OBSERVADO (contadas, nao documentadas). Um valor novo
    numa linha de OUTRO emissor tambem derruba a leitura: o arquivo e lido inteiro, e
    tratar o desconhecido como um dos conhecidos e o erro de tres ordens de grandeza."""
    outra = _ln("2024-03-31", "3.01", "1", cd="011111")
    outra[campo] = valor
    acv.capturar("2024-05-15T09:15:00Z", "itr", 2024, {"DRE_con": [
        _ln("2024-03-31", "3.01", "100"), outra]})
    with pytest.raises(L.EnumeracaoDesconhecida, match=campo):
        L.valor("itr", CD, _d("2024-03-31"), "3.01", "DRE_con", _d("2024-06-01"), **acv.kw())


def test_cd_cvm_numerico_e_o_texto_com_zeros_sao_o_mesmo_emissor(acv):
    acv.capturar("2024-05-15T09:15:00Z", "itr", 2024, {"DRE_con": [
        _ln("2024-03-31", "3.01", "100", cd="001023")]})
    assert L.valor("itr", 1023, _d("2024-03-31"), "3.01", "DRE_con", _d("2024-06-01"),
                   **acv.kw())["vl_conta"] == 100


def test_demonstrativo_e_recurso_fora_do_leiaute_sao_recusados(acv):
    with pytest.raises(ValueError, match="demonstrativo"):
        L.valor("itr", CD, _d("2024-03-31"), "3.01", "DRE", _d("2024-06-01"), **acv.kw())
    with pytest.raises(ValueError, match="recurso"):
        L.valor("fre", CD, _d("2024-03-31"), "3.01", "DRE_con", _d("2024-06-01"), **acv.kw())


def test_membro_ausente_na_versao_e_falha_nomeada(acv):
    """Ausencia de dado nao e zero (P1): a versao vigente sem o membro diz qual falta."""
    acv.capturar("2024-05-15T09:15:00Z", "itr", 2024, {"DRE_con": [
        _ln("2024-03-31", "3.01", "100")]})
    with pytest.raises(L.MembroAusente, match="itr_cia_aberta_DVA_con_2024.csv"):
        L.valor("itr", CD, _d("2024-03-31"), "7.01", "DVA_con", _d("2024-06-01"), **acv.kw())


def test_o_leiaute_vem_do_yaml_e_nao_do_codigo():
    """P2: as enumeracoes e a forma do arquivo sao dado. O ULTIMO que o leitor usa e o da
    lista OBSERVADO, e as colunas de periodo sao as declaradas."""
    lei = L.leiaute()
    ordem = lei["enumeracoes"]["ORDEM_EXERC"]
    assert ordem["status"] == "OBSERVADO" and ordem["usado"] in ordem["valores"]
    assert ordem["usado"] == ULTIMO
    assert lei["enumeracoes"]["ESCALA_MOEDA"]["valores"] == {"MIL": 1000, "UNIDADE": 1}
    assert lei["colunas_de_periodo"] == ["DT_INI_EXERC", "DT_FIM_EXERC", "COLUNA_DF"]
