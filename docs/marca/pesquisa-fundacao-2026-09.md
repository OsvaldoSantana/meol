# Pesquisa de fundação — MEOL

*Destino no repositório: `docs/marca/pesquisa-fundacao-2026-09.md`.*
*Rodada 1 · 20/09/2026 · feita em sessão de chat, com busca na web. Nenhum dado pessoal do usuário entra neste arquivo (U-01).*

*Revisão de 26/09/2026 (decisão dele): os códigos deste documento foram renomeados para não colidir com os achados do projeto, que já tinham C- e R- com outro sentido. O número se mantém; muda só o prefixo. As citações de achados do projeto (F-02, U-01) ficaram como estão. Notas de revisão no fim.*

| de | para | o que é | faixa neste documento |
|---|---|---|---|
| `R-nn` | `RI-nn` | requisito de interface | 01 a 10 (10 códigos) |

---

## 0. Como ler este arquivo

Cada afirmação carrega um status, na mesma régua do `custos.yaml`:

| status | significa aqui |
|---|---|
| `COMPLETO` | lido na fonte primária (relatório, artigo, documento oficial) nesta rodada |
| `PARCIAL` | fonte primária existe, mas a leitura foi por fonte secundária, **ou** a literatura diverge |
| `NAO_CONFIRMADO` | só há fonte secundária, fontes conflitam, ou é inferência minha |
| `OBSERVADO` | contado em material real coletado no projeto (os prints da auditoria de 20/09/2026: contas de terceiros ou de demonstração, **não do autor**; os prints não estão no repositório) |

Cada afirmação também carrega a sua fonte, pelo código entre colchetes (ex.: `[F01]`). A lista das fontes está na §9, com URL.

**O que esta rodada cobre:** o público e o mercado brasileiro (bloco A), as marcas ao redor (bloco B, parcial), o design para leigos (bloco C) e uma primeira fundação de marca (bloco D).

**O que esta rodada NÃO cobre, e fica declarado na §8:** a maior parte das marcas listadas no bloco B, a pesquisa com pessoas, e a verificação jurídica.

---

## 1. Sumário — as dez conclusões que mudam o desenho

1. **O público de entrada é grande e está mal servido.** O perfil "Diversifica" (investe em mais de um produto) soma 17% da população. Aplicado ao universo da pesquisa, são **cerca de 28,6 milhões de pessoas** `PARCIAL` `[F01]`. Ninguém mediu quantas delas se sentem inseguras ao decidir. Essa é a primeira medição que a pesquisa com pessoas precisa fazer.

2. **Quem investe diz buscar segurança, mas quase não vê risco.** Entre investidores, segurança é a vantagem mais citada (44%). Só 7% apontam o risco de perda como desvantagem, e 31% dizem que investir não tem desvantagem nenhuma `COMPLETO` `[F01]`. A primeira queda de preço vai surpreender. **O momento "ver cair" é o ponto crítico da jornada**, e precisa ser desenhado antes de acontecer.

3. **A decisão hoje é terceirizada a pessoas.** O principal meio de decidir é falar com o gerente ou assessor (26%), seguido de amigos e parentes (18%). Influenciadores ficam em 6% `COMPLETO` `[F01]`. O concorrente real do MEOL é **o gerente e o amigo**, não o app.

4. **Um em cada três brasileiros passou por golpe ou fraude, e entre investidores são 42%** `COMPLETO` `[F01]`. Segurança, no Brasil, é também **defesa contra imitação**. Isso vira requisito de produto (RI-08).

5. **Três em cada dez brasileiros de 15 a 64 anos são analfabetos funcionais, e só 10% são proficientes** `COMPLETO` `[F05]`. "Sem jargão" não é estilo, é **condição de acesso**.

6. **Leigos julgam credibilidade pela aparência; especialistas, pelo motivo da empresa.** No estudo de Stanford, 46,1% dos comentários citavam o visual. Especialistas em finanças olhavam foco da informação, motivo da empresa e viés `COMPLETO` `[F11]`. O MEOL precisa das duas coisas: **visual impecável para o leigo, independência verificável para quem já investe.**

7. **Educação financeira funciona, mas a literatura diverge sobre quanto e por quanto tempo** `PARCIAL` `[F06][F07]`. A conclusão de desenho sobrevive às duas leituras: **ensinar dentro da decisão, não num curso à parte.**

8. **A escolha padrão é lida como recomendação.** Na adesão automática estudada por Madrian e Shea, parte dos participantes manteve o padrão por inércia e parte por tomá-lo como conselho de investimento da empresa `COMPLETO` `[F08]`. No MEOL, **qualquer padrão é uma recomendação** e responde à CVM 19. *(confirmada em 26/09/2026 na fonte: [Res. CVM 19](../fontes/cvm-resolucao-19-consolidada.md), art. 1º, caput e § 1º, I e II, e art. 2º — vale para o MEOL oferecido a terceiros como serviço; nota N-CVM)*

9. **Mostrar incerteza em número não custa confiança; mostrar em palavras vagas custa** `COMPLETO` `[F10]`. Faixa numérica sim, "pode variar" não.

