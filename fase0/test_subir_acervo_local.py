# -*- coding: utf-8 -*-
"""Testes da carga inicial -- um acervo falso em `tmp_path` e o `ArmazemMemoria`."""
from __future__ import annotations

import hashlib
import os
import sys

import pytest

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import acervo as V  # noqa: E402
import armazem as A  # noqa: E402
import subir_acervo_local as S  # noqa: E402


def _sha(b):
    return hashlib.sha256(b).hexdigest()


def _acervo(tmp_path, snapshot_mente=False):
    (tmp_path / "pyproject.toml").write_text("[project]\nname='x'\n")
    b = tmp_path / "data" / "bronze"
    dfp = b / "cvm" / "dfp"
    (dfp / "_snapshots").mkdir(parents=True)
    (dfp / "dfp_cia_aberta_2024.zip").write_bytes(b"vigente")
    velho = b"de 13/09"
    sha12 = ("0" * 12) if snapshot_mente else _sha(velho)[:12]
    (dfp / "_snapshots" / f"dfp_cia_aberta_2024__v20260913__{sha12}.zip").write_bytes(velho)
    (b / "cvm" / "cad").mkdir(parents=True)
    (b / "cvm" / "cad" / "cad_cia_aberta.csv").write_bytes(b"CNPJ;X\n")
    (b / "cvm" / "_manifest").mkdir()                 # fora de dfp/itr/cad: ignorado
    (b / "b3" / "cotahist").mkdir(parents=True)
    (b / "b3" / "cotahist" / "COTAHIST_A1986.ZIP").write_bytes(b"1986")
    (b / "b3" / "cotahist" / "notas.txt").write_bytes(b"?")
    return str(tmp_path)


def test_plano_nao_envia_nada_e_da_chave_de_conteudo_a_cada_versao(tmp_path):
    repo = _acervo(tmp_path)
    arm = A.ArmazemMemoria()
    assert S.main([], armazem=arm, repo=repo) == 0
    assert arm.objetos == {}
    assert not os.path.exists(S.inventario(repo, "cvm"))
    itens = {(x["recurso"], x["papel"]): x for x in S.plano(repo) if x["acao"] == S.SUBIR}
    snap = itens[("dfp", "snapshot")]
    assert snap["arquivo"] == "dfp_cia_aberta_2024.zip", "o snapshot volta ao nome canonico"
    assert snap["chave"] == A.chave("cvm", "dfp", "dfp_cia_aberta_2024.zip", _sha(b"de 13/09"))
    assert itens[("cotahist", "canonico")]["chave"].startswith("b3/cotahist/COTAHIST_A1986.ZIP/")


def test_arquivo_fora_da_convencao_e_desconhecido_e_nao_sobe(tmp_path):
    repo = _acervo(tmp_path)
    desc = [x for x in S.plano(repo) if x["acao"] == S.DESCONHECIDO]
    assert [os.path.basename(x["caminho"]) for x in desc] == ["notas.txt"]


def test_aplicar_sobe_grava_inventario_e_repetir_nao_muda_nada(tmp_path):
    repo = _acervo(tmp_path)
    arm = A.ArmazemMemoria()
    assert S.main(["--aplicar"], armazem=arm, repo=repo) == 0
    assert arm.envios == 4
    inv_cvm = V._ler(S.inventario(repo, "cvm"))
    assert {x["papel"] for x in inv_cvm} == {"canonico", "snapshot"} and len(inv_cvm) == 3
    assert len(V._ler(S.inventario(repo, "b3"))) == 1
    antes = open(S.inventario(repo, "cvm"), "rb").read()
    assert S.main(["--aplicar"], armazem=arm, repo=repo) == 0
    assert arm.envios == 4, "a segunda carga nao escreve nada no armazem"
    assert open(S.inventario(repo, "cvm"), "rb").read() == antes, "nem no inventario"


def test_o_inventario_torna_a_versao_abrivel(tmp_path):
    repo = _acervo(tmp_path)
    arm = A.ArmazemMemoria()
    S.main(["--aplicar"], armazem=arm, repo=repo)
    import shutil
    shutil.rmtree(os.path.join(repo, "data", "bronze"))      # a maquina perdeu o disco
    p = V.abrir("dfp", "dfp_cia_aberta_2024.zip", _sha(b"de 13/09")[:8], armazem=arm,
                repo=repo)
    assert open(p, "rb").read() == b"de 13/09"


