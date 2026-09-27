# -*- coding: utf-8 -*-
"""Os numeros dos estimulos do teste de marca saem do motor, nao da mao (P-163, P1).

POR QUE ELE EXISTE. As direcoes visuais do teste de marca mostram a mesma tela T1 com a
mesma decisao. Um numero escrito a mao num estimulo seria o F-02 na vitrine: parece do
motor e nao e. Este script roda `alocar()` e `motor_aporte()` sobre o cenario SINTETICO de
`docs/marca/direcoes/cenario.yaml` e grava `docs/marca/direcoes/conteudo.yaml`, com a
origem de cada numero ao lado.

O QUE ELE NAO FAZ (P5). Nao le `estado.yaml` (D-01). Nao inventa faixa: o motor nao emite
`faixa.min/max` (F0-contrato, `NAO_EXISTE`); a faixa do estado PARCIAL e o custo da compra
calculado por `custo_entrada_pct()` com os dois valores que o proprio `custos.yaml` declara
para a tarifa da B3 (`valor` e `divergencia.valor_alternativo`). Nao informa preco: a rota
negocia em lote e o motor usa 1,0 quando o preco falta, entao a QUANTIDADE sai sem sentido e
o estimulo nao a mostra; o VALOR em reais e o do motor.

    python tools/conteudo_estimulo.py           # grava o conteudo.yaml
    python tools/conteudo_estimulo.py --conferir  # sai 1 se o gravado divergir do motor
"""
from __future__ import annotations

import argparse
import copy
import io
import os
import sys
from typing import Any

import yaml

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "alocacao"))

from alocacao import (Estado, alocar, carregar_politica, catalogo,  # noqa: E402
                      custo_entrada_pct, motor_aporte, reserva_alvo)
from motor import carregar as carregar_custos  # noqa: E402

PASTA = os.path.join(RAIZ, "docs", "marca", "direcoes")
CENARIO = os.path.join(PASTA, "cenario.yaml")
CONTEUDO = os.path.join(PASTA, "conteudo.yaml")
COMANDO = "python tools/conteudo_estimulo.py"
MESES = ("janeiro", "fevereiro", "mar\u00e7o", "abril", "maio", "junho", "julho", "agosto",
         "setembro", "outubro", "novembro", "dezembro")
NBSP = "\u00a0"
# Campos que mudam com o dia ou com a versao da politica sem mudar o que o estimulo
# mostra; o --conferir os ignora. Qualquer outro campo divergente reprova.
VOLATEIS = ("gerado_em", "politica_versao", "politica_hash", "custos_hash")


def brl(valor: float) -> str:
    """R$, espaco nao separavel, ponto de milhar, virgula decimal (RI-02)."""
    s = f"{valor:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")
    return f"R${NBSP}{s}"


def _cadastro() -> dict:
    sys.path.insert(0, os.path.join(RAIZ, "alocacao"))
    from test_usuario_novo import CADASTRO_MINIMO  # N-01: uma lista so
    return dict(CADASTRO_MINIMO)


