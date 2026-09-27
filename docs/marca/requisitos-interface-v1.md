# Requisitos de interface do MEOL — v1

*Destino no repositório: `docs/marca/requisitos-interface-v1.md`.*
*20/09/2026. Consolida RI-01 a RI-21, derivados de três rodadas de pesquisa.*
*27/09/2026, v1.1: RI-22 a RI-34, da WCAG 2.2 lida na fonte ([transcrição](../fontes/wcag-22-w3c.md); P-155). Tema E da §1.*

*Revisão de 26/09/2026 (decisão dele): os códigos deste documento foram renomeados para não colidir com os achados do projeto, que já tinham C- e R- com outro sentido. O número se mantém; muda só o prefixo. As citações de achados do projeto (F-02) ficaram como estão. Notas de revisão no fim.*

| de | para | o que é | faixa neste documento |
|---|---|---|---|
| `R-nn` | `RI-nn` | requisito de interface | 01 a 21 (21 códigos) |

---

## 0. Como ler este documento

Este é o **contrato de interface**: o que qualquer tela do MEOL precisa cumprir, qualquer que seja a direção visual escolhida depois. Ele não descreve telas. Descreve regras que as telas têm de passar.

Cada requisito traz:

- **enunciado** — a regra, em uma frase;
- **por quê** — a evidência que a sustenta, com o código da fonte nos relatórios de origem (`[F..]` rodada 1, `[G..]` rodada 2, `[H..]` Pix e pendências; desde a v1.1, `[WCAG n.n.n]` é o critério de sucesso da WCAG 2.2, transcrito em [`docs/fontes/wcag-22-w3c.md`](../fontes/wcag-22-w3c.md));
- **status da evidência** — mesma régua do `custos.yaml`: `COMPLETO`, `PARCIAL`, `NAO_CONFIRMADO`;
- **verificação** — como saber se a regra foi cumprida. Três tipos: **teste** (automático, roda no CI), **revisão** (checklist humano por tela) e **pesquisa** (só se decide com pessoas).

**A regra de ouro deste arquivo:** requisito sem verificação é intenção, não requisito. Se não dá para testar nem revisar, ele volta para a pesquisa.

**Numeração é estável.** Um requisito nunca é renumerado. Se cair, vira `REVOGADO` com a data e o motivo, e o número não é reaproveitado.

**Origem dos documentos:**

- rodada 1 — [`docs/marca/pesquisa-fundacao-2026-09.md`](pesquisa-fundacao-2026-09.md)
- rodada 2 — [`docs/marca/pesquisa-marcas-rodada2-2026-09.md`](pesquisa-marcas-rodada2-2026-09.md)
- Pix e pendências — [`docs/marca/pesquisa-pix-e-pendencias-2026-09.md`](pesquisa-pix-e-pendencias-2026-09.md)

---

## 1. Os requisitos, por tema

*Até a v1, "Os 21 requisitos". A v1.1 acrescentou o tema E.*

### A. Compreensão e linguagem

**RI-01 — nenhuma decisão depende de ler gráfico ou jargão; a camada 1 é uma frase curta.**
*Por quê:* 29% dos brasileiros de 15 a 64 anos são analfabetos funcionais e só 10% são proficientes `[F05]`; o Pix recomenda descrições curtas e diretas `[H01]`; a legibilidade é pilar de produto na Grand Seiko `[H05]` e o essencial é doutrina em Leica e Braun `[H04][H06]`. `COMPLETO`
*Verificação:* **teste** — toda frase da camada 1 com no máximo 15 palavras e sem termo do glossário técnico não definido em tela; **pesquisa** — teste de 5 segundos (a pessoa diz o que fazer neste mês).

**RI-02 — formatação numérica brasileira impecável, testada automaticamente.**
*Por quê:* duas das doze vitrines auditadas erram formato de número: Versace "R$ 16,900" e XP "R$ 70.000.00" `[OBSERVADO, rodada 1]`. Uma terceira, o Gorila, exibe R$ 4.159.382,64 numa posição de 45 ações a R$ 25,60, que dá R$ 1.152,00: valor incompatível com quantidade × preço, `NAO_CONFIRMADO` sem o print *(revisão de 26/09/2026, nota N-GORILA)*. Num produto financeiro isso custa confiança. `OBSERVADO`
*Verificação:* **teste** — todo valor monetário renderizado passa por um formatador único; teste que quebra se aparecer ponto decimal, separador errado ou número sem unidade.