def test_snapshot_cujo_nome_mente_para_o_plano_inteiro(tmp_path):
    repo = _acervo(tmp_path, snapshot_mente=True)
    arm = A.ArmazemMemoria()
    assert S.main(["--aplicar"], armazem=arm, repo=repo) == 1
    assert arm.objetos == {} and not os.path.exists(S.inventario(repo, "cvm"))
    with pytest.raises(SystemExit):
        S.aplicar(S.plano(repo), arm, repo)


def test_P145_o_banco_de_ISIN_sobe_e_a_captura_mais_recente_e_a_canonica(tmp_path):
    """Sem o isinp.zip no armazem, a ponte da P-145 so roda no desktop. Duas capturas: a
    mais nova e a vigente, a outra fica como versao anterior; pasta fora da convencao nao
    sobe."""
    repo = _acervo(tmp_path)
    isin = tmp_path / "data" / "bronze" / "b3" / "isin"
    for d, b in (("dt_captura=2026-09-25", b"isin 25"), ("dt_captura=2026-10-01", b"isin 01")):
        (isin / d).mkdir(parents=True)
        (isin / d / "isinp.zip").write_bytes(b)
    (isin / "rascunho").mkdir()
    itens = [x for x in S.plano(repo) if x["recurso"] == "isin"]
    subir = {x["papel"]: x for x in itens if x["acao"] == S.SUBIR}
    assert subir["canonico"]["sha256"] == _sha(b"isin 01")
    assert subir["snapshot"]["sha256"] == _sha(b"isin 25")
    assert subir["canonico"]["chave"].startswith("b3/isin/isinp.zip/")
    assert [x["arquivo"] for x in itens if x["acao"] == S.DESCONHECIDO] == ["rascunho"]
    arm = A.ArmazemMemoria()
    assert S.main(["--aplicar"], armazem=arm, repo=repo) == 0
    caminho = V.abrir("isin", "isinp.zip", repo=repo, armazem=arm,
                      cache=str(tmp_path / "cache"))
    with open(caminho, "rb") as f:
        assert f.read() == b"isin 01"


# -- P-150 parte 1: os eventos da B3 que so existem no disco dele (captura de 11/09) --

def _eventos(tmp_path, dias=("2026-09-11",)):
    """A arvore que o `coletar_b3.py` grava em `data/bronze/b3`, por dia de captura."""
    b3 = tmp_path / "data" / "bronze" / "b3"
    for i, dia in enumerate(dias):
        d = f"dt_captura={dia}"
        for rel, corpo in ((f"indices/{d}/IBOV.json", f'{{"carteira": {i}}}'),
                           (f"eventos/{d}/PETR.json", f'{{"cash": {i}}}'),
                           (f"proventos/{d}/PETR/pagina-001.json", f'{{"p": {i}}}'),
                           (f"proventos/{d}/VALE.cash.json", f'{{"evidencia": {i}}}')):
            p = b3 / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(corpo, encoding="utf-8")
    (b3 / "manifesto.jsonl").write_text('{"url": "x"}\n', encoding="utf-8")
    return b3


RECURSOS_EVENTOS = ("indice_carteira", "eventos_suplemento", "proventos")


def test_P150_o_plano_lista_indice_eventos_e_proventos(tmp_path):
    """Falha na versao anterior: o plano so conhecia cotahist e isin na B3, e os 207
    arquivos da captura de 11/09 ficavam no disco dele."""
    repo = _acervo(tmp_path)
    _eventos(tmp_path)
    subir = {(x["recurso"], x["arquivo"]) for x in S.plano(repo)
             if x["acao"] == S.SUBIR and x["recurso"] in RECURSOS_EVENTOS}
    assert subir == {("indice_carteira", "IBOV.json"), ("eventos_suplemento", "PETR.json"),
                     ("proventos", "PETR__pagina-001.json"), ("proventos", "VALE.cash.json")}


def test_P150_a_chave_e_a_mesma_que_o_passo_do_cron_daria(tmp_path):
    """A carga inicial e o `captura_eventos_b3` nao podem discordar sobre o nome: se
    discordassem, o 11/09 e a primeira segunda seriam dois arquivos, e nao duas versoes."""
    import capturar_eventos_b3 as E
    repo = _acervo(tmp_path)
    b3 = _eventos(tmp_path)
    plano = {x["chave"] for x in S.plano(repo)
             if x["acao"] == S.SUBIR and x["recurso"] in RECURSOS_EVENTOS}
    arm = A.ArmazemMemoria()
    E.enviar(E.arquivos_do_coletor(str(b3)), arm, str(tmp_path / "reg.csv"), [], {})
    assert plano == set(arm.objetos)


