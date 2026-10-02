# -*- coding: utf-8 -*-
"""Testes da camada de alocacao v3. Camadas 1, 3, 4 e 5 do manual.

Cada achado das auditorias de 02 e 03/09/2026 tem pelo menos um teste que FALHA na
versao anterior e passa nesta. O docstring de cada um nomeia o achado.
"""
import os, sys, re, ast, math, copy, dataclasses, datetime as dt, types
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pytest
from motor import carregar as carregar_custos, val
from alocacao import (simular_custo as al_simular, Estado, Divida, Objetivo,
                      MatchEmpregador, carregar_politica,
                      alocar, catalogo, reserva_alvo, fracao_rv, arrasto_anualizado,
                      custo_pct_aportado, custo_de_discordar, g3_atrito, g4_dominancia,
                      g6_coerencia_funcao, g5_status, retorno_liquido_aa, aliquota_ir_rf,
                      casa_duracao,
                      motor_aporte, vencimento_maximo, AQUI, g2_reserva,
                      compor_reserva, segmentos_de_capacidade, InsumoBloqueado,
                      carregar_catalogo, _resolve, _conferir_invariantes,
                      fase_aporte, fase_universo, distribuir_por_funcao,
                      custo_entrada_fixo_pct, g0_match_empregador, g1_divida,
                      g7_tese_registrada, g8_compromisso_de_carrego)
from tese import validar_tese, validar_carrego, impressao, impressao_carrego
import ambiente

C, P = carregar_custos(), carregar_politica()
BASE = dict(despesa_mensal=4500, reserva_atual=27000, aporte_mensal=500, horizonte_anos=25)
TETO_COMP = P["compromissos"]["maximo_anos"]


def tese_valida(rid="hash11"):
    t = dict(ativo_id=rid, funcao="APOSTA", catalogo="ESPECULATIVO",
             dt_classificacao=dt.date(2026, 9, 3), K01_perda_maxima_aceita=1.0,
             K02_tese="ate 31/12/2031 existe ETF de cripto na B3 com taxa abaixo de 0,5% ao ano",
             K03_prazo=dt.date(2031, 12, 31),
             K04_falsificacao="a taxa de administracao do veiculo subir acima de 1,5% ao ano",
             K05_liquidez_saida_dias=2,
             L_teste_de_classificacao=dict(rodado_em=dt.date(2026, 9, 3), reprova=["A-06"]))
    t["impressao"] = impressao(t)
    ok, probs, _ = validar_tese(t, dt.date(2026, 9, 3), TETO_COMP)
    assert ok, probs
    return {rid: dict(valida=True, motivo="", avisos=[], tese=t)}


def carrego_valido(rid="td_ipca", venc=dt.date(2035, 5, 15), teto=0.15):
    c = dict(ativo_id=rid, funcao="PROTECAO_REAL", catalogo="BUY_AND_HOLD",
             dt_registro=dt.date(2026, 9, 3), C01_horizonte_de_carrego=venc,
             C02_compromisso="carrego o NTN-B Principal ate o vencimento, travando juro "
                             "real de 6,8% ao ano na data da compra",
             C03_condicao_de_venda_antecipada="necessidade de caixa que a reserva de "
                             "emergencia nao cobre, comprovada por despesa efetiva",
             C04_custo_de_quebrar=dict(cenario="+2 p.p.", perda_estimada_pct=0.16,
                                       fonte_da_estimativa="duration x choque"),
             C05_teto_da_funcao=teto, C06_reconhecimento=True)
    c["impressao"] = impressao_carrego(c)
    ok, probs, _, dur = validar_carrego(c, dt.date(2026, 9, 3), TETO_COMP)
    assert ok, probs
    return {rid: dict(valida=True, motivo="", avisos=[], duracao_anos=dur, carrego=c)}


# ══ A OBJECAO DO USUARIO: ativo sem regra ganha regra, nao vira ausencia ═════
def test_ipca_volta_ao_universo_com_compromisso_registrado():
    """A objecao do usuario em 03/09/2026: 'investimentos nao devem sair por nao ter
    regras; devem ser definidas regras para os que nao tem'. A versao 1.1.0 tirava o
    Tesouro IPCA+ da carteira porque nenhuma funcao do modelo descrevia o que ele faz
    — LASTRO exige perda nominal zero e ele tem marcacao; DATADO exige um prazo e nao
    havia prazo. Ele caiu no vao entre as duas. A funcao PROTECAO_REAL e o registro
    CARREGO fecham o vao."""
    sem = alocar(Estado(**BASE), C, P, teses={}, carregos={})
    assert "td_ipca" not in sem["alvo"]["pesos"]
    assert any(p.id == "G8_carrego:td_ipca" for p in sem["pendencias"]), \
        "sem registro, a rota tem de virar PENDENCIA — nao sumir"

    com = alocar(Estado(**BASE), C, P, teses={}, carregos=carrego_valido())
    assert com["alvo"]["pesos"].get("td_ipca", 0) > 0
    assert com["alvo"]["blocos"]["protecao_real"] > 0
    assert com["alvo"]["pesos"]["td_ipca"] <= 0.15 + 1e-9, "o teto vem do C05 do registro"


def carrego_regra_decidida(rid="td_ipca"):
    """O mesmo registro de `carrego_valido`, em REGRA_DECIDIDA: C02 e C04 esperam a compra."""
    c = dict(carrego_valido(rid)[rid]["carrego"], estado="REGRA_DECIDIDA",
             C02_compromisso="AGUARDA_COMPRA", C04_custo_de_quebrar="AGUARDA_COMPRA")
    c["impressao"] = impressao_carrego(c)
    ok, probs, av, dur = validar_carrego(c, dt.date(2026, 9, 3), TETO_COMP)
    assert ok, probs
    assert any("G8 NAO libera peso" in a for a in av), "o validador tem de anunciar"
    return {rid: dict(valida=True, motivo="", avisos=av, duracao_anos=dur, carrego=c)}


def test_G07_regra_decidida_nao_libera_peso_no_g8():
    """G-07: o validador anuncia que o G8 NAO libera peso em REGRA_DECIDIDA, e o G8 liberava
    -- conferia so `valida` e `duracao_anos`. Com o registro valido e selado, a versao
    anterior dava 15% a `td_ipca`, uma posicao que nao existe. Agora: zero, e a pendencia
    diz o que falta (a compra), nao para registrar de novo o que ja foi registrado."""
    r = alocar(Estado(**BASE), C, P, teses={}, carregos=carrego_regra_decidida())
    assert "td_ipca" not in r["alvo"]["pesos"]
    assert r["alvo"]["blocos"]["protecao_real"] == 0
    pend = [p for p in r["pendencias"] if p.id == "G8_carrego:td_ipca"]
    assert len(pend) == 1, "a rota espera a compra -- nao pode sumir (P6)"
    assert "COMPROMISSO_ATIVO" in pend[0].pergunta and "Registrar" not in pend[0].pergunta


def test_G07_o_mesmo_registro_ativo_continua_liberando():
    """O conserto le o estado, nao a presenca do registro: o mesmo carrego, em
    COMPROMISSO_ATIVO, recebe o peso do C05 como antes."""
    r = alocar(Estado(**BASE), C, P, teses={}, carregos=carrego_valido())
    assert r["alvo"]["pesos"]["td_ipca"] == pytest.approx(0.15)


def test_G07_portao_e_validador_tem_o_mesmo_default_de_estado():
    """Registro sem `estado` vale COMPROMISSO_ATIVO nos dois lados; se um mudasse o default
    sozinho, o portao e o validador voltariam a discordar calados."""
    from alocacao import _estado_do_carrego
    import inspect, tese as T
    assert _estado_do_carrego({"carrego": {}}) == "COMPROMISSO_ATIVO"
    assert 'c.get("estado", "COMPROMISSO_ATIVO")' in inspect.getsource(T.validar_carrego)


def _td_ipca_do_repositorio_assinado():
    """O registro real de teses.yaml, assinado EM MEMORIA (nada gravado): sem `exemplo`,
    C06 verdadeiro e a impressao recalculada."""
    import yaml
    with open(os.path.join(AQUI, "teses.yaml"), encoding="utf-8") as f:
        c = dict(yaml.safe_load(f)["carregos"]["td_ipca"])
    c.pop("exemplo", None)
    c["C06_reconhecimento"] = True
    c["impressao"] = impressao_carrego(c)
    ok, probs, av, dur = validar_carrego(c, dt.date(2026, 9, 26), TETO_COMP)
    assert ok, probs
    return {"td_ipca": dict(valida=True, motivo="", avisos=av, duracao_anos=dur, carrego=c)}


def _reassinar(r):
    return [p for p in r["pendencias"] if p.id == "reassinar:td_ipca"]


def test_premissa_o_c03_do_repositorio_cita_9_meses():
    """Vacuidade: se o texto deixasse de citar a reserva, o alarme ficaria mudo."""
    from tese import meses_de_reserva_no_texto
    assert meses_de_reserva_no_texto(_td_ipca_do_repositorio_assinado()["td_ipca"]
                                     ["carrego"]) == 9


def test_premissa_meta_de_9_meses_nao_alarma():
    """Estabilidade baixa, sem dependente: 6 x 1,5 = 9 -- a meta que o C03 assinou."""
    e = Estado(**{**BASE, "estabilidade_renda": "baixa"})
    r = alocar(e, C, P, teses={}, carregos=_td_ipca_do_repositorio_assinado())
    assert _reassinar(r) == []


@pytest.mark.parametrize("mudanca, meta", [({"estabilidade_renda": "media"}, "6"),
                                           ({"estabilidade_renda": "baixa",
                                             "dependentes": 1}, "9.5")])
def test_premissa_meta_diferente_de_9_pede_reassinar(mudanca, meta):
    """Decisao dele, 26/09: o C03 fica com "9 meses" fixo e o sistema avisa quando a meta
    da reserva deixar de ser 9. Falha na versao anterior: nao havia pendencia nenhuma."""
    r = alocar(Estado(**{**BASE, **mudanca}), C, P, teses={},
               carregos=_td_ipca_do_repositorio_assinado())
    p = _reassinar(r)
    assert len(p) == 1
    assert p[0].pergunta.startswith("tese td_ipca desatualizada, reassinar?")
    assert f"meta vigente e {meta} meses" in p[0].pergunta


def test_premissa_alarma_mesmo_quando_o_g2_encerra():
    """Com a reserva curta o pipeline para na diretiva do G2 -- e e exatamente quando a
    reserva importa. O alarme nasce antes da fase de aporte para nao sumir ai."""
    r = alocar(Estado(**{**BASE, "reserva_atual": 9000}), C, P, teses={},
               carregos=_td_ipca_do_repositorio_assinado())
    assert r["alvo"] is None and len(_reassinar(r)) == 1


def test_premissa_registro_nao_assinado_nao_alarma():
    """Rascunho nao e tese: sem assinatura nao ha o que reassinar."""
    c = _td_ipca_do_repositorio_assinado()
    c["td_ipca"]["valida"] = False
    assert _reassinar(alocar(Estado(**BASE), C, P, teses={}, carregos=c)) == []


def test_cripto_volta_ao_universo_com_tese_registrada():
    com = alocar(Estado(**BASE), C, P, teses=tese_valida(), carregos={})
    assert com["alvo"]["pesos"].get("hash11", 0) > 0
    assert com["alvo"]["pesos"]["hash11"] <= P["tetos"]["aposta_pct"] + 1e-9


def test_registro_ausente_vira_pendencia_e_nao_exclusao():
    """A diferenca entre exclusao e pendencia e o que o output diz: uma rota sem
    registro nao foi rejeitada, esta esperando uma entrada que so o usuario pode dar.
    A instrucao tem de vir junto — 'preencha o registro' sem dizer ate quando nao e
    instrucao."""
    r = alocar(Estado(**BASE), C, P, teses={}, carregos={})
    ids = [p.id for p in r["pendencias"]]
    assert "G7_tese:hash11" in ids and "G8_carrego:td_ipca" in ids
    pend = next(p for p in r["pendencias"] if p.id == "G8_carrego:td_ipca")
    assert vencimento_maximo(P).isoformat() in pend.pergunta, \
        "a pendencia tem de dizer ate qual vencimento o teto de compromissos permite ir"
    assert "td_ipca" not in {x[0].id for x in r["universo"]["dominados"]}


def test_teto_de_compromisso_de_10_anos_barra_o_papel_longo():
    """Decisao do usuario: nenhum compromisso maior que 10 anos. E um teto ABSOLUTO,
    independente do horizonte — e por isso nao herda a fragilidade das posturas que
    amarram a duracao a um horizonte que o proprio usuario pode revisar."""
    c = dict(carrego_valido()["td_ipca"]["carrego"])
    c["C01_horizonte_de_carrego"] = dt.date(2060, 8, 15)
    c["impressao"] = impressao_carrego(c)
    ok, probs, _, dur = validar_carrego(c, dt.date(2026, 9, 3), TETO_COMP)
    assert not ok and dur > 30
    r = alocar(Estado(**BASE), C, P, teses={},
               carregos={"td_ipca": dict(valida=False, motivo="; ".join(probs),
                                         duracao_anos=dur, carrego=c)})
    assert "td_ipca" not in r["alvo"]["pesos"]


# ══ V-01 · desempate de horizonte declarado ══════════════════════════════════
def test_desempate_de_horizonte_e_parametro_e_nao_default_silencioso():
    """V-01: a versao 1.1.0 mudou o ROTULO e nao o comportamento — o conjunto de rotas
    eliminadas era identico ao da 1.0.0, e o REGISTRO afirmava 'so elimina se perder em
    todos'. Agora o comportamento e o mesmo POR ESCOLHA DECLARADA, e trocar a escolha
    e um commit no YAML."""
    assert P["portoes"]["G4_dominancia"]["desempate_preferencia_horizonte"] == \
        "menor_arrasto_no_horizonte"
    rotas = catalogo(C)
    P2 = copy.deepcopy(P); P2["portoes"]["G3_atrito"]["teto_custo_entrada_pct"] = 0.03
    dentro, _ = g3_atrito(rotas, C, P2, 500)
    dentro, _ = g5_status(dentro, P2)

    P2["portoes"]["G4_dominancia"]["desempate_preferencia_horizonte"] = "menor_arrasto_no_horizonte"
    vivos_a, dom_a, pref_a = g4_dominancia(dentro, C, 500, P2, 25)
    assert {x[0].id for x in pref_a} == {"ivvb11"}
    assert "ivvb11" not in {v[0].id for v in vivos_a}
    assert "ext_avenue" in {v[0].id for v in vivos_a}

    P2["portoes"]["G4_dominancia"]["desempate_preferencia_horizonte"] = "ambas"
    vivos_b, _, pref_b = g4_dominancia(dentro, C, 500, P2, 25)
    assert {"ivvb11", "ext_avenue"} <= {v[0].id for v in vivos_b}, \
        "no modo `ambas` as duas permanecem candidatas"

    P2["portoes"]["G4_dominancia"]["desempate_preferencia_horizonte"] = "usuario"
    vivos_c, _, _ = g4_dominancia(dentro, C, 500, P2, 25)
    assert not ({"ivvb11", "ext_avenue"} & {v[0].id for v in vivos_c}), \
        "no modo `usuario` nenhuma das duas recebe peso ate haver decisao"

    P3 = copy.deepcopy(P2)
    P3["portoes"]["G4_dominancia"]["desempate_preferencia_horizonte"] = "inventado"
    with pytest.raises(ValueError):
        g4_dominancia(dentro, C, 500, P3, 25)


def test_a_ordem_de_fato_inverte_entre_10_e_15_anos():
    rotas = {r.id: r for r in catalogo(C)}
    a = {h: (arrasto_anualizado(rotas["ivvb11"], C, 500, h),
             arrasto_anualizado(rotas["ext_avenue"], C, 500, h)) for h in (5, 10, 15, 30)}
    assert a[5][0] < a[5][1] and a[10][0] < a[10][1]
    assert a[15][0] > a[15][1] and a[30][0] > a[30][1]


def test_dominancia_verdadeira_continua_eliminando():
    r = alocar(Estado(**BASE), C, P, teses={}, carregos={})
    dom = {x[0].id for x in r["universo"]["dominados"]}
    assert "bova11_xp" in dom and "bova11" not in dom and "smal11" not in dom


# ══ V-02 · a interacao G3 × G4 deixa de ser silenciosa ═══════════════════════
def test_interacao_entre_g3_e_g4_e_reportada():
    """V-02: o G3 roda antes do G4, entao a Avenue e eliminada por atrito e nunca chega
    a dominancia — a tabela de inversao que o teste prova nunca aparecia em uso real.
    A ordem nao muda (esta declarada em decisoes.V01), mas a interacao passa a ser
    reportada: os dois portoes em sequencia produzem um resultado que nenhum dos dois
    produziria sozinho, e isso agora esta escrito no output."""
    r = alocar(Estado(**BASE), C, P, teses={}, carregos={})
    inter = r["universo"]["interacao_g3_g4"]
    assert inter, "nenhuma interacao reportada"
    ids = {x["rota"].id for x in inter}
    assert "ext_avenue" in ids
    av = next(x for x in inter if x["rota"].id == "ext_avenue")
    assert av["rival"].id == "ivvb11"
    assert 30 in av["horizontes_em_que_venceria"]


# ══ V-03 · literais fixos no Python ══════════════════════════════════════════
def test_horizonte_ir_do_g2_vem_do_yaml():
    """V-03: o `180` estava fixo no Python, enquanto o G1 — tres funcoes acima — lia o
    analogo do YAML. Assimetria entre dois portoes que fazem a mesma comparacao, e o
    parametro decide se a poupanca isenta vence ou perde para o RDB tributado."""
    assert "horizonte_ir_dias" in P["portoes"]["G2_reserva"]
    P2 = copy.deepcopy(P); P2["portoes"]["G2_reserva"]["horizonte_ir_dias"] = 900
    e = Estado(**{**BASE, "reserva_atual": 0})
    a = alocar(e, C, P, teses={}, carregos={})["diretiva"].memoria["retorno_liquido_aa"]
    b = alocar(e, C, P2, teses={}, carregos={})["diretiva"].memoria["retorno_liquido_aa"]
    assert b > a, "aliquota menor tem de elevar o retorno liquido"


def test_k_max_vem_do_yaml():
    """V-03: era default na assinatura da funcao, e e decisao de politica pura."""
    assert "k_max" in P["motor_aporte"]
    e = Estado(**{**BASE, "aporte_mensal": 3000,
                  "posicoes": {"bova11": 900, "pibb11": 900, "divo11": 900,
                               "smal11": 900, "ivvb11": 900, "acao_zero": 900,
                               "td_selic": 900}})
    alvo = alocar(e, C, P, teses={}, carregos={})["alvo"]
    P2 = copy.deepcopy(P); P2["motor_aporte"]["k_max"] = 5
    r1 = motor_aporte(e, alvo, C, P)
    r2 = motor_aporte(e, alvo, C, P2)
    assert r1["k_max"] == 2 and r2["k_max"] == 5
    assert len(r2["ordens"]) > len(r1["ordens"])


@pytest.mark.repositorio   # 146b: le o repositorio, a mutacao exclui
def test_nenhum_literal_de_politica_fixo_no_modulo():
    """V-03, o caminho inverso do teste de cobertura: a cobertura garante que toda
    chave do YAML e lida; este garante que nao ha constante de politica fixa no
    Python. A lista de excecoes e explicita de proposito."""
    import re
    fonte = open(os.path.join(AQUI, "alocacao.py"), encoding="utf-8").read()
    corpo = fonte.split("# ══ PORTOES ══")[1]
    corpo = re.sub(r'""".*?"""', "", corpo, flags=re.S)
    corpo = re.sub(r"#.*", "", corpo)
    corpo = re.sub(r'"[^"]*"|\'[^\']*\'', "", corpo)
    PERMITIDOS = {
        "0", "1", "2", "12", "100",      # aritmetica, meses do ano, conversao para %
        "3", "4", "5",                   # indices de tupla e casas de arredondamento
        "1e-9", "1e-12", "1e-6",         # tolerancias de ponto flutuante
        "0.0", "1.0", "0.01", "365.25",  # identidades, centavo, dias do ano
    }
    achados = set(re.findall(r"(?<![\w.])(\d+\.?\d*(?:e-?\d+)?)(?![\w.])", corpo)) - PERMITIDOS
    assert not achados, f"literais numericos nao declarados no modulo: {sorted(achados)}"


# ══ V-06 a V-15 ══════════════════════════════════════════════════════════════
def test_fracao_rv_realizada_e_reportada():
    """V-06: as invariantes verificavam soma 1,0 e os tetos, mas nao que o peso
    alocado a CRESCIMENTO e igual a p_rv. Como a sobra pode migrar de CRESCIMENTO
    para o bloco conservador, a fracao impressa no cabecalho podia divergir da
    realizada sem que nada alertasse."""
    r = alocar(Estado(**BASE), C, P, teses={}, carregos={})
    a = r["alvo"]
    assert "fracao_rv_realizada" in a
    rv = sum(w for rid, w in a["pesos"].items()
             if next(v[0] for v in r["universo"]["vivos"]
                     if v[0].id == rid).funcao == "CRESCIMENTO")
    assert abs(a["fracao_rv_realizada"] - rv) < 1e-9
    if abs(a["fracao_rv_realizada"] - a["blocos"]["rv"]) > 1e-6:
        assert any("REALIZADA" in x for x in a["alertas"])