**RI-03 — educação dentro da decisão; nenhuma trilha de curso separada.**
*Por quê:* a literatura diverge sobre o efeito da educação financeira `[F06][F07]`, mas ensinar no momento da decisão é o melhor desenho sob a leitura pessimista e não perde nada sob a otimista. `PARCIAL`
*Verificação:* **revisão** — todo termo técnico tem definição no ponto de uso; nenhum item de menu chamado "curso", "trilha" ou "aulas".

**RI-15 — risco nomeado por sensação; o sistema pergunta intenção, não parâmetro técnico.**
*Por quê:* Nubank nomeia fundos como Cautela, Equilíbrio e Potencial; a Toro pergunta quanto a pessoa quer ganhar e quanto aceita perder, em vez de pedir stop e alavancagem `[G10][G11]`. `PARCIAL`
*Verificação:* **revisão** — nenhuma pergunta de configuração pede parâmetro técnico sem oferecer a versão em intenção; **pesquisa** — o leigo consegue responder sem ajuda.

### B. Honestidade do número e da recusa

**RI-05 — incerteza em faixa numérica escrita em linguagem comum; nunca "pode variar".**
*Por quê:* em cinco experimentos com 5.780 pessoas, a faixa numérica quase não afetou a confiança na fonte, enquanto a incerteza verbal e vaga reduziu `[F10]`. `COMPLETO`
*Verificação:* **teste** — campo com status `PARCIAL` só renderiza como faixa; **revisão** — a faixa aparece em frase comum ("entre R$ 480 e R$ 620"), nunca como "IC 95%".

**RI-10 — estado vazio mostra "sem dado" e o motivo, nunca um zero colorido.**
*Por quê:* o Bastter System exibe "▲ R$ 0,00 · 0,00%" em verde numa conta sem dados `[OBSERVADO, rodada 1]`. É o F-02 na interface: ausência virando número, e número com cara de ganho. `OBSERVADO`
*Verificação:* **teste** — renderizar o relatório de um usuário novo (`test_usuario_novo`) e falhar se aparecer qualquer valor formatado onde o dado é ausente.

**RI-11 — toda comparação de retorno é líquido contra líquido, com IR e taxas.**
*Por quê:* o blog do Mercado Pago compara R$ 62 na poupança contra cerca de R$ 149 **brutos** na conta; a poupança é isenta de IR e a conta não `[G14]`. `COMPLETO`
*Verificação:* **teste** — a função de comparação recusa operar se faltar o insumo de IR ou de custo (mesma regra do F-02: sem insumo, não calcula).

**RI-12 — o número em destaque é o do caso padrão do usuário; o máximo condicionado só vem depois, com a condição escrita.**
*Por quê:* "até 121% do CDI" no PicPay, "105% se trouxer R$ 1.000" no Mercado Pago, e a Clear anunciando "tudo zero, sem asteriscos" com asterisco no mesmo material `[G01][G02][G14][G23]`. `COMPLETO`
*Verificação:* **revisão** — nenhum número de destaque usa "até"; se houver condição, ela está na mesma tela e no mesmo tamanho de leitura.

**RI-17 — toda recusa nomeia o motivo real e diz de quem é a falha.**
*Por quê:* o Pix obriga mensagens de erro específicas e, quando o erro é do próprio participante, exige que isso fique claro ao usuário `[H01]`. `COMPLETO`
*Verificação:* **teste** — cada exceção do motor (`InsumoBloqueado` e as demais) tem um texto de tela associado, e falha o teste se alguma exceção cair num texto genérico.

**RI-19 — a mensagem de confirmação descreve exatamente o que foi feito, e nada além.**
*Por quê:* o Pix determina que a mensagem de sucesso do registro de chave não induza o usuário a concluir que a chave é necessária para pagar `[H01]`. `COMPLETO`
*Verificação:* **revisão** — cada texto de confirmação é lido contra a pergunta: "isto afirma mais do que aconteceu?".

**RI-07 — todo padrão é escolha declarada, com procedência e responsável.**
*Por quê:* na adesão automática estudada por Madrian e Shea, parte dos participantes manteve o padrão por tomá-lo como conselho de investimento da empresa `[F08]`; e o percentual padrão de 2% a 3% virou padrão de mercado por acidente `[F09]`. Juridicamente, no MEOL, padrão é recomendação *(confirmada em 26/09/2026: [Res. CVM 19](../fontes/cvm-resolucao-19-consolidada.md), art. 1º, caput e § 1º, I e II, e art. 2º — para o MEOL oferecido a terceiros como serviço; nota N-CVM)*. `COMPLETO`
*Verificação:* **teste** — todo valor padrão vem de chave declarada em YAML, com fonte; nenhum número padrão nasce no código da interface.

