# -*- coding: utf-8 -*-
"""Serve a pagina do teste de marca localmente, com o banco SIMULADO (S6, P-162).

POR QUE EXISTE. A pagina (`pesquisa/`) so funciona com as duas funcoes da Vercel e o
Supabase, que sao contas dele. Para ver a pagina rodar nesta maquina -- e para os testes no
Chromium sem interface -- este servidor faz o papel das duas funcoes, em memoria:
  POST /api/abrir   soma 1 ao contador e devolve {id_resposta, versao}, versao = (contador
                    mod n_versoes) + 1, a mesma regra de public.abrir_resposta() (esquema.sql)
  POST /api/enviar  guarda o corpo em memoria e devolve 204
Nada vai para disco, nada sai da maquina, e nenhuma linha de acesso e escrita (o log padrao
do http.server esta desligado).

O QUE ELE NAO FAZ (P5). Nao valida o envio como a funcao da Vercel valida (essa validacao e a
de pesquisa/api/_comum.js, testada a parte); nao imita o banco (as regras dele estao no
esquema.sql e no teste_politicas.sql). Serve so para ver a pagina e para os testes.

    python tools/servir_pesquisa.py              # http://127.0.0.1:8000/
    python tools/servir_pesquisa.py --porta 8123
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import threading
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PESQUISA = os.path.join(RAIZ, "pesquisa")
TIPOS = {".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8",
         ".css": "text/css; charset=utf-8", ".json": "application/json; charset=utf-8",
         ".png": "image/png"}
SERVIDOS = (".html", ".js", ".css", ".json", ".png")


class Simulador:
    """O estado do banco simulado, e os ganchos que so os testes usam."""

    def __init__(self, pasta: str = PESQUISA, exposicao_segundos: float | None = None,
                 script_injetado: str | None = None, abrir_falha: bool = False) -> None:
        self.pasta = pasta
        self.exposicao_segundos = exposicao_segundos   # teste: outra duracao no JSON servido
        self.script_injetado = script_injetado         # teste: automacao de cliques
        self.abrir_falha = abrir_falha                 # teste: /api/abrir devolve erro
        self.contador = 0
        self.aberturas: list[dict[str, Any]] = []
        self.envios: list[dict[str, Any]] = []
        self._trava = threading.Lock()
        with open(os.path.join(pasta, "questionario.json"), encoding="utf-8") as f:
            self.n_versoes = len(json.load(f)["questionario"]["ordens"]["versoes"])

    def abrir(self) -> dict[str, Any]:
        with self._trava:
            versao = self.contador % self.n_versoes + 1
            self.contador += 1
            d = {"id_resposta": str(uuid.uuid4()), "versao": versao}
            self.aberturas.append(d)
            return d

    def conteudo(self, rel: str) -> bytes | None:
        """O arquivo servido, com os ganchos de teste aplicados; None se nao existe."""
        if rel in ("", "/"):
            rel = "index.html"
        rel = rel.lstrip("/")
        if rel == "_auto.js" and self.script_injetado is not None:
            return self.script_injetado.encode("utf-8")
        alvo = os.path.realpath(os.path.join(self.pasta, *rel.split("/")))
        if (not alvo.startswith(os.path.realpath(self.pasta) + os.sep)
                or not alvo.endswith(SERVIDOS) or not os.path.isfile(alvo)
                or os.sep + "api" + os.sep in alvo or os.sep + "supabase" + os.sep in alvo):
            return None
        with open(alvo, "rb") as f:
            dados = f.read()
        if rel == "questionario.json" and self.exposicao_segundos is not None:
            j = json.loads(dados)
            j["questionario"]["telas"]["exposicao_segundos"] = self.exposicao_segundos
            dados = json.dumps(j).encode("utf-8")
        if rel == "index.html" and self.script_injetado is not None:
            dados = dados.replace(b"</head>", b'<script src="_auto.js" defer></script>\n</head>')
        return dados


def _manipulador(sim: Simulador) -> type[BaseHTTPRequestHandler]:
    class Manipulador(BaseHTTPRequestHandler):
        def log_message(self, format: str, *args: Any) -> None:  # noqa: A002
            return   # privacidade: nem o servidor local registra acesso

        def _responder(self, codigo: int, corpo: bytes = b"", tipo: str | None = None) -> None:
            self.send_response(codigo)
            if tipo:
                self.send_header("Content-Type", tipo)
            self.send_header("Content-Length", str(len(corpo)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            if corpo:
                self.wfile.write(corpo)

        def do_GET(self) -> None:  # noqa: N802
            caminho = self.path.split("?")[0]
            dados = sim.conteudo(caminho)
            if dados is None:
                self._responder(404)
                return
            ext = os.path.splitext(caminho if caminho not in ("", "/") else "index.html")[1]
            self._responder(200, dados, TIPOS.get(ext, "application/octet-stream"))

        def do_POST(self) -> None:  # noqa: N802
            n = int(self.headers.get("Content-Length") or 0)
            corpo = self.rfile.read(n) if n else b""
            if self.path == "/api/abrir":
                if sim.abrir_falha:
                    self._responder(502, b'{"erro":"abertura"}', TIPOS[".json"])
                    return
                self._responder(200, json.dumps(sim.abrir()).encode("utf-8"), TIPOS[".json"])
            elif self.path == "/api/enviar":
                try:
                    sim.envios.append(json.loads(corpo))
                except ValueError:
                    self._responder(400)
                    return
                self._responder(204)
            else:
                self._responder(404)
    return Manipulador


def servir(sim: Simulador, porta: int = 0) -> tuple[ThreadingHTTPServer, str]:
    """Sobe o servidor numa thread; devolve o servidor e a URL. Porta 0 = uma livre."""
    httpd = ThreadingHTTPServer(("127.0.0.1", porta), _manipulador(sim))
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, f"http://127.0.0.1:{httpd.server_address[1]}/"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=(__doc__ or "").split("\n")[0])
    ap.add_argument("--porta", type=int, default=8000)
    a = ap.parse_args(argv)
    httpd, url = servir(Simulador(), a.porta)
    print(f"pagina da pesquisa em {url} (banco simulado, em memoria; Ctrl+C encerra)")
    try:
        threading.Event().wait()
    except KeyboardInterrupt:
        httpd.shutdown()
    return 0


if __name__ == "__main__":
    sys.exit(main())
