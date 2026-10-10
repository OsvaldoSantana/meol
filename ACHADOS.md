# ACHADOS.md — o registro histórico

Todo defeito encontrado neste projeto, com a medição que o provou e o teste que o
prende. **Este arquivo não é instrução: é memória.**

## Por que ele foi separado do CLAUDE.md — 06/09/2026

O `CLAUDE.md` chegou a **1.112 linhas (~15 mil tokens)** e estava fazendo dois trabalhos
incompatíveis ao mesmo tempo:

| trabalho | quando precisa ser lido |
|---|---|
| **instruções** — doutrinas, convenções, como trabalhar, próximo passo | **toda sessão**, antes de tocar em qualquer coisa |
| **história** — os 25 achados, com narrativa completa | **só quando a tarefa toca aquela área** |

Misturados, os dois custavam ~15 mil tokens em toda sessão, e ~10 mil deles eram
narrativa que a tarefa do dia normalmente não precisava. Somados aos ~11 mil do
`PENDENCIAS.md`, davam **26 mil tokens gastos antes de qualquer trabalho começar** —
num plano com limite compartilhado entre o app e o Claude Code.

**Nada foi apagado.** A auditabilidade é o ponto do projeto inteiro; o que mudou é
*quando* se paga por ela. O `CLAUDE.md` ficou com 449 linhas de instrução e aponta para
cá quando o assunto exige.

## Como usar

Procure pela letra do achado (`F-02`, `N-01`, `S-02`…). Cada um tem: o que era, como
foi medido, o que mudou, e o teste que impede a volta. Se você vai mexer numa área,
leia os achados dela **antes** — vários destes defeitos são reincidências de um mesmo
padrão, e reconhecer o padrão vale mais que decorar os casos.

**O padrão que mais se repetiu**, e que já apareceu quatro vezes com roupas
diferentes — F-05, N-01, R-01, S-02: *um arquivo declara um comportamento que o código
não tem, e os dois concordam por acaso, então ninguém descobre.*

---

### J-01 / K-01 — a reserva que nunca existiu, e o pedágio do Turbinado

**A resolução veio dele, e ela desfaz um erro meu de modelagem.** Eu vinha tratando os
R$7.671 do cofrinho como "reserva que por acaso está empenhada", e inventei
`reserva_disponivel` para descrever isso. Ele corrigiu:

> *"Não tenho problemas em a reserva não estar no cofrinho de limite de cartão. Eu
> deposito lá porque não tinha um cartão com bom limite e uso o cartão como meio de
> pagamento. É só considerar que aquele valor não é uma reserva."*

O modelo certo é mais simples: **aquele dinheiro nunca foi reserva.** É caução de um
meio de pagamento, com propósito próprio. Os 102% do CDI são consolo, não objetivo.

`estado.yaml` tem hoje `reserva_atual: 0.00` e um bloco `deposito_garantia` separado,
que não compete no G2, não conta meses de despesa e não entra em patrimônio investido.
**A reserva de emergência dele é zero — não "zero porque travada", mas zero porque
nunca foi constituída.** A Fase A começa do começo, e isso é o dado.

**Onde eu errei, e vale como aviso.** Escrevi que a reserva seria "consumida pela
dívida que a prendia" e falei em "correlação −1 com a própria necessidade". Com o
propósito declarado, isso cai: o cartão é **garantido**, e uma dívida coberta 14,5× pelo
próprio depósito não é risco de crédito, é pagamento antecipado. **Deduzi risco de uma
estrutura sem perguntar o propósito dela.** A limitação do motor continua registrada
(G1 e G2 tratam dívida e reserva como independentes, e isso é um defeito real), mas com
`aplica_se_ao_caso_do_usuario: false`.

**J-03, e ele foi REFUTADO no mesmo dia.** Eu escrevi que o depósito comprava limite
a 14,5 para 1 e que havia "capital ocioso". Errado, e o erro foi de método: li "limite
**extra** de R$530" como se fosse o retorno inteiro do depósito, sem perguntar o limite
**total**. Ele informou: R$9.551. A conta fecha ao centavo — base R$1.349,99 (sem
cofrinho) + R$7.671,01 (cofrinho, **1 para 1**) + R$530,00 (bônus de 6,9%). O cofrinho
vira limite 1:1 e ainda paga bônus. **Não há capital ocioso e não há o que liberar sem
perder limite na mesma medida.**

**K-01, o pedágio do Turbinado.** 121% do CDI e resgate livre, mas R$23,99/mês. A
vantagem de 19 p.p. do CDI vale 2,113% a.a. líquido e só cobre os R$287,88/ano a partir
de **R$13.625** — e o **teto do produto é R$10.000**. Pagando, nunca se paga: no teto
ainda perde R$76,60/ano. Só vale com a isenção.

**K-03: a isenção é paga em outra moeda.** As missões deste mês foram **gasto no cartão**
e **trazer uma chave Pix** — uma terceira via, por tarefas que o banco escolhe e que
mudam todo mês. Os R$287,88/ano são o **piso**: falta o gasto marginal induzido pela
missão. Condição rebaixada a `PARCIAL` — a do mês seguinte é desconhecida por construção.

**K-02:** a reserva-alvo de R$36.000 não cabe num produto de teto R$10.000, e `RotaAloc`
não tem campo para teto de saldo (P-24).

### L-01 — a fronteira entre o motor e um usuário

Ele lembrou em 05/09 que **escalabilidade inclui servir mais pessoas**, e que o
projeto estava construído sobre as preferências dele. Medi antes de opinar: **109
chaves de motor contra 13 de usuário, no mesmo arquivo**.

O problema não era o tamanho — era que **um segundo usuário não teria onde pôr as
escolhas dele sem editar o `politica.yaml`, e ao editar apagaria as do primeiro.**

`compromissos` e `decisoes` foram para `perfil.yaml`. A fusão acontece na carga, então
**nenhum consumidor mudou**: os seis arquivos que liam essas seções continuam lendo
igual. Trocar de usuário é passar outro `perfil` a `carregar_politica()`.

Três testes guardam a fronteira: seção de perfil dentro da política falha; perfil que
redefina `portoes` ou `funcoes` é recusado (dois usuários com motores diferentes não
produzem nada comparável); e o perfil tem hash próprio, porque procedência de saída
precisa dizer **qual** perfil a gerou.

**Por que agora e não depois:** eram 13 chaves. Depois da Fase 0 e dos blocos de
análise seriam muitas mais, e cada decisão nova escrita no lugar errado aprofunda o
acoplamento. Separar cedo custou uma função de carga; separar tarde custaria uma
migração.

**Continua parcial (P-27).** Quatro seções são mistas *por dentro* — `corretora` junta
metodologia com os pesos que ele escolheu, e `custos.yaml → cofrinho` junta termos de
produto com o estado da conta dele. Dividi-las sem decidir a granularidade criaria
bagunça pior que a atual.

### O-01 / K-02 — o G2 media a média, e a média não descreve nenhum real

Fui fechar a P-24 (`teto_de_saldo`) e encontrei um defeito maior debaixo dela.

O G2 avaliava cada rota de liquidez **no alvo inteiro**, ordenava pela média e mandava
100% do aporte para a primeira. O Tesouro Selic é isento de custódia até R$10.000 e paga
0,20% a.a. acima disso — então o retorno **depende do saldo**, e a média em R$36.000 não
descreve nenhum real: os dez mil primeiros rendem mais do que ela diz, os vinte e seis
mil seguintes, menos. Avaliado em R$10.000 o Tesouro ganha do RDB; avaliado em R$36.000,
perde. Os dois números são verdadeiros e nenhum é o critério.

Com retorno dependente de saldo, **ordenar pela média e encher a primeira não dá o
melhor resultado.** O critério é o marginal — quanto rende o *próximo* real.

| | destino | R$/ano | em emissor privado |
|---|---|---|---|
| rota única | RDB 100% CDI | 3.878,10 | R$ 36.000 |
| composição | Tesouro 10k + RDB 26k | 3.885,85 | R$ 26.000 |

**O ganho em reais é R$7,75 por ano, e inflar isso seria repetir o erro do J-02.** O que
muda de verdade é outra coisa: a rota única **obrigava a escolher** entre o melhor
retorno e o melhor crédito. A composição não escolhe — os R$10.000 saem do emissor
privado sem custar retorno.

E aí o K-02 fica pior do que estava escrito. Não é que o portão "para de funcionar"
quando o produto enche. Com a isenção do Turbinado confirmada, o G2 antigo o elegeria
avaliando no alvo inteiro: R$36.000 a 13,03% = **R$4.692/ano**. O produto aceita
R$10.000. O número não era otimista — era retorno **sobre dinheiro que o produto
recusa**, e o portão continuaria mandando aporte para lá. Mesma família do F-02: resposta
bem formada sobre premissa que deixou de valer.

O `teto_de_saldo` não é o teto do FGC, e confundi-los inverte a consequência: o FGC
limita a **garantia** — passar dele é um risco que se pode aceitar; o teto de saldo
limita o que o produto **aceita** — passar dele não é arriscado, é impossível.

**Duas rotas entraram no catálogo, e uma delas é a única posição que ele tem.** O
cofrinho do PicPay não existia no catálogo: o sistema opinava sobre onde pôr dinheiro sem
enxergar onde o dinheiro está — o pior caso da P6. Entra **sem** a função LIQUIDEZ, que é
o achado J-01 inteiro (0 a 29 dias de espera conforme o dia da emergência), e rendendo
102% do CDI. Rende acima do CDI e ainda assim não serve para a função que ele precisa
preencher primeiro.

### N-01 — a seção `corretora` prometia três regras que o Python decidia sozinho

`multiplicador_de_confirmacao: {C: 1.00, P: 0.75, N: 0.00}` estava no `politica.yaml`,
com uma `regra:` explicando o porquê. E estava também em `corretoras.py`, como o literal
`mult = {"C": 1.0, "P": 0.75, "N": 0.0}`. **Os dois concordavam.**

Concordar é pior que discordar. Discordância aparece; concordância faz o arquivo parecer
governar o sistema quando não governa. Editar o YAML não mudava o ranking — e o ranking
de corretoras é a decisão de **onde o dinheiro fica guardado por dez anos**.

Eram três, e a terceira mostra o padrão:

| declarado no YAML | onde de fato vivia | agora |
|---|---|---|
| `multiplicador_de_confirmacao` | literal em `pontuar()` | lido do YAML |
| `reclamacoes.escala: "índice 0 = 100 pontos"` | `1 - bc_indice/100` | `escala_indice_para_nota_zero` |
| corretagem: nenhum campo | `0.01` com um comentário ao lado | `custo_do_aporte_para_nota_zero` |
| `reclame_aqui.pontua: false` / `exibe: true` | ninguém lia nenhum dos dois | `pontua: true` levanta exceção; `exibe` exibe |

O terceiro caso é o mais instrutivo: **o YAML não dizia nada** sobre a escala de
corretagem. A escolha de que 1% do aporte zera a dimensão — R$5 numa ordem de R$500 —
é o que separa "caro" de "inviável", e estava num comentário de código.

O quarto fecha uma mentira menor e mais teimosa: `exibe: true` mandava mostrar o Reclame
Aqui sem pontuá-lo, e a saída não o mostrava. Exibir **é** o ponto: o Itaú tem 8,1 no
Reclame Aqui e é o 3º mais reclamado do Brasil no ranking do BC. Esconder a fonte que
discorda é escolher a que agrada.

É o mesmo achado do **F-05** (`bloqueia` era prosa), em outra seção. Duas ocorrências do
mesmo defeito em dois dias significam que ele não é acidente — é o modo de falha padrão
deste projeto, e a P2 existe justamente contra ele.

### P-28 — o guarda media o próprio escopo

O `test_cobertura_yaml` existia desde 02/09 para pegar exatamente esse defeito. Ele
varria **6 das 19 seções**, lendo **3 dos 11 módulos**, com as duas listas escritas à
mão. Um teste de cobertura com escopo manual mede o escopo, não a cobertura — e foi por
esse vão que `revisao` entrou, foi declarada e nunca lida.

Agora são quatro testes, e o que importa é o terceiro:

1. varre todas as seções e todos os módulos (a lista de módulos vem do `listdir`);
2. toda seção precisa de **regime declarado com motivo escrito** — `OPERACIONAL` (o
   motor lê), `REGISTRO` (testemunho), `ESPECIFICAÇÃO` (escrito e não ligado);
3. **seção nova sem regime quebra a suíte.** Não há default. Esquecer virou barulho;
4. a dívida conhecida vive num inventário que **não pode apodrecer**: entrada já paga,
   ou de chave removida, faz o teste falhar.

O item 4 se provou na hora — a correção do N-01 pagou quatro entradas do inventário e o
teste mandou apagá-las. Um inventário que só cresce é decoração.

O que a varredura completa encontrou: **três seções inteiras especificadas e não
ligadas** (`bloco_C_solvencia`, `regime_instituicao_financeira`,
`estrategias_pre_registradas` — P-29 a P-31), e mais três blocos de dívida menor
(P-32 a P-34). Nenhuma delas era visível antes.

### Bloqueado nele, não em código

- **Tese do HASH11** (K02/K03/K04) e **compromisso do IPCA+** (C02–C06). Sem
  eles os dois ativos ficam em zero. Só passam a importar na Fase B.
- **O aporte realizado.** R$500 é o piso planejado; o realizado é zero. É o único
  número do projeto que nenhuma linha de código substitui.
- **Onde constituir a reserva** — ela é zero e começa agora. Os candidatos são
  `td_reserva` (Selic, isento de custódia até R$10 mil) e o Turbinado com isenção; o
  G2 sabe escolher entre eles assim que o destino existir.
- ~~**Se o empenho do cofrinho é obrigatório**~~ — resolvido: não importa, o valor não é reserva.

---


---

## 9. Armadilhas de repositório já encontradas

### F-04 — CRLF corrompe a série do NEFIN

`git` no Windows converte LF em CRLF no checkout (`core.autocrlf=true`). Para
código é inofensivo. Para `alocacao/dados/nefin_factors.csv` não é: são **6.322
bytes a mais** (um por pregão), e o sha256 que `fatores.hash_fonte()` publica muda
de `619991c2192c` para `421b3b3b753e`.

Isso quebraria a única coisa que o pré-registro promete — que um resultado de
backtest é reproduzível. Um clone novo em outra máquina Windows produziria números
iguais com procedência diferente, e ninguém perceberia.

Protegido em três camadas: `.gitattributes` marca o arquivo como binário;
`test_fonte_e_exatamente_a_serie_pre_registrada` fixa o hash; e
`test_serie_nao_tem_fim_de_linha_do_windows` procura `\r\n` direto nos bytes.
**Nunca "conserte" o hash esperado para fazer o teste passar** — se ele falhou, ou
a fonte mudou de propósito (então atualize e registre em `REGISTRO-vN.md`) ou algo
corrompeu o arquivo.

### Identidade do commit

O primeiro commit saiu como `osvaldo.junior@volga.local` — e-mail derivado do
hostname, que o GitHub não consegue atribuir a ninguém. Confira com
`git log -1 --format='%an <%ae>'` antes de assumir que a autoria está certa.

### G-01 — o schema não sabia dizer "regra decidida, papel não comprado"

`teses.yaml` só admitia um estado: compromisso pronto. Ele presume uma posição que
existe ou vai existir já. Mas a Fase A vai até ~2031 e não há conta em corretora —
e `C02_compromisso` exige o **juro real travado**, que só existe no dia da compra.

Preencher C02 hoje não seria pré-registro: seria ficção com hash. Deixar em branco
também não serve, porque as **regras** (prazo, condição de venda, teto,
reconhecimento) são decidíveis hoje — e hoje é exatamente quando pré-registrá-las
tem valor, antes de a posição existir.

Daí dois estados. `REGRA_DECIDIDA` sela o decidível e exige que os campos que
esperam a compra valham `AGUARDA_COMPRA` **em voz alta** — campo vazio não
distingue "ainda não sei" de "esqueci". `COMPROMISSO_ATIVO` exige tudo. A migração
acontece na compra, recalcula a impressão e manda a antiga para `historico`.

**O G8 não libera peso em `REGRA_DECIDIDA`.** Regra seleada não é posição.

### Git dentro do OneDrive

Este repositório fica numa pasta sincronizada pelo OneDrive corporativo. Isso
funciona na maioria dos dias, mas o modo de falha existe: o OneDrive trava um
arquivo dentro de `.git` durante um commit e o índice fica inconsistente.

Se acontecer: `rm -f .git/index.lock` e `git status`. Se o índice em si
corromper, `rm .git/index && git reset` reconstrói a partir do HEAD — os commits
já feitos não se perdem. Pausar a sincronização antes de operações grandes
(rebase, filter-branch) evita o problema.

---

## 10. Auditoria de engenharia — 05/09/2026

O Osvaldo perguntou se o projeto usa boas práticas e se é fácil de auditar e manter.
A resposta medida é: **auditável sim, e por um motivo incomum; manutenível não, e por
motivos comuns.** Esta seção existe para que nenhuma sessão futura confunda as duas.

### Onde ele é genuinamente bom, e não é opinião

| prática | evidência |
|---|---|
| todo defeito vira teste que falha na versão anterior | 216 testes, cada docstring nomeia o achado |
| rastreabilidade de decisão | `changelog` com 12 entradas; todo achado tem letra e data |
| procedência de dado | `status` + `fonte` + `acesso` + `expira` em 55 constantes |
| limitações declaradas | 8 entradas com **direção do viés** — raro até em código profissional |
| guarda contra config morta | 4 testes; regime obrigatório por seção; inventário de dívida que não apodrece |
| reprodutibilidade da série | hash fixado em teste + `.gitattributes` |

O item das **limitações com direção do viés** é o que mais distingue este projeto de
código comum. Quase nenhum sistema declara "esta simplificação favorece o ETF contra a
ação, e a decisão A05 é exatamente entre os dois".

### Onde ele falha, medido

**1. ~~A doutrina P2 é violada pelas duas maiores estruturas de dado do projeto.~~ —
FECHADA em 05/09.** `alocacao.catalogo()` (183 linhas, 25 rotas) virou `catalogo.yaml`
com um carregador de **39 linhas**; `corretoras.catalogo_instituicoes()` (136 linhas,
24 casas) virou `instituicoes.yaml` com um de **32**. Ver P-36 e os achados Q-01/Q-02
abaixo.

**2. ~~Funções grandes demais em pontos concentrados.~~ — FECHADA em 05/09.**
`alocar()` tinha **300 linhas** e virou seis passos de 16 a 51. A maior função do
motor hoje é `g2_reserva`, com 102. Ver P-37 e o achado R-01 abaixo.

**3. ~~Ferramental de projeto: não existe.~~ — FECHADA em 05/09, e o conserto tem uma
forma que vale registrar.** Havia um furo real: as versões de `numpy` e `pandas` que
produziram os números pré-registrados não existiam em lugar nenhum do repositório. O
dado estava selado (sha256 + `.gitattributes`); o ambiente não. Ver P-15 e a seção
sobre `ambiente.py` abaixo.

~~Continua faltando lint, type-checker e CI~~ — **ruff e mypy fechados em 06/09
(P-40), ambos em zero e ligados à suíte.** Continua sem CI, porque não há para onde
apontar enquanto o repositório não estiver no GitHub.

**4. Dinheiro é `float`.** Zero uso de `Decimal`. Para as contas atuais (percentuais,
projeções) é aceitável e o erro é irrelevante. Deixa de ser quando existirem
lançamentos, saldos e conciliação — e aí a migração é global.

**5. Cerca de um terço dos testes não exercita o motor.** Eles afirmam o conteúdo do
YAML. Não são inúteis — o P-28 e as limitações declaradas *são* esse tipo de teste, e
foi um deles que pegou o N-01. Mas eles inflam a contagem: "216 testes" não significa
216 comportamentos verificados. Ao citar o número, dizer o que ele mede.

**6. ~~Estado global carregado no import.~~ — FECHADA em 05/09.** O `conftest.py`
tem fixtures `custos`/`politica` e uma guarda que acusa o teste que suja estado
compartilhado. E o S-02 mostrou que o problema era maior do que a pendência descrevia
— ver abaixo.

**7. Nenhuma camada de persistência.** O blueprint prevê DuckDB + Postgres + Parquet.
Existe: YAML e um CSV. Isso é adequado à fase — mas quem ler o blueprint e depois o
código vai achar que falta código, e não é isso: **a Fase 0 nunca rodou.**

### O veredito, sem enfeite

Auditável **por um humano**, e muito. Um leitor cuidadoso reconstrói toda decisão a
partir dos arquivos, o que quase nenhum código permite. Auditável **por ferramenta**,
não: não há tipos, lint, CI ou lockfile.

Manutenível por quem escreveu, no mês em que escreveu. **Não manutenível por um
terceiro** — e a razão não é o tamanho, é que os dois catálogos exigem editar Python
para mudar um número de pesquisa, e nada testa se esse número tem procedência.

**A prioridade honesta de engenharia:** ~~P-15~~, ~~P-36~~, ~~P-37~~, ~~P-38~~ e
~~P-40~~ feitas. A fila de engenharia acabou. O que resta é P-43 (o terceiro catálogo)
e CI — e CI só faz sentido depois do push.

**O que NÃO fazer:** adicionar tipos e lint antes disso. Melhoram a leitura e não
fecham nenhum furo de veracidade, que é o que este projeto promete.

### P-15 fechada — `ambiente.py`, e a assimetria é a decisão de desenho

O projeto já sabia dizer de onde veio cada **número** (`status`/`fonte`/`acesso`/
`expira` em 55 constantes) e cada **dado** (sha256 da série do NEFIN, fixado em teste).
Não sabia dizer de onde veio o **resultado** — em qual ambiente foi calculado. E
`alfa_contra_fatores()` sai de `numpy.linalg.lstsq`, que é uma *implementação*, não um
teorema. Mesmo modo de falha do F-04, deslocado do dado para a máquina.

Três regras, e elas têm severidades **diferentes de propósito**:

| | severidade | por quê |
|---|---|---|
| toda dependência importada está declarada, e vice-versa | **erro duro** | é o "funciona na minha máquina" em forma testável |
| a impressão em `politica.yaml` bate com o `pyproject` | **erro duro** | trocar de `numpy` vira decisão visível, não efeito colateral de um `pip install -U` |
| a versão instalada é a registrada | **aviso** | quem carrega o alarme é o **resultado**, não a suíte |

A assimetria não é conveniência. Um teste que ficasse vermelho porque a máquina dele
tem outro `numpy` puniria trabalho legítimo com um alarme que não é sobre o código.
Um backtest que não dissesse em que ambiente rodou seria meio pré-registro. O
mecanismo do aviso é o mesmo do `expira`: `motor.val()` avisa em `stderr` e devolve o
valor.

**As versões vivem só no `pyproject.toml`.** O `politica.yaml` guarda apenas a
impressão digital calculada a partir dele — repetir os números nos dois arquivos seria
o N-01 outra vez. Não há `requirements.txt`, pelo mesmo motivo; o comando de instalação
se deriva da lista (`python ambiente.py --instalar`).

Dependências classificadas por **consequência**, não por importância: `numpy` e
`pandas` são *numéricas* (mudam número registrado); `PyYAML` e `pytest` são
*ferramentas* (um parser ou entrega os mesmos floats, ou erro). Divergência numérica
avisa; divergência de ferramenta não diz nada sobre a validade de nenhum número.

**O que a impressão NÃO promete,** e está escrito no registro: sistema operacional,
BLAS ligada ao `numpy` e arquitetura de CPU continuam fora, e podem mover a última casa
decimal de uma regressão. Ela cobre o que dá para cobrir com o repositório.

### P-36 fechada — o catálogo saiu do Python, e trouxe dois achados

| | antes | depois |
|---|---|---|
| `alocacao.catalogo()` | 183 linhas, 25 rotas em literais | **39 linhas** + `catalogo.yaml` |
| `corretoras.catalogo_instituicoes()` | 136 linhas, 24 casas em literais | **32 linhas** + `instituicoes.yaml` |

**A garantia da migração foi conferida campo a campo contra o objeto anterior: zero
diferenças, nas duas metades.** Isso não é detalhe de processo — é o único jeito de
migrar 39 registros com ~15 campos cada sem introduzir um erro silencioso. O snapshot
foi comparado, não relido.

**Regra central: valor que vem do `custos.yaml` fica como referência, nunca cópia.**
`adm_aa: {de: etf.PIBB11}` e não `adm_aa: 0.0059`. Copiar o número criaria dois lugares
que concordam — o N-01 em escala de catálogo — e mataria `expira`, `status` e `bloqueia`
da constante. Um teste prova pelo comportamento: mexer na constante *tem* de mexer na
rota.

O vocabulário de referência é pequeno de propósito: `{de:}`, `{soma:}`,
`{de_se_na_lista:}`, `{de_campo:}`. As três **estratégias de bloqueio** continuam em
Python — são lógica, não dado. O YAML diz *qual* se aplica e a *que* fonte; o Python diz
*como*. Acrescentar uma rota não exige tocar em Python; acrescentar um **tipo novo de
regra** exige, e deve exigir.

#### Q-01 — insumo bloqueado derrubava o catálogo inteiro

O tratamento era **inconsistente**, e as duas metades nunca se encontravam no mesmo
teste:

- rotas de ETF **degradavam**: `val()` levantava, a rota entrava sem a taxa e com o
  motivo escrito — foi assim que o BOVV11 ficou visível;
- todas as outras **explodiam**: `val()` levantava dentro de `catalogo()` e o catálogo
  inteiro morria.

Uma constante `NAO_CONFIRMADO` em `corretagem.safra_terra` apagaria as 25 rotas,
**inclusive as 24 que não dependem dela** — o oposto exato da doutrina P6. Regra única
agora: insumo bloqueado bloqueia **a rota**, com o motivo escrito, e a mensagem aponta
para a *constante* e não para o campo, porque quem lê precisa saber que número ir buscar.

#### Q-02 — a letra sempre falou de custos, e o registro não sabia dizer

`confirmacao` era uma letra por instituição, e `pontuar()` a aplica como **multiplicador
de tudo**: `N` zera a nota inteira. Mas ela nunca significou "este registro é confiável".
Sempre significou "os **custos** podem ser lidos em fonte oficial" — a própria `regra` do
multiplicador, em `politica.yaml`, diz isso com todas as letras.

