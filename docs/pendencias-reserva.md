# Pendências em reserva

*Criado em 03/10/2026, na divisão do `PENDENCIAS.md` (decisão dele: dieta completa do
processo). Antes e depois: `docs/metricas/contexto-de-sessao.md`, seção de 03/10.*

**Não é lido por padrão.** Cada pendência daqui está **aberta**, com dono, gatilho e classe,
mas fora do caminho crítico de hoje. A sessão lê o `PENDENCIAS.md` (as ativas, no máximo 20) e
vem aqui só por busca: `grep -n "^## P-NN" docs/pendencias-reserva.md`.

- **O gatilho disparou, ou ela entrou no caminho crítico?** Move o bloco para o
  `PENDENCIAS.md`, no mesmo commit. Se as ativas estiverem em 20, uma sai antes (para cá ou
  fechada): o teto é guardado por `auditoria/test_plano_e_pendencias.py`.
- **Fechou?** O mesmo protocolo das ativas: cabeçalho riscado, evidência, e o bloco vai para
  `docs/historico/pendencias-fechadas.md`, com a linha na tabela `## Fechadas`.
- **Antes de abrir uma pendência nova**, procure aqui e na tabela das fechadas.

---

## P-05 · Quatro `NAO_CONFIRMADO` esperando download

**Dono:** Claude Code (sessão local: o degrau 4 da escada) · **Gatilho:** antes de BOVV11, ACWI11 ou a rota de stablecoin receberem peso · **Classe:** `BLOQUEIA_O_SISTEMA` *(campos dados na triagem de 03/10/2026, P-171)*

| chave | bloqueia | o que fecha |
|---|---|---|
| `etf.BOVV11` | `tabela_etf_rv_completa` | ~~site do gestor bloqueia robô — visita manual~~ escada subida em 27/09 sem resolver da nuvem (`docs/fontes/MAPA-CONSTANTES.md`); o degrau 4 é da sessão local, roteiro abaixo |
| ~~`etf.IMAB11`~~ | **fechada 05/09** — 0,25% a.a. (página do gestor, PARCIAL). Falta o regulamento para virar COMPLETO |
| `etf.ACWI11` | `comparacao_global_amplo` | regulamento / página do produto |
| `exterior.vest_stablecoin.iof` | `ordenacao_rotas_exterior` | tratamento de IOF em stablecoin |

O `IMAB11` é o mais valioso: é o único concorrente conhecido do Tesouro IPCA+ na
função `PROTECAO_REAL` que não paga a custódia de 0,20% a.a. da B3.

> **27/09/2026 — BOVV11, o degrau 4 da escada (§5-B.18), para a sessão local.** Da nuvem, os
> degraus 1 a 3 falharam com o erro transcrito no `MAPA-CONSTANTES.md` (403 do Akamai no site
> do gestor; túnel caído no `web.archive.org`; CVM sem campo de taxa para ETF). ⚙ **Na máquina
> dele**, sem navegador e sem sessão logada:
> 1. `curl -sS -L -o bovv11.html -w "%{http_code}\n" https://www.itnow.com.br/bovv11/` — IP
>    residencial costuma passar pela WAF. Se der 200, procurar a lâmina ou o regulamento
>    linkados na página e baixá-los com `curl`.
> 2. Se der 403: `curl -sS -L -o bovv11_wb.html "https://web.archive.org/web/20260513194558id_/https://www.itnow.com.br/bovv11/"`
>    (a cópia de 13/05/2026 que a API da Wayback aponta).
> 3. Transcrever para `docs/fontes/` o trecho com a **taxa total** e a composição (P-50: adm,
>    gestão, custódia), com URL, data do documento e sha256 do arquivo baixado.
> Só depois disso o valor entra no `custos.yaml`, pelo protocolo de mudança: ele muda a rota
> BOVV11 no motor, e o `conteudo.yaml` dos estímulos do teste de marca sai do motor (o
> `--conferir` pega se mudar).

---

## P-10 · `alfa_contra_fatores()` tem uma armadilha viva

**Dono:** Claude Code · **Gatilho:** antes de escrever a próxima estratégia do pré-registro · **Classe:** `DECISAO_DE_DESENHO` *(campos dados na triagem de 03/10/2026, P-171)*

Ela **subtrai o Risk_Free**, porque foi escrita para carteira comprada. Aplicada a um
fator long-short, troca o alfa do HML de +0,766% (t=+2,94) para −0,178% (t=−0,68):
inverte sinal e veredito, sem levantar erro.

Hoje há um teste que prende a diferença, e o `backtest_h1_h3.py` não a usa. Mas a
função continua com o nome que convida ao erro.

**Duas saídas:** renomear para `alfa_de_carteira_contra_fatores()`, ou aceitar um
parâmetro `auto_financiado=False` que dispensa a subtração.
**Gatilho:** antes de escrever a próxima estratégia do pré-registro.

---

## P-20 · Opções voltaram a ser pendência, não exclusão

**Dono:** Claude (a régua) · **Gatilho:** quando opções entrarem no catálogo; nada urgente · **Classe:** `DECISAO_DE_DESENHO` *(campos dados na triagem de 03/10/2026, P-171)*

Correção dele em 05/09: *"quando você me perguntou se operava opções eu disse que não,
mas além do meu cofrinho no PicPay eu não opero mais nada — isso não foi uma
autorização de exclusão."*

Ele está certo, e a falha é a mesma do banco com outra roupa: converti resposta
factual em decisão de escopo. Numa carteira vazia, "não opero X" é verdade para todo
X. `opcoes` perdeu o `fundamento` e voltou a ser pendência.

**O que falta é régua, e há um problema real de modelagem:** opção tem propriedades que
o catálogo não representa. No lançamento a descoberto a **perda pode exceder o capital
aplicado**, e a escala `perda_maxima` não tem degrau acima de `total`. E a posição tem
vencimento próprio, que interage com o teto de 10 anos.

**Gatilho:** nenhum urgente — ele não opera hoje. Mas a exclusão saiu do arquivo.

---

## P-27 · Separação motor/usuário ainda é parcial

**Dono:** Claude Code · **Gatilho:** antes de existir um segundo usuário · **Classe:** `DECISAO_DE_DESENHO` *(campos dados na triagem de 03/10/2026, P-171)*

Achado L-01. `compromissos` e `decisoes` foram para `perfil.yaml`; a fusão é na carga,
então nenhum consumidor mudou. **Quatro seções continuam mistas por dentro:**

- `corretora` — metodologia do ranking junto com os **pesos** que você escolheu
- `aporte_extraordinario` — regra junto com o seu padrão de bônus
- `sleeves`
- `custos.yaml → cofrinho` — termos de um produto de mercado junto com o estado da
  **sua** conta

Dividi-las exige decidir a granularidade, e isso é desenho, não arrumação.

**Gatilho:** antes de existir um segundo usuário — não antes disso.

---

## P-28 · `revisao` está declarada e nunca é lida — **o guarda foi consertado, a dívida não**

**Dono:** Claude Code · **Gatilho:** quando a cadência de revisão for desenhada, ou na próxima limpeza do inventário de dívida do YAML · **Classe:** `DECISAO_DE_DESENHO` *(campos dados na triagem de 03/10/2026, P-171)*

Nenhum `.py` referencia a seção `revisao` do `politica.yaml`. Ou vira comportamento
(cadência de revisão implementada), ou sai do arquivo.

**Em 05/09 o defeito de fundo foi fechado.** O `test_cobertura_yaml` varria **seis** das
dezenove seções lendo **três** dos onze módulos — media o próprio escopo, não a
cobertura. Foi por esse vão que `revisao` entrou e ficou. Agora são quatro testes:
toda seção precisa de um **regime declarado com motivo escrito** (`OPERACIONAL`,
`REGISTRO`, `ESPECIFICAÇÃO`), seção nova sem regime **quebra a suíte**, e a dívida
conhecida vive num inventário que **não pode apodrecer** — entrada já paga ou de chave
removida faz o teste falhar.

As três chaves de `revisao` continuam na dívida. O que mudou é que agora elas são
contadas, e o próximo `revisao` não tem por onde entrar.

---

## P-29 · `estrategias_pre_registradas` — o pré-registro não é lido pelo motor

**Dono:** Claude Code · **Gatilho:** quando o backtest completo existir (M3) · **Classe:** `DECISAO_DE_DESENHO` *(campos dados na triagem de 03/10/2026, P-171)*

121 chaves. Nenhum módulo do motor as referencia; quem lê são os testes e o
`backtest_h1_h3.py`. É defensável — o pré-registro descreve o que **será testado**, não
o que o alocador faz hoje. Mas até que o backtest completo exista, é uma especificação,
e especificação sem número some.

---

## P-31 · `regime_instituicao_financeira` — mesma situação, 46 chaves

**Dono:** Claude Code · **Gatilho:** quando a P-30 rodar sobre banco: banco não sai do universo (P6), fica sem peso deste bloco até o regime rodar · **Classe:** `DECISAO_DE_DESENHO` *(campos dados na triagem de 03/10/2026, P-171)*

Nasceu da sua correção sobre bancos: *"não faz o menor sentido excluir Itaú e Bradesco
— não deve ser excluído, deve ser encontrado o critério"*. O critério foi **escrito**.
Ele ainda não **roda**.

---

## P-32 · O que sobrou de prosa na seção `corretora`

**Dono:** Claude Code · **Gatilho:** no próximo toque em `corretoras.py` · **Classe:** `DECISAO_DE_DESENHO` *(campos dados na triagem de 03/10/2026, P-171)*

Depois do achado N-01, três regras saíram do Python e foram para o YAML. Restam
declarações sem consequência: `promocional` (peso negativo para promoção — argumento
escrito, nunca aplicado), `cobertura_e_penalidade` e `nota_cobertura` (o código
implementa a penalidade por dimensão ausente, mas com números próprios) e
`fora_do_ranking`.

**11/09/2026: `promocional` saiu desta lista.** O `regras()` agora recusa peso diferente
de zero, no mesmo padrão de `reclame_aqui` e `facilidade`. Restam
`cobertura_e_penalidade` e `fora_do_ranking`.

---

## P-34 · `sleeves` — seis chaves que o `sleeve.py` não lê

**Dono:** Claude Code · **Gatilho:** no próximo toque em `sleeve.py`, ou antes de a sleeve de seleção ativa receber peso · **Classe:** `DECISAO_DE_DESENHO` *(campos dados na triagem de 03/10/2026, P-171)*

`exige_selecao`, `n_ativos_efetivo`, `bloqueado_por`, `meses_para_montar`. O
`bloqueado_por: A05_nucleo_indexado_vs_selecao_ativa` é o mais grave: ele afirma que a
sleeve de seleção ativa está **travada por uma decisão em aberto**, e nada a trava.

### Fragmento sem cabeçalho, achado na triagem de 03/10/2026

*Estava solto entre a P-34 e a P-25 desde um corte anterior, sem código, e o `tools/estado.py`
o lia como parte da P-34. É do cofrinho (a mesma conta do K-01 e da P-74). Movido como estava;
os valores são os já publicados (exceção de 25/09 da D-01), nenhum novo.*

| item | valor |
|---|---|
| depositado | R$ 7.671,01 |
| limite extra obtido | R$ 530,00 |
| razão | **14,5 para 1** — 6,9% vira limite |

Ou o vínculo tem teto, ou a maior parte do saldo está parada sem comprar limite nenhum.
**A pergunta:** com quanto de depósito você mantém o limite de que precisa? Se R$1.000
bastarem, sobram R$6.671 livres — e aí eles têm destino, que é constituir a reserva que
hoje é zero.

