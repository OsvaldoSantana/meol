// A pagina do teste de marca (S6, P-162). Executa o questionario pre-registrado
// (docs/marca/teste-de-marca/questionario.yaml), lido de questionario.json, que e GERADO por
// tools/questionario_json.py. Nenhum texto de pergunta mora aqui, nem a duracao da exposicao,
// nem as ordens: tudo vem do JSON (P2). Os textos de botao e de erro vem de interface.json.
//
// O que a pagina NAO faz: nao sorteia versao (se /api/abrir falhar, ela para -- P1); nao
// grava nada antes do fim (um envio so); nao usa cookie nem script de terceiros; a marca no
// aparelho (localStorage) so AVISA que este aparelho ja enviou, e nao bloqueia.
'use strict';

(function () {
  const raiz = document.getElementById('pesquisa');
  let Q = null;   // questionario.json inteiro
  let q = null;   // Q.questionario
  let UI = null;  // interface.json
  const estado = { id: null, versao: null, ordem: null, respostas: {} };

  function el(tag, attrs, filhos) {
    const e = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs || {})) {
      if (k === 'texto') e.textContent = v;
      else if (k === 'aoClicar') e.addEventListener('click', v);
      else if (v === true) e.setAttribute(k, '');
      else if (v !== false && v !== null && v !== undefined) e.setAttribute(k, v);
    }
    for (const f of filhos || []) e.appendChild(f);
    return e;
  }

  function formatar(texto, vars) {
    return texto.replace(/\{(\w+)\}/g, (m, k) => (k in vars ? String(vars[k]) : m));
  }

  // Troca a tela inteira e leva o foco ao primeiro texto (teclado e leitor de tela).
  function tela(filhos) {
    raiz.replaceChildren(...filhos);
    const alvo = raiz.querySelector('[data-foco]');
    if (alvo) {
      alvo.setAttribute('tabindex', '-1');
      alvo.focus();
    }
  }

  function botao(texto, aoClicar) {
    return el('button', { type: 'button', texto, aoClicar });
  }

  async function obterJson(caminho) {
    const r = await fetch(caminho, { cache: 'no-store' });
    if (!r.ok) throw new Error(caminho);
    return r.json();
  }

  function jaEnviou() {
    try { return window.localStorage.getItem(UI.marca_no_aparelho) === '1'; } catch (_e) { return false; }
  }

  function marcarEnvio() {
    try { window.localStorage.setItem(UI.marca_no_aparelho, '1'); } catch (_e) { /* sem marca */ }
  }

  function falhaAoAbrir() {
    tela([el('p', { 'data-foco': true, role: 'alert', texto: UI.falha_ao_abrir })]);
  }

  // ------------------------------------------------------------------ inicio ----------
  async function iniciar() {
    try {
      Q = await obterJson('questionario.json');
      UI = await obterJson('interface.json');
    } catch (_e) {
      document.getElementById('falha-de-carga').hidden = false;
      return;
    }
    q = Q.questionario;
    document.title = UI.titulo_da_pagina;
    tela([el('p', { 'data-foco': true, texto: UI.carregando })]);
    let d = null;
    try {
      const r = await fetch('/api/abrir', {
        method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{}',
      });
      if (r.ok) d = await r.json();
    } catch (_e) {
      d = null;
    }
    const ordem = d && q.ordens.versoes[String(d.versao)];
    if (!d || typeof d.id_resposta !== 'string' || !ordem) {
      falhaAoAbrir();
      return;
    }
    estado.id = d.id_resposta;
    estado.versao = d.versao;
    estado.ordem = ordem;
    precarregar();
    if (jaEnviou()) {
      tela([el('p', { 'data-foco': true, texto: UI.ja_respondeu }),
        el('div', { class: 'acoes' }, [botao(UI.botao_continuar, () => escolha(q.consentimento, filtro))])]);
    } else {
      escolha(q.consentimento, filtro);
    }
  }

  function estimulo(k) {
    const n = estado.ordem.length;
    const direcao = estado.ordem[(k - 1) % n];
    return q.telas.estimulos[direcao][k <= n ? 'base' : 'rota'];
  }

  function precarregar() {
    for (let k = 1; k <= q.telas.quantidade; k++) {
      const i = new Image();
      i.src = estimulo(k);
    }
  }

  // --------------------------------------------- consentimento, filtro, amigos -------
  function escolha(pergunta, depois) {
    const acoes = pergunta.opcoes.map((o) => botao(o.rotulo, () => {
      estado.respostas[pergunta.id] = o.valor;
      const saida = pergunta.se && pergunta.se[o.valor];
      if (saida) enviar(saida);
      else depois();
    }));
    tela([el('p', { 'data-foco': true, texto: pergunta.texto }),
      el('div', { class: 'acoes' }, acoes)]);
  }

  function filtro() { escolha(q.filtro, amigo); }
  function amigo() { escolha(q.amigo, () => instrucao(1)); }

  // -------------------------------------------------------------- as telas -----------
  function vars(k) {
    return { n: q.telas.quantidade, k, segundos: q.telas.exposicao_segundos };
  }

  function instrucao(k) {
    const texto = formatar(k === 1 ? q.telas.instrucao : q.telas.instrucao_curta, vars(k));
    tela([el('p', { 'data-foco': true, texto }),
      el('div', { class: 'acoes' }, [botao(q.telas.botao_ver, () => expor(k))])]);
  }

  // A exposicao: a imagem aparece pelo tempo do questionario (exposicao_segundos) e sai do
  // documento. Nao ha botao de voltar a ela.
  function expor(k) {
    const img = el('img', { id: 'estimulo', src: estimulo(k), alt: UI.texto_alternativo_da_tela,
      hidden: true });
    tela([el('div', { class: 'exposicao' }, [img])]);
    let comecou = false;
    const comecar = () => {
      if (comecou) return;
      comecou = true;
      img.hidden = false;
      setTimeout(() => {
        img.remove();
        perguntas(k);
      }, q.telas.exposicao_segundos * 1000);
    };
    img.addEventListener('error', () => {
      tela([el('p', { 'data-foco': true, role: 'alert', texto: UI.falha_na_imagem })]);
    });
    if (img.complete && img.naturalWidth > 0) comecar();
    else img.addEventListener('load', comecar);
  }

  function escala(k, e) {
    const nome = `t${k}_${e.id}`;
    const pontos = [];
    for (let v = q.telas.escala_min; v <= q.telas.escala_max; v++) {
      const polo = v === q.telas.escala_min ? e.polo_1 : (v === q.telas.escala_max ? e.polo_7 : null);
      const filhos = [el('input', { type: 'radio', name: nome, value: String(v) }),
        el('span', { 'aria-hidden': 'true', texto: String(v) }),
        el('span', { class: 'so-leitor', texto: polo ? `${v}, ${polo}` : String(v) })];
      pontos.push(el('label', { class: 'ponto' }, filhos));
    }
    return el('fieldset', { 'data-nome': nome }, [
      el('legend', { texto: e.pergunta }),
      el('div', { class: 'polos', 'aria-hidden': 'true' },
        [el('span', { texto: e.polo_1 }), el('span', { texto: e.polo_7 })]),
      el('div', { class: 'pontos' }, pontos),
    ]);
  }

  function campoAberto(id, texto, limite) {
    return [el('label', { class: 'campo', for: id }, [
      document.createTextNode(`${texto} `),
      el('span', { class: 'secundario', texto: UI.opcional })]),
    el('textarea', { id, name: id, maxlength: String(limite), rows: '3' })];
  }

  function textoOuNulo(id) {
    const v = document.getElementById(id).value.trim();
    return v === '' ? null : v;
  }

  function perguntas(k) {
    const idLembra = `t${k}_${q.telas.lembranca.id}`;
    const conjuntos = q.telas.escalas.map((e) => escala(k, e));
    const alerta = el('div', { class: 'alerta', role: 'alert', hidden: true });
    const proxima = () => {
      const faltam = [];
      for (const [i, e] of q.telas.escalas.entries()) {
        const marcado = conjuntos[i].querySelector('input:checked');
        if (marcado) estado.respostas[`t${k}_${e.id}`] = Number(marcado.value);
        else if (q.telas.escalas_obrigatorias) faltam.push([i, e]);
      }
      if (faltam.length) {
        alerta.replaceChildren(document.createTextNode(UI.falta_nota),
          el('ul', {}, faltam.map(([, e]) => el('li', { texto: e.pergunta }))));
        alerta.hidden = false;
        conjuntos[faltam[0][0]].querySelector('input').focus();
        return;
      }
      estado.respostas[idLembra] = textoOuNulo(idLembra);
      if (k < q.telas.quantidade) instrucao(k + 1);
      else pronuncia();
    };
    const lembra = campoAberto(idLembra, q.telas.lembranca.texto,
      UI.limites.texto_aberto_caracteres);
    lembra[0].setAttribute('data-foco', '');
    tela([...lembra,
      el('p', { class: 'secundario', texto: q.telas.cabeca_das_escalas }),
      ...conjuntos, alerta,
      el('div', { class: 'acoes' }, [botao(UI.botao_proxima, proxima)])]);
  }

  function pronuncia() {
    const id = q.pronuncia.id;
    const campo = campoAberto(id, q.pronuncia.texto, UI.limites.pronuncia_caracteres);
    campo[0].setAttribute('data-foco', '');
    tela([...campo, el('div', { class: 'acoes' }, [botao(UI.botao_enviar, () => {
      estado.respostas[id] = textoOuNulo(id);
      enviar('concluiu');
    })])]);
  }

  // ------------------------------------------------------------------ o envio --------
  // Um envio so, no fim (ou na saida pelo consentimento ou pelo filtro). POST, com as
  // respostas no corpo: nada vai na URL (questionario.yaml -> privacidade).
  async function enviar(final) {
    const corpo = { id_resposta: estado.id, questionario_sha256: Q.questionario_sha256,
      ...estado.respostas };
    tela([el('p', { 'data-foco': true, role: 'status', texto: UI.enviando })]);
    let ok = false;
    try {
      const r = await fetch('/api/enviar', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(corpo),
      });
      ok = r.status === 204 || r.status === 409;   // 409: este envio ja tinha chegado
    } catch (_e) {
      ok = false;
    }
    if (!ok) {
      tela([el('p', { 'data-foco': true, role: 'alert', texto: UI.falha_ao_enviar }),
        el('div', { class: 'acoes' }, [botao(UI.botao_tentar_de_novo, () => enviar(final))])]);
      return;
    }
    marcarEnvio();
    tela([el('p', { 'data-foco': true, texto: q.final[final] })]);
  }

  iniciar();
}());
