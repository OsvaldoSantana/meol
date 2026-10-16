# Matriz de aderência: requisitos, evidências e validação

*Leitura de referência: [levantamento aplicado](levantamento-aplicado-2026-10-16.md). Base 2e60f7188b94dfcb999b8074967ba0161d2931e4. Este índice NÃO substitui PLANO, PENDENCIAS, RI nem F0.*

| Código | Capacidade / razão | Status | Evidência | O que precisa ser demonstrado |
|---|---|---|---|---|
| ATF-01 | Uso pessoal versus serviço a terceiros | pessoal declarado; expansão ABERTA | README; PLANO §1 | P-158 e decisão de atividade |
| ATF-02 | Entrada sem posição ou reserva | motor IMPLEMENTADO; UX ESPECIFICADA | alocacao/test_usuario_novo.py; docs/ux/mapa-de-telas-v1.md | F1 com participantes e somente dados sintéticos; serviço a terceiros depende de P-158 |
| ATF-03 | Aporte do mês com porquê | CLI IMPLEMENTADA; uso ABERTO | alocacao/aporte_do_mes.py; docs/uso/aporte-do-mes.md | P-181 do começo ao fim |
| ATF-04 | Interface F0 sem inventar campos | ESPECIFICADA em 23 campos | docs/ux/F0-contrato-de-saida.md | completar emissor e teste de contrato |
| ATF-05 | Ausência e recusa não viram zero | ESPECIFICADO | docs/marca/requisitos-interface-v1.md RI-10/RI-17 | F6 com valores ausentes, incluindo recusa |
| ATF-06 | Acessibilidade / WCAG 2.2 AA | ESPECIFICADA | docs/marca/requisitos-interface-v1.md RI-22 a RI-34 | P-167, contraste, teclado, leitor de tela e pessoas |
| ATF-07 | Experimento de marca versus app | pesquisa IMPLEMENTADA, deploy/uso não comprovado | pesquisa/; docs/marca/ | P-162/P-170 e decisão antes de UX final |
| ATF-08 | Motor no servidor, carteira no aparelho | DECIDIDO, controles ABERTOS | docs/decisoes/P-165-onde-o-motor-roda.md | P-175 prova em logs; P-178 minimização |
| ATF-09 | Correção e eficiência do cache | MEDIDO HISTORICAMENTE | ACHADOS.md §12; alocacao/test_alocacao.py | benchmark atual com entradas alteradas |
| ATF-10 | Latência p95/p99 e capacidade real | NÃO CONFIRMADO | nenhuma meta aprovada | carga e percentis por jornada após endpoint |
| ATF-11 | Ambiente reproduzível | Python 3.11 IMPLEMENTADO no manifesto | pyproject.toml; alocacao/ambiente.py | Verificado: 2.317 testes rápidos passaram em Python 3.11, 14 ignorados; job completo não executado (workflow #213) |
| ATF-12 | Ingestão e hash | código IMPLEMENTADO | fase0/acervo.py; fase0/armazem.py; docs/acervo/ | execução contra armazém externo e frescor |
| ATF-13 | Informação point-in-time | IMPLEMENTADO PARCIALMENTE | fase0/leitor_cvm.py; fase0/test_leitor_cvm.py | P-145/P-53b/P-183 |
| ATF-14 | Uso permitido de B3/NEFIN | documentação de fonte existente | docs/fontes/b3-termos-de-uso.md; docs/fontes/nefin.md | confirmar licenças por uso novo |
| ATF-15 | ML como ranking condicionado | ESPECIFICADO; eficácia NÃO CONFIRMADA | docs/aprendizado/preregistro-ml-v2.md | M2/M3, testes de ML e shadow mode |
| ATF-16 | Motor mantém portões e P6 | IMPLEMENTADO nos domínios existentes | docs/doutrinas.md; alocacao/alocacao.py | bloco C e guardas por classe |
| ATF-17 | Sigilo dos dados do investidor | guardas IMPLEMENTADOS; endpoint ABERTO | alocacao/test_p67_segredo.py; P-165 | P-175, threat model, sentinel logs |
| ATF-18 | Compliance ao atender terceiros | NÃO CONFIRMADO | PLANO P-158; docs/fontes/ | parecer conforme operação efetiva |
| ATF-19 | Ordem real com idempotência e reconciliação | FORA DO ESCOPO APROVADO | alocacao/aporte_do_mes.py | decidir execução antes de desenhar estados |
| ATF-20 | Rotinas automáticas e incidentes | workflows IMPLEMENTADOS em código | .github/workflows/; docs/metricas/ | Workflow de testes #213: rápido aprovado; captura e alertas externos ainda não verificados |
| ATF-21 | Deploy, SLO, RTO/RPO para serviço público | NÃO CONFIRMADO | decisões atuais tratam protótipo | necessidade, orçamento e estratégia de operação |
| ATF-22 | UX como resultado, não clique | ESPECIFICADO; medição ABERTA | RI-06/RI-13; PLANO §4–5 | sucesso da tarefa, compreensão e erros reais |

**Os caminhos na coluna Evidência são relativos à raiz do repositório**, não links ativos. Uma evidência de código não é validação operacional.

## 1. Encaminhamento efetivo após revisão do CI — 16/10/2026

Esta revisão **não cria nem reordena pendências**: aplica a prioridade já aprovada no [PLANO](../../PLANO.md), incluindo as condições de entrada estabelecidas no [PENDENCIAS](../../PENDENCIAS.md).

| Janela | Códigos existentes | Decisão de encaminhamento | Condição de aceite mensurável |
|---|---|---|---|
| Próximo avanço real do M1 | P-181 (ATF-03) | A porta CLI está construída; somente a execução de um aporte real pelo responsável conclui a validação de uso. Não simular isso com novo teste sintético. | Roteiro de dez passos realizado; cada fricção descrita sem publicar informações financeiras |
| Primeira frente técnica de M2 | P-145 (ATF-13) | **Não reimplementar a medição** já existente em `medicoes/p145_ponte_2013_2019.py`. O passo necessário é colocar a versão do `isinp.zip` no inventário/armazém autorizado, depois executar a medição. | Cada emissor de 2013–2019 classificado e rótulos ambíguos conferidos; logs públicos sem dado de negociação |
| Bitemporalidade histórica, antes de backtest | P-183 (ATF-13/15) | Medir `DT_RECEB` **por versão** e contar documento-meses ocultos por reapresentações; investigar cópias históricas antes de escolher reconstrução. P-53b depende da ponte P-145. | Medição com n e procedência; teste que reprova uso de informação futura; limitação mantida até veredito |
| Antes de nova conta com série ajustada | P-180 (ATF-12/15) | Cumprir o registro de limitação deliberado para C-02, sem promover a série a confirmada. Não competir com a sequência M2. | Entrada P5 no YAML e teste de limitação; número estatístico não liberado por suposição |
| Somente depois do M2 | P-30, P-17/18, P-58–61, P-64 (ATF-16) | Construir bloco C sobre dados com temporalidade demonstrada. O C-05 apenas **marca** até escolha de limiar depois da contagem já decidida. | Portão executado no universo, recusa com motivo e prova de preservação P6 |
| Trilha de UX previamente aprovada | P-162, P-170, depois P-160/167/156 (ATF-02/04/06/07/22) | Primeiro concluir pesquisa de marca; depois revisar F0 e construir protótipos sobre dados sintéticos. Pesquisa com participantes não autoriza serviço financeiro a terceiros. | Fluxos F1/F3/F6 compreendidos e acessíveis; sem tela baseada em campo inexistente |
| Após endpoint real e proteção de dados | P-175, P-178 (ATF-08/10/17) | Demonstrar ausência de carteira em logs e minimizar request **antes** de operações com dados reais; medir latência e concorrência somente com contrato representativo. | Valores-sentinela não aparecem em telemetria; percentis e carga com n, configuração e recorte |
| Após M3 e pré-registro ML | ATF-15 | Backtest pré-registrado, guardas e modo sombra. Nenhum modelo modifica portões nem pesos por conveniência. | Comparação fora da amostra com multiplicidade e custos; sem evidência, prevalece déficit |
| Se houver decisão de terceiros/ordens | P-158, ATF-18/19/21 | Parecer e escopo operacional **antes** de execução, cobrança, custódia e expansão. | Enquadramento, responsabilidades e controles formalmente definidos |

### 1.1. Evidência observada do CI, com escopo

O [PR #87](https://github.com/OsvaldoSantana/meol/pull/87), na revisão inicial, executou `Testes` #213 com `rapido=success` em Python 3.11. Saíram **2.317 passed e 14 skipped** nas cinco suítes, mais Ruff e mypy aprovados. O job `completo` teve status `skipped` **por desenho do workflow de pull request** (somente `schedule` ou `workflow_dispatch` rodam o completo); não foi reprovado nem executado. Esse resultado valida o estado rápido do commit da revisão inicial, **não** disponibilidade do armazém R2 nem performance, qualidade financeira de ML ou operação com terceiros.

### 1.2. Próxima mudança técnica selecionada, sem execução prematura

A primeira capacidade técnica a desbloquear é a **ponte temporal do M2**, começando pelo insumo da P-145. Como existe medição pronta e a falta está no registro de versão do armazém, não se justifica criar um novo motor, um novo coletor, um benchmark ou uma fila concorrente. **Bloqueio concreto:** envio do `isinp.zip` ao R2 pelo responsável na sessão local; a medição via `medir/` também precisa do token de leitura configurado. Sem esses requisitos, qualquer quantidade de emissores classificados seria inventada.

A parte da P-183 que pode ser pesquisada sem esse envio é medir a perda de cobertura de versões com `DT_RECEB`, mas não se deve alterar a política temporal antes do pré-registro de critérios e da análise do viés. Isso preserva a ordem do PLANO e permite preparar a evidência em paralelo, sem declarar a P-145 concluída.

---

## Restrições de arquitetura

P1: insumo bloqueado nunca vira valor; P2: regra é dado versionado; P3: portões, não score; P4: pré-registro anterior à medição; P5: limites declarados; P6: falta de régua não exclui; P7: automação não depende de lembrar. [Fonte única das doutrinas](../doutrinas.md).

**Sem decisões fictícias:** novos SLOs, uso de ML em produção, cotações streaming, monetização, execução de ordens, novas bases ou stack permanecem EM_ABERTO ou NÃO CONFIRMADOS até escolha/evidência. O [PLANO](../../PLANO.md) mantém a prioridade; esta matriz apenas informa o planejamento.

**Gate da entrega:** nenhum byte do motor, das políticas, dos testes e dos ativos visuais é alterado. Este levantamento e o link no README compõem uma aplicação **documental**; execução de mudanças técnicas exige decisões e validações específicas.