### C. Proteção contra o próprio impulso

**RI-04 — aviso de queda antes do primeiro aporte em renda variável, com o tamanho histórico da queda.**
*Por quê:* entre investidores, segurança é a vantagem mais citada (44%) e só 7% apontam risco de perda como desvantagem `[F01]`. A primeira queda contradiz a expectativa. `COMPLETO`
*Verificação:* **revisão** — o aviso existe antes do primeiro aporte e traz número histórico com fonte, não adjetivo.

**RI-06 — proibidos: confete, recompensa por operação, sequência de dias, lista de "mais populares", notificação para operar e ranking de usuários.**
*Por quê:* o regulador de Massachusetts acusou o Robinhood de usar confete, raspadinhas, ações de brinde, notificações e listas de mais populares para induzir operações frequentes; a empresa removeu o confete em 2021 e fechou acordo de US$ 7,5 milhões em 2024 `[F19][F20]`. O Nubank oferece "os 3 principais ativos do dia" `[G10]`. `COMPLETO`
*Verificação:* **revisão** — lista de proibições conferida a cada versão; **teste** — nenhuma notificação com verbo de ação de compra ou venda.

**RI-09 — a primeira jornada do leigo é a reserva.**
*Por quê:* 31% da população não tem reserva alguma e, entre quem tem, 43% a consumiria em até seis meses `[F01]`; o motor já trata a reserva como Fase A. `COMPLETO`
*Verificação:* **teste** — usuário novo sem reserva recebe decisão de reserva, nunca de ação.

**RI-14 — a reserva nunca vira garantia de crédito nem gatilho de oferta.**
*Por quê:* no PicPay o dinheiro do cofrinho do cartão soma ao limite `[G03]`; no Nubank, dinheiro guardado por três meses pode garantir empréstimo maior `[OBSERVADO]`. Isso inverte a função da reserva, que existe para não precisar de crédito. `PARCIAL`
*Verificação:* **revisão** — nenhuma tela de reserva contém oferta, e o motor não expõe o saldo da reserva a nenhum cálculo de crédito.

**RI-20 — o que reduz exposição vale na hora; o que aumenta exposição tem carência declarada.**
*Por quê:* no Pix, reduzir limite é imediato, e aumentar leva de 24 a 48 horas e depende de aprovação `[H01]`. `COMPLETO`
*Verificação:* **teste** — mudança de perfil que aumenta risco só vale no ciclo seguinte; mudança que reduz vale imediatamente.

**RI-13 — proibido persuadir por culpa, vergonha, depoimento de enriquecimento ou promessa de resultado.**
*Por quê:* o Procon-SP multou a Empiricus por publicidade enganosa no caso Bettina e o Conar suspendeu as peças `[G17][G18]`; um artigo da UFRJ analisa anúncios do Primo Rico que abordam o espectador pela vergonha `[G21]`; as regras da ANBIMA para influenciadores estão em vigor desde 13/11/2023 `[H07]`. `COMPLETO`
*Verificação:* **revisão** — todo texto de marketing passa pela lista de proibições antes de publicar.

### D. Segurança e antigolpe

**RI-08 — notificações e comprovantes sem link clicável.**
*Por quê:* 34% da população passou por golpe ou fraude em 2025, e 42% entre investidores; o mais comum é o link falso que imita banco `[F01]`. O Banco Central vedou propaganda, ofertas e hiperlinks em comprovantes de Pix `[H01][F14]`. `COMPLETO`
*Verificação:* **teste** — nenhuma notificação ou comprovante contém URL.

**RI-16 — um único canal oficial declarado; o MEOL nunca pede dado nem dinheiro por WhatsApp ou mensagem direta.**
*Por quê:* circularam posts falsos com a foto de Luis Stuhlberger indicando ações e levando a atendimento por WhatsApp `[G26]`; e um golpe usou o número oficial do Caixa Tem `[H02]`. `PARCIAL`
*Verificação:* **revisão** — o canal oficial está declarado em tela fixa e no site, com a frase do que o MEOL nunca pede.

