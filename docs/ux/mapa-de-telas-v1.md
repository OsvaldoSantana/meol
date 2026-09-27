# Mapa de telas e fluxos do MEOL — v1

*Destino no repositório: `docs/ux/mapa-de-telas-v1.md`.*
*20/09/2026. Etapa 4 (UX) do plano de front. Entrada: [`docs/marca/requisitos-interface-v1.md`](../marca/requisitos-interface-v1.md) (RI-01 a RI-21).*

*Revisão de 26/09/2026 (decisão dele): os códigos deste documento foram renomeados para não colidir com os achados do projeto, que já tinham C- e R- com outro sentido. O número se mantém; muda só o prefixo. As citações de achados do projeto (X-01) ficaram como estão. Notas de revisão no fim.*

| de | para | o que é | faixa neste documento |
|---|---|---|---|
| `R-nn` | `RI-nn` | requisito de interface | 01 a 21 (21 códigos) |

---

## 0. O que este documento é, e o que não é

**É:** a lista de telas, o que cada uma mostra, em que ordem elas aparecem, quais estados cada uma pode assumir e o que acontece quando o motor recusa decidir.

**Não é:** identidade visual, cor, tipografia, espaçamento, ícone ou protótipo navegável. Nada aqui depende do brandbook, que vem depois.

**Status:** `DECISAO_DE_DESENHO`. Nenhuma tela foi testada com pessoas. As hipóteses continuam as da §4 do documento de requisitos.

**Dependência declarada:** este mapa nomeia campos que o motor ainda não emite. A lista deles está na §6 e é a entrada da F0, o contrato de saída. Até a F0 existir, este mapa é desenho sobre campos previstos, não sobre campos reais.

---

## 1. Seis princípios de navegação

1. **Uma decisão por tela.** A tela inicial responde a uma pergunta só: o que fazer este mês.
2. **Três camadas.** Decisão → porquê em uma frase → procedência completa. Ninguém precisa descer para agir; qualquer um pode descer até o fim (RI-01, RI-03).
3. **Cadência mensal.** O ciclo da interface é o do aporte, não o do pregão. Não existe cotação ao vivo nem variação do dia (RI-06).
4. **A recusa é uma tela projetada,** não uma página de erro. Quando falta dado, o MEOL diz o que falta e o que destrava (RI-17).
5. **Nada que o usuário não pediu se mexe sozinho.** Sem notificação para operar, sem lista de populares, sem sequência de dias (RI-06).
6. **O caminho de volta é sempre igual:** toda gaveta de procedência fecha para a tela de onde saiu, sem perder o estado.

---

## 2. Inventário de telas

### Cadastro (só na primeira vez)

| id | tela | o que mostra | requisitos |
|---|---|---|---|
| **O1** | Boas-vindas | a promessa em uma frase, o que o MEOL **não** faz (não promete retorno, não vende produto, não recebe comissão), e o que ele guarda no aparelho | RI-01, RI-13, RI-19 |
| **O2** | Perguntas de intenção | quatro a seis perguntas em linguagem comum ("quanto você aceitaria ver cair sem vender?"), nunca parâmetro técnico | RI-15, RI-07 |
| **O3** | Sua situação hoje | quanto entra por mês, quanto já está guardado, se tem dívida cara. Campos opcionais: o que ficar vazio vira "sem dado", não zero | RI-09, RI-10 |
| **O4** | Carteira (opcional) | três caminhos: importar arquivo, digitar as posições, ou começar do zero. Quem pula continua com o produto inteiro | RI-01, RI-10 |
| **O5** | Escolhas declaradas | o resumo do que o MEOL assumiu por padrão, com o porquê de cada padrão e o botão de alterar | RI-07 |

**Regra do cadastro:** ele pode ser abandonado em qualquer ponto e o MEOL ainda responde. Um usuário que só respondeu a O2 recebe uma decisão de reserva. É o `test_usuario_novo` virando interface.

### Núcleo

| id | tela | o que mostra | requisitos |
|---|---|---|---|
| **T1** | **Decisão do mês** | uma frase de decisão ("este mês, guarde R$ 500 na reserva" ou "aporte R$ 500 em X"), o porquê em uma frase, a data da decisão, o selo de procedência e o botão "executei" | RI-01, RI-02, RI-05, RI-10, RI-12, RI-17, RI-19 |
| **T1b** | Confirmação | o que foi registrado, sem afirmar nada além disso; opção de desfazer antes de gravar | RI-19, RI-08 |
| **T2** | **Carteira e reserva** | progresso da reserva até a meta, fase atual (A, B ou C), desvio em relação ao alvo, e o custo de discordar quando houve desvio. Sem rentabilidade do dia | RI-04, RI-06, RI-09, RI-11, RI-14, RI-20 |
| **T3** | **O porquê** (gaveta, abre de qualquer número) | quatro abas: **funil** (quem eliminou cada rota), **procedência** (fonte, status, data, validade), **limitações** (o que o motor não modela), **e se** (mudar uma escolha declarada e ver a diferença) | RI-02, RI-03, RI-05, RI-10, RI-17, RI-18 |
| **T4** | Enciclopédia | lista de empresas e de rotas, **inclusive as bloqueadas**, com o motivo do bloqueio e o que destrava | RI-01, RI-06, RI-18 |
| **T5** | Registro | histórico das decisões: data, decisão, versão da política, impressão digital do dado. É o que sustenta a auditoria | RI-19, RI-07 |
| **T6** | Método | página pública: como o motor decide, o que ele recusa fazer, e o que ele não modela | RI-13, RI-16 |
| **T7** | Ajustes | perfil e intenções, dados (exportar, importar, apagar), canal oficial declarado, versão | RI-07, RI-16, RI-20 |
| **T8** | Contato | um toque a partir da tela inicial, sem etapas intermediárias, e a instrução de onde reclamar fora do MEOL | RI-21 |

