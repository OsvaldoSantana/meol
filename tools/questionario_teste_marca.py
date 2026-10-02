# -*- coding: utf-8 -*-
"""Gera a versao de leitura do questionario do teste de marca a partir do YAML (P-162, P2).

POR QUE EXISTE. O questionario e DADO: a pagina da S6 e o script de analise leem o
`docs/marca/teste-de-marca/questionario.yaml`. Uma copia em Markdown escrita a mao
concordaria com o YAML por acaso e divergiria calada no primeiro ajuste (N-01). Aqui o
Markdown sai do YAML, e --conferir reprova se alguem o editar a mao.

    python tools/questionario_teste_marca.py            # grava o questionario.md
    python tools/questionario_teste_marca.py --conferir  # sai 1 se o gravado divergir
"""
from __future__ import annotations

import argparse
import os
import sys
from typing import Any

import yaml

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA = os.path.join(RAIZ, "docs", "marca", "teste-de-marca")
YAML = os.path.join(PASTA, "questionario.yaml")
MD = os.path.join(PASTA, "questionario.md")


def ler(path: str = YAML) -> dict[str, Any]:
    with open(path, encoding="utf-8") as f:
        d: dict[str, Any] = yaml.safe_load(f)
    return d


def _opcoes(p: dict[str, Any]) -> str:
    return " \u00b7 ".join(f"`{o['rotulo']}`" for o in p["opcoes"])


