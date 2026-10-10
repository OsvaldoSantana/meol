# A fila do Osvaldo

*26/09/2026, sessão na nuvem, com o PC dele desligado até 28/09. Todas as pendências abertas
com dono Osvaldo foram conferidas no repositório. **16 estavam vencidas** e fecharam com a
evidência no `PENDENCIAS.md` (tabela `## Fechadas`, linhas de 26/09). Ficaram as decisões
abaixo, na ordem do que cada uma destrava.*

**Como responder pelo celular:** um código por decisão, por exemplo `115a 117a 63a`.
"ok" sozinho aceita todas as recomendações. Se discordar de um fechamento, é só dizer qual:
a pendência reabre.

---

## Respostas dele, 26/09/2026

`115a 117a 63a 65b 127a 146b 84a 81a 12a 52a 129b 124a 128b dep-a 01b` — todas registradas na
pendência de cada uma. **Três divergem da recomendação**, e a decisão é dele:

| bloco | resposta | o que muda em relação à recomendação |
|---|---|---|
| 4 · P-65 | **65b** — construir já | com a condição dele: **só extração determinística**, número com trecho, posição e sha256 da origem, e número sem trecho recusado |
| 13 · P-128 | **128b** — pesquisar | só pesquisa, em `docs/pesquisa/open-finance.md`; nada integrado |
| 15 · P-01 | **01b** — assinar as duas | a assinatura é preparada com impressão digital, sem mexer nos portões; o texto final de cada tese vai a ele **antes** de gravar |

As outras doze seguem a recomendação. A 115a tem um portão dele no meio: o critério é
redigido e **para**, e só é empurrado depois do "pode empurrar".

### Respostas dele, 26/09/2026, sobre os documentos de marca e UX

| pergunta | resposta | onde ficou |
|---|---|---|
| códigos C/R dos documentos colidem com achados | **(A) renomear** para MC-/RI-, só nesses documentos | tabela de/para no cabeçalho de cada um; `auditoria/test_codigos_de_marca.py` |
| os prints do Gorila e do Bastter são contas dele? | **não**: contas de terceiros ou de demonstração | procedência declarada na rodada 1 (nota N-PRINTS) |
| a F0 entra no `PLANO.md`? | **sim, agora, como trilha paralela** de produto | [`docs/decisoes/F0-trilha-de-produto.md`](F0-trilha-de-produto.md); `PLANO.md` §3-F0 |

### Respostas dele, 26/09/2026, sobre a fila do rosto

| pergunta | resposta | onde ficou |
|---|---|---|
| para quem é a v1 do rosto | protótipo com dado sintético para o teste com pessoas | [`rosto-v1.md`](rosto-v1.md) |
| a ordem da marca | à risca: pesquisa → design → mercado → UX → brandbook | idem; nota N-ORDEM no mapa |
| `SEM_POSICAO` primeiro | sim, depois da P-115 | P-164; a regra é o bloco 19, respondido em 03/10: (c) |
| o que sobrevive do Quanto-e-Onde | só o conceito | `rosto-v1.md`, com a medição |
| onde o motor roda | "servidor"; **fechado em 03/10: B′**, servidor sem estado | [`P-165-onde-o-motor-roda.md`](P-165-onde-o-motor-roda.md) |
| nome nos estímulos | MEOL | `rosto-v1.md`; logotipo espera a P-166 |

### Respostas dele, 27/09/2026, aos blocos 16 e 17 (P-162)

Dadas na sessão do Claude Code que abriu a S3, em resposta à pergunta feita quando o
portão da P-163 estava fechado. As duas seguem a recomendação.

| bloco | resposta | o que muda |
|---|---|---|
| 16 · direções no teste | **16b** — E, C e D | a S3 desenha só essas três. A H1 do pré-registro passa a "E supera D em confiável e honesto"; A e B saem do teste, e perde-se saber qual metade da E pesou |
| 17 · regra de decisão | **17a** — escala de 1 a 7, empate quando o intervalo de 95% da diferença pareada (bootstrap) contém zero; "não ficar abaixo da mediana" = não ser a pior direção em honesto; H3 com cada pessoa vendo a direção com e sem a faixa, em ordem aleatória | fecha três das lacunas do pré-registro de 20/09. **Ainda não é o pré-registro final:** ele só vale gravado e empurrado antes de qualquer estímulo ser mostrado (P-162) |

### Respostas dele, 27/09/2026, às perguntas da P-163 e aos achados das S1 a S3

Dadas em 27/09 e trazidas pelo prompt da S4. Nenhuma delas é a aprovação dos PNG: pelo
plano, a aprovação que a S5 exige é a dos PNG que a S4 gerar com estas mudanças.

| código | resposta | onde ficou |
|---|---|---|
| **g-B** | **ordem balanceada:** seis versões do formulário, uma por ordem das três direções, com os links enviados em rodízio. A versão fica registrada em cada resposta. O repasse na bola de neve desequilibra o rodízio, e isso fica declarado | P-162 (pré-registro final, S5) |
| **h-A** | **amostra de quem aparecer, com janela de coleta de 21 dias corridos:** começa no dia do primeiro convite e termina às 23:59 do 21º dia, horário de Brasília. As datas absolutas entram num commit próprio, empurrado antes do primeiro convite. Resposta fora da janela é guardada e não entra na análise. **Nunca encerrar olhando o resultado** | P-162 |
| **i-A** | **estímulo como imagem fixa**, gerada com fontes livres (OFL) embutidas | P-163; `docs/marca/direcoes/` |
| **j-A** | **a H3 testada por rota bloqueada real, nas três direções.** Confirmado por ele em 27/09: na primeira resposta ele escreveu "h-A" duas vezes, e a segunda era o j | P-163; a versão "com rota bloqueada" dos estímulos |
| **k-A** | **ilustração desenhada em código na D, PROVISÓRIA.** Regra de marca: todo ativo visual do MEOL é produzido para o MEOL; nada de banco de imagens | P-168 (nova); `data-provisorio="P-168"` no estímulo |
| **l-B** | **rótulo genérico no lugar do ticker real** | `docs/marca/direcoes/cenario.yaml` (rótulo por rota) |
| **m-B** | **a C troca o roxo por uma cor sem dono** entre as marcas financeiras | `docs/marca/tokens/direcoes.yaml`, bloco C, com a lista conferida |
| **n-A** | **a H-A2 passa para a P-154** | P-154 |
| **o-A** | **riscar a linha C da §5 do `PLANO.md`**: o corte do `CLAUDE.md` foi decidido em 19/09 e feito em 26/09 | `PLANO.md` §5 |
| **p-A** | **merge do #37 com merge commit, feito por ele** | feito: `89848ac` no `main` |
| amigos | **amigos contam no teste**, identificados pela pergunta "você conhece quem criou este app?" (sim/não). A análise sai com e sem eles, e as duas vão para o relatório | P-162 |
| recrutamento | **rede pessoal e bola de neve, sem painel pago** | P-162 |

### Aprovação dele, 27/09/2026: os seis PNG da S4 (PR #38)

