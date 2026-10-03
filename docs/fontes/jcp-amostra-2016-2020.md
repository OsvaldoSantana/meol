# D1 — a transcrição da amostra de JCP de 2016–2020 (§3.1, passo 2)

- **Fonte:** documentos das companhias no RAD da CVM (Empresas.NET), localizados pelo conjunto
  aberto `cia_aberta-doc-ipe` (dados.cvm.gov.br); para a posição 5, também o 20-F de 2018 da
  Gerdau na SEC (EDGAR).
- **Acesso:** 03/10/2026, entre 16:08 e 16:35 UTC, sessão do Claude Code na nuvem.
- **Status:** COMPLETO para as 10 posições que o D1 julga. Os PDFs **não** estão no armazém
  (ver "O que falta", abaixo).
- **Fecha:** o passo 2 da §3.1 de `docs/auditoria/C02-CRITERIO-V2-PREREGISTRO.md` (P-115).
- **Original:** nenhum arquivo entra no repositório. Cada prova tem URL e sha256: quem quiser
  conferir baixa de novo e compara.

**O sorteio** é o do commit `73ee120`: semente 20260927, 697 pares, silver `ec6b50da…98143`. A
regra é a da §3.1 com a **emenda E-D1a** (`95042ca`), empurrada antes desta classificação.

## O veredito: `PASSA`

As posições 1 a 10 têm documento achado, e as 10 são `BRUTO`. Nenhuma posição foi pulada.

**O que cada saída daria** (correção de 03/10, auditoria do claude.ai: o texto anterior dizia
que sem a E-D1a o D1 não seria `PASSA`, e só a leitura estrita leva a isso). As posições 5 e 10
são `BRUTO` pela E-D1a; a emenda e a sua limitação estão na §3.1.

| saída posta a ele antes da decisão | posição 5 (GGBR3) | posição 10 (TOTS3) | o D1 |
|---|---|---|---|
| retenção = bruto, aceitando o 20-F (**a decidida**) | `BRUTO` | `BRUTO` | `PASSA` (posições 1 a 10) |
| as duas não contam (falta a 4ª prova; regra de pular) | pulada | pulada | `PASSA`: entram a 11 e a 12, já registradas como "seriam `BRUTO`" |
| retenção = bruto, só com PDF | sem prova em PDF | `BRUTO` | depende da posição 5: se ela não contar, entra a 11 e dá `PASSA`; se contar como não `BRUTO`, `NAO_CONFIRMADO` |
| leitura estrita (só "bruto"/"gross" ou líquido ao lado) | não `BRUTO` | não `BRUTO` | `NAO_CONFIRMADO` |

