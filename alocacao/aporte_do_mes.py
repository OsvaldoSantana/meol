# -*- coding: utf-8 -*-
"""A porta de uso do M1 (P-181): o que fazer com o aporte deste mes, em linguagem comum.

POR QUE EXISTE. Ate 10/10/2026 o motor tinha codigo pronto e nenhuma porta: dos tres modulos
que liam o `estado.yaml`, nenhum chamava `alocar()` nem `motor_aporte()`, e o `demo_aporte.py`
usava um estado escrito no codigo. Nao havia como a pessoa perguntar "o que faco com o aporte
deste mes". Este comando le o estado dela, roda os portoes e o motor, e devolve tres coisas:
QUANTO, PARA ONDE e POR QUE -- com a procedencia de cada numero e o portao que eliminou cada
rota que ficou de fora.

    py -3.11 alocacao/aporte_do_mes.py
    py -3.11 alocacao/aporte_do_mes.py --preco bova11=128,43 --preco td_selic=19943,12
    py -3.11 alocacao/aporte_do_mes.py --aporte 1500        # mes com bonus (o alvo nao muda)

O QUE ELE NAO FAZ (P5): nao compra nem vende; nao grava a decisao (o registro com data e hash
e a T5 do mapa de telas, ainda nao feito); nao escolhe vencimento de Tesouro IPCA+ (o PU dele
depende do vencimento, e o comando pede o preco); nao le preco de ETF sozinho -- pede.

PRECO. O motor usa `precos.get(rota, 1.0)`: sem preco, uma rota negociada em lote seria
calculada a R$ 1,00 e a ordem sairia com a quantidade errada, sem aviso nenhum. Por isso o
comando vigia QUAIS precos o motor consultou (`PrecosVigiados`) e recusa a saida se algum
deles era de rota em lote sem preco informado -- e pede exatamente esses. O PU do Tesouro
Selic vem do CSV oficial do Tesouro Transparente, com data e sha256; sem rede, pede-se o PU.

Codigos de saida: 0 resposta dada; 2 o estado precisa de ajuste; 3 falta preco.
"""
from __future__ import annotations
import argparse
import csv
import datetime as dt
import hashlib
import io
import os
import re
import sys
import urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import estado_io  # noqa: E402
from alocacao import (Estado, alocar, carregar_politica, catalogo,  # noqa: E402
                      motor_aporte, preco_do_lote)
from motor import carregar as carregar_custos  # noqa: E402

URL_TESOURO = ("https://www.tesourotransparente.gov.br/ckan/dataset/"
               "df56aa42-484a-4a59-8184-7676580c81e3/resource/"
               "796d2059-14e9-44e3-80c9-2d9e30b405c1/download/PrecoTaxaTesouroDireto.csv")
# Qual titulo do CSV responde por qual rota. So o Selic: o PU do IPCA+ depende do
# vencimento, que vem do compromisso registrado (G8), e o comando nao o escolhe.
TITULO_DA_ROTA = {"td_selic": "Tesouro Selic"}

# Onde o motor guarda quem ficou de fora, e qual portao tirou. O texto de cada portao e do
# politica.yaml (porta_de_uso.fora_por_portao).
FORA = (("fora_status", "G5_status"), ("fora_atrito", "G3_atrito"),
        ("sem_tese", "G7_tese_registrada"), ("sem_carrego", "G8_compromisso_de_carrego"),
        ("dominados", "G4_dominancia"))

MESES = ("janeiro", "fevereiro", "marco", "abril", "maio", "junho", "julho", "agosto",
         "setembro", "outubro", "novembro", "dezembro")


class PrecosVigiados(dict):
    """O dicionario de precos que anota toda rota que o motor consultou. E assim que o comando
    sabe se o 1.0 de reserva do motor entrou numa conta que importava."""

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.consultadas = set()

    def get(self, chave, padrao=None):
        self.consultadas.add(chave)
        return super().get(chave, padrao)

    def __bool__(self):
        # O motor faz `precos = precos or {}`: vazio, este objeto seria trocado por um dict
        # comum e a vigilancia sumiria justamente no caso em que nenhum preco foi dado.
        return True


def reais(v):
    """R$ 1.234,56 -- o formato que a pessoa le no banco."""
    s = f"{abs(v):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return ("-R$ " if v < 0 else "R$ ") + s


