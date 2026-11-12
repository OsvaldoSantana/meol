# -*- coding: utf-8 -*-
"""P-30 (10/11/2026): a CVM chega ao cache pela release publica, sem segredo, e so com o sha256.

A contagem do bloco C ficou parada de 24/10 a 10/11 por "faltam dois segredos do R2" quando os
insumos dela eram todos da CVM, que o projeto publica na release `cvm-acervo-<ano>`. Aqui a
rede e falsa: o que se prova e o que entra no cache, e o que e recusado.
"""
from __future__ import annotations

import io
import os
import sys
import urllib.error

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import armazem as A  # noqa: E402
import cache_da_release as C  # noqa: E402
import publicar_cvm as pc  # noqa: E402
from test_publicar_cvm import REG_COLS, _repo, _sha  # noqa: E402

BYTE = b"PK-dfp-2025-versao-de-novembro"
ARQ = "dfp_cia_aberta_2025.zip"


def _reg(conteudo=BYTE, arquivo=ARQ, recurso="dfp", quando="2026-11-08T15:58:16Z"):
    return dict.fromkeys(REG_COLS, "") | dict(
        dt_captura=quando, recurso=recurso, arquivo=arquivo, sha256=_sha(conteudo),
        bytes=str(len(conteudo)), situacao="novo")


class Rede:
    """Um `urlopen` falso: {url: byte}; URL fora do dicionario responde 404."""
    def __init__(self, paginas):
        self.paginas, self.pedidos = paginas, []

    def __call__(self, url):
        self.pedidos.append(url)
        if url not in self.paginas:
            raise urllib.error.HTTPError(url, 404, "Not Found", None, None)
        return io.BytesIO(self.paginas[url])


def _url(sha, arquivo=ARQ, ano="2026"):
    base, ext = os.path.splitext(arquivo)
    return (f"https://github.com/{C.REPOSITORIO}/releases/download/cvm-acervo-{ano}/"
            f"{base}__{sha[:12]}{ext}")


def test_traz_da_release_do_ano_de_observacao_e_so_poe_no_cache_o_byte_conferido(tmp_path):
    repo = _repo(tmp_path, registro=[_reg()])
    rede = Rede({_url(_sha(BYTE)): BYTE})
    cache = str(tmp_path / "cache")
    r = C.trazer([("dfp", ARQ, _sha(BYTE))], repo=repo, cache=cache, abrir=rede)
    assert r == [(f"dfp_cia_aberta_2025__{_sha(BYTE)[:12]}.zip", "baixado")]
    destino = os.path.join(cache, *A.chave("cvm", "dfp", ARQ, _sha(BYTE)).split("/"))
    assert open(destino, "rb").read() == BYTE and not os.path.exists(destino + ".parcial")
    # idempotente: a segunda chamada nao toca a rede
    assert C.trazer([("dfp", ARQ, _sha(BYTE))], repo=repo, cache=cache, abrir=rede) == [
        (r[0][0], "ja_no_cache")]
    assert len(rede.pedidos) == 1


def test_byte_com_outro_sha256_nao_entra_no_cache(tmp_path):
    """A release entrega o nome certo com o conteudo errado: nada vai para o cache, e a chamada
    cai. Sem isto, o `acervo.abrir` serviria o byte errado como versao conferida."""
    repo = _repo(tmp_path, registro=[_reg()])
    cache = str(tmp_path / "cache")
    with pytest.raises(A.ConteudoDivergente, match="Nada foi para o cache"):
        C.trazer([("dfp", ARQ, _sha(BYTE))], repo=repo, cache=cache,
                 abrir=Rede({_url(_sha(BYTE)): b"outro conteudo"}))
    assert not any(arqs for _, _, arqs in os.walk(cache))


def test_versao_fora_do_registro_ou_fora_da_release_e_dita_e_nao_contornada(tmp_path):
    repo = _repo(tmp_path, registro=[_reg()])
    with pytest.raises(C.ForaDaRelease, match="nenhuma versao com byte"):
        C.trazer([("dfp", ARQ, "f" * 64)], repo=repo, cache=str(tmp_path / "c"), abrir=Rede({}))
    with pytest.raises(C.ForaDaRelease, match="HTTP 404"):
        C.trazer([("dfp", ARQ, _sha(BYTE))], repo=repo, cache=str(tmp_path / "c"),
                 abrir=Rede({}))
    assert not any(arqs for _, _, arqs in os.walk(str(tmp_path / "c")))


def test_so_a_CVM_vem_da_release(tmp_path):
    """Um COTAHIST no registro da CVM nao e publicavel (P-136): o pedido cai no guarda do
    publicador antes de qualquer download."""
    b3 = _reg(b"cotahist", arquivo="COTAHIST_A2026.ZIP", recurso="cotahist")
    repo = _repo(tmp_path, registro=[b3])
    rede = Rede({})
    with pytest.raises(pc.PublicacaoRecusada):
        C.trazer([("cotahist", "COTAHIST_A2026.ZIP", b3["sha256"])], repo=repo,
                 cache=str(tmp_path / "c"), abrir=rede)
    assert rede.pedidos == []


def test_o_repositorio_vem_do_ambiente_do_actions(monkeypatch):
    v = dict(fonte="cvm", recurso="dfp", arquivo=ARQ, sha256="a" * 64, ano="2026")
    monkeypatch.setenv("GITHUB_REPOSITORY", "outra/copia")
    assert C.url_da_versao(v).startswith("https://github.com/outra/copia/releases/download/")
    monkeypatch.delenv("GITHUB_REPOSITORY")
    assert C.url_da_versao(v) == _url("a" * 64)


def test_linha_de_comando_recusa_argumento_que_nao_fecha_em_trincas(capsys):
    assert C.main(["dfp", ARQ]) == 2
    assert "cache_da_release.py" in capsys.readouterr().err
