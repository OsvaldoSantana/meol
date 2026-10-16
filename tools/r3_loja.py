# -*- coding: utf-8 -*-
"""A rota da App Store da R3: a busca de app por marca e os quadros publicos de Financas (P-170).

POR QUE EXISTE. A decisao ae-a (dele, 02/10) manda ler a marca COM app pela 1a captura de
interface da App Store do Brasil; o site so vale para marca SEM app. De 04 a 11/10, 83 linhas
pararam em `AGUARDA DEGRAU 4` porque o SITE recusou o IP da nuvem, sem a pergunta "esta marca tem
app?" (Itau, BB, Santander, C6, Mercado Pago, XP, BTG...). Este script faz a pergunta, do jeito
que o plano v3 (docs/marca/rodada3/plano.yaml -> loja) escreveu antes da primeira busca: os dois
termos, o intervalo minimo entre consultas e a espera crescente no 403. E baixa os tres quadros
publicos de Financas (fila 28: o universo de robo e consolidador), com data e sha256.

O QUE ELE NAO FAZ (P5). Nao decide se o app e "do mesmo grupo e com a marca": grava o que a loja
devolveu (vendedor, desenvolvedor, nome do app) e quem le decide, com o motivo escrito em
leituras.yaml. Nao baixa as capturas do app (isso e `r3_capturar.py app <trackId>`). Nao grava no
git: as respostas da loja ficam em data/r3/loja/ (ignorado), e o sha256 vai para o registro.

    python tools/r3_loja.py pendentes            # busca as linhas AGUARDA DEGRAU 4 do CSV
    python tools/r3_loja.py pendentes --so bancos:5 corretora:3
    python tools/r3_loja.py quadros              # os tres quadros de Financas (topfree...)
    python tools/r3_loja.py termos robo          # o segundo quadro (termos fixos do plano)

O 403 DA APPLE (10/10/2026, medido pela arquitetura da nuvem): a 6a consulta seguida volta 403
e a mesma consulta volta 200 depois de esperar. E frequencia, nao bloqueio: depois da ultima
espera a busca falha alto, e nunca vira "sem app" (5-B.16).
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable
from typing import Any

import yaml

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
PLANO = os.path.join(RAIZ, "docs", "marca", "rodada3", "plano.yaml")
CSV = os.path.join(RAIZ, "docs", "marca", "rodada3", "classificacao.csv")
SAIDA = os.path.join(RAIZ, "data", "r3", "loja")
AGUARDA = "AGUARDA DEGRAU 4"

# Sufixos publicos que aparecem nos sites da R3. O que nao esta aqui cai no ultimo rotulo antes
# do TLD de um nivel, que e o caso comum (.com, .net, .io).
SUFIXOS = ("com.br", "net.br", "org.br", "gov.br", "coop.br", "art.br", "inf.br", "b.br",
           "bank.br", "com", "net", "org", "io", "app", "br", "co", "digital", "finance",
           "bank", "investments", "capital", "tech")


# ------------------------------------------------------------------ funcoes puras (testadas) ---

def dominio_base(url: str) -> str:
    """O nome do dominio sem www e sem o sufixo publico (plano v3, termo 2):
    https://www.sofisa.com.br/x -> sofisa; wealth.highpar.com.br -> highpar."""
    host = urllib.parse.urlsplit(url if "//" in url else "//" + url).hostname or ""
    rotulos = [r for r in host.lower().split(".") if r]
    if rotulos[:1] == ["www"]:
        rotulos = rotulos[1:]
    for suf in sorted(SUFIXOS, key=lambda s: -s.count(".")):
        partes = suf.split(".")
        if len(rotulos) > len(partes) and rotulos[-len(partes):] == partes:
            return rotulos[-len(partes) - 1]
    return rotulos[-2] if len(rotulos) >= 2 else (rotulos[0] if rotulos else "")


def termos_da_linha(marca: str, url: str) -> list[str]:
    """Os termos do plano, na ordem, sem repetir (a marca 'Sofisa' e o dominio 'sofisa')."""
    out: list[str] = []
    for t in (marca.strip(), dominio_base(url) if url else ""):
        if t and t.lower() not in (o.lower() for o in out):
            out.append(t)
    return out


def url_busca(modelo: str, termo: str, limite: int) -> str:
    return (modelo.replace("<termo>", urllib.parse.quote_plus(termo))
            .replace("<limite>", str(int(limite))))


