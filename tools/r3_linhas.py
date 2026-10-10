# -*- coding: utf-8 -*-
"""As linhas do classificacao.csv da R3 a partir da leitura a olho e da captura (P-170).

POR QUE EXISTE. A classificacao de uma marca junta duas coisas: o que o navegador mediu na
captura (data/r3/capturas/<cat>-<ordem>/medidas.json, fora do git) e o que o olho decidiu (qual
e o botao principal, a classe da fonte, os blocos contados), gravado em
docs/marca/rodada3/leituras.yaml. Este script cruza as duas, tira as medidas do livro e chama o
classificador congelado (tools/codigos_visuais.classificar): nenhum limiar mora aqui.

O QUE ELE NAO FAZ (P5). Nao decide o botao nem a familia: le o que a leitura escreveu. Sem a
pasta da captura, recusa a linha (a captura e a procedencia).

    python tools/r3_linhas.py                 # regrava docs/marca/rodada3/classificacao.csv
    python tools/r3_linhas.py --acrescentar   # so as entradas que ainda nao estao no CSV
    python tools/r3_linhas.py --acrescentar --refazer bancos:16   # e refaz estas, de leituras.yaml

`--acrescentar` (10/10/2026). Regravar o CSV inteiro exige a captura de CADA linha antiga, e as
capturas (de terceiros, fora do git) moram so na maquina que as fez: a sessao na nuvem de 10/10
nao tem as 51 de 04/10. Acrescentar mantem as linhas gravadas como estao e junta as entradas de
`leituras.yaml` cuja chave (categoria sorteada, ordem) o CSV ainda nao tem. Consequencia
declarada: mudar a leitura de uma entrada JA gravada nao a atualiza por aqui; isso e `--tudo`
(o padrao), na maquina que tem a captura. A data de uma entrada pode vir na propria entrada
(`data:`); a do arquivo vale para as que nao a trazem.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from collections import Counter
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


def cor_do_texto_por_pixels(px: list[tuple[int, int, int]]) -> str:
    """Botao VAZADO sem borda numa captura de app (so a imagem existe): a cor que o livro manda
    ler e a do texto ('so a borda ou o texto tiverem cor'). E a moda dos pixels que NAO sao o
    fundo da caixa (moda da caixa), tirando os de distancia < 60 (soma dos canais) do fundo,
    que sao o suavizado das bordas das letras. Caixa toda de fundo: devolve o fundo."""
    fundo = Counter(px).most_common(1)[0][0]
    outros = [p for p in px if sum(abs(a - b) for a, b in zip(p, fundo)) >= 60]
    return C.rgb_hex(Counter(outros).most_common(1)[0][0] if outros else fundo)


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


def chaves_novas(existentes: list[dict[str, str]],
                 leituras: dict[str, dict[int, Any]]) -> list[tuple[str, int]]:
    """As (categoria sorteada, ordem) de `leituras` que o CSV ainda nao tem, na ordem do arquivo."""
    tem = {(r["categoria_sorteada"], int(r["ordem_no_sorteio"])) for r in existentes}
    return [(cat, ordem) for cat, por_ordem in leituras.items() for ordem in sorted(por_ordem)
            if (cat, ordem) not in tem]


def sem_chaves(linhas: list[dict[str, str]], quais: list[str]) -> list[dict[str, str]]:
    """As linhas sem as de `quais` (cada uma 'categoria:ordem'): o `--refazer` de uma entrada ja
    gravada que mudou de leitura. Chave que nao existe e erro, para um erro de digitacao nao
    parecer que refez."""
    chaves = set()
    for q in quais:
        cat, _, ordem = q.rpartition(":")
        chaves.add((cat, int(ordem)))
    tem = {(r["categoria_sorteada"], int(r["ordem_no_sorteio"])) for r in linhas}
    if chaves - tem:
        raise ValueError(f"--refazer: sem linha gravada para {sorted(chaves - tem)}")
    return [r for r in linhas
            if (r["categoria_sorteada"], int(r["ordem_no_sorteio"])) not in chaves]


def linha(cat: str, ordem: int, leitura: dict[str, Any], sorteio: dict[str, str],
          livro: dict[str, Any]) -> dict[str, str]:
    base = {c: "" for c in R.COLUNAS}
    base.update(marca=leitura["marca"], categoria=leitura.get("categoria", cat),
                categoria_sorteada=cat, ordem_no_sorteio=str(ordem), cnpj=sorteio["cnpj"],
                situacao=leitura["situacao"], motivo=leitura.get("motivo", ""),
                escada=leitura.get("escada", ""), data=leitura["data"])
    pasta = os.path.join(CAPTURAS, f"{cat}-{ordem:02d}")
    mpath = os.path.join(pasta, "medidas.json")
    if leitura["situacao"] == "classificada" and not os.path.exists(mpath):
        # a captura e a procedencia (docstring): classificada sem ela nao tem de onde vir
        raise ValueError(f"{cat}-{ordem:02d}: classificada sem captura em {pasta}")
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
        destaque = (cor_do_texto_por_pixels(px) if botao == "vazado"
                    else preenchimento_por_pixels(px, leitura.get("cor_do_texto")))
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


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=(__doc__ or "").split("\n")[0])
    ap.add_argument("--acrescentar", action="store_true")
    ap.add_argument("--refazer", nargs="+", metavar="CATEGORIA:ORDEM",
                    help="com --acrescentar: descarta estas linhas e as refaz da leitura")
    a = ap.parse_args(argv)
    if a.refazer and not a.acrescentar:
        ap.error("--refazer so vale com --acrescentar (sem ele o CSV inteiro ja e refeito)")
    livro = V.ler_livro()
    with open(LEITURAS, encoding="utf-8") as f:
        leituras = yaml.safe_load(f)
    linhas = R.ler() if a.acrescentar else []
    if a.refazer:
        linhas = sem_chaves(linhas, a.refazer)
    quais = (chaves_novas(linhas, leituras["categorias"]) if a.acrescentar else
             [(c, o) for c, po in leituras["categorias"].items() for o in sorted(po)])
    sorteios: dict[str, dict[int, dict[str, str]]] = {}
    for cat, ordem in quais:
        if cat not in sorteios:
            with open(os.path.join(R.PASTA, f"sorteio-{cat}.csv"), encoding="utf-8") as f:
                sorteios[cat] = {int(r["ordem"]): r for r in csv.DictReader(f)}
        entrada = leituras["categorias"][cat][ordem]
        linhas.append(linha(cat, ordem, {**entrada, "data": entrada.get("data", leituras["data"])},
                            sorteios[cat][ordem], livro))
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