| pos | data ex | ticker | data com | documento (CVM/RAD) | bruto (doc.) | líquido (doc.) | alíquota | valor da B3 | classe |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 2019-06-27 | RADL3 | 26/06/2019 | Aviso aos Acionistas, `005258IPE210620190204363710-94` v2, 24/06/2019 | 0,162303512 | — | não declarada (cita o art. 9º da Lei 9.249/95) | 0.162303512 | `BRUTO` |
| 2 | 2019-12-23 | WEGE3 | 20/12/2019 | Aviso aos Acionistas, `005410IPE171220190204381610-96` v2, 17/12/2019 | 0,038235294 | 0,032500000 | 15% | 0.038235294 | `BRUTO` |
| 3 | 2018-12-28 | CPLE5 | 27/12/2018 | Aviso aos Acionistas, `014311IPE121220180104344611-20` v1, 12/12/2018 | 2,89050 (PNA) | — | 15,00% | 2.8905 | `BRUTO` |
| 4 | 2017-02-21 | ITUB4 | 20/02/2017 | Fato Relevante, `019348IPE060220170104276806-04` v1, 07/02/2017 | 0,77540 | 0,65909 | 15% | 0.7754 | `BRUTO` |
| 5 | 2018-08-22 | GGBR3 | 21/08/2018 | Aviso aos Acionistas, `003980IPE080820180104332004-43` v1, 08/08/2018 (+ 20-F na SEC) | 0,14 (E-D1a) | — | 15% (20-F) | 0.14 | `BRUTO` |
| 6 | 2020-09-02 | BBDC4 | 01/09/2020 | Aviso aos Acionistas, `000906IPE191220190104381811-23` v1, 19/12/2019 | 0,018974809 (PN) | 0,016128588 | 15% | 0.018974809 | `BRUTO` |
| 7 | 2019-05-03 | BBDC4 | 02/05/2019 | Aviso aos Acionistas, `000906IPE071220180104344110-89` v1, 07/12/2018 | 0,018974809 (PN) | 0,016128588 | 15% | 0.018974809 | `BRUTO` |
| 8 | 2016-12-02 | VALE5 | 01/12/2016 | Comunicado ao Mercado, `004170IPE281120160104270211-50` v1, 28/11/2016 | 0,166293936 | — | não declarada | 0.166293936 | `BRUTO` |
| 9 | 2019-10-01 | MULT3 | 30/09/2019 | Fato Relevante, `020982IPE250920190104373311-28` v1, 25/09/2019 | 0,13417101396 | — | 15% | 0.13417101396 | `BRUTO` |
| 10 | 2016-12-22 | TOTS3 | 21/12/2016 | Aviso aos Acionistas, `019992IPE161220160104272010-30` v1, 16/12/2016 | 0,248642967 (E-D1a) | — | não declarada | 0.248642967 | `BRUTO` |

**Como se mede "igual".** A diferença tem de ser ≤ meia unidade da última casa impressa no
documento. Nas 10, a diferença entre a B3 e o bruto é **zero** na precisão impressa. O líquido
esperado é o do documento ou, sem ele, bruto × (1 − alíquota):
- com a alíquota declarada: 3, 5 (pelo 20-F) e 9;
- com os 15% da lei (E-D1a), sem alíquota declarada: 1, 8 e 10.

A menor distância entre a B3 e o líquido é 0,0028 (posições 6 e 7), contra uma tolerância de
5 × 10⁻¹⁰. **Nenhuma alíquota positiva aproximaria o líquido do valor da B3**, então a classe
não depende da alíquota assumida.

## As provas, por evento

Todas as URLs do RAD são
`https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=<n>&numSequencia=<s>&numVersao=<v>`,
com os três números abaixo.

| pos | numProtocolo / numSequencia / numVersao | sha256 do PDF | bytes | págs. | página do valor |
|---|---|---|---|---|---|
| 1 | 697177 / 223378 / 2 | `cf4cd6f4c480243769ec5569dd45f41bb34dbb6d46d3a9ad96ff13e69dc48728` | 76.139 | 2 | 1 |
| 2 | 726802 / 251578 / 2 | `59aaaaa5192966823658b0a4ca3bedc45cc28b0776d7d3a8a58c235b1556ede6` | 88.530 | 2 | 1 |
| 3 | 656678 / 187541 / 1 | `6cbde45e3079092b667584ab3aa124388bbe8a072f06ea94ece575ff30e15b9b` | 121.547 | 1 | 1 |
| 4 | 546825 / 89573 / 1 | `f57da34d5a5fa17a08a72fa4320b2f51f97e3ffa0c78c79d1163c7ffb27c27d5` | 19.492 | 1 | 1 |
| 5 | 635827 / 169454 / 1 | `cd978d677cf7d6a95fe0f298b5ce29dfc12f1a484fa0be3f03ce9a4756797791` | 146.013 | 1 | 1 |
| 6 | 727283 / 252057 / 1 | `73b2db45717cfb150a1c9da1c110afc8fcbdbc9857be7c50185dcd419212c1ff` | 655.849 | 1 | 1 |
| 7 | 655277 / 186281 / 1 | `059aed21fe09b307e732f3f60c9c6ea4dd05b1505099d6c8251684a4c992989d` | 659.040 | 1 | 1 |
| 8 | 539538 / 82286 / 1 | `8c5bde917168b6a3ee5ba0046145578635969f4473d00cb649c99a7fd8530206` | 165.192 | 2 | 1 |
| 9 | 712472 / 237637 / 1 | `ace972b6887009e2eda0edcfd6495b73ae92b36fe358681de854162906598338` | 79.591 | 1 | 1 |
| 10 | 542284 / 85032 / 1 | `e7031ebec177ff2b078d209e0804aca596e32d71dcb100ed62d07f5437d0c947` | 183.497 | 1 | 1 |

