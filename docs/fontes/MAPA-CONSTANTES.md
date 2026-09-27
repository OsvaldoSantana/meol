# Mapa de Constantes — `custos.yaml` → fonte

Fonte: varredura das 55 constantes de `alocacao/custos.yaml` contra os 32 `.md` de `docs/fontes/`
Acesso: 05/09/2026
Status: OBSERVADO — cada linha diz o que foi CONFERIDO no texto, não o que se supõe
Fecha: a lacuna `.md` → chave do `custos.yaml` (o README mapeia `.md` → item do inventário, não `.md` → constante)
Metodo: para cada constante, leitura do campo `fonte`, localização do documento correspondente e **conferência do número no trecho literal**. Busca automática por valor foi usada só para gerar candidatos e descartada como prova — `0,01` casa em quase todo documento.

---

## Veredito em uma linha

**Nenhuma divergência de valor.** Toda constante cujo trecho-fonte existe no corpo dos `.md` bate exatamente com o YAML — incluindo as 10 faixas de custódia da B3, conferidas uma a uma.

Mas a varredura achou uma categoria que a tarefa não previa, e ela é a informação real deste documento.

## As cinco situações (e por que são cinco, não três)

| situação | o que significa | quantas |
|---|---|---|
| `RASTREADA` | valor conferido no trecho literal de um `.md` nomeado | **26** |
| `CITADA_NAO_TRANSCRITA` | o `fonte` nomeia documento e artigo reais, mas **esse trecho não está em nenhum `.md`** | ~~6~~ → **0** (fechadas em 05/09) |
| `FONTE_EXTERNA` | fonte legítima que não é — nem deveria ser — um `.md` | **16** |
| `SEM_FONTE` | campo `fonte` ausente | **7** |
| `DIVERGENTE` | valor do YAML difere da fonte | **0** |

`CITADA_NAO_TRANSCRITA` é a categoria nova, e é o achado. Não é erro de valor e não é ausência de fonte — é uma citação que **parece** procedência e não é verificável. Quem lê `fonte: "Lei 14.754/2023 art. 2o, §1o"` conclui que alguém leu o art. 2º §1º. Ninguém leu: o `.md` dessa lei transcreve os arts. 1º, 20, 21, 22 e 23, e diz em suas próprias Observações que os arts. 4º a 19 não foram lidos.

`FONTE_EXTERNA` também é distinção necessária. A tarefa presumia que toda constante deveria apontar para um `.md`. Não deveria: `macro.cdi_aa` vem da série 4389 do BCB — um número que muda todo dia, não um documento. Exigir `.md` para ele produziria um arquivo falso. O que essas 16 precisam é URL + data + prazo curto, não um `.md`.

---

## RASTREADA — 26 constantes

### B3 · `Tarifacao_Equities_V5.0_PT.md`

| chave | valor | trecho | conferido |
|---|---|---|---|
| `b3.custodia_rv_isencao` | 26 471,77 | item 4.2.3, linha de isenção | literal: "contas com valor inferior a R$26.471,77" |
| `b3.custodia_rv_faixas` | 10 faixas | item 4.2.3, tabela | **as 10 faixas, uma a uma**: 0,0500 / 0,0400 / 0,0200 / 0,0130 / 0,0072 / 0,0032 / 0,0025 / 0,0020 / 0,0015 / 0,0005 % |
| `b3.manutencao_conta_inativa` | 3,82 | item 4.2.2 | "R$3,82 por mês, a partir do 61º mês" |
| `b3.vista_total_pct` | 0,0300% | item 1.2.3 | **divergência já declarada no YAML** — a v5.0 decompõe 0,00500% + 0,02240% = 0,0274%; o YAML mantém 0,0300% (o maior) com o bloco `divergencia`. Registrada, não silenciosa. |

### Tesouro · `b3-tarifas-tesouro-direto-oc014-2024.md`

| chave | valor | trecho |
|---|---|---|
| `tesouro.custodia_aa` | 0,20% a.a. | OC 014/2024-VPC |
| `tesouro.isencao_selic` | 10 000,00 | item 1.1 |
| `tesouro.periodicidade` | netting pro rata | vigente desde 31/12/2024; revoga OC 137/2023-PRE |

### ETF brasileiros · regulamentos iShares (vigência 21/05/2026)

| chave | valor | `.md` | trecho |
|---|---|---|---|
| `etf.BOVA11` | 0,10% | `ishares-bova11-…` | tabela comparativa e item 5.1 do Anexo |
| `etf.BRAX11` | 0,20% | `ishares-brax11-…` | idem |
| `etf.CAPE11` | 0,30% | `ishares-cape11-…` | idem |
| `etf.EWBZ11` | 0,30% | `ishares-ewbz11-…` | "Valor da Taxa: 0,30% ao ano (base 252 dias)" |
| `etf.SMAL11` | 0,50% | `ishares-smal11-…` | idem |
| `etf.custodia_interna_ishares` | 0,025% | os 5 regulamentos | idêntica nos cinco — achado F-01 |