**RI-18 — texto vindo de fonte externa é exibido literalmente, nunca renderizado como link ou conteúdo dinâmico.**
*Por quê:* o Pix determina que o campo "Descrição" não contenha HTML e que o app exiba os caracteres literalmente `[H01]`. Nomes de empresa e campos de dado da CVM entram na mesma categoria. `COMPLETO`
*Verificação:* **teste** — o renderizador escapa todo texto vindo de dado; teste com carga maliciosa conhecida.

**RI-21 — canal de contato a um toque na tela principal, sem etapas intermediárias, e instrução de onde reclamar fora do MEOL.**
*Por quê:* o Pix obriga atalho na tela inicial para o canal de atendimento, sem etapas intermediárias, e mensagem informando que a reclamação pode ir ao Banco Central `[H01]`. `COMPLETO`
*Verificação:* **revisão** — contagem de toques até o canal: um.

### E. Acessibilidade (WCAG 2.2) — v1.1

Todos lidos na recomendação do W3C em 27/09/2026 ([transcrição](../fontes/wcag-22-w3c.md)), com o número, o nível e o limiar conferidos na fonte. O MEOL mira o **nível AA** da WCAG 2.2, que inclui o nível A. Todo limiar abaixo carrega o critério ao lado; o texto normativo mora na transcrição, não aqui (licença do W3C: cita-se o critério, não se reescreve a norma).

**Três verificações nomeadas, que ainda não existem e não são escritas agora:**

- **teste de contraste dos tokens** — o da P-163: lê `docs/marca/tokens/`, calcula a razão de contraste de cada par declarado pela fórmula da WCAG (`contrast ratio` e `relative luminance`, na transcrição) e reprova abaixo do limiar do critério; provado por mutação (um par que passa, trocado por um que não passa, reprova).
- **teste de navegador da etapa 4** — Playwright sobre o protótipo (decisão técnica do [`rosto-v1.md`](../decisoes/rosto-v1.md)), com as asserções escritas em cada requisito.
- **axe da etapa 4** — roda por cima dos dois. **Quais regras do axe cobrem quais critérios não foi lido** (`NAO_CONFIRMADO`); por isso nenhum requisito abaixo depende só dele. O axe é piso, não teto (decisão do `rosto-v1.md`).

**RI-22 — texto com contraste de pelo menos 4,5:1 contra o fundo; texto grande, 3:1 `[WCAG 1.4.3]`.**
*Por quê:* `[WCAG 1.4.3]`, nível AA. "Texto grande" é o da definição da WCAG: pelo menos 18 pt, ou 14 pt em negrito, que a página Understanding do critério dá como "approximately 18.5px and 24px" (24 CSS px, ou 18,5 CSS px em negrito). **A razão não se arredonda:** "4.499:1 would not meet the 4.5:1 threshold" (mesma página). As exceções do critério valem aqui: componente inativo, decoração pura e **logotipo** não têm exigência. O documento técnico do motor (Quanto-e-Onde.html) usava `--ink-3` a 3,84:1 em texto de 10,5 a 12 px ([`rosto-v1.md`](../decisoes/rosto-v1.md), item d): é exatamente o que este requisito reprova. `COMPLETO`
*Verificação:* **teste** — o teste de contraste dos tokens, sobre todo par texto × fundo declarado, comparando a razão **sem arredondar**; o par sem fundo declarado reprova (nota 4 da definição de `contrast ratio`: texto com cor e fundo sem cor é falha). **Revisão** — texto sobre imagem ou gradiente, que o teste de tokens não enxerga.

**RI-23 — componente de interface e gráfico necessário com contraste de pelo menos 3:1 contra as cores vizinhas `[WCAG 1.4.11]`.**
*Por quê:* `[WCAG 1.4.11]`, nível AA. Vale para a borda de um botão vazado, o indicador de foco, o marcador de estado (`COMPLETO`, `PARCIAL`, recusa) e a barra de progresso da reserva (T2). A direção E do teste de marca propõe "botões vazados" ([pré-registro](preregistro-teste-de-marca-2026-09-20.md)): num botão vazado, **a borda é a única coisa que identifica o componente**, e ela precisa dos 3:1. O `--rule` do Quanto-e-Onde, a 1,40:1, só passa como decoração. Também aqui a razão não se arredonda ("2.999:1 would not meet the 3:1 threshold", Understanding do 1.4.11). `COMPLETO`
*Verificação:* **teste** — o teste de contraste dos tokens, sobre os pares componente × fundo e marcador × fundo, declarados à parte dos pares de texto. **Revisão** — gráfico que não sai de token.

