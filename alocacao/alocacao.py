# -*- coding: utf-8 -*-
"""
Camada de alocacao v2 — decide QUANTO e ONDE, com a tabela de custo como insumo real.

Versao 2 (03/09/2026) responde a auditoria de 02/09/2026. O que mudou, e por que:

  A-01  G4 so elimina se a rota perder em TODOS os horizontes de teste. IVVB11 bate a
        Avenue ate 10 anos e perde dela a partir de 15 — custo por aporte dilui, taxa
        anual nao. Ordem que inverte com o horizonte nao e dominancia; e preferencia
        de horizonte, e agora sai rotulada como tal.
  A-02  G3 separa custo FIXO (dilui, e o sistema calcula o aporte de reentrada) de
        custo PERCENTUAL (nao dilui, a rota nunca volta). A promessa "ela volta sozinha
        quando o aporte cresce" era falsa para as quatro rotas que o portao elimina.
  A-03  Toda chave sob funcoes/portoes/crescimento/tetos e lida. test_cobertura_yaml
        falha se alguma nao for.
  A-04  Funcao LASTRO criada. DATADO passa a exigir objetivo datado e casamento de
        duracao. Sem objetivo, o bloco fica vazio e o dinheiro vai para LASTRO —
        pos-fixado, sem marcacao a mercado. Antes, 17% iam para Tesouro IPCA+ sob uma
        funcao cuja definicao exige um prazo que nao existia.
  A-05  G1 compara liquido com liquido.
  A-06  O gatilho de deriva compara a capacidade do aporte com o maior DEFICIT, nao
        com o maior desvio absoluto. O aporte so compra: excesso nao e problema dele.
  B-*   caixa como posicao, `negocia_em_lote` explicito, raise no lugar de assert,
        procedencia no retorno, segunda coluna de custo, criterio de custo no G2.

O que este modulo NAO faz, e por que:
  Nao calcula alocacao otima. DeMiguel, Garlappi & Uppal (2009) testaram 14 modelos
  de otimizacao contra 1/N em 7 conjuntos de dados; nenhum venceu fora da amostra, e
  seriam necessarios ~3.000 meses de historia para o otimizador ganhar com 25 ativos.
  Temos 16 anos de fundamentos brasileiros.
"""
from __future__ import annotations
import copy
import os, sys, math, hashlib, datetime as dt
from dataclasses import dataclass, field, replace
from typing import Optional
import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motor import val, custodia_rv_aa, InsumoBloqueado
from tese import carregar_registros, meses_de_reserva_no_texto

AQUI = os.path.dirname(os.path.abspath(__file__))

# Chaves que descrevem UMA pessoa, nao o sistema. Vivem em perfil.yaml (achado L-01).
SECOES_DE_PERFIL = ("compromissos", "decisoes")

def carregar_politica(path=None, perfil=None):
    """Funde politica.yaml (o motor) com perfil.yaml (um usuario).

    ACHADO L-01 (05/09/2026). O usuario lembrou que escalabilidade inclui SERVIR MAIS
    PESSOAS, e o projeto estava construido sobre as preferencias dele: 109 chaves de
    motor e 13 de usuario no MESMO arquivo. Um segundo usuario nao teria onde por as
    escolhas dele sem editar o politica.yaml — e ao editar, apagaria as do primeiro.

    A fusao acontece na CARGA, entao nenhum consumidor mudou: os seis arquivos que
    liam `compromissos` e `decisoes` continuam lendo igual. Trocar de usuario e
    passar outro `perfil`.
    """
    p = path or os.path.join(AQUI, "politica.yaml")
    with open(p, encoding="utf-8") as f:
        texto = f.read()
    P = yaml.safe_load(texto)

    for s in SECOES_DE_PERFIL:
        if s in P:
            raise ValueError(
                f"secao {s!r} esta em politica.yaml e ela descreve UM usuario. "
                f"O lugar dela e perfil.yaml — ver SECOES_DE_PERFIL e o achado L-01")

    pf = perfil or os.path.join(AQUI, "perfil.yaml")
    with open(pf, encoding="utf-8") as f:
        texto_perfil = f.read()
    PF = yaml.safe_load(texto_perfil)
    for k, v in PF.items():
        if k == "meta":
            P["_perfil"] = v
        elif k in P:
            raise ValueError(f"perfil sobrescreveria {k!r} da politica: o perfil "
                             f"descreve escolhas, nao redefine o motor")
        else:
            P[k] = v

    P["_hash"] = hashlib.sha256(texto.encode("utf-8")).hexdigest()[:12]
    P["_hash_perfil"] = hashlib.sha256(texto_perfil.encode("utf-8")).hexdigest()[:12]
    return P

_CACHE_HASH_CUSTOS: dict[tuple, str] = {}

def hash_custos(path=None):
    """sha256[:12] do custos.yaml. E a impressao digital que viaja na procedencia de
    toda saida, e tambem a chave de invalidacao do cache de arrasto.

    ACHADO S-01 (06/09/2026), medido com cProfile. Esta funcao era chamada 73 vezes
    por `alocar()` — uma por consulta ao cache de `arrasto_anualizado`, que a usa na
    chave — e cada chamada RELIA E RE-HASHEAVA os 33 KB do arquivo. Resultado: 37% do
    tempo de `alocar()` era gasto hasheando um arquivo para decidir se podia usar um
    valor ja calculado. O cache que existe para acelerar era o maior custo do motor.

    A intencao estava certa e continua: um numero memoizado TEM de ser invalidado se
    os custos mudarem — e a doutrina P1 aplicada a memoizacao. O que estava errado era
    o preco de perguntar.

    Agora o hash e memoizado por (caminho, mtime_ns, tamanho): se o arquivo nao mudou,
    devolve o hash ja calculado; se mudou, recalcula. Custa um `stat()` no lugar de um
    read + sha256 de 33 KB.

    LIMITE DECLARADO: duas escritas diferentes no MESMO nanossegundo e com o MESMO
    tamanho passariam despercebidas. Em Linux `st_mtime_ns` tem resolucao de
    nanossegundo e YAML editado a mao nao muda de tamanho por acaso — mas o buraco
    existe e esta escrito. Quem precisar de garantia absoluta chama
    `hash_custos_sem_cache()`."""
    p = path or os.path.join(AQUI, "custos.yaml")
    st = os.stat(p)
    k = (p, st.st_mtime_ns, st.st_size)
    if k not in _CACHE_HASH_CUSTOS:
        _CACHE_HASH_CUSTOS.clear()      # o arquivo mudou: nada do que havia vale
        _CACHE_HASH_CUSTOS[k] = hash_custos_sem_cache(p)
    return _CACHE_HASH_CUSTOS[k]


def hash_custos_sem_cache(path=None):
    """Le e hasheia de verdade. Existe para o caso em que a garantia importa mais que
    o tempo — e para o teste que prova que o cache devolve o mesmo valor."""
    p = path or os.path.join(AQUI, "custos.yaml")
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()[:12]

# ══ ENTRADA: estado financeiro. Tudo OBSERVAVEL — nada previsto. ══════════════
@dataclass
class Divida:
    nome: str
    saldo: float
    taxa_am: float          # custo mensal efetivo

@dataclass
class Objetivo:
    nome: str
    valor: float
    prazo_anos: float

@dataclass
class MatchEmpregador:
    """Contrapartida do empregador. `None` no Estado significa DESCONHECIDO, nao ausente."""
    taxa: float                  # 0.50 = empregador poe 50 centavos por real seu
    teto_pct_salario: float
    salario_bruto_mensal: float

@dataclass
class Estado:
    despesa_mensal: float
    reserva_atual: float
    aporte_mensal: float
    estabilidade_renda: str = "media"        # alta | media | baixa
    dependentes: int = 0
    horizonte_anos: float = 25
    dividas: list = field(default_factory=list)
    objetivos: list = field(default_factory=list)
    posicoes: dict = field(default_factory=dict)   # rota -> valor atual
    caixa: float = 0.0                             # B-03: residuo de lote mora aqui
    match_empregador: Optional[MatchEmpregador] = None
    match_verificado: bool = False                 # False = ninguem perguntou ao RH
    reserva_disponivel: Optional[float] = None     # J-01: None = nao ha empenho declarado
    # P-24. A reserva era UM numero e o mundo tem BALDES. Com teto de saldo por
    # produto, "quanto ha de reserva" deixa de bastar: para saber se a proxima
    # parcela cabe, e preciso saber ONDE ela esta. None = o motor nao sabe, e ele
    # diz isso em voz alta em vez de supor que foi construida na ordem do plano.
    reserva_por_rota: Optional[dict] = None

    @property
    def patrimonio_investido(self): return sum(self.posicoes.values()) + self.caixa

    @property
    def reserva_conferida(self):
        """True quando os baldes somam a reserva declarada. Divergencia nao e erro do
        usuario: e informacao que o motor tem de mostrar em vez de escolher um dos
        dois numeros por conta propria."""
        if self.reserva_por_rota is None: return None
        return abs(sum(self.reserva_por_rota.values()) - self.reserva_atual) < 0.01
    @property
    def reserva_efetiva(self):
        """J-01: o que da para SACAR, nao o que aparece no saldo.

        Reserva empenhada como garantia (cofrinho usado como limite de cartao, CDB
        dado em caucao) cobre o cenario em que nada acontece — o unico em que reserva
        nao serve para nada. Quando `reserva_disponivel` nao e informada, ela e igual
        a nominal: ausencia de informacao nao vira empenho presumido."""
        return self.reserva_atual if self.reserva_disponivel is None \
               else self.reserva_disponivel

    @property
    def reserva_empenhada(self):
        return max(0.0, self.reserva_atual - self.reserva_efetiva)

    @property
    def meses_cobertos(self):
        """Conta pela reserva EFETIVA. Contar pela nominal era responder a pergunta
        'quanto eu tenho' quando a pergunta do G2 e 'por quantos meses eu aguento'."""
        return self.reserva_efetiva/self.despesa_mensal if self.despesa_mensal else 0.0

    @property
    def meses_cobertos_nominal(self):
        return self.reserva_atual/self.despesa_mensal if self.despesa_mensal else 0.0

# ══ CATALOGO DE ROTAS ════════════════════════════════════════════════════════
@dataclass
class RotaAloc:
    id: str
    nome: str
    funcoes: list               # funcoes que a rota PODE ocupar (a 1a e a primaria)
    exposicao: str              # ativo-objeto — usado na regra de dominancia
    corr_fix: float = 0.0
    corr_pct: float = 0.0
    b3_vista: bool = False
    entrada_extra: float = 0.0
    saida_extra: float = 0.0
    adm_aa: float = 0.0
    custodia_interna_aa: float = 0.0  # taxa de custodia COBRADA DENTRO do fundo, alem da adm
    custodia_rv: bool = False
    custodia_td: bool = False
    td_isento: bool = False
    liquidez_dias: int = 1
    perda_maxima: str = "limitada"     # nominal_zero | limitada | total
    duracao_anos: Optional[float] = 0.0   # 0 = pos-fixado; None = vem do registro CARREGO
    # P-12 (12a, 26/09/2026): PRAZO ATE O VENCIMENTO, que NAO e a duracao acima. A duracao
    # de uma LCI pos-fixada e 0,0 -- a do juro --, e o vencimento dela pode ser 2 anos.
    # Casar vencimento com objetivo pela duracao deixaria passar a LCI de 9999 dias de
    # carencia. None = nao se sabe o vencimento, e sem ele a rota iliquida nao casa (P1).
    vencimento_anos: Optional[float] = None
    indexador: str = "cdi"             # para o retorno liquido do G2
    rendimento_fator: float = 1.0      # fracao do indexador que a rota entrega
    # P-13: dois campos, nao um. `isento_ir` era booleano e o FII nao cabia nele —
    # o RENDIMENTO distribuido e isento (>=100 cotistas, Lei 11.033/2004 art. 3o) e o
    # GANHO de capital e tributado a 20% (Lei 8.668/1993 art. 18), sem a isencao mensal
    # de R$20 mil. True subestimava o imposto, False superestimava; nao havia valor certo.
    # LCI e LCA sao o caso simples: as duas pontas isentas.
    isento_ir_rendimento: bool = False   # juros/dividendos/aluguel recebidos
    aliquota_ganho: Optional[float] = None  # None = usa a tabela geral da rota
    negocia_em_lote: bool = False      # B-04: nao inferir por magnitude do preco
    # P-179 (decisao dele, 04/10/2026): o lote do Tesouro Direto e 0,01 titulo. Com a fracao
    # declarada, o preco de um lote e `preco_do_lote(r, PU)`; None = o lote e uma unidade.
    lote_fracao: Optional[float] = None
    emissor: Optional[str] = None      # para o teto do FGC por conglomerado
    # P-24 / achado K-02. TETO DE SALDO nao e teto do FGC, e confundir os dois e um
    # erro de categoria com consequencias opostas:
    #   FGC       limita a GARANTIA. Passar dele deixa o excedente sem seguro — e um
    #             RISCO, e o usuario pode escolher aceita-lo.
    #   teto de   limita quanto o produto ACEITA. Passar dele nao e arriscado: e
    #   saldo     IMPOSSIVEL. O deposito e recusado.
    # O primeiro muda a qualidade do dinheiro aplicado; o segundo muda se ele pode
    # ser aplicado. Um portao que so conhece o primeiro recomenda um destino que nao
    # existe mais, e continua recomendando.
    teto_de_saldo: Optional[float] = None
    bloqueios: list = field(default_factory=list)
    nota: str = ""

    @property
    def funcao(self): return self.funcoes[0]
    @property
    def isento_ir(self):
        """Compatibilidade com quem lia o campo antigo. Ele SEMPRE se referiu ao
        rendimento — nunca ao ganho — e agora isso esta explicito no nome."""
        return self.isento_ir_rendimento
    def capacidade(self, saldo_ja_aplicado=0.0):
        """Quanto a rota ainda aceita. `None` = sem teto declarado, e sem teto
        declarado NAO e o mesmo que sem teto: e teto desconhecido. Quem chama decide
        o que fazer com a ausencia — aqui ela nao vira infinito em silencio."""
        if self.teto_de_saldo is None: return None
        return max(0.0, self.teto_de_saldo - saldo_ja_aplicado)

    @property
    def interno_aa(self):
        """Tudo que o veiculo desconta do patrimonio por dentro, ao ano.

        Achado F-01: o regulamento dos ETF iShares BR cobra, ALEM da taxa de
        administracao, uma taxa de custodia interna de ate 0,025% a.a. Modelar
        so a adm_aa subestimava o custo do BOVA11 em 25%.
        """
        return self.adm_aa + self.custodia_interna_aa
    @property
    def confiavel(self): return not self.bloqueios

