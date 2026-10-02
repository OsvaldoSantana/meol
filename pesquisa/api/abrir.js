// POST /api/abrir -- a abertura (ab-a, g-B revista). Chama public.abrir_resposta() no
// Supabase, que soma 1 ao contador, grava a abertura e devolve o id e a versao. Se falhar,
// devolve erro, e a pagina PARA: nao ha sorteio no lugar (P1: ausencia nao vira valor).
'use strict';

const { Q, supabase, soPost } = require('./_comum');

const N_VERSOES = Object.keys(Q.questionario.ordens.versoes).length;

module.exports = async function abrir(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  if (!soPost(req, res)) return;
  const r = await supabase('rpc/abrir_resposta', {});
  const d = r.dados;
  const versao = d && Number(d.versao);
  if (!r.ok || !d || typeof d.id_resposta !== 'string' ||
      !Number.isInteger(versao) || versao < 1 || versao > N_VERSOES) {
    res.status(502).json({ erro: 'abertura' });
    return;
  }
  res.status(200).json({ id_resposta: d.id_resposta, versao });
};
