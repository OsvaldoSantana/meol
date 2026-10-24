# -*- coding: utf-8 -*-
"""P-30 parte 1 + P-64 -- o bloco C como codigo: as cinco saidas do portao, sobre acervo SINTETICO.

POR QUE ESTE TESTE EXISTE (24/10/2026). `bloco_C_solvencia` tinha 48 chaves escritas em 05/09 e
nenhum modulo as aplicava: os testes conferiam o texto, nao o comportamento (P-17 deixou o aviso:
"o teste do C-04 tem de ganhar a irma comportamental"). Aqui o bloco roda sobre um DFP sintetico
(a forma do ZIP da CVM, do `fase0/test_leitor_cvm.py`) e prova o que a P-64 pede:

  a. banco -> RECUSA_REGIME, sem numero (o modo de falha do F-02: metrica que nao se aplica mas
     nao falha);
  b. EXIGE_DOSSIE, MARCA e RECUSA_REGIME nao tiram ninguem do universo; so REPROVA tira;
  c. limiar PENDENTE nunca reprova; limiar gravado reprova com o motivo completo; mudar o corte
     no YAML muda o resultado sem mudar codigo (`natureza_dos_cortes`);
  d. a 63a e lida do YAML: o nivel corta, a tendencia marca (AGUARDA_SERIE, sem serie);
  e. a contagem por corte e por ponto da grade: so numeros, sem nome e sem CD_CVM;
  f. o bloco so ve o documento CONHECIDO na data, pelo leitor (modo da captura e dt_receb),
     nunca pelo DT_REFER.

ALCANCE (P5): sintetico. Prova o comportamento do modulo e do YAML, NAO o numero de empresa
alguma: a contagem real e a `medicoes/p30_contagem.py`. Nenhum corte esta ativo (todos PENDENTE).
"""
from __future__ import annotations

import copy
import datetime as dt
import io
import json
import os
import sys
from decimal import Decimal

import pytest
import yaml

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(RAIZ, "fase0"))
import bloco_c as B  # noqa: E402
import test_leitor_cvm as TL  # noqa: E402
import acervo as V  # noqa: E402

POLITICA = os.path.join(AQUI, "politica.yaml")


@pytest.fixture
def acv(tmp_path, monkeypatch):
    """O acervo sintetico do leitor (fase0/test_leitor_cvm.py), com o frescor desligado: as
    capturas daqui sao de 2024-2026 de proposito e o frescor mede o relogio real."""
    a = TL.Acervo(tmp_path)
    monkeypatch.setattr(V, "frescor", lambda *x, **k: None)
    abrir = V.abrir

    def espiao(recurso, arquivo, versao=None, **k):
        a.abertos.append(arquivo)
        return abrir(recurso, arquivo, versao, **k)
    monkeypatch.setattr(V, "abrir", espiao)
    return a
IND = "Alimentos"           # um SETOR_ATIV OBSERVADO, regime GERAL


def _real():
    return B.carregar()


def _com_limiar(P, **limiares):
    """Uma COPIA da politica com o limiar gravado -- o 'YAML de teste' da P-64."""
    Q = copy.deepcopy(P)
    for cod, v in limiares.items():
        cod = cod.replace("_", "-")
        if cod == "C-05":                      # o C-05 le o limiar do campos_C04_C05
            Q["campos_C04_C05"]["C-05"]["limiar"] = v
        else:
            Q["metricas"][cod]["limiar"] = v
    return Q


def _yaml_de_teste(tmp_path, P):
    """Grava a politica de teste e a carrega pelo MESMO caminho do YAML real."""
    caminho = tmp_path / "politica_teste.yaml"
    caminho.write_text(yaml.safe_dump({"bloco_C_solvencia": P}, allow_unicode=False),
                       encoding="utf-8")
    return B.carregar(str(caminho))


# ── o DFP sintetico de uma empresa industrial ────────────────────────────────

def _c(dt_refer, conta, valor, ds, cd):
    ln = TL._ln(dt_refer, conta, str(valor), cd=cd)
    ln["DS_CONTA"] = ds
    return ln