CATALOGO_YAML = os.path.join(AQUI, "catalogo.yaml")


def _caminho(C, caminho):
    """Navega `a.b.c` dentro do custos.yaml. Caminho inexistente e ERRO DURO e nao
    None: um `{de:}` apontando para o vazio e erro de digitacao, e devolver None faria
    a rota nascer com o campo no default — silenciosamente errada."""
    no = C
    for parte in caminho.split("."):
        if not isinstance(no, dict) or parte not in no:
            raise KeyError(f"catalogo.yaml aponta para custos.yaml -> {caminho}, "
                           f"que nao existe (parou em {parte!r})")
        no = no[parte]
    return no


def _resolve(C, v, contexto):
    """Resolve um valor do catalogo.yaml. Literal passa direto; dict com chave
    reservada vira leitura do custos.yaml.

    Levanta InsumoBloqueado quando a constante referida esta NAO_CONFIRMADO — quem
    chama transforma isso em bloqueio DA ROTA (achado Q-01)."""
    if not isinstance(v, dict):
        return v
    if "de" in v:
        # o contexto e o CAMINHO DA CONSTANTE e nao o campo da rota: quem le a
        # mensagem precisa saber que numero ir buscar, nao onde ele seria usado.
        return val(_caminho(C, v["de"]), contexto=v["de"])
    if "de_campo" in v:
        return _caminho(C, v["de_campo"])
    if "soma" in v:
        return sum(_resolve(C, x, contexto) for x in v["soma"])
    if "de_se_na_lista" in v:
        # F-01: quem cobra custodia interna vem de `aplica_a` da propria constante,
        # nunca de uma lista escrita no codigo.
        d = v["de_se_na_lista"]
        no = _caminho(C, d["valor"])
        return val(no, contexto=d["valor"]) if d["chave"] in set(no["aplica_a"]) else d["senao"]
    raise ValueError(f"{contexto}: chave de referencia desconhecida em {sorted(v)}")


# ── As tres estrategias de bloqueio ──────────────────────────────────────────
# Isto e LOGICA e por isso fica em Python. O catalogo.yaml diz QUAL estrategia se
# aplica e a QUE fonte; aqui esta COMO. Acrescentar uma rota nao exige tocar neste
# arquivo; acrescentar um TIPO NOVO de regra exige — e deve exigir.
#
# Os tres formatos de mensagem sao DIFERENTES, e essa inconsistencia e herdada do
# codigo que existia antes da P-36. Ela esta preservada de proposito: unifica-la
# junto da migracao misturaria duas mudancas e destruiria a garantia forte de que o
# catalogo migrado e identico ao que era codigo.
def _bloq_val_recusa(C, fontes):
    """Bloqueia se `val()` recusar a constante. Mensagem: a da propria excecao."""
    fora = []
    for caminho in fontes:
        try: val(_caminho(C, caminho), contexto=caminho)
        except InsumoBloqueado as e: fora.append(str(e))
    return fora


def _bloq_motivo_literal(C, fontes):
    """Bloqueia sempre, com o campo `motivo` cru da constante."""
    return [_caminho(C, caminho)["motivo"] for caminho in fontes]


def _bloq_exige_status_completo(C, fontes):
    """Bloqueia enquanto o status nao for COMPLETO. Existe porque PARCIAL nao faz
    `val()` levantar: o valor existe, o que nao existe e a estabilidade dele."""
    fora = []
    for caminho in fontes:
        n = _caminho(C, caminho)
        if n.get("status") != "COMPLETO":
            fora.append(f"custos.yaml -> {caminho} esta {n.get('status')}: "
                        f"{n.get('motivo', '')}")
    return fora


ESTRATEGIAS_DE_BLOQUEIO = {
    "val_recusa": _bloq_val_recusa,
    "motivo_literal": _bloq_motivo_literal,
    "exige_status_completo": _bloq_exige_status_completo,
}

CAMPOS_RESERVADOS = ("procedencia", "bloqueio")


_CATALOGO_CRU: dict[str, dict] = {}

def carregar_catalogo(path=None):
    """Le o catalogo.yaml cru, sem resolver referencia nenhuma.

    Cacheado por caminho porque `catalogo(C)` e chamado centenas de vezes na suite e
    o custo e o PARSE, nao a resolucao. O cache guarda so o texto interpretado; as
    referencias sao resolvidas a cada chamada, contra o `C` que veio — senao um teste
    que altera o custos.yaml em memoria veria um catalogo velho."""
    p = path or CATALOGO_YAML
    if p not in _CATALOGO_CRU:
        with open(p, encoding="utf-8") as f:
            _CATALOGO_CRU[p] = yaml.safe_load(f)
    return copy.deepcopy(_CATALOGO_CRU[p])


def catalogo(C, path=None):
    """Monta o catalogo a partir do catalogo.yaml, resolvendo as referencias contra
    o custos.yaml. Pendencia P-36.

    Ate 05/09/2026 estas 25 rotas eram 183 linhas de literais Python. Mudar a
    corretagem de uma rota era editar codigo, e nada do aparato de procedencia do
    custos.yaml alcancava um unico desses valores — a doutrina P2 valia para as
    regras e nao para o catalogo, que e a maior estrutura de dado do projeto.

    ACHADO Q-01, encontrado na migracao: o tratamento de insumo bloqueado era
    INCONSISTENTE. As rotas de ETF degradavam (a rota entrava sem a taxa e com o
    motivo escrito); todas as outras derrubavam o CATALOGO INTEIRO. Uma constante
    NAO_CONFIRMADO em `corretagem.safra_terra` apagaria as 25 rotas, inclusive as 24
    que nao dependem dela — o oposto exato da doutrina P6. Aqui a regra e uma so:
    insumo bloqueado bloqueia A ROTA, com o motivo escrito."""
    d = carregar_catalogo(path)
    R = []
    for rid, cru in d["rotas"].items():
        if rid.startswith("_"):      # ancoras de modelo (&modelo_etf_b3)
            continue
        campos, bloqueios = {}, []
        b = cru.get("bloqueio")
        if b:
            estrategia = ESTRATEGIAS_DE_BLOQUEIO.get(b["regra"])
            if estrategia is None:
                raise ValueError(f"{rid}: estrategia de bloqueio desconhecida "
                                 f"{b['regra']!r}. As conhecidas sao "
                                 f"{sorted(ESTRATEGIAS_DE_BLOQUEIO)}")
            bloqueios += estrategia(C, b["fontes"])
        for k, v in cru.items():
            if k in CAMPOS_RESERVADOS: continue
            try:
                campos[k] = _resolve(C, v, contexto=f"{rid}.{k}")
            except InsumoBloqueado as e:
                # Q-01: o campo simplesmente nao entra, e a rota carrega o motivo.
                # Nascer com o default (custo ZERO) foi o achado F-02.
                bloqueios.append(str(e))
        R.append(RotaAloc(id=rid, bloqueios=bloqueios, **campos))
    return R


# ══ CUSTO ════════════════════════════════════════════════════════════════════
def custo_entrada_fixo_pct(r, aporte):
    """Parte do custo de entrada que DILUI com o aporte.

    Achado lateral do P-71/P-72 (11/09/2026), encontrado escrevendo o teste que prova
    o pipeline inteiro com `aporte_mensal=0` — estado que a P-72 passou a permitir.
    `r.corr_fix == 0` e custo zero para QUALQUER aporte, aporte==0 incluso: uma rota
    sem tarifa fixa nao fica infinitamente cara so porque nao ha aporte este mes. A
    versao anterior tratava aporte==0 como `math.inf` incondicional — isso reprovava
    TODA rota no G3 (inclusive as de tarifa zero) e `_conferir_invariantes` recusava
    pesos somando 0 em vez de 1. Para aporte>0 o resultado e identico ao de antes.

    A irma era `motor.custo_entrada_pct`, que em 12/09 ganhou o mesmo tratamento (E-01)
    e saiu com a P-43 em 24/09: esta e a unica."""
    if r.corr_fix == 0:
        return 0.0
    return r.corr_fix/aporte if aporte else math.inf

def custo_entrada_percentual(r, B3V):
    """Parte do custo de entrada que NAO dilui com aporte nenhum. Achado A-02."""
    return r.corr_pct + (B3V if r.b3_vista else 0.0) + r.entrada_extra

def custo_entrada_pct(r, aporte, B3V):
    return custo_entrada_fixo_pct(r, aporte) + custo_entrada_percentual(r, B3V)

def custo_saida_pct(r, B3V):
    return r.corr_pct + (B3V if r.b3_vista else 0) + r.saida_extra

class AporteConsumidoPelaEntrada(ValueError):
    """P-134 (B-16, divergencia 4): o custo de entrada iguala ou passa o aporte.

    Era `min(e*aporte, aporte)`: a rota comia o aporte inteiro e a simulacao devolvia um
    numero, sem dizer nada -- a forma do F-02, condicao engolida virando valor. O G3 barra
    a rota no pipeline com o aporte INTEIRO; mas `custo_pct_aportado` do alvo e o
    `custo_de_discordar` simulam cada rota com o aporte DELA (`aporte * peso`), e a
    proposta do segundo nem passa pelo G3. Medido em 25/09: `acao_450` (R$ 4,50 por
    ordem) chega aqui com aporte da rota de ate R$ 4,50 -- peso de 0,9% a R$ 500/mes."""


def simular_custo(r, C, aporte, anos):
    """Retorna (patrimonio_final, custo_total, aportado). Base das duas metricas.

    Achado F-02: uma rota BLOQUEADA nao simula. Antes, `bovv11` — cuja taxa de
    administracao e NAO_CONFIRMADO — devolvia custo como se a taxa fosse ZERO, o
    que a fazia parecer a rota MAIS BARATA do catalogo. O bloqueio so era honrado
    nos portoes; quem chamasse a simulacao direto recebia um numero falso e
    favoravel. Insumo ausente agora recusa o calculo, em vez de virar zero.
    """
    if not r.confiavel:
        raise InsumoBloqueado(f"rota {r.id} bloqueada: {'; '.join(r.bloqueios)}")
    B3V  = val(C["b3"]["vista_total_pct"], contexto="b3")
    ISEN = val(C["b3"]["custodia_rv_isencao"], contexto="isen")
    FX   = C["b3"]["custodia_rv_faixas"]["valor"]
    # B-17: ate 24/09 a unica leitura desta chave morava em `motor.simular`, que so testes
    # chamavam; aqui valia o default "deducao" da funcao -- igual ao YAML por acidente.
    INTERP = val(C["b3"]["custodia_rv_interpretacao"], contexto="b3.interp")
    TDC  = val(C["tesouro"]["custodia_aa"], contexto="tdc")
    TDI  = val(C["tesouro"]["isencao_selic"], contexto="tdi")
    bruto = val(C["macro"]["cdi_aa"], contexto="cdi")
    m = (1+bruto)**(1/12)-1
    pat = custo = 0.0
    e = custo_entrada_pct(r, aporte, B3V)
    if e >= 1.0:
        raise AporteConsumidoPelaEntrada(
            f"rota {r.id}: entrada de {e:.1%} do aporte de R$ {aporte:.2f} -- o custo come "
            f"o aporte inteiro, e nao ha patrimonio a simular")
    n = int(anos*12)
    for _ in range(n):
        c = e*aporte; pat += aporte-c; custo += c
        pat *= (1+m)
        if r.interno_aa:
            t = pat*((1+r.interno_aa)**(1/12)-1); pat -= t; custo += t
        if r.custodia_rv:
            t = custodia_rv_aa(pat, FX, ISEN, INTERP)/12; pat -= t; custo += t
        if r.custodia_td:
            # P-124 (124a, escolha dele de 26/09): mensal por decisao, nao por engano. A B3
            # cobra por netting pro rata, semestral e no resgate (OC 014/2024-VPC); o mensal
            # erra centavos por ano CONTRA o Tesouro. `politica.yaml -> limitacoes_declaradas
            # .periodicidade_da_custodia_do_tesouro`.
            base = max(0.0, pat-TDI) if r.td_isento else pat
            t = base*((1+TDC)**(1/12)-1); pat -= t; custo += t
    s = custo_saida_pct(r, B3V); custo += pat*s; pat -= pat*s
    return pat, custo, aporte*n

_CACHE_POR_CONTEUDO: dict[str, dict] = {}
_LIMITE_DE_CONTEUDOS = 32

def impressao_de_custos(C):
    """Impressao digital do CONTEUDO de custos em memoria.

    S-02 ensinou a distincao, e ela vale escrever porque confundi-la foi o defeito:
      `hash_custos()`        e do ARQUIVO em disco. Serve a PROCEDENCIA — dizer de
                             qual custos.yaml uma saida nasceu.
      `impressao_de_custos()` e do CONTEUDO que esta sendo usado. Serve a CORRECAO DE
                             CACHE — dizer se dois calculos podem compartilhar
                             resultado.
    Sao a mesma coisa enquanto ninguem altera o `C` em memoria. Todo teste altera."""
    return hashlib.sha256(repr(C).encode("utf-8")).hexdigest()[:16]


def memo_de_arrasto(C):
    """O memo compartilhado por todo mundo que usa ESTE conteudo de custos.

    Devolve o mesmo dict para dois `C` de conteudo igual, e dicts diferentes para
    conteudos diferentes — que e exatamente a garantia que faltava. Custa uma
    impressao (~0,3 ms) e economiza ~15 ms por `alocar()`.

    O dicionario e limitado a `_LIMITE_DE_CONTEUDOS` conteudos distintos: uma suite
    que varia custos em centenas de testes nao pode virar um vazamento de memoria.
    Quando estoura, o mais antigo sai — nao ha correcao em jogo, so reaproveitamento."""
    k = impressao_de_custos(C)
    if k not in _CACHE_POR_CONTEUDO and len(_CACHE_POR_CONTEUDO) >= _LIMITE_DE_CONTEUDOS:
        _CACHE_POR_CONTEUDO.pop(next(iter(_CACHE_POR_CONTEUDO)))
    return _CACHE_POR_CONTEUDO.setdefault(k, {})


