# -*- coding: utf-8 -*-
"""A captura do COTAHIST (P-135): diario a cada pregao, anual uma vez por mes, o 404 do
diario sem ficar vermelho, e o mesmo teto do armazem. Sem rede e sem boto3."""
from __future__ import annotations

import csv
import datetime as dt
import io
import os
import sys
import urllib.error

import pytest

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import armazem as A  # noqa: E402
import capturar_cotahist as T  # noqa: E402
from test_capturar_cvm import _Resp, _zip  # noqa: E402

LM = "Wed, 23 Sep 2026 23:41:41 GMT"
HOJE = dt.date(2026, 9, 24)          # quinta; a janela vai de 17/09 (qui) a 23/09 (qua)


class B3:
    """Um bvmf.bmfbovespa.com.br de mentira: publica ZIPs; o resto e 404, como medido."""

    def __init__(self):
        self.arquivos, self.chamadas = {}, []

    def publicar(self, nome, corpo, lm=LM):
        self.arquivos[T.BASE + nome] = dict(corpo=corpo, lm=lm)

    def gets(self):
        return [u for m, u in self.chamadas if m == "GET"]

    def __call__(self, req, timeout=None):
        url, metodo = req.full_url, req.get_method()
        self.chamadas.append((metodo, url))
        if url not in self.arquivos:
            raise urllib.error.HTTPError(url, 404, "Not Found", {}, None)
        a = self.arquivos[url]
        cab = {"Content-Length": str(len(a["corpo"])), "Last-Modified": a["lm"], "ETag": '"x"'}
        return _Resp(b"" if metodo == "HEAD" else a["corpo"], cab)


def _b3(sem=()):
    srv = B3()
    for d in ("17092026", "18092026", "21092026", "22092026", "23092026"):
        if d not in sem:
            srv.publicar(f"COTAHIST_D{d}.ZIP", _zip({f"COTAHIST_D{d}.TXT": "00COTAHIST\n"}))
    srv.publicar("COTAHIST_A2026.ZIP", _zip({"COTAHIST_A2026.TXT": "00COTAHIST.2026\n"}))
    return srv


def _politica(tmp_path):
    raiz = tmp_path / "repo"
    (raiz / "alocacao").mkdir(parents=True, exist_ok=True)
    (raiz / "alocacao" / "politica.yaml").write_text(
        "armazem:\n  aviso_gb: 7\n  teto_gb: 9\n", encoding="utf-8")
    return str(raiz)


def _rodar(tmp_path, srv, arm, hoje=HOJE):
    reg = str(tmp_path / "docs" / "acervo" / "b3" / "capturas.csv")
    rc = T.main(["--armazem", "s3", "--raiz", str(tmp_path / "data" / "bronze" / "b3"),
                 "--registro", reg, "--pausa", "0", "--raiz-repo", _politica(tmp_path)],
                abrir=srv, dormir=lambda s: None, armazem=arm, hoje=hoje)
    return rc, reg


def _log(arm):
    k = sorted(k for k in arm.objetos if k.startswith(T.LOGS))[-1]
    return list(csv.DictReader(io.StringIO(arm.objetos[k].decode()), delimiter=";"))


def test_janela_de_diarios_so_dia_util_e_do_mais_antigo_ao_mais_novo():
    nomes = [u.rsplit("_D", 1)[1] for u, r in T.diarios(HOJE)]
    assert nomes == ["17092026.ZIP", "18092026.ZIP", "21092026.ZIP", "22092026.ZIP",
                     "23092026.ZIP"]
    assert {r for _, r in T.diarios(HOJE)} == {T.DIARIO}


def test_anual_uma_vez_por_mes_e_o_do_mes_que_acabou():
    assert T.anual_do_mes(HOJE, []) == (T.BASE + "COTAHIST_A2026.ZIP", T.ANUAL)
    ja = [dict(recurso=T.ANUAL, dt_captura="2026-09-01T09:20:00Z")]
    assert T.anual_do_mes(HOJE, ja) is None
    assert T.anual_do_mes(dt.date(2026, 10, 1), ja)[0].endswith("COTAHIST_A2026.ZIP")
    # janeiro: o ultimo pregao de dezembro esta no anual do ano ANTERIOR
    assert T.anual_do_mes(dt.date(2027, 1, 4), ja)[0].endswith("COTAHIST_A2026.ZIP")
    # linha de diario deste mes nao conta como anual
    assert T.anual_do_mes(HOJE, [dict(recurso=T.DIARIO, dt_captura="2026-09-23")])