**Navegação:** três destinos fixos — **Decisão** (T1), **Carteira** (T2) e **Mais** (T4 a T8). A gaveta do porquê (T3) não é destino: ela abre por cima de onde o usuário estiver e fecha no mesmo lugar.

---

## 3. Fluxos

### F1 — Primeiro uso de quem nunca investiu

O1 → O2 → O3 → (pula O4) → O5 → **T1**.
A primeira decisão é quase sempre de reserva (RI-09). A frase da camada 2 explica o porquê sem jargão: "sem reserva, uma emergência obrigaria você a vender na pior hora."

### F2 — Primeiro uso de quem já investe

O1 → O2 → O3 → **O4 (importar)** → O5 → **T1**.
Se a importação falhar ou vier incompleta, o MEOL **não inventa**: as posições que não entraram aparecem como "sem dado" em T2, e a decisão de T1 sai com a limitação declarada na camada 3.

### F3 — O ciclo mensal (o fluxo principal)

1. O mês abre. T1 passa a mostrar a decisão do mês, com a data de referência.
2. O usuário lê a decisão (camada 1). Se quiser, abre o porquê (T3).
3. Executa na corretora dele, fora do MEOL.
4. Volta e toca em "executei" (T1b). O estado é atualizado.
5. T5 grava a decisão com data, versão e impressão digital.
6. Se o mês virar sem confirmação, T1 mostra "mês em aberto" e a decisão anterior continua visível. **O MEOL não cobra, não lembra e não notifica** (RI-06, P7).

### F4 — Mudar uma escolha declarada

T7 → escolhe a mudança → o MEOL mostra **o que essa mudança quebraria** (por exemplo, uma meta que deixa de fechar no prazo) → confirma.
Se a mudança **reduz** exposição, vale imediatamente. Se **aumenta**, vale no ciclo seguinte, com o prazo visível na tela (RI-20).

### F5 — Quando a recomendação é de venda

T1 mostra a venda com o **motivo nomeado**:

- **motivo 1** — existe alternativa melhor, já líquida de custo e IR;
- **motivo 2** — a empresa piorou (portões reaplicados, nunca preço);
- **motivo 3** — concentração acima do teto.

Cada motivo abre um porquê diferente em T3. Enquanto o IR de renda variável estiver em `limitacoes_declaradas`, **nenhuma venda sai do motor**, e T1 diz isso em vez de recomendar.

### F6 — Recusa (o fluxo que quase ninguém desenha)

O motor recusa → T1 troca a decisão por **três linhas fixas**:

1. **o que não foi possível decidir** ("não consigo recomendar o aporte deste mês");
2. **por quê, em linguagem comum, com a falha nomeada** ("o balanço da empresa X saiu depois da data de decisão" ou "a fonte de custos está fora do ar");
3. **o que destrava, e de quem é a vez** (do MEOL, da fonte, ou do usuário).

A camada 3 mostra qual insumo bloqueou, com data e fonte. **Nunca aparece um valor padrão no lugar da recusa** (RI-10, RI-17).

---

## 4. Estados que toda tela precisa ter

| estado | quando acontece | o que a tela faz |
|---|---|---|
| **normal** | tudo confirmado | mostra a decisão com selo `COMPLETO` |
| **parcial** | algum insumo é `PARCIAL` | o número vira faixa em linguagem comum (RI-05) |
| **sem dado** | insumo ausente | escreve "sem dado" e o motivo; nenhum zero formatado (RI-10) |
| **recusa** | `InsumoBloqueado` ou equivalente | as três linhas do F6 |
| **desatualizado** | o dado existe mas venceu | mostra a data do dado e diz que a decisão está congelada até a atualização |
| **falha do MEOL** | erro nosso, não do dado | diz que a falha é do MEOL (RI-17) |
| **sem rede** | aparelho offline | a última decisão continua legível; o que depende de dado novo aparece como desatualizado |

---

## 5. O que o registro guarda (T5)

Por decisão: data, decisão tomada, motivo, versão do `politica.yaml`, impressão digital do conjunto de dados, limitações aplicáveis naquele mês, e se o usuário seguiu ou não.