### ETF americanos · factsheets

| chave | valor | `.md` |
|---|---|---|
| `etf.IVV` | 0,03% | `ishares-ivv-factsheet.md` |
| `etf.VOO` | 0,03% | `vanguard-voo-factsheet.md` |
| `etf.VTI` | 0,03% | `vanguard-vti-factsheet.md` |

### Tributação · `lei-11033-2004-planalto.md`

| chave | valor | artigo | conferido |
|---|---|---|---|
| `tributacao.ir_rf_faixas` | 22,5 / 20 / 17,5 / 15 % | art. 1º, I a IV | as quatro faixas, literais |
| `tributacao.ir_acao` | 15% | art. 2º, II | "15% nas demais hipóteses" |
| `tributacao.irrf_dedo_duro` | 0,005% | art. 2º, §1º | "à alíquota de 0,005% (cinco milésimos por cento)" |
| `tributacao.isencao_mensal` | 20 000,00 | art. 3º, I | "igual ou inferior a R$ 20.000,00" |

### Tributação · `lei-13043-2014-planalto.md` + `in-rfb-1585-2015-normaslegais.md`

| chave | valor | artigo |
|---|---|---|
| `tributacao.ir_etf_rf_faixas` | 25 / 20 / 15 % | Lei 13.043 art. 2º, I–III e IN 1.585 art. 28 — texto idêntico nos dois, confirmação cruzada |

---

## CITADA_NAO_TRANSCRITA — ~~6~~ 0 · **fechada em 05/09/2026**

> **Todas as seis foram fechadas** buscando o texto na fonte pública. Cinco eram
> lacuna de leitura e foram transcritas; **uma era citação errada e foi corrigida.**
>
> | constante | desfecho |
> |---|---|
> | `iof_investimento` 1,10% | transcrito — Decreto 12.499/2025, art. 15-B, XXI-A |
> | `iof_conta` 3,5% | transcrito — art. 15-B, XXI |
> | `iof_repatriacao` 0,38% | transcrito — art. 15-B, XXV, "entrada de recursos" |
> | `ir_exterior` 15% | transcrito — Lei 14.754 art. 2º §1º, ajuste anual, sem dedução |
> | `come_cotas_etf` false | transcrito — art. 18, II **c/c** art. 24 §1º (precisa dos dois) |
> | `ir_fii` 20% | **CORRIGIDO** — a base é Lei 8.668/1993 art. 18, não a IN 1.585 art. 56 |
>
> Um teste (`test_nenhuma_constante_fica_com_trecho_nao_conferido`) impede que a
> categoria volte em silêncio.

### O que a categoria era, e por que ela precisava existir

O `fonte` nomeia documento e artigo que existem. O `.md` desse documento **não contém esse trecho**, e em três dos casos o próprio `.md` declara que a parte relevante não foi lida.

| chave | valor | fonte declarada | por que não está conferida |
|---|---|---|---|
| `exterior.iof_investimento` | 1,1% | Decreto 6.306/2007 art. 15-B, XXI-A | `decreto-6306-…md` transcreve os arts. 31–34 (títulos e valores mobiliários). O art. 15-B é do capítulo de **câmbio**, que o `.md` diz explicitamente não ter lido. |
| `exterior.iof_conta` | 3,5% | idem, XXI | idem |
| `exterior.iof_repatriacao` | 0,38% | idem, XXV | idem. O único "0,38%" no `.md` está no art. 32-D, **outro artigo**, e ali marcado `NAO_CONFIRMADO`. |
| `tributacao.ir_exterior` | 15% | Lei 14.754/2023 art. 2º, §1º | `lei-14754-…md` transcreve os arts. 1º, 20, 21, 22, 23. O art. 2º §1º não está lá. |
| `tributacao.come_cotas_etf` | `false` | Lei 14.754/2023 art. 18, II e art. 24, §1º | os arts. 18 e 24 **não aparecem** no `.md` — que declara não ter lido os arts. 4º a 19. |
| `tributacao.ir_fii` | 20% | IN RFB 1.585/2015 art. 56 | o art. 56 **está** transcrito e **não menciona 20%** — ele define o âmbito de ganhos líquidos. Os "20%" que existem no arquivo são do art. 28 (ETF de renda fixa), assunto diferente. |

**Os seis valores são provavelmente corretos.** 15% sobre ganho no exterior, ausência de come-cotas em ETF e 20% sobre ganho de FII são consequências conhecidas dessas leis. Mas "provavelmente correto porque eu sei" é exatamente o que este projeto recusa: é a diferença entre procedência e memória. Enquanto o trecho não for transcrito, o status honesto não é `COMPLETO`.

O caso do `ir_fii` é o mais nítido: a citação aponta para um artigo que **foi lido** e que **não diz o que a citação afirma**. Não é lacuna de leitura — é citação errada.

---

## FONTE_EXTERNA — 16 constantes

Fonte legítima que não é documento arquivável. Estas não precisam de `.md`; precisam de URL, data e prazo curto.