**O Osvaldo aprovou os seis PNG da S4 (PR #38).** Dada em 27/09/2026, na mensagem que abriu a
S5 na sessão do Claude Code. É a pré-condição 2 da S5 (P-162). O que ele aprovou são estes
arquivos, no commit `2625cc7` do PR #38:

| PNG | sha256 |
|---|---|
| `docs/marca/direcoes/png/E-base.png` | `302a50ab35a31e24166874f14dfebc4055bc794524c90a73a6894a7311be3665` |
| `docs/marca/direcoes/png/E-rota-bloqueada.png` | `04fe0520a5c4e0e022927ec37cca779fc88c169844b8d0185ff9bcca6e678962` |
| `docs/marca/direcoes/png/C-base.png` | `91b3f24e0eebd467306917b1c24df86ed6fdde4fe25ca9ac211abe4c76acd5b9` |
| `docs/marca/direcoes/png/C-rota-bloqueada.png` | `da85f3eb295e16d43872f5521ec18a13682888291d7ab4aa4c2912389c908174` |
| `docs/marca/direcoes/png/D-base.png` | `36a7c019c0410b1567e5dc17177473895deb5d90a175e630f58eace063115a83` |
| `docs/marca/direcoes/png/D-rota-bloqueada.png` | `f0ad96161c829d4536cd083f08d99581fc54deaa7f32f904c264702bb9b64b73` |

Qualquer mudança num desses arquivos depois daqui é imagem nova, e precisa de nova aprovação.

### Respostas dele, 27/09/2026, às lacunas achadas na S5 (P-162)

Ao juntar as decisões para o pré-registro final, a S5 achou quatro pontos que o texto de
20/09, a 17a e as respostas de 27/09 deixavam abertos. A S5 parou e perguntou; ele respondeu
na sessão do Claude Code. As quatro seguem a recomendação.

| código | a lacuna | resposta | alternativas não escolhidas |
|---|---|---|---|
| **q-a** | "vence a maior média em confiável **e** em é para mim": e se cada escala der uma direção? | **índice das duas:** por pessoa, a média de "confiável" e "é para mim" vira um índice, e a regra 17a roda sobre ele | vencer nas duas, com empate se discordarem; "confiável" decide sozinha |
| **r-a** | a análise sai com e sem amigos: qual decide? | **a sem amigos decide;** a com todos vai para o relatório como sensibilidade (o viés de agradar mora nos amigos) | a com todos decide; as duas precisam concordar |
| **s-a** | a H4 compara com "um iniciante", mas o filtro exclui iniciantes | **a H4 sai do teste**, declarada não testável neste desenho, e vai para a P-156 | pergunta direta exploratória; abrir o filtro para a H4 |
| **t-a** | a H2 compara a D com quem? | **contra a E e contra a C:** a D pior que as duas, com intervalo pareado excluindo zero, em "confiável/parece golpe" ou em "honesto/vendedor" | contra a média de E e C |

### Respostas dele, 27/09/2026, ao ensaio do questionário (S5, P-162)

Um subagente respondeu o questionário três vezes, como três investidores leigos, só para
achar defeito no instrumento (nada do ensaio é dado). Quatro achados mexiam em texto que ele
tinha decidido; a S5 perguntou, e as quatro respostas seguem a recomendação.

| código | o achado do ensaio | resposta |
|---|---|---|
| **u-a** | "Você conhece quem criou este app?" vem antes de qualquer tela e sem criador nomeado: amigo responde "não", e a análise sem amigos (que decide, r-a) se contamina | ~~**"Você conhece pessoalmente a pessoa que está fazendo esta pesquisa (é amigo, parente ou colega dela)?"**~~ *superada pela y-b (~~27/09~~ 02/10, data corrigida): volta o texto de 20/09, e o defeito vira limitação* **Restaurada pela y-a, 02/10/2026:** o texto acima volta a valer. |
| **v-a** | no filtro, "aporta" e "renda variável" são jargão, e quem só aplica no Tesouro pode marcar "sim" | ~~**"Há pelo menos 6 meses, você coloca dinheiro todo mês em ações, fundos de índice (ETF) ou fundos imobiliários?"**; o convite passa a dizer o mesmo~~ *superada pela y-b (~~27/09~~ 02/10, data corrigida): volta o texto de 20/09, e o defeito vira limitação* **Restaurada pela y-a, 02/10/2026:** o texto acima volta a valer, e o convite e a tela de conclusão dizem o mesmo critério. |
| **w-a** | "segura ou arriscada" mistura a tela com o produto, e "sofisticada ou simples" tem sentidos opostos para cada pessoa (nenhuma das duas entra na regra nem na H1 e H2) | **reescritas pelo visual:** "insegurança ou segurança" pelo jeito da tela, e "app popular ou de luxo" |
| **x-a** | "honesta ou vendedora" soa estranho e "parece golpe" planta suspeita, mas são as escalas da regra e da H2 | **manter os construtos de 20/09**, com a ordem das palavras igual à da escala e rótulos claros ("Quer me vender algo" ↔ "Honesta"; "Parece golpe" ↔ "Confiável"); o efeito de sugestão de "golpe" fica como limitação |

### Decisões dele, 27/09/2026, trazidas pelo prompt da S5 v2 (P-162)

O pré-registro gravado no #39 (`docs/marca/preregistro-teste-de-marca-final.md`) usava o
Google Forms. **Nenhum convite saiu**, e ele trocou o instrumento antes de qualquer pessoa ver
um estímulo; a S5 v2 grava o pré-registro de novo, em `docs/marca/teste-de-marca/`.

| decisão | o que ele decidiu | onde ficou |
|---|---|---|
| **instrumento** | **página própria no Vercel, com as respostas no Supabase**; sem IP, sem nome, sem e-mail. Construída na S6. Supera o Google Forms | pré-registro v2, §4; P-162 |
| **g-B, revista** | a ordem balanceada continua entre as 6 permutações, mas **a página atribui a versão ao abrir, por um contador no banco (versão = contador mod 6)**, e não pelo link. A versão fica registrada em cada resposta. Supera o rodízio de links | pré-registro v2, §5 |
| **veto de distinção** | a rodada 3 de marcas (R3) corre em paralelo. Se a direção vencedora pela regra 17a **imitar o código visual dominante** de uma categoria concorrente auditada na R3, a escolha volta para ele, com critério escrito. **A escolha da direção só sai com a R3 fechada** | `docs/marca/teste-de-marca/codigos-visuais.yaml`; pré-registro v2, §8 |

### Respostas dele, 27/09/2026, às divergências achadas na S5 v2 (P-162)

O prompt da S5 v2 trazia textos e definições que as respostas de 27/09 já tinham mudado, ou
deixava aberto. A S5 v2 parou e perguntou; ele respondeu na sessão do Claude Code.

| código | a divergência | resposta | alternativa não escolhida |
|---|---|---|---|
| ~~**y-b**~~ | ~~o prompt trazia o filtro e a pergunta dos amigos de 20/09 e da S4; a u-a e a v-a os tinham trocado depois do ensaio~~ | ~~**voltam os textos do prompt:** filtro "Você aporta todo mês em renda variável há pelo menos 6 meses?" e amigos "Você conhece quem criou este app?". **A u-a e a v-a ficam riscadas; o defeito que o ensaio achou vira limitação declarada**~~ | manter a u-a e a v-a (recomendação da S5 v2) *Superada pela y-a (02/10/2026). Data corrigida: a y-b entrou no commit `7321065`, de 02/10/2026, e não em 27/09 como o título desta seção dizia.* |
| **z-a** | o prompt não citava a q-a, a r-a, a s-a e a t-a | **todas valem:** índice de confiável e é para mim (q-a); a análise sem amigos decide (r-a); a H4 fora, na P-156 (s-a); a H2 é a D pior que a E e que a C (t-a) | revisar alguma |
| **aa-a** | "código dominante = combinação presente em pelo menos metade das marcas da categoria": combinação de quais variáveis? | **as quatro centrais** (fundo, matiz, família do título, raio), as mesmas que definem "imitar". Densidade e peso do botão são classificados e relatados, e não entram no veto | as seis variáveis |
| **ab-a** | "versão = contador mod 6": o contador conta o quê? | **aberturas da página.** Quem abandona gasta uma versão, e o relatório traz o abandono por versão | respostas concluídas |

### Resposta dele, 02/10/2026, na revisão do PR #43 antes do merge (P-162)

Dada na sessão local do Claude Code. O livro de códigos do #43 deixava a R3 declarar as
categorias concorrentes. Mas a classificação de E, C e D já está pública no pré-registro, e
quem escolhesse as categorias depois poderia escolher o veto.

| código | a lacuna | resposta | alternativas não escolhidas |
|---|---|---|---|
| **ac-a** | quais categorias contam como "concorrentes" no veto, e quem as fixa | **fixadas agora no livro de códigos, todas as financeiras:** banco tradicional, banco digital, corretora (com banco de investimento), gestora e private, pagamentos, consolidador de carteira, casa de análise e educação. As referências de sentimento (SBB, Volvo) ficam fora do veto | só quem vende investimento (sem pagamentos nem casa de análise); a R3 declara antes de começar |

### Respostas dele, 02/10/2026, ao abrir a rodada 3 de marcas (P-170)

Dadas na sessão local do Claude Code, antes da primeira marca classificada e antes do primeiro
convite (o commit das datas da janela não existe). O prompt da R3 dizia que o livro de códigos
não se alterava; a sessão mostrou três pontos em que, sem mudança, o veto não funcionaria, e
ele escolheu emendar.

| código | o problema | resposta | alternativas não escolhidas |
|---|---|---|---|
| **ad-a** | o prompt audita consultorias, assessores, robôs e planejadores, e nenhuma dessas é categoria do livro (ac-a): o `veto()` as recusaria. A consultoria é a categoria do próprio MEOL. **A falta foi da proposta da ac-a, feita por uma sessão** | **emendar o livro agora:** quatro categorias concorrentes novas (`consultoria_cvm`, `assessor`, `robo`, `planejador`) e uma precedência para marca que caiba em duas | ficarem fora do veto, só descritivas; encaixar nas sete da ac-a |
| **ae-a** | o livro classifica "a primeira tela do app", que fica atrás do login, e muita marca não tem app | **o app pela primeira captura de interface da App Store; sem app, o site em 390 px**; cada marca registra qual, e o dominante sai também só com as de app | só app (o resto fora do livro); app mais prints dele |
| **af-a** | a saturação pode parar uma categoria com 3 marcas, e o dominante pede n ≥ 5 | **pelo menos 10 marcas sorteadas por categoria** na classificação visual; a saturação continua valendo para os códigos MC | 5 sorteadas; só a saturação |

### Resposta dele, 02/10/2026: y-a, os textos do ensaio voltam (P-162)

Dada no claude.ai e aplicada na sessão da nuvem, **antes do primeiro convite** (o commit das
datas da janela não existe). Não tinha entrado no #43.

| código | o que ele decidiu | motivo | alternativa não escolhida |
|---|---|---|---|
| **y-a** | **supera a y-b.** Voltam os textos que o ensaio de 27/09 corrigiu: amigos (u-a) *"Você conhece pessoalmente a pessoa que está fazendo esta pesquisa (é amigo, parente ou colega dela)?"* e filtro (v-a) *"Há pelo menos 6 meses, você coloca dinheiro todo mês em ações, fundos de índice (ETF) ou fundos imobiliários?"*. O convite e a tela de conclusão deixam de usar "aporta" e "renda variável" e dizem o mesmo critério | a y-b veio de um prompt do claude.ai que citava os textos de 20/09 como decisão. O texto antigo dos amigos contamina a análise sem amigos, que é a que decide (r-a), e o filtro usava jargão | y-b: manter os textos de 20/09, com os defeitos como limitação |

Onde ficou: `docs/marca/teste-de-marca/questionario.yaml` (sha256 novo na §4 do
pré-registro final), o `questionario.md` e o `pesquisa/questionario.json` regenerados; no
pré-registro, a linha da y-a na §1, as limitações 6 (em parte) e 7 riscadas na §9 e a nota na
§10.

### Respostas dele, 03/10/2026, aos blocos 21 e 22

Dadas no claude.ai e registradas na sessão local de 03/10.

| bloco | resposta | onde ficou | alternativas não escolhidas |
|---|---|---|---|
| **21 · 21d** | **nenhuma das três.** Uma única vez, os eventos e os PRs de 16/09 a 02/10 (tudo em Opus) classificados nas classes de `modelos-por-tarefa.md`, marcados `OBSERVADO` porque a classe é inferida: é a referência, eventos por PR mergeado, por classe. Daí em diante, o `metricas_processo.py` do semanal compara, numa janela de 14 dias, a taxa da classe com o modelo novo. A classe volta para o modelo de cima quando a taxa passa de **1,5 vez** a referência **e** há pelo menos **4 PRs** da classe na janela. Até a referência existir, o relatório só mostra os números. O 1,5 e o 4 são escolha declarada no YAML, não medida | `docs/metricas/modelos-por-tarefa.yaml` (`regra_de_volta`), `docs/metricas/referencia-modelos.csv`, `auditoria/metricas_processo.py` e o passo "Regra de volta dos modelos" do semanal | 21a (2 eventos em 14 dias), 21b (4 em 28), 21c (ele lê e decide) |
| **22 · 22a** | **o `PLANO.md` fica na abertura.** A decisão volta a ele em **17/10/2026**, com duas semanas de dado da regra de volta | P-172, que põe o gatilho no `docs/estado.md` | 22b (sai, e o `estado.md` ganha a ordem do que falta) |

**O que a execução da 21d achou, e que a resposta não tinha como saber:**

1. **Não há PR antes de 25/09.** O primeiro PR mergeado no `main` é de 25/09 (#1, #3, #4); de
   16/09 a 24/09 o trabalho entrou por push direto. Os 10 eventos Claude desse trecho estão
   classificados no CSV, mas ficam fora da taxa: sem denominador, contá-los inflaria a
   referência. A referência vale de **25/09 a 02/10: 17 eventos em 37 PRs**.
2. **Três classes saem com referência zero ou sem referência.** `registro` tem 0 eventos em 6
   PRs, e `arquitetura`, 0 em 2. Com referência 0, 1,5 × 0 = 0, e **o primeiro evento** numa
   janela com 4 PRs devolve a classe. Para o `registro`, que é a classe que desceu para o Sonnet,
   a 21d vira na prática "um erro volta". `estatistica` não tem PR nenhum e fica só com os
   números até alguém refazer a referência. **Ajustado no mesmo dia, ver abaixo.**

**Ajuste da 21d, 03/10 (decisão dele, claude.ai), sobre o item 2:** a referência de cada classe
passa a ser **(eventos + 1) / (PRs + 1)**, para que classe com zero evento não tenha régua zero
(`registro`: 1/7; `estatistica`, sem PR: 1,0, e deixa de ser "só os números"), e a volta passa a
exigir **pelo menos 2 eventos** da classe na janela, além do fator 1,5 e dos 4 PRs, que não mudam.
Escolha declarada, não medida: `regra_de_volta.min_eventos: 2` no YAML e o `+ 1` em
`metricas_processo.regra_de_volta()`. Testes: referência (0 em 6) com 1 evento não volta, com 2
volta; provado por mutação (tirar o `+ 1` ou o `min_eventos` reprova). Alternativa não escolhida:
deixar a referência zero como estava (21d original).

3. **O denominador precisa de etiqueta.** Daqui em diante o PR abre o título com
   `[modelo=<m> classe=<c>]`, a mesma etiqueta do `eventos.csv`, e o CI reprova o PR sem ela
   (o Dependabot fica fora). PR sem etiqueta não entra na conta, e o relatório diz quantos
   ficaram fora.
4. **A referência subconta.** 40 das 73 linhas do período têm `autor = desconhecido` e ficaram
   fora, porque a regra só conta autoria Claude. Se a etiqueta obrigatória fizer as linhas novas
   saírem com autor, a taxa nova sobe sem que o modelo piore. O viés empurra para voltar, não
   para ficar.

### Resposta dele, 03/10/2026, ao bloco 18 (P-165)

Dada pelo formulário do Projeto no claude.ai.

| bloco | resposta | onde ficou | alternativas não escolhidas |
|---|---|---|---|
| **18 · B′** | **servidor sem estado.** O aparelho envia a situação, o servidor calcula e devolve, e nada é gravado, nem em log. O dado continua morando no aparelho; a P-157 fica de pé | [`P-165-onde-o-motor-roda.md`](P-165-onde-o-motor-roda.md), com as três consequências e o status de cada uma | A (motor no aparelho), B (servidor com banco de dados) |

### Decisões dele, 03/10/2026, depois da P-115 `NAO_CONFIRMADA`

Dadas no claude.ai e registradas pela sessão local de 03/10 (o PR da dieta). O texto de cada
decisão é o do prompt dele; **as alternativas foram reconstruídas pelo registro, não transcritas
da conversa** (o prompt trouxe as decisões, não as opções), e nenhuma razão é atribuída a ele.

| # | decisão | onde ficou | alternativas não escolhidas |
|---|---|---|---|
| 1 | **Caminho crítico = M2 pela CVM:** ponte ticker → CD_CVM (P-145) → DFP/ITR com bitemporalidade (passo 4) → bloco C sobre dado real. **A série ajustada vira limitação declarada; a P-127 corre em paralelo, sem bloquear** | `PLANO.md` §3; P-180 (a limitação); P-127 | seguir pela série com um critério v3 numa janela nova (sem n: PO-01, PO-02); a P-127 como portão da série, antes da CVM; a segunda esteira (65b) na frente |
| 2 | **Ritmo: duas sessões de motor para uma de rosto; registro vai dentro do PR que o gera, não em PR próprio** | `PLANO.md` §5; skill `bastter-proximo-passo`, regra 2b | sem ritmo declarado, como até 03/10 (de 47 PRs, 14 de rosto e um no caminho da CVM; IP-01); 1:1; registro em PR próprio (#54, #56, #59) |
| 3 | **Dieta completa do processo** | este PR: `PLANO.md` reescrito; `PENDENCIAS.md` em ativas (até 20) e `docs/pendencias-reserva.md`; `docs/estado.md` só com códigos; antes e depois em `docs/metricas/contexto-de-sessao.md` | um corte de cada vez, esperando a P-172 em 17/10 (a 22a); cortar só o `PLANO.md` |
| 4 | **O MEOL nunca foi usado por ele, que não o considera funcional. "Pronto" passa a exigir uso real por ele, do começo ao fim** | `PLANO.md` §2 (M1 = "código pronto, nunca usado") e §4 (frente "primeiro uso"); P-181 | manter o M1 "pronto" pelo teste verde (`test_usuario_novo.py`); "pronto" pelo teste com pessoas (P-156) |

**O que o registro achou ao executar, e que as decisões não tinham como saber:**

1. **Não existe porta de uso.** Dos três módulos que leem o `estado.yaml`, nenhum chama
   `alocar()` nem `motor_aporte()`. O "primeiro uso" começa por construí-la (P-181).
2. ~~**A cabeça do caminho crítico não espera por ele.**~~ **Retratado em 04/10:** espera por
   um passo dele. O `isinp.zip` está no disco, mas o `acervo.abrir` só o aceita depois do envio ao
   R2, que grava o inventário (P-145). O que se confirmou: o token de leitura não é preciso para
   medir na sessão local.
3. **A 65b ficou sem lugar.** O caminho de 03/10 não nomeia a P-65, decidida "construir já" em
   26/09. A posição dela é pergunta nova: bloco 23.

### Resposta dele, 26/09/2026, sobre o critério v2 do degrau (P-115)

**"Pode empurrar", dado no claude.ai**, com o teto combinado de ~19% à vista: a linha 231 do
critério v2 (`docs/auditoria/C02-CRITERIO-V2-PREREGISTRO.md`), que está no rascunho do PR #27
e só chega ao `main` com o merge dele (por isso o caminho vai sem link). Com σ no teto nos dois testes, a janela reprova um ajuste
perfeito em até 19,0% (`1 − 0,9²`). **O merge fica condicionado a duas coisas:** o sha256 do
silver preenchido na §2, pela sessão local, e a lista do D1 empurrada antes de abrir
qualquer documento.

| alternativa | o que acontecia | por que não |
|---|---|---|
| **10% por teste, ~19% na janela** (escolhida) | σ_max 0,0416 no JCP e 0,0463 no dividendo. Com o σ iid de 2021–2025, o JCP já sairia `NAO_CONFIRMADO` por falta de poder em 22% das vezes | — |
| 5% por teste, ~9,75% na janela | σ_max cai para 0,0383 no JCP e 0,0416 no dividendo (mesmo script, `alvo=0,05`, 26/09). O σ iid de 2021–2025 no JCP (0,0472) já passa dos dois tetos, e com um teto mais baixo o `NAO_CONFIRMADO` por falta de poder fica mais provável numa janela com menos JCP | troca uma reprovação à toa, que é visível, por um "sem poder" mais frequente, que não decide nada |
| ler antes, sem decidir agora | o critério fica parado até uma nova leitura dele | o texto e os números já estavam à vista, e o que falta para o merge (silver e D1) não depende desta escolha |

### Resposta dele, 26/09/2026: contar o n antes de escolher a janela (P-115, revisão 4)

**Decisão:** antes do merge do #27, contar os JCPs por ano no silver **sem ler preço** e
escolher a janela pela regra da §9 do critério v2, escrita antes de qualquer contagem.
- **Candidatas:** 2016–2020, 2015–2020, 2014–2020 e 2013–2020.
- **Regra:** vale a menor com `0,0472 × √(819/n_JCP) ≤ 0,8 × 0,0416`, ou seja, **n_JCP ≥ 1.648**.
- **Se nenhuma atender:** 2016–2020, com o `NAO_CONFIRMADO` provável declarado.

Nenhum ano de 2013–2015 tinha sido medido antes; a evidência está na §9.

| alternativa | o que acontecia | por que não |
|---|---|---|
| **contar o n e escolher pela regra** (escolhida) | a janela cresce para trás só se precisar, e o critério de crescer está escrito antes de ver o n | — |
| ficar em 2016–2020 sem contar | o K2 provavelmente sai `NAO_CONFIRMADO` por falta de poder (σ iid de 2021–2025 já passa do σ_max) | gasta a janela num teste que provavelmente não decide |
| medir em várias janelas e ficar com a que passar | — | é escolher pelo resultado: o jardim dos caminhos que se bifurcam, que o pré-registro existe para fechar |
| usar sempre 2013–2020 | o maior n possível | anos mais antigos sem necessidade, com mais JCP para o D1 achar documento e mais distância do que o critério viu; a menor janela que basta é a mais próxima do registro original |

~~**Pergunta aberta, a decidir antes da contagem de segunda:**~~ **Respondida, abaixo (`n-c`).**
Texto original, mantido: o n do silver é um **teto** do n do K2. Os 819 contaram só papel-dia
com preço no dia e na véspera, e o silver não sabe quem tem preço. As opções eram `n-a` (a
regra usa o n do silver) e `n-b` (calibrar pela razão 819 ÷ n_silver de 2021–2025).

### Resposta dele, 26/09/2026: `n-c`, o n na unidade dos 819 (P-115)

**Decisão:** o n passa a ser a **mesma unidade dos 819**: papel-dia só-JCP, dia sem evento de
quantidade, com negócio no COTAHIST no dia e na véspera. Três regras vêm com ela:
- **presença sem preço:** o script lê do COTAHIST só campos de identidade;
- **calibração como condição:** sobre 2021–2025 o script tem de dar **819**. Se der outro
  valor, a regra não escolhe janela, e o script para e mostra a diferença;
- **quarentena:** até o merge e a medição do #27, nenhuma medição lê o retorno do dia ex em
  2013–2020, a P-145 inclusive.

O texto está na §9 do critério, no rascunho do #27 (`d7811fd`).

| alternativa | o que acontecia | por que não |
|---|---|---|
| **`n-c`** · a unidade dos 819, por presença, calibrada (escolhida) | o n de cada janela é o que o K2 vai de fato contar, e a calibração prova isso antes de escolher | — |
| `n-a` · o n bruto do silver | papel-dia no silver, comparado com os 819 | não era a mesma unidade: é um teto, e a janela escolhida podia sair sem poder |
| `n-b` · o n do silver × 819 ÷ n_silver(2021–2025) | corrige o teto por proporção | supõe que a razão de 2021–2025 vale em 2013–2020, com outro universo e outra liquidez; é mais uma escolha, e sem medir a unidade |

**O conjunto de campos, também decisão dele (26/09).** O pedido era ler só DATA e CODNEG. Com
só esses dois, o casamento evento → papel exigiria uma tabela escrita à mão (ON → 3, PN → 4),
que o `ajustar.py` recusa (A-01). Faltariam também o filtro de mercado e a marca de ex, e a
calibração não daria 819. Ele escolheu **identidade, sem preço**: DATA, CODBDI, CODNEG,
TPMERC, ESPECI e CODISI. Ficaram de fora todos os campos de preço, volume, quantidade e fator
de cotação, e o teste envenena essas posições.

### Resposta dele, 27/09/2026: tolerância de 2% na calibração (P-115)

**Decisão:** a calibração sobre 2021–2025 aceita de **819 a 835** (819 × 1,02 = 835,38), e só
para cima.
- **819:** segue sem correção.
- **820 a 835:** segue. O n de cada candidata é multiplicado por 819 ÷ n_cal e arredondado para
  baixo, e a saída imprime o fator.
- **Abaixo de 819 ou acima de 835:** para, sai com código 2 e não imprime as candidatas.

Só para cima porque a presença só pode contar a mais que o `ajustar`: os descartes que ela não
vê são por valor do preço. A correção só diminui o n. Texto na §9 do critério, no rascunho do
#27 (`239acf1`).

| alternativa | o que acontecia | por que não |
|---|---|---|
| **tolerância de 2% só para cima, com correção para baixo** (escolhida) | uma diferença pequena, na direção que a presença explica, não trava a escolha da janela, e o n corrigido fica do lado conservador | — |
| parar sempre (a regra de 26/09) | qualquer diferença, mesmo de um degrau, deixava a janela em 2016–2020 | travava a decisão por uma diferença que a própria unidade explica, sem dizer nada sobre o poder |

### Resposta dele, 26/09/2026, sobre o app do Claude no GitHub

**Não instalar** (menor privilégio; os check-ins agendados cobrem). Revisitar se um aviso
perdido causar erro. Desenho e alternativas em
[`app-claude-github-nao-instalado.md`](app-claude-github-nao-instalado.md).

---

## 1 · Critério da série ajustada antes da próxima janela · P-115

**Pergunta:** empurramos o critério corrigido do degrau como pré-registro **antes** de medir
2016–2020?

- **115a** — sim: o Claude Code redige a partir de `docs/auditoria/C02-JANELA-2021-2025.md`,
  você diz "pode empurrar", e só depois se mede. → A janela nova vira teste de verdade.
- **115b** — medir 2016–2020 com o critério velho. → Já se sabe que ele reprova por um nulo
  errado (4 de 5 anos): vira número, não teste.
- **115c** — não estender, ficar em 2021–2025. → A família ML treina em 2010–2019 e fica sem
  preço ajustado validado nessa janela.

**Recomendo 115a.** O critério foi desenhado depois de ver 2021–2025; só vale para dado ainda
não medido, e só se o "antes" estiver no histórico público (P-116).
**Destrava:** a série ajustada de 2010 a 2020, que é a base de preço do backtest e da ML-3.

---

## 2 · Qual silver o `ajustar.py` lê · P-117

**Pergunta:** como o projeto escolhe entre dois silvers da mesma captura?

- **117a** — o nome passa a carregar os dois insumos (captura + calendário), sempre. → Mais
  honesto; mexe em testes que esperam o nome curto.
- **117b** — `ultimo_silver()` ganha regra explícita (maior cobertura) e teste. → Mais barato;
  a regra continua fora do nome.
- **117c** — aposentar o silver de 11/09. → Simples; perde o lado a lado da P-114.

**Recomendo 117a.** O defeito é o nome carregar um insumo de dois; as outras tratam o sintoma.
Hoje quem escolhe é o `sorted()`, e acerta por sorte.
**Destrava:** a próxima corrida do `refinar.py`/`ajustar.py` sem depender de ordem alfabética.
Vem junto da 1: toda janela nova passa por aqui.

---

## 3 · Nível ou tendência nos balanços · P-63 (PLANO §5-D)

**Pergunta:** o "híbrido" (o nível corta, a tendência só marca) é regra geral ou de cada
métrica?

- **63a** — por métrica: cada uma declara no YAML se lê nível, tendência ou híbrido.
  → Distrato vira "tendência domina", como você disse; solvência segue híbrida.
- **63b** — híbrido geral, com "nível" = média móvel. → **Contradiz o seu exemplo:** a média de
  5→7→11→16 é 9,75 e a de 12→11→10→9 é 10,5, então o nível continua achando a segunda pior.

**Recomendo 63a.** A 63b parece mais simples e erra justo o caso que motivou a pergunta.
**Destrava:** o bloco C e o regime de incorporação (P-58 a P-61, P-64, P-66): o portão que um
dia nomeia empresa.

---

## 4 · A segunda esteira: notas explicativas e IPE · PLANO §5-B, P-65

**Pergunta:** extrair documento (não CSV) entra no escopo, e quando?

- **65a** — entra agora só como **investigação** (uma sessão): formato do Empresas.NET, se as
  notas vêm em XML ou texto livre, volume do IPE. → Decide com medição.
- **65b** — entra já como construção. → Orçamento desconhecido; se a extração for heurística,
  produz número sem procedência e a P1 manda não fazer.
- **65c** — fica fora, declarado. → O portão cobre 3 dos 10 passos da sua sequência, e
  incorporação vira "exige dossiê" para sempre.

**Recomendo 65a.** Não dá para decidir escopo sem saber se a fonte é estruturada.
**Destrava:** 7 dos 10 passos da sua sequência de análise (X-01).

---

## 5 · Um oráculo externo para o preço ajustado · P-127

**Pergunta:** usamos um agregador gratuito como **controle** (nunca como fonte) numa amostra?

- **127a** — sim, depois da decisão 1, com o critério de "concordam" empurrado antes de olhar.
  → Duas fontes independentes, como a que pegou o A-13.
- **127b** — não; basta o C-02 e a marca de ex do COTAHIST. → Validação contra si mesmo.
- **127c** — adiar para depois da ML-3 v1. → A ML treina sobre uma série sem controle externo.

**Recomendo 127a.** O defeito mais caro da série (A-13) só apareceu com duas fontes
comparadas. Os fornecedores estão `NAO_CONFIRMADO`, e os termos de uso entram na conta.
**Destrava:** confiança na série ajustada antes de ela virar insumo da ML-3.

---

## 6 · Mutação: como tirar os testes de repositório · P-146, CI-03

**Pergunta:** a rodada de mutação quebra em ~20 testes que leem o repositório. Como separamos?

- **146a** — rodar só os testes unitários dos quatro módulos mutados. → Rápido; se a lista
  ficar curta, sobra mutante que parece teste fraco, e isso é silencioso.
- **146b** — marcador `repositorio` nos testes que leem o repositório, excluído na mutação.
  → Teste novo sem marcador derruba a rodada em voz alta (o portão `testados=0` já existe).

**Recomendo 146b.** Das duas, é a que falha em voz alta.
**Destrava:** a primeira medição de mutação que mede alguma coisa. Depois dela, um clique seu
em *Actions → Mutacao → Run workflow*, ou um "pode disparar" para a sessão.

---

## 7 · Corretagem de ETF no ranking de corretoras · P-84

**Pergunta:** os 0,50% da XP em ETF entram no ranking como?

- **84a** — segunda parcela da dimensão `corretagem` que já existe. → Nenhum peso novo.
- **84b** — dimensão própria, com peso que você declara. → Peso sem régua para escolher.
- **84c** — só exibido, sem pontuar. → O custo que mais importa para quem compra ETF fica
  fora da nota.

**Recomendo 84a.** Corretagem de ETF é corretagem, e peso novo é política nova sem motivo.
`corretagem_fii` e `exercicio_opcao_pct` são constantes: viram "exibe, não pontua".
**Destrava:** o ranking completo para quem compra ETF (fase B, não A).

---

## 8 · Decisão registrada × parâmetro órfão · P-81

**Pergunta:** como o `chaves_orfas.py` separa "chave que registra um julgamento" de "chave que
promete comportamento e não entrega"?

- **81a** — o YAML declara (por exemplo `e_registro: true` ao lado da chave) e o instrumento
  lê. → A regra mora no dado (P2).
- **81b** — uma lista de nomes dentro do instrumento. → A lista que alguém precisa lembrar
  de estender (a lição da P-82).

**Recomendo 81a.**
**Destrava:** a linha de base de órfãs sem misturar procedência com dívida.

---

## 9 · LCI/LCA e a função DATADO · P-12

**Pergunta:** DATADO continua exigindo liquidez de 30 dias?

- **12a** — passa a aceitar "vence até a data do objetivo **ou** líquida em 30 dias". → Uma
  LCI que vence na data certa deixa de ser eliminada.
- **12b** — fica como está. → Efeito zero hoje (LCI/LCA param no G5); morde quando a carência
  for confirmada.

**Recomendo 12a**, implementada junto do casamento de vencimento. Afrouxar só o número deixaria
entrar coisa ilíquida que não vence nunca.
**Destrava:** LCI/LCA como rota de objetivo com data.

---

## 10 · Série ANBIMA (IMA-B, IRF-M, ETTJ) · P-52

**Pergunta:** capturamos a série enquanto ela está pública (5 dias úteis)?

- **52a** — sim, no mesmo workflow, **se** os termos da ANBIMA permitirem uso pessoal.
  → Custo baixo: a infraestrutura da P-57 já existe.
- **52b** — não; o Tesouro Direto basta como referência, e a ausência vira limitação declarada.
  → O dia perdido não volta.

**Recomendo 52a condicional:** uma sessão lê os termos na fonte; se permitirem, captura; se
não, 52b.
**Destrava:** comparar um ETF de renda fixa com o índice que ele segue.

---

## 11 · Macro sem versão · P-129

**Pergunta:** o BCB não guarda as versões revisadas. O que fazemos?

- **129a** — limitação `FISICA` no dia em que macro entrar num pré-registro. → Honesto, e o
  backtest usa o valor de hoje.
- **129b** — começar **agora** a guardar a nossa própria versão: captura diária das séries do
  SGS no armazém. → Daqui para frente, o valor publicado em cada data fica registrado.

**Recomendo 129b para o futuro e 129a para o passado.** Custa uma linha no workflow, e daqui a
um ano cria a série que hoje não existe em lugar nenhum.
**Destrava:** macro utilizável num pré-registro futuro.

---

## 12 · Custódia do Tesouro: mês ou semestre · P-124

**Pergunta:** o motor desconta a custódia por mês e a B3 cobra por semestre. Mudamos?

- **124a** — fica, escrita como escolha. → Erra centavos por ano, **contra** o Tesouro, que
  ainda assim vence (F-03).
- **124b** — netting pro rata semestral. → Mais código por centavos.

**Recomendo 124a.** O erro vai na direção conservadora e não muda decisão nenhuma.
**Destrava:** nada; fecha a pendência.

---

## 13 · Open Finance para o aporte e as posições · P-128

**Pergunta:** vale pesquisar ligar o aporte e as posições por Open Finance?

- **128a** — não agora: o aporte é um número por mês, digitado. → Zero dado sensível com
  terceiro.
- **128b** — pesquisar (cobertura, custo, o que fica guardado com o terceiro), sem integrar.
- **128c** — integrar. → O dado mais sensível do projeto sai de casa.

**Recomendo 128a**, até haver posição em mais de uma instituição. A pergunta de privacidade
vem antes da técnica.
**Destrava:** pouco na fase A.

---

## 14 · Os dois PRs abertos do Dependabot · #6 (ruff 0.16) e #8 (mypy 2.3)

**Pergunta:** aceitamos as ferramentas de lint novas?

- **dep-a** — sim: a sessão local conserta o que as regras novas acusarem, num PR próprio, e
  os dois do Dependabot fecham. → O grupo `lint` fica **fora** da impressão do ambiente;
  nenhum número muda.
- **dep-b** — fechar e seguir nas versões atuais. → Os PRs voltam na semana que vem.

**Recomendo dep-a.** Os dois PRs estão vermelhos no CI desde 25/09 e o motivo não foi lido
(`NAO_CONFIRMADO`); o conserto começa por lê-lo.
**Destrava:** o Dependabot parar de reabrir a mesma pergunta.

---

## 15 · Assinar as teses · P-01

**Pergunta:** você quer a posição em HASH11, e em Tesouro IPCA+?

- **01a** — "não compro" o HASH11 agora; Tesouro IPCA+ só quando a reserva fechar. → Custo
  zero; resolução completa.
- **01b** — assinar os dois rascunhos. → O HASH11 reprova ou é inaplicável em todos os
  portões do buy & hold e custa 1,30% a.a.

**Recomendo 01a.** Assinar porque o rascunho está pronto é o erro que o pré-registro existe
para impedir, e na fase A o motor de aporte está ocioso de qualquer jeito.
**Destrava:** só a sua carteira. O sistema funciona sem (U-01).

---

## 16 · Quais direções entram no teste de marca · P-162 · **respondido em 27/09: 16b**

O pré-registro de 20/09 tem A (Instrumento), B (Private silencioso), C (Digital
amigável) e D (Ostentação, controle). Depois dele, o chat propôs a **E (Instrumento de
precisão)**, fundindo A e B, que não está em hipótese nenhuma.
- **(a)** A, B, C e D, como registrado; a E fica fora.
- **(b)** E, C e D. A H1 passa a ser "E supera D em confiável e honesto". Menos telas
  por pessoa, menos cansaço, mais precisão com amostra pequena. Perde-se saber qual
  metade da E pesou.
- **(c)** As cinco. Mais informação, mais pessoas necessárias, questionário longo.
**Recomendação: (b).** A E é a candidata real, a C é a estética do concorrente de
fintech, e a D é o controle. Mudar agora é legítimo, porque nenhum estímulo foi mostrado.

---

## 17 · A regra de decisão precisa de número antes do teste · P-162 · **respondido em 27/09: 17a**

A regra de 20/09 diz "empate dentro da margem" sem definir a margem, "abaixo da mediana
em honesto" sem dizer mediana de quê, e a H3 não diz como será testada.
- **(a)** Escala de 1 a 7. Empate quando o intervalo de 95% da diferença pareada
  (bootstrap) contém zero. "Não ficar abaixo da mediana" = não ser a pior direção em
  honesto. H3 testada com cada pessoa vendo a direção com e sem a faixa, em ordem
  aleatória.
- **(b)** Escala de 1 a 7, empate quando a diferença de médias for menor que 0,5 ponto;
  o resto igual a (a).
- **(c)** Sem estatística: vence a maior média, e empate só se forem iguais na primeira
  casa decimal.
**Recomendação: (a).** Cada pessoa vê todas as telas, então a comparação pareada é a
certa, e o script calcula sem julgamento humano depois de ver os dados.

---

## 18 · Onde o motor roda para o usuário · P-165 · **respondido em 03/10: B′**

- **(A)** No aparelho, como diz a P-157. Mais pesado de carregar, e o dado nunca sai.
- **(B)** Servidor com banco de dados. Leve, sincroniza entre aparelhos, mas o dado
  financeiro passa a morar com o MEOL: LGPD, backup, vazamento, login e custo mensal.
- **(B′)** Servidor **sem estado**. O aparelho envia a situação, o servidor calcula e
  devolve, e nada é gravado (nem em log). O dado continua morando no aparelho.
**Recomendação: (B′).** Fica com o ganho da resposta dele (motor em Python num lugar só,
sem carregar o motor no celular) e mantém a P-157. O que precisa ser verdade: log sem
conteúdo, verificado por teste.

---

## 19 · A regra do primeiro aporte com patrimônio zero · P-164 · **respondido em 03/10: (c)**

**Resposta, 03/10/2026 (claude.ai): (c), contra a recomendação (a).** Com patrimônio zero e
a reserva cheia, todo o primeiro aporte vai para a rota de maior peso-alvo.

- **Se a rota de maior peso não couber no aporte** (resposta dele, 03/10): vai inteiro para
  a próxima rota, em ordem decrescente de peso-alvo, que caiba. "Caber" usa as verificações
  que o motor já tem, **lote inteiro e G3 (atrito)**, sem critério novo. Se **nenhuma**
  couber, não há ordem: a saída é uma recusa com o motivo em linguagem comum ("o valor deste
  mês ainda não alcança nenhuma rota; ele fica guardado para o próximo"), nunca um zero e
  nunca `SEM_POSICAO` mudo (RI-10).
- **Empate no maior peso** (decisão técnica do claude.ai, não dele): vale a primeira rota na
  ordem declarada. O texto da decisão dizia "ordem do `politica.yaml`", mas as rotas são
  declaradas no **`catalogo.yaml`**, não no `politica.yaml`; a implementação usa a ordem do
  catálogo e o critério fica escrito no `politica.yaml` (`desempate: ordem_do_catalogo`).
- **Duas consequências da (c) que a pergunta não nomeou**, escritas na `nota` da regra: a
  `banda_sobre_alvo_pp` não se aplica (com patrimônio zero toda ordem é 100% da carteira e a
  banda recusaria todas) e o `k_max` também não (a regra emite uma ordem).

Implementado em `politica.yaml → motor_aporte.primeiro_aporte` (versão 1.37.0) e guardado
por `alocacao/test_p164_primeiro_aporte.py`; a P-164 fechou no histórico.

- **(a)** A mesma regra do motor com patrimônio zero: as `k_max` rotas de maior peso-alvo
  (hoje `k_max = 2`). Nenhuma regra nova.
- **(b)** Uma regra própria para o primeiro aporte (por exemplo, começar pela rota de
  menor custo de entrada), declarada no `politica.yaml`.
- **(c)** Todo o primeiro aporte na rota de maior peso.
**Recomendação: (a).** A P2 fica intacta: o caso vira um valor da mesma função, não uma
exceção. Responder quando a P-115 fechar.

---

## 20 · Ler a especificação da F0 · portão do esquema · **respondido em 03/10: aprovado com mudanças**

Ler `docs/ux/F0-contrato-de-saida.md` e responder: **aprovado**, **aprovado com
mudanças** (quais) ou **refazer**. Sem isso, nenhum código de esquema (decisão F0, regra
3). Não é urgente: pela ordem à risca, o esquema é da etapa 4.

**Resposta, 03/10/2026 (formulários do Projeto no claude.ai; ele não declarou razões):
aprovado com mudanças.**

1. **Os 23 campos: aprovados, todos ficam.**
2. **`reserva.atual` e `alocacao.atual[]`** ficam no contrato da **tela**, mas **não trafegam
   na resposta do servidor** (B′, P-165): a tela os monta com o que o aparelho já guarda.
3. **Venda:** "quero que o motor recomende venda". Recusou o texto fixo "o motor não
   recomenda venda" como solução permanente. → direção do produto e compromisso da
   [P-123](../../PENDENCIAS.md); até ela fechar vale o F5 do mapa, **provisório**.
4. **Frase curta (`decisao.motivo_curto`):** "frase curta sim, mas a interface pode montar".
   É **permissão**, não obrigação.

Efeitos: o contrato em [`F0-contrato-de-saida.md`](../ux/F0-contrato-de-saida.md); a
minimização da **entrada** virou a P-178; a consequência (c) da
[P-165](P-165-onde-o-motor-roda.md) foi atualizada.

---

## 21 · O limiar da regra de volta dos modelos · decisão de 02/10 · **respondido em 03/10: 21d**

O `eventos.csv` passou a levar `[modelo= classe=]` em todo evento de autoria Claude desde
03/10 ([`modelos-por-tarefa.md`](modelos-por-tarefa.md)). Falta o número que devolve uma classe
ao modelo de cima.

- **21a** — **2 eventos em 14 dias** na mesma classe, com modelo abaixo do Opus. → Volta rápido;
  com ~1,6 evento de autoria Claude por dia entre 16/09 e 02/10 (27 em 17 dias, e 40 das 73
  linhas sem autor), pode voltar por ruído.
- **21b** — **4 eventos em 28 dias**. → Mais lento e mais estável; um modelo ruim erra o dobro
  antes de voltar.
- **21c** — sem limiar: **você** lê o relatório do `metricas_processo.py` no semanal e decide. →
  Nenhum número inventado, e a volta depende de alguém lembrar (P7).

**Recomendação: 21a**, porque o custo de voltar cedo é só preço, e o de voltar tarde é erro no
registro. Já está no YAML como proposta; responder confirma ou troca.

**Resposta, 03/10: 21d**, que não estava na lista: taxa de eventos por PR mergeado, por classe,
contra uma referência classificada uma vez em Opus; volta com taxa acima de 1,5 vez a referência
e pelo menos 4 PRs na janela. O texto inteiro está nas respostas, acima do bloco 1.

---

## 22 · O `PLANO.md` continua na abertura? · decisão de 02/10 · **respondido em 03/10: 22a**, volta em 17/10

Depois do corte de 03/10 a abertura é de ~22.800 tokens, e o `PLANO.md` é o maior pedaço que
sobrou depois do `CLAUDE.md`: **8.779 tokens** (`auditoria/tamanho_do_contexto.py`, razão de
2,96 caracteres por token, sem `tiktoken`).

- **22a** — fica. → O §1 do `CLAUDE.md` diz que ele "ganha de qualquer fila"; quem não o lê não
  sabe o que vem primeiro.
- **22b** — sai, como o `PENDENCIAS.md`: o `estado.md` ganha as cinco linhas da ordem do que
  falta, e o resto se lê sob demanda. → Abertura de ~14 mil tokens; o risco é a sessão escolher
  trabalho sem ver a ordem inteira.

**Recomendação: 22a por enquanto**, até a regra de volta ter duas semanas de dado: medir um corte
de cada vez.

---

## 23 · Onde entra a segunda esteira (P-65, 65b) no caminho de 03/10 · **respondido em 10/10: 23a**

Em 26/09 você decidiu **65b, construir já** (só extração determinística). Em 03/10, o caminho
crítico ficou ponte → bitemporalidade → bloco C, sem a P-65. Nos oito dias entre as duas, nenhum
PR a tocou (IP-01). As duas decisões não dizem qual vem primeiro.

- **23a** — **depois do bloco C.** → O consumidor da esteira é o dossiê (P-64), que só roda na
  lista curta, e a lista curta é o que o bloco C produz. Antes disso a extração não tem quem a
  leia (o padrão da P-144: função sem consumidor).
- **23b** — **em paralelo, como a P-127:** uma sessão de motor em cada três, começando por medir o
  formato do Empresas.NET. → Honra o "já" da 65b; tira vaga do caminho crítico.
- **23c** — **na frente da bitemporalidade**, como a 65b mandava. → Desfaz a ordem de 03/10.

**Recomendação: 23a**, porque construir a esteira antes do dossiê existir é construir sem
consumidor. A 65b continua valendo: muda o quando, não o se nem a condição dele.

**Resposta dele, 10/10/2026, pelo formulário no claude.ai: 23a.** A P-65 entra **depois do bloco
C** (P-30), e a 65b segue com a condição dele (só extração determinística). Registrado na P-65
(gatilho novo) e no `PLANO.md` §3; o C-04, que só ela alcança, ficou na `politica.yaml` como
lacuna com caminho até lá (P-17, `campos_C04_C05`).

---

## 24 · Em qual plano da Vercel a página do teste de marca vai ao ar · P-162 · **respondido em 04/10: 24b**

Passo 0 do [roteiro](../marca/teste-de-marca/roteiro-no-ar.md). Lido na fonte em 04/10/2026
(`vercel.com/docs/limits/fair-use-guidelines`, `last_updated: 2026-09-14`): o Hobby é
"restricted to non-commercial personal use only", e uso comercial é qualquer deploy "used for
the purpose of financial gain of **anyone** involved in **any part of the production** of the
project". Os exemplos da página: cobrar do visitante, anunciar a venda de produto ou serviço,
receber para criar ou hospedar o site, link de afiliado, anúncio. O Pro custa US$ 20 por mês
(`vercel.com/pricing`, lido no mesmo dia), com teste grátis.

- **24a** — **Pro por um mês**, cancelado depois do dia 21. → Tira a ambiguidade, e o DPA da
  Vercel passa a cobrir a página (a limitação 4 do pré-registro diz que não cobre o Hobby).
- **24b** — **Hobby, com a leitura escrita.** → Grátis. A página não cobra, não anuncia, não
  vende, não tem afiliado nem anúncio. Risco: a Vercel pode pausar o deploy no meio da janela.
- **24c** — **perguntar ao suporte antes.** → Resposta escrita vira fonte; custa dias.

**Recomendação era 24a**, porque o MEOL é um produto comercial possível e a regra fala em ganho
de "qualquer parte da produção". **Resposta dele, 04/10/2026, pelo formulário: 24b.**

**A leitura escrita (24b), para quem auditar depois:** a página do teste é pesquisa, sem
cobrança, sem anúncio de produto ou serviço, sem afiliado e sem publicidade, e ninguém é pago
para criá-la ou hospedá-la; nenhum dos cinco exemplos da Vercel acontece nela. O texto da regra
é mais largo que os exemplos ("any part of the production"), e por isso a leitura é **dele**, não
da Vercel. **O que muda no teste se a Vercel discordar:** deploy pausado durante a janela é
**desvio do pré-registro** (§10: depois do primeiro convite nada muda) e vai para o relatório
com as datas da pausa; a janela não se estende (h-A). A limitação 4 (o DPA não cobre o Hobby)
continua valendo como está escrita.

---

## 25 · O matiz perto do branco e do preto, no livro de códigos · P-170, P-162 · **respondido em 04/10: ag-b**

Achado na primeira captura da R3 (04/10), antes de qualquer marca classificada. A regra do matiz
usava só a saturação HSL ≥ 0,15, que perto do branco e do preto explode: `#FFFEFE` dava 1,0
("vermelho"), e `#F5F3EE`, o creme do fundo da própria E, dava "laranja". Em 20 das 65 capturas
a cor cromática de maior área era um quase-branco ou quase-preto. Risco nos dois sentidos: veto
falso contra E e D, e veto escondido (botão quase-preto lido como azul).

- **ag-a** — manter e declarar como limitação 23. → Nada muda no pré-registro.
- **ag-b** — emenda curta, livro v3: cromática só com luminosidade HSL de 0,10 a 0,90. → E, C e
  D não mudam; o commit das datas e o primeiro convite esperam o merge.
- **ag-c** — croma perceptual (CIELAB ou OKLCH) com limiar novo. → Mais certo, sem âncora, mais
  código congelado mudado.

**Recomendação: ag-b. Resposta dele, 04/10/2026, pelo formulário: ag-b.** Na pergunta, a
sessão deu `#ECE6E4` como exemplo de "laranja"; medido depois, o matiz dele é 14,99999°, e o
ponto flutuante o põe em "vermelho". O exemplo certo é o `#F5F3EE` (retratação no
`eventos.csv`). O resto da pergunta não muda: 20 de 65, e o creme da E vira laranja.

---

## 26 · O mínimo do Tesouro entra no "caber" do primeiro aporte? · P-179 · **respondido em 04/10: entra, como lote**

Lido na fonte antes da pergunta (04/10/2026): desde 18/11/2024 o Tesouro Direto não tem piso em
reais, e o mínimo é 0,01 título (B3, Bora Investir, 18/11/2024). O PU de compra do Tesouro
Selic em 02/10/2026 ia de R$ 19.943 a R$ 20.017 (CSV `PrecoTaxaTesouroDireto.csv` do Tesouro
Transparente, sha256 `a2ebe116…b533`): o mínimo era ~R$ 200, e a ordem de R$ 40 do instantâneo
da P-164 seria recusada pela corretora.

- **Entra, como lote** — 0,01 título vira o lote da `td_selic`, pela mesma regra (c) dos ETFs:
  se não cabe, a rota cai e o motor passa para a próxima. Ordem sempre executável; exige o PU
  do dia, com data e hash.
- **Entra, e acumula no caixa** — se não cabe, a ordem diz "guarde até somar ~R$ 200". Mantém a
  classe, mas o mês não tem compra.
- **Entra com piso fixo** — um piso em reais no `catalogo.yaml`, revisto por teste. Mais
  simples, erra por alguns reais perto do limite.
- **Não entra: só aviso** — a tela diria "compre" algo que a casa recusa.

**Recomendação: entra, como lote. Resposta dele, 04/10/2026, pelo formulário: entra, como
lote.** Confirmado na fonte primária em 10/10 (tesourodireto.com.br, "Regras e regulamento",
item 9: "múltiplas de 0,01 título ou 1% (um por cento) do valor de um título"). Implementado no
PR da P-179; o que falta está na P-179.

---

## 27 · O limiar do C-05 (caixa / dívida de curto prazo) · P-17

Lido no escopo em 10/10/2026 (`docs/auditoria/escopo-campos-de-analise.md`): o C-05 é **caixa /
dívida de curto prazo**, Fase A, do balanço estruturado da CVM, e a fórmula diz só "Padrão". O
documento **não dá limiar como regra** — a §7 diz que nenhum aparece nele, de propósito. O único
critério escrito é o **exemplo** do bloco L (catálogo especulativo): uma aposta ilustrativa sai
com "reprova: … C-05 (caixa < dívida CP)". É ilustração do formato do registro, não um corte que
alguém escolheu; tratá-lo como regra seria o erro que o projeto corrige (apresentar como derivado
o que é escolha). Hoje a `politica.yaml` marca o limiar `PENDENTE`, e até você responder o C-05
calcula e **marca, sem cortar** (P6).

Visto ao lado, e muda o peso da resposta: **nenhum dos cortes do bloco C tem limiar no YAML**
(C-01 a C-03 também não; `grep` em 10/10). O jeito de decidir este tende a virar o dos outros
três. E nenhum número de "quantas empresas saem" existe ainda: o bloco C não roda (P-30).

- **27a** — **corte em 1,0** agora: caixa menor que a dívida de curto prazo reprova (o número do
  exemplo). → Simples e reproduzível. Reprova quem paga a dívida curta com a geração do ano, e
  não com caixa parado; e sai sem o "muda o universo em N empresas" que `natureza_dos_cortes`
  exige de todo corte, porque N ainda não foi contado.
- **27b** — **o C-05 não corta nunca, só marca**, como a tendência no híbrido (63a). O risco de
  rolagem fica com o C-03 (perfil de vencimento) e o C-01. → Nenhuma exclusão por número que
  ninguém escolheu; perde-se o único corte do bloco que olha liquidez imediata, e o C-03 mede
  quanto vence, não com o que se paga.
- **27c** — **decidir depois da contagem:** o bloco C roda com o C-05 só marcando; antes de ligar
  o corte, mede-se **quantas empresas sairiam** em 0,5 · 1,0 · 1,5 (só a contagem, sem nome e sem
  retorno), e você escolhe vendo isso; a escolha é gravada com impressão digital antes de
  qualquer backtest que use o bloco (P4). → Até lá vale o 27b. É o único caminho que entrega o
  "contra o corte X, que muda o universo em N" que o YAML promete; o risco é escolher de olho
  em quem sai, e por isso a contagem não traz nomes.

**Recomendação: 27c**, porque o próprio `politica.yaml` proíbe corte sem o custo de discordar, e
esse custo só existe contado. Na prática a escolha de hoje é entre fixar 1,0 já (27a) ou depois
de contar (27c). Quais contas somam o caixa e a dívida curta (aplicações de curto prazo?
arrendamento?) **não** é desta pergunta: sai do plano de contas, que o leitor as-of já lê (P-51), e
o arrendamento é da P-58.
**Destrava:** o corte do C-05 no bloco C (P-30); e, se você quiser, o mesmo caminho para C-01 a
C-03.

---

## Conferência de um minuto, com data

- **Token do R2 somente leitura (P-145, destrava toda medição na nuvem):** no Cloudflare, R2 →
  *Manage API tokens* → permissão **Object Read only**, só neste bucket. No GitHub, *Settings →
  Secrets and variables → Actions*, quatro segredos: `R2_LEITURA_ACCOUNT_ID`,
  `R2_LEITURA_ACCESS_KEY_ID`, `R2_LEITURA_SECRET_ACCESS_KEY`, `R2_LEITURA_BUCKET`. **Não
  reaproveite o token de escrita da captura**: o `medir.yml` foi desenhado para não conseguir
  apagar nada. Junto, no desktop: `py -3.11 fase0/subir_acervo_local.py --aplicar`.

- **Até 05/10:** as missões de outubro do cofrinho Turbinado, no app. É o que isenta a
  mensalidade, e `custos.yaml → cofrinho.turbinado_condicao_de_isencao` vence nesse dia. Basta
  mandar um print.

## O que saiu desta fila sem precisar de você

- **P-145:** as duas escolhas eram suas e foram decididas em 25/09; o resto é medição.
- **P-146, item 2:** o semanal rodou; o vermelho foi a guarda do GIT-01 vendo branch aberta
  (P-151, do Claude Code). A rodada de segunda, 28/09, é automática.
- **P-150** (nova): os eventos da B3 não têm rotina nem armazém. É do Claude Code; a carga
  inicial do acervo de 11/09 precisa do desktop.
