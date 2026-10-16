# Levantamento técnico e funcional aplicado ao MEOL

*16/10/2026 | AVALIAÇÃO ARQUITETURAL, não aprovação de novas funcionalidades | commit-base: 2e60f7188b94dfcb999b8074967ba0161d2931e4 | árvore Git: b2ba68c06176828a3564ae493885a5c4bc56eb74.*

Este levantamento aplica as dimensões de produto, UX/UI, desempenho, ML, dados, segurança, operação e negócio ao sistema **real**, e não a uma fintech hipotética. Não altera as [sete doutrinas](../doutrinas.md), o [PLANO](../../PLANO.md), a [fila de pendências](../../PENDENCIAS.md), o motor, a política ou os pré-registros. A [matriz de aderência](matriz-de-aderencia.md) relaciona capacidade, evidência, lacuna e prova necessária.

## 0. Cobertura da auditoria, método e limites

Antes desta proposta, todos os bytes dos **495 arquivos versionados, totalizando 7.110.982 bytes**, foram lidos de um ZIP fornecido pelo responsável. A árvore Git reconstruída reproduziu b2ba68c06176828a3564ae493885a5c4bc56eb74, exatamente a árvore do commit-base. O inventário contém 203 Python, 176 Markdown, 29 CSV, 21 YAML, 8 YML, 5 JSON, 5 HTML, 5 JavaScript, 3 SQL, 12 PNG, 10 WOFF2 e 18 arquivos diversos. Todos os Python passaram no parser AST; CSV/YAML/JSON/HTML foram inspecionados pelos parsers de formato, imagens foram decodificadas, fontes foram abertas; 208 links relativos de Markdown verificaram existência dos respectivos destinos. Seis PNG do experimento são cópias byte a byte dos estímulos originais.

**Limite da evidência:** cobertura de bytes e sintaxe **não** certifica correção semântica de 2.792 funções, eficácia financeira, conformidade jurídica, execução do CI ou utilização real. O acervo remoto R2 e o estado financeiro privado não vieram no ZIP; sua situação operacional segue NÃO CONFIRMADA por esta auditoria.

O projeto requer Python 3.11. A auditoria dispõe de 3.13; a instalação de 3.11 falhou por DNS. Uma tentativa exploratória de testes com 3.13 falhou em pré-condições que exigem metadados Git e tags ausentes de exportações ZIP. **Suíte declarada completa: NÃO CONFIRMADA**; requer CI em 3.11 e, para testes marcados, o acervo.

**Status:** IMPLEMENTADO = existe código; ESPECIFICADO = contrato/decisão sem prova de uso; MEDIDO HISTORICAMENTE = observação anterior, não SLO; ABERTO = falta decisão/implementação; NÃO CONFIRMADO = evidência insuficiente. Essas categorias não são intercambiáveis.

## 1. Produto e escopo funcional

**Relevância:** uma calculadora pessoal, um recomendador a terceiros, um executor de ordens e um gestor automatizado possuem riscos e workflows diferentes. **Estado:** o [README](../../README.md) declara sistema pessoal de análise e aporte, sem ordens, otimização genérica nem consultoria a terceiros. O [PLANO](../../PLANO.md) diferencia M1 (código pronto, mas ainda não usado do início ao fim), M2 (dados próprios, em andamento), M3 (régua da empresa depende de M2) e M4 (capturas previstas/implementadas). A porta em [aporte_do_mes.py](../../alocacao/aporte_do_mes.py) calcula destinos e explica, não compra.

**Riscos:** aplicar ao projeto um escopo comercial inexistente; tratar sugestão como execução; lançar para usuários externos sem responsabilidades definidas; afirmar que M1 está validado porque os testes sintéticos passam.

