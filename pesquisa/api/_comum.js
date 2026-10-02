// O que as duas funcoes da Vercel dividem (S6, P-162). O prefixo "_" impede a Vercel de
// servir este arquivo como funcao.
//
// Privacidade (questionario.yaml -> privacidade): nada aqui escreve no log -- nem corpo, nem
// cabecalho, nem erro com conteudo. O Supabase recebe so a chave e o corpo; os cabecalhos do
// cliente (x-forwarded-for, x-real-ip, user-agent) nunca sao repassados.
'use strict';

const Q = require('../questionario.json');
const INTERFACE = require('../interface.json');

const SIM_NAO = Q.questionario.exportacao.valores_sim_nao;
const T = Q.questionario.telas;
const ABERTAS = [];
const ESCALAS = [];
for (let k = 1; k <= T.quantidade; k++) {
  ABERTAS.push(`t${k}_${T.lembranca.id}`);
  for (const e of T.escalas) ESCALAS.push(`t${k}_${e.id}`);
}
const CONS = Q.questionario.consentimento.id;
const FILT = Q.questionario.filtro.id;
const AMIGO = Q.questionario.amigo.id;
const PRON = Q.questionario.pronuncia.id;
const NAO = SIM_NAO[1];
const PERMITIDAS = new Set(['id_resposta', 'questionario_sha256', CONS, FILT, AMIGO,
  ...ABERTAS, ...ESCALAS, PRON]);
const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/;

function simNao(v) {
  return SIM_NAO.includes(v);
}

// Devolve null se o corpo cumpre o questionario, ou o motivo (sem eco do conteudo) se nao.
function validar(corpo) {
  if (corpo === null || typeof corpo !== 'object' || Array.isArray(corpo)) return 'corpo';
  for (const k of Object.keys(corpo)) if (!PERMITIDAS.has(k)) return 'campo desconhecido';
  if (typeof corpo.id_resposta !== 'string' || !UUID.test(corpo.id_resposta)) return 'id';
  if (corpo.questionario_sha256 !== Q.questionario_sha256) return 'questionario';
  if (!simNao(corpo[CONS])) return CONS;
  const depois = [FILT, AMIGO, ...ABERTAS, ...ESCALAS, PRON];
  const presentes = (ks) => ks.filter((k) => corpo[k] !== undefined && corpo[k] !== null);
  if (corpo[CONS] === NAO) return presentes(depois).length ? 'sobra depois do consentimento' : null;
  if (!simNao(corpo[FILT])) return FILT;
  if (corpo[FILT] === NAO) {
    return presentes(depois.slice(1)).length ? 'sobra depois do filtro' : null;
  }
  if (!simNao(corpo[AMIGO])) return AMIGO;
  for (const k of ESCALAS) {
    const v = corpo[k];
    const falta = v === undefined || v === null;
    if (falta && T.escalas_obrigatorias) return 'falta nota';
    if (!falta && (!Number.isInteger(v) || v < T.escala_min || v > T.escala_max)) return 'nota';
  }
  const lim = INTERFACE.limites;
  for (const k of ABERTAS) {
    const v = corpo[k];
    if (v !== undefined && v !== null &&
        (typeof v !== 'string' || v.length > lim.texto_aberto_caracteres)) return 'texto';
  }
  const p = corpo[PRON];
  if (p !== undefined && p !== null &&
      (typeof p !== 'string' || p.length > lim.pronuncia_caracteres)) return PRON;
  return null;
}

// Uma chamada ao PostgREST do Supabase com a chave do papel anon. Nenhum cabecalho do cliente
// vai junto. A chave pode ser a publicavel (sb_publishable_..., que vira o papel anon) ou a
// anon antiga (um JWT, "eyJ..."). A publicavel vai SO no apikey: no Authorization ela e
// recusada com "Invalid JWT" (docs do Supabase, "Migrating to new API keys", lido em 02/10/2026).
async function supabase(caminho, corpo, prefer) {
  const url = process.env.SUPABASE_URL;
  const chave = process.env.SUPABASE_ANON_KEY;
  if (!url || !chave) return { ok: false, status: 503 };
  const cab = { apikey: chave, 'Content-Type': 'application/json' };
  if (chave.startsWith('eyJ')) cab.Authorization = `Bearer ${chave}`;
  if (prefer) cab.Prefer = prefer;
  let r;
  try {
    r = await fetch(`${url.replace(/\/+$/, '')}/rest/v1/${caminho}`,
      { method: 'POST', headers: cab, body: JSON.stringify(corpo) });
  } catch (_e) {
    return { ok: false, status: 502 };
  }
  let dados = null;
  if (r.ok && r.status !== 204) {
    try { dados = await r.json(); } catch (_e) { dados = null; }
  }
  return { ok: r.ok, status: r.status, dados };
}

function soPost(req, res) {
  if (req.method === 'POST') return true;
  res.setHeader('Allow', 'POST');
  res.status(405).json({ erro: 'metodo' });
  return false;
}

module.exports = { Q, INTERFACE, validar, supabase, soPost };
