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
QUESTIONARIO = os.path.join(RAIZ, "docs", "marca", "teste-de-marca-questionario.md")


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
                    for esc in AT.ESCALAS.values()}
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


# --- o CSV do Forms, a janela e a privacidade -------------------------------------------------

def _csv_sintetico(path, linhas):
    cab = ["Carimbo de data/hora"] + AT.colunas_esperadas()
    with io.open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(cab)
        for carimbo, consent, filtro, amigo, nota in linhas:
            w.writerow([carimbo, consent, filtro, amigo] + [str(nota)] * (6 * len(AT.ESCALAS)))


def test_janela_de_21_dias_e_filtros(tmp_path):
    """h-A: do dia 1 ao dia 21, 23:59:59; fora da janela, sem consentimento ou fora do filtro
    ficam no CSV e fora da analise."""
    ini, fim = AT.janela(dt.date(2026, 10, 5))
    assert (ini, fim) == (dt.datetime(2026, 10, 5, 0, 0, 0), dt.datetime(2026, 10, 25, 23, 59, 59))
    p = tmp_path / "versao-3.csv"
    _csv_sintetico(p, [
        ("05/10/2026 00:00:00", "Concordo", "Sim", "N\u00e3o", 5),
        ("25/10/2026 23:59:59", "Concordo", "Sim", "Sim", 5),
        ("26/10/2026 00:00:00", "Concordo", "Sim", "N\u00e3o", 5),
        ("06/10/2026 10:00:00", "N\u00e3o concordo", "", "", 5),
        ("06/10/2026 10:00:00", "Concordo", "N\u00e3o", "N\u00e3o", 5),
    ])
    rs, c = AT.ler_versao(str(p), dt.date(2026, 10, 5))
    assert c == {"linhas": 5, "sem_consentimento": 1, "fora_do_filtro": 1,
                 "fora_da_janela": 1, "validas": 2}
    assert [r.versao for r in rs] == [3, 3] and [r.amigo for r in rs] == [False, True]
    # versao 3 = C, E, D: a tela 1 e a C na base, a tela 4 e a C com rota bloqueada
    assert set(rs[0].notas) == {(d, v) for d in "CED" for v in ("base", "rota")}


def test_cabecalho_errado_reprova(tmp_path):
    p = tmp_path / "versao-1.csv"
    p.write_text("Carimbo de data/hora,Outra coisa\n", encoding="utf-8")
    with pytest.raises(SystemExit):
        AT.ler_versao(str(p), None)


def test_csv_dentro_do_repositorio_e_fora_do_ignore_e_recusado():
    """Resposta real nunca entra no git: um versao-N.csv que o git nao ignora e recusado."""
    assert AT._dentro_do_git_sem_ignorar(os.path.join(RAIZ, "docs", "versao-1.csv"))
    assert not AT._dentro_do_git_sem_ignorar(os.path.join(RAIZ, "data", "teste-marca",
                                                          "versao-1.csv"))


def test_nenhuma_resposta_real_no_repositorio():
    """Ate o teste rodar, nenhum CSV de resposta pode existir fora de data/ (ignorado)."""
    achados = []
    for base, dirs, arqs in os.walk(RAIZ):
        dirs[:] = [d for d in dirs if d not in (".git", "data", "node_modules")]
        achados += [os.path.join(base, a) for a in arqs if re.fullmatch(r"versao-\d\.csv", a)]
    assert achados == []


# --- o script e o questionario falam a mesma lingua ----------------------------------------

def _texto_questionario() -> str:
    with io.open(QUESTIONARIO, encoding="utf-8") as f:
        return f.read()


def test_titulos_das_escalas_batem_com_o_questionario():
    q = _texto_questionario()
    for titulo, nome in AT.ESCALAS.items():
        assert f"`[Tela k] {titulo}`" in q, titulo
        assert f"`{nome}`" in q, nome
    for fixo in (AT.CONSENTIMENTO, AT.FILTRO, AT.AMIGO):
        assert f"`{fixo}`" in q, fixo


