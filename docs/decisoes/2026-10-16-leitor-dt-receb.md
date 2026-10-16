# O leitor as-of ganha a data de conhecimento do mercado: `DT_RECEB` da versão presente (P-183)

*16/10/2026. **Pedido:** a arquitetura (prompt da P-183, 16/10). **Desenho, medição e registro:**
sessão local do Claude Code, mesmo dia. Decisão técnica: não muda regra de decisão; muda o que o
leitor consegue responder antes de 24/09/2026.*

## A pergunta

O leitor de 10/10 (`fase0/leitor_cvm.py`) responde o que **este sistema** tinha capturado até D,
e o registro começa em 24/09/2026: o backtest de 2010 a 2026 inteiro ficava sem resposta. A fonte
tem a segunda data. O índice de cada ZIP (`{recurso}_cia_aberta_{ano}.csv`) lista **todas** as
versões de cada documento, com o `DT_RECEB` de cada uma, e o demonstrativo traz só a última.

## As alternativas

| | alternativa | por que não |
|---|---|---|
| A | `DT_RECEB` da **primeira** versão do documento | devolveria em D o valor da última versão, que só chegou depois: *look-ahead*. É a mutação que o teste (e) reprova |
| B | Reconstruir pela captura (o modo de 10/10) e esperar | não responde nada antes de 24/09/2026; nenhuma espera muda isso |
| **C** | **`DT_RECEB` da versão presente ≤ D** (a escolhida, a regra que a P-183 já nomeava) | sem *look-ahead*. Entre a 1ª e a última versão o documento fica oculto, com `ContaAusente` dizendo qual versão o mercado conhecia, e o tamanho disso foi medido |
| D | C mais o valor da versão substituída lido do ENET | é o que resolve o resíduo, mas é um leitor de XML novo (o pacote do ENET não é o CSV dos dados abertos). Vira a P-184 |

## O modo

`valor(..., conhecimento="dt_receb")` e `linhas(..., conhecimento="dt_receb")`. O padrão continua
`"captura"`: nenhum chamador muda de comportamento sem pedir.

1. **Qual arquivo:** o do ano do `DT_REFER` (P-51, igual).
2. **Qual versão do arquivo:** a **mais recente** capturada (o índice dela tem todas as versões).
3. **Quais documentos:** só aqueles cuja versão presente no demonstrativo tem `DT_RECEB` ≤ D. Data
   inclui o dia inteiro. Num instante, o documento só conta depois de o dia do recebimento terminar
   em Brasília, com o deslocamento fixo de −3 h do leiaute: nos verões com horário de verão (até
   2019) isso faz o leitor esperar uma hora a mais, nunca uma a menos.
4. **O que ele recusa:** versão presente fora do índice (`DataDeConhecimentoAusente`: nenhuma
   outra data entra no lugar) e versão com duas datas (`DataDeConhecimentoAmbigua`, 5 chaves no
   dado real).

O leiaute do índice (membro, colunas, formato da data, deslocamento) está em
`docs/schemas/cvm-dfp-itr-v1.yaml → indice` (P2).

## O que a medição mostrou (`medicoes/resultados/p183_dt_receb.txt`)

As 31 versões vigentes de DFP 2010–2025 e ITR 2011–2025, baixadas da release pública
`cvm-acervo-2026` com o sha256 conferido contra o registro. Horizonte: 31/08/2026.

- **14.955 de 3.870.622 documento-meses ficam ocultos (0,4%)**; 2.727 de 40.905 documentos
  têm ao menos um; mediana de 2 meses por documento oculto, máximo de 97. Por ano, entre 0,3% e
  0,8%.
- Das 6.074 que têm mais de uma versão, 2.727 escondem algum fim de mês. As outras foram
  reapresentadas dentro do mesmo mês.
- Nos 16 demonstrativos, a premissa do modo valeu sem exceção: **0** documento com a versão
  presente diferente da maior do índice, **0** fora do índice, **0** com duas versões no mesmo
  membro.

## O que mudou no tipo da limitação

`dt_captura_nao_e_data_de_conhecimento_do_mercado` continua **NAO_CONSERTADA** (política 1.42.0),
reescrita. Pela §5-B.16: o resíduo não é do mundo. O `LINK_DOC` de cada versão no índice leva ao
ENET da CVM, que serviu as versões substituídas pelo `https`, com o XML estruturado inteiro, nos 2
documentos testados (n = 2). A frase de 10/10, *"físico, só o resíduo: o valor de versão
substituída que ninguém guardou"*, estava errada: a CVM guarda (CV-08).

## Mutação (§5-B.4)

Com o `DT_RECEB` da primeira versão no lugar do da presente, o teste (e) de duas versões reprova.
Ignorando o `DT_RECEB` (todo documento visível), quatro testes (e) reprovam. Um instante do
próprio dia do recebimento contando como conhecido (`<=` no lugar de `<`) reprova o teste do
instante.