class Espacador:
    """Intervalo minimo entre consultas e espera crescente no 403 (plano v3 -> loja).

    `consultar(fazer)` dorme o que falta para o intervalo desde a ultima consulta, chama `fazer` e,
    se ela levantar HTTPError 403, dorme a proxima espera da lista e tenta de novo. Esgotada a
    lista, o 403 sobe: a linha nao vira "sem app" por frequencia."""

    def __init__(self, intervalo_s: float, esperas_s: list[float],
                 dormir: Callable[[float], None] = time.sleep,
                 relogio: Callable[[], float] = time.monotonic) -> None:
        self.intervalo = float(intervalo_s)
        self.esperas = [float(e) for e in esperas_s]
        self.dormir = dormir
        self.relogio = relogio
        self.ultima: float | None = None
        self.n_403 = 0

    def _aguardar_vez(self) -> None:
        if self.ultima is not None:
            falta = self.intervalo - (self.relogio() - self.ultima)
            if falta > 0:
                self.dormir(falta)
        self.ultima = self.relogio()

    def consultar(self, fazer: Callable[[], Any]) -> Any:
        for espera in [*self.esperas, None]:
            self._aguardar_vez()
            try:
                return fazer()
            except urllib.error.HTTPError as e:
                if e.code != 403 or espera is None:
                    raise
                self.n_403 += 1
                self.dormir(espera)
        raise AssertionError("inalcancavel")


def resumo_app(r: dict[str, Any]) -> dict[str, Any]:
    """O que o criterio do plano olha: o nome do app, o vendedor e o desenvolvedor."""
    return {k: r.get(k) for k in ("trackId", "trackName", "sellerName", "artistName",
                                  "bundleId", "primaryGenreName", "trackViewUrl")}


def pendentes(linhas: list[dict[str, str]], so: list[str] | None = None
              ) -> list[dict[str, str]]:
    """As linhas AGUARDA DEGRAU 4, pela ordem do sorteio dentro de cada categoria sorteada."""
    alvo = None
    if so:
        alvo = {(c, int(o)) for c, _, o in (s.rpartition(":") for s in so)}
    out = [r for r in linhas if AGUARDA in r["motivo"]
           and (alvo is None or (r["categoria_sorteada"], int(r["ordem_no_sorteio"])) in alvo)]
    return sorted(out, key=lambda r: (r["categoria_sorteada"], int(r["ordem_no_sorteio"])))


def entradas_do_quadro(dados: dict[str, Any]) -> list[dict[str, Any]]:
    """As entradas do RSS JSON da Apple: posicao, trackId, nome, vendedor e o resumo."""
    brutas = dados.get("feed", {}).get("entry", [])
    if isinstance(brutas, dict):  # quadro com um app so: a Apple devolve objeto, nao lista
        brutas = [brutas]
    out = []
    for k, e in enumerate(brutas, start=1):
        out.append({"posicao": k,
                    "trackId": int(e["id"]["attributes"]["im:id"]),
                    "nome": e["im:name"]["label"],
                    "vendedor": e.get("im:artist", {}).get("label"),
                    "resumo": (e.get("summary") or {}).get("label", "")})
    return out


def uniao_dos_quadros(quadros: dict[str, list[dict[str, Any]]], ordem: list[str]
                      ) -> list[dict[str, Any]]:
    """Plano v3 (ordem_base): um trackId uma vez, na ordem dos quadros e da posicao."""
    vistos: set[int] = set()
    out = []
    for nome in ordem:
        for e in quadros.get(nome, []):
            if e["trackId"] not in vistos:
                vistos.add(e["trackId"])
                out.append({**e, "quadro": nome})
    return out


def sha256(dados: bytes) -> str:
    return hashlib.sha256(dados).hexdigest()


# ------------------------------------------------------------------------- o que toca rede ---

def _baixar(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        dados: bytes = r.read()
        return dados


def _gravar(caminho: str, dados: bytes) -> None:
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "wb") as f:
        f.write(dados)


def ler_plano() -> dict[str, Any]:
    with open(PLANO, encoding="utf-8") as f:
        plano: dict[str, Any] = yaml.safe_load(f)
        return plano


def buscar(termo: str, loja: dict[str, Any], esp: Espacador, destino: str) -> dict[str, Any]:
    url = url_busca(loja["busca"], termo, loja["limite"])
    dados = esp.consultar(lambda: _baixar(url))
    _gravar(destino, dados)
    res = json.loads(dados)["results"]
    return {"termo": termo, "url": url, "sha256": sha256(dados),
            "baixado_em": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
            "arquivo": os.path.relpath(destino, RAIZ).replace(os.sep, "/"),
            "resultados": [resumo_app(r) for r in res]}


