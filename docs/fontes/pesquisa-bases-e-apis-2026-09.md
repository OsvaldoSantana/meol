# Pesquisa — bases de dados e APIs para o projeto
Data da pesquisa: 06/09/2026
Metodo: 4 subagentes em paralelo (§11.3 do CLAUDE.md, primeira vez que a tecnica e usada de fato),
cada um devolvendo so a conclusao. O texto das paginas nunca entrou no contexto principal.
Conferencia de primeira mao: os dois endpoints da B3 marcados COMPLETO abaixo foram chamados
por mim, nao pelo subagente, e a saida esta transcrita.
Status: ver por linha. Nada aqui e COMPLETO por vir de subagente — so por ter fonte aberta.

---

## 1. O achado que muda a prioridade do projeto

O projeto vinha tratando a Fase 0 como "baixar DFP/ITR da CVM antes que sobrescrevam".
A pesquisa encontrou **tres fontes mais perecives que a CVM**, e uma delas e a que decide
se o backtest e possivel:

| fonte | janela publica | o que se perde por dia nao capturado |
|---|---|---|
| **Eventos societarios da B3** (proventos, desdobramento, grupamento, bonificacao) | endpoint **nao documentado**, sem contrato, sem SLA | pode sumir sem aviso. Nao ha espelho conhecido |
| **ANBIMA** — IMA-B, IRF-M, ETTJ, debentures | **5 dias uteis** | o dia. O historico so existe no ANBIMA Feed, pago para nao-associado |
| **Carteira teorica dos indices da B3** | **so o dia corrente** | a composicao daquele dia. Historico de composicao nao e publicado |
| CVM DFP/ITR | ZIP anual, mutavel | a versao substituida (ja registrado em `fase0/LEIA-PRIMEIRO.md`) |

**Consequencia:** sem eventos societarios, uma serie de precos e inutilizavel para backtest.
Um desdobramento de 100:1 na PETR em 2008 (confirmado abaixo) faz o preco cair 99% num dia
sem que nada tenha acontecido com o valor da empresa. Um backtest que leia COTAHIST cru le
isso como um crash. **Este e o insumo que falta, e nao estava no plano.**

---

## 2. B3 — eventos societarios (COMPLETO, chamado por mim em 06/09/2026)

### 2.1 Suplemento da empresa

```
GET https://sistemaswebb3-listados.b3.com.br/listedCompaniesProxy/CompanyCall/
    GetListedSupplementCompany/{base64 de {"issuingCompany":"PETR","language":"pt-br"}}
```

Chaves de primeiro nivel confirmadas:
`stockCapital, quotedPerSharSince, commonSharesForm, preferredSharesForm, hasCommom,
hasPreferred, roundLot, tradingName, numberCommonShares, numberPreferredShares,
totalNumberShares, code, codeCVM, segment, cashDividends, stockDividends, subscriptions`

Para PETR devolveu 24 `cashDividends`, **6 `stockDividends`**, 1 `subscriptions`.
Primeiro `stockDividends`, transcrito:

```
assetIssued  BRPETRACNOR9
factor       100,00000000000
approvedOn   25/04/2008
isinCode     BRPETRACNOR9
label        DESDOBRAMENTO
lastDatePrior 25/04/2008
remarks      ""
```

Primeiro `cashDividends`, transcrito:

```
assetIssued  BRPETRACNOR9
paymentDate  21/12/2026
rate         0,47156696000
relatedTo    Anual/2026
approvedOn   06/08/2026
isinCode     BRPETRACNOR9
label        DIVIDENDO
lastDatePrior 21/08/2026
remarks      ""
```

`lastDatePrior` e a **data ex** — o ultimo dia com direito. E ela, nao `paymentDate`,
que entra no fator de ajuste da serie.

**`codeCVM` vem no mesmo objeto.** Isso resolve de graca o problema de chave que o
projeto teria depois: ticker <-> CVM sem tabela intermediaria inventada.

### 2.2 Proventos paginados (historico longo)

```
GET .../listedCompaniesProxy/CompanyCall/GetListedCashDividends/
    {base64 de {"language":"pt-br","pageNumber":1,"pageSize":99,"tradingName":"PETROBRAS"}}
```

