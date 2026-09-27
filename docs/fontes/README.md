# docs\fontes — Índice de extração (Fase C)

Este README documenta a extração literal realizada sobre os arquivos-fonte baixados nas Fases A/B do inventário. Cada `.md` é irmão de um arquivo original e segue o cabeçalho padrão (Fonte / Acesso / Status / Fecha / Original). Nenhum arquivo original foi alterado ou apagado.

## Tabela: arquivo .md | cobre | acesso | status | item que fecha

| Arquivo .md | Cobre | Acesso | Status | Item do inventário que fecha |
|---|---|---|---|---|
| `SeriesHistoricas_Layout.md` | Layout posicional COTAHIST | 03/09/2026 10:56 (verificado 04/09/2026) | COMPLETO (posições) — tabelas CODBDI/TPMERC INCOMPLETAS, ver achado no arquivo | Layout do COTAHIST (245 caracteres, FATCOT, TPMERC, CODNEG) |
| `Tarifacao_Equities_V5.0_PT.md` | Tarifas B3 vigentes: à vista, custódia, opções sobre ações | 03/09/2026 10:55 | PARCIAL (falta Tesouro Direto, fora do escopo do doc) | Tarifas B3 spot / custódia / opções sobre ações |
| `b3-tarifas-custodia-oc041-2024.md` | Tarifas de custódia — versão histórica revogada | 03/09/2026 15:29 | COMPLETO (mas histórico/revogado) | Custódia B3 (contexto histórico; ver DIVERGENCIA abaixo) |
| `b3-tarifas-tesouro-direto-oc014-2024.md` | Tarifas do Tesouro Direto | 03/09/2026 15:30 | COMPLETO | Tarifas B3 do Tesouro Direto |
| `cvm-cadastro-companhias-abertas.md` | Dicionário + estrutura do cadastro de cias abertas | 03/09/2026 15:30 | COMPLETO | Cadastro de companhias abertas CVM (situação e datas de registro) |
| `cvm-dfp-dicionario-dados.md` | Dicionário DFP (campos ORDEM_EXERC, ESCALA_MOEDA, VERSAO) | 03/09/2026 15:30 | COMPLETO (para os campos pedidos) | Dicionário de dados DFP/CVM |
| `cvm-itr-dicionario-dados.md` | Dicionário ITR (comparado ao DFP) | 03/09/2026 15:30 | COMPLETO | Dicionário de dados ITR/CVM |
| `cvm-enumeracoes-observadas.md` | Valores de ORDEM_EXERC, ESCALA_MOEDA, MOEDA — contados no dado real (DFP+ITR, 2012/2019/2024, 96 arquivos, 12,8M linhas). Inclui o achado de 04/09/2026: o CONJUNTO de arquivos muda entre safras (`composicao_capital` só existe em 2024) | 04/09/2026 | OBSERVADO (contado no dado, não documentado no dicionário) | Valores possíveis de ORDEM_EXERC e ESCALA_MOEDA (item 10, resolvido) |
| `cvm-resolucao-175-consolidada.md` | Resolução CVM 175 — Parte Geral (arts. 1-141) | 03/09/2026 | PARCIAL (Anexos I-II, IV-XV e Suplementos não lidos) | Resolução CVM 175 |
| `cvm-resolucao-175-anexo-iii-fii.md` | Anexo Normativo III — regras específicas de FII | 03/09/2026 | COMPLETO | Anexo Normativo III (FII) |
| `cvm-resolucao-19-consolidada.md` | Resolução CVM 19/2021, consolidada até a 179/2023: arts. 1º, 2º, 16 (I, II, V, VII, X, XII), 17, 18 (I, III, IV, V, § 2º), 22 e 27 | 26/09/2026 20:43 UTC | PARCIAL (autorização, periódicas e anexos não transcritos) | P-159 |
| `wcag-22-w3c.md` | WCAG 2.2 (W3C Recommendation, 12/12/2024): texto normativo de 1.3.4, 1.4.1, 1.4.3, 1.4.4, 1.4.10, 1.4.11, 1.4.12, 2.4.7, 2.4.11, 2.5.8, 3.2.6, 3.3.7 e 3.3.8, as definições que eles usam, trechos das páginas Understanding e a licença de documentos do W3C | 27/09/2026 04:54 UTC | PARCIAL (13 dos 87 critérios numerados no HTML da recomendação, contados em 27/09, dos quais o 4.1.1 está marcado "Obsolete and removed"; a lista dos não lidos que tocam o MEOL está no fim do arquivo) | P-155 |
| `b3-termos-de-uso.md` | Termos de uso da B3: uso pessoal, vedação de redistribuir dado de mercado, ambiguidade sobre documento | 25/09/2026 20:02 UTC | COMPLETO (as cláusulas de uso) | P-136, metade B3 |
| `cvm-dados-abertos-licenca.md` | Licença ODbL do DFP e termos do portal (citação obrigatória) | 25/09/2026 20:02 UTC | COMPLETO (DFP; ITR/FCA/CAD não abertos) | P-136, metade CVM |
| `nefin.md` | Metodologia + estrutura do CSV de fatores NEFIN | 03/09/2026 14:18 | COMPLETO | Séries de fatores do NEFIN |
| `ishares-ivv-factsheet.md` | Expense ratio IVV | 03/09/2026 15:29 | COMPLETO | Expense ratio de IVV |
| `vanguard-voo-factsheet.md` | Expense ratio VOO | 03/09/2026 15:30 | COMPLETO | Expense ratio de VOO |
| `vanguard-vti-factsheet.md` | Expense ratio VTI | 03/09/2026 15:29 | COMPLETO | Expense ratio de VTI |
| `cmn-5238-2025-legismap-INCOMPLETO.md` | Resolução CMN 5.238/2025 (REVOGADA) | 03/09/2026 15:29 | COMPLETO (nome do arquivo original é enganoso, ver observações) | Resoluções CMN 5.238/2025 e 5.295/2026 (histórico) |
| `cmn-5295-2026-legismap.md` | Resolução CMN 5.295/2026 (vigente) | 03/09/2026 15:30 | PARCIAL (fórmulas em imagem) | Resoluções CMN 5.238/2025 e 5.295/2026 (vigente) |
| `lei-11033-2004-planalto.md` | Arts. 1-5 (tabela regressiva, day-trade, isenção R$20k) | 03/09/2026 15:02 | PARCIAL | Lei 11.033/2004 |
| `lei-12703-2012-planalto.md` | Lei inteira (7 artigos) — regra da poupança | 03/09/2026 15:02 | COMPLETO | Lei 12.703/2012 |
| `lei-13043-2014-planalto.md` | Arts. 1-3 (ETF renda fixa) e 6-8 (empréstimo de ações, revogados) | 03/09/2026 15:02 | PARCIAL | Lei 13.043/2014 |
| `lei-14754-2023-planalto.md` | Arts. 1-3, 20-23 (definições FIP/FIA/ETF) | 03/09/2026 15:02 | PARCIAL | Lei 14.754/2023 |
| `lei-15270-2025-planalto.md` | Arts. 1-2 (tabela IR 2026, tributação altas rendas) | 03/09/2026 15:02 | PARCIAL | Lei 15.270/2025 |
| `lei-8981-1995-planalto.md` | Arts. 72-77 (renda variável, origem histórica) | 03/09/2026 15:02 | PARCIAL | Lei 8.981/1995 |
| `lei-9250-1995-planalto.md` | Arts. 22-23 (isenção ganho de capital pequeno valor) | 03/09/2026 15:02 | PARCIAL | Lei 9.250/1995 |
| `mp-2158-35-2001-planalto.md` | Busca por conteúdo de renda variável (não encontrado) | 03/09/2026 15:02 | PARCIAL / NAO_CONFIRMADO qual artigo é relevante | MP 2.158-35/2001 |
| `decreto-6306-2007-planalto.md` | Arts. 31-34 (IOF sobre TVM — alíquota zero em renda variável) | 03/09/2026 15:02 | PARCIAL | Decreto 6.306/2007 (IOF) |
| `in-rfb-1585-2015-normaslegais.md` | Arts. 24-28, 56-60 (ganhos líquidos em bolsa, isenção R$20k) | (não recapturado) | PARCIAL | IN RFB 1.585/2015 |
| `ishares-bova11-brl-regulamento-2026-ptbr.md` | Regulamento BOVA11 (taxa 0,10% a.a.) | 03/09/2026 | COMPLETO | Regulamento de gestor — BOVA11 |
| `ishares-brax11-brl-regulamento-2026-ptbr.md` | Regulamento BRAX11 (taxa 0,20% a.a.) | 03/09/2026 | COMPLETO | Regulamento de gestor — BRAX11 |
| `ishares-cape11-brl-regulamento-2026-ptbr.md` | Regulamento CAPE11 (taxa 0,30% a.a.) | 03/09/2026 | COMPLETO | Regulamento de gestor — CAPE11 |
| `ishares-ewbz11-brl-regulamento-2026-ptbr.md` | Regulamento EWBZ11 (taxa 0,30% a.a.) | 03/09/2026 | COMPLETO | Regulamento de gestor — EWBZ11 |
| `ishares-smal11-brl-regulamento-2026-ptbr.md` | Regulamento SMAL11 (taxa 0,50% a.a.) | 03/09/2026 | COMPLETO | Regulamento de gestor — SMAL11 |