def test_casa_duracao_usa_o_menor_prazo_entre_os_objetivos():
    """V-07: com `any`, um objetivo de 20 anos admitia um papel de duracao 8,7 no
    bloco DATADO — e o bloco era dimensionado pela necessidade TOTAL, que inclui o
    objetivo de 1 ano. Bloco agregado, casamento isolado."""
    e = Estado(**{**BASE, "aporte_mensal": 3000,
                  "objetivos": [Objetivo("carro", 60_000, 3),
                                Objetivo("apartamento", 300_000, 20)]})
    r = alocar(e, C, P, teses={}, carregos=carrego_valido())
    assert r["alvo"]["bloco_por_rota"].get("td_ipca") != "DATADO", \
        "duracao 8,7a nao casa com o MENOR prazo (3a) dos objetivos que o bloco financia"
    # ele nao desaparece: cai em PROTECAO_REAL, que e a funcao que descreve o que ele faz
    assert r["alvo"]["bloco_por_rota"].get("td_ipca") == "PROTECAO_REAL"


def test_objetivo_inatingivel_nao_e_silenciado():
    """V-08: `min(1.0, total/base)` alocava 100% do bloco conservador sem dizer que a
    meta e inalcancavel com o aporte e o prazo declarados."""
    e = Estado(**{**BASE, "aporte_mensal": 500,
                  "objetivos": [Objetivo("apartamento", 400_000, 5)]})
    r = alocar(e, C, P, teses={}, carregos={})
    assert any("faltam R$" in a for a in r["alvo"]["alertas"])


def test_funcao_sem_rota_viavel_gera_alerta():
    """V-09: SEGURO_CAUDA sai 0% em todos os cenarios porque sua unica rota e
    eliminada por atrito, e nada no output dizia isso — uma funcao inteira do modelo
    morrendo em silencio."""
    r = alocar(Estado(**BASE), C, P, teses={}, carregos={})
    assert any("SEGURO_CAUDA" in a and "morta na pratica" in a for a in r["alvo"]["alertas"])


def test_g6_nao_muta_as_rotas_recebidas():
    """V-12: `cenarios.py` mantem um ROTAS de outra chamada de catalogo(); mutar
    `r.funcoes` no lugar fazia as rotas nomeadas no output nao serem as filtradas."""
    rotas = catalogo(C)
    antes = {r.id: list(r.funcoes) for r in rotas}
    for r in rotas:
        if r.id == "rdb_100": r.liquidez_dias = 30
    ok, ruins = g6_coerencia_funcao(rotas, P)
    assert any(r.id == "rdb_100" for r, f, m in ruins)
    assert {r.id: list(r.funcoes) for r in rotas} == antes, "g6 mutou a lista de entrada"


def test_universo_separa_elegibilidade_de_alocacao():
    """V-13: as tres rotas de LIQUIDEZ atravessam todos os portoes e nunca podem
    receber peso — a reserva e tratada pelo G2. Contar as duas coisas na mesma linha
    inflava o numero de 'rotas vivas' do output."""
    r = alocar(Estado(**BASE), C, P, teses={}, carregos={})
    u = r["universo"]
    assert len(u["alocaveis"]) < len(u["vivos"])
    assert not any(v[0].funcao == "LIQUIDEZ" for v in u["alocaveis"])


def test_freio_avalia_a_compra_executada():
    """V-14: o freio supunha `min(deficit, aporte)` e podia excluir uma rota que, de
    fato, nao cruzaria a banda — a ordem real e limitada tambem por k_max e lote."""
    e = Estado(**{**BASE, "posicoes": {"bova11": 9000, "td_selic": 1000}})
    r = motor_aporte(e, alocar(e, C, P, teses={}, carregos={})["alvo"], C, P)
    for a in r["alertas"]:
        assert "compra_avaliada" in a, "o alerta tem de dizer que compra foi avaliada"


def test_nota_de_bases_no_output_do_motor():
    """V-15: `peso_atual` usa V, `deficit` usa V+A. Correto e nao explicado."""
    e = Estado(**{**BASE, "posicoes": {"bova11": 2400, "td_selic": 1300}})
    r = motor_aporte(e, alocar(e, C, P, teses={}, carregos={})["alvo"], C, P)
    assert "nota_bases" in r and "V+A" in r["nota_bases"]


# ══ A-03 · cobertura do YAML, nas duas direcoes ══════════════════════════════
# ── P-28 · o proprio guarda tinha um vao ─────────────────────────────────────
# O teste abaixo existia desde 02/09 e varria SEIS secoes de politica.yaml, lendo
# TRES modulos. O arquivo tem dezenove secoes e o motor tem onze modulos. Foi por
# esse vao que a secao `revisao` entrou, ficou declarada e nunca foi lida por
# ninguem — e o guarda passou verde o tempo todo. Um teste de cobertura com escopo
# escrito a mao mede o escopo, nao a cobertura.
#
# A correcao tem tres partes, e a terceira e a que importa:
#   1. varrer TODAS as secoes e TODOS os modulos;
#   2. cada secao precisa de um REGIME declarado, com o motivo escrito;
#   3. secao nova sem regime FALHA. Nao ha default. Esquecer passa a ser barulhento.
#
# Os regimes:
#   OPERACIONAL   — o motor le. Chave nao lida e defeito, salvo divida inventariada.
#   REGISTRO      — log de decisao ou de fonte. E testemunho: existe para ser lido por
#                   gente, e o motor consome so os campos que o codigo nomeia.
#   ESPECIFICACAO — comportamento ESCRITO e ainda NAO ligado ao motor. Precisa de
#                   pendencia. E a categoria honesta para o que eu especifiquei numa
#                   sessao e nao implementei: some se ninguem contar, e agora conta.
OPERACIONAL, REGISTRO, ESPECIFICACAO = "OPERACIONAL", "REGISTRO", "ESPECIFICACAO"

REGIME_DAS_SECOES = {
    "funcoes":       (OPERACIONAL,   "define as funcoes de carteira que o G6 exige"),
    "portoes":       (OPERACIONAL,   "os portoes e a ordem deles (P-07)"),
    "crescimento":   (OPERACIONAL,   "fracao em renda variavel e ajuste de horizonte"),
    "tetos":         (OPERACIONAL,   "limites que o alocador aplica"),
    "compromissos":  (OPERACIONAL,   "teto absoluto de duracao — decisao A04"),
    "motor_aporte":  (OPERACIONAL,   "regras do aporte mensal"),
    "corretora":     (OPERACIONAL,   "pontuacao do ranking de instituicoes (N-01)"),
    "aporte_extraordinario": (OPERACIONAL, "destino do dinheiro fora do aporte mensal"),
    "sleeves":       (OPERACIONAL,   "indexado x selecao ativa"),
    "revisao":       (OPERACIONAL,   "cadencia e gatilhos de revisao — DIVIDA P-28"),
    "decisoes":      (REGISTRO,      "log das decisoes do usuario, com data e resposta; "
                                     "o motor le os campos que o codigo nomeia, o resto "
                                     "e a memoria de por que a decisao foi essa"),
    "fontes":        (REGISTRO,      "procedencia dos dados: arquivo, hash, cobertura"),
    "meta":          (REGISTRO,      "versao, data de emissao e changelog do arquivo"),
    "fora_de_escopo":(REGISTRO,      "o que saiu, quando, por que, e o que faz reentrar"),
    "doutrina_P6":   (REGISTRO,      "a doutrina e as tres vezes em que eu a violei"),
    "fase_A_recalculada": (REGISTRO, "o recalculo M-01 e o que ele mediu"),
    "limitacoes_declaradas": (REGISTRO, "o que o motor NAO faz, com a direcao do vies"),
    # 18/09: era ESPECIFICACAO com a pendencia P-29, e deixou de ser. O E-06 dizia que
    # o pre-registro declarava guardas que nada executava; `preregistro.py` passou a ler
    # `variantes_permitidas` (o `m` orcado) e os nomes das estrategias (integridade do
    # diario), e a propria guarda cobrou a reclassificacao. NAO virou OPERACIONAL: 67
    # das suas chaves nunca serao lidas por codigo nenhum, porque sao TESTEMUNHO —
    # D1..D7, `origem`, `nota_do_custo`, os `resultado` de 05/09. Inventaria-las como
    # divida seria registrar 67 promessas que ninguem pretende cumprir, e o
    # `test_P28_a_divida_de_cobertura_nao_apodrece` as guardaria para sempre.
    # O papel de ESPECIFICACAO nao se perdeu — virou NUMERO: `m_orcado - m_executado`
    # conta quantos testes pre-registrados nunca rodaram, e
    # `test_preregistro.py::test_o_que_o_pre_registro_promete_e_nao_executou_e_CONTADO`
    # o prende. Contagem que decai vale mais que 67 linhas de promessa.
    "estrategias_pre_registradas": (REGISTRO, "o que foi pre-registrado e o que "
                                     "aconteceu; a unica chave operacional e "
                                     "`variantes_permitidas`, lida por preregistro.py "
                                     "para calcular o `m` orcado (P-29 fechada)"),
    "pesquisa":      (OPERACIONAL,   "a familia de testes e o corte que ela exige; "
                                     "preregistro.py le TODA chave daqui — foi de "
                                     "proposito que este bloco nasceu pequeno e "
                                     "OPERACIONAL em vez de crescer dentro do "
                                     "`estrategias_pre_registradas`, que e "
                                     "ESPECIFICACAO e nao cobra leitura de ninguem"),
    "armazem":       (OPERACIONAL,   "aviso e teto do bucket do R2 (P-57, cobranca "
                                     "zero); quem le e fase0/armazem.py -- por isso "
                                     "_fontes_do_motor inclui o fase0"),
    "regimes_de_captura": (OPERACIONAL, "P7: o acervo cuja captura roda sozinha, com o "
                                     "executor, o passo e a execucao agendada que o "
                                     "provou; quem le e fase0/manifesto_cvm.py"),
    "cadencias_de_captura": (OPERACIONAL, "P-150: o dia em que uma captura sem HEAD pede "
                                          "a fonte; quem le e fase0/capturar_eventos_b3.py"),
    "bloco_C_solvencia":            (ESPECIFICACAO, "P-30: especificado em 05/09, "
                                     "nenhum modulo aplica"),
    "regime_instituicao_financeira":(ESPECIFICACAO, "P-31: especificado em 05/09, "
                                     "nenhum modulo aplica"),
}

# Prosa: campo cuja funcao E ser lido por gente. `*` casa UM segmento.
DOCUMENTAL = (
    "*.nome", "*.descricao", "*.*.nome", "*.*.descricao",
    "*.nota", "*.*.nota", "*.*.*.nota",
    "*.regra", "*.*.regra", "*.nota_ir", "*.*.nota_ir",
    "*.desativado_em", "*.*.desativado_em",
    "*.motivo_da_desativacao", "*.*.motivo_da_desativacao",
    "*.pergunta", "*.*.pergunta", "*.custo_de_ignorar", "*.*.custo_de_ignorar",
    "*.justificativa", "*.*.justificativa", "*.*.*.justificativa",
    "*.decidido_em", "*.decidido_por", "*.aplica_a", "*.nao_aplica_a",
    # prosa da secao corretora, nomeada campo a campo — a lista e longa de proposito:
    # cada linha aqui e uma frase que alguem escreveu e ninguem executa.
    "corretora.justificativa_da_ordem", "corretora.nota_cobertura",
    "corretora.*.formula_verificada", "corretora.*.limitacao_que_viaja_com_o_dado",
    "corretora.*.por_que_normalizada_importa", "corretora.*.motivo_de_nao_pontuar",
    "corretora.*.nota_de_coerencia", "corretora.*.o_que_so_o_usuario_pode_fazer",
    "corretora.*.por_que_importa_mais_do_que_o_peso_sugere",
    "corretora.*.e_uma_decisao_nao_uma_omissao", "corretora.*.argumento_para_peso_negativo",
    "corretora.*.o_que_ela_decide", "corretora.*.motivo",
    "corretora.reclamacoes.escala", "corretora.reclamacoes.indice",
    "corretora.reclamacoes.fonte",
    "sleeves.*.nota", "aporte_extraordinario.*.nota_de_lote",
)

# Divida inventariada: chave OPERACIONAL declarada e nao lida, com dono e numero.
# Uma entrada aqui e uma promessa registrada, nao uma isencao — o terceiro teste
# quebra se a entrada deixar de existir ou passar a ser lida.
DIVIDA_DE_COBERTURA = {
    "revisao.cadencia":                 "P-28",
    "revisao.mes":                      "P-28",
    "revisao.gatilhos_extraordinarios": "P-28",
    "corretora.cobertura_e_penalidade": "P-32",
    "corretora.fora_do_ranking":        "P-32",
    "sleeves.indexado":                 "P-34",
    "sleeves.indexado.n_ativos_efetivo": "P-34",
    "sleeves.indexado.exige_selecao":   "P-34",
    "sleeves.selecao_ativa.exige_selecao": "P-34",
    "sleeves.selecao_ativa.bloqueado_por": "P-34",
    "sleeves.selecao_ativa.meses_para_montar": "P-34",
}

DINAMICO = {"alta", "media", "baixa", "nominal_zero", "limitada", "total"}


PROSA_MINIMA = 120   # caracteres

def _chaves(no, prefixo=""):
    if isinstance(no, dict):
        for k, v in no.items():
            if str(k).startswith("_"): continue
            yield f"{prefixo}{k}", k, v
            yield from _chaves(v, f"{prefixo}{k}.")


def _e_prosa(caminho, valor):
    """Duas portas, e a segunda e a que evita uma lista de isencoes infinita.

    1. o caminho esta nomeado em DOCUMENTAL — prosa curta, isentada uma a uma;
    2. o VALOR e um paragrafo. Uma string de 120 caracteres ou mais nao e
       configuracao: e explicacao. Nenhum parametro deste projeto e um texto longo, e
       o teste `test_P28_prosa_por_tamanho_nunca_isenta_um_parametro` guarda isso —
       se um dia um valor longo virar comportamento, ele quebra.

    A regra por tamanho e deliberadamente estreita. Foi a tentacao oposta — um
    curinga generoso — que produziu o vao do P-28."""
    return _casa(caminho, DOCUMENTAL) or (isinstance(valor, str) and len(valor) >= PROSA_MINIMA)


def _casa(caminho, padroes):
    """`*` casa exatamente um segmento — nunca atravessa ponto. Um curinga guloso
    aqui isentaria secoes inteiras sem que ninguem percebesse."""
    for p in padroes:
        rx = "^" + r"\.".join("[^.]+" if seg == "*" else re.escape(seg)
                              for seg in p.split(".")) + "$"
        if re.match(rx, caminho): return True
    return False


def _modulos_do_motor():
    """TODOS os .py que nao sao teste nem demo. Fixar a lista a mao foi metade do
    defeito: o teste antigo lia tres modulos e o motor tem onze."""
    return sorted(f for f in os.listdir(AQUI)
                  if f.endswith(".py") and not f.startswith(("test_", "demo_")))


def _fontes_do_motor():
    """Os modulos do motor e, desde 24/09, os do fase0: a secao `armazem` e politica
    lida pela captura, nao pelo alocador. Deixar o fase0 fora faria a guarda acusar como
    morta uma chave que a captura le antes de cada envio -- o E-05 (varrer metade do
    sistema e chamar de conclusao)."""
    fase0 = os.path.join(os.path.dirname(AQUI), "fase0")
    extras = sorted(os.path.join(fase0, f) for f in os.listdir(fase0)
                    if f.endswith(".py") and not f.startswith("test_"))
    return "".join(open(os.path.join(AQUI, m), encoding="utf-8").read()
                   for m in _modulos_do_motor()) + \
        "".join(open(p, encoding="utf-8").read() for p in extras)


def _chaves_mortas(secao, fontes):
    mortas = []
    for caminho, chave, valor in _chaves(P[secao], f"{secao}."):
        if chave in DINAMICO or _e_prosa(caminho, valor): continue
        if f'"{chave}"' not in fontes and f"'{chave}'" not in fontes:
            mortas.append(caminho)
    return mortas


def test_P28_prosa_por_tamanho_nunca_isenta_um_parametro():
    """A porta 2 de `_e_prosa` isenta qualquer valor com 120+ caracteres. Isso so e
    seguro enquanto nenhum PARAMETRO for um texto longo. Este teste e o preco da
    regra: se alguem escrever um valor de comportamento com 120 caracteres, ele
    quebra aqui em vez de sumir da cobertura em silencio.

    O criterio de "parametro": string longa que ALGUM modulo do motor compara com
    igualdade — o jeito como este projeto usa string como valor de configuracao."""
    fontes = _fontes_do_motor()
    suspeitas = []
    for secao in REGIME_DAS_SECOES:
        for caminho, _, valor in _chaves(P[secao], f"{secao}."):
            if not (isinstance(valor, str) and len(valor) >= PROSA_MINIMA): continue
            if f'"{valor}"' in fontes or f"'{valor}'" in fontes:
                suspeitas.append(caminho)
    assert not suspeitas, ("valor longo usado como PARAMETRO pelo motor — a isencao "
                           "por tamanho o esconderia da cobertura: " + ", ".join(suspeitas))


def test_P28_toda_secao_do_politica_tem_regime_declarado():
    """O teste que teria pego a `revisao` no dia em que ela entrou. Nao ha default:
    secao sem regime nao 'passa por fora', ela quebra a suite."""
    do_arquivo = {k for k in P if not str(k).startswith("_")}
    sem_regime = do_arquivo - set(REGIME_DAS_SECOES)
    assert not sem_regime, (
        "secao em politica.yaml sem regime declarado em REGIME_DAS_SECOES: "
        + ", ".join(sorted(sem_regime)) + ". Escolha OPERACIONAL (o motor le), "
        "REGISTRO (testemunho) ou ESPECIFICACAO (escrito e nao ligado — exige pendencia).")
    fantasma = set(REGIME_DAS_SECOES) - do_arquivo
    assert not fantasma, ("regime declarado para secao que nao existe mais: "
                          + ", ".join(sorted(fantasma)))
    for secao, (regime, motivo) in REGIME_DAS_SECOES.items():
        assert regime in (OPERACIONAL, REGISTRO, ESPECIFICACAO), secao
        assert len(motivo) > 20, f"{secao}: o motivo do regime tem de ser uma frase"


def test_P28_secao_operacional_nao_tem_chave_morta():
    """A-03 com o escopo certo: onze modulos, todas as secoes OPERACIONAIS."""
    fontes = _fontes_do_motor()
    nao_lidas = []
    for secao, (regime, _) in REGIME_DAS_SECOES.items():
        if regime != OPERACIONAL: continue
        nao_lidas += [c for c in _chaves_mortas(secao, fontes) if c not in DIVIDA_DE_COBERTURA]
    assert not nao_lidas, ("chaves OPERACIONAIS declaradas e nunca lidas, e fora do "
                           "inventario de divida: " + ", ".join(nao_lidas))


def test_P28_a_divida_de_cobertura_nao_apodrece():
    """Inventario de divida so serve se encolher. Entrada que ja foi paga (a chave
    passou a ser lida) ou que evaporou (a chave saiu do YAML) tem de SAIR da lista —
    senao o inventario vira decoracao e volta a esconder o proximo `revisao`."""
    fontes = _fontes_do_motor()
    vivas = set()
    for secao, (regime, _) in REGIME_DAS_SECOES.items():
        if regime == OPERACIONAL:
            vivas |= set(_chaves_mortas(secao, fontes))
    obsoletas = sorted(set(DIVIDA_DE_COBERTURA) - vivas)
    assert not obsoletas, ("divida inventariada que ja nao existe (chave lida ou "
                           "removida). Apague estas linhas: " + ", ".join(obsoletas))
    for caminho, pend in DIVIDA_DE_COBERTURA.items():
        assert re.fullmatch(r"P-\d+", pend), f"{caminho}: divida sem numero de pendencia"


def test_P28_especificacao_e_uma_promessa_com_numero():
    """ESPECIFICACAO e a categoria perigosa: e onde eu ponho o que escrevi e nao liguei.
    Sem numero de pendencia, ela e so um jeito educado de nao implementar."""
    fontes = _fontes_do_motor()
    for secao, (regime, motivo) in REGIME_DAS_SECOES.items():
        if regime != ESPECIFICACAO: continue
        assert re.search(r"P-\d+", motivo), f"{secao}: ESPECIFICACAO sem pendencia no motivo"
        assert f'"{secao}"' not in fontes and f"'{secao}'" not in fontes, (
            f"{secao} esta declarada como ESPECIFICACAO mas ALGUM modulo do motor ja a "
            f"le. Promova para OPERACIONAL e feche a pendencia.")


def test_base_anos_vem_do_yaml_e_nao_do_python():
    assert "base_anos" in P["crescimento"]["ajuste_horizonte"]
    P2 = copy.deepcopy(P); P2["crescimento"]["ajuste_horizonte"]["base_anos"] = 20
    e = Estado(**BASE)
    assert abs(fracao_rv(e, P2) - fracao_rv(e, P)) > 1e-9


