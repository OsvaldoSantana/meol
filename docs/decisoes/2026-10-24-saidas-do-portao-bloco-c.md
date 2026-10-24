# As saídas do portão do bloco C (P-64)

**Data:** 24/10/2026 · **Autor:** Claude, como arquiteto (fecha o desenho da P-64) · **Não é decisão
dele.** Ele decide os cortes (27c); isto é a forma do que o portão devolve. Se discordar, a mudança
é no `politica.yaml → bloco_C_solvencia.saidas_do_portao`, não no código.

## O que se decide

O portão do bloco C devolve uma de **cinco** saídas por empresa. Antes eram duas (passa e reprova,
implícitas no texto de 05/09), e o regime de banco só existia como prosa.

| saída | quando | o que carrega |
|---|---|---|
| `APROVA` | passou em todo corte ativo | os valores medidos |
| `REPROVA` | um corte ativo falhou | **o código do corte, o valor medido, o corte escolhido e o N do universo.** Só existe com limiar gravado |
| `MARCA` | sinal sem veto: corte sem limiar, tendência em `AGUARDA_SERIE`, "C-04 não medido", empresa sem dado (P-16b) | a causa, e o valor quando ele existe |
| `RECUSA_REGIME` | instituição financeira ou seguradora | o motivo e o destino (`regime_instituicao_financeira`, P-31). **Nenhum número** |
| `EXIGE_DOSSIE` | regime sem dado estruturado, ou que o cadastro não identifica | o motivo. A empresa fica no universo, sem peso deste bloco |

**Invariante: só `REPROVA` tira empresa do universo.** Ausência de dado, de regime ou de limiar
nunca é critério de exclusão (P6). Está no YAML (`tiram_do_universo: [REPROVA]`) e no teste
(`test_b_*`). Na empresa, a saída mais severa vence, nesta ordem: `RECUSA_REGIME`, `EXIGE_DOSSIE`,
`REPROVA`, `MARCA`, `APROVA`.

## Consequência que o desenho já assume

Com a tendência sempre em `AGUARDA_SERIE` e o C-04 sempre "não medido", **nenhuma empresa chega a
`APROVA` hoje**: o melhor resultado é `MARCA`. É o que a 63a (o nível corta, a tendência marca) e o
`empresa_sem_dado` pedem, dito em voz alta. `APROVA` passa a existir quando a série e a P-65
existirem.

## Alternativas rejeitadas

1. **O booleano passa/reprova.** É o modo de falha do F-02: o banco devolveria um número (a conta
   `3.05` de banco é "Resultado antes dos Tributos", medido no DFP 2024 real: 17 de 467 emissores
   trazem outro plano de contas) e o número entraria como lixo plausível. Sem uma saída que diga
   "não se aplica", a única opção é calcular.
2. **A pontuação** (somar C-01 a C-05 numa nota). Fere a P3 (portões, não pontuação) e o
   `permite_score: false` do `politica.yaml`; esconderia qual corte tirou a empresa e o custo de
   discordar.
3. **`MARCA` e `EXIGE_DOSSIE` numa saída só.** Perderia a distinção que a P-64 pede: `MARCA` é
   um sinal sobre um número que existe; `EXIGE_DOSSIE` é a ausência de regime estruturado, e o
   consumidor dela é o dossiê (P-65).

## O que isto não resolve

Quais setores são `RECUSA_REGIME` e quais `EXIGE_DOSSIE` ao sair do cadastro é escolha de Claude
nas listas `setor_ativ.financeira` e `setor_ativ.a_decidir` (P-18); o regime delas é a P-31. A
holding genérica ("Emp. Adm. Participações", "Sem Setor Principal", 265 linhas) fica em `GERAL` e
é a escolha em aberto mais cara dessa lista.
