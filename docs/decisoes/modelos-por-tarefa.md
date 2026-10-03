# Modelos por tarefa e a abertura de sessão em 2 mil tokens

*Decisão dele, 02/10/2026. Registrada em 03/10/2026, sessão na nuvem. A tabela que o código
lê é [`docs/metricas/modelos-por-tarefa.yaml`](../metricas/modelos-por-tarefa.yaml) (P2): este
arquivo é o porquê, e o YAML ganha se os dois divergirem.*

## A tabela de 02/10

| classe de tarefa | modelo | observação |
|---|---|---|
| registro (`PENDENCIAS.md`, fila, `eventos.csv`, changelog) | **Sonnet** | |
| pesquisa | **Sonnet**, com subagentes **Haiku** | a leitura larga vai para o `Explore` do repositório (`.claude/agents/Explore.md`), em Haiku |
| engenharia | **opusplan** | Opus planeja, Sonnet executa |
| pré-registro | **Opus** | |
| estatística | **Opus** | |
| P-115 (o critério do degrau) | **Opus** | |
| auditoria | **Opus** | |
| arquitetura | **Opus** | |
| — | **Fable não** | em classe nenhuma |

O padrão do repositório (`"model": "sonnet"` em `.claude/settings.json`) é o da classe mais
frequente. Quem abre uma sessão de outra classe escolhe o modelo ao abrir.

## A regra de volta, pelo `eventos.csv`

**O buraco que ela tinha:** o `docs/metricas/eventos.csv` registra quem errou (`autor`), mas não
**com que modelo**, e 40 das 73 linhas de 03/10 têm `autor = desconhecido`. Sem o modelo, a
regra não teria o que contar: seria prosa.

**O que mudou:** todo evento de autoria Claude com data a partir de 03/10 abre a `descricao` com
a etiqueta `[modelo=<m> classe=<c>]`, com os valores da tabela (ou `modelo=desconhecido`).
`auditoria/metricas_processo.py` reprova a linha sem etiqueta ou com valor fora da tabela, e
imprime, no fim do relatório, as classes que dispararam a regra.

**A regra (decisão dele, 03/10: 21d, fila bloco 21):** a **taxa** de uma classe é o número de
eventos de autoria Claude por PR mergeado no `main`, os dois etiquetados nela com modelo abaixo
do Opus. O semanal (`testes.yml`, passo "Regra de volta dos modelos") mede a taxa numa janela de
**14 dias** e a compara com a **referência**: os eventos e os PRs de 16/09 a 02/10, tudo em Opus,
classificados uma vez em [`docs/metricas/referencia-modelos.csv`](../metricas/referencia-modelos.csv).
A classe volta um degrau (`haiku → sonnet → opusplan → opus`) quando a taxa **passa de 1,5 vez**
a referência **e** há **pelo menos 4 PRs** dela na janela. *(Ajuste de 03/10: a referência é
(eventos + 1) / (PRs + 1) e a volta exige também pelo menos 2 eventos da classe na janela.)* O 1,5 e o 4 são escolha declarada, não medida. Quando uma classe volta, o semanal abre
uma issue, e a volta se registra aqui, com a data e os números.

**O PR leva a etiqueta no título**, `[modelo=<m> classe=<c>]`, porque é ele o denominador. O CI
reprova o PR sem ela (`metricas_processo.py --titulo-pr`), com o Dependabot fora.

**O que a regra não vê (P5):**

- **Erro que ninguém achou.** O `eventos.csv` só tem o que alguém registrou; um modelo mais barato
  que erra em silêncio passa na regra. A guarda que existe contra isso é a suíte, não a regra.
- **A classe da referência é inferida (`OBSERVADO`).** A sessão de 03/10 leu a descrição de cada
  evento e o título de cada PR e escolheu a classe; ninguém a declarou na hora. Outro leitor
  pode classificar diferente, e a referência muda com isso.
- **A referência começa em 25/09, não em 16/09.** O primeiro PR mergeado no `main` é de 25/09.
  Os 10 eventos de 16/09 a 24/09 estão no CSV, mas fora da taxa, porque não têm denominador.
  Ficam 17 eventos em 37 PRs.
