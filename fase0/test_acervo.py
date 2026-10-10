# -*- coding: utf-8 -*-
"""Testes do `acervo.py` -- um repositorio falso em `tmp_path` e o `ArmazemMemoria`.

O que se prova: `abrir` acha a versao pelo que esta versionado e confere o byte que
entrega; o frescor avisa quando a captura para, e so entao -- o espelho de todo aviso e o
caso em que ele NAO sai.
"""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import os
import sys
import warnings

import pytest

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import acervo as V  # noqa: E402
import armazem as A  # noqa: E402

COLS = ("dt_captura", "recurso", "arquivo", "url", "http_last_modified", "etag", "sha256",
        "bytes", "caminho", "situacao", "motivo")
AGORA = dt.datetime(2026, 9, 30, 12, 0, 0, tzinfo=dt.timezone.utc)
B1, B2 = b"versao um", b"versao dois"
S1, S2 = hashlib.sha256(B1).hexdigest(), hashlib.sha256(B2).hexdigest()
ARQ = "dfp_cia_aberta_2024.zip"


def _csv(caminho, colunas, linhas):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=colunas, delimiter=";")
        w.writeheader()
        for ln in linhas:
            w.writerow({c: ln.get(c, "") for c in colunas})


def _repo(tmp_path, registro, inventario=()):
    (tmp_path / "pyproject.toml").write_text("[project]\nname='x'\n")
    _csv(str(tmp_path / "docs" / "acervo" / "cvm" / "capturas.csv"), COLS, registro)
    if inventario:
        _csv(str(tmp_path / "docs" / "acervo" / "cvm" / V.INVENTARIO),
             V.COLUNAS_INVENTARIO, inventario)
    return str(tmp_path)


def _ln(quando, sha, situacao="novo", recurso="dfp", arquivo=ARQ):
    return dict(dt_captura=quando, recurso=recurso, arquivo=arquivo, sha256=sha,
                situacao=situacao, bytes="9")


def _armazem(*pares):
    arm = A.ArmazemMemoria()
    for sha, byte in pares:
        arm.objetos[A.chave("cvm", "dfp", ARQ, sha)] = byte
    return arm


@pytest.fixture(autouse=True)
def _sem_aviso_de_frescor_por_padrao(monkeypatch):
    """`abrir` mede o frescor pelo relogio real; os testes de `abrir` nao sao sobre ele."""
    monkeypatch.setattr(V, "frescor", lambda *a, **k: None)


# ── versoes e abrir ───────────────────────────────────────────────────────────

def test_a_vigente_e_a_ultima_do_registro_e_a_anterior_continua_listada(tmp_path):
    repo = _repo(tmp_path, [_ln("2026-09-20T09:15:00Z", S1),
                            _ln("2026-09-27T09:15:00Z", S2, "atualizado")])
    vs = V.versoes("dfp", ARQ, repo)
    assert [v["sha256"] for v in vs] == [S1, S2]
    assert [v["vigente"] for v in vs] == [False, True]


def test_abrir_baixa_do_armazem_confere_e_guarda_no_cache(tmp_path):
    repo = _repo(tmp_path, [_ln("2026-09-20T09:15:00Z", S1)])
    arm = _armazem((S1, B1))
    p = V.abrir("dfp", ARQ, armazem=arm, repo=repo)
    assert open(p, "rb").read() == B1
    assert p.startswith(os.path.join(repo, "data", "armazem"))
    arm.objetos.clear()
    assert V.abrir("dfp", ARQ, armazem=arm, repo=repo) == p, "a segunda vez vem do cache"


def test_abrir_versao_anterior_por_prefixo(tmp_path):
    repo = _repo(tmp_path, [_ln("2026-09-20T09:15:00Z", S1),
                            _ln("2026-09-27T09:15:00Z", S2, "atualizado")])
    arm = _armazem((S1, B1), (S2, B2))
    assert open(V.abrir("dfp", ARQ, S1[:12], armazem=arm, repo=repo), "rb").read() == B1
    assert open(V.abrir("dfp", ARQ, armazem=arm, repo=repo), "rb").read() == B2


def test_byte_do_armazem_que_nao_bate_e_recusado_e_o_cache_fica_limpo(tmp_path):
    repo = _repo(tmp_path, [_ln("2026-09-20T09:15:00Z", S1)])
    arm = _armazem((S1, b"adulterado"))
    with pytest.raises(A.ConteudoDivergente):
        V.abrir("dfp", ARQ, armazem=arm, repo=repo)
    k = A.chave("cvm", "dfp", ARQ, S1)
    assert not os.path.exists(os.path.join(repo, "data", "armazem", *k.split("/")))