def arrasto_anualizado(r, C, aporte, anos, cache=None):
    """Quanto de RETORNO a rota consome por ano, em pontos de taxa.

    ATENCAO ao rotulo (achado B-06): este numero NAO e comparavel com a taxa de
    administracao que o leitor conhece. Ele e o quociente de valores terminais
    anualizado sobre o horizonte inteiro, enquanto a exposicao media de um fluxo
    mensal e ~metade do horizonte. Para uma rota cujo unico custo e 1,30% a.a. ele
    devolve 0,73% em 5 anos e 1,05% em 40. Use junto com custo_pct_aportado().

    ACHADO S-02 (06/09/2026), e ele e da familia do F-02 e do N-01: um mecanismo que
    parecia funcionar e nao funcionava.

    Havia um cache GLOBAL, `_CACHE_ARRASTO`, cuja chave incluia `hash_custos()` — o
    hash do ARQUIVO em disco. Mas o custo que esta funcao usa vem do `C` que chega
    como PARAMETRO. Passar um `C` modificado em memoria (que e o que todo teste faz,
    via deepcopy) devolvia o valor calculado com o `C` ORIGINAL, em silencio.

    Medido: com a taxa do BOVA11 alterada de 0,10% para 50% ao ano, o arrasto voltava
    identico. Qualquer teste que alterasse um custo e conferisse arrasto ou dominancia
    estava testando nada.

    Nao ha mais cache global. `cache` e um dict OPCIONAL que quem chama cria e cuja
    validade quem chama garante — na pratica, um por invocacao, onde o `C` nao muda.
    Um cache cuja chave nao inclui a entrada nao e um cache: e uma resposta errada
    guardada.
    """
    k = (r.id, round(aporte,2), round(anos,4))
    if cache is not None and k in cache: return cache[k]
    bruto = val(C["macro"]["cdi_aa"], contexto="cdi")
    m = (1+bruto)**(1/12)-1
    pat, _custo, _ap = simular_custo(r, C, aporte, anos)
    sem_custo = sum(aporte*(1+m)**(anos*12-i) for i in range(int(anos*12)))
    out = math.inf if (pat <= 0 or sem_custo <= 0) else (sem_custo/pat)**(1/anos) - 1
    if cache is not None: cache[k] = out
    return out

def custo_pct_aportado(r, C, aporte, anos):
    """B-06: segunda coluna. Custo total como fracao do que foi aportado.
    Esta e a metrica que o leitor consegue interpretar sem conversao."""
    _pat, custo, aportado = simular_custo(r, C, aporte, anos)
    return custo/aportado if aportado else math.inf

# ── retorno liquido, para o G1 e o G2 (achados A-05 e B-08) ───────────────────
def aliquota_ir_rf(C, dias):
    for fx in C["tributacao"]["ir_rf_faixas"]["valor"]:
        if fx["ate_dias"] is None or dias <= fx["ate_dias"]:
            return fx["aliquota"]
    return 0.15

# ── P-77: as DUAS pontas do imposto, e por que uma funcao so nao expressa as duas ──
def regime_tributario(r):
    """Devolve (aliquota_sobre_o_rendimento_ou_None, motivo_ou_None).

    ACHADO P-77, 13/09/2026. A P-13 partiu `isento_ir` em DOIS campos porque o FII
    nao cabia num booleano: o RENDIMENTO distribuido e isento (Lei 11.033/2004 art.
    3o, com >=100 cotistas) e o GANHO e tributado a 20% (Lei 8.668/1993 art. 18),
    sem a isencao mensal de R$20 mil.

    **A P-13 criou o campo e ninguem o leu.** Medido em 13/09: `aliquota_ganho` tem
    ZERO leituras no motor -- as unicas quatro estao em `test_alocacao.py`. A
    correcao anunciada era mudanca de ESQUEMA sem mudanca de COMPORTAMENTO, que e a
    assinatura deste projeto: um arquivo declara um comportamento que o codigo nao
    tem, e os dois concordam por acidente.

    POR QUE NINGUEM VIU, e sao tres camadas:
      1. o FII e `indexador: rv`, e `retorno_liquido_aa` devolve None antes da linha
         do imposto -- entao hoje ele nao erra o numero, ele nao produz numero;
      2. o FII esta BLOQUEADO (`val_recusa` sobre `fii.taxa_administracao`);
      3. as unicas outras rotas com `aliquota_ganho` sao LCI e LCA, e nelas o valor e
         **0,0** -- as duas pontas isentas, onde a diferenca nao aparece.
    Tres coincidencias, e o campo morto atravessou todas.

    QUANDO MORDE: no dia em que existir uma rota de RENDA FIXA cujo ganho seja
    tributado diferente do rendimento -- debenture incentivada e o caso obvio. Ai
    `isento_ir_rendimento: true` zera o imposto INTEIRO e o `aliquota_ganho`
    continua inerte, e o numero sai errado para MENOS.

    O QUE ESTA FUNCAO NAO FAZ, de proposito: nao inventa um modelo de duas pontas.
    `retorno_liquido_aa` modela um instrumento que ACUMULA rendimento -- nele o ganho
    E o rendimento, e nao ha duas pontas a separar. Quando a rota declara pontas
    divergentes, a resposta honesta nao e um numero aproximado: e recusar, dizendo
    por que. P6 -- ausencia de criterio nao vira criterio de exclusao, vira lacuna
    declarada."""
    isento_rend = bool(r.isento_ir_rendimento)
    ag = r.aliquota_ganho
    if ag is None:
        return (0.0 if isento_rend else None), None      # None = usa a tabela geral
    if isento_rend and ag == 0.0:
        return 0.0, None                                  # LCI/LCA: as duas isentas
    if (not isento_rend) and ag == 0.0:
        return None, None                                 # so a tabela geral
    if isento_rend and ag > 0.0:
        return None, ("%s: rendimento isento e ganho a %.1f%% sao DUAS aliquotas, e "
                      "esta funcao modela uma so. Nao ha numero certo a devolver."
                      % (r.id, ag*100))
    return None, ("%s: rendimento tributado pela tabela e ganho a %.1f%% divergem."
                  % (r.id, ag*100))


def retorno_liquido_aa(r, C, dias_horizonte, patrimonio=0.0, motivos=None):
    """Retorno liquido anual de uma rota de renda fixa/caixa: rendimento do indexador
    vezes o fator que a rota entrega, menos IR da faixa, menos custo de custodia.
    B-08: e este o criterio do G2, nao a ordem alfabetica do id.

    `motivos`: dict opcional {rota_id: motivo}. Quando a rota e recusada por pontas
    tributarias divergentes (P-77), o motivo entra aqui em vez de sumir junto com o
    `None` -- porque foi exatamente um `None` calado que escondeu a P-77."""
    if r.indexador == "cdi":        bruto = val(C["macro"]["cdi_aa"], contexto="cdi")
    elif r.indexador == "selic":    bruto = val(C["macro"]["selic_aa"], contexto="selic")
    elif r.indexador == "poupanca":
        bruto = (1+val(C["macro"]["poupanca_am"], contexto="poup"))**12 - 1
    else:                           return None      # renda variavel: nao ha retorno conhecido
    fixa, motivo = regime_tributario(r)
    if motivo:
        if motivos is not None:
            motivos[r.id] = motivo
        return None
    bruto *= r.rendimento_fator
    ir = fixa if fixa is not None else aliquota_ir_rf(C, dias_horizonte)
    liq = bruto*(1-ir)
    if r.custodia_td:
        TDC = val(C["tesouro"]["custodia_aa"], contexto="tdc")
        TDI = val(C["tesouro"]["isencao_selic"], contexto="tdi")
        base = max(0.0, patrimonio-TDI) if r.td_isento else patrimonio
        liq -= TDC*(base/patrimonio if patrimonio > 0 else 0.0)
    liq -= r.interno_aa
    return liq

def ganho_anual(r, C, dias_horizonte, saldo):
    """Reais por ano que a rota entrega sobre `saldo`. E a integral do retorno; e a
    forma honesta de somar duas rotas, porque somar percentuais de bases diferentes
    nao significa nada."""
    if saldo <= 0: return 0.0
    x = retorno_liquido_aa(r, C, dias_horizonte, saldo)
    return None if x is None else saldo*x


def segmentos_de_capacidade(r, C, dias_horizonte):
    """ACHADO O-01 (05/09/2026). O G2 ordenava as rotas pelo retorno MEDIO calculado
    no alvo inteiro, e depois mandava tudo para a primeira. Duas coisas estao erradas
    nisso, e a segunda so aparece quando existe teto:

    1. O retorno de alguns produtos DEPENDE DO SALDO. O Tesouro Selic e isento de
       custodia ate R$10.000 e paga 0,20% a.a. acima disso. Avaliar a rota inteira em
       R$36.000 mistura os dois trechos numa media que nao descreve nenhum real: os
       dez mil primeiros rendem mais do que a media diz, e os vinte e seis mil
       seguintes, menos.
    2. Com retorno dependente de saldo, ordenar por media e encher a primeira NAO da o
       melhor resultado. O criterio certo e o MARGINAL — quanto rende o PROXIMO real —
       e ele muda conforme a pilha cresce.

    Esta funcao devolve a rota fatiada em trechos de retorno marginal CONSTANTE. Para
    a estrutura de custo deste catalogo isso e exato, nao aproximado: o unico ponto de
    quebra e a isencao de custodia do Tesouro, e o resultado e uma escada.

    Devolve [(marginal_aa, capacidade_do_trecho)], em ordem decrescente de marginal.
    `capacidade` None = trecho sem teto declarado."""
    base = retorno_liquido_aa(r, C, dias_horizonte, 1.0)
    if base is None: return []
    teto = r.teto_de_saldo
    if not (r.custodia_td and r.td_isento):
        # sem quebra: o marginal e o proprio retorno, constante em qualquer saldo
        return [(_marginal_plano(r, C, dias_horizonte), teto)]
    TDC = val(C["tesouro"]["custodia_aa"], contexto="tdc")
    TDI = val(C["tesouro"]["isencao_selic"], contexto="tdi")
    m_baixo = _marginal_plano(r, C, dias_horizonte)          # sem custodia
    m_alto  = m_baixo - TDC                                  # com custodia
    if teto is not None and teto <= TDI:
        return [(m_baixo, teto)]
    return [(m_baixo, TDI), (m_alto, None if teto is None else teto - TDI)]


def _marginal_plano(r, C, dias_horizonte):
    """Retorno do proximo real ignorando a custodia do Tesouro (tratada a parte)."""
    if r.indexador == "cdi":        bruto = val(C["macro"]["cdi_aa"], contexto="cdi")
    elif r.indexador == "selic":    bruto = val(C["macro"]["selic_aa"], contexto="selic")
    elif r.indexador == "poupanca":
        bruto = (1+val(C["macro"]["poupanca_am"], contexto="poup"))**12 - 1
    else: return None
    fixa, motivo = regime_tributario(r)      # P-77: a mesma regra nos DOIS lugares
    if motivo: return None
    bruto *= r.rendimento_fator
    ir = fixa if fixa is not None else aliquota_ir_rf(C, dias_horizonte)
    return bruto*(1-ir) - r.interno_aa


def compor_reserva(rotas, C, P, alvo, ja_aplicado=None):
    """P-24. Distribui `alvo` entre as rotas de liquidez por retorno MARGINAL,
    respeitando o teto de saldo de cada uma.

    Por que composicao e nao rota unica: com teto, a pergunta "qual a melhor rota"
    nao tem resposta — a melhor rota comporta 28% do alvo. E mesmo SEM teto a
    pergunta ja era mal posta, porque o retorno depende do saldo (achado O-01).

    `ja_aplicado`: {rota_id: saldo}. Quando None, o motor NAO SABE onde a reserva
    esta — ver limitacoes_declaradas.reserva_e_um_numero_e_o_mundo_tem_baldes. Nesse
    caso ele compoe o alvo do zero, o que responde "para onde ir", nao "onde ja
    esta".

    Devolve dict com `tramos`, `nao_alocado` e `ganho_anual`."""
    ja = dict(ja_aplicado or {})
    dias = P["portoes"]["G2_reserva"]["horizonte_ir_dias"]
    escada = []
    for r in rotas:
        usado = ja.get(r.id, 0.0)
        for k, (marg, cap) in enumerate(segmentos_de_capacidade(r, C, dias)):
            if marg is None: continue
            # o saldo ja aplicado consome os trechos de baixo primeiro
            if cap is not None:
                come = min(usado, cap); cap -= come; usado -= come
                if cap <= 0: continue
            else:
                usado = 0.0
            escada.append(dict(rota=r, marginal_aa=marg, capacidade=cap, trecho=k))
    escada.sort(key=lambda t: -t["marginal_aa"])
    falta, tramos = alvo, []
    for t in escada:
        if falta <= 1e-9: break
        cabe = falta if t["capacidade"] is None else min(falta, t["capacidade"])
        if cabe <= 1e-9: continue
        tramos.append(dict(rota_id=t["rota"].id, nome=t["rota"].nome, valor=cabe,
                           marginal_aa=t["marginal_aa"], trecho=t["trecho"],
                           emissor=t["rota"].emissor,
                           teto_de_saldo=t["rota"].teto_de_saldo))
        falta -= cabe
    # tramos consecutivos da mesma rota (os dois lados da isencao) somam num so destino
    juntos = []
    for t in tramos:
        if juntos and juntos[-1]["rota_id"] == t["rota_id"]:
            juntos[-1]["valor"] += t["valor"]
            juntos[-1]["marginal_aa"] = min(juntos[-1]["marginal_aa"], t["marginal_aa"])
        else:
            juntos.append(dict(t))
    return dict(tramos=juntos, nao_alocado=max(0.0, falta),
                ganho_anual=sum(t["valor"]*t["marginal_aa"] for t in tramos))


# ══ PORTOES ══════════════════════════════════════════════════════════════════
@dataclass
class Diretiva:
    portao: str
    veredito: str
    destino: Optional[str] = None
    valor: Optional[float] = None
    memoria: dict = field(default_factory=dict)

@dataclass
class Pendencia:
    id: str
    pergunta: str
    consequencia: str
    bloqueia: str = ""

