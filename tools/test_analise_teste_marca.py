# -*- coding: utf-8 -*-
"""A regra do teste de marca, provada sobre respostas SINTETICAS antes de existir resposta real.

Nada aqui e dado de pessoa: as notas sao geradas com semente fixa para cada caso.
"""
from __future__ import annotations

import csv
import datetime as dt
import io
import os
import re
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import analise_teste_marca as AT  # noqa: E402

RAIZ = AT.RAIZ


def _pessoas(medias: dict[str, dict[str, float]], n: int = 40, semente: int = 1,
             amigo: bool = False, rota: dict[str, dict[str, float]] | None = None
             ) -> list[AT.Resposta]:
    """n pessoas com notas em torno das medias dadas (ruido +-1), cortadas em 1..7."""
    rng = np.random.default_rng(semente)
    out = []
    for i in range(n):
        r = AT.Resposta(versao=1 + i % 6, amigo=amigo)
        for d in AT.DIRECOES:
            for ve, fonte in (("base", medias), ("rota", rota or medias)):
                r.notas[(d, ve)] = {
                    esc: int(np.clip(round(fonte[d].get(esc, 4) + rng.integers(-1, 2)), 1, 7))
                    for esc in AT.ESCALAS}
        out.append(r)
    return out


def M(confiavel: float, para_mim: float, honesto: float) -> dict[str, float]:
    return {"confiavel": confiavel, "para_mim": para_mim, "honesto": honesto}


# --- os tres casos pedidos ----------------------------------------------------------------

def caso_e_vence(at=AT):
    rs = _pessoas({"E": M(6, 6, 6), "C": M(4, 4, 5), "D": M(3, 3, 2)})
    r = at.decidir(rs)
    assert r["resultado"] == "VENCE" and r["vencedora"] == "E", r
    assert r["fora_por_honesto"] == ["D"]
    return r


def caso_empate(at=AT):
    """Empate construido, nao sorteado: pessoa a pessoa, a C e a E mais 1 numa metade e menos
    1 na outra, entao a diferenca pareada media e zero e o IC a contem."""
    rs = _pessoas({"E": M(4, 4, 5), "C": M(4, 4, 5), "D": M(3, 3, 2)}, semente=7)
    for i, r in enumerate(rs):
        passo = 1 if i % 2 == 0 else -1
        r.notas[("C", "base")] = {k: v + passo if k in ("confiavel", "para_mim") else v
                                  for k, v in r.notas[("E", "base")].items()}
    r = at.decidir(rs)
    assert r["resultado"] == "EMPATE", r
    lo, hi = r["ic"]
    assert lo <= 0 <= hi
    return r


def caso_honesto_exclui_a_maior_media(at=AT):
    """A D tem o MAIOR indice, mas a pior media em honesto: sai, e a E vence entre E e C."""
    rs = _pessoas({"E": M(5.5, 5.5, 5), "C": M(4, 4, 5), "D": M(6.5, 6.5, 1.5)}, semente=3)
    r = at.decidir(rs)
    assert max(r["media_indice"], key=r["media_indice"].get) == "D", "pre-condicao do caso"
    assert r["fora_por_honesto"] == ["D"]
    assert r["resultado"] == "VENCE" and r["vencedora"] == "E", r
    return r


def test_caso_e_vence():
    caso_e_vence()


def test_caso_empate():
    caso_empate()


def test_caso_honesto_exclui_a_vencedora_por_media():
    caso_honesto_exclui_a_maior_media()


# --- a guarda falha quando a regra e trocada (regua 5-B, pergunta 4) ------------------------

def test_mutacao_sem_a_regra_do_honesto_o_caso_reprova(monkeypatch):
    """Sem a exclusao pelo honesto, a D venceria: o caso tem de reprovar."""
    monkeypatch.setattr(AT, "_pior_em_honesto", lambda medias: [])
    with pytest.raises(AssertionError):
        caso_honesto_exclui_a_maior_media()


def test_mutacao_honesto_invertido_o_caso_reprova(monkeypatch):
    """Excluir a MELHOR em honesto (a regra do avesso) tambem tem de reprovar."""
    monkeypatch.setattr(AT, "_pior_em_honesto",
                        lambda medias: [max(medias, key=medias.get)])
    with pytest.raises(AssertionError):
        caso_e_vence()