---

| saldo | ganho extra a.a. | mensalidade a.a. | saldo liquido |
|---|---|---|---|
| R$ 7.671 | R$ 162,07 | R$ 287,88 | **−R$ 125,81** |
| R$ 10.000 *(teto)* | R$ 211,28 | R$ 287,88 | **−R$ 76,60** |
| R$ 13.625 | R$ 287,87 | R$ 287,88 | R$ 0,00 *(empate)* |

**O empate está 1,4× acima do teto do produto.** Pagando a mensalidade, o Turbinado
nunca se paga. Só vale com a isenção — e a isenção é mensal.

As duas condições escritas: **R$20 mil investidos** para liberar um produto que aceita
no máximo R$10 mil; ou **R$2.500 em 3 meses no cartão**, que só é grátis se você
gastaria isso de qualquer forma. Induzir R$100/mês de gasto extra custa R$1.200/ano
para economizar R$287,88.

### As duas perguntas que sobraram — **só você**

1. **O que exatamente te isenta hoje, e isso se repete todo mês?** A tela diz "Tarefas
   concluídas — ativo **este mês**", o que sugere requalificação mensal e não status
   permanente. Se depender de tarefa mensal, é um custo de atenção recorrente que a
   conta acima não captura.
2. **O saldo do cofrinho do cartão pode migrar para o Turbinado, ou está preso
   enquanto garantir o limite?** Se estiver preso, a decisão passa a ser sobre o
   **aporte novo**, não sobre os R$7.671.

Com a isenção valendo, o Turbinado rende **13,88% a.a. líquido** contra 11,70% do
cofrinho atual — **R$167,14/ano** sobre o saldo de hoje, e com liquidez.

---

## P-25 · Reserva e dívida não são independentes — **estrutural**

**Dono:** Claude Code · **Gatilho:** a reserva de um usuário deixar de ser zero com parte dela empenhada · **Classe:** `DECISAO_DE_DESENHO` *(campos dados na triagem de 03/10/2026, P-171)*

Achado J-02, e é o mais sério do dia. O cofrinho garante a **fatura do cartão**. Sua
reserva de emergência é colateral de uma dívida de **consumo sua**.

No cenário para o qual a reserva existe — perda do contrato único, com estabilidade de
renda medida como **baixa, 6 de 6** — você teria ao mesmo tempo: renda zero, fatura
aberta, e a reserva empenhada nessa fatura. **Ela não fica só indisponível: é consumida
pela dívida que a prendia.**

Iliquidez atrasa o acesso. Colateral destrói o ativo no cenário em que ele deveria ser
usado — reserva com correlação −1 com a própria necessidade.

O G1 (dívida) e o G2 (reserva) rodam em sequência como se os dois lados fossem
independentes. Neste arranjo não são: é o mesmo dinheiro contado duas vezes, uma como
segurança e outra como limite de gasto.

**Efeito no motor hoje: zero** — `reserva_disponivel: 0.00` já zera a contagem por
outro caminho. Mas o motivo registrado dizia "iliquidez" quando o problema é
"colateral", e a distinção decide o remédio.

---

## P-35 · A reserva é um número e o mundo tem baldes — **consequência do P-24**

**Dono:** Claude Code · **Gatilho:** o primeiro depósito na reserva, de qualquer usuário · **Classe:** `DECISAO_DE_DESENHO` *(campos dados na triagem de 03/10/2026, P-171)*

Com teto por produto, "quanto há de reserva" deixou de bastar: para saber se a próxima
parcela cabe é preciso saber **onde** ela está. `Estado.reserva_por_rota` foi criado e é
**opcional**. Quando ausente, o G2 avisa que não sabe em vez de supor que a reserva foi
construída na ordem do plano.

**Hoje não morde** — a reserva é zero e o `estado.yaml` declara `reserva_por_rota: {}`,
que *afirma* que não há reserva em lugar nenhum, diferente de omitir a chave. Morde a
partir do primeiro depósito, e o viés aponta para **recomendar demais** a rota melhor.

---

## P-22 · Opções: duas famílias, não uma

**Dono:** Claude (pesquisa de custo da coberta) · **Gatilho:** junto da P-20 · **Classe:** `DECISAO_DE_DESENHO` *(campos dados na triagem de 03/10/2026, P-171)*

Contexto que ele trouxe em 05/09 — no Bastter, opções e **aluguel de ações** eram
apresentados como forma de *rentabilizar* a carteira, não como aposta direcional.
Isso resolve metade do problema de modelagem da P-20.

**Coberta** (call sobre ação que já se tem; aluguel de ação detida): perda máxima é
custo de oportunidade acima do strike, mais risco de contraparte. Cabe em
`perda_maxima: limitada` — **o catálogo já representa.** Falta pesquisa de custo, e
o `Tarifacao_Equities_V5.0` item 1.3.1.4 (exercício de opções) já está em `docs/fontes`.

**Descoberta:** perda pode exceder o capital aplicado, e a escala não tem degrau
acima de `total`. Essa continua irrepresentável.

A exclusão genérica de "opções" era grossa demais: juntava duas coisas com perfis de
perda opostos.

---

## P-23 · Método Mille pré-registrado, com a crítica antes do teste

**Dono:** Claude Code · **Gatilho:** quando o bloco C rodar sobre dado real (os pilares 2 a 4 saem da CVM) · **Classe:** `DECISAO_DE_DESENHO` *(campos dados na triagem de 03/10/2026, P-171)*

Mille é João Bosco Oliveira Junior, coautor do Bastter — **mesma casa**, não fonte
independente. Quatro pilares: governança, produtividade, geração de caixa,
endividamento. Dois cortes numéricos: **margem líquida > 20%** e FCL Capex não
negativo por muito tempo.

**Crítica registrada antes de rodar:** margem líquida acima de 20% é **filtro
setorial disfarçado de filtro de qualidade**. Banco, software e concessionária têm
margem estruturalmente alta; varejo, distribuição e construção têm baixa — e nenhuma
das duas coisas fala da administração. Se rodar, tem de ser com controle setorial.

**Três dos quatro pilares saem da CVM.** Governança não: "ligar para o RI" não vira
coluna. Quem rodar só os pilares 2–4 está rodando três quartos do método, e o
registro diz isso em vez de fingir cobertura.

---

## P-19 · Imóvel direto foi excluído por argumento geral, sem medição

**Dono:** Claude · **Gatilho:** quando imóvel entrar no catálogo; nada urgente · **Classe:** `DECISAO_DE_DESENHO` *(campos dados na triagem de 03/10/2026, P-171)*

Achado ao escrever a P6. A entrada `imovel_consorcio_COE_previdencia_sem_match` dizia
"fora por custo e iliquidez; **não avaliados individualmente**" — e essa segunda metade
não é fundamento legítimo.

Consórcio e COE têm custo estruturalmente alto e documentado, o que sustenta a exclusão
por `CRITERIO_MEDIDO`. "Previdência sem match" está resolvida por outro caminho (ele é
PJ e não tem previdência). **Imóvel direto é o elo fraco:** excluído por argumento
geral, sem medição.

**Gatilho:** nenhum urgente — ele não tem capital para imóvel na Fase A. Mas a exclusão
precisa de régua ou de reclassificação para pendência.

---

## P-41 · Carregamento de YAML domina o custo multiusuário

**Dono:** Claude Code · **Gatilho:** o segundo usuário · **Classe:** `DECISAO_DE_DESENHO` *(campos dados na triagem de 03/10/2026, P-171)*

`carregar_politica()` custa **82 ms** e `carregar()` **42 ms**, contra 2,75 ms do motor.
Para um usuário é irrelevante. Para N usuários × M chamadas, 124 ms de parse por chamada
domina tudo.

**Deliberadamente não feito.** Otimizar agora seria para um cenário que não existe — e o
S-02 é a prova de que cache mal dimensionado custa correção, não só tempo.
**Gatilho:** o segundo usuário.

---

## P-42 · O catálogo é quadrático em número de rotas

**Dono:** Claude Code · **Gatilho:** o catálogo passar de ~100 rotas · **Classe:** `DECISAO_DE_DESENHO` *(campos dados na triagem de 03/10/2026, P-171)*

| rotas | `alocar()` |
|---|---|
| 25 | 12 ms |
| 400 | 728 ms |
| 800 | 2.810 ms |

Quatro `next(v[0] for v in vivos if v[0].id == rid)` dentro de laços sobre `pesos`.
**Limitado por desenho:** rota é um *tipo* de caminho, não um papel — ação individual é
uma sleeve dentro de `acao_zero`. Barato de consertar, não é o gargalo.
**Gatilho:** se o catálogo passar de ~100 rotas.

---

## P-48 · Viés de sobrevivência na composição de índice — declarado, não resolvido

**Classe:** `BLOQUEIA_O_SISTEMA`. **Dono:** Claude. **Gatilho:** antes de rodar o backtest.

A carteira teórica do Ibovespa só existe publicamente **para o dia corrente**. O primeiro
snapshot do projeto foi capturado em 06/09/2026 (76 ativos, referência B3 08/09/26, lista
em `docs/fontes/pesquisa-bases-e-apis-2026-09.md`). O histórico de composição não é
publicado por ninguém, de graça.

Um backtest 1998–2026 que use a carteira de hoje **compra empresas que só entraram no
índice depois de darem certo**. Isso não se conserta coletando daqui para frente — só se
declara. Vai para `politica.yaml → limitacoes_declaradas` com a direção do viés
(otimista) e a condição em que deixa de importar (quando houver ≥1 ciclo de
rebalanceamento capturado, ou seja, ~2027).

Mesma família: **backtest anterior a 2026 é reconstrução, não observação.** O acervo
ponto-no-tempo começa no primeiro dia de captura. Isto também é limitação declarada, e é
a mais importante das duas.

> **26/09/2026 — a captura dos eventos da B3 (P-150) herda este viés.** O universo dela é o
> IBOV do dia: quem sai do índice para de ser capturado. Está em
> `limitacoes_declaradas.universo_da_captura_de_eventos_e_o_ibov_do_dia`, com esta pendência.
> O que resolve é uma decisão de desenho: pedir também quem já passou pela carteira, ou todo
> o COTAHIST. Do lado bom, o retrato semanal da carteira gravado pela mesma captura é a
> composição observada daqui para frente.

---

## P-50 · P-05 estava mal formulada — não é número ausente, é campo errado

**Classe:** `BLOQUEIA_O_SISTEMA` (rebaixa a P-05, não a substitui). **Dono:** Claude.
**Gatilho:** antes de escrever qualquer taxa de ETF no `custos.yaml`.

Nas lâminas do Itaú, **"taxa de administração" é só um componente**: há também gestão,
custódia e estruturação. O BOVV11 tem adm 0,02% + custódia 0,01% + gestão 0,07% = **0,10%
total**. O PIBB11, 0,005 + 0,005 + 0,049 = **0,06% total**. A BlackRock, ao contrário,
publica número único (BOVA11 0,10%, SMAL11 0,50%, IVVB11 0,23%).

Guardar isso num campo `taxa_adm` e comparar rotas por ele **subestima sistematicamente o
custo do lado Itaú**. É o F-02 num disfarce novo: o número existe, está certo, e mede
outra coisa. `custos.yaml` precisa de `taxa_total_aa` + `composicao` + `fonte_url` +
`data_doc`.

Os valores acima são **PARCIAL** — vieram de subagente, não da minha leitura. Antes de
entrar no `custos.yaml` cada um precisa da conferência de trecho que a doutrina exige.

