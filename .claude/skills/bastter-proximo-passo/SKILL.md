---
name: bastter-proximo-passo
description: Como escolher e propor o próximo passo do projeto Bastter sem pôr dado pessoal no caminho crítico nem empilhar engenharia. Use ao encerrar uma sessão ou ao decidir no que trabalhar.
---

# Escolher o próximo passo — projeto Bastter

Esta skill existe porque o próximo passo foi escolhido errado **várias vezes seguidas**,
e de duas formas diferentes. As regras abaixo são correções medidas, não teoria.

## Regra 1 — classifique por QUEM está bloqueado (achado U-01)

Antes de chamar qualquer coisa de bloqueio, pergunte:

> **Um cliente novo desta ferramenta teria isso?**

Se não teria, **o sistema precisa funcionar sem** — e aquilo não é bloqueio de
desenvolvimento.

| classe | significa | está no caminho crítico? |
|---|---|---|
| `BLOQUEIA_O_SISTEMA` | o sistema não faz o trabalho dele | **sim** |
| `DECISAO_DE_DESENHO` | precisa de *um* humano decidindo sobre o sistema | só se travar outra coisa |
| `DADO_DE_UM_USUARIO` | o estado de **uma** carteira | **nunca** |

> **Como o erro aconteceu.** Eu listava "aporte realizado = zero" e "teses não
> assinadas" como bloqueios do projeto. O Osvaldo corrigiu: *"imagina que fosse uma
> ferramenta para ser vendida — eu não teria informações sobre o aporte e a reserva do
> cliente porque ele não existiria."*
>
> Só **2 de 29** pendências eram dado do usuário, e eu tinha as duas no caminho
> crítico. É o achado L-01 (separar motor de perfil) num nível acima: a configuração
> foi separada, o **plano** nunca tinha sido.
>
> `test_usuario_novo.py` guarda isso: patrimônio zero e nada assinado recebem resposta
> completa e acionável.

## Regra 2 — não proponha engenharia duas vezes seguidas (P-44)

Se a sessão anterior fechou uma pendência de engenharia, a próxima proposta é de
**produto, dado, ou uma pergunta ao Osvaldo**.

> **Como o erro aconteceu.** Sete rodadas seguidas de qualidade de engenharia, zero de
> propósito — e eu propus todas, uma no fim de cada resposta. Cada uma era real; a
> **sequência** foi guiada por "qual a próxima tarefa de engenharia" em vez de "o que o
> projeto precisa".
>
> É o achado M-01 aplicado a nós: trocar o **destino** do aporte move 3 meses, trocar o
> **valor** move 33, e o sistema trabalhava na alavanca de 3. **A alavanca da
> engenharia move 0** — nenhum teste aproxima a reserva de existir.

Engenharia entra quando **destrava** algo, não quando é o que sobrou de mais fácil.

## Regra 2b — duas sessões de motor para uma de rosto (decisão dele, 03/10/2026)

Motor é o caminho crítico e a frente "primeiro uso" do `PLANO.md` (§3 e §4); rosto é marca,
UX e pesquisa com pessoas. Antes de propor, conte os três últimos PRs mergeados pela etiqueta
e pelo assunto: se dois deles já são de rosto, o próximo é de motor. Registro não é sessão: vai
dentro do PR que o gera. **Sem guarda automática** — a conta é desta skill, e o `PLANO.md` §5
declara isso.

> **Como o erro aconteceu.** De 26/09 a 03/10, 47 PRs: 14 de rosto, 15 de processo, 9 da série
> ajustada, e **um** (#15) no caminho da CVM, que parou à espera de dois passos dele. Nenhum
> tocou a P-65, que ele decidira construir já (65b). Achado IP-01.

## Regra 3 — prazo vence preferência

Algumas coisas têm janela e não voltam. A **Fase 0** (baixar DFP/ITR da CVM) é a
principal: a CVM **sobrescreve os arquivos anuais**, e `DT_RECEB` não se reconstrói
depois. Trabalho com prazo passa na frente de trabalho melhor sem prazo.

## Como encerrar uma sessão

1. `PENDENCIAS.md` atualizado — **antes** de encerrar, não durante. O que sobrou só se
   sabe no fim.
2. O que fazer ao voltar ao desktop, escrito.
3. **Sempre nomear o próximo passo.** Se não houver plano, elaborar um.
4. Dizer a **classe** do próximo passo em voz alta. Se for `BLOQUEIA_O_SISTEMA` duas
   vezes seguidas e as duas forem engenharia, a Regra 2 foi violada.
