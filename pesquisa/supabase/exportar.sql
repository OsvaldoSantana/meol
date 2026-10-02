-- GERADO por `python tools/questionario_json.py` a partir de
-- docs/marca/teste-de-marca/questionario.yaml -- nao editar a mao (P2);
-- `--conferir` reprova se este arquivo divergir do gerador.
--
-- A exportacao para a analise (tools/analise_teste_marca.py): uma linha por ABERTURA (ab-a),
-- com EXATAMENTE as colunas do contrato, na ordem dele (questionario.yaml -> exportacao). Rodar
-- como o dono, no editor SQL, e baixar o resultado em CSV como data/teste-marca/respostas.csv
-- (fora do git). O sha256 do questionario NAO vai na exportacao (o contrato nao o tem): confira-o
-- antes com a consulta do fim, que tem de dar UM valor so, o gravado no pre-registro final.

select
  a.id_resposta,
  a.versao,
  to_char(a.aberta_em, 'YYYY-MM-DD') as aberta_em,
  to_char(r.concluida_em, 'YYYY-MM-DD') as concluida_em,
  r.consentimento,
  r.filtro,
  r.amigo,
  r.t1_lembra,
  r.t1_seguro,
  r.t1_para_mim,
  r.t1_honesto,
  r.t1_confiavel,
  r.t1_luxo,
  r.t2_lembra,
  r.t2_seguro,
  r.t2_para_mim,
  r.t2_honesto,
  r.t2_confiavel,
  r.t2_luxo,
  r.t3_lembra,
  r.t3_seguro,
  r.t3_para_mim,
  r.t3_honesto,
  r.t3_confiavel,
  r.t3_luxo,
  r.t4_lembra,
  r.t4_seguro,
  r.t4_para_mim,
  r.t4_honesto,
  r.t4_confiavel,
  r.t4_luxo,
  r.t5_lembra,
  r.t5_seguro,
  r.t5_para_mim,
  r.t5_honesto,
  r.t5_confiavel,
  r.t5_luxo,
  r.t6_lembra,
  r.t6_seguro,
  r.t6_para_mim,
  r.t6_honesto,
  r.t6_confiavel,
  r.t6_luxo,
  r.pronuncia
from public.aberturas a
left join public.respostas r using (id_resposta)
order by a.aberta_em, a.id_resposta;

-- Conferencia: um sha256 so, igual ao de questionario.yaml no pre-registro final.
-- select questionario_sha256, count(*) from public.respostas group by 1;