Reportado pelo subagente (PARCIAL — nao chamei este): 343 registros, 10/12/2010 a 06/08/2026,
com `closingPricePriorExDate` — o fechamento na vespera do ex, que e o **denominador do fator
de ajuste**, no mesmo registro. Se confirmado, dispensa cruzar com COTAHIST para ajustar.

**Armadilha ja observada pelo subagente e que precisa virar teste:** a chave e
`tradingName` (texto, "PETROBRAS"), e um caractere errado devolve `totalRecords: 0`
**em silencio**, sem erro HTTP. Coletor que nao rejeite retorno vazio grava ausencia
como se fosse ausencia de eventos. E o padrao F-02 outra vez: insumo faltante virando numero.

### 2.3 Carteira teorica do indice (COMPLETO, chamado por mim em 06/09/2026)

```
GET https://sistemaswebb3-listados.b3.com.br/indexProxy/indexCall/GetPortfolioDay/
    {base64 de {"language":"pt-br","pageNumber":1,"pageSize":120,"index":"IBOV","segment":"1"}}
```

Devolveu `date: 08/09/26`, `totalRecords: 76`, campos por ativo:
`segment, cod, asset, type, part, partAcum, theoricalQty`.

**Carteira do Ibovespa capturada em 06/09/2026, valida para 08/09/26 — 76 ativos:**

ALOS3, ABEV3, ASAI3, AURE3, AXIA3, AZZA3, B3SA3, BBSE3, BBDC3, BBDC4, BRAP4, BBAS3,
BRAV3, BPAC11, CXSE3, CEAB3, CMIG4, COGN3, CSMG3, CPLE3, CSAN3, CPFE3, CMIN3, CURY3,
CYRE3, DIRR3, EMBJ3, ENGI11, ENEV3, EGIE3, EQTL3, FLRY3, GGBR4, GOAU4, HAPV3, HYPE3,
IGTI11, ISAE4, ITSA4, ITUB4, KLBN11, RENT3, LREN3, MGLU3, POMO4, MBRF3, BEEF3, MOTV3,
MRVE3, MULT3, NATU3, PETR3, PETR4, PSSA3, PRIO3, RADL3, RDOR3, RAIL3, SBSP3, SANB11,
CSNA3, SMFT3, SUZB3, TAEE11, VIVT3, TEND3, TIMS3, TOTS3, UGPA3, USIM5, VALE3, VAMO3,
VBBR3, VIVA3, WEGE3, YDUQ3

Este e o **primeiro snapshot de composicao do projeto**. Nao ha como obte-lo retroativo.
Nota de leitura: e a carteira do dia, nao a carteira de rebalanceamento; os pesos (`part`)
mudam todo dia com o preco.

**Viés de sobrevivencia, declarado:** esta lista e de hoje. Um backtest que a use para
1998-2026 compra empresas que so entraram no indice depois de darem certo. O historico de
composicao nao e publico, e comecar a coletar hoje so resolve daqui para frente.
Isto entra em `politica.yaml -> limitacoes_declaradas`.

---

## 3. Armazenamento ponto-no-tempo — recomendacao

**Parquet imutavel particionado por `dt_captura` como acervo + DuckDB como motor.**

O ponto que decide: o acervo **nao pode depender de engine nenhum**. O `.duckdb` deve ser
artefato reconstruivel, nao arquivo de registro. DuckDB garante que versao nova le arquivo
antigo, mas o contrario e "best effort" — se o acervo for o `.duckdb`, um upgrade quebrado
custa o acervo; se for Parquet, custa um `rebuild.py`.

Segundo lugar: **DuckLake** (extensao oficial, 1.0 em abr/2026), com `AT (TIMESTAMP => ...)`
nativo. Perdeu por acoplar um acervo de decada a um formato com 1.0 recente, e porque o
time travel dele e tempo de sistema do lakehouse — nao substitui as colunas bitemporais
explicitas que a CVM exige de qualquer jeito (`DT_REFER`, `VERSAO`, `ORDEM_EXERC`).