10. **O regulador brasileiro já legisla experiência do usuário.** O Banco Central mantém um manual de requisitos mínimos de experiência para o Pix, com capítulo de acessibilidade. A versão de setembro de 2026 proíbe propaganda em comprovantes para reduzir golpes `COMPLETO` `[F13][F14]`. É o padrão de referência para "simples e seguro" no Brasil.

---

## 2. Método e régua

- **Fonte primária** é o documento de quem produziu o dado: o relatório da ANBIMA, o artigo científico, o manual do Banco Central. Imprensa e blogs servem para **achar** a fonte, não para **ser** a fonte.
- **Números derivados** (percentual aplicado a uma população) são marcados `PARCIAL` e mostram a conta.
- **Divergência na literatura** não é resolvida escolhendo o lado conveniente. As duas leituras são registradas, e só vira requisito o que sobrevive às duas.
- **Estudos de fora do Brasil** (Stanford, Madrian e Shea, van der Bles, Robinhood) são evidência sobre comportamento humano, não sobre o brasileiro. A transferência para o Brasil é hipótese até ser testada (§7).

---

## 3. Bloco A — o público e o mercado brasileiro

### A1. Quantos são

| grupo | número | status | fonte |
|---|---|---|---|
| universo da pesquisa (16 anos ou mais) | ~168,1 milhões | `COMPLETO` | `[F01]` |
| investidores em produtos financeiros | 36% · 60,6 milhões | `COMPLETO` | `[F01]` |
| perfil **Caderneta** (só poupança) | 19% · ~31,9 milhões (derivado) | `PARCIAL` | `[F01]` |
| perfil **Diversifica** (mais de um produto) | 17% · ~28,6 milhões (derivado) | `PARCIAL` | `[F01]` |
| perfil **Sem Reserva** | 52% | `COMPLETO` | `[F01]` |
| perfil **Economiza mas não investe** | 12% | `COMPLETO` | `[F01]` |
| CPFs em renda variável na B3 (jun/2026) | 5,7 milhões | `PARCIAL` (imprensa, boletim da B3) | `[F03]` |
| investidores ativos no Tesouro Direto | ~3,5 milhões | `PARCIAL` | `[F03]` |

**Conta dos derivados:** 19% × 168,1 mi = 31,9 mi; 17% × 168,1 mi = 28,6 mi. É uma ordem de grandeza, não uma contagem.

**Leitura para o MEOL.** O público de entrada ("já investe, sem segurança na decisão") está dentro do perfil Diversifica e, em parte, do Caderneta. A fatia insegura **não foi medida por ninguém** `NAO_CONFIRMADO`. É a primeira pergunta da pesquisa com pessoas (§7, H-A1).

### A2. O que o investidor valoriza, e o que ele não vê

Entre investidores `COMPLETO` `[F01]`:

- **Vantagens de investir:** segurança 44%, retorno 33%.
- **Desvantagens:** nenhuma 31%, baixo retorno 25%, esperar para resgatar 8%, **risco de perda 7%**.
- **Destino do retorno:** comprar imóvel 32%, manter aplicado 22%.
- **Por que escolhe um produto** (quem pretende investir em 2026): retorno 37%, segurança 26%, facilidade 15%, **imagem da marca 12%**.

**Diferenças por geração** `COMPLETO` `[F01]`:

- Geração Z e Millennials citam mais o retorno (41%).
- Geração X e Boomers citam mais a segurança (50% e 47%).
- Os mais velhos reclamam de baixo retorno; os mais novos, de ter de esperar para resgatar.

**Achado.** "Segurança" para esse público significa **não ver o saldo cair**, e não compreensão de risco. A carteira da maioria ainda é poupança (61% dos investidores). Quando o MEOL levar alguém da poupança para renda variável, a primeira queda contradiz a expectativa. Daí o requisito RI-04.

### A3. A quem ele recorre para decidir

`COMPLETO` `[F01]`

| meio de decisão | investidores | Geração Z |
|---|---|---|
| gerente ou assessor, pessoalmente | 26% | 15% |
| amigos e parentes | 18% | 23% |
| app ou site do banco/corretora | 11% | — |
| sites de notícias | 11% | — |
| influenciadores | 6% | 11% |

**Canais de informação** (investidores): YouTube 35%, Instagram 27%, televisão 21%, ferramentas de busca 20%, WhatsApp 15%, **assistentes de IA 9%**. A IA já supera Facebook, e-mail, TikTok e rádio `COMPLETO` `[F01]`.

**Achado.** Os quatro concorrentes reais do MEOL são o gerente (que tem conflito, porque distribui), o amigo (que não tem método), o influenciador (que decide pelo carisma) e o assistente de IA genérico (que responde sem procedência). O quarto está crescendo: quem usa IA é mais jovem, de maior renda e mais diversificado `COMPLETO` `[F01]`, que é exatamente o perfil de entrada.

### A4. Como ele executa