As fontes provam: BTG, Bradesco, Mirae e Avenue têm `N` e `fonte` dizendo *"BCB IF.data
03/2026 (porte) — custos NÃO OBTIDOS"*. O balanço deles vem do **Banco Central**; o
índice de reclamações do BTG e do Bradesco vem do **ranking do BC**. Duas fontes
primárias, ambas completas.

**O comportamento estava certo** — não publicar custo tira da ordenação, por decisão
declarada. **O registro é que não sabia dizer**: um leitor do arquivo antigo concluiria
que o dado de balanço do BTG é duvidoso, quando ele veio do regulador.

A procedência passou a ser **por grupo de campos** — custos, balanço, reclamações,
Reclame Aqui, societário, facilidade —, porque é assim que as fontes de fato se agrupam.
E `confirmacao` deixou de ser campo próprio: é **derivada** de
`custos.procedencia.status`. Dois campos que podiam discordar viraram um; é o N-01
prevenido em vez de encontrado.

**O que isso não conserta, declarado:** a granularidade é por grupo, não por campo.
Procedência por campo daria 24 × 15 = 360 blocos para registrar cinco fontes reais, e
registro que ninguém lê é pior que registro nenhum. Se um campo um dia vier de fonte
diferente da do grupo, ele precisa de grupo próprio.

### P-37 fechada — e o achado que só apareceu depois da quebra

`alocar()` tinha 300 linhas e orquestrava nove portões. Virou seis passos:

| | linhas |
|---|---|
| `_preparar` | 16 |
| `fase_aporte` | 43 |
| `fase_universo` | 17 |
| `distribuir_por_funcao` | 46 |
| `alocar` | 51 |

A quebra segue **as fases que já existiam no YAML**, não um critério novo. A maior
função do motor hoje é `g2_reserva`, com 102 linhas, e um teste novo
(`test_P37_nenhuma_funcao_do_motor_passa_de_120_linhas`) impede que a próxima apareça
sem alguém decidir que deve aparecer.

**A garantia:** 38 cenários de estado foram serializados campo a campo antes da quebra
— pesos, **cada string de alerta**, cada pendência, cada rota em cada lista de rejeição
— e comparados depois. A única diferença em toda a matriz é o próprio `politica_hash`,
que mudou porque o `politica.yaml` mudou. Isso é o sistema de procedência funcionando,
não desvio.

#### R-01 — a ordem dos portões era um dado que só aceitava 18 de 120 valores

Este achado **só foi possível depois da quebra**, e é o argumento inteiro da P-37: com
`fase_universo` isolada, dá para permutar a ordem no YAML e observar o resultado sem
rodar a alocação completa. Com 300 linhas, não dava.

A P-07 declarou a ordem dos portões como dado e afirmou que trocá-la é um commit no
YAML. **Isso é falso para 102 das 120 ordens.**

A causa: os portões mudam a **forma** do que trafega. O `G3_atrito` é o único que
transforma — entra rota, sai `(rota, custo)` — e `G4`, `G7` e `G8` consomem pares.
Qualquer um deles antes do G3 estourava com `TypeError: cannot unpack non-iterable
RotaAloc object` disparado no fundo de uma função de portão, nunca com uma mensagem
dizendo que a **ordem** era o problema.

Declarar a ordem como dado sem declarar o contrato é declarar uma liberdade que não
existe — mesma família do F-05 (`bloqueia` era prosa) e do N-01.

Cada portão da fase `universo` passou a declarar `consome`/`produz`, e
`conferir_ordem_do_universo` recusa antes de rodar. O quadro medido:

| | ordens | |
|---|---|---|
| rodam | 18 | |
| recusadas com mensagem clara | 90 | novo |
| `InsumoBloqueado` | 12 | **não é defeito** — é o guarda do F-02 disparando |

As 12 são as ordens que põem o `G5_status` depois de um portão que calcula custo, e aí
uma rota bloqueada chega a uma conta. A mensagem já nomeia a rota e a constante.
Transformar isso num erro de ordem esconderia que a causa é outra.

**O `G5_status` é polimórfico de propósito** — aceita rota nua ou par e devolve o que
recebeu. Foi isso que permitiu corrigir o F-02 movendo-o para a frente sem quebrar nada,
e está declarado como `produz: mesma_forma`.

#### A cadeia de `elif` virou tabela

A fase `universo` era uma cadeia de `elif nome == ...`, e a consequência não era
estética: **a lista de portões implementados só existia escondida naqueles ramos**. Duas
validações precisavam dela — "este portão existe?" e "esta ordem é executável?" — e
nenhuma podia enxergá-la. Agora é `PORTOES_DO_UNIVERSO`, e o G6 aparece nela como um
não-faz-nada **nomeado, com o motivo escrito**, em vez de um `continue` que não
distingue "já rodou" de "esqueceram de implementar".

---

## 11. Como rastrear o alcance de uma alteração — 06/09/2026

O Osvaldo perguntou como eu rastreio, a cada mudança, onde o que foi alterado interage
com os outros arquivos. **A resposta honesta era: três ferramentas e nenhum mapa.**

| ferramenta | o que responde | limite |
|---|---|---|
| a suíte (265 testes) | *"quebrou?"* | responde **depois** |
| `grep` | *"onde aparece este nome?"* | depende de eu lembrar do nome certo |
| instantâneo dourado | *"mudou algum número?"* | caro; só vale para mudança grande |

Nenhuma delas responde, **antes** de editar: *"se eu mexer em `etf.BOVA11`, o que
alcança esse valor?"*. Foi assim que o **N-01** quase passou — procurei
`multiplicador_de_confirmacao` no Python, achei zero, e só não concluí "ninguém lê"
porque desconfiei do número repetido.

**`impacto.py` responde.** Ele não substitui a suíte: a suíte julga, ele orienta.

```bash
python impacto.py etf.BOVA11        # constante
python impacto.py simular_custo     # função
python impacto.py teto_de_saldo     # campo de dataclass
```

O que ele enxerga: `catalogo.yaml → custos.yaml` (46 arestas — e esse grafo é **dado**,
não inferência, desde a P-36), chave de YAML → módulo, o grafo de imports, o grafo de
chamadas com **fecho transitivo inverso**, e acesso a atributo.

**O que ele NÃO enxerga é a parte que importa mais**, e ele reporta junto: 14 leituras
com chave montada em tempo de execução (`P["funcoes"][f]`), `getattr` dinâmico, e
despacho por dicionário de funções. Toda conclusão de "ninguém lê isto" passa por essa
lista antes de virar decisão. **Um mapa que finge completude é pior que grep, porque
grep ninguém confunde com garantia.**

Três testes impedem o mapa de mentir: toda referência do catálogo aparece no grafo;
toda aresta aponta para constante que existe; e — o que separa mapa de desenho —
**alterar a constante que o mapa aponta tem de mudar exatamente as rotas que ele diz**.

### O protocolo, na prática

1. `python impacto.py <alvo>` — antes de editar, ver o que alcança.
2. Ler os pontos cegos. Se o alvo for lido por chave dinâmica, o mapa não basta.
3. Para mudança de contrato (dataclass, retorno de função, YAML estrutural):
   **instantâneo dourado antes**, comparar campo a campo depois. Foi o que garantiu a
   P-36 (39 registros) e a P-37 (38 cenários).
4. Rodar a suíte. Ela é o júri, não o guia.

---

## 12. Performance e escalabilidade — medido em 06/09/2026

O Osvaldo perguntou se estamos bem nas duas. **Estávamos mal na primeira, por um
motivo que também era um defeito de correção.**

### S-01 e S-02 — o cache que existia para acelerar era o defeito

**S-01.** `hash_custos()` era chamada **73 vezes por `alocar()`** — uma por consulta ao
cache de arrasto, que a usava na chave — e cada chamada **relia e re-hasheava os 33 KB**
do `custos.yaml`. **37% do tempo do motor** era gasto hasheando um arquivo para decidir
se podia usar um valor já calculado.

**S-02, e este é pior.** O cache global de `arrasto_anualizado` tinha na chave o hash do
**arquivo**. Mas o custo que a função usa vem do **`C` que chega como parâmetro**. Passar
um `C` alterado em memória — que é o que **todo teste faz**, via `deepcopy` — devolvia,
em silêncio, o valor calculado com o `C` original.

> Medido: com o CDI alterado de 13,9% para 50%, o arrasto voltava **idêntico**.
> Qualquer teste que alterasse um custo e conferisse arrasto ou dominância estava
> testando nada.

É a mesma família do F-02 e do N-01: um mecanismo que parecia funcionar e não
funcionava. E ensinou uma distinção que faltava:

| | do quê | serve a |
|---|---|---|
| `hash_custos()` | do **arquivo** em disco | **procedência** — de qual `custos.yaml` a saída nasceu |
| `impressao_de_custos(C)` | do **conteúdo** em memória | **correção de cache** — se dois cálculos podem compartilhar |

São iguais enquanto ninguém altera o `C` em memória. Todo teste altera. **Um cache cuja
chave não inclui a entrada não é um cache: é uma resposta errada guardada.**

`alocar()`: **9,79 ms → 2,75 ms**, e agora correto, que antes não era.

### Escalabilidade, por eixo — e os três eixos são diferentes

**Rotas do catálogo: quadrático, e não urgente.** Medido inflando o catálogo:

| rotas | `alocar()` | ms/rota |
|---|---|---|
| 25 | 12 ms | 0,48 |
| 100 | 68 ms | 0,68 |
| 400 | 728 ms | 1,82 |
| 800 | 2.810 ms | 3,51 |

A causa são quatro `next(v[0] for v in vivos if v[0].id == rid)` dentro de laços sobre
`pesos`. **Mas o input é limitado por desenho**: rota é um *tipo* de caminho, não um
papel — ação individual é uma *sleeve* dentro de `acao_zero`, não 400 rotas. O catálogo
realisticamente fica na casa das dezenas. É barato de consertar e não é o gargalo.

**Multiusuário: o gargalo é o carregamento, não o motor.** `carregar_politica()` custa
**82 ms** e `carregar()` **42 ms**. Para um usuário, irrelevante — são pagos uma vez.
Para N usuários × M chamadas, 124 ms de parse de YAML por chamada domina os 2,75 ms do
motor. É trivialmente cacheável **e ainda não foi feito** (P-41): fazer agora seria
otimizar para um cenário que não existe, e o S-02 é a prova de que cache mal
dimensionado custa correção.

**Fase 0 (dados da CVM): não existe.** O blueprint prevê DuckDB + Postgres + Parquet;
existe YAML e um CSV. Isso é adequado à fase — mas quem ler o blueprint e depois o
código vai achar que falta código, e não é isso: **a Fase 0 nunca rodou.**

### O veredito

**Performance: boa agora, e não era.** O que estava ruim não era lentidão — era um cache
que respondia errado, e a lentidão era o sintoma que fez olhar.

**Escalabilidade: boa no eixo que existe, não testada no que não existe.** A separação
motor/usuário (`perfil.yaml`) está feita e é o que importa para o segundo usuário. O
quadrático no catálogo é real e limitado por desenho. E não dá para afirmar nada sobre
o eixo de dados enquanto a Fase 0 não rodar — qualquer número aqui seria invenção.

---

## 13. P-40 fechada — lint e tipos, com cada dispensa justificada

**Zero, e não "poucos".** Uma barreira com baseline conhecida não é barreira: com 33
violações aceitas, a 34ª se esconde no ruído. Por isso a P-40 zerou antes de ligar a
guarda.

**A regra da casa vale para o próprio lint: toda dispensa tem motivo escrito**, e um
teste conta as linhas de justificativa — não dá para acrescentar um código de regra em
silêncio.

| dispensada | por quê |
|---|---|
| `E701`/`E702` | convenção da casa, 228 ocorrências, **nenhuma descuido**. Este código tem docstrings longas de propósito — elas carregam o achado, a fonte e o porquê. Espalhar o corpo afastaria o código da explicação que o justifica. |
| `E401` | `import os, sys, math` no topo; a lista é curta o bastante. |
| `E402` | `sys.path.insert` **antes** dos imports. Necessidade, não estilo — a alternativa é empacotar de verdade, que é mudança de estrutura. |
| `E731` | dois adaptadores de uma linha, usados logo abaixo. |
| `I001` | **incoerente com `E401`**: ele quer quebrar `import os, sys` em três linhas para poder ordená-las. Ligar uma regra que exige o que a outra dispensa é pedir para o lint brigar consigo mesmo. |

**`E501` ficou ligado**, ao contrário. As 39 linhas longas foram medidas antes de
decidir, e **seis delas eu mesmo criei na P-37** ao passar `P`, `pesos` e `alertas`
explicitamente para `espalhar` — viraram a tabela `BLOCOS_A_ESPALHAR`, que é melhor
código e cabe. Linha longa aqui costuma ser sintoma de assinatura que cresceu.

**As ferramentas ficam no grupo `lint` do pyproject, fora da impressão do ambiente.**
Não mudam número, então não pertencem à impressão que serve à reprodução (P-15); e
exigi-las instaladas deixaria vermelha a máquina de quem só quer rodar o motor.
**Vermelho que não é sobre o código ensina a ignorar vermelho.** Os testes pulam com o
comando que as liga.

### O que o lint achou de verdade

Pouco, e foi bom: 25 imports mortos, 5 f-strings sem placeholder, 2 nomes ambíguos, e
dois achados que valem por si:

**Um `None * float`** que o mypy não conseguia descartar em `pontuar()`. **Não era bug
em execução** — era um tipo que não dava para provar. Reescrito para calcular num local
e atribuir uma vez, ficou melhor e verificável em vez de argumentável.

**T-01 — há um terceiro catálogo.** `motor.montar_rotas` é paralelo ao `catalogo.yaml`:
**22 rotas contra 25, com 13 nomes que só existem lá**. A P-36 disse "os dois catálogos"
e havia três. Nenhum módulo de produção o chama — só o `test_motor.py`.

> O ruff viu uma **variável** morta; o defeito era a **chamada**. `B3V = val(C["b3"]
> ["vista_total_pct"])` era cópia da função de baixo, e a chamada **abortaria** se o
> valor fosse `NAO_CONFIRMADO` — dentro de uma função cuja docstring promete *"capturar
> InsumoBloqueado como marcador em vez de abortar"*.

Não foi apagado (P-43). **Apagar código com teste próprio sem medir o que os testes
guardam é como se perde uma rede.**

---

# Pendências fechadas — a narrativa completa

Migradas do `PENDENCIAS.md` em 06/09/2026. A tabela-resumo continua lá; aqui
está o texto inteiro de cada uma, para quem precisar reconstituir por que uma
decisão foi tomada daquele jeito.

---

## ~~P-03~~ · FECHADA em 05/09 — as seis citações conferidas

Cinco transcritas da fonte pública, uma **corrigida**: `ir_fii` citava a IN 1.585
art. 56, que está transcrito e não diz 20%. A base real é a **Lei 8.668/1993 art. 18
(red. Lei 9.779/1999)**. Era o único dos seis em que a fonte apontava para o lugar
errado — os outros cinco eram lacuna de leitura.

Teste novo impede que a categoria volte em silêncio.

---

## ~~P-07~~ · FECHADA em 05/09 — ordem dos portões virou dado

`politica.yaml → portoes.*.ordem` é iterado pelo motor. Portão sem `ordem` é erro
duro; portão declarado numa fase sem execução no motor também.

**Achado I-01 no caminho:** a ordem real **nunca foi G0→G8**. Sempre foi G6, G0, G1,
G2, G5, G3, G7, G8, G4 — G6 primeiro, G4 por último. A numeração sugeria uma sequência
que o código não executa, e a tabela do `CLAUDE.md` ensinava o modelo errado. Corrigida.

Um teste inverte a ordem no YAML e exige que o comportamento mude — se fosse
decorativa, ele passaria com qualquer sequência.

---

## ~~P-16~~ · RESOLVIDA em 05/09 — híbrido, e admite sem dado

**P-16a: híbrido.** O nível corta, a tendência marca sem poder de veto. A metade que
corta roda hoje; a que marca fica em `AGUARDA_SERIE` até a Fase 0 — mesmo padrão do
`REGRA_DECIDIDA`. O bloco não fica travado esperando: roda cego à direção e **diz que
está cego**.

**P-16b: admitir com marcação.** Contra a minha recomendação, e ele está certo:
admitir não inventa número nenhum, logo não fere a P1. Excluir por falta de dado seria
viés de sobrevivência pela porta dos fundos.

Registrei por que isso **não** contradiz o caso BOVV11: lá o custo era insumo de
**ordenação** e sem ele só dava para ranquear inventando zero. Solvência é critério de
**exclusão** — deixar de excluir não produz número falso.

**Falta decidir**, só quando a série existir: quantos trimestres a tendência olha, e o
que fazer com empresa jovem sem histórico.

---

## ~~P-21~~ · RESOLVIDA — aquele dinheiro não é reserva

*"É só considerar que aquele valor não é uma reserva."* Isso desfez o nó e um erro meu:
eu modelava os R$7.671 como reserva-empenhada e inventei `reserva_disponivel`. O modelo
certo é mais simples — é **caução de um meio de pagamento**.

`estado.yaml`: `reserva_atual: 0.00` e um bloco `deposito_garantia` à parte, fora do
G2 e fora do patrimônio. **Sua reserva de emergência é zero porque nunca foi
constituída**, não porque está travada.

**Rebaixei o J-02.** Eu havia escrito que a reserva seria "consumida pela dívida" e
falei em "correlação −1". Com o propósito declarado isso cai: o cartão é garantido, e
dívida coberta 14,5× pelo próprio depósito é pagamento antecipado, não risco. Deduzi
risco de uma estrutura sem perguntar o propósito dela.

---

## ~~P-26~~ · REFUTADA — o depósito compra limite 1 para 1

Eu havia calculado 14,5:1 e falado em "capital ocioso". **Errado.** Li "limite extra de
R$530" como se fosse o retorno inteiro, sem perguntar o limite total.

| | |
|---|---|
| limite base, sem cofrinho | R$ 1.349,99 |
| cofrinho, convertido **1:1** | R$ 7.671,01 |
| bônus por guardar (6,9%) | R$ 530,00 |
| **total** | **R$ 9.551,00** |

Fecha ao centavo com o que você informou. Não há capital ocioso, e não há o que
liberar sem perder limite na mesma medida.

---

## ~~P-33~~ · FALSO POSITIVO, retirada em 05/09

`aporte_extraordinario.registro` é uma **instrução ao humano** de 244 caracteres, não um
parâmetro. O primeiro inventário de dívida a listou porque eu classifiquei prosa à mão.
O guarda ganhou uma segunda porta — valor de 120 caracteres ou mais é parágrafo, não
configuração — e mandou apagar a linha. Um teste novo cobra o preço dessa regra: se
algum dia um valor longo virar comportamento, ele quebra.

---

## ~~P-24~~ · FECHADA em 05/09 — o G2 devolve composição, e apareceu um segundo achado

`RotaAloc.teto_de_saldo` existe, e o G2 passou a compor a reserva em vez de eleger uma
rota. O que o conserto encontrou pelo caminho vale mais que o conserto:

**K-02 é pior do que estava escrito.** Não é só que o portão "para de funcionar" quando
o produto enche. Com a isenção do Turbinado confirmada, o G2 antigo o elegeria avaliando
no alvo inteiro: **R$36.000 a 13,03% = R$4.692/ano**. O produto aceita **R$10.000**. O
número não era otimista — era **retorno sobre dinheiro que o produto recusa**. A
composição devolve R$4.112, que é o que existe. R$580/ano de ficção, 14%.

**O-01, achado novo.** O retorno de algumas rotas **depende do saldo**: o Tesouro Selic
é isento de custódia até R$10.000 e paga 0,20% a.a. acima disso. O G2 avaliava tudo no
alvo inteiro, e a média não descreve nenhum real — os dez mil primeiros rendem mais do
que ela diz, os vinte e seis mil seguintes, menos. Com retorno dependente de saldo,
**ordenar pela média e encher a primeira não dá o melhor resultado.** O critério certo é
o marginal.

| | destino | R$/ano | em emissor privado |
|---|---|---|---|
| rota única (antes) | RDB 100% CDI | 3.878,10 | R$ 36.000 |
| composição (agora) | Tesouro 10k + RDB 26k | 3.885,85 | R$ 26.000 |

**O ganho em reais é pequeno — R$7,75/ano — e dizer o contrário seria inflar o achado.**
O que muda de verdade é outra coisa: a rota única **obrigava a escolher** entre o melhor
retorno e o melhor crédito. A composição não escolhe: os R$10.000 do Tesouro saem do
emissor privado **sem custar retorno**.

`criterio_escolha_rota` passou de `retorno_liquido` para `retorno_liquido_marginal`, e o
valor antigo agora **levanta erro** em vez de ser aceito em silêncio — ele nomeia um
comportamento que o motor não faz mais.

**Duas rotas entraram no catálogo** (doutrina P6): `picpay_cofrinho` e
`picpay_turbinado`. A primeira é a única posição que você possui e **não existia no
catálogo** — o pior caso da P6: o sistema opinava sobre onde pôr dinheiro sem enxergar
onde o dinheiro está. Ela entra **sem a função LIQUIDEZ**, que é o achado J-01 inteiro:
0 a 29 dias de espera conforme o dia em que a emergência cair. O Turbinado entra
**bloqueado** — a isenção depende de missões que mudam todo mês e que o banco escolhe.

---

## ~~P-13~~ · FECHADA em 05/09 — `isento_ir` virou dois campos

`isento_ir_rendimento` (bool) e `aliquota_ganho` (float ou `None`). `None` significa
"usa a tabela geral", **não** zero — confundir os dois seria o F-02 outra vez, com
ausência virando o número mais favorável.

O campo antigo virou propriedade que lê o novo: ele **sempre** se referiu ao
rendimento, e o rename só tornou isso explícito. Um teste garante que nenhum chamador
antigo mudou de resposta.

---

## ~~P-14~~ · RESOLVIDA em 05/09 — construir a fonte do BCB

**Banco não sai do universo.** Eu havia oferecido três variantes de excluir e
recomendado uma; isso contradiz a regra fundadora do projeto, agora escrita como
doutrina P6.

Meu argumento — "se a A05 der núcleo indexado, o bloco nunca roda" — é verdadeiro e
**irrelevante**: ele justifica *adiar a construção*, nunca *excluir o ativo*. Confundi
ordem de trabalho com escopo.

**Consequência:** a Fase 0 passa a ter duas esteiras — CVM (societária → bloco C) e BCB
(prudencial → bloco de banco). Aumento de escopo decidido **antes** de construir, que
era exatamente o ponto do achado H-02.

**Continua aberto:** a ordem entre as duas esteiras. Aí o argumento da A05 vale — a
esteira da CVM serve aos dois caminhos, a do BCB só a um.

---

---

## ~~P-15~~ · FECHADA em 05/09 — `pyproject.toml` + `ambiente.py`

Não era higiene: era um furo na promessa central. O pré-registro afirma que um
resultado de backtest é reproduzível, e o `.gitattributes` + o hash da série protegiam
*o dado*. As versões de `numpy` e `pandas` que produziram os números **não estavam
registradas em lugar nenhum** — e `alfa_contra_fatores` passa por
`numpy.linalg.lstsq`, que é uma implementação, não um teorema.

**Três regras, com severidades diferentes de propósito:**

| | severidade |
|---|---|
| toda dependência importada está declarada, e vice-versa | **erro duro** |
| a impressão em `politica.yaml` bate com o `pyproject` | **erro duro** |
| a versão instalada é a registrada | **aviso** |

A assimetria é a decisão de desenho. Um teste vermelho porque a sua máquina tem outro
`numpy` puniria trabalho legítimo com um alarme que não é sobre o código. Quem carrega
o alarme é o **resultado** — `alfa_contra_fatores()["ambiente"]` traz
`reproduz_o_registrado` —, não a suíte. Mesmo mecanismo do `expira`.

**As versões vivem só no `pyproject.toml`.** O `politica.yaml` guarda a impressão
digital (`7565df1381e2c1ed`) calculada a partir dele. Não há `requirements.txt` de
propósito: duas listas concordando é o N-01. O comando sai da lista:

```powershell
python ambiente.py --instalar
```

Dependências classificadas por **consequência**: `numpy` e `pandas` são *numéricas*;
`PyYAML` e `pytest` são *ferramentas*.

**O que não cobre, declarado:** sistema operacional, BLAS e arquitetura de CPU
continuam fora e podem mover a última casa de uma regressão.

**Na terça:** se `python ambiente.py` acusar versões diferentes, isso é informação
correta e não um problema a consertar às pressas. Rode o comando de instalação se
quiser reproduzir os números registrados; se preferir suas versões, os 224 testes
continuam válidos e o backtest passa a produzir número novo em vez de conferir o
antigo. **A decisão é sua e agora ela é visível** — que era exatamente o que faltava.

---

## ~~P-36~~ · FECHADA em 05/09 — o catálogo saiu do Python, e trouxe dois achados

| | antes | depois |
|---|---|---|
| `alocacao.catalogo()` | 183 linhas, 25 rotas em literais | **39 linhas** + `catalogo.yaml` |
| `corretoras.catalogo_instituicoes()` | 136 linhas, 24 casas em literais | **32 linhas** + `instituicoes.yaml` |

**As duas migrações foram conferidas campo a campo contra o objeto anterior: zero
diferenças.** Não é detalhe de processo — é o único jeito de mover 39 registros com ~15
campos cada sem introduzir um erro silencioso.

**Valor que vem do `custos.yaml` ficou como referência, nunca cópia:**
`adm_aa: {de: etf.PIBB11}`. Copiar o número seria o N-01 em escala de catálogo, e
mataria `expira`, `status` e `bloqueia` da constante. Um teste prova pelo comportamento:
mexer na constante *tem* de mexer na rota.

### Q-01 · insumo bloqueado derrubava o catálogo inteiro

O tratamento era **inconsistente**, e as duas metades nunca se encontravam no mesmo
teste: rotas de ETF **degradavam** (entravam sem a taxa e com o motivo escrito — foi
assim que o BOVV11 ficou visível); todas as outras **explodiam** dentro de `catalogo()`.

Uma constante `NAO_CONFIRMADO` em `corretagem.safra_terra` apagaria as 25 rotas,
**inclusive as 24 que não dependem dela** — o oposto exato da P6. Regra única agora:
insumo bloqueado bloqueia **a rota**.

### Q-02 · a letra sempre falou de custos, e o registro não sabia dizer

