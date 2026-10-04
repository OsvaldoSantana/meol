# -*- coding: utf-8 -*-
"""As linhas do classificacao.csv da R3 a partir da leitura a olho e da captura (P-170).

POR QUE EXISTE. A classificacao de uma marca junta duas coisas: o que o navegador mediu na
captura (data/r3/capturas/<cat>-<ordem>/medidas.json, fora do git) e o que o olho decidiu (qual
e o botao principal, a classe da fonte, os blocos contados), gravado em
docs/marca/rodada3/leituras.yaml. Este script cruza as duas, tira as medidas do livro e chama o
classificador congelado (tools/codigos_visuais.classificar): nenhum limiar mora aqui.

O QUE ELE NAO FAZ (P5). Nao decide o botao nem a familia: le o que a leitura escreveu. Sem a
pasta da captura, recusa a linha (a captura e a procedencia).

    python tools/r3_linhas.py            # regrava docs/marca/rodada3/classificacao.csv
"""
from __future__ import annotations

import csv
import json
import os
import sys
from typing import Any

import yaml

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import codigos_visuais as V  # noqa: E402
import r3_capturar as C  # noqa: E402
import r3_dominante as R  # noqa: E402

RAIZ = os.path.dirname(AQUI)
LEITURAS = os.path.join(RAIZ, "docs", "marca", "rodada3", "leituras.yaml")
CAPTURAS = os.path.join(RAIZ, "data", "r3", "capturas")


def achar_botao(botoes: list[dict[str, Any]], texto: str) -> dict[str, Any]:
    """O botao da leitura, pelo comeco do texto (o navegador corta em 60 caracteres)."""
    alvo = texto.strip().lower()
    achados = [b for b in botoes if b["texto"].strip().lower().startswith(alvo)]
    if not achados:
        raise ValueError(f"botao {texto!r} nao esta na captura")
    return achados[0]


def destaque_do_botao(b: dict[str, Any], botao: str,
                      pixels_da_caixa: list[tuple[int, int, int]] | None = None) -> str:
    """Cheio: o fundo computado; sem fundo computado (gradiente ou imagem), a moda dos pixels da
    caixa. Vazado: a borda; sem borda, a cor do texto (livro: 'so a borda ou o texto')."""
    if botao == "cheio":
        fundo = C.css_para_hex(b["fundo"])
        if fundo:
            return fundo
        if not pixels_da_caixa:
            raise ValueError("botao cheio sem fundo computado e sem pixels para medir")
        return preenchimento_por_pixels(pixels_da_caixa, C.css_para_hex(b["cor"]))
    tem_borda = b["borda_estilo"] != "none" and b["borda_px"] not in ("0px", "0")
    borda = C.css_para_hex(b["borda_cor"]) if tem_borda else None
    return borda or (C.css_para_hex(b["cor"]) or "#000000")