**Decisões:** terceiros, remuneração, corretoras, execução e custódia são **NÃO CONFIRMADOS**. A P-158 exige parecer jurídico antes de terceiros. A primeira prova de utilidade permanece o uso efetivo P-181 conforme [roteiro](../uso/aporte-do-mes.md), sem tornar saldo pessoal público.

## 2. UX/UI, fluxos e visualização de finanças

**Relevância:** o produto prioriza QUANTO, PARA ONDE e POR QUÊ, com procedência e recusa compreensível. **Estado:** já há [RI-01 a RI-34](../marca/requisitos-interface-v1.md), [mapa O1–O5, T1–T6, F1–F6](../ux/mapa-de-telas-v1.md) e [contrato F0](../ux/F0-contrato-de-saida.md) com 23 campos; vários campos seguem sem emissor. Os [estímulos visuais](../marca/direcoes/README.md) e a [página de pesquisa](../../pesquisa/README.md) são instrumentos de marca, **não aplicação financeira funcional**. A ordem pesquisa → design → mercado → UX → brandbook já está [decidida](../decisoes/rosto-v1.md).

**Riscos:** ausência parecer zero; estado PARCIAL aparentar exatidão; fluxo de venda parecer implementado; fonte de preço sem data; gráfico sem equivalente textual; confirmação afirmar mais do que ocorreu; onboarding exigir carteira de quem ainda não tem.

**Decisões e provas:** completar especificação F0 e mapa por P-160; testar F1 (iniciante), F2 (com carteira), F3 (mês), F4 (mudança), F5 (venda futura) e F6 (recusa) com dados sintéticos; usar tarefas reais para medir compreensão e erro. WCAG 2.2 AA, teclado, leitor de tela, zoom e contraste seguem RI e P-167, com testes automatizados e humanos. Não iniciar novo design system paralelo ao existente.

**Tempo real:** o [mapa v1](../ux/mapa-de-telas-v1.md) estabelece cadência **mensal**, sem cotação ao vivo ou notificações que induzam negociação. Streaming não é melhoria aprovada apenas porque é tecnologicamente possível.

## 3. Arquitetura de execução e contratos

**Relevância:** a experiência rápida exige interface desacoplada do motor e transmissão mínima dos dados pessoais. **Estado:** Python 3.11 e módulos de alocação/dados já estão implementados; o [P-165](../decisoes/P-165-onde-o-motor-roda.md) aprovou servidor **sem armazenar o estado financeiro do usuário**, que continua no aparelho (B′). Contrato de retorno F0 aprovado com ressalvas; entrada mínima permanece P-178; prova de ausência de dados nos logs é P-175.

**Riscos:** backend supostamente stateless vazando request em telemetria; frontend recalculando motor com regras diferentes; APIs ligadas diretamente ao formato interno Python; migrar para microsserviços sem necessidade; confundir a infraestrutura do experimento de marca com a do produto.

**Decisões:** primeiro fechar request/response e erros versionados, minimização da entrada e prova sentinela de não retenção. Stack de frontend, hospedagem, região, cache de processo e estratégia de concorrência dependem de comparação real; nenhuma migração para C#, Go, Rust ou serviços distribuídos é demonstradamente necessária. O padrão inicial recomendável é modularidade com separação de captura/treino das requisições interativas.

## 4. Desempenho e escalabilidade

**Relevância:** latência de tela, validação, rede, carregamento de política, cálculo e inferência afetam o usuário em momentos distintos. **Estado:** [ACHADOS.md §12](../../ACHADOS.md) relata S-01/S-02 e melhora histórica de alocar() de **9,79 ms para 2,75 ms** após corrigir cache que também produzia resultados errados. Houve medições históricas para 25, 100, 400 e 800 rotas, mas não são dados atuais de p95 de API, tampouco prova multiusuário. O carregamento YAML foi apontado como custo relevante para chamadas repetidas, sem autorização para inserir cache ingênuo.