---

## P-52 · ANBIMA — o segundo prazo real do projeto, e ele não estava registrado

**Classe:** `DECISAO_DE_DESENHO`. **Dono:** Osvaldo. **Gatilho:** decidir se o projeto
quer série ANBIMA.

IMA-B, IRF-M, ETTJ e debêntures ficam públicos por **5 dias úteis**. O histórico só existe
no ANBIMA Feed — grátis para associado, pago para o resto. Ou o projeto começa a coletar
diariamente, ou aceita não ter a série.

A decisão é de desenho porque muda o escopo: sem IMA-B não há comparação direta de um ETF
de inflação com o índice que ele segue. Hoje o projeto usa Tesouro direto como referência,
e isso pode bastar. **Não decidi por ele.**

> **Decisão dele, 26/09/2026: `52a`** (recomendada) — capturar IMA-B/IRF-M/ETTJ no workflow diário **se** os termos da ANBIMA permitirem; se não, vale 52b. Registro em `docs/decisoes/fila-do-osvaldo.md`.

---

## P-56 · `composicao_capital` só em 2024 — a explicação apareceu, e ela é uma regra

**Classe:** `DECISAO_DE_DESENHO`. **Dono:** Claude. **Gatilho:** ao escrever o parser.

`cvm-enumeracoes-observadas.md` registrou que `composicao_capital` só existe na safra de
2024, e deixou o porquê em aberto. A página do conjunto diz que ele "também disponibiliza
as seções Pareceres e Declarações e **Dados da Empresa/Composição do Capital**".

**Inferência (não leitura):** se só os últimos cinco anos são regerados, as safras
congeladas de 2012 e 2019 ficaram no formato anterior à inclusão dessa seção e **nunca
serão regeradas**.

Isso converte "a estrutura muda entre safras sem motivo" em **"a estrutura de uma safra
congelada é a do dia em que ela congelou"** — que é regra, e regra se testa. O parser
passa a poder afirmar: safra fora da janela tem estrutura estável para sempre; safra
dentro da janela pode ganhar coluna a qualquer semana.

NAO_CONFIRMADO: o ano exato de entrada da seção.

---

## P-66 · Os cortes de distrato entram no YAML como decisão declarada

**Classe:** `DECISAO_DE_DESENHO`. **Dono:** Claude (implementar). **Gatilho:** junto da P-64.

10% / 15% / 20% são os cortes dele. **Ele mesmo escreveu que "não existe percentual
universal"**, então são `DECISAO_DO_USUARIO`, **não** `CRITERIO_MEDIDO` — exatamente como o
bloco C já declara que "dívida líquida/EBITDA abaixo de 3 é costume de mercado, não norma".

Vão para o YAML com o **custo de discordar medido**: quantas empresas mudam de lado se o
corte for 10 em vez de 15.

---

## P-74 · K-01 comparou contra a alternativa errada

**Classe:** `BLOQUEIA_O_SISTEMA`. **Dono:** Claude. **Gatilho:** antes de reescrever a
seção `cofrinho` do `custos.yaml`.

O K-01 mediu **121% × 102%** e concluiu que a mensalidade de R$287,88/ano fazia o
Turbinado perder. **Mas a alternativa real não é o cofrinho comum de 102%** — é o
**Cofrinho do Cartão a 120%**, que ele já tem e onde já estão R$7.681,71.

Com CDI de 13,90% a.a.:

| comparação | diferencial | sobre R$8.181,71 |
|---|---|---|
| 121% × **120%** | **0,139 p.p. a.a.** | **R$ 11,37/ano bruto · R$ 8,81–9,67 líquido** |
| 121% × 102% | 2,641 p.p. a.a. | R$ 216,08/ano bruto |

**As missões valem ~R$9 por ano**, antes de contar o que custa gerá-las (o K-01 registrou
~R$2.500 de gasto no cartão em 3 meses). É o M-01 outra vez: o destino move pouco, o
aporte move tudo — R$50/mês a mais valem R$600/ano, **66 vezes** o prêmio das missões.

E é a **P7** aplicada a dinheiro: manter o 121% depende de lembrar de cumprir tarefa todo
mês. Uma rotina que depende de alguém lembrar não é uma rotina — e aqui ela vale R$9.

**NAO_CONFIRMADO antes de reescrever o K-01:** a tela de 10/09 diz apenas *"Tarefas
concluídas"*; o K-01 registrou R$287,88/ano a partir de capturas de **05/09**. As duas
leituras podem estar descrevendo **planos diferentes**, e isso precisa ser reconciliado —
não reescrever o achado antigo com o dado novo sem entender a diferença.

---

## P-88 · ~~Ninguém mediu a dependência serial~~ **MEDIDA em 19/09 — existe, e são ~8%**

**Dono:** próxima sessão (integrar no `multiplicidade.py`) · **Gatilho:** quando o
`multiplicidade.py` estiver em mãos · **Classe:** `DECISAO_DE_DESENHO` ·
*(laudo em `docs/auditoria/P88-DEPENDENCIA-SERIAL.md`)*

> **A previsão desta pendência estava certa.** Ljung-Box(12) no **resíduo** — a série que o
> bootstrap de fato reamostra: **HML p = 0,031** (tem dependência), **SMB p = 0,166** (não
> tem). O SMB virou o **controle**, e ele não foi construído: estava ali, com a mesma `n`, a
> mesma `k` e o mesmo procedimento.
>
> | L | blocos | HML | vs iid | SMB (controle) | vs iid | líquido |
> |---|---|---|---|---|---|---|
> | 1 | 306 | 3,1099 | — | 2,8473 | — | — |
> | 2 | 153 | 3,2909 | +5,8% | 2,7736 | −2,6% | **+8,4%** |
> | 3 | 102 | 3,3133 | +6,5% | 2,7695 | −2,7% | **+9,3%** |
> | 6 | 51 | 3,2145 | +3,4% | 2,6991 | −5,2% | **+8,6%** |
> | 24 | **13** | 2,9624 | −4,7% | 2,7573 | −3,2% | −1,6% |
>
> **Sinais opostos na faixa informativa** (L = 2 a 8, ≥ 39 blocos). Corte iid 3,1099 →
> **~3,36**; folga do HML de −0,175 → **~−0,45**. O veredito **não muda**, e a conclusão
> **não exige escolher um L** — que era exatamente o que esta pendência pedia evitar.
>
> **Sem o controle, a leitura teria sido a oposta:** em L = 24 são 13 blocos distintos, o
> reamostrador degenera e o corte cai **por artefato**. Eu teria lido *"a dependência não
> importa"*, a conclusão errada pelo motivo errado.
>
> `auditoria/p88_block_bootstrap.py` + 18 testes. **`L=1` reproduz 3,1473**, o número
> registrado em 18/09 — sem essa calibração, um corte maior não provaria nada: poderia ser a
> minha implementação diferindo da registrada.

**O que continua aberto, e é pouco:**

1. **Romano-Wolf não entrou.** O container tinha a versão do `backtest_h1_h3.py` *anterior* a
   18/09, sem `bootstrap_conjunto`. Integrar `corte_*_por_bloco` no
   `alocacao/multiplicidade.py` é o passo, e só então o número absoluto vale para as duas
   correções.
2. **O "líquido" é inferência, não medição** — supõe que o artefato da degeneração é igual nas
   duas séries (plausível: mesma `n`, mesma `k`, mesmo procedimento). `NAO_CONFIRMADO` para os
   ~3,36; **MEDIDO** para o sinal, a faixa e o veredito.
3. ~~A última versão do teste não foi executada.~~ **Executada: 18 passed, ruff limpo** —
   mas o caminho até lá rendeu um achado de método, registrado na §6 do laudo: quando o shell
   voltou, a suíte falhou com o **nome antigo** do teste, e foi essa mensagem que revelou que
   **a chamada que aplicava a correção era justamente a que o shell havia derrubado.** Eu
   documentei como *"corrigido, sem rodar"* algo que estava *"não corrigido, sem rodar"* —
   e foi a nota de incerteza que fez o par ser conferido em vez de acreditado.

<details><summary>o texto original desta pendência, mantido</summary>

O corte de 18/09 sai de um bootstrap que sorteia **meses soltos**. Se os fatores tiverem
dependência serial, a distribuição da estatística é outra e o corte medido está
**subestimado** — na mesma direção do achado (o HML fica ainda mais longe de sobreviver),
o que torna a limitação conservadora e não convidativa.

Medir pede *block bootstrap* com blocos de comprimento declarado. O custo é baixo; o que
falta é escolher o comprimento do bloco **com medição de sensibilidade**, e não por
convenção — senão troca-se uma suposição tabelada por outra.

</details>

---

## P-89 · O corte de m = 8 é `NAO_CONFIRMADO`, e a margem é menor que o ruído

**Dono:** próxima sessão · **Gatilho:** se alguém quiser julgar as oito pré-registradas ·
**Classe:** `DECISAO_DE_DESENHO`

Em m = 8 o corte medido é 2,9337 e o `t` do HML é 2,9351: **0,0014 de diferença**, contra
um desvio de reamostragem de ~0,075. O veredito ali não é "rejeita" nem "não rejeita" — é
`NAO_CONFIRMADO`, e é assim que está escrito. Fechar exige mais repetições (100.000 já
estabilizam a terceira casa) ou aceitar que a família de interesse são os dois `m` que o
sistema calcula, e não o 8 que ninguém usa.

---

## P-90 · Obter os custos das casas que a coleta não alcançou

**Dono:** próxima sessão de pesquisa (nuvem, com subagentes) · **Gatilho:** nenhum —
está pronta para começar · **Classe:** `BLOQUEIA_O_SISTEMA`

Correção dele, 18/09: *"se a informação existe e você não conseguiu, o item não deve ser
excluído — mas o problema de conseguir a informação deve ser solucionado."*

A metade "não excluir" está feita (`docs/auditoria/P90-INFORMACAO-NAO-OBTIDA.md`). **Esta
pendência é a outra metade**, e ela existe porque o campo `pegadinha` guardava um
fracasso do meu raspador como se fosse característica da instituição:

| casa | o que `pegadinha` diz | o que isso descreve |
|---|---|---|
| BTG Pactual digital | *site é SPA sem HTML servido* | o meu leitor, não o BTG |
| Bradesco / Ágora | *PDF de tarifas não pôde ser baixado* | idem |
| Mirae Asset | *HTTP 403; DNS não resolve* | idem |
| Órama, Guide, Necton, Vitreo | SPA / 404 / IPv6 / DNS | idem |

**A regra que sai disto, e ela é geral:** *"não consegui obter"* é um estado do
INSTRUMENTO e tem de ser registrado como tal — com a data da tentativa, o método usado e
o erro. Escrito no campo que descreve a instituição, ele vira, seis meses depois, um fato
sobre ela. É a mesma classe do C-01 (número plausível em prosa que ninguém precisa medir
para repetir).

**Primeira tarefa, e ela não é raspar de novo:** listar as fontes que **não dependem do
site da corretora**. O precedente já existe e é do próprio projeto — `solidez` e
`reclamacoes` dessas casas foram obtidas assim, de balanço e do Ranking de Reclamações do
BCB, e são justamente as que sobreviveram ao fracasso. Candidatos a verificar, nenhum
confirmado: tabela de tarifas na página institucional de RI, taxas de custódia
publicadas pelo Tesouro Direto por instituição habilitada, e a lista de participantes da
B3. **Não registrar nenhuma como fonte antes de abrir e ler.**

---

## P-91 · Comparar retrato de CVM por hash de arquivo produz falso positivo