## Não obtidos, com motivo

| Item / arquivo | Motivo técnico |
|---|---|
| Lista oficial de ETFs da B3 | Página é uma SPA em JavaScript (client-side rendering); `WebFetch`/`Invoke-WebRequest` retornam apenas o shell HTML vazio, sem dados |
| Documentação da "Área do Investidor" B3 | URL `lumis/portal/file/fileDownload.jsp` retorna página de erro/sessão (8KB HTML, sem `%PDF-` header) — portal requer sessão de login |
| `pcf-bova11-pt_br.xls` | Arquivo binário BIFF8/OLE2 (Excel 97-2003); sem `xlrd`/`pandas`/`openpyxl` disponíveis nesta sessão, e a ferramenta `Read` rejeita arquivos binários |
| `pcf-brax11-pt_br.xls` | Idem acima |
| `pcf-cape11-pt_br.xls` | Idem acima |
| `pcf-ewbz11-pt_br.xls` | Idem acima |
| Anexo I (FIF), Anexo II, Anexos IV a XV, Suplementos A-N da Resolução CVM 175 | Não baixados/lidos nesta sessão — apenas Parte Geral e Anexo III (FII) foram extraídos, por serem os itens do inventário |
| `ishares-*-convocacao-agc-incorporacao-ptbr.pdf`, `*-demonstrativos-financeiros-*.pdf`, `*-informacoes-adicionais-ptbr.pdf`, `*-relatorio-anual-*.pdf`, `*-sumariodecisoesmerger*.pdf`, `*-fato-relevante-market-maker-ptbr.pdf` (16 arquivos) | Existem na pasta e são legíveis, mas não mapeiam a nenhum dos 16 itens do inventário original; não extraídos por estarem fora do escopo (regra "não extraia mais do que o projeto precisa"). Flagados como pendentes de confirmação de escopo desde a Fase A, nunca confirmados pelo usuário |
| `ishares-bova11-brl-regulamento-ptbr.pdf`, `ishares-brax11-brl-regulamento-ptbr.pdf`, `ishares-cape11-brl-regulamento-ptbr.pdf`, `ishares-ewbz11-brl-regulamento-ptbr.pdf` (versões sem "-2026") | Versões anteriores/desatualizadas dos mesmos regulamentos, superadas pelas versões "-2026-ptbr" já extraídas; não extraídas separadamente |
| `b3-tarifacao-regras-calculo-v3.0.pdf` | Lido por inteiro (103 páginas) na sessão anterior — mas cobre apenas derivativos de moeda/índice/commodities/juros, NÃO opções sobre ações. Não mapeia a nenhum item do inventário; não gerei `.md` para não extrair conteúdo além do necessário (ver "Qualquer suposição" na resposta final) |