Investir pela internet subiu de 48% para 63% em cinco anos. O app do banco é o meio de 46% dos investidores. Entre Boomers, 66% ainda preferem ir ao banco `COMPLETO` `[F01]`.

### A5. Vulnerabilidade e estresse

`COMPLETO` `[F01]`

- **Reserva de emergência:** 31% da população não tem nenhuma. Entre quem tem, 43% a consumiria em até seis meses. Entre investidores, 11% não têm reserva.
- **Estresse financeiro alto:** 47% da população. Estresse médio: 48%.
- **Dívida em atraso:** 29%.
- **Imediatismo** (preferir receber menos agora a esperar um mês por 10% a mais): 44% da população, 38% dos investidores.
- **Apostas online:** 17% apostaram em 2025. **20% dos apostadores veem a aposta como investimento.**

**Leitura.** O motor já trata a reserva como Fase A, antes de qualquer aporte. A pesquisa confirma que essa é a primeira necessidade real de quase um terço da população. Para o leigo, **o primeiro produto do MEOL é a reserva, não a ação.**

### A6. Golpes e fraudes

`COMPLETO` `[F01]`

- 34% da população passou por pelo menos uma situação de golpe ou fraude em 2025. Entre investidores, 42%. Na classe AB, 47%.
- O mais comum: clicar em link falso que imita banco (15%).
- "Falsos investimentos com promessa de retorno alto" aparece entre as situações pesquisadas.

**Leitura.** Para o brasileiro, "parecer seguro" inclui **não parecer golpe**. As estéticas associadas a promessa (retorno garantido, urgência, ostentação) disputam território visual com os golpes. Reforça a hipótese H2 do teste de marca.

### A7. Educação financeira e conhecimento

`COMPLETO` `[F01]`

- 21% da população já fez aula, curso ou palestra de educação financeira; 33% entre investidores; 47% no perfil Diversifica.
- Na pergunta de juros compostos (uma das três de Lusardi e Mitchell), 66% acertaram: 74% entre investidores, 53% entre quem tem só o ensino fundamental.
- A ANBIMA registra que **não dá para afirmar a direção da causa**: se o curso gera o investidor, ou se o investidor procura o curso.

### A8. Alfabetismo funcional

`COMPLETO` `[F05]`

- 29% dos brasileiros de 15 a 64 anos são analfabetos funcionais (7% analfabetos, 22% rudimentares). É o mesmo patamar de 2018.
- Só 10% estão no nível proficiente.
- 60% dos analfabetos funcionais ficaram no nível mais baixo de habilidade digital.
- Entre jovens de 15 a 29 anos, a taxa subiu de 14% para 16%.

**Leitura.** Um produto "para o leigo" no Brasil precisa funcionar para quem lê frases curtas e reconhece preços, mas não lê um texto de três parágrafos. Isso dá os requisitos RI-01 e RI-02.

### A9. Onde o brasileiro perde a confiança

- O Banco Central publica trimestralmente um ranking de reclamações procedentes por milhão de clientes `COMPLETO` `[F15]`.
- Temas frequentes em 2026: segurança e legitimidade de operações com cartão de crédito, e crédito consignado `PARCIAL` `[F16]`.
- No 4º trimestre de 2024, o Nubank ficou na última posição entre os 15 maiores `PARCIAL` `[F17]`.
- Quem liderou o 2º trimestre de 2026 **diverge entre as fontes de imprensa** `NAO_CONFIRMADO` `[F16]`. A consulta tem de ser feita no próprio site do BC.

**Pendência.** O Reclame Aqui não foi lido nesta rodada.

### A10. Mapa emocional da jornada — hipótese de trabalho

Status geral: `PARCIAL`. As evidências vêm de `[F01]` e `[F05]`; as emoções dominantes são **inferência** minha e serão testadas (§7).

| etapa | o que os dados mostram | emoção provável | o que o MEOL faz |
|---|---|---|---|
| **guardar** | 31% sem reserva; estresse alto 47%; imediatismo 44% | culpa, aperto | começa pela reserva, com passos pequenos e sem julgamento |
| **escolher onde** | decide com gerente (26%) e amigos (18%) | insegurança, dependência | uma decisão com o porquê em uma frase |
| **aportar** | 63% executa online | alívio e dúvida ("fiz certo?") | confirmação e registro; o selo do mês |
| **ver cair** | só 7% veem risco de perda | susto, arrependimento, vontade de vender | aviso **antes** da queda: "isto vai acontecer, e o plano já conta com isso" |
| **resgatar** | 8% reclamam de esperar para resgatar | pressa, frustração | prazo e custo de saída mostrados no momento de entrar |

---

## 4. Bloco B — as marcas ao redor

### B1. As marcas financeiras mais valiosas do Brasil

`COMPLETO` `[F04]`

- No Kantar BrandZ 2026, Itaú (US$ 13,2 bi) e Nubank (US$ 12,0 bi) são as duas marcas mais valiosas do país.
- O Nubank teve o maior crescimento: 162% em dois anos. Serviços financeiros foram o destaque da edição, com crescimento médio de 68,7%.
- A Kantar atribui a força do Nubank a transformar **simplicidade e transparência** numa plataforma de uso diário. A do Itaú, a renovação da identidade com disciplina e investimento em IA.

