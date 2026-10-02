# F0 — o contrato de saída do motor

**Status: `ESPECIFICACAO`. 26/09/2026.** Primeiro entregável da trilha F0 (`PLANO.md` §3-F0;
decisão em [`docs/decisoes/F0-trilha-de-produto.md`](../decisoes/F0-trilha-de-produto.md)).
**Nenhum esquema em código antes de ele ler este documento.**

**Entrada:** a lista de campos da §6 do [mapa de telas v1](mapa-de-telas-v1.md) e os
[requisitos de interface v1](../marca/requisitos-interface-v1.md) (RI-01 a RI-21).

**O que foi lido no motor** (`alocacao/`, `main` em `f5710f2`):

| arquivo | o que emite |
|---|---|
| `alocacao/alocacao.py` → `alocar()` | o dicionário `saida`: `estado`, `portoes` (as `Diretiva` do G0–G2), `pendencias` (`Pendencia`), `universo` (vivos e rejeitados por portão, com motivo), `alvo` (pesos, blocos, alertas, custos), `procedencia` (versão e hash da política, hash dos custos, data da rodada), `incoerencias_de_funcao`, `fora_de_escopo`, e `diretiva` quando o G0, G1 ou G2 encerram |
| `alocacao/alocacao.py` → `_preparar()` | o esqueleto de `saida` e o bloco `procedencia` |
| `alocacao/alocacao.py` → `fase_aporte()`, `g0_match_empregador()`, `g1_divida()`, `g2_reserva()` | a `Diretiva(portao, veredito, destino, valor, memoria)`; a do G2 traz na `memoria` o alvo, o atual e a falta da reserva |
| `alocacao/alocacao.py` → `motor_aporte()` | as ordens do mês (`rota`, `valor`, `peso_atual`, `peso_alvo`), o caixa, os alertas de concentração e a deriva. Devolve `SEM_APORTE` com aporte zero e `SEM_POSICAO` com patrimônio zero |
| `alocacao/alocacao.py` → `custo_de_discordar()` | a diferença de arrasto entre o alvo e uma proposta, em p.p. ao ano |
| `alocacao/alocacao.py` → `reserva_alvo()`, `meses_de_reserva_alvo()` | a meta da reserva em R$ e em meses |
| `alocacao/motor.py` → `val()`, `InsumoBloqueado` | o valor de cada insumo do `custos.yaml`; recusa `NAO_CONFIRMADO` **levantando exceção**, com o motivo e o que bloqueia no texto |
| `alocacao/politica.yaml` → `limitacoes_declaradas` | as limitações do motor, com tipo e pendência; **o `alocar()` não as emite** |

## 1. Como ler a tabela

- **origem**: o módulo e a função que produzem o campo hoje. Três situações:
  - `EXISTE` — o motor já emite, com esse conteúdo;
  - `EXISTE_EM_PARTE` — o dado existe, mas não em todo caso, não nesse formato, ou espalhado;
  - `NAO_EXISTE` — o motor não emite. A §3 diz o que ele precisaria emitir, **sem implementar**.
- **exemplo**: ilustrativo, sem nenhum número do usuário (D-01).
- **RI**: o requisito de interface que o campo atende.

## 2. Os campos

### Decisão (T1)