**RI-24 — cor nunca é o único meio de dizer algo: estado, erro, ganho e perda levam texto ou forma além da cor.**
*Por quê:* `[WCAG 1.4.1]`, nível A. É o critério da WCAG que responde ao daltonismo: não fixa paleta nenhuma, proíbe que a cor carregue a informação sozinha. No MEOL, o selo de procedência (`COMPLETO`, `PARCIAL`, recusa), o "sem dado" do RI-10 e qualquer verde ou vermelho de variação. A página Understanding é explícita: quando o sentido depende de distinguir uma cor, o indicador a mais é exigido "regardless of the contrast ratio between those colors" — contraste alto entre verde e vermelho não dispensa o rótulo. `COMPLETO`
*Verificação:* **teste** — todo token de cor de estado em `docs/marca/tokens/` tem um rótulo de texto declarado ao lado, e o componente de estado não renderiza sem o rótulo (teste de navegador da etapa 4). **Revisão** — cada tela vista em tons de cinza: nenhuma informação se perde.

**RI-25 — o texto aumenta até 200% sem perder conteúdo nem função `[WCAG 1.4.4]`.**
*Por quê:* `[WCAG 1.4.4]`, nível AA. O Pix mostra "aumentar a fonte" como opção de acessibilidade na tela principal `[H01]`. `COMPLETO`
*Verificação:* **teste** — teste de navegador da etapa 4: com o texto a 200% (`[WCAG 1.4.4]`), nenhum elemento de texto das telas F1, F3 e F6 fica cortado (conteúdo maior que a caixa com `overflow` escondido) e todo controle continua alcançável.

**RI-26 — nenhuma tela exige rolagem nas duas direções numa largura de 320 CSS px `[WCAG 1.4.10]`.**
*Por quê:* `[WCAG 1.4.10]`, nível AA. O critério aceita rolagem nas duas direções em "data tables (not individual cells)" (nota 2): a tabela do funil da T3 pode rolar de lado; a frase da decisão, a faixa numérica e os botões, nunca. `COMPLETO`
*Verificação:* **teste** — teste de navegador da etapa 4 com a janela em 320 CSS px de largura (`[WCAG 1.4.10]`): a largura rolável do documento não passa da janela, fora dos elementos marcados como tabela de dados.

**RI-27 — o texto aguenta o espaçamento do usuário sem perder conteúdo: entrelinha 1,5, parágrafo 2, letra 0,12 e palavra 0,16 vezes o tamanho da fonte `[WCAG 1.4.12]`.**
*Por quê:* `[WCAG 1.4.12]`, nível AA. O critério não obriga o MEOL a usar esses espaçamentos (nota 1): obriga a tela a não quebrar quando o usuário os impõe. `COMPLETO`
*Verificação:* **teste** — teste de navegador da etapa 4 que injeta os quatro valores do critério e reprova se algum texto das telas F1, F3 e F6 ficar cortado ou sobreposto.

**RI-28 — a tela funciona em retrato e em paisagem; o MEOL não trava a orientação.**
*Por quê:* `[WCAG 1.3.4]`, nível AA. Nenhuma tela do mapa é caso em que a orientação é essencial (os exemplos do critério são cheque, piano, slide e realidade virtual). `COMPLETO`
*Verificação:* **teste** — teste de navegador da etapa 4 que renderiza as telas F1, F3 e F6 nas duas orientações; e nenhuma trava de orientação no código do protótipo (busca no build).

**RI-29 — todo elemento que recebe foco pelo teclado mostra o foco.**
*Por quê:* `[WCAG 2.4.7]`, nível AA. O indicador de foco é componente para o RI-23: precisa dos 3:1. `COMPLETO`
*Verificação:* **teste** — teste de navegador da etapa 4 que percorre com Tab todos os elementos focáveis e reprova quando o foco não muda nada visível (estilo com e sem foco iguais).

**RI-30 — o elemento com foco nunca fica inteiramente escondido por algo que o MEOL desenhou.**
*Por quê:* `[WCAG 2.4.11]`, nível AA, novo na 2.2. O mapa tem os dois casos de risco: a barra fixa dos três destinos (Decisão, Carteira, Mais) e a gaveta do porquê (T3), que abre por cima. `COMPLETO`
*Verificação:* **teste** — no mesmo percurso com Tab do RI-29, reprova quando o elemento com foco está inteiramente coberto por outro (o ponto central e os quatro cantos dele pertencem a outro elemento). É uma amostra de cinco pontos, não a área inteira: declarado como limite do instrumento.

