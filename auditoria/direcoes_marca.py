# -*- coding: utf-8 -*-
"""O que os estimulos do teste de marca podem e nao podem ter (P-163).

POR QUE ELE EXISTE. O teste de marca compara DIRECOES VISUAIS. Se o texto, o numero ou a
ordem mudarem entre elas, a comparacao mede o texto, nao o visual -- e ninguem veria,
porque cada arquivo parece certo sozinho. E um estimulo com cor fora do YAML, recurso
remoto ou numero mal formatado quebra a P2, a privacidade de quem abre o arquivo ou o RI-02.

O QUE ELE MEDE (P5). Sobre `docs/marca/direcoes/<direcao>.html`, em cada versao ("base" e
"com_rota_bloqueada", S4): o texto visivel e igual entre as direcoes e contem o que o
`conteudo.yaml` diz; as duas versoes diferem SO no elemento `data-diferenca` (a linha da rota
bloqueada, j-A); nenhum ticker do catalogo do motor aparece (l-B); toda cor hexadecimal esta
no bloco da direcao em `docs/marca/tokens/direcoes.yaml` e nao ha rgb()/hsl(); o unico url()
permitido aponta para uma fonte embutida em `docs/marca/tipografia/` com o `OFL.txt` ao lado
(i-A); todo real esta no formato brasileiro; a frase da camada 1 tem no maximo 15 palavras;
nao ha imagem, emoji nem gradiente; todo SVG esta dentro de um `data-provisorio` e nao tem
texto (k-A, P-168); todo botao tem texto. NAO mede: cor nomeada no CSS ("white"), o tamanho
real da fonte, o contraste de um par que o YAML nao declara, se a ilustracao "imita um cartao
real", nem como a tela fica num aparelho -- isso e da revisao dele e da etapa 4.
"""
from __future__ import annotations

import html
import io
import os
import re
import sys
from html.parser import HTMLParser
from typing import Any

import yaml

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
PASTA = os.path.join(RAIZ, "docs", "marca", "direcoes")
TIPOGRAFIA = os.path.join(RAIZ, "docs", "marca", "tipografia")
TOKENS = os.path.join(RAIZ, "docs", "marca", "tokens", "direcoes.yaml")
CONTEUDO = os.path.join(PASTA, "conteudo.yaml")
VERSOES = ("base", "com_rota_bloqueada")

HEXCOR = re.compile(r"#(?:[0-9A-Fa-f]{8}|[0-9A-Fa-f]{6}|[0-9A-Fa-f]{3,4})(?![0-9A-Za-z_-])")
FUNCAO_COR = re.compile(r"\b(?:rgba?|hsla?|hwb|lab|lch|oklab|oklch|color)\s*\(", re.I)
REMOTO = re.compile(r"(?:https?:|ftp:|//[a-z0-9]|\bsrc\s*=|\bhref\s*=|@import|<link\b|<script\b|"
                    r"<iframe\b|<object\b|<embed\b|srcset)", re.I)
URL = re.compile(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)", re.I)
FONT_FACE = re.compile(r"@font-face\s*\{([^}]*)\}", re.I)
IMAGEM = re.compile(r"<(?:img|picture|video|audio|canvas|image)\b|background-image", re.I)
GRADIENTE = re.compile(r"(?:linear|radial|conic)-gradient", re.I)
EMOJI = re.compile("[\u2600-\u27bf\U0001f000-\U0001faff\ufe0f]")
MOEDA_OK = re.compile(r"R\$\u00a0\d{1,3}(?:\.\d{3})*,\d{2}(?!\d)")
TICKER = re.compile(r"\b[A-Z]{4}\d{1,2}\b")
LIMITE_CAMADA_1 = 15   # RI-01: a camada 1 e uma frase curta, no maximo 15 palavras
# Fronteira de bloco vira espaco; elemento de linha (span, strong) nao: "peso-<span>alvo" e
# uma palavra so, e juntar tudo com espaco a partia -- defeito do proprio instrumento, 27/09.
BLOCO = {"p", "h1", "h2", "h3", "dt", "dd", "div", "section", "header", "footer", "nav",
         "main", "button", "li", "dl", "ul", "ol", "br"}
