# O leitor as-of de DFP/ITR começa antes da P-145 (P-51, P-53)

*10/10/2026. **Decisão:** sessão de arquitetura de 10/10/2026, transmitida pelo Osvaldo no prompt
da sessão que a executou. **Registro, desenho do leitor e medições:** sessão do Claude Code na
nuvem, mesmo dia. O que é da decisão e o que é do desenho está separado abaixo.*

## A decisão

O passo 2 do caminho crítico (`PLANO.md` §3) começa **antes** da P-145. DFP e ITR são chaveados
por `CD_CVM`; a ponte ticker → `CD_CVM` só entra no join com o papel. O leitor nasce agora, com
os testes sobre **dado sintético**. A parte da P-53 que diz "a ponte também é bitemporal" espera
a P-145 e vira a **P-53b**.

## As alternativas

| | alternativa | por que não |
|---|---|---|
| A | **Esperar a P-145** e escrever o leitor depois da ponte | O leitor não usa a ponte: a pergunta dele é por `CD_CVM`. Esperar empilha dois passos que não dependem um do outro, e a P-145 espera um passo dele (o envio ao R2). |
| B | **Construir com dado real pelo `medir/`** | O `medir.yml` roda um script e commita a saída. Não é onde se desenvolve código com teste. E o teste do leitor tem de rodar em todo push, sem armazém: dado sintético roda; o acervo, não. |
| **C** | **Começar agora, sobre sintético** (a escolhida) | Os quatro testes pedidos são de **regra**, não de número: sintético os prova, e a forma do dado vem medida (abaixo). |

**Uma ressalva sobre a C, da sessão que a executou:** "sintético" vale para os **testes**. A
**forma** do sintético foi medida no dado real: o `itr_cia_aberta_2024.zip` público da CVM,
baixado em 10/10 para o scratchpad da sessão, fora do repositório, com o mesmo sha256
(`6158b55d…`) que o registro dá como vigente desde 04/10. Sem essa medição, três das armadilhas
abaixo teriam ficado de fora do desenho.

## A pergunta que o leitor responde

> Qual era o valor da CONTA para o CD_CVM no DT_REFER, sabendo só o que tinha sido capturado
> até a data D?

`fase0/leitor_cvm.py → valor(recurso, cd_cvm, dt_refer, cd_conta, demonstrativo, ate)`, e
`linhas(...)` para a série de um emissor dentro de uma partição. Três regras:

1. **Qual arquivo:** o do ano do `DT_REFER`, e só ele (P-51). O DFP de 2025 não é lido para
   2023, **nem depois de capturado**. A correção de 2023 entra quando o próprio
   `dfp_cia_aberta_2023` for regerado com a `VERSAO` nova. **Consequência declarada:** uma
   reapresentação que só apareça como comparativo de um ano posterior nunca alcança o ano
   corrigido. É o que a P-51 escolheu; o viés é "o número do próprio ano, na última versão
   capturada daquele arquivo".
2. **Qual versão do arquivo:** a última vigência do registro com instante ≤ D
   (`acervo.vigencias`). Data inclui o dia inteiro em UTC; instante sem fuso é recusado.
   Antes da primeira captura: `SemCaptura`, nunca a versão de hoje.
3. **Quais linhas:** só `ORDEM_EXERC = ÚLTIMO`.

E recusa em vez de adivinhar (P1): `PeriodoAmbiguo`, `ValorAmbiguo`, `EnumeracaoDesconhecida`,
`ContaAusente`, `MembroAusente`, `LimitacaoNaoDeclarada`.

## O que a medição de 10/10 mudou no desenho

Tudo medido no `itr_cia_aberta_2024.zip` (n = 1 arquivo) e no registro
`docs/acervo/cvm/capturas.csv`:

| medição | n | consequência no desenho |
|---|---|---|
| Na DRE consolidada, a chave (`CD_CVM`, `DT_REFER`, `CD_CONTA`) em `ÚLTIMO` repete | **32.901 de 48.907** chaves | trimestre e acumulado do ano, que só o `DT_INI_EXERC` separa. O leitor exige o período (`PeriodoAmbiguo`) |
| Na DMPL, a mesma chave repete mesmo com o período | **40.080 de 40.080** | falta `COLUNA_DF`; ela entra nas colunas de período |
| Duplicatas exatas (mesma chave, mesmo valor) | 572 na DRE con, 809 no BPA con, … | contam como uma linha |
| A mesma chave com **valores diferentes** | **13** no BPP con, **11** no BPP ind, um só emissor | `ValorAmbiguo`: o dado não diz qual vale |
| `ESCALA_MOEDA` | `MIL` e `UNIDADE` em todos os 16 demonstrativos | `valor_em_reais = VL_CONTA × escala`, em `Decimal` |
| `VL_CONTA` ilegível | **0 de 3.786.457** | o valor vira `Decimal` só na linha pedida |
| Os demonstrativos trazem uma `VERSAO` por documento | **0 de 1.408** documentos com mais de uma | a reapresentação **substitui** o valor no arquivo; a versão antiga só existe se foi capturada |
| O índice lista **todas** as versões, com o `DT_RECEB` de cada | 2.448 linhas, 2.161 documentos, **238** com mais de uma, até a `VERSAO` 6 | é a data de conhecimento que falta: **P-183** |
| No registro, o `deslocado` da migração tem a mesma `dt_captura` do `atualizado` que o substituiu | `dfp_cia_aberta_2023`, 2026-09-24T12:16:32Z | `vigencias` ignora `deslocado`, senão o `max(≤ D)` empata |
| Arquivos da carga inicial só têm `inalterado` sem sha256 no registro | **34**; sem a regra, 2010–2021 responderiam `SemCaptura` para sempre | o primeiro `inalterado` atesta o `canonico` do inventário, se há um só do mesmo tamanho (a premissa do portão HEAD). Depois disso, **33 de 33** arquivos DFP/ITR do registro têm vigência |