**Riscos:** otimização alterar correção; cache não incluir conteúdo da política/custos, como no S-02; parse YAML repetido; sobrecarga de rede; visualização pesada; concorrência degradar latências de cauda; inferência síncrona bloquear a decisão; falsos SLA vindos de benchmark local.

**Decisões e verificações:** antes de aprovar números, medir cenário de usuário novo, carteira grande, insumo recusado, política alterada, várias requisições e falha de fonte. Registrar p50/p95/p99 e duração ponta a ponta, CPU, memória, concorrência, throughput e custo por chamada; no web, LCP/INP/CLS em dispositivos reais. **Orçamento de latência, quantidade de usuários e SLO: NÃO CONFIRMADOS.** Definir gatilhos de regressão somente com baseline reproduzível. Não usar cache como fonte autoritativa de valor financeiro.

## 5. Machine Learning, pré-registro e inferência

**Relevância:** previsão/ranking não pode substituir regras financeiras nem ser tratada como garantia de retorno. **Estado:** [pesquisa e plano ML](../aprendizado/pesquisa-e-plano-ml-1.md) e [pré-registro v2](../aprendizado/preregistro-ml-v2.md) fixam alvo, seleção temporal, variáveis, modelos candidatos (incluindo multifator, LightGBM, TabPFN e conjunto), métricas, família de hipóteses, testes de vazamento, manutenção e modo sombra. [insumo_ml.py](../../fase0/insumo_ml.py) já fixa versões/impressões da fonte. **ML ordena entre elegíveis e NÃO define pesos do aporte.**

**Riscos:** look-ahead, viés de sobrevivência, contabilidade reapresentada, ajuste inválido de proventos, escolha retrospectiva de modelo, overfitting, mudança de regime, drift e linguagem causal indevida ao explicar scores. A pesquisa pré-registrada não é demonstração de ganho econômico.

**Decisões e verificações:** concluir dependências M2/M3 e dados point-in-time; executar nove testes de ML-1 sobre dados sintéticos, validar fora da amostra e comparar contra déficit/multifator com custos; conservar o orçamento de multiplicidade, hashes e política de mudança. Inferência/retreino não serão colocados no caminho crítico do aporte sem medição. Se critério operativo não for satisfeito, prevalece o déficit, com ML em sombra. **Eficácia e desempenho de inferência: NÃO CONFIRMADOS.**

## 6. Dados de mercado, integridade e temporalidade

**Relevância:** decisões e testes financeiros dependem do que realmente era conhecido em cada data, não do arquivo mais recente. **Estado:** capturas CVM/B3/NEFIN estão declaradas em [captura_cvm.yml](../../.github/workflows/captura_cvm.yml), com registros em [docs/acervo](../acervo/); [armazem.py](../../fase0/armazem.py) e [acervo.py](../../fase0/acervo.py) implementam endereçamento/conferência de conteúdo; [leitor_cvm.py](../../fase0/leitor_cvm.py) implementa parte do as-of. O leitor não reconstrói, por si, conhecimento histórico anterior à primeira captura.

**Riscos:** misturar tempo da informação, tempo de publicação e de captura; usar balanço corrigido futuramente no passado; confundir preço bruto com ajustado; captar sem retenção licenciada; substituir ausência por zero. Dados brutos externos e licenças comerciais não foram reproduzidos neste ZIP.

**Decisões:** caminho crítico M2: P-145, P-53b/P-183 e P-30. Separar evento, publicação, captura e vigência; preservar hashes e origem. Respeitar termos [B3](../fontes/b3-termos-de-uso.md) e [NEFIN](../fontes/nefin.md); não publicar seus bytes como se públicos fossem. Necessidade e custo de feeds comerciais intradiários: NÃO CONFIRMADOS.

## 7. Segurança, privacidade e compliance