def _demonstrativos(dt_refer, cd, *, ebit=300, resfin=-100, caixa=50, aplic=50, cp=100, lp=300):
    """EBIT 300 / despesa liquida 100 = cobertura 3; divida CP 100 / total 400 = 0,25;
    caixa 100 / divida CP 100 = 1. As descricoes sao as do plano de contas lido no DFP real."""
    return {
        "DRE_con": [_c(dt_refer, "3.05", ebit,
                       "Resultado Antes do Resultado Financeiro e dos Tributos", cd),
                    _c(dt_refer, "3.06", resfin, "Resultado Financeiro", cd)],
        "BPA_con": [_c(dt_refer, "1.01.01", caixa, "Caixa e Equivalentes de Caixa", cd),
                    _c(dt_refer, "1.01.02", aplic, "Aplicações Financeiras", cd)],
        "BPP_con": [_c(dt_refer, "2.01.04", cp, "Empréstimos e Financiamentos", cd),
                    _c(dt_refer, "2.02.01", lp, "Empréstimos e Financiamentos", cd)],
    }


def _capturar(acv, quando, ano, cd, receb=None, **v):
    dt_refer = f"{ano}-12-31"
    idx = [TL._idx(dt_refer, "1", receb or f"{ano + 1}-03-20", cd=cd, categ="DFP")]
    acv.capturar(quando, "dfp", ano, _demonstrativos(dt_refer, cd, **v), indice=idx)


CAD = {99001: IND}                       # CD_CVM -> SETOR_ATIV (o cadastro sintetico)
ATE = dt.date(2025, 6, 30)
CD = "099001"


def _avaliar(acv, P, cd=CD, cadastro=None, ate=ATE, n=10, **k):
    return B.avaliar(cd, ate, CAD if cadastro is None else cadastro, P, n_universo=n,
                     **{**acv.kw(), **k})


@pytest.fixture
def empresa(acv):
    _capturar(acv, "2025-04-10T12:00:00Z", 2024, CD)
    return acv


# ── o YAML: nenhum corte ativo, grades com fonte e autor ─────────────────────

def test_nenhum_corte_esta_ativo_e_toda_metrica_tem_grade_com_fonte_e_autor():
    P = _real()
    for cod in P["ordem_de_avaliacao"]:
        m = P["metricas"].get(cod)
        if m is None:
            continue                              # C-04 mora em campos_C04_C05
        if m["status"] == "NAO_IMPLEMENTADA":
            assert m["motivo"].strip() and m["pendencia"].startswith("P-")
        assert len(m["grade"]) == 3, cod
        for ponto in m["grade"]:
            assert isinstance(ponto["valor"], (int, float)) and ponto["fonte"].strip()
            assert ponto["autor"].startswith(("Claude, 24/10/2026", "Osvaldo, 16/10/2026"))
            assert "nao e corte" in ponto["autor"]
    assert B.limiar(P, "C-01") is None and B.limiar(P, "C-03") is None
    assert B.limiar(P, "C-05") is None and B.limiar(P, "C-02") is None


def test_a_grade_do_C05_e_a_que_ele_deu_no_27c():
    grade = [p["valor"] for p in _real()["metricas"]["C-05"]["grade"]]
    assert grade == [0.5, 1.0, 1.5]


def test_a_ordem_estruturada_concorda_com_a_prosa_da_secao_5():
    import re
    P = _real()
    citados = [c for linha in P["ordem"] for c in re.findall(r"C-[0]\d", linha)]
    na_prosa = list(dict.fromkeys(citados))          # a prosa repete C-04 e C-05 nas notas
    assert P["ordem_de_avaliacao"] == na_prosa


# ── a. banco: RECUSA_REGIME, sem numero ──────────────────────────────────────

def test_a_banco_e_recusado_sem_numero_e_sem_abrir_o_acervo(acv):
    _capturar(acv, "2025-04-10T12:00:00Z", 2024, "099002", ebit=-1)
    r = _avaliar(acv, _real(), cd="099002", cadastro={99002: "Bancos"})
    assert r["saida"] == "RECUSA_REGIME"
    assert r["metricas"] == {} and "valor" not in json.dumps(r, default=str)
    assert acv.abertos == [], "recusar nao pode ler o demonstrativo (F-02)"
    assert "regime_instituicao_financeira" in r["motivo"]


