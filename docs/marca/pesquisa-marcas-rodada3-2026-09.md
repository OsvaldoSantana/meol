# Pesquisa de marcas — rodada 3 (P-170, antes P-B5b)

*Aberta em 02/10/2026, sessão local do Claude Code. A rodada leva várias sessões: cada uma
grava aqui o progresso e o que falta. **Estado em 02/10: o plano e o sorteio estão gravados;
nenhuma marca foi visitada nem classificada.***

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
  conta para a categoria em que foi sorteada.
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
| `consultoria_cvm` | CVM, `cad_consultor_vlmob_pj` | 575 | **528** | 0 de 10 |
| `assessor` | CVM, `cad_agente_auton_pj` | 1.396 | **148** | 0 de 10 |
| `corretora` (com as distribuidoras, onde ficam as plataformas de fundos) | CVM, `cad_intermed` | 161 | **138** | 0 de 10 |
| `gestora_e_private` | CVM, gestores PJ de fundos em funcionamento (`registro_fundo`), com o site do `cad_adm_cart` | 1.267 gestores; 1.204 no cadastro de administradores | **1.195** | 0 de 10 |
| `robo`, `consolidador`, `planejador` | lista oficial a procurar, subindo a escada | — | — | — |
| `banco_tradicional`, `banco_digital`, `pagamentos`, `casa_de_analise_e_educacao` | listas do Banco Central e da CVM a ler na fonte | — | — | — |
| não auditadas nas rodadas 1 e 2 | Santander, Caixa, Itaú Personnalité e Private, Suno, SPX, Braun, Grand Seiko e Leica | — | — | — |
| **fora do Brasil** (seção separada, decisão dele de 27/09) | universo a declarar na fonte; não entra no dominante brasileiro (o livro não diz o contrário) | — | — | — |

**A recontagem das consultorias.** O claude.ai contou 573 PJ em funcionamento normal em 27/09;
em 02/10 são 576 linhas e 575 CNPJ (um CNPJ aparece duas vezes). A diferença de 3 é do
cadastro, que muda; a fonte de cada número é o arquivo do dia, com o sha256.

## 3. Achados

Nenhum ainda: nenhuma marca foi visitada.

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

## 5. O que falta, em ordem

1. O merge deste PR: a emenda do livro e o sorteio valem a partir dele.
2. As visitas, categoria por categoria, na ordem dos `sorteio-*.csv`, começando por
   `consultoria_cvm`, a categoria do MEOL.
3. As listas oficiais de robô, consolidador, planejador, bancos, pagamentos e casas de análise.
4. As não auditadas das rodadas 1 e 2, e a seção fora do Brasil.
5. A tabela do veto completa **antes do fim da janela de 21 dias** do teste.