**Os trechos, copiados do documento** (a quebra de linha do PDF virou espaço):

1. RADL3: "O valor bruto a ser pago por ação é de R$ 0,162303512 e não sofrerá nenhuma
   atualização monetária." · "haverá retenção de Imposto de Renda na Fonte, de acordo com o
   artigo 9º da Lei 9249/95"
2. WEGE3: "correspondente a R$ 0,038235294 por ação" · "será feito pelo valor líquido, de
   R$ 0,032500000 por ação, já deduzido o imposto de renda na fonte de 15% (quinze por cento)"
3. CPLE5: "1.2.2. R$ 2,89050 por ação preferencial classe “A” – PNA" · "1.5. Tributação:
   15,00%, conforme estabelece a Lei 9.249/95"
4. ITUB4: "a declaração de “JCPs” complementares do exercício de 2016 no valor de R$ 0,77540
   por ação" · "com retenção de 15% de imposto de renda na fonte, resultando em juros líquidos
   de R$ 0,65909 por ação". O "(líquidos de imposto de renda)" do mesmo parágrafo se refere ao
   total de "R$ 4,3 bilhões", não ao valor por ação: o líquido por ação é o 0,65909 escrito
   na mesma frase.
5. GGBR3, CVM: "Para o caso específico da Gerdau S.A. o pagamento será feito sob a forma de
   juros sobre capital próprio." · a tabela: "GERDAU S.A. R$ 0,14". Esse documento não rotula o
   valor; o rótulo vem do 20-F (abaixo).
6. BBDC4: "Setembro 1o.9.2020 2.9.2020 1o.10.2020" (mês, data-base, "Ex-Direito", pagamento) ·
   "R$0,018974809 por ação preferencial, que, líquidos do imposto de renda na fonte de 15%
   (quinze por cento), correspondem a R$0,014662352 por ação ordinária e R$0,016128588 por ação
   preferencial"
7. BBDC4: "Maio 2.5.2019 3.5.2019 3.6.2019" · o mesmo parágrafo de valores da posição 6,
   palavra por palavra, no cronograma de 2019.
8. VALE5: "no valor bruto de R$ 856.975.000,00 (US$ 250 milhões), correspondente ao valor de
   R$ 0,166293936 (US$ 0,048511898) por ação ordinária ou preferencial" · "totalmente na forma
   de juros sobre capital próprio"
9. MULT3: "no montante bruto de R$ 80.000.000,00 (oitenta milhões de reais), correspondente a
   R$ 0,13417101396 por ação, sujeito à retenção de 15% de imposto de renda na fonte"
10. TOTS3: "valor este que corresponde a R$0,248642967 por ação" · "5. Haverá retenção do
    Imposto de Renda Retido na Fonte – IRRF de acordo com a legislação vigente" (E-D1a)

**A prova do bruto da posição 5 (E-D1a), no 20-F de 2018 da Gerdau:**
- **URL:** `https://www.sec.gov/Archives/edgar/data/1073404/000110465919018684/a19-2248_120f.htm`,
  arquivado em 29/03/2019.
- **sha256 como baixado** (6.652.190 bytes):
  `081de950a3f2694cc382094ee0ffb7dd59339690f48dfc49c79f2da7a23a52e2`.