Descartados com motivo: PostgreSQL 18 tem primitivas bitemporais reais
(`PRIMARY KEY ... WITHOUT OVERLAPS`) mas e row-store e e servico para administrar;
SQLite perde em varredura; Iceberg/Delta/Hudi sem Spark ainda custam catalogo;
DVC/lakeFS/git-annex versionam o par codigo-dado, nao respondem "as of";
Dolt tem `AS OF` de verdade mas e MySQL row-store — serve para a **tabela de mapeamento**
(ticker <-> CNPJ <-> CD_CVM), nao para 100 M de linhas de fato.

### A consulta as-of

```sql
INSTALL encodings; LOAD encodings;   -- CSV da CVM e ISO-8859-1
WITH cap AS (
  SELECT max(dt_captura) AS d
  FROM read_parquet('bronze/cvm/dfp/dt_captura=*/*.parquet', hive_partitioning = true)
  WHERE dt_captura <= DATE '2026-04-15'      -- max(captura <= D), nunca "= D"
)
SELECT * FROM read_parquet('bronze/cvm/dfp/dt_captura=*/*.parquet', hive_partitioning = true)
WHERE dt_captura = (SELECT d FROM cap);
```

Camada silver, SCD2 bitemporal:

```sql
SELECT * FROM fato_cvm
WHERE sys_from <= DATE '2026-04-15' AND DATE '2026-04-15' < sys_to
  AND dt_refer <= DATE '2026-04-15'
QUALIFY row_number() OVER (PARTITION BY cd_cvm, dt_refer, ordem_exerc, cd_conta
                           ORDER BY versao DESC, sys_from DESC) = 1;
```

Alinhar preco ao conhecimento: `ASOF LEFT JOIN` e nativo no DuckDB;
em pandas, `merge_asof(..., by=..., direction='backward')`.

### As armadilhas que este projeto ainda nao sabia que tinha

1. **`dt_captura` nao e data de conhecimento do mercado.** Comecando a capturar hoje, nao
   existe PIT anterior a hoje. Backtest pre-2026 e **reconstrucao, nao observacao** — e
   isso pertence a `limitacoes_declaradas`, nao a um README.
2. **`ORDEM_EXERC = PENULTIMO` e look-ahead puro.** O arquivo anual traz o ano anterior
   **ja reapresentado**. Usar so `ULTIMO` do arquivo daquele ano. O projeto contou as duas
   enumeracoes e nao havia percebido que uma delas contamina o backtest.
3. **Reapresentacao cruzada:** o DFP de 2025 corrige 2023. A particao e o ano do arquivo,
   nao o ano do dado.
4. **Sumico silencioso:** empresa que deixa de aparecer no ZIP. Snapshot completo detecta;
   coleta incremental nao.
5. **Identidade temporal:** ticker e reciclado; o mapeamento ticker<->CNPJ<->CD_CVM tambem
   precisa ser bitemporal, senao o join vaza futuro.
6. **DuckDB e single-writer por arquivo** — nao rodar download e backtest no mesmo `.duckdb`.
7. **`DECIMAL`, nunca `DOUBLE`,** para valores monetarios.

NAO_CONFIRMADO: razao de compressao Parquet/CSV para os arquivos da CVM (nao medido);
custo real de um `.duckdb` de dezenas de GB (nenhum benchmark oficial encontrado).

---

## 4. Banco Central — o que existe, com endpoint

| recurso | URL | auth | limite | status |
|---|---|---|---|---|
| SGS | `https://api.bcb.gov.br/dados/serie/bcdata.sgs.{cod}/dados` | nenhuma | **max. 10 anos por requisicao** | COMPLETO |
| IF.data (**tem OData**) | `https://olinda.bcb.gov.br/olinda/servico/IFDATA/versao/v1/odata/` | nenhuma | trimestral, T+60/90d, desde mar/2000 | PARCIAL |
| Ranking de Reclamacoes | `https://www3.bcb.gov.br/rdrweb/rest/ext/ranking/arquivo` | nenhuma | desde jul/2014 | COMPLETO |
| Balancetes de IFs (Cosif ate nivel 4) | `https://dadosabertos.bcb.gov.br/dataset/ifs-balancetes` | nenhuma | **sem API**, CSV.ZIP | COMPLETO |
| PTAX | `https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/` | nenhuma | — | PARCIAL |
| Taxas de juros por instituicao | `https://olinda.bcb.gov.br/olinda/servico/taxaJuros/versao/v2/odata/` | nenhuma | — | PARCIAL |

