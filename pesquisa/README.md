# A página do teste de marca (S6, P-162)

*02/10/2026. A página que executa o questionário **pré-registrado** na S5
([`docs/marca/teste-de-marca/preregistro-final.md`](../docs/marca/teste-de-marca/preregistro-final.md)).
Nada aqui foi publicado: o deploy e as contas são dele (roteiro em `PENDENCIAS.md`, "Ao voltar ao
desktop"). Nenhuma resposta real existe.*

## O que é cada arquivo

| arquivo | o que é | quem escreve |
|---|---|---|
| `index.html`, `estilo.css`, `app.js` | a página: HTML, CSS e JS sem framework, sem recurso remoto, visualmente neutra (preto, branco, cinza, fonte do sistema) para não interferir na nota das direções | à mão |
| `questionario.json` | o questionário, com o sha256 do `questionario.yaml` (vai em cada resposta) | **gerado** por `tools/questionario_json.py` |
| `estimulos/*.png` | cópias byte a byte dos seis PNG aprovados (a Vercel só serve o que está nesta pasta) | **gerado** |
| `interface.json` | textos de botão, aviso e erro, e os limites dos campos abertos. **Não são perguntas e não estão no pré-registro** | à mão |
| `api/abrir.js`, `api/enviar.js`, `api/_comum.js` | as duas funções da Vercel e o que elas dividem (validação, chamada ao Supabase) | à mão |
| `supabase/esquema.sql` | tabelas, RLS e permissões | **gerado** |
| `supabase/exportar.sql` | a consulta que produz o `respostas.csv` da análise, com as colunas do contrato | **gerado** |
| `supabase/teste_politicas.sql` | a prova, no banco, de que o anon não lê nada | à mão |
| `vercel.json` | cabeçalhos: `noindex`, política de conteúdo só da própria origem, sem referer | à mão |
| `.vercelignore` | tira este README e a pasta `supabase/` do ar (a URL da pesquisa serve só a página) | à mão |

```bash
py -3.11 tools/questionario_json.py             # gera o JSON, os PNG e o SQL do YAML
py -3.11 tools/questionario_json.py --conferir  # sai 1 se algum gerado divergir
py -3.11 tools/servir_pesquisa.py               # a página em http://127.0.0.1:8000/,
                                                # com o contador e o envio SIMULADOS em memória
```

## Como funciona

1. **Abertura.** Ao abrir, a página chama `POST /api/abrir`. A função chama
   `public.abrir_resposta()` no Supabase, que soma 1 ao contador, grava a abertura (versão e
   dia) e devolve o id e a versão: `versão = (contador mod 6) + 1` (g-B revista, ab-a). **Se
   falhar, a página para e diz que falhou: não sorteia no lugar** (P1).
2. **As telas**, na ordem do questionário: consentimento, filtro, amigos, e as seis telas da
   ordem da versão (três bases e as mesmas três com a rota bloqueada). Cada imagem aparece ao
   toque em "Ver a tela", fica `telas.exposicao_segundos` segundos (lido do JSON), **sai do
   documento** e não volta.
3. **Um envio só**, no fim, por `POST /api/enviar`. A função valida o corpo contra o
   questionário e insere com a chave do papel `anon`. Quem sai pelo consentimento ou pelo filtro
   envia só a resposta que o tirou.

## Onde o prompt da S6 e o contrato congelado divergiam, e o que valeu

O questionário é pré-registrado: mudar o contrato seria pré-registro novo. Valeu o contrato.

| o prompt da S6 dizia | o contrato (questionario.yaml) diz | o que a página faz |
|---|---|---|
| guardar "horário" | "a tabela não tem IP, nome, e-mail, user agent **nem hora**"; datas "SÓ O DIA" | só o dia (`date`), em Brasília, posto pelo banco |
| a página pede a versão "por uma função do banco" | "o navegador **nunca** chama o Supabase" | a página chama `/api/abrir` (Vercel), que chama a função do banco |
| a função do contador "só incrementa e devolve o mod 6" | "uma linha por **abertura**" (ab-a), com a versão e o dia | a função também grava a linha da abertura; o anon continua sem inserir em `aberturas` |
| o sha256 do questionário "em cada resposta" | a exportação tem colunas fixas, e a análise recusa coluna a mais | o sha256 fica na tabela; `exportar.sql` não o traz e tem a consulta de conferência |

## O que fica declarado (P5)

- **A marca no aparelho só avisa.** Depois de um envio, a página grava no `localStorage` que
  este aparelho já enviou; ao reabrir, mostra "este aparelho já enviou" e **deixa seguir**.
  Não bloqueia: aparelho compartilhado é legítimo, e a marca some com a limpeza do navegador
  ou em outro aparelho. Resposta duplicada continua não detectável (limitação 17 do
  pré-registro). Não é cookie e não vai para o servidor.
- **Os textos de interface** (`interface.json`) não estão no pré-registro. São neutros e sem
  promessa de produto (P-158); mudar um deles antes do convite é ajuste de instrumento, não
  de questionário.
- **O teste é visual.** A imagem tem um texto alternativo genérico; quem não enxerga a tela não
  consegue dar a nota sobre ela. As perguntas, os botões e as escalas funcionam por teclado e
  leitor de tela.
- **A exposição conta tempo de tela, não de atenção** (limitação 19): o relógio corre mesmo com
  a aba em segundo plano.
- **A conta gratuita da Vercel (Hobby) é para uso pessoal, não comercial** (lido em
  02/10/2026, `vercel.com/docs/limits/fair-use-guidelines`). A página não cobra, não anuncia
  e não vende, mas testa a marca de um produto possível. Se isso é uso comercial é decisão
  dele (passo 0 do roteiro).
- **Acessibilidade (RI-22 a RI-34): o que foi verificado e o que não.** Por teste:
  - contraste das quatro cores (RI-22 e RI-23);
  - alvo mínimo de 24 px (RI-31; a página usa 44);
  - foco visível (RI-29).

  **Por desenho, sem teste:** o escolhido na escala não se marca só pela cor (RI-24): fundo
  invertido, borda e negrito.

  **Não verificado**:
  - o percurso automático por Tab (RI-29 e RI-30 dinâmicos);
  - o axe;
  - o zoom de 200% (RI-25);
  - 320 px sem rolagem lateral (RI-26), que o desenho permite (grade de 7 com mínimo de
    24 px), mas nenhum teste mede.

  RI-32 a RI-34 não se aplicam: não há canal de ajuda, cadastro nem login.
- **O banco foi testado fora do CI.** O `esquema.sql` e o `teste_politicas.sql` rodaram em
  02/10/2026 num Postgres 18.3 em WebAssembly (PGlite 0.5.8), com os privilégios padrão do
  Supabase imitados. Resultado: as 11 provas passaram; com um `grant select` a mais para o
  anon, o teste parou em "FALHA: o anon leu public.respostas". O CI confere o texto do
  esquema (`tools/test_pesquisa.py`), não um banco.
