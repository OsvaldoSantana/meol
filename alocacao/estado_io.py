# -*- coding: utf-8 -*-
"""
Leitura e validacao do estado.yaml — o insumo que o usuario preenche.

Por que existe um validador aqui, e nao um `yaml.safe_load` direto:
  o arquivo e preenchido a mao, e as tres falhas mais provaveis sao SILENCIOSAS.
  Numero com virgula decimal vira STRING em YAML e o motor faria aritmetica com
  texto; um campo deixado no default do modelo passa por valor declarado; e uma
  data no formato brasileiro vira string tambem. Nenhuma das tres levanta erro
  sozinha — todas produzem um resultado plausivel e errado, que e a pior classe
  de defeito deste projeto inteiro.

Mesmo desenho do validador de tese: devolve TODOS os problemas de uma vez, separa
o que bloqueia do que e aviso, e nao inventa valor nenhum.
"""
from __future__ import annotations
import dataclasses, math, os, re, sys, typing, datetime as dt
import yaml

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
# P-71: sem ciclo de import. `alocacao.py` NAO importa `estado_io` (conferido antes
# desta linha existir) -- so o inverso seria um problema, e o inverso nao acontece.
from alocacao import Divida, MatchEmpregador, Objetivo

NUMERICOS = ("despesa_mensal", "reserva_atual", "aporte_mensal", "caixa", "horizonte_anos")

class EstadoInvalido(Exception):
    pass

def _finito(n, campo, problemas):
    """CX-04: o UNICO lugar onde um numero vira dinheiro. `float()` aceita "nan", "inf" e
    "Infinity", e o YAML le `.nan` e `.inf` como float: sem esta conferencia, NaN atravessava a
    porta e estourava no motor (ValueError), e infinito virava saldo."""
    if not math.isfinite(n):
        problemas.append(f"{campo}: {n!r} nao e um numero finito. Escreva o valor em reais, "
                         f"com ponto decimal")
        return None
    return n

def _num(v, campo, problemas):
    """Converte para float recusando as armadilhas de preenchimento manual.

    CX-04 (auditoria do Codex, 03/10/2026): `bool` e subclasse de `int`, e o teste de tipo
    `isinstance(v, (int, float))` deixava `true` virar R$ 1,00. O YAML 1.1, que o PyYAML
    implementa, le `yes`, `no`, `on` e `off` sem aspas como booleano -- `caixa: no` chegava ao
    motor como zero. O booleano e recusado ANTES do teste de numero, e todo numero passa por
    `_finito()`. Todo campo numerico do estado passa por aqui, `posicoes` e `dependentes`
    inclusive (antes, os dois entravam crus)."""
    if v is None:
        problemas.append(f"{campo}: nao preenchido"); return None
    if isinstance(v, bool):
        problemas.append(
            f"{campo}: {str(v).lower()} nao e numero. O YAML le true/false, e tambem "
            f"yes/no/on/off sem aspas, como booleano; escreva o valor em reais")
        return None
    if isinstance(v, (int, float)): return _finito(float(v), campo, problemas)
    if isinstance(v, str):
        s = v.strip()
        if re.fullmatch(r"-?\d{1,3}(\.\d{3})*,\d+", s) or re.fullmatch(r"-?\d+,\d+", s):
            convertido = float(s.replace(".", "").replace(",", "."))
            problemas.append(
                f"{campo}: '{v}' foi lido como TEXTO, nao numero — YAML usa PONTO como "
                f"separador decimal. Escreva {convertido:.2f}. Interpretei como "
                f"{convertido:.2f} para seguir, mas corrija o arquivo")
            return convertido
        try: return _finito(float(s), campo, problemas)
        except ValueError:
            problemas.append(f"{campo}: '{v}' nao e numero"); return None
    problemas.append(f"{campo}: tipo inesperado {type(v).__name__}"); return None