`confirmacao` era uma letra por instituição, aplicada como **multiplicador de tudo**.
Mas sempre significou *"os **custos** podem ser lidos em fonte oficial"* — a própria
`regra` do multiplicador diz isso. BTG, Bradesco, Mirae e Avenue têm `N` com `fonte`
dizendo *"BCB IF.data 03/2026 (porte) — custos NÃO OBTIDOS"*: o balanço vem do **Banco
Central** e o índice de reclamações, do **ranking do BC**.

**O comportamento estava certo. O registro é que não sabia dizer** — um leitor
concluiria que o dado de balanço do BTG é duvidoso, quando veio do regulador.

Procedência passou a ser **por grupo de campos**, e `confirmacao` virou **derivada** de
`custos.procedencia.status`. Dois campos que podiam discordar viraram um.

**Declarado, não consertado:** a granularidade é por grupo, não por campo. Por campo
seriam 24 × 15 = 360 blocos para cinco fontes reais, e registro que ninguém lê é pior
que registro nenhum.

---

## ~~P-37~~ · FECHADA em 05/09 — e o achado só apareceu depois da quebra

`alocar()` virou seis passos: `_preparar` (16), `fase_aporte` (43), `fase_universo`
(17), `distribuir_por_funcao` (46), `alocar` (51). A quebra segue **as fases que já
existiam no YAML**, não um critério novo. Maior função do motor hoje: `g2_reserva`, 102
linhas — e um teste novo impede que a próxima passe de 120 sem alguém decidir.

**A garantia:** 38 cenários serializados campo a campo antes — pesos, **cada string de
alerta**, cada pendência, cada rota em cada lista de rejeição. A única diferença em toda
a matriz é o próprio `politica_hash`, que mudou porque o `politica.yaml` mudou.

### R-01 · a ordem dos portões era um dado que só aceitava 18 de 120 valores

**Só foi possível encontrar depois da quebra** — é o argumento inteiro da P-37. Com
`fase_universo` isolada dá para permutar a ordem e observar o resultado sem rodar a
alocação inteira; com 300 linhas, não dava.

A P-07 declarou a ordem como dado e afirmou que trocá-la é um commit no YAML. **Falso
para 102 das 120 ordens.** Os portões mudam a **forma** do que trafega: o `G3_atrito` é
o único que transforma (entra rota, sai `(rota, custo)`) e `G4`, `G7` e `G8` consomem
pares. Qualquer um antes do G3 estourava com `TypeError` no fundo de uma função de
portão, nunca dizendo que a ordem era o problema.

| | ordens | |
|---|---|---|
| rodam | 18 | |
| recusadas com mensagem clara | 90 | novo |
| `InsumoBloqueado` | 12 | **não é defeito** — guarda do F-02 disparando |

Cada portão passou a declarar `consome`/`produz`. Declarar a ordem como dado sem
declarar o contrato era declarar uma liberdade que não existe — mesma família do F-05.

---

## ~~P-38~~ · FECHADA em 06/09 — e o problema era maior que a pendência

`conftest.py` com fixtures `custos`/`politica` e uma guarda que **acusa o teste que
suja estado compartilhado, nomeia o objeto e restaura** para que só o culpado fique
vermelho.

**A escolha de desenho:** copiar sempre custaria 0,23 s e *esconderia* o defeito;
detectar custa 0,38 s e o *reporta*. Este projeto detecta — esconder defeito atrás de
cópia é o padrão que ele passou a semana rejeitando. Declarado no arquivo: a guarda
mora no teardown, então o pytest rotula **ERROR**, não FAILED. Dá para relabelar com um
hook; não foi feito, porque seriam dez linhas de esperteza para mudar uma palavra.

---

## ~~S-01~~ e ~~S-02~~ · FECHADOS em 06/09 — o cache que acelerava era o defeito

**S-01:** `hash_custos()` era chamada **73 vezes por `alocar()`** e cada chamada relia e
re-hasheava os 33 KB do `custos.yaml`. **37% do tempo do motor.**

**S-02, pior:** o cache global de `arrasto_anualizado` tinha na chave o hash do
**arquivo**, mas o custo vem do **`C` que chega como parâmetro**. Passar um `C` alterado
em memória — o que **todo teste faz** — devolvia o valor do original, em silêncio.
Medido: com o CDI de 13,9% para 50%, o arrasto voltava idêntico. **Qualquer teste que
alterasse um custo e conferisse arrasto ou dominância estava testando nada.**

Nasceu a distinção que faltava: `hash_custos()` é do **arquivo** e serve à
**procedência**; `impressao_de_custos()` é do **conteúdo** e serve à **correção de
cache**. `alocar()`: 9,79 ms → **2,75 ms**, e correto.

---

## ~~P-39~~ · FECHADA em 06/09 — `impacto.py`, o mapa que não existia

Pergunta do Osvaldo: *como você rastreia onde o que foi alterado interage com os outros
arquivos?* A resposta honesta era **suíte + grep + instantâneo dourado, e nenhum mapa**.

`python impacto.py <constante | função | campo>` responde antes de editar. Reporta os
**14 pontos cegos** junto — chave montada em tempo de execução, `getattr` dinâmico,
despacho por dicionário. Três testes impedem o mapa de mentir, e o terceiro é o que
separa mapa de desenho: **alterar a constante que o mapa aponta tem de mudar exatamente
as rotas que ele diz.**

---

## ~~P-40~~ · FECHADA em 06/09 — ruff e mypy em zero, ligados à suíte

**Zero, e não "poucos".** Barreira com baseline conhecida não é barreira: com 33
violações aceitas, a 34ª se esconde no ruído.

**Toda dispensa tem motivo escrito no `pyproject.toml`**, e um teste conta as linhas de
justificativa — não dá para acrescentar um código de regra em silêncio. `E701`/`E702`
são convenção da casa (228 ocorrências, nenhuma descuido); `I001` saiu por ser
**incoerente com `E401`**; `E501` ficou **ligado**, porque seis das linhas longas eu
criei na P-37 e viraram uma tabela.

As ferramentas ficam no grupo `lint`, **fora da impressão do ambiente** — não mudam
número, e exigi-las instaladas deixaria vermelha a máquina de quem só quer rodar o
motor. Os testes **pulam** com o comando que as liga. **Na terça isso vai pular, e está
certo.**

**O que achou:** 25 imports mortos, 5 f-strings vazias, 2 nomes ambíguos, 1 `None *
float` que não era bug em execução (era tipo não provável — o código ficou melhor), e o
T-01 abaixo.

---

---

## Achados de 06/09 a 18/09 — o corpo que saiu do `CLAUDE.md` em 19/09/2026

