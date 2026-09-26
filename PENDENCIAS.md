# Pendências

Registro único e vivo **do que está aberto**. Atualizado a cada sessão, **antes** de encerrar.
Cada pendência tem **dono**, **gatilho** e **classe** (`CLAUDE.md` §5-A.1); sem os três é
desabafo.

- **Fechou?** Risca o número no cabeçalho (`## ~~P-NN~~ · … — **FECHADA em DD/MM/AAAA**`),
  escreve a evidência, e **move o bloco** para `docs/historico/pendencias-fechadas.md`, com a
  linha na tabela `## Fechadas` de lá — no mesmo commit.
- **Antes de abrir uma pendência nova**, procure lá: é a tabela que impede reabrir tarefa
  pronta.
- **As decisões que esperam o Osvaldo**, prontas para responder pelo celular:
  `docs/decisoes/fila-do-osvaldo.md`.

---

## P-44 · O próximo passo não pode ser de engenharia duas vezes seguidas

**Regra de processo, criada em 06/09 depois de medir o próprio ritmo.** Sete rodadas
seguidas de qualidade de engenharia, zero de propósito — e **eu propus todas**, uma no
fim de cada resposta.

É o M-01 aplicado a nós: trocar o destino do aporte move 3 meses, trocar o valor move
33, e o sistema trabalhava na alavanca de 3. **A alavanca da engenharia move 0.**
Nenhum teste aproxima a reserva de existir.

Se a sessão anterior fechou uma pendência de engenharia, a próxima proposta é de
**produto, dado, ou uma pergunta a você**. Engenharia entra quando **destrava** algo.

---

## P-46 · Usar subagentes na leitura de fonte primária

Ler os 32 arquivos de `docs/fontes` custou o texto **inteiro** de cada um dentro do
contexto. Um subagente lê e devolve só a conclusão.

Para a Fase 0 deixa de ser detalhe: os layouts da CVM e do COTAHIST têm centenas de
páginas. **Um subagente por documento** é a diferença entre caber e não caber.

**Gatilho:** a primeira sessão da Fase 0.

---

## P-05 · Quatro `NAO_CONFIRMADO` esperando download

| chave | bloqueia | o que fecha |
|---|---|---|
| `etf.BOVV11` | `tabela_etf_rv_completa` | site do gestor bloqueia robô — visita manual |
| ~~`etf.IMAB11`~~ | **fechada 05/09** — 0,25% a.a. (página do gestor, PARCIAL). Falta o regulamento para virar COMPLETO |
| `etf.ACWI11` | `comparacao_global_amplo` | regulamento / página do produto |
| `exterior.vest_stablecoin.iof` | `ordenacao_rotas_exterior` | tratamento de IOF em stablecoin |

O `IMAB11` é o mais valioso: é o único concorrente conhecido do Tesouro IPCA+ na
função `PROTECAO_REAL` que não paga a custódia de 0,20% a.a. da B3.

---

## P-08 · Constantes vencendo — macro renovadas em 05/09

`cdi_aa` e `selic_aa` reconferidos na API do BCB: **13,90%** (SGS 4389, 03/09) e meta
**14,00%** (SGS 432). **Os dois valores estavam certos** — era prazo vencido, não número
errado. Novo `expira`: 04/12/2026. Falta `poupanca_am`, que vence em 28/09.

| constante | `expira` |
|---|---|
| `macro.cdi_aa` | **04/09/2026 — já venceu** |
| `macro.selic_aa` | 07/09/2026 |
| `macro.poupanca_am` | 28/09/2026 |
| tarifas B3 e Tesouro (9) | 04/12/2026 |
| tabelas comerciais (11) | 04/12/2026 |
| taxas de fundo (19) | 05/09/2027 |

`motor.val()` avisa em stderr quando passa da data. Leis usam `expira: null` +
`revisar_se`, porque lei não vence no aniversário.

---

## P-09 · Fase 0 virou o único caminho — **prioridade máxima**

Depois de H1/H3 (05/09), os três testes pré-registrados terminam no mesmo lugar:

- **H1 (valor)** — o alfa medido é de um long-short cuja perna vendida não existe
  para pessoa física. O NEFIN publica só o spread, nunca as pernas. Medir a carteira
  investível exige montar os tercis a partir do dado de ação.
- **H2 (dividendo)** — não há fator de DY na série. A carteira precisa ser montada.
- **H3 (tamanho)** — fechada, e fechada sem precisar da Fase 0.

Dois de três terminam nela. Somado ao prazo que já existia (a CVM sobrescreve os
arquivos anuais e `dt_disponivel` não se reconstrói), a Fase 0 deixou de ser "a maior
peça restante" e passou a ser **a única que destrava alguma coisa**.

**Gatilho:** próxima sessão no desktop.

---

## P-10 · `alfa_contra_fatores()` tem uma armadilha viva

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

121 chaves. Nenhum módulo do motor as referencia; quem lê são os testes e o
`backtest_h1_h3.py`. É defensável — o pré-registro descreve o que **será testado**, não
o que o alocador faz hoje. Mas até que o backtest completo exista, é uma especificação,
e especificação sem número some.

---

## P-30 · `bloco_C_solvencia` — especificado em 05/09, nenhum módulo aplica

48 chaves escritas na mesma sessão em que a régua de solvência foi desenhada. Só
`test_alocacao.py` as menciona: os testes verificam que o **texto** existe, não que
algum comportamento derive dele. A régua de banco (P-16) depende dela.

---

## P-31 · `regime_instituicao_financeira` — mesma situação, 46 chaves

Nasceu da sua correção sobre bancos: *"não faz o menor sentido excluir Itaú e Bradesco
— não deve ser excluído, deve ser encontrado o critério"*. O critério foi **escrito**.
Ele ainda não **roda**.

---

## P-32 · O que sobrou de prosa na seção `corretora`

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

`exige_selecao`, `n_ativos_efetivo`, `bloqueado_por`, `meses_para_montar`. O
`bloqueado_por: A05_nucleo_indexado_vs_selecao_ativa` é o mais grave: ele afirma que a
sleeve de seleção ativa está **travada por uma decisão em aberto**, e nada a trava.

---

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

Com teto por produto, "quanto há de reserva" deixou de bastar: para saber se a próxima
parcela cabe é preciso saber **onde** ela está. `Estado.reserva_por_rota` foi criado e é
**opcional**. Quando ausente, o G2 avisa que não sabe em vez de supor que a reserva foi
construída na ordem do plano.

**Hoje não morde** — a reserva é zero e o `estado.yaml` declara `reserva_por_rota: {}`,
que *afirma* que não há reserva em lugar nenhum, diferente de omitir a chave. Morde a
partir do primeiro depósito, e o viés aponta para **recomendar demais** a rota melhor.

---

## P-22 · Opções: duas famílias, não uma

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

---

## P-19 · Imóvel direto foi excluído por argumento geral, sem medição

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

---

## P-17 · C-04 e C-05 não foram lidos — ⚙ **exige o desktop**

O regime do bloco C está escrito, mas a lista de campos vive em
`docs/auditoria/escopo-campos-de-analise.md`, na sua máquina, e a ponte estava fora do ar.
C-01 a C-03 são conhecidos por referência cruzada dentro do próprio `politica.yaml`;
**C-04 e C-05 são citados como existentes e nunca nomeados ali.**

Não inventei os dois. Um bloco de exclusão com critério inventado excluiria empresa
por regra que ninguém escolheu — pior que bloco nenhum.

**Gatilho:** primeira sessão de desktop. Ler o arquivo e reconciliar.