def numero_br(texto):
    """'19.943,12', '19943,12' ou '19943.12' -> 19943.12; '1.500' -> 1500.0. O argumento vem do
    teclado de quem le o banco, e ponto sozinho em grupos de tres e separador de milhar."""
    t = texto.strip()
    if "," in t or re.fullmatch(r"\d{1,3}(\.\d{3})+", t):
        t = t.replace(".", "").replace(",", ".")   # "1.500" e mil e quinhentos, nao 1,5
    return float(t)


def pu_do_tesouro(texto_csv, titulo):
    """O maior PU de compra do dia mais recente, entre os vencimentos de `titulo` a venda.

    O maior, e nao o mais barato: o minimo (0,01 titulo, P-179) tem de caber em QUALQUER
    vencimento que a pessoa escolher na corretora. Devolve dict(pu, data_base, vencimento) ou
    None se o titulo nao aparece."""
    linhas = [x for x in csv.DictReader(io.StringIO(texto_csv), delimiter=";")
              if x.get("Tipo Titulo") == titulo]
    if not linhas:
        return None

    def data(s):
        return dt.datetime.strptime(s, "%d/%m/%Y").date()

    ultima = max(data(x["Data Base"]) for x in linhas)
    do_dia = [(numero_br(x["PU Compra Manha"]), x["Data Vencimento"]) for x in linhas
              if data(x["Data Base"]) == ultima and numero_br(x["PU Compra Manha"]) > 0]
    if not do_dia:
        return None
    pu, venc = max(do_dia)
    return dict(pu=pu, data_base=ultima, vencimento=venc)


def baixar_csv_tesouro(url=URL_TESOURO, timeout=60):
    """(texto, sha256) do CSV oficial. Falha de rede levanta: quem chama decide pedir o PU."""
    with urllib.request.urlopen(url, timeout=timeout) as r:
        bruto = r.read()
    return bruto.decode("utf-8", errors="replace"), hashlib.sha256(bruto).hexdigest()


def precos_informados(pares, rotas):
    """--preco ROTA=VALOR -> ({rota: preco do LOTE}, {rota: procedencia}, [erros]).

    A pessoa informa o preco que ve: a cota do ETF, o PU de 1 titulo do Tesouro. A conversao
    para o preco de um lote e de `preco_do_lote()` (P-179), nunca de quem digita."""
    precos, origem, erros = {}, {}, []
    for par in pares or []:
        rota, _, valor = par.partition("=")
        rota = rota.strip().lower()
        if rota not in rotas:
            erros.append(f"--preco {par}: nao existe rota '{rota}' no catalogo")
            continue
        try:
            unit = numero_br(valor)
        except ValueError:
            erros.append(f"--preco {par}: '{valor}' nao e numero")
            continue
        if not unit > 0:
            erros.append(f"--preco {par}: o preco tem de ser maior que zero")
            continue
        precos[rota] = preco_do_lote(rotas[rota], unit)
        origem[rota] = f"{reais(unit)} informado por voce (--preco) em {dt.date.today():%d/%m/%Y}"
    return precos, origem, erros


def _nome(rid, rotas):
    r = rotas.get(rid)
    return r.nome if r is not None else rid


def _quantidade(ordem, rotas):
    r = rotas.get(ordem["rota"])
    if r is not None and r.lote_fracao is not None:
        q = ordem["quantidade"] * r.lote_fracao
        return f"{q:.2f}".replace(".", ",") + " titulo"
    if r is not None and r.negocia_em_lote:
        return f"{int(ordem['quantidade'])} cota(s)"
    return None


def quem_ficou_de_fora(resultado, textos):
    """[(nome da rota, frase do portao)] -- todo eliminado, com o portao que o eliminou."""
    u = resultado.get("universo") or {}
    linhas = []
    for chave, portao in FORA:
        for item in u.get(chave, []):
            r = item[0] if isinstance(item, tuple) else item
            if chave == "fora_status":
                motivo = (r.bloqueios[0] if r.bloqueios else "status")
            elif chave in ("sem_tese", "sem_carrego"):
                motivo = item[1]
            else:
                motivo = ""
            rival = item[3].nome if chave == "dominados" else ""
            frase = textos["fora_por_portao"][portao].format(motivo=_curto(motivo), rival=rival)
            linhas.append((r.nome, portao, frase))
    vivas = {v[0].id for v in u.get("vivos", [])}
    for r, funcao, motivos in resultado.get("incoerencias_de_funcao", []):
        if funcao == "TODAS" and r.id not in vivas:
            frase = textos["fora_por_portao"]["G6_coerencia_funcao"].format(
                motivo=_curto("; ".join(motivos)), rival="")
            linhas.append((r.nome, "G6_coerencia_funcao", frase))
    return linhas