| campo | tipo | origem | tela | RI | exemplo |
|---|---|---|---|---|---|
| `decisao.tipo` | texto, um de `reserva`, `aporte`, `venda`, `recusa` | `NAO_EXISTE`. Hoje se deduz: `saida["diretiva"].portao == "G2_reserva"` é reserva; `motor_aporte()["status"] == "OK"` é aporte; venda o motor não faz; recusa é exceção | T1 | RI-01, RI-09 | `"reserva"` |
| `decisao.valor` | dinheiro em R$, 2 casas | `EXISTE_EM_PARTE`: `Diretiva.valor` (G0–G2) ou `motor_aporte()["ordens"][i]["valor"]`. **Com patrimônio zero, `motor_aporte` devolve `SEM_POSICAO` e não há valor**, embora `saida["alvo"]["pesos"]` exista | T1 | RI-02, RI-12 | `1000.00` |
| `decisao.destino` | texto (nome da rota) | `EXISTE_EM_PARTE`: `Diretiva.destino` ou `motor_aporte()["ordens"][i]["rota"]`; mesmo buraco do `SEM_POSICAO` | T1 | RI-01 | `"Tesouro Selic"` |
| `decisao.motivo_curto` | texto, até 15 palavras | `NAO_EXISTE`. `Diretiva.veredito` é um rótulo técnico em caixa alta (`"TODO O APORTE PARA A RESERVA"`), não a frase para o leigo | T1 | RI-01, RI-03 | `"sem reserva, uma emergência obrigaria a vender na pior hora"` |
| `decisao.data_referencia` | data (mês de referência) | `NAO_EXISTE`. `saida["procedencia"]["gerado_em"]` é o **dia da rodada**, não o mês a que a decisão se refere | T1, T5 | RI-19 | `"2026-10"` |
| `decisao.status` | texto, um de `COMPLETO`, `PARCIAL`, `RECUSA` | `NAO_EXISTE`. `val()` aceita `PARCIAL` sem registrar que aceitou | T1, T3 | RI-05, RI-10 | `"PARCIAL"` |

### Recusa (T1 camada 3, T3)

| campo | tipo | origem | tela | RI | exemplo |
|---|---|---|---|---|---|
| `recusa.insumo` | texto (caminho do insumo) | `NAO_EXISTE` como campo. `InsumoBloqueado` carrega o contexto no **texto** da exceção (`motor.val()`), e o `alocar()` não a captura | T1, T3 | RI-17, RI-10 | `"custos.tesouro.taxa_b3"` |
| `recusa.responsavel` | texto, um de `dado`, `fonte`, `meol`, `usuario` | `NAO_EXISTE` | T1, T3 | RI-17 | `"fonte"` |
| `recusa.o_que_destrava` | texto | `NAO_EXISTE` como campo. `motor._consequencia()` põe o `bloqueia` do YAML no texto da exceção | T1, T3 | RI-17 | `"a B3 publicar a tabela de custódia do ano"` |

### O porquê (T3)

| campo | tipo | origem | tela | RI | exemplo |
|---|---|---|---|---|---|
| `portoes[]` | lista de {id, nome, rotas_eliminadas, motivo} | `EXISTE_EM_PARTE`: `saida["portoes"]` só tem as `Diretiva` do G0–G2; os rejeitados do G3–G8 estão espalhados em `saida["universo"]` (`fora_atrito`, `fora_status`, `dominados`, `sem_tese`, `sem_carrego`). Não há a contagem por portão num lugar só | T3 (funil) | RI-03, RI-17 | `{id: "G3_atrito", nome: "atrito", rotas_eliminadas: 4, motivo: "custo de entrada come o aporte"}` |
| `procedencia[]` | lista de {numero, fonte, status, data_acesso, validade} | `NAO_EXISTE` na saída. O `custos.yaml` tem fonte, status e `expira` por valor, mas `val()` devolve só o número; a saída leva só os hashes | T1, T3 | RI-07, RI-05 | `{numero: "custódia do Tesouro", fonte: "B3, tabela de tarifas", status: "COMPLETO", data_acesso: "2026-09-05", validade: "2027-09-05"}` |
| `limitacoes[]` | lista de {id, frase, tipo} | `NAO_EXISTE` na saída. Estão em `politica.yaml → limitacoes_declaradas`, sem filtro do que se aplica ao mês | T1 (camada 3), T3 | RI-10, RI-17 | `{id: "ir_na_venda_de_renda_variavel", frase: "o motor não calcula o imposto de uma venda", tipo: "NAO_CONSERTADA"}` |
| `faixa.min`, `faixa.max` | dinheiro em R$ | `NAO_EXISTE` | T1, T2 | RI-05 | `{min: 480.00, max: 620.00}` |

### Carteira e reserva (T2)