**Decisão C, executada.** Estas 962 linhas viviam na §7 do `CLAUDE.md` ("Onde o projeto
está"), e a §10 do mesmo arquivo dizia desde 06/09 que achado mora aqui — *"não estão ali
de propósito"*. O corte foi fazer o arquivo cumprir a própria regra.

No `CLAUDE.md` ficou um **índice**: uma linha por achado, com a **regra** que ele deixou. O
critério do Osvaldo era *"otimização sem perder contexto"*, e a triagem foi por **função**:
a regra impede a repetição e fica; a narrativa explica e vem para cá. Medido: 26/26 achados
com endereço, `−17.816 tokens` no `CLAUDE.md` (−33,7%).

O texto abaixo está **como estava**, sem edição — inclusive as retificações internas e o
E-05 retirado, porque achado retirado fica como retratação.

---

> **X-01 — o dado estruturado não alcança a decisão. 06/09/2026, e é o achado mais caro
> desta sessão.**
>
> O Osvaldo respondeu como se lê uma incorporadora (`docs/auditoria/regime-incorporacao.md`).
> A sequência dele tem dez passos. **Três são obtíveis nas 8 demonstrações estruturadas da
> CVM.** VSO, vendas líquidas, distratos, receita a apropriar, unidades em estoque, e a
> separação entre dívida SFH e corporativa **não existem** nos CSVs — vivem em **nota
> explicativa** e em **release de resultados** (protocolado como IPE).
>
> E os três obtíveis são justamente os que ele **não** colocaria em primeiro lugar.
>
> A Fase 0 inteira foi desenhada em cima dos CSVs de DFP/ITR. **Isto não invalida a Fase 0
> — ela continua necessária. Mostra que ela não é suficiente**, e que existe uma segunda
> esteira (extração de documento) de ordem de grandeza diferente, que nunca foi orçada.
> Não há razão para supor que construção seja exceção: banco já era, e agora são dois.
>
> **O que a doutrina obriga:** P6 — construção não sai do universo. `empresa_sem_dado` —
> admitir com marcação. Então empresa de regime `INCORPORACAO` entra marcada, com o motivo
> escrito e **contável**. E nasce uma camada de desenho que o projeto não tinha:
> **portão** (automático, todo o universo, dado estruturado) × **dossiê** (manual, lista
> curta, notas e release). Para incorporação o portão só pode dizer *"esta empresa exige
> dossiê"* — P-64.

> **Y-01 — chave YAML duplicada é sobrescrita em silêncio. 10/09/2026.**
>
> `custos.yaml` tem **duas** entradas `etf.IMAB11` (linhas 171 e 253). O PyYAML **não
> reclama**: fica com a última. O que o motor lê hoje é `valor: null,
> status: NAO_CONFIRMADO` — a entrada de 05/09, com valor 0,25%, fonte e data de acesso,
> **está morta desde que foi escrita**.
>
> É o F-02 numa camada nova: lá insumo ausente virava zero; aqui **insumo presente é
> sobrescrito por um ausente**. O erro é na direção conservadora (a rota fica bloqueada),
> o que é sorte, não desenho.
>
> **Pergunta aberta:** o registro diz "F-03 medida e refutada (IMAB11 perde do Tesouro)".
> Se o motor lê `None`, **com que número essa medição foi feita?** Responder antes de
> apagar qualquer das duas entradas.
>
> **O teste que falta não é sobre IMAB11** — é uma varredura do YAML cru procurando chave
> repetida em qualquer mapping. Um teste do IMAB11 seria patch.

> **A-01 e A-02 — 11/09/2026, a primeira corrida real da Fase 0, e ela rendeu dois
> achados que nenhuma leitura teria dado.**
>
> **A-01 — `B3SA3` virou `BSA`, e a B3 respondeu 200.** O coletor derivava a emissora
> filtrando dígitos do ticker. Funciona em 73 dos 74 ativos do Ibovespa e erra em
> **B3SA3**, cujo código de emissora é `B3SA` — tem dígito no meio. O endpoint **casou
> com outra empresa** e devolveu capital social de R$9,61 bi datado de 1981.
>
> Este é o modo de falha mais caro do projeto inteiro: **não é ausência de dado, é dado
> do ativo errado, com aparência perfeita.** Nenhum teste de "veio resposta?" o pega. A
> regra certa é posicional — ticker da B3 é 4 caracteres de emissora + dígitos —, e o
> coletor agora imprime o nome da empresa em cada linha, para que a divergência seja
> visível a olho.
>
> **A-02 — eu registrei o formato do endpoint errado.** `docs/fontes/pesquisa-bases-e-apis-2026-09.md`
> diz que `GetListedSupplementCompany` devolve um **objeto**. Devolve uma **lista**. As 74
> emissoras vieram como lista, sem exceção. A leitura original passou por uma ferramenta
> de resumo, que desembrulhou a lista de um elemento **sem avisar**, e eu transcrevi a
> conclusão dela como se fosse o dado.
>
> É a mesma classe do F-05/N-01 com um intermediário novo: **um resumo não é uma
> observação.** Quando a fonte é máquina, o que vale é o byte que ela devolve, e a única
> prova é o arquivo bruto gravado no acervo.
>
> **O acerto de desenho, e vale registrar porque foi barato:** a guarda escrita em 10/09
> — *"resposta estranha é evidência, não lixo: grave o bruto e acuse no fim"* — fez o
> coletor sobreviver às 74 e trazer a forma real de volta, em vez de morrer na primeira.
> A versão anterior perdia 75 ativos por causa de um.

> **A-03 — o código da emissora muda, e a história não vem junto. 11/09/2026.**
>
> `MBRF` voltou com `tradingName: MARFRIG`, `codeCVM: 20788`, e **as três listas de
> eventos vazias**. Não é falha de rede nem chave errada: o código mudou (`MRFG` → `MBRF`,
> na fusão com a BRF) e o histórico **ficou sob o código antigo**.
>
> Zero numa lista é comum e legítimo — há empresa que nunca desdobrou. **Zero nas três,
> numa empresa do Ibovespa, é quase sempre troca de código.** Das 74 emissoras, só a MBRF
> caiu nesse caso, o que torna a guarda barata e precisa.
>
> É a confirmação concreta do que a pesquisa de 06/09 tinha previsto em abstrato: **o
> mapeamento ticker ↔ CNPJ ↔ CD_CVM também precisa ser bitemporal**, senão o join vaza
> futuro. Aqui ele não vaza futuro — ele **apaga passado**, que é o outro lado da mesma
> moeda. Série de preços sem ajuste de proventos é série inútil.
>
> Note o que salvou: `codeCVM` vem no mesmo objeto. **O CNPJ/CD_CVM é estável quando o
> ticker não é** — é por ele que a ponte para o código antigo se faz.

> **11/09/2026 — cinco rodadas no Claude Code, e o saldo real.**
>
> Fechadas e commitadas: **P-69/Y-01** (`258ca3b`), **P-70** (`9e1aa8a` + `e15d205`),
> **P-71/P-72** (`4f54f31` + `c989ac6`), **campos mortos** (`fb8ce78`), e a esteira
> `--proventos-completos` escrita com testes sem rede.
>
> **A pergunta do Y-01 foi respondida:** a F-03 foi medida **à mão, com 0,25%, fora do
> motor** — está em `politica.yaml → fora_de_escopo.ETF_renda_fixa`. O valor nunca passou
> por `val()`, então a duplicata não a contaminou. Mas abriu a **P-76**: a conclusão foi
> registrada como *"refutada"* e o insumo que a sustenta é `PARCIAL`. Se 0,25% for o
> **teto** do regulamento, a taxa efetiva pode ficar abaixo de 0,20% e **a comparação
> inverte**. *Uma conclusão medida herda o status do insumo mais fraco dela?* — é a P1
> aplicada ao relato de uma medição, e ainda não tem resposta.
>
> **O achado de maior valor não estava em nenhum prompt: P-77.** `retorno_liquido_aa` faz
> `ir = 0.0 if r.isento_ir else ...`, e `isento_ir` resolve por `isento_ir_rendimento` —
> então, para o FII, **o IR de ganho de capital vira zero**. É exatamente o defeito que a
> P-13 foi criada para corrigir, vivo, no código. Hoje não produz número errado **só
> porque o FII está bloqueado por falta de insumo** — o bloqueio está *escondendo* o bug.
> É o F-02 ao contrário: lá a ausência virava zero; aqui a ausência **esconde** um zero
> que já está errado.
>
> **O portão da P-40, instalado em 11/09:** `ruff check .` → **All checks passed**.
> `mypy` **não rodou**: parou nos stubs do numpy com *"Type statement is only supported in
> Python 3.12 and greater"*.
>
> **Isso não é dívida de código — é a P-73 pela terceira vez.** O `pyproject.toml` declara
> `python_version = "3.11"`, a máquina roda **3.13**, e o numpy instalado traz stubs com
> sintaxe de 3.12+. O mypy **nunca vai passar nessa máquina** enquanto a divergência
> existir. Instalar o Python 3.11 deixou de ser preferência de reprodutibilidade e virou
> **requisito operacional**: sem ele, metade do portão está permanentemente desligada.
>
> E nenhum commit fez o bump de versão do `politica.yaml` nem o changelog — passo 9 do
> protocolo, cinco commits seguidos.

> **B-02 — a causa do TOTAL-ZERO não era truncamento. Medida em 11/09/2026.**
>
> A esteira de proventos fechou **71 de 74** emissoras — mais de **8 mil registros**, com
> ITUB em 956, BBDC em 902, ITSA em 506 e PETR em 343. Falharam três: **ABEV, CURY,
> KLBN**, todas com `totalRecords: 0`.
>
> O código supunha **truncamento no campo de 12 posições**. Nenhuma das três estava
> truncada: `AMBEV S/A` tem 9 caracteres, `CURY S/A` tem 8, `KLABIN S/A` tem 10.
>
> **O que elas têm em comum é a barra.** Chamei o endpoint com os nomes sem o sufixo e ele
> respondeu: **`AMBEV` → 134 registros. `KLABIN` → 18.** Com `S/A`, zero. E os nomes com
> `S.A.` **de ponto** — SUZANO, RUMO, VIVARA, IGUATEMI — passaram todos.
>
> **A causa real: os dois endpoints da B3 guardam o nome comercial de formas diferentes.**
> O suplemento devolve `AMBEV S/A`; a tabela de proventos guarda `AMBEV`. Não é bug de
> codificação nosso — é divergência entre duas bases da mesma casa.
>
> **E o teste que importava mais deu a resposta tranquilizadora:** chamei com `ITAU`
> (prefixo de `ITAUUNIBANCO`) e voltou **zero**. Ou seja, **o match é exato, não por
> prefixo nem por conteúdo.** Isso fecha a dúvida que eu tinha e que valia mais que as
> três falhas: **não existe match parcial silencioso.** Ou o nome bate e vem tudo, ou não
> bate e vem zero — e zero é visível. **O acervo das 71 está íntegro**, e `ITAUUNIBANCO`,
> com exatamente 12 caracteres, é o nome real e não um nome cortado.
>
> **Corrigido e commitado (`b02b789`), 13 testes novos.** O coletor tenta o nome como veio
> e, **só depois de um zero**, sem o sufixo societário; a forma usada vai para o manifesto,
> porque **a forma é procedência, não detalhe de implementação** — quem reprocessar precisa
> saber qual nome trouxe o dado.
>
> Dois testes valem por si: um garante que a segunda tentativa **nunca acontece antes** de
> um zero (resposta fora do formato não é culpa do nome, e trocar o nome mascararia o
> defeito); outro garante que zero **nas duas formas** continua sendo `TOTAL-ZERO`, e não
> vira "empresa sem proventos". As duas respostas ficam no acervo como evidência, com a
> forma no nome do arquivo.
>
> E os comentários do código que culpavam o truncamento foram corrigidos. **Uma hipótese
> errada deixada num comentário engana a próxima sessão com a autoridade de um fato.**

> **A suíte deixou de ficar verde nesta máquina — e isso agora é o caminho crítico.**
>
> Enquanto `ruff` e `mypy` não estavam instalados, o `test_p40_lint.py` **pulava** e a
> suíte fechava verde. Instalados em 11/09, o ruff passou em `alocacao/` e em `fase0/`
> (zero), e o **mypy falha em toda rodada** — nos stubs do numpy, que exigem Python 3.12+.
>
> **Não é dívida de código. É a P-73**, e ela mudou de natureza: deixou de ser uma questão
> de reprodutibilidade de backtest e virou operacional. **Uma suíte permanentemente
> vermelha deixa de ser sinal** — em duas semanas ninguém olha mais, e o dia em que um
> teste de verdade quebrar, ele vai entrar no meio do vermelho de sempre.
>
> Instalar o Python 3.11 é o que devolve o verde. Não é preferência.
>
> *(O ruff na raiz acusa 20 erros, **14 deles em `docs/historico/pesquisa-custos-2026-08/calc/`** — a
> cópia congelada de agosto que o §4 marca como armadilha. Corretamente não tocada.)*

> **B-03 — não há regra única, e isso muda a estratégia. Medido em 11/09/2026.**
>
> A correção do B-02 fechou **ABEV (134)** e **KLBN (18)**, exatamente os números previstos.
> **CURY falhou nas duas formas.** Fui atrás e achei:
>
> | emissora | suplemento guarda | tabela de proventos guarda | o que aconteceu |
> |---|---|---|---|
> | ABEV | `AMBEV S/A` | `AMBEV` | sufixo **removido** |
> | KLBN | `KLABIN S/A` | `KLABIN` | sufixo **removido** |
> | **CURY** | `CURY S/A` | **`CURY S.A.`** → **20 registros** | sufixo **reescrito**: barra vira ponto |
>
> **As duas bases da B3 divergem sem regra.** Às vezes o sufixo societário some, às vezes
> ele muda de grafia. Uma normalização determinística — "tire o sufixo" — **não cobre os
> três casos**, e foi exatamente por isso que a correção do B-02, que estava certa, ainda
> deixou uma de fora.
>
> A estratégia certa não é uma regra: é uma **cascata de candidatos** — como veio, sem
> sufixo, sufixo com pontos, sufixo sem pontuação — parando no primeiro que responder, e
> **registrando qual funcionou**. O acervo precisa guardar a forma, não a regra.
>
> **O que NÃO está em risco, e vale dizer:** o match é exato (`ITAU` → 0), então as 73 que
> bateram bateram **exatamente**. Divergência de grafia produz zero, nunca dado parcial.
> **O acervo é íntegro ou visivelmente incompleto — nunca silenciosamente errado.**

> **12/09/2026 — três marcos no mesmo dia, e um deles é inédito.**
>
> **1. O ambiente reproduz o registrado.** `ambiente.py` no Python 3.11.9, com numpy
> 2.4.4, pandas 3.0.2, PyYAML 6.0.3 e pytest 9.1.1: *"O ambiente instalado E o
> registrado."* **Desde que o P-15 foi escrito em 05/09, nenhuma máquina havia rodado o
> que o projeto declara.** A impressão é `7565df1381e2c1ed`.
>
> **2. A suíte fechou verde sem nenhum `s`.** Antes havia dois skips — ruff e mypy
> ausentes. O portão da P-40 **rodou de verdade** e passou. **P-73 fechada.**
>
> **3. O acervo de eventos fechou em 74/74.** A CURY veio pela terceira forma da cascata
> (`CURY S/A` → `CURY` → **`CURY S.A.` → 20 registros**), exatamente como o B-03 previa.
>
> **A Fase 0 mudou de estado: deixou de ser coleta e virou refino.** O desenho está em
> `docs/referencia/DESENHO-PIPELINE.md`, e o achado que o organiza é este: **cada registro de provento
> traz `closingPricePriorExDate`**, o fechamento na véspera do ex. **A série de fatores
> de ajuste pode ser construída inteira sem tocar no COTAHIST** — o preço só entra depois,
> para aplicar. As duas metades do problema se separam, e a metade difícil já está no disco.

> **C-01 — eu errei um número e ele se propagou por três arquivos. 12/09/2026.**
>
> Escrevi, aqui e em dois documentos de fonte, que a PETR *"desdobrou 100:1"* e que *"o
> preço cai 99% num dia"*. O registro traz `factor: "100,00000000000"` com
> `label: DESDOBRAMENTO`.
>
> **`factor` quase certamente é percentual, não multiplicador.** Um desdobramento de 100%
> faz cada ação virar duas e o preço cair **pela metade** — não 99%.
>
> ```
> leitura percentual     fator = 1/(1 + 100/100) = 0,5
> leitura multiplicador  fator = 1/100           = 0,01
> ```
>
> **As duas produzem número, e diferem por cinquenta vezes.** Nenhum teste de "veio
> número?" distingue. Não há documentação da B3 sobre o campo, e o suplemento não traz
> preço de véspera para desempatar.
>
> **`refinar.py` não escolhe.** Grava `ratio` cru e devolve `FACTOR_AMBIGUO`. A
> desambiguação é **medição**: com o COTAHIST, a razão entre o fechamento de 24/04/2008 e
> o de 25/04/2008 responde em uma consulta.
>
> **O que me incomoda mais que o erro:** ele durou seis dias e apareceu em três arquivos
> porque era uma afirmação *plausível* que ninguém precisava medir para repetir. O projeto
> tem doutrina contra número sem procedência **em YAML**; não tinha nada contra número sem
> procedência **em prosa**. Agora tem: achado só entra no `CLAUDE.md` com a conta escrita
> ou com o `NAO_CONFIRMADO` explícito.

> **D-01 — a guarda do segredo mede o arquivo, e o dado sai pela prosa. 12/09/2026.**
>
> A P-62 decidiu que `estado.yaml` não entra no repositório, e o `test_p67_segredo.py`
> garante isso medindo o **índice do git**. Funciona.
>
> **Só que eu escrevi os mesmos números na prosa deste arquivo e do `PENDENCIAS.md`** —
> saldo dos cofrinhos, aporte, reserva — e esses dois **entram**. O repositório é público
> desde 11/09.
>
> É o padrão do projeto contra ele mesmo: um guarda que checa nome de arquivo não vê
> conteúdo, e quem escreveu o guarda escreveu o vazamento na mesma semana.
>
> **Decisão dele, 12/09: `DECISAO_DO_USUARIO` — pode ficar.** *"Não me incomoda."* Fica
> registrado como escolha declarada, não como descuido.
>
> **O que a decisão NÃO cobre:** ela vale para o que existe hoje, com a ordem de grandeza
> de hoje. Se o patrimônio crescer, ou se entrar dado de outra natureza — corretora, conta,
> valor de posição —, **a decisão precisa ser revisitada, não herdada.** Uma escolha feita
> sobre R$8 mil não se estende sozinha a R$800 mil.

> **A-04 — "a história está sob o código antigo" era uma suposição minha, e ela é falsa
> como regra. 12/09/2026.**
>
> O A-03 acima termina com uma frase que eu escrevi sem medir: *"o histórico ficou sob o
> código antigo"*. Fui medir. **Não há regra.**
>
> | código antigo | o endpoint responde? |
> |---|---|
> | `MRFG` (Marfrig) | **vazio** — nem `tradingName`, nem conteúdo |
> | `BRFS` (BRF) | **responde** — `BRF SA`, `codeCVM 16292`, 2 `cashDividends`, 2 `stockDividends` |
>
> Duas empresas da **mesma fusão**, dois comportamentos opostos. E há um detalhe que
> fecha o círculo: entre os `stockDividends` que o `BRFS` devolve está **a própria
> incorporação**. O evento que apagou o código está registrado sob o código que ele
> apagou.
>
> **O que isso corrige na fila:** "buscar pelo código antigo" não é um passo do pipeline
> — é uma tentativa, que às vezes funciona. Um ativo cujo emissor mudou de código tem a
> **lacuna declarada por ativo**, com status, e não uma correção presumida. A P5 na veia:
> limitação declarada vale mais que remendo silencioso.
>
> **O que continua aberto:** a MBRF. A história da Marfrig não está sob `MRFG` nem sob
> `MBRF`. Ou ela vem de outra fonte — CVM, que é por `CD_CVM` e imune a troca de ticker —
> ou o ativo entra com a lacuna escrita.

> **A-05 — o `refinar.py` violava uma regra que o próprio projeto tinha escrito.
> 12/09/2026.**
>
> `docs/fontes/cvm-enumeracoes-observadas.md` diz, com todas as letras: *"um parser que
> encontre valor fora de uma lista OBSERVADO deve falhar ruidosamente — nunca tratar como
> um dos valores conhecidos por padrão, nunca ignorar a linha em silêncio."*
>
> O `refinar.py` aceitava **qualquer** `label` calado. Só apareceu porque o `BRFS` do
> A-04 devolveu um tipo que eu nunca tinha visto: **`INCORPORACAO`**.
>
> **E `INCORPORACAO` não é mais um tipo na lista.** Os outros eventos de quantidade mudam
> o *preço* de um ativo. A incorporação troca ações de uma empresa por ações de **outra**,
> numa relação de troca: é mudança de **identidade** do ativo, não de escala. Tratá-la
> como evento comum **junta duas séries diferentes** e o gráfico fica lindo.
>
> **A correção:** `TIPOS_OBSERVADOS` (caixa, quantidade, direito), `conferir_tipo()` que
> **acumula** o desconhecido, marca a linha com `fator_status = TIPO_DESCONHECIDO`,
> **não descarta** (descartar perderia dado) e **não adivinha** (adivinhar seria o F-02).
> No fim, relatório em voz alta e **código de saída ≠ 0**.
>
> **A regra que fica:** regra escrita num documento de fonte não é regra até existir um
> teste que a meça. O projeto tinha a frase desde 06/09 e o parser que a violava desde
> 12/09 — e os dois conviviam sem se ver.

> **A-06 — a guarda contra duplicação passou um dia inteiro medindo o sintoma errado.
> 12/09/2026. É o pior achado da semana.**
>
> O `refinar.py` importa `desembrulhar` de `coletar_b3` em vez de reimplementá-la, porque
> duas leituras da mesma regra concordam por acidente até o dia em que não concordam
> (N-01). Havia teste para isso, e ele era verde:
>
> ```python
> assert r.desembrulhar is coletar_b3.desembrulhar
> ```
>
> **`desembrulhar` não existia no `coletar_b3.py` de produção.** A lógica estava
> **embutida** dentro de `coletar_eventos`. O nome só existia numa **cópia de teste** que
> eu mesmo escrevi aqui, com o comentário *"réplica local para teste; a versão de produção
> está no repositório dele"* — uma afirmação que eu nunca conferi.
>
> Ou seja: **existiam exatamente as duas implementações que a guarda existia para
> proibir, e a guarda dizia que não.**
>
> O defeito não era o código — era a **medição**. `is` mede se duas variáveis apontam
> para o mesmo objeto. Apontavam. O que ninguém media era se o **coletor usava a própria
> função que exporta**.
>
> **É o padrão recorrente do projeto na sua forma mais cara** — *um arquivo declara um
> comportamento que o código não tem, e os dois concordam por acidente* — com um
> agravante: aqui o arquivo que declarava era **o teste**. Teste verde é a coisa que a
> gente não volta a ler.
>
> **Como teria aparecido sem mim:** na segunda-feira, na primeira execução real. O
> `refinar.py` não falha em silêncio — o `try/except ImportError` levanta `SystemExit`
> com o texto do N-01. O desenho segurou; a **entrega** é que não.
>
> **A correção, e ela é dupla:**
> 1. `desembrulhar(texto) -> (dados, n_registros)` extraída de verdade para o
>    `coletar_b3.py`, com `coletar_eventos` **chamando-a**;
> 2. o teste reescrito para medir a **ausência de duplicata**: lê o código-fonte de
>    `coletar_eventos` e exige que ele chame `desembrulhar` e **não** contenha
>    `json.loads(texto)` nem `isinstance(dados, list)`.
>
> A guarda nova foi **testada contra a mutação**: reintroduzi o desembrulho embutido e ela
> falhou. Guarda que nunca falhou é guarda que ninguém sabe se funciona — foi essa a
> lição inteira.

> **A-07 — a mesma falha era barulhenta numa função e muda na vizinha. 12/09/2026.**
>
> Dois silêncios, achados ao arrumar o A-06:
>
> **1. Mais de um registro para a mesma emissora.** `desembrulhar` já contava quantos
> vinham, e o coletor imprimia o número. O `refinar.py` **descartava a contagem e usava o
> primeiro**. Mais de um registro não é erro — é informação. Mas escolher um deles sem
> dizer é escrever **ausência de critério no lugar de critério**, que é a P6 ao contrário.
> A contagem agora sobe até o relatório final, com o texto que importa: *"o silver usou o
> primeiro; isso não é uma regra, é a ordem em que a B3 devolveu."*
>
> **2. Página que não desembrulha para objeto.** No `linhas_do_suplemento`, esse caso
> devolve **aviso**. No `linhas_do_paginado`, era `continue` **mudo** — a página sumia do
> silver sem deixar rastro. **A mesma condição, o mesmo módulo, duas leituras que
> discordam — e a muda vencia, porque é a que roda oito mil vezes.**
>
> **A pergunta que isso deixa como método:** quando a mesma condição aparece em dois
> lugares do mesmo módulo, elas concordam? Não é uma pergunta de revisão de código — é
> uma pergunta de auditoria, e vale para todo par de funções irmãs do projeto.

> **A auditoria do A-07 — seis achados, quatro medidos. 12/09/2026.**
> *Documento inteiro em `docs/auditoria/AUDITORIA-A07-FUNCOES-IRMAS.md`. Status `PARCIAL`:
> medida sobre o instantâneo de 06/09, não sobre o repositório real. Reconferir.*
>
> **E-01 — o `simular` de um módulo recusa rota bloqueada; o do outro devolve número.**
> `alocacao.simular_custo` levanta `InsumoBloqueado` se `not r.confiavel` (é o F-02
> escrito na docstring). `motor.simular` **não tem a guarda** — e o `motor.Rota` tem a
> propriedade `confiavel` e o `montar_rotas` preenche `bloqueios`. O dado está lá; a
> função não olha. Medido: BOVV11 bloqueada devolve **custo R$1.329,68, empatada com a
> rota que de fato não cobra nada**, e `alertas` vazio — porque a taxa desconhecida vira
> `adm_aa = 0.0` no default do dataclass. **É o K-07/F-02 literal, vivo no módulo irmão.**
> O teste que existia afirma `not bovv.confiavel`: confere que a bandeira está
> levantada, não que alguém a honra. **O A-06 outra vez, em outro arquivo.**
>
> **E-02 — arquivo ausente virou "nada registrado".** `tese.carregar_registros` faz
> `if not os.path.exists(p): return {}, {}`. O irmão `ambiente.declarado` faz o oposto,
> e escreveu a doutrina na própria docstring: *"NÃO tem valores de reserva: se o arquivo
> sumir, é erro, porque sem ele não há nada a conferir."* G7/G8 falham para o lado
> seguro, então o sistema não fica perigoso — fica **mentiroso**: você lê *"nenhuma tese
> registrada para esta rota"* quando o fato é *"o teses.yaml não foi encontrado"*.
> Rodando da pasta errada com vinte teses, você lê a mensagem errada vinte vezes. E
> `teses.yaml` **é** o pré-registro: a P4 existe justamente para que não se confunda
> *"nunca me comprometi"* com *"o registro sumiu"*. Oito carregadores, **três
> tratamentos** para a mesma condição — e os dois que acertam são os dois que
> escreveram a consequência na mensagem. Não é coincidência: quem escreve a
> consequência descobre que precisa levantar.
>
> **E-02 RESOLVIDO em 12/09, e a decisão de desenho é dele.** Perguntei se arquivo
> ausente e arquivo vazio deviam ser a mesma coisa — porque a U-01 manda não quebrar o
> primeiro dia de um usuário. Resposta: **são coisas diferentes.** Ficaram três estados,
> com três mensagens: **ausente** levanta `RegistroAusente`; **vazio** (em branco, `{}`,
> só `meta:`, seções nulas) devolve `({}, {})` e isso é legítimo — é o estado do
> primeiro dia; **ilegível** levanta `RegistroIlegivel`, porque YAML quebrado pode ter
> o registro inteiro dentro, ilegível por um caractere, e chamar isso de "nenhuma tese"
> seria dizer que não há registro quando há.
>
> A U-01 virou **parâmetro**, não padrão: `permitir_ausente=True`. Quem simula um
> usuário novo **pede** a ausência em vez de recebê-la calado e nunca saber a diferença.
> E o caminho do usuário novo nem passa por ali — `alocar()` aceita `teses={}` injetado,
> que é o que o `test_usuario_novo.py` já fazia.
>
> 13 testes, e o que dá nome ao achado é `test_a_diferenca_entre_ausente_e_vazio_e_
> OBSERVAVEL`: antes, os dois devolviam `({}, {})` e eram **indistinguíveis de fora** —
> e era exatamente essa indistinguibilidade o defeito.

> **E-03 — o `politica.yaml` declara nove interruptores e dois não estão ligados em
> nada.** Sete portões leem `g["ativo"]`. `g3_atrito` e `g4_dominancia` **não**. Medido:
> `G3_atrito.ativo = false` barra **os mesmos 5 ativos de 25**. Hoje os nove estão
> `true`, então **arquivo e código concordam por acidente** — a frase do defeito
> recorrente, literal. O custo não é erro: é **conclusão errada sobre o próprio
> sistema**. O dia em que você perguntar *"quanto do resultado vem do atrito?"* — que é
> para isso que o sistema foi feito — a resposta será "nada", e será falsa. Nenhum teste
> pega, porque nada está quebrado. P2 violada em 2 de 9 consumidores.
>
> **E-04 — o `impacto.py` só responde quando você já desconfia.** `quem_le`,
> `leituras_de_yaml`, `quem_usa_campo` são boas ferramentas e todas exigem que você
> **nomeie a chave**. Ninguém ia perguntar por `portoes.G3_atrito.ativo` — justamente
> porque ninguém suspeitava. Faltava a pergunta inversa, que não precisa de suspeita:
> **quais chaves o YAML declara que código nenhum lê?** Agora existe:
> `auditoria/chaves_orfas.py`.
>
> **E-05 — RETIRADO em 12/09, no mesmo dia em que foi escrito. Era falso positivo
> meu, e é o maior erro da auditoria.** Eu escrevi que `liquidez_media_dias: 15` e
> `liquidez_pior_caso_dias: 29` não tinham leitor e que o G2 escolhia a rota da reserva
> sem termo de liquidez. **As três afirmações são falsas.** O `catalogo.yaml` lê a
> chave por `{de_campo: "cofrinho.picpay_garantia_de_limite.liquidez_pior_caso_dias"}`;
> o portão existe (`exige_liquidez_dias`, em `g6_coerencia_funcao`); ele está declarado
> por função (`LIQUIDEZ: 1`, `LASTRO: 5`, `DATADO: 30`); e roda **ordem 1**, antes do
> G1 e do G2, tirando a função da rota lenta — então ela nem chega ao G2. Medido: o
> `picpay_cofrinho` de 29 dias **nunca teve LIQUIDEZ**, declara LASTRO e perde até isso;
> as três rotas da reserva resgatam em **zero dias**.
>
> **A causa raiz, e ela é sobre método:** minha ferramenta varria **só os `.py`**, num
> projeto que põe regra em YAML de propósito e cujo `impacto.py` **já mapeia** as
> arestas YAML→YAML. Auditei metade do sistema e chamei o resultado de conclusão.
> É o A-06 do meu lado da mesa: a ferramenta mediu o lugar errado e o verde dela me
> convenceu. `chaves_orfas.py` agora conta `{de:}/{de_campo:}/{soma:}` como leitura.
>
> **E o que o derrubou não foi eu conferir:** foi ele responder *"portão"* e eu ir
> escrever o código que já existia. Um achado pode sobreviver a uma revisão e morrer
> na primeira tentativa de agir sobre ele.

> **E-06 — o pré-registro declara as próprias guardas e nada as executa.**
> `hml_puro_v1.variantes_permitidas: 1` é o **limite anti-p-hacking**: os graus de
> liberdade que ele se autorizou antes de olhar o resultado. Zero leituras. Nada conta,
> nada compara, nada falha na décima variante. `greenblatt_v1.verificar_monotonicidade:
> true` idem. **Um pré-registro que declara a guarda e não a executa vira documento
> sobre intenções** — a P4 entrega a impressão digital e o compromisso fica em prosa.
>
> **E-06 — as duas medições que mudaram a pergunta. 12/09/2026.**
> *Documento em `docs/auditoria/E06-O-QUE-CONTA-COMO-VARIANTE.md`. Decisão de desenho aberta.*
>
> Antes de contar variantes é preciso saber o que se conta. Fui procurar, no próprio
> pré-registro, um grau de liberdade não declarado. Achei dois candidatos, **e nenhum
> dos dois é o que eu esperava.**
>
> **O filtro de pregões não era p-hacking, e a medição é que diz.** O pré-registro fala
> em 307 meses; a execução registra 306, *"filtro n_dias >= 15"* — e o 15 é um **default
> em Python** (`fatores.premios(minimo_dias=15)`), invisível ao registro. Variando só o
> filtro: **de 5 a 18 o alfa é idêntico ao quinto decimal** (0,00766, t = 2,94), porque
> qualquer corte razoável corta o mesmo mês — o último, de 3 pregões. Hipótese minha,
> medida e **caída**. Registro porque a conclusão importa nos dois sentidos: uma escolha
> não declarada pode ser inofensiva, e a única forma de saber é medir a sensibilidade.
>
> **O grau de liberdade que existe inverte o SINAL, e nenhum contador o pegaria.**
> `alfa_contra_fatores` faz `y = retorno − Risk_Free`, porque foi escrita para
> estratégia long-only. HML é long-short, de custo zero: já é excesso. Subtrair o CDI
> brasileiro (0,938% ao mês na amostra) leva o alfa de **+0,00766 (t = 2,94, rejeita)**
> para **−0,00178 (t = −0,68, não rejeita)**. Mesmo dado, mesma regressão, mesma
> amostra, **veredito invertido** — e não é parâmetro, nem amostra, nem campo do
> registro: é como se monta a variável dependente.
>
> **E o projeto já sabia.** Eu ia publicar isto como achado e parei ao ler em volta:
> `backtest_h1_h3.py` linha 9 avisa em português para não usar aquela função ali; o
> idioma correto (`alfa_contra_fatores(m.HML + m.Risk_Free, m)`) está nos testes;
> `test_h1_h3_reproduzem_o_resultado_registrado` afirma 0,00766 e t = 2,94; e
> `test_subtrair_risk_free_de_um_fator_inverte_o_veredito` **prende a armadilha num
> teste**, com a docstring dizendo que existe para o dia em que alguém "consertar" o
> código. É o projeto no seu melhor.
>
> **A consequência de desenho, e ela governa a decisão:** o grau de liberdade mais
> perigoso do pré-registro **não é contável** por nenhuma definição de variante. O que o
> segura é uma convenção escrita e um teste. Qualquer desenho que trate
> `variantes_permitidas` como defesa principal protege o flanco errado — e por isso a
> recomendação é **rebaixar o contador a alarme**: estourar o limite não bloqueia a
> execução, exige justificativa escrita. **O que protege contra p-hacking não é o número
> de tentativas; é o registro de todas elas.** Um limite de 1 sem registro da tentativa 2
> é mais fraco que um limite de 5 com as cinco escritas.
>
> **E há uma régua de sizing que ele já usa sem ter escrito:** o Greenblatt tem 3 porque
> a especificação publicada é ambígua (`nota_definicao`: implementações honestas divergem
> por um fator de três); o `hml_puro_v1` tem 1 porque é regressão sobre série publicada,
> sem espaço. **O número segue a ambiguidade da fonte.**

> **E-06 decidido por ele em 12/09/2026 — e a decisão corrigiu o meu desenho em três
> pontos.** *Modelo de dados em `docs/auditoria/PRE-REGISTRO-MODELO-DE-DADOS.md`.*
>
> **1. Dado novo, mesma spec = EXTENSÃO**, não variante. A razão dele é de incentivo e
> é decisiva: transformar atualização temporal em variante ensina *"não atualize o
> estudo, isso gasta a sua única bala"* — e é o mesmo defeito que derrubou o D1, onde
> corrigir um erro consumia a mesma bala que uma escolha metodológica.
>
> > **Meu acréscimo:** a extensão não precisa de regra própria se a amostra for
> > registrada como **regra** e não como data — `fim: ULTIMA_DISPONIVEL`. Aí a data
> > literal vira **saída** da execução e não entrada do registro, e toda a tabela de
> > classificação dele (`2001→2005` é variante, novo filtro é variante, novo fim é
> > extensão) passa a ser **consequência do formato** em vez de lista a decorar.
> > Cláusula de exceção é a superfície por onde o contorno entra.
>
> **2. O controle é do CONJUNTO**, com o limite por estratégia como camada auxiliar —
> multiplicidade é problema da família, ambiguidade metodológica é local.
>
> > **E o conjunto tem um NÚMERO, que nem ele nem eu tínhamos.** Se cada estratégia
> > rejeita a t > 1,96, oito testes dão **1 − 0,95⁸ ≈ 34%** de ao menos uma rejeição
> > falsa sob a nula. Medido, com Bonferroni: m=2 (as executadas) → corte **2,253**;
> > m=8 (as pré-registradas) → **2,754**; m=13 (o orçamento inteiro, soma dos
> > `variantes_permitidas`) → **2,913**.
> >
> > **O HML (t = 2,94) sobrevive até o corte mais severo — por 0,027 de um t.** ⚠️
> > **RETIFICADO em 18/09 — ver a seção de 18/09/2026 no fim deste arquivo.** Medido, o
> > `t` estimado **não** se distribui como a tabela de Student: a cauda é ~7% mais gorda,
> > o corte de m=13 sobe de 2,9131 para **3,1473**, e a folga de +0,027 vira um déficit de
> > **−0,212**. O HML **não** sobrevive ao orçamento. Não o
> > invalida; recoloca. "t = 2,94" soa como p ≈ 0,003; corrigido pela família que o
> > próprio projeto pré-registrou, é significância **na margem** — coerente com as
> > quatro razões que o registro já dava para não agir sobre ele. ~~Ressalva contra mim:
> > Bonferroni **superestima** a correção com testes correlacionados, e estes são (mesma
> > série, mesmos cinco fatores). O corte verdadeiro fica entre 1,96 e 2,891.~~
> > **RETIRADA em 18/09: a correlação medida entre as duas estatísticas é −0,064** — o
> > próprio "alfa contra os DEMAIS" já particiona os fatores comuns, e resíduos de
> > regressões que partilham regressores não andam juntos. O corte verdadeiro fica
> > **acima** de 2,913, não abaixo. Eu inferi dependência da origem comum dos dados em
> > vez de medi-la.
>
> > **E `pesquisa_id` não pode ser declarado.** Ele viu o buraco — *"alguém cria
> > Conjunto A, B, C e reseta o contador"* — e fechou com julgamento. Julgamento é
> > contornável por quem está de boa-fé e com pressa, que é o caso perigoso. **Ancorar
> > no dado:** `pesquisa_id` derivado de `hash_fonte()` + regra de amostra, os dois já
> > existentes. Renomear não reseta, porque o nome não é a chave — e `m` passa a ser
> > **calculável** a partir do diário, não afirmado por quem registra.
>
> **3. Erro factual é isento de variante, mas auditável e com fonte primária quando
> material** — e a distinção dele é a que importa: erro de fato **não tem alternativa
> defensável do outro lado**; grau de liberdade tem duas leituras e você escolheu uma. O
> `tratamento_rf` é o caso puro de grau de liberdade disfarçado de correção.
>
> > E ele acrescentou o quarto tipo, que fecha a porta: quando há duas leituras e
> > **nenhuma fonte desempata**, não se declara erro factual — declara-se
> > `NAO_CONFIRMADO` e para. É o C-01 virando regra de processo.
>
> **4. A regra dele que vale mais que as três:** extensão nunca sobrescreve, correção
> nunca apaga, variante nunca apaga a especificação anterior. O sistema vira uma
> sequência de estados auditáveis em vez de uma planilha melhorada até dar o resultado
> desejado — e é a mesma doutrina do *achado retirado fica como retratação*.
>
> > **O que falta nela, e o sistema precisa agir:** se R1 rejeita e R2 (extensão) não,
> > **o que o portão lê?** Sem regra, "preservar tudo" vira "escolha o que preferir" —
> > p-hacking com auditoria completa. Proposta: a extensão mais recente é o **operativo**,
> > e divergência de veredito entre R1 e Rn é **bloqueante** até estar escrita. Um alfa
> > que morre ao estender é o evento mais informativo que este projeto pode produzir;
> > merece uma parada, não uma linha de log.
>
> **E o que este aparato NÃO protege, declarado de propósito (P5):** nada nele teria
> pego o Risk_Free invertido. Especificação congelada, graus de liberdade, diário e
> contador passariam por aquilo sem piscar, porque `tratamento_rf` só entra na lista se
> alguém **souber que ele existe**. O que pegou foi um comentário em português e dois
> testes. **A limitação declarada vale mais que a proteção presumida** — e é por isso que
> o contador é alarme, não defesa.

> **Correção dos meus próprios números do E-06, e ela aperta a margem. 13/09/2026.**
> Calculei os cortes com a **normal**; o certo para 306 meses e 5 parâmetros é a **t de
> Student com 301 gl**, que é um pouco mais alta. Recalculado: m=2 → **2,253**; m=8 →
> **2,754**; m=13 → **2,913**. **A folga do HML cai de 0,049 para 0,027.** O sinal da
> conclusão não muda — ele sobrevive — mas a margem é ainda mais fina do que escrevi.

> **P-77 FECHADA em 13/09/2026 — e a pendência estava descrevendo o sintoma errado.**
> *Documento em `docs/auditoria/P77-CAMPO-MORTO.md`.*
>
> A pendência dizia que *"`retorno_liquido_aa` zera o IR de ganho do FII"*. **Não zera:
> devolve `None`** — o FII é `indexador: rv` e a função sai antes da linha do imposto.
> Procurar pelo sintoma descrito não achava nada, e é por isso que ficou aberta.
>
> **O defeito real:** `aliquota_ganho` tem **zero leituras no motor**. As quatro únicas
> estão em `test_alocacao.py`. A P-13 partiu `isento_ir` em dois campos pela razão certa
> (rendimento isento por Lei 11.033/2004; ganho a 20% por Lei 8.668/1993), criou o
> campo, o catálogo preencheu com a lei citada — **e nenhuma linha consumiu**. Mudança
> de ESQUEMA anunciada como correção de COMPORTAMENTO.
>
> **Três coincidências o esconderam:** o FII é `rv`; o FII está bloqueado; e as únicas
> outras rotas com `aliquota_ganho` são LCI/LCA, **com 0,0**, onde a diferença não
> aparece.
>
> **O número, medido, com a rota que vai existir amanhã:** uma debênture incentivada
> (`isento_ir_rendimento: true`, `aliquota_ganho: 0.20`, `indexador: cdi`) devolvia
> **0,13900** — o imposto inteiro zerado, e **exatamente o número da LCI/LCA**. O motor
> a trataria como isenta nas duas pontas. Errado **para menos**: a rota apareceria mais
> rentável do que é e competiria melhor no G2.
>
> **A correção recusa em vez de chutar.** `regime_tributario()` devolve a alíquota
> quando há uma só, e **um motivo** quando há duas. `retorno_liquido_aa` não inventa um
> modelo de duas pontas — ela modela instrumento que ACUMULA rendimento, onde o ganho é
> o rendimento. P6: lacuna declarada, não critério inventado. E o motivo **não some
> junto com o `None`** — foi um `None` calado que escondeu isto por oito dias.
>
> **A guarda que impede a próxima:** *todo campo que o `catalogo.yaml` preenche tem de
> ser lido por um módulo que não é teste*. Rodada contra o código de antes, ela acusa
> `aliquota_ganho` pelo nome. Teria pegado a P-77 no dia em que nasceu.
>
> **E a lição é sobre o meu instrumento, pela quarta vez no mesmo tema.** O
> `chaves_orfas.py` que escrevi ontem **não** pegou este campo. Fui ver por quê
> esperando um problema de dataclass; era outra coisa: ele varre **todos** os `.py`,
> testes inclusive. **Campo que só o teste toca é campo que o motor não usa** — e é
> categoria pior que órfã pura, porque tem uma testemunha: o teste prova o esquema e
> ninguém prova o comportamento. Foi assim que a P-13 anunciou correção com a suíte
> verde. A ferramenta agora separa leitor do motor de leitor de teste e reporta
> **"LIDA SÓ POR TESTE"** como categoria própria.

> **A terceira vez no mesmo padrão, e agora é regra de método. 12/09/2026.**
>
> Nesta auditoria eu **publiquei** o E-05 (retirado: a chave era lida por outro YAML),
> **quase publiquei** o multiplicador de estabilidade (era leitura por índice variável) e
> **quase publiquei** o Risk_Free acima — com o projeto já tendo um comentário, uma
> convenção e dois testes sobre ele.
>
> Os três têm a mesma forma: **medi, e conclui antes de ler em volta.** Os dois achados
> que sobreviveram — E-01 e E-03 — foram confirmados **lendo**, não medindo.
>
> **A ordem é: medir → ler a vizinhança → concluir.** Numa auditoria a medição levanta o
> candidato; quem o promove a achado é a leitura. Eu vinha fazendo medir → concluir, e
> lendo só quando alguma coisa me obrigava.

> **O falso positivo, e ele ensina mais que dois achados.** A ferramenta acusou
> `G2_reserva.ajuste_estabilidade.{alta,media,baixa}` — o multiplicador da reserva por
> estabilidade de renda. **Falso:** é lido quatro vezes, com índice **variável**
> (`g["ajuste_estabilidade"][estado.estabilidade_renda]`), e por isso o nome da folha
> nunca aparece literal. O que pegou não foi a ferramenta — foi **ler**. Virou regra no
> código (`pais_varridos()`: quem alcança os filhos por variável lê todos os filhos) e
> derrubou 23 candidatos para 19 **sem derrubar nenhum achado**, que é o teste certo de
> um filtro. E virou a razão de os dois scripts imprimirem *"candidatos"*, nunca
> *"achados"*: **P3 aplicada à própria auditoria.**
>
> **Uma convenção que existe e ninguém escreveu.** Sete impressões digitais, dois
> cortes de `sha256` — e não é inconsistência: **arquivo → `[:12]`, conteúdo →
> `[:16]`**, os sete obedecem. Só que a regra não está escrita, então a oitava é
> cara-ou-coroa, e comparar um `[:12]` com um `[:16]` nunca bate, em silêncio.

> **P-76, P-78 e B-04 — fechadas em 13/09/2026, e duas mudaram de forma ao serem
> medidas.** *Documento em `docs/auditoria/P76-P78-B04.md`.*
>
> **P-76 — a doutrina, e ela vale sozinha:** uma conclusão **não herda** o status do
> insumo mais fraco. Ela herda o resultado de uma **medição de sensibilidade** —
> sobrevive a toda a faixa que a incerteza admite → `COMPLETO` com a faixa declarada;
> inverte dentro da faixa → `PARCIAL` com a fronteira declarada; faixa desconhecida →
> `NAO_CONFIRMADO`. Herdar o mais fraco enterraria conclusões robustas junto com as
> frágeis e ensinaria a não medir. **O status de uma conclusão é uma medição, não uma
> herança.**
>
> > **Mas o caso F-03 não é exemplo disso — é vazamento.** `custos.yaml` diz
> > `etf.IMAB11: valor None, status NAO_CONFIRMADO, motivo "taxa nao obtida"`. E a
> > conclusão cita **0,25%**, que existe em **três** documentos (`PENDENCIAS.md:152`,
> > `politica.yaml:859`, `pesquisa-bases-e-apis:293`, decomposto em adm 0,04 +
> > custódia 0,03 + gestão 0,18) **e não existe no arquivo que o código lê**. Quem roda
> > o motor hoje recebe o IMAB11 bloqueado enquanto os documentos dizem que a questão
> > está resolvida. É o C-01 no lugar mais caro.
> >
> > **E medida, a conclusão é frágil:** 0,25% contra 0,20% são **5 pontos-base**, com o
> > lado incerto sendo soma de três componentes de fonte secundária. A F-03 é
> > **`PARCIAL`**, com fronteira declarável: inverte se o IMAB11 ficar abaixo de 0,20%.
> > Não ponho o valor no `custos.yaml` sozinho — é entrada de valor com fonte, e eu não
> > abri a página do gestor; registrar citando documento interno seria citar a mim mesmo.
>
> **P-78 — os oito campos existem (a contagem estava certa), mas são TRÊS naturezas:**
>
> - **procedência, e está certo (2):** `bc_procedentes`/`bc_clientes` são lidos por
>   `test_corretoras.py:90-91`, que **recalcula o índice a partir das partes**. São o
>   insumo que prova o número derivado. **Reclassificar, não consertar.**
> - **ausência de critério declarada, e está certo (3):** `home_broker_web`,
>   `exporta_csv` e os `ra_*` — e `regras()` **levanta `NotImplementedError`** se
>   alguém ligar `facilidade.pontua`. **P6 executada corretamente**, o oposto do E-03:
>   aqui o interruptor falha alto em vez de não fazer nada.
> - **defeito de verdade (3):** `mesa_minimo`, `corretagem_fii`, `exercicio_opcao_pct`
>   — custos por operação que `pontuar()` não considera.
>
> > **E o `corretagem_etf_pct` — o 0,50% da XP — é N-01, não campo ignorado.** ⚠️
> > **RETIFICADO em 13/09, ver o bloco E-08 abaixo:** eu escrevi que o `catalogo.yaml`
> > tinha `corr_pct: 0.005` literal. **Não tem.** Ele faz
> > `corr_pct: {de: "corretagem.xp_etf_pct"}` — referencia, exatamente como o próprio
> > cabeçalho dele manda. O catálogo é o **contraexemplo**, não o culpado. A duplicata
> > está em outro lugar, e são seis, não uma.
>
> **B-04 — a correção é apagar, não construir.** `pip install -e .` falha por
> descoberta automática com vários diretórios de topo. Declarar os pacotes seria a
> correção óbvia e **errada**: ninguém instala este projeto —
> `comando_de_instalacao()` monta `pip install "numpy==..."`, instala as
> **dependências**, e nenhuma linha faz `import bastter`. `[build-system]` era uma
> promessa que o código não usa; o `pyproject.toml` daqui é **manifesto**, lido por
> `ambiente.declarado()` via tomllib, e é disso que a P-15 depende. **Medido antes de
> apagar: a impressão do ambiente é `7565df1381e2c1ed` com e sem a seção** — idêntica à
> registrada, então a remoção não invalida resultado pré-registrado nenhum.
>
> > **E um erro meu, pego rodando duas vezes.** A primeira guarda de idempotência do
> > `B04-patch.py` era `if "[build-system]" not in s: sair` — e a nota que o patch
> > **insere** menciona `[build-system]` em prosa, então a segunda execução casava com
> > o próprio comentário e aplicava de novo. **Guarda de idempotência também precisa
> > ser testada rodando duas vezes.** Agora a marca é do patch, não da string removida.

> **A série histórica do JCP FECHOU — e o fechamento corrige um erro meu. 13/09/2026.**
> *Transcrições em `docs/fontes/lei-9249-1995-jcp-planalto.md`, todas do Planalto.*
>
> | de | até | alíquota | norma |
> |---|---|---|---|
> | 01/01/1996 | 31/12/2015 | **15%** | Lei 9.249/1995 art. 9º §2º, redação original |
> | **01/01/2016** | **08/03/2016** | **18%** | MP 694/2015 art. 1º, efeitos por art. 4º, I; encerrada pelo Ato Declaratório nº 5/2016 |
> | 09/03/2016 | 31/12/2025 | **15%** | redação original restabelecida |
> | 01/01/2026 | — | **17,5%** | LC 224/2025 art. 8º, vigência pelo art. 14, **III** |
>
> **A janela do meio tem 68 dias** — 31 de janeiro + 29 de fevereiro (bissexto) + 8 de
> março. Todo JCP pago nela sofreu 18%, e **o imposto permanece devido**: a CF art. 62
> §11 mantém as relações regidas pela MP quando o Congresso não edita decreto
> legislativo, e não editou. **Caducar não devolve imposto pago.**
>
> **A CORREÇÃO, e ela é contra mim.** Em 12/09 escrevi aqui que a LC 224 vigora em
> **01/04/2026** pelo art. 14, I, "b", e que a fonte secundária que dizia 01/01/2026
> estava contradita pelo Planalto — *"fonte primária ganha"*. **Estava errado, e a
> secundária estava certa.** A alínea "b" cobre **os arts. 7º e 9º**; o art. 8º — o do
> JCP — cai no **inciso III**, *"a partir de 1º de janeiro de 2026"*.
>
> > **O erro não foi de fonte, foi de ENDEREÇAMENTO:** li a cláusula certa e a apliquei
> > ao artigo errado. Ler um artigo de vigência sem checar **qual item ele nomeia** é
> > ler metade dele. E é pior que não ter consultado: usei a autoridade da fonte
> > primária para descartar uma secundária correta, **com confiança**.
> >
> > **Regra que fica: "fonte primária ganha" não é passe livre.** Ela ganha depois de
> > se verificar qual dispositivo a cláusula alcança. Procedência é sobre **verificar**,
> > não sobre hierarquia.
>
> **E a mesma fonte secundária errava a primeira faixa ao contrário** — dizia 18% até
> 2015 e 15% pela MP 694, quando a original é 15% e a MP **subiu** para 18%. Duas
> fontes secundárias, dois erros em direções opostas, e num deles ela estava certa.
>
> **MP 1.303/2025 não entra:** o Planalto não a lista entre as que deram redação ao
> §2º, e ela caducou em outubro/2025 (retirada de pauta na Câmara) antes de produzir
> efeito.
>
> **O que foi entregue:** `tributacao.ir_jcp_fonte` no `custos.yaml` com as quatro
> vigências e a norma ao lado de cada número; `alocacao/jcp.py` com `aliquota_jcp(data,
> C)` e `jcp_liquido()`; **16 testes**, e os que importam são os de **fronteira** — no
> meio de uma faixa qualquer implementação acerta.
>
> **Uma coisa declarada de propósito (lição da P-77):** `jcp.py` **não tem chamador no
> motor hoje**, porque a série de retorno total líquida ainda não existe. Isso está
> escrito no topo do módulo, junto com a consequência: **se a série líquida nascer sem
> chamar esta função, é defeito.**
>
> **E um erro que o próprio teste pegou:** eu tinha escrito "67 dias" — 2016 é
> bissexto, e são **68**.

> **E-08 — o `bloqueia` que nomeia o consumidor, e o consumidor que não pergunta.
> 13/09/2026.** *Testes em `alocacao/test_e08_bloqueio_e_copia.py`.*
>
> **Primeiro a retratação, porque ela vem antes do achado.** Em `P76-P78-B04.md` e aqui
> eu escrevi que o `catalogo.yaml` carregava `corr_pct: 0.005` literal, duplicando a
> constante. **Fui ler o arquivo e ele faz o contrário:**
>
> ```yaml
> bova11_xp:
>   corr_pct:    {de: "corretagem.xp_etf_pct"}
>   saida_extra: {de: "corretagem.xp_etf_pct"}
> ```
>
> Referencia, duas vezes, e por isso herda status, procedência e `expira` de graça. **O
> catálogo é o contraexemplo do defeito, não o defeito.** Foi a sexta vez nesta semana
> que concluí antes de ler o arquivo — e a segunda que a conclusão chegou a ser
> publicada.
>
> **O achado de verdade, medido:** `custos.yaml -> corretagem.xp_swing` é `PARCIAL` e
> declara **`bloqueia: ["ranking_corretoras"]`** — nomeia **este** consumidor, não um
> genérico. E o ranking **roda**: `pontuar()` devolve **46,0** para a XP, com
> multiplicador **0,8**. Porque `pontuar()` lê `inst.corretagem_rv` do
> `instituicoes.yaml` e **nunca chama `val()`** — então a consequência declarada não
> chega até ele.
>
> A mesma incerteza, sobre o mesmo número, tratada de dois jeitos: **bloqueio duro** no
> `custos.yaml`, **multiplicador 0,8** no `instituicoes.yaml`. E o macio vence, porque é
> o do caminho que executa.
>
> > **E o ponto não é que alguém escolheu o multiplicador: é que ninguém escolheu.** Os
> > dois mecanismos são deliberados, moram em arquivos diferentes e não se conhecem —
> > **o layout dos arquivos decidiu qual vence.** É o F-05 pela metade: `bloqueia`
> > deixou de ser prosa para quem passa por `val()`; para quem não passa, continua prosa.
>
> **E-08b — a cópia não herda o relógio, e são SEIS.** Medindo o mesmo fato nos dois
> arquivos (e descartando as quatro coincidências de valor — `exercicio_opcao_pct:
> 0.005` bate com `xp_etf_pct` por acaso, 0,5% é taxa comum):
>
> | `instituicoes.yaml` | `custos.yaml` |
> |---|---|
> | `xp.corretagem_rv` 4,9 | `corretagem.xp_swing` (PARCIAL) |
> | `xp.corretagem_etf_pct` 0,005 | `corretagem.xp_etf_pct` (COMPLETO) |
> | `caixa.corretagem_rv` 4,49 | `corretagem.caixa_fixa` |
> | `caixa.corretagem_pct` 0,0002 | `corretagem.caixa_pct` |
> | `safra.corretagem_rv` 4,5 | `corretagem.safra_terra` |
> | `terra.corretagem_rv` 4,5 | `corretagem.safra_terra` |
>
> **As cinco constantes têm `expira: 2026-12-04`. As seis cópias não têm campo de
> validade nenhum.** Em 05/12/2026 o `val()` começa a avisar para quem **referencia** — e
> as cópias continuam caladas, para sempre. **O projeto construiu um relógio e metade
> dos números não está ligada nele.**
>
> Note também que o `xp_etf_pct` é `COMPLETO` no `custos.yaml` e o bloco que o copia
> declara `PARCIAL`: **o mesmo número com dois status.**
>
> **A causa raiz não é de quem escreveu o número:** o `instituicoes.yaml` **não tem
> resolvedor de referência**. O `catalogo.yaml` tem `{de:}` e por isso acerta. Enquanto
> o formato não oferecer a alternativa, copiar é a única coisa que se pode fazer.
>
> **14 testes**, 7 verdes e **7 `xfail(strict=True)`** — os sete medem defeito aberto, e
> o `strict` obriga a tirar o marcador no dia do conserto.

> **E-08 FECHADO em 13/09/2026 — o `instituicoes.yaml` ganhou resolvedor de
> referência.** *Decisão dele: resolvedor, não remoção. Documento em
> `docs/auditoria/E08-RESOLVEDOR.md`.*
>
> `{de: "corretagem.xp_etf_pct"}` passa a valer em qualquer campo de custo, e a
> resolução **passa por `val()`** — é isso que faz status, procedência, `expira` e
> `bloqueia` caírem de graça. As seis cópias viraram referência.
>
> **Três regras, e cada uma responde a um erro anterior:** constante `COMPLETO` devolve
> o valor; constante que **bloqueia o contexto declarado** devolve `None` com o motivo;
> `NAO_CONFIRMADO` devolve `None` sempre. **O contexto é opcional de propósito** — *um
> consumidor que não se nomeia não pode reivindicar um bloqueio dirigido a outro*.
>
> E o `None` **não é um buraco**: é o valor que `pontuar()` já sabia tratar, marcando a
> dimensão como não avaliada e deixando a `cobertura` penalizar. *"Dimensão ausente é
> penalidade, não neutralidade"* já estava escrito lá dentro. **O resolvedor não
> inventou tratamento nenhum — fez o dado chegar ao tratamento que existia.**
>
> O ranking passou a **se nomear**: `catalogo_instituicoes(contexto=RANKING)`. Uma
> linha, e é ela que transforma a frase do YAML em comportamento.
>
> **Medido — e o número engana:**
>
> ```
> XP antes:   total 46,0   corretagem = 2,0     multiplicador 0,80
> XP depois:  total 45,9   corretagem = None    "corretagem NÃO CONFIRMADA"
> ```
>
> > **A nota praticamente não mudou** — perder a dimensão tira um peso de 12 que valia
> > 2,0, e os efeitos quase se cancelam. **E isso não torna a correção menor.** O que
> > mudou não foi *quanto*, foi **o que o sistema afirma**: antes ele dizia *"a
> > corretagem da XP é ruim, nota 2,0"*, uma asserção sobre um número que o próprio
> > projeto declarava não conseguir ler; agora diz *"não sei ler, e isso custa
> > cobertura"*. **Uma correção de honestidade pode não mexer no resultado e continuar
> > sendo correção.** Chamar isso de "sem impacto" seria medir a coisa errada.
>
> **Prova de inércia:** os conjuntos de falha da suíte são **idênticos** com e sem o
> patch — 12 nos dois, nenhuma nova, nenhuma sumiu (as 12 são P-15 e P-40 do meu
> ambiente). `test_corretoras.py` segue com 26 verdes. As seis referências, sem
> contexto, devolvem exatamente os valores de antes.
>
> **17 testes novos, zero `xfail`** — os sete que documentavam defeito aberto agora
> medem o conserto. O melhor deles **adianta o relógio** (`motor.HOJE = 2027-01-01`) e
> confirma que o aviso de expiração passou a sair também para o `instituicoes.yaml`.
> **O relógio existia; faltava ligar o outro lado nele.**

> **E-09 — a chave duplicada que apagou oito dias de trabalho. 13/09/2026, e é o
> achado mais silencioso do projeto.** *Documento em `docs/auditoria/F03-IMAB11-E09.md`.*
>
> `custos.yaml -> etf:` tinha **`IMAB11:` duas vezes**: a de cima (05/09) com
> `valor: 0.0025, status: PARCIAL` e a página do gestor como fonte; a de baixo, oitenta
> linhas abaixo, com `valor: null, NAO_CONFIRMADO`. **PyYAML fica com a última, sem
> aviso nenhum.** O `PENDENCIAS.md` dizia *"fechada 05/09 — 0,25%"*, o motor via
> `NAO_CONFIRMADO`, e **os dois discordaram em silêncio por oito dias**.
>
> **E eu errei sobre isto ontem:** escrevi que *"a taxa nunca entrou no arquivo que o
> código lê"*. Entrou. Medi `C['etf']['IMAB11']` — o valor **carregado** — e concluí
> sobre o **arquivo**. É a décima linha da régua §5-B.
>
> **A guarda é da classe:** `auditoria/chaves_duplicadas.py`, um `SafeLoader` que
> **recusa** duplicata em vez de escolher. Varrido sobre os sete YAMLs: **exatamente
> uma no projeto inteiro**, e era a que importava. 10 testes, com prova por mutação — e
> o teste mostra que o `yaml.safe_load` padrão **não reclama** da duplicata sintética.
>
> > **E a ferramenta errou antes de acertar, na mesma manhã em que escrevi a régua.** A
> > primeira versão reprovava o `catalogo.yaml` inteiro, porque ele usa âncora e merge
> > (`<<: *base`) e meu loader não construía a tag. **Sobrescrever chave da âncora é o
> > propósito do merge.** Alcance do instrumento menor que o sistema, outra vez.

> **F-03 e P-05 FECHADAS — ele mandou a lâmina do gestor. 13/09/2026.**
>
> Lâmina It Now ID ETF IMA-B, Itaú Asset, **31/08/2026**: administração **0,04%** +
> custódia **0,03%** + gestão **0,18%** = **0,25% a.a.**, e a linha *"taxa cobrada"* é
> **igual** à *"taxa máxima"* nas três colunas — o que responde exatamente a dúvida
> registrada (*"é teto de regulamento ou taxa efetiva?"*) sem precisar do regulamento.
>
> **A P-05 estava certa ao dizer que a pendência era mal formulada:** não era número
> ausente, era **campo errado**. "Taxa de administração" é um componente, e aqui é o
> **menor dos três** — comparar por `taxa_adm` subestimaria em **seis vezes**.
>
> **F-03 remedida, e a conclusão ficou mais forte:** incluindo a custódia de RV da B3
> que o ETF paga acima de R$26.471,77 e o Tesouro não, o Tesouro IPCA+ vence em **todas**
> as faixas, e a margem **abre** de +0,05 pp (R$5 mil) para **+0,09 pp** (R$100 mil).
> Pela régua da P-76, isso é `COMPLETO` com a faixa declarada — **a fragilidade que eu
> apontei era do insumo, não da conclusão.**

> **A evidência sobre pré-registro — e ela contraria a MINHA recomendação. 13/09/2026.**
> *Documentos em `docs/auditoria/PREREGISTRO-EVIDENCIA.md` e o relatório completo, 25 fontes.*
>
> Ele confirmou o desenho e pediu evidência. A evidência apoia duas camadas, é ambígua
> numa e **contraria a quarta — o contador como alarme, que fui eu quem recomendou.**
>
> - **Lerner & Tetlock (1999):** *accountability* **piora** o julgamento quando a escolha
>   envolve *"options easiest to justify"* — e "rodar mais uma variante" é sempre a mais
>   fácil de justificar. Pior: audiência de visões **conhecidas** (ele mesmo) produz
>   **conformidade**, não autocrítica. **A justificativa escrita pode virar máquina de
>   licenças.**
> - **Sharon et al. (2022)**, meta-análise: em tarefas **complexas**, *accountability* de
>   **resultado** é superior à de processo — **d ≈ −0,48**. Backtest de 8 estratégias é
>   tarefa configural por qualquer definição.
> - **E a trava mais dura que existe — a revisão Stage 1 dos Registered Reports — é a
>   que tem os maiores efeitos medidos:** 43,7% de hipóteses apoiadas contra 96,1% da
>   literatura padrão.
> - **Brodeur et al. (2024)**, 15.992 estatísticas: *"no evidence that pre-registration
>   in itself reduces p-hacking"*. **O que funciona é o plano de análise detalhado**, não
>   o ato de registrar.
>
> **O problema estrutural:** todo benefício demonstrado vem de arranjos com **verificador
> externo**. Auto-registro sem leitor é o caso em que os estudos não acham efeito.
>
> > **Mas ele tem um verificador e talvez não tenha percebido: o repositório é público,
> > com commits datados.** Um pré-registro commitado antes da execução, num histórico que
> > não se reescreve sem rastro, é muito mais perto do `clinicaltrials.gov` do que de uma
> > anotação privada. **Regra concreta que sai daí:** o commit da especificação precisa
> > ser anterior ao commit do resultado, e isso é verificável por qualquer pessoa.
>
> **Recomendação revista: trava, com uma saída nomeada.** Exceder o orçado não se
> resolve com um parágrafo — cria-se um **`v2`**, com especificação e `m` próprios, e o
> `v1` fica de pé com o resultado dele. O custo de exceder deixa de ser escrever e passa
> a ser **admitir que é outro experimento**. E entra uma **camada zero**: o plano de
> análise detalhado, que é o que Brodeur mede como sendo o que funciona — hoje só o
> `hml_puro_v1` o tem de fato.

---

## C-03 · Quatro moedas no COTAHIST, e só uma deixou quebra no arquivo

**19/09/2026.** Documento completo em `docs/auditoria/C03-A-QUEBRA-DE-MOEDA.md`.

O acervo passou de 1 para 41 anos e a série começa em 02/01/1986, atravessando seis planos
econômicos. O campo **`MODREF`** (posições 53–56, *moeda de referência* — o nome certo,
conferido no leiaute rev. 02) muda **dentro do mesmo arquivo anual**.

**Medido** — razão `PREULT(depois)/PREULT(antes)` do **mesmo `CODNEG`**, mercado à vista,
com o controle do dia anterior ao lado:

| troca | pares | mediana | |
|---|---|---|---|
| 1986 Cruzado (1.000:1) | 274 | 1,197 | **sem quebra** |
| 1989 Verão (1.000:1) | 198 | 0,968 | **sem quebra** |
| 1993 Cruzeiro Real (1.000:1) | 182 | 0,998 | **sem quebra** — e o `MODREF` nem distingue as duas |
| 1990 Collor | **2** | — | `NAO_CONFIRMADO`: o mercado parou |
| **1994 Real (CR$ 2.750 = R$ 1)** | 136 | **0,364** | **QUEBRA**, contra controle de 1,011 |

**Três das quatro trocas não deixam quebra.** A suposição natural — *"toda troca de moeda é
uma quebra"* — erra em 3 de 4. **Uma tabela de planos econômicos teria acusado quatro e
acertado uma:** o fator é medição, nunca tabela.

**A peça que explica**, e ela está no header do próprio arquivo: os COTAHIST de 1986 a 1995
foram **todos gerados em 19991210**, o mesmo dia, treze anos depois do primeiro pregão e
cinco depois do Plano Real. 2001 em 20060331; 2023 em 20231228.

> **`MODREF` é rótulo histórico, não a unidade em que o número está gravado.** A B3
> reexpressou a série pré-Real numa base única ao regerá-la em 1999, e deixou a fronteira
> do Real como está. `NAO_CONFIRMADO` — é a leitura que reconcilia cinco medições com a
> data de geração, não um documento da B3.

**Por que é caro:** troca de moeda **não é evento societário** — não tem `factor`, não tem
data-ex, não existe no silver. A quebra de 04/07/1994 entra na série ajustada como
**−63,6% no mercado inteiro, em um dia, sem causa.**

É o **F-02 na forma mais cara que ele já tomou**: não é insumo ausente virando zero, é
insumo **presente, correto e anunciado pela própria fonte** que ninguém lê. E é o **C-01 em
escala de mercado** — lá um `factor` mal lido movia um papel por até 50x; aqui um rótulo mal
lido move **todos** por 2,75x, e o gráfico fica plausível.

> **O perigo simétrico, e é o que fecha o achado:** um leitor que confie em `MODREF` para
> converter aplica **três conversões falsas** e erra a única verdadeira em direção nenhuma.
> *Campo que parece dizer o fator e não diz* — exatamente o `factor` do C-01, em outra roupa.

---

## P-99 · O COTAHIST muda de convenção de nome dentro da série, e o leitor devolvia zero calado

**19/09/2026.** Testes em `fase0/test_calendario_p99.py` (24).

`registros()` achava o membro do ZIP filtrando `n.upper().endswith(".TXT")`. Mas:

| faixa | nome do membro dentro do ZIP |
|---|---|
| 1986–2000 | `COTAHIST.A1986` — **ponto**, sem extensão |
| 2001 | `COTAHIST_A2001` — **sublinhado**, sem extensão |
| 2002–2025 | `COTAHIST_A2023.TXT` |

**Medido nos 9 arquivos em mãos: 7 devolviam ZERO registros, sem erro e sem aviso.** O ano
não quebrava — ele não existia. A série passaria a começar em 2002 sem ninguém ter decidido
isso, e nenhum teste de *"veio número?"* pega isso.

**Dois irmãos do mesmo defeito, e o segundo é pior:**

- `arquivos()` usava `os.path.splitext`, e `splitext("COTAHIST.A1986")` devolve
  `('COTAHIST', '.A1986')` — o TXT extraído nem era reconhecido, e se fosse, **quinze anos
  (1986–2000) disputariam a chave `COTAHIST`** no mesmo dict.
- `pregoes()` **morria inteiro** num `BadZipFile`. O `COTAHIST_A2026.ZIP` chegou truncado em
  18/09, e **um arquivo ruim apagava o calendário do acervo todo.**

**A correção NÃO é uma lista de nomes** — seria a P-82/P-98 pela terceira vez em três dias
(*regra escrita numa lista de nomes não é regra, é lembrete*). A regra é: **um membro só, e
ele tem de começar com um header de COTAHIST.** *Nome é a propriedade que varia; leiaute é a
que identifica.*

E o arquivo ilegível agora é **acusado por nome** em stderr, com o ano faltando declarado —
o desenho do `coletar_b3.py` de 10/09 (*"resposta estranha é evidência, não lixo"*), que
salvou as 74 emissoras e **não tinha atravessado de módulo para módulo**. A-07/P-85 outra vez.

**Instantâneo dourado (passo 3 do protocolo §9):** `pregoes()` sobre 2023, antes e depois —
**248 pregões**, `sha256 e4a9d81d3d6d4cb8810b86322de3d08415f7a3fed23b32d923b4291c13bd551c`,
**idêntico** ao registrado em 18/09. Entraram 17 anos sem mover um bit do que já funcionava.

> **A tolerância tem armadilha própria, e ela está num teste.** Aceitar arquivo sem header
> (ZIP sintético de teste) exige `next()`, que **consome** a linha — e devolvê-la é
> obrigatório, senão o arquivo perde o primeiro pregão em silêncio: o próprio defeito da
> P-99 reintroduzido pela correção dele. O teste conta **duas** linhas, não uma.

---

## P-102 · Uma guarda acessória derrubou o trabalho que ela existe para proteger

**18/09/2026.** Testes em `fase0/test_p7_captura_declarada.py`.

Liguei `acervos_sem_regime()` ao `main()` do `manifesto_cvm.py` sem guarda. Em `tmp_path` o
`raiz_do_repositorio` acha o `pyproject.toml` que o próprio teste cria, a política não existe
ali, e o `FileNotFoundError` subiu — derrubando **três testes que não tinham nada a ver com
P7 nenhuma**. Foram commitados e **empurrados vermelhos, no primeiro push da história do
repositório** (`3ee5e97`).

**Dois erros, e o segundo vale mais:**

1. **rodei só o teste novo, não a suíte de `fase0`** — passo 5 do protocolo §9, *"pytest, o
   júri, nunca o guia"*, pulado na mesma resposta em que eu citei o protocolo;
2. **uma guarda acessória matou o trabalho principal.** O comando grava o retrato de
   procedência; conferir a P7 é um extra pendurado nele. Num instrumento cuja única função é
   não perder procedência, **cair é a pior saída possível** — e veio da coisa escrita para
   proteger.

**A correção fica entre dois extremos:** `PoliticaAusente` **levanta** na função (engolir
seria o **E-02** — arquivo ausente virando *"nada declarado"*), e o `main()` **avisa que a
conferência não rodou** e deixa o retrato de pé.

> ***"Conferi e está certo"* e *"não consegui conferir"* não podem ter a mesma saída.**

---

## P-98 · O `.gitignore` cobria por extensão, e 507 MB não tinham extensão

**18/09/2026.** Guarda em `alocacao/test_p98_acervo_fora_do_indice.py` (5 testes).

O acervo COTAHIST (5,6 GB) foi baixado para dentro de `docs/fontes/`. O `.gitignore` cobria
`docs/fontes/**/*.zip` e `**/*.txt` — 65 dos 81 arquivos. **Os 16 de 1986–2001 não têm
extensão**, e eram **507 MB** a um `git add -A` de virarem história permanente num
repositório público. Blob commitado não sai com `git rm`.

**É a P-82 pela segunda vez em dois dias.** Lá a lista era de **pastas** e `pacote_segunda/`
não estava nela. Aqui é de **extensões**, e estendê-la exigiria saber de antemão como um
publicador nomeia o conteúdo de um ZIP de 1986. Ninguém sabe.

A guarda mede **tamanho no índice do git**, não nome: *bytes não dependem de alguém ter
acertado a extensão*. Mesmo instrumento do `test_p67_segredo` (segredo) e do
`test_p82_copia_do_projeto` (cópia) — **os três medem o índice, porque o defeito nasce no
`git add`, não no disco.**

---

## Retratação · "não existe automação deste download" — regra §5-B.13

**18/09/2026.** A retratação formal está em `politica.yaml →
limitacoes_declaradas.captura_do_cotahist_passa_por_captcha` (marcada `RETIRADA`) e no topo
de `docs/fontes/b3-series-historicas-cotahist.md`. A regra de método está na régua §5-B como
**linha 13**.

Declarei impossível um download que era um `GET` aberto
(`bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_A<ANO>.ZIP`), porque o formulário de
séries anuais tem CAPTCHA. Ele baixou os 41 anos com um laço de `Invoke-WebRequest`.

Medi *"existe um CAPTCHA no formulário"*; concluí *"não existe caminho até este arquivo sem
CAPTCHA"* — uma afirmação sobre **todos** os caminhos, a partir de **um**. E o agravante:
escrevi que **não leria** o JS da página porque saber o endereço *"é a única peça que
faltaria para passar por cima do portão"*, e depois usei o fato de não ter olhado como razão
para afirmar que não havia o que ver.

> **Princípio no lugar de medição é a forma mais difícil de detectar deste defeito, porque a
> frase soa como rigor.** Conclusão mal medida se derruba medindo; **recusa apresentada como
> conclusão fecha a porta da própria verificação.**

**A regra:** *"não dá para fazer X"* só se escreve **depois de tentar X e falhar, com o erro
transcrito**. Sem isso, escreve-se **"não sei se dá"** — e mede-se. Vale em dobro quando o
destino é `limitacoes_declaradas`, a seção em que o leitor confia por construção.

**O custo real não foi a frase:** foi **não entregar o script que era possível**. Ele
escreveu sozinho o que eu devia ter entregado. É a **U-01/P7 pela quarta vez** — pôr o
Osvaldo no caminho crítico de algo que é do sistema, aqui com cinco CAPTCHAs manuais que
não existiam.

---

## P-06 · FECHADA — o leiaute do COTAHIST tem URL, e não há revisão 03

**19/09/2026.** Fonte em `docs/fontes/b3-cotahist-leiaute.md`.

`https://www.b3.com.br/data/files/33/67/B9/50/D84057102C784E47AC094EA8/SeriesHistoricas_Layout.pdf`
— **revisão 02, de 05/10/2020**, a mesma que o projeto já transcrevia. A pergunta da P-06
era *"existe revisão 03?"*. **Não existe.**

**E é a §5-B.13 dois dias seguidos, com o mesmo arquivo.** Eu escrevi que *"a página onde
ela deveria estar não a tem"*. O leiaute está numa **terceira** página — *Cotações
Históricas*, não *Séries Históricas*, duas irmãs de nome quase igual. Uma busca resolveu:
**a conclusão saiu mais larga que a medição, e a diferença era um passo de procura que eu
não dei.**

Três correções que vêm junto:

- **O campo 53–56 chama-se `MODREF`**, *moeda de referência*, não `MOEDA`. Nome errado em
  campo de posição fixa é barato hoje e caro no dia em que alguém procurar no leiaute.
- **O leiaute não traz tabela de valores para `MODREF`.** Não é tabela incompleta (como o
  `ESPECI` da P-95) — é tabela **inexistente**. A enumeração tem de sair do dado observado,
  com falha ruidosa fora dela (A-05).
- **A B3 declara, em texto:** *"As cotações são fornecidas na moeda e forma de cotação da
  época, **sem nenhum ajuste para a inflação ou proventos**."* Ajuste de proventos é nosso, e
  agora está escrito na fonte em vez de presumido.

---

## C-02 na janela · O critério do degrau esperava zero, e o dia ex ajustado tem o retorno do mercado

**21/09/2026.** Documento completo em `docs/auditoria/C02-JANELA-2021-2025.md`.

O critério do C-02 para 2023 foi aplicado a cada ano de 2021–2025 como critério **declarado
pré-registrado, sem impressão digital** — escrito antes da primeira corrida, mas commitado junto
com os resultados (`b54787b`), então a P4 não o verifica (P-116). Reprovou em quatro dos cinco. Fica em `xfail(strict=True)`, por decisão
dele, com a causa medida no motivo. As causas são pós-hoc, e nenhuma é o ajuste errando:
evento de quantidade dentro da média (grupamento de 15:1 = +1378% no bruto — **erro meu no
desenho do critério**), bonificação ausente do silver (A-11), evento sem fator no mesmo dia.

**E embaixo, o que o critério escondia:** o dia ex ajustado não tem retorno zero, tem o do
mercado — e 2023 passou em 18/09 porque o mercado subiu, em média, nos dias ex daquele ano.
Descontada a mediana do dia, o resíduo de 2023 é −0,21% (t −1,89). E o preço **não cai o
provento**: queda ÷ provento = **1,164** no dividendo (IC 95% [1,09; 1,24], n = 400) e
**0,951** no JCP ([0,86; 1,04], n = 819). O número é medido; o mecanismo (dividendo isento
× ganho de capital a 15% → 1,18) é hipótese, `NAO_CONFIRMADO`.

**A regra:** um critério de "o ajuste está certo" não pode ter como nulo *"o retorno ajustado
é zero"* — ele confunde o ajuste com o mercado e com a razão de queda. É a forma da §5-B:
a medição de 18/09 estava certa; a pergunta que ela respondeu era mais estreita que a
conclusão. **Guarda:** `test_POSHOC_*` em `fase0/test_ajustar_janela.py`, rotulados como
pós-hoc — guarda de número publicado, não prova.

## A-10 · A janela larga casava pior que a estreita

**21/09/2026.** Com cinco anos, o **BPAC13** — UNT que só negociou em 2021 — passou a
disputar o par `(BPAC, UNT)` com o BPAC11, e 16 JCPs que o 2023 isolado aplicava viraram
`AMBIGUO`. Quem pegou foi o instantâneo da medição (os degraus de 2023 dentro da janela têm
de ser os de 18/09). **Regra:** ambiguidade de par se desfaz por **vigência observada** — o
candidato cuja série alcança a data ex —, nunca por nome ou ordem. Com os dois vigentes, a
ambiguidade continua de pé. `ajustar.vigente()`; 16 → 0.

## A-11 · O COTAHIST declara bonificação que o silver não tem

**21/09/2026.** O ESPECI do dia ex marca `EDB`/`EJB` em **11 papéis-dia (6 datas)** em que o
silver só traz o provento — CMIG3/4 em 2021 e 2022 (−27% ajustados em 02/05/2022), ITSA3/4
de 2022 a 2024, PSSA3 em 2021. **Nenhum em 2025**: é a janela recente do
`GetListedSupplementCompany`, já declarada, vista de dentro do arquivo de preço e com o custo
medido. **Regra:** a marca de ex do COTAHIST é **testemunha**, não insumo — separa os dias que
medem o acervo dos que medem o ajuste, e não vira fator (a tabela ESPECI está incompleta,
P-95). Fechar a lacuna é a P-112.

## A-12 · A identidade de um evento era montada com um campo derivado, e 128 eventos viraram um

**23/09/2026.** Ele chegou disfarçado de número que mudou. Ao fechar a P-114 o silver foi
regerado com o calendário dos 41 anos, e o `ajustar.py` passou a colapsar **206** duplicatas
onde a corrida de 21/09 colapsava **334**.

> **Calendário não cria nem destrói evento.** Um número que cai 128 unidades ao trocar o
> calendário diz que um dos dois estava errado — e diz isso sem que ninguém tivesse
> perguntado nada sobre duplicatas.

Estava o de cima. `_chave_de_evento` incluía `data_ex`, que o projeto **deriva** — e que no
silver de 11/09 estava **vazio em 8.889 das 9.272 linhas**, porque o calendário só cobria
2023. Duas linhas que diferiam apenas pela data colidiam na chave, e a colisão não aparecia
como colisão: aparecia como *duplicata exata*, rótulo que o relatório imprime sem levantar
suspeita, e que o A-09 tinha acabado de tornar respeitável.

**O que foi colapsado, medido linha a linha:** das 334, **128 não eram duplicata**, e **as
128 se distinguem pelo `ultimo_dia_com_direito`**. O Bradesco pagou R$ 0,01 em 30/04/1996,
30/08/1996, 30/12/1996, 28/02/1997 e 31/03/1997 — cinco parcelas, cinco dias, e para a chave
antiga um pagamento só.

| chave | silver com calendário de 2023 | silver com calendário de 41 anos |
|---|---|---|
| `data_ex` (a de 21/09) | **334** | 206 |
| `ultimo_dia_com_direito` | **206** | **206** |

**A correção é da chave, não do calendário**, e a tabela é a prova: com o campo observado a
contagem é 206 dos dois lados — deixa de depender de quanto calendário existe no disco.

**A regra, e ela é maior que este módulo:**

> **Identidade se monta com o campo OBSERVADO, nunca com o DERIVADO.** `ultimo_dia_com_direito`
> vem da B3 e está preenchido em 9.272 de 9.272; `data_ex` nós calculamos, e o que nós
> calculamos pode faltar. **Campo vazio dentro de uma chave não distingue: ele UNE, e em
> silêncio.** É o F-02 na camada da identidade — ausência de insumo virando *igualdade*, em
> vez de virando zero.

**E o pior era como ele ia sumir.** Com o calendário largo a chave antiga também dá 206. O
defeito se auto-encobriria na corrida seguinte, e o único vestígio seria a linha "334
duplicata(s) exata(s)" no laudo de 21/09 — que ninguém teria motivo para reabrir. **Defeito
que se apaga sozinho ao se corrigir outra coisa é o que não deixa achado.**

**Guarda:** `fase0/test_a12_chave_de_evento.py`, 8 testes. O que nomeia o achado exige a
contagem **igual nos dois silvers**; outro reintroduz a chave de 21/09 e mede os 334 contra
206, com as 128 verificadas como distinguíveis pelo campo observado. Um teste que só
afirmasse o número certo não documentaria nada.

**Efeito na série:** os 128 eventos passam a ser aplicados. Na janela 2021–2025, as séries por
status não mudam (23 `AJUSTADO`, 78 `INCOMPLETO`, 1 `NIVEL_INCERTO`), o degrau do dia ex vai
de 1.584 para 1.586 casos, e o ajustado de −0,1885% (t = −2,49) para −0,1864% (t = −2,46).
**O veredito do C-02 não muda; o número muda na terceira casa.** O CSV de 21/09 foi
preservado ao lado do novo, porque ele é o artefato por trás de um laudo publicado.

## A-13 · O mesmo provento chega pelas duas esteiras, e dar preço a ele o aplicaria duas vezes

**23/09/2026.** Achado ao executar a decisão da P-113 — usar o fechamento do COTAHIST onde a
B3 não traz `closingPricePriorExDate`. A previsão pré-registrada (`docs/auditoria/P113-CRITERIOS.md`,
commit `9a08a55`) era de **172** eventos ganhando fator. Ganharam **11**.

**Os outros 161 não eram fatores faltando: eram o mesmo pagamento chegando pela segunda
porta.** As duas esteiras da B3 se sobrepõem na janela recente — `GetListedSupplementCompany`
devolve os últimos meses, o paginado devolve o histórico longo —, então o dividendo de
setembro de 2025 está nas duas, com mesmo ticker, mesmo dia, mesmo rótulo e mesmo valor até a
última casa.

`_chave_de_evento` não as colapsa, e **isso é deliberado**: `origem` e `arquivo_origem` entram
nela pelo A-09, porque *"dois registros iguais em páginas diferentes são sobreposição de
paginação, e aí o julgamento seria outro"*.

> **Até 23/09 isso era inofensivo por acidente.** A cópia do suplemento vinha sem preço, logo
> sem fator, logo não era aplicada. **É o P-83 na letra:** *insumo ausente adormecido num campo
> morto continua sendo insumo ausente — o campo morto não é o defeito, é o anestésico.* Lá eram
> zeros dormindo num campo que ninguém lia; aqui é uma duplicata dormindo atrás de um
> `SEM_PRECO`, e a própria correção é que a acordaria.

**A prova é o resíduo, pelo mesmo instrumento que provou o A-09** — 2025 é o ano onde a
sobreposição mora:

| | n | ajustado | **t** |
|---|---|---|---|
| colapsando (o que entrou) | 388 | **+0,0330%** | **+0,39** |
| sem colapsar | 388 | +0,7377% | **+6,31** |

**A armadilha vale mais que o achado: o agregado melhorava enquanto o ano quebrava.** A média
dos cinco anos sem colapsar é −0,0192% (t −0,24); colapsando, −0,1909% (t −2,53). O número que
parece melhor é o da versão errada — o +0,74% de 2025 cancelava o resíduo negativo dos outros
quatro. O laudo do C-02 já dizia por que a tabela é por ano; aqui o agregado esconderia um ano
**quebrado** atrás de quatro certos.

**E o critério que eu havia pré-registrado não teria pego.** R3 exigia `|ajustado| < |bruto|`
no agregado e nos cinco anos, e a versão errada passa nos seis: **encolhimento não detecta
super-ajuste** — um fator aplicado duas vezes ainda encolhe um degrau de −5%, só que passa do
outro lado do zero.

> **Quem pegou foi a coluna de procedência que a decisão dele mandou criar.** `B3+COTAHIST=131`
> num relatório é uma pergunta — *por que um degrau precisaria de preço das duas fontes?* — e
> sem ela os 161 teriam entrado calados. **Procedência não é documentação do número: é
> instrumento de medida.**

**A regra:** identidade de *pagamento* (`_provento`) não é identidade de *registro*
(`_chave_de_evento`). A segunda inclui a porta de entrada, de propósito; a primeira não pode,
porque a pergunta que ela responde é *este pagamento já está contado?* — e a resposta não pode
depender de por qual porta ele entrou. Valor comparado como número, nunca como texto:
`0.10216531400` e `0.102165314` vieram assim das duas esteiras.

**Guarda:** `fase0/test_p113_preco_de_vespera.py`, 17 testes. O que nomeia o achado reintroduz
a duplicata por mutação e exige **as duas** consequências: 2025 quebra (t +0,39 → +6,31) **e** o
agregado melhora. Um teste que só verificasse o número certo não documentaria a armadilha.

---

## CV-04 · O pré-registro v2 promete fundamento desde jan/2010, e o primeiro chega em 27/01/2011

*24/09/2026, medido sem alterar nada, antes de construir a montagem (§11.1).*

O `preregistro-ml-v2.md` §2 diz: *"Período: jan/2010 a ago/2026 (fundamentos DFP desde
2010 …)"*, e na mesma seção: *"variável contábil só entra se `DT_RECEB` ≤ data de decisão"*.
As duas frases estão certas cada uma por si. Juntas, não fecham: o `dfp_cia_aberta_2010`
é o **exercício** de 2010, e ele foi **entregue** em 2011.