def g0_match_empregador(estado, rotas, C, P):
    """A unica rota que domina o pagamento de divida. Roda ANTES do G1.
    Retorna (diretiva, pendencia) — desconhecido nao e ausente."""
    g = P["portoes"]["G0_match_empregador"]
    if not g["ativo"]: return None, None
    if estado.match_empregador is None:
        if estado.match_verificado:
            return None, None                 # verificado e nao existe: silencio legitimo
        return None, Pendencia("G0_match", g["pergunta"], g["custo_de_ignorar"],
                               bloqueia="veredito_final")
    m = estado.match_empregador
    limite = m.teto_pct_salario * m.salario_bruto_mensal
    if limite <= 0 or m.taxa <= 0: return None, None
    valor = min(estado.aporte_mensal, limite)
    return Diretiva("G0_match_empregador",
        f"OS PRIMEIROS R${valor:,.2f} DO APORTE VAO PARA A PREVIDENCIA COM MATCH".replace(",", "."),
        destino="previdencia_com_match", valor=valor,
        memoria=dict(taxa_match=m.taxa, retorno_imediato=m.taxa, limite_casado=limite,
                     sobra_para_os_demais_portoes=max(0.0, estado.aporte_mensal-valor),
                     nota="retorno certo de {:.0%} em um unico mes. Nenhuma divida de "
                          "cartao chega perto — por isso este portao vem antes do G1"
                          .format(m.taxa))), None

def rotas_de_liquidez(rotas, P):
    """As rotas que podem sustentar a reserva de emergencia.

    `conta_como_liquidez: false` na funcao e uma exclusao explicita: um NTN-B carregado
    ate o vencimento nao vira dinheiro amanha sem realizar a marcacao a mercado, e a
    reserva existe justamente para nunca precisar disso. Sem esta leitura, bastaria uma
    rota declarar LIQUIDEZ entre suas funcoes para entrar no calculo da reserva."""
    out = []
    for r in rotas:
        if not r.confiavel or "LIQUIDEZ" not in r.funcoes: continue
        if any(P["funcoes"][f].get("conta_como_liquidez") is False for f in r.funcoes):
            continue
        out.append(r)
    return out

def g1_divida(estado, rotas, C, P):
    """A-05: liquido contra liquido."""
    g = P["portoes"]["G1_divida"]
    if not g["ativo"] or not estado.dividas: return None
    dias = g["horizonte_ir_dias"]
    liq = rotas_de_liquidez(rotas, P)
    cand = [(r, retorno_liquido_aa(r, C, dias, estado.reserva_atual)) for r in liq]
    cand = [(r, x) for r, x in cand if x is not None]
    melhor_r, melhor_aa = max(cand, key=lambda t: t[1])
    melhor_am = (1+melhor_aa)**(1/12)-1
    bruto_aa = val(C["macro"]["cdi_aa"], contexto="cdi")
    pior = max(estado.dividas, key=lambda d: d.taxa_am)
    if pior.taxa_am > melhor_am + g["tolerancia_pp_am"]:
        return Diretiva("G1_divida", "TODO O APORTE PARA A DIVIDA",
            destino=pior.nome, valor=estado.aporte_mensal,
            memoria=dict(divida_am=pior.taxa_am, melhor_investimento_am=melhor_am,
                         melhor_rota=melhor_r.nome, aliquota_ir=aliquota_ir_rf(C, dias),
                         bruto_am_referencia=(1+bruto_aa)**(1/12)-1,
                         ganho_certo_am=pior.taxa_am-melhor_am, saldo=pior.saldo,
                         nota="comparacao liquido contra liquido: a divida nao gera "
                              "rendimento tributavel, o investimento gera. Usar o bruto "
                              "deixava passar divida entre 0,84% e 1,09% ao mes"))
    return None

def meses_de_reserva_alvo(estado, P):
    """A meta da reserva em MESES: G2 x estabilidade + dependentes, limitada ao teto."""
    g = P["portoes"]["G2_reserva"]
    meses = g["meses_base"] * g["ajuste_estabilidade"][estado.estabilidade_renda]
    meses += g["ajuste_dependentes_por_pessoa"] * estado.dependentes
    return min(meses, g["teto_meses"])

def reserva_alvo(estado, P):
    return meses_de_reserva_alvo(estado, P) * estado.despesa_mensal

def pendencias_de_premissa(estado, P, carregos):
    """Registro assinado que cita a meta da reserva e ja nao bate com ela.

    Decisao dele (26/09/2026): o C03 do td_ipca fica com "9 meses" fixo, e o sistema avisa
    se a meta deixar de ser 9. A meta nao e um campo do perfil: sai do G2 do politica.yaml,
    da estabilidade (EST01 do perfil.yaml) e dos dependentes do estado -- por isso a
    comparacao usa a mesma conta do G2, e nao um numero copiado."""
    meta = meses_de_reserva_alvo(estado, P)
    out = []
    for aid, reg in sorted((carregos or {}).items()):
        if not reg.get("valida"):
            continue
        n = meses_de_reserva_no_texto(reg.get("carrego") or {})
        if n is None or abs(n - meta) < 1e-9:
            continue
        out.append(Pendencia(
            f"reassinar:{aid}",
            f"tese {aid} desatualizada, reassinar? O C03 foi assinado com reserva de "
            f"emergencia de {n} meses; a meta vigente e {meta:g} meses.",
            "A condicao de venda antecipada cita um numero que o sistema ja nao usa. Para "
            "mudar o texto, mova o registro para `historico` e assine outro.",
            bloqueia=""))
    return out

def g2_reserva(estado, rotas, C, P):
    """B-08: escolhe por retorno liquido e verifica o teto do FGC por conglomerado.
    P-24: devolve uma COMPOSICAO, nao uma rota unica.

    Por que o contrato mudou. Ate 05/09/2026 o portao avaliava cada rota no ALVO
    INTEIRO, ordenava pela media e mandava 100% do aporte para a primeira, para
    sempre. Isso falha de duas maneiras distintas:

      teto de saldo  o Cofrinho Turbinado aceita R$10.000 e o alvo e R$36.000. O
                     portao recomendaria um destino que, a partir do mes ~20, RECUSA
                     o deposito — e continuaria recomendando (achado K-02).
      retorno que    o Tesouro Selic e isento de custodia ate R$10.000. Avaliado em
      depende do     R$36.000 ele parece pior que o RDB; avaliado no primeiro real,
      saldo          e melhor. A media nao descreve nenhum dos dois trechos, e
                     escolher por ela custa dinheiro e concentra credito (achado
                     O-01).

    A composicao resolve os dois com o mesmo criterio: enche por retorno MARGINAL,
    respeitando o teto de cada rota."""
    g = P["portoes"]["G2_reserva"]
    if not g["ativo"]: return None
    alvo = reserva_alvo(estado, P)
    if estado.reserva_atual >= alvo: return None
    crit = g["criterio_escolha_rota"]
    if crit == "retorno_liquido":
        raise ValueError(
            "criterio_escolha_rota: 'retorno_liquido' foi APOSENTADO pelo achado O-01. "
            "Ele significava avaliar cada rota no alvo inteiro, ordenar pela media e "
            "mandar tudo para a primeira — e a media no alvo inteiro nao descreve nenhum "
            "real quando o retorno depende do saldo. Use 'retorno_liquido_marginal'. "
            "Nao aceitamos o valor antigo em silencio porque ele nomeia um comportamento "
            "diferente do que o motor faz hoje.")
    if crit != "retorno_liquido_marginal":
        raise ValueError(f"criterio_escolha_rota desconhecido: {crit}")
    if g["devolve"] != "COMPOSICAO":
        raise ValueError(f"G2_reserva.devolve desconhecido: {g['devolve']}")
    liq = [r for r in rotas if "LIQUIDEZ" in r.funcoes and r.confiavel]
    dias = g["horizonte_ir_dias"]
    ranking = sorted(((r, retorno_liquido_aa(r, C, dias, alvo)) for r in liq),
                     key=lambda t: -(t[1] if t[1] is not None else -math.inf))
    excl = g["exclusividade"]
    if not 0 < excl <= 1:
        raise ValueError(f"G2_reserva.exclusividade fora de (0,1]: {excl}")

    comp = compor_reserva(liq, C, P, alvo, estado.reserva_por_rota)
    alertas = []
    if not comp["tramos"]:
        raise InsumoBloqueado("nenhuma rota de liquidez confiavel comporta a reserva")
    if comp["nao_alocado"] > 0.01:
        alertas.append(
            f"os tetos das rotas de liquidez confiaveis somam menos que o alvo: sobram "
            f"R${comp['nao_alocado']:,.2f} SEM DESTINO. Nao e um detalhe de execucao — "
            f"a reserva-alvo nao cabe no que o catalogo tem hoje.".replace(",", "."))
    if estado.reserva_por_rota is None and estado.reserva_atual > 0:
        alertas.append(
            "a reserva existente e um numero unico: o motor NAO SABE em quais rotas ela "
            "esta. A composicao abaixo e o plano do alvo inteiro; para saber se a "
            "proxima parcela cabe, informe `reserva_por_rota`.")
    if estado.reserva_conferida is False:
        alertas.append(
            f"`reserva_por_rota` soma R${sum(estado.reserva_por_rota.values()):,.2f} e "
            f"`reserva_atual` diz R${estado.reserva_atual:,.2f}. O motor nao escolhe "
            f"entre os dois.".replace(",", "."))

    # FGC: por CONGLOMERADO, e sobre o que cada emissor recebe na composicao — nao
    # sobre o alvo inteiro. Compor ja reduz a exposicao; o alerta tem de refletir isso.
    if P["tetos"]["por_conglomerado"]:
        teto_fgc = P["tetos"]["por_emissor_credito_privado"]
        por_emissor = {}
        for t in comp["tramos"]:
            if t["emissor"] and t["emissor"] != "TESOURO_NACIONAL":
                por_emissor[t["emissor"]] = por_emissor.get(t["emissor"], 0.0) + t["valor"]
        for em, v in sorted(por_emissor.items()):
            if v > teto_fgc:
                n = math.ceil(v/teto_fgc)
                alertas.append(
                    f"a composicao poe R${v:,.2f} em {em}, acima do limite do FGC "
                    f"(R${teto_fgc:,.2f} POR CONGLOMERADO, nao por marca): exige {n} "
                    f"emissores distintos, ou o Tesouro, que nao tem FGC porque nao "
                    f"precisa".replace(",", "."))

    primeiro = comp["tramos"][0]
    melhor = next(r for r in liq if r.id == primeiro["rota_id"])
    melhor_aa = retorno_liquido_aa(melhor, C, dias, primeiro["valor"])
    valor = estado.aporte_mensal*excl
    n_rotas = len(comp["tramos"])
    veredito = ("TODO O APORTE PARA A RESERVA" if excl >= 1.0 else
                f"{excl*100:.0f}% DO APORTE PARA A RESERVA, "
                f"{(1-excl)*100:.0f}% SEGUE PARA A ALOCACAO")
    if n_rotas > 1:
        veredito += f" — EM {n_rotas} ROTAS, na ordem da composicao"
    return Diretiva("G2_reserva", veredito,
        destino=melhor.nome, valor=valor,
        memoria=dict(alvo=alvo, atual=estado.reserva_atual, falta=alvo-estado.reserva_atual,
                     exclusividade=excl, aporte_liberado=estado.aporte_mensal-valor,
                     meses_alvo=alvo/estado.despesa_mensal, meses_atual=estado.meses_cobertos,
                     retorno_liquido_aa=melhor_aa,
                     composicao=comp["tramos"], nao_alocado=comp["nao_alocado"],
                     ganho_anual_da_composicao=comp["ganho_anual"],
                     ranking=[(r.id, round(x,5) if x is not None else None) for r, x in ranking],
                     alertas=alertas,
                     meses_para_completar=math.ceil((alvo-estado.reserva_atual)/valor)
                        if valor else None))

def g3_atrito(rotas, C, P, aporte):
    """A-02: elegibilidade por custo de entrada, com o motivo separado por natureza."""
    g = P["portoes"]["G3_atrito"]
    B3V = val(C["b3"]["vista_total_pct"], contexto="b3")
    teto = g["teto_custo_entrada_pct"]
    # E-03: desligar suspende a ELIMINACAO, nunca o CALCULO. `dentro` e lista de PARES
    # (rota, e) e o G4 consome o `e` -- devolver `rotas` cru entregaria rota nua onde o
    # resto espera par. Desligado: calcula `e` de todas e nao elimina ninguem.
    ligado = g["ativo"]
    dentro, fora = [], []
    for r in rotas:
        fixo = custo_entrada_fixo_pct(r, aporte)
        pct  = custo_entrada_percentual(r, B3V)
        e = fixo + pct
        if e <= teto or not ligado:
            dentro.append((r, e))
        else:
            if pct >= teto:
                motivo = "PERCENTUAL"
                reentrada = None
            else:
                motivo = "FIXO"
                reentrada = r.corr_fix/(teto-pct) if r.corr_fix else None
            fora.append((r, e, motivo, reentrada))
    return dentro, fora