**Dono:** próxima sessão · **Gatilho:** antes de escrever a rotina semanal automática ·
**Classe:** `DECISAO_DE_DESENHO`

Medido em 18/09 (`docs/auditoria/CVM-PRIMEIRO-RETRATO.md`): o `dfp_cia_aberta_2024.zip` mudou
de sha256 em 14 dias **sem nenhuma mudança de dado** — a CVM regerou o arquivo e 8 linhas
de 94.517 trocaram de posição. `sorted(a) == sorted(b)`.

A estratégia do `CLAUDE.md` §11.6 — *"baixar, comparar, guardar o delta"* — declararia
uma reapresentação aqui e comitaria ruído toda semana. `fase0/manifesto_cvm.py --comparar`
já faz a comparação certa (normalizada por ordem, quatro vereditos nomeados). **O que
falta é a decisão de desenho:** a rotina semanal guarda o delta de *quê* — do ZIP, do CSV,
ou das linhas com chave `(CNPJ, DT_REFER, ORDEM_EXERC, conta)`? A terceira é a única que
sobrevive a uma mudança de separador ou de codificação, e é a mais cara.

---

## P-93 · Treze eventos de 2023 não encontram ticker, e o preço deles fica sem ajuste

**Dono:** próxima sessão · **Gatilho:** antes de usar a série ajustada em qualquer conta ·
**Classe:** `BLOQUEIA_O_SISTEMA`

O A-03/A-04 chegou ao preço. A emissora troca de código, o evento chega com o código
**novo** e o preço de 2023 está sob o **antigo**:

| emissora no evento | ticker de 2023 | eventos dentro da janela |
|---|---|---|
| AXIA (ON, PNA, PNB) | ELET3 / ELET5 / ELET6 | 3 |
| AZZA (ON) | ARZZ3 | 4 |
| ISAE (ON, PN) | TRPL3 / TRPL4 | 4 |
| MOTV (ON) | CCRO3 | 2 |

`ajustar.py` acusa os 13 e sai com código ≠ 0 — **e não remenda**, porque não há a quem
atribuir a marca: as séries de ELET3, ARZZ3, TRPL4 e CCRO3 saem `AJUSTADO` ou
`SEM_EVENTO_CAPTURADO` sem que nada nelas diga que falta um provento.

**O que resolve não é casar nome parecido** — seria o A-01 outra vez, dado do ativo errado
com aparência perfeita. É a ponte ticker↔`codeCVM`↔data, que o A-03 já pediu por outro
motivo: o `codeCVM` vem no mesmo objeto do suplemento e é **estável quando o ticker não é**.

---

## P-94 · O evento na borda desloca o nível e não aparece em teste nenhum — achado A-08

**Dono:** próxima sessão · **Gatilho:** quando o SEGUNDO ano de COTAHIST entrar no acervo ·
**Classe:** `BLOQUEIA_O_SISTEMA`

Oito eventos com `ultimo_dia_com_direito = 28/12/2023` — o **último pregão observado**. A
data ex é 02/01/2024, que o calendário não alcança, então não foi derivada, então o fator
não foi aplicado. Ele multiplicaria a série **inteira**: nenhum retorno de dentro de 2023
muda, e o **nível** fica deslocado.

**É o único defeito do módulo que não muda número nenhum hoje.** Não aparece no degrau, não
aparece no controle, não aparece na suíte. Aparece na hora de emendar 2023 com 2024 — com
um salto artificial exatamente na virada do ano. Sete tickers marcados `NIVEL_INCERTO`:
B3SA3, CMIN3, ENGI3, ENGI4, ENGI11, ITUB3, ITUB4.

**O que NÃO é isto**, e a distinção é o achado: 1.368 eventos têm data ex *posterior* à
janela e também não entraram. Isso é **propriedade** do ajuste retroativo — ele reescala o
passado a partir do fim da série, então todo ano novo reescala tudo. Contar os dois juntos
poria 1.368 linhas no relatório e ensinaria a ignorá-lo.

**Ao entrar o ano seguinte, a borda resolve sozinha** (o calendário passa a alcançar a data
ex). O que esta pendência guarda é a **conferência**: o número de `NIVEL_INCERTO` tem de
cair para zero na emenda, e se não cair é porque a borda mudou de lugar em vez de fechar.

---

## P-95 · O COTAHIST escreve a data ex, e o layout publicado não lista todas as marcas

**Dono:** próxima sessão · **Gatilho:** nenhum — vale como conferência barata a qualquer
momento · **Classe:** `DECISAO_DE_DESENHO`

Achado lateral de 18/09, e ele é gratuito: o campo **ESPECI** do COTAHIST não é só
`ON`/`PN` — carrega a marca de ex (`ON  ED  NM`, `PN  EJ  N1`, `ON  EB  NM`, `ON  EG`).
Medido: em **284 das 293** datas ex derivadas do calendário, o ESPECI muda exatamente
naquele dia, contra uma taxa de fundo de **1,59%** nos 86.736 pares sem evento; e em
**nenhuma** das 293 o dia ex vem sem marca. As 9 restantes são datas ex consecutivas, em
que a véspera já estava marcada — inconclusivas, não contrárias.

**É uma terceira fonte para a data ex, dentro do mesmo arquivo de preço, que não depende de
preço nenhum.** Hoje ela fica em bruto em duas colunas do `degrau_datas_ex_*.csv`, para
conferência humana, e não entra em conta nenhuma.

**O que impede usá-la, e é o mesmo padrão do A-05:** usar exige enumerar as marcas, e a
tabela ESPECI do layout publicado está **incompleta** — 2023 traz `EX`, `EC`, `EBG`, `ERC`,
`EDG`, `ERG`, `EDC` e `EDS`, que ela não lista. A enumeração tem de sair do **dado
observado**, com falha ruidosa no que estiver fora dela, e o `docs/fontes/SeriesHistoricas_Layout.md`
precisa registrar que a tabela dele não é exaustiva — hoje o arquivo diz que as tabelas
incompletas são as de CODBDI e TPMERC, e a de ESPECI foi transcrita como "integral".

---

## P-101 · Quatro moedas no acervo, e uma quebra de 2,75x que nenhum evento societário explica

**Dono:** próxima sessão · **Gatilho:** **só quando a janela do `ajustar.py` passar de
04/07/1994** · **Classe:** `BLOQUEIA_O_SISTEMA` · *(achado C-03)*

> **19/09 — MEDIDA e instrumentada, ainda NÃO aplicada.** Nasceu `fase0/moeda.py`: varre o
> acervo, acha as fronteiras de `MODREF`, mede o fator pela razão do mesmo `CODNEG` com o
> controle do dia anterior ao lado, e devolve `QUEBRA_MEDIDA` / `SEM_QUEBRA` /
> `NAO_CONFIRMADO`. 19 testes.
>
> ```
> COTAHIST_A1986  19860227->19860304  CR$->CZ$    274  1.1973  ctrl 1.0000 (n=339)      --  SEM_QUEBRA
> COTAHIST_A1989  19890113->19890118  CZ$->NCZ$   198  0.9677  ctrl 1.0000 (n=307)      --  SEM_QUEBRA
> COTAHIST_A1990  19900313->19900319  NCZ$->CR$     2  0.7142  ctrl 1.0000 (n=238)      --  NAO_CONFIRMADO
> COTAHIST_A1994  19940630->19940704  CR$->R$     136  0.3644  ctrl 1.0106 (n=251)  2.7440  QUEBRA_MEDIDA
> ```
>
> **Ele NÃO aplica a reexpressão, e há um teste que prende isso.** Escolher a base —
> reexpressar tudo para R$? manter cada ano na moeda dele? — é **decisão de desenho sua**,
> e a P6 manda deixar a lacuna declarada em vez de inventar critério. Mesmo desenho do
> `refinar.py` com o `FACTOR_AMBIGUO`.
>
> **Achado lateral, e ele veio de imprimir o `n` do controle:** nas fronteiras de 1986,
> 1989 e 1990 o controle mede **1,0000 exato** com 339, 307 e 238 pares — em plena
> hiperinflação. Não é mercado estável: é a **maioria dos papéis repetindo o preço** do dia
> anterior, mercado raso. Isso *fortalece* a leitura — se o dia comum de 1986 mede 1,0000,
> a fronteira medindo 1,1973 teve mais movimento que o normal, e ainda assim nada perto de
> 1.000x.

> **19/09 — NÃO está no caminho crítico hoje, e isso é decisão de ordem, não de mérito.** O
> próximo passo é `ajustar.py` sobre **2021–2025**, e essa janela está **inteira em `R$`**.
> Pôr a P-101 na frente por ser o achado mais novo seria escolher tarefa pelo frescor — o
> erro que a P-44 registra.
>
> E a explicação do achado avançou: o header mostra que 1986–1995 foram **todos gerados em
> 19991210**. `MODREF` é **rótulo histórico**, não a unidade gravada — ver
> `docs/fontes/b3-cotahist-leiaute.md` §4.

A série agora começa em 02/01/1986 e atravessa seis planos econômicos. O campo `MOEDA`
(posições 53–56) muda **dentro do mesmo arquivo anual**: `CR$`, `CZ$`, `NCZ$`, `R$`.

**Medido — razão do mesmo ticker, mercado à vista, com controle do dia anterior:**

| troca | pares | mediana | |
|---|---|---|---|
| 1986 Cruzado (1.000:1) | 274 | 1,197 | **sem quebra** — já reexpresso |
| 1989 Verão (1.000:1) | 198 | 0,968 | **sem quebra** |
| 1993 Cruzeiro Real (1.000:1) | 182 | 0,998 | **sem quebra** — e a `MOEDA` nem distingue as duas |
| 1990 Collor | **2** | — | `NAO_CONFIRMADO` — o mercado parou |
| **1994 Real (CR$ 2.750 = R$ 1)** | 136 | **0,364** | **QUEBRA**, contra controle de 1,011 |

**Três das quatro trocas não deixam quebra.** A suposição natural — *"toda troca de moeda
é uma quebra"* — erra em 3 de 4, e só a medição diz qual. A tabela de planos econômicos
teria acusado quatro e acertado uma.

**A do Real é real:** 1/0,364 = **2,744**, consistente com os 2,750 da lei, com o resto
sendo variação de um pregão. E ela entra na série ajustada como **−63,6% no mercado
inteiro, em um dia, sem causa** — porque troca de moeda não é evento societário, não tem
`factor`, não tem data-ex e não existe no silver.

**É o F-02 na forma mais cara:** não é insumo ausente virando zero — é insumo
**presente, correto e anunciado** que ninguém lê. E é o C-01 em escala de mercado.

**O que falta, e é pouco:** varrer os 33 arquivos não abertos para fechar a enumeração
`OBSERVADO` de `MOEDA`; medir o fator de cada quebra encontrada (nunca tabelar); e decidir
se a série utilizável começa em **04/07/1994** ou em **02/01/1986** — decisão que entra em
`limitacoes_declaradas` ou vira trabalho, mas não fica em silêncio.

---

## P-104 · Vinte e quatro achados são citados só em código, e podem não ser achados

**Dono:** próxima sessão · **Gatilho:** quando o `ACHADOS.md` estiver em mãos ·
**Classe:** `DECISAO_DE_DESENHO` · *(levantado por `auditoria/achados_ancorados.py`)*

A guarda que nasceu com a Decisão C varreu o repositório e achou **45 códigos citados sem
definição em `.md` nenhum**. Vinte e um caem quando o `ACHADOS.md` entrar na árvore — ele
não estava. **Os outros 24 são citados SÓ em código:**