SEM_TEXTO_EM_SVG = {"text", "tspan", "textpath", "title", "desc", "a", "image", "foreignobject",
                    "use"}


class _Texto(HTMLParser):
    """Texto visivel por versao (com e sem o elemento de diferenca), camada 1, botoes, SVG."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.versao: str | None = None
        self.textos: dict[str, list[str]] = {}
        self.sem_diferenca: dict[str, list[str]] = {}
        self.diferencas: dict[str, list[str]] = {}
        self.camada1: list[str] = []
        self._c1 = 0
        self.botoes: list[str] = []
        self._botao: list[str] | None = None
        self._ocultar = 0
        self._dif = 0
        self._pilha: list[tuple[str, bool, bool]] = []   # (tag, abriu_diferenca, provisorio)
        self._provisorio = 0
        self._svg = 0
        self.svg_fora_de_provisorio = 0
        self.svg_com_texto: list[str] = []
        self.provisorios: list[str] = []

    def _fronteira(self, tag: str) -> None:
        if tag in BLOCO and self.versao is not None and not self._ocultar:
            for alvo in (self.textos, self.sem_diferenca):
                alvo[self.versao].append(" ")

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = dict(attrs)
        if tag in ("style", "script", "title", "head"):
            self._ocultar += 1
        versao = a.get("data-versao")
        if tag == "section" and versao:
            self.versao = versao
            for alvo in (self.textos, self.sem_diferenca, self.diferencas):
                alvo.setdefault(versao, [])
        if a.get("data-camada") == "1":
            self._c1 += 1
            self.camada1.append("")
        if tag == "button":
            self._botao = []
        dif = a.get("data-diferenca") is not None
        prov = a.get("data-provisorio") is not None
        if prov:
            self._provisorio += 1
            self.provisorios.append(a.get("data-provisorio") or "")
        if tag == "svg":
            self._svg += 1
            if not self._provisorio:
                self.svg_fora_de_provisorio += 1
        elif self._svg and tag.lower() in SEM_TEXTO_EM_SVG:
            self.svg_com_texto.append(tag)
        if dif:
            self._dif += 1
        self._fronteira(tag)
        self._pilha.append((tag, dif, prov))

    def handle_endtag(self, tag: str) -> None:
        if tag in ("style", "script", "title", "head"):
            self._ocultar -= 1
        self._fronteira(tag)
        if tag == "section":
            self.versao = None
        if tag == "h1" and self._c1:
            self._c1 -= 1
        if tag == "button" and self._botao is not None:
            self.botoes.append(" ".join("".join(self._botao).split()))
            self._botao = None
        if tag == "svg" and self._svg:
            self._svg -= 1
        while self._pilha:
            t, dif, prov = self._pilha.pop()
            if dif:
                self._dif -= 1
            if prov:
                self._provisorio -= 1
            if t == tag:
                break

    def handle_data(self, data: str) -> None:
        if self._ocultar:
            return
        if self._svg and data.strip():
            self.svg_com_texto.append(data.strip())
        if self.versao is not None:
            self.textos[self.versao].append(data)
            (self.diferencas if self._dif else self.sem_diferenca)[self.versao].append(data)
        if self._c1:
            self.camada1[-1] += data
        if self._botao is not None:
            self._botao.append(data)


def _norm(partes: list[str]) -> str:
    return re.sub(r"[ \t\r\n]+", " ", "".join(partes)).strip()


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


def texto_por_versao(fonte: str) -> dict[str, str]:
    """Texto visivel normalizado de cada versao (espacos colapsados; o U+00A0 fica)."""
    return {k: _norm(v) for k, v in analisar(fonte).textos.items()}


def diferenca_entre_versoes(fonte: str) -> dict[str, Any]:
    """A base e a versao com rota bloqueada, SEM o elemento de diferenca, tem de ser iguais;
    e so a versao com rota bloqueada pode ter elemento de diferenca."""
    p = analisar(fonte)
    return {"base_sem": _norm(p.sem_diferenca.get("base", [])),
            "rota_sem": _norm(p.sem_diferenca.get("com_rota_bloqueada", [])),
            "dif_base": _norm(p.diferencas.get("base", [])),
            "dif_rota": _norm(p.diferencas.get("com_rota_bloqueada", []))}


def tickers_do_catalogo() -> set[str]:
    """Os tickers que o catalogo do motor nomeia (l-B: nenhum pode aparecer no estimulo)."""
    sys.path.insert(0, os.path.join(RAIZ, "alocacao"))
    from alocacao import catalogo
    from motor import carregar
    return {t for r in catalogo(carregar()) for t in TICKER.findall(r.nome)}


def tickers_no_texto(texto: str, tickers: set[str]) -> list[str]:
    return sorted(t for t in tickers if re.search(rf"\b{re.escape(t)}\b", texto))


def cores_fora_do_yaml(fonte: str, cores: dict[str, str]) -> list[str]:
    permitidas = {c.upper() for c in cores.values()}
    achadas = [m.group(0).upper() for m in HEXCOR.finditer(fonte)]
    return sorted({c for c in achadas if c not in permitidas}) + \
        sorted({m.group(0) for m in FUNCAO_COR.finditer(fonte)})


def remotos(fonte: str, pasta: str = PASTA, tipografia: str = TIPOGRAFIA) -> list[str]:
    """Todo recurso remoto, e todo url() que nao seja fonte embutida com licenca ao lado."""
    ruins = [m.group(0) for m in REMOTO.finditer(fonte)]
    for m in URL.finditer(fonte):
        alvo = os.path.normpath(os.path.join(pasta, m.group(1)))
        dentro = alvo.startswith(os.path.normpath(tipografia) + os.sep)
        licenca = os.path.join(os.path.dirname(alvo), "OFL.txt")
        if not (dentro and os.path.isfile(alvo) and os.path.isfile(licenca)):
            ruins.append(f"url({m.group(1)})")
    return ruins


def fontes_declaradas(fonte: str) -> set[str]:
    return {m.group(1) for bloco in FONT_FACE.findall(fonte)
            for m in [re.search(r"font-family:\s*['\"]([^'\"]+)['\"]", bloco)] if m}


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
    p = analisar(fonte)
    out = [m.group(0) for m in IMAGEM.finditer(fonte)]
    out += [m.group(0) for m in GRADIENTE.finditer(fonte)]
    out += [f"emoji U+{ord(m.group(0)):04X}" for m in EMOJI.finditer(fonte)]
    out += ["botao sem texto" for b in p.botoes if not b]
    out += ["svg fora de data-provisorio"] * p.svg_fora_de_provisorio
    out += [f"svg com texto ou referencia: {t}" for t in p.svg_com_texto]
    out += [f"data-provisorio sem pendencia: {x!r}" for x in p.provisorios
            if not re.fullmatch(r"P-\d{3}", x)]
    return out


def tokens() -> dict[str, Any]:
    with io.open(TOKENS, encoding="utf-8") as f:
        return yaml.safe_load(f)


def conteudo() -> dict[str, Any]:
    with io.open(CONTEUDO, encoding="utf-8") as f:
        return yaml.safe_load(f)


def textos_obrigatorios(c: dict[str, Any], rotulos: dict[str, str]) -> dict[str, list[str]]:
    """O que o conteudo.yaml manda aparecer em cada versao (P1: o numero e o do motor)."""
    b = c["base"]
    comuns = [b["frase_decisao"], b["porque"], b["valor_fmt"], b["data_referencia"],
              b["custo_fmt"], b["custo_motivo"], rotulos["parcial"]]
    return {"base": comuns, "com_rota_bloqueada": comuns + [c["com_rota_bloqueada"]["linha"]]}


def matiz(hexcor: str) -> float:
    import colorsys
    r, g, b = (int(hexcor[i:i + 2], 16) / 255 for i in (1, 3, 5))
    return colorsys.rgb_to_hls(r, g, b)[0] * 360


def distancia_de_matiz(a: float, b: float) -> float:
    d = abs(a - b) % 360
    return min(d, 360 - d)
