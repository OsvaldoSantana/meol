# Pesquisa de marcas — rodada 3 (P-170, antes P-B5b)

*Aberta em 02/10/2026, sessão local do Claude Code. A rodada leva várias sessões: cada uma
grava aqui o progresso e o que falta. **Estado em 11/10: 413 marcas lidas nas sete listas com
sorteio, 85 classificadas (as 10 da af-a em consultoria CVM, assessor, gestora e private,
corretora, banco tradicional, banco digital, pagamentos e casa de análise e educação), nenhuma
arquivada no Wayback ainda, três categorias sem universo e nenhum código dominante em categoria
nenhuma.***

## 0. Para que serve, e o que mudou antes de começar

A rodada 3 audita as categorias que as rodadas 1 e 2 não viram e aplica o **livro de códigos
visuais** do pré-registro do teste de marca
([`teste-de-marca/codigos-visuais.yaml`](teste-de-marca/codigos-visuais.yaml)). Ela é a entrada
do **veto de distinção**: se a direção vencedora do teste imitar o código dominante de uma
categoria concorrente, a escolha volta para ele.

Antes da primeira marca, ele emendou o livro (versão 2; fila, 02/10). O prompt da rodada dizia
que o livro não mudava, e a sessão mostrou três pontos em que, sem a emenda, o veto não
funcionaria:

| código | o que mudou | por quê |
|---|---|---|
| **ad-a** | quatro categorias novas: consultoria CVM, assessor, robô e planejador, com uma precedência para quem cabe em duas | estavam no prompt e fora do livro; o `veto()` as recusaria. A consultoria é a categoria do próprio MEOL |
| **ae-a** | a unidade: a primeira captura de interface da App Store; sem app, o site em 390 px | a tela depois do login está fora do alcance, e muita marca não tem app |
| **af-a** | pelo menos **10 marcas sorteadas por categoria** na classificação visual | a saturação pode parar uma categoria com 3 marcas, e o dominante pede n ≥ 5 |
| **ag-b** *(04/10, livro v3)* | a cor só é cromática com luminosidade HSL de 0,10 a 0,90, além da saturação ≥ 0,15 | nas 65 primeiras capturas, 20 tinham um quase-branco ou quase-preto como "cor de maior área"; `#F5F3EE`, o creme da E, virava laranja. Feita antes da primeira marca classificada |

## 1. Método

- **Universo:** lista oficial, lida na fonte, com o sha256 do arquivo
  ([`rodada3/plano.yaml`](rodada3/plano.yaml)). Sem lista oficial, sobe-se a escada (CLAUDE.md
  §5-B.18) atrás de uma antes de montar lista por busca; se for por busca, fica declarado.
- **Sorteio:** `tools/r3_universo.py` permuta o universo, em CNPJ crescente, com a **semente
  20261002**. A ordem de visita de cada categoria está em `rodada3/sorteio-<categoria>.csv`,
  gravada e empurrada antes da primeira visita (P-170). A semente é a data da sessão, escolhida
  por ela: o pedido era semente fixa, não qual.
- **Visita**, na ordem do sorteio, até classificar 10 marcas na categoria (af-a). Quem não passa
  num critério é **pulado com o motivo**, e a visita segue. São quatro motivos, escritos antes
  de qualquer visita: site inacessível depois da escada, não atende pessoa física, duplicada,
  sem marca própria. Marca cuja categoria pela precedência é outra é classificada na dela e não
  conta para a categoria em que foi sorteada. **Desde 10/10 (plano v2, antes de qualquer visita
  aos três universos novos):** um quinto motivo, `excedente_da_categoria`, para onde um universo
  alimenta duas categorias (`bancos`: tradicional e digital); a visita segue pela mesma lista até
  as duas fecharem 10, e quem aparece depois de a sua categoria ter as 10 primeiras entra como
  pulada, para a lista visitada ficar inteira.
- **Por marca:** posicionamento, promessa, modelo de receita (comissão, taxa, assinatura) e
  regime regulatório, lidos no site e no cadastro; códigos novos continuam no prefixo **MC**,
  depois do MC-29; requisitos novos no **RI**, depois do RI-34.
- **Visual:** captura da página pública por Chromium sem interface (390 e 1280 px) e a imagem da
  App Store. Classificação pelo livro, na unidade da ae-a. As capturas **não** entram no
  repositório (são de terceiros): entram a URL, a data, o sha256 da captura e o link do
  arquivamento no Wayback Machine (Save Page Now). Tela atrás de login fica fora do alcance.
- **Saturação**, por categoria: três marcas seguidas sem código MC novo encerram a parte textual
  daquela categoria. A classificação visual continua até as 10 da af-a. Parar por orçamento de
  tempo é permitido e fica escrito como orçamento.
- **Saída:** [`rodada3/classificacao.csv`](rodada3/classificacao.csv), uma linha por marca
  visitada, inclusive as puladas, com o motivo. A tabela do veto,
  [`rodada3/veto.md`](rodada3/veto.md), é **gerada** desse CSV por `tools/r3_dominante.py`,
  com as funções do classificador congelado no pré-registro.

### 1.1 O procedimento da leitura (04/10/2026, antes da primeira marca classificada)