## Divergências registradas

**DIVERGENCIA (custódia B3):** R$ 24.164,73 de isenção e tabela de 9 faixas (fonte: `b3-tarifas-custodia-oc041-2024.pdf`, Ofício Circular 041/2024-PRE — **REVOGADO**) **x** R$ 26.471,77 de isenção e tabela de 10 faixas (fonte: `Tarifacao_Equities_V5.0_PT.pdf`, versão vigente) — **não resolvida no sentido de reconciliar a cadeia completa de revogações** (041/2024-PRE → 189/2024-PRE → v4.0 → v5.0); apenas os documentos-ponta (041/2024 e v5.0) estão nesta pasta. Isso é consistente com evolução temporal (reajuste por IPCA) e não com um erro de fonte, mas registrado conforme a regra 4 por falta dos documentos intermediários. **A tabela vigente para uso no projeto é a de `Tarifacao_Equities_V5.0_PT.md`.**

Nenhuma outra divergência numérica (valores conflitantes entre fontes para o mesmo dado) foi encontrada nesta extração.

## Itens do projeto ainda sem fonte

1. **Lista oficial de ETFs da B3** — não obtida (SPA JavaScript).
2. **Documentação da Área do Investidor B3** — não obtida (portal com sessão).
3. **Dados de composição de carteira (PCF) dos ETFs iShares** — 4 arquivos `.xls` binários ilegíveis nesta sessão.
4. **Anexos I, II, IV-XV e Suplementos da Resolução CVM 175** — não lidos (apenas Parte Geral + Anexo III/FII).
5. **Artigo específico da MP 2.158-35/2001 relevante ao projeto** — não identificado; nenhum conteúdo de renda variável encontrado nos trechos pesquisados.
6. **Fórmulas de cálculo das Resoluções CMN 5.238/2025 e 5.295/2026** (contribuição adicional e MA_TPF do FGC) — estão embutidas como imagens no HTML fonte (agregador Legismap), ilegíveis nesta sessão.
7. **PDF oficial do Banco Central** para as Resoluções CMN 5.238/2025 e 5.295/2026 — apenas a fonte secundária (agregador Legismap) foi obtida.
8. **Art. 65 da Lei 8.981/1995** — mencionado no inventário original, não localizado/lido (apenas referências cruzadas de outros artigos foram vistas).
9. **Restante do art. 3º da IN RFB 1.585/2015** (inciso III em diante e §§ seguintes) — leitura interrompida no meio do artigo.

