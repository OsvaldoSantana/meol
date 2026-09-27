# -*- coding: utf-8 -*-
"""O que os estimulos do teste de marca podem e nao podem ter (P-163).

POR QUE ELE EXISTE. O teste de marca compara DIRECOES VISUAIS. Se o texto, o numero ou a
ordem mudarem entre elas, a comparacao mede o texto, nao o visual -- e ninguem veria,
porque cada arquivo parece certo sozinho. E um estimulo com cor fora do YAML, recurso
remoto ou numero mal formatado quebra a P2, a privacidade de quem abre o arquivo ou o RI-02.

O QUE ELE MEDE (P5). Sobre `docs/marca/direcoes/<direcao>.html`: o texto visivel de cada
estado (normal e parcial) e igual entre as direcoes e contem o que o `conteudo.yaml` diz;
toda cor hexadecimal esta no bloco da direcao em `docs/marca/tokens/direcoes.yaml` e nao ha
rgb()/hsl(); nao ha URL nem recurso remoto; todo valor em reais esta no formato brasileiro;
a frase da camada 1 tem no maximo 15 palavras; nao ha imagem, emoji nem gradiente; todo
botao tem texto. NAO mede: cor nomeada no CSS ("white"), o tamanho real da fonte, o
contraste de um par que o YAML nao declara, nem como a tela fica num aparelho -- isso e do
teste de navegador da etapa 4 e da revisao dele.
"""
from __future__ import annotations

import html
import io
import os
import re
from html.parser import HTMLParser
from typing import Any

import yaml

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
PASTA = os.path.join(RAIZ, "docs", "marca", "direcoes")
TOKENS = os.path.join(RAIZ, "docs", "marca", "tokens", "direcoes.yaml")
CONTEUDO = os.path.join(PASTA, "conteudo.yaml")

HEXCOR = re.compile(r"#(?:[0-9A-Fa-f]{8}|[0-9A-Fa-f]{6}|[0-9A-Fa-f]{3,4})(?![0-9A-Za-z_-])")
FUNCAO_COR = re.compile(r"\b(?:rgba?|hsla?|hwb|lab|lch|oklab|oklch|color)\s*\(", re.I)
REMOTO = re.compile(r"(?:https?:|ftp:|\bsrc\s*=|\bhref\s*=|url\s*\(|@import|<link\b|<script\b|"
                    r"<iframe\b|<object\b|<embed\b|srcset)", re.I)
IMAGEM = re.compile(r"<(?:img|picture|video|audio|canvas|svg)\b|background-image", re.I)
GRADIENTE = re.compile(r"(?:linear|radial|conic)-gradient", re.I)
EMOJI = re.compile("[☀-➿\U0001f000-\U0001faff️]")
MOEDA_OK = re.compile(r"R\$ \d{1,3}(?:\.\d{3})*,\d{2}(?!\d)")
LIMITE_CAMADA_1 = 15   # RI-01: a camada 1 e uma frase curta, no maximo 15 palavras
# Fronteira de bloco vira espaco; elemento de linha (span, strong) nao: "peso-<span>alvo" e
# uma palavra so, e juntar tudo com espaco a partia -- defeito do proprio instrumento, 27/09.
BLOCO = {"p", "h1", "h2", "h3", "dt", "dd", "div", "section", "header", "footer", "nav",
         "main", "button", "li", "dl", "ul", "ol", "br"}