O livro diz **o que** medir; estas são as escolhas de **como**, que o livro não fixa. São
técnicas, foram escritas antes de qualquer linha classificada e valem para todas as marcas.

| ponto | como se faz | por quê |
|---|---|---|
| captura | `tools/r3_capturar.py site <url>`: Chromium sem interface (Playwright 1.56.0, build 1194), 390 × 844, DPR 1, emulação de celular, `pt-BR`; espera o `load`, a rede parada (até 12 s) e mais 2,5 s; **não clica em nada**. Grava `390.png`, `1280.png` e `medidas.json` (moda dos pixels, botões visíveis com cor, borda e raio computados, textos de maior corpo com a família, sobreposições, links para a App Store, o começo do texto da página) | a mesma tela para todas; o que o navegador computa se confere depois, o olho não |
| aviso de cookies, chat, pop-up | **ficam na captura** e entram na moda do fundo como chegaram; **nunca são o botão principal** | clicar em "aceitar" é consentir em nome dele; tirar do DOM é mexer na página |
| botão principal | o botão da chamada do conteúdo principal na primeira tela; sem ele, o botão de ação do cabeçalho (cheio ou com borda); menu, logotipo, ícone de rede social, seta de carrossel e link de texto não contam | é "a ação que a tela pede" do livro, escrito antes de olhar a classificação |
| sem botão | `matiz` = a cor cromática de maior área (`moda_cromatica`, que usa a regra do livro), `raio` = 0 se não houver cartão, `botao` = vazado | o livro manda; o raio 0 sem cartão é a leitura de "o do cartão principal" quando não há cartão |
| família | o nome da fonte computada do texto de maior corpo fora o logotipo; a classe genérica (serifa, sem serifa, monoespaçada) sai do desenho da fonte nomeada, conferido no olho | o CSS nomeia a fonte, não a classe; limitação 5 |
| densidade | contada no olho, na `390.png`, pela regra do livro | não entra no veto (aa-a) |
| unidade app | a marca **tem app** se o site oficial aponta para a App Store, ou se a busca da App Store do Brasil (`itunes.apple.com/search`, `country=br`) devolve app do mesmo grupo e com a marca; app da plataforma parceira (o do BTG para um assessor do BTG) **não** é app da marca | ae-a: classifica-se o app da marca, não o do parceiro |
| navegador | **10/10/2026:** o Playwright subiu para 1.63.0 (PR #69) e espera o Chromium 1243; a nuvem traz o **1194 (Chromium 141.0.7390.37)**, o build das 51 primeiras visitas (Playwright 1.56.0). A captura usa o 1194 por `R3_CHROMIUM=<executável>`, e o `medidas.json` guarda `navegador`. Não rodei `playwright install`: baixaria um build novo no meio da rodada, e o instrumento ficaria diferente entre as visitas de 04/10 e as de 10/10 | o que se mede (moda dos pixels, estilos computados) depende do motor de renderização; trocar de build no meio é mexer no instrumento sem ninguém ter decidido |
| site do cadastro que não é o da marca | o cadastro do BCB traz, em vários bancos, um link de ouvidoria, chat ou WhatsApp no campo de site (Inter: `intergo.app`; C6: `api.whatsapp.com`; XP: página de chat). A escada usa o domínio que o próprio BCB verificou para o mesmo CNPJ (recurso `DominiosVerificados`, mesmo serviço) e transcreve na coluna `escada`. Fonte sem site (APIMEC): o degrau 3, a busca pelo nome, é o primeiro; não achar é `site_inacessivel` | o site declarado é o da instituição, não necessariamente o da marca que o cliente vê (limitação 2) |
| site inacessível | a escada, transcrita na coluna `escada`: (1) `curl` com e sem `www` e `http`; (2) a API `archive.org/wayback/available`; (3) o site atual por busca; (4) a sessão local, pelo IP dele. Verificação "confirme que é humano" (Cloudflare) **não se resolve aqui**: é degrau 4 | contornar verificação de robô é proibido; o IP residencial dele pode não receber a verificação |
| arquivamento | a nuvem **não alcança** `web.archive.org` (degraus abaixo); a linha leva `PENDENTE_LOCAL`, e `tools/r3_arquivar.py`, na máquina dele, arquiva e escreve o link. **A R3 não fecha com nenhuma linha pendente** (`tools/r3_dominante.py` conta) | degrau 4 da escada |
| as capturas | ficam em `data/r3/capturas/<categoria>-<ordem>/`, fora do git, com cópia na pasta dele | são de terceiros (§1); o sha256 está no CSV |

**A escada do arquivamento, 04/10/2026, sessão na nuvem.** (1) `curl https://web.archive.org/save/<url>`:
`Recv failure: Connection reset by peer`; o mesmo em `/web/2026/<url>`, em `archive.ph` e em
`pragma.archivelab.org`; `http://web.archive.org/save/…` deu 403. O relatório do proxy registra
`tunnel closed (code 1006)` para `web.archive.org:443`. (2) `archive.org/wayback/available` responde
200, mas só devolve arquivamento já existente, não o de hoje. (3) Não há outra cópia pública da
mesma página no mesmo dia. (4) **Sessão local:** `py -3.11 tools/r3_arquivar.py`.

## 2. Os universos, por categoria

Contagem de 02/10/2026, no cadastro baixado nesse dia (sha256 no plano): PJ em funcionamento
normal, um CNPJ uma vez.

| categoria | fonte | em funcionamento | com site declarado (o universo) | classificadas |
|---|---|---|---|---|
| `consultoria_cvm` | CVM, `cad_consultor_vlmob_pj` | 575 | **528** | **10 de 10** (visitadas 1 a 12) |
| `assessor` | CVM, `cad_agente_auton_pj` | 1.396 | **148** | **10 de 10** (visitadas 1 a 12) |
| `corretora` (com as distribuidoras, onde ficam as plataformas de fundos) | CVM, `cad_intermed` | 161 | **138** | **10 de 10** (visitadas 1 a 70; 16 aguardam o degrau 4; 3 foram para gestora e 1 para banco digital) |
| `gestora_e_private` | CVM, gestores PJ de fundos em funcionamento (`registro_fundo`), com o site do `cad_adm_cart` | 1.267 gestores; 1.204 no cadastro de administradores | **1.195** | **14** (10 do sorteio, visitadas 1 a 15, mais 3 sorteadas em corretora e 1 em bancos; 3 aguardam o degrau 4) |
| `bancos` → `banco_tradicional` e `banco_digital` | BCB, serviço `Instituicoes_em_funcionamento`, recurso `SedesBancoComMultCE` (10/10) | 153 sedes | **143** | **10 de 10 e 10 de 10** (visitadas 1 a 143, a lista inteira; 42 aguardam o degrau 4; a 10ª de banco digital veio de corretora) |
| `pagamentos` | BCB, mesmo serviço, recurso `SedesSociedades`, segmento Instituição de Pagamento (10/10) | 195 | **136** | **11 de 10** (visitadas 1 a 136, a lista inteira; 20 aguardam o degrau 4; 1 veio de bancos) |
| `casa_de_analise_e_educacao` | APIMEC, analistas de valores mobiliários PJ credenciados (10/10) | 141 (131 credenciados, 10 licenciados) | **131** (a planilha não declara site: o filtro não se aplica ao cadastro, e quem não tem site sai na visita) | **10 de 10** (visitadas 1 a 34; 2 aguardam o degrau 4; 4 saem por precedência, para banco ou corretora, e 3 são excedentes depois da 10ª) |
| `robo`, `consolidador`, `planejador` | **sem universo**: §2.1 | — | — | — |
| não auditadas nas rodadas 1 e 2 | Santander, Caixa, Itaú Personnalité e Private, Suno, SPX, Braun, Grand Seiko e Leica: lista **nominal**, não sorteio (plano, `a_fazer`) | — | — | — |
| **fora do Brasil** (seção separada, decisão dele de 27/09) | universo a declarar na fonte; não entra no dominante brasileiro; o livro não a lista como categoria | — | — | — |

**Os três universos de 10/10, como foram feitos.** Os arquivos estão em `data/r3/` (fora do git),
com o sha256 no plano; `tools/r3_baixar_bcb.py` os baixa. O que entra no git é, para cada marca,
o identificador, o nome e o site que a instituição declara, nada de e-mail nem telefone; a
licença de reuso do conjunto do BCB **não foi lida** nesta sessão (`NAO_CONFIRMADO`).

- **`bancos`: um universo, duas categorias.** O cadastro do BCB não separa banco de varejo de
  banco digital; o livro separa por agência física × app, e isso só se vê na visita. Em vez de
  inventar um limiar de agências (o cadastro tem 70 bancos com exatamente uma agência, a sede, e
  entre eles estão o Inter, o C6 e o JPMorgan), sorteia-se uma lista só e a categoria sai da
  leitura. Filtrar uma permutação sorteada por uma propriedade e tomar as primeiras *k* é amostra
  simples dessa propriedade. **Sem filtro por carteira comercial**: ele tiraria o Digio e o
  Agibank (`Não`), bancos digitais pelo que o livro define. O preço é visitar também os 40 bancos
  sem carteira comercial (montadoras, câmbio, atacado), que saem com o motivo escrito. A chave é a
  raiz de 8 dígitos do CNPJ, que é o que o serviço traz.
- **`pagamentos`:** as 195 instituições de pagamento autorizadas; muitas são B2B (adquirência,
  BaaS) e saem por `nao_atende_pf`.
- **`casa_de_analise_e_educacao`:** a CVM não mantém lista de analistas; delega o credenciamento à
  APIMEC (Resolução CVM 20; a página da CVM remete a ela). A planilha pública tem razão social,
  nome fantasia, número de registro e status, sem CNPJ nem site. Entram os **credenciados**; os
  10 licenciados estão afastados da atividade. A categoria cobre a casa de análise e a parte da
  educação financeira que é analista credenciada; a educação sem credenciamento (Me Poupe!, Primo
  Rico) **não tem cadastro e fica fora**, declarado. Contei 30 de 141 que são bancos ou
  corretoras (um quinto), que a precedência do livro reclassifica.
- **O que a planilha tem de estranho:** o rótulo do cabeçalho não acompanha o conteúdo (a coluna
  "Solicitação" traz o número de registro; "Vencimento" e "Credenciamento" estão trocadas), e três
  credenciados têm vencimento anterior à data do arquivo e seguem `Regular`. O plano lê as colunas
  pela letra e usa só o status.

**A recontagem das consultorias.** O claude.ai contou 573 PJ em funcionamento normal em 27/09;
em 02/10 são 576 linhas e 575 CNPJ (um CNPJ aparece duas vezes). A diferença de 3 é do
cadastro, que muda; a fonte de cada número é o arquivo do dia, com o sha256.

### 2.1 As categorias sem universo, e por quê (10/10/2026, sessão na nuvem)

Para cada uma subiu-se a escada (§5-B.18), com o erro ou a ausência transcritos. **Nenhuma ficou
"não confirmada por falta de acesso": para as três, a ausência é o resultado da busca, não do
acesso.** Sem universo, a categoria fica com 0 marcas e, pela regra do livro
(`n_minimo_de_marcas: 5`), **não tem dominante e não aciona o veto**. Lista montada por busca seria
escolha de quem busca, que é o que o sorteio existe para impedir; só entra por decisão dele.

| categoria | o que se tentou, e o que voltou | por que não há universo | o que resolveria |
|---|---|---|---|
| `robo` | (1) `dados.cvm.gov.br/dados/`: HTTP 200, **24 pastas** (ADM_CART … SECURIT), nenhuma de robô; página "Consultas por participante" da CVM: analistas, consultores etc., sem robô. (2) busca na web por lista oficial de robôs na CVM ou na ANBIMA: nenhuma; só artigos sobre o enquadramento. (3) nenhuma outra fonte primária. | **Robô não é categoria regulatória.** Quem exige registro entra como consultor, gestor ou corretora, que já têm sorteio, onde a precedência do livro o reclassifica como robô | decisão dele: aceitar a categoria sem veto, ou autorizar uma lista por busca com a regra escrita **antes** de ver qualquer marca |
| `consolidador` | (1) mesmas pastas da CVM e cadastros do BCB: nada. (2) o diretório do Open Finance (`data.directory.openbankingbrasil.org.br/participants`, HTTP 200, 4,5 MB) tem **105 organizações**; Kinvo, Gorila, Mobills, Organizze, Guiabolso, Warren e Magnetis **não estão**; a Pluggy está, como instituição de pagamento. (3) nenhuma outra. | **App de acompanhamento de carteira não é atividade autorizada por ninguém**, e o diretório do Open Finance lista participantes do Open Finance, não consolidadores | idem |
| `planejador` | (1) `www.planejar.org.br/encontre-um-profissional-cfp` (HTTP 200) leva ao portal `portal.planejar.org.br/legado/busca-planejador`, uma aplicação de página única que carrega o **reCAPTCHA v2 de caixa de seleção** (`google.com/recaptcha/api2/anchor`, `size=normal`) e chama `novaplanejar-api.planejar.org.br` (`obter-especialidades`, `obter-estados`; a chamada de busca **não foi feita**). (2) a Planejar é a única entidade que concede o CFP no Brasil, e a lista de certificados só existe nessa busca; a imprensa cita 10.634 certificados no fim de 2024 (fonte secundária). | O cadastro existe, mas **atrás de uma verificação de robô**, e o procedimento da R3 (§1.1) proíbe contorná-la; chamar a API direto, sem o desafio, seria o mesmo contorno. Além disso a **unidade do cadastro é a pessoa**, e a categoria do livro é a marca própria que atende pessoa física | degrau 4: ele busca como pessoa (especialidade × estado × modalidade) e envia a lista; ou aceitar a categoria sem veto. Mesmo assim, o registro de pessoa não é lista de marcas |

**Fora do sorteio por desenho** (plano, `a_fazer`): as **8 marcas nominais** das rodadas 1 e 2
(Santander, Caixa, Itaú Personnalité e Private, Suno, SPX, Braun, Grand Seiko, Leica) são lista
nominal, não universo: Santander e Caixa estão em `bancos`, a Suno na APIMEC e a SPX na CVM, e a
marca já sorteada vale pelo sorteio; Grand Seiko e Leica são referência de sentimento, fora do
veto. A seção **fora do Brasil** segue sem universo declarado e o livro não a lista como
categoria.

## 3. Achados

*04/10/2026, sessão na nuvem. As linhas estão em [`rodada3/classificacao.csv`](rodada3/classificacao.csv),
a leitura de cada uma em [`rodada3/leituras.yaml`](rodada3/leituras.yaml), e a tabela do veto em
[`rodada3/veto.md`](rodada3/veto.md). 51 visitadas: 34 classificadas, 14 puladas (com o
motivo), 3 fora do livro (agente fiduciário e duas casas de câmbio).*

1. **Nenhuma categoria tem código dominante até aqui.** A combinação mais frequente não chega à
   metade em nenhuma:

   | categoria | n | combinação mais frequente | quantas |
   |---|---|---|---|
   | consultoria CVM | 10 | claro / celeste / sem serifa / reto (e escuro / neutro / sem serifa / pequeno) | 2 e 2 |
   | assessor | 10 | claro / celeste / sem serifa / reto (e **claro / laranja / serifa / reto**) | 2 e 2 |
   | gestora e private | 12 | claro / celeste / sem serifa / reto | 4 |
   | corretora | 2 | — | — |

   Por variável, o que se repete é o **título sem serifa** (8 de 10 nas consultorias e nos
   assessores, 10 de 12 nas gestoras) e o **canto reto** (8 de 10 nos assessores, 10 de 12 nas
   gestoras). A cor se espalha; o celeste é o mais comum nas três.
2. **O código exato da E aparece em dois assessores** (Septem Capital e MP Investimentos:
   claro, laranja, serifa, reto). Não é dominante (2 de 10) e não veta, mas é o sinal de que a
   estética "instrumento de precisão" da E tem parentes no assessor que se vende como private.
   Na Septem, o laranja vem de 0,17% da tela (o dourado do título "Quem somos"): ver a
   limitação 8.
3. **Quase uma visita em seis não se lê da nuvem.** Das 51 visitas, 5 pararam em bloqueio ou
   verificação de robô para o IP da nuvem (EUA) ou em erro do proxy: XP Gestão, Mérito (duas
   vezes, em duas categorias), BREI e Morgan Stanley; e, entre as capturadas fora das visitadas,
   Santander Corretora, StoneX, Galapagos, Coinvalores, Genial e FIDD. Outras 3 tinham o domínio
   morto (DNS sem endereço: MoneyMark, Pi e Vitreo), e essas saem pela escada inteira, porque o
   domínio não existe para ninguém. Ver a limitação 7.
4. **O livro precisou de emenda antes da primeira marca** (ag-b, livro v3): §0.

### 3.2 A fase 2 (10 e 11/10/2026, sessão na nuvem): o que saiu do resultado

*O que se mediu: 413 linhas, 85 classificadas pela regra do livro v3 sobre a captura da nuvem; a
conclusão não passa dessa frase (§5-B, pergunta 1).*

5. **Nenhuma das oito categorias tem código dominante** (`python tools/r3_dominante.py`, 11/10;
   `rodada3/veto.md`). Com n = 10 (11 em pagamentos, 14 em gestora), a combinação mais frequente
   dos quatro códigos centrais:

   | categoria | n (só app) | combinação mais frequente | quantas |
   |---|---|---|---|
   | banco tradicional | 10 (8) | claro / celeste / sem serifa / grande | 3 |
   | banco digital | 10 (7) | claro ou escuro / neutro / sem serifa / grande | 2 e 2 |
   | corretora | 10 (1) | claro / celeste / sem serifa / grande | 2 |
   | gestora e private | 14 (1) | claro / celeste / sem serifa / reto | 4 |
   | pagamentos | 11 (9) | claro / verde-água / sem serifa / grande | 2 |
   | casa de análise e educação | 10 (3) | **claro / neutro / sem serifa / grande** | **4** |
   | consultoria CVM, assessor | 10 e 10 | (§3, item 1) | 2 |
   | robô, consolidador, planejador | 0 | sem universo (§2.1) | — |

   O mais perto de dominar é a casa de análise (4 de 10), e o limiar do livro não foi alcançado.
   **Resultado: "nenhum dominante", como saiu.** A ressalva está nas limitações 10 a 13: o que
   falta (42 de 143 bancos, 20 de 136 instituições de pagamento) é justamente o que a nuvem não
   abre.
6. **Por variável, o que se repete é o título sem serifa** (10 de 10 em banco digital, 11 de 11
   em pagamentos, 9 de 10 em banco tradicional e em corretora, 8 de 10 em casa de análise) e, nas
   que são app, o **canto grande** (7 de 10 em banco digital, 7 de 11 em pagamentos, 5 de 10 em
   banco tradicional). A cor se espalha; nas casas de análise o matiz "neutro" aparece em 8 de
   10, e a causa é de medida, não de estética: o botão principal é preto, branco ou cinza (limitação 12).
7. **Um quinto de cada lista de IP residencial.** Bancos: 46 de 143 pularam por `site_inacessivel`
   (42 aguardam o degrau 4, 4 têm domínio morto); pagamentos: 24 de 136 (20 aguardam). Os que
   bloquearam são os grandes: Itaú (em quatro linhas), Banco do Brasil, Santander (em duas,
   fora a corretora), Sicredi, Sofisa, C6, Original, XP e BTG, Digio, Rendimento e Mercado Pago. O banco tradicional
   da amostra é feito de bancos menores (Caixa, BRB, Safra, Daycoval, Banestes, Banco da
   Amazônia, BNB, Bradesco, Nación e Banpará). **Direção do viés:** os grandes têm app e site
   caprichados; a amostra descreve o banco que se deixa abrir por um IP dos EUA, e o resultado
   "nenhum dominante" pode mudar quando o degrau 4 entrar (limitação 10).
8. **O universo de pagamentos é B2B em 83 de 136** (`nao_atende_pf`), e o de bancos tem 33
   `nao_atende_pf` e 34 `fora_do_livro` (financiamento de montadora, câmbio, atacado). A precedência do livro
   reclassifica entre universos: o Neon (cadastro da Magliano DTVM, corretora) é banco digital, o
   PicPay Bank (bancos) é pagamentos, o Andbank (bancos) e o Rio Bravo, o Azimut e a 4UM
   (corretora) são gestora e private.

### 3.3 A fase 3 (16/10/2026, sessão local): a rota da loja e o degrau 4 em ordem

*O que se mediu: as 89 linhas paradas na máquina dele (83 `AGUARDA DEGRAU 4` e 6 que a guarda nova
achou sem o status), refeitas pela ae-a e pela escada com o degrau 4 em ordem (4a, 4b, 4c), e a
amostra refeita pela ordem do sorteio (plano v3). A conclusão não passa disso (§5-B, pergunta 1).*

9. **Sessenta das 89 marcas tinham app na App Store do Brasil** (31 em bancos, 18 em pagamentos,
   9 em corretora, 1 em gestora, 1 em casa de análise), achado pela busca `country=br` com o
   critério escrito antes no plano v3 (`tools/r3_loja.py`, 4 s entre consultas: **zero 403** em
   ~180 consultas). Para essas, o site que recusou o IP **nunca foi a unidade** (ae-a): Itaú, Banco
   do Brasil, Santander, C6, Sofisa Direto, Crefisa, Mercado Pago, XP, BTG, Genial e outras.
10. **O degrau 4 em ordem, nos 29 sem app.** 4a, o servidor do GitHub (`captura_r3.yml`, run
    38900940103, Cheyenne/EUA, AS8075 Microsoft): **abriram 3 de 23** (Original, MUFG, Qore). 4b,
    o runner `br-sp`: não existe. 4c, esta sessão (Campinas, AS16735 Algar): **abriram 4 de 23**
    (Trustee, Integral Access, BREI, Mizuho), e **o resto recusou também daqui**: verificação da
    Cloudflare (StoneX, RNX, Integral Brei), "Acesso Bloqueado" (Randon, XP Gestão), 403 da Akamai
    (Pay4Fun, Hyundai, BNP com 504) e erro de HTTP/2 (Morgan Stanley, Genial). Ver a limitação 15.
11. **Desfecho das 89:** 13 classificadas, 15 `nao_atende_pf`, 4 `fora_do_livro`, 12 duplicadas,
    25 excedentes (a categoria fechou antes delas) e 20 `site_inacessivel` com a escada inteira
    transcrita. **Nenhuma linha espera a máquina dele.** Com a amostra refeita, **18 classificadas
    de 10 e 11/10 saíram como excedentes** (Bradesco, Inter, Pan, BCN, Banpará, Banco VR, EQI,
    Banrisul Corretora, CV Invest, Afinz, Credishop, MagaluPay; e as de outro universo pela regra
    `de_outro_universo`: Azimut, 4UM, Rio Bravo, Andbank, PicPay e Neon).
12. **Robô e consolidador ganharam universo** (fila 28): nos três quadros de Finanças da loja de
    16/10 (100 + 100 + 96 apps, 291 distintos, sha256 no plano) há **5 consolidadores** pelo
    critério escrito antes (Só Dividendos, TradeMap, Investidor10, Status Invest, Dividendos.me) e
    **nenhum robô**; o segundo quadro (termos fixos) achou **1** (Warren). Planejador: 28c, com ele.
13. **`tools/r3_dominante.py` de novo, 16/10:** **nenhum código dominante em categoria nenhuma.**
    n = 10 em todas as oito categorias de cadastro (antes, 14 em gestora e 11 em pagamentos),
    5 em consolidador, 1 em robô. A combinação mais frequente: banco tradicional
    claro/celeste/sem serifa/grande e claro/neutro/sem serifa/grande (3 e 3); banco digital
    escuro/neutro/sem serifa/grande (3); corretora escuro/neutro/sem serifa/pequeno (2); gestora
    claro/celeste/sem serifa/reto (3); pagamentos claro/verde-água/sem serifa/grande (2); casa de
    análise claro/neutro/sem serifa/grande (4, a mais perto do limiar de 5); consolidador, cinco
    combinações diferentes. **Resultado: "nenhum dominante", como em 11/10**, agora sem o viés da
    limitação 10 (os grandes bancos entraram).

## 3.1 O que aguarda a sessão local (degrau 4)

*16/10/2026: **resolvido na fase 3 (§3.3)**; a tabela abaixo fica como foi escrita, e o que ela
mandava esperar da máquina dele foi feito pela loja e pelo degrau 4 em ordem. O Wayback das 86
continua (§5).*

| categoria | ordem | marca | o que fazer |
|---|---|---|---|
| gestora e private | 3 | XP Gestão | capturar do IP dele; se abrir, ler e classificar |
| gestora e private | 7 | Mérito DTVM | idem (verificação da Cloudflare) |
| gestora e private | 10 | BREI | idem |
| corretora | 3 | Mérito DTVM | é o mesmo domínio da gestora 7: uma captura, e a marca entra numa categoria só |
| corretora | 4 | Morgan Stanley | idem (502 do proxy da nuvem) |
| bancos | 42 linhas | as que a nuvem não abre (Itaú, Banco do Brasil, Santander, Sicredi, C6, Original, Sofisa, XP, BTG, Digio e outras) | `grep "AGUARDA DEGRAU 4" docs/marca/rodada3/classificacao.csv`: capturar do IP dele, ler, e `r3_linhas.py --acrescentar --refazer bancos:N` |
| pagamentos | 20 linhas | idem (Mercado Pago, PagSeguro, Rede, Pinbank, Uzzipay, Okto e outras) | idem |
| corretora | 16 linhas | StoneX, Galápagos, Santander Corretora, Genial, Apex, Terra, Trustee, XP, Qore e outras | idem; a corretora já tem as 10, e quem abrir entra **pela ordem do sorteio** |
| gestora e private | 3 linhas | XP Gestão, Mérito, BREI | idem (as de 04/10) |
| casa de análise e educação | 2 linhas | HM Research (o domínio é suposição: confirmar a marca ao abrir) e Suno | idem; a Suno vem depois da 10ª e só conta se alguma anterior cair |
| todas | — | as 85 classificadas | `py -3.11 tools/r3_arquivar.py`: o Wayback de cada uma |
| robô, consolidador, planejador | — | sem universo | decisão dele (fila, bloco 28) |

Se uma pendente abrir e for classificada, a amostra da categoria se refaz **pela ordem do
sorteio**: entram as 10 primeiras classificadas, e as do fim saem (gestora: 13, 14 e 15 são as
primeiras a sair). Com os universos de 10/10, a regra vale em todas as categorias: se uma
pendente abrir e for classificada, a 10ª sai e ganha a linha `excedente_da_categoria`.

## 4. Limitações declaradas

1. **Só quem declara site entra no universo.** Nos assessores, isso é **10,6%** (148 de
   1.396): a amostra descreve os assessores que se mostram na internet, não a categoria. Nas
   consultorias, 92%; nas corretoras, 86%; nas gestoras, 94% dos que estão no cadastro de
   administradores.
2. **O site declarado é o do cadastro**, que a própria empresa preenche e pode estar velho; se
   ele não abrir, a escada procura o site atual antes de pular a marca.
3. **Gestora, na CVM, é quase sempre institucional.** O critério "não atende pessoa física"
   vai pular muitas; a contagem de puladas por motivo sai no fim.
4. **A unidade da R3 não é a das direções** (limitação 22 do pré-registro): marketing da App
   Store, ou site de venda, contra a tela de uso de E, C e D.
5. **A classificação é de quem visita.** A família da fonte e o botão principal são lidos no
   olho, com a regra do livro; não há segundo classificador.
6. **A moda exata dos pixels é instável sobre foto e degradê.** O livro manda medir o fundo
   pela moda dos pixels; numa foto quase todo pixel é único, e a moda vira a cor de um detalhe.
   Em 8 das 34 classificadas a cor da moda cobre menos de 15% da tela, e em 6 o fundo da moda
   discorda da luminância média da tela (Montclair, Amary e Avalon saem "claro" sobre foto
   escura; Ripen, HGR e Finance Academy, "escuro" com média clara). A regra é a do livro e foi
   aplicada como está: o livro não muda depois da primeira marca classificada (§10 do
   pré-registro). **Direção do viés:** desconhecida; o fundo é variável central, então pode
   criar ou esconder imitação.
7. **A captura da nuvem é de um IP dos EUA** (`ipinfo.io`, 04/10: Columbus, Ohio). Site que
   bloqueia, verifica robô ou redireciona por país mostra outra coisa, ou nada: a Hashdex
   (gestora 16, fora das visitadas) redirecionou `hashdex.com.br` para `/en-US`. As marcas
   afetadas aguardam o degrau 4 (§3.1). Nas que abriram, não há como saber daqui se o site
   muda por país; **o que resolveria:** a sessão local recapturar uma amostra das classificadas
   e conferir se a classificação se mantém.
8. **Sem botão, o matiz vem de área pequena.** Em 14 classificadas não há botão na primeira
   tela, e o matiz é a cor cromática de maior área; em 4 delas essa cor cobre menos de 1% da tela
   (Septem 0,17%, Book Capital 0,02%, Avalon 0,09%, Azimut 0,30%).
9. **A captura da App Store é arte de marketing** (limitação 22 do pré-registro). Na Onze, a
   primeira captura mostra o aparelho inclinado e não se recorta como tela: valeu a segunda, a
   primeira de frente (anotado na leitura).

10. **O degrau 4 pesa mais nos bancos e nos pagamentos do que nas outras categorias.** Dos 143
    bancos, 42 aguardam, e entre eles estão os maiores; o banco tradicional da amostra é de
    bancos menores. **O que resolveria:** a sessão local abrir as 42 e as 20, em ordem. Até lá, o
    "nenhum dominante" de bancos e pagamentos vale para a parte que a nuvem alcança.
11. **O instrumento da unidade app muda de uma marca para outra.** 24 das 31 classificadas em
    banco tradicional, banco digital e pagamentos são lidas pela captura da loja (arte de
    marketing, limitação 9); na casa de análise, 3 de 10, e na corretora, 1 de 10. Na Safra a loja
    não traz captura de interface mensurável e valeu o site; na Maree e na Capitalizo a primeira
    captura em pé é uma tela de abertura sem botão ("sem botão", matiz da área mais cromática).
    A unidade, portanto, não é a mesma entre categorias (consultoria, assessor e gestora são
    site), e a comparação entre categorias herda essa diferença.
12. **Botão preto, branco ou cinza dá matiz "neutro".** Em 8 das 10 casas de análise o destaque é
    neutro (Altivuz, MSX, Finclass, Desmistificando, Simpla, Trade ao Vivo, Invius, Dolarame). É a
    regra do livro (o destaque é a cor do botão); o efeito é um "neutro" frequente que **pode
    esconder ou criar** semelhança entre marcas que só diferem no tom do botão.
13. **A cor do botão vazado de app saía da moda dos pixels fora do fundo.** Em 5 leituras
    (Caixa, Bmg, Banestes, BASA, Credishop) isso pegava o suavizado das letras: o Credishop,
    vermelho, saiu rosa pálido e neutro. `r3_linhas.cor_do_texto_por_pixels` passou a tomar o grupo
    mais frequente entre os pixels mais longe do fundo (teste que falha na versão anterior); as
    cinco linhas foram refeitas, e só a do Credishop mudou de matiz (neutro → vermelho). O livro
    não mudou: a regra "cor do texto" é a mesma, o que mudou foi a medida dela.
14. **Domínio achado por busca ou por teste direto só vale com a marca na página.** Nas casas de
    análise o cadastro não traz site: os 10 classificados vieram de teste de domínio, de busca ou
    da loja de apps, e cada site foi aceito só quando a página nomeava a marca (o Simpla Club, pelo texto da página;
    o `bullbear.com.br`, de uma consultoria empresarial, foi recusado para a Team BullBear;
    `doup.com.br` era uma escola de inglês e `desmistificando.com.br`, um escritório de advocacia).
    A Simpla traz o CNPJ do grupo na página, e não o do cadastro: a identidade é pela marca.

15. **O bloqueio era ao navegador sem interface, não só ao IP estrangeiro** (16/10). Das 20
    páginas que o servidor do GitHub não abriu, 17 também falharam no Chromium sem interface do IP
    residencial de Campinas: 9 em bloqueio ou verificação de robô (o mesmo que o IP dos EUA viu) e
    8 em erro de rede, de certificado ou de HTTP/2. O registro de 04/10 atribuía o bloqueio ao IP dos EUA; ele explica
    parte (a Hashdex em `/en-US`), não o todo. Contornar verificação de robô é proibido, e o
    instrumento não muda: essas marcas ficam `site_inacessivel` com a escada inteira. **Direção
    do viés:** desconhecida; são, na maioria, bancos e corretoras de atacado que a leitura já
    tendia a pular por `nao_atende_pf`.
16. **O universo de consolidador é o quadro de Finanças da loja de um dia** (16/10, sha256 no
    plano): o ranking muda toda semana, e ele mede quem paga ou é baixado, não a categoria.
    **Robô tem n = 1**, e vem do segundo quadro (os quatro termos fixos são escolha de quem busca):
    abaixo do mínimo de 5, sem dominante e sem veto, declarado.
17. **Três leituras de categoria são duvidosas e mudam a amostra se forem refeitas:** o
    Rendimento lido `banco_digital` (6 agências, mas o app se vende como "100% digital"), o
    RendimentoPay lido `nao_atende_pf` (cartões pré-pagos corporativos) e a Santander Corretora
    lida como marca comercial própria (como o Itaú Private no livro). Em cada caso a alternativa
    está escrita na leitura. **Decisão dele, 16/10/2026 (formulário no claude.ai): as três ficam
    como estão.** Medido pela arquitetura antes da decisão: nenhuma alternativa cria código
    dominante. Nessas categorias a combinação mais frequente fica em 2 ou 3 de 10, com ou sem a
    troca, e o livro exige pelo menos 5 (`fracao_minima` 0,5 de n = 10). A limitação continua
    declarada: a leitura é de uma sessão só, sem segundo classificador (limitação 5).
18. **Captura de loja sem tela inteira vale o site, e o site recusou:** a Genial (todas as capturas
    em perspectiva) e o Casas Bahia Pay (a tela partida entre duas capturas) ficaram
    `site_inacessivel`, pelo precedente do Safra (10/10).

## 5. O que falta, em ordem

1. ~~O merge do PR do sorteio~~ (#45) e o da emenda ag-b (livro v3), antes deste.
2. ~~As visitas de consultoria CVM e assessor~~ (04/10). Corretora e gestora: a sessão local
   (§3.1).
3. ~~As listas oficiais de bancos, pagamentos e casas de análise~~ (10/10, nuvem; §2) e as
   visitas delas (11/10). **Robô, consolidador e planejador: sem universo (§2.1); a decisão é
   dele (fila, bloco 28).**
3b. ~~O degrau 4: as 83 linhas `AGUARDA DEGRAU 4`~~ (16/10, §3.3: pela loja e pelo degrau 4 em
   ordem; nenhuma espera a máquina dele). **O Wayback das 86** (`tools/r3_arquivar.py`) continua:
   é publicar no archive.org, e a ordem do degrau 4 vale para ele também (4a primeiro).
3c. Robô e consolidador: ~~sem universo~~ (16/10, §3.3, item 12). **Planejador: fila 28c, dele.**
4. As não auditadas das rodadas 1 e 2, e a seção fora do Brasil.
5. A tabela do veto completa **antes do fim da janela de 21 dias** do teste.