**RI-31 — todo alvo de toque tem pelo menos 24 × 24 CSS px, ou o espaçamento que o critério aceita no lugar `[WCAG 2.5.8]`.**
*Por quê:* `[WCAG 2.5.8]`, nível AA, novo na 2.2. As exceções do critério valem: alvo **dentro de uma frase** (o termo definido no ponto de uso do RI-03), controle do próprio navegador, e alvo menor com o círculo de 24 CSS px livre. O critério vale também para o conteúdo que abre por cima de outro (Understanding do 2.5.8): os botões da gaveta do porquê entram. O Pix recomenda "aumento do tamanho das áreas de toque" `[H01]`, sem número. O 2.5.5 (nível AAA) pede 44 × 44 e não é exigido no AA; adotá-lo é escolha de desenho da P-163, declarada nos tokens. `COMPLETO`
*Verificação:* **teste** — teste de navegador da etapa 4: todo elemento clicável fora de frase mede pelo menos 24 × 24 CSS px na caixa renderizada, ou passa na regra do círculo de 24 CSS px (`[WCAG 2.5.8]`).

**RI-32 — o caminho de ajuda (o canal do RI-21) fica na mesma posição relativa em toda tela.**
*Por quê:* `[WCAG 3.2.6]`, nível A, novo na 2.2. O RI-21 põe o canal a um toque; este requisito fixa **onde**, para que quem precisou dele uma vez o ache de novo. A gaveta do porquê (T3) é "contextual help", que a página Understanding põe fora do 3.2.6: ela não entra aqui. `COMPLETO`
*Verificação:* **teste** — teste de navegador da etapa 4: em todas as telas do protótipo, o mecanismo de contato aparece na mesma ordem relativa ao resto do conteúdo (ordem no documento). **Revisão** — a cada tela nova.

**RI-33 — o que a pessoa já informou no cadastro não é pedido de novo no mesmo processo: vem preenchido ou selecionável.**
*Por quê:* `[WCAG 3.3.7]`, nível A, novo na 2.2. No mapa: O2 a O5 e a edição em T7 (F4). As exceções do critério valem: o dado que precisa ser redigitado por segurança, e o que deixou de ser válido. E o critério "does not add a requirement to store information between sessions" (Understanding do 3.3.7): o que vem preenchido de um mês para o outro é decisão do MEOL, não exigência daqui. `COMPLETO`
*Verificação:* **teste** — teste de navegador da etapa 4: voltar e avançar no cadastro, e abrir T7, mostra os campos já respondidos preenchidos. **Revisão** — o fluxo inteiro do cadastro, contra a pergunta "isto já foi pedido antes?".

**RI-34 — nenhum passo de login exige teste de função cognitiva sem alternativa (lembrar senha, resolver quebra-cabeça, transcrever código).**
*Por quê:* `[WCAG 3.3.8]`, nível AA, novo na 2.2. A própria WCAG aceita como mecanismo o gerenciador de senhas e o copiar e colar (nota 2 do critério). A página Understanding acrescenta que código de verificação que só se digita à mão reprova, e que a biometria do sistema do aparelho não é teste de função cognitiva. **Não se aplica à v1: ela não tem login** ([`rosto-v1.md`](../decisoes/rosto-v1.md), "Fora da v1"). Passa a se aplicar no dia em que a P-165 escolher um desenho com conta (servidor com banco de dados, bloco 18 da fila). `COMPLETO` (a fonte); **inativo** na v1.
*Verificação:* **revisão** — hoje: nenhuma tela de autenticação no protótipo. Quando a P-165 trouxer login: **teste** de navegador que cola a senha no campo e reprova se o colar for bloqueado, e **revisão** do fluxo contra a lista de testes de função cognitiva da definição da WCAG.

---

## 2. Conflitos entre requisitos, e como ficam resolvidos