def _registro(x, classe, rot, problemas):
    """Um mapa do YAML -> um dataclass, com as mesmas guardas dos campos do topo.

    P-71, segunda metade: a primeira conversao era `classe(**x)` cru, e aceitava
    exatamente o que este modulo existe para recusar -- virgula decimal virava texto,
    campo em branco virava TypeError, chave errada sumia. Devolve None quando o
    registro nao se sustenta; o motivo ja esta em `problemas`."""
    campos = dataclasses.fields(classe)
    # B-11: `f.type` e a ANOTACAO CRUA. Com `from __future__ import annotations` no
    # modulo da classe ela e a string "str"; sem ele e a classe `str`. Comparar com
    # "str" so funcionava porque o alocacao.py tem o __future__ -- um dataclass de
    # outro modulo tinha o campo de texto mandado para `_num()` em silencio.
    # `get_type_hints` resolve os dois casos para o tipo de verdade.
    tipos = typing.get_type_hints(classe)
    nomes = [f.name for f in campos]
    if not isinstance(x, dict):
        problemas.append(f"{rot}: tem de ser um mapa com {nomes}"); return None
    sobra = sorted(set(x) - set(nomes))
    if sobra:
        problemas.append(f"{rot}: {sobra} nao existe(m) em {classe.__name__} e seria(m) "
                         f"descartado(s) em silencio. Campos aceitos: {nomes}")
    vals = {}
    for f in campos:
        v = x.get(f.name)
        if tipos[f.name] is str:
            ok = isinstance(v, str) and v.strip()
            if not ok: problemas.append(f"{rot}.{f.name}: nao preenchido")
            vals[f.name] = v if ok else None
        else:
            vals[f.name] = _num(v, f"{rot}.{f.name}", problemas)
    if any(v is None for v in vals.values()): return None
    return classe(**vals)

def _registros(lista, classe, rot, problemas):
    if lista is None: return []
    if not isinstance(lista, list):
        problemas.append(f"{rot} tem de ser uma lista"); return []
    out = [_registro(x, classe, f"{rot}[{i}]", problemas) for i, x in enumerate(lista)]
    return [r for r in out if r is not None]

def _conferir_empenho(doc, d, problemas):
    """`reserva_empenhada` e uma segunda forma de dizer o que `reserva_atual -
    reserva_disponivel` ja diz (J-01). Ate 11/09 era lida e descartada -- campo morto,
    4a ocorrencia da auditoria de 10/09; antes de 11/09 ia para `d` e quebrava
    `Estado(**d)`. Agora e CONFERENCIA, no padrao de `reserva_por_rota`: duas medidas
    do mesmo saldo que discordam viram problema. O motor continua usando so
    `reserva_disponivel`."""
    if doc.get("reserva_empenhada") is None: return
    emp = _num(doc.get("reserva_empenhada"), "reserva_empenhada", problemas)
    nom, disp = d.get("reserva_atual"), d.get("reserva_disponivel")
    if emp is None or nom is None or disp is None: return
    if abs(emp - (nom - disp)) > 0.01:
        problemas.append(
            f"reserva_empenhada diz {emp:.2f} e reserva_atual - reserva_disponivel da "
            f"{nom - disp:.2f}. Sao duas medidas do mesmo empenho e elas discordam — o "
            f"sistema nao escolhe entre as duas por voce. O motor usa reserva_disponivel")

def _match(doc, problemas):
    """P-71, segunda metade: os dois campos que `estado.exemplo.yaml` pede e que ate
    11/09 nunca eram lidos. Ausente e diferente de falso: sem `match_verificado` o G0
    pergunta; com `true` ele se cala -- e essa resposta nao pode sumir no caminho.
    Funcao propria porque `validar()` passou do teto de 120 linhas da P-37."""
    mv = doc.get("match_verificado", False)
    if not isinstance(mv, bool):
        problemas.append(f"match_verificado = {mv!r}: use true ou false")
        mv = False
    me = doc.get("match_empregador")
    return mv, (None if me is None else
                _registro(me, MatchEmpregador, "match_empregador", problemas))

def _posicoes(pos, problemas):
    """rota -> valor investido. CX-04: ate 04/10 entrava cru, e `bova11: yes` virava uma
    posicao de R$ 1,00. Ausente e `{}` (nenhuma posicao), como antes."""
    if pos is None: return {}
    if not isinstance(pos, dict):
        problemas.append("posicoes tem de ser um mapa rota -> valor"); return {}
    return {k: _num(v, f"posicoes.{k}", problemas) for k, v in pos.items()}