**Leitura.** O mercado brasileiro **já recompensa transparência como marca.** O Nubank provou isso no crédito. O território "transparência na decisão de investimento" ainda está livre na amostra auditada (B3).

### B2. Independência estrutural: o caso Vanguard

`PARCIAL` (documento da própria Vanguard lido por trecho) `[F18]`

A Vanguard é de propriedade dos seus próprios fundos, que são de propriedade dos investidores. Não há dono externo cobrando lucro. A empresa usa isso como argumento de alinhamento de interesse, e diz que é o que sustenta taxas menores.

**Leitura.** A independência que constrói confiança é a **da estrutura**, não a do slogan. O MEOL não tem essa estrutura. O equivalente verificável é **não distribuir produto, não receber comissão e não aceitar anúncio** (achado de 20/09, CVM 19). *(**RETIRADA em 26/09/2026** como atribuição à CVM 19: a norma exige independência e veda remuneração que a prejudique, mas **permite distribuir** com segregação de atividades (art. 18, I e § 2º) e **não fala de anúncio**. As três condições ficam como escolha do MEOL, mais estrita que a norma. Fonte: [Res. CVM 19](../fontes/cvm-resolucao-19-consolidada.md); nota N-CVM)*

### B3. A auditoria visual de 20/09/2026 — resumo

`OBSERVADO` (prints coletados pelo usuário e classificados na sessão; são de contas de terceiros ou de demonstração, **não do autor** — declaração dele em 26/09/2026 — e não estão no repositório)

**12 marcas:** Patek Philippe, Bentley, Apple, Versace, American Express, Nubank, Inter, XP, Bastter, Kinvo, Gorila e Investidor10.

1. **Quadrante vazio:** nenhuma financeira do recorte combina baixa densidade, tom de processo e decisão mensal com procedência.
2. **Um só concorrente direto na decisão mensal personalizada:** o Bastter ("Onde Aportar", e agora "De Onde Retirar").
3. **Erro de formato numérico em 2 das 12 vitrines:** Versace "R$ 16,900"; XP "R$ 70.000.00". **E uma terceira com valor exibido incompatível com quantidade × preço:** Gorila, posição de 45 ações a R$ 25,60 (45 × 25,60 = R$ 1.152,00) exibindo R$ 4.159.382,64 — `NAO_CONFIRMADO` sem o print, que não está no repositório *(revisão de 26/09/2026, nota N-GORILA)*.
4. **Estado vazio exibido como ganho:** o Bastter mostra "▲ R$ 0,00 · 0,00%" em verde numa conta sem dados. É o F-02 na interface.
5. **Exclusividade por patrimônio** (XP: Premium → Unique; Amex: Centurion) contra **pertencimento por método** (proposta para o MEOL).
6. **Guilhochê** como código comum a Patek e Amex: é padrão de segurança de cédula e pode ser gerado por código a partir do hash da decisão.

### B4. O Banco Central como autoridade de experiência do usuário

`COMPLETO` `[F13][F14]`

- O Pix tem **requisitos mínimos obrigatórios de experiência do usuário**, voltados a apps de pessoas físicas por serem "mais sensíveis à padronização". A versão 7.4, de setembro de 2026, entra em vigor em 01/03/2027 e tem capítulo próprio de acessibilidade.
- A mesma versão **proíbe propaganda, ofertas e links em comprovantes de Pix**, para que o comprovante não vire vetor de golpe.

**Leitura.** No Brasil, simplicidade e segurança já têm um padrão de referência escrito pelo regulador. Ler os requisitos do Pix inteiros é tarefa da próxima rodada (pendência P-B4). O princípio da proibição de links serve de modelo direto: **notificação do MEOL não tem link para clicar** (RI-08).

### B5. Marcas listadas e NÃO auditadas nesta rodada

Fica declarado, para que não considerar seja uma decisão e não uma omissão (P6):

- **Bancos:** Bradesco, Banco do Brasil, Caixa, Santander, Itaú Personnalité e Private.
- **Crédito e pagamentos:** PicPay, Mercado Pago, Serasa.
- **Corretoras:** BTG, Rico, Clear, Toro, Nu Invest, Genial.
- **Gestoras:** Verde, SPX, Dynamo.
- **Educação e influência:** Me Poupe, Primo Rico, Suno, Empiricus.
- **Referências de sentimento:** Grand Seiko, Leica, Braun, relógio das ferrovias suíças, Volvo.

Critério de parada da próxima rodada: **saturação.** Três marcas seguidas sem código novo encerram o bloco.

---

## 5. Bloco C — design para o leigo

### C1. Informação em camadas (progressive disclosure)

`PARCIAL` `[F12]`

- A recomendação do Nielsen Norman Group: mostrar primeiro só as opções mais importantes e deixar as avançadas para quando o usuário pedir. Isso melhora aprendizado, eficiência e taxa de erro.
- **Ressalva de evidência:** uma revisão do tema aponta que estudos controlados sobre a técnica são escassos, e que a base é sobretudo prática e estudos de caso `NAO_CONFIRMADO` (fonte secundária em `[F12]`).