def test_mutacao_empate_ignorado_o_caso_reprova(monkeypatch):
    """Se o IC nao fosse consultado (vence a maior media sempre), o empate sumiria."""
    monkeypatch.setattr(AT, "ic_diferenca",
                        lambda a, b: (float((a - b).mean()), 0.01, 0.02))
    with pytest.raises(AssertionError):
        caso_empate()


def test_mutacao_indice_so_de_confiavel_muda_o_resultado(monkeypatch):
    """q-a: o indice e confiavel E para_mim. Com so confiavel, este caso vira outro."""
    rs = _pessoas({"E": M(5, 7, 5), "C": M(6, 3, 5), "D": M(3, 3, 2)}, semente=5)
    certo = AT.decidir(rs)
    real = AT._matriz

    def so_confiavel(respostas, ve, medida):
        return real(respostas, ve, "confiavel" if medida == "indice" else medida)

    monkeypatch.setattr(AT, "_matriz", so_confiavel)
    errado = AT.decidir(rs)
    assert certo.get("vencedora") == "E"
    assert errado.get("vencedora") != "E"


# --- o resto do que foi decidido -------------------------------------------------------

def test_sem_amigos_decide_e_com_todos_e_sensibilidade():
    """r-a: amigos que so elogiam a D nao mudam a decisao; mudam a sensibilidade."""
    estranhos = _pessoas({"E": M(6, 6, 6), "C": M(4, 4, 5), "D": M(3, 3, 3)}, n=30)
    amigos = _pessoas({"E": M(1, 1, 5), "C": M(1, 1, 5), "D": M(7, 7, 7)}, n=60, amigo=True,
                      semente=9)
    rel = AT.analisar(estranhos + amigos)
    assert rel["sem_amigos_DECIDE"]["regra"]["vencedora"] == "E"
    assert rel["com_todos_SENSIBILIDADE"]["regra"].get("vencedora") != "E"
    assert rel["n_amigos"] == 60


def test_h1_e_h2_sobre_o_caso_em_que_a_e_vence():
    h = AT.hipoteses(_pessoas({"E": M(6, 6, 6), "C": M(5, 5, 5), "D": M(3, 3, 2)}))
    assert h["H1"]["resultado"] == "CONFIRMADA"
    assert h["H2"]["resultado"] == "CONFIRMADA"
    assert h["H4"].startswith("fora do teste")


def test_h2_nao_confirma_se_a_d_so_perde_para_uma():
    """t-a: a D tem de ser pior que a E E pior que a C."""
    h = AT.hipoteses(_pessoas({"E": M(6, 6, 6), "C": M(3, 3, 3), "D": M(3, 3, 3)}, semente=11))
    assert h["H2"]["resultado"] == "NAO_CONFIRMADA"


def test_h3_e_exploratoria_e_mede_rota_menos_base():
    rs = _pessoas({"E": M(5, 5, 5), "C": M(5, 5, 5), "D": M(5, 5, 5)},
                  rota={"E": M(2, 5, 5), "C": M(5, 5, 5), "D": M(5, 5, 5)}, semente=13)
    h3 = AT.hipoteses(rs)["H3"]
    assert h3["exploratoria"] is True and h3["ordem_fixa"] == "base antes"
    assert h3["direcoes"]["E"]["leitura"] == "reduz"
    assert h3["direcoes"]["C"]["leitura"] == "sem evidencia de reducao"


def test_semente_e_reamostragens_declaradas_e_resultado_reprodutivel():
    assert AT.REAMOSTRAGENS == 10_000 and AT.SEMENTE == 20260927 and AT.NIVEL == 0.95
    rs = _pessoas({"E": M(5, 5, 5), "C": M(4.6, 4.6, 5), "D": M(3, 3, 2)}, semente=17)
    assert AT.decidir(rs) == AT.decidir(rs)


def test_menos_de_duas_pessoas_nao_decide():
    assert AT.decidir([])["resultado"] == "SEM_DADOS"


# --- a exportacao da pagina, a janela e a privacidade ------------------------------------------

def _linha(versao, aberta, concluida, consent="sim", filtro="sim", amigo="nao", nota=5):
    """Uma linha do contrato: notas iguais em todas as escalas e telas (so a leitura importa)."""
    val = {"id_resposta": f"r{versao}{aberta}{concluida}", "versao": str(versao),
           "aberta_em": aberta, "concluida_em": concluida, "consentimento": consent,
           "filtro": filtro, "amigo": amigo, "pronuncia": ""}
    out = []
    for c in AT.colunas_esperadas():
        if c in val:
            out.append(val[c])
        elif c.endswith("_lembra"):
            out.append("")
        else:
            out.append("" if not concluida else str(nota))
    return out