Codigos de serie do SGS conferidos na ficha oficial:

| codigo | serie | unidade |
|---|---|---|
| 12 | CDI | % a.d. |
| 11 | Selic efetiva diaria | % a.d. |
| 432 | Meta Selic (Copom) | % a.a. |
| 1178 | Selic anualizada base 252 | % a.a. |
| 4390 | Selic acumulada no mes | % a.m. |
| 433 | IPCA | var. % mensal |
| 189 | IGP-M | var. % mensal |
| 226 | TR | % a.m. |
| 195 | Poupanca apos 04.05.2012 | % a.m. |
| 1 | Dolar venda, diario | R$/US$ |

Requisicao montada e conferida (formato de data e **dd/MM/aaaa** com barras; `valor` volta
como **string**, com ponto decimal):

```
https://api.bcb.gov.br/dados/serie/bcdata.sgs.12/dados?formato=json&dataInicial=01/09/2025&dataFinal=10/09/2025
-> [{"data":"01/09/2025","valor":"0.055131"}, ...]
```

**O limite de 10 anos por requisicao e procedencia, nao detalhe de implementacao:** e a razao
pela qual o coletor de CDI vai ter um laco. Registrar isso evita que a proxima sessao ache
que o laco e paranoia.

**P-14 (solvencia de banco) fica mais barata do que estava previsto:** o IF.data **tem API
OData**, nao so download por navegador — o projeto supunha o contrario. O recurso
`ListaDeRelatorio` descreve a estrutura e diz em qual relatorio vivem Basileia, PR e
imobilizacao, sem chutar. Complemento: Balancetes com Cosif nivel 4 por CNPJ, mas com
defasagem material — o dado de out-dez so sai em 31/03 do ano seguinte.

**Achado lateral, do catalogo, que ninguem pediu e vale mais que varios que pedi:**
`Instituicoes submetidas a regimes de resolucao` — praticamente um sinal binario de risco
terminal para "onde o dinheiro vai ficar". Tambem: Ranking de Qualidade de Ouvidorias,
Penalidades do PAS, Multas emitidas, Tarifas Bancarias por Instituicao.

~~NAO_CONFIRMADO: `olinda.bcb.gov.br` esta **bloqueado por robots.txt** (ROBOTS_DISALLOWED) —
nao contornado. As URLs-base vem das paginas do portal de dados abertos; a **sintaxe de
parametro** do OData do BCB nao foi verificada. Antes de codificar, abrir o Swagger no
navegador.~~ ESTBAN nao existe no catalogo de dados abertos e o caminho antigo devolveu 404.

> **27/09/2026, medido de novo — resolvido no degrau 1 da escada (`CLAUDE.md` §5-B.18),
> escada: 1 curl no terminal → HTTP 200.** O `ROBOTS_DISALLOWED` era a politica da ferramenta
> de busca do subagente, nao uma recusa do servidor. `curl` em
> `https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarDia(dataCotacao=@dataCotacao)?@dataCotacao='09-25-2026'&$format=json`
> respondeu **HTTP 200**, com os campos `cotacaoCompra`, `cotacaoVenda` e `dataHoraCotacao`.
> A **sintaxe de parametro** fica verificada pelo mesmo comando: parametro nomeado
> `@dataCotacao`, data em `MM-DD-AAAA` entre aspas simples, `$format=json`. O
> `https://olinda.bcb.gov.br/robots.txt` respondeu **HTTP 502** (pagina de erro do BCB, sem
> regra legivel). As outras duas URLs-base da tabela (IF.data e taxaJuros) seguem `PARCIAL`:
> o degrau 1 foi tentado so no PTAX.

