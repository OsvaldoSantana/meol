# Marca e interface — índice

*26/09/2026. Os quatro documentos desta pasta e o mapa de telas em `docs/ux/` foram escritos
em sessões de chat de 20/09 e trazidos do Projeto no claude.ai para o repositório em 26/09.*

## O que vale hoje

| documento | papel |
|---|---|
| **[requisitos de interface v1](requisitos-interface-v1.md)** | o contrato: RI-01 a RI-34, cada um com a sua verificação (teste, revisão ou pesquisa); os RI-22 a RI-34 (v1.1, 27/09) vêm da [WCAG 2.2 lida na fonte](../fontes/wcag-22-w3c.md) |
| **[mapa de telas v1](../ux/mapa-de-telas-v1.md)** | as telas, os fluxos, os estados e os campos que a F0 (contrato de saída do motor) precisa emitir; desde 26/09, **rascunho de UX adiantado**, revisado na etapa 4 (nota N-ORDEM nele) |
| **[estímulos das direções E, C e D](direcoes/README.md)** | a T1 em cada direção escolhida (16b), versões base e com rota bloqueada (j-A), com os [tokens](tokens/direcoes.yaml), as [fontes OFL](tipografia/README.md) e os números do motor ([`conteudo.yaml`](direcoes/conteudo.yaml)); P-163, refeita na S4 e **aprovada por ele em 27/09** (sha256 na fila) |
| **[pré-registro do teste de marca, versão final 2](teste-de-marca/preregistro-final.md)** | o que vale para o teste (P-162, S5 v2, 27/09): as decisões dele, a regra, H1 a H3, o veto de distinção, as limitações, e o sha256 dos seis PNG, do [questionário como dado](teste-de-marca/questionario.yaml) ([versão de leitura](teste-de-marca/questionario.md)), do [livro de códigos visuais](teste-de-marca/codigos-visuais.yaml) (com as categorias do veto, ac-a), do classificador (`tools/codigos_visuais.py`) e da análise (`tools/analise_teste_marca.py`). **Vale a partir do merge no `main`**, antes do primeiro convite |
| ~~[pré-registro, versão final 1](preregistro-teste-de-marca-final.md)~~ | **superado sem uso** pela versão 2 (o Google Forms deu lugar a uma página própria); fica como registro, com o [questionário v1](teste-de-marca-questionario.md) |
| [pré-registro do teste de marca, 20/09](preregistro-teste-de-marca-2026-09-20.md) | a **origem** do final: as direções A a D, as hipóteses H1 a H4 e a regra como declaradas em 20/09, **sem impressão digital**; fica como registro, e onde diverge do final vale o final |

Os três documentos de pesquisa abaixo são a **origem** desses dois: explicam de onde cada
requisito veio, mas não se editam para mudar um requisito. Requisito novo, revogado ou
reescrito muda o documento de requisitos, com nova versão (regra da §6 dele).

## Ordem de leitura

1. [pesquisa de fundação (rodada 1)](pesquisa-fundacao-2026-09.md) — o público, o mercado
   brasileiro, o design para leigo e a primeira fundação de marca; RI-01 a RI-10.
2. [pesquisa de marcas, rodada 2](pesquisa-marcas-rodada2-2026-09.md) — 20 marcas, o livro de
   códigos MC-01 a MC-24, e RI-11 a RI-16.
3. [Pix v7.4 e pendências](pesquisa-pix-e-pendencias-2026-09.md) — o manual de experiência do
   Banco Central, MC-25 a MC-29, RI-17 a RI-21, e o bloco de marcas encerrado por decisão.
4. [requisitos de interface v1](requisitos-interface-v1.md) — a consolidação.
5. [mapa de telas v1](../ux/mapa-de-telas-v1.md) — a etapa de UX.
6. [pré-registro do teste de marca, 20/09](preregistro-teste-de-marca-2026-09-20.md) — o que o
   teste de marca da etapa 3 vai medir, como declarado antes de qualquer estímulo.
7. [pré-registro final](preregistro-teste-de-marca-final.md) e o
   [questionário](teste-de-marca-questionario.md) — o teste como vai rodar.

A trilha de produto que continua daqui é a F0, paralela ao motor: ver `PLANO.md` §3-F0 e a
decisão em [`docs/decisoes/F0-trilha-de-produto.md`](../decisoes/F0-trilha-de-produto.md).
A ordem das etapas do rosto (pesquisa → design → mercado → UX → brandbook) e o que a v1 é
estão em [`docs/decisoes/rosto-v1.md`](../decisoes/rosto-v1.md) (26/09/2026, decisão dele).

## Os códigos

Os documentos chegaram com os prefixos C (livro de códigos) e R (requisitos), que já eram
usados por achados do projeto. Foram renomeados para **MC** (código de marca) e **RI**
(requisito de interface), mantendo o número. A tabela de/para está no cabeçalho de cada
documento, e `auditoria/test_codigos_de_marca.py` reprova se um código desta pasta voltar a
colidir com um achado.

## Apelido

`pesquisa-fundacao-marca-2026-09.md` é o **mesmo documento** que
[`pesquisa-fundacao-2026-09.md`](pesquisa-fundacao-2026-09.md): é o nome com que ele existia no
Projeto do claude.ai, e é o nome citado em `docs/auditoria/AUDITORIA-PREREGISTRO-ML-V1.md`
(§ das limitações), que fica como está por ser registro datado. O nome no repositório é o que
o próprio documento declara como destino.

## O que estes documentos não são

- **Não são decisão de marca tomada.** A fundação de marca (rodada 1, bloco D) é síntese,
  `NAO_CONFIRMADO`, a testar com pessoas.
- **Não são parecer jurídico.** As afirmações sobre a Resolução CVM 19 foram conferidas no
  texto dela em 26/09/2026 ([transcrição](../fontes/cvm-resolucao-19-consolidada.md)): duas
  confirmadas com escopo, uma retirada, com a retratação ao lado do texto original. O
  enquadramento do MEOL é da P-158.
- **Não carregam dado do autor.** Os prints da auditoria visual de 20/09 são de contas de
  terceiros ou de demonstração, e não estão no repositório.