**A medição**, sobre o acervo capturado em 24/09 (os CSVs de índice dentro dos ZIPs, uma linha
por documento e versão; data de decisão = último pregão do mês pelo `calendario.pregoes()`,
496 pregões em 2010–2011):

| arquivo | linhas | empresas | menor `DT_RECEB` |
|---|---|---|---|
| `dfp_cia_aberta_2010.csv` | 1.113 | 663 | **2011-01-27** |
| `itr_cia_aberta_2011.csv` | 2.510 | 678 | **2011-04-04** |

Não existe `itr_cia_aberta_2010` no índice da CVM. A fonte já dizia isso desde 06/09
(*"Histórico desde 2011"*, `docs/fontes/cvm-itr-politica-atualizacao.md`).

Empresas (`CD_CVM`) com pelo menos um documento de `DT_RECEB` ≤ último pregão do mês, somando
dfp 2010–2011 e itr 2011–2012:

| mês | empresas | só DFP | só ITR |
|---|---|---|---|
| jan/2010 … dez/2010 | **0** | 0 | 0 |
| jan/2011 | 3 | 3 | 0 |
| fev/2011 | 82 | 82 | 0 |
| mar/2011 | 510 | 510 | 0 |
| abr/2011 | 593 | 593 | 22 |
| mai/2011 | 618 | 618 | 573 |
| jun/2011 | 635 | 635 | 602 |
| dez/2011 | 675 | 670 | 662 |