```
B-05  B-06  B-07  B-08  D-1   H-02  K-04  K-05  K-08  K-11
V-02  V-03  V-04  V-05  V-06  V-07  V-08  V-09  V-10  V-12
V-13  V-14  V-15  Z-01
```

**E parte deles provavelmente não é achado.** `K-04` aparece com as teses (`teses.yaml`,
`tese.py`), e os `V-*` aparecem no changelog do `politica.yaml` como itens de um laudo de
agosto. **Namespaces diferentes com a mesma forma.**

**Não os pus na linha de base, e a razão é a régua §5-B:** *medir levanta o candidato; quem
o promove é a leitura* — e eu não tenho o `ACHADOS.md` nem os laudos de agosto para ler.
Jogá-los na exclusão sem motivo seria pior que deixá-los acusados: viraria **cobertura
falsa**. Ficam nomeados em `CANDIDATOS_19_09`, com um teste que impede que virem linha de
base sem o motivo escrito.

**O que decidir:** para cada um, ou o motivo (*"é tese"*, *"é item do laudo de agosto"*) e a
saída para `NAO_SAO_ACHADOS`, ou a constatação de que é achado de verdade — e aí **é um nome
que o código cita e ninguém pode consultar**, que é o defeito que esta guarda existe para
pegar.

---

## P-112 · Eventos de quantidade antigos faltam no silver, e o COTAHIST sabe onde

**Dono:** Claude Code · **Gatilho:** antes de usar qualquer série ajustada anterior a 2024 em
backtest · **Classe:** `BLOQUEIA_O_SISTEMA`

A-11: o ESPECI marca `EDB`/`EJB` em 11 papéis-dia de 2021–2024 sem evento de quantidade no
silver, e a série da CMIG fica −27% num dia. O suplemento da B3 devolve janela **recente**.
**Primeiro passo, e ele é barato:** rodar a testemunha sobre o acervo **inteiro** (1986–2025)
e contar papéis-dia com marca B/G e sem evento — mede o tamanho da lacuna **antes** de
procurar fonte para ela. Sem isso, qualquer série antes de 2024 carrega degrau não removido
e o `ajuste_status` diz `AJUSTADO`.

---

## P-119 · A página de investimento estrangeiro da B3 não está no acervo

**Dono:** Claude Code (captura) · **Gatilho:** antes de a regra do não residente entrar em
qualquer conta · **Classe:** `DECISAO_DE_DESENHO`

O laudo do C-02 afirma que o investidor não residente tem regime próprio, com exceção do país
de tributação abaixo de 20%, que paga 15%. **A afirmação veio do enunciado dele, não de fonte
primária lida** — a página não está em `docs/fontes/` e eu não a capturei nesta sessão.

Está marcada `NAO_CONFIRMADO` no laudo e no `P113-MEDIDO.md`, em vez de ficar implícita, que
é o que a **§5-B.13** manda: *"não dá para fazer X" só se escreve depois de tentar X e falhar,
com o erro transcrito*. **Eu não tentei** — o que falta é uma captura, não um caminho.

Quando for capturada, o limiar dos 20% se confere **contra a norma que o define**, não contra
a página que a resume — é a §5-B.5: *fonte primária ganha depois de se verificar qual
dispositivo a cláusula alcança*. A isenção dos R$ 20 mil já está fechada
(`docs/fontes/lei-11033-2004-planalto.md`, art. 3º, I).

---

## P-116 · O critério da janela entrou no mesmo commit que os resultados

**Dono:** Claude Code · **Gatilho:** toda medição nova contra o acervo · **Classe:**
`DECISAO_DE_DESENHO`

Os critérios do `fase0/test_ajustar_janela.py` foram escritos antes da primeira corrida, mas
entraram no **mesmo commit** que os números (`b54787b`). Um leitor externo não tem como
distinguir critério de resultado: **"pré-registrado" não é verificável pela P4.** No laudo e no
`ACHADOS.md` o rótulo passou a ser *"declarado pré-registrado, sem impressão digital"*. O
processo que evita a repetição: critério em um commit, **empurrado**, e só então a corrida
— o hash do commit do critério é a impressão digital.

---

## P-122 · `lightgbm` e `tabpfn` nunca foram medidos contra a faixa fechada

**Dono:** Claude Code (sessão local) · **Gatilho:** antes da ML-1 · **Classe:**
`BLOQUEIA_O_SISTEMA` · ⚙ **exige o desktop**

O `preregistro-ml-v2.md` §11 deixa as versões `NAO_CONFIRMADO` porque a consulta ao PyPI
**da nuvem** foi recusada por `robots.txt`. A sessão local não tem essa recusa.

> **27/09/2026 — degrau 1 da escada (§5-B.18), da nuvem:** `curl https://pypi.org/pypi/tabpfn/json`
> respondeu **HTTP 200**. O `tabpfn` 9.0.0 declara `torch>=2.5` e `lightgbm>=4.4` entre as
> dependências obrigatórias: **o TabPFN traz `torch`**. A recusa era da ferramenta de busca, não
> do PyPI. O resto da pendência (o `--dry-run` contra a faixa fechada e o tamanho) segue aberto,
> e talvez não exija o desktop: o índice do PyPI responde desta sessão. O conserto é
`py -3.11 -m pip install --dry-run lightgbm tabpfn "numpy==2.4.4" "pandas==3.0.2"` — e, se o
TabPFN trouxer `torch`, anotar o tamanho. É a entrada
`dependencias_da_familia_aprendizado_nao_medidas`.

---

## P-123 · O motor não aplica IR na venda de renda variável

**Dono:** próxima sessão · **Gatilho:** quando o motor ganhar rebalanceamento ou fase de
retirada · **Classe:** `BLOQUEIA_O_SISTEMA`

Era limitação declarada desde 04/09 **sem pendência** — o portão da §5-B.16 a cobrou. O vício
favorece o ETF (a isenção de R$ 20 mil/mês é só da ação), que é exatamente a decisão A05.
Efeito zero na acumulação sem venda. Entrada `ir_na_venda_de_renda_variavel`.

> **03/10/2026 — a decisão do Osvaldo torna a venda um compromisso.** Ao ler a F0 (item 20 da
> fila) ele disse "quero que o motor recomende venda" e recusou o texto fixo "o motor não
> recomenda venda" como permanente. A pendência deixa de ser só limitação do rebalanceamento: é
> pré-condição de um compromisso de produto. **Classe e gatilho não mudam.** A ordem:
> 1. **regra de venda pré-registrada** (P4), decisão dele;
> 2. **IR da venda lido na fonte primária**;
> 3. **o motor emite `venda.motivo`**, com teste que falha antes da mudança.
>
> Os motivos a emitir são os três do F5 do [mapa de telas](ux/mapa-de-telas-v1.md). **Até
> fechar, vale o F5 do mapa, PROVISÓRIO:** a T1 diz que o motor ainda não avalia venda. Esse
> intervalo é **proposta do Claude**, que ele pode vetar.

---

## P-128 · Open Finance para posições e aporte — **decisão sua**

**Dono:** Osvaldo (decidir) · **Gatilho:** nenhum · **Classe:** `DECISAO_DE_DESENHO`

Ideia 4b. O aporte realizado e as posições (P-02) são o único insumo em que ele está no
caminho crítico todo mês (U-01, P7). É **candidata a pesquisa, não a integração**: cobertura,
custo e o que fica guardado com o terceiro estão `NAO_CONFIRMADO`, e é o dado mais sensível do
projeto — o mesmo que o `estado.yaml` protege ficando fora do git. A pergunta de privacidade
vem antes da técnica.

> **Decisão dele, 26/09/2026: `128b`** (**diverge da recomendada (128a)**) — **pesquisar** Open Finance (cobertura, custo, o que fica com o terceiro), sem integrar nada. Registro em `docs/decisoes/fila-do-osvaldo.md`.

---

## P-129 · Macro sem vintage — **decisão sua**

**Dono:** Osvaldo (decidir) · **Gatilho:** quando uma variável macro entrar num pré-registro ·
**Classe:** `DECISAO_DE_DESENHO`

Ideia 4c. O BCB SGS não guarda versões: série revisada substitui a antiga, então macro no
backtest seria o valor de hoje, não o publicado em `t`. Hoje não morde (o pré-registro ML não
usa macro). No dia em que usar, a proposta é uma entrada em `limitacoes_declaradas`, `tipo:
FISICA` — a fonte não publica as versões —, ou buscar vintage em outra fonte (ALFRED cobre
EUA, não BCB). A decisão é qual das duas.

> **Decisão dele, 26/09/2026: `129b`** (recomendada) — começar agora a guardar a versão própria das séries do SGS no armazém; para o passado, `FISICA` quando entrar num pré-registro. Registro em `docs/decisoes/fila-do-osvaldo.md`.

---

## P-133 · O acervo da CVM tem 49 arquivos com sha256 e nenhum com origem declarada

**Dono:** Claude Code · **Gatilho:** antes de a captura virar rotina (P-57) ·
**Classe:** `BLOQUEIA_O_SISTEMA`

Visto na primeira captura integrada (24/09): o `manifesto_cvm.py` imprime *"P-06: 49 de 49
arquivo(s) tem sha256 e NAO tem de onde vieram"*. O `docs/acervo/cvm/origem.csv` nunca
existiu. A URL de cada arquivo canônico está no registro (`capturas.csv`), e a de cada
snapshot também, na linha `deslocado`. Mas o manifesto não lê o registro, e os
`(1).zip` do navegador não têm linha nenhuma. As saídas: o manifesto ler a origem do
registro (os dois papéis continuam separados, e só a **URL** atravessa), ou a captura
escrever o `origem.csv`. Não foi feito junto para não misturar a integração com uma mudança
no `manifesto_cvm.py`, que também serve ao acervo da B3.

**24/09, depois da limpeza:** o acervo tem **45** arquivos, e os dois snapshots
`__v20260913__` de 2024 vieram de `(1).zip` do navegador e **não têm linha no registro**.
A origem deles, declarada aqui para quando a P-133 for feita, é a mesma URL do canônico,
baixada à mão em 18/09 (manifesto de 18/09).

---

## P-150 · Os eventos societários da B3 foram capturados uma vez e não têm rotina nem armazém

**Dono:** Claude Code (escrever) · o desktop (subir o acervo de 11/09) · **Gatilho:** nenhum — a
fonte pode sumir sem aviso (V-01) · **Classe:** `BLOQUEIA_O_SISTEMA`