def validar(doc, P=None, hoje=None):
    """(dados, problemas, avisos). `problemas` impedem o uso como estado REAL."""
    hoje = hoje or dt.date.today()
    problemas, avisos, d = [], [], {}

    for c in NUMERICOS:
        d[c] = _num(doc.get(c), c, problemas)
    # Ausente continua sendo zero dependentes; presente passa pela mesma porta (CX-04), e o
    # inteiro volta inteiro, porque `Estado.dependentes` e `int`.
    dep = doc.get("dependentes")
    d["dependentes"] = 0 if dep is None else _num(dep, "dependentes", problemas)
    if isinstance(d["dependentes"], float) and d["dependentes"].is_integer():
        d["dependentes"] = int(d["dependentes"])
    d["estabilidade_renda"] = doc.get("estabilidade_renda")
    d["posicoes"] = _posicoes(doc.get("posicoes"), problemas)
    # P-24. Onde a reserva esta, rota por rota. AUSENTE e diferente de VAZIO:
    #   ausente = o motor nao sabe, e o G2 diz isso em voz alta;
    #   {}      = nao ha reserva em lugar nenhum, que e afirmacao, nao ignorancia.
    # Manter os dois distintos e o que impede o motor de supor uma composicao que
    # ninguem informou.
    d["reserva_por_rota"] = doc.get("reserva_por_rota")
    if d["reserva_por_rota"] is not None:
        if not isinstance(d["reserva_por_rota"], dict):
            problemas.append("reserva_por_rota tem de ser um mapa rota -> valor")
            d["reserva_por_rota"] = None
        else:
            d["reserva_por_rota"] = {k: _num(v, f"reserva_por_rota.{k}", problemas)
                                     for k, v in d["reserva_por_rota"].items()}
            soma = sum(v for v in d["reserva_por_rota"].values() if v is not None)
            nom0 = d.get("reserva_atual")
            if nom0 is not None and abs(soma - nom0) > 0.01:
                problemas.append(
                    f"reserva_por_rota soma {soma:.2f} e reserva_atual diz {nom0:.2f}. "
                    f"Sao duas medidas do mesmo saldo e elas discordam — o sistema nao "
                    f"escolhe entre as duas por voce")
    # P-71: ate 11/09/2026 estes dois viravam LISTA DE DICT, e todo consumidor real
    # (g1_divida: `d.taxa_am`; necessidade_datada: `o.prazo_anos`) espera dataclass.
    # Nao estourava porque nenhum teste carregava um estado pelo caminho real -- as
    # duas listas do estado.yaml de producao estao vazias. Convertido aqui, na UNICA
    # porta de entrada, para que quem chama `Estado(**d)` receba o contrato certo.
    d["dividas"] = _registros(doc.get("dividas"), Divida, "dividas", problemas)
    d["objetivos"] = _registros(doc.get("objetivos"), Objetivo, "objetivos", problemas)
    d["match_verificado"], d["match_empregador"] = _match(doc, problemas)

    meta = doc.get("meta") or {}
    if meta.get("status") != "REAL":
        problemas.append(
            f"meta.status = {meta.get('status')!r}: enquanto nao for REAL, o sistema trata "
            f"os numeros como cenario. Nenhuma decisao deve sair de um estado MODELO")
    pe = meta.get("preenchido_em")
    if isinstance(pe, str):
        avisos.append(f"meta.preenchido_em = '{pe}' e texto. YAML entende data como "
                      f"AAAA-MM-DD; escreva {hoje.isoformat()}")
        m = re.fullmatch(r"(\d{2})/(\d{2})/(\d{4})", pe.strip())
        if m and int(m.group(3)) > hoje.year:
            problemas.append(f"meta.preenchido_em aponta para {m.group(3)}, no futuro — "
                             f"provavel erro de digitacao no ano")
    elif pe is None:
        avisos.append("meta.preenchido_em vazio")

    # ── J-01: reserva empenhada nao e reserva ────────────────────────────────
    # Achado de 05/09/2026. O app do PicPay declara "Usado como limite: R$7.671,01 /
    # Disponivel para resgate: R$0,00" — o saldo inteiro garante o limite do cartao.
    # A funcao LIQUIDEZ exige resgate em ate 1 dia. Reserva empenhada cobre o cenario
    # em que nada acontece, que e o unico em que reserva nao serve para nada.
    d["reserva_disponivel"] = _num(doc.get("reserva_disponivel"), "reserva_disponivel",
                                   problemas) if doc.get("reserva_disponivel") is not None \
                              else d.get("reserva_atual")
    _conferir_empenho(doc, d, problemas)
    nom, disp = d.get("reserva_atual"), d.get("reserva_disponivel")
    if nom is not None and disp is not None and disp < nom - 1e-9:
        desp = d.get("despesa_mensal") or 0
        meses = (disp / desp) if desp else 0.0
        problemas.append(
            f"RESERVA EMPENHADA: nominal {nom:.2f}, disponivel para resgate {disp:.2f}. "
            f"A funcao LIQUIDEZ exige resgate em ate 1 dia — o que esta empenhado nao "
            f"cobre emergencia nenhuma. Meses de despesa cobertos DE VERDADE: {meses:.1f}, "
            f"nao {(nom/desp if desp else 0):.1f}. Fonte: "
            f"{doc.get('reserva_empenhada_fonte', '(nao declarada)')}")

    if d["estabilidade_renda"] not in ("alta", "media", "baixa"):
        problemas.append(f"estabilidade_renda = {d['estabilidade_renda']!r}: "
                         f"use alta, media ou baixa")

    # P-72 (11/09/2026): aporte_mensal == 0 bloqueava o carregamento inteiro, o que
    # contradiz a U-01 -- um cliente novo que ainda nao guarda nada e um ESTADO, nao
    # um erro de preenchimento. So o NEGATIVO continua impossivel (bloqueia).
    if d["aporte_mensal"] is not None and d["aporte_mensal"] < 0:
        problemas.append(
            f"aporte_mensal = {d['aporte_mensal']:.2f}: negativo nao existe. Corrija "
            f"o arquivo")
    elif d["aporte_mensal"] == 0:
        avisos.append(
            "aporte_mensal = 0. Sem aporte nao ha reserva a formar nem alocacao a "
            "executar, e nenhum portao que decide 'quanto' tem o que fazer -- mas isto "
            "e o estado de um cliente que ainda nao guarda nada, e o sistema responde "
            "mesmo assim (achado U-01). Se o valor for real, a questao do projeto "
            "deixa de ser 'onde aportar' e passa a ser 'de onde sai o aporte'. Se foi "
            "deixado em branco, e o campo mais importante a preencher")

    if d["despesa_mensal"] and d["reserva_atual"] is not None:
        # P-71, mesmo achado lateral: `d["meses_cobertos"]` tambem quebrava
        # `Estado(**d)` -- `Estado.meses_cobertos` ja e uma property calculada da
        # reserva EFETIVA (nao da nominal, achado J-01). Guardar aqui era a N-01,
        # "duplicacao de formula", que a auditoria externa tambem ja tinha achado.
        meses = d["reserva_atual"]/d["despesa_mensal"]
        if meses < 1: avisos.append(f"reserva cobre {meses:.1f} mes de despesa")


    return d, problemas, avisos

