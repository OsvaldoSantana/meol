# -*- coding: utf-8 -*-
"""Gera, do questionario pre-registrado, tudo o que a pagina e o banco da pesquisa leem (S6, P2).

POR QUE EXISTE. O questionario do teste de marca e DADO, congelado pelo sha256 no
pre-registro final (`docs/marca/teste-de-marca/preregistro-final.md`). A pagina (`pesquisa/`)
nao pode ter texto de pergunta escrito a mao, e o banco nao pode ter uma lista de colunas que
concorde com a analise por acaso (N-01). Daqui saem, do `questionario.yaml`:

  pesquisa/questionario.json        o questionario para a pagina e para a funcao de envio,
                                    com o sha256 do YAML (vai em cada resposta)
  pesquisa/estimulos/*.png          copias BYTE A BYTE dos seis PNG aprovados (a Vercel so
                                    serve o que esta dentro de pesquisa/)
  pesquisa/supabase/esquema.sql     as tabelas, o RLS e as permissoes do anon
  pesquisa/supabase/exportar.sql    a consulta que devolve EXATAMENTE as colunas do contrato
                                    que tools/analise_teste_marca.py le

As colunas vem de `analise_teste_marca.colunas_esperadas()`: uma lista so, a da analise.

O QUE ELE NAO FAZ (P5). Nao cria projeto, nao roda SQL em banco nenhum e nao publica nada:
o deploy e as contas sao dele (roteiro em PENDENCIAS.md, "Ao voltar ao desktop").

    python tools/questionario_json.py            # grava os quatro
    python tools/questionario_json.py --conferir  # sai 1 se algum gravado divergir
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from typing import Any

import yaml

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)
from analise_teste_marca import colunas_esperadas  # noqa: E402  (N-01: a lista da analise)

YAML = os.path.join(RAIZ, "docs", "marca", "teste-de-marca", "questionario.yaml")
PESQUISA = os.path.join(RAIZ, "pesquisa")
JSON = os.path.join(PESQUISA, "questionario.json")
INTERFACE = os.path.join(PESQUISA, "interface.json")
ESTIMULOS = os.path.join(PESQUISA, "estimulos")
ESQUEMA = os.path.join(PESQUISA, "supabase", "esquema.sql")
EXPORTAR = os.path.join(PESQUISA, "supabase", "exportar.sql")
VERSOES_DO_ESTIMULO = {"base": "base", "rota": "rota-bloqueada"}
CABECALHO_SQL = ("-- GERADO por `python tools/questionario_json.py` a partir de\n"
                 "-- docs/marca/teste-de-marca/questionario.yaml -- nao editar a mao (P2);\n"
                 "-- `--conferir` reprova se este arquivo divergir do gerador.\n")
# Colunas que o BANCO preenche, nunca quem envia: a versao e o dia da abertura saem da funcao
# do contador; o dia da conclusao, do default da tabela (so o dia, em Brasilia: a tabela nao
# tem hora -- questionario.yaml -> privacidade).
DA_ABERTURA = ("id_resposta", "versao", "aberta_em")
DO_BANCO_NA_CONCLUSAO = ("concluida_em",)


def _sha256(path: str) -> str:
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def ler_yaml(path: str = YAML) -> dict[str, Any]:
    with open(path, encoding="utf-8") as f:
        d: dict[str, Any] = yaml.safe_load(f)
    return d


def ler_interface(path: str = INTERFACE) -> dict[str, Any]:
    with open(path, encoding="utf-8") as f:
        d: dict[str, Any] = json.load(f)
    return d


def _estimulos(q: dict[str, Any]) -> dict[str, dict[str, str]]:
    """{direcao: {base|rota: caminho relativo a pesquisa/}} e a origem de cada copia."""
    return {d: {v: f"estimulos/{d}-{VERSOES_DO_ESTIMULO[v]}.png" for v in caminhos}
            for d, caminhos in q["telas"]["estimulos"].items()}


def gerar_json(yaml_path: str = YAML) -> dict[str, Any]:
    q = ler_yaml(yaml_path)
    origem = q["telas"]["estimulos"]
    destino = _estimulos(q)
    q["telas"]["estimulos"] = destino
    sha_png = {destino[d][v]: _sha256(os.path.join(RAIZ, *origem[d][v].split("/")))
               for d in origem for v in origem[d]}
    return {
        "_gerado_por": "python tools/questionario_json.py -- nao editar a mao",
        "questionario_sha256": _sha256(yaml_path),
        "estimulos_origem": {destino[d][v]: origem[d][v] for d in origem for v in origem[d]},
        "estimulos_sha256": sha_png,
        "questionario": json.loads(json.dumps(q, default=str)),
    }


def texto_json(d: dict[str, Any]) -> str:
    return json.dumps(d, ensure_ascii=True, indent=1, sort_keys=False) + "\n"


# ---------------------------------------------------------------- SQL --------------------

def colunas_de_envio(q: dict[str, Any]) -> list[str]:
    """O que a pessoa (pela funcao de envio) grava: o contrato menos o que o banco preenche,
    mais o sha256 do questionario."""
    return (["id_resposta", "questionario_sha256"]
            + [c for c in colunas_esperadas(q) if c not in DA_ABERTURA + DO_BANCO_NA_CONCLUSAO])


def _por_tela(q: dict[str, Any]) -> tuple[list[str], list[str]]:
    t = q["telas"]
    ks = range(1, t["quantidade"] + 1)
    abertas = [f"t{k}_{t['lembranca']['id']}" for k in ks]
    escalas = [f"t{k}_{e['id']}" for k in ks for e in t["escalas"]]
    return abertas, escalas


def gerar_esquema(q: dict[str, Any], interface: dict[str, Any]) -> str:
    t = q["telas"]
    lim = interface["limites"]
    sim, nao = q["exportacao"]["valores_sim_nao"]
    n_versoes = len(q["ordens"]["versoes"])
    fuso = q["janela"]["fuso"]
    hoje = f"((now() at time zone '{fuso}')::date)"
    abertas, escalas = _por_tela(q)
    pron = q["pronuncia"]["id"]
    simnao = f"in ('{sim}', '{nao}')"
    linhas = [
        f"  {q['consentimento']['id']} text not null check ({q['consentimento']['id']} {simnao}),",
        f"  {q['filtro']['id']} text check ({q['filtro']['id']} {simnao}),",
        f"  {q['amigo']['id']} text check ({q['amigo']['id']} {simnao}),",
    ]
    for c in abertas:
        linhas.append(f"  {c} text check (char_length({c}) <= {lim['texto_aberto_caracteres']}),")
    faixa = f"between {t['escala_min']} and {t['escala_max']}"
    for c in escalas:
        linhas.append(f"  {c} smallint check ({c} {faixa}),")
    linhas.append(f"  {pron} text check (char_length({pron}) <= {lim['pronuncia_caracteres']}),")
    resto = ", ".join([q["amigo"]["id"]] + abertas + escalas + [pron])
    tudo = ", ".join([q["filtro"]["id"]] + [q["amigo"]["id"]] + abertas + escalas + [pron])
    cons, filt, amig = q["consentimento"]["id"], q["filtro"]["id"], q["amigo"]["id"]
    obrig = (f"{amig} is not null and num_nonnulls({', '.join(escalas)}) = {len(escalas)}"
             if t["escalas_obrigatorias"] else f"{amig} is not null")
    envio = colunas_de_envio(q)
    return CABECALHO_SQL + f"""--