def test_custo_maximo_classe_peso_limita_em_vez_de_excluir():
    P2 = copy.deepcopy(P); P2["tetos"]["custo_maximo_classe_aa"] = 0.0009
    r = alocar(Estado(**BASE), C, P2, teses={}, carregos={})
    assert r["alvo"]["pesos"].get("smal11", 0) > 0, "rota cara foi EXCLUIDA em vez de limitada"
    assert r["alvo"]["pesos"]["smal11"] <= P2["tetos"]["custo_maximo_classe_peso"] + 1e-9
    assert any("LIMITADA" in a for a in r["alvo"]["alertas"])


def test_fgc_por_conglomerado_e_verificado():
    e = Estado(**{**BASE, "reserva_atual": 0, "despesa_mensal": 60000, "aporte_mensal": 5000})
    r = alocar(e, C, P, teses={}, carregos={})
    assert r["diretiva"].portao == "G2_reserva"
    assert any("FGC" in a for a in r["diretiva"].memoria["alertas"])


# ══ A-02 · G3 separa custo fixo de percentual ════════════════════════════════
def test_rota_com_custo_fixo_volta_com_aporte_maior_e_o_sistema_diz_em_qual():
    rotas = catalogo(C)
    _, f200 = g3_atrito(rotas, C, P, 200)
    fora200 = {r.id: (m, reent) for r, e, m, reent in f200}
    assert fora200["acao_450"][0] == "FIXO"
    assert 400 < fora200["acao_450"][1] < 500
    _, f500 = g3_atrito(rotas, C, P, 500)
    assert "acao_450" not in {r.id for r, *_ in f500}


def test_rota_com_custo_percentual_nao_volta_com_aporte_maior():
    rotas = catalogo(C)
    for aporte in (500, 10_000, 1_000_000):
        _, fora = g3_atrito(rotas, C, P, aporte)
        d = {r.id: (m, reent) for r, e, m, reent in fora}
        for rid in ("ext_avenue", "ext_nomad1", "ext_conta"):
            assert d[rid][0] == "PERCENTUAL" and d[rid][1] is None


def test_custo_entrada_fixo_pct_zero_aporte_nao_inflaciona_rota_gratuita():
    """Achado lateral do P-71/P-72 (11/09/2026). `aporte_mensal=0` passou a ser
    estado legitimo (P-72), e isso expos que `custo_entrada_fixo_pct` tratava
    aporte==0 como custo INFINITO para QUALQUER rota — inclusive as de tarifa
    fixa zero. Estourava o universo inteiro e `_conferir_invariantes` recusava
    pesos somando 0 em vez de 1. Uma rota sem tarifa fixa e gratis para qualquer
    aporte, aporte==0 incluso; uma rota com tarifa continua math.inf a aporte 0 —
    esse caso nao muda em relacao ao comportamento anterior."""
    gratis = types.SimpleNamespace(corr_fix=0.0)
    cobra = types.SimpleNamespace(corr_fix=4.50)
    assert custo_entrada_fixo_pct(gratis, 0) == 0.0
    assert custo_entrada_fixo_pct(gratis, 500) == 0.0
    assert custo_entrada_fixo_pct(cobra, 0) == math.inf
    assert custo_entrada_fixo_pct(cobra, 500) == pytest.approx(4.50/500)


# ══ E-03 · dois portoes ignoravam o proprio interruptor ══════════════════════
def _universo_real(politica):
    """G6 e G5 rodam ANTES do G3 na ordem do YAML. Alimentar o G4 com o catalogo CRU
    faria calcular arrasto de rota BLOQUEADA, e isso levanta InsumoBloqueado -- com
    razao, e o F-02 trabalhando. Sao 18 rotas aqui contra 25 no catalogo cru."""
    r6, _ = g6_coerencia_funcao(catalogo(C), politica)
    r5, _ = g5_status(r6, politica)
    return r5


def _cenarios_E03():
    """Um cenario por portao em que ele, LIGADO, reprova alguma coisa. Cada entrada
    devolve `f(P) -> (passaram, reprovados, total)`; para os portoes da fase `aporte`
    "reprovar" e emitir diretiva ou pendencia -- desviar o dinheiro -- e "passar" e
    devolver None, deixando o aporte seguir."""
    cat = catalogo(C)
    rotas = _universo_real(P)
    pares, _ = g3_atrito(rotas, C, P, 500.0)
    vivos, _, _ = g4_dominancia(pares, C, 500.0, P, 25)
    com_match = Estado(**BASE, match_empregador=MatchEmpregador(0.5, 0.06, 10000.0))
    divida_cara = Estado(**{**BASE, "dividas": [Divida("cartao", 5000, 0.10)]})
    sem_reserva = Estado(**{**BASE, "reserva_atual": 0.0})

    def aporte(chamada):
        def f(Px):
            saida = chamada(Px)
            saida = saida if isinstance(saida, tuple) else (saida,)
            desvios = [x for x in saida if x is not None]
            return ([] if desvios else ["aporte"]), desvios, 1
        return f

    def universo(chamada, n):
        def f(Px):
            saida = chamada(Px)
            return saida[0], [x for resto in saida[1:] for x in resto], n
        return f

    return {
        "G0_match_empregador": aporte(lambda Px: g0_match_empregador(com_match, cat, C, Px)),
        "G1_divida": aporte(lambda Px: g1_divida(divida_cara, cat, C, Px)),
        "G2_reserva": aporte(lambda Px: g2_reserva(sem_reserva, cat, C, Px)),
        "G3_atrito": universo(lambda Px: g3_atrito(rotas, C, Px, 500.0), len(rotas)),
        "G4_dominancia": universo(lambda Px: g4_dominancia(pares, C, 500.0, Px, 25),
                                  len(pares)),
        "G5_status": universo(lambda Px: g5_status(cat, Px), len(cat)),
        "G6_coerencia_funcao": universo(lambda Px: g6_coerencia_funcao(cat, Px), len(cat)),
        "G7_tese_registrada": universo(lambda Px: g7_tese_registrada(vivos, Px, {}),
                                       len(vivos)),
        "G8_compromisso_de_carrego": universo(
            lambda Px: g8_compromisso_de_carrego(vivos, Px, {}), len(vivos)),
    }


def test_E03_todo_portao_que_declara_ativo_le_o_proprio_interruptor():
    """Fecha a CLASSE, nao os dois casos. Qualquer portao que declare `ativo` no
    politica.yaml precisa HONRAR o campo -- senao o decimo portao repete o E-03.
    Interruptor morto nao da erro: da conclusao errada em analise de sensibilidade,
    que e para isso que este projeto existe.

    B-15 (24/09/2026): ate aqui o teste procurava a palavra `ativo` no codigo-fonte da
    funcao -- a forma do A-06, *medir a bandeira nao e medir quem a honra*. Um
    `if g["ativo"]: pass`, ou um comentario com a palavra, passava. Agora mede o
    COMPORTAMENTO: com `ativo: true` o portao reprova algo no cenario; com
    `ativo: false`, no mesmo cenario, nao reprova nada e deixa passar tudo. Portao com
    `ativo` e sem cenario aqui reprova -- o decimo portao tem de trazer o seu."""
    cenarios = _cenarios_E03()
    sem_cenario = [n for n, cfg in P["portoes"].items()
                   if isinstance(cfg, dict) and "ativo" in cfg and n not in cenarios]
    assert not sem_cenario, f"portao com `ativo` e sem cenario no E-03: {sem_cenario}"
    mudos, cenario_fraco = [], []
    for nome, f in cenarios.items():
        ligado, desligado = copy.deepcopy(P), copy.deepcopy(P)
        ligado["portoes"][nome]["ativo"] = True
        desligado["portoes"][nome]["ativo"] = False
        _, reprovados_on, _ = f(ligado)
        passaram_off, reprovados_off, total = f(desligado)
        if not reprovados_on:
            cenario_fraco.append(nome)
        if reprovados_off or len(passaram_off) != total:
            mudos.append(nome)
    assert not cenario_fraco, ("o cenario nao faz o portao reprovar nada nem LIGADO, "
                               "entao desligar nao provaria nada: " + ", ".join(cenario_fraco))
    assert not mudos, ("portao declara `ativo` no YAML e desliga-lo NAO desliga a "
                       "eliminacao: " + ", ".join(mudos))


def test_E03_g3_desligado_nao_elimina_ninguem():
    rotas = _universo_real(P)
    P2 = copy.deepcopy(P); P2["portoes"]["G3_atrito"]["ativo"] = False
    dentro_on, fora_on = g3_atrito(rotas, C, P, 500.0)
    dentro_off, fora_off = g3_atrito(rotas, C, P2, 500.0)
    assert (len(dentro_on), len(fora_on)) == (14, 4), "a base mudou: remeca o E-03"
    assert len(dentro_off) == len(rotas) and fora_off == []


def test_E03_g4_desligado_nao_elimina_ninguem():
    rotas = _universo_real(P)
    pares, _ = g3_atrito(rotas, C, P, 500.0)
    P2 = copy.deepcopy(P); P2["portoes"]["G4_dominancia"]["ativo"] = False
    vivos_on, dom_on, pref_on = g4_dominancia(pares, C, 500.0, P, 25)
    vivos_off, dom_off, pref_off = g4_dominancia(pares, C, 500.0, P2, 25)
    assert (len(vivos_on), len(dom_on), len(pref_on)) == (12, 2, 0), \
        "a base mudou: remeca o E-03"
    assert len(vivos_off) == len(pares) and dom_off == [] and pref_off == []


def test_E03_desligado_preserva_a_ARIDADE_das_tuplas():
    """O teste que pega a correcao ingenua (`return rotas, []`): `dentro` e lista de
    PARES e `vivos` de QUADRAS, e quem vem depois consome esses campos. Medido em
    12/09: 2 e 4. Desligar o portao desliga a eliminacao, nao o contrato."""
    rotas = _universo_real(P)
    P2 = copy.deepcopy(P)
    P2["portoes"]["G3_atrito"]["ativo"] = False
    P2["portoes"]["G4_dominancia"]["ativo"] = False
    for politica in (P, P2):
        dentro, _ = g3_atrito(rotas, C, politica, 500.0)
        assert dentro and all(len(t) == 2 for t in dentro)
        vivos, _, _ = g4_dominancia(dentro, C, 500.0, politica, 25)
        assert vivos and all(len(t) == 4 for t in vivos)


def test_E03_com_a_configuracao_padrao_a_correcao_e_inerte():
    """Instantaneo dourado do E-03. Com os nove `ativo: true` -- a configuracao real --
    a mudanca tem de nao mexer em nada. O `alocar()` inteiro foi serializado antes e
    depois e comparado campo a campo (zero diferencas, sha256 fa57ee253758dacd); estes
    numeros sao a parte que fica medida na suite."""
    rotas = _universo_real(P)
    dentro, fora = g3_atrito(rotas, C, P, 500.0)
    vivos, dominados, preferencia = g4_dominancia(dentro, C, 500.0, P, 25)
    assert (len(rotas), len(dentro), len(fora)) == (18, 14, 4)
    assert (len(vivos), len(dominados), len(preferencia)) == (12, 2, 0)


# ══ A-05 · G1 liquido contra liquido ═════════════════════════════════════════
def test_g1_dispara_na_fronteira_de_090_ao_mes():
    e = Estado(**{**BASE, "dividas": [Divida("consignado", 20000, 0.0090)]})
    r = alocar(e, C, P, teses={}, carregos={})
    assert r["diretiva"].portao == "G1_divida"
    m = r["diretiva"].memoria
    assert m["melhor_investimento_am"] < 0.0090 < m["bruto_am_referencia"]


def test_g1_divida_barata_nao_dispara():
    e = Estado(**{**BASE, "dividas": [Divida("consignado", 20000, 0.004)]})
    assert "diretiva" not in alocar(e, C, P, teses={}, carregos={})


def test_g1_usa_a_aliquota_da_faixa_declarada():
    assert aliquota_ir_rf(C, P["portoes"]["G1_divida"]["horizonte_ir_dias"]) == 0.225
    assert aliquota_ir_rf(C, 800) == 0.15


# ══ A-06 · deriva sobre deficit ══════════════════════════════════════════════
def test_deriva_dispara_quando_o_aporte_nao_fecha_o_deficit():
    e = Estado(**{**BASE, "posicoes": {"bova11": 900000, "td_selic": 100000}})
    r = motor_aporte(e, alocar(e, C, P, teses={}, carregos={})["alvo"], C, P)
    assert r["deriva"] is not None
    assert r["deriva"]["capacidade_anual"] < r["deriva"]["deficit_max"]
    assert r["excesso_max"] > r["deficit_max"]


# ══ G0, G6, G7, G8 ═══════════════════════════════════════════════════════════
def test_g0_esta_desligado_porque_a_resposta_existe():
    """04/09/2026: o usuario e PJ na Volga e nao tem previdencia de nenhum tipo.
    A pendencia some do output — mas o portao permanece no arquivo com ativo: false,
    porque desativado por resposta verificada e diferente de nunca ter existido."""
    assert P["portoes"]["G0_match_empregador"]["ativo"] is False
    r = alocar(Estado(**BASE), C, P, teses={}, carregos={})
    assert not any(p.id == "G0_match" for p in r["pendencias"])


def test_g0_volta_a_funcionar_se_for_religado():
    """O mecanismo continua testado: se o vinculo virar CLT com plano, religar o
    portao no YAML tem de bastar."""
    P2 = copy.deepcopy(P); P2["portoes"]["G0_match_empregador"]["ativo"] = True
    r = alocar(Estado(**BASE), C, P2, teses={}, carregos={})
    assert any(p.id == "G0_match" for p in r["pendencias"])


def test_g0_desaparece_quando_verificado_e_inexistente():
    r = alocar(Estado(**{**BASE, "match_verificado": True}), C, P, teses={}, carregos={})
    assert not any(p.id == "G0_match" for p in r["pendencias"])


def test_g0_precede_g1_e_absorve_o_aporte_ate_o_limite_casado():
    e = Estado(**{**BASE, "aporte_mensal": 400,
                  "dividas": [Divida("cartao", 3000, 0.14)],
                  "match_empregador": MatchEmpregador(0.5, 0.05, 12000)})
    P2 = copy.deepcopy(P); P2["portoes"]["G0_match_empregador"]["ativo"] = True
    r = alocar(e, C, P2, teses={}, carregos={})
    assert r["portoes"][0].portao == "G0_match_empregador"


def test_g0_com_sobra_cai_no_g1():
    e = Estado(**{**BASE, "aporte_mensal": 2000,
                  "dividas": [Divida("cartao", 3000, 0.14)],
                  "match_empregador": MatchEmpregador(0.5, 0.05, 12000)})
    P2 = copy.deepcopy(P); P2["portoes"]["G0_match_empregador"]["ativo"] = True
    r = alocar(e, C, P2, teses={}, carregos={})
    assert [d.portao for d in r["portoes"]] == ["G0_match_empregador", "G1_divida"]
    assert r["diretiva"].valor == 2000 - 600


def test_g6_retira_a_funcao_que_a_rota_nao_satisfaz():
    rotas = catalogo(C)
    for r in rotas:
        if r.id == "rdb_100": r.liquidez_dias = 30
    ok, ruins = g6_coerencia_funcao(rotas, P)
    assert not any(r.id == "rdb_100" for r in ok)


def test_aposta_perda_total_aceita_false_zera_o_bloco():
    P2 = copy.deepcopy(P); P2["tetos"]["aposta_perda_total_aceita"] = False
    r = alocar(Estado(**BASE), C, P2, teses=tese_valida(), carregos={})
    assert r["alvo"]["pesos"].get("hash11", 0) == 0


# ══ B-* implementacao ════════════════════════════════════════════════════════
def test_invariante_valor_igual_quantidade_vezes_preco_com_precos_reais():
    precos = {"bova11": 128.43, "pibb11": 302.11, "divo11": 11.77, "smal11": 98.02,
              "ivvb11": 415.60, "acao_zero": 37.19, "td_selic": 1.0}
    e = Estado(**{**BASE, "aporte_mensal": 1500,
                  "posicoes": {"bova11": 2400, "pibb11": 900, "divo11": 950,
                               "smal11": 1500, "ivvb11": 1100, "acao_zero": 800,
                               "td_selic": 1300}})
    rotas = {r.id: r for r in catalogo(C)}
    r = motor_aporte(e, alocar(e, C, P, teses={}, carregos={})["alvo"], C, P,
                     precos=precos, rotas_por_id=rotas)
    assert r["ordens"]
    for o in r["ordens"]:
        assert abs(o["valor"] - o["quantidade"]*o["preco"]) < 0.01, o
    gasto = sum(o["valor"] for o in r["ordens"])
    assert abs(gasto + (r["caixa"] - e.caixa) - e.aporte_mensal) < 0.02


def test_residuo_de_lote_vai_para_caixa():
    precos = {"ivvb11": 415.60, "acao_zero": 128.43}
    e = Estado(**{**BASE, "aporte_mensal": 500,
                  "posicoes": {"bova11": 900, "pibb11": 900, "divo11": 900,
                               "smal11": 900, "ivvb11": 100, "acao_zero": 100,
                               "td_selic": 9000}})
    rotas = {r.id: r for r in catalogo(C)}
    r = motor_aporte(e, alocar(e, C, P, teses={}, carregos={})["alvo"], C, P,
                     precos=precos, rotas_por_id=rotas)
    assert r["caixa"] > 0


def test_rota_sem_lote_nao_e_arredondada_por_magnitude_de_preco():
    rotas = {r.id: r for r in catalogo(C)}
    assert rotas["td_selic"].negocia_em_lote is False
    assert rotas["bova11"].negocia_em_lote is True


def test_invariantes_de_saida_sao_raise_e_nao_assert():
    """B-05: a instrucao `assert` do Python e removida inteira por `python -O`, e
    levaria a guarda junto. Uma guarda que some quando se liga otimizacao e pior que
    nenhuma: da a impressao de estar la.

    Este teste era FRAGIL POR CONSTRUCAO ate 05/09/2026 — ele fatiava o texto de
    alocacao.py entre dois comentarios (`# invariantes de saida` e `# V-06`) e
    quebrou na primeira vez que alguem mexeu na estrutura, que foi a P-37. Agora ele
    olha para a FUNCAO, pelo AST, e depois exercita o comportamento. Um teste que
    depende da posicao de um comentario nao esta testando o codigo."""
    arvore = ast.parse(open(os.path.join(AQUI, "alocacao.py"), encoding="utf-8").read())
    alvo = next(n for n in ast.walk(arvore)
                if isinstance(n, ast.FunctionDef) and n.name == "_conferir_invariantes")
    assert not [n for n in ast.walk(alvo) if isinstance(n, ast.Assert)], \
        "`assert` aqui desaparece com python -O"
    levantados = [n for n in ast.walk(alvo) if isinstance(n, ast.Raise)]
    assert len(levantados) >= 3

    # e ela de fato levanta: soma errada, teto de APOSTA, teto de SEGURO_CAUDA
    vivos = [(r, None, 0.0) for r in catalogo(C)]
    with pytest.raises(ValueError, match="pesos somam"):
        _conferir_invariantes({"bova11": 0.5}, vivos, P)
    with pytest.raises(ValueError, match="teto de APOSTA"):
        _conferir_invariantes({"hash11": 1.0}, vivos, P)


def test_segunda_coluna_de_custo_existe():
    r = alocar(Estado(**BASE), C, P, teses={}, carregos={})
    assert set(r["alvo"]["custo_pct_aportado"]) == set(r["alvo"]["pesos"])
    rotas = {x.id: x for x in catalogo(C)}
    assert custo_pct_aportado(rotas["hash11"], C, 500, 20) > \
           arrasto_anualizado(rotas["hash11"], C, 500, 20)


def test_g2_escolhe_por_retorno_liquido_e_nao_por_ordem_alfabetica():
    """B-08. O criterio e SENSIVEL ao tamanho da reserva, e por isso nao pode ser
    constante: ate R$10 mil o Tesouro e isento de custodia e ganha; acima disso a
    custodia de 0,20% a.a. o derruba abaixo do RDB a 100% do CDI."""
    peq = alocar(Estado(**{**BASE, "despesa_mensal": 1200, "reserva_atual": 0}),
                 C, P, teses={}, carregos={})["diretiva"].memoria["ranking"]
    gra = alocar(Estado(**{**BASE, "reserva_atual": 0}),
                 C, P, teses={}, carregos={})["diretiva"].memoria["ranking"]
    assert peq[0][0] == "td_reserva" and gra[0][0] == "rdb_100"
    for rank in (peq, gra):
        assert rank[-1][0] == "poupanca"
        assert [x[0] for x in rank] != sorted([x[0] for x in rank])


def test_procedencia_no_retorno_de_alocar():
    p = alocar(Estado(**BASE), C, P, teses={}, carregos={})["procedencia"]
    assert p["politica_versao"] == P["meta"]["versao"]
    assert len(p["politica_hash"]) == 12 and len(p["custos_hash"]) == 12


def test_determinismo():
    a = alocar(Estado(**BASE), C, P, teses={}, carregos={})["alvo"]["pesos"]
    b = alocar(Estado(**BASE), C, P, teses={}, carregos={})["alvo"]["pesos"]
    assert a == b