def g4_dominancia(pares, C, aporte, P, anos, memo=None):
    """Dominancia verdadeira: perde em TODOS os horizontes de teste.

    Devolve (vivos, dominados, preferencia). Duas categorias, porque sao duas coisas:

      DOMINADA     perde em todos os horizontes. E logica: nenhuma escolha de horizonte
                   a salva. BOVA11 via corretora que cobra 0,50% na entrada e na saida
                   perde do BOVA11 de corretagem zero sempre.
      PREFERENCIA  a ordem INVERTE com o horizonte. IVVB11 (adm 0,23% a.a.) bate a
                   Avenue (1,60% por aporte) ate 10 anos e perde dela a partir de 15,
                   porque custo por aporte dilui no tempo e taxa anual nao. Aqui o
                   portao NAO tem autoridade logica, e o que ele faz vem de
                   `desempate_preferencia_horizonte`, declarado no YAML."""
    g = P["portoes"]["G4_dominancia"]
    # E-03: desligar suspende a ELIMINACAO, nunca o CALCULO. `vivos` e lista de QUADRAS
    # (rota, e, arrasto_no_horizonte, motivo) e quem vem depois consome o arrasto --
    # devolver os pares crus quebraria o contrato de tupla de todo mundo que le a saida.
    if not g["ativo"]:
        _m = {} if memo is None else memo
        return ([(r, e, arrasto_anualizado(r, C, aporte, anos, _m), None) for r, e in pares],
                [], [])
    modo = g["desempate_preferencia_horizonte"]
    if modo not in ("menor_arrasto_no_horizonte", "ambas", "usuario"):
        raise ValueError(f"desempate_preferencia_horizonte desconhecido: {modo}")
    hs = sorted(set(list(g["horizontes_teste"]) + [anos]))
    # S-02: o memo tem DONO. Ele vem de quem chama, que e quem sabe ate onde o `C`
    # e o mesmo. Um default `{}` aqui tambem seria correto — so nao aproveitaria
    # entre os portoes da mesma passada, que e onde estao 72 das chamadas.
    _memo = {} if memo is None else memo
    arr = {(r.id, h): arrasto_anualizado(r, C, aporte, h, _memo) for r, _ in pares for h in hs}
    vivos, dominados, preferencia = [], [], []
    for r, e in pares:
        rivais = [o for o, _ in pares if o.exposicao == r.exposicao and o.id != r.id]
        dom = [o for o in rivais
               if all(arr[(o.id, h)] < arr[(r.id, h)] - 1e-12 for h in hs)]
        if dom:
            dominados.append((r, e, arr[(r.id, anos)], dom[0]))
            continue
        pref = [o for o in rivais if arr[(o.id, anos)] < arr[(r.id, anos)] - 1e-12]
        if pref:
            tabela = {h: {r.id: arr[(r.id,h)], pref[0].id: arr[(pref[0].id,h)]} for h in hs}
            preferencia.append((r, e, arr[(r.id, anos)], pref[0], tabela, modo))
            if modo == "menor_arrasto_no_horizonte":
                continue                          # sai do universo — mas rotulada
            if modo == "usuario":
                continue                          # nenhuma das duas recebe peso
        vivos.append((r, e, arr[(r.id, anos)], None))
    if modo == "usuario" and preferencia:
        # nem a vencedora entra: a decisao e do usuario, e nao ha default silencioso
        perdedoras = {x[0].id for x in preferencia}
        vencedoras = {x[3].id for x in preferencia}
        vivos = [v for v in vivos if v[0].id not in vencedoras | perdedoras]
    return vivos, dominados, preferencia

def interacao_g3_g4(fora_atrito, vivos, C, aporte, P, anos, memo=None):
    """V-02: o G3 roda antes do G4, entao rota de custo percentual alto e eliminada por
    atrito e nunca chega a dominancia. Os dois portoes em sequencia produzem um
    resultado que nenhum dos dois produziria sozinho.

    A ordem nao muda (a decisao esta declarada em decisoes.V01_desempate_de_horizonte),
    mas a interacao deixa de ser silenciosa: esta funcao reporta toda rota barrada por
    atrito que VENCERIA a sobrevivente de mesma exposicao em algum horizonte testado."""
    hs = sorted(set(list(P["portoes"]["G4_dominancia"]["horizontes_teste"]) + [anos]))
    _memo = {} if memo is None else memo      # S-02: o memo tem dono
    out = []
    for item in fora_atrito:
        r = item[0]
        rivais = [v for v in vivos if v.exposicao == r.exposicao]
        if not rivais: continue
        for riv in rivais:
            try:
                ganha = [h for h in hs
                         if arrasto_anualizado(r, C, aporte, h, _memo) <
                            arrasto_anualizado(riv, C, aporte, h, _memo) - 1e-12]
            except AporteConsumidoPelaEntrada:
                # P-134: rota cuja entrada come o aporte nao vence ninguem. Antes ela
                # entrava aqui como NaN (aporte R$ 0: inf*0 dentro do `min`) ou como numero
                # falso -- e NaN < x e falso, entao a resposta saia certa por acidente.
                continue
            if ganha:
                out.append(dict(rota=r, rival=riv, horizontes_em_que_venceria=ganha,
                    nota=f"{r.nome} foi eliminada pelo G3 (atrito) e venceria "
                         f"{riv.nome} no G4 em {ganha} anos. Os dois portoes em "
                         f"sequencia produzem um resultado que nenhum produziria "
                         f"sozinho — isto e conhecido e aceito, nao um defeito oculto"))
    return out

def g5_status(itens, P=None):
    """Aceita tanto rotas nuas quanto pares (rota, custo).

    F-02: passou a rodar ANTES do G3, quando os itens ainda sao rotas nuas — o
    custo so pode ser comparado depois que o status foi verificado. Continua
    aceitando pares para nao quebrar quem o chama isolado.
    """
    if P is not None and not P["portoes"]["G5_status"]["ativo"]:
        return itens, []
    rota = lambda x: x[0] if isinstance(x, tuple) else x
    return ([x for x in itens if rota(x).confiavel],
            [x for x in itens if not rota(x).confiavel])

def g6_coerencia_funcao(rotas, P):
    """A-03: as exigencias declaradas na funcao passam a ser verificadas.
    Devolve (rotas_ok, incoerencias). Uma rota incoerente perde a FUNCAO, nao o catalogo."""
    g = P["portoes"]["G6_coerencia_funcao"]
    if not g["ativo"]: return rotas, []
    ordem = g["ordem_perda"]
    ok, ruins = [], []
    for r in rotas:
        mantidas = []
        for f in r.funcoes:
            spec = P["funcoes"][f]
            lim_d = spec.get("exige_liquidez_dias")
            lim_p = spec.get("exige_perda_maxima")
            falhas = []
            if lim_d is not None and lim_d is not False and r.liquidez_dias > lim_d:
                # P-12 (12a): a funcao que aceita vencimento casado no lugar da liquidez
                # nao reprova aqui a rota que TEM vencimento conhecido -- o G6 nao sabe o
                # prazo do objetivo, e quem casa e o `casa_duracao`, na alocacao.
                if not (spec.get("liquidez_ou_vencimento_casado")
                        and r.vencimento_anos is not None):
                    falhas.append(f"resgate em {r.liquidez_dias}d > exige_liquidez_dias={lim_d}")
            if lim_p is not None and ordem.index(r.perda_maxima) > ordem.index(lim_p):
                falhas.append(f"perda_maxima={r.perda_maxima} pior que exige_perda_maxima={lim_p}")
            if falhas: ruins.append((r, f, falhas))
            else:      mantidas.append(f)
        if mantidas:
            # V-12: copia, nao mutacao. `cenarios.py` mantem um ROTAS de outra chamada
            # de catalogo(); mutar aqui fazia as rotas nomeadas no output nao serem as
            # que o pipeline filtrou.
            ok.append(replace(r, funcoes=mantidas))
        else:
            ruins.append((r, "TODAS", ["nenhuma funcao declarada e satisfeita"]))
    return ok, ruins

def g7_tese_registrada(pares, P, teses):
    """Bloco K do escopo de campos. Sem tese datada e falsificavel, a posicao nao e
    especulacao — e esperanca sem prazo. Devolve (com_tese, sem_tese)."""
    g = P["portoes"]["G7_tese_registrada"]
    if not g["ativo"]: return pares, []
    com, sem = [], []
    for p in pares:
        r = p[0]
        exige = any(P["funcoes"][f].get("exige_tese_registrada") for f in r.funcoes)
        if not exige: com.append(p); continue
        t = (teses or {}).get(r.id)
        if t and t.get("valida"): com.append(p)
        else: sem.append((r, (t or {}).get("motivo", "nenhuma tese registrada para esta rota")))
    return com, sem

MOTIVO_REGRA_DECIDIDA = ("REGRA_DECIDIDA: as regras estao seladas, a posicao nao existe; "
                         "libera no dia da compra, quando o registro virar COMPROMISSO_ATIVO")


def _estado_do_carrego(c):
    """O estado do registro validado. Ausente vale COMPROMISSO_ATIVO -- o mesmo default de
    `tese.validar_carrego`, para que o portao e o validador nao possam discordar."""
    return (c.get("carrego") or {}).get("estado", "COMPROMISSO_ATIVO")


def g8_compromisso_de_carrego(pares, P, carregos):
    """Gemeo do G7, para o outro modo de falha: quebra de compromisso.

    Devolve (com_compromisso, sem_compromisso). A rota que passa recebe a DURACAO
    declarada no registro — e so entao pode ser dimensionada."""
    g = P["portoes"]["G8_compromisso_de_carrego"]
    if not g["ativo"]: return pares, []
    com, sem = [], []
    for p in pares:
        r = p[0]
        exige = any(P["funcoes"][f].get("exige_compromisso_de_carrego") for f in r.funcoes)
        if not exige: com.append(p); continue
        c = (carregos or {}).get(r.id)
        # G-07: REGRA_DECIDIDA sela as regras, mas a posicao nao existe -- o validador
        # anuncia que o G8 nao libera peso neste estado, e o portao tem de honrar isso.
        if c and c["valida"] and _estado_do_carrego(c) == "REGRA_DECIDIDA":
            sem.append((r, MOTIVO_REGRA_DECIDIDA))
        elif c and c["valida"] and c["duracao_anos"] is not None:
            r2 = replace(r, duracao_anos=c["duracao_anos"])
            com.append((r2,) + tuple(p[1:]))
        else:
            sem.append((r, (c or {}).get("motivo", "nenhum compromisso de carrego registrado")))
    return com, sem

def vencimento_maximo(P, hoje=None):
    """A data-limite que o teto de compromissos impoe. Vai para a PENDENCIA, porque
    'preencha o registro' sem dizer ate quando nao e instrucao."""
    hoje = hoje or dt.date.today()
    return hoje + dt.timedelta(days=int(P["compromissos"]["maximo_anos"]*365.25))

# ══ ALOCACAO ═════════════════════════════════════════════════════════════════
def fracao_rv(estado, P):
    c = P["crescimento"]
    if c["metodo"] != "capacidade_de_suportar_queda":
        raise ValueError(f"metodo de crescimento nao implementado: {c['metodo']}")
    f  = c["base_rv"]
    f += ((estado.meses_cobertos - P["portoes"]["G2_reserva"]["meses_base"])
          * c["ajuste_meses_reserva"]["por_mes_extra"])
    f += c["ajuste_estabilidade"][estado.estabilidade_renda]
    f += ((estado.horizonte_anos - c["ajuste_horizonte"]["base_anos"])
          * c["ajuste_horizonte"]["por_ano_extra"])
    return max(c["piso_rv"], min(c["teto_rv"], f))

def necessidade_datada(estado, P):
    """A-04: quanto do bloco conservador esta comprometido com objetivo DATADO.
    Sem objetivo, e zero — e o bloco DATADO fica vazio, como a funcao manda.
    Devolve (fracao, objetivos, alertas)."""
    if not P["funcoes"]["DATADO"].get("exige_objetivo"): return 1.0, [], []
    if not estado.objetivos: return 0.0, [], []
    prazo_max = max(o.prazo_anos for o in estado.objetivos)
    base = estado.patrimonio_investido + estado.aporte_mensal*12*prazo_max
    total = sum(o.valor for o in estado.objetivos)
    al = []
    if base > 0 and total > base:      # V-08: nao silenciar meta inalcancavel
        falta = total - base
        preciso = total/(12*prazo_max) if prazo_max else float("inf")
        al.append(f"objetivos datados somam R${total:,.0f} e o aporte atual acumula "
                  f"R${base:,.0f} no prazo: faltam R${falta:,.0f}. Seria preciso aportar "
                  f"R${preciso:,.0f}/mes, ou alongar o prazo. O sistema alocou 100% do "
                  f"bloco conservador ao objetivo — o que NAO o torna alcancavel"
                  .replace(",", "."))
    return (min(1.0, total/base) if base > 0 else 0.0), estado.objetivos, al

def casa_duracao(r, objetivos, P):
    """funcoes.DATADO.regra: duracao_do_instrumento <= prazo_do_objetivo.

    V-07: contra o MENOR prazo entre os objetivos que o bloco financia, nao contra
    qualquer um. Com `any`, um objetivo de 20 anos admitia um papel de duracao 18 no
    bloco — e o bloco era dimensionado pela necessidade TOTAL, que inclui o objetivo
    de 1 ano. O bloco era agregado e o casamento era isolado."""
    regra = P["funcoes"]["DATADO"]["regra"]
    if regra != "duracao_do_instrumento <= prazo_do_objetivo":
        raise ValueError(f"regra de DATADO nao implementada: {regra}")
    if not objetivos or r.duracao_anos is None: return False
    prazo = min(o.prazo_anos for o in objetivos)
    spec = P["funcoes"]["DATADO"]
    lim_d = spec.get("exige_liquidez_dias")
    if lim_d is not None and r.liquidez_dias > lim_d:
        # P-12 (12a): iliquida so casa se VENCE ate o objetivo -- o mesmo menor prazo do
        # V-07. Sem vencimento conhecido, nao casa: insumo ausente nao vira casamento.
        if not spec.get("liquidez_ou_vencimento_casado") or r.vencimento_anos is None:
            return False
        if r.vencimento_anos > prazo + 1e-9:
            return False
    return r.duracao_anos <= prazo + 1e-9

def ordem_dos_portoes(P, fase=None):
    """A sequencia vem do YAML (P-07). Ate 05/09/2026 ela vivia no corpo de `alocar`.

    O F-02 provou que a ordem e regra com consequencia material, e o I-01 mostrou que
    a ordem real nunca foi G0..G8: e G6, G0, G1, G2, G5, G3, G7, G8, G4. Enquanto isso
    estava no codigo, trocar a sequencia era deploy; agora e commit no politica.yaml.

    Portao sem `ordem` declarada e erro duro, nao padrao silencioso — inventar uma
    posicao para ele seria escolher a regra em vez de le-la.
    """
    itens = []
    for nome, spec in P["portoes"].items():
        if "ordem" not in spec:
            raise ValueError(f"portao {nome} sem `ordem` declarada em politica.yaml")
        if fase and spec.get("fase") != fase:
            continue
        itens.append((spec["ordem"], nome, spec))
    return [(n, sp) for _o, n, sp in sorted(itens)]