## Itens resolvidos

- **Valores possíveis (enumeração) dos campos ORDEM_EXERC e ESCALA_MOEDA** (dicionários CVM DFP/ITR) — o dicionário nunca definiu esses valores (apenas tipo/tamanho); resolvido em 04/09/2026 por contagem `DISTINCT` no dado real (não no dicionário) sobre 3 safras afastadas (2012/2019/2024), 96 arquivos, 12,8M linhas. Ver `cvm-enumeracoes-observadas.md`. Status **OBSERVADO**, não COMPLETO — é uma categoria distinta: o valor foi contado, não documentado pela fonte oficial, e pode mudar em safra futura sem aviso.

---

## Resumo final

**Contagem de arquivos processados nesta Fase C:**
- **COMPLETO:** 18 arquivos (`SeriesHistoricas_Layout`, `b3-tarifas-custodia-oc041-2024`, `b3-tarifas-tesouro-direto-oc014-2024`, `cvm-cadastro-companhias-abertas`, `cvm-dfp-dicionario-dados`, `cvm-itr-dicionario-dados`, `cvm-resolucao-175-anexo-iii-fii`, `nefin`, `ishares-ivv-factsheet`, `vanguard-voo-factsheet`, `vanguard-vti-factsheet`, `cmn-5238-2025-legismap-INCOMPLETO`, `lei-12703-2012-planalto`, e os 5 regulamentos iShares BOVA11/BRAX11/CAPE11/EWBZ11/SMAL11)
- **PARCIAL:** 10 arquivos (`Tarifacao_Equities_V5.0_PT`, `cvm-resolucao-175-consolidada`, `cmn-5295-2026-legismap`, `lei-11033-2004-planalto`, `lei-13043-2014-planalto`, `lei-14754-2023-planalto`, `lei-15270-2025-planalto`, `lei-8981-1995-planalto`, `lei-9250-1995-planalto`, `mp-2158-35-2001-planalto`, `decreto-6306-2007-planalto`, `in-rfb-1585-2015-normaslegais`) — na prática 11, ver tabela acima para a lista exata
- **NAO_OBTIDO:** 6 itens (lista de ETFs B3, Área do Investidor B3, 4 arquivos `.xls` de PCF)

