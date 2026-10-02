# O app do Claude no GitHub não é instalado

**Decidida em 26/09/2026. Autor: Osvaldo.** Registrada pelo Claude Code, na sessão da nuvem.

## A pergunta

A sessão da nuvem acompanha os PRs que abre (`subscribe_pr_activity`). Ao assinar o PR #30,
a resposta foi esta: *"the Claude GitHub App isn't installed on osvaldosantana/bastter or
doesn't have access to it"*. Sem o app, nenhum evento do PR (CI vermelho, comentário de
revisão, conflito) acorda a sessão. Instala-se o app?

## As alternativas

| opção | o que acontece | consequência |
|---|---|---|
| **A · não instalar** (escolhida) | a sessão confere o PR por check-in agendado (`send_later`): CI, conflito e revisão, e faz o merge se estiver verde | **menor privilégio:** nenhuma integração nova com acesso ao repositório. O custo é a latência: uma falha entre dois check-ins só é vista no seguinte, e todo PR precisa de check-in agendado |
| B · instalar o app | os eventos do PR chegam sozinhos | mais uma credencial de terceiro com acesso ao repositório, para ganhar minutos num projeto que não tem pressa (`CLAUDE.md` §6). As permissões exatas que o app pede **não foram lidas** nesta sessão: `NAO_CONFIRMADO` |

## A decisão

1. **O app não é instalado.** Os check-ins agendados cobrem o acompanhamento dos PRs.
2. **Todo PR aberto pela sessão da nuvem sai com um check-in agendado.** Sem o app, o
   check-in é o único aviso. PR aberto sem check-in é rotina que depende de alguém lembrar
   (P7).
3. Isto não muda a regra 7 da §5-A: disparar workflow e mexer em segredo continuam pedidos a
   ele.

## Quando revisitar

**Se um aviso perdido causar erro**, por exemplo um PR mesclado sobre CI vermelho, um
conflito que ninguém viu, ou um comentário de revisão sem resposta. Nesse dia, o caso entra
aqui com a data e o PR, e a pergunta volta para a fila.