def gerar(q: dict[str, Any]) -> str:
    t = q["telas"]
    seg = t["exposicao_segundos"]
    obrig = "obrigat\u00f3ria" if t["lembranca"]["obrigatoria"] else "n\u00e3o obrigat\u00f3ria"
    L = [
        "# Teste de marca \u2014 o question\u00e1rio (vers\u00e3o de leitura)",
        "",
        "*GERADO de `questionario.yaml` por `tools/questionario_teste_marca.py`. N\u00e3o edite: "
        "`--conferir` reprova. Quem vale \u00e9 o YAML, cujo sha256 est\u00e1 no "
        "pr\u00e9-registro final.*",
        "",
        f"Vers\u00e3o {q['versao']}, {q['data']}.",
        "",
        "## 1. O convite (mensagem, fora da p\u00e1gina)",
        "",
        f"> {q['convite']['texto']}",
        "",
        "## 2. Consentimento",
        "",
        f"> {q['consentimento']['texto']}",
        "",
        f"Op\u00e7\u00f5es: {_opcoes(q['consentimento'])}. \"N\u00e3o concordo\" leva \u00e0 "
        "sa\u00edda.",
        "",
        "## 3. Filtro de entrada",
        "",
        f"> {q['filtro']['texto']}",
        "",
        f"Op\u00e7\u00f5es: {_opcoes(q['filtro'])}. \"N\u00e3o\" leva \u00e0 sa\u00edda.",
        "",
        "## 4. A pergunta dos amigos",
        "",
        f"> {q['amigo']['texto']}",
        "",
        f"Op\u00e7\u00f5es: {_opcoes(q['amigo'])}. Todos seguem; a an\u00e1lise sai com e sem "
        "quem responde "
        "\"Sim\", e a sem eles decide (r-a).",
        "",
        f"## 5. As {t['quantidade']} telas",
        "",
        "Antes de cada imagem, a instru\u00e7\u00e3o:",
        "",
        f"> {t['instrucao'].format(segundos=seg, n=t['quantidade'])}",
        "",
        "Antes das telas 2 em diante, a instru\u00e7\u00e3o curta (aqui, a da tela 2):",
        "",
        f"> {t['instrucao_curta'].format(k=2, segundos=seg, n=t['quantidade'])}",
        "",
        f"A imagem aparece quando a pessoa toca em \"{t['botao_ver']}\", fica **{seg} segundos**, "
        "some, e s\u00f3 ent\u00e3o v\u00eam as perguntas; n\u00e3o h\u00e1 como voltar a ela, e "
        "ela cabe inteira na tela, "
        "sem rolar. As telas 1 a 3 s\u00e3o as tr\u00eas dire\u00e7\u00f5es na vers\u00e3o base; "
        "as 4 a 6, as "
        "mesmas tr\u00eas, na mesma ordem, com a rota bloqueada.",
        "",
        f"1. **Aberta** (`{t['lembranca']['id']}`, "
        f"{obrig}): "
        f"{t['lembranca']['texto']}",
        f"2. **Cinco escalas de {t['escala_min']} a {t['escala_max']}, obrigat\u00f3rias**, sob a "
        "frase "
        f"\"{t['cabeca_das_escalas']}\", nesta ordem; o "
        f"{t['escala_min']} fica \u00e0 esquerda, o {t['escala_max']} \u00e0 direita, e o meio "
        "n\u00e3o tem "
        "r\u00f3tulo:",
        "",
        f"| id | pergunta | polo do {t['escala_min']} | polo do {t['escala_max']} |",
        "|---|---|---|---|",
    ]
    for e in t["escalas"]:
        L.append(f"| `{e['id']}` | {e['pergunta']} | {e['polo_1']} | {e['polo_7']} |")
    L += [
        "",
        "## 6. A pron\u00fancia do nome",
        "",
        f"> {q['pronuncia']['texto']}",
        "",
        "## 7. As mensagens finais",
        "",
        f"- **Quem respondeu tudo:** {q['final']['concluiu']}",
        f"- **Quem n\u00e3o concordou:** {q['final']['saida_sem_consentimento']}",
        f"- **Quem n\u00e3o passou no filtro:** {q['final']['saida_fora_do_filtro']}",
        "",
        "## 8. As seis ordens",
        "",
        f"Atribui\u00e7\u00e3o: {q['ordens']['atribuicao']}.",
        "",
        "| vers\u00e3o | telas 1 a 3 (base) e 4 a 6 (com rota bloqueada) |",
        "|---|---|",
    ]
    for v, ordem in q["ordens"]["versoes"].items():
        L.append(f"| {v} | {', '.join(ordem)} |")
    x = q["exportacao"]
    L += [
        "",
        "## 9. O contrato da exporta\u00e7\u00e3o (a p\u00e1gina da S6 grava assim)",
        "",
        f"Arquivo `{x['arquivo']}` (fora do git), {x['codificacao']}, separador "
        f"`{x['separador']}`, uma linha por **abertura** da p\u00e1gina. As respostas s\u00f3 "
        "s\u00e3o gravadas "
        "no envio final: quem para no meio deixa s\u00f3 a vers\u00e3o e o dia da abertura, com "
        "`concluida_em` vazio. Quem sai pelo consentimento ou pelo filtro conclui ali, e s\u00f3 "
        "a resposta que o tirou fica gravada. "
        f"Datas: {x['formato_data']}, sem hora. Colunas, nesta ordem:",
        "",
        f"- fixas: {', '.join(f'`{c}`' for c in x['colunas_fixas'])};",
        f"- por tela: {x['por_tela']};",
        f"- finais: {', '.join(f'`{c}`' for c in x['colunas_finais'])}.",
        "",
        "Nada de IP, nome ou e-mail. Exig\u00eancias de privacidade para a p\u00e1gina (ver "
        "`docs/fontes/vercel-supabase-metadados-de-acesso.md`):",
        "",
    ]
    priv = q["privacidade"]
    L += [f"- {r};" if i < len(priv) - 1 else f"- {r}." for i, r in enumerate(priv)]
    L += [
        "",
        "## 10. A janela",
        "",
        f"{q['janela']['dias']} dias corridos, no fuso `{q['janela']['fuso']}`; conta o "
        f"instante `{q['janela']['instante_que_conta']}`. As datas absolutas entram num commit "
        "pr\u00f3prio, antes do primeiro convite.",
        "",
    ]
    return "\n".join(L)


def conferir(q: dict[str, Any] | None = None, md: str = MD) -> bool:
    q = ler() if q is None else q
    if not os.path.exists(md):
        return False
    with open(md, encoding="utf-8") as f:
        return f.read() == gerar(q)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--conferir", action="store_true")
    a = ap.parse_args(argv)
    q = ler()
    if a.conferir:
        ok = conferir(q)
        print("questionario.md confere com o YAML" if ok else
              "questionario.md DIVERGE do YAML: rode sem --conferir e revise o diff")
        return 0 if ok else 1
    with open(MD, "w", encoding="utf-8", newline="\n") as f:
        f.write(gerar(q))
    print(f"gravado {os.path.relpath(MD, RAIZ)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