- **sha256 do documento arquivado** (6.652.067 bytes, o tamanho que o índice do EDGAR declara):
  `20f8599eadcabc4f0a65410856f894ddfe7d3dfef7a8fac7b0c05b0de2d3b512`. A diferença são os 123
  bytes de um `<script>` que o servidor da SEC acrescenta antes de `</body>`. Uma cópia
  futura pode trazer outro script; o sha256 que se reproduz é o do documento arquivado.
- **Página 6:** "2nd Quarter 2018 (1) 07/08/2018 0.1400 0.0373" · "(1) Payment of interest on
  equity."
- **Página 7:** "The payment of interest on equity described herein is subject to a 15%
  withholding tax."

## A integridade, conferida antes do sha256

**O RAD corta a transferência.** O servidor responde em `Transfer-Encoding: chunked`, sem
`Content-Length`. Na primeira tentativa (posição 1), o `curl` sem opções saiu com
`curl: (18) transfer closed with outstanding read data remaining`. Foram cinco cópias cortadas,
cada uma com outro tamanho: 12.289, 12.223, 13.631, 17.322 e 3.706 bytes (esta última em
HTTP/1.0). Uma tem os mesmos 13.631 bytes que chegaram no claude.ai em 03/10. O proxy da sessão
não registrou falha (`recentRelayFailures` vazio): o corte vem do servidor. Com `--compressed`
e um User-Agent de navegador, o mesmo endereço chegou inteiro (76.139 bytes), e o resto da
transcrição usou essas duas opções.

**Sem `Content-Length`, o tamanho se confere pela estrutura do PDF.** Um arquivo só conta se:
- começa com `%PDF-`;
- termina com `%%EOF`;
- o `startxref` aponta para dentro do arquivo;
- o `pdfinfo` abre e o `pdftotext` extrai **cada página**, sem erro;
- **duas cópias seguidas** têm o mesmo sha256.

Quando o servidor manda `Content-Length` (o S3 da Totvs), ele tem de bater com o tamanho
recebido.

**A guarda pega o corte.** Aplicada às cinco cópias cortadas, as cinco reprovam: sem `%%EOF`,
sem `startxref` válido e sem páginas legíveis.

**Duas rodadas.** Depois da primeira, as 10 provas e o 20-F foram baixados de novo numa rodada
independente: os 11 sha256 repetiram (n = 11). As posições 3 e 4 deram um *Syntax Warning* da
tabela de linearização (*page offset hints*); não é erro de leitura, as páginas abrem.

## Como os documentos foram achados (e o que o instrumento não via)

- **Companhia:** o CNPJ de cada ticker vem do FCA da CVM (`fca_cia_aberta_valor_mobiliario`,
  2017 e 2019, campo `Codigo_Negociacao`). O VALE5 não está no FCA de 2017, que não traz
  código de negociação para a Vale; ele foi casado pelo prefixo VALE com o CNPJ do FCA
  (33.592.510/0001-54, "VALE S.A.").
- **Documento:** no `ipe_cia_aberta_<ano>`, os documentos do CNPJ entregues entre 60 dias antes
  e 2 dias depois da data ex, filtrados por palavras do assunto (juros, JCP, capital próprio,
  provento, dividendo, aviso aos acionistas).
- **O filtro deixou passar dois casos, ambos achados na leitura:**
  - o comunicado da Vale tem assunto "Vale aprova pagamento de remuneração aos acionistas";
    foi achado listando todos os documentos da Vale no período;
  - o JCP mensal do Bradesco sai num **cronograma** publicado em dezembro do ano anterior, fora
    da janela de 60 dias; foi achado ampliando a busca a todos os avisos do Bradesco.

## A escada das posições 5 e 10 (antes da E-D1a)