# ══ PIPELINE ════════════════════════════════════════════════════════════════
# P-37. `alocar()` tinha 300 linhas e orquestrava nove portoes. A mediana das
# funcoes deste projeto e 8 linhas — o corpo e pequeno e legivel, e a cauda nao era.
#
# POR QUE ISSO ERA UM DEFEITO E NAO UMA QUESTAO DE GOSTO:
#   Uma funcao de 300 linhas so se testa PELO RESULTADO FINAL. Nao da para perguntar
#   "a fase de universo devolveu o que devia?" sem rodar a alocacao inteira, e um
#   erro numa etapa intermediaria so aparece se por acaso mover um peso. Foi assim
#   que o achado I-01 sobreviveu semanas: a ordem real dos portoes nunca foi G0->G8,
#   e nenhum teste conseguia olhar so para a sequencia.
#
# A QUEBRA SEGUE AS FASES QUE JA EXISTIAM NO YAML, e nao um criterio novo:
#   _preparar             insumos, registros, catalogo, esqueleto da saida
#   fase_aporte           G6, G0, G1, G2 — decide QUANTO segue; pode encerrar
#   fase_universo         G5, G3, G7, G8, G4 — decide QUAIS rotas seguem
#   _pendencias_de_registro   G7/G8 sem registro viram pergunta, nao rejeicao
#   distribuir_por_funcao alocacao 1/N por bloco, tetos, sobra
#   _conferir_saida       invariantes e avisos de coerencia
#
# GARANTIA DESTA MUDANCA: 38 cenarios de estado foram serializados campo a campo
# ANTES da quebra — pesos, cada string de alerta, cada pendencia, cada rota em cada
# lista de rejeicao — e comparados depois. Zero diferencas. Refatorar sem essa rede
# e reescrever e torcer.

def _preparar(estado, C, P, anos, teses, carregos):
    """Insumos e esqueleto. Separado porque e a unica parte que TOCA O MUNDO —
    le registros do disco e a data de hoje. Isolar impuro de puro e o que torna o
    resto testavel sem preparar arquivo nenhum."""
    anos = anos or estado.horizonte_anos
    teto_comp = P["compromissos"]["maximo_anos"]
    if teses is None or carregos is None:
        _t, _c = carregar_registros(compromisso_maximo_anos=teto_comp)
        teses = _t if teses is None else teses
        carregos = _c if carregos is None else carregos
    saida = dict(estado=estado, portoes=[], pendencias=[], universo=None, alvo=None,
                 procedencia=dict(politica_versao=P["meta"]["versao"],
                                  politica_hash=P.get("_hash"),
                                  custos_hash=hash_custos(),
                                  gerado_em=dt.date.today().isoformat()))
    return anos, teto_comp, teses, carregos, catalogo(C), saida


def fase_aporte(estado, rotas, C, P, saida):
    """G6, G0, G1, G2. Decide QUANTO dinheiro segue, e pode encerrar o pipeline.

    Devolve (estado, rotas, encerrou). `estado` pode voltar com aporte MENOR: o G0
    e o G2 consomem parte dele. `encerrou` True significa que a diretiva ja esta em
    `saida` e nao ha alocacao a fazer — nao e erro, e a resposta.

    Por que G6 mora aqui apesar de ser da fase `universo` no YAML: ele e ordem 1 e
    e PRE-CONDICAO DO CATALOGO — uma rota so pode ocupar funcao cujas exigencias ela
    satisfaz, e isso vale antes de qualquer decisao sobre o aporte. O laco da fase
    `universo` o pula explicitamente, e um teste guarda essa duplicidade."""
    rotas, incoerentes = g6_coerencia_funcao(rotas, P)
    saida["incoerencias_de_funcao"] = incoerentes

    # G0 — antes do G1, e a pendencia sobrevive a qualquer diretiva
    d0, pend = g0_match_empregador(estado, rotas, C, P)
    if pend: saida["pendencias"].append(pend)
    if d0:
        saida["portoes"].append(d0)
        estado = Estado(**{**estado.__dict__,
                           "aporte_mensal": d0.memoria["sobra_para_os_demais_portoes"]})
        if estado.aporte_mensal <= 0:
            saida["diretiva"] = d0
            return estado, rotas, True

    d = g1_divida(estado, rotas, C, P)
    if d:
        saida["portoes"].append(d); saida["diretiva"] = d
        return estado, rotas, True

    d = g2_reserva(estado, rotas, C, P)
    if d:
        saida["portoes"].append(d)
        liberado = d.memoria.get("aporte_liberado", 0.0)
        if liberado <= 0:                 # exclusividade = 1.0, a regra atual
            saida["diretiva"] = d
            return estado, rotas, True
        # exclusividade < 1: a reserva leva sua fatia e o resto segue para a alocacao.
        # A decisao RES01 mediu que isto NAO cria patrimonio enquanto as duas pontas
        # rendem igual — o parametro existe para que a escolha seja declarada e
        # testavel, nao porque o split seja recomendado.
        estado = Estado(**{**estado.__dict__, "aporte_mensal": liberado})
    return estado, rotas, False


# ── Tabela de execucao da fase `universo` ────────────────────────────────────
# P-37. Isto era uma cadeia de `elif nome == ...` dentro de uma funcao de 300 linhas,
# e a consequencia nao era estetica: a LISTA DE PORTOES IMPLEMENTADOS so existia
# escondida naqueles ramos. Duas validacoes precisavam dela — "este portao existe?" e
# "esta ordem e executavel?" — e nenhuma das duas podia enxerga-la.
#
# Cada adaptador recebe (dentro, ctx) e devolve o novo `dentro`, registrando o que
# rejeitou em `ctx`. A assinatura uniforme e o que permite iterar a ordem do YAML sem
# saber qual portao vem.
def _exec_g5(dentro, ctx):
    dentro, ctx["rejeitados"]["fora_status"] = g5_status(dentro, ctx["P"])
    return dentro

def _exec_g3(dentro, ctx):
    dentro, ctx["rejeitados"]["fora_atrito"] = g3_atrito(
        dentro, ctx["C"], ctx["P"], ctx["estado"].aporte_mensal)
    return dentro

def _exec_g7(dentro, ctx):
    dentro, ctx["rejeitados"]["sem_tese"] = g7_tese_registrada(
        dentro, ctx["P"], ctx["teses"])
    return dentro

def _exec_g8(dentro, ctx):
    dentro, ctx["rejeitados"]["sem_carrego"] = g8_compromisso_de_carrego(
        dentro, ctx["P"], ctx["carregos"])
    return dentro

def _exec_g4(dentro, ctx):
    dentro, ctx["dominados"], ctx["preferencia"] = g4_dominancia(
        dentro, ctx["C"], ctx["estado"].aporte_mensal, ctx["P"], ctx["anos"],
        ctx["memo_arrasto"])
    return dentro

def _exec_g6(dentro, ctx):
    """Nao faz nada AQUI de proposito: o G6 e ordem 1 no YAML e roda na fase `aporte`,
    porque e pre-condicao do catalogo. Aparece nesta tabela para que ele conte como
    IMPLEMENTADO — sem esta linha, a validacao o acusaria de declarado e sem execucao,
    que e falso. Pular em silencio dentro do laco escondia essa distincao."""
    return dentro

PORTOES_DO_UNIVERSO = {
    "G6_coerencia_funcao":       _exec_g6,
    "G5_status":                 _exec_g5,
    "G3_atrito":                 _exec_g3,
    "G7_tese_registrada":        _exec_g7,
    "G8_compromisso_de_carrego": _exec_g8,
    "G4_dominancia":             _exec_g4,
}


def conferir_execucao_do_universo(P):
    """P2 ao contrario: declarar sem implementar. Roda ANTES do contrato de forma —
    um portao que nem existe no motor tem um problema mais basico que a ordem dele."""
    for nome, _spec in ordem_dos_portoes(P, fase="universo"):
        if nome not in PORTOES_DO_UNIVERSO:
            raise ValueError(f"portao {nome} declarado na fase universo e sem execucao "
                             f"no motor — declarar sem implementar e o erro da P2")


def conferir_ordem_do_universo(P):
    """ACHADO R-01 (05/09/2026). A P-07 declarou a ordem dos portoes como DADO e
    afirmou que troca-la e um commit no YAML. Isso e falso para 102 das 120 ordens
    possiveis — so 18 rodam.

    A causa: os portoes mudam a FORMA do que trafega. O G3 e o unico que transforma
    (entra rota, sai `(rota, custo)`), e o G4, o G7 e o G8 consomem pares. Uma ordem
    que ponha qualquer um deles antes do G3 estoura la dentro, com um `TypeError:
    cannot unpack non-iterable RotaAloc object` disparado no fundo de uma funcao de
    portao — nunca com uma mensagem que diga que a ORDEM e que esta errada.

    Declarar a ordem como dado sem declarar o CONTRATO e declarar uma liberdade que
    nao existe. E a mesma familia do F-05 e do N-01: o arquivo promete um
    comportamento que o codigo nao tem.

    Esta funcao le `consome`/`produz` do YAML e recusa a ordem invalida ANTES de
    rodar, dizendo qual par de portoes esta trocado. Ela nao conserta a dependencia —
    a dependencia e real e legitima. Ela a torna VISIVEL e o erro, legivel.

    O QUADRO COMPLETO das 120 ordens, medido:
      18   rodam.
      90   recusadas AQUI, com a mensagem dizendo que a ordem e o problema.
      12   levantam InsumoBloqueado, e isso NAO e defeito: sao as ordens que poem o
           G5_status depois de um portao que calcula custo, e ai uma rota bloqueada
           chega a uma conta. E o guarda do F-02 funcionando, e a mensagem dele ja
           nomeia a rota e a constante. Nao foi "consertado" de proposito: transformar
           isso num erro de ordem esconderia que a causa e outra.

    Ou seja: das 102 ordens que nao rodam, 90 agora dizem por que, e 12 ja diziam."""
    produzido = "rotas"
    for nome, spec in ordem_dos_portoes(P, fase="universo"):
        if nome == "G6_coerencia_funcao":
            continue
        consome = spec.get("consome")
        produz = spec.get("produz")
        if consome is None or produz is None:
            raise ValueError(
                f"{nome} nao declara `consome`/`produz`. Sem o contrato de forma nao "
                f"da para saber se a ordem do YAML e executavel (achado R-01).")
        if consome == "pares" and produzido != "pares":
            anterior = [n for n, _ in ordem_dos_portoes(P, fase="universo")]
            raise ValueError(
                f"ordem invalida: {nome} consome pares (rota, custo) e nada antes dele "
                f"produziu pares. O unico portao que produz pares e o G3_atrito, e na "
                f"ordem declarada ele vem depois. Ordem atual: {' -> '.join(anterior)}")
        if produz == "pares":
            produzido = "pares"
        elif produz not in ("mesma_forma", "pares"):
            raise ValueError(f"{nome}: `produz` desconhecido {produz!r}")


def fase_universo(estado, rotas, C, P, anos, teses, carregos, memo_arrasto=None):
    """G5, G3, G7, G8, G4. Cada portao filtra, nenhum encerra. A SEQUENCIA vem do YAML.

    Devolve (vivos, rejeitados, dominados, preferencia).

    Por que a ordem importa (F-02): com o G3 antes do G5, uma rota de custo
    NAO_CONFIRMADO era ranqueada por custo tratando o desconhecido como zero, e zero
    ganha de todo mundo. A BOVV11 atravessava o G3 como a rota mais barata do catalogo
    e so morria no G5 — o veredito final saia certo, mas por acidente."""
    conferir_execucao_do_universo(P)   # P2: declarado e nao implementado
    conferir_ordem_do_universo(P)      # R-01: recusa antes de estourar la dentro
    # S-02: um memo de arrasto por PASSADA. O `C` nao muda dentro de uma passada, e e
    # so isso que autoriza reaproveitar. O cache global anterior supunha que o `C`
    # nunca mudava em lugar nenhum, e essa suposicao era falsa em todo teste.
    ctx = dict(estado=estado, C=C, P=P, anos=anos, teses=teses, carregos=carregos,
               rejeitados={}, dominados=[], preferencia=[],
               memo_arrasto={} if memo_arrasto is None else memo_arrasto)
    dentro = rotas
    for nome, _spec in ordem_dos_portoes(P, fase="universo"):
        dentro = PORTOES_DO_UNIVERSO[nome](dentro, ctx)
    return dentro, ctx["rejeitados"], ctx["dominados"], ctx["preferencia"]


def _pendencias_de_registro(rejeitados, P, teto_comp):
    """G7/G8 sem registro NAO e exclusao: e uma entrada que so o usuario pode dar.

    Vai para `pendencias`, ao lado do G0, com a instrucao exata — nao para a lista de
    rejeitadas. E a doutrina P6 na saida: a rota nao sumiu, ela esta esperando."""
    venc_max = vencimento_maximo(P)
    out = []
    for r, motivo in rejeitados.get("sem_tese", []):
        out.append(Pendencia(
            f"G7_tese:{r.id}",
            f"Escrever a tese de {r.nome} em teses.yaml: K02 (frase falsificavel com "
            f"numero), K03 (data, no maximo {teto_comp} anos), K04 (evento que INVALIDA "
            f"a tese, nao que machuca a posicao).",
            f"Enquanto nao houver tese, a rota nao recebe peso — nao porque o ativo seja "
            f"ruim, mas porque uma posicao sem prazo e sem condicao de encerramento nao "
            f"pode ser dimensionada. Motivo atual: {motivo}",
            bloqueia=f"alocacao_de_{r.id}"))
    for r, motivo in rejeitados.get("sem_carrego", []):
        if motivo == MOTIVO_REGRA_DECIDIDA:
            # G-07: o registro existe e esta assinado; pedir para "registrar" seria mandar
            # refazer o que ja foi feito. O que falta e a compra.
            out.append(Pendencia(
                f"G8_carrego:{r.id}",
                f"Na compra de {r.nome}, preencher C02 (papel e juro real travado) e C04 "
                f"(custo de quebrar) e mudar o estado para COMPROMISSO_ATIVO.",
                f"As regras estao seladas em REGRA_DECIDIDA; o peso so vem quando a "
                f"posicao existir. Motivo atual: {motivo}",
                bloqueia=f"alocacao_de_{r.id}"))
            continue
        out.append(Pendencia(
            f"G8_carrego:{r.id}",
            f"Registrar o compromisso de carrego de {r.nome} em teses.yaml: C01 "
            f"(vencimento do papel, ate {venc_max.isoformat()} pelo teto de "
            f"{teto_comp} anos), C02 (juro real travado), C03 (o UNICO evento que "
            f"autoriza vender antes — nao um preco), C04 (o custo de quebrar).",
            f"A duracao vem do papel que voce escolher, nao do catalogo. Sem o registro "
            f"o sistema nao sabe dimensionar a posicao. Motivo atual: {motivo}",
            bloqueia=f"alocacao_de_{r.id}"))
    return out