-- O banco da pagina do teste de marca (P-162, S6). Rodar UMA vez, no editor SQL do projeto
-- Supabase, como o dono (postgres). Depois, rodar teste_politicas.sql (prova que o anon nao le).
--
-- O que o anon pode, e so isto (o anon e o papel da chave que a funcao da Vercel usa):
--   * executar public.abrir_resposta(): soma 1 ao contador, grava a ABERTURA (versao e dia) e
--     devolve o id e a versao (ab-a: uma linha por abertura, conclua ou nao; a versao e
--     (contador mod {n_versoes}) + 1, g-B revista);
--   * inserir em public.respostas, e so nas colunas do envio: o dia da conclusao e o banco que
--     poe. Nenhum select, update ou delete, em tabela nenhuma.
-- Nenhuma coluna de IP, nome, e-mail, user agent ou hora: as datas sao so o dia, em Brasilia
-- (questionario.yaml -> privacidade e exportacao).

begin;

create table public.contador_de_aberturas (
  unica boolean primary key default true check (unica),
  aberturas bigint not null default 0
);
insert into public.contador_de_aberturas (unica, aberturas) values (true, 0);

create table public.aberturas (
  id_resposta uuid primary key default gen_random_uuid(),
  versao smallint not null check (versao between 1 and {n_versoes}),
  aberta_em date not null default {hoje}
);

create table public.respostas (
  id_resposta uuid primary key references public.aberturas (id_resposta),
  questionario_sha256 text not null check (questionario_sha256 ~ '^[0-9a-f]{{64}}$'),
  concluida_em date not null default {hoje},
{chr(10).join(linhas)}
  -- quem nao consentiu ou nao passou no filtro grava so a resposta que o tirou; quem passou
  -- grava a pergunta dos amigos e todas as notas (escalas obrigatorias)
  constraint coerencia check (
    case
      when {cons} = '{nao}' then num_nonnulls({tudo}) = 0
      when {filt} is null then false
      when {filt} = '{nao}' then num_nonnulls({resto}) = 0
      else {obrig}
    end)
);