def _curto(texto, n=110):
    t = " ".join(str(texto).split())
    return t if len(t) <= n else t[:n - 3].rstrip() + "..."


def responder(estado_doc, C, P, precos_lote=None, origem_precos=None, aporte_do_mes=None,
              hoje=None):
    """O coracao do comando, sem disco nem rede: (codigo, linhas de texto). Testavel sobre um
    estado sintetico (`test_aporte_do_mes.py`)."""
    hoje = hoje or dt.date.today()
    textos = P["porta_de_uso"]
    d, problemas, avisos = estado_io.validar(estado_doc, P)
    if problemas:
        out = ["Antes de responder, o seu estado.yaml precisa de ajuste:", ""]
        out += [f"  - {p}" for p in problemas]
        return 2, out
    rotas = {r.id: r for r in catalogo(C)}
    e = Estado(**d)
    res = alocar(e, C, P)
    A = aporte_do_mes if aporte_do_mes is not None else e.aporte_mensal
    out = [f"APORTE DE {MESES[hoje.month - 1].upper()} DE {hoje.year} -- {reais(A)}", ""]

    if res.get("alvo") is None:
        out += _resposta_da_diretiva(res, A)
        motor = None
    else:
        vigiados = PrecosVigiados(precos_lote or {})
        motor = motor_aporte(e, res["alvo"], C, P, precos=vigiados, rotas_por_id=rotas,
                             aporte_do_mes=aporte_do_mes)
        faltam = sorted(rid for rid in vigiados.consultadas
                        if rid not in (precos_lote or {}) and rid in rotas
                        and rotas[rid].negocia_em_lote)
        if faltam:
            ex = f"{faltam[0]}=<preco de hoje>"
            nomes = ", ".join(f"{_nome(r, rotas)} ({r})" for r in faltam)
            return 3, [" ".join(textos["falta_preco"].format(rotas=nomes, exemplo=ex).split())]
        out += _resposta_do_motor(motor, rotas)

    fora = quem_ficou_de_fora(res, textos)
    if fora:
        out += ["", "QUEM FICOU DE FORA, E POR QUE"]
        out += [f"  - {nome}: {frase} [{portao}]" for nome, portao, frase in fora]
    pend = res.get("pendencias") or []
    if pend:
        out += ["", "O QUE O SISTEMA PEDE DE VOCE"]
        out += [f"  - {_curto(p.pergunta, 200)}" for p in pend]
    out += ["", "DE ONDE VEIO CADA NUMERO"]
    meta = estado_doc.get("meta") or {}
    out.append(f"  - aporte, reserva e despesa: o seu estado.yaml (preenchido em "
               f"{meta.get('preenchido_em') or 'data nao informada'})")
    if aporte_do_mes is not None:
        out.append(f"  - aporte deste mes: {reais(aporte_do_mes)} informado por voce (--aporte); "
                   f"o alvo continua calculado sobre {reais(e.aporte_mensal)}")
    for rid, txt in sorted((origem_precos or {}).items()):
        if motor is not None and rid in vigiados.consultadas:
            out.append(f"  - preco de {_nome(rid, rotas)}: {txt}")
    pr = res["procedencia"]
    out.append(f"  - regras: politica.yaml versao {pr['politica_versao']} (impressao "
               f"{pr['politica_hash']}); custos.yaml (impressao {pr['custos_hash']})")
    out += [f"  - aviso do validador: {a}" for a in avisos]
    out += ["", " ".join(textos["aviso"].split())]
    return 0, out


def _resposta_da_diretiva(res, A):
    """O pipeline parou num portao da fase de aporte (divida, contrapartida, reserva)."""
    dv = res["diretiva"]
    out = [f"O QUE FAZER: {dv.veredito}", f"  destino: {dv.destino}", ""]
    m = dv.memoria or {}
    if dv.portao == "G2_reserva" and m:
        out += ["POR QUE",
                f"  - a sua reserva de emergencia tem {reais(m['atual'])} e o alvo e "
                f"{reais(m['alvo'])} ({m['meses_alvo']:.0f} meses de despesa); faltam "
                f"{reais(m['falta'])}.",
                "  - enquanto a reserva nao estiver completa, o aporte vai para ela, e nao "
                "para investimento (portao G2_reserva)."]
        if m.get("meses_para_completar"):
            out.append(f"  - no ritmo do aporte, ela se completa em cerca de "
                       f"{m['meses_para_completar']} meses.")
        comp = m.get("composicao") or []
        if comp:
            out.append(f"  - comece por: {comp[0]['nome']}.")
        out += [f"  - atencao: {_curto(a, 220)}" for a in m.get("alertas", [])]
    else:
        out += ["POR QUE", f"  - portao {dv.portao}; valor: {reais(dv.valor or A)}"]
    return out