def _csv(path, linhas, cabecalho=None):
    with io.open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(cabecalho or AT.colunas_esperadas())
        w.writerows(linhas)


def test_janela_de_21_dias_filtros_e_abandono_por_versao(tmp_path):
    """h-A: do dia 1 ao dia 21, inclusive, pelo dia da conclusao. Fora da janela, sem
    consentimento ou fora do filtro: guardada no CSV e fora da analise. ab-a: abandono conta
    por versao."""
    assert AT.janela(dt.date(2026, 10, 5)) == (dt.date(2026, 10, 5), dt.date(2026, 10, 25))
    p = tmp_path / "respostas.csv"
    _csv(p, [
        _linha(3, "2026-10-05", "2026-10-05"),                      # dia 1: entra
        _linha(3, "2026-10-25", "2026-10-25", amigo="sim"),         # dia 21: entra
        _linha(1, "2026-10-25", "2026-10-26"),                      # abriu no 21, concluiu no 22
        _linha(2, "2026-10-04", "2026-10-04"),                      # antes do dia 1
        _linha(4, "2026-10-06", "2026-10-06", consent="nao"),
        _linha(5, "2026-10-06", "2026-10-06", filtro="nao"),
        _linha(6, "2026-10-06", ""),                                 # abandono
        _linha(6, "2026-10-07", ""),                                 # abandono
    ])
    rs, c = AT.ler(str(p), dt.date(2026, 10, 5))
    assert (c["aberturas"], c["abandonos"], c["sem_consentimento"], c["fora_do_filtro"],
            c["fora_da_janela"], c["validas"]) == (8, 2, 1, 1, 2, 2)
    assert c["abandonos_por_versao"][6] == 2 and c["aberturas_por_versao"][3] == 2
    assert [r.versao for r in rs] == [3, 3] and [r.amigo for r in rs] == [False, True]
    # versao 3 = C, E, D: a tela 1 e a C na base, a tela 4 e a C com rota bloqueada
    assert set(rs[0].notas) == {(d, v) for d in "CED" for v in ("base", "rota")}


def test_mutacao_resposta_fora_da_janela_nao_pode_entrar(tmp_path, monkeypatch):
    """Se a janela fosse ignorada, a resposta do dia 22 entraria: a guarda tem de ver."""
    p = tmp_path / "respostas.csv"
    _csv(p, [_linha(1, "2026-10-05", "2026-10-05"), _linha(1, "2026-10-26", "2026-10-26")])
    assert AT.ler(str(p), dt.date(2026, 10, 5))[1]["validas"] == 1
    monkeypatch.setattr(AT, "janela", lambda inicio: (dt.date(1900, 1, 1), dt.date(2999, 1, 1)))
    assert AT.ler(str(p), dt.date(2026, 10, 5))[1]["validas"] == 2


def test_tela_k_vai_para_a_direcao_da_ordem_da_versao(tmp_path):
    """g-B: a tela k da versao v e a direcao ORDENS[v][(k-1) % 3]; base ate a 3, rota depois."""
    p = tmp_path / "respostas.csv"
    linha = _linha(5, "2026-10-05", "2026-10-05")          # versao 5 = D, E, C
    ix = AT.colunas_esperadas().index
    linha[ix("t1_confiavel")] = "1"                         # tela 1: D base
    linha[ix("t5_confiavel")] = "7"                         # tela 5: E rota
    _csv(p, [linha])
    r = AT.ler(str(p), dt.date(2026, 10, 5))[0][0]
    assert r.notas[("D", "base")]["confiavel"] == 1 and r.notas[("E", "rota")]["confiavel"] == 7


def test_cabecalho_fora_do_contrato_reprova(tmp_path):
    p = tmp_path / "respostas.csv"
    cab = AT.colunas_esperadas()
    _csv(p, [], cabecalho=cab[:-1] + ["ip"])
    with pytest.raises(SystemExit):
        AT.ler(str(p), None)
    assert AT.conferir_cabecalho(list(reversed(cab))) == ["colunas fora da ordem do contrato"]


def test_contrato_nao_tem_coluna_que_identifica():
    proibidas = {"ip", "email", "e_mail", "nome", "user_agent", "hora"}
    assert not proibidas & {c.lower() for c in AT.colunas_esperadas()}


