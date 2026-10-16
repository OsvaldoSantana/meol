# Matriz de aderência: requisitos, evidências e validação

*Leitura de referência: [levantamento aplicado](levantamento-aplicado-2026-10-16.md). Base 2e60f7188b94dfcb999b8074967ba0161d2931e4. Este índice NÃO substitui PLANO, PENDENCIAS, RI nem F0.*

| Código | Capacidade / razão | Status | Evidência | O que precisa ser demonstrado |
|---|---|---|---|---|
| ATF-01 | Uso pessoal versus serviço a terceiros | pessoal declarado; expansão ABERTA | README; PLANO §1 | P-158 e decisão de atividade |
| ATF-02 | Entrada sem posição ou reserva | motor IMPLEMENTADO; UX ESPECIFICADA | alocacao/test_usuario_novo.py; docs/ux/mapa-de-telas-v1.md | F1 com usuários reais |
| ATF-03 | Aporte do mês com porquê | CLI IMPLEMENTADA; uso ABERTO | alocacao/aporte_do_mes.py; docs/uso/aporte-do-mes.md | P-181 do começo ao fim |
| ATF-04 | Interface F0 sem inventar campos | ESPECIFICADA em 23 campos | docs/ux/F0-contrato-de-saida.md | completar emissor e teste de contrato |
| ATF-05 | Ausência e recusa não viram zero | ESPECIFICADO | docs/marca/requisitos-interface-v1.md RI-10/RI-17 | F6 com valores ausentes, incluindo recusa |
| ATF-06 | Acessibilidade / WCAG 2.2 AA | ESPECIFICADA | docs/marca/requisitos-interface-v1.md RI-22 a RI-34 | P-167, contraste, teclado, leitor de tela e pessoas |
| ATF-07 | Experimento de marca versus app | pesquisa IMPLEMENTADA, deploy/uso não comprovado | pesquisa/; docs/marca/ | P-162/P-170 e decisão antes de UX final |
| ATF-08 | Motor no servidor, carteira no aparelho | DECIDIDO, controles ABERTOS | docs/decisoes/P-165-onde-o-motor-roda.md | P-175 prova em logs; P-178 minimização |
| ATF-09 | Correção e eficiência do cache | MEDIDO HISTORICAMENTE | ACHADOS.md §12; alocacao/test_alocacao.py | benchmark atual com entradas alteradas |
| ATF-10 | Latência p95/p99 e capacidade real | NÃO CONFIRMADO | nenhuma meta aprovada | carga e percentis por jornada após endpoint |
| ATF-11 | Ambiente reproduzível | Python 3.11 IMPLEMENTADO no manifesto | pyproject.toml; alocacao/ambiente.py | CI em versão pinada; recorte identificado |
| ATF-12 | Ingestão e hash | código IMPLEMENTADO | fase0/acervo.py; fase0/armazem.py; docs/acervo/ | execução contra armazém externo e frescor |
| ATF-13 | Informação point-in-time | IMPLEMENTADO PARCIALMENTE | fase0/leitor_cvm.py; fase0/test_leitor_cvm.py | P-145/P-53b/P-183 |
| ATF-14 | Uso permitido de B3/NEFIN | documentação de fonte existente | docs/fontes/b3-termos-de-uso.md; docs/fontes/nefin.md | confirmar licenças por uso novo |
| ATF-15 | ML como ranking condicionado | ESPECIFICADO; eficácia NÃO CONFIRMADA | docs/aprendizado/preregistro-ml-v2.md | M2/M3, testes de ML e shadow mode |
| ATF-16 | Motor mantém portões e P6 | IMPLEMENTADO nos domínios existentes | docs/doutrinas.md; alocacao/alocacao.py | bloco C e guardas por classe |
| ATF-17 | Sigilo dos dados do investidor | guardas IMPLEMENTADOS; endpoint ABERTO | alocacao/test_p67_segredo.py; P-165 | P-175, threat model, sentinel logs |
| ATF-18 | Compliance ao atender terceiros | NÃO CONFIRMADO | PLANO P-158; docs/fontes/ | parecer conforme operação efetiva |
| ATF-19 | Ordem real com idempotência e reconciliação | FORA DO ESCOPO APROVADO | alocacao/aporte_do_mes.py | decidir execução antes de desenhar estados |
| ATF-20 | Rotinas automáticas e incidentes | workflows IMPLEMENTADOS em código | .github/workflows/; docs/metricas/ | verificar últimas execuções e alertas |
| ATF-21 | Deploy, SLO, RTO/RPO para serviço público | NÃO CONFIRMADO | decisões atuais tratam protótipo | necessidade, orçamento e estratégia de operação |
| ATF-22 | UX como resultado, não clique | ESPECIFICADO; medição ABERTA | RI-06/RI-13; PLANO §4–5 | sucesso da tarefa, compreensão e erros reais |

**Os caminhos na coluna Evidência são relativos à raiz do repositório**, não links ativos. Uma evidência de código não é validação operacional.

## Restrições de arquitetura

P1: insumo bloqueado nunca vira valor; P2: regra é dado versionado; P3: portões, não score; P4: pré-registro anterior à medição; P5: limites declarados; P6: falta de régua não exclui; P7: automação não depende de lembrar. [Fonte única das doutrinas](../doutrinas.md).

**Sem decisões fictícias:** novos SLOs, uso de ML em produção, cotações streaming, monetização, execução de ordens, novas bases ou stack permanecem EM_ABERTO ou NÃO CONFIRMADOS até escolha/evidência. O [PLANO](../../PLANO.md) mantém a prioridade; esta matriz apenas informa o planejamento.

**Gate da entrega:** nenhum byte do motor, das políticas, dos testes e dos ativos visuais é alterado. Este levantamento e o link no README compõem uma aplicação **documental**; execução de mudanças técnicas exige decisões e validações específicas.