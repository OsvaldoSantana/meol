# -*- coding: utf-8 -*-
"""P-150: os eventos societarios da B3 no armazem, pela cadencia da politica.

O QUE MEDE (P5): com um coletor falso no lugar do `coletar_b3` (nenhum pedido sai para a
B3), que (1) fora do dia da cadencia nada e pedido; (2) sem a cadencia na politica, recusa;
(3) cada arquivo sobe pela chave de conteudo em `b3/`, e a segunda rodada igual nao sobe
nada; (4) o registro so ganha linha do que mudou, e da rodada com ressalva ou falha;
(5) o teto recusa, com a linha no registro e o passo vermelho; (6) erro da B3 e falha, nao
silencio. NAO mede o endpoint real: isso e o cron do workflow (P-150 fecha com ele verde).
"""
from __future__ import annotations

import datetime as dt
import json
import os
import shutil
import sys
import types

import pytest

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import armazem as armazem_mod  # noqa: E402
import capturar_cvm as C  # noqa: E402
import capturar_eventos_b3 as E  # noqa: E402

SEGUNDA = dt.date(2026, 9, 28)
TERCA = dt.date(2026, 9, 29)


def _politica(tmp_path, cadencia="segunda", motivo="semanal porque o historico vem inteiro"):
    """Uma raiz de repositorio minima: so o que `cadencia()` e o teto leem."""
    real = os.path.join(C.raiz_repo(), "alocacao", "politica.yaml")
    (tmp_path / "alocacao").mkdir()
    import yaml
    with open(real, encoding="utf-8") as f:
        P = yaml.safe_load(f)
    if cadencia is None:
        P.pop("cadencias_de_captura", None)
    else:
        P["cadencias_de_captura"] = {"b3_eventos": {"dia_da_semana": cadencia,
                                                    "motivo": motivo}}
    with open(tmp_path / "alocacao" / "politica.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump(P, f)
    return str(tmp_path)


def _coletor(pedidos, eventos_rc=0, proventos_rc=0, erro=None, conteudo="v1"):
    def _grava(caminho, obj):
        os.makedirs(os.path.dirname(caminho), exist_ok=True)
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(obj, f)

    def coletar_indice(raiz, indice, dia, forcar):
        pedidos.append(("indice", indice))
        if erro:
            raise erro
        _grava(os.path.join(raiz, "indices", f"dt_captura={dia}", f"{indice}.json"),
               {"carteira": ["AAAA", "BBBB"], "v": conteudo})
        return ["AAAA", "BBBB"]

    def coletar_eventos(raiz, tickers, dia, forcar):
        pedidos.append(("eventos", tuple(tickers)))
        for t in tickers:
            _grava(os.path.join(raiz, "eventos", f"dt_captura={dia}", f"{t}.json"),
                   {"t": t, "v": conteudo})
        with open(os.path.join(raiz, "manifesto.jsonl"), "a", encoding="utf-8") as f:
            f.write('{"ok": true}\n')
        return eventos_rc

    def coletar_proventos(raiz, dia, pausa=None):
        pedidos.append(("proventos", pausa))
        _grava(os.path.join(raiz, "proventos", f"dt_captura={dia}", "AAAA",
                            "pagina-001.json"), {"p": 1, "v": conteudo})
        return proventos_rc

    return types.SimpleNamespace(coletar_indice=coletar_indice,
                                 coletar_eventos=coletar_eventos,
                                 coletar_proventos=coletar_proventos)


def _rodar(raiz, registro, arm, hoje, coletor, *extra):
    return E.main(["--armazem", "local", "--registro", registro, "--raiz-repo", raiz,
                   *extra], armazem=arm, hoje=hoje, coletor=coletor, pausa=0)


def test_fora_da_cadencia_nada_e_pedido(tmp_path):
    raiz, pedidos = _politica(tmp_path), []
    arm = armazem_mod.ArmazemMemoria()
    reg = str(tmp_path / "reg.csv")
    assert _rodar(raiz, reg, arm, TERCA, _coletor(pedidos)) == 0
    assert pedidos == [] and arm.listar() == [] and not os.path.exists(reg)


def test_qualquer_dia_roda_fora_da_cadencia(tmp_path):
    raiz, pedidos = _politica(tmp_path), []
    assert _rodar(raiz, str(tmp_path / "r.csv"), armazem_mod.ArmazemMemoria(), TERCA,
                  _coletor(pedidos), "--qualquer-dia") == 0
    assert [p[0] for p in pedidos] == ["indice", "eventos", "proventos"]


@pytest.mark.parametrize("cad,motivo", [(None, "x"), ("feriado", "x"), ("segunda", "")])
def test_sem_cadencia_valida_na_politica_recusa(tmp_path, cad, motivo):
    """P2: cadencia inventada no codigo seria regra fora do dado."""
    raiz = _politica(tmp_path, cad, motivo)
    with pytest.raises(E.CadenciaAusente):
        E.cadencia(raiz)


def test_a_cadencia_real_e_lida_da_politica_do_repositorio():
    dia, motivo = E.cadencia(C.raiz_repo())
    assert E.DIAS[dia] == "segunda" and motivo.strip()


def test_sobe_por_chave_de_conteudo_em_b3_e_a_segunda_rodada_nao_sobe_nada(tmp_path):
    raiz, pedidos = _politica(tmp_path), []
    arm, reg = armazem_mod.ArmazemMemoria(), str(tmp_path / "reg.csv")
    assert _rodar(raiz, reg, arm, SEGUNDA, _coletor(pedidos)) == 0
    dados = [k for k in arm.listar() if not k.startswith("logs/")]
    assert len(dados) == 4 and all(k.startswith("b3/") for k in dados)
    recursos = {k.split("/")[1] for k in dados}
    assert recursos == {"indice_carteira", "eventos_suplemento", "proventos"}
    assert any("/AAAA__pagina-001.json/" in k for k in dados), "a barra vira __"
    for k in dados:
        assert armazem_mod.sha_da_chave(k)
    linhas = C.ler_registro(reg)
    assert [ln["situacao"] for ln in linhas] == [C.NOVO] * 4
    assert any(k.startswith(E.LOGS + "/") and "manifesto" in k for k in arm.listar())

    assert _rodar(raiz, reg, arm, SEGUNDA, _coletor(pedidos)) == 0
    assert [k for k in arm.listar() if not k.startswith("logs/")] == dados
    assert len(C.ler_registro(reg)) == 4, "rodada sem mudanca nao escreve no registro"

    assert _rodar(raiz, reg, arm, SEGUNDA, _coletor(pedidos, conteudo="v2")) == 0
    novas = C.ler_registro(reg)[4:]
    assert [ln["situacao"] for ln in novas] == [C.ATUALIZADO] * 4


def test_ressalva_do_coletor_fica_no_registro_e_o_passo_segue_verde(tmp_path):
    raiz = _politica(tmp_path)
    reg = str(tmp_path / "reg.csv")
    rc = _rodar(raiz, reg, armazem_mod.ArmazemMemoria(), SEGUNDA,
                _coletor([], eventos_rc=1, proventos_rc=1))
    assert rc == 0
    fim = C.ler_registro(reg)[-1]
    assert fim["recurso"] == "rodada" and fim["situacao"] == E.RESSALVA
    assert "eventos" in fim["motivo"] and "proventos" in fim["motivo"]


def test_sem_tradingname_e_falha(tmp_path):
    raiz = _politica(tmp_path)
    reg = str(tmp_path / "reg.csv")
    assert _rodar(raiz, reg, armazem_mod.ArmazemMemoria(), SEGUNDA,
                  _coletor([], proventos_rc=2)) == 1
    assert C.ler_registro(reg)[-1]["situacao"] == C.ERRO


def test_erro_ou_bloqueio_da_B3_e_falha_com_motivo_e_nao_silencio(tmp_path):
    """Nao se contorna CAPTCHA nem bloqueio: o erro vira vermelho e o motivo, registro."""
    raiz = _politica(tmp_path)
    reg = str(tmp_path / "reg.csv")
    rc = _rodar(raiz, reg, armazem_mod.ArmazemMemoria(), SEGUNDA,
                _coletor([], erro=RuntimeError("HTTP 403 captcha")))
    assert rc == 1
    fim = C.ler_registro(reg)[-1]
    assert fim["situacao"] == C.ERRO and "403" in fim["motivo"]


def test_o_teto_recusa_com_linha_no_registro_e_passo_vermelho(tmp_path):
    raiz = _politica(tmp_path)
    reg = str(tmp_path / "reg.csv")
    arm = armazem_mod.ArmazemMemoria().limitar(1)
    rc = _rodar(raiz, reg, arm, SEGUNDA, _coletor([]))
    assert rc == 1
    linhas = C.ler_registro(reg)
    assert linhas[0]["situacao"] == C.RECUSADO_POR_TETO
    assert not [k for k in arm.listar() if k.startswith("b3/")]
    assert any(k.startswith("logs/") for k in arm.listar()), "a prova da recusa sobe"


def test_o_armazem_do_ambiente_vem_com_o_teto_da_politica(tmp_path, monkeypatch):
    """O mesmo teto da CVM: `do_ambiente` le `politica.yaml -> armazem`."""
    monkeypatch.setenv("ARMAZEM_LOCAL", str(tmp_path / "arm"))
    _, teto = armazem_mod.limites_da_politica(C.raiz_repo())
    assert armazem_mod.do_ambiente("local", raiz_repo=C.raiz_repo()).teto == teto


def test_arquivos_do_coletor_ignora_o_manifesto_e_o_que_nao_e_json(tmp_path):
    for rel in ("manifesto.jsonl", "eventos/dt_captura=2026-09-28/X.json",
                "eventos/dt_captura=2026-09-28/X.tmp"):
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("{}", encoding="utf-8")
    out = E.arquivos_do_coletor(str(tmp_path))
    assert [(r, n) for r, n, _ in out] == [("eventos_suplemento", "X.json")]
    shutil.rmtree(tmp_path / "eventos")
    assert E.arquivos_do_coletor(str(tmp_path)) == []
