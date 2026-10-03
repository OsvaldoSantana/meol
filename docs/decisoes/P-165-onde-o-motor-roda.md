# P-165 — onde o motor roda para o usuário

*03/10/2026. Decisão do Osvaldo, pelo formulário do Projeto no claude.ai (bloco 18 da
[fila](fila-do-osvaldo.md)). Registro feito pela sessão local do Claude Code.*

## As alternativas

- **A · No aparelho**, como diz a P-157. Mais pesado de carregar; o dado nunca sai.
- **B · Servidor com banco de dados.** Leve e sincroniza entre aparelhos, mas o dado financeiro
  passa a morar com o MEOL: LGPD, backup, vazamento, login e custo mensal.
- **B′ · Servidor sem estado.** O aparelho envia a situação, o servidor calcula e devolve, e nada
  é gravado, nem em log. O dado continua morando no aparelho.

## A escolhida: B′

A e B foram recusadas. A P-157 ("o dado fica no aparelho") fica de pé.

**Por quê**, nas palavras do desenho:

1. **O motor em Python num lugar só.** Não se reimplementa nem se empacota o motor para rodar no
   celular; a resposta dele de 26/09 ("servidor") era isso.
2. **O dado não mora no MEOL.** Sem banco, não há base de dados financeiros de pessoas para
   guardar, fazer backup, vazar ou responder em pedido de titular.
3. **Não guardar é coerente com as provas de independência e com a recusa da marca:** o MEOL não
   recebe comissão, não vende produto e não constrói ranking nem comparação entre pessoas
   (RI-06). Um sistema que acumulasse as carteiras teria um ativo que contradiz isso.

## As três consequências, com status

| | consequência | status |
|---|---|---|
| (a) | **A LGPD continua valendo: processar é tratar, mesmo sem gravar.** Pedem-se base legal, aviso, transporte cifrado e região de hospedagem declarada. | **NAO_CONFIRMADO juridicamente.** Nada disto foi lido na fonte nem passou por parecer; segue na **P-158**. |
| (b) | **"Não grava" exige prova:** teste com valores-sentinela que reprova se qualquer um aparecer em log, erro ou métrica, incluindo o padrão da plataforma de hospedagem. | **Aberta: P-175**, antes do primeiro endpoint do motor (etapa 4). |
| (c) | **O contrato da F0 passa a ser também o formato que trafega na rede.** Na leitura do item 20 da fila, minimizar os campos em trânsito. | **Aberta**, junto do item 20 da fila ("Ler a especificação da F0"). |

## O que esta decisão não faz

Não escolhe a plataforma de hospedagem nem a região, não resolve a LGPD e não prova nada sobre
log: promete. A v1 do rosto é sintética e não é afetada. A P-175 é o que transforma a promessa
em fato.