---

## P-18 · `SETOR_ATIV` da CVM não foi contado

O bloco C recusa instituição financeira, e a identificação sai do campo `SETOR_ATIV`
do cadastro da CVM. O campo foi conferido, mas **só dois valores foram vistos** — a
enumeração nunca foi contada no dado real, como foi feito com `ORDEM_EXERC` e
`ESCALA_MOEDA`. Sem isso o corte automático não pode ser codificado.

**Gatilho:** antes de codificar a recusa. ⚙ exige o desktop.

---

## P-41 · Carregamento de YAML domina o custo multiusuário

`carregar_politica()` custa **82 ms** e `carregar()` **42 ms**, contra 2,75 ms do motor.
Para um usuário é irrelevante. Para N usuários × M chamadas, 124 ms de parse por chamada
domina tudo.

**Deliberadamente não feito.** Otimizar agora seria para um cenário que não existe — e o
S-02 é a prova de que cache mal dimensionado custa correção, não só tempo.
**Gatilho:** o segundo usuário.

---

## P-42 · O catálogo é quadrático em número de rotas

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

## P-51 · `ORDEM_EXERC = PENÚLTIMO` contamina o backtest

**Classe:** `BLOQUEIA_O_SISTEMA`. **Dono:** Claude. **Gatilho:** ao escrever o parser da CVM.

O projeto contou as duas enumerações em 12,8 milhões de linhas e registrou as duas como
válidas. Elas são — mas **`PENÚLTIMO` é o ano anterior já reapresentado**. Usar a linha
`PENÚLTIMO` do arquivo de 2025 para saber o que se sabia em 2024 é look-ahead puro: é
justamente o número corrigido depois.

Regra que sai daqui: o parser usa **só `ÚLTIMO`, do arquivo daquele ano**. E a partição é
o **ano do arquivo**, não o ano do dado — o DFP de 2025 corrige 2023.

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

## P-53 · O acervo não pode depender de engine nenhum

**Classe:** `DECISAO_DE_DESENHO`. **Dono:** Claude. **Gatilho:** ao criar `data/bronze/`.

Recomendação da pesquisa: **Parquet imutável particionado por `dt_captura` como acervo, e
DuckDB como motor de consulta** — com o `.duckdb` sendo artefato reconstruível, nunca o
arquivo de registro. Segundo lugar: DuckLake (1.0 em abr/2026), com `AT (TIMESTAMP => …)`
nativo; perdeu por acoplar um acervo de década a um formato recente.

A consulta as-of e as sete armadilhas estão em
`docs/fontes/pesquisa-bases-e-apis-2026-09.md` §3. Duas que este projeto não sabia que
tinha, além da P-51: **`dt_captura` não é data de conhecimento do mercado** e **o
mapeamento ticker↔CNPJ↔CD_CVM também precisa ser bitemporal**, senão o join vaza futuro.

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

## P-58 a P-61 · Regimes de leitura de balanço — a pergunta que expôs o defeito

**Documento:** `docs/auditoria/regimes-de-leitura-de-balanco.md`. **Classe:** todas
`BLOQUEIA_O_SISTEMA`. **Gatilho:** depois da P-18 (contar `SETOR_ATIV`), que bloqueia as
quatro.

**Pergunta do Osvaldo, 06/09/2026:** como o sistema lida com empresa que lucrou menos por
reinvestir, com dívida feita para capex, e com setores que funcionam com dívida alta —
construção civil, porque se realiza imóvel com financiamento.

**Resposta honesta: não estava desenhado.** E a pergunta expôs um defeito do projeto, não
uma lacuna de escopo.

O `bloco_C_solvencia` já escreve que dívida líquida/EBITDA aplicado a um banco *"devolve
um número, e esse é o perigo: métrica que não se aplica mas não falha é o modo de falha do
F-02"*. **O projeto reconheceu esse modo de falha para banco e não o generalizou.** Existe
um regime para instituição financeira e **um único regime para "todo o resto"** — que lê
uma incorporadora e uma WEG com a mesma régua.

| | |
|---|---|
| **P-58** | o portão de regime tem 2 saídas e precisa de N. Candidatos: incorporação, utilities/concessões, propriedades para renda, arrendamento pesado (IFRS 16) |
| **P-59** | **C-01 (cobertura de juros) exclui empresa em fase de investimento** — EBIT deprimido por depreciação nova E despesa financeira alta pela dívida do capex: as duas pontas pioram pelo mesmo motivo, que pode ser saudável. E cai no portão de **exclusão**, o pior lugar |
| **P-60** | **ROIC vs custo da dívida** não existe no sistema, e é o único critério que separa dívida que cria valor de dívida que destrói |
| **P-61** | capex de **manutenção** vs **expansão**: a CVM não separa, e a heurística "manutenção ≈ depreciação" é conhecidamente errada em empresa que cresce. **Limitação declarada**, com direção de viés: **o sistema subestima quem investe para crescer** |

**A correção que a pergunta dele também recebeu:** capex **não passa pela DRE**. O que
derruba o lucro são três causas distintas — depreciação do capex passado, juros da dívida
do capex, e opex não capitalizado — e elas têm leitura **oposta**. Consequência de
desenho: **a porta de entrada é a DFC, não a DRE.**

**P6 aplicada:** construção civil **não sai do universo**. A saída fácil seria excluir por
falta de régua, e foi exatamente essa a correção que criou a P6 — no caso do banco. Se eu
excluir agora, é a quarta vez.

**O que só ele responde** (§6 do documento): dívida SFH vs corporativa, receita a
apropriar, permuta, distratos, e qual número um planejador olha primeiro. Ele é engenheiro
civil e analista de planejamento; isso é procedência melhor que artigo, **desde que
registrada como decisão dele**.

---

## P-63 · O híbrido nível/tendência é regra geral ou regra do bloco C?

**Classe:** `DECISAO_DE_DESENHO`. **Dono:** Osvaldo. **Gatilho:** ao implementar qualquer
métrica com leitura temporal.

Em 05/09 ficou decidido, para solvência: **HÍBRIDO — o nível corta, a tendência marca sem
poder de veto.**

Em 06/09, sobre distratos, ele disse o contrário: `5% → 7% → 11% → 16%` preocupa **muito
mais** que `12% → 11% → 10% → 9%`, mesmo com o segundo em nível mais alto. **A tendência
domina.**

Os dois podem estar certos — mas então **o híbrido não é regra geral, é regra do bloco C**,
e isso precisa ser dito. Duas saídas, ambas defensáveis:

- **(a)** o híbrido é *por métrica*, e distrato é uma métrica cuja informação mora na
  direção;
- **(b)** o híbrido é geral, e o que muda é o que conta como "nível" — para distrato, o
  nível seria a **média móvel**, não o ponto.

Decidir por omissão aqui seria deixar o código escolher, que é exatamente o que a P2 proíbe.

> **Decisão dele, 26/09/2026: `63a`** (recomendada) — nível, tendência ou híbrido é declarado **por métrica** no YAML. Registro em `docs/decisoes/fila-do-osvaldo.md`.


---

## P-64 · Portão × dossiê — uma camada de desenho que o projeto não tem

**Classe:** `BLOQUEIA_O_SISTEMA`. **Dono:** Claude. **Gatilho:** antes de implementar
qualquer regime.

Ele respondeu como analista lendo **uma** empresa. O sistema precisa varrer **centenas**.
Uma sequência manual de dez passos não é portão.

| | o que é | quando roda | fonte |
|---|---|---|---|
| **portão** | automático, todo o universo | sempre | dado estruturado |
| **dossiê** | leitura manual guiada, empresa a empresa | só na lista curta | notas, release, IPE |