**Doze meses sem fundamento nenhum**, justamente no começo do desenvolvimento (jan/2010 a
dez/2019). A regra de disponibilidade faz o que deve: recusa o dado que não existia. O que
estava errado era a frase do período.

**Duas curiosidades observadas e não investigadas, com n:** o `dfp_cia_aberta_2011.csv` tem
linhas com `DT_REFER` 2011-03-31 (o mínimo do arquivo), e o `itr_cia_aberta_2012.csv` tem um
documento com `DT_RECEB` 2011-11-11 para um `DT_REFER` de 2012. Nenhuma das duas muda a tabela
acima: ambas estão depois de dez/2010.

**A regra:** um período declarado **com** uma variável começa no primeiro `DT_RECEB` dela,
não no primeiro `DT_REFER`. Ano do exercício não é ano da disponibilidade. **O que fica
aberto:** a emenda ao pré-registro é decisão dele e vai empurrada antes de qualquer resultado
(P-116): P-132. O limite da fonte está em `limitacoes_declaradas → itr_da_cvm_comeca_em_2011`
(FISICA).

---

## CV-05 · O FCA não traz código de negociação antes de 2018, e o universo do ML identifica empresa pelo `CD_CVM`

*25/09/2026, medido ao preparar a medição da emenda 1 (P-132), depois de ela ser empurrada e
antes de qualquer mês ser calculado.*

A §2 do `preregistro-ml-v2.md` monta o universo com o COTAHIST, que fala **ticker**, e
identifica a empresa pelo **`codeCVM`**. Os documentos da CVM (DFP, ITR) falam `CD_CVM`. A ponte
entre os dois, na fonte primária, é o FCA (`fca_cia_aberta_valor_mobiliario_AAAA.csv`, coluna
`Codigo_Negociacao`), capturado pela primeira vez neste dia.

**A medição**, ações (`Valor_Mobiliario` = ações ordinárias/preferenciais) com
`Codigo_Negociacao` preenchido, por arquivo:

| FCA | linhas de ações | com código | CNPJs com código |
|---|---|---|---|
| 2010 … 2017 | 425, 358, 316, 265, 446, 432, 415, 411 | **0 em todos** | **0** |
| 2018 | 569 | 460 | 321 |
| 2021 | 660 | 571 | 413 |
| 2026 | 562 | 519 | 378 |

**Oito anos sem ticker nenhum.** O campo existe no leiaute e vem vazio. Uma ponte montada com o
FCA de 2018 em diante só enxerga quem **continuou listado até 2018**: é viés de sobrevivência
dentro do instrumento. Com a operacionalização 2 da emenda (*sem `CD_CVM` conta como sem
documento*), toda empresa deslistada entre 2010 e 2017 empurraria o início do desenvolvimento
para frente. A medição estaria medindo **a ponte**, não a chegada do fundamento.

**Por isso o mês da emenda NÃO foi medido.** A regra diz que o primeiro mês fecha a questão, e
registrar um mês produzido por um instrumento sabidamente defeituoso o fecharia errado. É a
régua §5-B.1: a frase do que a medição mediria (*"quantas empresas a ponte de 2018 reconhece
em 2011"*) é mais estreita que a conclusão (*"quando o fundamento chegou"*).

**O alcance é maior que a emenda:** o universo da §2 inteiro, de 2010 a 2017 — a maior parte do
desenvolvimento —, não se monta com o que o projeto tem. Os eventos da B3 trazem `codeCVM` para
as 74 emissoras atuais do Ibovespa, o que é sobrevivência de novo.

**Candidatas não tentadas, `NAO_CONFIRMADO`:** o cadastro de ISIN da B3 (tabela de emissores:
código de 4 letras e CNPJ) e o Formulário de Referência da CVM. Uma tentativa de endpoint do
arquivo de ISIN deu `404`; o endereço tinha sido suposto, não lido de uma página, e parei ali
para não inventar URL. **Não é afirmação de que a ponte não existe** (§5-B.13): é afirmação de
que o FCA não é ela antes de 2018. Pendência: **P-143**.

> **Seguimento, 25/09 (P-143 fechada):** a ponte existe, e o endereço estava no JS da página
> `isinPage/` (`GetTextDownload/` lista; `GetFileDownload/<btoa(id)>` entrega o `isinp.zip`). O
> `404` da primeira tentativa era o endereço suposto. O FCA de 2010 a 2017 também **não** tem
> coluna de ISIN (cabeçalho medido em 2010, 2014 e 2017). Ver CV-06.

---

## CV-06 · A tabela de emissores da B3 descreve o dono ATUAL de cada código, e um código de 2010 pode apontar para outra empresa

*25/09/2026, medido ao montar a ponte da P-143.*

O banco de ISIN da B3 (`EMISSOR.TXT`, 69.359 emissores, todos com data `20180628`) liga código
de 4 caracteres a CNPJ. Aplicado aos 190 emissores do universo do ML de 2010–2012:

| resultado | emissores |
|---|---|
| ligados a um CNPJ registrado na CVM | 136 |
| — deles, nome incompatível com o do COTAHIST | 20, **todos corretos** na conferência à mão (renomeações: Hypera, Brookfield, T4F…) |
| código **ausente** do `EMISSOR.TXT` (trocou depois de 2010: CCRO, ELET, BVMF, DTEX…) | 50 |
| código **reaproveitado**, CNPJ de outra entidade | 4: `EMBR` = Embrast Ltda (a Embraer está em `EMBJ`), `JBSS` = JBS N.V., `TRPL` = um FII, `PMAM` |

**O perigo não são os 50, é a forma dos 4:** eles só apareceram porque o dono novo não tem
registro na CVM. Um código reaproveitado por uma empresa registrada ligaria o papel de 2010 a
ela **em silêncio**. É o A-01 com outra porta, e a conferência por nome dos 136 não achou
nenhum caso. Isso vale **para esta amostra**, não como regra.

**O segundo tropeço:** os índices DFP/ITR de 2010–2012 não trazem o nome da época. A CVM os
regerou em 08/2024 (CV-02) e o `DENOM_CIA` é o atual: "Terra Santa Agro" em 2010. Casar por
nome contra eles procura Duratex e acha zero.

**A regra:** tabela de identidade de hoje não é identidade de ontem. Ponte histórica passa por
**sucessão conferida**, com o par CNPJ/CD_CVM checado no cadastro por teste, como na
`docs/aprendizado/ponte-emissor-cvm.yaml` (42 linhas, 6 sem ponte declaradas).

---

## GIT-01 · Duas redações publicadas da mesma seção de pré-registro, porque uma sessão olhou só o `main`

*25/09/2026. Erro meu (Claude Code, sessão local). Achado ao responder se o repositório estava
pronto para terceiros, listando as branches remotas.*

**O que houve.** Às 15:11Z uma sessão na nuvem empurrou a §6 da emenda 1 do pré-registro ML
(`2f939ae`, sha256 `71621ba64c899281`) para `origin/claude/brave-gates-g4zm6k`. A mesma sessão
trocou as actions para node24 e registrou CI-03 e CI-04. Nada disso chegou ao `main`. Às 16:54Z,
eu, numa sessão local, conferi só `git log` e `git status` do `main`, escrevi *"nada dos dois
itens chegou ao repositório"* e publiquei **outra redação** da mesma §6 (`53112d6`, sha256
`7fc09d780c5012ac`). A troca de actions também saiu duplicada, e a minha, pior: trocou o SHA e
deixou o comentário dizendo v4/v5.

**A medição.** `git branch -r --no-merged HEAD` listava `origin/claude/brave-gates-g4zm6k`, com
4 commits. As duas §6 têm a mesma substância (t-2..t; ≥ mediana, empate entra) e hashes
diferentes. O Osvaldo não sabia que a branch existia: o nome `claude/…` é o padrão das sessões
na nuvem.