def test_P150_metadados_inventario_do_acervo_de_eventos_e_versao_pelo_dia(tmp_path):
    repo = _acervo(tmp_path)
    _eventos(tmp_path, dias=("2026-09-06", "2026-09-11"))
    itens = [x for x in S.plano(repo) if x["acao"] == S.SUBIR
             and (x["recurso"], x["arquivo"]) == ("proventos", "PETR__pagina-001.json")]
    papeis = {x["versao"]: x["papel"] for x in itens}
    assert papeis == {"20260906": "snapshot", "20260911": "canonico"}
    arm = A.ArmazemMemoria()
    assert S.main(["--aplicar"], armazem=arm, repo=repo) == 0
    inv = V._ler(S.inventario(repo, "b3_eventos"))
    assert {ln["recurso"] for ln in inv} >= set(RECURSOS_EVENTOS)
    assert all(ln["fonte"] == "b3" for ln in inv)
    assert not any(ln["recurso"] in RECURSOS_EVENTOS
                   for ln in V._ler(S.inventario(repo, "b3"))), "o acervo dos eventos e outro"
    caminho = V.abrir("proventos", "PETR__pagina-001.json", repo=repo, armazem=arm,
                      cache=str(tmp_path / "cache"))
    with open(caminho, encoding="utf-8") as f:
        assert f.read() == '{"p": 1}', "a vigente e a do dia mais recente"


def test_P150_o_manifesto_do_coletor_sobe_como_log_e_fora_do_teto(tmp_path):
    """O manifesto e a procedencia do 11/09 (sha256 e instante de cada pedido)."""
    repo = _acervo(tmp_path)
    _eventos(tmp_path)
    man = [x for x in S.plano(repo) if x["recurso"] == "manifesto_coletor"]
    assert len(man) == 1 and man[0]["acao"] == S.SUBIR
    assert man[0]["chave"].startswith("logs/capturas_b3_eventos/carga-inicial__manifesto__")
    arm = A.ArmazemMemoria().limitar(1)            # teto de 1 byte: so o isento sobe
    assert S.aplicar(man, arm, repo) == 1
    assert list(arm.objetos) == [man[0]["chave"]]
    with pytest.raises(A.TetoExcedido):
        S.aplicar([x for x in S.plano(repo) if x["recurso"] == "proventos"
                   and x["acao"] == S.SUBIR], arm, repo)


def test_P150_fora_da_convencao_nos_eventos_e_desconhecido(tmp_path):
    repo = _acervo(tmp_path)
    b3 = _eventos(tmp_path)
    (b3 / "eventos" / "solto.json").write_text("{}", encoding="utf-8")
    (b3 / "eventos" / "dt_captura=2026-09-11" / "notas.txt").write_text("?", encoding="utf-8")
    desc = sorted(os.path.basename(x["caminho"]) for x in S.plano(repo)
                  if x["acao"] == S.DESCONHECIDO)
    assert desc == ["notas.txt", "notas.txt", "solto.json"]


def test_P150_o_padrao_continua_plano_e_nada_sai(tmp_path):
    repo = _acervo(tmp_path)
    _eventos(tmp_path)
    arm = A.ArmazemMemoria()
    assert S.main([], armazem=arm, repo=repo) == 0
    assert arm.objetos == {} and not os.path.exists(S.inventario(repo, "b3_eventos"))


def test_P150_P136_os_eventos_nao_entram_na_release(tmp_path):
    """A release le so o acervo da CVM, e o `publicavel` recusa qualquer fonte que nao
    seja a CVM: depois da carga, nenhum evento aparece como candidato."""
    import publicar_cvm
    repo = _acervo(tmp_path)
    _eventos(tmp_path)
    arm = A.ArmazemMemoria()
    assert S.main(["--aplicar"], armazem=arm, repo=repo) == 0
    assert all(v.get("fonte") == "cvm" for v in publicar_cvm.versoes(repo))
    for x in S.plano(repo):
        if x["acao"] == S.SUBIR and x["recurso"] in RECURSOS_EVENTOS:
            with pytest.raises(publicar_cvm.PublicacaoRecusada):
                publicar_cvm.publicavel(dict(fonte=x["fonte"], recurso=x["recurso"],
                                             arquivo=x["arquivo"], sha256=x["sha256"]))