def _ler_csv() -> list[dict[str, str]]:
    with open(CSV, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def cmd_pendentes(so: list[str] | None) -> int:
    loja = ler_plano()["loja"]
    esp = Espacador(loja["intervalo_minimo_s"], loja["espera_no_403_s"])
    for r in pendentes(_ler_csv(), so):
        chave = f"{r['categoria_sorteada']}-{int(r['ordem_no_sorteio']):03d}"
        buscas = []
        for k, termo in enumerate(termos_da_linha(r["marca"], r["url"]), start=1):
            buscas.append(buscar(termo, loja, esp,
                                 os.path.join(SAIDA, "busca", f"{chave}-termo{k}.json")))
        reg = {"categoria_sorteada": r["categoria_sorteada"],
               "ordem": int(r["ordem_no_sorteio"]), "marca": r["marca"], "cnpj": r["cnpj"],
               "url": r["url"], "buscas": buscas}
        with open(os.path.join(SAIDA, "busca", f"{chave}.json"), "w", encoding="utf-8") as f:
            json.dump(reg, f, ensure_ascii=False, indent=1)
        nomes = "; ".join(f"[{b['termo']}] " + " | ".join(
            f"{a['trackName']} ({a['sellerName']})" for a in b["resultados"][:5])
            for b in buscas)
        print(f"{chave} {r['marca']}: {nomes}", flush=True)
    print(f"RESUMO: 403 da loja absorvidos pela espera: {esp.n_403}")
    return 0


def cmd_quadros() -> int:
    plano = ler_plano()["universos_da_loja"]
    esp = Espacador(ler_plano()["loja"]["intervalo_minimo_s"],
                    ler_plano()["loja"]["espera_no_403_s"])
    hoje = dt.date.today().isoformat()
    quadros = {}
    for nome, url in plano["quadros"].items():
        dados = esp.consultar(lambda u=url: _baixar(u))  # type: ignore[misc]
        destino = os.path.join(SAIDA, "quadros", f"{nome}-{hoje}.json")
        _gravar(destino, dados)
        quadros[nome] = entradas_do_quadro(json.loads(dados))
        print(f"{nome}: {len(quadros[nome])} apps, sha256 {sha256(dados)}, "
              f"{os.path.relpath(destino, RAIZ)}, baixado_em {hoje}")
    uniao = uniao_dos_quadros(quadros, list(plano["quadros"]))
    destino = os.path.join(SAIDA, "quadros", f"uniao-{hoje}.json")
    with open(destino, "w", encoding="utf-8") as f:
        json.dump(uniao, f, ensure_ascii=False, indent=1)
    print(f"uniao: {len(uniao)} apps distintos em {os.path.relpath(destino, RAIZ)}")
    return 0


def cmd_termos(categoria: str) -> int:
    plano = ler_plano()
    seg = plano["universos_da_loja"]["segundo_quadro"]
    loja = {**plano["loja"], "limite": seg["limite_por_termo"]}
    esp = Espacador(loja["intervalo_minimo_s"], loja["espera_no_403_s"])
    hoje = dt.date.today().isoformat()
    for k, termo in enumerate(seg[categoria], start=1):
        b = buscar(termo, loja, esp,
                   os.path.join(SAIDA, "segundo", f"{categoria}-{hoje}-termo{k}.json"))
        print(f"[{termo}] sha256 {b['sha256']}: " + " | ".join(
            f"{a['trackId']} {a['trackName']} ({a['sellerName']})" for a in b["resultados"]))
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=(__doc__ or "").split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("pendentes")
    p.add_argument("--so", nargs="+", metavar="CATEGORIA:ORDEM")
    sub.add_parser("quadros")
    t = sub.add_parser("termos")
    t.add_argument("categoria", choices=["robo", "consolidador"])
    a = ap.parse_args(argv)
    # 16/10/2026: no Windows o stdout e cp1252, e um nome de app com caractere fora dele (emoji,
    # letra arabe) derrubou a busca na 30a linha. A saida e UTF-8 em toda maquina.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if a.cmd == "pendentes":
        return cmd_pendentes(a.so)
    if a.cmd == "quadros":
        return cmd_quadros()
    return cmd_termos(a.categoria)


if __name__ == "__main__":
    sys.exit(main())
