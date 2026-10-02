# -*- coding: utf-8 -*-
"""As guardas da pagina do teste de marca (S6, P-162).

  (ii)  o esquema SQL nao tem coluna de identificacao, e o anon so insere e abre;
  (iii) toda pagina tem noindex, nenhum recurso remoto, nenhum rastreador, nenhuma chave;
  (iv)  a duracao da exposicao vem do JSON, nunca de um literal no JS;
  (v)   no Chromium sem interface, a imagem esta visivel antes do tempo e fora depois;
  e a validacao da funcao de envio (node), e o percurso inteiro com o contador simulado.

O LIMITE DESTE INSTRUMENTO (5-B). A (ii) le o TEXTO do esquema.sql; o comportamento no banco e
o do teste_politicas.sql, que roda no Supabase (roteiro dele) -- e que a S6 rodou num Postgres
18.3 em WebAssembly (PGlite), fora do CI. O node e o Chromium sao exigidos no CI: la, a falta
de um deles reprova, para a guarda nao passar calada; fora do CI, pula.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys

import pytest

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import codigos_visuais as V  # noqa: E402  (a luminancia da WCAG, uma so)
import questionario_json as G  # noqa: E402
import servir_pesquisa as S  # noqa: E402

PESQUISA = G.PESQUISA
Q = G.ler_yaml()
ENVIO = G.colunas_de_envio(Q)


def _ler(*partes: str) -> str:
    with open(os.path.join(PESQUISA, *partes), encoding="utf-8") as f:
        return f.read()


def _arquivos(*exts: str) -> list[str]:
    out = []
    for base, _dirs, arqs in os.walk(PESQUISA):
        out += [os.path.join(base, a) for a in arqs if a.endswith(exts)]
    return sorted(out)


def _exigir(binario: str | None, nome: str) -> str:
    if binario:
        return binario
    if os.environ.get("GITHUB_ACTIONS") == "true":
        pytest.fail(f"{nome} ausente no CI: esta guarda nao pode passar calada")
    pytest.skip(f"{nome} ausente nesta maquina")
    raise AssertionError  # inalcancavel; o pytest.skip levanta


# ------------------------------------------------------------------ (ii) o esquema ------

PROIBIDO_NOME = re.compile(
    r"(^|_)(ip|ips|inet|user_agent|agente|navegador|nome|email|e_mail|telefone|celular|cpf|rg|"
    r"endereco|cep|cidade|latitude|longitude|geo|hora|horario|criado_em|timestamp)($|_)")
PROIBIDO_TIPO = {"inet", "cidr", "macaddr", "macaddr8", "timestamp", "timestamptz", "time",
                 "timetz", "interval"}
GRANT = re.compile(r"grant\s+(?P<priv>\w+)(?:\s*\((?P<cols>[^)]*)\))?\s+on\s+(?P<tipo>table|"
                   r"function)\s+(?P<obj>[\w.]+(?:\(\))?)\s+to\s+(?P<papeis>[\w, ]+);", re.I)


def auditar_esquema(sql: str) -> list[str]:
    """Os problemas do esquema (lista vazia = o anon so insere e abre, e nada identifica)."""
    probs = []
    tabelas = re.findall(r"create table (public\.\w+) \((.*?)\n\);", sql, re.S)
    if not tabelas:
        probs.append("nenhuma tabela")
    for nome, corpo in tabelas:
        for linha in corpo.splitlines():
            m = re.match(r"\s+(\w+)\s+(\w+)", linha)
            if not m or m.group(1) in ("constraint", "check", "case", "when", "else", "end"):
                continue
            col, tipo = m.group(1).lower(), m.group(2).lower()
            if PROIBIDO_NOME.search(col):
                probs.append(f"coluna de identificacao ou hora: {nome}.{col}")
            if tipo in PROIBIDO_TIPO:
                probs.append(f"tipo proibido: {nome}.{col} {tipo}")
        if f"alter table {nome} enable row level security;" not in sql:
            probs.append(f"sem RLS: {nome}")
        if not re.search(rf"revoke all on table {re.escape(nome)} from public, anon, "
                         r"authenticated;", sql):
            probs.append(f"sem revoke: {nome}")
    grants = [m.groupdict() for m in GRANT.finditer(sql)]
    esperado = {("insert", "table", "public.respostas", "anon"),
                ("execute", "function", "public.abrir_resposta()", "anon")}
    achados = {(g["priv"].lower(), g["tipo"].lower(), g["obj"], g["papeis"].strip())
               for g in grants}
    if achados != esperado or len(grants) != len(esperado):
        probs.append(f"grants diferentes de insert+execute para o anon: {sorted(achados)}")
    for g in grants:
        if g["priv"].lower() == "insert":
            cols = [c.strip() for c in (g["cols"] or "").split(",") if c.strip()]
            if cols != ENVIO:
                probs.append("insert do anon fora das colunas do envio (ou sem lista)")
    if re.search(r"grant\s+all", sql, re.I):
        probs.append("grant all")
    politicas = re.findall(r"create policy \w+ on ([\w.]+)\s+for (\w+)\s+to (\w+)", sql)
    if politicas != [("public.respostas", "insert", "anon")]:
        probs.append(f"politicas alem do insert do anon: {politicas}")
    if "security definer" not in sql or "set search_path = ''" not in sql:
        probs.append("a funcao do contador sem security definer ou sem search_path vazio")
    m = re.search(r"%\s*(\d+)\)", sql)
    if not m or int(m.group(1)) != len(Q["ordens"]["versoes"]):
        probs.append("o mod do contador nao e o numero de versoes do questionario")
    return probs


def test_ii_o_esquema_so_deixa_o_anon_inserir_e_abrir():
    assert auditar_esquema(_ler("supabase", "esquema.sql")) == []


@pytest.mark.parametrize("mutacao", [
    ("  aberta_em date", "  ip_origem inet,\n  aberta_em date"),
    ("  aberta_em date not null", "  aberta_em timestamptz not null"),
    ("grant execute on function public.abrir_resposta() to anon;",
     "grant execute on function public.abrir_resposta() to anon;\n"
     "grant select on table public.respostas to anon;"),
    ("grant insert (id_resposta,", "grant insert (concluida_em, id_resposta,"),
    ("alter table public.respostas enable row level security;\n", ""),
    ("for insert to anon with check (true);", "for insert to anon with check (true);\n"
     "create policy anon_le on public.respostas for select to anon using (true);"),
    ("security definer\n", ""),
])
def test_ii_mutacao_cada_brecha_reprova(mutacao):
    sql = _ler("supabase", "esquema.sql")
    antes, depois = mutacao
    assert antes in sql, antes
    assert auditar_esquema(sql.replace(antes, depois, 1)) != []


def test_ii_teste_de_politica_cobre_leitura_alteracao_e_data():
    t = _ler("supabase", "teste_politicas.sql")
    assert "set local role anon;" in t and t.rstrip().endswith("rollback;")
    for tabela in ("public.respostas", "public.aberturas", "public.contador_de_aberturas"):
        assert f"perform 1 from {tabela}" in t, tabela
    for prova in ("update public.respostas", "delete from public.respostas", "concluida_em",
                  "insert into public.aberturas", "foreign_key_violation"):
        assert prova in t, prova


# ------------------------------------------- (iii) noindex, nada remoto, nada de chave ---

RASTREADORES = re.compile(
    r"google-analytics|googletagmanager|gtag\(|facebook|fbq\(|hotjar|segment\.(io|com)|"
    r"mixpanel|plausible|clarity\.ms|_vercel/insights|speed-insights|@vercel/analytics|"
    r"doubleclick|matomo|document\.cookie", re.I)
REMOTO = re.compile(r"(?<![\w:])(?:https?:)?//[a-z0-9-]+\.[a-z]", re.I)
CHAVE = re.compile(r"eyJ[A-Za-z0-9_-]{10,}\.|\.supabase\.co|"
                   r"sb_(?:publishable|secret)_[A-Za-z0-9_-]{8,}")


def test_iii_toda_pagina_tem_noindex():
    htmls = _arquivos(".html")
    assert htmls
    for h in htmls:
        with open(h, encoding="utf-8") as f:
            assert re.search(r'<meta name="robots" content="noindex', f.read()), h
    v = json.loads(_ler("vercel.json"))
    todas = [r for r in v["headers"] if r["source"] == "/(.*)"]
    assert any(h["key"] == "X-Robots-Tag" and h["value"].startswith("noindex")
               for r in todas for h in r["headers"])


def test_iii_nenhum_recurso_remoto_nenhum_rastreador_nenhuma_chave():
    for p in _arquivos(".html", ".css", ".js", ".json"):
        with open(p, encoding="utf-8") as f:
            t = f.read()
        rel = os.path.relpath(p, PESQUISA)
        assert not REMOTO.search(t), f"recurso remoto em {rel}: {REMOTO.search(t)}"
        assert not RASTREADORES.search(t), f"rastreador em {rel}"
        assert not CHAVE.search(t), f"chave ou URL do Supabase em {rel}"
    html = _ler("index.html")
    assert re.findall(r"<script[^>]*>", html) == ['<script src="app.js" defer>']
    assert re.findall(r'<link[^>]*>', html) == ['<link rel="stylesheet" href="estilo.css">']


def test_iii_mutacao_recurso_remoto_e_rastreador_sao_pegos():
    assert REMOTO.search('<script src="https://cdn.exemplo.com/x.js"></script>')
    assert REMOTO.search("url(//fonts.exemplo.com/f.woff2)")
    assert not REMOTO.search("// comentario de codigo, nao URL")
    assert RASTREADORES.search("window.gtag('config')")
    assert CHAVE.search("SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6.x")
    assert CHAVE.search("sb_publishable_AbC123xyz_890")
    assert not CHAVE.search("// a publicavel (sb_publishable_...) vai no apikey")


def test_iii_a_chave_so_vem_do_ambiente():
    c = _ler("api", "_comum.js")
    assert "process.env.SUPABASE_URL" in c and "process.env.SUPABASE_ANON_KEY" in c
    for p in _arquivos(".js"):
        with open(p, encoding="utf-8") as f:
            assert "console." not in f.read(), f"log em {os.path.relpath(p, PESQUISA)}"


# ------------------------------------------------- (iv) a duracao vem do JSON ------------

def auditar_app(js: str, segundos: float) -> list[str]:
    probs = []
    if not re.search(r"setTimeout\([\s\S]*?exposicao_segundos\s*\*\s*1000\s*\)", js):
        probs.append("a exposicao nao usa telas.exposicao_segundos do JSON")
    for m in re.finditer(r"setTimeout\(", js):
        trecho = js[m.end():m.end() + 400]
        prof, fim = 1, None
        for i, ch in enumerate(trecho):
            prof += ch == "("
            prof -= ch == ")"
            if prof == 0:
                fim = i
                break
        if fim is not None and re.search(r",\s*[\d_.]+\s*$", trecho[:fim]):
            probs.append("setTimeout com espera literal")
    ms = int(segundos * 1000)
    if re.search(rf"(?<![\w.]){ms}(?![\w.])|(?<![\w.]){ms // 1000}e3(?![\w.])", js):
        probs.append(f"o valor da exposicao ({ms} ms) aparece como literal")
    return probs


def test_iv_a_duracao_da_exposicao_vem_do_json():
    assert auditar_app(_ler("app.js"), Q["telas"]["exposicao_segundos"]) == []


@pytest.mark.parametrize("troca", ["5000", "Q_SEGUNDOS * 1000", "4999"])
def test_iv_mutacao_literal_no_lugar_do_json_reprova(troca):
    js = _ler("app.js").replace("q.telas.exposicao_segundos * 1000", troca)
    assert auditar_app(js, Q["telas"]["exposicao_segundos"]) != []


def test_iv_nenhum_texto_de_pergunta_no_codigo():
    """A pagina nunca tem texto de pergunta escrito a mao: tudo vem do questionario.json."""
    t = Q["telas"]
    textos = [Q["consentimento"]["texto"], Q["filtro"]["texto"], Q["amigo"]["texto"],
              t["instrucao"], t["instrucao_curta"], t["lembranca"]["texto"],
              t["cabeca_das_escalas"], t["botao_ver"], Q["pronuncia"]["texto"],
              *Q["final"].values()]
    textos += [e[k] for e in t["escalas"] for k in ("pergunta", "polo_1", "polo_7")]
    codigo = _ler("app.js") + _ler("index.html")
    for txt in textos:
        assert txt[:20] not in codigo, txt


# --------------------------------------------- acessibilidade (RI-22, RI-23, RI-31) ----

def test_contraste_e_alvo_da_pagina_neutra():
    css = _ler("estilo.css")
    cor = dict(re.findall(r"--(\w[\w-]*):\s*(#[0-9a-fA-F]{6});", css))

    def razao(a: str, b: str) -> float:
        la, lb = sorted((V.luminancia(cor[a]), V.luminancia(cor[b])), reverse=True)
        return (la + 0.05) / (lb + 0.05)
    assert razao("texto", "fundo") >= 4.5 and razao("texto-2", "fundo") >= 4.5   # RI-22
    assert razao("borda", "fundo") >= 3.0                                          # RI-23
    alturas = [int(x) for x in re.findall(r"min-height:\s*(\d+)px", css)]
    assert alturas and min(alturas) >= 24                                          # RI-31
    assert "minmax(24px" in css
    assert ":focus-visible" in css                                                 # RI-29


# ------------------------------------------- a validacao da funcao de envio (node) -----

NODE = shutil.which("node")


def _validar(casos: list[dict]) -> list[str | None]:
    node = _exigir(NODE, "node")
    js = ("const {validar} = require(process.argv[1]);"
          "const casos = JSON.parse(require('fs').readFileSync(0, 'utf8'));"
          "process.stdout.write(JSON.stringify(casos.map(validar)));")
    r = subprocess.run([node, "-e", js, os.path.join(PESQUISA, "api", "_comum.js")],
                       input=json.dumps(casos), capture_output=True, text=True, timeout=60,
                       check=True)
    out: list[str | None] = json.loads(r.stdout)
    return out


def _completa() -> dict:
    with open(G.JSON, encoding="utf-8") as f:
        sha = json.load(f)["questionario_sha256"]
    d: dict = {"id_resposta": "0b6b2f5e-1c2d-4e5f-8a9b-0c1d2e3f4a5b",
               "questionario_sha256": sha, "consentimento": "sim", "filtro": "sim",
               "amigo": "nao", "pronuncia": "me-ol"}
    for c in ENVIO:
        if re.fullmatch(r"t\d+_\w+", c) and not c.endswith("_" + Q["telas"]["lembranca"]["id"]):
            d[c] = 4
    return d


def test_validacao_do_envio_segue_o_questionario():
    ok = _completa()
    sem_nota = dict(ok)
    sem_nota.pop("t6_luxo")
    casos = [
        ok,
        {k: ok[k] for k in ("id_resposta", "questionario_sha256")} | {"consentimento": "nao"},
        {k: ok[k] for k in ("id_resposta", "questionario_sha256", "consentimento")}
        | {"filtro": "nao"},
        sem_nota,
        dict(ok, t3_honesto=8),
        dict(ok, t3_honesto="4"),
        dict(ok, ip="1.2.3.4"),
        dict(ok, concluida_em="2026-10-02"),
        dict(ok, questionario_sha256="0" * 64),
        dict(ok, id_resposta="nao-e-uuid"),
        {k: ok[k] for k in ("id_resposta", "questionario_sha256")}
        | {"consentimento": "nao", "filtro": "sim"},
        dict(ok, t1_lembra="x" * 2001),
    ]
    r = _validar(casos)
    assert r[:3] == [None, None, None], r
    assert all(m is not None for m in r[3:]), r


FUNCOES = r"""
const path = require('path');
const api = process.argv[1];
const chamadas = [];
global.fetch = async (url, op) => {
  chamadas.push({ url, metodo: op.method, cab: op.headers, corpo: JSON.parse(op.body) });
  if (url.endsWith('/rpc/abrir_resposta')) {
    return { ok: true, status: 200, json: async () => ({ id_resposta: 'x', versao: 3 }) };
  }
  return { ok: true, status: 201, json: async () => null };
};
function res() {
  const r = { codigo: null, cab: {}, corpo: null };
  r.status = (c) => { r.codigo = c; return r; };
  r.json = (d) => { r.corpo = d; return r; };
  r.end = () => r;
  r.setHeader = (k, v) => { r.cab[k] = v; };
  return r;
}
(async () => {
  const entrada = JSON.parse(require('fs').readFileSync(0, 'utf8'));
  const out = [];
  for (const caso of entrada) {
    process.env.SUPABASE_URL = 'http://banco.invalido';
    process.env.SUPABASE_ANON_KEY = caso.chave;
    chamadas.length = 0;
    const h = require(path.join(api, caso.funcao + '.js'));
    const r = res();
    await h({ method: caso.metodo, headers: { 'x-forwarded-for': '9.9.9.9',
      'user-agent': 'Navegador', 'content-length': '10' }, body: caso.corpo }, r);
    out.push({ codigo: r.codigo, corpo: r.corpo, chamadas: chamadas.slice() });
  }
  process.stdout.write(JSON.stringify(out));
})();
"""


def _funcoes(casos: list[dict]) -> list[dict]:
    node = _exigir(NODE, "node")
    r = subprocess.run([node, "-e", FUNCOES, os.path.join(PESQUISA, "api")],
                       input=json.dumps(casos), capture_output=True, text=True, timeout=60,
                       check=True)
    out: list[dict] = json.loads(r.stdout)
    return out


def test_funcoes_da_vercel_com_o_banco_simulado():
    ok = _completa()
    r = _funcoes([
        {"funcao": "abrir", "metodo": "POST", "chave": "sb_publishable_teste", "corpo": {}},
        {"funcao": "abrir", "metodo": "POST", "chave": "eyJlegado.x.y", "corpo": {}},
        {"funcao": "abrir", "metodo": "GET", "chave": "sb_publishable_teste", "corpo": None},
        {"funcao": "enviar", "metodo": "POST", "chave": "sb_publishable_teste", "corpo": ok},
        {"funcao": "enviar", "metodo": "POST", "chave": "sb_publishable_teste",
         "corpo": dict(ok, ip="1.2.3.4")},
    ])
    abrir_novo, abrir_legado, abrir_get, enviar_ok, enviar_ruim = r
    assert abrir_novo["codigo"] == 200 and abrir_novo["corpo"] == {"id_resposta": "x",
                                                                    "versao": 3}
    cab = abrir_novo["chamadas"][0]["cab"]
    assert cab["apikey"] == "sb_publishable_teste" and "Authorization" not in cab
    assert abrir_legado["chamadas"][0]["cab"]["Authorization"] == "Bearer eyJlegado.x.y"
    assert abrir_get["codigo"] == 405 and abrir_get["chamadas"] == []
    assert enviar_ok["codigo"] == 204
    c = enviar_ok["chamadas"][0]
    assert c["url"] == "http://banco.invalido/rest/v1/respostas" and c["metodo"] == "POST"
    assert c["corpo"] == ok
    for chamada in abrir_novo["chamadas"] + enviar_ok["chamadas"]:
        nomes = {k.lower() for k in chamada["cab"]}
        assert not nomes & {"x-forwarded-for", "user-agent", "x-real-ip"}, nomes
    assert enviar_ruim["codigo"] == 400 and enviar_ruim["chamadas"] == []


# ---------------------------------------- (v) o Chromium sem interface, de verdade -----

def _chrome() -> str | None:
    for nome in (os.environ.get("CHROME_BIN"), "google-chrome", "google-chrome-stable",
                 "chromium", "chromium-browser"):
        if nome and shutil.which(nome):
            return shutil.which(nome)
    for p in (r"C:\Program Files\Google\Chrome\Application\chrome.exe",
              r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"):
        if os.path.isfile(p):
            return p
    return None


AUTO_EXPOR = """(function () {
  function passo() {
    var b = document.querySelector('.acoes button');
    if (b && !window.__visto) {
      if (b.textContent === %(ver)s) {
        window.__visto = 1;
        document.documentElement.setAttribute('data-visto-em', String(performance.now()));
      }
      b.click();
    }
    setTimeout(passo, 100);
  }
  setTimeout(passo, 100);
}());"""

AUTO_COMPLETO = """(function () {
  function passo() {
    var fs = document.querySelectorAll('fieldset');
    fs.forEach(function (f) {
      if (!f.querySelector('input:checked')) f.querySelector('input[value="4"]').click();
    });
    var t = document.querySelector('textarea');
    if (t && !t.value) t.value = 'algo';
    var b = document.querySelector('.acoes button');
    if (b) b.click();
    setTimeout(passo, 200);
  }
  setTimeout(passo, 200);
}());"""


def _dom(sim: S.Simulador, orcamento_ms: int, perfil: str) -> str:
    chrome = _exigir(_chrome(), "Chromium/Chrome")
    httpd, url = S.servir(sim)
    try:
        r = subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-sandbox",
                            "--no-first-run", "--no-default-browser-check",
                            "--disable-extensions", f"--user-data-dir={perfil}",
                            f"--virtual-time-budget={orcamento_ms}", "--dump-dom", url],
                           capture_output=True, text=True, encoding="utf-8", timeout=180)
    finally:
        httpd.shutdown()
    return r.stdout


def _exposicao(dom: str) -> tuple[float, bool, int]:
    """(quando a tela comecou, em ms virtuais; a imagem esta visivel?; quantas escalas)."""
    m = re.search(r'data-visto-em="([\d.]+)"', dom)
    assert m, "a automacao nao chegou ao botao de ver a tela"
    img = re.search(r'<img[^>]*id="estimulo"[^>]*>', dom)
    return float(m.group(1)), bool(img and "hidden" not in img.group(0)), dom.count("<fieldset")


def _sim_expor(**kw) -> S.Simulador:
    return S.Simulador(script_injetado=AUTO_EXPOR % {"ver": json.dumps(Q["telas"]["botao_ver"])},
                       **kw)


def test_v_imagem_visivel_antes_do_tempo_e_fora_depois(tmp_path):
    seg = Q["telas"]["exposicao_segundos"]
    antes = 2500
    inicio, visivel, escalas = _exposicao(_dom(_sim_expor(), antes, str(tmp_path / "a")))
    assert antes - inicio < seg * 1000 - 500, "pre-condicao: medir antes do fim"
    assert visivel and escalas == 0
    depois = int(seg * 1000 + 3000)
    inicio, visivel, escalas = _exposicao(_dom(_sim_expor(), depois, str(tmp_path / "b")))
    assert depois - inicio > seg * 1000 + 500
    assert not visivel and escalas == len(Q["telas"]["escalas"])


def test_v_a_duracao_obedece_ao_json_servido(tmp_path):
    """(iv) no navegador: com 2 s no JSON, a imagem ja saiu aos 3,5 s; com o do questionario,
    ainda esta la. Se a duracao fosse literal no JS, os dois dariam o mesmo."""
    curto, visivel_curto, _ = _exposicao(_dom(_sim_expor(exposicao_segundos=2), 3500,
                                              str(tmp_path / "c")))
    real, visivel_real, _ = _exposicao(_dom(_sim_expor(), 3500, str(tmp_path / "e")))
    assert 3500 - curto > 2500 and 3500 - real < Q["telas"]["exposicao_segundos"] * 1000 - 500
    assert not visivel_curto and visivel_real


def test_v_a_versao_vem_do_contador(tmp_path):
    """Contador em 2 -> versao 3 -> a primeira tela e a primeira direcao da ordem 3, na base."""
    sim = _sim_expor()
    sim.contador = 2
    dom = _dom(sim, 2500, str(tmp_path / "f"))
    primeira = Q["ordens"]["versoes"][3][0]
    assert f'src="estimulos/{primeira}-base.png"' in dom


def test_v_sem_contador_a_pagina_para_e_nao_sorteia(tmp_path):
    """P1: se /api/abrir falha, a pagina diz que falhou e nao mostra pergunta nenhuma."""
    with open(G.INTERFACE, encoding="utf-8") as f:
        falha = json.load(f)["falha_ao_abrir"]
    dom = _dom(_sim_expor(abrir_falha=True), 3000, str(tmp_path / "g"))
    assert falha[:30] in dom
    assert Q["consentimento"]["texto"][:30] not in dom and "<button" not in dom


def test_v_percurso_inteiro_com_o_contador_simulado(tmp_path):
    """A pagina roda sobre o JSON: abre, passa pelas seis telas e envia UM corpo que a
    validacao da funcao de envio aceita, com as colunas do envio e nada mais."""
    sim = S.Simulador(script_injetado=AUTO_COMPLETO)
    orcamento = int(Q["telas"]["quantidade"] * (Q["telas"]["exposicao_segundos"] + 2) * 1000)
    dom = _dom(sim, orcamento + 10_000, str(tmp_path / "h"))
    assert Q["final"]["concluiu"][:30] in dom
    assert len(sim.aberturas) == 1 and len(sim.envios) == 1
    corpo = sim.envios[0]
    assert corpo["id_resposta"] == sim.aberturas[0]["id_resposta"]
    assert set(corpo) == set(ENVIO)
    assert _validar([corpo]) == [None]