| campo | tipo | origem | tela | RI | exemplo |
|---|---|---|---|---|---|
| `reserva.alvo` | dinheiro em R$ | `EXISTE_EM_PARTE`: `Diretiva(G2).memoria["alvo"]` só quando o G2 dispara; com a reserva completa, só pela função `reserva_alvo()`, fora da saída | T2 | RI-09 | `27000.00` |
| `reserva.atual` | dinheiro em R$ | `EXISTE_EM_PARTE`: `Diretiva(G2).memoria["atual"]`, idem; senão `Estado.reserva_atual` (entrada) | T2 | RI-09, RI-14 | `9000.00` |
| `reserva.fase` | texto, um de `A`, `B`, `C` | `NAO_EXISTE`. A fase se deduz do G2 ter disparado, mas não é campo | T2 | RI-09 | `"A"` |
| `alocacao.alvo[]` | lista de {rota, peso} | `EXISTE`: `saida["alvo"]["pesos"]` | T2 | RI-02 | `{rota: "bova11", peso: 0.30}` |
| `alocacao.atual[]` | lista de {rota, peso} | `EXISTE`: `Estado.posicoes` (entrada) e `motor_aporte()["ordens"][i]["peso_atual"]` | T2 | RI-02 | `{rota: "bova11", peso: 0.25}` |
| `custo_de_discordar` | p.p. ao ano | `EXISTE`: `custo_de_discordar()`, chamada à parte, fora do `alocar()` | T2 | RI-11 | `0.12` |

### Venda (T1, T3)

| campo | tipo | origem | tela | RI | exemplo |
|---|---|---|---|---|---|
| `venda.motivo` | número, um de 1, 2, 3 | `NAO_EXISTE`. O motor não vende: `motor_aporte()` só acusa `DERIVA_ESTRUTURAL`, e a limitação `ir_na_venda_de_renda_variavel` impede a venda por desenho | T1, T3 | RI-17 | `3` |

### Registro (T5)

| campo | tipo | origem | tela | RI | exemplo |
|---|---|---|---|---|---|
| `impressao.politica` | hash | `EXISTE`: `saida["procedencia"]["politica_hash"]` e `politica_versao` | T5 | RI-07 | `"1.33.0 · 8c1f…"` |
| `impressao.dados` | hash | `EXISTE_EM_PARTE`: `saida["procedencia"]["custos_hash"]` cobre o `custos.yaml`; não cobre o acervo (CVM, COTAHIST) nem os registros de tese | T5 | RI-07 | `"custos 3e9a… · acervo NAO_EXISTE"` |

### Enciclopédia (T4)

| campo | tipo | origem | tela | RI | exemplo |
|---|---|---|---|---|---|
| `rotas_bloqueadas[]` | lista de {rota, portao, motivo, o_que_destrava} | `EXISTE_EM_PARTE`: o motivo está em `saida["universo"]` por portão; `o_que_destrava` só existe para G7 e G8, em `saida["pendencias"]` (`Pendencia.pergunta`) | T4 | RI-01, RI-18 | `{rota: "hash11", portao: "G7_tese_registrada", motivo: "sem tese registrada", o_que_destrava: "registrar a tese em teses.yaml"}` |

### A contagem

| origem | campos |
|---|---|
| `EXISTE` | **4** — `alocacao.alvo[]`, `alocacao.atual[]`, `custo_de_discordar`, `impressao.politica` |
| `EXISTE_EM_PARTE` | **7** — `decisao.valor`, `decisao.destino`, `portoes[]`, `reserva.alvo`, `reserva.atual`, `impressao.dados`, `rotas_bloqueadas[]` |
| `NAO_EXISTE` | **12** — `decisao.tipo`, `decisao.motivo_curto`, `decisao.data_referencia`, `decisao.status`, `recusa.insumo`, `recusa.responsavel`, `recusa.o_que_destrava`, `procedencia[]`, `limitacoes[]`, `faixa`, `reserva.fase`, `venda.motivo` |
| **total** | **23** campos da §6 do mapa |

## 3. O que o motor precisa emitir — sem implementar

Uma linha por campo que não existe inteiro. É a lista de trabalho de quando ele decidir
construir, não uma decisão de construir.

1. **`decisao`** como objeto único no topo da saída, preenchido nos três caminhos (diretiva do
   G0–G2, ordens do `motor_aporte`, recusa), em vez de a tela deduzir o tipo.
