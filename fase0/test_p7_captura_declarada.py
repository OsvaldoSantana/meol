#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P7 com teste: nenhum acervo existe sem regime de captura escrito.

A P7 e de 06/09/2026 e e dele: *"rotina que depende de alguem lembrar nao e rotina"*.
Ela admite duas saidas e so duas -- rodar sem intervencao humana, ou ser declarada em
`limitacoes_declaradas` com a mesma seriedade das outras. Nao existe terceira chamada
"eu lembro".

E ate 18/09/2026 o projeto estava na terceira. Duas capturas manuais (CVM e COTAHIST)
alimentavam o acervo havia semanas e NENHUMA das duas estava declarada. A doutrina
existia, escrita em dois arquivos, e nada media. E o defeito recorrente da casa na sua
forma mais barata de cometer: *um arquivo declara um comportamento que o codigo nao
tem, e os dois concordam por acidente* -- aqui nem por acidente, por ausencia de
instrumento.

ALCANCE, declarado antes de qualquer resultado (P5 aplicada ao instrumento): este
arquivo mede que cada subpasta de `docs/acervo/` e nomeada por alguma entrada de
`limitacoes_declaradas.*.acervos`, e que nenhuma entrada nomeia pasta inexistente.
NAO mede que a captura seja manual, que alguem a tenha rodado, ou quando. Um acervo
que ganhe rotina automatica continua passando aqui ate alguem tirar o nome da lista --
e e por isso que `quando_deixa_de_importar` esta escrito em cada entrada.
"""
from __future__ import annotations
import datetime as dt
import io
import os
import sys

import pytest
import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import manifesto_cvm as m  # noqa: E402

RAIZ = m.raiz_do_repositorio(os.path.dirname(os.path.abspath(__file__)))


def _politica():
    with io.open(os.path.join(RAIZ, m.POLITICA), encoding="utf-8") as f:
        return yaml.safe_load(f)


def test_o_repositorio_foi_encontrado():
    """Se a ancora falhar, todos os outros passam por vacuidade -- que e o modo de
    falha que o A-06 ensinou a temer: guarda verde porque nao mediu nada."""
    assert RAIZ and os.path.isdir(os.path.join(RAIZ, "alocacao"))


def test_existe_pelo_menos_um_acervo_para_medir():
    """Vacuidade outra vez, do outro lado: sem pasta em docs/acervo/ a diferenca de
    conjuntos e vazia e o teste principal passa sem ter visto nada."""
    base = os.path.join(RAIZ, m.ACERVO)
    assert os.path.isdir(base), f"{m.ACERVO} nao existe -- o manifesto grava ali"
    assert [n for n in os.listdir(base) if os.path.isdir(os.path.join(base, n))]


def test_P7_todo_acervo_tem_regime_de_captura_declarado():
    sem, _ = m.acervos_sem_regime(RAIZ)
    assert not sem, (
        f"acervo(s) sem regime de captura declarado: {sorted(sem)}. "
        "P7: ou a captura roda sem humano, ou ela entra em "
        "limitacoes_declaradas com `acervos`, direcao do vies e condicao de saida."
    )


def test_P7_nenhuma_declaracao_aponta_para_acervo_que_nao_existe():
    """Declaracao apodrecida e pior que declaracao ausente: ela parece cobertura.
    Se um acervo for renomeado ou removido, o nome velho fica na politica dizendo que
    alguem pensou no regime de uma pasta que nao existe mais."""
    _, orfas = m.acervos_sem_regime(RAIZ)
    assert not orfas, f"declaracao sem acervo correspondente: {sorted(orfas)}"


def test_a_declaracao_carrega_o_que_a_P5_exige_e_nao_so_o_nome():
    """Nomear o acervo e barato. O que torna a limitacao util -- e o que
    `limitacoes_declaradas` exige das outras oito -- e a DIRECAO DO VIES e a condicao
    em que ela deixa de importar. Sem os dois, a entrada e um alibi: cumpre a letra da
    P7 e nao diz nada a quem ler o resultado."""
    faltando = {}
    for nome, lim in _politica()["limitacoes_declaradas"].items():
        if not isinstance(lim, dict) or "acervos" not in lim:
            continue
        ausentes = [c for c in ("direcao_do_vies", "quando_deixa_de_importar", "fonte")
                    if not lim.get(c)]
        if ausentes:
            faltando[nome] = ausentes
    assert not faltando, faltando


def test_o_campo_acervos_e_lista_de_texto_e_nao_um_texto_solto():
    """`acervos: cvm` em vez de `acervos: ["cvm"]` faria a uniao virar o conjunto das
    LETRAS -- e {'c','v','m'} nao casa com pasta nenhuma, entao o teste principal
    reprovaria com uma mensagem que nao explica nada. Falhar aqui explica."""
    for nome, lim in _politica()["limitacoes_declaradas"].items():
        if isinstance(lim, dict) and "acervos" in lim:
            a = lim["acervos"]
            assert isinstance(a, list) and a and all(isinstance(x, str) for x in a), \
                f"{nome}.acervos deve ser lista nao vazia de texto, veio {a!r}"


# ── prova por mutacao ─────────────────────────────────────────────────────────
# Guarda que nunca falhou e guarda que ninguem sabe se funciona (regra 4 da §5-B).

def _repo_falso(tmp_path, acervos, declarados):
    (tmp_path / "pyproject.toml").write_text("[tool.x]\n", encoding="utf-8")
    pol = tmp_path / "alocacao"
    pol.mkdir()
    corpo = {"limitacoes_declaradas": {
        f"lim_{i}": {"acervos": list(d), "direcao_do_vies": "x",
                     "quando_deixa_de_importar": "y", "fonte": "z"}
        for i, d in enumerate(declarados)}}
    (pol / "politica.yaml").write_text(yaml.safe_dump(corpo), encoding="utf-8")
    for a in acervos:
        (tmp_path / "docs" / "acervo" / a).mkdir(parents=True)
    return str(tmp_path)


def test_mutacao_acervo_novo_sem_declaracao_e_ACUSADO(tmp_path):
    raiz = _repo_falso(tmp_path, ["cvm", "b3", "anbima"], [["cvm", "b3"]])
    sem, orfas = m.acervos_sem_regime(raiz)
    assert sem == {"anbima"} and not orfas


def test_mutacao_declaracao_de_acervo_inexistente_e_ACUSADA(tmp_path):
    raiz = _repo_falso(tmp_path, ["cvm"], [["cvm", "tesouro"]])
    sem, orfas = m.acervos_sem_regime(raiz)
    assert orfas == {"tesouro"} and not sem


def test_mutacao_acervo_coberto_por_qualquer_entrada_serve(tmp_path):
    """A cobertura e por UNIAO: duas limitacoes diferentes podem cobrir um acervo cada,
    e e assim que a CVM e a B3 estao hoje -- regimes distintos, entradas distintas."""
    raiz = _repo_falso(tmp_path, ["cvm", "b3"], [["cvm"], ["b3"]])
    assert m.acervos_sem_regime(raiz) == (set(), set())


def test_mutacao_arquivo_no_lugar_de_pasta_nao_vira_acervo(tmp_path):
    """`docs/acervo/` guarda um CSV por captura DENTRO da pasta do acervo; um arquivo
    solto na raiz nao e acervo e nao deve exigir declaracao."""
    raiz = _repo_falso(tmp_path, ["cvm"], [["cvm"]])
    (tmp_path / "docs" / "acervo" / "LEIA.md").write_text("x", encoding="utf-8")
    assert m.acervos_sem_regime(raiz) == (set(), set())


# ── P-57 passo 3: o regime AUTOMATICO e dado, e a limitacao resolvida nao cobre ──

@pytest.mark.repositorio   # 146b: le o repositorio, a mutacao exclui
def test_P57_todo_regime_declarado_esta_inteiro_no_arquivo_real():
    assert m.defeitos_de_regime(RAIZ) == {}


def test_P57_cvm_e_b3_rodam_sozinhas_e_nao_sao_mais_limitacao():
    """Falha na versao de 25/09 antes deste commit: as duas eram limitacao vigente com a
    execucao agendada verde ja feita (36148547193)."""
    P = _politica()
    assert {"cvm", "b3"} <= set(P["regimes_de_captura"])
    assert not {"cvm", "b3"} & set(m.acervos_em_limitacao(P))


def _com_regime(tmp_path, regimes, limitacoes=None, passos=("captura",)):
    (tmp_path / "pyproject.toml").write_text("[tool.x]\n", encoding="utf-8")
    (tmp_path / "alocacao").mkdir()
    wf = tmp_path / ".github" / "workflows"
    wf.mkdir(parents=True)
    (wf / "c.yml").write_text(yaml.safe_dump(
        {"jobs": {"j": {"steps": [{"id": p} for p in passos]}}}), encoding="utf-8")
    (tmp_path / "docs" / "acervo" / "cvm").mkdir(parents=True)
    (tmp_path / "docs" / "acervo" / "cvm" / "capturas.csv").write_text("x", encoding="utf-8")
    corpo = {"regimes_de_captura": regimes, "limitacoes_declaradas": limitacoes or {}}
    (tmp_path / "alocacao" / "politica.yaml").write_text(yaml.safe_dump(corpo),
                                                          encoding="utf-8")
    return str(tmp_path)


def _regime(**muda):
    r = {"regime": "AUTOMATICO", "executor": ".github/workflows/c.yml", "passo": "captura",
         "registro": "docs/acervo/cvm/capturas.csv", "primeira_execucao_agendada": 1,
         "em": dt.date(2026, 9, 25)}
    r.update(muda)
    return r


def test_mutacao_regime_inteiro_cobre_o_acervo(tmp_path):
    raiz = _com_regime(tmp_path, {"cvm": _regime()})
    assert m.acervos_sem_regime(raiz) == (set(), set())
    assert m.defeitos_de_regime(raiz) == {}


@pytest.mark.parametrize("muda, trecho", [
    ({"regime": "MANUAL"}, "regime"),
    ({"executor": ".github/workflows/nao.yml"}, "executor"),
    ({"passo": "captura_nefin"}, "passo"),
    ({"registro": "docs/acervo/cvm/nao.csv"}, "registro"),
    ({"primeira_execucao_agendada": None}, "execucao agendada"),
    ({"em": "2026-09-25"}, "data"),
])
def test_mutacao_regime_com_defeito_e_ACUSADO(tmp_path, muda, trecho):
    raiz = _com_regime(tmp_path, {"cvm": _regime(**muda)})
    d = m.defeitos_de_regime(raiz)
    assert list(d) == ["cvm"] and any(trecho in f for f in d["cvm"]), d


def test_mutacao_acervo_automatico_E_limitacao_vigente_e_ACUSADO(tmp_path):
    lim = {"x": {"tipo": "NAO_CONSERTADA", "acervos": ["cvm"]}}
    d = m.defeitos_de_regime(_com_regime(tmp_path, {"cvm": _regime()}, lim))
    assert any("limitacao vigente x" in f for f in d["cvm"]), d


def test_mutacao_limitacao_RESOLVIDA_nao_cobre_acervo(tmp_path):
    """Sem o filtro de HISTORICO, a frase que ja caiu continuaria cobrindo o acervo, e
    apagar o regime passaria calado."""
    lim = {"x": {"RESOLVIDA": "ja rodou", "acervos": ["cvm"]}}
    raiz = _com_regime(tmp_path, {}, lim)
    assert m.acervos_sem_regime(raiz) == ({"cvm"}, set())


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))


# ── P-102: a conferencia e ACESSORIA, e nao pode derrubar o manifesto ─────────
# 18/09/2026, e o defeito e meu, do mesmo dia em que escrevi o arquivo acima.
#
# Eu liguei `acervos_sem_regime` ao `main()` sem guarda. Em `tmp_path` o
# `raiz_do_repositorio` acha o `pyproject.toml` FALSO que o teste cria, a politica nao
# existe ali, e o `FileNotFoundError` subiu -- derrubando TRES testes do
# `test_manifesto_cvm.py` que nao tinham nada a ver com P7 nenhuma. Eles foram
# commitados e EMPURRADOS vermelhos, no primeiro push da historia do repositorio.
#
# Sao dois erros, e o segundo vale mais que o primeiro:
#
#   1. eu rodei so o meu teste novo, nao a suite de `fase0`. E o passo 5 do protocolo
#      §9 -- *"pytest, o juri, nunca o guia"* -- pulado por quem escreveu o protocolo
#      na resposta anterior;
#
#   2. uma guarda ACESSORIA derrubou o TRABALHO que ela existe para proteger. O comando
#      grava o retrato de procedencia; conferir a P7 e um extra que eu pendurei nele.
#      Extra que mata o principal inverteu o proprio proposito -- e num instrumento cuja
#      unica funcao e nao perder procedencia, cair e a pior saida possivel.
#
# E a correcao NAO e engolir o erro: isso seria o E-02, arquivo ausente virando "nada
# declarado". E avisar que a conferencia nao rodou, e deixar o retrato de pe.

def _acervo_falso(tmp_path, com_politica):
    (tmp_path / "pyproject.toml").write_text("[project]\n", encoding="utf-8")
    ac = tmp_path / "data" / "b3"
    ac.mkdir(parents=True)
    import zipfile
    with zipfile.ZipFile(ac / "x.zip", "w") as z:
        z.writestr("a.csv", "c1;c2\n1;2\n")
    if com_politica:
        pol = tmp_path / "alocacao"
        pol.mkdir()
        (pol / "politica.yaml").write_text(yaml.safe_dump({"limitacoes_declaradas": {
            "lim": {"acervos": ["b3"], "direcao_do_vies": "x",
                    "quando_deixa_de_importar": "y", "fonte": "z"}}}), encoding="utf-8")
    return ac


def test_P102_sem_politica_o_MANIFESTO_continua_de_pe(tmp_path, capsys):
    """O portao. Falha contra a versao de 18/09, que subia FileNotFoundError daqui."""
    ac = _acervo_falso(tmp_path, com_politica=False)
    assert m.main(["--manifesto", str(ac)]) == 0, "o retrato e o trabalho; ele nao cai"
    saida = capsys.readouterr()
    assert "manifesto:" in saida.out
    assert (tmp_path / "docs" / "acervo" / "b3").exists()


def test_P102_sem_politica_a_conferencia_AVISA_que_nao_rodou(tmp_path, capsys):
    """Nao rodar em silencio seria o F-02 na camada do relato: ausencia de acusacao lida
    como "esta tudo declarado". O aviso separa *conferi e esta certo* de *nao consegui
    conferir* -- e e a P5 aplicada ao proprio instrumento."""
    ac = _acervo_falso(tmp_path, com_politica=False)
    m.main(["--manifesto", str(ac)])
    err = capsys.readouterr().err
    assert "a conferencia da P7 NAO rodou" in err
    assert "sem regime de captura declarado" not in err, \
        "sem politica nao se AFIRMA que falta regime -- nao se sabe"


def test_P102_com_politica_a_conferencia_roda_de_verdade(tmp_path, capsys):
    """Prova por mutacao do aviso: com a politica presente ele SOME e a conferencia
    acontece. Aviso que nunca some e ruido; conferencia que nunca roda e enfeite."""
    ac = _acervo_falso(tmp_path, com_politica=True)
    assert m.main(["--manifesto", str(ac)]) == 0
    err = capsys.readouterr().err
    assert "a conferencia da P7 NAO rodou" not in err
    assert "sem regime de captura declarado" not in err


def test_P102_politica_ausente_NAO_e_lida_como_nada_declarado(tmp_path):
    """E-02, decidido por ele em 12/09: ausente e vazio sao coisas diferentes. A funcao
    LEVANTA em vez de devolver (set(), set()) -- devolver o par vazio seria afirmar
    "conferi, nenhum acervo sem regime" sobre um arquivo que nunca foi aberto."""
    (tmp_path / "pyproject.toml").write_text("[project]\n", encoding="utf-8")
    with pytest.raises(m.PoliticaAusente):
        m.acervos_sem_regime(str(tmp_path))


def test_P150_eventos_b3_tem_cadencia_com_motivo_e_limitacao_ate_o_cron_provar():
    """26/09/2026, P-150. Falha na versao anterior: a politica nao declarava cadencia nenhuma
    para os eventos da B3. O acervo fica em limitacao (NAO_CONSERTADA, P-150) ate a primeira
    execucao verde; so entao entra em `regimes_de_captura`, que exige a execucao."""
    P = _politica()
    c = P["cadencias_de_captura"]["b3_eventos"]
    assert c["dia_da_semana"] in ("segunda", "terca", "quarta", "quinta", "sexta")
    assert len(c["motivo"].split()) >= 20
    cobre = [lim for lim in P["limitacoes_declaradas"].values()
             if "b3_eventos" in (lim.get("acervos") or [])]
    assert len(cobre) == 1 and cobre[0]["pendencia"] == "P-150"
    assert cobre[0]["tipo"] == "NAO_CONSERTADA"
    assert "b3_eventos" not in P["regimes_de_captura"]
    assert os.path.isfile(os.path.join(RAIZ, "docs", "acervo", "b3_eventos", "capturas.csv"))


# ── P-150: regime automatico sem registro em acervo.REGISTROS e captura sem vigia ──

import acervo  # noqa: E402


@pytest.mark.repositorio
def test_P150_todo_regime_tem_o_registro_em_acervo_REGISTROS():
    """P7, a lacuna do #32. `acervo.frescor()` e `abrir()` so leem os registros de
    `acervo.REGISTROS`: um acervo que entrasse em `regimes_de_captura` (o `b3_eventos`,
    quando o cron provar) sem entrar ali seria captura automatica que ninguem vigia -- se
    ela parar, nada acusa."""
    assert acervo.regimes_sem_registro(RAIZ) == []


def test_P150_mutacao_b3_eventos_no_regime_e_fora_de_REGISTROS_e_ACUSADO(tmp_path):
    reg = "docs/acervo/b3_eventos/capturas.csv"
    raiz = _com_regime(tmp_path, {"b3_eventos": {
        "regime": "AUTOMATICO", "executor": ".github/workflows/c.yml",
        "passo": "captura", "registro": reg}})
    assert acervo.regimes_sem_registro(raiz) == ["b3_eventos"]
    com = dict(acervo.REGISTROS, b3_eventos=os.path.join(*reg.split("/")))
    assert acervo.regimes_sem_registro(raiz, registros=com) == []


def test_P150_regime_sem_campo_registro_tambem_e_acusado(tmp_path):
    raiz = _com_regime(tmp_path, {"x": {"regime": "AUTOMATICO"}})
    assert acervo.regimes_sem_registro(raiz) == ["x"]