**Conclusão de desenho:** as três camadas (decisão → porquê → procedência). A técnica é consenso de prática, não resultado experimental. O teste com pessoas mede se funciona para o MEOL.

### C2. Educação dentro da decisão

`PARCIAL` — a literatura diverge

- **Leitura A** `[F06]`: meta-análise de Fernandes, Lynch e Netemeyer (2014). Intervenções de educação financeira explicam cerca de 0,1% da variação no comportamento, e o efeito decai com o tempo. Os autores defendem educação "no momento certo" (*just-in-time*).
- **Leitura B** `[F07]`: meta-análise posterior de Kaiser, Lusardi, Menkhoff e Urban, com 76 experimentos randomizados. O efeito é pelo menos três vezes maior que o da leitura A, e **não há evidência nem a favor nem contra a decadência** após seis meses.

**O que sobrevive às duas:** ensinar no momento da decisão é o melhor desenho sob a leitura A e não perde nada sob a leitura B. Vira o requisito RI-03. Uma "trilha de cursos" separada **não** vira requisito.

### C3. A escolha padrão

`COMPLETO` `[F08][F09]`

- Madrian e Shea (2001): a adesão automática a planos de previdência aumentou fortemente a participação. Numa das empresas estudadas, a participação dos contratados no primeiro ano chegou a 86% `PARCIAL` (número de apresentação secundária em `[F09]`).
- Os participantes mantiveram a contribuição e o fundo padrão, por **inércia e por tomar o padrão como conselho de investimento** da empresa `COMPLETO` `[F08]`.
- O mesmo relato registra que o percentual padrão de 2% ou 3% foi um número **escolhido para ilustrar** uma norma, e acabou virando o padrão do mercado por acidente `PARCIAL` `[F09]`.

**Leitura para o MEOL, e ela é dupla:**

1. O padrão é a alavanca mais forte que existe para o leigo.
2. Por isso mesmo, **todo padrão do MEOL é uma escolha declarada, com procedência** (P1), e juridicamente é uma recomendação (CVM 19) *(confirmada em 26/09/2026 na fonte: [Res. CVM 19](../fontes/cvm-resolucao-19-consolidada.md), art. 1º, caput e § 1º, I e II, e art. 2º — vale para o MEOL oferecido a terceiros como serviço; nota N-CVM)*. O caso do "2% por acidente" é exatamente o erro que a P1 existe para impedir: um número sem dono virando regra.

### C4. O que a mecânica de jogo fez no Robinhood

`COMPLETO` `[F19][F20]`

- Em 2020, o regulador de valores mobiliários de Massachusetts acusou o Robinhood de usar mecânica de jogo para atrair e manipular investidores inexperientes. Os exemplos: confete na tela, raspadinhas digitais, ações grátis de brinde, notificações e listas de "mais populares" para incentivar operações frequentes.
- O Robinhood removeu o confete em 2021 e, em 2024, fez acordo pagando US$ 7,5 milhões e reformulando as práticas.

**Proibições derivadas** (requisito RI-06): no MEOL não há confete, recompensa por operação, sequência de dias, lista de "mais populares", notificação para operar, nem ranking de usuários.

### C5. Como mostrar incerteza

`COMPLETO` `[F10]`

- Cinco experimentos com 5.780 pessoas, incluindo uma replicação pré-registrada e um teste no site da BBC.
- Comunicar incerteza fez as pessoas perceberem mais incerteza, com **pequena queda de confiança**, e **sobretudo quando a incerteza era verbal**.
- Faixas numéricas praticamente não afetaram a confiança na fonte.

**Regra (RI-05):** "entre R$ 480 e R$ 620", sim; "o valor pode variar", não. Para o leigo, a faixa vem em frase comum, nunca como "IC 95%".

### C6. Credibilidade: o leigo e o especialista olham coisas diferentes

`COMPLETO` `[F11]`

- No estudo de Stanford (2.684 participantes, 100 sites), o visual apareceu em **46,1%** dos comentários sobre credibilidade.
- Em estudo paralelo, **especialistas em finanças** avaliaram primeiro o foco da informação, o motivo da empresa e o viés da informação.

**Leitura.** É a base empírica do posicionamento em duas camadas:

- o **leigo** confia no MEOL pela aparência, e por isso o brandbook não é cosmético;
- o **investidor de entrada** confia pelo motivo, e por isso a independência verificável é argumento de venda.

### C7. Acessibilidade e letramento

`PARCIAL`

Requisitos derivados de A8 e B4. Serão conferidos contra o capítulo de acessibilidade do Pix (P-B4).

- Frases de até cerca de 15 palavras.
- Números grandes, com formatação brasileira.
- Ícone sempre acompanhado de texto.
- Nenhuma decisão que dependa de ler um gráfico.

---

## 6. Bloco D — fundação de marca (primeira versão)

Status geral: `NAO_CONFIRMADO`. É síntese minha a partir dos blocos A a C, e será testada com pessoas.