---

## 5. Tesouro, ANBIMA, e o resto

| fonte | conjunto | URL | historico | status |
|---|---|---|---|---|
| Tesouro Transparente | precos e taxas diarios do Tesouro Direto | CKAN, `precotaxatesourodireto.csv` (13,7 MiB) | **jan/2002** | COMPLETO, licenca ODbL |
| Tesouro Transparente | vendas, resgates, estoque, investidores | CKAN | jan/2002 | COMPLETO |
| Tesouro | **historico da taxa de custodia** | — | — | **NAO_CONFIRMADO** — nao ha serie; so paginas narrativas |
| ANBIMA | IMA, IRF-M, ETTJ, debentures | paginas publicas | **so 5 dias uteis** | COMPLETO quanto ao modelo de acesso |
| ANBIMA Feed / Data | historico | `developers.anbima.com.br` | — | PARCIAL: gratis para associado, pago para o resto |
| B3 | COTAHIST | pagina de series historicas | **1986** | COMPLETO, continua gratuito |
| B3 | `developers.b3.com.br` | — | — | COMPLETO: **B2B, "nao oferecemos acesso direto a pessoas fisicas"** |
| B3 | `arquivos.b3.com.br` / UP2DATA | — | — | NAO_CONFIRMADO (SPA; endpoints testados deram 400/404) |

A janela de 5 dias uteis da ANBIMA e o segundo prazo real do projeto, e ele nao estava
registrado em lugar nenhum.

---

## 6. Taxas de ETF — a P-05 fica mais barata, e mais errada do que parecia

Nao existe CSV/JSON oficial com as taxas de todos os ETFs — nao encontrado, nao desmentido.
O caminho e **um documento por fundo**: pagina do produto (BlackRock, URL estavel) ou lamina
em PDF (Itau). Cerca de 15 documentos, 1-2 h, com reconferencia semestral.

**O defeito de modelagem que a pesquisa achou, e ele e maior que a pendencia:**
nas laminas do Itau, "taxa de administracao" e **so um componente** — ha tambem gestao,
custodia e estruturacao. O numero comparavel e a **taxa total maxima a.a.** A BlackRock
divulga um numero unico. Guardar isso num campo `taxa_adm` e comparar rotas por ele
subestima o custo do lado Itau e produz exatamente o tipo de defeito silencioso que a P1
existe para impedir. `custos.yaml` precisa de `taxa_total_aa` + `composicao` +
`fonte_url` + `data_doc`, nao de um numero solto.

Valores levantados em 06/09/2026 (**PARCIAL — nao conferi as paginas eu mesmo; e o
subagente que as leu, e antes de entrar no `custos.yaml` cada um precisa da conferencia
de trecho que a doutrina exige**):

| ETF | valor | decomposicao |
|---|---|---|
| BOVA11 | 0,10% | numero unico do gestor |
| SMAL11 | 0,50% | numero unico |
| IVVB11 | 0,23% | numero unico |
| BOVV11 | **0,10% total** | adm 0,02 + custodia 0,01 + gestao 0,07 |
| PIBB11 | **0,06% total** | adm 0,005 + custodia 0,005 + gestao 0,049 |
| IMAB11 | **0,25% total** | adm 0,04 + custodia 0,03 + gestao 0,18 |
| IRFM11 | adm 0,04% | total **nao** confirmado |
| B5P211 | adm 0,04% | total **nao** confirmado |

~~NAO_CONFIRMADO: se `cad_fi` da CVM tem campo de taxa (dominio bloqueado);~~ NAO_CONFIRMADO:
se a B3 publica taxa de ETF (pagina devolveu 500); gestores BTG, Investo, Buena Vista, Bradesco
*(estes dois nao foram reabertos em 27/09)*.