**A consequência.** Um pré-registro vale pelo que foi publicado primeiro (P-116). Com duas
versões no `origin`, *"qual texto valia antes da medição"* deixa de ter uma resposta só. Não
houve dano porque nenhum número da P-145 tinha sido medido. E os dois vermelhos do job completo
(CI-04) ficaram invisíveis no `main` por duas horas.

**A forma é a da régua 15 (§5-B), um nível acima:** *"o repositório"* medido como *"a branch em
que eu estou"*. Medi o `main` e concluí sobre o `origin`.

**O conserto.** Merge da branch no `main`, com a versão dela onde as duas se sobrepõem, porque
foi a primeira no `origin` e é a mais completa. `53112d6` fica no histórico como registro.
`auditoria/test_git01_branches_integradas.py` reprova qualquer ref do `origin` que o HEAD não
contenha. Ele reprovou antes do merge. **O limite dele:** só vê o que o clone buscou. No CI
(`fetch-depth` 1) passa sem medir nada, e na máquina depende de um `git fetch` antes.

---

## CI-01 · Dois testes dependiam do `estado.yaml` privado, e ninguém sabia porque nenhum portão rodava fora desta máquina

*25/09/2026. Achado pela primeira execução do workflow *Testes* (`36142833762`, vermelha),
reproduzido num clone limpo do `origin/main`.*

`test_estado_real_nao_tem_mais_reserva_empenhada_a_denunciar` e
`test_reserva_e_zero_e_o_deposito_esta_fora_dela` abrem `alocacao/estado.yaml`, que está fora
do git **por desenho** (§11.6, repositório público). Em qualquer clone eles dão
`FileNotFoundError`. Passaram verdes semanas a fio porque toda rodada acontecia na única
máquina que tem o arquivo. É a régua 15 no nível do repositório: *verde numa árvore* não é
*verde no repositório*, e agora havia um executor para provar isso.

**O conserto não é pular quando falta** (seria a P-142 do avesso: na máquina dele, arquivo
sumido viraria skip calado). É uma marca explícita `privado`. O CI exclui por nome, e na máquina
dele o teste roda e falha alto.

---

## CI-02 · O conserto do `ReadOnly` da limpeza da CVM só funcionava no Windows

*25/09/2026. Terceira execução do workflow *Testes* (`36143785286`), já com a falha anotada.*

`test_3_pasta_somente_leitura_sai_inteira` falhou no Linux com `PermissionError` no CSV
**dentro** da pasta. O `_tirar_somente_leitura` (24/09) liberava a permissão do caminho que
falhou. No Windows, `ReadOnly` na pasta impede o `rmdir` **dela**, e isso bastava. No POSIX, pasta
sem escrita impede apagar **o que está dentro**, e a permissão que falta é a da pasta-mãe. O teste
estava certo, e o código só funcionava no sistema em que foi escrito. O conserto libera as duas.

**Por que ninguém viu:** o mesmo da CI-01. O projeto nunca tinha rodado um teste fora desta
máquina, e **esta máquina é Windows**.

---

## CI-03 · A mutação ficou verde sem ter testado alteração nenhuma

*25/09/2026. *Mutacao* `36152691790` (55 s) e `36164242671` (46 s), as duas verdes. Medido pela
sessão na nuvem (P-146): os **4.935** mutantes ficaram `not checked`.*

A rodada limpa do mutmut (os testes sobre o código **sem** mutação) falha com `failed to collect
stats`, e o `set +e` do passo engolia o erro. Num clone, fora os `privado`, **20 testes** quebram
dentro da cópia `mutants/`: ela não leva `.git`, `.github`, `.gitignore` nem `PENDENCIAS.md`, e
os testes que varrem o fonte veem a instrumentação do mutmut. **Verde sem medição é o F-02 na
camada da mutação:** ausência de teste com a cara de "nenhum sobrevivente".

**O que foi consertado agora é o portão, não a causa.** `auditoria/mutmut_contagem.py` conta
pelos `mutants/*.meta` com a tabela de status **do próprio mutmut** (injetada, não copiada),
publica `gerados`, `testados`, `killed`, `survived`… como `::notice` (a API pública lê sem
login) e sai 1 quando **nada** foi testado, com as 15 últimas linhas do `mutmut run` como
anotação. **A causa continua aberta, e ela é decisão dele (P-146):** restringir os testes da
mutação aos unitários dos quatro módulos, ou marcar os testes de repositório e excluí-los por
marcador. Até lá a *Mutacao* fica **vermelha**, e isso é o certo.

---

## CI-04 · O job `completo` reprovava dois testes que só o armazém expõe