**Promessa:** confiança na decisão. Não "seu dinheiro seguro", que nenhum produto honesto garante (e a CVM veda garantir rentabilidade *(confirmada em 26/09/2026: [Res. CVM 19](../fontes/cvm-resolucao-19-consolidada.md), art. 18, III, vedação ao consultor)*).

**Três provas, todas verificáveis:**

1. **Registro:** toda decisão datada, com hash, reproduzível. É a herança que o MEOL tem sem fingir idade.
2. **Independência:** não distribui produto, não recebe comissão, não aceita anúncio. É o critério do especialista (C6) e da CVM. *(**RETIRADA em 26/09/2026** a parte "e da CVM": a norma não veda distribuir, que permite com segregação (art. 18, I e § 2º), nem fala de anúncio; veda remuneração que prejudique a independência (art. 18, V). As três condições são escolha do MEOL. Fonte: [Res. CVM 19](../fontes/cvm-resolucao-19-consolidada.md); nota N-CVM)*
3. **Recusa:** quando falta dado, o MEOL diz "sem dado" em vez de chutar. É o F-02 como virtude pública.

**O que o MEOL não reivindica:** herança, tradição, exclusividade por patrimônio, retorno.

**Pertencimento:** pelo método, aprendido no uso. "Membro desde", como **registro de decisões**, nunca como sequência de dias.

**Tom:** colega técnico para quem já investe; frase curta e concreta para o leigo. As duas vozes são a mesma marca em camadas diferentes.

**Metáfora:** o relógio de precisão, não o carro esportivo. Confia-se porque marca a hora certa e dá para conferir.

---

## 7. Requisitos derivados e hipóteses para a pesquisa com pessoas

### Requisitos

| código | requisito | origem |
|---|---|---|
| **RI-01** | nenhuma decisão depende de ler gráfico ou jargão; a camada 1 é uma frase curta | A8, C7 |
| **RI-02** | formatação numérica brasileira impecável, testada automaticamente | A8, B3 |
| **RI-03** | educação dentro da decisão; nenhuma trilha de curso separada | C2 |
| **RI-04** | aviso de queda **antes** do primeiro aporte em renda variável, com o tamanho histórico da queda | A2, A10 |
| **RI-05** | incerteza em faixa numérica escrita em linguagem comum; nunca "pode variar" | C5 |
| **RI-06** | proibidos: confete, recompensa por operação, sequência de dias, "mais populares", notificação para operar, ranking | C4 |
| **RI-07** | todo padrão é escolha declarada, com procedência e responsável | C3, P1 |
| **RI-08** | notificações e comprovantes sem link clicável | A6, B4 |
| **RI-09** | a primeira jornada do leigo é a reserva | A5 |
| **RI-10** | estado vazio mostra "sem dado" e o motivo, nunca um zero colorido | B3, F-02 |

### Hipóteses (atualiza o pré-registro de 20/09)

- **H-A1:** entre quem já investe, existe uma fatia mensurável que se sente insegura, medida por três sinais: paralisia (dinheiro parado), dependência (decide só por indicação) e arrependimento (compra ou venda impulsiva).
- **H-A2:** o primeiro susto com queda é um evento comum entre quem saiu da poupança, e está associado a abandono.
- **H-C1:** o leigo entende a camada 1 sem ajuda (teste de 5 segundos: consegue dizer o que fazer este mês?).
- **H-C2:** a faixa numérica em linguagem comum não reduz a confiança, contra uma versão verbal vaga (replicação de C5 no Brasil).
- **H1 a H4 do teste de marca:** mantidas.

---

## 8. Limitações declaradas (P5)

1. **Bloco B está incompleto.** 25 marcas listadas não foram auditadas (B5). A conclusão "quadrante vazio" vale para a amostra de 12.
2. **Transferência internacional.** C3, C4, C5 e C6 vêm de estudos nos EUA e no Reino Unido. A transferência para o Brasil é hipótese (§7).
3. **O ranking do BC foi lido por imprensa**, com divergência sobre o 2º trimestre de 2026. O Reclame Aqui não foi lido.
4. **Requisitos do Pix:** li o índice e a notícia da versão 7.4, não o capítulo de acessibilidade.
5. **Números derivados** (§3, A1) aplicam percentuais a uma população estimada. São ordem de grandeza.
6. **Bloco D é síntese**, sem validação externa.
7. **Nenhuma verificação jurídica.** As menções à CVM 19 retomavam um achado de 20/09 que não estava no repositório. Em 26/09/2026 a resolução foi lida na fonte primária e transcrita em [Res. CVM 19](../fontes/cvm-resolucao-19-consolidada.md): duas teses foram confirmadas com escopo e a de que as três condições de independência são "o critério da CVM" foi retirada (nota N-CVM). A leitura é do texto, **não é parecer**; o enquadramento do MEOL é da P-158.
8. **Data.** Tudo o que é dado de mercado (B3, Kantar, BC) envelhece. Os números valem para setembro de 2026 (§8 do CLAUDE.md: "números que envelhecem").

