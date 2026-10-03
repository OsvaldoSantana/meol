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

**A regra (proposta, bloco 21 da fila):** em **14 dias corridos**, **2 eventos** de autoria
Claude numa classe, etiquetados com modelo abaixo do Opus, devolvem a classe um degrau acima
(`haiku → sonnet → opusplan → opus`). A volta se registra aqui, com a data e os eventos.

**O que a regra não vê (P5):**

- **Erro que ninguém achou.** O `eventos.csv` só tem o que alguém registrou; um modelo mais barato
  que erra em silêncio passa na regra. A guarda que existe contra isso é a suíte, não a regra.
- **A linha de base.** Antes de 03/10 não havia etiqueta: não há taxa por classe do Opus para
  comparar. O limiar de 2 é escolha, não medida; por isso vai para a fila.
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