# ══ varredura de horizonte ═══════════════════════════════════════════════════
@pytest.mark.parametrize("anos", [5, 10, 15, 25, 30, 40])
def test_invariantes_valem_em_todo_horizonte(anos):
    e = Estado(**{**BASE, "horizonte_anos": anos})
    r = alocar(e, C, P, teses=tese_valida(), carregos=carrego_valido())
    assert abs(sum(r["alvo"]["pesos"].values()) - 1.0) < 1e-6
    assert r["alvo"]["pesos"].get("hash11", 0) <= P["tetos"]["aposta_pct"] + 1e-9
    assert r["alvo"]["pesos"].get("td_ipca", 0) <= 0.15 + 1e-9


def test_limiar_de_custo_de_classe_e_atravessado_e_o_sistema_avisa():
    rotas = {r.id: r for r in catalogo(C)}
    a25 = arrasto_anualizado(rotas["hash11"], C, 500, 25)
    a40 = arrasto_anualizado(rotas["hash11"], C, 500, 40)
    assert a25 < P["tetos"]["custo_maximo_classe_aa"] < a40
    r = alocar(Estado(**{**BASE, "horizonte_anos": 40}), C, P,
               teses=tese_valida(), carregos={})
    assert any("LIMITADA" in a for a in r["alvo"]["alertas"])


# ══ portoes e invariantes gerais ═════════════════════════════════════════════
def test_g2_reserva_vazia_absorve_tudo():
    r = alocar(Estado(**{**BASE, "reserva_atual": 0}), C, P, teses={}, carregos={})
    assert r["diretiva"].portao == "G2_reserva"
    assert r["diretiva"].memoria["meses_para_completar"] == 54


def test_g1_tem_precedencia_sobre_g2():
    e = Estado(**{**BASE, "reserva_atual": 0, "dividas": [Divida("cartao", 3000, 0.14)]})
    assert alocar(e, C, P, teses={}, carregos={})["diretiva"].portao == "G1_divida"


def test_reserva_alvo_responde_a_estabilidade():
    assert reserva_alvo(Estado(**{**BASE, "estabilidade_renda": "baixa"}), P) == 4500*9
    assert reserva_alvo(Estado(**{**BASE, "estabilidade_renda": "alta"}), P) == 4500*4.5


def test_g5_status_tira_rota_nao_confirmada():
    r = alocar(Estado(**BASE), C, P, teses={}, carregos={})
    # F-02: fora_status agora carrega a ROTA, nao (rota, custo) — nao ha custo a
    # reportar para uma rota cujo custo e o proprio insumo bloqueado.
    assert "bovv11" in {x.id for x in r["universo"]["fora_status"]}
    assert "bovv11" not in r["alvo"]["pesos"]


def test_pesos_somam_um():
    for ap in (200, 500, 1000, 3000):
        for t, c in (({}, {}), (tese_valida(), carrego_valido())):
            r = alocar(Estado(**{**BASE, "aporte_mensal": ap}), C, P, teses=t, carregos=c)
            assert abs(sum(r["alvo"]["pesos"].values()) - 1.0) < 1e-6


def test_teto_de_aposta_nunca_e_violado():
    """Regressao do bug que produziu 60% em cripto. Com tese valida, para que a
    alocacao seja de fato exercida (backlog 16 do laudo anterior)."""
    exercitou = 0
    for ap in (200, 500, 1000, 3000, 10000):
        for est in ("alta", "media", "baixa"):
            e = Estado(**{**BASE, "aporte_mensal": ap, "estabilidade_renda": est,
                          "reserva_atual": 54000})
            r = alocar(e, C, P, teses=tese_valida(), carregos=carrego_valido())
            if r["alvo"] is None:
                assert r["diretiva"].portao == "G2_reserva"; continue
            assert r["alvo"]["pesos"].get("hash11", 0) <= P["tetos"]["aposta_pct"] + 1e-9
            if r["alvo"]["pesos"].get("hash11", 0) > 0: exercitou += 1
    assert exercitou >= 10


def test_fracao_rv_respeita_piso_e_teto():
    baixo = Estado(**{**BASE, "estabilidade_renda": "baixa",
                      "reserva_atual": 0, "horizonte_anos": 1})
    alto = Estado(**{**BASE, "estabilidade_renda": "alta",
                     "reserva_atual": 500000, "horizonte_anos": 50})
    assert fracao_rv(baixo, P) >= P["crescimento"]["piso_rv"]
    assert fracao_rv(alto, P) <= P["crescimento"]["teto_rv"]


def test_diversificacao_minima_e_reportada():
    r = alocar(Estado(**{**BASE, "aporte_mensal": 1000}), C, P, teses={}, carregos={})
    for rid, d in r["alvo"]["diversificacao"].items():
        assert d["n_minimo"] == math.ceil(d["peso"]/P["tetos"]["por_ativo_pct_patrimonio"])


def test_nenhuma_rota_eliminada_recebe_peso():
    r = alocar(Estado(**{**BASE, "aporte_mensal": 200}), C, P, teses={}, carregos={})
    eliminadas = ({x[0].id for x in r["universo"]["dominados"]}
                  | {x.id for x in r["universo"]["fora_status"]}
                  | {x[0].id for x in r["universo"]["sem_tese"]}
                  | {x[0].id for x in r["universo"]["sem_carrego"]}
                  | {x[0].id for x in r["universo"]["preferencia_horizonte"]}
                  | {x[0].id for x in r["universo"]["fora_atrito"]})
    assert not (eliminadas & set(r["alvo"]["pesos"]))


def test_custo_de_discordar_e_positivo_quando_a_proposta_e_mais_cara():
    rotas = {x.id: x for x in catalogo(C)}
    d = custo_de_discordar({"pibb11": 0.5, "td_selic": 0.5},
                           {"hash11": 0.5, "td_selic": 0.5}, C, 500, 20, rotas)
    assert d["diferenca_pp_aa"] > 0


def test_P134_entrada_que_come_o_aporte_e_recusada_com_nome():
    """Antes: `min(e*aporte, aporte)` e a simulacao devolvia numero. A R$ 4,00 a ordem de
    R$ 4,50 come o aporte inteiro; nao ha patrimonio a simular, e isso tem nome."""
    from alocacao import AporteConsumidoPelaEntrada, simular_custo
    r = {x.id: x for x in catalogo(C)}["acao_450"]
    with pytest.raises(AporteConsumidoPelaEntrada, match="acao_450"):
        simular_custo(r, C, 4.0, 1)
    pat, custo, ap = simular_custo(r, C, 500.0, 1)       # controle: aporte normal simula
    assert ap == 6000.0 and 0 < custo < ap and pat > 0


def test_P134_proposta_com_peso_minimo_de_rota_de_custo_fixo_nao_vira_numero():
    """O caminho que o G3 nao cobre: a proposta do usuario nao passa por portao, e cada
    rota e simulada com o aporte DELA. 0,5% de R$ 500 = R$ 2,50 < R$ 4,50 da ordem."""
    rotas = {x.id: x for x in catalogo(C)}
    d = custo_de_discordar({"td_selic": 1.0}, {"td_selic": 0.995, "acao_450": 0.005},
                           C, 500, 20, rotas)
    assert d["arrasto_proposta_aa"] is None and d["diferenca_pp_aa"] is None
    assert any("acao_450" in m for m in d["aporte_consumido"])
    assert d["arrasto_alvo_aa"] is not None


def test_P134_com_aporte_zero_a_interacao_g3_g4_nao_cai_nem_vira_NaN():
    """Aporte R$ 0 dava entrada fixa infinita, e `min(inf*0, 0)` devolvia NaN calado. A
    interacao G3xG4 comparava NaN e acertava por acidente (NaN < x e falso)."""
    from alocacao import interacao_g3_g4
    rotas = {x.id: x for x in catalogo(C)}
    fora = [(rotas["acao_450"], float("inf"), "FIXO", None)]
    vivos = [x for x in rotas.values() if x.exposicao == rotas["acao_450"].exposicao
             and x.id != "acao_450" and x.confiavel]
    assert vivos, "controle: precisa haver rival de mesma exposicao"
    assert interacao_g3_g4(fora, vivos, C, 0.0, P, 10) == []


def test_fora_de_escopo_viaja_para_o_output_e_nao_contem_ipca_nem_cripto():
    """A objecao do usuario: o que tem regra nao vira ausencia declarada."""
    r = alocar(Estado(**BASE), C, P, teses={}, carregos={})
    fe = r["fora_de_escopo"]
    assert {"LCI_LCA", "FII", "match_empregador", "PGBL", "ouro_e_dolar"} <= set(fe)
    chaves = " ".join(fe).lower()
    assert "ipca" not in chaves and "cripto" not in chaves
    for k, v in fe.items():
        assert v.get("motivo") and v.get("reentra"), k


# ══ motor de aporte ══════════════════════════════════════════════════════════
def test_aporte_recusa_rodar_sem_posicao():
    e = Estado(**BASE)
    alvo = alocar(e, C, P, teses={}, carregos={})["alvo"]
    assert motor_aporte(e, alvo, C, P)["status"] == "SEM_POSICAO"


def test_aporte_produz_ordem_em_carteira_normal():
    e = Estado(**{**BASE, "posicoes": {"bova11": 2400, "pibb11": 900, "divo11": 950,
                  "smal11": 1500, "ivvb11": 1100, "acao_zero": 800, "td_selic": 1300}})
    r = motor_aporte(e, alocar(e, C, P, teses={}, carregos={})["alvo"], C, P)
    assert r["status"] == "OK" and len(r["ordens"]) >= 1


def test_aporte_vai_para_o_maior_deficit():
    e = Estado(**{**BASE, "posicoes": {"bova11": 5000, "td_selic": 100}})
    alvo = alocar(e, C, P, teses={}, carregos={})["alvo"]
    r = motor_aporte(e, alvo, C, P)
    D = {rid: alvo["pesos"].get(rid, 0)*(e.patrimonio_investido+e.aporte_mensal)
              - e.posicoes.get(rid, 0) for rid in alvo["pesos"]}
    assert r["ordens"][0]["rota"] == max(D, key=D.get)


def test_aporte_nunca_vende():
    e = Estado(**{**BASE, "posicoes": {"bova11": 9000, "td_selic": 1000}})
    r = motor_aporte(e, alocar(e, C, P, teses={}, carregos={})["alvo"], C, P)
    assert all(o["valor"] > 0 and o["quantidade"] > 0 for o in r["ordens"])


# ══ RES-01 · exclusividade da reserva ════════════════════════════════════════
from reserva import simular, taxa_liquida_reserva


def test_exclusividade_da_reserva_e_parametro_declarado():
    """04/09/2026: o tudo-ou-nada era regra IMPLICITA — o codigo devolvia o aporte
    inteiro e ninguem tinha declarado que aquilo era uma escolha."""
    assert P["portoes"]["G2_reserva"]["exclusividade"] == 1.0


def test_split_da_reserva_nao_cria_patrimonio():
    """O achado que decidiu RES-01: com a mesma taxa nos dois potes, mover aporte da
    reserva para investimento nao cria valor — troca o rotulo. O patrimonio total em
    10 anos e identico ate o centavo nas quatro regras."""
    t = taxa_liquida_reserva(C, P)
    totais = [simular(4000, 7667.91, 500, 36000, 120, t, t, f)["total_final"]
              for f in (1.0, 0.8, 0.6, 0.5)]
    for x in totais[1:]:
        assert abs(x - totais[0]) < 0.01, "o split nao pode criar nem destruir patrimonio"


def test_split_atrasa_a_reserva_e_aumenta_a_exposicao():
    t = taxa_liquida_reserva(C, P)
    cheio = simular(4000, 7667.91, 500, 36000, 120, t, t, 1.0)
    meio  = simular(4000, 7667.91, 500, 36000, 120, t, t, 0.5)
    assert meio["mes_alvo"] > cheio["mes_alvo"] + 20
    assert meio["meses_abaixo_3"] > cheio["meses_abaixo_3"]


def test_o_split_so_paga_com_premio_de_renda_variavel():
    """A pergunta invertida: no premio MEDIDO (0,96% a.a.), o 50/50 rende R$1.294 em
    10 anos — 2,2% do aportado — em troca de 25 meses a mais sem reserva."""
    t = taxa_liquida_reserva(C, P)
    aa = (1 + t)**12 - 1
    ganhos = {}
    for premio in (0.0, 0.0096, 0.06):
        ti = (1 + aa + premio)**(1/12) - 1
        a = simular(4000, 7667.91, 500, 36000, 120, t, ti, 1.0)["total_final"]
        b = simular(4000, 7667.91, 500, 36000, 120, t, ti, 0.5)["total_final"]
        ganhos[premio] = b - a
    assert abs(ganhos[0.0]) < 0.01
    assert 900 < ganhos[0.0096] < 1800
    assert ganhos[0.06] > ganhos[0.0096] * 5


def test_exclusividade_parcial_libera_o_resto_para_a_alocacao():
    """O parametro tem de MUDAR comportamento, nao so existir no YAML — foi o teste de
    cobertura que pegou a declaracao sem implementacao."""
    e = Estado(despesa_mensal=4000, reserva_atual=7667.91, aporte_mensal=500,
               estabilidade_renda="baixa", horizonte_anos=10)
    cheio = alocar(e, C, P, teses={}, carregos={})
    assert cheio["diretiva"].portao == "G2_reserva" and cheio["alvo"] is None
    assert cheio["diretiva"].valor == 500

    P2 = copy.deepcopy(P); P2["portoes"]["G2_reserva"]["exclusividade"] = 0.5
    meio = alocar(e, C, P2, teses={}, carregos={})
    assert meio["portoes"][0].valor == 250
    assert meio["alvo"] is not None, "com exclusividade < 1 a alocacao tem de rodar"
    assert abs(sum(meio["alvo"]["pesos"].values()) - 1.0) < 1e-6
    assert meio["portoes"][0].memoria["meses_para_completar"] > \
           cheio["diretiva"].memoria["meses_para_completar"]


def test_exclusividade_invalida_levanta():
    for v in (0.0, -0.5, 1.5):
        P2 = copy.deepcopy(P); P2["portoes"]["G2_reserva"]["exclusividade"] = v
        with pytest.raises(ValueError):
            alocar(Estado(**{**BASE, "reserva_atual": 0}), C, P2, teses={}, carregos={})


# ══ o aporte nao e uma verdade em pedra ══════════════════════════════════════
def test_mes_de_bonus_usa_o_dinheiro_do_mes_e_nao_o_piso():
    """Critica do usuario em 04/09/2026. O alvo continua calculado sobre o PISO — um
    alvo que oscila com o bonus nao e alvo, e reacao — mas as ORDENS do mes usam o
    dinheiro que de fato entrou."""
    e = Estado(**{**BASE, "aporte_mensal": 500,
                  "posicoes": {"bova11": 2400, "pibb11": 900, "divo11": 950,
                               "smal11": 1500, "ivvb11": 1100, "acao_zero": 800,
                               "td_selic": 1300}})
    alvo = alocar(e, C, P, teses={}, carregos={})["alvo"]
    normal = motor_aporte(e, alvo, C, P)
    bonus = motor_aporte(e, alvo, C, P, aporte_do_mes=3500)
    assert normal["aporte"] == 500 and bonus["aporte"] == 3500
    assert bonus["extraordinario"] == 3000 and normal["extraordinario"] == 0
    assert sum(o["valor"] for o in bonus["ordens"]) > sum(o["valor"] for o in normal["ordens"])
    assert bonus["aporte_base"] == 500, "o piso tem de continuar visivel no output"


def test_aporte_zero_no_mes_nao_quebra_o_motor():
    """O realizado do usuario hoje e zero. O motor tem de dizer isso, nao levantar."""
    e = Estado(**{**BASE, "posicoes": {"bova11": 2400, "td_selic": 1300}})
    r = motor_aporte(e, alocar(e, C, P, teses={}, carregos={})["alvo"], C, P,
                     aporte_do_mes=0)
    assert r["status"] == "SEM_APORTE" and "falta e o dinheiro" in r["nota"]


def test_data_da_reserva_e_faixa_e_o_piso_e_o_limite_superior():
    """A data com bonus e sempre <= a data do piso, e so a do piso pode ser prometida."""
    from aporte import Aporte, faixa_da_reserva
    from reserva import taxa_liquida_reserva
    t = taxa_liquida_reserva(C, P)
    a = Aporte(base=500, extraordinario_tipico=1500, extraordinarios_por_ano=2)
    f = faixa_da_reserva(36000, 7667.91, a, t)
    assert f["mes_com_extraordinario"] < f["mes_no_piso"]
    assert f["antecipacao"] > 0
    sem = Aporte(base=500)
    f2 = faixa_da_reserva(36000, 7667.91, sem, t)
    assert f2["antecipacao"] == 0 and f2["mes_no_piso"] == f2["mes_com_extraordinario"], \
        "sem extraordinario declarado, as duas datas coincidem — e a faixa colapsa no piso"


def test_regra_do_extraordinario_muda_com_a_fase():
    from aporte import regra_do_extraordinario
    antes = regra_do_extraordinario(P, reserva_completa=False)
    depois = regra_do_extraordinario(P, reserva_completa=True)
    assert "reserva" in antes["destino"].lower()
    assert "G3" in depois["destino"]
    assert antes["destino"] != depois["destino"]


def test_universo_elegivel_muda_pouco_com_o_aporte_neste_catalogo():
    """Achado da medicao: a critica esta certa em principio e MORDE POUCO aqui. Como o
    catalogo e dominado por rotas de corretagem zero, so `acao_450` entra e sai — e ela
    e dominada por `acao_zero` de qualquer forma. Onde a variabilidade do aporte de
    fato pesa e na DATA DA RESERVA, nao no universo."""
    from aporte import universo_por_aporte
    linhas, limiares = universo_por_aporte(C, P, valores=(200, 500, 20000))
    n = [len(L["dentro"]) for L in linhas]
    assert n[0] < n[1] == n[2], "so um degrau, e ele fecha cedo"
    fixos = [rid for rid, d in limiares.items() if d["motivo"] == "FIXO"]
    assert fixos == ["acao_450"]


# ── F-01: custodia interna do ETF ────────────────────────────────────────────
def test_custodia_interna_entra_no_custo_e_so_em_quem_a_cobra():
    rotas = {r.id: r for r in catalogo(C)}
    CI  = C["etf"]["custodia_interna_ishares"]["valor"]
    alv = set(x.lower() for x in C["etf"]["custodia_interna_ishares"]["aplica_a"])
    for rid in ("bova11", "smal11"):
        assert rid in alv
        assert abs(rotas[rid].custodia_interna_aa - CI) < 1e-12
        assert abs(rotas[rid].interno_aa - (rotas[rid].adm_aa + CI)) < 1e-12
    # quem NAO esta na lista da fonte nao paga: PIBB11 e Itau, IVVB11 tem
    # regulamento proprio nao lido — nenhum dos dois entra pela porta dos fundos
    for rid in ("pibb11", "divo11"):
        assert rotas[rid].custodia_interna_aa == 0.0
        assert rotas[rid].interno_aa == rotas[rid].adm_aa

def test_custodia_interna_muda_o_custo_medido_e_nao_so_o_texto():
    """Se o campo existisse mas nao fosse lido pelo motor, este teste passaria
    igual — por isso ele compara DUAS simulacoes, nao um atributo."""
    from alocacao import simular_custo
    rotas = {r.id: r for r in catalogo(C)}
    b = rotas["bova11"]
    import dataclasses
    sem = dataclasses.replace(b, custodia_interna_aa=0.0)
    p_com, c_com, _ = simular_custo(b,   C, 500.0, 10)
    p_sem, c_sem, _ = simular_custo(sem, C, 500.0, 10)
    assert c_com > c_sem and p_com < p_sem
    # e a diferenca precisa ser material: >1% do custo total, nao arredondamento
    assert (c_com - c_sem)/c_sem > 0.01


# ── B-17: a interpretacao da isencao da custodia vem do YAML ─────────────────
def test_B17_mudar_a_interpretacao_no_yaml_muda_o_custo():
    """Ate 24/09 `simular_custo` nao lia `b3.custodia_rv_interpretacao`: usava o default
    "deducao" de `custodia_rv_aa`, e concordava com o YAML por acidente. A unica leitura
    da chave estava em `motor.simular`, que so testes chamavam (P-43). Mede-se trocando o
    VALOR no YAML e exigindo outro numero -- um teste de atributo passaria nas duas."""
    b = {r.id: r for r in catalogo(C)}["bova11"]
    C2 = copy.deepcopy(C)
    C2["b3"]["custodia_rv_interpretacao"]["valor"] = "limiar"
    _, c_deducao, _ = al_simular(b, C, 5000.0, 25)
    _, c_limiar, _ = al_simular(b, C2, 5000.0, 25)
    # limiar tira a isencao da base: acima dela, cobra desde o primeiro real
    assert c_limiar > c_deducao

def test_B17_interpretacao_fora_das_duas_leituras_falha_em_vez_de_virar_limiar():
    """`custodia_rv_aa` tratava todo valor diferente de "deducao" como "limiar". Com a
    chave lida do YAML, um erro de digitacao mudaria o custo calado (A-05)."""
    b = {r.id: r for r in catalogo(C)}["bova11"]
    C2 = copy.deepcopy(C)
    C2["b3"]["custodia_rv_interpretacao"]["valor"] = "marginal"
    with pytest.raises(ValueError, match="custodia_rv_interpretacao"):
        al_simular(b, C2, 5000.0, 25)


