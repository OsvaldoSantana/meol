# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motor import carregar as carregar_custos
from alocacao import Estado, carregar_politica, alocar, motor_aporte, catalogo, custo_de_discordar

C, P = carregar_custos(), carregar_politica()
ROTAS = {r.id: r for r in catalogo(C)}

print("="*100); print("CAMADA 5 — MOTOR DE APORTE"); print("="*100)
e0 = Estado(despesa_mensal=4500, reserva_atual=27000, aporte_mensal=500, horizonte_anos=25)
alvo = alocar(e0, C, P)["alvo"]
print("\n[a] primeiro aporte, sem posicao (P-164) — uma ordem, e o porque:")
o0 = motor_aporte(e0, alvo, C, P, rotas_por_id=ROTAS)["ordens"][0]
print(f"    {ROTAS[o0['rota']].nome}: R${o0['valor']:,.2f}")
print("   ", o0["porque"])

print("\n[b] com 18 meses de aportes ja feitos, e a carteira derivou:")
e1 = Estado(despesa_mensal=4500, reserva_atual=27000, aporte_mensal=500, horizonte_anos=25,
    posicoes={"bova11":2400,"pibb11":900,"divo11":950,"smal11":1500,"ivvb11":1100,
              "acao_zero":800,"td_selic":1300,"hash11":650})
PRECOS = {"bova11":128.43,"pibb11":302.11,"divo11":11.77,"smal11":98.02,"ivvb11":415.60,
          "acao_zero":37.19,"td_selic":1.0,"hash11":48.10}
r = motor_aporte(e1, alvo, C, P, precos=PRECOS, rotas_por_id=ROTAS)
print(f"    patrimonio R${r['patrimonio']:,.0f} · aporte R${r['aporte']:,.0f} · "
      f"maior deficit {r['deficit_max']*100:.1f} p.p. · "
      f"maior excesso {r['excesso_max']*100:.1f} p.p.")
print(f"\n    {'ordem':<34}{'valor':>10}{'deficit':>11}{'atual':>9}{'alvo':>9}")
for o in r["ordens"]:
    print(f"    {ROTAS[o['rota']].nome:<34}{o['valor']:>10,.2f}{o['deficit']:>11,.0f}"
          f"{o['peso_atual']*100:>8.1f}%{o['peso_alvo']*100:>8.1f}%"
          f"   ({o['quantidade']} x R${o['preco']:.2f})")
print(f"    residuo de lote para caixa: R${r['caixa']:,.2f}")
for a in r["alertas"]:
    print(f"    [ALERTA {a['tipo']}] {ROTAS[a['rota']].nome}: "
          f"{a['peso']*100:.1f}% > teto {a['teto']*100:.0f}% — {a['acao']}")

print("\n[c] gatilho de deriva estrutural — patrimonio grande, aporte pequeno:")
e2 = Estado(despesa_mensal=4500, reserva_atual=27000, aporte_mensal=500, horizonte_anos=25,
    posicoes={"bova11":900000,"td_selic":100000})
r2 = motor_aporte(e2, alvo, C, P)
d = r2["deriva"]
print(f"    capacidade anual do aporte: {d['capacidade_anual']*100:.2f}% do patrimonio")
print(f"    maior DEFICIT a fechar:     {d['deficit_max']*100:.1f} p.p.")
print(f"    maior excesso (nao e problema do aporte): {d['excesso_max']*100:.1f} p.p.")
print(f"    -> {d['nota']}")

print("\n" + "="*100); print("CAMADA 4 — CUSTO DE DISCORDAR"); print("="*100)
proposta = dict(alvo["pesos"])
proposta["hash11"] = 0.15
resto = 1 - 0.15
soma_outros = sum(v for k,v in alvo["pesos"].items() if k!="hash11")
for k in proposta:
    if k!="hash11": proposta[k] = alvo["pesos"][k]/soma_outros*resto
d = custo_de_discordar(alvo["pesos"], proposta, C, 500, 25, ROTAS)
print("\n  você quer 15% em cripto; a regra diz 3%.")
print(f"  arrasto da regra:     {d['arrasto_alvo_aa']*100:.3f}% a.a.")
print(f"  arrasto da sua versao:{d['arrasto_proposta_aa']*100:.3f}% a.a.")
print(f"  diferenca:            {d['diferenca_pp_aa']:+.3f} p.p. ao ano — SÓ de custo")
print(f"\n  {d['nota']}")
print("\n  O sistema nao impede. Mostra o preco e registra a decisao.")