def gerar(cenario_path: str = CENARIO) -> dict[str, Any]:
    with io.open(cenario_path, encoding="utf-8") as f:
        cen = yaml.safe_load(f)
    C, P = carregar_custos(), carregar_politica()
    cad = _cadastro()
    reserva = reserva_alvo(Estado(**{**cad, "reserva_atual": 0.0}), P)
    posicoes = {k: float(v) for k, v in cen["posicoes"].items()}
    estado = Estado(**{**cad, "reserva_atual": reserva, "posicoes": posicoes})
    rotas = {r.id: r for r in catalogo(C)}
    r = alocar(estado, C, P, teses={}, carregos={})
    if "diretiva" in r:
        raise SystemExit("o cenario caiu num portao de aporte (reserva/divida); nao e o "
                         "publico de quem ja aporta")
    m = motor_aporte(estado, r["alvo"], C, P, rotas_por_id=rotas)
    if m.get("status") not in (None, "OK") or len(m.get("ordens", [])) != 1:
        raise SystemExit(f"o estimulo espera UMA ordem; o motor devolveu {m.get('status')} "
                         f"com {len(m.get('ordens', []))} ordem(ns)")
    ordem = m["ordens"][0]
    rota = rotas[ordem["rota"]]
    ticker = rota.nome.split(" ")[0]
    proc = r["procedencia"]
    ano, mes, _ = (int(x) for x in proc["gerado_em"].split("-"))

    # Faixa do PARCIAL: o custo da compra com os dois valores declarados da tarifa B3.
    b3 = C["b3"]["vista_total_pct"]
    C_alt = copy.deepcopy(C)
    C_alt["b3"]["vista_total_pct"]["valor"] = b3["divergencia"]["valor_alternativo"]
    custo_decl = custo_entrada_pct(rota, ordem["valor"], b3["valor"]) * ordem["valor"]
    custo_alt = custo_entrada_pct(
        rota, ordem["valor"], C_alt["b3"]["vista_total_pct"]["valor"]) * ordem["valor"]
    lo, hi = sorted((round(custo_decl, 2), round(custo_alt, 2)))

    frase = f"Este m\u00eas, aporte {brl(ordem['valor'])} em {ticker}."
    porque = "\u00c9 a parte da sua carteira mais abaixo do peso-alvo."
    return {
        "versao": 1,
        "meta": {
            "comando": COMANDO,
            "cenario": "docs/marca/direcoes/cenario.yaml",
            "gerado_em": proc["gerado_em"],
            "politica_versao": proc["politica_versao"],
            "politica_hash": proc["politica_hash"],
            "custos_hash": proc["custos_hash"],
            "sintetico": True,
        },
        "cenario_resolvido": {
            "reserva_atual": reserva,
            "reserva_origem": "alocacao.reserva_alvo(cadastro, politica)",
            "patrimonio_investido": estado.patrimonio_investido,
            "aporte_mensal": estado.aporte_mensal,
        },
        "normal": {
            "frase_decisao": frase,
            "valor": ordem["valor"],
            "valor_fmt": brl(ordem["valor"]),
            "valor_origem": "motor_aporte(...)['ordens'][0]['valor']",
            "destino": ticker,
            "destino_origem": "catalogo(C)[ordens[0]['rota']].nome, primeira palavra",
            "rota_id": ordem["rota"],
            "deficit": ordem["deficit"],
            "deficit_origem": "motor_aporte(...)['ordens'][0]['deficit']: o maior do cenario",
            "data_referencia": f"{MESES[mes - 1]} de {ano}",
            "data_origem": ("procedencia['gerado_em'] (dia da rodada). O motor nao emite o "
                            "mes de referencia: decisao.data_referencia e NAO_EXISTE na F0"),
            "porque": porque,
            "porque_origem": ("texto; o fato e do motor: a rota escolhida e a de maior "
                              "deficit (motor_aporte ordena por deficit, k_max da politica)"),
            "custo_compra_fmt": brl(round(custo_decl, 2)),
            "custo_compra_origem": ("custo_entrada_pct(rota, valor, b3.vista_total_pct.valor) "
                                    "x valor. CONTRAFACTUAL: a tarifa e PARCIAL no custos.yaml; "
                                    "o estado normal a mostra como se fosse COMPLETA, de "
                                    "proposito, para a H3"),
            "limitacao_quantidade": ("rota em lote sem preco no cenario: motor_aporte usa 1,0 "
                                     "(precos.get). A quantidade nao se mostra; o valor e o "
                                     "do motor"),
        },
        "parcial": {
            "status": "PARCIAL",
            "custo_compra_min": lo,
            "custo_compra_max": hi,
            "faixa_fmt": f"entre {brl(lo)} e {brl(hi)}",
            "faixa_origem": ("custo_entrada_pct() com b3.vista_total_pct.valor e com "
                             "b3.vista_total_pct.divergencia.valor_alternativo (custos.yaml)"),
            "motivo": "A tarifa da B3 tem duas fontes que ainda n\u00e3o batem.",
        },
    }


def _sem_volateis(d: dict) -> dict:
    d = copy.deepcopy(d)
    for k in VOLATEIS:
        d.get("meta", {}).pop(k, None)
    return d


def gravar(conteudo: dict, path: str = CONTEUDO) -> None:
    cab = ("# GERADO por `python tools/conteudo_estimulo.py` -- nao editar a mao (P1).\n"
           "# Cenario sintetico; nenhum numero do Osvaldo (D-01). Ver cenario.yaml.\n")
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(cab)
        yaml.safe_dump(conteudo, f, allow_unicode=False, sort_keys=False, width=100)


def conferir(path: str = CONTEUDO) -> list[str]:
    """Os campos que divergem entre o gravado e o que o motor da hoje."""
    with io.open(path, encoding="utf-8") as f:
        gravado = yaml.safe_load(f)
    agora = gerar()
    a, b = _sem_volateis(gravado), _sem_volateis(agora)
    out = []
    for secao in sorted(set(a) | set(b)):
        va, vb = a.get(secao), b.get(secao)
        if isinstance(va, dict) and isinstance(vb, dict):
            out += [f"{secao}.{k}" for k in sorted(set(va) | set(vb)) if va.get(k) != vb.get(k)]
        elif va != vb:
            out.append(secao)
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--conferir", action="store_true")
    a = ap.parse_args(argv)
    if a.conferir:
        dif = conferir()
        for d in dif:
            print(f"DIVERGE: {d}")
        return 1 if dif else 0
    c = gerar()
    gravar(c)
    print(c["normal"]["frase_decisao"], "|", c["parcial"]["faixa_fmt"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
