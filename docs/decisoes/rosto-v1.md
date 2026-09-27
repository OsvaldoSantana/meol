# O rosto do MEOL, v1: estímulo e protótipo para teste, na ordem que ele definiu

**Decidida em 26/09/2026. Autor: Osvaldo.** Preparada no claude.ai; registrada pelo
Claude Code. Continua a trilha F0 (`PLANO.md` §3-F0) e **não passa na frente da
P-115**.

## As perguntas, as respostas e o que cada uma deixou de fora

| # | pergunta | resposta | alternativas não escolhidas |
|---|---|---|---|
| a | para quem é a v1 do rosto | **protótipo com dado sintético para o teste com pessoas** | só para ele, com os números dele (exigiria os 12 campos `NAO_EXISTE` no motor e disputaria com a P-115); beta com terceiros (bloqueado pela P-158) |
| b | a ordem da marca, com a UX feita antes de design e mercado | **seguir a ordem à risca**: pesquisa → design → mercado → UX → brandbook | tratar mapa e requisitos como requisitos funcionais e manter a UX adiantada; reescrever a ordem |
| c | o `SEM_POSICAO` é o primeiro item de motor para a tela | **sim**, depois da P-115, com a regra escrita por ele (P-164) | a primeira tela só para quem já tem posição; só um estado de recusa, sem mudar o motor |
| d | o que do Quanto-e-Onde.html sobrevive | **só o conceito** "quanto e onde" como primeira linha | a tipografia IBM Plex; cada cor que passasse no contraste; nada |
| e | onde o motor roda para o usuário | respondeu **servidor**; **fica em aberto** (P-165), porque colide com a P-157 | no aparelho; adiar |
| f | que nome aparece no protótipo | **MEOL** | nome neutro de trabalho; decidir o nome agora |

## O que cada resposta muda

- **b · o mapa de telas v1** fica como **rascunho de UX adiantado** (nota N-ORDEM
  nele), revisado na etapa 4. A etapa 2 (design) é a que o chat de 20/09 já tinha
  desenhado: três direções visuais mais um controle, mostradas como a mesma tela
  T1. O pré-registro daquele dia está transcrito em
  `docs/marca/preregistro-teste-de-marca-2026-09-20.md`.
- **c · a regra já existe no motor.** Com patrimônio zero, a fórmula de
  `motor_aporte()` (`D = peso × (V + A) − posição`) põe o aporte nas `k_max` rotas
  de maior peso. O guarda `V <= 0` existe porque o código divide por `V` depois
  (`peso_atual`, `deficit_rel`). Lido no código, **não medido numa execução**. E o
  `test_depois_da_reserva_o_sistema_aloca_sem_nada_assinado` confere o alvo, não as
  ordens. **Ressalva registrada:** o caso atende quem nunca investiu; o público de
  entrada, decidido em 20/09, é quem já aporta.
- **d · o Quanto-e-Onde é documento técnico do motor**, não tela para leigo
  (seções 0 a 10: arquitetura, portões, elegibilidade, custo de discordar). Medido
  em 26/09 (luminância relativa da WCAG), tema claro:

  | par | razão | leitura |
  |---|---|---|
  | `--ink-3` #6D7C8B sobre `--paper` #EFF3F7 | 3,84:1 | reprova o 1.4.3 em texto pequeno; o arquivo o usa em 10,5 a 12 px |
  | `--ink-3` sobre `--surface-2` #E3EAF1 | 3,53:1 | idem |
  | `--rule` #C4D0DD sobre `--paper` | 1,40:1 | abaixo de 3:1; só vale como decoração |
  | `--ink` sobre `--paper` | 16,18:1 | passa |

  Carrega fontes do Google Fonts, que é recurso remoto. O **conteúdo** fica como
  candidato à T6 (Método).
- **e · a resposta "servidor" colide** com a P-157 e com o mapa (O1, §5). Existe
  uma terceira via: **servidor sem estado**. Fica aberta na P-165 e no bloco 18 da
  fila.
