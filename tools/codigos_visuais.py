# -*- coding: utf-8 -*-
"""O classificador do livro de codigos visuais do veto de distincao (P-162).

POR QUE EXISTE. O veto (decisao dele, 27/09/2026) compara a direcao vencedora com o codigo
visual dominante das categorias concorrentes auditadas na R3. Se as direcoes e as marcas
fossem classificadas por regras diferentes -- ou pela mesma regra escrita duas vezes -- o
veto mediria a diferenca entre duas maos. Aqui fica a regra UMA vez, lida de
`docs/marca/teste-de-marca/codigos-visuais.yaml`, e as tres direcoes sao classificadas AGORA,
antes da R3, a partir dos proprios estimulos: tokens (`docs/marca/tokens/direcoes.yaml`) e o
CSS do HTML (`docs/marca/direcoes/<X>.html`).

O QUE ELE NAO FAZ (P5). Nao mede captura de tela de marca: a R3 mede os valores (cor de
fundo, cor do botao, familia, raio, blocos) e os passa para `classificar()`. Nao le a
densidade das direcoes no HTML: e contagem na imagem, gravada no YAML com a lista dos blocos.
A familia da fonte vem do generico no fim da pilha do CSS (serif, sans-serif, monospace), que
e o que o autor declarou, nao uma leitura do desenho das letras.

    python tools/codigos_visuais.py        # a classificacao de E, C e D
"""
from __future__ import annotations

import colorsys
import os
import re
import sys
from collections import Counter
from typing import Any

import yaml

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIVRO = os.path.join(RAIZ, "docs", "marca", "teste-de-marca", "codigos-visuais.yaml")
TOKENS = os.path.join(RAIZ, "docs", "marca", "tokens", "direcoes.yaml")
HTML = os.path.join(RAIZ, "docs", "marca", "direcoes", "{d}.html")
CENTRAIS = ("fundo", "matiz", "familia_do_titulo", "raio")
GENERICO = {"serif": "serifa", "sans-serif": "sem_serifa", "monospace": "monoespacada"}


def ler_livro(path: str = LIVRO) -> dict[str, Any]:
    with open(path, encoding="utf-8") as f:
        d: dict[str, Any] = yaml.safe_load(f)
    return d


def _rgb(hexa: str) -> tuple[float, float, float]:
    h = hexa.lstrip("#")
    return (int(h[0:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:6], 16) / 255)


def luminancia(hexa: str) -> float:
    """Luminancia relativa da WCAG 2.2 (a mesma de auditoria/contraste_tokens.py)."""
    def lin(c: float) -> float:
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(c) for c in _rgb(hexa))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def matiz_saturacao(hexa: str) -> tuple[float, float]:
    """(matiz HSL em graus, saturacao HSL de 0 a 1)."""
    h, _l, s = colorsys.rgb_to_hls(*_rgb(hexa))
    return h * 360.0, s


def faixa_de_matiz(hexa: str, livro: dict[str, Any]) -> str:
    m = livro["variaveis"]["matiz"]
    graus, sat = matiz_saturacao(hexa)
    if sat < m["saturacao_minima"]:
        return "neutro"
    for f in m["faixas"]:
        de, ate = f["de"], f["ate"]
        dentro = de <= graus < ate if de < ate else (graus >= de or graus < ate)
        if dentro:
            return str(f["nome"])
    raise ValueError(f"matiz {graus} fora de todas as faixas: o livro tem buraco")


def classificar(medidas: dict[str, Any], livro: dict[str, Any] | None = None) -> dict[str, str]:
    """Os seis valores de uma tela a partir do que se mediu nela.

    medidas: fundo_hex, destaque_hex, familia_generica (serif | sans-serif | monospace),
    raio_px, densidade_blocos, botao (cheio | vazado)."""
    livro = ler_livro() if livro is None else livro
    v = livro["variaveis"]
    raio = float(medidas["raio_px"])
    lim_r = v["raio"]["limites_px"]
    blocos = int(medidas["densidade_blocos"])
    lim_d = v["densidade"]["limites"]
    out = {
        "fundo": ("claro" if luminancia(medidas["fundo_hex"]) > v["fundo"]["limiar_luminancia"]
                  else "escuro"),
        "matiz": faixa_de_matiz(medidas["destaque_hex"], livro),
        "familia_do_titulo": GENERICO[medidas["familia_generica"]],
        "raio": ("reto" if raio <= lim_r["reto_ate"] else
                 "pequeno" if raio <= lim_r["pequeno_ate"] else "grande"),
        "densidade": ("baixa" if blocos <= lim_d["baixa_ate"] else
                      "media" if blocos <= lim_d["media_ate"] else "alta"),
        "botao": str(medidas["botao"]),
    }
    for var, valor in out.items():
        if valor not in v[var]["valores"]:
            raise ValueError(f"{var}={valor} fora dos valores fechados do livro")
    return out