**Relevância:** o serviço manipula informações financeiras, mesmo que o estado não seja persistido. **Estado:** estado pessoal fica fora do Git e tem guarda em testes; a pesquisa [Vercel/Supabase](../../pesquisa/README.md) possui contratos específicos e guarda respostas de pesquisa, não a carteira financeira. O modelo B′ exige P-175, ainda aberta, e P-178. O enquadramento para terceiros exige P-158.

**Riscos:** logs de provedor guardarem request, credenciais expostas, autorização entre usuários incorreta, retenção inesperada, tratar ausência de banco como isenção da LGPD ou usar fluxos sem parecer regulatório.

**Decisões e provas:** modelagem de ameaças, criptografia no transporte, minimização, controle de acesso, teste com valores-sentinela em logs/erros/métricas e revisão de dependências. Para terceiros, avaliar concretamente CVM 19/20/21/30/35/50 e LGPD conforme a atividade — **aplicabilidade específica NÃO CONFIRMADA**, não automática. Consultoria, intermediação e gestão delegada exigem desenhos distintos. Parecer antes de abertura a usuários externos.

## 8. Confiabilidade, integridade transacional e riscos

**Relevância:** estados de recomendação, intenção e ordem não são equivalentes. **Estado:** o motor [aporta no plano](../../alocacao/aporte_do_mes.py), mas **não executa** compra/venda. O catálogo e os portões recusam insumo ausente; P-179 documenta regra de lote. F0 e P-123 preveem venda futura, ainda sem execução comprovada.

**Riscos:** cálculo monetário com precisão inadequada; propostas não executáveis; indisponibilidade de provedores; se ordens forem autorizadas futuramente, duplicação por retry, liquidação parcial e posições inconsistentes.

**Decisões:** testar invariantes monetários, lote, custos, recusa e procedência no escopo atual. **Somente após aprovação expressa de execução**, especificar idempotência, autorização, máquina de estados, intermediário como fonte autoritativa, reconciliação, limites e rollback operacional. Não construir infraestrutura transacional fictícia antes dessa decisão.

## 9. Observabilidade, infraestrutura e operação

**Relevância:** disponibilidade do produto inclui a qualidade/frescor das fontes, não só HTTP 200. **Estado:** existem workflows de captura, teste, mutação e medição, com rotinas previstas por P7. Presença de YAML de CI não prova êxito da última execução. O deploy do experimento de marca não equivale à hospedagem do motor.

**Riscos:** cron suspenso, falhas silenciosas, telemetria expondo patrimônio, alerta sem responsável, custo inesperado e recuperação não testada.

**Decisões:** medir execução e idade por fonte, taxa de recusa por motivo sem payload pessoal, latência, saturação, número de entradas com erro, tempo de fila e custo. Definir RTO/RPO, disponibilidade, rollback, on-call e região após decisão sobre operação para terceiros. Não agendar lembretes humanos como substituto de controle automático.

## 10. Classes de ativo e modelo financeiro

**Relevância:** ações, ETFs, Tesouro, CDB/LCI/LCA, FII, fundos, derivativos, câmbio e cripto têm regras distintas de lote, liquidez, marcação, custo e imposto. **Estado:** [catálogo](../../alocacao/catalogo.yaml) e [política](../../alocacao/politica.yaml) distinguem funções, status e rotas. A P6 proíbe excluir ativo apenas porque falta régua; pode ficar no universo sem peso, com motivo.

**Riscos:** confundir taxa anual e custo fixo, preço executável e preço teórico, retorno bruto e líquido, valor sem dado e zero; abstração genérica esconder alavancagem e liquidação.

**Decisões:** matriz por classe com suporte para listar/analisar/simular/selecionar/vender/executar, sinalizando separadamente IMPLEMENTADO, BLOQUEADO e NÃO MODELADO; teste de precisão e fonte por instrumento. Derivativos, execução internacional e cripto em tempo real não são funcionalidades aprovadas só porque constam do universo conceitual.

## 11. Negócio, ética e métricas