def coerencia_da_estabilidade(respostas):
    """Traduz as tres perguntas objetivas em uma classificacao.

    Existe para que `estabilidade_renda` nao seja opiniao: as tres perguntas tem
    resposta verificavel, e a classificacao sai delas. O campo mais consequente do
    arquivo nao pode depender de como a pessoa se sente em relacao a risco."""
    n_clientes   = respostas["n_clientes"]
    meses_garantidos = respostas["meses_de_receita_garantida"]
    tem_aviso    = respostas["tem_aviso_previo"]
    pontos = 0
    razoes = []
    if n_clientes <= 1:
        pontos += 2; razoes.append("cliente unico: a perda do contrato zera a receita")
    elif n_clientes <= 3:
        pontos += 1; razoes.append(f"{n_clientes} clientes: concentracao alta")
    if not tem_aviso:
        pontos += 2; razoes.append("sem aviso previo: a receita pode parar de um mes para o outro")
    if meses_garantidos < 3:
        pontos += 1; razoes.append(f"{meses_garantidos} meses de receita contratada a frente")
    if respostas.get("parte_variavel_pode_ser_zero"):
        pontos += 1; razoes.append("parte da remuneracao e variavel e pode nao vir")
    nivel = "baixa" if pontos >= 3 else ("media" if pontos >= 1 else "alta")
    return dict(nivel=nivel, pontos=pontos, razoes=razoes)

def carregar(path=None, P=None, exigir_real=True):
    p = path or os.path.join(AQUI, "estado.yaml")
    with open(p, encoding="utf-8") as f:
        doc = yaml.safe_load(f) or {}
    d, problemas, avisos = validar(doc, P)
    if problemas and exigir_real:
        raise EstadoInvalido("\n  - " + "\n  - ".join(problemas))
    return d, problemas, avisos

if __name__ == "__main__":
    with open(os.path.join(AQUI, "estado.yaml"), encoding="utf-8") as f:
        doc = yaml.safe_load(f) or {}
    d, problemas, avisos = validar(doc)
    print("="*84); print("VALIDACAO DO estado.yaml"); print("="*84)
    print(f"\n{len(problemas)} problema(s) que impedem tratar como estado REAL:")
    for x in problemas: print(f"  [BLOQUEIA] {x}\n")
    for x in avisos: print(f"  [aviso] {x}")
    print("\nLido:")
    for k in NUMERICOS + ("estabilidade_renda", "dependentes"):
        print(f"  {k:<20} {d.get(k)}")
    print("\n" + "="*84)
    print("COERENCIA DA ESTABILIDADE — a partir das SUAS respostas de 04/09/2026")
    print("="*84)
    c = coerencia_da_estabilidade(dict(
        n_clientes=1, meses_de_receita_garantida=0, tem_aviso_previo=False,
        parte_variavel_pode_ser_zero=True))
    print(f"  declarado no arquivo: {d.get('estabilidade_renda')}")
    print(f"  implicado pelas respostas: {c['nivel'].upper()}  ({c['pontos']} pontos de 6)")
    for r in c["razoes"]: print(f"     - {r}")