create function public.abrir_resposta()
returns json
language plpgsql
security definer
set search_path = ''
as $$
declare
  v_anteriores bigint;
  v_versao smallint;
  v_id uuid;
begin
  update public.contador_de_aberturas set aberturas = aberturas + 1 where unica
    returning aberturas - 1 into v_anteriores;
  v_versao := (v_anteriores % {n_versoes}) + 1;
  insert into public.aberturas (versao) values (v_versao) returning id_resposta into v_id;
  return json_build_object('id_resposta', v_id, 'versao', v_versao);
end;
$$;

alter table public.contador_de_aberturas enable row level security;
alter table public.aberturas enable row level security;
alter table public.respostas enable row level security;

-- O Supabase da ao anon, por padrao, tudo nas tabelas novas do schema public, e o Postgres da
-- execucao de toda funcao nova a PUBLIC. Tira-se tudo, e devolve-se so o necessario.
revoke all on table public.contador_de_aberturas from public, anon, authenticated;
revoke all on table public.aberturas from public, anon, authenticated;
revoke all on table public.respostas from public, anon, authenticated;
revoke all on function public.abrir_resposta() from public, anon, authenticated;

grant execute on function public.abrir_resposta() to anon;
grant insert ({', '.join(envio)}) on table public.respostas to anon;

create policy anon_so_insere on public.respostas for insert to anon with check (true);

commit;
"""


def gerar_exportar(q: dict[str, Any]) -> str:
    origem = {c: "a" for c in DA_ABERTURA}
    cols = []
    for c in colunas_esperadas(q):
        if c in ("aberta_em", "concluida_em"):
            tab = origem.get(c, "r")
            cols.append(f"  to_char({tab}.{c}, 'YYYY-MM-DD') as {c}")
        else:
            cols.append(f"  {origem.get(c, 'r')}.{c}")
    return CABECALHO_SQL + f"""--
-- A exportacao para a analise (tools/analise_teste_marca.py): uma linha por ABERTURA (ab-a),
-- com EXATAMENTE as colunas do contrato, na ordem dele (questionario.yaml -> exportacao). Rodar
-- como o dono, no editor SQL, e baixar o resultado em CSV como data/teste-marca/respostas.csv
-- (fora do git). O sha256 do questionario NAO vai na exportacao (o contrato nao o tem): confira-o
-- antes com a consulta do fim, que tem de dar UM valor so, o gravado no pre-registro final.

select
{("," + chr(10)).join(cols)}
from public.aberturas a
left join public.respostas r using (id_resposta)
order by a.aberta_em, a.id_resposta;

-- Conferencia: um sha256 so, igual ao de questionario.yaml no pre-registro final.
-- select questionario_sha256, count(*) from public.respostas group by 1;
"""


# ---------------------------------------------------------------- gravar e conferir ------

def alvos() -> dict[str, bytes]:
    """{caminho absoluto: conteudo} de tudo o que o gerador escreve."""
    q, i = ler_yaml(), ler_interface()
    j = gerar_json()
    out = {JSON: texto_json(j).encode("utf-8"),
           ESQUEMA: gerar_esquema(q, i).encode("utf-8"),
           EXPORTAR: gerar_exportar(q).encode("utf-8")}
    for destino, origem in j["estimulos_origem"].items():
        with open(os.path.join(RAIZ, *origem.split("/")), "rb") as f:
            out[os.path.join(PESQUISA, *destino.split("/"))] = f.read()
    return out


def gravar() -> list[str]:
    feitos = []
    for path, conteudo in alvos().items():
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            f.write(conteudo)
        feitos.append(os.path.relpath(path, RAIZ))
    return feitos


def conferir() -> list[str]:
    """Os arquivos gravados que divergem do que o gerador produz hoje (ou que faltam)."""
    out = []
    for path, conteudo in alvos().items():
        if not os.path.isfile(path):
            out.append(f"falta {os.path.relpath(path, RAIZ)}")
            continue
        with open(path, "rb") as f:
            gravado = f.read()
        if not path.endswith(".png"):
            # F-04: o git no Windows pode trazer CRLF no checkout; o conteudo e o mesmo
            gravado = gravado.replace(b"\r\n", b"\n")
        if gravado != conteudo:
            out.append(f"diverge {os.path.relpath(path, RAIZ)}")
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=(__doc__ or "").split("\n")[0])
    ap.add_argument("--conferir", action="store_true")
    a = ap.parse_args(argv)
    if a.conferir:
        dif = conferir()
        for d in dif:
            print(d)
        return 1 if dif else 0
    for f in gravar():
        print(f"gravado {f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
