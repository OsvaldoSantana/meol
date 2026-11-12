#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cache_da_release.py -- traz versoes da CVM para o cache do acervo pela release PUBLICA.

POR QUE ELE EXISTE (10/11/2026, P-30). A contagem do bloco C ficou parada de 24/10 a 10/11 com
"faltam dois segredos do R2", e os insumos dela sao so da CVM, que o proprio projeto publica
desde 25/09 na release `cvm-acervo-<ano>` (fase0/publicar_cvm.py, P-136). Era o degrau 2 da
escada (outra copia) que ninguem tinha subido: medicao que so le a CVM nao precisa de segredo
nenhum. Rodado em 10/11: as 8 versoes da contagem vieram da release com o sha256 do registro.

O QUE ELE FAZ. Para cada (recurso, arquivo, sha256) pedido: acha a versao no registro e no
inventario (a mesma lista do publicador), baixa `<nome>__<sha256[:12]>.<ext>` da release do ano
de observacao e so poe o byte no cache (`data/armazem/<chave>`) depois de conferir o sha256
INTEIRO. O `acervo.abrir` olha o cache antes de qualquer armazem, entao quem le continua lendo
por ele, sem saber de onde o byte veio.

O QUE ELE NAO FAZ (P5):
  - nao traz B3 nem NEFIN: nao estao na release, e `publicar_cvm.publicavel` recusa o pedido;
  - nao usa credencial: a release e publica. Num repositorio privado o download falha, e a
    falha e dita (ForaDaRelease), nunca contornada;
  - nao confia no nome do arquivo: byte com outro sha256 e apagado e derruba a chamada.

  python fase0/cache_da_release.py dfp dfp_cia_aberta_2025.zip <sha256> [recurso arquivo sha256 ...]
"""
from __future__ import annotations

import hashlib
import os
import sys
import urllib.error
import urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)
import acervo  # noqa: E402
import armazem as armazem_mod  # noqa: E402
import publicar_cvm  # noqa: E402

# O repositorio que publica a release. No Actions vem do ambiente; fora dele, o do projeto.
REPOSITORIO = "OsvaldoSantana/meol"
URL = "https://github.com/{repositorio}/releases/download/{tag}/{nome}"
BLOCO = 1 << 20


class ForaDaRelease(LookupError):
    """A versao pedida nao tem byte registrado, ou a release nao a entrega."""


def url_da_versao(v, repositorio=None):
    """A URL do arquivo da versao na release do ano em que ela foi observada."""
    publicar_cvm.publicavel(v)                        # so a CVM; recusa o resto (P-136)
    repositorio = repositorio or os.environ.get("GITHUB_REPOSITORY") or REPOSITORIO
    return URL.format(repositorio=repositorio, tag=publicar_cvm.PREFIXO_TAG + v["ano"],
                      nome=publicar_cvm.nome_do_arquivo(v))


def _versao(recurso, arquivo, sha256, repo):
    for v in publicar_cvm.versoes(repo):
        if (v["recurso"], v["arquivo"], v["sha256"]) == (recurso, arquivo, sha256):
            return v
    raise ForaDaRelease(f"{recurso}/{arquivo} {sha256[:12]}: nenhuma versao com byte no "
                        f"registro nem no inventario da CVM; a release so tem o que eles listam")


def trazer(itens, *, repo=None, cache=None, abrir=urllib.request.urlopen, repositorio=None):
    """Poe no cache cada (recurso, arquivo, sha256) de `itens`. Devolve [(nome, situacao)], com
    situacao `ja_no_cache` ou `baixado`. O cache so recebe byte conferido."""
    repo = repo or acervo.raiz_repo()
    cache = cache or os.path.join(repo, acervo.CACHE_RELATIVO)
    out = []
    for recurso, arquivo, sha256 in itens:
        v = _versao(recurso, arquivo, sha256, repo)
        destino = os.path.join(cache, *publicar_cvm.publicavel(v).split("/"))
        nome = publicar_cvm.nome_do_arquivo(v)
        if os.path.exists(destino):
            if armazem_mod.sha256(destino) != sha256:
                raise armazem_mod.ConteudoDivergente(f"{destino} nao tem o sha256 da chave")
            out.append((nome, "ja_no_cache"))
            continue
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        parcial, h = destino + ".parcial", hashlib.sha256()
        url = url_da_versao(v, repositorio)
        try:
            with abrir(url) as r, open(parcial, "wb") as f:
                for bloco in iter(lambda: r.read(BLOCO), b""):
                    h.update(bloco)
                    f.write(bloco)
        except urllib.error.HTTPError as e:
            if os.path.exists(parcial):
                os.remove(parcial)
            raise ForaDaRelease(f"{nome}: a release respondeu HTTP {e.code} em {url}") from e
        if h.hexdigest() != sha256:
            os.remove(parcial)
            raise armazem_mod.ConteudoDivergente(
                f"{nome}: a release entregou sha256 {h.hexdigest()[:12]}, o registro diz "
                f"{sha256[:12]}. Nada foi para o cache.")
        os.replace(parcial, destino)
        out.append((nome, "baixado"))
    return out


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    if not args or len(args) % 3:
        print((__doc__ or "").strip().splitlines()[-1].strip(), file=sys.stderr)
        return 2
    for nome, situacao in trazer(list(zip(args[0::3], args[1::3], args[2::3]))):
        print(f"{situacao}: {nome}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