def _dividir_em_blocos(vivos, estado, P, carregos):
    """Quanto cabe a cada funcao, e quais rotas ocupam cada uma.

    Semantica dos tetos, e ela e a parte que ja produziu erro grave:
      - teto de FUNCAO (aposta, seguro de cauda) e MAXIMO ABSOLUTO. Redistribuicao
        nunca o viola. Na v1 desta camada, o excesso de outros blocos era despejado
        na unica rota abaixo do teto — que era justamente a de perda total. O motor
        produziu 60% em cripto e a tabela parecia plausivel.
      - teto POR ATIVO nao se aplica a uma "rota": uma rota de acao individual e uma
        SLEEVE que vai conter N papeis. O teto vira REQUISITO DE DIVERSIFICACAO.
      - custo_maximo_classe_aa nao EXCLUI a rota cara: LIMITA ela a
        custo_maximo_classe_peso do patrimonio (achado A-03)."""
    T = P["tetos"]
    f_rv = fracao_rv(estado, P)
    # cada rota entra em UM bloco; a ordem e a prioridade declarada da funcao
    ordem_func = sorted(P["funcoes"], key=lambda f: P["funcoes"][f]["prioridade"])
    frac_datada, objetivos, al_obj = necessidade_datada(estado, P)
    por_funcao = {f: [] for f in ordem_func}
    usados, bloco_por_rota = set(), {}
    for f in ordem_func:
        for v in vivos:
            if v[0].id in usados or f not in v[0].funcoes: continue
            if f == "DATADO":
                if frac_datada <= 0 or not casa_duracao(v[0], objetivos, P): continue
            por_funcao[f].append(v); usados.add(v[0].id); bloco_por_rota[v[0].id] = f

    p_cauda  = T["seguro_cauda_pct"] if por_funcao.get("SEGURO_CAUDA") else 0.0
    p_aposta = (T["aposta_pct"] if (por_funcao.get("APOSTA") and
                                    T["aposta_perda_total_aceita"]) else 0.0)
    disponivel = 1.0 - p_cauda - p_aposta
    p_rv = disponivel * f_rv
    conservador = disponivel - p_rv
    p_datado = conservador * frac_datada if por_funcao.get("DATADO") else 0.0
    # PROTECAO_REAL: o teto vem do PROPRIO COMPROMISSO (C05), nao da politica. Quem
    # assume a trava declara quanto do patrimonio aceita travar.
    p_protecao = 0.0
    if por_funcao.get("PROTECAO_REAL"):
        tetos_c = [ (carregos or {}).get(b[0].id, {}).get("carrego", {}).get("C05_teto_da_funcao")
                    for b in por_funcao["PROTECAO_REAL"] ]
        tetos_c = [t for t in tetos_c if isinstance(t, (int, float))]
        p_protecao = min(conservador - p_datado, max(tetos_c)) if tetos_c else 0.0
    p_lastro = conservador - p_datado - p_protecao
    blocos = dict(rv=p_rv, datado=p_datado, protecao_real=p_protecao,
                  lastro=p_lastro, cauda=p_cauda, aposta=p_aposta)
    return por_funcao, blocos, bloco_por_rota, f_rv, frac_datada, al_obj


def espalhar(bloco, total, nome_bloco, P, pesos, alertas, teto_por_rota=None):
    """1/N dentro do bloco (DeMiguel). Devolve a SOBRA.

    V-05: a versao anterior afirmava "excesso NUNCA sai do bloco" e dois caminhos
    faziam exatamente isso — bloco sem rota barata, e teto por rota. O valor devolvido
    vira `sobra` e e redirecionado ao bloco conservador. O comportamento e defensavel;
    a frase estava errada. O que de fato nunca acontece e sobra entrar em APOSTA ou
    SEGURO_CAUDA.

    P-37: `pesos` e `alertas` sao PARAMETROS agora, nao variaveis capturadas de uma
    funcao de 300 linhas. Uma funcao que muta dois dicts invisiveis do escopo de cima
    e legivel enquanto cabe numa tela e indefensavel depois disso."""
    T = P["tetos"]
    if total <= 1e-12: return 0.0
    if not bloco: return total       # bloco vazio nao engole peso: devolve como sobra
    caras = [b for b in bloco if b[2] > T["custo_maximo_classe_aa"]]
    baratas = [b for b in bloco if b not in caras]
    limite_cara = T["custo_maximo_classe_peso"]
    w_igual = total/len(bloco)
    alocado = 0.0
    for b in caras:
        w = min(w_igual, limite_cara, teto_por_rota or math.inf)
        pesos[b[0].id] = pesos.get(b[0].id, 0)+w; alocado += w
        alertas.append(f"{b[0].nome}: arrasto de {b[2]*100:.2f}% a.a. excede o teto de "
                       f"{T['custo_maximo_classe_aa']*100:.1f}% — LIMITADA a "
                       f"{w*100:.1f}% (teto de peso {limite_cara*100:.0f}%), nao excluida")
    resto = total - alocado
    if not baratas: return max(0.0, resto)
    w = resto/len(baratas)
    if teto_por_rota and w > teto_por_rota:
        for b in baratas: pesos[b[0].id] = pesos.get(b[0].id,0)+teto_por_rota
        sobra = resto - teto_por_rota*len(baratas)
        alertas.append(f"bloco {nome_bloco}: teto de {teto_por_rota*100:.0f}% por rota "
                       f"deixa {sobra*100:.1f}% sem destino — universo pequeno demais")
        return sobra
    for b in baratas: pesos[b[0].id] = pesos.get(b[0].id,0)+w
    return 0.0


def _funcoes_mortas(rotas, por_funcao, P):
    """V-09: funcao declarada na politica com ZERO rota viavel some sem aviso.

    Nos cinco cenarios SEGURO_CAUDA sai 0% porque sua unica rota e eliminada por
    atrito, e nada no output dizia isso — uma funcao inteira do modelo morrendo em
    silencio. A distincao entre "nao ha rota no catalogo" e "ha e nenhuma passou"
    importa: a primeira e buraco de modelagem, a segunda e consequencia do estado."""
    out = []
    for f, spec in P["funcoes"].items():
        if f in ("LIQUIDEZ",) or por_funcao.get(f): continue
        candidatas = [r for r in rotas if f in r.funcoes]
        if not candidatas:
            out.append(f"funcao {f} nao tem NENHUMA rota no catalogo — o modelo "
                       f"declara a funcao e nao ha com o que preenche-la")
        else:
            out.append(f"funcao {f} tem {len(candidatas)} rota(s) no catalogo e "
                       f"ZERO viavel neste estado: o peso dela foi redistribuido. "
                       f"A funcao esta declarada e morta na pratica")
    return out


# P-40. Eram seis chamadas alinhadas em coluna — legiveis quando `espalhar` tinha
# quatro argumentos, longas demais depois que a P-37 passou a receber `P`, `pesos` e
# `alertas` explicitamente (o que foi um ganho: eram capturados de um escopo invisivel).
# Em tabela, a lista de blocos e QUAL TETO cada um respeita viram dado que se le de
# uma vez. `None` no teto significa "sem teto por rota", nao "teto zero".
BLOCOS_A_ESPALHAR = (
    ("SEGURO_CAUDA",  "cauda",         "seguro_cauda_pct"),
    ("APOSTA",        "aposta",        "aposta_pct"),
    ("CRESCIMENTO",   "rv",            None),
    ("DATADO",        "datado",        None),
    ("PROTECAO_REAL", "protecao_real", None),
    ("LASTRO",        "lastro",        None),
)


def distribuir_por_funcao(vivos, rotas, estado, C, P, anos, carregos):
    """Alocacao 1/N por bloco, com tetos e redistribuicao de sobra.

    Devolve (pesos, alertas, blocos, bloco_por_rota, f_rv, frac_datada)."""
    T = P["tetos"]
    dc = P["crescimento"]["dentro_da_classe"]
    if dc["metodo"] != "1/N":
        raise ValueError(f"metodo dentro da classe nao implementado: {dc['metodo']}")
    if dc["permite_score"]:
        raise ValueError("permite_score=true exige que A05_nucleo_indexado_vs_selecao_ativa "
                         "esteja RESOLVIDA por backtest com pre-registro")

    por_funcao, blocos, bloco_por_rota, f_rv, frac_datada, al_obj = \
        _dividir_em_blocos(vivos, estado, P, carregos)
    pesos, alertas = {}, []
    alertas.extend(al_obj)

    hmin = P["funcoes"]["CRESCIMENTO"].get("horizonte_minimo_anos")
    if hmin and anos < hmin:
        alertas.append(f"horizonte de {anos:.0f} anos abaixo do horizonte_minimo_anos "
                       f"de CRESCIMENTO ({hmin}): a fracao em renda variavel ainda respeita "
                       f"o piso de {P['crescimento']['piso_rv']*100:.0f}%, mas o piso e uma "
                       f"escolha declarada, nao uma consequencia do horizonte")

    sobra = 0.0
    for funcao, chave, teto in BLOCOS_A_ESPALHAR:
        sobra += espalhar(por_funcao.get(funcao, []), blocos[chave], funcao, P, pesos,
                          alertas, T[teto] if teto else None)

    alertas.extend(_funcoes_mortas(rotas, por_funcao, P))

    # sobra vai para a funcao conservadora de menor prioridade numerica disponivel,
    # nunca para APOSTA ou SEGURO_CAUDA
    if sobra > 1e-9:
        cand = (por_funcao.get("LASTRO") or por_funcao.get("DATADO")
                or por_funcao.get("LIQUIDEZ") or por_funcao.get("CRESCIMENTO"))
        destino = min(cand, key=lambda b: b[2], default=None) if cand else None
        if destino:
            pesos[destino[0].id] = pesos.get(destino[0].id,0)+sobra
            alertas.append(f"sobra de {sobra*100:.1f}% direcionada para {destino[0].nome} "
                           f"(menor arrasto do bloco conservador) — nunca para APOSTA")
            sobra = 0.0
    return pesos, alertas, blocos, bloco_por_rota, f_rv, frac_datada


def _requisito_de_diversificacao(pesos, vivos, P):
    """O teto por ativo vira numero minimo de papeis. Uma rota de acao individual nao
    e um ativo — e uma SLEEVE que vai conter N empresas."""
    T = P["tetos"]
    teto_a = T["por_ativo_pct_patrimonio"]
    out = {}
    for rid, w in pesos.items():
        r = next(v[0] for v in vivos if v[0].id == rid)
        if r.exposicao in ("acao_br",) and w > teto_a:
            n = math.ceil(w/teto_a)
            out[rid] = dict(peso=w, n_minimo=n,
                nota=f"sleeve de {w*100:.0f}% com teto de {teto_a*100:.0f}% por papel "
                     f"exige no minimo {n} empresas distintas")
    return out


def _alerta_fgc(pesos, vivos, estado, P, anos):
    """Teto do FGC por CONGLOMERADO sobre o alvo projetado (A-03)."""
    T = P["tetos"]
    if not T["por_conglomerado"]: return []
    base = estado.patrimonio_investido or estado.aporte_mensal*12*anos
    por_emissor = {}
    for rid, w in pesos.items():
        r = next(v[0] for v in vivos if v[0].id == rid)
        if r.emissor and r.emissor != "TESOURO_NACIONAL":
            por_emissor[r.emissor] = por_emissor.get(r.emissor, 0.0) + w*base
    out = []
    for em, v_ in por_emissor.items():
        if v_ > T["por_emissor_credito_privado"]:
            n = math.ceil(v_/T["por_emissor_credito_privado"])
            out.append(f"emissor {em}: R${v_:,.0f} projetados excedem o FGC de "
                f"R${T['por_emissor_credito_privado']:,.0f} por CONGLOMERADO — "
                f"exige {n} conglomerados distintos".replace(",", "."))
    return out


def _conferir_invariantes(pesos, vivos, P):
    """B-05: ValueError e nao `assert`, porque a instrucao `assert` do Python e
    removida inteira por `python -O` e levaria a guarda junto. Uma guarda que some
    quando se liga otimizacao e pior que nenhuma: da a impressao de estar la."""
    T = P["tetos"]
    total = sum(pesos.values())
    if abs(total-1.0) >= 1e-6:
        raise ValueError(f"invariante violada: pesos somam {total}, nao 1")
    for rid, w in pesos.items():
        r = next(v[0] for v in vivos if v[0].id == rid)
        if r.funcao == "APOSTA" and w > T["aposta_pct"]+1e-9:
            raise ValueError(f"invariante violada: teto de APOSTA ({T['aposta_pct']}) — {rid}={w}")
        if r.funcao == "SEGURO_CAUDA" and w > T["seguro_cauda_pct"]+1e-9:
            raise ValueError(f"invariante violada: teto de SEGURO_CAUDA — {rid}={w}")


def _rv_realizada(pesos, vivos, blocos):
    """V-06: a fracao de RV impressa no cabecalho pode divergir da realizada, porque a
    sobra migra de CRESCIMENTO para o bloco conservador. Devolve (valor, alertas)."""
    rv = sum(w for rid, w in pesos.items()
             if next(v[0] for v in vivos if v[0].id == rid).funcao == "CRESCIMENTO")
    al = []
    if abs(rv - blocos["rv"]) > 1e-6:
        al.append(f"fracao de renda variavel ALVO {blocos['rv']*100:.1f}% x REALIZADA "
                  f"{rv*100:.1f}%: a sobra migrou de CRESCIMENTO para o "
                  f"bloco conservador. O cabecalho mostra o alvo; esta e a realizada")
    return rv, al