def test_data_com_hora_viola_o_contrato(tmp_path):
    """O contrato grava so o dia: uma data com hora e recusada, e a conferencia a pega."""
    p = tmp_path / "respostas.csv"
    _csv(p, [_linha(1, "2026-10-05T14:03:22-03:00", "2026-10-05")])
    with pytest.raises(SystemExit):
        AT.main(["--arquivo", str(p), "--conferir-cabecalho"])


def test_analise_nao_roda_antes_do_fim_da_janela(tmp_path, capsys):
    """h-A, "nunca encerrar olhando o resultado": ate o fim do dia 21 o script recusa a
    analise. Sem esta guarda, a regra dependeria de alguem lembrar (P7)."""
    p = tmp_path / "respostas.csv"
    _csv(p, [_linha(1, "2026-10-06", "2026-10-06", nota=n) for n in (3, 5, 6)])
    args = ["--arquivo", str(p), "--inicio", "2026-10-05"]
    assert AT.main(args, hoje=dt.date(2026, 10, 25)) == 3
    assert "regra:" not in capsys.readouterr().out
    assert AT.main(args, hoje=dt.date(2026, 10, 26)) == 0
    assert "sem_amigos_DECIDE (n=3)" in capsys.readouterr().out


def test_csv_dentro_do_repositorio_e_fora_do_ignore_e_recusado():
    """Resposta real nunca entra no git: um CSV que o git nao ignora e recusado."""
    assert AT._dentro_do_git_sem_ignorar(os.path.join(RAIZ, "docs", "respostas.csv"))
    assert not AT._dentro_do_git_sem_ignorar(os.path.join(RAIZ, "data", "teste-marca",
                                                          "respostas.csv"))


def test_nenhuma_resposta_real_no_repositorio():
    """Ate o teste rodar, nenhuma exportacao pode existir fora de data/ (ignorado)."""
    achados = []
    for base, dirs, arqs in os.walk(RAIZ):
        dirs[:] = [d for d in dirs if d not in (".git", "data", "node_modules")]
        achados += [os.path.join(base, a) for a in arqs
                    if re.fullmatch(r"respostas.*\.csv|versao-\d\.csv", a)]
    assert achados == []


def test_descritivas_trazem_as_cinco_escalas_nas_seis_telas():
    rel = AT.analisar(_pessoas({"E": M(6, 6, 6), "C": M(4, 4, 5), "D": M(3, 3, 2)}))
    desc = rel["sem_amigos_DECIDE"]["descritivas"]
    assert set(desc) == {f"{d}-{v}" for d in AT.DIRECOES for v in ("base", "rota")}
    assert all(set(m) == set(AT.ESCALAS) for m in desc.values())


# --- o pre-registro final congela os arquivos pelo sha256 ------------------------------------

PREREGISTRO = os.path.join(RAIZ, "docs", "marca", "teste-de-marca", "preregistro-final.md")
CONGELADOS = {f"docs/marca/direcoes/png/{d}-{v}.png" for d in "ECD"
              for v in ("base", "rota-bloqueada")} | {
    "docs/marca/teste-de-marca/questionario.yaml",
    "docs/marca/teste-de-marca/codigos-visuais.yaml",
    "tools/analise_teste_marca.py"}


def _sha256_gravados(texto: str) -> dict[str, str]:
    """Cada linha de tabela com um caminho entre crases e um sha256 entre crases."""
    par = re.compile(r"`((?:docs|tools)/[^`]+)`.*?`([0-9a-f]{64})`")
    return {m.group(1): m.group(2) for m in map(par.search, texto.splitlines()) if m}


def _divergentes(gravados: dict[str, str]) -> list[str]:
    import hashlib
    out = []
    for rel, h in gravados.items():
        with open(os.path.join(RAIZ, *rel.split("/")), "rb") as f:
            if hashlib.sha256(f.read()).hexdigest() != h:
                out.append(rel)
    return out


def test_preregistro_final_congela_os_nove_arquivos_pelo_sha256():
    """P4: mudar um byte do questionario, do livro de codigos, do script ou de um PNG sem mudar
    o pre-registro no mesmo commit reprova. Mutacao: um sha256 trocado aparece como divergente."""
    with io.open(PREREGISTRO, encoding="utf-8") as f:
        gravados = _sha256_gravados(f.read())
    assert set(gravados) == CONGELADOS
    assert _divergentes(gravados) == []
    mutado = dict(gravados, **{"tools/analise_teste_marca.py": "0" * 64})
    assert _divergentes(mutado) == ["tools/analise_teste_marca.py"]
