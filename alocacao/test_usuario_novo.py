# -*- coding: utf-8 -*-
"""
A PRIMEIRA EXPERIENCIA: o que o sistema responde a quem nao tem nada. Pendencia P-47.

POR QUE ESTE ARQUIVO EXISTE — e a origem dele e uma correcao do Osvaldo, em 06/09/2026:

  "isso me parece estranho, eu nao ter reserva ou aporte ser uma barreira de
   desenvolvimento. imagina que em vez de uma ferramenta para mim fosse uma ferramenta
   para ser vendida: eu nao teria informacoes sobre o aporte e a reserva do cliente
   porque ele nao existiria. entao o sistema tem que existir e funcionar independente
   do input do usuario."

  Ele esta certo, e o erro era meu. Eu vinha listando "aporte realizado = zero" e
  "as duas teses nao assinadas" como se fossem BLOQUEIOS DE DESENVOLVIMENTO. Nao sao:
  sao o estado de UM usuario. Um cliente novo de um produto tem exatamente isso —
  zero de tudo — e o sistema precisa responder mesmo assim.

  E o achado L-01 num nivel acima. A L-01 separou `politica.yaml` (o motor) de
  `perfil.yaml` (um usuario) na CONFIGURACAO. O PLANO nunca recebeu essa separacao, e
  por isso o caminho critico do projeto tinha, no meio dele, coisas que so dizem
  respeito a carteira do Osvaldo.

O QUE ESTES TESTES GARANTEM
  Que a primeira experiencia e COMPORTAMENTO DO SISTEMA, e nao um caso particular.
  Nenhum deles usa o `estado.yaml` — todos constroem um usuario do zero, como um
  cadastro faria.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from alocacao import Estado, alocar, carregar_politica, reserva_alvo
from motor import carregar as carregar_custos

C, P = carregar_custos(), carregar_politica()

# O MINIMO que um cadastro precisa perguntar. Nada aqui e patrimonio: sao fatos sobre
# a vida da pessoa, e e legitimo exigi-los — um sistema que nao sabe a despesa mensal
# nao tem como dimensionar reserva de emergencia.
CADASTRO_MINIMO = dict(despesa_mensal=3000, estabilidade_renda="media",
                       horizonte_anos=30, aporte_mensal=800)


def usuario_novo(**mudancas):
    """Alguem que acabou de chegar: zero de tudo, nada assinado, nada registrado."""
    return Estado(**{**CADASTRO_MINIMO, "reserva_atual": 0.0, **mudancas})


def test_o_sistema_responde_a_quem_nao_tem_nada():
    """O teste que a correcao do Osvaldo exigia. Patrimonio zero, nenhuma tese
    assinada, nenhum compromisso registrado — e o sistema tem de dar uma resposta
    COMPLETA, nao uma lista de pendencias."""
    r = alocar(usuario_novo(), C, P, teses={}, carregos={})
    d = r.get("diretiva")
    assert d is not None, "usuario novo tem de receber uma diretiva, nao um vazio"
    assert d.portao == "G2_reserva", "com reserva zero, o primeiro passo e a reserva"
    assert d.valor > 0 and d.destino, "a resposta tem de dizer QUANTO e PARA ONDE"


def test_a_resposta_e_acionavel_sem_o_usuario_ter_decidido_mais_nada():
    """Acionavel = a pessoa consegue AGIR hoje, sem responder mais nenhuma pergunta.
    Um sistema que responde "depende" para quem acabou de chegar nao serve."""
    r = alocar(usuario_novo(), C, P, teses={}, carregos={})
    m = r["diretiva"].memoria
    assert m["composicao"], "tem de dizer em quais rotas, nao so o valor total"
    assert m["meses_para_completar"] > 0, "tem de dizer quanto tempo leva"
    assert m["alvo"] == reserva_alvo(usuario_novo(), P)
    for t in m["composicao"]:
        assert t["rota_id"] and t["valor"] > 0
    assert abs(sum(t["valor"] for t in m["composicao"]) - m["alvo"]) < 0.01, \
        "a composicao tem de cobrir o alvo inteiro — plano parcial nao e plano"


def test_nenhuma_pendencia_de_registro_atrapalha_quem_esta_comecando():
    """As teses do HASH11 e do IPCA+ sao decisoes de UM usuario. Um cliente novo nao
    as tem, e isso NAO pode travar a resposta dele — e a doutrina P6 vista do lado do
    produto: falta de decisao do usuario nao vira ausencia de sistema."""
    r = alocar(usuario_novo(), C, P, teses={}, carregos={})
    assert r["diretiva"] is not None
    # na fase de reserva nem chegam a aparecer; o que importa e que nao bloqueiam
    assert not any("BLOQUEIA" in (p.consequencia or "").upper() and "reserva" in p.id.lower()
                   for p in r["pendencias"])


def test_depois_da_reserva_o_sistema_aloca_sem_nada_assinado():
    """O passo seguinte da mesma pessoa. Sem tese e sem carrego, o sistema ainda
    entrega uma carteira completa: as rotas que EXIGEM registro ficam de fora com o
    motivo escrito, e as outras recebem peso."""
    pronto = usuario_novo(reserva_atual=27000)
    r = alocar(pronto, C, P, teses={}, carregos={})
    alvo = r["alvo"]
    assert alvo, "com a reserva pronta, tem de vir alocacao"
    assert abs(sum(alvo["pesos"].values()) - 1.0) < 1e-6
    assert len(alvo["pesos"]) >= 5, "uma carteira de uma rota so nao e diversificacao"
    ids = [p.id for p in r["pendencias"]]
    assert "G7_tese:hash11" in ids and "G8_carrego:td_ipca" in ids, \
        "as rotas que exigem registro viram PERGUNTA, nao somem"
    assert "hash11" not in alvo["pesos"] and "td_ipca" not in alvo["pesos"], \
        "e nao recebem peso enquanto o registro nao existir"


def test_o_sistema_diz_o_que_nao_conseguiu_preencher():
    """P5 do lado do produto. Tres funcoes do modelo ficam sem rota viavel para quem
    esta comecando, e o sistema AVISA em vez de entregar uma carteira que parece
    completa. Silencio aqui seria a pior resposta possivel."""
    r = alocar(usuario_novo(reserva_atual=27000), C, P, teses={}, carregos={})
    mortas = [a for a in r["alvo"]["alertas"] if "ZERO viavel" in a or "NENHUMA rota" in a]
    assert mortas, "funcao sem rota viavel tem de aparecer no output"


@pytest.mark.parametrize("perfil,rotulo", [
    (dict(despesa_mensal=1500, aporte_mensal=200, horizonte_anos=40,
          estabilidade_renda="baixa"), "renda baixa, autonomo, jovem"),
    (dict(despesa_mensal=12000, aporte_mensal=8000, horizonte_anos=10,
          estabilidade_renda="alta"), "renda alta, CLT, meia-idade"),
    (dict(despesa_mensal=4000, aporte_mensal=500, horizonte_anos=25,
          estabilidade_renda="media", dependentes=3), "com tres dependentes"),
    (dict(despesa_mensal=6000, aporte_mensal=1000, horizonte_anos=2,
          estabilidade_renda="media"), "horizonte muito curto"),
])
def test_perfis_diferentes_recebem_respostas_diferentes_e_validas(perfil, rotulo):
    """O sistema e para MAIS DE UMA PESSOA. Se ele responde a mesma coisa para um
    autonomo de renda baixa e para um CLT de renda alta, ele nao esta modelando nada —
    esta imprimindo uma opiniao."""
    e = Estado(**{**perfil, "reserva_atual": 0.0})
    r = alocar(e, C, P, teses={}, carregos={})
    assert r.get("diretiva") or r.get("alvo"), f"{rotulo}: sem resposta"
    if r.get("diretiva"):
        assert r["diretiva"].memoria["alvo"] > 0
        assert r["diretiva"].memoria["meses_para_completar"] > 0


def test_a_reserva_alvo_reage_ao_perfil_e_nao_e_um_numero_fixo():
    """A prova de que o sistema modela a PESSOA. Estabilidade e dependentes tem de
    mover o alvo — se nao movessem, os campos seriam decoracao."""
    base = usuario_novo()
    estavel = usuario_novo(estabilidade_renda="alta")
    instavel = usuario_novo(estabilidade_renda="baixa")
    com_filhos = usuario_novo(dependentes=3)
    a_base = reserva_alvo(base, P)
    assert reserva_alvo(estavel, P) < a_base < reserva_alvo(instavel, P)
    assert reserva_alvo(com_filhos, P) > a_base


def _nomes_do_carregar(fonte):
    """Os nomes pelos quais `fonte` alcanca `estado_io.carregar`. Vazio = nao alcanca.

    A guarda pegou o proprio autor em 06/09/2026, e por isso ela foi AFIADA em vez
    de afrouxada. O proibido nao e o modulo `estado_io` — e a funcao `carregar()`,
    que le o `estado.yaml` do Osvaldo do caminho padrao. `validar(d)` sobre um dict
    e legitimo: valida o MODELO, nao a pessoa.

    B-13 (24/09/2026): o import registrava `a.asname or a.name`, entao
    `from estado_io import carregar as c` entrava como "c" e a chamada `c()` e
    `ast.Name`, nao `ast.Attribute` -- escapava pelas duas pontas. Agora conta o nome
    ORIGINAL. E `from estado_io import *` traz o `carregar` sem nomea-lo: sem saber o
    que entrou, a guarda recusa."""
    import ast
    nomes = set()
    for n in ast.walk(ast.parse(fonte)):
        if isinstance(n, ast.ImportFrom) and n.module == "estado_io":
            nomes |= {a.name for a in n.names}
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute):
            nomes.add(n.func.attr)
    return nomes & {"carregar", "*"}


def test_nenhum_teste_deste_arquivo_toca_o_estado_do_osvaldo():
    """A garantia estrutural: a primeira experiencia nao pode depender do estado.yaml,
    que e de UMA pessoa. Se algum teste daqui passar a le-lo, ele deixa de medir o
    sistema e passa a medir o Osvaldo."""
    alcance = _nomes_do_carregar(open(__file__, encoding="utf-8").read())
    assert not alcance, (
        f"este arquivo alcanca `estado_io.carregar()` por {sorted(alcance)}, e ela le o "
        "estado.yaml do Osvaldo. A primeira experiencia tem de ser construida do zero, "
        "como um cadastro faria — senao ela deixa de medir o SISTEMA e passa a medir "
        "uma pessoa.")
    # e a prova positiva: os cenarios sao montados a mao, com o cadastro minimo
    assert set(CADASTRO_MINIMO) == {"despesa_mensal", "estabilidade_renda",
                                    "horizonte_anos", "aporte_mensal"}


@pytest.mark.parametrize("fonte, pega", [
    ("import estado_io\nestado_io.carregar()\n", True),
    ("from estado_io import carregar as c\nc()\n", True),          # B-13: escapava
    ("from estado_io import *\ncarregar()\n", True),               # B-13: escapava
    ("from estado_io import validar\nvalidar({})\n", False),       # legitimo
    ("from motor import carregar as carregar_custos\ncarregar_custos()\n", False),
])
def test_B13_a_guarda_do_carregar_ve_alias_e_import_estrela(fonte, pega):
    """A guarda provada numa fonte SINTETICA, e nao so neste arquivo: aplicada a si
    mesma ela so prova que ninguem chama `carregar` hoje, nao que chamar seria pego.
    As duas ultimas linhas sao o controle -- uma guarda que recusasse tudo tambem
    passaria nas tres primeiras."""
    assert bool(_nomes_do_carregar(fonte)) is pega


# ══ P-48 · o modelo de estado, e a fronteira que ele torna visivel ═══════════
def test_o_modelo_de_estado_declara_o_que_e_obrigatorio():
    """Ate 06/09 havia UM `estado.yaml`, e ele era do Osvaldo. A L-01 separou motor de
    perfil na configuracao; o ESTADO FINANCEIRO ficou sem modelo, e nao havia como
    saber o que um cadastro precisa perguntar sem ler o validador.

    O modelo torna a fronteira visivel: quatro fatos sobre a VIDA (obrigatorios) e
    todo o resto PATRIMONIO (comeca vazio em cliente novo)."""
    import yaml
    d = yaml.safe_load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                         "estado.exemplo.yaml"), encoding="utf-8"))
    obrigatorios = {k for k, v in d.items()
                    if v is None and k not in ("meta", "match_empregador")}
    assert obrigatorios == set(CADASTRO_MINIMO), (
        f"o modelo pede {sorted(obrigatorios)} e os testes da primeira experiencia "
        f"usam {sorted(CADASTRO_MINIMO)}. Os dois tem de dizer a mesma coisa.")
    assert d["reserva_atual"] == 0.0 and d["posicoes"] == {} and d["dividas"] == []
    assert d["meta"]["status"] == "MODELO", \
        "modelo com status REAL vira numero de exemplo servindo de base para decisao"


def test_o_modelo_nao_carrega_ate_alguem_preencher():
    """Recusar e o comportamento certo: um modelo que rodasse com `null` produziria
    uma recomendacao a partir de nada. E o F-02 outra vez — ausencia virando numero."""
    from estado_io import validar
    import yaml
    d = yaml.safe_load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                         "estado.exemplo.yaml"), encoding="utf-8"))
    # CX-05: o retorno e (dados, problemas, avisos). Ate 04/10 esta linha desempacotava
    # `problemas, _avisos, _`, e `problemas` era o dicionario de dados: as chaves do modelo
    # faziam o teste passar com o validador sem recusa nenhuma (test_cx05_guarda_do_modelo).
    _dados, problemas, _avisos = validar(d)
    assert isinstance(problemas, list), f"problemas tem de ser a lista, veio {type(problemas)}"
    assert problemas, "o modelo em branco tem de ser recusado"
    for campo in CADASTRO_MINIMO:
        assert any(campo in p for p in problemas), \
            f"{campo} e obrigatorio e a recusa nao o nomeia"