def test_a_seguradora_tambem_e_recusada():
    P = _real()
    r = B.avaliar("099003", ATE, {99003: "Seguradoras e Corretoras"}, P, n_universo=1)
    assert r["saida"] == "RECUSA_REGIME"


# ── b. o invariante: so REPROVA tira empresa do universo ─────────────────────

def test_b_so_REPROVA_tira_do_universo(empresa):
    P = _real()
    assert P["saidas_do_portao"]["tiram_do_universo"] == ["REPROVA"]
    saidas = {s: {"saida": s} for s in P["saidas_do_portao"]["saidas"]}
    assert set(saidas) == {"APROVA", "REPROVA", "MARCA", "RECUSA_REGIME", "EXIGE_DOSSIE"}
    ficam = B.universo(list(saidas.values()), P)
    assert {x["saida"] for x in ficam} == set(saidas) - {"REPROVA"}


def test_b_EXIGE_DOSSIE_marca_e_recusa_ficam_no_universo(empresa):
    P = _real()
    banco = _avaliar(empresa, P, cd="099002", cadastro={99002: "Bancos"})
    dossie = _avaliar(empresa, P, cd="099004", cadastro={99004: "Factoring"})
    marca = _avaliar(empresa, P)
    sem_cadastro = _avaliar(empresa, P, cd="099005", cadastro={})
    assert [x["saida"] for x in (banco, dossie, marca, sem_cadastro)] == [
        "RECUSA_REGIME", "EXIGE_DOSSIE", "MARCA", "EXIGE_DOSSIE"]
    assert B.universo([banco, dossie, marca, sem_cadastro], P) == [
        banco, dossie, marca, sem_cadastro]


def test_b_regime_sem_identificacao_cai_em_EXIGE_DOSSIE_nunca_em_zero(empresa):
    """Setor vazio (6 linhas no cadastro real) e CD_CVM fora do cadastro: nao se sabe se e
    banco. O portao nao calcula e nao assume GERAL."""
    P = _real()
    for cad in ({99001: ""}, {}):
        r = _avaliar(empresa, P, cadastro=cad)
        assert r["saida"] == "EXIGE_DOSSIE" and r["metricas"] == {}


def test_b_setor_fora_da_enumeracao_falha_ruidosamente(empresa):
    with pytest.raises(B.SetorForaDaEnumeracao, match="P1"):
        _avaliar(empresa, _real(), cadastro={99001: "Setor Que Nao Existe"})


# ── c. limiar PENDENTE nunca reprova; gravado reprova com o motivo completo ──

def test_c_limiar_PENDENTE_nunca_reprova_ainda_que_o_valor_seja_pessimo(acv):
    _capturar(acv, "2025-04-10T12:00:00Z", 2024, CD, ebit=1, resfin=-1000, caixa=0, aplic=0)
    r = _avaliar(acv, _real())
    assert r["saida"] == "MARCA"
    c01 = r["metricas"]["C-01"]
    assert c01["saida"] == "MARCA" and c01["causa"] == "LIMIAR_PENDENTE"
    assert c01["valor"] == Decimal("0.001")        # o numero sai: calcula e marca
    assert r["metricas"]["C-05"]["saida"] == "MARCA"


def test_c_limiar_gravado_reprova_com_codigo_valor_corte_e_N(empresa):
    P = _com_limiar(_real(), C_01=3.5)
    r = _avaliar(empresa, P, n=427)
    c01 = r["metricas"]["C-01"]
    assert (c01["saida"], c01["codigo"]) == ("REPROVA", "C-01")
    assert c01["valor"] == Decimal(3) and c01["corte"] == 3.5 and c01["n_universo"] == 427
    for parte in ("C-01", "3", "3.5", "427"):
        assert parte in c01["motivo"], parte
    assert r["saida"] == "REPROVA" and B.universo([r], P) == []