def preenchimento_por_pixels(px: list[tuple[int, int, int]], cor_do_texto: str | None) -> str:
    """Gradiente ou imagem de fundo: a moda e o texto (cada pixel do degrade e unico). Tira os
    pixels perto da cor do texto (distancia < 60 por canal somado) e da a MEDIANA por canal."""
    if cor_do_texto:
        t = tuple(int(cor_do_texto[i:i + 2], 16) for i in (1, 3, 5))
        px = [p for p in px if sum(abs(a - b) for a, b in zip(p, t)) >= 60] or px
    canais = [sorted(p[i] for p in px) for i in range(3)]
    return C.rgb_hex(c[len(c) // 2] for c in canais)


def _pixels_caixa(png: str, caixa: list[int]) -> list[tuple[int, int, int]]:
    from PIL import Image
    x, y, w, h = caixa
    with Image.open(png) as im:
        reg = im.convert("RGB").crop((x, y, x + w, y + h))
        dados: Any = reg.get_flattened_data()
        return [(int(p[0]), int(p[1]), int(p[2])) for p in dados]


def linha(cat: str, ordem: int, leitura: dict[str, Any], sorteio: dict[str, str],
          livro: dict[str, Any]) -> dict[str, str]:
    base = {c: "" for c in R.COLUNAS}
    base.update(marca=leitura["marca"], categoria=leitura.get("categoria", cat),
                categoria_sorteada=cat, ordem_no_sorteio=str(ordem), cnpj=sorteio["cnpj"],
                situacao=leitura["situacao"], motivo=leitura.get("motivo", ""),
                escada=leitura.get("escada", ""), data=leitura["data"])
    pasta = os.path.join(CAPTURAS, f"{cat}-{ordem:02d}")
    mpath = os.path.join(pasta, "medidas.json")
    if os.path.exists(mpath):
        with open(mpath, encoding="utf-8") as f:
            m = json.load(f)
        base["url"] = m["390"].get("url_final") or m["url_pedida"]
        base["sha256_captura"] = m["390"]["sha256"]
    if leitura["situacao"] != "classificada":
        base["url"] = base["url"] or leitura.get("url", "")
        return base
    a = m["390"]
    png = os.path.join(pasta, "390.png")
    if leitura["unidade"] == "app":
        # ae-a: a captura da App Store, recortada na tela do aparelho (r3_capturar recortar)
        with open(os.path.join(pasta, "app_390.json"), encoding="utf-8") as f:
            rec = json.load(f)
        with open(os.path.join(pasta, "app.json"), encoding="utf-8") as f:
            loja = json.load(f)
        a = {"moda": rec["moda"], "botoes": []}
        png = os.path.join(pasta, "app_390.png")
        base["url"] = loja["trackViewUrl"].split("?")[0]
        base["sha256_captura"] = rec["sha256"]
    botao = leitura["botao"]
    if leitura.get("botao_texto"):
        b = achar_botao(a["botoes"], leitura["botao_texto"])
        caixa = _pixels_caixa(png, b["caixa"])
        destaque = destaque_do_botao(b, botao, caixa)
        raio = C.raio_px(b["raio"], b["caixa"][3])
    elif leitura.get("botao_caixa"):
        # o botao que o navegador nao listou (div com clique, texto em imagem): a caixa e o raio
        # foram medidos no olho sobre a 390.png e estao na leitura, com a nota
        px = _pixels_caixa(png, leitura["botao_caixa"])
        destaque = preenchimento_por_pixels(px, leitura.get("cor_do_texto"))
        raio = float(leitura["raio_px"])
    else:  # sem botao: livro e procedimento da R3, sec. 1.1
        crom = C.moda_cromatica(C._pixels(png), livro)
        destaque = crom[0] if crom else a["moda"]
        raio = float(leitura.get("raio_px", 0))
    medidas = {"fundo_hex": a["moda"], "destaque_hex": destaque,
               "familia_generica": leitura["familia_generica"], "raio_px": raio,
               "densidade_blocos": leitura["densidade_blocos"], "botao": botao}
    base.update(V.classificar(medidas, livro))
    base.update(unidade=leitura["unidade"], fundo_hex=a["moda"], destaque_hex=destaque,
                familia_generica=leitura["familia_generica"], raio_px=f"{raio:g}",
                densidade_blocos=str(leitura["densidade_blocos"]),
                arquivo_wayback=leitura.get("arquivo_wayback", R.PENDENTE))
    return base


def main() -> int:
    livro = V.ler_livro()
    with open(LEITURAS, encoding="utf-8") as f:
        leituras = yaml.safe_load(f)
    linhas = []
    for cat, por_ordem in leituras["categorias"].items():
        with open(os.path.join(R.PASTA, f"sorteio-{cat}.csv"), encoding="utf-8") as f:
            sorteio = {int(r["ordem"]): r for r in csv.DictReader(f)}
        for ordem in sorted(por_ordem):
            linhas.append(linha(cat, ordem, {**por_ordem[ordem], "data": leituras["data"]},
                                sorteio[ordem], livro))
    probs = R.validar(linhas, livro)
    for p in probs:
        print(p)
    if probs:
        return 1
    with open(R.CSV, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=R.COLUNAS, lineterminator="\n")
        w.writeheader()
        w.writerows(linhas)
    print(f"gravadas {len(linhas)} linhas em docs/marca/rodada3/classificacao.csv")
    return 0


if __name__ == "__main__":
    sys.exit(main())