def test_acervo_local_com_o_hash_certo_dispensa_o_armazem(tmp_path):
    repo = _repo(tmp_path, [_ln("2026-09-20T09:15:00Z", S1)])
    local = tmp_path / "data" / "bronze" / "cvm" / "dfp" / ARQ
    local.parent.mkdir(parents=True)
    local.write_bytes(B1)
    arm = A.ArmazemMemoria()                 # vazio: se fosse consultado, KeyError
    assert V.abrir("dfp", ARQ, armazem=arm, repo=repo) == str(local)


def test_acervo_local_com_outro_hash_nao_e_entregue(tmp_path):
    """O espelho: o arquivo local tem o nome certo e o byte de outra versao."""
    repo = _repo(tmp_path, [_ln("2026-09-27T09:15:00Z", S2)])
    local = tmp_path / "data" / "bronze" / "cvm" / "dfp" / ARQ
    local.parent.mkdir(parents=True)
    local.write_bytes(B1)
    p = V.abrir("dfp", ARQ, armazem=_armazem((S2, B2)), repo=repo)
    assert p != str(local) and open(p, "rb").read() == B2


def test_inventario_da_carga_inicial_tambem_da_versao(tmp_path):
    repo = _repo(tmp_path, [], inventario=[
        dict(fonte="cvm", recurso="dfp", arquivo=ARQ, sha256=S1, papel="snapshot",
             versao="20260913"),
        dict(fonte="cvm", recurso="dfp", arquivo=ARQ, sha256=S2, papel="canonico")])
    arm = _armazem((S1, B1), (S2, B2))
    assert open(V.abrir("dfp", ARQ, armazem=arm, repo=repo), "rb").read() == B2
    assert open(V.abrir("dfp", ARQ, S1[:8], armazem=arm, repo=repo), "rb").read() == B1


@pytest.mark.parametrize("versao, erro", [
    (None, V.VersaoDesconhecida), ("abc", ValueError), ("f" * 12, V.VersaoDesconhecida)])
def test_pedido_sem_resposta_falha_em_vez_de_adivinhar(tmp_path, versao, erro):
    repo = _repo(tmp_path, [_ln("2026-09-20T09:15:00Z", S1, arquivo="outro.zip")])
    if versao is not None:
        repo = _repo(tmp_path, [_ln("2026-09-20T09:15:00Z", S1)])
    with pytest.raises(erro):
        V.abrir("dfp", ARQ, versao, armazem=A.ArmazemMemoria(), repo=repo)


# ── frescor ───────────────────────────────────────────────────────────────────

_FRESCOR = V.frescor                         # antes de a fixture autouse troca-la


def _frescor():
    return _FRESCOR


def test_frescor_dentro_do_limite_nao_avisa(tmp_path):
    f = _frescor()
    repo = _repo(tmp_path, [_ln("2026-09-25T09:15:00Z", S1)])
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        r = f("dfp", repo=repo, agora=AGORA)
    assert r["status"] == "OK" and r["dias"] == pytest.approx(5.1, abs=0.1)


def test_frescor_acima_de_8_dias_avisa_pelo_nome(tmp_path):
    f = _frescor()
    repo = _repo(tmp_path, [_ln("2026-09-20T09:15:00Z", S1)])
    with pytest.warns(V.CapturaParada, match="CAPTURA_PARADA: dfp.*60 dias"):
        r = f("dfp", repo=repo, agora=AGORA)
    assert r["status"] == "CAPTURA_PARADA" and r["dias"] > 8


def test_frescor_do_recurso_nunca_observado_avisa(tmp_path):
    f = _frescor()
    repo = _repo(tmp_path, [_ln("2026-09-29T09:15:00Z", S1, recurso="itr")])
    with pytest.warns(V.CapturaParada, match="NUNCA_OBSERVADO"):
        assert f("dfp", repo=repo, agora=AGORA)["status"] == "NUNCA_OBSERVADO"


def test_o_log_do_armazem_prova_a_rodada_que_o_registro_nao_viu(tmp_path):
    """O `inalterado` pelo portao so vai para o log. Sem consultar o log, uma rotina que
    rodou ontem e nao achou nada novo parece parada ha doze dias."""
    f = _frescor()
    repo = _repo(tmp_path, [_ln("2026-09-18T09:15:00Z", S1)])
    arm = A.ArmazemMemoria()
    log = tmp_path / "log.csv"
    _csv(str(log), COLS, [_ln("2026-09-29T09:15:00Z", "", "inalterado")])
    arm.enviar_se_ausente("logs/capturas/2026-09-29.csv", str(log))
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        r = f("dfp", armazem=arm, repo=repo, agora=AGORA)
    assert r["status"] == "OK" and "log do armazem" in r["consultado"]
    with pytest.warns(V.CapturaParada):
        assert f("dfp", repo=repo, agora=AGORA)["status"] == "CAPTURA_PARADA"


