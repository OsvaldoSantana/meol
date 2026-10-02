-- Prova de que o anon NAO le nada e so faz o que o esquema da (S6, P-162).
-- Rodar no editor SQL do Supabase, como o dono, DEPOIS do esquema.sql. Nao deixa rastro: tudo
-- roda numa transacao que termina em rollback (o contador volta ao que era).
-- Resultado esperado: so mensagens "ok: ..." e, no fim, "TODAS AS PROVAS PASSARAM". Qualquer
-- "FALHA: ..." e erro, e o esquema NAO pode ir para o convite.

begin;

set local role anon;

do $$
declare
  v json;
  v_id uuid;
begin
  -- 1. o anon nao le nenhuma das tres tabelas
  begin
    perform 1 from public.respostas limit 1;
    raise exception 'FALHA: o anon leu public.respostas';
  exception when insufficient_privilege then raise notice 'ok: o anon nao le respostas';
  end;
  begin
    perform 1 from public.aberturas limit 1;
    raise exception 'FALHA: o anon leu public.aberturas';
  exception when insufficient_privilege then raise notice 'ok: o anon nao le aberturas';
  end;
  begin
    perform 1 from public.contador_de_aberturas limit 1;
    raise exception 'FALHA: o anon leu public.contador_de_aberturas';
  exception when insufficient_privilege then raise notice 'ok: o anon nao le o contador';
  end;

  -- 2. o anon abre (a funcao do contador) e recebe id e versao de 1 a 6
  v := public.abrir_resposta();
  v_id := (v ->> 'id_resposta')::uuid;
  if (v ->> 'versao')::int not between 1 and 6 then
    raise exception 'FALHA: versao fora de 1 a 6: %', v;
  end if;
  raise notice 'ok: o anon abre uma resposta (versao %)', v ->> 'versao';

  -- 3. o anon insere a saida pelo consentimento, so nas colunas do envio
  insert into public.respostas (id_resposta, questionario_sha256, consentimento)
    values (v_id, repeat('0', 64), 'nao');
  raise notice 'ok: o anon insere uma resposta';

  -- 4. o anon nao escolhe o dia da conclusao (quem poe e o banco)
  begin
    insert into public.respostas (id_resposta, questionario_sha256, consentimento, concluida_em)
      values (gen_random_uuid(), repeat('0', 64), 'nao', date '2000-01-01');
    raise exception 'FALHA: o anon escolheu concluida_em';
  exception when insufficient_privilege then raise notice 'ok: o anon nao escolhe a data';
  end;

  -- 5. o anon nao altera nem apaga resposta, nem grava abertura sem a funcao
  begin
    update public.respostas set consentimento = 'sim' where id_resposta = v_id;
    raise exception 'FALHA: o anon alterou uma resposta';
  exception when insufficient_privilege then raise notice 'ok: o anon nao altera';
  end;
  begin
    delete from public.respostas where id_resposta = v_id;
    raise exception 'FALHA: o anon apagou uma resposta';
  exception when insufficient_privilege then raise notice 'ok: o anon nao apaga';
  end;
  begin
    insert into public.aberturas (versao) values (1);
    raise exception 'FALHA: o anon gravou uma abertura sem a funcao';
  exception when insufficient_privilege then raise notice 'ok: o anon nao grava abertura direto';
  end;
  begin
    update public.contador_de_aberturas set aberturas = 0;
    raise exception 'FALHA: o anon mexeu no contador';
  exception when insufficient_privilege then raise notice 'ok: o anon nao mexe no contador';
  end;

  -- 6. resposta sem abertura (id inventado) nao entra
  begin
    insert into public.respostas (id_resposta, questionario_sha256, consentimento)
      values (gen_random_uuid(), repeat('0', 64), 'nao');
    raise exception 'FALHA: entrou resposta sem abertura';
  exception when foreign_key_violation then raise notice 'ok: resposta sem abertura nao entra';
  end;

  raise notice 'TODAS AS PROVAS PASSARAM';
end;
$$;

rollback;