def test_as_seis_ordens_batem_com_o_questionario():
    q = _texto_questionario()
    for v, ordem in AT.ORDENS.items():
        base = ", ".join(ordem)
        assert f"| {v} | {base} | {base} |" in q, v
    assert sorted(AT.ORDENS.values()) == sorted(
        "".join(p) for p in __import__("itertools").permutations("ECD"))


def test_conferir_cabecalho_le_o_carimbo_de_toda_linha(tmp_path):
    """O formato do carimbo do Forms e NAO_CONFIRMADO: o roteiro confere com uma resposta de
    teste ("Nao concordo", descartada na analise). Formato desconhecido para o script."""
    _csv_sintetico(tmp_path / "versao-2.csv",
                   [("06/10/2026 10:00:00", "N\u00e3o concordo", "", "", 1)])
    assert AT.main(["--pasta", str(tmp_path), "--conferir-cabecalho"]) == 0
    _csv_sintetico(tmp_path / "versao-2.csv",
                   [("2026-10-06T10:00:00Z", "N\u00e3o concordo", "", "", 1)])
    with pytest.raises(SystemExit):
        AT.main(["--pasta", str(tmp_path), "--conferir-cabecalho"])


def test_analise_nao_roda_antes_do_fim_da_janela(tmp_path, capsys):
    """h-A, "nunca encerrar olhando o resultado": ate 23:59:59 do dia 21 o script recusa a
    analise. Sem esta guarda, a regra dependeria de alguem lembrar (P7)."""
    linhas = [("06/10/2026 10:00:00", "Concordo", "Sim", "N\u00e3o", n) for n in (3, 5, 6)]
    _csv_sintetico(tmp_path / "versao-1.csv", linhas)
    args = ["--pasta", str(tmp_path), "--inicio", "2026-10-05"]
    assert AT.main(args, agora=dt.datetime(2026, 10, 25, 23, 59, 59)) == 3
    assert "regra:" not in capsys.readouterr().out
    assert AT.main(args, agora=dt.datetime(2026, 10, 26, 0, 0, 0)) == 0
    assert "sem_amigos_DECIDE (n=3)" in capsys.readouterr().out


def test_descritivas_trazem_as_cinco_escalas_nas_seis_telas():
    rel = AT.analisar(_pessoas({"E": M(6, 6, 6), "C": M(4, 4, 5), "D": M(3, 3, 2)}))
    desc = rel["sem_amigos_DECIDE"]["descritivas"]
    assert set(desc) == {f"{d}-{v}" for d in AT.DIRECOES for v in ("base", "rota")}
    assert all(set(m) == set(AT.ESCALAS.values()) for m in desc.values())


# --- o pre-registro final congela os arquivos pelo sha256 ------------------------------------

PREREGISTRO = os.path.join(RAIZ, "docs", "marca", "preregistro-teste-de-marca-final.md")
CONGELADOS = {f"docs/marca/direcoes/png/{d}-{v}.png" for d in "ECD"
              for v in ("base", "rota-bloqueada")} | {
    "docs/marca/teste-de-marca-questionario.md", "tools/analise_teste_marca.py"}


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


def test_preregistro_final_congela_os_oito_arquivos_pelo_sha256():
    """P4: mudar um byte do questionario, do script ou de um PNG sem mudar o pre-registro no
    mesmo commit reprova. Mutacao: um sha256 trocado no texto tem de aparecer como divergente."""
    with io.open(PREREGISTRO, encoding="utf-8") as f:
        gravados = _sha256_gravados(f.read())
    assert set(gravados) == CONGELADOS
    assert _divergentes(gravados) == []
    mutado = dict(gravados, **{"tools/analise_teste_marca.py": "0" * 64})
    assert _divergentes(mutado) == ["tools/analise_teste_marca.py"]
