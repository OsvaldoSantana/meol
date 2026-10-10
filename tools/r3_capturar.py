# -*- coding: utf-8 -*-
"""A captura de uma marca da R3 e as medidas cruas do livro de codigos (P-170).

POR QUE EXISTE. O livro de codigos (docs/marca/teste-de-marca/codigos-visuais.yaml) diz O QUE
medir em cada marca: a cor de maior area (moda dos pixels), a cor do botao principal, a fonte do
texto de maior corpo, o raio do botao, os blocos sem rolar. Medir a olho numa imagem solta nao
deixa conferir depois. Este script fixa a captura (390 x 844, DPR 1, sem clicar em nada) e
grava, ao lado do PNG, o que o navegador mede: a moda dos pixels, os botoes visiveis com cor,
borda e raio computados, e os textos de maior corpo com a familia da fonte. Quem classifica le
isso, olha a imagem, escolhe o botao principal e escreve a linha do CSV. A regra de
classificacao continua so em tools/codigos_visuais.py (congelado no pre-registro): aqui nao ha
limiar nenhum.

O QUE ELE NAO FAZ (P5). Nao escolhe o botao principal nem a familia generica de uma fonte com
nome proprio (isso e do olho, limitacao 5 da R3). Nao clica em aviso de cookies nem aceita nada.
Nao arquiva no Wayback (a sessao na nuvem nao alcanca web.archive.org: degraus na R3, sec. 1).
Nao grava nada no git: as capturas sao de terceiros e ficam em data/r3/capturas/ (ignorado).

    python tools/r3_capturar.py site <url> <pasta>     # 390.png, 1280.png, medidas.json
    python tools/r3_capturar.py app <trackId> <pasta>  # as capturas da App Store do Brasil
    python tools/r3_capturar.py recortar <png> <x0> <y0> <x1> <y1> <pasta>  # a tela, em 390 px

O NAVEGADOR (10/10/2026). A captura usa o Chromium que o Playwright instalado espera. Quando a
maquina tem outro (a nuvem traz o build 1194, o das 51 primeiras visitas da R3, e o Playwright
1.63.0 espera o 1243), `R3_CHROMIUM=<caminho do executavel>` o aponta: o instrumento das visitas
nao muda no meio da rodada. O `medidas.json` guarda `navegador` (a versao do Chromium), para que
a versao de cada captura se confira depois.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.request
from collections import Counter
from collections.abc import Callable, Iterable
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import codigos_visuais as V  # noqa: E402  (o livro e o classificador congelados)

LARGURA, ALTURA = 390, 844          # a unidade do livro: 390 px de largura, sem rolar
LARGURA_DESKTOP, ALTURA_DESKTOP = 1280, 800
ESPERA_MS = 2500                    # depois do load e da rede parada: animacao de entrada

# O que o navegador devolve de cada elemento visivel na primeira tela (so le, nao clica).
JS_MEDIDAS_ARQUIVO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "r3_medidas.js")


# ------------------------------------------------------------------ funcoes puras (testadas) ---

def rgb_hex(rgb: Iterable[int]) -> str:
    r, g, b = (int(c) for c in rgb)
    return f"#{r:02x}{g:02x}{b:02x}"


def css_para_hex(css: str) -> str | None:
    """`rgb(1, 2, 3)` ou `rgba(1, 2, 3, a)` -> `#010203`; transparente (a == 0) -> None."""
    m = re.match(r"rgba?\(\s*(\d+)[,\s]+(\d+)[,\s]+(\d+)(?:[,\s/]+([\d.]+%?))?\s*\)", css.strip())
    if not m:
        return None
    alfa = m.group(4)
    if alfa is not None:
        a = float(alfa[:-1]) / 100 if alfa.endswith("%") else float(alfa)
        if a == 0:
            return None
    return rgb_hex(int(m.group(i)) for i in (1, 2, 3))


def raio_px(css: str, altura_px: float) -> float:
    """O raio computado em px. Porcentagem vira px pela altura do botao (50% de um botao de 44 px
    sao 22 px). Valores enormes (9999px, a pilula) ficam como estao: o livro so pergunta se
    passam de 8."""
    css = css.strip().split(" ")[0]
    if css.endswith("%"):
        return float(css[:-1]) / 100 * altura_px
    if css.endswith("px"):
        return float(css[:-2])
    return float(css or 0)


def moda(pixels: Iterable[tuple[int, int, int]]) -> tuple[str, float]:
    """A cor de maior area (moda exata dos pixels, como o livro manda) e a fracao dela."""
    c = Counter(pixels)
    total = sum(c.values())
    if not total:
        raise ValueError("imagem vazia")
    cor, n = c.most_common(1)[0]
    return rgb_hex(cor), n / total


def moda_cromatica(pixels: Iterable[tuple[int, int, int]],
                   livro: dict[str, Any] | None = None) -> tuple[str, float] | None:
    """A cor cromatica de maior area, o matiz quando nao ha botao. "Cromatica" e o que o livro
    diz (codigos_visuais.faixa_de_matiz diferente de neutro): a regra nao se reescreve aqui."""
    livro = V.ler_livro() if livro is None else livro
    c = Counter(pixels)
    total = sum(c.values())
    cromaticas = {cor: n for cor, n in c.items()
                  if V.faixa_de_matiz(rgb_hex(cor), livro) != "neutro"}
    if not cromaticas:
        return None
    cor = max(cromaticas, key=lambda k: cromaticas[k])
    return rgb_hex(cor), cromaticas[cor] / total


def em_alta(url: str) -> str:
    """A lookup da App Store devolve a miniatura (392x696). O servidor de imagens da Apple serve a
    mesma captura em outra largura trocando o ultimo segmento: pede 1242 de largura."""
    return re.sub(r"/\d+x\d+bb\.(png|jpg)$", r"/1242x0w.\1", url)


def chromium_do_ambiente(ambiente: dict[str, str] | None = None) -> str | None:
    """`R3_CHROMIUM` aponta o executavel do Chromium; sem ela (None), o do Playwright."""
    exe = (os.environ if ambiente is None else ambiente).get("R3_CHROMIUM", "").strip()
    return exe or None


def com_tentativas(fazer: Callable[[], Any], tentativas: int = 4,
                   dormir: Callable[[float], None] = time.sleep) -> Any:
    """Repete `fazer` ate `tentativas` vezes com espera crescente (2, 4, 8 s) quando a rede
    derruba a conexao. 10/10/2026: o proxy da nuvem reinicia conexoes ao acaso (`Connection reset
    by peer`) e a mesma consulta funciona na tentativa seguinte; sem a repeticao, a marca virava
    'sem app' por um erro de transporte, que e o que a 5-B.16 manda nao chamar de limitacao."""
    for n in range(tentativas):
        try:
            return fazer()
        except OSError:
            if n == tentativas - 1:
                raise
            dormir(2 ** (n + 1))
    raise AssertionError("inalcancavel")


def sha256_arquivo(path: str) -> str:
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


# ------------------------------------------------------------- o que toca rede ou imagem ---

def _pixels(png: str) -> list[tuple[int, int, int]]:
    from PIL import Image  # grupo `r3` do pyproject: so quem captura precisa
    with Image.open(png) as im:
        dados: Any = im.convert("RGB").get_flattened_data()  # Pillow tipa pixel como uniao
        return [(int(p[0]), int(p[1]), int(p[2])) for p in dados]


def _resumo_imagem(png: str) -> dict[str, Any]:
    px = _pixels(png)
    fundo, fr = moda(px)
    crom = moda_cromatica(px)
    return {"sha256": sha256_arquivo(png), "moda": fundo, "moda_fracao": round(fr, 4),
            "moda_cromatica": crom[0] if crom else None,
            "moda_cromatica_fracao": round(crom[1], 4) if crom else None}


def capturar_site(url: str, pasta: str) -> dict[str, Any]:
    from playwright.sync_api import sync_playwright
    os.makedirs(pasta, exist_ok=True)
    saida: dict[str, Any] = {"url_pedida": url}
    with sync_playwright() as p:
        nav = p.chromium.launch(executable_path=chromium_do_ambiente())
        saida["navegador"] = nav.version
        for nome, w, h, movel in (("390", LARGURA, ALTURA, True),
                                  ("1280", LARGURA_DESKTOP, ALTURA_DESKTOP, False)):
            ctx = nav.new_context(viewport={"width": w, "height": h}, device_scale_factor=1,
                                  is_mobile=movel, has_touch=movel, locale="pt-BR")
            pg = ctx.new_page()
            resp = pg.goto(url, wait_until="load", timeout=90000)
            try:
                pg.wait_for_load_state("networkidle", timeout=12000)
            except Exception:  # rede que nunca para (chat, analytics): segue com o que tem
                pass
            pg.wait_for_timeout(ESPERA_MS)
            png = os.path.join(pasta, f"{nome}.png")
            pg.screenshot(path=png)
            info = {"status_http": resp.status if resp else None, **_resumo_imagem(png)}
            if nome == "390":
                with open(JS_MEDIDAS_ARQUIVO, encoding="utf-8") as f:
                    info.update(pg.evaluate(f.read()))
            saida[nome] = info
            ctx.close()
        nav.close()
    with open(os.path.join(pasta, "medidas.json"), "w", encoding="utf-8") as f:
        json.dump(saida, f, ensure_ascii=False, indent=1)
    return saida


def baixar_app(track_id: str, pasta: str) -> dict[str, Any]:
    os.makedirs(pasta, exist_ok=True)
    url = f"https://itunes.apple.com/lookup?id={int(track_id)}&country=br"
    def _lookup() -> dict[str, Any]:
        with urllib.request.urlopen(url, timeout=30) as r:
            achado: dict[str, Any] = json.load(r)["results"][0]
            return achado
    d = com_tentativas(_lookup)
    saida = {"lookup": url, "trackName": d.get("trackName"), "artistName": d.get("artistName"),
             "sellerName": d.get("sellerName"), "trackViewUrl": d.get("trackViewUrl"),
             "capturas": []}
    for k, u in enumerate(d.get("screenshotUrls", []), start=1):
        u = em_alta(u)
        png = os.path.join(pasta, f"app_{k}.png")
        def _baixar(u: str = u, png: str = png) -> None:
            urllib.request.urlretrieve(u, png)
        com_tentativas(_baixar)
        saida["capturas"].append({"k": k, "url": u, "sha256": sha256_arquivo(png)})
    with open(os.path.join(pasta, "app.json"), "w", encoding="utf-8") as f:
        json.dump(saida, f, ensure_ascii=False, indent=1)
    return saida


def recortar(png: str, caixa: tuple[int, int, int, int], pasta: str) -> dict[str, Any]:
    """A area da tela do aparelho, sem moldura nem legenda, levada a 390 px de largura."""
    from PIL import Image
    with Image.open(png) as im:
        tela = im.convert("RGB").crop(caixa)
        alt = round(tela.height * LARGURA / tela.width)
        tela = tela.resize((LARGURA, alt), Image.Resampling.NEAREST)
        destino = os.path.join(pasta, "app_390.png")
        tela.save(destino)
    info = {"origem": png, "origem_sha256": sha256_arquivo(png), "caixa": list(caixa),
            "escala": LARGURA / (caixa[2] - caixa[0]), **_resumo_imagem(destino)}
    with open(os.path.join(pasta, "app_390.json"), "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=1)
    return info


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=(__doc__ or "").split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("site")
    s.add_argument("url")
    s.add_argument("pasta")
    a_ = sub.add_parser("app")
    a_.add_argument("track_id")
    a_.add_argument("pasta")
    r = sub.add_parser("recortar")
    r.add_argument("png")
    r.add_argument("caixa", nargs=4, type=int)
    r.add_argument("pasta")
    a = ap.parse_args(argv)
    if a.cmd == "site":
        out = capturar_site(a.url, a.pasta)
    elif a.cmd == "app":
        out = baixar_app(a.track_id, a.pasta)
    else:
        out = recortar(a.png, (a.caixa[0], a.caixa[1], a.caixa[2], a.caixa[3]), a.pasta)
    print(json.dumps(out, ensure_ascii=False, indent=1)[:6000])
    return 0


if __name__ == "__main__":
    sys.exit(main())
