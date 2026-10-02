// POST /api/enviar -- o envio unico do fim (as respostas so sao gravadas quando a pessoa
// conclui). Valida o corpo contra o questionario e insere em public.respostas com a chave
// anon, que so pode inserir. O dia da conclusao e o banco que poe.
'use strict';

const { INTERFACE, validar, supabase, soPost } = require('./_comum');

module.exports = async function enviar(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  if (!soPost(req, res)) return;
  const tamanho = Number(req.headers['content-length'] || 0);
  if (tamanho > INTERFACE.limites.corpo_do_envio_bytes) {
    res.status(413).json({ erro: 'tamanho' });
    return;
  }
  const corpo = req.body;
  const motivo = validar(corpo);
  if (motivo) {
    res.status(400).json({ erro: motivo });
    return;
  }
  const r = await supabase('respostas', corpo, 'return=minimal');
  if (r.status === 409) {
    res.status(409).json({ erro: 'ja enviada' });
    return;
  }
  if (!r.ok) {
    res.status(502).json({ erro: 'gravacao' });
    return;
  }
  res.status(204).end();
};