def test_c_mudar_o_corte_no_yaml_muda_o_resultado_sem_mudar_codigo(empresa, tmp_path):
    base = _real()
    com_3_5 = _yaml_de_teste(tmp_path, _com_limiar(base, C_01=3.5))
    com_2_0 = _yaml_de_teste(tmp_path, _com_limiar(base, C_01=2.0))
    assert _avaliar(empresa, com_3_5)["metricas"]["C-01"]["saida"] == "REPROVA"
    assert _avaliar(empresa, com_2_0)["metricas"]["C-01"]["saida"] == "APROVA"


def test_c_o_sentido_de_cada_corte_vem_do_yaml(empresa):
    """C-03 reprova ACIMA do corte (rolagem), C-01 e C-05 reprovam ABAIXO."""
    P = _real()
    assert (P["metricas"]["C-01"]["sentido"], P["metricas"]["C-03"]["sentido"],
            P["metricas"]["C-05"]["sentido"]) == (
        "reprova_abaixo", "reprova_acima", "reprova_abaixo")
    r = _avaliar(empresa, _com_limiar(P, C_03=0.2, C_05=1.5))
    assert r["metricas"]["C-03"]["saida"] == "REPROVA"        # 0,25 > 0,2
    assert r["metricas"]["C-05"]["saida"] == "REPROVA"        # 1,0 < 1,5
    r = _avaliar(empresa, _com_limiar(P, C_03=0.3, C_05=0.5))
    assert r["metricas"]["C-03"]["saida"] == "APROVA"
    assert r["metricas"]["C-05"]["saida"] == "APROVA"


def test_c_C02_e_NAO_IMPLEMENTADA_e_nunca_produz_numero(empresa):
    r = _avaliar(empresa, _com_limiar(_real(), C_02=3.0))
    c02 = r["metricas"]["C-02"]
    assert c02["saida"] == "MARCA" and c02["causa"] == "NAO_IMPLEMENTADA"
    assert "valor" not in c02


def test_c_C04_nao_medido_marca_e_nunca_exclui(empresa):
    c04 = _avaliar(empresa, _real())["metricas"]["C-04"]
    assert (c04["saida"], c04["causa"]) == ("MARCA", "C-04_NAO_MEDIDO")


def test_c_conta_com_outra_descricao_nao_vira_numero(acv):
    """O plano de contas e o da empresa industrial; no DFP real de 2024, 17 dos 467 emissores
    trazem outra descricao em 3.05 (banco: 'Resultado antes dos Tributos'). Numero seria
    lixo plausivel (F-02): o bloco marca e nao calcula."""
    dem = _demonstrativos("2024-12-31", CD)
    dem["DRE_con"][0]["DS_CONTA"] = "Resultado antes dos Tributos sobre o Lucro"
    acv.capturar("2025-04-10T12:00:00Z", "dfp", 2024, dem,
                 indice=[TL._idx("2024-12-31", "1", "2025-03-20", cd=CD, categ="DFP")])
    r = _avaliar(acv, _com_limiar(_real(), C_01=3.5))
    c01 = r["metricas"]["C-01"]
    assert (c01["saida"], c01["causa"]) == ("MARCA", "PLANO_DE_CONTAS_DIFERENTE")
    assert "valor" not in c01 and r["saida"] != "REPROVA"


def test_c_sem_despesa_financeira_liquida_a_cobertura_e_indefinida_nao_zero(acv):
    _capturar(acv, "2025-04-10T12:00:00Z", 2024, CD, resfin=40)
    r = _avaliar(acv, _com_limiar(_real(), C_01=3.5))
    c01 = r["metricas"]["C-01"]
    assert (c01["saida"], c01["causa"]) == ("MARCA", "INDEFINIDA") and "valor" not in c01


# ── d. a 63a: o nivel corta, a tendencia marca ───────────────────────────────

