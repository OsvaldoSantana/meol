# Contexto de sessão — o que toda sessão lê, antes e depois de cada corte

*Medido por `python auditoria/tamanho_do_contexto.py` (razão de 2,96 caracteres por token, sem
`tiktoken`; ±15%, e o erro é o mesmo nas duas pontas, então a diferença vale mais que o valor
absoluto). O que é `SEMPRE` é declarado no próprio instrumento. Nenhum destes números é copiado
para o `CLAUDE.md`.*

## 03/10/2026, à noite — a dieta completa: `PLANO.md` curto, pendências em ativas e reserva

Decisão dele, 03/10 (fila, "Decisões dele, 03/10/2026, depois da P-115"). O `PENDENCIAS.md`
volta à abertura **só com as ativas** (teto 20, lidas inteiras), o resto aberto vai para
`docs/pendencias-reserva.md` (por busca), e o `docs/estado.md` passa a levar só códigos.

| arquivo | antes (linhas / tokens) | depois (linhas / tokens) | diferença |
|---|---|---|---|
| `CLAUDE.md` | 436 / 8.924 | 437 / 8.957 | +33 (o §1 diz como ler as duas listas) |
| `PLANO.md` | 411 / 8.850 | 123 / 2.802 | **−6.048** |
| `PENDENCIAS.md` (16 ativas, inteiras) | fora da abertura | 263 / 5.376 | +5.376 |
| `docs/estado.md` | 101 / 1.892 | 19 / 339 | −1.553 |
| `docs/doutrinas.md` | 185 / 3.478 | 185 / 3.478 | 0 |
| **leitura de sessão** | **1.133 / 23.144** | **1.027 / 20.952** | **−2.192 (−9,5%)** |