# ── K-06 e K-07, trazidos do test_motor quando o `motor.simular` saiu (P-43) ──
def test_K06_perna_de_saida_e_contabilizada():
    """Teria pego K-06: a rota XP cobra 0,50% na entrada E na saida, e o exterior paga
    IOF de repatriacao. Ate 24/09 isto so era afirmado sobre o catalogo morto
    (`motor.montar_rotas`); aqui e sobre o que o sistema usa -- atributo E simulacao."""
    from alocacao import custo_saida_pct
    rotas = {r.id: r for r in catalogo(C)}
    b3v = val(C["b3"]["vista_total_pct"], contexto="b3")
    xp = rotas["bova11_xp"]
    assert xp.saida_extra == pytest.approx(val(C["corretagem"]["xp_etf_pct"], contexto="xp"))
    assert custo_saida_pct(xp, b3v) == pytest.approx(xp.corr_pct + b3v + xp.saida_extra)
    ext = rotas["ext_avenue"]
    assert ext.saida_extra == pytest.approx(val(C["exterior"]["iof_repatriacao"], contexto="iof"))
    # a perna precisa CUSTAR, nao so existir: sem ela o custo total cai
    for r in (xp, ext):
        _, c_com, _ = al_simular(r, C, 500.0, 10)
        _, c_sem, _ = al_simular(dataclasses.replace(r, saida_extra=0.0), C, 500.0, 10)
        assert c_com > c_sem, r.id

def test_K07_vest_com_iof_nao_confirmado_nao_entra_na_ordenacao():
    """Teria pego K-07: a rota Vest aparecia como a mais barata do exterior porque um
    NAO_CONFIRMADO era renderizado como zero. O teste do BOVV11 (F-02, abaixo) ja existia
    aqui; o da Vest so existia no catalogo morto."""
    from motor import InsumoBloqueado
    vest = {r.id: r for r in catalogo(C)}["ext_vest"]
    assert not vest.confiavel
    with pytest.raises(InsumoBloqueado):
        al_simular(vest, C, 500.0, 10)
    r = alocar(Estado(**BASE), C, P, anos=10)
    assert "ext_vest" in {x.id for x in r["universo"]["fora_status"]}
    assert "ext_vest" not in r["alvo"]["pesos"]


# ── F-02: bloqueio antes de custo ────────────────────────────────────────────
def test_rota_bloqueada_recusa_simular_em_vez_de_valer_zero():
    """Antes, BOVV11 (adm NAO_CONFIRMADO) simulava com custo zero e aparecia como
    a rota MAIS BARATA do catalogo. Insumo ausente nao pode virar o melhor numero."""
    from motor import InsumoBloqueado
    rotas = {r.id: r for r in catalogo(C)}
    b = rotas["bovv11"]
    assert not b.confiavel
    with pytest.raises(InsumoBloqueado):
        al_simular(b, C, 500.0, 10)
    with pytest.raises(InsumoBloqueado):
        arrasto_anualizado(b, C, 500.0, 10)

def test_g5_roda_antes_do_g3_e_o_bloqueado_nunca_e_ranqueado_por_custo():
    """A ordem dos portoes tem consequencia: se o G3 vier primeiro, ele precisa
    atribuir um custo a uma rota cujo custo e desconhecido."""
    e = Estado(**BASE)
    r = alocar(e, C, P, anos=10)
    ids_atrito = {x[0].id for x in r["universo"]["fora_atrito"]}
    ids_vivos  = {x[0].id if isinstance(x, tuple) else x.id for x in r["universo"]["vivos"]}
    assert "bovv11" not in ids_atrito and "bovv11" not in ids_vivos
    assert "bovv11" in {x.id for x in r["universo"]["fora_status"]}


# ── H-01/H-02: rotas novas e regime de banco ─────────────────────────────────
def test_lci_lca_fii_estao_no_catalogo_e_bloqueadas_com_motivo():
    """A doutrina: investimento nao sai por falta de regra. A rota existe, aparece,
    e diz por que nao recebe peso — em vez de sumir do catalogo em silencio."""
    rotas = {r.id: r for r in catalogo(C)}
    for rid in ("lci", "lca", "fii"):
        assert rid in rotas, f"{rid} sumiu do catalogo"
        assert not rotas[rid].confiavel, f"{rid} deveria estar bloqueada"
        assert rotas[rid].bloqueios, f"{rid} bloqueada sem motivo escrito"
        assert any("BLOQUEIA" in b for b in rotas[rid].bloqueios), \
            "F-05: a consequencia tem de viajar junto com o motivo"

def test_lci_perde_todas_as_funcoes_quando_a_carencia_chegar():
    """H-01. Com carencia de 9 meses e SEM vencimento conhecido, a rota nao serve nem
    LASTRO nem DATADO. Desde a 12a (26/09) o DATADO aceita vencimento casado, mas so
    com `vencimento_anos` declarado: sem ele, a regra nova nao tem o que casar."""
    import dataclasses
    rotas = {r.id: r for r in catalogo(C)}
    lci = dataclasses.replace(rotas["lci"], liquidez_dias=270, bloqueios=[])
    ok, _ruins = g6_coerencia_funcao([lci], P)
    assert not ok or not ok[0].funcoes, \
        "rota iliquida SEM vencimento conhecido nao pode ficar com o DATADO (P1)"

def test_P12_DATADO_aceita_vencimento_casado_no_lugar_da_liquidez():
    """12a, decisao dele de 26/09: "vence ate a data do objetivo OU e liquida em 30 dias".
    Casa pelo VENCIMENTO, contra o menor prazo -- nunca pela duracao, que na LCI
    pos-fixada e 0,0 e deixaria passar qualquer carencia. Tres mutacoes: sem o
    vencimento, vencimento alem do objetivo, e a chave desligada no YAML."""
    import copy
    import dataclasses
    rotas = {r.id: r for r in catalogo(C)}
    lci = dataclasses.replace(rotas["lci"], liquidez_dias=270, bloqueios=[],
                              vencimento_anos=1.0)
    ok, _ = g6_coerencia_funcao([lci], P)
    assert ok and "DATADO" in ok[0].funcoes, "com vencimento conhecido, o G6 deixa casar"
    dois = [Objetivo("carro", 10_000, 2)]
    assert casa_duracao(ok[0], dois, P), "vence em 1 ano, objetivo em 2: casa"
    assert not casa_duracao(ok[0], [Objetivo("x", 1, 0.5)], P), "vence depois do objetivo"
    sem = dataclasses.replace(lci, vencimento_anos=None)
    assert not casa_duracao(sem, dois, P), "sem vencimento, iliquida nao casa"
    P2 = copy.deepcopy(P)
    P2["funcoes"]["DATADO"]["liquidez_ou_vencimento_casado"] = False
    ok2, _ = g6_coerencia_funcao([lci], P2)
    assert not ok2 or "DATADO" not in ok2[0].funcoes, "desligado no YAML, volta a reprovar"
    liquida = dataclasses.replace(rotas["lci"], liquidez_dias=1, bloqueios=[])
    assert casa_duracao(liquida, dois, P), "a liquida continua casando pela duracao"


def test_regime_de_banco_esta_especificado_e_declara_a_lacuna_de_dado():
    r = P["regime_instituicao_financeira"]
    assert r["status"] == "ESPECIFICADO_EM_CONSTRUCAO"   # P-14 resolvida em 05/09
    assert r["decisao_P14"]["status"] == "RESOLVIDA"
    assert len(r["bloco_substituto"]) == 5
    # so o Basileia tem piso legal — e essa distincao e o ponto do bloco
    com_piso = [k for k, v in r["bloco_substituto"].items() if v.get("tem_piso_legal")]
    assert com_piso == ["B01_indice_de_basileia"]
    # e a lacuna de fonte de dados precisa estar escrita, nao subentendida
    assert "achado_H02_a_fase_0_nao_alimenta_este_bloco" in r


# ── Bloco C: o regime, nao os campos ─────────────────────────────────────────
def test_bloco_C_recusa_instituicao_financeira_em_vez_de_calcular():
    """A regra que impede o modo de falha do F-02 nesta camada: divida
    liquida/EBITDA aplicado a um banco DEVOLVE um numero, e o numero e lixo."""
    b = P["bloco_C_solvencia"]
    assert b["status"] == "REGIME_ESPECIFICADO"
    r = b["recusa_em_vez_de_calcular"]
    assert "NAO produz numero" in r["regra"]
    # a identificacao ainda nao e automatica, e isso precisa estar declarado
    assert r["como_identificar"]["status"] == "PARCIAL"
    assert r["como_identificar"]["bloqueia"]

def test_bloco_C_declara_que_nenhum_corte_tem_ancora_legal():
    """A diferenca frente ao regime de banco, onde Basileia tem piso legal. Se
    algum dia um corte deste bloco ganhar ancora, esta asserção falha e obriga a
    revisar a doutrina em vez de deixa-la desatualizada em silencio."""
    b = P["bloco_C_solvencia"]["natureza_dos_cortes"]
    assert b["nenhum_corte_tem_ancora_legal"] is True
    banco = P["regime_instituicao_financeira"]["bloco_substituto"]
    assert banco["B01_indice_de_basileia"]["tem_piso_legal"] is True

def test_bloco_C_admite_em_voz_alta_o_que_nao_sabe():
    """C-04 e C-05 nao foram inventados. Um bloco de exclusao com criterio
    inventado excluiria empresa por regra que ninguem escolheu."""
    lac = P["bloco_C_solvencia"]["lacuna_declarada"]
    assert "C-04" in lac["o_que_falta"] and "C-05" in lac["o_que_falta"]
    assert lac["para_fechar"]
    ordem = " ".join(P["bloco_C_solvencia"]["ordem"])
    assert "LACUNA DECLARADA" in ordem, "a ordem tem de carregar a lacuna, nao escondê-la"


# ── P-07 / I-01: a ordem dos portoes virou dado ──────────────────────────────
def test_ordem_dos_portoes_vem_do_yaml_e_nao_do_codigo():
    from alocacao import ordem_dos_portoes
    nomes = [n for n, _ in ordem_dos_portoes(P)]
    assert nomes == ["G6_coerencia_funcao", "G0_match_empregador", "G1_divida",
                     "G2_reserva", "G5_status", "G3_atrito", "G7_tese_registrada",
                     "G8_compromisso_de_carrego", "G4_dominancia"]

def test_I01_a_ordem_real_nunca_foi_G0_ate_G8():
    """O achado: a numeracao sugeria uma sequencia que o codigo nao executa.
    G6 roda primeiro e G4 por ultimo. Se alguem 'consertar' a ordem para ficar
    numerica, este teste avisa que isso muda o comportamento."""
    from alocacao import ordem_dos_portoes
    nomes = [n for n, _ in ordem_dos_portoes(P)]
    assert nomes[0].startswith("G6") and nomes[-1].startswith("G4")
    assert nomes != sorted(nomes), "a ordem NAO e a numerica — e esse e o ponto"

def test_trocar_a_ordem_no_yaml_muda_o_comportamento():
    """Se a ordem fosse decorativa, este teste passaria com a lista invertida.
    Ele reproduz o F-02: G3 antes do G5 faz rota bloqueada ser ranqueada por custo."""
    P2 = copy.deepcopy(P)
    P2["portoes"]["G3_atrito"]["ordem"] = 5     # G3 passa a vir
    P2["portoes"]["G5_status"]["ordem"] = 6     # antes do G5, como era ate o F-02
    from alocacao import ordem_dos_portoes
    nomes = [n for n, _ in ordem_dos_portoes(P2, fase="universo")]
    assert nomes.index("G3_atrito") < nomes.index("G5_status")
    e = Estado(**BASE)
    from motor import InsumoBloqueado
    with pytest.raises(InsumoBloqueado):
        alocar(e, C, P2, anos=10)   # o G3 tenta custear a rota bloqueada e o F-02 barra

def test_portao_sem_ordem_declarada_e_erro_duro():
    """Padrao silencioso e o que a P1 proibe. Sem `ordem`, o motor recusa."""
    from alocacao import ordem_dos_portoes
    P2 = copy.deepcopy(P); del P2["portoes"]["G4_dominancia"]["ordem"]
    with pytest.raises(ValueError, match="sem `ordem` declarada"):
        ordem_dos_portoes(P2)

def test_portao_declarado_na_fase_universo_sem_execucao_falha_alto():
    """P2 ao contrario: declarar sem implementar. O motor recusa em vez de ignorar."""
    P2 = copy.deepcopy(P)
    P2["portoes"]["G9_inventado"] = {"ativo": True, "ordem": 10, "fase": "universo"}
    e = Estado(**BASE)
    with pytest.raises(ValueError, match="sem execucao no motor"):
        alocar(e, C, P2, anos=10)


# ── P-13: isento_ir virou dois campos ────────────────────────────────────────
def test_fii_expressa_rendimento_isento_e_ganho_tributado():
    """O caso que quebrava o booleano: True subestimava o imposto do FII, False
    superestimava, e nenhum dos dois estava certo."""
    r = {x.id: x for x in catalogo(C)}["fii"]
    assert r.isento_ir_rendimento is True   # Lei 11.033/2004 art. 3o, >=100 cotistas
    assert r.aliquota_ganho == 0.20         # Lei 8.668/1993 art. 18
    assert r.isento_ir is True              # o campo antigo sempre falou do rendimento

def test_lci_lca_tem_as_duas_pontas_isentas():
    rotas = {x.id: x for x in catalogo(C)}
    for rid in ("lci", "lca"):
        assert rotas[rid].isento_ir_rendimento is True
        assert rotas[rid].aliquota_ganho == 0.0

def test_rota_tributada_normal_nao_declara_aliquota_propria():
    """None significa 'usa a tabela geral', nao 'zero'. Confundir os dois seria o
    F-02 outra vez: ausencia virando o numero mais favoravel."""
    rotas = {x.id: x for x in catalogo(C)}
    assert rotas["rdb_100"].aliquota_ganho is None
    assert rotas["rdb_100"].isento_ir_rendimento is False
    assert rotas["acao_zero"].aliquota_ganho is None

def test_o_campo_antigo_continua_lendo_o_que_sempre_leu():
    """Compatibilidade: `isento_ir` sempre se referiu ao rendimento. O rename so
    tornou explicito — se algum chamador antigo mudasse de resposta, seria bug."""
    for r in catalogo(C):
        assert r.isento_ir == r.isento_ir_rendimento


# ── P6: ausencia de criterio nao e criterio de exclusao ──────────────────────
def test_doutrina_P6_existe_e_lista_as_tres_correcoes():
    """Promovida a doutrina depois de a MESMA correcao ser necessaria tres vezes.
    Se voltar a quatro, o problema nao e do usuario."""
    d = P["doutrina_P6"]
    assert len(d["as_tres_vezes"]) == 3
    assert d["teste_pratico"] and d["o_que_ela_NAO_proibe"]

def test_nada_sai_do_universo_por_falta_de_regua():
    """A P6 na pratica: toda entrada de fora_de_escopo tem de dizer o que falta e
    como reentra. `reentra: nao previsto` so vale quando o usuario DECLAROU que nao
    opera aquilo — nunca quando o projeto e que nao sabe medir."""
    for nome, spec in P["fora_de_escopo"].items():
        if isinstance(spec, str): continue
        assert spec.get("reentra"), f"{nome} sem condicao de reentrada"
        if spec.get("reentra") == "nao previsto":
            # P6: exclusao permanente exige FUNDAMENTO declarado, e so ha dois
            # legitimos. "ainda nao temos regua" descreve o projeto, nao o ativo.
            assert spec.get("fundamento") in ("DECISAO_DO_USUARIO", "CRITERIO_MEDIDO"), \
                f"{nome}: exclusao permanente sem fundamento legitimo declarado"

def test_banco_nao_foi_excluido_e_a_segunda_esteira_esta_declarada():
    r = P["regime_instituicao_financeira"]
    assert "NAO sai do universo" in r["decisao_P14"]["resposta"]
    assert "DUAS esteiras" in r["decisao_P14"]["consequencia_para_a_fase_0"]

def test_bloco_C_hibrido_com_degradacao_declarada():
    """P-16a: o usuario escolheu hibrido. A metade que corta roda hoje; a que marca
    espera a serie EM VOZ ALTA, como o REGRA_DECIDIDA faz em teses.yaml."""
    n = P["bloco_C_solvencia"]["nivel_ou_tendencia"]
    assert n["status"] == "RESOLVIDA" and "HIBRIDO" in n["resposta"]
    assert "AGUARDA_SERIE" in n["degradacao_declarada"]

def test_bloco_C_admite_empresa_sem_dado_e_explica_por_que_nao_e_o_caso_BOVV11():
    e = P["bloco_C_solvencia"]["empresa_sem_dado"]
    assert e["status"] == "RESOLVIDA" and "ADMITIR" in e["resposta"]
    assert "ordenacao" in e["diferenca_para_o_caso_BOVV11"]


def test_nao_operar_nao_e_fundamento_de_exclusao():
    """Correcao do usuario em 05/09: 'nao opero opcoes' descreve a carteira dele,
    que esta vazia — numa carteira vazia isso e verdade para TODO ativo, e portanto
    nao distingue nada. Resposta factual nao autoriza exclusao."""
    import re
    estado = re.compile(r"o usuario (nao opera|nao tem|nao possui)\b", re.I)
    for nome, spec in P["fora_de_escopo"].items():
        if not isinstance(spec, dict): continue
        if spec.get("fundamento") != "DECISAO_DO_USUARIO": continue
        m = spec.get("motivo", "")
        assert not estado.search(m), (
            f"{nome}: o fundamento DECISAO_DO_USUARIO se apoia num ESTADO "
            f"('nao opera'), nao numa decisao ('nao quer'). Ver doutrina_P6.")

def test_opcoes_deixou_de_ser_exclusao_permanente():
    o = P["fora_de_escopo"]["opcoes"]
    assert o.get("fundamento") is None
    assert "quando houver" in o["reentra"]   # condicao de reentrada, nao exclusao
    assert o["o_que_falta"], "P6: exclusao sem fundamento vira pendencia COM o que falta"
    # o contexto que ele trouxe separou duas familias com perfis de perda opostos
    assert "COBERTA" in o["duas_familias_que_nao_podem_compartilhar_regua"]
    assert "EXCEDER o capital" in o["duas_familias_que_nao_podem_compartilhar_regua"]

def test_P6_registra_a_armadilha_da_pergunta_factual():
    assert "resposta factual nao autoriza exclusao" in \
        P["doutrina_P6"]["a_armadilha_da_pergunta_factual"]


# ── J-01: reserva empenhada nao e reserva ────────────────────────────────────
def test_reserva_empenhada_nao_conta_como_meses_cobertos():
    """O caso real: cofrinho do PicPay usado como garantia do limite do cartao,
    'Disponivel para resgate: R$ 0,00'. Contar 1,9 mes de reserva ali seria
    responder 'quanto eu tenho' quando a pergunta do G2 e 'quantos meses eu aguento'."""
    e = Estado(despesa_mensal=4000, reserva_atual=7671.01, reserva_disponivel=0.0,
               aporte_mensal=500, horizonte_anos=10)
    assert e.meses_cobertos == 0.0
    assert abs(e.meses_cobertos_nominal - 1.9177) < 1e-3
    assert abs(e.reserva_empenhada - 7671.01) < 1e-9

def test_ausencia_de_informacao_nao_vira_empenho_presumido():
    """A P1 ao contrario: nao inventar o numero ruim tambem e nao inventar. Quem nao
    declara `reserva_disponivel` tem reserva inteira, nao reserva zero."""
    e = Estado(despesa_mensal=4000, reserva_atual=7671.01, aporte_mensal=500,
               horizonte_anos=10)
    assert e.reserva_efetiva == 7671.01 and e.reserva_empenhada == 0.0

# P-146 (25/09): le o alocacao/estado.yaml, que e PRIVADO por desenho (fora do git, secao
# 11.6). O CI exclui `privado` por nome; na maquina dele o teste roda e falha alto se o
# arquivo sumir -- pular por ausencia reabriria a P-142.
@pytest.mark.privado
def test_estado_real_nao_tem_mais_reserva_empenhada_a_denunciar():
    """O aviso de empenho continua no motor e vale para quem empenhar reserva de
    verdade. O estado dele deixou de dispara-lo porque a reserva virou 0,00 e o
    deposito saiu do campo — o modelo certo era mais simples que o meu.

    P-71, achado lateral: `dados["meses_cobertos"]` nao existe mais (duplicava a
    property de `Estado`, e quebrava `Estado(**dados)` — o proprio caminho que este
    teste agora exercita, em vez de ler uma segunda formula da mesma conta)."""
    import yaml as _y, estado_io
    d = _y.safe_load(open(os.path.join(AQUI, "estado.yaml"), encoding="utf-8"))
    dados, problemas, _av = estado_io.validar(d)
    assert not any("RESERVA EMPENHADA" in p for p in problemas)
    assert dados["reserva_atual"] == 0.0
    assert Estado(**dados).meses_cobertos == 0.0

