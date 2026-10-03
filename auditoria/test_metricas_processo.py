# -*- coding: utf-8 -*-
"""O registro de erros e o resumo semanal. O primeiro teste e o pedido: evento sem codigo
reprova."""
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import metricas_processo as M  # noqa: E402


def _e(**kw):
    base = dict(data="2026-09-25", codigo="CV-07", tipo="achado", autor="claude-code",
                quem_achou="claude-code", regua="desconhecido", commit_introduziu="x",
                commit_corrigiu="aberto", descricao="d")
    base.update(kw)
    return base


def test_evento_SEM_CODIGO_reprova():
    with pytest.raises(M.EventoInvalido, match="sem codigo"):
        M.validar([_e(codigo="  ")])


def test_valor_fora_da_lista_e_campo_vazio_reprovam():
    with pytest.raises(M.EventoInvalido, match="tipo"):
        M.validar([_e(tipo="bug")])
    with pytest.raises(M.EventoInvalido, match="quem_achou"):
        M.validar([_e(quem_achou="gpt")])
    with pytest.raises(M.EventoInvalido, match="desconhecido"):
        M.validar([_e(regua="")])


def test_por_semana_conta_retratacao_por_autor_e_a_fracao_do_osvaldo():
    ev = [_e(data="2026-09-18", tipo="retratacao", autor="claude-chat", quem_achou="osvaldo"),
          _e(data="2026-09-19", tipo="reincidencia"),
          _e(data="2026-09-25")]
    s = M.por_semana(ev)
    assert s["2026-S38"]["retratacoes"] == {"claude-chat": 1}
    assert s["2026-S38"]["reincidencias"] == 1 and s["2026-S38"]["achados_osvaldo"] == 1
    assert "50% (1 de 2)" in M.relatorio(ev, None)


def test_sem_sessoes_o_relatorio_DIZ_que_nao_mediu(tmp_path):
    assert M.sessoes_por_semana(str(tmp_path / "nao.csv")) is None
    assert "NAO medida" in M.relatorio([_e()], None)


def test_o_eventos_csv_do_repositorio_e_valido():
    ev = M.validar(M.ler())
    assert len(ev) >= 39 and all(e["codigo"] for e in ev)


# ── 02/10/2026: o modelo no evento, e a regra de volta ─────────────────────────────

def _t(data, etiqueta, autor="claude-code"):
    return _e(data=data, autor=autor, descricao=f"{etiqueta} texto")


def test_evento_claude_novo_sem_etiqueta_reprova_e_o_antigo_nao():
    M.validar([_e(data="2026-10-02")])                      # antes da regra: passa
    with pytest.raises(M.EventoInvalido, match="modelo="):
        M.validar([_e(data="2026-10-03")])
    M.validar([_e(data="2026-10-03", autor="osvaldo")])     # erro dele nao tem modelo
    M.validar([_t("2026-10-03", "[modelo=sonnet classe=registro]")])


def test_etiqueta_fora_da_tabela_reprova():
    with pytest.raises(M.EventoInvalido, match="fora de"):
        M.validar([_t("2026-10-03", "[modelo=fable classe=registro]")])
    with pytest.raises(M.EventoInvalido, match="fora de"):
        M.validar([_t("2026-10-03", "[modelo=sonnet classe=faxina]")])


def test_a_tabela_tem_as_classes_da_decisao_e_fable_fora():
    m = M.ler_modelos()
    assert m["classes"]["registro"] == "sonnet" and m["classes"]["engenharia"] == "opusplan"
    assert m["classes"]["p-115"] == "opus" and "fable" not in m["ordem"]


# ── 03/10/2026: a regra de volta por taxa contra a referencia (fila, decisao 21d) ─────────
# Dados sinteticos. A tabela e a do repositorio; a regra vem num dict proprio, para o teste nao
# mudar de sentido quando ele mexer no 1,5 ou no 4 do YAML.

HOJE = M.dt.date(2026, 10, 20)
REGRA = dict(janela_dias=14, fator=1.5, min_prs=4, min_eventos=2)


def _modelos(**regra):
    m = M.ler_modelos()
    m["regra_de_volta"] = {**m["regra_de_volta"], **REGRA, **regra}
    return m