**De ponta a ponta, sobre o byte real** (`6158b55d…`, posto no cache local `data/armazem/`, que o
git ignora): conta 3.01 da DRE consolidada em 30/06/2024, 476 emissores. Sem o período: 461
`PeriodoAmbiguo`, 6 respostas, 9 `ContaAusente`. Com `dt_ini_exerc = 2024-04-01`: 467 respostas,
9 `ContaAusente`. A mesma pergunta *as-of* 20/09/2026: `SemCaptura`. BPP 2.01.01 em 31/03: 454,
21 `ContaAusente`, 1 `ValorAmbiguo`. As 952 consultas mais a leitura do membro levaram 7,6 s.

## O motor: nenhum pacote novo

A P-53 recomendava Parquet imutável e DuckDB. **O leitor não usa nenhum dos dois**, e a decisão
é minha, com a razão:

- **O ponto da P-53 já está cumprido sem eles.** "O acervo lido não depende de engine": o acervo
  é o ZIP da CVM, chaveado por sha256 no armazém, imutável. O leitor monta em memória um índice
  reconstruível a cada leitura. Nada que ele produz é registro.
- **DuckDB e pyarrow não estão nas dependências** (conferido em 10/10). Em `dependencies` ou
  `dev`, mudariam a impressão `7565df1381e2c1ed`, e isso vai para a fila. Num grupo próprio
  fora da impressão, poderiam entrar, mas não há medida que os peça: o caso medido (476
  emissores, um membro de 164.564 linhas) roda em segundos com a biblioteca padrão.
- **Quando revisitar:** quando o custo em escala for **medido** (400 empresas × 17 anos × 2
  recursos) e passar do aceitável. Aí o Parquet entra como cache derivado do ZIP, num grupo
  fora da impressão. Hoje esse custo é `NAO_CONFIRMADO`.

## A limitação (d)

`politica.yaml → limitacoes_declaradas.dt_captura_nao_e_data_de_conhecimento_do_mercado`,
**`NAO_CONSERTADA`**, pendência **P-183** (política 1.39.0).

Por que não é `FISICA` (§5-B.16): o mundo fornece a data de conhecimento (`DT_RECEB` por versão,
no próprio ZIP) e, em parte, as versões antigas. A Wayback Machine tem o
`dfp_cia_aberta_2022.zip` de 26/03/2026 (status 200). A escada (§5-B.18), transcrita:

- **degrau 1:** o CDX da `web.archive.org` levou `Connection reset by peer` (o proxy registrou
  `ws_closed_mid_exchange` para `web.archive.org:443`), e o WebFetch respondeu "unable to fetch
  from web.archive.org";
- **degrau 2:** a API `archive.org/wayback/available` respondeu. Há cópia do dfp 2022 e nenhuma
  do dfp 2015, 2020 e 2023, nem do itr 2021 e 2023;
- **degrau 4:** contar todas as cópias pelo `medir/` fica para a P-183.

Físico, só o resíduo: o valor de versão substituída que ninguém guardou (CV-01).

O leitor lê a entrada e **recusa responder** sem ela. Toda resposta carrega o nome dela.

## O que fecha, o que abre

- **P-51 fecha:** o leitor e o teste que falha se uma linha `PENÚLTIMO` entrar na série.
- **P-53 fecha na parte do leitor:** a consulta *as-of* e o teste com duas versões do mesmo
  `DT_REFER`. A sobra vira a **P-53b**: a ponte ticker ↔ CNPJ ↔ `CD_CVM` também é bitemporal,
  com gatilho na P-145 fechada.
- **Abre a P-183:** a segunda data de conhecimento (`DT_RECEB` por versão e as cópias de
  terceiro). Sem ela, o leitor não responde nada do backtest de 2010 a 2026.

## Mutação (§5-B.4)

Cada defeito foi reintroduzido no código e um teste reprovou: sem o filtro de `ORDEM_EXERC`,
(a); a versão de hoje no lugar da vigente em D, (b); o `DT_REFER` procurado em todo arquivo
capturado, (c) e (b); `deslocado` contando como vigência; o leitor sem exigir a limitação, (d);
a enumeração frouxa; a primeira linha escolhida quando os valores divergem. **7 de 7**.

## O que esta decisão não faz

Não liga papel a empresa (P-53b). Não responde o que o mercado sabia (P-183). Não mede o custo
em escala. Não toca o FRE nem o FCA.