| conflito | resolução |
|---|---|
| RI-01 (sem gráfico, frase curta) × RI-05 (faixa numérica) | a faixa aparece **em frase** ("entre R$ 480 e R$ 620"), não em gráfico de intervalo |
| RI-01 (frase curta) × RI-03 (ensinar na decisão) | a explicação fica na camada 2, aberta por toque; a camada 1 não cresce |
| RI-01 (sem jargão) × procedência técnica | o vocabulário do método vive na camada 3 e é aprendido no uso, nunca exigido para decidir |
| RI-07 (padrão declarado) × RI-06 (sem empurrão) | o padrão é mostrado com o porquê e é sempre alterável; nunca é empurrado por notificação |
| RI-20 (carência para aumentar risco) × autonomia do usuário | a carência é **declarada antes** e tem prazo visível; não é bloqueio silencioso |
| RI-09 (reserva primeiro) × público que já investe | quem já tem reserva formada pula a Fase A; o motor decide pelo estado, não por telas diferentes |
| RI-26 (sem rolagem lateral em 320 CSS px, `[WCAG 1.4.10]`) × a tabela do funil da T3 | a tabela é "data table", exceção da nota 2 do `[WCAG 1.4.10]`: ela pode rolar de lado; o resto da T3 não |
| RI-31 (alvo de 24 × 24, `[WCAG 2.5.8]`) × RI-03 (termo definido no ponto de uso) | o termo tocável dentro da frase é alvo **inline**, exceção do `[WCAG 2.5.8]`; o botão fora da frase não tem exceção |
| RI-23 (borda de componente a 3:1, `[WCAG 1.4.11]`) × a direção E ("botões vazados", "um único destaque metálico fosco") | a direção pode ter botão vazado, mas a borda dele entra no teste de contraste dos tokens como componente; um latão ou taupe claro demais para 3:1 não serve de borda |

---

## 3. Matriz requisito × tela

| tela | requisitos que incidem |
|---|---|
| **T1 — aporte do mês** | RI-01, RI-02, RI-03, RI-05, RI-07, RI-10, RI-12, RI-17, RI-19, RI-21 |
| **T2 — carteira e reserva** | RI-02, RI-04, RI-06, RI-09, RI-11, RI-14, RI-20 |
| **T3 — o porquê (procedência e portões)** | RI-02, RI-03, RI-05, RI-10, RI-17, RI-18 |
| **T4 — enciclopédia** | RI-01, RI-02, RI-06, RI-18 |
| **cadastro e perfil** | RI-07, RI-15, RI-19, RI-20 |
| **notificações e comprovantes** | RI-06, RI-08, RI-16, RI-18, RI-19 |
| **páginas públicas e marketing** | RI-12, RI-13, RI-16 |
| **toda tela, T1 a T8, O1 a O5, T1b** *(v1.1)* | RI-22, RI-23, RI-24, RI-25, RI-26, RI-27, RI-28, RI-29, RI-30, RI-31, RI-32 |
| **cadastro e perfil** *(v1.1, acréscimo)* | RI-33 |
| **autenticação** *(v1.1; não existe na v1, entra com a P-165)* | RI-34 |

*v1.1:* o tema E incide em toda tela porque cada critério da WCAG vale para a página inteira, não para um tipo de conteúdo. As linhas acima não substituem as de cima: somam.

A matriz é o equivalente do Anexo I do Pix, onde o regulador exige que o participante apresente a tela de cada item `[H01]`: **cada requisito precisa apontar para pelo menos uma tela, e cada tela precisa passar pelos requisitos que a tocam.**

---

## 4. O que ainda é hipótese

Estes requisitos vêm de estudos feitos fora do Brasil ou de síntese minha, e continuam sujeitos ao teste com pessoas:

- **RI-05** (faixa numérica não custa confiança): replicação no Brasil é a hipótese H-C2 da rodada 1.
- **RI-03** (educação na decisão): a literatura diverge `[F06][F07]`.
- **RI-01** (camada 1 entendida sem ajuda): é a hipótese H-C1.
- **RI-15** (pergunta de intenção): boa prática observada em duas marcas, sem medição.

---

## 5. Limitações declaradas

