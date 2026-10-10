# -*- coding: utf-8 -*-
"""Baixa os recursos do Banco Central e a planilha da APIMEC que o plano da R3 usa (P-170).

POR QUE EXISTE. O plano (docs/marca/rodada3/plano.yaml) guarda o sha256 de cada cadastro, e quem
quiser refazer o sorteio precisa do mesmo arquivo. Os do BCB vem de um servico OData que se
pagina, e o servico tem um defeito que um `curl` solto esconde: responde 500 a `$skip=0`, entao
a primeira pagina vai SEM `$skip`. Aqui a paginacao esta escrita uma vez, com teste.

O QUE ELE NAO FAZ (P5). Nao classifica nada e nao decide filtro: grava o recurso inteiro em
`data/r3/` (fora do git) e imprime linhas, sha256 e data. O servico muda: o sha256 de amanha nao
e o de hoje, e o arquivo de hoje e o que o plano cita. Nao garante que `$top` grande devolva tudo
(o servico corta sozinho); por isso pagina ate vir uma pagina curta.

    python tools/r3_baixar_bcb.py            # os tres arquivos do plano v2
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import sys
import time
import urllib.request
from collections.abc import Callable
from typing import Any

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
OLINDA = "https://olinda.bcb.gov.br/olinda/servico/{servico}/versao/v1/odata/{recurso}"
APIMEC = ("https://www.apimecbrasil.com.br/wp-content/uploads/sites/1125/2026/10/"
          "analistas-de-valores-mobiliarios-pessoa-juridica.xlsx")
PASSO = 5000


def paginar(pegar: Callable[[str], list[dict[str, Any]]], base: str,
            passo: int = PASSO) -> list[dict[str, Any]]:
    """Todas as linhas de um recurso OData. `pegar(url)` devolve a lista `value` da pagina."""
    linhas: list[dict[str, Any]] = []
    pulo = 0
    while True:
        consulta = f"$format=json&$top={passo}" + (f"&$skip={pulo}" if pulo else "")
        pagina = pegar(f"{base}?{consulta}")
        linhas += pagina
        if len(pagina) < passo:
            return linhas
        pulo += passo


def _pegar(url: str) -> list[dict[str, Any]]:
    for tentativa in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=120) as r:
                v: list[dict[str, Any]] = json.load(r)["value"]
                return v
        except OSError as e:
            print(f"  erro ({e}); tentativa {tentativa + 1}", file=sys.stderr)
            time.sleep(2 ** (tentativa + 1))
    raise SystemExit(f"falhou: {url}")


def _gravar(destino: str, dados: bytes, o_que: str) -> None:
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    with open(destino, "wb") as f:
        f.write(dados)
    agora = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
    print(f"{os.path.relpath(destino, RAIZ)}: {o_que}, sha256 {hashlib.sha256(dados).hexdigest()}, "
          f"baixado em {agora}")


def main() -> int:
    bcb = os.path.join(RAIZ, "data", "r3", "bcb")
    for recurso, nome in (("SedesBancoComMultCE", "sedes_banco_com_mult_ce.json"),
                          ("SedesSociedades", "sedes_sociedades.json")):
        linhas = paginar(_pegar, OLINDA.format(servico="Instituicoes_em_funcionamento",
                                               recurso=recurso))
        _gravar(os.path.join(bcb, nome),
                json.dumps(linhas, ensure_ascii=False, separators=(",", ":")).encode("utf-8"),
                f"{len(linhas)} linhas")
    req = urllib.request.Request(APIMEC, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as r:
        xlsx = r.read()
    _gravar(os.path.join(RAIZ, "data", "r3", "apimec", "analistas_pj.xlsx"), xlsx, "planilha")
    return 0


if __name__ == "__main__":
    sys.exit(main())