Guardar "seguiu ou não" é o que permite calcular o custo de discordar em T2. É dado do usuário, mora no aparelho, e nunca vira ranking nem comparação com outras pessoas (RI-06).

---

## 6. Campos que o contrato de saída precisa emitir (entrada da F0)

Esta é a lista que a F0 tem de contemplar. Campo que nenhuma tela usa não deveria existir; tela que precisa de campo inexistente não pode ser construída.

| campo | tela | obrigatório |
|---|---|---|
| `decisao.tipo` (reserva, aporte, venda, recusa) | T1 | sim |
| `decisao.valor` e `decisao.destino` | T1 | sim, exceto na recusa |
| `decisao.motivo_curto` (uma frase) | T1 | sim |
| `decisao.data_referencia` | T1, T5 | sim |
| `decisao.status` (`COMPLETO`, `PARCIAL`, recusa) | T1, T3 | sim |
| `recusa.insumo`, `recusa.responsavel`, `recusa.o_que_destrava` | T1, T3 | quando houver recusa |
| `portoes[]` com id, nome, quantas rotas eliminou e o motivo | T3 (funil) | sim |
| `procedencia[]` por número: fonte, status, data de acesso, validade | T1, T3 | sim |
| `limitacoes[]` aplicáveis ao mês | T1 (camada 3), T3 | sim |
| `faixa.min` e `faixa.max` para todo valor `PARCIAL` | T1, T2 | quando `PARCIAL` |
| `reserva.alvo`, `reserva.atual`, `reserva.fase` | T2 | sim |
| `alocacao.alvo[]` e `alocacao.atual[]` | T2 | sim |
| `custo_de_discordar` | T2 | quando houver desvio |
| `venda.motivo` (1, 2 ou 3) | T1, T3 | quando houver venda |
| `impressao.politica` e `impressao.dados` | T5 | sim |
| `rotas_bloqueadas[]` com motivo e o que destrava | T4 | sim |

---

## 7. O que fica de fora da v1

Declarado para não virar omissão (P6): notificações de qualquer tipo, gráficos, comparação com outros usuários, conteúdo educativo fora da decisão, dossiê X-01, conta e cobrança, e sincronização entre aparelhos. Cada um desses entra por decisão própria, não por acúmulo.

---

## 8. Pendências e próximo passo

| pendência | classe |
|---|---|
| **F0 — contrato de saída** com os campos da §6 | trilha de produto paralela; **não bloqueia o motor** *(revisão de 26/09/2026, nota N-F0)* |
| ~~P-WCAG — ler contraste, tamanho de alvo e daltonismo~~ | fechada em 27/09/2026 como P-155: RI-22 a RI-34 nos requisitos de interface v1.1 |
| Teste com pessoas das hipóteses H-C1, H-C2, RI-15 | `DECISAO_DE_DESENHO` |
| Importação de carteira: descobrir quais formatos são viáveis | `DECISAO_DE_DESENHO` |

**Próximo passo: a F0, o esquema do relatório de decisão, com a lista da §6 como escopo.**

- **Por que agora:** o mapa parou exatamente onde começa o contrato. Toda tela daqui depende de campos que o motor ainda não emite.
- **Classe:** trilha de produto paralela (`PLANO.md`, §3-F0), que não disputa o caminho crítico com a P-115 e **não bloqueia o motor**. O primeiro entregável é uma especificação em `docs/ux/`, não código *(revisão de 26/09/2026, nota N-F0)*.
- **O que exige:** desktop, para rodar o motor contra o esquema.
- **O que não exige:** nenhum dado pessoal. O esquema é validado com o usuário novo.

---

## Notas de revisão

*26/09/2026 — trazido do Projeto no claude.ai para o repositório.*

- **N-COD.** C-nn → MC-nn e R-nn → RI-nn, só neste documento (tabela no cabeçalho). Motivo: os achados do projeto sobre o fator, o ajuste de proventos, a moeda e a ordem dos portões já usavam esses mesmos números com os prefixos C- e R-, e outros C/R já existiam em outros arquivos com outro sentido; os instrumentos `achados_ancorados` e `codigos_preservados` contariam todos como achados. Guardado por `auditoria/test_codigos_de_marca.py`.
- **N-F0.** A F0 estava como `BLOQUEIA_O_SISTEMA`, mas o motor decide sem ela: ela bloqueia a **interface**, não o sistema. Decisão dele (26/09/2026): trilha de produto paralela no `PLANO.md`, que não disputa o caminho crítico com a P-115, com uma especificação como primeiro entregável. Registro em [`docs/decisoes/F0-trilha-de-produto.md`](../decisoes/F0-trilha-de-produto.md).
- **N-ORDEM.** 26/09/2026, decisão dele (docs/decisoes/rosto-v1.md): a ordem pesquisa → design → mercado → UX → brandbook vale à risca. Este mapa foi feito antes das etapas de design e mercado e fica como rascunho de UX adiantado, revisado na etapa 4 (mapa v2). Nada dele se apaga.