def _pr(data, etiqueta="[modelo=sonnet classe=registro]", n=1):
    return dict(numero=n, titulo=f"{etiqueta} titulo", autor="OsvaldoSantana", data=data)


def _ev(k, data="2026-10-18", etq="[modelo=sonnet classe=registro]"):
    return [_t(data, etq)] * k


def _volta(eventos, prs, ref, **regra):
    return M.regra_de_volta(eventos, prs, HOJE, ref, _modelos(**regra))["registro"]


# referencia sintetica: 1 evento em 3 PRs -> (1 + 1) / (3 + 1) = 0,5. O limiar e 1,5 x 0,5 = 0,75.
REF = {"registro": (1, 3)}


def test_21d_volta_quando_a_taxa_PASSA_de_1_5_vez_a_referencia():
    prs = [_pr("2026-10-15")] * 4
    v = _volta(_ev(4), prs, REF)                        # 4/4 = 1,0 > 0,75
    assert v["volta"] and v["taxa"] == 1.0 and v["ref"] == 0.5
    # mutacao `>` -> `>=`: 3/4 = 0,75 e exatamente 1,5 x 0,5, e "passa de" e estrito
    assert not _volta(_ev(3), prs, REF)["volta"]


def test_21d_nao_volta_com_menos_de_4_PRs_da_classe_na_janela():
    # mutacao `>= min_prs` -> `> min_prs` ou o 4 trocado por 3: 3 PRs com taxa 2,0 nao voltam,
    # e 4 PRs com a mesma taxa voltam
    assert not _volta(_ev(6), [_pr("2026-10-15")] * 3, REF)["volta"]
    assert _volta(_ev(8), [_pr("2026-10-15")] * 4, REF)["volta"]


def test_21d_referencia_zero_nao_tem_regua_zero_e_um_evento_so_nao_volta():
    # (0 + 1) / (6 + 1) = 1/7; limiar 1,5/7 = 0,214. 1 evento em 4 PRs = 0,25 > limiar, mas e UM
    # evento so. Mutacao: tirar o `+ 1` da referencia (regua 0) ou o `min_eventos` -> volta.
    ref0 = {"registro": (0, 6)}
    prs = [_pr("2026-10-15")] * 4
    v = _volta(_ev(1), prs, ref0)
    assert v["ref"] == 1 / 7 and v["taxa"] == 0.25 and not v["volta"]
    assert _volta(_ev(2), prs, ref0)["volta"]            # dois eventos: volta
    # o minimo vem do YAML (P2): com min_eventos 1 o mesmo caso volta
    assert _volta(_ev(1), prs, ref0, min_eventos=1)["volta"]


def test_21d_classe_sem_PR_na_referencia_tem_regua_1_e_o_relatorio_mostra():
    # (0 + 1) / (0 + 1) = 1,0: limiar 1,5; 9 eventos em 5 PRs = 1,8 volta, 7 em 5 = 1,4 nao
    prs = [_pr("2026-10-15")] * 5
    assert _volta(_ev(9), prs, {"registro": (0, 0)})["volta"]
    assert not _volta(_ev(7), prs, {"registro": (0, 0)})["volta"]
    v = _volta(_ev(9), prs, {"registro": (0, 0)})
    assert "1.00 (0 / 0)" in M.relatorio_volta({"registro": v}, [], HOJE, _modelos())


def test_21d_a_janela_vale_para_o_evento_E_para_o_PR():
    # 07/10 dentro; 06/10 (14 dias antes de 20/10) fora: a janela e (hoje-14, hoje]
    dentro = [_pr("2026-10-07")] * 4
    assert _volta(_ev(4, data="2026-10-07"), dentro, REF)["volta"]
    assert not _volta(_ev(4, data="2026-10-06"), dentro, REF)["volta"]
    assert _volta(_ev(4), [_pr("2026-10-06")] * 4, REF)["prs"] == 0