def test_d_a_63a_vem_do_yaml_nivel_corta_tendencia_marca(empresa):
    P = _real()
    assert "HIBRIDO" in P["nivel_ou_tendencia"]["resposta"]
    assert P["nivel_ou_tendencia"]["tendencia_estado"] == "AGUARDA_SERIE"
    for cod in ("C-01", "C-03", "C-05"):
        assert P["metricas"][cod]["leitura"] == {"nivel": "CORTA", "tendencia": "MARCA"}
    r = _avaliar(empresa, _com_limiar(P, C_01=3.5))
    c01 = r["metricas"]["C-01"]
    assert c01["saida"] == "REPROVA"                     # o nivel corta
    assert c01["tendencia"] == {"saida": "MARCA", "causa": "AGUARDA_SERIE"}  # a tendencia nao


def test_d_a_tendencia_nunca_reprova_ainda_que_o_yaml_diga_que_o_nivel_marca(empresa):
    """Troque no YAML o que o nivel faz: o comportamento muda sem mudar codigo."""
    P = _com_limiar(_real(), C_01=3.5)
    P["metricas"]["C-01"]["leitura"]["nivel"] = "MARCA"
    c01 = _avaliar(empresa, P)["metricas"]["C-01"]
    assert (c01["saida"], c01["causa"]) == ("MARCA", "NIVEL_SO_MARCA")


# ── e. a contagem: so numero, sem nome, sem CD_CVM ───────────────────────────

def _capturar_varios(acv, quando, ano, empresas):
    """UMA captura do DFP do ano com varias empresas: capturas sucessivas do mesmo ano se
    substituem (a vigente e a ultima), como no acervo real."""
    dem, idx = {}, []
    for cd, v in empresas.items():
        for nome, linhas in _demonstrativos(f"{ano}-12-31", cd, **v).items():
            dem.setdefault(nome, []).extend(linhas)
        idx.append(TL._idx(f"{ano}-12-31", "1", f"{ano + 1}-03-20", cd=cd, categ="DFP"))
    acv.capturar(quando, "dfp", ano, dem, indice=idx)


def _universo_sintetico(acv):
    """Tres industriais (cobertura 3, 1,5 e 0,5), um banco e uma sem dado."""
    cobertura = {"099010": (300, -100), "099011": (150, -100), "099012": (50, -100)}
    _capturar_varios(acv, "2025-04-10T12:00:00Z", 2024,
                     {cd: dict(ebit=e, resfin=r) for cd, (e, r) in cobertura.items()})
    cad = {int(cd): IND for cd in cobertura}
    cad.update({99020: "Bancos", 99030: IND})            # 99030 nao tem DFP capturado
    return [_avaliar(acv, _real(), cd=cd, cadastro=cad, n=5) for cd in
            list(cobertura) + ["099020", "099030"]]


def test_e_a_contagem_por_corte_e_ponto_da_grade(acv):
    P = _real()
    aval = _universo_sintetico(acv)
    c = B.contar(aval, P)
    grade_c01 = [str(p["valor"]) for p in P["metricas"]["C-01"]["grade"]]
    assert list(c["cortes"]["C-01"]["grade"]) == grade_c01
    n = {float(k): v for k, v in c["cortes"]["C-01"]["grade"].items()}
    # coberturas 3, 1,5 e 0,5: o numero que SAIRIA em cada ponto (reprova abaixo do corte)
    for ponto, esperado in ((0.5, 0), (1.0, 1), (1.5, 1), (2.0, 2), (3.0, 2), (3.5, 3)):
        assert B.contar_em(aval, P, "C-01", ponto) == esperado, ponto
    assert sum(n.values()) == sum(B.contar_em(aval, P, "C-01", p) for p in n)
    assert c["cortes"]["C-01"]["com_valor"] == 3
    assert c["regime"] == {"RECUSA_REGIME": 1, "EXIGE_DOSSIE": 0}
    assert c["sem_dado"] == 1 and c["universo_total"] == 5
    assert c["nao_implementadas"] == ["C-02"]


def test_e_a_contagem_do_C05_usa_a_grade_dele(acv):
    P = _real()
    c = B.contar(_universo_sintetico(acv), P)
    assert list(c["cortes"]["C-05"]["grade"]) == ["0.5", "1.0", "1.5"]