- **f · o nome MEOL** entra nos estímulos com texto simples, sem logotipo, até a
  busca de anterioridade (P-166).

## Decisões técnicas (do claude.ai, com as alternativas)

| decisão | escolhida | alternativas | por quê |
|---|---|---|---|
| onde vivem os tokens de design | **dado em YAML** (`docs/marca/tokens/`), verificado em Python no CI que já existe | CSS solto; biblioteca de tokens em Node | P2: regra como dado; zero dependência nova; o contraste vira teste que falha |
| estímulos da etapa 2 | **HTML estático**, um arquivo por direção, sem framework, sem recurso remoto, em `docs/marca/direcoes/` | protótipo em framework; ferramenta de design externa | são estímulos descartáveis, não produto; sem build e sem dependência |
| números nos estímulos | **saem de uma rodada do motor sobre cenário sintético**, com o comando registrado | números escritos à mão | P1 vale até no estímulo; D-01: nenhum número dele |
| front da etapa 4 | TypeScript, build estático, React, testes com Playwright e axe-core; formatação num formatador único testado byte a byte (`Intl.NumberFormat('pt-BR')` usa U+00A0 depois de "R$"). Pasta própria (`rosto/`), porque a raiz é guardada por `test_raiz_viva.py`. Revisitável sem custo até a abertura da etapa 4 | Svelte; HTML puro | maior base de documentação; primitivas acessíveis maduras |
| hospedagem do protótipo | GitHub Pages, **só dado sintético** | Cloudflare Pages | nenhuma conta ou credencial nova; mesmo caminho das releases da CVM |
| verificação automática | piso, não teto: o axe cobre parte da WCAG. A revisão humana da P-155 e o teste com pessoas continuam | "passa no axe = acessível" | o limite do instrumento declarado (CLAUDE.md §5-B) |

## Fora da v1

Notificações, gráficos, comparação entre usuários, conteúdo educativo fora da
decisão, conta e cobrança, sincronização entre aparelhos (mapa §7). Mais as telas
sem campo da P-160 (O5, aba "e se" da T3, empresas da T4, RI-04, RI-11), a
importação de carteira (P-157), login e qualquer página pública. Cada um entra por
decisão própria, não por acúmulo.

## Limitações declaradas

1. O pré-registro de 20/09 foi escrito num chat, **sem impressão digital**. Vale
   como pré-registro a partir do commit que grava a versão final, se esse commit
   for empurrado antes de qualquer estímulo ser mostrado (a lição da P-116).
2. A regra do `SEM_POSICAO` foi lida no código, não executada.
3. Os estímulos são desenhados com ajuda de IA. O risco conhecido é o visual
   genérico, e um controle D caricato que tornaria a H2 trivial. A P-163 cobra os
   dois.
4. Uma amostra de conveniência escolhe entre direções; não descreve o investidor
   brasileiro.

## Notas de registro

*27/09/2026, Claude Code, ao gravar o texto preparado no claude.ai.*

- **O que foi conferido no repositório antes de gravar.** O item c: `motor_aporte()` em
  `alocacao/alocacao.py` devolve `SEM_POSICAO` com `V <= 0`, a fórmula das ordens é
  `pesos × (V + A) − posição` ordenada pelo déficit, e `k_max` vem do `politica.yaml`
  (hoje 2); o teste citado existe em `alocacao/test_usuario_novo.py` e confere só o alvo.
  O item d: as três razões com hex no texto foram recalculadas pela fórmula da WCAG e dão
  3,84, 3,53 e 1,40 (n=3); a quarta não tem o hex de `--ink` no texto e não foi recalculada.
- **Uma troca no texto de origem.** A limitação 3 dizia "a S3 cobra os dois", com o nome
  de sessão da fila do chat. O repositório não define sessões numeradas, e a regra desta
  gravação era não criar prefixo novo; ficou o código da pendência que faz os estímulos,
  a P-163.