1. **O capítulo de acessibilidade do Pix é recomendação, não obrigação** `[H01]`. Os requisitos daqui não substituem a lei de acessibilidade.
2. ~~**WCAG não foi lida.** Contraste, tamanho de alvo e daltonismo ainda não têm fonte própria neste documento. Fica a pendência P-WCAG.~~ **Lida em 27/09/2026** (P-155, antes P-WCAG): a WCAG 2.2 na recomendação do W3C, transcrita em [`docs/fontes/wcag-22-w3c.md`](../fontes/wcag-22-w3c.md), deu os RI-22 a RI-34. **O que segue fora:** só 13 dos critérios da WCAG 2.2 foram lidos (os candidatos da P-155); os que ficaram de fora e tocam o MEOL estão listados no fim da transcrição, sem leitura. **Nada disso substitui a lei brasileira de acessibilidade**, que não foi lida.
6. **O que a WCAG não resolve para este público** *(v1.1)*. Os critérios lidos tratam de percepção e operação: contraste, tamanho, foco, orientação. Nenhum deles mede se a pessoa **entende** a decisão. Alfabetismo funcional (29% dos brasileiros de 15 a 64 anos `[F05]`), jargão financeiro e número sem contexto ficam com o **RI-01** (camada 1 curta e sem jargão) e o **RI-03** (definição no ponto de uso), e só se verificam com pessoas: é a hipótese H-C1, no teste com pessoas da **P-156**. Uma tela pode passar em todos os RI-22 a RI-34 e continuar incompreensível para quem ela quer servir. **A WCAG trata do assunto só no nível AAA**, que a meta AA não inclui: o 3.1.3 (jargão; o RI-03 faz o que ele pede) e o 3.1.5 (nível de leitura, com a régua de nove anos de escola, acima do que muita gente do público lê). Lidos na recomendação e transcritos em [`docs/fontes/wcag-22-w3c.md`](../fontes/wcag-22-w3c.md). Nenhuma das 13 páginas Understanding lidas diz que a WCAG deixa de cobrir letramento: esta limitação é leitura nossa dos critérios, não frase do W3C.
3. **Nenhuma verificação jurídica.** As menções à ANBIMA descrevem o que as regras dizem `[H07]`. As menções à CVM 19 foram conferidas no texto da resolução em 26/09/2026 ([Res. CVM 19](../fontes/cvm-resolucao-19-consolidada.md); nota N-CVM). Nenhuma substitui parecer (P-158).
4. **Os requisitos foram derivados sem nenhum teste com pessoas.** Nenhum deles foi validado com o público-alvo.
5. **Números de mercado envelhecem** (§8 do `CLAUDE.md`). Os deste documento valem para setembro de 2026.

---

## 6. Controle de versão

| versão | data | o que mudou |
|---|---|---|
| v1 | 20/09/2026 | consolidação inicial de RI-01 a RI-21, com verificação e matriz de telas |
| v1.1 | 27/09/2026 | RI-22 a RI-34 (tema E, WCAG 2.2 lida na fonte, P-155); três conflitos novos na §2; três linhas na matriz da §3; limitação 2 da §5 atualizada e limitação 6 nova. Nenhum requisito anterior mudou de enunciado |

**Regra de mudança:** requisito novo entra com número seguinte, evidência e verificação. Requisito que cai vira `REVOGADO` com data e motivo. Mudança de enunciado exige nova versão deste arquivo.

---

## Notas de revisão

*26/09/2026 — trazido do Projeto no claude.ai para o repositório.*

- **N-COD.** C-nn → MC-nn e R-nn → RI-nn, só neste documento (tabela no cabeçalho). Motivo: os achados do projeto sobre o fator, o ajuste de proventos, a moeda e a ordem dos portões já usavam esses mesmos números com os prefixos C- e R-, e outros C/R já existiam em outros arquivos com outro sentido; os instrumentos `achados_ancorados` e `codigos_preservados` contariam todos como achados. Guardado por `auditoria/test_codigos_de_marca.py`.
- **N-GORILA.** No RI-02, o Gorila deixou de contar como erro de formato: é valor incompatível com quantidade × preço (45 × 25,60 = 1.152 contra 4.159.382,64), `NAO_CONFIRMADO` sem o print. Os prints são de contas de terceiros ou de demonstração, não do autor.
- **N-CVM.** "Padrão é recomendação" (RI-07) se apoiava num achado de 20/09 que não estava no repositório e passou a `NAO_CONFIRMADO` em 26/09/2026. No mesmo dia, a Resolução CVM 19/2021 foi lida na fonte primária ([Res. CVM 19](../fontes/cvm-resolucao-19-consolidada.md)): a tese foi **confirmada com escopo** (art. 1º, caput e § 1º, I e II; art. 2º), valendo para o MEOL oferecido a terceiros como serviço. Não é parecer (P-158).
- **N-WCAG.** *27/09/2026, v1.1.* Os RI-22 a RI-34 nasceram com o prefixo RI e não passaram pela renomeação da N-COD; a tabela de/para do cabeçalho continua valendo só para os 21 primeiros. Fonte: a WCAG 2.2 na recomendação do W3C, lida em 27/09/2026 ([transcrição](../fontes/wcag-22-w3c.md)). Fecha a P-155 (antes P-WCAG).
