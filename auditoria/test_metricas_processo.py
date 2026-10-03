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


def test_regra_de_volta_dispara_no_limiar_e_so_na_janela():
    hoje = M.dt.date(2026, 10, 20)
    um = [_t("2026-10-18", "[modelo=sonnet classe=registro]")]
    dois = um + [_t("2026-10-10", "[modelo=sonnet classe=registro]")]
    assert M.regra_de_volta(um, hoje) == {}
    assert M.regra_de_volta(dois, hoje) == {"registro": 2}
    # mutacao: o segundo evento fora da janela de 14 dias nao conta
    velho = um + [_t("2026-10-05", "[modelo=sonnet classe=registro]")]
    assert M.regra_de_volta(velho, hoje) == {}


def test_regra_de_volta_nao_conta_o_modelo_de_cima_nem_desconhecido():
    hoje = M.dt.date(2026, 10, 20)
    ev = [_t("2026-10-18", "[modelo=opus classe=registro]")] * 3
    ev += [_t("2026-10-18", "[modelo=desconhecido classe=registro]")] * 3
    assert M.regra_de_volta(ev, hoje) == {}


def test_a_tabela_tem_as_classes_da_decisao_e_fable_fora():
    m = M.ler_modelos()
    assert m["classes"]["registro"] == "sonnet" and m["classes"]["engenharia"] == "opusplan"
    assert m["classes"]["p-115"] == "opus" and "fable" not in m["ordem"]