---

## 9. Pendências e próximo passo

| código | pendência | classe |
|---|---|---|
| P-B5 | auditar as marcas de B5, com regra de saturação | `DECISAO_DE_DESENHO` |
| P-B4 | ler os requisitos mínimos de experiência do Pix (v7.4) inteiros, em especial acessibilidade | `DECISAO_DE_DESENHO` |
| P-A9 | ranking do BC direto na fonte e leitura do Reclame Aqui por categoria | `DECISAO_DE_DESENHO` |
| P-A1 | medir a fatia insegura (H-A1) | `DECISAO_DE_DESENHO` |

**Próximo passo proposto: P-B5, a segunda rodada de marcas**, com os requisitos RI-01 a RI-10 como lente de auditoria.

- **Por que antes das outras:** fecha o bloco que esta rodada deixou mais aberto, e as marcas de B5 incluem exatamente os concorrentes reais do achado A3 (bancos com gerente e educação e influência).
- **O que destrava:** a pesquisa com pessoas, cujos estímulos dependem do mapa completo.
- **O que impede hoje:** nada. É pesquisa de fonte pública, e não é engenharia (Regra 2 da skill de próximo passo).

---

## 10. Fontes

Acesso em 20/09/2026, salvo indicação.

- **[F01]** ANBIMA / Datafolha. *Raio X do Investidor Brasileiro, 9ª edição* (abril de 2026). 5.832 entrevistas, campo de 4 a 21/11/2025, margem de 1 p.p. — https://www.anbima.com.br/data/files/BE/05/B0/55/1EABD91008E6DAD9F82BA2A8/Raio-X-do-Investidor-9-edicao.pdf
- **[F02]** ANBIMA. Notícia de lançamento da 9ª edição (23/04/2026) — https://www.anbima.com.br/pt_br/noticias/anbima-lanca-a-nona-edicao-do-raio-x-do-investidor-brasileiro-36-da-populacao-aplica-em-produtos-financeiros.htm
- **[F03]** InfoMoney, sobre o boletim da B3 "Análise da Evolução dos Investidores na B3", 2º tri/2026 (17/09/2026) — https://www.infomoney.com.br/onde-investir/etfs-ganham-140-mil-investidores-no-ano-e-ja-somam-862-mil-cpfs/ · boletim do 4º tri/2025: https://static.poder360.com.br/2026/05/Uma-analise-da-evolucao-dos-investidores-na-B3-1.pdf
- **[F04]** Kantar. *Kantar BrandZ Brasil 2026* (26/08/2026) — https://www.kantar.com/brazil/inspiration/marcas/quais-sao-as-marcas-brasileiras-mais-valiosas-de-2026 · crescimento médio de 68,7% dos serviços financeiros, via Propmark: https://propmark.com.br/?p=128722
- **[F05]** INAF 2024 (Ação Educativa / Conhecimento Social), via UNICEF Brasil (05/05/2025) — https://www.unicef.org/brazil/comunicados-de-imprensa/analfabetismo-funcional-nao-apresenta-melhora-e-alcanca-29-por-cento-dos-brasileiros-mesmo-patamar-de-2018-aponta-novo-levantamento-do-inaf · detalhes em Poder360: https://www.poder360.com.br/poder-educacao/29-dos-jovens-e-adultos-brasileiros-sao-analfabetos-funcionais/ · proficiente 10%: https://www.gazetadopovo.com.br/vida-e-cidadania/quase-30-dos-brasileiros-sao-analfabetos-funcionais-aponta-estudo/ · habilidade digital: https://www.publishnews.com.br/materias/2025/05/06/indice-de-alfabetizados-em-nivel-proficiente-segue-o-mesmo-no-brasil-ha-23-anos
- **[F06]** Fernandes, Lynch & Netemeyer (2014). *Financial Literacy, Financial Education, and Downstream Financial Behaviors.* Management Science 60(8):1861–1883 — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2333898
- **[F07]** Kaiser, Lusardi, Menkhoff & Urban. *Financial Education Affects Financial Knowledge and Downstream Behaviors* (NBER w27057) — https://www.nber.org/system/files/working_papers/w27057/w27057.pdf
- **[F08]** Madrian & Shea (2001). *The Power of Suggestion.* Quarterly Journal of Economics 116(4):1149–1187 — https://www.nber.org/papers/w7682
- **[F09]** Apresentação de Z. J. Wang ao legislativo do Oregon (participação de 86%) — https://apps.oregonlegislature.gov/liz/2017R1/Downloads/CommitteeMeetingDocument/102060 · entrevista de B. Madrian à ThinkAdvisor (2015): https://thinkadvisor.com/2015/08/31/brigitte-madrians-power-of-suggestion-and-how-it/?amp=1
- **[F10]** van der Bles, van der Linden, Freeman & Spiegelhalter (2020). PNAS 117(14):7672–7683 — https://research.rug.nl/en/publications/the-effects-of-communicating-uncertainty-on-public-trust-in-facts/
- **[F11]** Fogg et al. (2002/2003). *How Do People Evaluate a Web Site's Credibility?* Consumer Reports WebWatch — https://advocacy.consumerreports.org/research/how-do-people-evaluate-a-web-sites-credibility · estudo com especialistas, resumo em: https://humanfactors.com/newsletters/key_research_findings_related_to_user_centered_design_2002_2003.asp
- **[F12]** Nielsen Norman Group. *Progressive Disclosure* — https://www.nngroup.com/videos/progressive-disclosure/ · ressalva de evidência (secundária): https://skills.cat/skills/bfmcneill/agi-marketplace/progressive-disclosure
- **[F13]** Banco Central do Brasil. *Requisitos Mínimos para a Experiência do Usuário* (Pix), v7.4, set/2026 — https://static.poder360.com.br/uploads/2026/09/requisitos-minimos-experiencia-usuario-pix.pdf · v7.1: https://www.bcb.gov.br/content/estabilidadefinanceira/pix/Regulamento_Pix/versoes_futuras/IV_RequisitosMinimosparaExperienciadoUsuario-versao7-1.pdf
- **[F14]** Money Times, sobre a proibição de propaganda em comprovantes do Pix (03/09/2026) — https://www.moneytimes.com.br/bc-proibe-propagandas-e-ofertas-comerciais-em-comprovantes-de-pagamento-do-pix/
- **[F15]** Banco Central. *Ranking de Reclamações* (página, cópia de 22/01/2026) — https://static.poder360.com.br/2026/01/ranking-reclamacoes-bc-22jan2026.pdf
- **[F16]** Let's Money e Finsiders, sobre o ranking do 2º tri/2026 (divergentes) — https://www.letsmoney.com.br/noticias/bradesco-ranking-reclamacoes-bc-2tri/ · https://finsidersbrasil.com.br/?p=371286
- **[F17]** Finsiders, sobre o ranking do 4º tri/2024 — https://finsidersbrasil.com.br/regulamentacao/pagbank-inter-c6-e-99pay-lideram-reclamacoes-no-quarto-trimestre/
- **[F18]** Vanguard. *The Vanguard effect* (jan/2026) — https://www.vanguard.ca/content/dam/intl/americas/canada/en/documents/ABVA_012026_ENG_sq_sc.pdf
- **[F19]** Secretary of the Commonwealth of Massachusetts, acordo com o Robinhood (18/01/2024) — https://business.cch.com/srd/left-story.pdf · acusação de 16/12/2020: https://www.napa-net.org/sites/napa-net.org/files/2020.12.16%20Galvin%20Charges%20Robinhood%20over%20Gamification.pdf
- **[F20]** CNBC. Robinhood remove o confete (31/03/2021) — https://www.cnbc.com/2021/03/31/robinhood-gets-rid-of-confetti-feature-amid-scrutiny-over-gamification.html