def alocar(estado, C, P, anos=None, teses=None, carregos=None):
    """Pipeline completo. Retorna dict com diretiva OU alocacao alvo + memoria.

    Sao seis passos e cada um cabe na cabeca. A ordem NAO e escolha desta funcao: as
    duas fases e a sequencia dentro delas vem de `politica.yaml -> portoes.*.ordem`
    (P-07), e este corpo apenas as executa."""
    anos, teto_comp, teses, carregos, rotas, saida = _preparar(
        estado, C, P, anos, teses, carregos)
    saida["pendencias"].extend(pendencias_de_premissa(estado, P, carregos))

    estado, rotas, encerrou = fase_aporte(estado, rotas, C, P, saida)
    if encerrou:
        return saida

    memo_arrasto = memo_de_arrasto(C)     # S-02: compartilhado por conteudo, nao global
    vivos, rejeitados, dominados, preferencia = fase_universo(
        estado, rotas, C, P, anos, teses, carregos, memo_arrasto)
    saida["pendencias"].extend(_pendencias_de_registro(rejeitados, P, teto_comp))

    fora_atrito = rejeitados.get("fora_atrito", [])
    saida["universo"] = dict(
        vivos=vivos, fora_atrito=fora_atrito,
        fora_status=rejeitados.get("fora_status", []),
        dominados=dominados, preferencia_horizonte=preferencia,
        sem_tese=rejeitados.get("sem_tese", []),
        sem_carrego=rejeitados.get("sem_carrego", []),
        interacao_g3_g4=interacao_g3_g4(fora_atrito, [v[0] for v in vivos], C,
                                        estado.aporte_mensal, P, anos, memo_arrasto),
        # V-13: elegibilidade nao e alocacao. As rotas de LIQUIDEZ atravessam todos os
        # portoes e nunca podem receber peso, porque a reserva e tratada pelo G2 —
        # contar as duas coisas na mesma linha inflava o "11 vivas" do output.
        alocaveis=[v for v in vivos if v[0].funcao != "LIQUIDEZ"])

    pesos, alertas, blocos, bloco_por_rota, f_rv, frac_datada = distribuir_por_funcao(
        vivos, rotas, estado, C, P, anos, carregos)

    diversificacao = _requisito_de_diversificacao(pesos, vivos, P)
    alertas.extend(_alerta_fgc(pesos, vivos, estado, P, anos))
    _conferir_invariantes(pesos, vivos, P)
    rv_realizada, al_rv = _rv_realizada(pesos, vivos, blocos)
    alertas.extend(al_rv)

    saida["fora_de_escopo"] = P["fora_de_escopo"]
    saida["alvo"] = dict(fracao_rv=f_rv, fracao_rv_realizada=rv_realizada,
                         pesos=pesos, alertas=alertas,
                         diversificacao=diversificacao, bloco_por_rota=bloco_por_rota,
                         custo_pct_aportado={rid: _custo_ou_motivo(
                             next(v[0] for v in vivos if v[0].id==rid), C,
                             max(estado.aporte_mensal*w, 1.0), anos, alertas)
                             for rid, w in pesos.items()},
                         blocos=blocos,
                         fracao_datada=frac_datada)
    return saida


def _custo_ou_motivo(r, C, aporte, anos, alertas):
    """`custo_pct_aportado`, ou None com o motivo nos alertas (P-134): o peso pequeno pode
    dar a rota um aporte menor que o custo fixo dela, e o numero seria mentira."""
    try:
        return custo_pct_aportado(r, C, aporte, anos)
    except AporteConsumidoPelaEntrada as e:
        alertas.append(f"P-134: {e}")
        return None


# ══ CUSTO DE DISCORDAR ═══════════════════════════════════════════════════════
def custo_de_discordar(alvo, proposta, C, aporte, anos, rotas_por_id):
    """O sistema nunca impoe. Mostra o que a diferenca custa, em taxa."""
    comem = []                    # P-134: rota cujo custo de entrada come o aporte dela
    def arrasto_carteira(pesos):
        tot = 0.0
        for rid, w in pesos.items():
            r = rotas_por_id.get(rid)
            if r is None: continue
            try:
                tot += w * arrasto_anualizado(r, C, max(aporte*w, 1.0), anos)
            except AporteConsumidoPelaEntrada as e:
                comem.append(str(e))
                return None
        return tot
    a_alvo, a_prop = arrasto_carteira(alvo), arrasto_carteira(proposta)
    dif = None if a_alvo is None or a_prop is None else (a_prop-a_alvo)*100
    return dict(arrasto_alvo_aa=a_alvo, arrasto_proposta_aa=a_prop,
                diferenca_pp_aa=dif, aporte_consumido=comem,
                nota="diferenca de CUSTO, que e computavel. Diferenca de RETORNO nao e — "
                     "para isso existe o backtest com pre-registro, nao esta funcao")

# ══ CAMADA 5 — MOTOR DE APORTE ═══════════════════════════════════════════════
def preco_do_lote(r, preco_unitario):
    """O preco que o motor recebe em `precos`: o de UM lote. P-179: no Tesouro o lote e 0,01
    titulo, e quem tem o PU do dia passa por aqui para nao entregar o PU como preco do lote
    (o que faria R$ 40 parecerem 0 lotes por um fator de 100, ou o contrario)."""
    return preco_unitario * r.lote_fracao if r.lote_fracao is not None else preco_unitario


def _primeiro_aporte(estado, pesos, A, C, P, precos, rotas_por_id, k_max):
    """P-164 (decisao dele, 03/10/2026, bloco 19, opcao c): com patrimonio zero o aporte
    vai INTEIRO para uma rota so -- a de maior peso-alvo que caiba no valor do mes.

    "Caber" sao as verificacoes que o motor ja tinha, e nenhuma nova: lote inteiro e o G3
    sobre o valor que a ordem gasta. A banda de concentracao fica de fora de proposito:
    com V = 0 toda ordem e 100% da carteira, e a banda recusaria todas. Sem a rota em
    `rotas_por_id` o motor nao conhece lote nem custo dela, e confere so o valor
    positivo -- o mesmo que ja fazia nas ordens com patrimonio (B-04).

    Nenhuma rota cabe: nao ha ordem, o dinheiro vai para o caixa e o motivo e dito
    (RI-10). Um zero ou um SEM_POSICAO mudo seriam a condicao engolida do F-02."""
    regra = P["motor_aporte"]["primeiro_aporte"]
    if regra["regra"] != "rota_de_maior_peso_que_cabe":
        raise ValueError(f"primeiro_aporte.regra desconhecida: {regra['regra']}")
    if regra["desempate"] != "ordem_do_catalogo":
        raise ValueError(f"primeiro_aporte.desempate desconhecido: {regra['desempate']}")
    ordem_cat = {rid: i for i, rid in enumerate(carregar_catalogo()["rotas"])}
    fila = sorted((rid for rid, w in pesos.items() if w > 0),
                  key=lambda rid: (-pesos[rid], ordem_cat.get(rid, len(ordem_cat))))

    def nome(rid):
        r = rotas_por_id.get(rid)
        return r.nome if r is not None else rid

    nao_couberam, ordem = [], None
    for rid in fila:
        r = rotas_por_id.get(rid)
        p = precos.get(rid, 1.0)
        em_lote = r.negocia_em_lote if r is not None else False   # B-04: flag, nao magnitude
        if em_lote:
            qtd = math.floor(A/p); gasto = qtd*p
        else:
            qtd = round(A, 2);     gasto = qtd
        if qtd <= 0:
            nao_couberam.append(dict(rota=rid, peso_alvo=round(pesos[rid], 4),
                                     verificacao="lote",
                                     detalhe=f"um lote custa R$ {p:.2f}, o aporte e R$ {A:.2f}"))
            continue
        if r is not None and not g3_atrito([r], C, P, gasto)[0]:
            nao_couberam.append(dict(rota=rid, peso_alvo=round(pesos[rid], 4),
                                     verificacao="G3_atrito",
                                     detalhe=f"o custo de entrada sobre R$ {gasto:.2f} passa "
                                             f"do teto do G3"))
            continue
        ordem = dict(rota=rid, quantidade=qtd, preco=p, valor=round(gasto, 2),
                     deficit=round(pesos[rid]*A, 2), peso_atual=0.0,
                     peso_alvo=round(pesos[rid], 4))
        break

    base = dict(aporte=A, aporte_base=estado.aporte_mensal,
                extraordinario=round(A-estado.aporte_mensal, 2), patrimonio=0.0,
                regra="primeiro_aporte", nao_couberam=nao_couberam,
                politica_versao=P["meta"]["versao"], politica_hash=P.get("_hash"),
                custos_hash=hash_custos())
    if ordem is None:
        return dict(status="NENHUMA_ROTA_CABE", ordens=[], motivo=regra["motivo_sem_rota"],
                    caixa=round(estado.caixa + A, 2), **base)

    peso = f"{pesos[ordem['rota']]*100:.1f}%".replace(".", ",")
    if nao_couberam:
        acima = [nome(d["rota"]) for d in nao_couberam]
        ordem["porque"] = regra["porque_cedeu"].format(
            rota=nome(ordem["rota"]), peso=peso, acima=" e ".join(acima),
            cabe="cabe" if len(acima) == 1 else "cabem")
    else:
        ordem["porque"] = regra["porque"].format(rota=nome(ordem["rota"]), peso=peso)
    # B-01/B-02/B-03: o residuo do lote vai para caixa, nunca para a ordem
    return dict(status="OK", ordens=[ordem], caixa=round(estado.caixa + A - ordem["valor"], 2),
                deficit_max=None, excesso_max=None, alertas=[], deriva=None, k_max=k_max,
                nota_bases="P-164: com patrimonio zero nao ha peso atual nem deficit "
                           "relativo; deficit_max e excesso_max ficam None, nao zero",
                **base)


def motor_aporte(estado, alvo, C, P, precos=None, k_max=None, rotas_por_id=None,
                 aporte_do_mes=None):
    """Onde aportar este mes. Retorna ordens + memoria de calculo (principio P4).

    `aporte_do_mes` existe porque o aporte nao e uma verdade em pedra (critica do
    usuario, 04/09/2026): num mes de bonus entra mais dinheiro que o piso. Duas
    coisas que NAO podem ser confundidas:

      o ALVO e estrutural e se calcula sobre o PISO. Recalcula-lo a cada mes faria a
      carteira-alvo oscilar com o bonus, e uma carteira-alvo que muda todo mes nao e
      um alvo — e uma reacao.

      as ORDENS do mes se calculam sobre o dinheiro do mes. Mais dinheiro fecha mais
      deficit, e o k_max continua limitando o numero de ordens.
    """
    V = estado.patrimonio_investido
    A = aporte_do_mes if aporte_do_mes is not None else estado.aporte_mensal
    if A <= 0:
        return dict(status="SEM_APORTE",
                    nota="aporte do mes igual a zero: nao ha ordem a emitir. O alvo e "
                         "os portoes continuam validos — o que falta e o dinheiro.")
    if k_max is None: k_max = P["motor_aporte"]["k_max"]   # V-03: era default na assinatura
    pesos = alvo["pesos"]
    precos = precos or {}
    rotas_por_id = rotas_por_id or {}
    if V <= 0:
        # P-164: era SEM_POSICAO, e quem tinha a reserva cheia e nada investido ficava
        # sem "quanto e onde". As divisoes por V abaixo sao o motivo do caminho proprio.
        return _primeiro_aporte(estado, pesos, A, C, P, precos, rotas_por_id, k_max)
    D = {rid: pesos.get(rid,0.0)*(V+A) - estado.posicoes.get(rid,0.0) for rid in pesos}
    candidatos = sorted([(rid,d) for rid,d in D.items() if d > 0], key=lambda x:-x[1])

    # V-14: o freio avalia a compra QUE SERA EXECUTADA, nao o deficit inteiro. A versao
    # anterior supunha `min(d, A)` e podia excluir uma rota que, de fato, nao cruzaria a
    # banda — porque a ordem real e limitada tambem pelo k_max e pelo lote inteiro.
    banda = P["tetos"]["banda_sobre_alvo_pp"]
    alertas, ordens, restante = [], [], A
    executadas = 0
    for rid, d in candidatos:
        if executadas >= k_max: break
        r = rotas_por_id.get(rid)
        em_lote = r.negocia_em_lote if r is not None else False   # B-04: flag, nao magnitude
        p = precos.get(rid, 1.0)
        valor = min(d, restante)
        if em_lote:
            qtd = math.floor(valor/p); gasto = qtd*p
        else:
            qtd = round(valor, 2);     gasto = qtd
        if qtd <= 0: continue
        w_pos = (estado.posicoes.get(rid,0.0)+gasto)/(V+A)        # a compra REAL
        alvo_r = pesos.get(rid, 0.0)
        if w_pos > alvo_r + banda + 1e-9:
            alertas.append(dict(tipo="CONCENTRACAO", rota=rid, peso=w_pos, teto=alvo_r+banda,
                                compra_avaliada=round(gasto,2),
                                acao="fora da fila de aporte — nao vendido "
                                     "(quarentena automatica)"))
            continue
        ordens.append(dict(rota=rid, quantidade=qtd, preco=p, valor=round(gasto,2),
                           deficit=round(d,2),
                           peso_atual=round(estado.posicoes.get(rid,0)/V,4),
                           peso_alvo=round(pesos.get(rid,0),4)))
        restante -= gasto; executadas += 1
    # B-01/B-02/B-03: o residuo NAO vai para a primeira ordem (isso aumentava o desvio
    # na direcao oposta e quebrava valor == quantidade x preco). Vai para caixa.
    caixa_novo = round(estado.caixa + max(0.0, restante), 2)

    # A-06: o gatilho compara a capacidade com o maior DEFICIT relativo. O aporte so
    # compra; rota acima do alvo nunca e corrigida por compra, com capacidade nenhuma.
    capacidade = (A*12)/V if V else math.inf
    deficit_rel = max((max(0.0, pesos.get(r,0.0) - estado.posicoes.get(r,0.0)/V) for r in pesos),
                      default=0.0)
    excesso_rel = max((max(0.0, estado.posicoes.get(r,0.0)/V - pesos.get(r,0.0)) for r in pesos),
                      default=0.0)
    deriva = None
    if capacidade < deficit_rel:
        deriva = dict(tipo="DERIVA_ESTRUTURAL", capacidade_anual=capacidade,
            deficit_max=deficit_rel, excesso_max=excesso_rel,
            nota="o aporte nao fecha o maior DEFICIT nem em 12 meses. Rebalancear so por "
                 "compra expirou. O sistema NAO vende sozinho: proximo passo e apresentar "
                 "os cenarios de venda com o custo fiscal de cada um.")
    return dict(status="OK", aporte=A, aporte_base=estado.aporte_mensal,
                extraordinario=round(A-estado.aporte_mensal, 2),
                patrimonio=V, ordens=ordens, caixa=caixa_novo,
                deficit_max=round(deficit_rel,4), excesso_max=round(excesso_rel,4),
                alertas=alertas, deriva=deriva, k_max=k_max,
                nota_bases="V-15: `peso_atual` e sobre o patrimonio ATUAL (V); `deficit` "
                           "e o que falta para o alvo DEPOIS do aporte (V+A). Sao bases "
                           "diferentes de proposito — o peso descreve hoje, o deficit "
                           "descreve o destino — e por isso nao fecham entre si",
                politica_versao=P["meta"]["versao"], politica_hash=P.get("_hash"),
                custos_hash=hash_custos())