*25/09/2026. *Testes* `36152684302` (#6) e `36164255949` (#9, `94c5348`, vermelho em 7m50).*

A única anotação do #9 era `Process completed with exit code 1`, do passo que junta suíte, lint
e faltas do armazém. O log exige login, e a causa foi separada na máquina dele, uma hipótese
por vez:

| hipótese | medição | resultado |
|---|---|---|
| faltas do armazém | as 98 chaves de registro + inventário, **na árvore `94c5348`**, perguntadas ao R2 | **0 faltas**. A carga do FCA (14:23Z) é anterior à execução (16:59Z) |
| lint | `ruff` + `mypy` nas quatro pastas | zero |
| suíte, no disco dele | as quatro suítes, `-m "not privado"` | verde |
| suíte, **como o runner** | worktree em `94c5348` com só as 98 chaves (91 conferidas por sha256, 7 baixadas do R2), testes **sem** as `R2_*` | **dois FALHAM** |

*(A primeira reprodução rodou com as `R2_*` no ambiente e mostrou só uma falha. O runner não
tem segredo no passo dos testes. Sem elas, apareceu a segunda, como a P-146 já dizia.)*

**(a) `test_P97_nao_sobrou_ZIP_sem_origem_no_acervo`.** Os seis `cotahist_diario/COTAHIST_D*.ZIP`
da rotina (P-135) não têm linha no `origem.csv`. Na máquina dele o teste passava porque esses
arquivos nunca chegaram ao disco (régua 15). **A origem estava declarada:** a URL de cada um
está no `capturas.csv`, escrita por quem baixou. Uma linha manual por pregão violaria a P7, e
copiar a URL criaria duas listas (N-01). `origem_declarada` passou a ler também o registro de
captura da pasta. Só conta a linha que **trouxe byte** (situação vigente, sha256 e URL): um
`404` de feriado não é origem de arquivo nenhum. O `origem.csv` manual ganha em conflito.
`fase0/test_ci04_origem_da_captura.py`, com duas mutações provadas.

**(b) `test_REAL_todo_ano_fixado_confere_nesta_maquina`.** O pin de 2026 (`fb3546ed…`) deixou de
ser a vigente com a captura de 24/09. O `materializar_acervo` só punha a vigente em disco, e o
leitor do ML (P-139) ia ao R2 buscar a fixada, e dava `ArmazemIndisponivel`, porque o passo não
tem segredo. Agora o materializador também põe as **23 versões fixadas** no cache
`data/armazem/`, no único passo com credenciais, e a fixada que falta vira FALTA.

As duas propostas eram as do comentário no PR #1, que esperavam decisão dele. O prompt de 25/09
mandou consertar depois de reproduzir. Prova: árvore do runner, materialização **com**
credenciais (98 no lugar, 23 fixadas, 0 faltas) e as quatro suítes **sem** elas, **verdes**.

---

## LIC-01 · O CSV do NEFIN foi redistribuído por duas semanas sem ninguém ler os termos

*25/09/2026. Achado ao cumprir o item 3 da Sessão A, que pedia a leitura.*

`alocacao/dados/nefin_factors.csv` entrou no git em 10/09 (`8b98028`). O `.gitignore` o mantinha
**de propósito**, com um argumento de reprodução, e o `NOTICE` dizia só *"os termos de uso são
os do NEFIN"*, sem que ninguém os tivesse lido. Com o repositório público desde 11/09, isso é
redistribuição.

**Medido na fonte em 25/09** (`docs/fontes/nefin.md`): *"freely available to academics and
practitioners"*, *"Please cite the dataset when you use it in published work"* e *"© 2026 NEFIN
— All rights reserved"*. A metodologia não traz termo nenhum. Nada autoriza redistribuir.

**A causa do erro de método:** "dado público, gratuito" foi lido como "dado redistribuível".
São perguntas diferentes, e a P-136 já fazia a pergunta certa sobre a B3 sem que ela
atravessasse para a outra fonte que estava **dentro** do repositório.

**O conserto não perdeu reprodução.** O pré-registro fixa o sha256 (`pesquisa.fonte`), não o
caminho. O arquivo continua no disco, no mesmo lugar e com o mesmo hash (`619991c2192c`),
ignorado pelo git. O byte foi para o armazém pela captura nova (`fase0/capturar_nefin.py`,
diária), e o `materializar_acervo.py` põe a versão **fixada** no lugar no job semanal. Os 30
testes que leem o arquivo ganharam o marcador `acervo`: o push os exclui por nome, o semanal
os roda. Os commits anteriores continuam contendo o arquivo, porque o histórico publicado não
se reescreve (CLAUDE.md §6).

---

## CI-05 · Pull request nunca teve portão

*25/09/2026. Achado ao configurar o Dependabot (Sessão B).*

O `testes.yml` rodava em `push` para o `main`, no agendamento e no disparo manual. Pull request
não estava em lugar nenhum. Um PR de contribuidor, ou o PR semanal que o Dependabot passaria a
abrir, chegaria ao `main` sem nenhuma suíte ter rodado nele: o primeiro vermelho seria o do
merge, depois do fato. O template de PR que pede "suítes em zero" teria pedido uma coisa que
nenhuma máquina conferia.

**Conserto:** `pull_request` para o `main` roda o job rápido, e só ele. PR não recebe segredo, e
o completo lê o armazém. `auditoria/test_workflows.py::test_pr_roda_o_rapido_e_nunca_o_completo`.


---

## GIT-02 · O Dependabot reprovava a guarda do GIT-01 em toda máquina que fizesse `git fetch`

*25/09/2026. Achado pelo Claude Code (nuvem) ao rodar a suíte `auditoria` depois da P-148.*

O `.github/dependabot.yml` da Sessão B abriu quatro branches na primeira rodada
(`dependabot/pip/{mypy,numpy,pandas,ruff}-…`). A guarda do GIT-01 exige que toda ref de
`origin/` esteja no HEAD, e passou a reprovar em qualquer clone com `git fetch`, por branches
que **não** são outra sessão fazendo a tarefa: são propostas que só entram por PR, pelo portão
do CI-05. A cada segunda-feira viriam outras — o alarme que dispara sempre (A-08), e a guarda
que existe para pegar uma segunda redação de pré-registro deixaria de ser lida.

**Conserto:** `origin/dependabot/` fica fora da GIT-01, pelo prefixo que só o Dependabot usa.
`auditoria/test_git01_branches_integradas.py::test_git02_so_o_dependabot_fica_de_fora` prende
que o corte não alarga (`origin/dependabotx`, `origin/wip/…` e `origin/claude/…` continuam
pegos).

---

## CV-07 · Captura local sem `--armazem` desincroniza o registro e o R2: o byte nunca sobe

*25/09/2026. Erro meu (Claude Code), achado por mim ao desenhar o job semanal.*

Na P-132 rodei `py -3.11 fase0/capturar_cvm.py` **sem** `--armazem` para trazer o FCA, e commitei
o `docs/acervo/cvm/capturas.csv` com 17 linhas `novo`. Os dois modos compartilham o portão HEAD,
e o estado sai do registro (`estado_do_registro`). A rodada diária do GitHub vai ver o FCA com o
mesmo `Last-Modified` e marcá-lo `inalterado`: **os bytes nunca sobem ao R2**, e nenhum erro
aparece. Quem abrir o FCA pelo armazém recebe `VersaoDesconhecida` ou nada.

**O conserto dos bytes é dele** (credencial): `py -3.11 fase0/subir_acervo_local.py --aplicar`,
que desde a P-132 inclui o `fca`. **O conserto da classe é visibilidade:**
`fase0/materializar_acervo.py` lista, no job semanal, todo arquivo que o registro diz existir e
o armazém não entrega, e o job fica vermelho.

**A regra:** onde existe armazém, captura sem armazém é **escrever no registro uma promessa que o
armazém não cumpre**. Declaração sem execução, a forma de sempre, agora entre o git e o R2.

---

## CV-01 · A versão de 06/09 da CVM não foi capturada, e não volta

*24/09/2026. FISICA: a CVM serve só a versão corrente de cada arquivo.*

Data de versão (o maior `date_time` entre os membros, CV-03) de todo ZIP de 2022–2026 no
acervo, depois da integração da captura:

| ano | versões no acervo |
|---|---|
| 2022, 2023, 2026 (dfp e itr) | 13/09 · 20/09 |
| 2024 (dfp e itr) | **30/08** · 13/09 (só no `(1).zip`) · 20/09 |
| 2025 (dfp e itr) | **14/09** · 20/09 |

As regerações observadas caem em domingo (30/08, 13/09, 20/09), e o 14/09 do 2025 é uma
segunda-feira. **Nenhum ano tem versão de 06/09.** Que ela *existiu* é inferência pela
cadência (domingo entre 30/08 e 13/09), não observação. O que é observação: se existiu, não
está aqui, e a CVM não a serve mais. As reapresentações que entraram entre 30/08 e 13/09
deixaram de ser observáveis na forma **entregue**. Isso vale para o 2024 e, para os outros
anos, desde antes de 13/09.

**E o 2024 de 13/09 escapou por acaso:** a única cópia dele é o `dfp_cia_aberta_2024 (1).zip`,
um download duplicado do navegador. Entra no acervo como snapshot pela Tarefa 3 (P-133).

**A regra:** cada semana sem captura é uma versão perdida, e perdida de forma FISICA. É o
argumento da P-57 em número: a rotina não é conveniência, é o único jeito de a versão existir.

## CV-02 · "Congelado" não é imutável: 2010–2019 foram regerados em agosto de 2024

*24/09/2026, medido nos `Last-Modified` do HEAD e nos membros dos ZIPs.*

A página da CVM chama 2010–2020 de *"arquivos não sujeitos à política de atualização"*, e o
`tools/baixar_cvm.py` os tratava como escopo `congelados`, capturado uma vez. Os cabeçalhos
dizem outra coisa:

| anos | `Last-Modified` |
|---|---|
| dfp 2010–2019 | 05/08/2024, 20:27 a 20:54 GMT, um a cada ~3 min |
| itr 2011–2019 | 06/08/2024, 00:06 a 01:24 GMT |
| 2020 (dfp e itr) | 29/12/2024 |
| 2021 (dfp e itr) | 28/12/2025 |
| 2022–2026 | 20/09/2026, regerados toda semana |

"Não sujeito à política" quer dizer que **não há reapresentação periódica**. Não quer dizer
que o byte não muda: em 08/2024 a CVM regerou a série inteira em lote. E a fronteira da
janela se mede. O **2021** saiu dela na virada de 2025 e o 2020 na de 2024: a janela semanal
são **cinco** anos (2022–2026), não os seis (2021–2026) que o script original supunha. Um
ano deixa a janela com uma última regeração no fim de dezembro.

**A regra:** o padrão da rotina é capturar **todos** os anos com o portão HEAD, que custa um
cabeçalho por arquivo. O escopo ficou só como filtro. Congelado é hipótese que o HEAD confere
toda semana, de graça.

## CV-03 · A data da versão está dentro do ZIP, no relógio de Brasília

*24/09/2026.*

Cada membro de ZIP carrega `date_time`, e é a CVM quem o escreve, na hora de gerar. Nos 34
arquivos canônicos, o maior `date_time` fica **3 h exatas** antes do `Last-Modified` em GMT
(`dfp_cia_aberta_2012`: membro 05/08/2024 17:48, cabeçalho 20:48:19 GMT). O membro está em
horário de Brasília (UTC−3), sem fuso declarado. Por isso **a data muda perto da meia-noite**:
o `itr_cia_aberta_2011` é versão 05/08 pelo membro (22:24) e 06/08 pelo cabeçalho (01:24 GMT).

É por isso que o snapshot se nomeia pelo membro (`__v<AAAAMMDD>__`) e não pela hora da
captura, que era o que o script original fazia (`__20260924T121630Z__`). Duas capturas da
mesma versão passam a ter o **mesmo** nome, e o `sha12` no nome desempata versões do mesmo
dia. O arquivo sem membro, o `cad_cia_aberta.csv`, usa o `Last-Modified`, **em GMT**: as
duas convenções diferem por 3 h e estão declaradas no `capturar_cvm.data_da_versao`.
Sem nenhum dos dois, `vDESCONHECIDA`, nunca a data de hoje.

## CH-01 · O anual do COTAHIST muda de sha256 sem mudar de conteúdo: a B3 reordena ao regerar

*24/09/2026. Medido, sem mudar código. Script e saída em nenhum lugar versionado: os números
estão aqui, e o método em três frases no fim.*

A captura de 24/09 trouxe um `COTAHIST_A2026.ZIP` **menor** que o de 21/09, com três pregões
a mais. Dois bytes-de-verdade, os dois conferidos pelo sha256 do registro (o novo
rebaixado da própria B3 em 24/09 19:22 UTC, com o mesmo `ETag` `d0e7bd48b54bdd1:0` e o mesmo
`Last-Modified`; os cinco diários também, os cinco batendo com `docs/acervo/b3/capturas.csv`):

| | `fb3546ed…` (baixado 21/09) | `4f2cf2aa…` (Last-Modified 23/09 23:43) |
|---|---|---|
| ZIP | 85.779.964 B | 84.469.516 B |
| membro `file_size` | 709.321.015 | 721.181.214 (+11.860.199 = 48.017 × 247) |
| header / trailer | `…20260918` | `…20260923` |
| `TOTREG` = registros `01` contados | 2.871.743 = 2.871.743 | 2.919.760 = 2.919.760 |
| pregões | 179, 02/01 → 18/09 | 182, 02/01 → 23/09 |
| **trechos contíguos de uma mesma data** | **94.173** | **364** (= 2 × 182) |

**Os 179 pregões em comum diferem todos** no sha256 das linhas do dia, na ordem do arquivo —
e **todos os 179 são o mesmo multiconjunto de linhas**: mesmo número de registros, e o
sha256 das linhas **ordenadas** coincide dia a dia. Não há papel a mais, a menos, nem campo
nenhum diferente em dia nenhum. A janela do pré-registro v2 (02/01 a 31/08: 166 pregões,
2.632.789 registros) tem a mesma impressão de conteúdo nas duas versões:
`sha256(registros 01 ordenados) = ab74104d4aec2da2f0bab5ae0bd7b2d725096e9dbc3d876fb67246330dbfe972`.

**O que mudou foi a ordem.** O arquivo de 18/09 intercala datas (94 mil trechos: blocos de
dezenas de linhas de janeiro, de setembro, de janeiro de novo); o de 23/09 passa duas vezes
pelo calendário, cada dia em dois trechos contíguos. Linhas vizinhas mais parecidas
comprimem melhor — é por isso que o ZIP **encolheu** enquanto o conteúdo **cresceu** 1,7%.

**E os diários:** dos cinco (17, 18, 21, 22 e 23/09), os cinco têm exatamente o multiconjunto
do mesmo dia no anual novo; **só o de 23/09 tem também a mesma ordem.** 17 e 18/09 também
batem, como conjunto, com o anual velho.

**O que isto diz, e o que não diz (régua §5-B.1).** Mede **um** par de versões, a cinco
dias de distância, sobre 179 pregões: nesse par, a B3 regerou o anual e **não revisou dia
nenhum**. Não mede que a B3 nunca revise — `n = 1` par. E derruba duas suposições que o
projeto ia herdar da CVM sem medir:

1. **sha256 do ZIP não é identidade de conteúdo no COTAHIST** — o `REORDENADO` × `REAPRESENTADO`
   do `manifesto_cvm.comparar()`, agora na B3. Um detector de revisão por hash acusaria
   revisão em 179 de 179 dias;
2. **conciliação diário × anual não pode ser por linha na ordem** (P-137): quatro de cinco
   diários reprovariam sem diferença nenhuma de dado.

E um terceiro efeito, sobre o pré-registro: ele fixa o sha256 do **ZIP** (`fb3546ed…`), e o
`acervo.versoes()` passou a marcar `4f2cf2aa…` como vigente. Os dois dão o mesmo dado na
janela — **para quem lê sem depender da ordem**. Ver P-139.

**Método:** membro único lido inteiro; `TOTREG` nas posições 32–42 do trailer; linhas `01`
agrupadas por `DATA` (3–10); sha256 das linhas do dia em ordem de arquivo e ordenadas.
Diários conferidos pelo multiconjunto e pela lista ordenada.

---

## Sessão B, 24/09/2026 — itens de uma auditoria externa, B-11 a B-18

*Worktree `sessao-b`, só em `alocacao/`. Juntada a `main` no mesmo dia. Os códigos nasceram
provisórios (`B-n` sem zero, de 1 a 7) e foram renumerados no merge: o projeto já tinha B-01 a B-04 (aqui)
e B-05 a B-10 (`docs/referencia/auditoria-camada-alocacao.md`), e o `achados_ancorados.py` trata o `B-n` sem zero e o `B-0n`
como códigos distintos — a máquina não confunde, um leitor confunde. Cada item tem o teste que
**falha antes e passa depois**, e o "falha antes" foi **medido** — por mutação ou rodando o teste
novo contra o arquivo de `HEAD`.*

**O que NÃO foi aplicado:** C2, C3 e C5 da auditoria externa, por instrução — C2 + C3 juntos
reabririam o **J-01** (reserva empenhada não é reserva).

### B-11 · `estado_io._registro` só reconhecia campo de texto por causa de um `__future__` alheio

`f.type == "str"`: `dataclasses.fields()` devolve a anotação **crua**, que só é a string `"str"`
porque `alocacao.py` tem `from __future__ import annotations`. Num dataclass de módulo sem o
`__future__`, `f.type is str`, a comparação dá `False`, e o campo de texto vai para `_num()`, que o
reprova com *"'corrente' nao e numero"* — erro que não aponta para a causa. Conserto:
`typing.get_type_hints(classe)`. Teste: `alocacao/test_b11_registro_sem_future.py` (3), com o
dataclass escrito em disco e importado de verdade; o primeiro prende a pré-condição (sem
`__future__`). **Falha antes:** 2 de 3 reprovam com o `estado_io.py` de `HEAD`.

### B-12 · As fixtures de sessão eram protegidas por docstring

`custos_originais` e `politica_original` (escopo `session`) tinham como única proteção *"NAO
altere"* — disciplina, que a P-38 recusa, no pior lugar: vivem a suíte inteira e alimentam a porta
sancionada de todo teste seguinte. Conserto no desenho da guarda existente: a fixture registra
impressão e cópia pristina ao nascer; a guarda autouse confere depois de cada teste que **recebeu**
a fixture (via `request.fixturenames`) e restaura com `clear()/update()`. **Não** se limpa cache nem
se recarrega — seria o COPIAR SEMPRE que o `conftest.py` rejeita (S-02). Teste:
`test_B12_a_guarda_vigia_as_fixtures_de_sessao`, por subprocesso. **Falha antes:** `2 failed, 2
passed` — os dois culpados verdes, as duas vítimas vermelhas, longe da causa. Depois: só os
culpados acusados, com o nome da fixture. Limite herdado: impressão por `repr()`.

### B-13 · A guarda do `carregar` escapava por alias e por `import *`

`test_usuario_novo` registrava `a.asname or a.name`: com `from estado_io import carregar as c`, a
chamada `c()` escapava pelas duas pontas; `import *` trazia o `carregar` sem nomeá-lo. A lógica
saiu para `_nomes_do_carregar(fonte)`, que registra o nome original e trata `*` como alcance.
Teste: `test_B13_a_guarda_do_carregar_ve_alias_e_import_estrela`, 5 fontes — três que têm de ser
pegas e **dois controles** (uma guarda que recusasse tudo passaria nas três). **Falha antes:** por
mutação, alias e estrela reprovam. Fora do alcance (P5): `f = estado_io.carregar` e `getattr`.

### B-14 · `test_P72_aporte_mensal_negativo_continua_bloqueando` não testava o bloqueio

Chamava `carregar(..., exigir_real=False)` e conferia a lista. *Bloquear* é o que a porta faz no
modo padrão: levantar `EstadoInvalido`. Agora `pytest.raises(EstadoInvalido, match="aporte_mensal =
-100")`. **Falha antes:** com `carregar()` mutado para não honrar `exigir_real`, o antigo passa e o
novo reprova com `DID NOT RAISE`.

### B-15 · O teste do E-03 media a bandeira, não quem a honra

`test_E03_todo_portao_que_declara_ativo_le_o_proprio_interruptor` procurava a palavra `ativo` em
`inspect.getsource(fn)` — a forma do **A-06**. Virou comportamento: `_cenarios_E03()` dá a cada um
dos nove portões um cenário em que ele, ligado, reprova algo; desligado, não reprova nada. Portão
com `ativo` e sem cenário reprova. **Falha antes:** trocando no G7 `return pares, []` por `pass`,
o teste de `HEAD` passa (a palavra está lá) e o novo reprova.

### B-16 · `motor.simular` × `alocacao.simular_custo` — o F-01 não atravessou

19 rotas confiáveis do `catalogo.yaml`, espelhadas num `motor.Rota` e simuladas pelas duas funções
em três configurações (R$500 × 10a, R$500 × 25a, R$5.000 × 25a): **57 pares**. A aritmética do laço
é a mesma (0 de 57 divergem com `adm_aa` ← `interno_aa`). Com o espelho honesto, **9 de 57
divergem** — as três rotas com `custodia_interna_aa = 0,00025`: `bova11` até **+17,4%**,
`bova11_xp` até +8,0%, `smal11` +4,3% (custo total, `alocacao` maior). O `motor.Rota` **não tem** o
campo: o F-01 foi corrigido só do lado da alocação — o **A-07**. Inerte, porque `motor.simular` não
tinha chamador de produção. Outras divergências: `anos` fracionário (`range` × `int`), custo de
entrada ≥ aporte (o `motor` alerta, a `alocacao` faz `min()` calado → **P-134**), e as
intencionais (bruto/custódia absorvida como parâmetros, contratos de retorno, `entrada_pct` ×
`entrada_extra`). **Desfecho:** a P-43 apagou o lado morto — ver a P-43 em `PENDENCIAS.md`.

### B-17 · `custodia_rv_interpretacao` concordava com o YAML por acidente

A única leitura de `b3.custodia_rv_interpretacao` estava dentro de `motor.simular`, que só testes
chamavam. O caminho de produção, `simular_custo`, usava o **default** `"deducao"` da função — igual
ao YAML, por acidente. É a forma da **P-77**. Promovido na Tarefa 1 de 24/09 (ver o fechamento da
P-43): `simular_custo` passa a ler a chave, e um teste exige que mudar o YAML mude o resultado.

### B-18 · O P-38 falhava de vez em quando, e não era a guarda

O subprocesso não desligava o cache do pytest. No Windows o rename da pasta de cache às vezes falha
(`WinError 5`), sai um `PytestCacheWarning`, e a linha de contagem vira `2 passed, 1 warning, 1
error` — a substring `"2 passed, 1 error"` reprova por um aviso alheio. Conserto: `-p
no:cacheprovider` nos subprocessos. Reproduzido fora da suíte, com o aviso transcrito.

---

## B-19 · Aporte R$ 0 virava NaN dentro do `min()` da P-134, e a interação G3×G4 acertava por acidente

*25/09/2026. Achado pelo Claude Code (nuvem) ao consertar a P-134.*

`simular_custo` fazia `c = min(e*aporte, aporte)`. Com aporte **R$ 0**, a entrada fixa dá
`e = inf`, `inf*0` é **NaN**, e `min(NaN, 0)` devolve NaN: o custo, o patrimônio e o arrasto
viravam NaN, sem erro. `interacao_g3_g4` roda com `estado.aporte_mensal` — que é zero para um
usuário novo — e comparava `NaN < x`, que é sempre falso: a resposta ("nenhuma rota eliminada
venceria") saía **certa por acidente**. É a forma do F-02 em aritmética, a mesma do `t_quantil`
saturado de 18/09: número de borda com cara de número.

**Conserto (P-134):** a condição tem nome, `AporteConsumidoPelaEntrada`, e a simulação recusa
em vez de devolver número. Quem simula aporte fracionado (o `custo_pct_aportado` do alvo, o
`custo_de_discordar`) converte em motivo escrito; a interação G3×G4 tira a rota da comparação,
porque rota que come o aporte não vence ninguém.

**Declarado:** `test_P134_com_aporte_zero_a_interacao_g3_g4_nao_cai_nem_vira_NaN` **passaria na
versão antiga** — o NaN dava a resposta certa. Ele guarda contra a queda que a exceção nova
poderia trazer, não contra o defeito antigo. Os dois que reprovam na versão antiga são os da
recusa e o da proposta com peso mínimo.


---

## G-07 · O G8 libera peso a um carrego em `REGRA_DECIDIDA`, e o validador diz que não

*26/09/2026, medido ao preparar a assinatura da P-01 (decisão dele: `01b`).*

O validador do carrego (`tese.py`, `validar_carrego`) avisa, em todo registro em
`REGRA_DECIDIDA`: *"O G8 NAO libera peso neste estado — ele libera quando virar
COMPROMISSO_ATIVO, no dia da compra"*. O mapa do `CLAUDE.md` repete: *"REGRA_DECIDIDA (G8 NAO
libera peso)"*. **O `g8_compromisso_de_carrego` não lê o estado**: confere só `valida` e
`duracao_anos`.

**Medido** com o cenário sintético dos testes (`test_alocacao.BASE`: despesa 4.500, reserva
27.000, aporte 500, horizonte 25) e os dois registros de `teses.yaml` assinados **em memória**
(nada gravado): hoje, `protecao_real = 0`; assinados, `protecao_real = 0,15`, com `td_ipca` no
bloco — um carrego cuja posição não existe, cujo juro real não foi contratado (`C02:
AGUARDA_COMPRA`), recebendo 15% do patrimônio.

**Por que ninguém viu:** nenhum carrego estava assinado, então a bandeira nunca foi testada
contra o motor. O teste do G-01 (`test_regra_decidida_aceita_c02_e_c04_adiados`) prova que o
**validador** aceita o estado e **avisa** — e é o aviso que o motor não honra. É o E-01/E-03
outra vez: *a bandeira estava levantada e ninguém a honrava*, e o arquivo que declarava era o
teste.

**Não consertado nesta sessão, de propósito:** a instrução dele foi preparar a assinatura
*"sem mexer nos portões"*, e fazer o G8 honrar o estado muda o que um portão faz. O conserto
proposto está na P-152; a assinatura do `td_ipca` espera a decisão.

**Consertado em 26/09/2026** (decisão dele: *"G-07 é defeito, não política"* — a regra é dele e
está escrita; o portão é que a ignorava). `g8_compromisso_de_carrego` lê o estado por
`_estado_do_carrego`, com o **mesmo default** de `validar_carrego` (ausente =
`COMPROMISSO_ATIVO`), e um teste prende os dois defaults juntos. `REGRA_DECIDIDA` vai para
`sem_carrego` e vira pendência com o que falta — a compra —, não com "registrar", que mandaria
refazer o que já está assinado. **Mudança de comportamento, medida por instantâneo dourado**
(`alocar()` inteiro, 9 cenários, campo a campo): com o registro assinado em memória, `td_ipca`
**15% → 0%**, os 15 p.p. voltam ao `lastro` (`td_selic`), e aparecem a pendência
`G8_carrego:td_ipca` e o alerta de PROTECAO_REAL sem rota viável. Com o `teses.yaml` do
repositório (não assinado) e com o carrego em `COMPROMISSO_ATIVO`: **zero diferenças**.
Teste: `test_G07_regra_decidida_nao_libera_peso_no_g8`, que reprova no G8 anterior.


---

## CX-01 · A guarda de segredo dos workflows prometia mais do que fazia

*03/10/2026. Achado externo (auditoria do Codex), conferido pelo Claude do Projeto; medido e
consertado pelo Claude Code.*

**É o padrão do F-05**, com o YAML vigente a mascarar a diferença: a guarda dizia "segredo só
no passo que precisa", e o que ela media era "a *forma* `secrets.NOME` só aparece no passo
que precisa". O `auditoria/test_workflow_medir.py` usava `secrets\.([A-Za-z0-9_]+)`, e o
`test_workflows.py` usava `"secrets." in str(...)` para o `testes.yml` — que roda em
`pull_request`. `secrets['R2_ESCRITA_TOKEN']`, `toJSON(secrets)` e `secrets[format(...)]`
passavam. Como os quatro workflows só escrevem a forma com ponto, **nenhum teste vigente
podia acusar a diferença**.

**Medição.** No `main` (198d0c5), com `defeitos()` do `medir.yml`: das 42 combinações
(7 formas × 6 lugares: env do workflow, do job, do passo autorizado, de outro passo, `with:`,
`run:`), **36 não eram reprovadas** — as 6 que eram usam a forma com ponto dentro de uma
expressão composta. Para o `testes.yml`, a guarda antiga aceita `toJSON(secrets)` no env de
um passo do job `rapido`. O `fase0/test_workflow_captura.py` não tinha o regex, mas só
conferia os passos que conhecia (`==` nos dois passos): um segredo a mais em outro passo, ou
no env do job, passava.

**Consequência.** Um PR com `${{ toJSON(secrets) }}` num passo do `testes.yml` (ou um push em
`medir/**` com `secrets['R2_ESCRITA_TOKEN']`) exfiltraria o token de escrita do armazém com
todas as guardas verdes — e o `medir.yml` existe justamente para o token de leitura ser o
único alcançável (5-A.11).

**Conserto, por lista de permissão e com uma função só (N-01):**
`auditoria/guarda_segredos.py::defeitos_de_segredo`. Percorre todo valor do YAML, extrai cada
`${{ ... }}` (e o `if:`, que é expressão sem delimitador), e toda expressão que mencione o
identificador `secrets` — sem diferenciar maiúscula — tem de ser **exatamente**
`secrets.<NOME>`, no `env` de um passo, com `<NOME>` permitido para aquele (job, passo).
`secrets:` como chave (`inherit`) e expressão sem fechamento também reprovam. A lista
(`PERMITIDOS_POR_WORKFLOW`) é uma só e um teste exige entrada para todo arquivo de
`.github/workflows/`. Usam-na `medir.yml`, `testes.yml`, `mutacao.yml` e `captura_cvm.yml`.

**Testes que falham na versão anterior:** `test_cx01_forma_de_segredo_que_escapava_do_regex_reprova`
(36 das 42 falhavam no `main`) e `auditoria/test_guarda_segredos.py` (10 formas × 8 lugares ×
4 workflows, controle do YAML vigente e vacuidade por workflow).

**O que a guarda não vê:** um script que leia `os.environ` do passo já autorizado; e workflow
reutilizável de outro repositório (`uses:`), que só é pego se declarar `secrets:`.

**Retratação parcial (03/10/2026, mesmo dia): o conserto reabriu uma garantia.** A guarda de
`198d0c5` reprovava um segundo passo com segredo (`"segredo em mais de um passo"`). A
`guarda_segredos` autorizava por **nome** de passo, e um passo homônimo — duplicado no fim ou
inserido antes do original, com outro `run:` e o mesmo `env` — herdava a autorização:
`defeitos_de_segredo` devolvia `[]` em `medir.yml`, `testes.yml` (job `completo`) e
`captura_cvm.yml`. Medido no `main` (`f336042`): 24 dos novos testes de mutação falham
(16 de duplicata, em início e fim; 8 de passo ausente). O nome do teste
`..._so_tem_contents_write_e_o_token_de_leitura_num_passo` ainda prometia a garantia perdida.
**Causa raiz do erro de método:** o prompt do conserto não listava os invariantes da guarda
antiga, e eu troquei de mecanismo sem inventariar o que o mecanismo velho garantia por
acidente (é o N-01 de novo, do lado da guarda). **Conserto:** cada `(job, nome)` autorizado
tem de casar com exatamente um passo; zero ou dois ou mais é defeito, com nome e contagem na
mensagem. **Processo:** troca de guarda passa a ter a tabela "garantia antiga → teste que a
cobre hoje" no PR (ficou no PR #53).

---

## CX-02 · `pais_varridos()` não separa motor de teste

*03/10/2026. Achado externo (auditoria do Codex), **aberto** — pendência P-173.*

Medido em 03/10: 49 candidatos a chave órfã hoje, 67 contando só os pais do motor. Das 18
escondidas, 15 são leitura legítima por `getattr` da lista `exibidos` (`corretoras.py:398`), 1
é a P-32 (vigiada em `DIVIDA_DE_COBERTURA`) e 2 (`custos.yaml`
`etf.IMAB11.composicao.{administracao,gestao}`) estão escondidas por colisão de nome com
`memoria["composicao"]` em `test_alocacao.py:2042`. É a pergunta 2 da régua (5-B): o
instrumento incluiu o que não devia. Conserto e ordem em P-173; teste ainda não escrito.

---

## CX-03 · `conftest.py:146` trata `atual is None` como "não mudou"

*03/10/2026. Achado externo (auditoria do Codex), **aberto**, prioridade baixa — pendência P-174.*

`C = None` e `del C` num módulo vigiado escapam da acusação e da restauração. Conserto
(sentinela de ausência) e teste de mutação descritos em P-174; ainda não feitos.

---

## CX-04 · A porta de entrada aceitava NaN, infinito e booleano como dinheiro

*04/10/2026. Achado externo (auditoria do Codex de 03/10, `A-01` no original; registro e de/para
em `docs/auditoria/AUDITORIA-CODEX-2026-10-03.md`). Conferido e consertado pelo Claude (Cowork).*

`estado_io._num()` testava `isinstance(v, (int, float))`, e `bool` é subclasse de `int`:
`despesa_mensal: true` virava R$ 1,00 de despesa. `float(s)` aceita `"nan"`, `"inf"` e
`"Infinity"`, e o YAML lê `.nan` e `.inf` como float; nada conferia finitude. E dois campos nem
passavam por `_num()`: `posicoes` e `dependentes` entravam crus.

**O agravante que a auditoria não mediu:** o YAML 1.1, que o PyYAML implementa, lê `yes`, `no`,
`on` e `off` sem aspas como booleano. Quem escreve `caixa: no` (de "não tenho") entregava ao
motor um `False`, isto é, zero, sem aviso nenhum.

**Medição.** As três provas da §9.9 falham no `main` (`0247a21`) como a auditoria transcreve
(`DID NOT RAISE EstadoInvalido`, n=3). A ampliação, em
`alocacao/test_cx04_porta_de_entrada.py`, cobre os 17 campos numéricos que o `validar()` lê
(os 5 de `NUMERICOS`, `reserva_disponivel`, `reserva_empenhada`, `dependentes`, um valor de
`reserva_por_rota` e de `posicoes`, e os campos numéricos de `Divida`, `Objetivo` e
`MatchEmpregador`, lidos da própria classe). No `main`: **306 de 306 casos passavam pela
porta** (17 campos × 8 valores do Python, mais 17 × 10 grafias escritas como texto de YAML).

**Consequência medida pela auditoria:** `NaN` em `aporte_mensal` chegava ao `alocar()` e
terminava em `ValueError`; `true` em `despesa_mensal` produzia a diretiva `G2_reserva` a partir
de uma despesa de R$ 1,00. É dado inválido com aparência de dado válido, a classe do A-01 de
11/09 em outra porta.

**Conserto, num ponto só:** `_num()` recusa o booleano antes do teste de número, e todo número
passa por `_finito()`. `posicoes` (função `_posicoes`) e `dependentes` passam a usar `_num()`;
`dependentes` inteiro volta `int`, porque `Estado.dependentes` é `int`, e ausente continua
sendo zero.

**Instantâneo dourado** (11 estados sintéticos válidos, `validar` + `alocar` + `motor_aporte`,
campo a campo): **nenhum valor mudou**. A única diferença é de tipo: os valores de `posicoes`
escritos como inteiro (`bova11: 900`) saem `float` (`900.0`), como todo outro campo numérico já
saía. As ordens do motor são idênticas.

**O que não cobre:** intervalo econômico (despesa negativa, taxa de 900% ao mês), rota
desconhecida em `posicoes`, e campo que o `validar()` não lê. Um teste de cobertura reprova
campo numérico novo do `estado.exemplo.yaml` que fique sem prova.

---

## CX-05 · A guarda do modelo em branco conferia o dicionário de dados, não os problemas

*04/10/2026. Achado externo (auditoria do Codex de 03/10, `A-02` no original; registro em
`docs/auditoria/AUDITORIA-CODEX-2026-10-03.md`). Conferido e consertado pelo Claude (Cowork).*

**É o padrão do F-05/N-01/R-01/S-02**: o teste declarava "o modelo em branco é recusado, e a
recusa nomeia cada campo obrigatório", e media outra coisa. `validar()` devolve
`(dados, problemas, avisos)`; `test_o_modelo_nao_carrega_ate_alguem_preencher` desempacotava
`problemas, _avisos, _ = validar(d)`, e `problemas` era o **dicionário de dados**. O modelo tem
as chaves obrigatórias, com valor nulo: `assert problemas` passava porque o dicionário não é
vazio, e `campo in p` achava cada nome entre as chaves. Os dois concordavam por acaso.

**Medição.** Os dois mutantes da §9.9 (o validador sem recusa nenhuma; só com a recusa do
status MODELO) deixam o teste verde no `main` (`0247a21`): `DID NOT RAISE AssertionError`, n=2.
Dos 9 desempacotamentos de `estado_io.validar()` e `estado_io.carregar()` no `main` (`grep`, 04/10), este é o
único na ordem errada.

**Consequência.** A recusa do modelo em branco, que impede uma recomendação feita a partir de
nada, podia sumir do `validar()` sem nenhum teste deste arquivo reprovar. A auditoria não mediu
se outro teste da suíte pegaria a mesma regressão, e eu também não.

**Conserto:** `_dados, problemas, _avisos = validar(d)`, e o teste confere que `problemas` é uma
lista antes de conferir o conteúdo. Os dois mutantes, um controle e o contrato do retorno ficam
em `alocacao/test_cx05_guarda_do_modelo.py`.

---

## PO-01 · O limiar de poder do C-02 foi calculado numa convenção, e o resultado foi lido em outra

*03/10/2026. Achado na leitura do resultado da corrida de 2016–2020 (`b331172`), depois da
corrida. Introduzido em `2e11c48` (26/09, §9 do pré-registro, revisão 4) e mantido em
`2638de1` (revisão 5). **Não muda o veredito, que saiu como saiu (P-115, opção A); é lição
para um critério v3.***

**O que se mediu, em uma frase.** O bootstrap **por pregão** da §3.1 deu σ̂ do JCP =
**0,0971 (n=555, 271 pregões)**. A §9 projetava ~**0,058** (0,0482 × √(807 ÷ 555)) a partir de
um σ **por ponto**, iid, de 2021–2025. O σ̂ real ficou 1,67 vez acima da projeção.

**A conta que faltou.** Pela convenção que julga o K2, chegar ao σ_max de 0,0416 exigiria
555 × (0,0971 ÷ 0,0416)² = **3.024 JCPs (≈ 3.000)**. A regra da §9, que pede σ ≤ 0,8 × σ_max =
0,03328, exigiria 555 × (0,0971 ÷ 0,03328)² = **4.725**. O acervo inteiro de 2013–2025 tem
cerca de **1.658** (851 em 2013–2020 e 807 em 2021–2025, as duas contagens do
`c02_contar_n.py`). Com isso, **nenhuma janela possível no acervo dava poder ao K2 do JCP**. O
K3 do dividendo também ficou sem poder (σ̂ 0,0778 > 0,0463, n=416), e este não tinha nem o
aviso da §9.

**A consequência em termos do projeto.** A §9 escolheu a janela com uma régua que não era a do
juiz. O veredito não mudaria, porque com qualquer σ acima de 0,0342 a janela é 2016–2020 de
qualquer jeito. Mas **a inviabilidade teria aparecido antes da corrida**, com uma medição de
2021–2025 fora da quarentena. A §9 ("O que não se mediu") descreveu essa medição e não a fez.
Com ela, a pergunta para ele seria "o K2 do JCP não tem poder em nenhuma janela; roda assim
mesmo?", e não a leitura de um `NAO_CONFIRMADO` depois.

**Lição: o limiar de poder tem de ser calculado com a mesma convenção que vai ler o
resultado** (mesma unidade reamostrada, mesmo gerador e mesmo estimador do σ). É o padrão N-01
do lado da estatística: dois números com o mesmo nome (σ) que concordavam por suposição.

**Retratação (claude.ai, 03/10/2026).** Na auditoria de 03/10 (`1828c18`), o claude.ai afirmou
que a diferença de convenção "não muda nenhuma decisão". **A evidência que a derruba:** o σ̂ por
pregão saiu 1,67 vez o projetado, e a conta acima mostra o K2 inviável em todo o acervo. **O
que estava certo:** a janela escolhida e o veredito não mudariam. **O que estava errado:** "não
muda nenhuma decisão". Rodar ou não uma corrida sem poder **é** uma decisão, e a medição que a
teria informado estava descrita e não foi feita. **Causa raiz do erro de método:** o alcance da
frase foi medido só contra a escolha da janela (a tabela de 0,0276 a 0,0342), e não contra a
decisão de rodar. É a pergunta 1 da régua (5-B): a frase da medição era mais estreita que a
conclusão.

**O que muda no processo.** Um pré-registro com teste de poder calcula o σ esperado pela
**função que julga**, ou declara em uma linha por que não pode. No C-02, essa função é
`c02_corrida.bootstrap_por_pregao`. **Guarda:** ainda não há teste. Ela vale para um critério v3
(§7: o v3 só vale para dado que ninguém mediu) e entra no pré-registro dele.

---

## GIT-03 · Duas sessões locais no mesmo clone ao mesmo tempo, durante a corrida do C-02

*03/10/2026. Sem efeito no resultado, **medido**. Mesma família do GIT-01: duas mãos no mesmo
repositório sem uma ver a outra.*

**O que o reflog do clone mostra** (`git reflog --date=iso`, 03/10/2026, horário de Brasília):

| hora | o que |
|---|---|
| 15:34:40 | `pull --ff-only origin main` → HEAD `506678e` (o commit que a corrida grava) |
| 15:36:48–54 | checkout de `claude/p-165-autoria-das-razoes` e rebase dela sobre `origin/main` |
| 15:36:56 | checkout de `claude/p-115-corrida-2016-2020`, com HEAD em `97bdc56` (o commit da P-165) |
| 15:38:10 | `branch: Reset to 506678e`, checkout e o commit do resultado `b331172` |
| 15:38:49 | checkout de volta para `claude/p-165-autoria-das-razoes` |

Duas sessões alternaram o HEAD da mesma pasta em intervalos de segundos. A da P-165 trocou de
branch 39 s depois do commit do resultado. O branch da corrida chegou a apontar para o commit
da P-165 por 74 s, até o reset. **O reflog não diz qual sessão fez cada passo**, e a hora exata
da corrida (44 s) não está nele; o JSON grava o commit `506678e`.

**Por que não contaminou.** A trava P7 do `c02_corrida.py` exige árvore limpa e HEAD no
`origin`, e o JSON registra o commit que de fato rodou. **E a prova é a reexecução:** em
03/10, nesta sessão, `julgar(ajustar.medir(...))` sobre os mesmos insumos (sha256 da §2
conferidos) reproduziu o `resultado` do JSON **folha a folha: 150 folhas, 0 diferenças (n=1)**.
O código medido (`auditoria/c02_corrida.py`, `fase0/`, `custos.yaml`, a transcrição do D1) é
idêntico entre `506678e` e o HEAD da reexecução (`git diff --stat` vazio).

**O risco, que desta vez não se realizou.** Uma troca de branch no meio de uma corrida muda os
`.py` que ainda não foram importados. Um `git add` de uma sessão pega o arquivo da outra. O
commit "do resultado" pode sair em cima do commit errado: aqui o reset corrigiu, mas por mão,
não por guarda.

**Conserto:** regra no `CLAUDE.md` §5. É **uma sessão local por pasta**; sessões paralelas
usam `git worktree`, uma pasta por branch. Guarda automática: nenhuma. Duas sessões não se veem,
e a regra é de quem as abre.

---

## PO-02 · O K2 sem poder era o resultado esperado, e foi tratado como risco

*03/10/2026. Retratação do claude.ai, registrada pela sessão local a pedido dele. Complementa o
PO-01: aquele é o limiar calculado na convenção errada; este é a leitura errada do que os
números já diziam antes da corrida.*

**O resultado da P-115, como saiu** (opção A; `b331172`, #57). K2 do JCP: σ̂ = **0,097**
(0,0971, n=555, bootstrap por pregão) contra σ_max = **0,0416**. Para chegar ao σ_max, o K2
pediria ~**3.024** JCPs (4.725 pela regra de 0,8 × σ_max); o acervo inteiro de 2013–2025 tem
~**1.658**. **Nenhuma janela do acervo atinge o n.** O K3 do dividendo também ficou sem poder
(σ̂ 0,0778 > 0,0463, n=416). Veredito: `NAO_CONFIRMADA`.

**A retratação, nas palavras do claude.ai:** *"tratei o sem poder do K2 como risco quando era o
resultado esperado"*. **A evidência que a derruba**, com os números do PO-01 (conta do registro,
não releitura da §9): a própria projeção da §9 dava σ ≈ 0,058 para n = 555, já acima do σ_max de
0,0416. Mesmo na convenção otimista, 2016–2020 não tinha poder no K2. "Pode faltar poder" era a
frase; "vai faltar poder" era a conta.

**A consequência em termos do projeto.** A corrida foi decidida como quem aceita um risco, e não
como quem já sabe o resultado do K2. Com a leitura certa, a pergunta para ele seria a do PO-01
("o K2 não tem poder em janela nenhuma; roda assim mesmo?"), e a série ajustada teria virado
limitação declarada uma semana antes (é a decisão de 03/10, P-180). Nesse intervalo, 9 dos 47
PRs de 26/09 a 03/10 foram da série (IP-01).

**Causa raiz do erro de método.** Probabilidade dita onde havia aritmética. Pela régua (5-B,
pergunta 1), a frase "é um risco" era mais fraca que a medição que existia: o n do acervo e o
σ projetado já fechavam a conta.

**O que muda no processo.** Pré-registro com teste de poder escreve, antes de rodar, o poder
**previsto** de cada critério com a conta ao lado (`PREVISTO: sem poder`, não "risco"); se algum
sai sem poder em toda janela possível, a pergunta vai para ele antes da corrida. **Guarda:
nenhuma**, e não há critério v3 em vista: a série é limitação declarada desde 03/10.

---

## IP-01 · A decisão 65b ficou oito dias sem PR, atrás de outros 47

*03/10/2026. Inversão de prioridade, apontada na conversa de 03/10 no claude.ai e medida pelo
registro.*

**O que se mediu.** `gh pr list --search "created:>=2026-09-26"`: **47 PRs, de #13 a #59**;
nenhum título cita P-65, nota explicativa, IPE ou esteira. `git log --since=2026-09-26`: **103
commits**, nenhum assunto cita a P-65. Ele tinha decidido em 26/09 **65b, construir já** (fila,
bloco 4). Pelo título, classificação do registro: 15 de processo e registro, **14 de rosto**,
**9 da série ajustada** (P-115 e P-117), 4 de captura, 4 do motor do M1 (teses, G-07) e **1 no
caminho da CVM** (#15, o `medir.yml` da P-145, que parou à espera de dois passos dele).

**A consequência em termos do projeto.** "Construir já" virou, na prática, "não construir", sem
ninguém decidir isso. E o `PLANO.md` continuou listando a segunda esteira na §5, entre as
"decisões que são dele e o plano não anda sem elas": **a decisão tomada parecia pendente**, e
quem lia o plano não tinha como ver a inversão.

**O padrão, e ele é o de sempre** (F-05, N-01, R-01, S-02): um arquivo declara um comportamento,
e nada o executa. Aqui o arquivo é a fila, e o comportamento é a ordem do trabalho. A resposta
foi registrada na pendência e na fila; o `PLANO.md` não a absorveu; e a escolha do próximo passo
não olha decisão sem PR.

**O que muda.** (1) O caminho crítico de 03/10 está no `PLANO.md`, e decisão respondida sai da
lista de abertas no mesmo commit. (2) Ritmo de duas sessões de motor para uma de rosto, contado
na skill `bastter-proximo-passo` (regra 2b). (3) A P-65 está nas ativas, e a posição dela é o
bloco 23 da fila, porque o caminho de 03/10 não a nomeia e escolher entre as duas decisões não é
da sessão. **Guarda automática: nenhuma** para "decisão sem PR", declarado no `PLANO.md` §5. A
parte do plano que repetia limitação retirada tem guarda (`auditoria/test_plano_e_pendencias.py`).
