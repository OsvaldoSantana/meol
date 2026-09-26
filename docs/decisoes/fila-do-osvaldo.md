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

**Pergunta aberta, a decidir antes da contagem de segunda:** o n do silver é um **teto** do n
do K2. Os 819 contaram só papel-dia com preço no dia e na véspera, e o silver não sabe quem
tem preço.
- **`n-a`** (a regra como está): a regra usa o n do silver. É otimista, e a janela escolhida
  pode ainda sair sem poder.
- **`n-b`** (calibrar): o script também conta 2021–2025 no silver, e o n de cada candidata é
  multiplicado por `819 ÷ n_silver(2021–2025)` antes de comparar com 1.648. Não lê preço e
  corrige o teto pela proporção observada. Exige que o calendário do silver cubra também
  2021–2025, e acrescenta à regra uma razão que também é escolha.

Se a resposta não vier antes da contagem, vale **`n-a`**, que é o texto já empurrado no #27.

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
