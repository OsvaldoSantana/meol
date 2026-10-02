-- GERADO por `python tools/questionario_json.py` a partir de
-- docs/marca/teste-de-marca/questionario.yaml -- nao editar a mao (P2);
-- `--conferir` reprova se este arquivo divergir do gerador.
--
-- O banco da pagina do teste de marca (P-162, S6). Rodar UMA vez, no editor SQL do projeto
-- Supabase, como o dono (postgres). Depois, rodar teste_politicas.sql (prova que o anon nao le).
--
-- O que o anon pode, e so isto (o anon e o papel da chave que a funcao da Vercel usa):
--   * executar public.abrir_resposta(): soma 1 ao contador, grava a ABERTURA (versao e dia) e
--     devolve o id e a versao (ab-a: uma linha por abertura, conclua ou nao; a versao e
--     (contador mod 6) + 1, g-B revista);
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
  versao smallint not null check (versao between 1 and 6),
  aberta_em date not null default ((now() at time zone 'America/Sao_Paulo')::date)
);

create table public.respostas (
  id_resposta uuid primary key references public.aberturas (id_resposta),
  questionario_sha256 text not null check (questionario_sha256 ~ '^[0-9a-f]{64}$'),
  concluida_em date not null default ((now() at time zone 'America/Sao_Paulo')::date),
  consentimento text not null check (consentimento in ('sim', 'nao')),
  filtro text check (filtro in ('sim', 'nao')),
  amigo text check (amigo in ('sim', 'nao')),
  t1_lembra text check (char_length(t1_lembra) <= 2000),
  t2_lembra text check (char_length(t2_lembra) <= 2000),
  t3_lembra text check (char_length(t3_lembra) <= 2000),
  t4_lembra text check (char_length(t4_lembra) <= 2000),
  t5_lembra text check (char_length(t5_lembra) <= 2000),
  t6_lembra text check (char_length(t6_lembra) <= 2000),
  t1_seguro smallint check (t1_seguro between 1 and 7),
  t1_para_mim smallint check (t1_para_mim between 1 and 7),
  t1_honesto smallint check (t1_honesto between 1 and 7),
  t1_confiavel smallint check (t1_confiavel between 1 and 7),
  t1_luxo smallint check (t1_luxo between 1 and 7),
  t2_seguro smallint check (t2_seguro between 1 and 7),
  t2_para_mim smallint check (t2_para_mim between 1 and 7),
  t2_honesto smallint check (t2_honesto between 1 and 7),
  t2_confiavel smallint check (t2_confiavel between 1 and 7),
  t2_luxo smallint check (t2_luxo between 1 and 7),
  t3_seguro smallint check (t3_seguro between 1 and 7),
  t3_para_mim smallint check (t3_para_mim between 1 and 7),
  t3_honesto smallint check (t3_honesto between 1 and 7),
  t3_confiavel smallint check (t3_confiavel between 1 and 7),
  t3_luxo smallint check (t3_luxo between 1 and 7),
  t4_seguro smallint check (t4_seguro between 1 and 7),
  t4_para_mim smallint check (t4_para_mim between 1 and 7),
  t4_honesto smallint check (t4_honesto between 1 and 7),
  t4_confiavel smallint check (t4_confiavel between 1 and 7),
  t4_luxo smallint check (t4_luxo between 1 and 7),
  t5_seguro smallint check (t5_seguro between 1 and 7),
  t5_para_mim smallint check (t5_para_mim between 1 and 7),
  t5_honesto smallint check (t5_honesto between 1 and 7),
  t5_confiavel smallint check (t5_confiavel between 1 and 7),
  t5_luxo smallint check (t5_luxo between 1 and 7),
  t6_seguro smallint check (t6_seguro between 1 and 7),
  t6_para_mim smallint check (t6_para_mim between 1 and 7),
  t6_honesto smallint check (t6_honesto between 1 and 7),
  t6_confiavel smallint check (t6_confiavel between 1 and 7),
  t6_luxo smallint check (t6_luxo between 1 and 7),
  pronuncia text check (char_length(pronuncia) <= 200),
  -- quem nao consentiu ou nao passou no filtro grava so a resposta que o tirou; quem passou
  -- grava a pergunta dos amigos e todas as notas (escalas obrigatorias)
  constraint coerencia check (
    case
      when consentimento = 'nao' then num_nonnulls(filtro, amigo, t1_lembra, t2_lembra, t3_lembra, t4_lembra, t5_lembra, t6_lembra, t1_seguro, t1_para_mim, t1_honesto, t1_confiavel, t1_luxo, t2_seguro, t2_para_mim, t2_honesto, t2_confiavel, t2_luxo, t3_seguro, t3_para_mim, t3_honesto, t3_confiavel, t3_luxo, t4_seguro, t4_para_mim, t4_honesto, t4_confiavel, t4_luxo, t5_seguro, t5_para_mim, t5_honesto, t5_confiavel, t5_luxo, t6_seguro, t6_para_mim, t6_honesto, t6_confiavel, t6_luxo, pronuncia) = 0
      when filtro is null then false
      when filtro = 'nao' then num_nonnulls(amigo, t1_lembra, t2_lembra, t3_lembra, t4_lembra, t5_lembra, t6_lembra, t1_seguro, t1_para_mim, t1_honesto, t1_confiavel, t1_luxo, t2_seguro, t2_para_mim, t2_honesto, t2_confiavel, t2_luxo, t3_seguro, t3_para_mim, t3_honesto, t3_confiavel, t3_luxo, t4_seguro, t4_para_mim, t4_honesto, t4_confiavel, t4_luxo, t5_seguro, t5_para_mim, t5_honesto, t5_confiavel, t5_luxo, t6_seguro, t6_para_mim, t6_honesto, t6_confiavel, t6_luxo, pronuncia) = 0
      else amigo is not null and num_nonnulls(t1_seguro, t1_para_mim, t1_honesto, t1_confiavel, t1_luxo, t2_seguro, t2_para_mim, t2_honesto, t2_confiavel, t2_luxo, t3_seguro, t3_para_mim, t3_honesto, t3_confiavel, t3_luxo, t4_seguro, t4_para_mim, t4_honesto, t4_confiavel, t4_luxo, t5_seguro, t5_para_mim, t5_honesto, t5_confiavel, t5_luxo, t6_seguro, t6_para_mim, t6_honesto, t6_confiavel, t6_luxo) = 30
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
  v_versao := (v_anteriores % 6) + 1;
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
grant insert (id_resposta, questionario_sha256, consentimento, filtro, amigo, t1_lembra, t1_seguro, t1_para_mim, t1_honesto, t1_confiavel, t1_luxo, t2_lembra, t2_seguro, t2_para_mim, t2_honesto, t2_confiavel, t2_luxo, t3_lembra, t3_seguro, t3_para_mim, t3_honesto, t3_confiavel, t3_luxo, t4_lembra, t4_seguro, t4_para_mim, t4_honesto, t4_confiavel, t4_luxo, t5_lembra, t5_seguro, t5_para_mim, t5_honesto, t5_confiavel, t5_luxo, t6_lembra, t6_seguro, t6_para_mim, t6_honesto, t6_confiavel, t6_luxo, pronuncia) on table public.respostas to anon;

create policy anon_so_insere on public.respostas for insert to anon with check (true);

commit;