> **27/09/2026, medido de novo — `cad_fi` resolvido no degrau 1, escada: 1 curl no terminal
> → HTTP 206.** `curl -r 0-4095 https://dados.cvm.gov.br/dados/FI/CAD/DADOS/cad_fi.csv`
> devolveu o cabecalho: 41 colunas, **`TAXA_PERFM` na 22 e `TAXA_ADM` na 24** (mais
> `INF_TAXA_PERFM` na 23 e `INF_TAXA_ADM` na 25). O `robots.txt` de `dados.cvm.gov.br` de hoje
> barra so `/dataset/rate/`, `/revision/`, `/dataset/*/history` e `/api/`; `/dados/` fica livre.
> **O que o cabecalho nao diz** (§5-B.1): o arquivo inteiro (17.921.330 bytes, sha256
> `612adad8548d313d…`, `Last-Modified` 26/09/2026) tem `TAXA_ADM` preenchida em **15.117 de
> 46.806 linhas, e so 1 delas `EM FUNCIONAMENTO NORMAL`**. Depois da adaptacao a RCVM 175 os
> fundos vivos estao no `registro_fundo_classe.zip`, **que nao tem campo de taxa** (lidas as
> colunas de `registro_fundo`, `registro_classe` e `registro_subclasse`); o `extrato_fi` de
> 2025 e 2026 tem `TAXA_ADM` e `TAXA_CUSTODIA_MAX`, mas so para classes FIF (6.565 de 6.565
> em 2026). **Para ETF, a CVM em dados abertos nao e fonte da taxa de hoje**: ver a escada do
> BOVV11 em `MAPA-CONSTANTES.md` e a P-05.

---

## 7. Bibliotecas — o que esta vivo

| pacote | veredito |
|---|---|
| `python-bcb` (0.4.0, jun/2026) | **fonte primaria** — bate direto nas APIs do BCB |
| `b3cotahist` (0.1.9, nov/2024) | olhar antes de escrever parser proprio; licenca nao declarada no PyPI |
| `finbr` (MIT, ativa) | olhar; mistura B3 + Yahoo + SGS, entao a procedencia e mista |
| `brapi.dev` | **so conferencia** — consolida CVM+BCB mas nao cita linha a linha |
| `yfinance` `.SA` | **so conferencia** — falhas de split/dividendo documentadas, sem avaliacao de erro publicada para BR |
| `investpy` | **nao usar** — ultima release 01/2022, quebrado |
| Fundamentus, Status Invest, Investidor10, Fundamentei | so conferencia; termos de uso nao lidos |

**Nenhuma biblioteca encontrada le `cad_fi` ou o informe diario da CVM.** Parser proprio.

Regra da casa que sai daqui: agregador nunca e fonte primaria neste projeto. Ele entra
como **conferencia cruzada** — se o numero dele diverge do da fonte primaria, e um achado,
nao um empate.

---

## 8. O que a pesquisa NAO conseguiu conferir

- **Todo o catalogo da CVM alem de DFP/ITR.** `dados.cvm.gov.br` devolveu ROBOTS_DISALLOWED
  de novo, em `/dataset` e em `/dados/CIA_ABERTA/DOC/`. Nao contornei — nem eu nem o
  subagente. FRE, FCA, IPE, VLMO, `cad_fi`, `inf_diario_fi`, `cda`, FIIs: os slugs aparecem
  indexados em busca, mas **nenhuma pagina foi lida**. Tudo PARCIAL ou NAO_CONFIRMADO.
  Isto so se resolve da maquina dele, ou do celular dele — ver o roteiro em
  `fase0/CELULAR-CVM.md`.

> ⚠ **RETRATAÇÃO — 24/09/2026:** tratada como manual; um script na máquina dele resolve. A limitação era da ferramenta de quem respondia, não da tarefa. Hoje é `py -3.11 fase0/capturar_cvm.py` (CLAUDE.md §3, §5-B.17).
- Cobertura do endpoint de proventos da B3 para empresas **deslistadas** e para o periodo
  anterior a 2010. Ponto cego, e e viés de sobrevivencia direto no backtest.
- ~~Sintaxe de parametro do OData do BCB (olinda bloqueado).~~ *Verificada em 27/09 pelo
  degrau 1 (curl na API PTAX, HTTP 200): ver a nota da secao 4.*
- Se `arquivos.b3.com.br` ainda tem arquivo gratuito.
- Historico da taxa de custodia do Tesouro.