def test_e_a_saida_da_contagem_e_so_numero(acv):
    c = B.contar(_universo_sintetico(acv), _real())
    texto = json.dumps(c, sort_keys=True)
    for proibido in ("099010", "99010", "099020", "Bancos", "Alimentos", "cd_cvm", "preco"):
        assert proibido not in texto, proibido

    def so_numero(x):
        if isinstance(x, dict):
            return all(isinstance(k, str) and so_numero(v) for k, v in x.items())
        if isinstance(x, list):
            return all(isinstance(v, str) for v in x)          # so os codigos C-0x
        return isinstance(x, int) and not isinstance(x, bool)
    assert so_numero(c)


# ── f. so o documento conhecido na data, pelo leitor, nunca pelo DT_REFER ────

def test_f_modo_da_captura_usa_so_o_que_estava_capturado_na_data(acv):
    _capturar(acv, "2024-04-10T12:00:00Z", 2023, CD, ebit=300)
    _capturar(acv, "2025-03-26T12:00:00Z", 2024, CD, ebit=900)
    r = _avaliar(acv, _real(), ate=dt.date(2025, 2, 1))
    assert r["exercicio"]["dt_refer"] == "2023-12-31"
    assert r["metricas"]["C-01"]["valor"] == Decimal(3)
    r = _avaliar(acv, _real(), ate=dt.date(2025, 4, 1))
    assert r["exercicio"]["dt_refer"] == "2024-12-31"
    assert r["metricas"]["C-01"]["valor"] == Decimal(9)


def test_f_modo_dt_receb_nunca_usa_o_DT_REFER(acv):
    """O DFP de 2024 tem DT_REFER 31/12/2024, anterior a 01/02/2025, e so foi RECEBIDO em
    25/03/2025. Pelo DT_REFER ele entraria; pelo DT_RECEB, nao."""
    _capturar(acv, "2026-09-24T12:00:00Z", 2023, CD, receb="2024-03-20", ebit=300)
    _capturar(acv, "2026-09-24T12:00:00Z", 2024, CD, receb="2025-03-25", ebit=900)
    antes = _avaliar(acv, _real(), ate=dt.date(2025, 2, 1), conhecimento="dt_receb")
    assert antes["exercicio"]["dt_refer"] == "2023-12-31"
    assert antes["exercicio"]["dt_receb"] == "2024-03-20"
    assert antes["metricas"]["C-01"]["valor"] == Decimal(3)
    depois = _avaliar(acv, _real(), ate=dt.date(2025, 3, 25), conhecimento="dt_receb")
    assert depois["exercicio"]["dt_refer"] == "2024-12-31"
    assert depois["metricas"]["C-01"]["valor"] == Decimal(9)


def test_f_o_modo_da_captura_antes_da_primeira_captura_nao_responde_nada(acv):
    _capturar(acv, "2026-09-24T12:00:00Z", 2024, CD)
    r = _avaliar(acv, _real(), ate=dt.date(2025, 6, 30))
    assert r["exercicio"] is None
    assert r["saida"] == "MARCA" and r["metricas"]["C-01"]["causa"] == "SEM_DADO"


def test_f_sem_dado_admite_com_marcacao_e_nao_exclui(acv):
    r = _avaliar(acv, _com_limiar(_real(), C_01=3.5))
    assert r["saida"] == "MARCA" and B.universo([r], _real()) == [r]       # P-16b


def test_f_o_modulo_pede_o_documento_ao_leitor_e_nao_olha_dt_refer():
    fonte = open(os.path.join(AQUI, "bloco_c.py"), encoding="utf-8").read()
    assert "leitor_cvm" in fonte and "zipfile" not in fonte


# ── a fronteira: o bloco NAO esta ligado ao motor (P-30 parte 1) ────────────

def test_o_bloco_nao_esta_ligado_ao_alocar_nem_ao_motor_de_aporte():
    """Decisao desta sessao: o bloco existe como codigo e como contagem, e nenhum modulo do
    motor o importa. Ligar e a parte 2 da P-30 -- e quando ligar, este teste muda de proposito,
    junto com o regime de `bloco_C_solvencia` em test_alocacao.py."""
    for f in sorted(os.listdir(AQUI)):
        if f.endswith(".py") and not f.startswith("test_") and f != "bloco_c.py":
            assert "bloco_c" not in open(os.path.join(AQUI, f), encoding="utf-8").read(), f