**Relevância:** sucesso em investimentos é compreensão e qualidade de decisão, não número de cliques, ordens ou receita por giro. **Estado:** o projeto é pessoal, com identidade em pesquisa; não há evidência de clientes pagantes, receita recorrente, corretagem ou estratégia com alfa líquido operacional comprovado.

**Riscos:** gamificação induzir excesso de operações, padrão interpretado como conselho, benchmark incompatível, prometer performance preditiva não medida.

**Decisões:** testar conclusão de F1/F2/F3/F6, tempo de decisão, compreensão das recusas, exatidão dos números e primeiro uso M1. Para modelos futuros, comparar estatística fora da amostra e retorno líquido por método válido. Monetização e posicionamento competitivo como produto comercial: NÃO CONFIRMADOS.

## 12. Testes e critérios de aceite

**Relevância:** testes unitários não cobrem rede, pessoas, escala nem validade estatística. **Estado:** módulos trazem testes sintéticos, verificações de arquivos, segurança, CI e contratos; [tools/testar.py](../../tools/testar.py) orquestra o recorte declarado. A execução de toda a suíte no ambiente 3.11 e com acervo não foi confirmada nesta auditoria.

**Riscos:** aceitar uma árvore exportada ZIP como clone Git; confundir AST OK com código correto; ignorar testes lentos, privados ou de acervo; inferir segurança de frontend de screenshot; comparar resultados de Python com versões não pinadas.

**Decisões:** manter testes existentes e, para cada alteração futura, acrescentar golden snapshot de contratos, teste negativo de insumo e teste de regressão real. Para UI, Playwright + axe + pessoas. Para performance, ensaio representativo no mesmo contrato de entrada/saída; para ML, provas sintéticas e preregistro. Nenhum teste novo é criado sem funcionalidade nova e critério de falha explícito.

## 13. Governança das decisões e custo de mudança

**Relevância:** as sete doutrinas são restrições de arquitetura, não slogans. **Estado:** [CLAUDE.md](../../CLAUDE.md) §9 exige análise de impacto, testes, snapshots, lint, atualização das pendências e controle de versão quando mudar política; [PLANO](../../PLANO.md) decide ordem; [fila](../../PENDENCIAS.md) distingue sistema e dados de usuário.

**Riscos:** duplicar regra em código e YAML (P2), usar score agregado (P3), mudar hipótese depois do resultado (P4), esconder limitações (P5), excluir por ignorância (P6), depender de rotina manual (P7) ou fazer engenharia de UI competir com M2.

**Decisões:** toda mudança de stack/domínio deve registrar alternativas, efeitos, dono, gatilho e teste; não atribuir ao responsável decisão que ele não deu. **Este documento não cria códigos P-nnn, não reordena o caminho crítico e não altera política ou fonte de dados.**

## 14. Sequência e gates de evolução

1. **Primeiro uso M1** — medir fluxo real P-181, sem tornar dados pessoais públicos.
2. **M2 no caminho crítico** — temporalidade, ponte e bloco C conforme PLANO. Não permitir que ML salte M2/M3.
3. **Trilha do rosto** — concluir pesquisa de marca, revisar F0/mapa, produzir protótipo sintético e testar com usuários; B′ exige prova de não retenção antes de dados reais.
4. **Baseline de UX/performance** — com aplicação executável, medir p50/p95/p99, estabilidade e custo. SLO só depois de medição/decisão.
5. **ML condicionado** — concluir dados point-in-time, testes do pré-registro e modo sombra; sem prova, manter déficit.
6. **Terceiros/execução** — decisão futura separada, condicionada a responsabilidade jurídica, segurança, contratos e fluxo transacional específico.

**Critério de aceite deste levantamento:** ligação explícita entre requisito e evidência do MEOL; distinção de implementado/especificado/não confirmado; nenhuma reescrita de metodologia existente; todos os arquivos do motor, YAML, testes e ativos preservados byte a byte.