---

## Notas de revisão

*26/09/2026 — trazido do Projeto no claude.ai para o repositório.*

- **N-COD.** C-nn → MC-nn e R-nn → RI-nn, só neste documento (tabela no cabeçalho). Motivo: os achados do projeto sobre o fator, o ajuste de proventos, a moeda e a ordem dos portões já usavam esses mesmos números com os prefixos C- e R-, e outros C/R já existiam em outros arquivos com outro sentido; os instrumentos `achados_ancorados` e `codigos_preservados` contariam todos como achados. Guardado por `auditoria/test_codigos_de_marca.py`.
- **N-GORILA.** O item do Gorila deixou de ser "erro de formato": o formato está certo, e o que não bate é o valor exibido contra quantidade × preço (45 × 25,60 = 1.152 contra 4.159.382,64). Fica `NAO_CONFIRMADO` enquanto o print não estiver no repositório. A contagem de erros de formato passa de 3 para 2 das 12 vitrines.
- **N-PRINTS.** A procedência dos prints da auditoria de 20/09 foi declarada: contas de terceiros ou de demonstração, não do autor (declaração dele, 26/09/2026). Nenhum número deles descreve o dinheiro do autor (D-01).
- **N-CVM.** O "achado de 20/09" sobre a Resolução CVM 19 só existia no chat daquele dia. Toda afirmação apoiada nele passou a `NAO_CONFIRMADO` em 26/09/2026 e, no mesmo dia, foi conferida no texto consolidado da resolução, lido na fonte primária ([Res. CVM 19](../fontes/cvm-resolucao-19-consolidada.md), com URL, data de acesso e sha256). **Confirmadas:** o padrão individualizado é recomendação no sentido do art. 1º (§ 1º, I e II) e a atividade é privativa de consultor autorizado (art. 2º), **para o MEOL oferecido a terceiros como serviço**; e a vedação de garantir rentabilidade (art. 18, III). **Retirada:** que "não distribuir, não receber comissão e não aceitar anúncio" seja o critério da CVM. A norma permite distribuir com segregação (art. 18, I e § 2º) e não fala de anúncio; as três ficam como escolha do MEOL. O texto original das frases retiradas continua onde estava, com a retratação ao lado. Nada disto é parecer jurídico (P-158).