**Posição 5 (GGBR3).**
1. **Outros documentos do mesmo evento na CVM:**
   - ata do Conselho (`635826`) e ata da Diretoria (`635825`): "calculados à razão de R$ 0,14
     por ação", sem rótulo;
   - press-release do 2T18 (`635837`): "R$ 238,3 milhões (R$ 0,14 por ação)", sem rótulo;
   - DFP 2018, notas, p. 56 (PDF da companhia dentro do `.dfp` do RAD): "2º trimestre Juros
     0,14 … 238.293", sem rótulo.
2. **Wayback Machine:** o `web.archive.org` falhou duas vezes no túnel do proxy
   (`ws_closed_mid_exchange`, "tunnel closed (code 1006)").
3. **SEC (outra fonte primária da companhia):**
   - 6-K de 08 e 09/08/2018: press-release e demonstrações em inglês, sem rótulo;
   - **20-F de 2018:** rotulado, como na seção das provas acima.

**Posição 10 (TOTS3).**
1. **Outros documentos do mesmo evento na CVM:**
   - atas do Conselho (`542280` e `543054`): "R$ 0,248642967 por ação", sem rótulo;
   - DFP 2016, nota 20: só o total de "R$40.615", sem rótulo.
2. **Site de RI da Totvs:**
   - a tabela "Dividendos e JCP" tem só "Valor (R$) · Total · Por ação";
   - o aviso em inglês, vindo do arquivo da MZ no S3 (sha256 `1ec7428e…40a9`, igual ao caminho
     do S3, `Content-Length` 110.453 batendo), repete o português: "Payments will be subject to
     Income Tax withholding". Não diz *gross*.
3. **Wayback Machine:** mesma falha da posição 5.

Nenhum degrau achou a palavra "bruto" ou um líquido declarado. A E-D1a decide pela frase de
retenção, que a posição 10 tem no próprio aviso e a posição 5 tem no 20-F.

## Abertas e fora do D1: posições 11 e 12

Foram abertas **antes** da decisão sobre 5 e 10, quando ainda não se sabia que os 10 eventos do
D1 são as posições 1 a 10. Ficam registradas e **não entram no veredito**:
- **11, BBDC3, ex 2018-08-02:** cronograma de 2018 (`000906IPE201220170104308910-76`, sha256
  `6e1a656c…4e02`), "Agosto 1o.8.2018 2.8.2018 3.9.2018", ON R$ 0,017249826, líquido
  0,014662352. Seria `BRUTO`.
- **12, WEGE3, ex 2017-12-18:** aviso `005410IPE121220170104308110-52` (sha256 `b984739…7fc3`),
  R$ 0,057058824, líquido R$ 0,048500000 com 15%. Seria `BRUTO`.

## O que o D1 não diz (P5)

- **Do que o D1 fala (N-D1d):** de JCPs de companhias com aviso no RAD. São 9 companhias nos 10
  eventos, porque o Bradesco PN aparece duas vezes (posições 6 e 7, com o mesmo valor por ação).
- **Os eventos 6 e 7 vêm de cronogramas "previstos".** Os valores e as datas foram publicados
  em dezembro do ano anterior, e o Bradesco "informará ao mercado … quaisquer alterações". Não
  se achou no IPE de 2019 e 2020 um documento mensal que confirme o pagamento. O valor da B3 é
  igual ao previsto.
- **A alíquota das posições 1, 8 e 10 não foi declarada em número.** A classe não depende dela
  (acima).
- **A E-D1a veio depois de abrir os documentos** (§3.1, emenda). Das quatro saídas postas a
  ele, só a leitura estrita leva a `NAO_CONFIRMADO` (tabela no início).

## O que falta

- **Os PDFs no armazém (§3.1: "com o PDF no armazém").** A sessão na nuvem não escreve no R2
  (CLAUDE.md 5-A.7). Quem pode: a sessão local, baixando pelas URLs acima e conferindo cada
  sha256 antes de subir. Registrado na P-115 e em "Ao voltar ao desktop".
