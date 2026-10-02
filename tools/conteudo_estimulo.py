# -*- coding: utf-8 -*-
"""Os numeros dos estimulos do teste de marca saem do motor, nao da mao (P-163, P1).

POR QUE ELE EXISTE. As direcoes visuais do teste de marca mostram a mesma tela T1 com a
mesma decisao. Um numero escrito a mao num estimulo seria o F-02 na vitrine: parece do
motor e nao e. Este script roda `alocar()` e `motor_aporte()` sobre o cenario SINTETICO de
`docs/marca/direcoes/cenario.yaml` e grava `docs/marca/direcoes/conteudo.yaml`, com a
origem de cada numero ao lado.

O QUE ELE NAO FAZ (P5). Nao le `estado.yaml` (D-01). Nao inventa faixa: o motor nao emite
`faixa.min/max` (F0-contrato, `NAO_EXISTE`); a faixa do custo da compra e
`custo_entrada_pct()` com os dois valores que o proprio `custos.yaml` declara para a tarifa
da B3 (`valor` e `divergencia.valor_alternativo`), e o selo e o do insumo, PARCIAL, nas duas
versoes (S4, 27/09: sem estado contrafactual). Nao inventa rota bloqueada: a da versao da
H3 e a primeira que o motor elimina (`rota_bloqueada()`), e o script para se nao houver.
Nao escreve ticker: destino e rota bloqueada saem com o rotulo generico do cenario (l-B).
Nao informa preco: a rota negocia em lote e o motor usa 1,0 quando o preco falta, entao a
QUANTIDADE sai sem sentido e o estimulo nao a mostra; o VALOR em reais e o do motor.

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


# j-A: a ordem em que os portoes de UNIVERSO eliminam rota, e onde cada um deixa a lista.
# A ordem vem do politica.yaml (portoes.*.ordem); este mapa so diz em que chave da saida
# de alocar() o portao guarda o que eliminou. O G6 fica fora de proposito: ele tira a
# FUNCAO da rota, nao a rota (doutrina P3), entao nao produz "rota bloqueada".
SAIDA_DO_PORTAO = {"G5_status": "fora_status", "G3_atrito": "fora_atrito",
                   "G7_tese_registrada": "sem_tese", "G8_compromisso_de_carrego": "sem_carrego",
                   "G4_dominancia": "dominados"}
LIMITE_PALAVRAS = 15   # RI-01: frase de camada 1 com no maximo 15 palavras


def _motivo_do_motor(item: Any) -> tuple[str, str]:
    """(rota_id, motivo literal do motor) de um item de qualquer lista de eliminadas."""
    if isinstance(item, tuple):
        rota = item[0]
        extra = [x for x in item[1:] if isinstance(x, str)]
        return rota.id, "; ".join(extra) or str(item[1:])
    return item.id, "; ".join(getattr(item, "bloqueios", []) or [])


def rota_bloqueada(saida: dict, P: dict) -> dict[str, str]:
    """A primeira rota eliminada, na ordem declarada dos portoes de universo.

    Regra escrita ANTES de ver qual rota ela escolhe no cenario? Nao: foi escrita depois de
    listar as eliminadas (S4, 27/09). O que a torna aceitavel e ser mecanica e declarada:
    ordem do politica.yaml, e dentro do portao a ordem em que o motor lista."""
    u = saida["universo"]
    portoes = sorted((k for k, v in P["portoes"].items() if v.get("fase") == "universo"),
                     key=lambda k: P["portoes"][k]["ordem"])
    for g in portoes:
        chave = SAIDA_DO_PORTAO.get(g)
        if chave and u.get(chave):
            rota_id, motivo = _motivo_do_motor(u[chave][0])
            return {"rota_id": rota_id, "portao": g, "motivo_motor": motivo,
                    "origem": f"alocar(...)['universo']['{chave}'][0], o primeiro portao de "
                              "universo que elimina, na ordem de politica.yaml -> portoes.*.ordem"}
    raise SystemExit("o motor nao rejeitou nenhuma rota no cenario: sem rota bloqueada real, "
                     "a versao da H3 nao existe (j-A). Nada foi inventado.")


def _palavras(t: str) -> int:
    return len(t.split())


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
    rot = cen.get("rotulos", {}).get(ordem["rota"])
    if not rot:
        raise SystemExit(f"a rota {ordem['rota']} nao tem rotulo generico no cenario.yaml "
                         "(l-B): o estimulo nao mostra ticker")
    proc = r["procedencia"]
    ano, mes, _ = (int(x) for x in proc["gerado_em"].split("-"))

    # O custo, como esta no custos.yaml: a tarifa B3 e PARCIAL, entao o custo sai em faixa,
    # entre o valor declarado e o valor_alternativo da divergencia. Sem estado contrafactual.
    b3 = C["b3"]["vista_total_pct"]
    custos = sorted(round(custo_entrada_pct(rota, ordem["valor"], t) * ordem["valor"], 2)
                    for t in (b3["valor"], b3["divergencia"]["valor_alternativo"]))
    lo, hi = custos

    frase = f"Este m\u00eas, aporte {brl(ordem['valor'])} {rot['contracao']} {rot['rotulo']}."
    porque = "\u00c9 a parte da sua carteira mais abaixo da meta."
    blq = rota_bloqueada(r, P)
    trad = cen.get("motivos_em_linguagem_comum", {}).get(blq["rota_id"])
    rot_b = cen.get("rotulos", {}).get(blq["rota_id"])
    if not trad or not rot_b or trad.get("portao") != blq["portao"]:
        raise SystemExit(f"a rota bloqueada {blq['rota_id']} ({blq['portao']}) nao tem rotulo "
                         "e motivo em linguagem comum no cenario.yaml para ESTE portao")
    linha = f"{rot_b['rotulo'][0].upper()}{rot_b['rotulo'][1:]}: {trad['texto']}"
    for nome, t in (("frase_decisao", frase), ("porque", porque), ("linha_rota_bloqueada", linha)):
        if _palavras(t) > LIMITE_PALAVRAS:
            raise SystemExit(f"{nome} passa de {LIMITE_PALAVRAS} palavras (RI-01): {t!r}")
    return {
        "versao": 2,
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
        "base": {
            "status": "PARCIAL",
            "status_origem": ("custos.yaml -> b3.vista_total_pct.status, insumo do custo da "
                              "compra; o selo e o do insumo, sem contrafactual (S4, 27/09)"),
            "frase_decisao": frase,
            "valor": ordem["valor"],
            "valor_fmt": brl(ordem["valor"]),
            "valor_origem": "motor_aporte(...)['ordens'][0]['valor']",
            "destino": rot["rotulo"],
            "destino_origem": ("cenario.yaml -> rotulos[ordens[0]['rota']] (l-B: rotulo "
                               "generico no lugar do ticker)"),
            "rota_id": ordem["rota"],
            "deficit": ordem["deficit"],
            "deficit_origem": "motor_aporte(...)['ordens'][0]['deficit']: o maior do cenario",
            "data_referencia": f"{MESES[mes - 1]} de {ano}",
            "data_origem": ("procedencia['gerado_em'] (dia da rodada). O motor nao emite o "
                            "mes de referencia: decisao.data_referencia e NAO_EXISTE na F0"),
            "porque": porque,
            "porque_origem": ("texto; o fato e do motor: a rota escolhida e a de maior "
                              "deficit (motor_aporte ordena por deficit, k_max da politica)"),
            "custo_compra_min": lo,
            "custo_compra_max": hi,
            "custo_fmt": f"entre {brl(lo)} e {brl(hi)}",
            "custo_origem": ("custo_entrada_pct() com b3.vista_total_pct.valor e com "
                             "b3.vista_total_pct.divergencia.valor_alternativo (custos.yaml)"),
            "custo_motivo": "A tarifa da B3 tem duas fontes que ainda n\u00e3o batem.",
            "limitacao_quantidade": ("rota em lote sem preco no cenario: motor_aporte usa 1,0 "
                                     "(precos.get). A quantidade nao se mostra; o valor e o "
                                     "do motor"),
        },
        "com_rota_bloqueada": {
            "difere_da_base": "so pela linha abaixo (j-A); o resto e a base, igual",
            "linha": linha,
            "rota_id": blq["rota_id"],
            "portao": blq["portao"],
            "motivo_motor": blq["motivo_motor"],
            "rota_origem": blq["origem"],
            "linha_origem": ("cenario.yaml -> rotulos[rota_id] + motivos_em_linguagem_comum"
                             "[rota_id].texto, conferido contra o portao do motor"),
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
    # data_referencia deriva de gerado_em, que e volatil: compara-se com o mes da rodada
    # GRAVADA, nao com o de hoje. Sem isto o --conferir reprovava todo mes que virasse
    # (medido em 02/10/2026: "setembro de 2026" gravado contra "outubro" do motor).
    ano, mes, _ = (int(x) for x in str(gravado["meta"]["gerado_em"]).split("-"))
    agora["base"]["data_referencia"] = f"{MESES[mes - 1]} de {ano}"
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
    print(c["base"]["frase_decisao"], "|", c["base"]["custo_fmt"], "|",
          c["com_rota_bloqueada"]["linha"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