Antes: `origin/main` em `b6b7f80` (com a #60). Depois: o commit que trouxe esta seção.

**A triagem, das 86 abertas em `82600e2`:** 14 ficaram ativas, 60 foram para a reserva e 12
fecharam com a evidência (`docs/historico/pendencias-fechadas.md`: P-08, P-09, P-44, P-46, P-63,
P-67, P-82, P-98, P-103, P-136, P-137, P-171). Duas novas entraram ativas (P-180, P-181): **76
abertas**, 16 ativas. No mesmo dia a #60 fechou a P-164 e abriu a P-179, que entrou ativa no
lugar dela (frente "primeiro uso"): seguem 76 e 16. As 24 sem dono, gatilho ou classe (P-171) ganharam os três ou fecharam; a
guarda é `auditoria/test_plano_e_pendencias.py`.

**Para onde foi o texto** (movido, não apagado): o `PLANO.md` anterior, inteiro, em
`docs/historico/plano-ate-2026-10-03.md`; o texto integral das ativas e a seção "Ao voltar ao
desktop" como estava, em `docs/historico/pendencias-ativas-ate-2026-10-03.md`; o roteiro da página
do teste de marca, em `docs/marca/teste-de-marca/roteiro-no-ar.md`. `auditoria/codigos_preservados.py`:
**408 códigos, 0 sumidos** da linha de base.

**O que estes números não são (P5):**

- **O "antes" não somava a seção da P da tarefa** (mediana de 318 tokens). Somada, a diferença
  é de ~2.500. O "depois" já tem as 16 ativas inteiras: não há seção a mais para ler.
- **O ganho é pequeno de propósito.** A sessão passou a ler o texto das ativas em vez de uma
  linha de 86; o corte veio do `PLANO.md`. O maior pedaço que sobrou é o `CLAUDE.md` (~9 mil),
  fora desta decisão.
- Mesma razão de 2,96 caracteres por token, sem `tiktoken` (±15%).

## 03/10/2026 — o `PENDENCIAS.md` sai da abertura, e entra o `docs/estado.md`

Decisão dele, 02/10 ([`docs/decisoes/modelos-por-tarefa.md`](../decisoes/modelos-por-tarefa.md)).

| arquivo | antes (linhas / tokens) | depois (linhas / tokens) | diferença |
|---|---|---|---|
| `CLAUDE.md` | 410 / 8.170 | 427 / 8.658 | +488 (as quatro regras novas) |
| `PENDENCIAS.md` | 2.044 / 40.364 | sai da abertura | **−40.364** |
| `docs/estado.md` (novo, injetado pelo hook) | — | 101 / 1.864 | +1.864 |
| `PLANO.md` | 410 / 8.779 | 410 / 8.779 | 0 |
| `docs/doutrinas.md` | 185 / 3.478 | 185 / 3.478 | 0 |
| **leitura de sessão** | **3.049 / 60.791** | **1.123 / 22.779** | **−38.012 (−62,5%)** |

Antes: `origin/main` em `ed5e0b5`. Depois: o commit que trouxe esta seção. O `estado.md` muda a
cada pendência: `python tools/estado.py --conferir` diz o tamanho do dia.

**Somado à leitura, e fora do instrumento:** a seção da P da tarefa. Nas 80 abertas de 03/10, a
mediana é **318 tokens**, o percentil 90 é **1.168** e a maior tem **2.197**. A abertura típica
fica em **~23.100**, a pior em **~25.000**: **−59% a −62%**.

**O que estes números não são (P5):**

- **Estimativa, não contagem do tokenizador do Claude.** Sem `tiktoken` nesta sessão, a razão é a
  de 19/09 (2,96 caracteres por token, ±15%); o erro é o mesmo nas duas pontas, e a diferença vale
  mais que o valor absoluto.
- **A releitura do `CLAUDE.md` não está no "antes".** Ele já chega no contexto pelo Claude Code; a
  instrução antiga ("leia inteiro") fazia a sessão pagá-lo de novo com a ferramenta de leitura,
  ~8 mil tokens a mais. O instrumento conta cada arquivo uma vez, então esse ganho não aparece na
  tabela e não está somado à diferença.
- **O variável continua sem medida** (P-103, item 2): resposta, saída de ferramenta, a suíte. O
  `tools/testar.py` corta a saída da rodada final para uma linha por suíte, e isso também não está
  na tabela.

## 26/09/2026 — a história saiu do `CLAUDE.md` e as fechadas saíram do `PENDENCIAS.md`

| arquivo | antes (linhas / tokens) | depois (linhas / tokens) | diferença |
|---|---|---|---|
| `CLAUDE.md` | 2.211 / 45.983 | 383 / 7.398 | **−38.585 (−83,9%)** |
| `PENDENCIAS.md` | 3.705 / 79.986 | 1.667 / 30.263 | **−49.723 (−62,2%)** |
| `PLANO.md` | 351 / 6.996 | 351 / 6.996 | 0 |
| `docs/doutrinas.md` | 185 / 3.478 | 185 / 3.478 | 0 |
| **leitura de sessão** | **6.452 / 136.443** | **2.586 / 48.135** | **−88.308 (−64,7%)** |

Antes: commit `c85ce59`. Depois: o commit que trouxe este arquivo.

**Para onde foi o texto** (movido, não apagado):

- `docs/historico/claude-md-ate-2026-09.md` — o `CLAUDE.md` de `c85ce59` **inteiro**, só com os
  links relativos reescritos para a pasta nova: as retratações, o índice de achados, as rodadas
  de 16 a 19/09, as §7, §10 e §11.
- `docs/historico/pendencias-fechadas.md` — os 54 blocos de pendência fechada (49 com o
  cabeçalho já riscado e 5 fechados só no corpo, riscados agora: P-69 a P-72, P-83, P-85, P-86,
  P-118), a tabela `## Fechadas`, os marcos auditáveis, o achado U-01 e as notas antigas de
  "Ao voltar ao desktop".

**Nada se perdeu, medido:** `auditoria/codigos_preservados.py` conta os códigos `LETRA-NUMERO`
e `5-B.n` em todo `.py`, `.md`, `.yaml` e `.yml`. Antes: **368 códigos, 4.374 ocorrências**.
Depois: **368 códigos, 4.415 ocorrências**, e nenhum código da linha de base sumiu. As
ocorrências sobem porque o `CLAUDE.md` novo cita códigos que o antigo também citava. A linha de
base (`auditoria/codigos_linha_de_base.txt`) só cresce; `test_codigos_preservados.py` reprova
se algum código sair do repositório, com prova por mutação e controle (mover não reprova).

**O que o corte não mede (P5):** se a sessão acha a regra de que precisa, agora que o porquê
está a um arquivo de distância. O `CLAUDE.md` vivo termina num índice (§13) que diz onde cada
pedaço da história foi morar, e as seções mantiveram a numeração antiga (§3, §5-A, §5-B, §8,
§9, §12) para que as citações espalhadas pelo código continuem apontando para o lugar certo.