def test_o_aviso_de_empenho_continua_funcionando_para_quem_empenhar():
    """A maquinaria nao virou codigo morto: ela so nao e exercitada pelo estado dele."""
    import estado_io
    d = {"meta": {"status": "REAL"}, "despesa_mensal": 4000, "reserva_atual": 10000,
         "reserva_disponivel": 2000, "aporte_mensal": 500, "horizonte_anos": 10,
         "estabilidade_renda": "baixa"}
    _dados, problemas, _av = estado_io.validar(d)
    assert any("RESERVA EMPENHADA" in p for p in problemas)


def test_mille_pre_registrada_com_a_critica_setorial_ANTES_de_rodar():
    """A critica tem de estar no registro antes do teste. Depois de ver o resultado,
    qualquer ressalva parece ter sido a original — e a margem de 20% e um filtro
    setorial disfarcado de filtro de qualidade."""
    m = P["estrategias_pre_registradas"]["mille_v1"]
    assert m["status"] == "PRE_REGISTRADA_NAO_EXECUTAVEL"
    assert "FILTRO SETORIAL" in m["critica_a_registrar_ANTES_de_rodar"]
    assert "controle setorial" in m["hipotese_nula_esperada"] or \
           "controle setorial" in m["critica_a_registrar_ANTES_de_rodar"]
    # e o registro tem de admitir que so 3 dos 4 pilares sao mensuraveis
    assert "NAO_testavel" in m["o_que_e_testavel_e_o_que_nao_e"]


def test_decisao_J01_registra_o_custo_em_meses_e_a_pergunta_aberta():
    """A decisao foi tomada (registrar zero) mas o registro nao pode fingir que a
    questao fechou: se o empenho for automatico, aportar no cofrinho constroi limite
    de cartao, nao reserva — e a Fase A vira um laco."""
    d = P["decisoes"]["J01_reserva_empenhada"]
    # RESOLVIDA: o usuario desfez o no dizendo que aquele valor nao e reserva, e
    # sim caucao de meio de pagamento. O modelo certo era mais simples que o meu.
    assert d["status"] == "RESOLVIDA"
    assert "NUNCA FOI RESERVA" in d["resolucao_final_05_09_2026"]
    assert "EU DRAMATIZEI" in d["correcao_do_assistente_J02"]
    assert d["custo_medido_da_decisao"]["custo_em_meses"] == 14
    assert d["pergunta_aberta_que_so_o_usuario_responde"]
    assert "NAO CONSTROI RESERVA" in d["PORQUE_SO_PARCIALMENTE_RESOLVIDA"]


# ── K-01: o pedagio do Cofrinho Turbinado ────────────────────────────────────
def test_turbinado_nao_se_paga_dentro_do_proprio_teto():
    """A aritmetica que decide: 19 p.p. de CDI so cobrem R$287,88/ano de mensalidade
    a partir de R$13.625 — e o produto aceita no maximo R$10.000. Pagando, ele NUNCA
    se paga. Se o CDI subir muito, este teste falha e obriga a refazer a conta."""
    from motor import val
    cdi = val(C["macro"]["cdi_aa"], contexto="cdi")
    teto = C["cofrinho"]["turbinado_teto"]["valor"]
    mensal = C["cofrinho"]["turbinado_mensalidade"]["valor"]
    extra_liq = cdi * (C["cofrinho"]["turbinado_pct_cdi"]["valor"]
                       - C["cofrinho"]["picpay_pct_cdi"]["valor"]) * 0.80
    empate = mensal * 12 / extra_liq
    assert empate > teto, (
        f"a conta mudou: empate em {empate:.2f} contra teto de {teto:.2f}. "
        f"Se o empate caiu abaixo do teto, o achado K-01 deixou de valer")
    assert teto * extra_liq - mensal * 12 < 0   # no teto, ainda perde

def test_isencao_do_turbinado_esta_nao_confirmada_e_bloqueia():
    """P1: o custo efetivo da rota depende de uma condicao que ninguem confirmou."""
    n = C["cofrinho"]["turbinado_condicao_de_isencao"]
    # PARCIAL desde 05/09: a via e conhecida (missoes mensais) mas a condicao do mes
    # seguinte e desconhecida POR CONSTRUCAO — o banco escolhe e muda.
    assert n["status"] == "PARCIAL"
    assert "custo_efetivo_da_rota_cofrinho_turbinado" in n["bloqueia"]
    assert "projecao_de_custo_do_turbinado_alem_do_mes_corrente" in n["bloqueia"]

def test_teto_de_saldo_saiu_das_limitacoes_porque_foi_IMPLEMENTADO():
    """Este teste mudou de sentido em 05/09/2026, e a mudanca e o registro.

    Ele existia para garantir que a limitacao continuasse ESCRITA enquanto nao fosse
    resolvida. P-24 a resolveu: `teto_de_saldo` existe em RotaAloc e o G2 devolve
    composicao. Uma limitacao resolvida que permanece declarada e ruido — na proxima
    leitura alguem gastaria uma sessao reimplementando o que ja existe.

    No lugar entrou a limitacao que o proprio conserto criou: com varios baldes, um
    escalar de reserva nao basta."""
    assert "rota_com_teto_de_saldo" not in P["limitacoes_declaradas"]
    lim = P["limitacoes_declaradas"]["reserva_e_um_numero_e_o_mundo_tem_baldes"]
    assert "reserva_por_rota" in lim["como_apareceu"]
    assert "NAO" in lim["o_que_o_motor_faz_quando_nao_sabe"], \
        "a limitacao tem de dizer o que o motor NAO supoe, nao so o que falta"
    assert "RECOMENDAR DEMAIS" in lim["direcao_do_vies"]


# ── J-02: reserva empenhada em divida do proprio usuario ─────────────────────
def test_limitacao_de_acoplamento_existe_mas_nao_se_aplica_a_ele():
    """O principio vale em geral; o caso dele nao e esse. Deduzir risco de uma
    estrutura sem perguntar o proposito dela foi o erro — e o registro guarda as
    duas coisas separadas, porque a limitacao do motor continua real."""
    lim = P["limitacoes_declaradas"]["reserva_e_divida_tratadas_como_independentes"]
    assert "correlacao -1" in lim["por_que_e_pior_que_iliquidez"]
    assert lim["aplica_se_ao_caso_do_usuario"] is False

# P-146 (25/09): le o alocacao/estado.yaml, que e PRIVADO por desenho (fora do git, secao
# 11.6). O CI exclui `privado` por nome; na maquina dele o teste roda e falha alto se o
# arquivo sumir -- pular por ausencia reabriria a P-142.
@pytest.mark.privado
def test_reserva_e_zero_e_o_deposito_esta_fora_dela():
    """O modelo do usuario: aquele dinheiro nao e reserva, e caucao de meio de
    pagamento. Nao compete no G2, nao conta meses, nao entra em patrimonio."""
    import yaml as _y
    d = _y.safe_load(open(os.path.join(AQUI, "estado.yaml"), encoding="utf-8"))
    assert d["reserva_atual"] == 0.00
    g = d["deposito_garantia"]
    assert g["valor"] == 7671.01 and g["proposito"]
    # CORRIGIDO: o cofrinho vira limite 1 PARA 1, mais 6,9% de bonus. A razao de
    # 14,5:1 que eu havia calculado veio de ler o bonus como retorno inteiro.
    assert g["razao_deposito_limite"] == 1.0
    assert abs(g["limite_base_sem_cofrinho"] + g["valor"] + g["bonus_por_guardar"]
               - g["limite_total_picpay"]) < 0.01, "a conta do limite tem de fechar"

def test_J03_foi_refutado_e_o_registro_guarda_o_erro():
    """O achado caiu quando o usuario deu o limite TOTAL. O registro guarda a
    refutacao junto com o metodo que a causou — deduzir de um fragmento."""
    d = P["decisoes"]["J01_reserva_empenhada"]
    assert "achado_J03_REFUTADO" in d
    txt = d["achado_J03_REFUTADO"]
    assert "ERRADO" in txt and "1 PARA 1" in txt
    assert "sem perguntar o limite TOTAL" in txt   # o metodo que causou o erro

def test_a_isencao_do_turbinado_tem_custo_nao_medido():
    """K-03: R$23,99 nao foi dispensada, foi paga em gasto no cartao e chave Pix.
    Os R$287,88/ano do K-01 sao o PISO, nao o total."""
    n = C["cofrinho"]["turbinado_condicao_de_isencao"]
    assert "PISO do custo" in n["achado_K03_a_isencao_nao_e_gratuita"]
    assert n["valor"] == "MISSOES MENSAIS"


# ── L-01: a fronteira entre o motor e UM usuario ─────────────────────────────
def test_secoes_de_perfil_nao_podem_voltar_para_a_politica():
    """A fronteira se apaga sozinha se ninguem a guardar: a proxima sessao que
    escrever uma decisao do usuario vai escreve-la onde as outras estao. Este teste
    e o que torna caro fazer isso."""
    import yaml as _y
    from alocacao import SECOES_DE_PERFIL
    pol = _y.safe_load(open(os.path.join(AQUI, "politica.yaml"), encoding="utf-8"))
    intrusas = [s for s in SECOES_DE_PERFIL if s in pol]
    assert not intrusas, f"secoes de usuario dentro de politica.yaml: {intrusas}"

def test_carregar_politica_recusa_perfil_que_redefine_o_motor():
    """Perfil descreve escolhas; nao redefine regra. Se pudesse sobrescrever
    `portoes` ou `funcoes`, dois usuarios teriam motores diferentes e nada do que
    o sistema mede seria comparavel."""
    import tempfile, yaml as _y
    with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False,
                                     encoding="utf-8") as f:
        _y.dump({"meta": {"usuario": "x"}, "portoes": {"G9": {}}}, f)
        caminho = f.name
    with pytest.raises(ValueError, match="nao redefine o motor"):
        carregar_politica(perfil=caminho)

def test_o_perfil_tem_hash_proprio():
    """Procedencia por usuario: dois perfis diferentes produzem saidas diferentes,
    e o output precisa dizer QUAL perfil gerou aquilo."""
    P2 = carregar_politica()
    assert P2["_hash_perfil"] and P2["_hash_perfil"] != P2["_hash"]
    assert P2["_perfil"]["usuario"]

def test_trocar_de_perfil_troca_a_decisao_sem_tocar_na_politica():
    """A prova de que a separacao serve para alguma coisa: outro usuario, outro
    teto de compromisso, mesmo motor."""
    import tempfile, yaml as _y
    with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False,
                                     encoding="utf-8") as f:
        _y.dump({"meta": {"usuario": "outro"},
                 "compromissos": {"maximo_anos": 25},
                 "decisoes": {}}, f)
        caminho = f.name
    P2 = carregar_politica(perfil=caminho)
    assert P2["compromissos"]["maximo_anos"] == 25
    assert P2["_perfil"]["usuario"] == "outro"
    assert P2["portoes"] == P["portoes"]        # o motor nao mudou


def test_M01_a_alavanca_do_aporte_e_dez_vezes_a_do_destino():
    """O achado que reordena a Fase A. Se algum dia o destino passar a importar mais
    que o aporte, este teste falha e obriga a rever a conclusao."""
    m = P["fase_A_recalculada"]
    assert m["verdade"]["meses"] == 56 and m["antes_dizia"]["meses"] == 42
    assert m["atraso_em_meses"] == 14
    txt = m["ACHADO_M01_o_portao_ativo_e_o_que_menos_importa"]
    assert "3 meses" in txt and "33" in txt
    # e a ressalva tem de viajar junto: o achado vale para a Fase A, nao para sempre
    assert "Fase B e C" in m["o_que_isso_NAO_significa"]


# ══ P-24 / K-02 / O-01 · o G2 devolve composicao, nao rota unica ═════════════
def _liq(C_=None):
    return [r for r in catalogo(C_ or C) if "LIQUIDEZ" in r.funcoes and r.confiavel]


def test_P24_teto_de_saldo_nao_e_teto_do_FGC():
    """Erro de categoria com consequencias OPOSTAS. Passar do FGC deixa dinheiro sem
    seguro — um risco que se pode escolher aceitar. Passar do teto do produto e
    impossivel: o deposito e recusado. Um portao que so conhece o primeiro recomenda
    um destino que nao existe mais."""
    t = next(r for r in catalogo(C) if r.id == "picpay_turbinado")
    assert t.teto_de_saldo == 10_000.0 and t.emissor == "BANCO_MEDIO"
    assert t.capacidade(0) == 10_000.0 and t.capacidade(7_000) == 3_000.0
    assert t.capacidade(12_000) == 0.0, "teto estourado nao devolve capacidade negativa"
    rdb = next(r for r in catalogo(C) if r.id == "rdb_100")
    assert rdb.teto_de_saldo is None and rdb.capacidade(1e9) is None, \
        "teto NAO DECLARADO nao pode virar infinito em silencio — devolve None"


def test_O01_o_retorno_do_tesouro_selic_depende_do_saldo_e_a_media_esconde():
    """O achado que a composicao expos. `retorno_liquido_aa` devolve a MEDIA da pilha:
    avaliado em R$10 mil o td_reserva ganha do rdb_100; avaliado em R$36 mil, perde.
    Nenhum dos dois numeros descreve um real especifico."""
    dias = P["portoes"]["G2_reserva"]["horizonte_ir_dias"]
    td = next(r for r in _liq() if r.id == "td_reserva")
    rdb = next(r for r in _liq() if r.id == "rdb_100")
    assert retorno_liquido_aa(td, C, dias, 10_000) > retorno_liquido_aa(rdb, C, dias, 10_000)
    assert retorno_liquido_aa(td, C, dias, 36_000) < retorno_liquido_aa(rdb, C, dias, 36_000)
    # o marginal, ao contrario da media, e uma escada exata de dois degraus
    segs = segmentos_de_capacidade(td, C, dias)
    assert len(segs) == 2 and segs[0][1] == 10_000.0 and segs[1][1] is None
    assert abs((segs[0][0] - segs[1][0]) - val(C["tesouro"]["custodia_aa"])) < 1e-12, \
        "a diferenca entre os dois degraus TEM de ser exatamente a custodia do Tesouro"


def test_O01_a_composicao_bate_o_melhor_destino_unico():
    """A afirmacao que justifica trocar o contrato do portao. Se a composicao NAO
    ganhasse da melhor rota unica, a complexidade nao se pagaria."""
    dias = P["portoes"]["G2_reserva"]["horizonte_ir_dias"]
    alvo = 36_000.0
    comp = compor_reserva(_liq(), C, P, alvo)
    melhor_unica = max(alvo*retorno_liquido_aa(r, C, dias, alvo) for r in _liq())
    assert comp["ganho_anual"] > melhor_unica
    assert [t["rota_id"] for t in comp["tramos"]] == ["td_reserva", "rdb_100"]
    assert comp["tramos"][0]["valor"] == val(C["tesouro"]["isencao_selic"]), \
        "o primeiro tramo tem de parar EXATAMENTE na isencao de custodia"


def test_P24_a_composicao_reduz_a_exposicao_a_um_emissor_privado():
    """O ganho em reais e pequeno (~R$8 ao ano). O ganho que importa e outro: a rota
    unica obrigava a escolher ENTRE o melhor retorno e o melhor credito. A composicao
    nao precisa escolher — R$10 mil vao para o Tesouro e o resto para onde rende
    mais. Medir so o retorno aqui seria medir a metade errada."""
    comp = compor_reserva(_liq(), C, P, 36_000.0)
    privado = sum(t["valor"] for t in comp["tramos"] if t["emissor"] != "TESOURO_NACIONAL")
    assert privado == 26_000.0, "10 mil sairam do emissor privado sem custar retorno"


def test_K02_com_teto_a_rota_unica_promete_retorno_sobre_dinheiro_recusado():
    """O achado K-02 em numeros, e e mais grave do que 'o portao para de funcionar'.

    Com a isencao do Turbinado confirmada, o G2 ANTIGO elegeria o Turbinado avaliando-o
    no alvo inteiro: R$36.000 a 13,03% = R$4.692 ao ano. O produto aceita R$10.000. O
    numero nao era otimista — era sobre dinheiro que o produto RECUSA. A composicao
    devolve R$4.112, que e o que existe."""
    C2 = copy.deepcopy(C)
    C2["cofrinho"]["turbinado_condicao_de_isencao"]["status"] = "COMPLETO"
    liq2 = _liq(C2)
    dias = P["portoes"]["G2_reserva"]["horizonte_ir_dias"]
    turbo = next(r for r in liq2 if r.id == "picpay_turbinado")
    fantasia = 36_000.0 * retorno_liquido_aa(turbo, C2, dias, 36_000.0)
    comp = compor_reserva(liq2, C2, P, 36_000.0)
    assert comp["tramos"][0]["rota_id"] == "picpay_turbinado"
    assert comp["tramos"][0]["valor"] == 10_000.0, "o teto do produto tem de cortar aqui"
    assert comp["ganho_anual"] < fantasia
    assert fantasia - comp["ganho_anual"] > 500, \
        "a diferenca entre o prometido e o possivel passa de R$500 ao ano"
    assert sum(t["valor"] for t in comp["tramos"]) == 36_000.0


def test_P24_o_turbinado_entra_bloqueado_e_nao_ausente():
    """Doutrina P6. A isencao da mensalidade depende de missoes que mudam todo mes e
    que o banco escolhe — o custo do mes seguinte e desconhecido POR CONSTRUCAO. Isso
    bloqueia a rota; nao a apaga. E o `bloqueia` do custos.yaml passa a ter efeito
    (achado F-05)."""
    turbo = next(r for r in catalogo(C) if r.id == "picpay_turbinado")
    assert not turbo.confiavel and "PARCIAL" in turbo.bloqueios[0]
    assert turbo not in _liq(), "rota bloqueada nao entra na composicao da reserva"
    with pytest.raises(InsumoBloqueado):
        al_simular(turbo, C, 500, 10)


def test_P24_o_cofrinho_do_usuario_existe_no_catalogo_e_NAO_e_liquidez():
    """Era a unica posicao que ele possui, e nao existia no catalogo — o pior caso da
    P6: opinar sobre onde por dinheiro sem enxergar onde o dinheiro esta.

    Entra, e entra sem a funcao que o marketing sugere. O saldo e caucao do limite do
    cartao: destrava ao pagar a fatura e volta a travar. A espera vai de 0 a 29 dias
    conforme o dia da emergencia, e reserva se julga pelo PIOR caso."""
    cof = next(r for r in catalogo(C) if r.id == "picpay_cofrinho")
    assert cof.confiavel, "o produto e conhecido: nao ha insumo faltando"
    assert "LIQUIDEZ" not in cof.funcoes and cof.liquidez_dias == 29
    assert cof.rendimento_fator > 1.0, "rende ACIMA do CDI e ainda assim nao serve"
    assert cof not in _liq()


def test_P24_reserva_e_um_numero_e_o_mundo_tem_baldes():
    """Com teto por produto, 'quanto ha de reserva' deixa de bastar: para saber se a
    proxima parcela cabe e preciso saber ONDE ela esta. O motor nao supoe — avisa."""
    e = Estado(**{**BASE, "reserva_atual": 12_000})
    d = g2_reserva(e, catalogo(C), C, P)
    assert any("NAO SABE em quais rotas" in a for a in d.memoria["alertas"])

    e2 = Estado(**{**BASE, "reserva_atual": 12_000,
                   "reserva_por_rota": {"td_reserva": 10_000, "rdb_100": 2_000}})
    d2 = g2_reserva(e2, catalogo(C), C, P)
    assert e2.reserva_conferida is True
    assert not any("NAO SABE" in a for a in d2.memoria["alertas"])
    # a isencao do td_reserva ja esta consumida: o proximo real vai para o rdb
    assert d2.memoria["composicao"][0]["rota_id"] == "rdb_100"

    e3 = Estado(**{**BASE, "reserva_atual": 12_000,
                   "reserva_por_rota": {"td_reserva": 5_000}})
    assert e3.reserva_conferida is False
    d3 = g2_reserva(e3, catalogo(C), C, P)
    assert any("nao escolhe entre os dois" in a for a in d3.memoria["alertas"])


def test_P24_alvo_que_nao_cabe_nos_tetos_vira_alerta_e_nao_truncamento():
    """Se os tetos somarem menos que o alvo, o portao NAO pode devolver uma composicao
    parcial em silencio — seria a mesma familia do F-02: resposta bem formada sobre
    uma premissa que nao vale."""
    rotas = [dataclasses.replace(r, teto_de_saldo=5_000.0) for r in _liq()]
    comp = compor_reserva(rotas, C, P, 36_000.0)
    assert comp["nao_alocado"] == 36_000.0 - 5_000.0*len(rotas)
    e = Estado(**{**BASE, "reserva_atual": 0})
    d = g2_reserva(e, rotas + [r for r in catalogo(C) if "LIQUIDEZ" not in r.funcoes], C, P)
    assert any("SEM DESTINO" in a for a in d.memoria["alertas"])


def test_P24_o_veredito_diz_quantas_rotas_porque_uma_so_deixou_de_ser_verdade():
    d = g2_reserva(Estado(**{**BASE, "reserva_atual": 0}), catalogo(C), C, P)
    assert "EM 2 ROTAS" in d.veredito
    assert len(d.memoria["composicao"]) == 2
    assert d.memoria["ganho_anual_da_composicao"] > 0