def test_21d_so_conta_modelo_abaixo_do_topo_nos_dois_lados():
    prs = [_pr("2026-10-15")] * 4
    opus = _ev(8, etq="[modelo=opus classe=registro]")
    desc = _ev(8, etq="[modelo=desconhecido classe=registro]")
    assert _volta(opus + desc, prs, REF)["eventos"] == 0
    assert _volta(_ev(8), [_pr("2026-10-15", "[modelo=opus classe=registro]")] * 4, REF)["prs"] == 0
    # PR sem etiqueta nao entra no denominador, e o relatorio conta quantos ficaram fora
    sem = [_pr("2026-10-15", etiqueta="Sem etiqueta")]
    assert "sem etiqueta, fora da conta (Dependabot excluido): 1" in M.relatorio_volta(
        {}, sem, HOJE, _modelos())


def test_21d_o_fator_e_o_minimo_sao_lidos_do_YAML_e_nao_do_codigo():
    """P2: com fator 2,5 a mesma taxa de 1,0 contra 0,5 deixa de voltar."""
    prs = [_pr("2026-10-15")] * 4
    assert _volta(_ev(4), prs, REF)["volta"]
    assert not _volta(_ev(4), prs, REF, fator=2.5)["volta"]
    assert not _volta(_ev(4), prs, REF, min_prs=5)["volta"]


def test_21d_a_referencia_conta_so_entre_desde_e_ate():
    m = _modelos()
    linhas = [dict(tipo="evento", data="2026-09-24", classe="registro"),   # antes do 1o PR
              dict(tipo="evento", data="2026-09-25", classe="registro"),
              dict(tipo="pr", data="2026-10-02", classe="registro"),
              dict(tipo="pr", data="2026-10-03", classe="registro")]       # depois do fim
    assert M.referencia(linhas, m)["registro"] == (1, 1)
    assert M.referencia(linhas, m)["estatistica"] == (0, 0)


def test_21d_titulo_de_PR_sem_etiqueta_ou_fora_da_tabela_reprova():
    assert M.validar_titulo("[modelo=sonnet classe=registro] Fila 21") == ("sonnet", "registro")
    for ruim in ("Fila 21", "[modelo=fable classe=registro] x", "[modelo=sonnet classe=faxina] x"):
        with pytest.raises(M.EventoInvalido):
            M.validar_titulo(ruim)
    assert M.main(["--titulo-pr", "Fila 21"]) == 1


def test_21d_mergedAt_em_UTC_vira_a_data_de_Brasilia(tmp_path):
    f = tmp_path / "prs.json"
    # o PR #34: mergeado as 22:12 de 26/09 em Brasilia, 01:12 de 27/09 em UTC
    f.write_text('[{"number": 34, "title": "x", "mergedAt": "2026-09-27T01:12:25Z", '
                 '"author": {"login": "OsvaldoSantana"}}]', encoding="utf-8")
    assert M.prs_do_gh(str(f))[0]["data"] == "2026-09-26"


# ── a referencia do repositorio: classificada uma vez, e inteira ────────────────────────

def _asc(s):
    import unicodedata
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().replace(";", ",")


def test_21d_a_referencia_classifica_TODO_evento_Claude_de_16_09_a_02_10_uma_vez():
    """Evento que falta some do numerador da referencia e deixa a regra mais sensivel calado."""
    linhas = [r for r in M.ler_referencia() if r["tipo"] == "evento"]
    alvo = [e for e in M.ler() if e["autor"].startswith("claude")
            and "2026-09-16" <= e["data"] <= "2026-10-02"]
    usados = set()
    for r in linhas:
        casa = [k for k, e in enumerate(alvo) if k not in usados and e["data"] == r["data"]
                and e["codigo"] == r["id"] and _asc(e["descricao"]).startswith(r["trecho"])]
        assert casa, r
        usados.add(casa[0])
    assert len(usados) == len(alvo) == len(linhas) == 27


def test_21d_a_referencia_so_usa_classes_da_tabela_e_PR_sem_repeticao():
    m = M.ler_modelos()
    linhas = M.ler_referencia()
    assert {r["classe"] for r in linhas} <= set(m["classes"])
    assert {r["tipo"] for r in linhas} == {"evento", "pr"}
    prs = [r["id"] for r in linhas if r["tipo"] == "pr"]
    assert len(prs) == len(set(prs)) == 37
    assert m["regra_de_volta"]["referencia"]["status"] == "OBSERVADO"