def test_primeira_rodada_sobe_os_diarios_e_o_anual_com_chave_da_b3(tmp_path):
    arm = A.ArmazemMemoria()
    rc, reg = _rodar(tmp_path, _b3(), arm)
    assert rc == 0
    ks = sorted(k for k in arm.objetos if not k.startswith(T.LOGS))
    assert len(ks) == 6
    assert all(k.startswith("b3/cotahist_diario/COTAHIST_D") for k in ks[1:])
    assert ks[0].startswith("b3/cotahist/COTAHIST_A2026.ZIP/")   # a chave da carga inicial
    linhas = [x for x in csv.DictReader(open(reg, encoding="utf-8"), delimiter=";")]
    assert [x["situacao"] for x in linhas] == ["novo"] * 6


def test_segunda_rodada_no_mesmo_mes_nao_baixa_nada(tmp_path, monkeypatch):
    """O portao HEAD fecha os diarios, e o anual ja foi observado neste mes: nenhum GET
    -- e o anual nem recebe HEAD. E isso que impede 85 MB por dia."""
    # O registro grava dt_captura pelo relogio real (C.agora) e o teste fixa `hoje`: em
    # outubro de 2026 o anual "observado" deixou de ser do mes do `hoje` e o teste caiu
    # (medido em 02/10/2026). O relogio fica no mesmo dia do `hoje` da rodada.
    monkeypatch.setattr(T.C, "agora", lambda: "2026-09-24T12:00:00Z")
    srv, arm = _b3(), A.ArmazemMemoria()
    _rodar(tmp_path, srv, arm)
    srv.chamadas.clear()
    rc, _ = _rodar(tmp_path, srv, arm, hoje=dt.date(2026, 9, 25))
    assert rc == 0 and srv.gets() == []
    assert not any("COTAHIST_A" in u for _, u in srv.chamadas)


def test_diario_404_e_ausente_no_log_e_nao_fica_vermelho(tmp_path):
    arm = A.ArmazemMemoria()
    rc, reg = _rodar(tmp_path, _b3(sem=("21092026",)), arm)
    assert rc == 0
    aus = [x for x in _log(arm) if x["situacao"] == "ausente"]
    assert len(aus) == 1 and aus[0]["arquivo"] == "COTAHIST_D21092026.ZIP"
    assert "feriado" in aus[0]["motivo"]
    assert "COTAHIST_D21092026" not in open(reg, encoding="utf-8").read(), \
        "ausente nao muda estado: vai so para o log"


def test_anual_404_e_erro_e_fica_vermelho(tmp_path):
    srv = _b3()
    del srv.arquivos[T.BASE + "COTAHIST_A2026.ZIP"]
    rc, reg = _rodar(tmp_path, srv, A.ArmazemMemoria())
    assert rc == 1
    assert "erro" in open(reg, encoding="utf-8").read()


def test_mesmo_teto_do_armazem_vale_para_o_cotahist(tmp_path):
    arm = A.ArmazemMemoria().limitar(400)
    rc, reg = _rodar(tmp_path, _b3(), arm)
    sit = [x["situacao"] for x in csv.DictReader(open(reg, encoding="utf-8"), delimiter=";")]
    # os ZIPs de teste medem ~150 bytes: cabem os primeiros e o resto e recusado
    assert sit[0] == "novo" and sit[-1] == "recusado_por_teto" and rc == 1


def test_log_da_b3_nao_se_mistura_com_o_da_cvm(tmp_path):
    arm = A.ArmazemMemoria()
    _rodar(tmp_path, _b3(), arm)
    logs = [k for k in arm.objetos if k.startswith("logs/")]
    assert logs and all(k.startswith("logs/capturas_b3/") for k in logs)


@pytest.mark.parametrize("arg", [[], ["--armazem", "disco"]])
def test_so_existe_modo_armazem(tmp_path, arg):
    with pytest.raises(SystemExit):
        T.main(arg, abrir=_b3(), dormir=lambda s: None, armazem=A.ArmazemMemoria())