2. **`decisao.valor` e `decisao.destino` com patrimônio zero:** hoje o `SEM_POSICAO` deixa o
   usuário novo sem "quanto e onde", embora os pesos existam. O motor precisa emitir a
   primeira compra a partir de `alvo.pesos` e do aporte.
3. **`decisao.motivo_curto`:** uma frase por veredito e por portão, **como dado** (no YAML),
   com teste de até 15 palavras (RI-01). Nunca montada na interface.
4. **`decisao.data_referencia`:** o mês a que a decisão se refere, distinto do `gerado_em`.
5. **`decisao.status`:** o `val()` registra quando aceitou um `PARCIAL`, e o status da decisão
   é o pior dos insumos que ela usou.
6. **`recusa`:** o `alocar()` captura o `InsumoBloqueado` e devolve `recusa.insumo`,
   `recusa.responsavel` e `recusa.o_que_destrava` como campos, em vez de levantar. O
   `responsavel` é dado no `custos.yaml`, por nó.
7. **`procedencia[]`:** o `val()` passa a registrar, para cada número usado, fonte, status,
   data de acesso e validade, e a saída leva a lista.
8. **`limitacoes[]`:** as `limitacoes_declaradas` que tocam as rotas e os portões usados na
   decisão do mês, com a frase para o leigo.
9. **`faixa`:** para todo valor que dependeu de insumo `PARCIAL`, o mínimo e o máximo, com a
   regra de cálculo declarada.
10. **`reserva`:** alvo, atual e fase em todo caso, não só quando o G2 dispara.
11. **`venda.motivo`:** fica `NAO_EXISTE` enquanto `ir_na_venda_de_renda_variavel` estiver
    aberta; o campo entra no contrato com o valor fixo "o motor não recomenda venda", para a
    T1 dizer isso em vez de silenciar.
12. **`portoes[]` e `rotas_bloqueadas[]`:** um formato único para os nove portões, com a
    contagem e o `o_que_destrava` de cada rejeição, não só do G7 e do G8.
13. **`impressao.dados`:** o hash do acervo usado (CVM, COTAHIST) e o dos registros de tese.

## 4. Campo sem tela não entra

O `alocar()` emite hoje campos que **nenhuma tela usa**, e que por isso **ficam fora do
contrato** (continuam no motor, para auditoria): `incoerencias_de_funcao`,
`universo.interacao_g3_g4`, `alvo.diversificacao`, `alvo.fracao_datada`,
`alvo.custo_pct_aportado`, `alvo.fracao_rv_realizada`, `fora_de_escopo`, e do
`motor_aporte` o `caixa`, o `k_max` e a `nota_bases`. Se uma tela precisar de um deles, o
campo entra no contrato junto com a tela.

## 5. Tela sem campo vira pendência

Telas e requisitos do mapa que **não têm campo na §6** e, pela regra, não podem ser
construídos até ganharem um. Registrados como P-160 no `PENDENCIAS.md`.

| tela ou requisito | o que falta |
|---|---|
| **O5 — escolhas declaradas** | a lista dos padrões que o MEOL assumiu, com o porquê e a origem de cada um (RI-07). Nenhum campo da §6 a carrega |
| **T3, aba "e se"** | mudar uma escolha e ver a diferença exige rodar o motor de novo com outra entrada: é um contrato de **chamada**, não um campo |
| **T4 — empresas** | o mapa lista empresas na enciclopédia; o motor decide rota, não papel (PLANO, M3) |
| **RI-04 — aviso de queda** | o tamanho histórico da queda de cada rota de renda variável, com fonte |
| **RI-11 — líquido contra líquido** | a comparação com a poupança, líquida de IR e de custo |

## 6. O que esta especificação não é

- **Não é esquema.** Os tipos acima dizem o que o campo contém, não a sintaxe (JSON Schema,
  dataclass). A sintaxe vem depois de ele ler.
- **Não é decisão de construir.** A §3 é o tamanho do trabalho, para ele decidir quando.
- **Não foi rodada contra o motor.** A origem de cada campo foi lida no código, não medida
  numa execução. Rodar `alocar()` para o usuário novo (`test_usuario_novo`) e conferir campo
  a campo é o primeiro passo de quem for implementar.