- **Referência zero, resolvida no ajuste de 03/10.** Com a referência em eventos / PRs,
  `registro` (0 em 6) e `arquitetura` (0 em 2) voltavam no **primeiro** evento numa janela com 4
  PRs. Decisão dele, no mesmo dia: a referência passa a ser **(eventos + 1) / (PRs + 1)**, e a
  volta exige **pelo menos 2 eventos** da classe na janela, além do fator e dos 4 PRs. `registro`
  fica com 1/7 = 0,14 (limiar 0,21) e `estatistica`, sem PR, com 1,0 (limiar 1,5), em vez de
  "só os números". O +1 e o 2 são escolha declarada, não medida; o efeito é de piso, e quem diz
  se o piso é alto demais é a revisão de 17/10 (P-172).
- **O autor desconhecido.** 40 das 73 linhas do período não dizem quem errou e ficaram fora da
  referência. Se as linhas novas saírem mais completas, a taxa nova sobe sem que o modelo piore.
- **O PR não mede o tamanho do trabalho.** Um PR de uma linha e um de mil contam igual.
- **`modelo=desconhecido` não conta e não absolve.** Ele é aceito para não forçar ninguém a
  inventar o modelo; o relatório de etiquetas mostra quantos são.

## A abertura de sessão

**O que se lia antes:** os quatro arquivos `SEMPRE` de `auditoria/tamanho_do_contexto.py`,
`CLAUDE.md`, `PENDENCIAS.md`, `PLANO.md` e `docs/doutrinas.md`: 60.791 tokens, dos quais 40.364
do `PENDENCIAS.md`. Medição e recorte: [`docs/metricas/contexto-de-sessao.md`](../metricas/contexto-de-sessao.md).

**O que se lê agora:** o `PENDENCIAS.md` sai da abertura. `tools/estado.py` gera
`docs/estado.md` (pendências abertas com código, título, dono, gatilho e classe, mais os blocos
da fila sem resposta, abaixo de 2 mil tokens), um hook `SessionStart` o injeta, e a sessão lê do
`PENDENCIAS.md` só a seção da P da tarefa. O CI reprova o `estado.md` velho
(`tools/test_estado.py`).

**Conferido na documentação oficial do Claude Code em 03/10/2026:**

- **Hooks de projeto rodam na nuvem**, em sessão de **um** repositório: *"Your repo's
  `.claude/settings.json` hooks and permission rules — Yes, in a session with one repository"*
  (code.claude.com/docs/en/cloud-environments, *What carries over from your setup*). Numa sessão
  de vários repositórios (thread de projeto, inclusive) eles **não rodam**; ali, a instrução do
  `CLAUDE.md` §1 manda ler o `docs/estado.md` à mão.
- **O texto injetado tem teto de 10.000 caracteres**; acima disso vira arquivo e só uma prévia de
  2.000 entra (code.claude.com/docs/en/hooks). O `estado.py --conferir` reprova acima do teto.
- **A chave `model` do `.claude/settings.json` é lida** em sessão de um repositório, mas
  `--model`, `ANTHROPIC_MODEL` e a escolha do modelo ao abrir a sessão passam por cima dela
  (code.claude.com/docs/en/settings). Ela é o padrão, não uma trava.
- **O `Explore` embutido roda no modelo da conversa**, não em Haiku; um `Explore` do projeto o
  substitui e mantém o próprio `model`. **E um subagente do projeto lê o `CLAUDE.md`** a menos que
  declare `omitClaudeMd: true` (code.claude.com/docs/en/sub-agents). O nosso declara, e por isso
  as duas ordens da §5-A.10 (não inventar; marcar `NAO_CONFIRMADO`) estão no prompt dele.

**Não conferido:** se o hook roda no desktop dele, no Windows. O comando é `cat`, e esta sessão
não leu como o Claude Code executa hooks lá nem viu o `estado.md` aparecer numa sessão local. A
primeira sessão no desktop confere: se o estado não estiver no contexto, o hook não rodou.