class _Texto(HTMLParser):
    """Texto visivel por estado, os textos de camada 1 e os botoes sem texto."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.pilha: list[str] = []
        self.estado: str | None = None
        self.textos: dict[str, list[str]] = {}
        self.camada1: list[str] = []
        self._c1 = 0
        self.botoes: list[str] = []
        self._botao: list[str] | None = None
        self._ocultar = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = dict(attrs)
        if tag in ("style", "script", "title", "head"):
            self._ocultar += 1
        estado = a.get("data-estado")
        if tag == "section" and estado:
            self.estado = estado
            self.textos.setdefault(estado, [])
        if a.get("data-camada") == "1":
            self._c1 += 1
            self.camada1.append("")
        if tag == "button":
            self._botao = []
        self._fronteira(tag)
        self.pilha.append(tag)

    def _fronteira(self, tag: str) -> None:
        if tag in BLOCO and self.estado is not None and not self._ocultar:
            self.textos[self.estado].append(" ")

    def handle_endtag(self, tag: str) -> None:
        if tag in ("style", "script", "title", "head"):
            self._ocultar -= 1
        self._fronteira(tag)
        if tag == "section":
            self.estado = None
        if tag == "h1" and self._c1:
            self._c1 -= 1
        if tag == "button" and self._botao is not None:
            self.botoes.append(" ".join("".join(self._botao).split()))
            self._botao = None
        if self.pilha:
            self.pilha.pop()

    def handle_data(self, data: str) -> None:
        if self._ocultar:
            return
        if self.estado is not None:
            self.textos[self.estado].append(data)
        if self._c1:
            self.camada1[-1] += data
        if self._botao is not None:
            self._botao.append(data)


def ler(path: str) -> str:
    with io.open(path, encoding="utf-8") as f:
        return f.read()


def direcoes(pasta: str = PASTA) -> dict[str, str]:
    return {n[:-5]: os.path.join(pasta, n) for n in sorted(os.listdir(pasta))
            if n.endswith(".html")}


def analisar(fonte: str) -> _Texto:
    p = _Texto()
    p.feed(fonte)
    return p


def texto_por_estado(fonte: str) -> dict[str, str]:
    """Texto visivel normalizado (espacos colapsados; o U+00A0 fica)."""
    t = analisar(fonte).textos
    return {k: re.sub(r"[ \t\r\n]+", " ", "".join(v)).strip() for k, v in t.items()}


def cores_fora_do_yaml(fonte: str, cores: dict[str, str]) -> list[str]:
    permitidas = {c.upper() for c in cores.values()}
    achadas = [m.group(0).upper() for m in HEXCOR.finditer(fonte)]
    return sorted({c for c in achadas if c not in permitidas}) + \
        sorted({m.group(0) for m in FUNCAO_COR.finditer(fonte)})


def remotos(fonte: str) -> list[str]:
    return [m.group(0) for m in REMOTO.finditer(fonte)]


def moeda_fora_do_formato(texto: str) -> list[str]:
    """Todo 'R$' do texto visivel tem de casar com o formato brasileiro inteiro."""
    ruins = []
    for m in re.finditer(r"R\$", texto):
        trecho = texto[m.start():m.start() + 24]
        if not MOEDA_OK.match(trecho):
            ruins.append(trecho.split(" e ")[0])
    # numero decimal com ponto (R$ 70.000.00) ou virgula de milhar (16,900) sem R$ na frente
    ruins += re.findall(r"\b\d{1,3}(?:,\d{3})+(?:\.\d{2})?\b", texto)
    return ruins


def camada1_longa(fonte: str) -> list[str]:
    return [t for t in analisar(fonte).camada1
            if len(html.unescape(t).split()) > LIMITE_CAMADA_1]


def proibidos(fonte: str) -> list[str]:
    out = [m.group(0) for m in IMAGEM.finditer(fonte)]
    out += [m.group(0) for m in GRADIENTE.finditer(fonte)]
    out += [f"emoji U+{ord(m.group(0)):04X}" for m in EMOJI.finditer(fonte)]
    out += ["botao sem texto" for b in analisar(fonte).botoes if not b]
    return out


def tokens() -> dict[str, Any]:
    with io.open(TOKENS, encoding="utf-8") as f:
        return yaml.safe_load(f)


def conteudo() -> dict[str, Any]:
    with io.open(CONTEUDO, encoding="utf-8") as f:
        return yaml.safe_load(f)


def textos_obrigatorios(c: dict[str, Any], rotulos: dict[str, str]) -> dict[str, list[str]]:
    """O que o conteudo.yaml manda aparecer em cada estado (P1: o numero e o do motor)."""
    n, p = c["normal"], c["parcial"]
    comuns = [n["frase_decisao"], n["porque"], n["valor_fmt"], n["destino"],
              n["data_referencia"]]
    return {"normal": comuns + [n["custo_compra_fmt"], rotulos["completo"]],
            "parcial": comuns + [p["faixa_fmt"], p["motivo"], rotulos["parcial"]]}