def test_abrir_mede_o_frescor_de_recurso_com_rotina(tmp_path, monkeypatch):
    chamados = []
    monkeypatch.setattr(V, "frescor", lambda r, **k: chamados.append(r))
    repo = _repo(tmp_path, [_ln("2026-09-20T09:15:00Z", S1)])
    V.abrir("dfp", ARQ, armazem=_armazem((S1, B1)), repo=repo)
    assert chamados == ["dfp"]


# ── vigencias: a linha do tempo do que se tinha capturado (P-53, 10/10/2026) ──────

def test_vigencias_e_a_sequencia_de_quem_ficou_no_lugar(tmp_path):
    repo = _repo(tmp_path, [_ln("2026-09-20T09:15:00Z", S1),
                            _ln("2026-09-21T09:15:00Z", "", "inalterado"),
                            _ln("2026-09-27T09:15:00Z", S2, "atualizado")])
    assert [(str(i), s) for i, s in V.vigencias("dfp", ARQ, repo)] == [
        ("2026-09-20 09:15:00+00:00", S1), ("2026-09-27 09:15:00+00:00", S2)]


def test_vigencias_ignora_o_deslocado_que_empata_no_instante_da_migracao(tmp_path):
    """O registro REAL de 24/09: a migracao gravou o `atualizado` (519a0317...) e o
    `deslocado` (00a5f1e6..., versao de 13/09) com a MESMA `dt_captura`, 12:16:32Z. A
    linha `deslocado` diz que uma versao existiu, nao desde quando ela era a vigente:
    contada, o `max(dt_captura <= D)` empata e pode devolver a versao velha.

    Mutacao: aceite `deslocado` em `vigencias` e a ultima vigente passa a ser S1."""
    repo = _repo(tmp_path, [_ln("2026-09-24T12:16:32Z", S2, "atualizado"),
                            _ln("2026-09-24T12:16:32Z", S1, "deslocado")])
    assert [s for _, s in V.vigencias("dfp", ARQ, repo)] == [S2]


def test_vigencias_nao_inventa_data_para_a_versao_so_do_inventario(tmp_path):
    """O inventario da carga inicial diz o que havia no disco dele, com a data da VERSAO
    (o membro do ZIP, CV-03) e a do ENVIO -- nenhuma das duas e quando ela foi capturada.
    Sem linha no registro, a versao nao entra na linha do tempo (fica em `versoes`)."""
    inv = [dict(fonte="cvm", recurso="dfp", arquivo=ARQ, sha256=S1, papel="snapshot",
                versao="20260913", dt_envio="2026-09-24T18:17:37Z")]
    repo = _repo(tmp_path, [_ln("2026-09-27T09:15:00Z", S2, "atualizado")], inv)
    assert [s for _, s in V.vigencias("dfp", ARQ, repo)] == [S2]
    assert {v["sha256"] for v in V.versoes("dfp", ARQ, repo)} == {S1, S2}


def test_vigencias_o_inalterado_sem_byte_atesta_o_canonico_do_inventario(tmp_path):
    """Medido no registro real em 10/10: 34 arquivos (os anos congelados) so tem linhas
    `inalterado` sem sha256 -- o byte veio da carga inicial, pelo inventario, e o portao
    HEAD so escreve `inalterado` quando Last-Modified e tamanho batem com a versao que ja
    se tinha. A primeira dessas linhas atesta o canonico do inventario daquele instante em
    diante. Sem isto, 2010-2021 responderiam SemCaptura para sempre.

    Mutacao: ignore o `inalterado` sem sha256 e a lista sai vazia."""
    inv = [dict(fonte="cvm", recurso="dfp", arquivo=ARQ, sha256=S1, bytes="9",
                papel="canonico", dt_envio="2026-09-24T18:17:37Z")]
    repo = _repo(tmp_path, [_ln("2026-09-24T13:36:00Z", "", "inalterado"),
                            _ln("2026-09-25T12:24:16Z", "", "inalterado")], inv)
    assert [(str(i), s) for i, s in V.vigencias("dfp", ARQ, repo)] == [
        ("2026-09-24 13:36:00+00:00", S1)]


def test_vigencias_nao_atesta_canonico_de_outro_tamanho_nem_ambiguo(tmp_path):
    """O portao compara o tamanho; um canonico de outro tamanho nao e o byte que ele
    atestou. Dois canonicos do mesmo tamanho: nao ha como saber qual -- nenhum."""
    um = [dict(fonte="cvm", recurso="dfp", arquivo=ARQ, sha256=S1, bytes="8",
               papel="canonico")]
    dois = [dict(um[0], bytes="9"), dict(um[0], sha256=S2, bytes="9")]
    for inv in (um, dois):
        repo = _repo(tmp_path, [_ln("2026-09-24T13:36:00Z", "", "inalterado")], inv)
        assert V.vigencias("dfp", ARQ, repo) == []