Achada ao fechar a P-47 e a P-49, em 26/09. A captura de 11/09 (74 emissoras, 132 páginas de
proventos) mora **só no disco dele**: `docs/acervo/b3/inventario-armazem.csv` lista apenas os 41
COTAHIST, e o `captura_cvm.yml` não tem passo de eventos. No CI, os três testes de
`fase0/test_coletar_b3.py` que leem o acervo são pulados (*"nao ha acervo de eventos neste
disco"*, execução `36178274615`).

É o insumo que o V-01 chamou de **mais perecível** do projeto — endpoint não documentado, sem
SLA, sem espelho — e é a mesma forma da P-57: uma captura que depende de alguém lembrar. O que
falta: (1) subir o acervo de 11/09 ao R2 — conferir antes se o `subir_acervo_local.py` cobre a
pasta de eventos; ⚙ exige o desktop; (2) um passo no workflow que rode o `coletar_b3.py` numa
cadência declarada em `politica.yaml → regimes_de_captura.b3`, com o mesmo portão, o mesmo teto
e o mesmo registro. Os termos da B3 permitem capturar para uso pessoal e vedam publicar
(P-136): o armazém é privado, e os eventos não entram na release da CVM.

**26/09, parte 2 feita (esta sessão, na nuvem).** `fase0/capturar_eventos_b3.py` roda o
`coletar_b3` numa pasta temporária e sobe cada arquivo ao armazém pela chave de conteúdo
(`b3/indice_carteira|eventos_suplemento|proventos/…`), com o teto e o registro da CVM
(`docs/acervo/b3_eventos/capturas.csv`). O passo `captura_eventos_b3` entrou no
`captura_cvm.yml`; a cadência é dado (`politica.yaml → cadencias_de_captura.b3_eventos`,
segunda-feira, com motivo), e fora dela o script sai 0 sem pedir nada à B3. O acervo fica em
`limitacoes_declaradas.captura_de_eventos_b3_ainda_nao_rodou_no_executor` até o cron provar:
`regimes_de_captura` exige a execução, e a chave `b3` já é do COTAHIST. Rodada real daqui, com
armazém local: 5m44s, 207 arquivos, 4,3 MB, saída 0 com uma ressalva (MBRF sem evento nenhum —
A-03). **Fecha quando** o passo sair verde no cron de uma segunda (a primeira é 28/09); nesse
dia, `b3_eventos` entra em `regimes_de_captura` com a execução e a limitação sai.

~~**A parte 1 não roda como está:** `subir_acervo_local.py` só lê `data/bronze/b3/cotahist` e
`…/isin`, e não as pastas `indices`, `eventos` e `proventos`. Falta estendê-lo (Claude Code, na
nuvem; reusar `capturar_eventos_b3.arquivos_do_coletor`, para que o 11/09 caia nas mesmas chaves
que o cron) antes de ⚙ o desktop rodar o `--aplicar`.~~ **Estendido em 26/09.** O
`subir_acervo_local.py` agora planeja `data/bronze/b3/{indices,eventos,proventos}/dt_captura=…`.
O recurso e o nome vêm das mesmas funções do passo do cron (`capturar_eventos_b3.RECURSOS` e
`nome_no_armazem`), e um teste compara as chaves do plano com as que o passo daria para os
mesmos arquivos. O inventário vai para `docs/acervo/b3_eventos/`. A versão é o dia da captura,
e o dia mais recente é o canônico. O `manifesto.jsonl` do coletor sobe como log, fora do teto.
Fora de `dt_captura=…/*.json`, o arquivo sai `DESCONHECIDO` e não sobe. O padrão continua sendo
o plano. **Falta só a parte do desktop** (roteiro em `## Ao voltar ao desktop`).

**Achado lateral (26/09):** `fase0/acervo.py → REGISTROS` não lista o registro
`docs/acervo/b3_eventos/capturas.csv`. Com isso, o `abrir()` enxerga as versões dos eventos pelo
inventário da carga, mas não as que o cron registrar, e o `frescor()` não vigia essa captura.
**No dia em que a P-150 fechar**, junto com a entrada em `regimes_de_captura`, o registro entra
em `REGISTROS`. Antes disso não entra, porque o `frescor` acusaria `NUNCA_OBSERVADO` enquanto o
cron não roda. **Guardado desde 26/09:** `acervo.regimes_sem_registro()` e
`test_P150_todo_regime_tem_o_registro_em_acervo_REGISTROS` reprovam um regime cujo registro
não esteja em `REGISTROS`. Esquecer a segunda metade deixa a suíte vermelha, não calada.

**O universo é o IBOV do dia (26/09, registro).** A captura lê a carteira do dia e pede eventos
só de quem está nela. Quem sai do índice deixa de ser capturado na segunda seguinte: o que já
subiu fica no armazém, e o evento novo não entra mais. É o viés da P-48, com direção
**otimista** no universo. Na série de quem saiu, o erro não tem sinal conhecido: um grupamento
perdido vira alta no ajuste, e um provento perdido vira queda. Declarado em
`limitacoes_declaradas.universo_da_captura_de_eventos_e_o_ibov_do_dia`, ligado à P-48 e não a
esta, porque não acaba quando esta fechar.

---

## P-146 · Três passos das métricas que só ele pode dar

**Dono:** Osvaldo · **Gatilho:** nenhum; quanto antes, antes o semanal fica verde ·
**Classe:** `BLOQUEIA_O_SISTEMA` (o semanal nasce vermelho pelo item 1)

1. **Subir o FCA ao R2** (CV-07): `py -3.11 fase0/subir_acervo_local.py --aplicar`, com as
   `R2_*` no ambiente. Sem isso, o job semanal lista os 17 FCA como falta e fica vermelho, que é
   o comportamento certo.
2. **Primeira execução do semanal:** Actions → *Testes* → *Run workflow*. O `gh` não está
   instalado nesta máquina, e a §5-A manda pedir.
3. **A medição de mutação:** Actions → *Mutacao* → *Run workflow*. Até essa execução, a
   configuração `[tool.mutmut]` é `NAO_CONFIRMADO`. Cada sobrevivente vira achado candidato.

> **25/09, os itens 2 e 3 rodaram no branch `claude/brave-gates-g4zm6k`, disparados pela sessão
> na nuvem a pedido dele** (conferir os workflows depois da troca para node24). Dois achados:
>
> - **CI-03: a *Mutacao* sai verde sem ter medido nada** (execução `36152691790`, 55 s). Os 4.935
>   mutantes ficaram `not checked`. A rodada limpa do mutmut falha (`failed to collect stats`)
>   e o `set +e` do workflow engole o erro. Reproduzido num clone: fora os `privado`, **20 testes**
>   quebram na cópia `mutants/`. A cópia não leva `.git`, `.github`, `.gitignore` nem `PENDENCIAS.md`
>   (os de `test_workflow_captura`, `p67`, `p82` e `limitacoes_tipo`), e os testes que varrem o
>   fonte veem a instrumentação do mutmut (`test_nenhum_literal_de_politica_fixo_no_modulo`
>   acusa `101`, `1.01`, `366.25`…). **Decisão dele:** restringir os testes da mutação aos
>   unitários dos quatro módulos mutados, ou marcar os testes de repositório e excluí-los por
>   marcador. Nos dois casos o workflow passa a falhar quando nenhum mutante é checado.
> - **CI-04: o job `completo` do *Testes* fica vermelho em dois testes que já falhavam no `main`**
>   (execução `36152684302`, a primeira do job). (a) `test_P97_nao_sobrou_ZIP_sem_origem_no_acervo`:
>   os 6 `COTAHIST_D*.ZIP` da P-135 têm origem no `capturas.csv`, não no `origem.csv`. (b)
>   `test_REAL_todo_ano_fixado_confere_nesta_maquina`: o pin de 2026 (`fb3546ed…`) não é a versão
>   vigente, a materialização só copia a vigente, e o R2 não tem segredo no passo dos testes.
>   Propostas no PR osvaldosantana/bastter#1. **Decisão dele** nas duas.
>
> A *Captura CVM* (`36152688055`) ficou verde com checkout v7.0.1, e o push do bot funcionou.

> **25/09, fim do dia (Claude Code, local), e o estado mudou:**
>
> - **Item 1 FEITO:** o FCA e o `cad` estão no R2 (carga das 14:23Z, 18 envios, inventário
>   commitado). O *Testes #9* mediu **0 faltas**.
> - **CI-04 CONSERTADA**, as duas metades, pelas propostas do PR #1: `origem_declarada` lê
>   também o `capturas.csv`, e o `materializar_acervo` põe as 23 versões fixadas do ML no
>   cache. Prova na árvore do runner, com as quatro suítes verdes sem `R2_*` no passo dos
>   testes. Detalhe em `ACHADOS.md → CI-04`.
> - **CI-03: o portão entrou, a causa não.** A *Mutacao* publica a contagem como anotação
>   e **fica vermelha** quando nada é testado. Com a rodada limpa ainda falhando, a próxima
>   execução **vai sair vermelha**, e isso é o certo. A escolha entre restringir os testes
>   e excluir por marcador continua **dele**.
> - **Falta (dele):** *Run workflow* em **Testes** (espera-se verde) e em **Mutacao**
>   (espera-se vermelho, com `gerados=… testados=0` na anotação).

> **26/09, medido pela nuvem no log:** o item 2 **rodou** — *Testes #16* (`36178274615`), disparo
> manual de 25/09 19:12Z — e saiu vermelho por **um** teste, a guarda do GIT-01 vendo duas branches
> de sessão abertas naquele minuto. Não é dele: é a **P-151**. A próxima rodada do semanal é a
> agendada de segunda, 28/09, 11:00 UTC, e não precisa de clique. **Sobra dele:** a escolha do CI-03
> e o *Run workflow* da *Mutacao* depois dela — os dois na `docs/decisoes/fila-do-osvaldo.md`.

> **Decisão dele, 26/09/2026: `146b`** (recomendada) — marcador `repositorio` nos testes que leem o repositório, excluído na mutação; depois ele dispara a *Mutacao*. Registro em `docs/decisoes/fila-do-osvaldo.md`.

> **26/09/2026 — 146b aplicada, e ela revelou a segunda causa do CI-03.** Marcador
> `repositorio` em 17 testes (os que leem `.git`, `.github`, a raiz ou o próprio fonte) e a
> mutação passa a rodar `-m "not slow and not repositorio and not privado and not acervo"`;
> `auditoria/test_workflows.py::test_146b_...` prende a configuração. **Medido aqui com o
> mutmut 3.8.0 pinado:** a rodada limpa, que falhava, agora **passa** — 1017 testes verdes
> dentro da cópia `mutants/`. E o mutmut para em outra coisa: *"tests recorded trampoline hits
> but none match any mutant key"* — os testes importam `ajustar` (por `sys.path`) e o mutmut
> espera `fase0.ajustar`. **Nenhum mutante casa.** Disparar a *Mutacao* agora daria vermelho por
> esse motivo, previsto. O conserto é de engenharia e é do Claude Code: rodar o mutmut por
> pacote (com `cwd` em `alocacao/` e `fase0/`) ou fazer os testes importarem pelo caminho do
> pacote. **Só depois dele o *Run workflow* é pedido ao Osvaldo.**

---

## P-144 · Emenda de desenho não tem mecanismo que a leia — a P-138 só enxerga emenda de orçamento

**Dono:** Claude Code · **Gatilho:** ao escrever a montagem da ML que decide o início do
desenvolvimento · **Classe:** `DECISAO_DE_DESENHO`

Medido em 25/09: `preregistro.emendas_publicadas()` devolve `[]` para a emenda 1. Ela está
publicada, e o sha256 no `origin/main` é igual ao do disco (`1aac96023fdc0de9`). O mecanismo da
P-138 lê `pesquisa.emendas` do `politica.yaml`, só aceita `variantes_adicionais ≥ 1`, e a família
ML nem está em `estrategias_pre_registradas`. Esta emenda não acrescenta variante. Forçá-la ali
inflaria o `m` com uma especificação que não existe. **Não construído agora:** uma função de
conferência sem consumidor seria a P-77/P-106. O consumidor é a montagem, que deve abrir
`preregistro-ml-v2.md` e as emendas **pelo conteúdo no ramo publicado**, como a P-138 faz com o
orçamento, e recusar rodar se o sha divergir.

---

## P-130 · As posições do header do COTAHIST moram em Python

**Dono:** Claude Code · **Gatilho:** no próximo toque em `conferir_cabecalho` ou no leiaute ·
**Classe:** `DECISAO_DE_DESENHO`

Achado lateral da P-125. O `cotahist-v02.yaml` tem as posições do registro `01` desde a P-105,
mas o header (`00`) não: `conferir_cabecalho` fatia `[11:15]` e `[23:31]` no código. É a P-105
num registro vizinho — e foi exatamente numa fatia escrita à mão que o erro de um entrou. O
leiaute rev. 02 descreve o header; transcrevê-lo para o YAML e ler de lá é o conserto. Não foi
feito agora para não misturar mudança de esquema com o conserto de um valor.

---

## P-153 · Ranking de reclamações do BC na fonte, e o Reclame Aqui atualizado · era P-A9

**Dono:** sessão de pesquisa (nuvem) · **Gatilho:** antes de usar reclamação de cliente como
argumento de marca ou de produto · **Classe:** `DECISAO_DE_DESENHO`

Aberta pela [pesquisa de fundação](marca/pesquisa-fundacao-2026-09.md) (A9) e não fechada
pela [rodada do Pix](marca/pesquisa-pix-e-pendencias-2026-09.md) (§2.3): o ranking do
Banco Central foi lido por imprensa, com duas fontes divergindo sobre o 2º trimestre de 2026, e
o único dado do Reclame Aqui sobre investimentos é de 2017. O que fecha: a consulta no site do
BC, transcrita em `docs/fontes/` com data, e o ranking da categoria "Corretoras e Bancos de
Investimentos" do Reclame Aqui com a data da leitura.

---

## P-154 · Medir a fatia de quem investe sem segurança na decisão (H-A1) · era P-A1

**Dono:** Osvaldo (decide se, como e com quanto dinheiro) · Claude (desenho do questionário) ·
**Gatilho:** antes de dimensionar o público de entrada em qualquer texto comercial ·
**Classe:** `DECISAO_DE_DESENHO`

A rodada 1 estima ~28,6 milhões no perfil "Diversifica" (`PARCIAL`, derivado da ANBIMA), mas
**ninguém mediu** quantos deles se sentem inseguros ao decidir. A hipótese H-A1 propõe três
sinais: paralisia, dependência e arrependimento. Sem essa medição, "o público é grande" é
ordem de grandeza do perfil, não do público.

> **27/09/2026 — a H-A2 passa para cá** (resposta n-A dele). Origem: rodada 1, §7
> ([pesquisa de fundação](marca/pesquisa-fundacao-2026-09.md)): *"o primeiro susto com
> queda é um evento comum entre quem saiu da poupança, e está associado a abandono."* Ela
> tinha ficado sem pendência quando a nota de 26/09 na P-156 deixou lá só as hipóteses de
> interface. Como a H-A1, é pergunta sobre o público, não sobre a tela.

---

## P-156 · Teste com pessoas das hipóteses de interface e de marca

**Dono:** Osvaldo (recrutamento e custo) · Claude (roteiro, estímulos e pré-registro do
critério) · **Gatilho:** quando a especificação da F0 existir (`PLANO.md` §3-F0) ·
**Classe:** `DECISAO_DE_DESENHO`

Nenhum requisito foi validado com o público ([requisitos de
interface](marca/requisitos-interface-v1.md), §4 e §5). Entram no teste: H-A1 e H-A2
(rodada 1), H-C1 (a camada 1 é entendida sem ajuda), H-C2 (a faixa numérica não custa
confiança, replicação no Brasil), RI-15 (a pergunta de intenção é respondida sem ajuda) e as
hipóteses H1 a H4 do teste de marca. O critério de cada uma é gravado antes de olhar (P4).
As H1 a H4 vêm de um pré-registro do teste de marca de 20/09 que **não está no repositório**
(a rodada 1 o cita e diz que o atualiza); trazê-lo do Projeto no claude.ai é o primeiro passo
desta pendência, antes de qualquer estímulo ser mostrado a alguém.

> **26/09/2026:** o escopo de marca (H1 a H4) passa para a P-162, na etapa 3. Esta pendência
> fica com as hipóteses de interface (H-C1, H-C2, RI-15), na etapa 4. O "primeiro passo"
> (trazer o pré-registro de 20/09) está feito:
> `docs/marca/preregistro-teste-de-marca-2026-09-20.md`.

> **27/09/2026 — a H4 do teste de marca vem para cá** (resposta s-a dele, S5). "Esse público
> aceita mais informação por tela do que um iniciante aceitaria" não é testável no teste de
> marca, cujo filtro exclui iniciantes. Aqui, onde o teste de interface pode ter os dois
> grupos, ela entra com o critério gravado antes (P4).

---

## P-157 · Importação de carteira: quais formatos são viáveis

**Dono:** sessão de pesquisa (nuvem) · **Gatilho:** antes de desenhar a tela O4 do [mapa de
telas](ux/mapa-de-telas-v1.md) além do "digitar as posições" · **Classe:**
`DECISAO_DE_DESENHO`

O mapa prevê três caminhos (importar arquivo, digitar, começar do zero) e não sabe quais
arquivos existem. Candidatos a levantar na fonte: extrato da área do investidor da B3, nota de
corretagem, exportação das corretoras e o Open Finance (que a P-128 pesquisa). Critério: o
formato traz posição e custo com procedência, e o dado fica no aparelho (é dado de usuário).

---

## P-158 · Parecer jurídico sobre o enquadramento do MEOL

**Dono:** Osvaldo (contratar) · **Gatilho:** antes de qualquer usuário além dele, ou de
qualquer texto comercial público · **Classe:** `DECISAO_DE_DESENHO`

Nenhum documento de marca é parecer: todos o declaram. As perguntas abertas: se a decisão
mensal com procedência é recomendação de investimento no sentido da regulação; como os bancos
com agente de IA que recomenda e executa se enquadram ([rodada
2](marca/pesquisa-marcas-rodada2-2026-09.md), §4.1, `NAO_CONFIRMADO`); e se "padrão é
recomendação" (RI-07) se sustenta. Depende da P-159: o parecer começa pela norma lida.

> **26/09/2026 — a P-159 fechou, e deixa três perguntas para cá.** A Resolução CVM 19 está
> transcrita em [`docs/fontes/cvm-resolucao-19-consolidada.md`](fontes/cvm-resolucao-19-consolidada.md).
> (1) O art. 1º exige prestação "de forma profissional" a um cliente. O uso pessoal dele fica
> fora? A partir de qual momento o MEOL passa a ser serviço? *(26/09/2026: a transcrição dava
> "o uso pessoal não é prestação de serviço" como confirmado. Virou `INFERENCIA`, nota
> N-PESSOAL na transcrição: o texto lido não diz isso, e a resposta é do parecer.)* (2) O art. 2º, parágrafo único, I, e
> o art. 16, II, remetem à norma de adequação ao perfil do cliente, que não foi lida. (3) As
> Resoluções CVM 21 e 35, citadas pela pesquisa, não foram lidas. Nenhuma das três se resolve
> por leitura: é parecer.

---

## P-160 · Telas sem campo no contrato de saída da F0

**Dono:** Osvaldo (decidir o que entra) · Claude Code (especificar) · **Gatilho:** antes de
desenhar qualquer uma destas telas · **Classe:** `DECISAO_DE_DESENHO`

A especificação da F0 ([`docs/ux/F0-contrato-de-saida.md`](ux/F0-contrato-de-saida.md),
§5) aplicou a regra do mapa de telas: tela sem campo não se constrói. Cinco ficaram sem campo:
a O5 (escolhas declaradas, com o porquê), a aba "e se" da T3 (que é contrato de chamada, não
de campo), as empresas da T4 (o motor decide rota, não papel), o aviso de queda do RI-04 e a
comparação líquido contra líquido do RI-11. Cada uma ganha campo na especificação, ou sai do
mapa com o motivo escrito.

---

## P-161 · A versão do `pyproject.toml` diverge da do `politica.yaml`, e nada as prende

**Dono:** Osvaldo (decidir qual é a fonte) · Claude Code (o teste que prende) · **Gatilho:** a
próxima subida de versão do `politica.yaml` · **Classe:** `DECISAO_DE_DESENHO`

O `pyproject.toml` diz `version = "1.18.0"`, com o comentário *"acompanha politica.yaml ->
meta.versao"*. O `politica.yaml` está em **1.35.0**. Medido em 26/09 no clone raso da nuvem
(113 commits visíveis): as duas já divergem no primeiro commit visível, `b0f494a` de 23/09
(1.18.0 contra 1.22.0), e a política subiu treze versões depois disso sem o `pyproject`
acompanhar. Antes de 23/09, este clone não mostra. Nenhum código lê a versão do `pyproject`
(`grep` em `alocacao/`, `fase0/`, `auditoria/` e `tools/`). A da política vai na procedência de
todo resultado (`politica_versao`, lida três vezes em `alocacao/alocacao.py`). **Nenhum teste
compara as duas.** O comentário declara um comportamento que o código não tem.

As perguntas: **qual das duas é a fonte**, e **qual teste as prende**.
- **(a)** A política é a fonte, e um teste reprova quando `[project].version` ≠
  `meta.versao`. É o que o comentário promete. O custo é subir dois arquivos a cada mudança
  de regra.
- **(b)** As versões são de coisas diferentes: o `pyproject` versiona o ambiente e as
  dependências, e a política versiona as regras. O comentário sai, e um teste reprova quando
  alguém escrever de novo que uma acompanha a outra.
- **(c)** O `pyproject` deixa de ter versão própria (`dynamic`), lida do `politica.yaml`.
  Exige ferramenta de build, e o projeto não é pacote (B-04).

---

## P-166 · Busca de anterioridade da marca MEOL e do domínio

**Dono:** sessão de pesquisa (nuvem), e Osvaldo · **Gatilho:** antes de desenhar
logotipo ou marca nominativa · **Classe:** `DECISAO_DE_DESENHO`

A busca pública do INPI por marcas iguais ou parecidas nas classes de serviço financeiro e
de software (quais classes, `NAO_CONFIRMADO`: a pesquisa confirma na fonte), mais a
disponibilidade de domínio. **Não é parecer:** viabilidade jurídica é da P-158. Colisão
encontrada vai para ele antes de qualquer desenho de marca.

---

## P-167 · Os critérios da WCAG 2.2 que a P-155 não leu, a começar pelo 3.3.4 (erro em operação financeira)

**Dono:** sessão de pesquisa (nuvem) · **Gatilho:** antes do protótipo F1, F3 e F6 da etapa 4
(`PLANO.md`, fila do rosto) · **Classe:** `DECISAO_DE_DESENHO`

A P-155 leu os 13 critérios candidatos e fechou em 27/09 com os RI-22 a RI-34. A leitura achou
critérios fora da lista que parecem tocar o MEOL, listados sem leitura no fim de
`docs/fontes/wcag-22-w3c.md`. O que mais pesa é o **3.3.4 Error Prevention (Legal, Financial,
Data)**, nível AA, que o alvo AA do MEOL inclui: é o critério de um produto que mexe com
dinheiro, e o "executei" da T1b (com desfazer antes de gravar) é o caso dele. Os outros doze
(1.1.1, 1.3.1, 1.3.2, 1.4.13, 2.1.1, 2.4.3, 2.4.6, 3.3.1, 3.3.2, 3.3.3, 4.1.2 e 4.1.3) estão na
mesma lista. O que fecha: cada um lido na fonte, virando RI com verificação ou declarado sem
aplicação com o motivo.

---

## P-168 · Ativos visuais próprios do MEOL (ilustração, ícone, imagem)

**Dono:** Osvaldo (decide) · Claude (desenha e testa) · **Gatilho:** a etapa 5 (brandbook) da
fila do rosto · **Classe:** `DECISAO_DE_DESENHO`

Resposta k-A dele (27/09/2026): **todo ativo visual do MEOL é produzido para o MEOL; nada de
banco de imagens.** O único ativo hoje é a ilustração da direção D, um cartão metálico
genérico desenhado em código (SVG, sem marca e sem texto), marcado `data-provisorio="P-168"`
em `docs/marca/direcoes/D.html` e guardado por `auditoria/test_direcoes_marca.py`. Ele é
**provisório**: existe só para o controle D do teste de marca não perder a "imagem de estilo
de vida" do pré-registro de 20/09. O que fecha: o conjunto de ativos do brandbook, feito para
o MEOL, com licença e origem de cada um.

---

## P-169 · A escada de contorno fora do Markdown: 21 linhas de YAML, 12 delas da S4

**Dono:** Claude (a guarda, na nuvem; o degrau 4 dos bancos, na sessão local) · Osvaldo só
se aparecer colisão com a cor da C · **Gatilho:** antes da etapa 5 (brandbook) da fila do
rosto; não bloqueia o teste de marca, cujos PNG estão congelados · **Classe:**
`DECISAO_DE_DESENHO`

`auditoria/escada_contorno.py` (regra 18 da §5-B) varre só `.md`, como a tarefa pediu. Em
27/09, uma varredura com janela de 3 linhas achou **21 linhas de YAML** com `NAO_CONFIRMADO`
perto de um motivo de acesso. As que pesam:

- **`docs/marca/tokens/direcoes.yaml`, a lista da regra m-B (S4, minha).** Dos 20 bancos e
  fintechs, **9 foram OBSERVADOS e 11 ficaram `NAO_CONFIRMADO`** (escada: só o degrau 1,
  um `curl` na página inicial): 9 por 403, a Caixa por um 302 sem destino lido, e o Bradesco
  por HTML sem cor. A regra "matiz a 30° de toda cor dominante observada" foi
  conferida contra **n=9**, não contra o mercado. A S4 escreveu isso com honestidade
  ("não se completou de memória"), mas não subiu os degraus 2 a 4: CSS e manifest do próprio
  site, Wayback, manual de marca publicado e sessão local.
- **`alocacao/custos.yaml` e `alocacao/catalogo.yaml`, BOVV11** ("site do gestor bloqueia
  acesso automatizado"). A escada está no `MAPA-CONSTANTES.md` e na P-05; o texto do YAML
  segue antigo e muda junto com o valor, pelo protocolo de mudança.

O que fecha: (1) a guarda passa a ler YAML por campo (`status: NAO_CONFIRMADO` com `metodo`
ou `motivo` de acesso exige `escada`), com a própria linha de base; (2) os 11 bancos sobem a
escada, e a cor observada de cada um entra na lista; se algum ficar a menos de 30° do magenta
da C (318°), a decisão volta para ele antes do brandbook.

---

## P-173 · CX-02 · `pais_varridos()` não separa motor de teste, e 18 chaves ficam escondidas

**Dono:** Claude Code · **Gatilho:** a próxima sessão que tocar `auditoria/chaves_orfas.py`, ou
antes de o `exibidos` ganhar mais um leitor por `getattr` · **Classe:** `DECISAO_DE_DESENHO`

Achado externo (auditoria do Codex, 03/10/2026, conferida pelo Claude do Projeto). **Medido em
03/10:** 49 candidatos a chave órfã hoje; **67** contando só os pais lidos pelo motor. Das 18
escondidas: **15** são leitura legítima, por `getattr`, da lista `exibidos`
(`corretoras.py:398`); **1** é a P-32, já vigiada em `DIVIDA_DE_COBERTURA`; **2**
(`custos.yaml` `etf.IMAB11.composicao.{administracao,gestao}`) estão escondidas por colisão de
nome com `memoria["composicao"]` em `test_alocacao.py:2042` — um teste a ler uma chave faz o
instrumento achar que o motor a lê (5-B.2: o filtro incluiu o que não devia).

**Conserto, em duas partes e nesta ordem:** (a) ler `exibidos` como aresta de YAML, para as 15
deixarem de depender de acidente; (b) excluir arquivos de teste de `pais_varridos()`. Fazer (b)
antes de (a) faria as 15 virarem falso-órfão.

---

## P-174 · CX-03 · `conftest.py:146` trata `atual is None` como "não mudou"

**Dono:** Claude Code · **Gatilho:** a próxima sessão que tocar `alocacao/conftest.py` ·
**Classe:** `DECISAO_DE_DESENHO` · **Prioridade:** baixa

Achado externo (mesma auditoria do Codex). Um teste que faz `C = None` ou `del C` num módulo
vigiado escapa da acusação e da restauração, porque `None` é lido como "sem mudança".
**Conserto:** sentinela de ausência (`_AUSENTE = object()`) no lugar de `None`, com um teste de
mutação que faz `C = None` e `del C` e exige a acusação nos dois.

---

## P-175 · "Não grava" exige prova: teste com valores-sentinela no servidor sem estado

**Dono:** Claude Code · **Gatilho:** antes do primeiro endpoint do motor (etapa 4) · **Classe:**
`DECISAO_DE_DESENHO`

Consequência (b) da decisão da P-165 ([`docs/decisoes/P-165-onde-o-motor-roda.md`](decisoes/P-165-onde-o-motor-roda.md)):
o servidor é sem estado e "nada é gravado, nem em log" é promessa até alguém provar. O teste
manda requisições com valores-sentinela (patrimônio, posições, aporte) e reprova se qualquer
um aparecer em log, mensagem de erro ou métrica — **incluindo o log padrão da plataforma de
hospedagem** (acesso, proxy, tracing), que o código da aplicação não controla. A escolha da
plataforma tem de passar por esse teste antes de valer. A LGPD (consequência (a)) é da P-158,
e a minimização dos campos em trânsito (consequência (c)): a da saída foi decidida em 03/10;
a da entrada é a P-178.

---

## P-182 · `motor_aporte` calcula rota em lote a R$ 1,00 quando falta o preço

**Dono:** Claude (decisão técnica) · **Gatilho:** antes de qualquer porta além da
`aporte_do_mes.py` chamar o motor (protótipo F1, servidor da B′) · **Classe:**
`DECISAO_DE_DESENHO`

Visto ao escrever a porta de uso (P-181, 10/10/2026). `motor_aporte()` e `_primeiro_aporte()` usam
`precos.get(rota, 1.0)`: sem preço, uma rota com `negocia_em_lote` vira lote de R$ 1,00, e a
ordem sai com quantidade e preço errados e aparência perfeita (a classe do F-02: ausência
virando número). A `aporte_do_mes.py` se protege vigiando quais preços o motor consultou
(`PrecosVigiados`) e recusando a saída; o `demo_aporte.py` e os testes passam preço ou aceitam o
1,0 de propósito. **Fecha com:** o motor devolver um status `FALTA_PRECO` com as rotas, no lugar
do 1,0, e um teste que falha na versão de hoje; a vigilância da porta vira conferência redundante.

## P-178 · Contrato de ENTRADA do motor: quais campos do Estado viajam do aparelho

**Dono:** sessão de especificação, com aprovação do Osvaldo · **Gatilho:** antes do primeiro
endpoint do motor, junto da P-175 · **Classe:** `DECISAO_DE_DESENHO`

A F0 cobre só a **saída**. Na B′ ([P-165](decisoes/P-165-onde-o-motor-roda.md)) o que viaja
do aparelho para o servidor é o `Estado` (`alocacao/alocacao.py:150`): `despesa_mensal`,
`reserva_atual`, `reserva_por_rota`, `aporte_mensal`, `estabilidade_renda`, `dependentes`,
`dividas`, `objetivos`, `posicoes`, `caixa`, `match_empregador`.

**Objetivo:** minimizar os campos em trânsito (consequência (c) da P-165). A saída já foi
decidida em 03/10 (`reserva.atual` e `alocacao.atual[]` não são devolvidos na resposta; o motor pode precisar recebê-los); falta dizer, campo a
campo, qual desses onze o motor precisa receber para decidir e qual a tela pode guardar. Como a
saída calcula `falta` da reserva e `peso_atual`, vale conferir o que o motor realmente lê antes
de cortar (`python impacto.py` sobre cada campo). **Fecha com:** um documento no formato da F0,
campo a campo, aprovado por ele, e a P-175 apontando para ele.

---

## P-176 · K5 e completude saíram 1, 2, 3, 4 e 5 por ano na corrida de 2016–2020

**Dono:** Claude Code (sessão local: lê o acervo) · **Gatilho:** antes de qualquer número do
K5 ou da completude ser citado como medida, e antes de o `c02_corrida.py` rodar de novo ·
**Classe:** `DECISAO_DE_DESENHO`

No JSON de `b331172`, o `K5.n` e o `completude.grandes_quantidade` saíram exatamente **1, 2, 3,
4 e 5** em 2016 a 2020 (soma 15, o `K5_janela.n`). **Hipótese: defeito de contagem.** Ainda não
é achado, porque nada foi medido além do JSON.

O que a leitura do código já diz: as duas contagens são independentes. A do K5 é a
`k5_por_ano`, sobre as linhas medidas; a da completude é a `completude_por_ano`, sobre os
`degraus`. As duas só têm em comum o `grande()` e a população que o `ajustar.medir` devolve.
Coincidirem é coerente com `sem_mercado = 0`. A escada, então, sai do contador e vai para o
que alimenta os dois.

**Primeiro passo:** listar os 15 eventos (ticker, data ex, tipos, fator) e conferir contra o
silver. Isso lê só o que a corrida já leu, e a quarentena acabou com o resultado.

**Se for defeito:** o conserto é **emenda declarada como posterior ao resultado**, com um teste
que falha antes. O veredito da janela **não muda**: ele vem do K2 e do K3 (§7 do pré-registro).
Se não for, a coincidência fica registrada com a lista na §7.

---

## P-177 · `c02_corrida.py` não recusa insumo com sha256 diferente da §2

**Dono:** Claude Code (nuvem ou local) · **Gatilho:** antes de qualquer nova corrida do
`c02_corrida.py`, ou de um script derivado dele para um critério v3 · **Classe:**
`DECISAO_DE_DESENHO`

A §2 do pré-registro diz: *"A corrida recusa qualquer insumo cujo sha256 difira destes."* O
código não faz isso. `insumos()` (`auditoria/c02_corrida.py:587`) **calcula e grava** o sha256,
e `main()` não o compara com nada. É o padrão F-05: o texto declara um comportamento que o
código não tem. A corrida de 03/10 bateu nos sha256 porque **a sessão conferiu à mão antes**
(commit `b331172`), não porque o script recusaria. O resultado vale; a guarda não existia.

**Conserto:**
- os sha256 da §2 como dado (silver e os cinco ZIPs, ou as impressões de conteúdo da P-139);
- `main()` sai com código próprio **antes de ler preço** quando um deles diferir;
- um teste que falha na versão de hoje: um silver sintético com um byte trocado tem de ser
  recusado.

O `auditoria/test_c02_janela_2016_2020.py` já faz a conferência do lado do teste. Ele não
substitui a do script.

**Junto: o JSON do resultado e o fim de linha.** O `.gitattributes` **já tem** `*.json text
eol=lf` desde o F-04. Conferido em 03/10: a cópia de trabalho no Windows tem o mesmo sha256 do
blob (`73e43fba…87defd`). O que falta é **declarar o sha256 do blob como o canônico**: no
cabeçalho do `.gitattributes` e na §2. Assim, quem citar o resultado cita o byte do
repositório, e não o da sua cópia.