| grupo | chaves | fonte | natureza |
|---|---|---|---|
| macro | `cdi_aa`, `selic_aa`, `poupanca_am` | séries BCB/SGS 4389, 432, 25 | série temporal, muda diariamente — já têm `expira` |
| ETF (gestor) | `PIBB11`, `DIVO11`, `B5P211` | Itaú Asset | página de produto |
| ETF (gestor) | `NASD11` | XP Vista Asset | idem |
| ETF (gestor) | `AREA11` | "gestor" — **fonte genérica demais** | idem |
| ETF (gestor) | `IVVB11` | BlackRock Brasil, página do produto | idem |
| ETF (gestor) | `HASH11` | Hashdex, "taxa máxima global 1,3% a.a." | idem |
| corretagem | `zero`, `safra_terra`, `caixa_fixa`, `caixa_pct`, `xp_etf_pct` | sites das corretoras | tabela comercial, muda sem aviso |
| exterior | `spread_avenue_melhor`, `spread_avenue_inicial`, `spread_nomad_n1`, `spread_nomad_n5`, `spread_wise`, `vest_stablecoin.spread` | sites e medição ao vivo | idem |

`exterior.spread_wise` merece nota: fonte é "medição ao vivo conferida contra PTAX". Isso é **observação**, não documento — o status natural dela é `OBSERVADO`, não `COMPLETO`.

---

## SEM_FONTE — 7 constantes

| chave | valor | status atual | o que fecha |
|---|---|---|---|
| `etf.BOVV11` | — | `NAO_CONFIRMADO` | ~~site do gestor bloqueia robô; visita manual~~ **27/09/2026, escada subida (§5-B.18) sem resolver da nuvem — P-05.** escada: (1) `curl` em `itnow.com.br` e `itnow.com.br/bovv11/` → HTTP 403 do `AkamaiGHost` (a WAF do site, não o proxy da sessão); (2) Wayback: a API aponta a cópia `20260513194558` (status 200), mas `web.archive.org` fecha o túnel desta sessão (`ws_closed_mid_exchange`, 4 de 4); (3) CVM: o fundo é o It Now Ibovespa (CNPJ 21.407.758/0001-19, FIIM, em funcionamento, no `registro_fundo_classe`), que **não tem campo de taxa**; o `extrato_fi` só cobre FIF; o `cad_fi` só o tem cancelado; o FundosNet devolve 0 documentos para o CNPJ (controle com um FII devolve); (4) sessão local, roteiro na P-05. O número de 06/09 (0,10% total, PARCIAL, de subagente) segue sem conferência de trecho (P-50) |
| `etf.IMAB11` | — | `NAO_CONFIRMADO` | regulamento do fundo |
| `etf.ACWI11` | — | `NAO_CONFIRMADO` | regulamento / página do produto |
| `exterior.vest_stablecoin.iof` | — | `NAO_CONFIRMADO` | tratamento de IOF em stablecoin |
| `b3.quem_paga_custodia` | — | `NAO_CONFIRMADO` | **ver abaixo — não é falta de fonte, é falta de definição** |
| `b3.custodia_rv_interpretacao` | `deducao` | `PARCIAL` | não é dado: é **escolha de interpretação**. Deveria declarar-se como tal, não esperar fonte. |
| `corretagem.xp_swing` | 4,90 | `PARCIAL` | página de corretagem da XP |

### `b3.quem_paga_custodia` — fura a P1 pelo lado que ninguém olha

É `NAO_CONFIRMADO` e **não declara `bloqueia` nada**. As outras quatro `NAO_CONFIRMADO` declaram. Um insumo não confirmado do qual nenhum cálculo se recusa a depender é um insumo que a doutrina não protege: ele não bloqueia porque ninguém o lê, e se um dia alguém ler, lerá `None`.

Duas saídas, e é decisão sua: ou ele bloqueia algo e precisa dizer o quê, ou não é insumo e sai do `custos.yaml`.

---

## Advertência

Este mapa registra **o que foi conferido em 05/09/2026**, contra os `.md` que existiam nessa data. Ele não é permanente por três motivos:

1. **`.md` novo muda o mapa.** Se alguém transcrever o art. 15-B do Decreto 6.306, três linhas saem de `CITADA_NAO_TRANSCRITA` para `RASTREADA`.
2. **Fonte externa envelhece sem aviso.** Uma corretora muda a tabela e nada aqui pisca. É por isso que as 16 precisam de prazo curto, não de `.md`.
3. **`RASTREADA` fala do texto, não do mundo.** Que o número esteja no `.md` prova que a transcrição está fiel. Não prova que a B3 não publicou uma revisão nova — e a v5.0 já sucedeu o OC 041/2024, que sucedeu outro.

**Regra para quem mantiver:** ao acrescentar constante, escolher a situação **antes** de escrever o `fonte`. Citação que aponta para trecho não lido é pior que campo vazio — o campo vazio é honesto sobre o que não se sabe.