# ══ P-15 · procedencia do AMBIENTE, nao so do dado ═══════════════════════════
@pytest.mark.repositorio   # 146b: le ou roda o fonte, que a mutacao instrumenta
def test_P15_toda_dependencia_de_terceiro_esta_declarada():
    """O "funciona na minha maquina" em forma testavel, e nos DOIS sentidos.

    Varre o AST de todos os modulos, separa o que e biblioteca padrao e o que e do
    projeto, e cobra que o resto esteja no pyproject. A armadilha que este teste
    existe para pegar tem nome: `import yaml` instala-se como `PyYAML`, e quem confia
    no nome do import esquece de declarar. Por isso o mapa e explicito e nao
    adivinhado."""
    D = ambiente.declarado()
    locais = {os.path.splitext(f)[0] for f in os.listdir(AQUI) if f.endswith(".py")}
    padrao = set(sys.stdlib_module_names)
    usados = set()
    for f in sorted(x for x in os.listdir(AQUI) if x.endswith(".py")):
        for n in ast.walk(ast.parse(open(os.path.join(AQUI, f), encoding="utf-8").read())):
            alvo = []
            if isinstance(n, ast.Import):
                alvo = [a.name.split(".")[0] for a in n.names]
            elif isinstance(n, ast.ImportFrom) and n.level == 0 and n.module:
                alvo = [n.module.split(".")[0]]
            usados |= {m for m in alvo if m not in locais and m not in padrao}

    declarados_como_import = {ambiente.PACOTE_PARA_IMPORT.get(k, k).lower()
                              for k in D["versoes"]}
    indeclarados = sorted(m for m in usados if m.lower() not in declarados_como_import)
    assert not indeclarados, (
        "importado e NAO declarado no pyproject: " + ", ".join(indeclarados) +
        ". Um clone novo quebraria, e so na hora de rodar.")

    usados_norm = {m.lower() for m in usados}
    supérfluos = sorted(k for k in D["versoes"]
                        if ambiente.PACOTE_PARA_IMPORT.get(k, k).lower() not in usados_norm)
    assert not supérfluos, (
        "declarado e nunca importado: " + ", ".join(supérfluos) +
        ". Dependencia morta e o mesmo defeito do P-28 noutro arquivo — o pyproject "
        "passa a descrever um ambiente maior que o necessario.")


def test_P15_nenhuma_dependencia_tem_faixa_de_versao(tmp_path):
    """`>=` permite que um `pip install` amanha mude um numero registrado hoje sem
    nada avisar. Este projeto nao e uma biblioteca que outros importam: e um sistema
    que produz numeros que alguem vai defender."""
    D = ambiente.declarado()
    assert D["versoes"], "o pyproject tem de declarar dependencias"
    for pacote, v in D["versoes"].items():
        assert re.fullmatch(r"\d+(\.\d+)*", v), f"{pacote}: versao {v!r} nao e um pino"

    # e a recusa e do LEITOR, nao um grep no texto: `build-system.requires` usa `>=68`
    # legitimamente, e um teste que olhasse o arquivo inteiro estaria olhando a linha
    # errada. O que precisa ser pinado sao as dependencias do projeto.
    # P-141: era `AQUI/_pyproject_frouxo.toml`, caminho fixo dentro do repositorio: duas
    # rodadas simultaneas disputavam o mesmo arquivo, e o `os.remove` de uma derrubava a
    # outra. Era o unico teste das tres suites que escrevia em caminho fixo.
    frouxo = tmp_path / "_pyproject_frouxo.toml"
    frouxo.write_text(
        '[project]\nname="x"\nversion="0"\nrequires-python="==3.11.*"\n'
        'dependencies=["numpy>=2.0"]\n', encoding="utf-8")
    with pytest.raises(ambiente.AmbienteIndeclarado):
        ambiente.declarado(str(frouxo))


def test_P15_toda_dependencia_declarada_esta_instalada():
    """Erro duro, e o unico do bloco P-15 que e. Uma dependencia declarada e ausente
    significa que o projeto nao roda inteiro — nao ha resultado a discutir."""
    _, _, ausentes = ambiente.conferir(avisar=False)
    assert not ausentes, ("declarado no pyproject e NAO instalado: " + ", ".join(ausentes))


def test_P15_a_impressao_registrada_bate_com_o_pyproject():
    """O mesmo contrato do sha256 da serie do NEFIN, aplicado ao ambiente.

    As versoes vivem SO no pyproject; o politica.yaml guarda so a impressao. Mudar uma
    dependencia sem re-registrar a impressao quebra aqui — que e o ponto: trocar de
    numpy passa a ser uma decisao visivel, e nao um efeito colateral de um `pip
    install -U`.

    NAO 'conserte' a impressao esperada para o teste passar. Se ele falhou, ou o
    ambiente de referencia mudou de proposito (entao registre em REGISTRO-vN.md e
    reconfira os resultados pre-registrados), ou alguem mexeu no pyproject sem saber
    o que estava mexendo."""
    reg = P["fontes"]["ambiente_de_execucao"]
    assert reg["impressao"] == ambiente.impressao(), (
        f"a impressao registrada em politica.yaml ({reg['impressao']}) nao bate com a "
        f"calculada do pyproject ({ambiente.impressao()}). Alguma dependencia mudou.")
    assert reg["expira"] is None, "ambiente nao vence no aniversario; vence quando muda"
    assert "revisar_se" in reg


def test_P15_a_divergencia_numerica_avisa_e_nao_quebra():
    """A assimetria deliberada, e ela e a decisao de desenho deste bloco.

    Um teste que ficasse vermelho porque a maquina do usuario tem outro numpy puniria
    trabalho legitimo com um alarme que nao e sobre o codigo. Um backtest que nao
    dissesse em que ambiente rodou seria meio pre-registro. Entao: a suite nao quebra,
    e quem carrega o aviso e o RESULTADO.

    E o mesmo mecanismo do `expira` — `motor.val()` avisa em stderr e devolve o valor.

    ACHADO Z-01, 11/09/2026. Este teste DIZIA isso e fazia o contrario: ele afirmava
    `reproduz_o_registrado is True`, ou seja, ficava vermelho exatamente na maquina com
    outro numpy — a coisa que a docstring acima proibe em duas linhas.

    Passou despercebido por um motivo simples: a unica maquina que rodava a suite tinha
    as versoes pinadas, entao a afirmacao errada e a certa davam o mesmo resultado. E o
    padrao F-05/N-01 na sua forma mais pura — arquivo e codigo concordando por acidente.
    Quem o encontrou foi o proprio mecanismo, no dia em que a suite rodou numa maquina
    com numpy 2.5.3 e pandas 3.0.5.

    O que este teste mede AGORA: que o selo e HONESTO, nao que ele e verde. Ou seja,
    que `reproduz_o_registrado` e derivado das divergencias em vez de afirmado, e que o
    bloco carrega o que precisa para alguem julgar o resultado depois."""
    selo = ambiente.selo()
    # A afirmacao certa: o selo nao pode MENTIR. Ele diz que reproduz se, e somente se,
    # nao ha divergencia numerica nem pacote ausente.
    assert selo["reproduz_o_registrado"] == (
        not (selo["divergencia_numerica"] or selo["ausentes"])), \
        "o selo contradiz as proprias divergencias que ele lista"
    assert selo["impressao"] == ambiente.impressao()
    assert "python" in selo
    assert "divergencia_de_ferramenta" in selo, \
        "a divergencia de ferramenta e reportada e NAO entra em reproduz_o_registrado"
    # E a suite NAO quebra por ambiente diferente — que e a frase da docstring virando
    # medicao. Se um dia alguem trocar isto por `is True`, este comentario e a razao
    # pela qual nao deve.


def test_P15_a_divergencia_numerica_e_separada_da_de_ferramenta():
    """Classificar por CONSEQUENCIA, nao por importancia. Trocar de pytest muda como o
    trabalho e feito; trocar de numpy pode mudar um numero ja registrado. Juntar as
    duas numa lista de 'coisas diferentes' apagaria a unica distincao que importa."""
    D = ambiente.declarado()
    assert set(D["numericas"]) == {"numpy", "pandas"}
    assert "pytest" in D["ferramentas"], "pytest nao produz numero nenhum"
    assert "PyYAML" in D["ferramentas"], \
        "o parser so transporta valores: ou entrega os mesmos floats, ou erro"
    assert not (set(D["numericas"]) & set(D["ferramentas"])), \
        "um pacote nao pode estar nas duas listas — a classificacao decide um aviso"


@pytest.mark.acervo   # le o CSV do NEFIN (armazem desde 25/09)
def test_P15_o_resultado_do_backtest_carrega_o_selo_do_ambiente():
    """Ate 05/09/2026 `alfa_contra_fatores()` publicava `fonte_hash` e mais nada. O
    sha256 diz de que DADO o numero saiu; nao dizia em que AMBIENTE foi calculado — e
    o alfa sai de `numpy.linalg.lstsq`, que e uma implementacao e nao um teorema."""
    import fatores
    m = fatores.mensal()
    r = fatores.alfa_contra_fatores(m["SMB"] + m["Risk_Free"], m)
    assert r["fonte_hash"] == fatores.hash_fonte()
    assert r["ambiente"]["impressao"] == ambiente.impressao()
    # Z-01: o que importa e que o resultado CARREGUE o selo, nao que o selo seja verde.
    # Um alfa calculado em ambiente divergente continua sendo um numero legitimo — ele
    # so nao e a CONFERENCIA de um numero antigo, e e o selo que diz isso a quem ler.
    assert "reproduz_o_registrado" in r["ambiente"]
    assert r["ambiente"]["reproduz_o_registrado"] == ambiente.selo()["reproduz_o_registrado"], \
        "o selo publicado com o resultado tem de ser o mesmo que o ambiente reporta"


def test_P15_o_que_a_impressao_do_ambiente_NAO_promete():
    """P5. Sistema operacional, BLAS ligada ao numpy e arquitetura de CPU continuam
    fora do registro e podem mover a ultima casa de uma regressao. A limitacao esta
    escrita para que ninguem leia na impressao mais do que ela diz."""
    reg = P["fontes"]["ambiente_de_execucao"]
    txt = reg["o_que_ela_NAO_protege"]
    assert "BLAS" in txt and "bit a bit" in txt


# ══ P-36 · o catalogo saiu do Python ═════════════════════════════════════════
@pytest.mark.repositorio   # 146b: le ou roda o fonte, que a mutacao instrumenta
def test_P36_nenhuma_rota_e_construida_por_literal_no_python():
    """O teste que define a pendencia. A P2 dizia "regras como dados" e valia so para
    as regras: 25 rotas com todos os parametros viviam como literais dentro de
    `alocacao.catalogo()`, 183 linhas, fora de todo o aparato de procedencia.

    A varredura e no AST e nao no texto: um `RotaAloc(...)` escrito em qualquer lugar
    de alocacao.py, com qualquer formatacao, cai aqui. A UNICA construcao permitida e
    a de `catalogo()`, que monta a partir do YAML."""
    fonte = open(os.path.join(AQUI, "alocacao.py"), encoding="utf-8").read()
    arvore = ast.parse(fonte)
    dentro_do_carregador = set()
    for n in ast.walk(arvore):
        if isinstance(n, ast.FunctionDef) and n.name == "catalogo":
            dentro_do_carregador = {id(x) for x in ast.walk(n)}
    construcoes = [n for n in ast.walk(arvore)
                   if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                   and n.func.id == "RotaAloc" and id(n) not in dentro_do_carregador]
    assert not construcoes, (
        f"{len(construcoes)} rota(s) construida(s) fora de catalogo(), na(s) linha(s) "
        + ", ".join(str(n.lineno) for n in construcoes))


def test_P36_toda_rota_do_yaml_declara_procedencia():
    """P1 estendida ao catalogo. Uma rota nao e um numero medido — e uma DECISAO DE
    MODELAGEM ("o Tesouro Selic serve LASTRO e tambem DATADO"). A procedencia dela e
    quem decidiu, quando, e com base em que."""
    cru = carregar_catalogo()["rotas"]
    for rid, r in cru.items():
        if rid.startswith("_"): continue
        p = r.get("procedencia")
        assert p, f"{rid}: sem procedencia"
        assert p["status"] in ("COMPLETO", "PARCIAL", "NAO_CONFIRMADO", "OBSERVADO"), \
            f"{rid}: status {p['status']!r} fora da taxonomia"
        assert isinstance(p.get("decidido_em"), dt.date), f"{rid}: sem data de decisao"
        assert len(p.get("base", "")) > 80, \
            f"{rid}: `base` tem de dizer em que a decisao se apoia, nao um rotulo"


def test_P36_valor_que_vem_do_custos_e_referencia_e_nao_copia():
    """A regra que evita repetir o N-01 em escala de catalogo. `adm_aa: 0.0059` seria
    um segundo lugar guardando o mesmo numero — e mataria `expira`, `status` e
    `bloqueia` da constante original. A referencia herda tudo isso.

    Verificado pelo comportamento e nao pela leitura: mexer na constante TEM de mexer
    na rota. Se fosse copia, nada mudaria."""
    C2 = copy.deepcopy(C)
    C2["etf"]["PIBB11"]["valor"] = 0.5
    r = next(x for x in catalogo(C2) if x.id == "pibb11")
    assert r.adm_aa == 0.5
    assert next(x for x in catalogo(C) if x.id == "pibb11").adm_aa != 0.5

    C3 = copy.deepcopy(C)
    C3["corretagem"]["safra_terra"]["valor"] = 99.0
    assert next(x for x in catalogo(C3) if x.id == "acao_450").corr_fix == 99.0


def test_P36_a_soma_de_spread_e_iof_continua_sendo_soma():
    """As rotas de exterior guardam `{soma: [spread, IOF]}` e nao o total. Sao coisas
    de naturezas diferentes — o spread e comercial e muda quando a casa quiser; o IOF
    e legal e muda por decreto. Somar na LEITURA faz uma mudanca de IOF se propagar
    sozinha para as quatro rotas; guardar o total exigiria lembrar de recalcular."""
    C2 = copy.deepcopy(C)
    C2["exterior"]["iof_investimento"]["valor"] = 0.10
    afetadas = {r.id: r.entrada_extra for r in catalogo(C2)
                if r.id in ("ext_avenue", "ext_nomad5", "ext_nomad1", "ext_conta")}
    base = {r.id: r.entrada_extra for r in catalogo(C)
            if r.id in ("ext_avenue", "ext_nomad5", "ext_nomad1", "ext_conta")}
    for rid in afetadas:
        _delta = 0.10 - val(C["exterior"]["iof_investimento"])
        assert abs((afetadas[rid] - base[rid]) - _delta) < 1e-12, \
            f"{rid}: o IOF nao se propagou — sinal de que o total foi copiado"


def test_P36_quem_cobra_custodia_interna_vem_da_constante_e_nao_de_lista_no_codigo():
    """Achado F-01, agora guardado pelo YAML. O rol de quem cobra custodia interna
    esta em `custos.yaml -> etf.custodia_interna_ishares.aplica_a`. Tirar um ticker de
    la TEM de zerar a custodia interna daquela rota."""
    alvo = next(r for r in catalogo(C) if r.id == "bova11")
    assert alvo.custodia_interna_aa > 0
    C2 = copy.deepcopy(C)
    C2["etf"]["custodia_interna_ishares"]["aplica_a"] = [
        t for t in C2["etf"]["custodia_interna_ishares"]["aplica_a"] if t != "BOVA11"]
    assert next(r for r in catalogo(C2) if r.id == "bova11").custodia_interna_aa == 0.0


def test_Q01_insumo_bloqueado_bloqueia_a_ROTA_e_nunca_o_catalogo():
    """ACHADO Q-01, encontrado na migracao. O tratamento era INCONSISTENTE e as duas
    metades nunca se encontravam no mesmo teste:

      - rotas de ETF degradavam com elegancia: `val()` levantava, a rota entrava sem a
        taxa e COM o motivo escrito (foi assim que o BOVV11 ficou visivel);
      - todas as outras explodiam: `val()` levantava dentro de `catalogo()` e o
        CATALOGO INTEIRO morria.

    Uma constante NAO_CONFIRMADO em `corretagem.safra_terra` apagaria as 25 rotas,
    inclusive as 24 que nao dependem dela — o oposto exato da doutrina P6: sumir com o
    ativo por falta de dado. Este teste falha na versao anterior levantando
    InsumoBloqueado em vez de devolver catalogo."""
    C2 = copy.deepcopy(C)
    C2["corretagem"]["safra_terra"] = dict(
        valor=None, status="NAO_CONFIRMADO", motivo="teste do Q-01")
    rotas = catalogo(C2)                      # NAO levanta
    assert len(rotas) == len(catalogo(C)), "nenhuma rota pode sumir do catalogo"
    ferida = next(r for r in rotas if r.id == "acao_450")
    assert not ferida.confiavel and "teste do Q-01" in ferida.bloqueios[0]
    assert ferida.corr_fix == 0.0, "o campo fica no default e a rota carrega o motivo"
    intactas = [r for r in rotas if r.id != "acao_450"]
    assert all(r.confiavel == next(x for x in catalogo(C) if x.id == r.id).confiavel
               for r in intactas), "as outras 24 rotas nao podem ser afetadas"


def test_Q01_a_mensagem_do_bloqueio_aponta_para_a_CONSTANTE():
    """Quem le a mensagem precisa saber que numero ir buscar, nao onde ele seria
    usado. `etf.BOVV11: site do gestor bloqueia...` e acionavel; `bovv11.adm_aa: ...`
    manda o leitor para o lugar errado."""
    b = next(r for r in catalogo(C) if r.id == "bovv11")
    assert not b.confiavel and b.bloqueios[0].startswith("etf.BOVV11:")


def test_P36_estrategia_de_bloqueio_desconhecida_e_erro_duro():
    """O YAML diz QUAL estrategia se aplica; o Python implementa COMO. Um nome que
    nao existe tem de parar o carregamento — nao ser ignorado, que faria a rota nascer
    desbloqueada e parecendo saudavel."""
    cru = carregar_catalogo()
    cru["rotas"]["fii"]["bloqueio"]["regra"] = "inventada"
    import tempfile, yaml as _y
    with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False,
                                     encoding="utf-8") as f:
        _y.safe_dump(cru, f, allow_unicode=True); caminho = f.name
    try:
        with pytest.raises(ValueError, match="estrategia de bloqueio desconhecida"):
            catalogo(C, caminho)
    finally:
        os.remove(caminho)


def test_P36_referencia_para_caminho_inexistente_e_erro_duro():
    """`{de: etf.NAO_EXISTE}` e erro de digitacao. Devolver None faria a rota nascer
    com o campo no default — silenciosamente errada, que e a familia do F-02."""
    with pytest.raises(KeyError, match="que nao existe"):
        _resolve(C, {"de": "etf.NAO_EXISTE"}, contexto="teste")


def test_P36_a_duracao_do_td_ipca_continua_sendo_uma_AUSENCIA_deliberada():
    """O campo mais importante do catalogo.yaml, e ele e um `null`. A duracao nao e
    constante de catalogo: vem do papel que o usuario se compromete a carregar
    (registro CARREGO, G8). Supor uma duracao aqui seria supor um compromisso que
    ninguem assumiu — foi assim que a versao 1.0.0 alocou 17% num NTN-B de duracao 18
    sem prazo nenhum a casar. Migrar para YAML e exatamente onde um `null` vira `0.0`
    por descuido."""
    cru = carregar_catalogo()["rotas"]["td_ipca"]
    assert cru["duracao_anos"] is None
    assert "AUSENCIA DELIBERADA" in cru["procedencia"]["base"]
    assert next(r for r in catalogo(C) if r.id == "td_ipca").duracao_anos is None


# ══ P-37 · as fases sao testaveis SOZINHAS ═══════════════════════════════════
# O argumento inteiro da pendencia esta nestes testes. Nenhum deles era possivel
# quando `alocar()` tinha 300 linhas: para perguntar "a fase de universo devolveu o
# que devia?" era preciso rodar a alocacao completa e inferir a resposta pelos pesos.
# Um erro de etapa intermediaria so aparecia se por acaso movesse um numero — foi
# assim que o I-01 (a ordem dos portoes nunca foi G0→G8) sobreviveu semanas.

def _saida_vazia():
    return dict(estado=None, portoes=[], pendencias=[], universo=None, alvo=None)


def test_P37_a_fase_de_aporte_encerra_e_diz_que_encerrou():
    """Antes, "o pipeline parou aqui" era um `return` no meio de 300 linhas. Agora e
    um valor de retorno que da para afirmar."""
    e = Estado(**{**BASE, "reserva_atual": 0})
    saida = _saida_vazia()
    _, _, encerrou = fase_aporte(e, catalogo(C), C, P, saida)
    assert encerrou is True
    assert saida["diretiva"].portao == "G2_reserva"

    e2 = Estado(**BASE)                      # reserva completa: nao encerra
    saida2 = _saida_vazia()
    est2, _, encerrou2 = fase_aporte(e2, catalogo(C), C, P, saida2)
    assert encerrou2 is False and "diretiva" not in saida2
    assert est2.aporte_mensal == e2.aporte_mensal, "sem G0 e sem G2, o aporte segue inteiro"


