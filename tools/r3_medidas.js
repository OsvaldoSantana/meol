// O que o navegador devolve de cada elemento visivel na primeira tela da R3 (P-170).
// Lido por tools/r3_capturar.py e avaliado dentro da pagina: so le, nao clica nem muda nada.
() => {
  const W = window.innerWidth, H = window.innerHeight;
  const vis = (el) => {
    const r = el.getBoundingClientRect(), s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && r.bottom > 0 && r.top < H && r.right > 0 && r.left < W
      && s.visibility !== 'hidden' && s.display !== 'none' && parseFloat(s.opacity) > 0.05;
  };
  const caixa = (r) => [Math.round(r.left), Math.round(r.top), Math.round(r.width), Math.round(r.height)];
  const botoes = [];
  for (const el of document.querySelectorAll('a, button, [role=button], input[type=submit], input[type=button]')) {
    if (!vis(el)) continue;
    const s = getComputedStyle(el), r = el.getBoundingClientRect();
    const txt = (el.innerText || el.value || el.getAttribute('aria-label') || '').trim().slice(0, 60);
    botoes.push({texto: txt, caixa: caixa(r), fundo: s.backgroundColor, cor: s.color,
                 borda_cor: s.borderTopColor, borda_px: s.borderTopWidth, borda_estilo: s.borderTopStyle,
                 raio: s.borderTopLeftRadius, imagem_de_fundo: s.backgroundImage !== 'none'});
  }
  const textos = [];
  const andar = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  while (andar.nextNode()) {
    const n = andar.currentNode, t = n.textContent.trim();
    if (!t) continue;
    const el = n.parentElement;
    if (!el || !vis(el)) continue;
    const s = getComputedStyle(el), r = el.getBoundingClientRect();
    textos.push({texto: t.slice(0, 60), corpo_px: parseFloat(s.fontSize), familia: s.fontFamily,
                 peso: s.fontWeight, caixa: caixa(r), tag: el.tagName.toLowerCase()});
  }
  textos.sort((a, b) => b.corpo_px - a.corpo_px);
  const fixos = [];
  for (const el of document.querySelectorAll('body *')) {
    const s = getComputedStyle(el);
    if (s.position !== 'fixed' && s.position !== 'sticky') continue;
    if (!vis(el)) continue;
    const r = el.getBoundingClientRect();
    const area = Math.max(0, Math.min(r.right, W) - Math.max(r.left, 0))
               * Math.max(0, Math.min(r.bottom, H) - Math.max(r.top, 0));
    if (area / (W * H) >= 0.15)
      fixos.push({tag: el.tagName.toLowerCase(), id: el.id, classe: String(el.className).slice(0, 80),
                  fracao: Math.round(100 * area / (W * H)) / 100, texto: (el.innerText || '').trim().slice(0, 80)});
  }
  const lojas = [...document.querySelectorAll('a[href*="apps.apple.com"], a[href*="itunes.apple.com"]')]
    .map(a => a.href).slice(0, 5);
  return {titulo: document.title, url_final: location.href, botoes: botoes.slice(0, 40),
          texto_da_pagina: (document.body.innerText || '').replace(/\s+/g, ' ').slice(0, 1500),
          textos: textos.slice(0, 12), sobreposicoes: fixos, links_app_store: lojas,
          fontes_carregadas: [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family)};
}
