# -*- coding: utf-8 -*-
"""A guarda de segredo dos workflows: lista de PERMISSAO, uma funcao para todos (CX-01).

Por que existe: cada guarda procurava `secrets.NOME` por regex, e `secrets['NOME']`,
`toJSON(secrets)` e `secrets[format(...)]` passavam; o YAML vigente so usava a forma com
ponto e mascarava o buraco (padrao F-05/N-01: a guarda prometia mais do que fazia).

A regra: toda expressao `${{ ... }}` (e todo `if:`, que e expressao sem delimitador) que
mencione o identificador `secrets` tem de ser EXATAMENTE `secrets.<NOME>`, escrita no `env`
de um passo, com <NOME> permitido para aquele (job, passo). Qualquer outra forma, ou o mesmo
nome em outro lugar (env do workflow, env do job, `with:`, `run:`, `if:`), e defeito.
O que a funcao NAO ve: segredo lido de dentro de um script (`os.environ`) por quem ja tem o
env do passo; e workflow reutilizavel (`uses:` de outro repositorio) -- por isso `secrets:`
como chave, inclusive `secrets: inherit`, tambem reprova."""
from __future__ import annotations

import re

EXPRESSAO = re.compile(r"\$\{\{(.*?)\}\}", re.DOTALL)
MENCAO = re.compile(r"\bsecrets\b", re.IGNORECASE)
FORMA_PERMITIDA = re.compile(r"\s*secrets\.([A-Za-z0-9_]+)\s*", re.IGNORECASE)


def _valores(no, caminho=()):
    """Percorre o YAML inteiro: (caminho, chave_final, valor_escalar)."""
    if isinstance(no, dict):
        for k, v in no.items():
            if isinstance(k, str) and MENCAO.fullmatch(k.strip()):
                yield caminho + (k,), "<chave>", k
            yield from _valores(v, caminho + (k,))
    elif isinstance(no, list):
        for i, v in enumerate(no):
            yield from _valores(v, caminho + (i,))
    else:
        yield caminho, (caminho[-1] if caminho else None), no


def _expressoes(valor, chave):
    """As expressoes de um escalar. `if:` e expressao inteira, com ou sem `${{ }}`."""
    if not isinstance(valor, str):
        return [], False
    achadas = [m.group(1) for m in EXPRESSAO.finditer(valor)]
    resto = EXPRESSAO.sub("", valor)
    aberta = "${{" in resto and bool(MENCAO.search(resto))
    if chave == "if" and not achadas:
        achadas = [valor]
    return achadas, aberta


def referencias(d):
    """[(job, passo, onde, expressao)] de toda mencao a `secrets` -- 'onde' e o caminho
    dentro do job (ou do workflow). Serve ao teste de vacuidade."""
    out = []
    for caminho, chave, valor in _valores(d):
        if chave == "<chave>":
            job, passo, onde = _local(d, caminho)
            out.append((job, passo, onde, "<chave secrets>"))
            continue
        exprs, aberta = _expressoes(valor, chave)
        job, passo, onde = _local(d, caminho)
        for e in exprs:
            if MENCAO.search(e):
                out.append((job, passo, onde, e.strip()))
        if aberta:
            out.append((job, passo, onde, "<expressao sem fechamento>"))
    return out


def _local(d, caminho):
    """(job|None, nome do passo|None, 'campo.subcampo')."""
    if len(caminho) >= 2 and caminho[0] == "jobs":
        job = caminho[1]
        if len(caminho) >= 4 and caminho[2] == "steps":
            p = d["jobs"][job]["steps"][caminho[3]]
            nome = p.get("name") or p.get("id") or p.get("uses") or f"#{caminho[3]}"
            return job, nome, ".".join(str(c) for c in caminho[4:])
        return job, None, ".".join(str(c) for c in caminho[2:])
    return None, None, ".".join(str(c) for c in caminho)


def defeitos_de_segredo(d, permitidos):
    """[defeito] -- vazio e o unico resultado aceito.

    `permitidos`: {(job, nome_do_passo): {NOME, ...}}. So o `env` desse passo pode ler esses
    segredos, e so pela forma `secrets.NOME`. Cada chave tem de casar com exatamente um passo."""
    out = []
    # CX-01 (retratacao): autorizar por nome so vale se o nome acha UM passo. Dois homonimos
    # herdariam a autorizacao um do outro; zero e lista permitindo o que nao existe.
    for (job, nome), _ in permitidos.items():
        passos = d.get("jobs", {}).get(job, {}).get("steps", [])
        n = sum(1 for p in passos if p.get("name") == nome)
        if n != 1:
            out.append(f"passo autorizado {nome!r} do job {job!r} casa com {n} passos; "
                       "tem de ser exatamente 1")
    for job, passo, onde, expr in referencias(d):
        local = f"{job or '<workflow>'}/{passo or '<fora de passo>'}/{onde}"
        autorizado = passo is not None and (job, passo) in permitidos
        if not (autorizado and onde.startswith("env.")):
            out.append(f"segredo fora do env de um passo autorizado: {local}: {expr}")
            continue
        m = FORMA_PERMITIDA.fullmatch(expr)
        if not m:
            out.append(f"forma de segredo nao permitida em {local}: {expr!r}; so secrets.NOME")
        elif m.group(1) not in permitidos[(job, passo)]:
            out.append(f"segredo {m.group(1)} nao permitido no passo {passo!r} ({local})")
    return out


_R2 = frozenset({"R2_ACCOUNT_ID", "R2_ACCESS_KEY_ID", "R2_SECRET_ACCESS_KEY", "R2_BUCKET"})
_R2_LEITURA = frozenset({"R2_LEITURA_ACCOUNT_ID", "R2_LEITURA_ACCESS_KEY_ID",
                         "R2_LEITURA_SECRET_ACCESS_KEY", "R2_LEITURA_BUCKET"})

# A lista de permissao, UMA so (N-01): workflow -> {(job, passo): segredos que o env do passo
# pode ler}. Workflow sem entrada aqui reprova (test_guarda_segredos): nao existe workflow
# "esquecido" pela guarda. mutacao.yml e vazio de proposito: nao le segredo.
PERMITIDOS_POR_WORKFLOW = {
    "medir.yml": {("medir", "Medir (token de leitura)"): _R2_LEITURA},
    "testes.yml": {("completo", "Materializar o acervo do armazem"): _R2},
    "mutacao.yml": {},
    "captura_cvm.yml": {("captura", n): _R2 for n in (
        "Capturar", "Capturar COTAHIST", "Capturar NEFIN", "Capturar eventos B3",
        "Conciliar COTAHIST", "Publicar CVM")},
}