Para incorporação **o portão não pode ser o regime** — o dado não existe (X-01). O portão só
pode dizer: *"esta empresa é do regime INCORPORACAO, exige dossiê, e até ter um permanece no
universo sem peso atribuído por este bloco."*

Coerente com P6 (nada sai), P1 (nada é inventado) e A05 (o sistema não nomeia empresa). E
transforma o painel de cinco camadas dele **no roteiro do dossiê** — que é o que ele é.

**Vale para todo regime, não só incorporação.**

---

## P-65 · Extração de nota explicativa e de IPE — a segunda esteira, nunca orçada

**Classe:** `BLOQUEIA_O_SISTEMA`. **Dono:** Claude. **Gatilho:** depois da Fase 0 rodar.

**Achado X-01.** Dos dez passos da sequência dele, **3 são obtíveis** no dado estruturado
(FCO, margem bruta, caixa) e **7 não são**. E os 3 obtíveis são os que ele não colocaria em
primeiro lugar.

O caminho existe: a página do conjunto DFP publica *"os endereços para download dos
Formulários DFP entregues"* (documento completo do Empresas.NET), e o **IPE** carrega
releases de resultados. Mas é **extração de documento**, não leitura de CSV — ordem de
grandeza diferente do que o projeto orçou.

**A investigar antes de prometer:** formato dos formulários do Empresas.NET; se as notas
vêm em XML estruturado ou em texto livre; volume do IPE; e se existe alguma padronização
que torne a extração determinística em vez de heurística. **Se for heurística, ela produz
número sem procedência — e aí a P1 manda não fazer.**

> **Decisão dele, 26/09/2026: `65b`** (**diverge da recomendada (65a)**) — a segunda esteira entra **já como construção**, com a condição dele: só extração **determinística** — todo número carrega o trecho, a posição e o sha256 do arquivo de origem, e número sem trecho é recusado (P1). Começa medindo o formato. Registro em `docs/decisoes/fila-do-osvaldo.md`.


---

## P-66 · Os cortes de distrato entram no YAML como decisão declarada

**Classe:** `DECISAO_DE_DESENHO`. **Dono:** Claude (implementar). **Gatilho:** junto da P-64.

10% / 15% / 20% são os cortes dele. **Ele mesmo escreveu que "não existe percentual
universal"**, então são `DECISAO_DO_USUARIO`, **não** `CRITERIO_MEDIDO` — exatamente como o
bloco C já declara que "dívida líquida/EBITDA abaixo de 3 é costume de mercado, não norma".

Vão para o YAML com o **custo de discordar medido**: quantas empresas mudam de lado se o
corte for 10 em vez de 15.

---

## P-67 · Falta o teste que impede `estado.yaml` de ir para um repositório público

**Classe:** `BLOQUEIA_O_SISTEMA`. **Dono:** Claude. **Gatilho:** **antes** do primeiro
`git add`.

A decisão P-62 depende de uma linha de `.gitignore`, e uma linha de `.gitignore` é
exatamente o tipo de coisa que se perde numa refatoração sem ninguém notar. **Isso é o
padrão que o projeto inteiro existe para combater:** um arquivo declara um comportamento e
nada testa se ele acontece.

O teste: falha se `estado.yaml` estiver rastreado pelo git, ou se qualquer arquivo com o
padrão de estado real entrar no índice. Barato, e é a diferença entre uma decisão e uma
esperança.

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

## P-82 · O repositório guardou uma cópia de si mesmo, e a suíte continuou verde

**Classe:** `BLOQUEIA_O_SISTEMA`. **FECHADA em 16/09/2026**, no mesmo dia em que abriu —
mas ela tem seis minutos de vida que valem mais que o conserto.

Ao fechar as seis falhas herdadas, o `git rm` apagou os cinco `*-patch.py` e a guarda
duplicada. Fez o certo. O `git add -A` seguinte encontrou na raiz a pasta
`pacote_segunda/pacote_segunda/` — o zip de 14/09 descompactado ali por engano — e a
levou junto. O git então viu os mesmos bytes saindo de um lugar e aparecendo em outro, e
registrou **rename**: os arquivos não foram removidos, **foram mudados de lugar para
dentro da cópia**.

O commit `bebea75` passou a carregar uma cópia congelada do projeto de 14/09: um segundo
`CLAUDE.md`, um segundo `chaves_orfas.py`, um segundo `refinar.py`, um segundo
`test_chaves_orfas.py`. **E a suíte ficou verde**, porque nenhum portão olha para lá —
`testpaths = ["alocacao"]`, `campos_mortos.py` varre `alocacao/`, o `ruff` do P-40 roda
com `cwd=alocacao/`. **A P-80 cobrou a primeira conta em menos de uma hora.**

### O que é caro aqui não é o erro, é que a regra já estava escrita

O `.gitignore` ignora `Claude outputs/` com o motivo por extenso: *"ela contém uma CÓPIA
INTEIRA do projeto... não é só tamanho: é a armadilha do `docs/historico/pesquisa-custos-2026-08/calc/`
outra vez, e pior."* A armadilha tinha **nome**, tinha **precedente citado**, e tinha
**remédio** — e o remédio era uma **lista de nomes de pasta que alguém precisa lembrar de
estender**. `pacote_segunda/` não estava na lista. É a P7 na forma mais limpa que o
projeto já produziu: *rotina que depende de lembrar não é rotina*.

`alocacao/test_p82_copia_do_projeto.py` mede o **índice do git**, não o disco — como o
`test_p67_segredo.py` faz com o `estado.yaml`. Descompactar um zip na pasta é inofensivo;
o defeito nasce no `git add`. Duas regras: módulo com o mesmo nome de um módulo dos três
pacotes, e **pasta de pacote aninhada** — a segunda existe porque a primeira não pegaria
`pacote_segunda/pacote_segunda/alocacao/E02-patch.py`, cujo nome não colide com nada.

### O que fica aberto dentro dela

`docs/historico/pesquisa-custos-2026-08/calc/` tem `motor.py`, `test_motor.py` e `custos.yaml` — os
mesmos nomes do projeto vivo, congelados em 28/08. Entrou em `COPIAS_DECLARADAS` com o
motivo escrito, que é o terceiro caminho honesto do protocolo das órfãs. **Mas declarar
não é resolver:** quem abrir `calc/motor.py` continua lendo uma versão de três semanas
atrás sem nada no arquivo avisar. Mover para `docs/historico/` ou renomear os arquivos
resolveria de vez — e isso é decisão sua.

---

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


## P-98 · 507 MB entraram em `docs/fontes/` sem casar com nenhum padrão do `.gitignore`

**Dono:** próxima sessão (feito: guarda escrita) · **Gatilho:** **antes do próximo
`git add`** · **Classe:** `BLOQUEIA_O_SISTEMA` · ⚙ **exige o desktop**