def _resposta_do_motor(motor, rotas):
    st = motor["status"]
    if st == "SEM_APORTE":
        return ["O QUE FAZER: nada a comprar este mes -- o aporte e zero.", ""]
    if st == "NENHUMA_ROTA_CABE":
        out = [f"O QUE FAZER: guardar {reais(motor['caixa'])} no caixa. {motor['motivo']}", ""]
        out += ["POR QUE"] + [f"  - {_nome(x['rota'], rotas)}: {x['detalhe']}"
                              for x in motor.get("nao_couberam", [])]
        return out
    out = ["O QUE FAZER"]
    for i, o in enumerate(motor["ordens"], start=1):
        q = _quantidade(o, rotas)
        out.append(f"  {i}. {_nome(o['rota'], rotas)}: {reais(o['valor'])}"
                   + (f" ({q})" if q else ""))
    if motor.get("caixa"):
        out.append(f"  - fica no caixa: {reais(motor['caixa'])} (sobra de lote ou de limite)")
    out += ["", "POR QUE"]
    for o in motor["ordens"]:
        if o.get("porque"):
            out.append(f"  - {' '.join(o['porque'].split())}")
        else:
            out.append(f"  - {_nome(o['rota'], rotas)}: hoje {o['peso_atual']:.1%} da carteira, "
                       f"alvo {o['peso_alvo']:.1%}; e a parte mais longe do alvo.")
    out += [f"  - nao coube: {_nome(x['rota'], rotas)} ({x['detalhe']})"
            for x in motor.get("nao_couberam", [])]
    out += [f"  - fora da fila: {_nome(a['rota'], rotas)} ja passou do teto ({a['acao']})"
            for a in motor.get("alertas", [])]
    if motor.get("deriva"):
        out.append(f"  - {' '.join(motor['deriva']['nota'].split())}")
    return out


def main(argv=None, saida=sys.stdout, baixar=baixar_csv_tesouro):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--estado", default=os.path.join(AQUI, "estado.yaml"))
    ap.add_argument("--preco", action="append", metavar="ROTA=VALOR")
    ap.add_argument("--aporte", help="o valor deste mes, se diferente do aporte_mensal")
    ap.add_argument("--sem-rede", action="store_true", help="nao baixa o PU do Tesouro")
    a = ap.parse_args(argv)
    if saida is sys.stdout and hasattr(saida, "reconfigure"):
        # Console do Windows redirecionado usa cp1252: um caractere fora dele derrubaria a
        # resposta inteira no fim. Melhor um "?" no lugar do que nenhuma resposta.
        saida.reconfigure(errors="replace")
    import yaml
    if not os.path.exists(a.estado):
        print(f"Nao achei o arquivo {a.estado}. Copie alocacao/estado.exemplo.yaml para "
              f"alocacao/estado.yaml, preencha os seus numeros e rode de novo.", file=saida)
        return 2
    with open(a.estado, encoding="utf-8") as f:
        doc = yaml.safe_load(f) or {}
    C, P = carregar_custos(), carregar_politica()
    rotas = {r.id: r for r in catalogo(C)}
    precos, origem, erros = precos_informados(a.preco, rotas)
    if erros:
        print("\n".join(erros), file=saida)
        return 2
    if not a.sem_rede:
        for rid, titulo in TITULO_DA_ROTA.items():
            if rid in precos:
                continue
            try:
                texto, sha = baixar()
            except Exception as ex:   # rede: sem PU, o comando pede (codigo 3)
                origem[f"_{rid}"] = f"nao baixado ({type(ex).__name__})"
                continue
            pu = pu_do_tesouro(texto, titulo)
            if pu:
                precos[rid] = preco_do_lote(rotas[rid], pu["pu"])
                origem[rid] = (f"PU de compra {reais(pu['pu'])} em {pu['data_base']:%d/%m/%Y} "
                               f"({titulo} {pu['vencimento']}, o maior PU do dia), "
                               f"Tesouro Transparente, sha256 {sha[:12]}")
    aporte = numero_br(a.aporte) if a.aporte else None
    codigo, linhas = responder(doc, C, P, precos, {k: v for k, v in origem.items()
                                                   if not k.startswith("_")}, aporte)
    print("\n".join(linhas), file=saida)
    return codigo


if __name__ == "__main__":
    raise SystemExit(main())
