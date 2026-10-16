# O Playwright da R3 volta a 1.56.0 e fica parado até a rodada fechar

**Decidida em 16/10/2026. Autor: a arquitetura** (sessão do Projeto no claude.ai, prompt de 16/10
da P-170). Registrada pelo Claude Code, na sessão local. Decisão técnica: não muda o que a R3
mede, muda com que instrumento.

## A pergunta

A captura da R3 (`tools/r3_capturar.py`) mede o que o navegador computa: a moda dos pixels da
tela de 390 px, as cores, bordas e raios dos botões, a família da fonte. As 51 visitas de 04/10
rodaram no **Playwright 1.56.0, Chromium build 1194** (`pesquisa-marcas-rodada3-2026-09.md` §1,
linha "captura"). Em **10/10/2026, 08:46**, a arquitetura fez o merge do **PR #69 do Dependabot**
(`4ed1727`): o grupo `r3` do `pyproject.toml` subiu para **1.63.0**, que espera o **Chromium
1243**. A rodada estava no meio (visitas de bancos e pagamentos começaram no mesmo dia).

A sessão da nuvem de 10/10 percebeu e compensou: apontou o Chromium 1194 que a máquina dela já
tinha por `R3_CHROMIUM`, e o `medidas.json` grava `navegador` em cada captura. Então **as capturas
de 10 e 11/10 não trocaram de motor**; o que trocou foi o **padrão**: quem instalasse o grupo `r3`
do zero (a sessão local, o workflow da captura) ganharia o 1243 sem ninguém decidir. Fica-se
com o 1194 até a R3 fechar?

## As alternativas

| opção | o que acontece | consequência |
|---|---|---|
| **A · voltar a 1.56.0 e ignorar o playwright no Dependabot até a R3 fechar** (escolhida) | `playwright==1.56.0` no grupo `r3`; `dependabot.yml` ignora o `playwright`; a lista `tool.meol.dependencias.instrumento_r3` diz por quê, e `auditoria/test_workflows.py` confere as duas juntas | **um instrumento na rodada inteira**: `playwright install chromium` baixa o 1194 em qualquer máquina, a da sessão local e o servidor do GitHub; nenhuma variável de ambiente lembrada por alguém (P7). Custo: as correções de segurança do Playwright entre 1.56 e 1.63 esperam a R3 fechar; o alcance é um navegador sem interface que só abre páginas públicas e não clica em nada |
| B · ficar no 1.63.0 e manter o `R3_CHROMIUM` | nada muda no `pyproject` | o instrumento depende de cada máquina ter o 1194 e de alguém exportar a variável; o workflow do GitHub não tem o 1194 e capturaria no 1243 |
| C · subir a rodada inteira para o 1.63.0 e recapturar as 85 | instrumento novo, uma vez | refaz duas semanas de captura para ganhar uma versão que nada na R3 pede; e as capturas de 04/10 de quem não abre mais mudariam de conteúdo |

## A decisão

1. **`playwright==1.56.0`** no grupo `r3`, com o comentário apontando para cá.
2. **O Dependabot ignora o `playwright`** até a R3 fechar. A lista que justifica o ignore é
   `tool.meol.dependencias.instrumento_r3`: não é `numericas` (não muda a impressão do ambiente,
   o grupo `r3` fica fora dela), e a guarda P-148 passou a exigir `ignore == numericas ∪
   instrumento_r3`.
3. O `R3_CHROMIUM` continua no `r3_capturar.py` (a nuvem traz o 1194 sem `playwright install`),
   mas deixa de ser necessário em máquina que instala o grupo.

## Quando sai

**Quando a P-170 for para a tabela das fechadas**: no mesmo commit, apagar `instrumento_r3` do
`pyproject.toml` e o `ignore` do `playwright` no `dependabot.yml` (a guarda reprova se só um dos
dois sair). Se chegar aviso de segurança do Playwright antes disso (os Dependabot alerts não
dependem do `dependabot.yml`), a pergunta volta para ele.

## O que este episódio deixou

O merge do #69 está registrado como retratação da arquitetura (`docs/metricas/eventos.csv`,
16/10, e `ACHADOS.md`, EX-04): **atualizar dependência de um grupo que é instrumento de uma
rodada em andamento troca o instrumento**, e o Dependabot não tem como saber que um grupo é
instrumento. Agora a lista diz.