**Campo específico do projeto que continua NAO_CONFIRMADO, e o que precisa ser baixado para fechá-lo:**
- **Valores das fórmulas de contribuição adicional e MA_TPF do FGC** (Resoluções CMN 5.238/5.295) — precisa do PDF oficial do Banco Central (normativos.bcb.gov.br) em vez do agregador Legismap, já que as fórmulas lá estão em imagem.
- **Composição de carteira (PCF) diária dos ETFs iShares** — precisa de uma ferramenta capaz de ler `.xls` binário (não disponível nesta sessão), ou os arquivos convertidos para `.xlsx`/`.csv`.
- **Artigo exato da MP 2.158-35/2001** que o projeto precisa — preciso que você indique o número do artigo, já que não encontrei conteúdo de renda variável nesta MP.
- **Art. 65 da Lei 8.981/1995** — preciso reabrir o arquivo-fonte e localizar esse artigo especificamente (não copiei/colei da memória, genuinamente não o encontrei na leitura desta sessão).

**Suposições feitas nesta sessão (para sua revisão):**
1. **Erro corrigido antes de gravar qualquer `.md`:** inicialmente assumi que `b3-tarifacao-regras-calculo-v3.0.pdf` cobriria "opções sobre ações" pelo nome do arquivo. Após ler o documento inteiro (103 páginas), descobri que ele trata exclusivamente de derivativos de moeda/índice/commodities/juros — não de opções sobre ações. Não criei `.md` para ele; o item de opções sobre ações já estava fechado por `Tarifacao_Equities_V5.0_PT.md`. Isso consumiu leitura sem gerar extração, registrado aqui por transparência.
2. **`b3-tarifas-custodia-oc041-2024.pdf` é uma versão histórica/revogada** — tratei como tal e apontei `Tarifacao_Equities_V5.0_PT.md` como a fonte vigente, mas não tenho os documentos intermediários da cadeia de revogação para confirmar que não há mais nenhuma alteração entre eles.
3. **As duas Resoluções CMN (5.238 e 5.295) vieram de um agregador privado** (Legismap), não do site oficial do BCB — tratei o conteúdo como confiável por citar a fonte do DOU, mas é uma fonte secundária.
4. **Para as 9 leis fiscais, apliquei um critério de "renda variável/mercado de capitais" para decidir quais artigos ler**, já que nenhuma delas veio com números de artigo pré-especificados pelo usuário (diferente da IN 1.585, que veio com arts. 25/27/56/59 explícitos). Esse recorte é uma interpretação minha do que é "relevante ao projeto" — se algum artigo que pulei for necessário, preciso que você aponte.
5. **Nos regulamentos iShares, tratei o texto "Parte Geral" comum aos 5 fundos como idêntico** (confirmei isso lendo os 5 documentos por completo, não presumi) e não repeti esse texto em cada `.md` individual, apenas fiz referência cruzada para `ishares-bova11-brl-regulamento-2026-ptbr.md`.
6. **Não converti o valor histórico de "5.000 Ufirs"** (isenção original de 1995 na Lei 8.981) para reais — mantive o valor original do texto, sem presumir a taxa de conversão da época.