# ---------------------------------------------------------------- as direcoes E, C, D ---

def _regras_css(html: str) -> list[tuple[list[str], dict[str, str]]]:
    css = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", html, re.S))
    regras = []
    for sel, corpo in re.findall(r"([^{}]+)\{([^{}]*)\}", css):
        decl = {}
        for k, val in re.findall(r"([-\w]+)\s*:\s*([^;]+);?", corpo):
            decl[k.strip()] = val.strip()
        regras.append(([s.strip() for s in sel.split(",")], decl))
    return regras


def _var(valor: str, raiz: dict[str, str]) -> str:
    m = re.fullmatch(r"var\((--[\w-]+)\)", valor.strip())
    return raiz[m.group(1)] if m else valor


def medidas_da_direcao(d: str, livro: dict[str, Any] | None = None) -> dict[str, Any]:
    """O que se mede numa direcao: cores e botao dos tokens; fonte do titulo e raio do botao
    principal no CSS do estimulo; densidade da contagem gravada no livro."""
    livro = ler_livro() if livro is None else livro
    with open(TOKENS, encoding="utf-8") as f:
        tok = yaml.safe_load(f)["direcoes"][d]
    with open(HTML.format(d=d), encoding="utf-8") as f:
        regras = _regras_css(f.read())
    raiz: dict[str, str] = {}
    for sels, decl in regras:
        if ":root" in sels:
            raiz.update({k: v for k, v in decl.items() if k.startswith("--")})
    fonte = raio = None
    for sels, decl in regras:
        if "body" in sels and "font-family" in decl and fonte is None:
            fonte = decl["font-family"]
    for sels, decl in regras:
        # o texto de maior corpo da tela e o h1.decisao nas tres direcoes (a camada 1)
        if ".decisao" in sels and "font-family" in decl:
            fonte = decl["font-family"]
        if ".primario" in sels and "border-radius" in decl:
            raio = decl["border-radius"]
    if fonte is None:
        raise ValueError(f"{d}: sem font-family no body nem no .decisao")
    generico = _var(fonte, raiz).split(",")[-1].strip().strip("'\"")
    raio_px = float(re.match(r"[\d.]+", raio).group(0)) if raio else 0.0  # type: ignore[union-attr]
    return {
        "fundo_hex": tok["cores"]["fundo"],
        "destaque_hex": tok["cores"]["destaque"],
        "familia_generica": generico,
        "raio_px": raio_px,
        "densidade_blocos": livro["direcoes"][d]["densidade_blocos"],
        "botao": tok["forma"]["botao"],
    }


def classificar_direcoes(livro: dict[str, Any] | None = None) -> dict[str, dict[str, str]]:
    livro = ler_livro() if livro is None else livro
    return {d: classificar(medidas_da_direcao(d, livro), livro) for d in ("E", "C", "D")}


# ---------------------------------------------------------------- o veto -----------------

def codigos_dominantes(marcas: list[dict[str, str]], livro: dict[str, Any] | None = None
                       ) -> list[tuple[str, ...]]:
    """As combinacoes das quatro variaveis centrais (aa-a) presentes em pelo menos metade das
    marcas da categoria. Com menos de n_minimo marcas, a categoria nao tem codigo dominante."""
    livro = ler_livro() if livro is None else livro
    veto = livro["veto"]
    if len(marcas) < veto["n_minimo_de_marcas"]:
        return []
    cont = Counter(tuple(m[v] for v in CENTRAIS) for m in marcas)
    return sorted(c for c, n in cont.items() if n / len(marcas) >= veto["fracao_minima"])


def imita(direcao: dict[str, str], dominantes: list[tuple[str, ...]]) -> bool:
    """Imitar = partilhar os quatro valores centrais com um codigo dominante."""
    return tuple(direcao[v] for v in CENTRAIS) in dominantes


def main() -> int:
    livro = ler_livro()
    print("direcao | " + " | ".join(livro["variaveis"]))
    for d, c in classificar_direcoes(livro).items():
        print(f"{d} | " + " | ".join(c[v] for v in livro["variaveis"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