# ── o modulo nao tem literal de corte (CX-06, por AST) ───────────────────────

PERMITIDOS = {0, 1}                       # identidade e sinal; nenhum corte e 0 ou 1


def _literais(fonte):
    import ast
    return sorted({(n.lineno, n.value) for n in ast.walk(ast.parse(fonte))
                   if isinstance(n, ast.Constant) and type(n.value) in (int, float)
                   and n.value not in PERMITIDOS})


@pytest.mark.repositorio
def test_cx06_o_modulo_nao_tem_literal_numerico_de_politica():
    fonte = open(os.path.join(AQUI, "bloco_c.py"), encoding="utf-8").read()
    assert _literais(fonte) == []


@pytest.mark.repositorio
@pytest.mark.parametrize("literal", ["1.5", "3.0", "7e-1", "1_5", "0.5"],
                         ids=["1.5", "3.0", "expoente", "separador", "0.5"])
def test_cx06_a_guarda_pega_um_literal_plantado(literal):
    """Mutacao (5-B.4): planto um corte no codigo, em notacoes diferentes do mesmo valor, e a
    guarda tem de acusar. Sem este, o teste acima passaria com uma guarda que nao ve nada."""
    fonte = open(os.path.join(AQUI, "bloco_c.py"), encoding="utf-8").read()
    ponto = "def sai_do_universo"
    assert fonte.count(ponto) == 1, "o ponto de injecao mudou; a prova perdeu o alvo"
    mutante = fonte.replace(ponto, f"_CORTE_PLANTADO = {literal}\n\n\n{ponto}")
    compile(mutante, "bloco_c.py", "exec")
    assert _literais(mutante), literal


# ── o cadastro: a enumeracao OBSERVADA do SETOR_ATIV (P-18) ──────────────────

def test_p18_a_enumeracao_e_observada_com_procedencia_e_conta_todos_os_valores():
    s = _real()["setor_ativ"]
    assert s["status"] == "OBSERVADO"
    for campo in ("data", "url", "sha256", "linhas", "distintos"):
        assert str(s[campo]).strip(), campo
    assert len(s["valores"]) == s["distintos"] and sum(s["valores"].values()) == s["linhas"]
    assert set(s["financeira"]) <= set(s["valores"]) and set(s["a_decidir"]) <= set(s["valores"])
    assert not set(s["financeira"]) & set(s["a_decidir"])


def test_p18_o_leitor_do_cadastro_falha_fora_da_enumeracao(tmp_path):
    cab = "CD_CVM;SETOR_ATIV\n"
    ok = tmp_path / "ok.csv"
    ok.write_bytes((cab + "1;Bancos\n2;Energia Elétrica\n").encode("latin-1"))
    assert B.ler_cadastro(str(ok), _real()) == {1: "Bancos", 2: "Energia Elétrica"}
    novo = tmp_path / "novo.csv"
    novo.write_bytes((cab + "1;Criptomoedas\n").encode("latin-1"))
    with pytest.raises(B.SetorForaDaEnumeracao, match="Criptomoedas"):
        B.ler_cadastro(str(novo), _real())


def test_p18_cd_cvm_com_dois_setores_diferentes_e_recusado(tmp_path):
    p = tmp_path / "amb.csv"
    p.write_bytes("CD_CVM;SETOR_ATIV\n1;Bancos\n1;Alimentos\n".encode("latin-1"))
    with pytest.raises(B.CadastroAmbiguo):
        B.ler_cadastro(str(p), _real())
    q = tmp_path / "dup.csv"                     # a duplicata EXATA (107 no dado real) e uma linha
    q.write_bytes("CD_CVM;SETOR_ATIV\n1;Bancos\n1;Bancos\n".encode("latin-1"))
    assert B.ler_cadastro(str(q), _real()) == {1: "Bancos"}


def test_a_politica_real_carrega_com_o_mesmo_caminho_do_yaml_de_teste(tmp_path):
    P = _real()
    assert _yaml_de_teste(tmp_path, P) == yaml.safe_load(
        io.StringIO(yaml.safe_dump(P)))