O acervo COTAHIST (6,0 GB) foi baixado para `docs\fontes\series-historicas-cotahist\`
— **dentro do repositório, que é público.** O `.gitignore` cobria
`docs/fontes/**/*.zip` e `**/*.txt`, e por isso 65 dos 81 arquivos estavam cobertos.

**Os 16 de 1986–2001 não.** O ZIP da B3 muda de convenção no meio da série e esses anos
saem **sem extensão** (`COTAHIST.A1986`, `COTAHIST_A2001`). São **507 MB** que padrão
nenhum pegava, a um `git add -A` de virar histórico permanente — blob commitado não se
apaga com `git rm`, só com reescrita de histórico, e depois de um push nem isso.

**É a P-82 pela segunda vez em dois dias:** *regra escrita numa lista de nomes não é
regra, é lembrete.* Lá era uma lista de **pastas**; aqui é uma lista de **extensões**,
e estendê-la exigiria saber de antemão como um publicador nomeia o conteúdo de um ZIP
de 1986. Ninguém sabe.

**Fechado nesta sessão, nos dois níveis:** `.gitignore` ganhou a pasta, e
`alocacao/test_p98_acervo_fora_do_indice.py` mede **tamanho no índice do git** — bytes
não dependem de alguém ter acertado o nome. 5 testes, com prova por mutação usando os
números reais do incidente. **Falta rodar `git status` antes do próximo commit** para
confirmar que nada já entrou.

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

## P-103 · O `CLAUDE.md` afirmava tokens sem conta, e um plano externo calibrou nele

**Dono:** próxima sessão · **Gatilho:** nenhum — fechada no que dava para fechar ·
**Classe:** `DECISAO_DE_DESENHO` · *(retratação na §11.4; laudo em
`docs/auditoria/AUDITORIA-PLANO-DE-TOKENS.md`)*

A §11.4 declarava a leitura de sessão em **"~26 mil"** antes do corte de 06/09 e
**"~13 mil"** depois. Medido em 19/09 com `tiktoken`: a razão real deste repositório é
**19,0 tokens/linha**, logo os valores são **~38.400** e **~19.900** — erros de **+48%** e
**+53%**, os dois na direção que faz o projeto parecer mais enxuto.

**O custo não foi interno.** Três planos de otimização de tokens foram escritos em 19/09, e
um deles declarou ter **calibrado a própria razão empírica** nos "~13 mil" da §11.4. Ele
errou a leitura inicial por **90%** — e a conta dele estava certa; a fonte é que não
estava. **Número plausível em prosa, citado por terceiro como fonte: C-01 na camada do
token.**

**Fechado no processo, não na tabela:** `auditoria/tamanho_do_contexto.py` + 8 testes, com
prova por mutação. A §11.4 não afirma mais valor — aponta para o comando.

**O que a medição abriu e continua aberto:**

| # | o que | classe |
|---|---|---|
| 1 | ~~O cache não foi medido~~ **FECHADO em 19/09 na fonte oficial, e ele me derrubou.** O write é **2,0x** e o read 0,1x; como o fator incide sobre todo o prefixo, **cortar X% corta X% do custo, com cache ou sem** — medido, **−25%**. A inversão de prioridade que eu anunciei não existe. O risco do split é a **janela de 20 blocos**, não o prefixo. `docs/auditoria/CACHE-E-O-CORTE.md` | — |
| 2 | **O variável não tem instrumento.** Resposta, saída de ferramenta e arquivo reescrito são o que custa integral em todo turno, e eu não os meço | `DECISAO_DE_DESENHO` |
| 3 | **A §11.5 está `NAO_CONFIRMADO`** — ordenação sem número, e o título dizia "medido" | — |
| 4 | **`## Fechadas` = 7.457 tokens** (7,7% da leitura). Mover para `FECHADAS.md` é o único item de tamanho com número verificado | `DECISAO_DE_DESENHO` |
| 5 | ~~49% do `CLAUDE.md` são blocos `>`~~ **DECISÃO C EXECUTADA em 19/09.** Critério dele: *otimização sem perder contexto* → triagem por **função**, não por percentual. Saíram 962 linhas e **20.085 tokens** (os 30 achados de 06/09–18/09); ficou um **índice** com a regra de cada um. **−17.816 tok, −33,7% do arquivo**, e **26/26 achados com endereço, medido** | — |
| 6 | **P-45, P-46 e P-53 têm gatilho vencido há 13 dias** (push, Fase 0, `data/bronze/`). Os três "pilares" de um dos planos são essas três pendências. **O problema não é falta de plano: é que nada dispara o gatilho** — P7 | `BLOQUEIA_O_SISTEMA` |

> **O achado de método, e vale para além de token:** a regra do C-01 (*"achado só entra com
> a conta escrita"*) é de 12/09; a §11.4 é de 06/09. **Regra nova não audita o passado
> sozinha.** Nenhum instrumento do projeto varre prosa antiga procurando número sem
> procedência — e a §11.4 sobreviveu treze dias por isso, com a regra que a condenava
> escrita dezoito parágrafos acima.

> **26/09/2026 — o item 4 foi executado, e mais que ele.** As fechadas saíram para
> `docs/historico/pendencias-fechadas.md`, e a história do `CLAUDE.md` para
> `docs/historico/claude-md-ate-2026-09.md`. Leitura de sessão: **136.443 → 48.135 tokens
> (−64,7%)**, medido pelo `tamanho_do_contexto.py` antes e depois
> (`docs/metricas/contexto-de-sessao.md`); 368 códigos de 368 continuam no repositório
> (`auditoria/codigos_preservados.py`). Segue aberto o item 2.

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

## P-115 · O critério do degrau precisa ser re-pré-registrado antes da próxima janela

**Dono:** Osvaldo decide · **Gatilho:** antes de medir qualquer janela nova (2016–2020, ou o
acervo inteiro) · **Classe:** `DECISAO_DE_DESENHO`

O critério do C-02 reprovou em 4 de 5 anos (`docs/auditoria/C02-JANELA-2021-2025.md`) e o nulo
estava errado: o dia ex ajustado tem o retorno do mercado, e o dividendo tira do preço 1,16×
o que paga. O critério corrigido — dias **limpos**, **descontado o mercado** do dia, razão
queda/provento **por tipo** — foi desenhado **depois** de ver 2021–2025, então só vale como
pré-registro para dado que ainda não foi medido.

**E só vale se for commitado e empurrado ANTES de rodar sobre 2016–2020.** Commit local não
basta: o que torna o "antes" verificável (P4) é o histórico **público** datado — o verificador
externo do laudo `docs/auditoria/PREREGISTRO-EVIDENCIA.md`. Sem o push anterior à corrida, o
critério corrigido repete o defeito da P-116.

> **Decisão dele, 26/09/2026: `115a`** (recomendada) — empurrar o critério corrigido do degrau como pré-registro antes de medir 2016–2020. O Claude Code redige; ele responde "pode empurrar" antes de qualquer medição. Registro em `docs/decisoes/fila-do-osvaldo.md`.

> **26/09/2026, revisão 4 (no rascunho do PR #27, §9):** "pode empurrar" dado, com merge
> condicionado. **Antes do merge, a janela é escolhida pelo n de JCPs, sem ler preço.** As
> candidatas são 2016–2020, 2015–2020, 2014–2020 e 2013–2020. Vale a menor com
> **n_JCP ≥ 1.648**; se nenhuma atender, fica 2016–2020 com o `NAO_CONFIRMADO` provável
> declarado. Quem conta é o `auditoria/c02_contar_n.py` (só no branch do #27 até o merge),
> que lê do silver só `cod`, `type_stock`, `tipo` e as duas datas. **A ordem da sessão local:**
> 1. silver com calendário desde **2013-01-01**;
> 2. contar;
> 3. gravar contagem, janela e sha256 num commit só;
> 4. sortear e empurrar o D1;
> 5. merge.
>
> **Aberta, e decidir antes de segunda:** o n do silver é teto do n do K2. A calibração pela
> razão de 2021–2025 está na fila (`n-a` ou `n-b`).


## P-116 · O critério da janela entrou no mesmo commit que os resultados

**Dono:** Claude Code · **Gatilho:** toda medição nova contra o acervo · **Classe:**
`DECISAO_DE_DESENHO`

Os critérios do `fase0/test_ajustar_janela.py` foram escritos antes da primeira corrida, mas
entraram no **mesmo commit** que os números (`b54787b`). Um leitor externo não tem como
distinguir critério de resultado: **"pré-registrado" não é verificável pela P4.** No laudo e no
`ACHADOS.md` o rótulo passou a ser *"declarado pré-registrado, sem impressão digital"*. O
processo que evita a repetição: critério em um commit, **empurrado**, e só então a corrida
— o hash do commit do critério é a impressão digital.

## P-122 · `lightgbm` e `tabpfn` nunca foram medidos contra a faixa fechada

**Dono:** Claude Code (sessão local) · **Gatilho:** antes da ML-1 · **Classe:**
`BLOQUEIA_O_SISTEMA` · ⚙ **exige o desktop**

O `preregistro-ml-v2.md` §11 deixa as versões `NAO_CONFIRMADO` porque a consulta ao PyPI
**da nuvem** foi recusada por `robots.txt`. A sessão local não tem essa recusa. O conserto é
`py -3.11 -m pip install --dry-run lightgbm tabpfn "numpy==2.4.4" "pandas==3.0.2"` — e, se o
TabPFN trouxer `torch`, anotar o tamanho. É a entrada
`dependencias_da_familia_aprendizado_nao_medidas`.

## P-123 · O motor não aplica IR na venda de renda variável

**Dono:** próxima sessão · **Gatilho:** quando o motor ganhar rebalanceamento ou fase de
retirada · **Classe:** `BLOQUEIA_O_SISTEMA`

Era limitação declarada desde 04/09 **sem pendência** — o portão da §5-B.16 a cobrou. O vício
favorece o ETF (a isenção de R$ 20 mil/mês é só da ação), que é exatamente a decisão A05.
Efeito zero na acumulação sem venda. Entrada `ir_na_venda_de_renda_variavel`.

## P-127 · Oráculo externo do preço ajustado — **decisão sua**

**Dono:** Osvaldo (decidir) · **Gatilho:** antes de usar a série ajustada na ML-3 ·
**Classe:** `DECISAO_DE_DESENHO`

Ideia 4a de `docs/pesquisa/analise-pesquisa-apis-2026-09-23.md`. O C-02 valida o
`ajustar.py` contra ele mesmo; o instrumento que pegou o A-13 foi **duas fontes independentes
comparadas**. Um agregador de preço ajustado (plano gratuito) serviria de **controle** numa
amostra — mesmo papel, mesmo período, medir a divergência — e **nunca de feed** (rebaixaria a
P1). Exige pré-registro (P-116): o critério de "concordam" empurrado antes de olhar. A decisão
é se vale o custo, e qual fornecedor (os nomes são dos relatórios, `NAO_CONFIRMADO`).

> **Decisão dele, 26/09/2026: `127a`** (recomendada) — oráculo externo como **controle** numa amostra, depois da P-115, com o critério de "concordam" gravado antes de olhar e os termos do fornecedor lidos na fonte. Registro em `docs/decisoes/fila-do-osvaldo.md`.


## P-128 · Open Finance para posições e aporte — **decisão sua**

**Dono:** Osvaldo (decidir) · **Gatilho:** nenhum · **Classe:** `DECISAO_DE_DESENHO`

Ideia 4b. O aporte realizado e as posições (P-02) são o único insumo em que ele está no
caminho crítico todo mês (U-01, P7). É **candidata a pesquisa, não a integração**: cobertura,
custo e o que fica guardado com o terceiro estão `NAO_CONFIRMADO`, e é o dado mais sensível do
projeto — o mesmo que o `estado.yaml` protege ficando fora do git. A pergunta de privacidade
vem antes da técnica.

> **Decisão dele, 26/09/2026: `128b`** (**diverge da recomendada (128a)**) — **pesquisar** Open Finance (cobertura, custo, o que fica com o terceiro), sem integrar nada. Registro em `docs/decisoes/fila-do-osvaldo.md`.


## P-129 · Macro sem vintage — **decisão sua**

**Dono:** Osvaldo (decidir) · **Gatilho:** quando uma variável macro entrar num pré-registro ·
**Classe:** `DECISAO_DE_DESENHO`

Ideia 4c. O BCB SGS não guarda versões: série revisada substitui a antiga, então macro no
backtest seria o valor de hoje, não o publicado em `t`. Hoje não morde (o pré-registro ML não
usa macro). No dia em que usar, a proposta é uma entrada em `limitacoes_declaradas`, `tipo:
FISICA` — a fonte não publica as versões —, ou buscar vintage em outra fonte (ALFRED cobre
EUA, não BCB). A decisão é qual das duas.

> **Decisão dele, 26/09/2026: `129b`** (recomendada) — começar agora a guardar a versão própria das séries do SGS no armazém; para o passado, `FISICA` quando entrar num pré-registro. Registro em `docs/decisoes/fila-do-osvaldo.md`.


## P-137 · Conciliar os diários do COTAHIST contra o anual do mês

**Dono:** Claude Code · **Gatilho:** no primeiro dia 1º com diários e anual no armazém
(01/10/2026) · **Classe:** `BLOQUEIA_O_SISTEMA`

A B3 responde o mesmo `404` para feriado, fim de semana e dia útil cujo diário não foi
publicado (medido em 24/09). A captura registra `ausente` e segue — ela **não** sabe qual dos
três foi. O anual do mês tem todo pregão: o conserto é, depois de capturá-lo, comparar as
datas de pregão dele (`calendario.py`, que já lê COTAHIST pelo conteúdo) com os diários do
mês no armazém, e acusar por nome o pregão sem diário — e o diário que diverge do anual
naquela data. Sem isso, um diário perdido vira buraco calado na série diária até alguém
reconstruir do anual à mão: a forma do F-02, em que ausência de arquivo parece ausência de
pregão.

**Acrescentado em 24/09 (CH-01), duas exigências medidas:**
- a comparação diário × anual é por **multiconjunto** de linhas do dia (ordenar antes do
  sha256), nunca na ordem do arquivo: 4 dos 5 diários de 17–23/09 têm outra ordem que o
  anual e o mesmo conteúdo;
- a mesma rodada compara o anual **novo com o anual anterior** nos pregões em comum, pelo
  mesmo multiconjunto. É o que transforma o CH-01 (`n = 1` par, nenhum dia revisado) numa
  série: um par por mês, de graça, porque os dois anuais já estão no armazém. Um dia que
  mude ali é revisão da B3 — e é a única medição que diria se o anual mensal perde versões.


**25/09/2026 — o código existe, e está ligado ao workflow.** `fase0/conciliar_cotahist.py` +
12 testes (duas mutações reprovam: tirar a ordenação do multiconjunto e tirar o
`ANTES_DA_ROTINA`). Passo `Conciliar COTAHIST` no `captura_cvm.yml`, com vermelho próprio;
resultado em `docs/acervo/b3/conciliacoes.csv`, commitado pelo bot. **Medido antes de
escrever:** o diário tem o mesmo leiaute do anual (header `00COTAHIST.2026BOVESPA 20260924`,
245 posições, trailer com 15.903), então a leitura é a do `calendario.registros()`.

Duas escolhas de desenho, escritas no módulo: pregão anterior ao primeiro diário capturado é
`ANTES_DA_ROTINA`, não perda (a rotina começou em 17/09); e a versão anterior do anual é
escolhida pelo **instante** observado, não pela ordem das linhas do registro.

**O que vai acontecer, simulado sobre o registro real:** em 26/09 ele concilia **agosto** (o
anual de 24/09 cobre o mês); todos os pregões saem `ANTES_DA_ROTINA`, e a comparação entre o
anual de 24/09 (`4f2cf2…`) e o íntegro do inventário (`fb3546…`, até 18/09) é o **primeiro
ponto da série do CH-01** — quantos dias a B3 revisou. Em 01/10, setembro contra os diários.
**Fecha quando** a conciliação de setembro rodar no executor, com os diários de 17/09 em diante.

## P-136 · Ler a licença de redistribuição comercial dos dados da B3 — portão antes de servir outro usuário

**Dono:** Claude (leitura) · Osvaldo (decisão) · **Gatilho:** **antes de servir qualquer
usuário além dele** · **Classe:** `DECISAO_DE_DESENHO`

Hoje o dado da B3 (COTAHIST, eventos societários) é guardado para um usuário, num armazém
privado. A U-01 pergunta *"se esta ferramenta fosse vendida"*: nesse dia o sistema passaria a
redistribuir dado da B3 sem ninguém ter lido se pode. A leitura é com fonte primária e data de
acesso, para `docs/fontes/`; a mesma pergunta vale para a CVM (dados abertos) e é
provavelmente mais simples. Declarada em
`limitacoes_declaradas.licenca_de_redistribuicao_da_b3_nao_lida`.

> **25/09/2026 — a mesma leitura, feita para o NEFIN, e ela mudou o repositório.** O CSV de
> fatores estava no git, e portanto redistribuído, desde 04/09, sem ninguém ter lido os termos.
> Lidos na fonte (`docs/fontes/nefin.md`): uso livre, citação pedida, *"All rights reserved"*,
> nada sobre redistribuir. O arquivo saiu do git e foi para o armazém com captura diária
> (`fase0/capturar_nefin.py`), e o limite ficou declarado em `nefin_fora_do_git`. Achado
> LIC-01. **A B3 e a CVM continuam sem leitura.** O NEFIN mostrou que "dado público" e
> "redistribuível" são perguntas diferentes.


> **25/09/2026, noite — a leitura NÃO foi feita, e o motivo é da ferramenta, não da fonte
> (§5-B.17).** A sessão na nuvem tentou ler as duas fontes primárias e as duas responderam
> `EGRESS_BLOCKED` na política de rede **deste ambiente**: `www.b3.com.br`
> (`/pt_br/termos-de-uso-e-protecao-de-dados/termos-de-uso/` e a página de Séries Históricas) e
> `dados.cvm.gov.br` (`/dataset/cia_aberta-doc-dfp`). Destrava por dois caminhos: liberar os
> dois hosts em *Network access* do ambiente, ou a sessão local ler as páginas.
>
> **O que um buscador devolveu, e NÃO vale como leitura:** que os termos da B3 proíbem
> *"distribuição, redistribuição, […] publicação […] de todo ou parte"* do Market Data sem
> consentimento prévio, e que o portal da CVM publica sob **ODbL**. Os dois são resumo de
> buscador, sem o texto nem a data de vigência na mão — `NAO_CONFIRMADO` até a leitura.
>
> **O que foi medido no índice do git, e não depende da licença:**
> 1. **Nenhum dado de mercado bruto da B3 está no repositório.** `git grep` por registro
>    COTAHIST (`01` + data + código, 245 posições) e por payload de evento
>    (`lastDatePrior`, `closingPricePriorExDate`) não acha nenhum arquivo de dado: os acertos
>    são prosa de laudo e um comentário de código. Os CSVs de `docs/acervo/` guardam **metadado**:
>    URL, `Last-Modified`, ETag, sha256, tamanho.
> 2. **A pergunta tem uma segunda metade que ninguém tinha formulado: direito autoral de
>    DOCUMENTO, não só redistribuição de dado.** `docs/fontes/SeriesHistoricas_Layout.md`
>    (394 linhas) e `docs/fontes/Tarifacao_Equities_V5.0_PT.md` (182 linhas) transcrevem
>    publicações da B3 em seções marcadas *"texto literal"*. É a forma que dá procedência ao
>    projeto — e é também reprodução de documento de terceiro num repositório público. A
>    leitura dos termos tem de responder as duas.
> 3. **Os dois arquivos acima carregam `Fonte: NAO_REGISTRADA`**, o primeiro desde 03/09 —
>    embora a P-06 tenha fechado a fonte do leiaute em 19/09 (a URL está em
>    `docs/schemas/cotahist-v02.yaml`). Não troquei: provar que o `.md` transcreve **a mesma
>    revisão** daquele PDF é medição, não suposição (§5-B.1). O URL da V5.0 da tarifação não
>    está em lugar nenhum do repositório.


> **25/09/2026, 20:02 UTC — LIDA.** Ele liberou os dois hosts, e a leitura foi feita com `curl`
> (a ferramenta de leitura de página continuou com o bloqueio antigo). Texto das cláusulas,
> data de acesso e sha256 em `docs/fontes/b3-termos-de-uso.md` e
> `docs/fontes/cvm-dados-abertos-licenca.md`. O resumo do buscador estava certo nos dois pontos.
>
> - **B3:** "uso exclusivamente pessoal"; redistribuir, publicar, reformatar ou fornecer base
>   a terceiros a partir de dado de mercado é vedado sem consentimento prévio e expresso —
>   **sem** o qualificador "para fins comerciais". Virou `limitacoes_declaradas.
>   redistribuir_dado_da_b3_exige_consentimento` (`FISICA`); a entrada "não lida" ficou
>   `RESOLVIDA`. Servir um segundo usuário exige contrato com a B3.
> - **CVM:** ODbL no DFP, e citação obrigatória em todo uso secundário. A frase está no `NOTICE`.
>
> **O que resta é decisão dele — por isso a pendência continua aberta, agora com dono único:**
>
> 1. **DECIDIDA por ele, 25/09/2026: manter, sem mudança** (opção c). As transcrições ficam
>    como estão; o risco fica declarado aqui, com a leitura dos termos ao lado. Reabre se a B3
>    pedir a remoção ou mudar os termos (o sha256 em `docs/fontes/b3-termos-de-uso.md` acusa).
>    O texto abaixo é o que ele tinha diante de si ao decidir.
>
>    **As duas transcrições de documento da B3** (`SeriesHistoricas_Layout.md`, 394 linhas;
>    `Tarifacao_Equities_V5.0_PT.md`, 182). Os termos autorizam uso "exclusivamente pessoal" e a
>    proibição de "reprodução […] publicação" é ambígua quanto a "fins comerciais"; nenhuma
>    leitura torna a transcrição **integral** claramente permitida. Saídas: (a) reduzir a
>    **citação de passagens** com a fonte (Lei 9.610/1998, art. 46, III) — o leiaute como dado já
>    mora em `docs/schemas/cotahist-v02.yaml`; (b) pedir autorização à B3; (c) manter e declarar
>    o risco. Recomendação: (a). O histórico do git continua tendo o texto, como no NEFIN.
> 2. **DECIDIDA por ele, 25/09/2026: "pode ser público", e "pode executar o desenho".**
>    `docs/decisoes/P-136-cvm-publica.md` — release do GitHub, sem conta nem credencial nova,
>    porque o acesso público do R2 é do bucket inteiro e abriria a B3. **Executado:**
>    `fase0/publicar_cvm.py` + passo `Publicar CVM` no workflow. **A P-136 fecha quando a
>    release `cvm-acervo-2026` existir com as 64 versões** (plano medido) — P7: código escrito
>    não é rotina rodando. O texto abaixo é o que ele tinha diante de si.
>
>    **O armazém da CVM pode ser público.** A ODbL permite redistribuir com atribuição e
>    *share-alike*; as versões que a CVM já substituiu, que hoje só existem no R2, poderiam ser
>    servidas a quem reproduz. É escolha, não exigência — e custa banda do R2.
>
> **Não lido (P5):** a Política Comercial de Market Data da B3 (é ela que diz como se pede o
> consentimento) e a página de licença do ITR, FCA e CAD na CVM.

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

## P-147 · A captura do NEFIN ainda não rodou no executor

**Dono:** o workflow (ninguém dispara) · **Gatilho:** o cron diário das 09:15 UTC, ou um *Run
workflow* da *Captura CVM* · **Classe:** `BLOQUEIA_O_SISTEMA` (o CSV saiu do git e só volta
ao runner pelo armazém)

O CSV do NEFIN saiu do git em 25/09 (LIC-01). `fase0/capturar_nefin.py` rodou uma vez, na
máquina dele, e subiu a versão fixada ao R2 (`novo`, `619991c2192c…`). O passo `captura_nefin`
entrou no `captura_cvm.yml`. **Fecha quando** o passo sair verde no executor. Nesse dia, apagar
`limitacoes_declaradas.captura_do_nefin_ainda_nao_rodou_no_executor`, e o `test_P7` cobra que o
regime seja declarado onde ele lê.

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

## P-145 · A ponte e o universo do ML depois de 2012, e duas escolhas que a §2 não fez

**Dono:** Claude Code (medir) · ~~Osvaldo (as duas escolhas)~~ decididas por ele em 25/09 ·
**Gatilho:** antes da primeira
variável da ML-3 · **Classe:** `DECISAO_DE_DESENHO`

A P-143 fechou a ponte para **2010–2012** (a janela da emenda). O desenvolvimento vai até 2019:
os emissores do universo de 2013–2019 ainda não passaram pela conferência da CV-06, e a ponte
manual cresce com eles. Há também duas escolhas da §2 que mudam o universo e que a medição da
emenda não precisou fazer, porque o mês saiu igual nas duas:
1. *"3 meses anteriores"*: t-2..t ou t-3..t-1;
2. *"percentil ≥ 50"*: aplicado aqui como `≥ mediana` dos que passaram no filtro de pregões.

> **As duas escolhas foram decididas por ele em 25/09:** `t-2..t` e `≥ mediana` (inclusiva). Estão
> em `preregistro-ml-v2-emenda-1.md` §6 "Esclarecimentos", empurrada em `2f939ae` **antes** de
> qualquer número desta pendência (P-116). **sha256 publicado: `71621ba64c899281`.** O texto do
> commit `2f939ae` cita `380d747051f5e9b5`, o sha de um rascunho anterior à última correção de
> redação; o commit não foi reescrito, e o sha que vale é o do arquivo no `origin`. Falta a
> ponte de 2013–2019 e a captura do ISIN.
> **Houve uma segunda publicação da mesma §6, e ela não vale.** Uma sessão local, sem ver esta
> branch, empurrou ao `main` em `53112d6` (16:54Z) um texto de mesma substância e outra redação
> (sha256 `7fc09d780c5012ac`). O merge de 25/09 ficou com a versão de `2f939ae`, a primeira no
> `origin`; `53112d6` fica no histórico como registro. Achado GIT-01.
**E a captura do banco de ISIN não é rotina** (P7): foi uma vez, 25/09, `isinp.zip` sha256
`c4654dbd…`. Para 2010–2017 isso basta (o passado não muda), mas a ponte de um ano novo precisa
de captura, ou de limitação declarada.

> **26/09/2026 — a medição existe e roda sem o desktop; falta insumo e token, os dois dele.**
> `medicoes/p145_ponte_2013_2019.py`, pelo `.github/workflows/medir.yml` (CLAUDE.md §5-A.11), na
> branch `medir/p145_ponte_2013_2019`, com as duas leituras fixadas (`t-2..t`, `≥ mediana`
> inclusiva). Classifica cada emissor de 2013–2019 em `MANUAL`, `LIGADO_NOME_CONFERE`,
> `LIGADO_NOME_DIVERGE`, `CNPJ_SEM_CVM` (a forma dos 4 reaproveitados da CV-06) e
> `AUSENTE_DO_ISIN`, e lista os três últimos para a conferência à mão.
>
> **Resultado da primeira execução** (`36246813373`, 13:56Z): parou em *Conferir insumos*, sem
> segredo nenhum no ambiente — `isin/isinp.zip: nenhum registro nem inventario`. Medido também
> aqui, pelo mesmo comando: é o **único** insumo ausente; os oito COTAHIST fixados (2012–2019),
> o cadastro, os DFP de 2010–2019 e os ITR de 2011–2019 o acervo conhece. **Nenhum número da
> ponte existe ainda.** Para rodar faltam dois passos dele, na ordem:
> 1. ⚙ **desktop:** `py -3.11 fase0/subir_acervo_local.py --aplicar` — agora cobre o banco de
>    ISIN e sobe o `isinp.zip` de 25/09 (sha256 `c4654dbd…`) com o inventário;
> 2. **Cloudflare + GitHub:** um token do R2 **somente leitura** e os quatro segredos
>    `R2_LEITURA_ACCOUNT_ID`, `R2_LEITURA_ACCESS_KEY_ID`, `R2_LEITURA_SECRET_ACCESS_KEY`,
>    `R2_LEITURA_BUCKET`.
>
> Depois, a sessão empurra de novo a branch e o resultado volta commitado nela.
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

## P-130 · As posições do header do COTAHIST moram em Python

**Dono:** Claude Code · **Gatilho:** no próximo toque em `conferir_cabecalho` ou no leiaute ·
**Classe:** `DECISAO_DE_DESENHO`

Achado lateral da P-125. O `cotahist-v02.yaml` tem as posições do registro `01` desde a P-105,
mas o header (`00`) não: `conferir_cabecalho` fatia `[11:15]` e `[23:31]` no código. É a P-105
num registro vizinho — e foi exatamente numa fatia escrita à mão que o erro de um entrou. O
leiaute rev. 02 descreve o header; transcrevê-lo para o YAML e ler de lá é o conserto. Não foi
feito agora para não misturar mudança de esquema com o conserto de um valor.

## P-153 · Ranking de reclamações do BC na fonte, e o Reclame Aqui atualizado · era P-A9

**Dono:** sessão de pesquisa (nuvem) · **Gatilho:** antes de usar reclamação de cliente como
argumento de marca ou de produto · **Classe:** `DECISAO_DE_DESENHO`

Aberta pela [pesquisa de fundação](docs/marca/pesquisa-fundacao-2026-09.md) (A9) e não fechada
pela [rodada do Pix](docs/marca/pesquisa-pix-e-pendencias-2026-09.md) (§2.3): o ranking do
Banco Central foi lido por imprensa, com duas fontes divergindo sobre o 2º trimestre de 2026, e
o único dado do Reclame Aqui sobre investimentos é de 2017. O que fecha: a consulta no site do
BC, transcrita em `docs/fontes/` com data, e o ranking da categoria "Corretoras e Bancos de
Investimentos" do Reclame Aqui com a data da leitura.

## P-154 · Medir a fatia de quem investe sem segurança na decisão (H-A1) · era P-A1

**Dono:** Osvaldo (decide se, como e com quanto dinheiro) · Claude (desenho do questionário) ·
**Gatilho:** antes de dimensionar o público de entrada em qualquer texto comercial ·
**Classe:** `DECISAO_DE_DESENHO`

A rodada 1 estima ~28,6 milhões no perfil "Diversifica" (`PARCIAL`, derivado da ANBIMA), mas
**ninguém mediu** quantos deles se sentem inseguros ao decidir. A hipótese H-A1 propõe três
sinais: paralisia, dependência e arrependimento. Sem essa medição, "o público é grande" é
ordem de grandeza do perfil, não do público.

## P-155 · Ler a WCAG na fonte: contraste, alvo de toque e daltonismo · era P-WCAG

**Dono:** sessão de pesquisa (nuvem) · **Gatilho:** antes do brandbook e da primeira tela
desenhada · **Classe:** `DECISAO_DE_DESENHO`

O capítulo de acessibilidade do Pix é recomendação e não cobre contraste, tamanho de alvo nem
daltonismo ([Pix v7.4](docs/marca/pesquisa-pix-e-pendencias-2026-09.md), §1.1). Os requisitos
de interface declaram a lacuna (§5, item 2). O que fecha: a WCAG lida na fonte, com os critérios
que viram requisito novo (RI-22 em diante) e a verificação de cada um.

## P-156 · Teste com pessoas das hipóteses de interface e de marca

**Dono:** Osvaldo (recrutamento e custo) · Claude (roteiro, estímulos e pré-registro do
critério) · **Gatilho:** quando a especificação da F0 existir (`PLANO.md` §3-F0) ·
**Classe:** `DECISAO_DE_DESENHO`

Nenhum requisito foi validado com o público ([requisitos de
interface](docs/marca/requisitos-interface-v1.md), §4 e §5). Entram no teste: H-A1 e H-A2
(rodada 1), H-C1 (a camada 1 é entendida sem ajuda), H-C2 (a faixa numérica não custa
confiança, replicação no Brasil), RI-15 (a pergunta de intenção é respondida sem ajuda) e as
hipóteses H1 a H4 do teste de marca. O critério de cada uma é gravado antes de olhar (P4).
As H1 a H4 vêm de um pré-registro do teste de marca de 20/09 que **não está no repositório**
(a rodada 1 o cita e diz que o atualiza); trazê-lo do Projeto no claude.ai é o primeiro passo
desta pendência, antes de qualquer estímulo ser mostrado a alguém.

## P-157 · Importação de carteira: quais formatos são viáveis

**Dono:** sessão de pesquisa (nuvem) · **Gatilho:** antes de desenhar a tela O4 do [mapa de
telas](docs/ux/mapa-de-telas-v1.md) além do "digitar as posições" · **Classe:**
`DECISAO_DE_DESENHO`

O mapa prevê três caminhos (importar arquivo, digitar, começar do zero) e não sabe quais
arquivos existem. Candidatos a levantar na fonte: extrato da área do investidor da B3, nota de
corretagem, exportação das corretoras e o Open Finance (que a P-128 pesquisa). Critério: o
formato traz posição e custo com procedência, e o dado fica no aparelho (é dado de usuário).

## P-158 · Parecer jurídico sobre o enquadramento do MEOL

**Dono:** Osvaldo (contratar) · **Gatilho:** antes de qualquer usuário além dele, ou de
qualquer texto comercial público · **Classe:** `DECISAO_DE_DESENHO`

Nenhum documento de marca é parecer: todos o declaram. As perguntas abertas: se a decisão
mensal com procedência é recomendação de investimento no sentido da regulação; como os bancos
com agente de IA que recomenda e executa se enquadram ([rodada
2](docs/marca/pesquisa-marcas-rodada2-2026-09.md), §4.1, `NAO_CONFIRMADO`); e se "padrão é
recomendação" (RI-07) se sustenta. Depende da P-159: o parecer começa pela norma lida.

> **26/09/2026 — a P-159 fechou, e deixa três perguntas para cá.** A Resolução CVM 19 está
> transcrita em [`docs/fontes/cvm-resolucao-19-consolidada.md`](docs/fontes/cvm-resolucao-19-consolidada.md).
> (1) O art. 1º exige prestação "de forma profissional" a um cliente. O uso pessoal dele fica
> fora? A partir de qual momento o MEOL passa a ser serviço? *(26/09/2026: a transcrição dava
> "o uso pessoal não é prestação de serviço" como confirmado. Virou `INFERENCIA`, nota
> N-PESSOAL na transcrição: o texto lido não diz isso, e a resposta é do parecer.)* (2) O art. 2º, parágrafo único, I, e
> o art. 16, II, remetem à norma de adequação ao perfil do cliente, que não foi lida. (3) As
> Resoluções CVM 21 e 35, citadas pela pesquisa, não foram lidas. Nenhuma das três se resolve
> por leitura: é parecer.

## P-160 · Telas sem campo no contrato de saída da F0

**Dono:** Osvaldo (decidir o que entra) · Claude Code (especificar) · **Gatilho:** antes de
desenhar qualquer uma destas telas · **Classe:** `DECISAO_DE_DESENHO`

A especificação da F0 ([`docs/ux/F0-contrato-de-saida.md`](docs/ux/F0-contrato-de-saida.md),
§5) aplicou a regra do mapa de telas: tela sem campo não se constrói. Cinco ficaram sem campo:
a O5 (escolhas declaradas, com o porquê), a aba "e se" da T3 (que é contrato de chamada, não
de campo), as empresas da T4 (o motor decide rota, não papel), o aviso de queda do RI-04 e a
comparação líquido contra líquido do RI-11. Cada uma ganha campo na especificação, ou sai do
mapa com o motivo escrito.

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

## Ao voltar ao desktop

> **26/09/2026, nuvem — substitui a nota de 25/09 abaixo.** A revisão das pendências dele fechou
> 16 vencidas; o que é decisão dele está em **`docs/decisoes/fila-do-osvaldo.md`**, 15 blocos
> para responder pelo celular. Em ordem:
>
> 1. **As respostas da fila** viram o trabalho da sessão seguinte, a começar pela 1 (P-115) e
>    pela 2 (P-117), que vêm antes de qualquer janela nova da série ajustada.
> 2. ~~**P-151 antes de segunda, 28/09, 11:00 UTC.**~~ **Fechada em 26/09** (a guarda do GIT-01 pula no CI).
> 3. **P-150 — subir ao R2 o acervo de eventos de 11/09.** ⚙ **exige o desktop**. O script
>    cobre as pastas desde 26/09. Primeiro `py -3.11 fase0/subir_acervo_local.py` (só o plano):
>    conferir que os eventos aparecem como `SUBIR` em `b3/indice_carteira|eventos_suplemento|
>    proventos/…` e que não há `PARAR`. Um `DESCONHECIDO` em pasta de eventos se lê antes de
>    seguir. Depois, com as `R2_*` no ambiente, `--aplicar`, e commitar
>    `docs/acervo/b3_eventos/inventario-armazem.csv`. E conferir o cron de segunda, 28/09.
> 4. **P-147 (NEFIN) e a release `cvm-acervo-2026`:** conferir depois do cron de 26/09. Não
>    exige desktop.
> 5. ~~`macro.poupanca_am` vence em 28/09~~ — renovada em 25/09; vence em **24/10**.
> 6. **P-145 — dois passos dele destravam a medição na nuvem:** ⚙ **desktop:**
>    `py -3.11 fase0/subir_acervo_local.py --aplicar` (sobe o `isinp.zip`); e, de qualquer
>    lugar, o token do R2 **somente leitura** com os quatro segredos `R2_LEITURA_*`.