def test_P37_a_divida_cara_encerra_antes_da_reserva():
    """A precedencia G1 > G2 vira uma afirmacao direta, sem passar pela alocacao."""
    e = Estado(**{**BASE, "reserva_atual": 0,
                  "dividas": [Divida("cartao", 8000, 0.14)]})
    saida = _saida_vazia()
    _, _, encerrou = fase_aporte(e, catalogo(C), C, P, saida)
    assert encerrou and saida["diretiva"].portao == "G1_divida"
    assert [d.portao for d in saida["portoes"]] == ["G1_divida"], \
        "o G2 nem chega a rodar — quem encerra encerra"


def test_P37_a_fase_de_universo_nao_encerra_nunca():
    """A distincao entre as duas fases, agora verificavel: `aporte` pode devolver
    "encerrou"; `universo` devolve rotas, sempre. Uma fase que so filtra nao tem como
    dizer "pare" — e se um dia tiver, este teste quebra."""
    e = Estado(**BASE)
    vivos, rejeitados, dominados, pref = fase_universo(
        e, catalogo(C), C, P, 25, {}, {})
    assert isinstance(vivos, list) and vivos, "universo sempre devolve rotas vivas"
    assert set(rejeitados) <= {"fora_status", "fora_atrito", "sem_tese", "sem_carrego"}
    assert all(isinstance(v, tuple) for v in vivos), \
        "depois do G3 o que trafega sao PARES, e e disso que nasce o achado R-01"


def test_R01_a_ordem_dos_portoes_era_um_DADO_que_so_aceitava_18_de_120_valores():
    """ACHADO R-01, e ele so foi possivel de encontrar porque a P-37 permitiu chamar
    `fase_universo` sozinha, com uma politica alterada, sem rodar a alocacao inteira.

    A P-07 declarou a ordem dos portoes como dado e afirmou que troca-la e um commit
    no YAML. Isso e falso para 102 das 120 ordens: os portoes mudam a FORMA do que
    trafega — o G3 transforma rota em `(rota, custo)`, e o G4, o G7 e o G8 consomem
    pares. Qualquer um deles antes do G3 estourava com `TypeError: cannot unpack
    non-iterable RotaAloc object` no fundo de uma funcao de portao.

    Declarar a ordem como dado sem declarar o CONTRATO e declarar uma liberdade que
    nao existe — mesma familia do F-05 e do N-01."""
    import itertools
    nomes = ["G5_status", "G3_atrito", "G7_tese_registrada",
             "G8_compromisso_de_carrego", "G4_dominancia"]
    posicoes = sorted(P["portoes"][n]["ordem"] for n in nomes)
    e = Estado(**BASE)
    conta = {"roda": 0, "recusada_pela_ordem": 0, "insumo_bloqueado": 0}
    for perm in itertools.permutations(nomes):
        P2 = copy.deepcopy(P)
        for n, o in zip(perm, posicoes): P2["portoes"][n]["ordem"] = o
        try:
            fase_universo(e, catalogo(C), C, P2, 25, {}, {}); conta["roda"] += 1
        except InsumoBloqueado:
            conta["insumo_bloqueado"] += 1
        except ValueError as ex:
            assert "ordem invalida" in str(ex), str(ex)
            conta["recusada_pela_ordem"] += 1
    assert conta["roda"] == 18, conta
    assert conta["recusada_pela_ordem"] == 90, conta
    # os 12 restantes NAO sao defeito: sao as ordens que poem o G5 depois de um portao
    # que calcula custo, e ai uma rota bloqueada chega a uma conta. E o guarda do F-02
    # funcionando, e a mensagem dele ja nomeia a rota e a constante.
    assert conta["insumo_bloqueado"] == 12, conta
    assert sum(conta.values()) == 120


def test_R01_a_regra_e_G3_antes_de_G4_G7_e_G8():
    """A dependencia medida, e ela e uma so: o G3 e o unico portao que PRODUZ pares.
    O G5 e polimorfico de proposito (aceita rota nua ou par) — e foi isso que
    permitiu corrigir o F-02 movendo-o para a frente sem quebrar nada."""
    assert P["portoes"]["G3_atrito"]["produz"] == "pares"
    assert P["portoes"]["G5_status"]["produz"] == "mesma_forma"
    for g in ("G4_dominancia", "G7_tese_registrada", "G8_compromisso_de_carrego"):
        assert P["portoes"][g]["consome"] == "pares"

    P2 = copy.deepcopy(P)                       # G4 antes do G3
    P2["portoes"]["G4_dominancia"]["ordem"] = P["portoes"]["G3_atrito"]["ordem"]
    P2["portoes"]["G3_atrito"]["ordem"] = P["portoes"]["G4_dominancia"]["ordem"]
    with pytest.raises(ValueError, match="consome pares"):
        fase_universo(Estado(**BASE), catalogo(C), C, P2, 25, {}, {})


def test_R01_portao_sem_contrato_declarado_e_recusado():
    """Sem `consome`/`produz` nao da para saber se a ordem e executavel. Faltar o
    contrato tem de ser erro duro — a alternativa e supor, e supor foi o que criou o
    problema."""
    P2 = copy.deepcopy(P)
    del P2["portoes"]["G4_dominancia"]["consome"]
    with pytest.raises(ValueError, match="nao declara"):
        fase_universo(Estado(**BASE), catalogo(C), C, P2, 25, {}, {})


def test_P37_G6_roda_uma_vez_so_e_isso_e_deliberado():
    """G6 e ordem 1 no YAML e mora na fase `aporte` do codigo, porque e PRE-CONDICAO
    DO CATALOGO. O laco da fase `universo` o pula explicitamente. Essa duplicidade e
    o tipo de coisa que se perde numa refatoracao — o teste a prende."""
    fonte = open(os.path.join(AQUI, "alocacao.py"), encoding="utf-8").read()
    arvore = ast.parse(fonte)
    def corpo(nome):
        n = next(x for x in ast.walk(arvore)
                 if isinstance(x, ast.FunctionDef) and x.name == nome)
        return ast.unparse(n)
    from alocacao import PORTOES_DO_UNIVERSO, _exec_g6
    assert "g6_coerencia_funcao(" in corpo("fase_aporte")
    assert "g6_coerencia_funcao(" not in corpo("fase_universo")
    # e na tabela ele aparece como um NAO-FAZ-NADA nomeado, com o motivo escrito —
    # nao como um `continue` no meio de um laco, que nao distingue "ja rodou" de
    # "esqueceram de implementar".
    assert PORTOES_DO_UNIVERSO["G6_coerencia_funcao"] is _exec_g6
    assert "pre-condicao do catalogo" in _exec_g6.__doc__
    antes = catalogo(C)
    assert _exec_g6(antes, {}) is antes, "o adaptador do G6 nao toca no que recebe"


def test_P37_espalhar_nao_captura_mais_pesos_e_alertas_de_um_escopo_invisivel():
    """Era uma funcao aninhada que mutava dois dicts do escopo de cima. Legivel
    enquanto cabe numa tela; indefensavel em 300 linhas — e impossivel de testar
    isolada. Agora e uma funcao de modulo com os dois como parametros."""
    from alocacao import espalhar
    pesos, alertas = {}, []
    bloco = [(r, 0.0, 0.0) for r in catalogo(C) if r.id in ("bova11", "pibb11")]
    sobra = espalhar(bloco, 0.60, "CRESCIMENTO", P, pesos, alertas)
    assert sobra == 0.0
    assert abs(sum(pesos.values()) - 0.60) < 1e-12
    assert len(pesos) == 2 and abs(pesos["bova11"] - 0.30) < 1e-12

    vazio_pesos, vazio_alertas = {}, []
    assert espalhar([], 0.25, "DATADO", P, vazio_pesos, vazio_alertas) == 0.25, \
        "bloco vazio devolve tudo como sobra, nao engole peso"
    assert not vazio_pesos


def test_P37_distribuir_por_funcao_e_uma_funcao_pura_do_universo():
    """Ela nao le disco, nao consulta data, nao muta o estado. Dado o mesmo universo,
    devolve o mesmo resultado — o que torna possivel testar a alocacao sem montar um
    pipeline inteiro."""
    e = Estado(**BASE)
    vivos, _, _, _ = fase_universo(e, catalogo(C), C, P, 25, {}, {})
    a = distribuir_por_funcao(vivos, catalogo(C), e, C, P, 25, {})
    b = distribuir_por_funcao(vivos, catalogo(C), e, C, P, 25, {})
    assert a[0] == b[0] and a[1] == b[1], "duas chamadas iguais dao resultado igual"
    pesos = a[0]
    assert abs(sum(pesos.values()) - 1.0) < 1e-9


def test_P37_nenhuma_funcao_do_motor_passa_de_120_linhas():
    """A regra que a P-37 instala. 120 e o limite declarado, nao um numero magico: e
    o ponto em que uma funcao deixa de caber numa tela e passa a so ser testavel pelo
    resultado final. `alocar()` tinha 300.

    Este teste vale mais como CONTENCAO do que como conquista: ele impede que a
    proxima funcao grande apareca sem alguem decidir que ela deve aparecer."""
    LIMITE = 120
    grandes = []
    for f in sorted(os.listdir(AQUI)):
        if not f.endswith(".py") or f.startswith(("test_", "demo_")): continue
        for n in ast.walk(ast.parse(open(os.path.join(AQUI, f), encoding="utf-8").read())):
            if isinstance(n, ast.FunctionDef):
                L = n.end_lineno - n.lineno + 1
                if L > LIMITE: grandes.append(f"{f}:{n.name} ({L} linhas)")
    assert not grandes, ("funcao acima de " + str(LIMITE) + " linhas: "
                         + ", ".join(grandes) + ". Quebre em partes nomeadas ou "
                         "suba o limite DE PROPOSITO, com o motivo escrito.")


# ══ S-01 e S-02 · o cache que existia para acelerar era o defeito ════════════
def test_S01_o_hash_dos_custos_nao_e_recalculado_a_cada_consulta():
    """Medido com cProfile em 06/09/2026: `hash_custos()` era chamada 73 vezes por
    `alocar()` — uma por consulta ao cache de arrasto, que a usava na chave — e cada
    chamada RELIA E RE-HASHEAVA os 33 KB do custos.yaml. 37% do tempo de `alocar()`
    era gasto hasheando um arquivo para decidir se podia usar um valor ja calculado.

    O cache que existe para acelerar era o maior custo do motor."""
    from alocacao import hash_custos, hash_custos_sem_cache, _CACHE_HASH_CUSTOS
    assert hash_custos() == hash_custos_sem_cache(), \
        "o cache tem de devolver exatamente o que a leitura devolveria"
    _CACHE_HASH_CUSTOS.clear()
    hash_custos()
    n = len(_CACHE_HASH_CUSTOS)
    for _ in range(200): hash_custos()
    assert len(_CACHE_HASH_CUSTOS) == n, "200 consultas nao podem criar entrada nova"


def test_S01_arquivo_alterado_invalida_a_impressao():
    """A invalidacao e o ponto: memoizar sem invalidar seria trocar um defeito por
    outro pior. A chave e (caminho, mtime_ns, tamanho) — mexeu no arquivo, recalcula."""
    from alocacao import hash_custos
    import tempfile, shutil
    with tempfile.TemporaryDirectory() as d:
        alvo = os.path.join(d, "custos.yaml")
        shutil.copy(os.path.join(AQUI, "custos.yaml"), alvo)
        h1 = hash_custos(alvo)
        with open(alvo, "a", encoding="utf-8") as f:
            f.write("\n# uma linha a mais\n")
        assert hash_custos(alvo) != h1, "arquivo mudou e a impressao nao mudou"


def test_S02_o_arrasto_honra_o_C_que_recebeu():
    """ACHADO S-02, e ele e da familia do F-02 e do N-01: um mecanismo que parecia
    funcionar e nao funcionava.

    Havia um cache GLOBAL cuja chave incluia `hash_custos()` — o hash do ARQUIVO. Mas
    o custo que a funcao usa vem do `C` que chega como PARAMETRO. Passar um `C`
    modificado em memoria (o que todo teste faz, via deepcopy) devolvia o valor
    calculado com o `C` ORIGINAL, em silencio.

    Consequencia: qualquer teste que alterasse um custo e conferisse arrasto ou
    dominancia estava testando NADA. Este teste falha na versao anterior."""
    r = next(x for x in catalogo(C) if x.id == "bova11")
    C2 = copy.deepcopy(C); C2["macro"]["cdi_aa"]["valor"] = 0.50
    a1 = arrasto_anualizado(r, C, 500, 10)
    a2 = arrasto_anualizado(r, C2, 500, 10)
    assert a1 != a2, "mudar o CDI tem de mudar o arrasto"
    assert a2 > a1


def test_S02_o_memo_e_por_CONTEUDO_e_nao_global():
    """A correcao nao foi tirar o cache — foi dar a ele uma chave que inclui a
    entrada. Dois `C` de conteudo igual compartilham; conteudos diferentes nao."""
    from alocacao import memo_de_arrasto, impressao_de_custos
    C2 = copy.deepcopy(C); C2["macro"]["cdi_aa"]["valor"] = 0.50
    assert memo_de_arrasto(C) is memo_de_arrasto(copy.deepcopy(C))
    assert memo_de_arrasto(C) is not memo_de_arrasto(C2)
    assert impressao_de_custos(C) != impressao_de_custos(C2)


def test_S02_procedencia_e_do_ARQUIVO_e_cache_e_do_CONTEUDO():
    """A distincao que o defeito ensinou, e que vale mais que o conserto:
      `hash_custos()`         — do arquivo em disco. Serve a PROCEDENCIA.
      `impressao_de_custos()` — do conteudo em memoria. Serve a CORRECAO DE CACHE.
    Sao iguais enquanto ninguem altera o `C` em memoria. Todo teste altera."""
    from alocacao import hash_custos, impressao_de_custos
    C2 = copy.deepcopy(C); C2["macro"]["cdi_aa"]["valor"] = 0.50
    assert hash_custos() == hash_custos(), "o do arquivo nao muda com o C em memoria"
    assert impressao_de_custos(C) != impressao_de_custos(C2)
    # e a procedencia de uma saida continua citando o ARQUIVO, que e o que ela promete
    r = alocar(Estado(**BASE), C, P, teses={}, carregos={})
    assert r["procedencia"]["custos_hash"] == hash_custos()


def test_S02_o_memo_por_conteudo_nao_cresce_sem_limite():
    """Uma suite que varia custos em centenas de testes nao pode virar vazamento."""
    from alocacao import memo_de_arrasto, _CACHE_POR_CONTEUDO, _LIMITE_DE_CONTEUDOS
    for i in range(_LIMITE_DE_CONTEUDOS * 3):
        Ci = copy.deepcopy(C); Ci["macro"]["cdi_aa"]["valor"] = 0.10 + i/10000
        memo_de_arrasto(Ci)
    assert len(_CACHE_POR_CONTEUDO) <= _LIMITE_DE_CONTEUDOS


# ══ P-38 · a disciplina virou garantia ═══════════════════════════════════════
@pytest.mark.repositorio   # 146b: le ou roda o fonte, que a mutacao instrumenta
def test_P38_a_guarda_acusa_o_teste_que_suja_o_estado_compartilhado(tmp_path):
    """O teste que prova a guarda. Ele roda um pytest SEPARADO sobre um arquivo que
    muta `P` de proposito, e exige que o resultado seja vermelho COM O NOME do objeto.

    Sem isto, a guarda seria uma afirmacao sobre si mesma — e a suite passar com ela
    ligada so provaria que ninguem esta sujando hoje, nao que sujar seria pego."""
    import subprocess, shutil
    for f in ("conftest.py", "alocacao.py", "motor.py", "tese.py", "custos.yaml",
              "politica.yaml", "perfil.yaml", "catalogo.yaml", "teses.yaml"):
        shutil.copy(os.path.join(AQUI, f), tmp_path / f)
    (tmp_path / "test_sujo.py").write_text(
        "import sys, os\n"
        "sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\n"
        "from alocacao import carregar_politica\n"
        "P = carregar_politica()\n"
        "def test_que_suja():\n"
        "    P['tetos']['aposta_pct'] = 0.99\n"
        "    assert True\n", encoding="utf-8")
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
                        str(tmp_path / "test_sujo.py")],
                       capture_output=True, text=True, cwd=str(tmp_path))
    assert r.returncode != 0, "o teste que sujou o compartilhado tinha de dar vermelho"
    assert "alterou objeto(s) compartilhado(s)" in r.stdout
    assert "P-38" in r.stdout, "a mensagem tem de dizer onde ler sobre isso"
    # A guarda mora no TEARDOWN, entao o pytest rotula ERROR e nao FAILED — e o teste
    # culpado conta nas duas colunas. Esta declarado no conftest e o teste afirma o
    # comportamento REAL, nao o que seria mais bonito.
    assert "error" in r.stdout


@pytest.mark.repositorio   # 146b: le ou roda o fonte, que a mutacao instrumenta
def test_P38_a_guarda_restaura_para_que_so_o_culpado_falhe(tmp_path):
    """Detectar sozinho nao basta: se o teste A muta e ninguem restaura, todos os
    seguintes falham por causa do A e o rastro se perde. A guarda restaura DEPOIS de
    acusar — o segundo teste do arquivo abaixo tem de passar."""
    import subprocess, shutil
    for f in ("conftest.py", "alocacao.py", "motor.py", "tese.py", "custos.yaml",
              "politica.yaml", "perfil.yaml", "catalogo.yaml", "teses.yaml"):
        shutil.copy(os.path.join(AQUI, f), tmp_path / f)
    (tmp_path / "test_dois.py").write_text(
        "import sys, os\n"
        "sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\n"
        "from alocacao import carregar_politica\n"
        "P = carregar_politica()\n"
        "ORIGINAL = P['tetos']['aposta_pct']\n"
        "def test_a_que_suja():\n"
        "    P['tetos']['aposta_pct'] = 0.99\n"
        "def test_b_que_herdaria_a_sujeira():\n"
        "    assert P['tetos']['aposta_pct'] == ORIGINAL\n", encoding="utf-8")
    # B-18: sem `-p no:cacheprovider`, o Windows as vezes nega o rename da pasta de
    # cache (WinError 5), sai um PytestCacheWarning e a linha vira "2 passed, 1
    # warning, 1 error" -- a substring abaixo reprovava por um aviso alheio a guarda.
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
                        str(tmp_path / "test_dois.py")],
                       capture_output=True, text=True, cwd=str(tmp_path))
    assert "2 passed, 1 error" in r.stdout, \
        f"esperado: os dois testes passam a execucao e SO o culpado erra na limpeza. "\
        f"Se `test_b` tambem falhasse, a restauracao nao teria acontecido e a sujeira "\
        f"do primeiro teria contaminado o segundo. Saida:\n{r.stdout[-1200:]}"
    assert "test_a_que_suja" in r.stdout and "test_b_que_herdaria" not in r.stdout


def test_P38_as_fixtures_entregam_copia_e_nao_a_original(custos, politica,
                                                         custos_originais, politica_original):
    """O jeito sancionado de alterar. Existir uma saida limpa e o que torna a guarda
    justa — acusar sem oferecer alternativa seria so atrito."""
    assert custos is not custos_originais and politica is not politica_original
    custos["macro"]["cdi_aa"]["valor"] = 0.99
    politica["tetos"]["aposta_pct"] = 0.99
    assert custos_originais["macro"]["cdi_aa"]["valor"] != 0.99
    assert politica_original["tetos"]["aposta_pct"] != 0.99


@pytest.mark.repositorio   # 146b: le ou roda o fonte, que a mutacao instrumenta
def test_B12_a_guarda_vigia_as_fixtures_de_sessao(tmp_path):
    """B-12: `custos_originais` e `politica_original` eram protegidas so pela docstring
    "NAO altere". Mesmo desenho do teste da P-38: um pytest SEPARADO sobre um arquivo
    que as suja de proposito. Os testes `b` e `d` sao a prova da RESTAURACAO -- `d`
    recebe `custos`, a copia fresca, que e feita a partir da original: sem restaurar,
    a sujeira de `c` chegaria nele pela porta sancionada."""
    import subprocess, shutil
    for f in ("conftest.py", "alocacao.py", "motor.py", "tese.py", "custos.yaml",
              "politica.yaml", "perfil.yaml", "catalogo.yaml", "teses.yaml"):
        shutil.copy(os.path.join(AQUI, f), tmp_path / f)
    (tmp_path / "test_sessao.py").write_text(
        "def test_a_suja_a_politica(politica_original):\n"
        "    politica_original['tetos']['aposta_pct'] = 0.99\n"
        "def test_b_herdaria_a_politica(politica_original):\n"
        "    assert politica_original['tetos']['aposta_pct'] != 0.99\n"
        "def test_c_suja_os_custos(custos_originais):\n"
        "    custos_originais['macro']['cdi_aa']['valor'] = 0.99\n"
        "def test_d_herdaria_pela_copia(custos):\n"
        "    assert custos['macro']['cdi_aa']['valor'] != 0.99\n", encoding="utf-8")
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
                        str(tmp_path / "test_sessao.py")],
                       capture_output=True, text=True, cwd=str(tmp_path))
    assert "4 passed, 2 errors" in r.stdout, (
        f"esperado: os quatro passam a execucao e SO os dois culpados erram na limpeza. "
        f"Saida:\n{r.stdout[-1500:]}")
    assert "fixture de sessao `politica_original`" in r.stdout
    assert "fixture de sessao `custos_originais`" in r.stdout
    assert "test_b_herdaria" not in r.stdout and "test_d_herdaria" not in r.stdout
