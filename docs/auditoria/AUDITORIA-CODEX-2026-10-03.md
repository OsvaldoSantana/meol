# Auditoria do Codex de 03/10/2026 — o registro

*Registrada em 04/10/2026 pelo Claude (Cowork), a pedido dele. **Autor do conteúdo: Codex
(outra IA).** O original chegou como anexo, `AUDITORIA-CODEX-2026-10-03.md`, com 1.074 linhas e
sha256 `a3fa0b864b40211065de26ff95cdc8c7ce1d20e0953c501e776d267a9caa6351`. Abaixo do traço está o texto original,
com uma única mudança: o nome dos três achados.*

## De/para dos códigos

`A-01`, `A-02` e `A-03` já são achados deste projeto desde 11/09/2026, da primeira corrida real
da Fase 0 (`ACHADOS.md`): `B3SA3` virou `BSA`; o formato do endpoint registrado errado; o
código da emissora que muda e deixa a história para trás. O Codex numerou os dele a partir de
`A-01`. Registrados com o nome original, os três teriam duas definições cada, e toda citação de
`A-01` no código passaria a ter dois endereços com sentidos diferentes. Nenhum instrumento do
repositório acusava isso: o `achados_ancorados` mede que o código tem endereço, não que o
endereço é um só. A guarda nova é `auditoria/codigos_redefinidos.py`.

Os três seguem a família CX, que já tem CX-01 a CX-03 (auditoria do Codex do mesmo dia).

| no original (Codex) | aqui | o que é | conserto |
|---|---|---|---|
| `A-01` | CX-04 | a entrada aceita `NaN`, infinito e booleano como dinheiro | passo 1 da P-181 |
| `A-02` | CX-05 | o teste do modelo em branco confere o dicionário de dados, não os problemas | passo 2 |
| `A-03` | CX-06 | a guarda de política fixa aceita `7e+1` e `7_0` | passo 3 |

**A troca é mecânica e reversível:** as 19 ocorrências de `A-01`, `A-02` e `A-03` do original
viraram CX-04, CX-05 e CX-06, e nenhuma outra palavra mudou. Desfazer a troca neste corpo
devolve o original byte a byte (conferido no PR que registrou este arquivo).

**Conferido contra o `main` de 04/10 (`0247a21`):** as linhas citadas continuam as mesmas
(`estado_io.py:31-48`, `test_usuario_novo.py:222-233`, `test_alocacao.py:311-328`), e as três
provas da §9.9 falham nele como a auditoria transcreve. As seções 3 a 5 (fontes, roadmap,
inovações) são proposta do Codex, não decisão do projeto.

---

# AUDITORIA CODEX — MEOL / Bastter

Iniciada em 03/10/2026; consolidada em 04/10/2026. Nome do documento preservado conforme o pedido.

**Árvore medida:** `97bdc5676a5e98eab9032884b53ee205cfd7c047`.
**Checkout observado na retomada:** `232ca4b882fb85cf7b8f07654db00cdfc1d5dc4b`.
`git merge-base --is-ancestor 9c424b4 HEAD` retornou código 0.
A rodada completa abaixo pertence à árvore medida; não é certificação do checkout posterior.
As funções dos três achados foram comparadas por AST entre esses commits e são idênticas
(n=3 funções; comando e saída no apêndice). A mudança posterior da P-164 foi considerada
para não repetir como aberto um problema já implementado.

O checkout do dono permaneceu somente para leitura. Execuções e propostas ficaram na réplica
`C:/Users/OSVALD~1.JUN/AppData/Local/Temp/meol-descoberta-97bdc56`.
É uma cópia temporária isolada, em caminho Windows, e não o caminho literal Linux
`/tmp/meol-prova` pedido originalmente. O relatório também está fora da raiz do projeto.
Não houve commit, PR ou aplicação das propostas no checkout do dono.

## 1. Sumário executivo e alcance do instrumento

**Foram confirmados três defeitos, com contraexemplos executados. Não foram provados três P0.**
O defeito de entrada numérica é P1; as duas guardas ineficazes são P2. Na régua inicial
da frente C, correspondem a S1, S2 e S2. A ampliação posterior do pedido incluiu a entrada
do motor; o primeiro achado extrapola a frente C original.

- A entrada aceita `NaN`, infinito e booleano em campos financeiros. O `NaN` chega ao
  motor e termina em `ValueError`; o booleano é convertido em unidade monetária.
- O teste que promete recusar o modelo em branco verifica as chaves do dicionário de
  dados, porque desempacota o retorno de `validar()` na ordem errada.
- A guarda contra política fixa no Python aceita `7e+1` e `7_0`, embora rejeite
  `70.0`. As três escritas representam o mesmo valor no contraexemplo.

### O que foi lido

Leituras integrais iniciais: `CLAUDE.md`, `docs/doutrinas.md`, `docs/estado.md` e
`docs/auditoria/analise-auditoria-otimizacoes-2026-09-24.md`. Também foram lidos integralmente
`PLANO.md`, `PENDENCIAS.md` e `ACHADOS.md`, conforme o pedido posterior.
A leitura dos livros grandes foi feita em partes; buscas temáticas conferiram os candidatos
contra o histórico de pendências fechadas.

Foram lidos `pyproject.toml`, `tools/testar.py`, `.gitignore`, o workflow de testes,
`estado_io.py`, `conftest.py`, `demo_aporte.py`, `aporte.py`,
`auditoria/chaves_orfas.py`, a guarda de duplicatas e os trechos vizinhos dos testes
questionados. Os YAML `custos`, `politica`, `perfil`, `catalogo`, `teses` e
`estado.exemplo` foram lidos integralmente. `instituicoes.yaml` entrou na medição
automática, sem leitura integral. O motor e os demais testes foram examinados por trechos,
AST e buscas; **não afirmo ter lido integralmente todos os arquivos das suítes**.

Na retomada, comparei os arquivos alterados e li as novas pendências relevantes.
As linhas de código dos achados continuam iguais no checkout posterior.
A listagem de nomes, isoladamente, não foi tratada como leitura de conteúdo.

### O que ficou fora

Não abri `alocacao/estado.yaml`, arquivos em `data/` ou acervo bruto. Não medi quantidade
de ZIPs efetivamente presentes no disco, cobertura real de COTAHIST, saldos, ordens pessoais,
nem integridade do byte bruto contra os manifestos. Metadados versionados em `docs/acervo/`
foram contados sem seguir seus caminhos para o acervo. Essa exclusão decorre da regra D-01
do usuário; não é uma falha de acesso nem prova de ausência.

Não executei testes `slow`, `privado` ou `acervo`, captura real, publicação, backtest
financeiro, benchmark de decisões realizadas, navegação com participantes ou integração com
corretora. O teste arquivado em `docs/historico/pesquisa-custos-2026-08/calc/` não integra
as cinco suítes vivas executadas.

### Ambiente e rodada inicial

Comando exigido de instalação, adaptado ao launcher Windows:
`py -3.11 -m pip install ".[dev,lint,paralelo]"`.
A primeira tentativa restrita falhou:
`ERROR: No matching distribution found for setuptools>=40.8.0`.
A repetição autorizada fora do sandbox terminou em `Successfully installed meol-1.18.0`.
As dependências desses extras já estavam satisfeitas; a instalação foi conferida depois
da rodada inicial, sem repetir o orquestrador. Essa diferença de ordem está declarada.

`py -3.11 tools/testar.py` foi executado **uma vez**, com
`PYTHONDONTWRITEBYTECODE=1`, na réplica de `97bdc56`.
Transcrição do resumo — **recorte do CI, sem acervo, estado pessoal e testes slow**:

```text
recorte: -m "not slow and not privado and not acervo" (o do push; 5-B.15)
alocacao       OK    552 passed in 41.92s [42s]
fase0          OK    539 passed, 10 skipped in 16.84s [17s]
auditoria      OK    638 passed, 1 skipped in 19.09s [20s]
tools          OK    141 passed, 1 skipped in 16.26s [17s]
medicoes       OK    5 passed in 6.71s [7s]
ruff           OK    [0s]
mypy alocacao  OK    [0s]
mypy fase0     OK    [10s]
mypy auditoria OK    [7s]
mypy tools     OK    [8s]
mypy medicoes  OK    [1s]
```

Total aritmético: **1875 passed e 12 skipped**, n=5 suítes, uma execução por suíte no
orquestrador. Comando de totalização: `sum([552,539,638,141,5])` e
`sum([0,10,1,1,0])`. Isso não inclui a população excluída pelos marcadores.

A execução separada por pasta, pedida para durações, usou:
`py -3.11 -m pytest -o addopts='' -q --durations=10 --durations-min=1.0 -m 'not slow and not privado and not acervo' -p no:cacheprovider --tb=short`.
O `addopts` foi neutralizado para preservar o resumo, sem duplicar `-q`.

| Suíte | Resultado na réplica, recorte do CI | Duração | n |
|---|---|---|---|
| alocacao | 552 passed, 22 deselected | 48.87s | uma rodada |
| fase0 | 539 passed, 10 skipped, 41 deselected | 41.54s | uma rodada |
| auditoria | 638 passed, 1 skipped, 18 deselected | 47.14s | uma rodada |
| tools | 141 passed, 1 skipped | 19.39s | uma rodada |
| medicoes | 5 passed | 0.07s | uma rodada |

Os tempos não são benchmark repetido nem medida de regressão. Não há base nesta amostra
para chamar a suíte de “cronicamente lenta”. O apêndice transcreve os testes mais lentos,
inclusive os ocultados pelo limiar solicitado.

### Lacunas de produto observadas, sem recadastrá-las como bugs novos

- **Porta de produto:** `alocacao/responder.py` e `alocacao/aportes.yaml` não constam
  da árvore medida. Isso não prova que o motor não responda: um cadastro sintético válido
  produziu a diretiva `G2_reserva` (n=1). `demo_aporte.py:11` e `:17` montam
  estados fictícios. A F0 reconhece campos de saída ainda inexistentes; falta a ligação
  de produto descrita em `docs/ux/F0-contrato-de-saida.md:58`, não um nome de arquivo
  obrigatório por si só.
- **Conhecimento no tempo:** `PLANO.md:260-264` declara bitemporalidade desenhada e
  ainda sem implementação. Busca por `dt_disponivel|sys_from|sys_to|asof|merge_asof`
  nos módulos operacionais de `fase0/` e `alocacao/` não encontrou ocorrência.
  É evidência de alcance limitado, não demonstração de que qualquer algoritmo equivalente
  esteja ausente. Nenhum backtest foi executado para promover vazamento de futuro a bug.
- **Registro da decisão:** o histórico com data, motivo, impressão dos dados e adesão está
  especificado em `docs/ux/mapa-de-telas-v1.md:131-135`. A pesquisa desta auditoria
  não demonstra sua persistência operacional. Contrafactual e benchmark Real × Motor × Nada
  ficam como propostas de produto, não resultados existentes.

**P-164 não é uma lacuna atual deste relatório.** Era um bloqueio na árvore medida, mas o
checkout posterior implementou `_primeiro_aporte` e adicionou
`alocacao/test_p164_primeiro_aporte.py`. Li a alteração; não atribuo a ela os números da
rodada completa antiga. P-179, sobre o mínimo do Tesouro, já está registrada e não foi
reproduzida aqui.

### Riscos de dados que delimitam a conclusão

- O endpoint de eventos B3 sem contrato público é risco já documentado em
  `docs/fontes/pesquisa-bases-e-apis-2026-09.md:19`; a existência do coletor e de cron
  não prova disponibilidade futura. Não foi constatada perda de evento nesta auditoria.
- A janela pública curta da ANBIMA é assunto da P-52. A consulta pública de IMA-B 5
  informa últimos cinco dias úteis no resultado indexado da fonte; não extrapolei essa
  janela como limite contratual de todas as APIs Feed.
- A CVM altera arquivos sob o mesmo nome, motivo do manifesto em
  `fase0/manifesto_cvm.py:28`. Os manifestos lidos têm hashes com formato válido;
  sem abrir o acervo não há prova de correspondência byte a byte nem de cobertura atual.

## 2. Tabela de achados

| ID | Arquivo:linha, base e checkout posterior | Sev. | Categoria | Descrição | Correção proposta | Teste |
|---|---|---|---|---|---|---|
| CX-04 | alocacao/estado_io.py:31-48 | P1 / S1 | erro | Conversão aceita não finitos e booleano como dinheiro | Recusar bool antes de int/float; exigir finitude em todos os caminhos de conversão | três entradas rejeitadas por carregar |
| CX-05 | alocacao/test_usuario_novo.py:222-233 | P2 / S2 | falha_silenciosa | Guarda do modelo em branco verifica dados em vez de problemas | Corrigir a ordem do desempacotamento | dois validadores mutantes precisam derrubar a guarda |
| CX-06 | alocacao/test_alocacao.py:311-328 | P2 / S2 | falha_silenciosa | Regex deixa passar política fixa em notações válidas de Python | Ler constantes por AST no mesmo recorte do módulo | três escritas equivalentes de um literal proibido |

Os três achados são **técnicos**; não alteram risco, carteira, marca ou preferência do dono.
Não foram encontrados registros dos contraexemplos nas buscas temáticas em
`PENDENCIAS.md`, `ACHADOS.md` e `docs/historico/pendencias-fechadas.md`.
Isso descreve o resultado da busca, não garante ausência de qualquer formulação equivalente.

### CX-04 — Valores que não são dinheiro atravessam a porta de entrada

**Evidência:** em `estado_io.py:35`, `isinstance(v, (int, float))` aceita também
`bool`; em `:45`, `float(s)` aceita representações não finitas. Nenhum desses
caminhos confere finitude. Foram preparados YAML exclusivamente sintéticos, derivados do
modelo público, com um campo inválido por caso.

Comando na réplica, antes da proposta:
`py -3.11 -m pytest .testar/provas/test_estado_invalido.py -o addopts='' -q -p no:cacheprovider --tb=short`.

```text
[aporte_mensal-nan]  Failed: DID NOT RAISE EstadoInvalido
[caixa-inf]          Failed: DID NOT RAISE EstadoInvalido
[despesa_mensal-True] Failed: DID NOT RAISE EstadoInvalido
3 failed in 1.00s
```

n=3 entradas inválidas independentes. A tentativa inicial do pytest foi impedida por
`PermissionError: [WinError 5] Acesso negado` na pasta `pytest-of-osvaldo.junior`;
a execução autorizada fora do sandbox produziu as falhas acima.

**Consequência medida:** executar o código original de `estado_io.py` obtido por
`git show HEAD:alocacao/estado_io.py`, validar um dicionário sintético e passá-lo a
`alocar(Estado(**d), C, P, teses={}, carregos={})` produziu:

```text
{"campo":"aporte_mensal","n":1,"problemas":0,"erro":"ValueError: cannot convert float NaN to integer"}
{"campo":"despesa_mensal","n":1,"problemas":0,"booleano_virou_unidade":true,"diretiva":"G2_reserva"}
```

A entrada apresentada como válida pode quebrar adiante ou dimensionar reserva com uma
unidade monetária fabricada a partir de `true`. Não foi observado efeito sobre a carteira
pessoal, que permaneceu fora do instrumento.

**Cinco perguntas:** (a) mediu aceitação de três valores inválidos pela carga normal;
(b) não cobre todos os campos, intervalos econômicos, posições ou valores extremos;
(c) ler a carga e o G2 mostrou que não há recusa intermediária nos casos reproduzidos;
(d) os testes de recusa falham no código atual; (e) não depende de cláusula externa,
mas do contrato “número” da entrada e da procedência da decisão.
Não classifico como repetição exata de F-05: o mecanismo principal é conversão permissiva.

**Proposta provada na cópia:** bloqueio explícito de booleanos e conversão finita
centralizada, inclusive para texto numérico. O diff está no apêndice.
A validação direcionada das duas primeiras propostas terminou em
`32 passed in 1.15s`, n=32 testes selecionados, árvore temporária modificada,
sem acervo/estado pessoal/slow. Não é uma rodada completa dessa árvore modificada.

### CX-05 — Modelo em branco: o teste passa quando o validador perde a recusa

O contrato da função é `(dados, problemas, avisos)`; a linha
`problemas, _avisos, _ = validar(d)` atribui o dicionário de dados à variável
`problemas`. Como as chaves obrigatórias estão presentes no dicionário mesmo com valores
vazios, tanto `assert problemas` quanto o laço que procura nomes podem passar.

**Medição:** o validador real devolveu cinco problemas e quatorze chaves no dicionário
(n=1 modelo público). Ao substituí-lo por `(dados, [], avisos)`, o teste continuou passando.
Também passou quando restou apenas a mensagem de status MODELO, sem as recusas dos campos.

Comando antes:
`py -3.11 -m pytest .testar/provas/test_modelo_guarda.py -o addopts='' -q -p no:cacheprovider --tb=short`.

```text
[nenhum_problema] Failed: DID NOT RAISE AssertionError
[so_status]      Failed: DID NOT RAISE AssertionError
2 failed in 0.28s
```

n=2 mutações do retorno. **Consequência:** essa guarda não comprova o que anuncia.
Não afirmo que toda a suíte deixaria a regressão passar: outros testes podem detectá-la.

**Cinco perguntas:** (a) mediu a reação deste teste a duas perdas da validação;
(b) não mediu a capacidade da suíte inteira de matar os mesmos mutantes;
(c) a leitura da assinatura esclareceu que não é apenas nome confuso, mas objeto errado;
(d) a guarda passou diante dos dois defeitos deliberados; (e) fonte interna,
o contrato de `validar()`, cobre exatamente o desempacotamento.

**Padrão F-05/N-01/R-01/S-02: sim.** A declaração de comportamento do teste não corresponde
ao que ele verifica; as chaves do dicionário fazem os dois concordarem por acaso.

**Proposta:** `_dados, problemas, _avisos = validar(d)`.
Compilada na réplica. Os dois testes de mutação e o arquivo de usuário novo passaram:
`20 passed in 0.44s` (n=20, recorte selecionado da réplica).
Depois, a verificação conjunta com CX-04 produziu os 32 testes já informados.

### CX-06 — A guarda de política confunde representação textual e constante Python

O teste remove comentários/strings por regex e tenta reconhecer números por outra regex.
O contraexemplo substitui a leitura de
`P["motor_aporte"]["k_max"]` por uma constante em uma cópia **em memória** de
`alocacao.py`; cada fonte mutante foi compilada antes de submetê-la à guarda.
Não se trata de um número colocado apenas num comentário.

Comando antes:
`py -3.11 -m pytest .testar/provas/test_literal_guarda.py -o addopts='' -q -p no:cacheprovider --tb=short`.

```text
[70.0]  passed
[7e+1]  Failed: DID NOT RAISE AssertionError
[7_0]   Failed: DID NOT RAISE AssertionError
2 failed, 1 passed in 1.38s
```

n=3 escritas equivalentes; uma é controle positivo da guarda.
O `passed` da prova significa que a guarda **rejeitou** a constante, como deveria.

**Consequência:** esse teste permite reintroduzir uma decisão de política fixa no motor
dependendo apenas de como o número foi escrito. O caso original de V-03 era conhecido;
o acréscimo aqui é o bypass demonstrado por duas notações. Não afirmo que outros testes
de `k_max` aceitariam a mudança.

**Cinco perguntas:** (a) mediu a guarda com três fontes compiláveis equivalentes;
(b) não mede todos os literais, funções anteriores ao marcador ou toda a suíte;
(c) a leitura do ponto real de `k_max` e do YAML tornou o exemplo uma violação de P2;
(d) duas mutações escaparam e o controle foi recusado;
(e) `docs/doutrinas.md:26-35` descreve justamente a garantia pretendida.
O padrão declarativo de F-05 se aplica à garantia anunciada pelo teste.

**Proposta:** AST das constantes numéricas, mantendo o recorte e a lista de valores permitidos.
O primeiro rascunho falhou com `SyntaxError: invalid character '═' (U+2550)` ao deixar
um pedaço do separador no texto analisado. Foi corrigido e retestado; esse rascunho não
é a proposta entregue.

Resultado da proposta final:
`4 passed in 0.76s`, n=3 contraexemplos/controle + o teste original.
Comando:
`py -3.11 -m pytest .testar/provas/test_literal_guarda.py alocacao/test_alocacao.py::test_nenhum_literal_de_politica_fixo_no_modulo -o addopts='' -q -p no:cacheprovider --tb=short`.
Ruff: `All checks passed!`. Nenhum desses testes abre o acervo ou o estado pessoal.

## 3. Fontes e APIs verificadas

**Esta é uma lista de disponibilidade, não uma declaração de que todas devam ser integradas.**
ANBIMA, IFData e Tesouro já são discutidos em
`docs/fontes/pesquisa-bases-e-apis-2026-09.md:194-275`; apresentá-los como descobertas
inéditas repetiria a auditoria ruim. A ausência de uma referência textual não foi usada
para provar ausência de toda integração possível.

| Fonte | URL da documentação ou recurso | Formato | Janela / atualização conferida | Gratuita? | API? |
|---|---|---|---|---|---|
| ANBIMA IMA-B / IRF-M | [Índices](https://developers.anbima.com.br/pt/documentacao/precos-indices/apis-de-indices/indices/) | JSON | resultados diários e consulta por data; limite histórico contratado não medido | Feed tem condições comerciais; associado tem gratuidade | REST, incluindo resultados-ima |
| ANBIMA ETTJ | [Curvas de juros](https://developers.anbima.com.br/en/documentacao/precos-indices/apis-de-precos/) | JSON | diária; consulta por data | conforme Feed | REST, titulos-publicos/curvas-juros |
| ANBIMA debêntures | [Mercado secundário](https://developers.anbima.com.br/pt/documentacao/precos-indices/apis-de-precos/debentures/) | JSON | diária; não medi a primeira data disponível | conforme Feed | REST |
| BCB IFData | [Catálogo OData](https://olinda.bcb.gov.br/olinda/servico/IFDATA/versao/v1/odata/?$format=json) | JSON / OData | catálogo acessado; janela completa dos relatórios não foi enumerada | acesso público sem autenticação na consulta executada | sim, HTTP 200, seis recursos no catálogo |
| SEC EDGAR | [Documentação oficial](https://www.sec.gov/search-filings/edgar-application-programming-interfaces) | JSON e ZIP com JSON | atualizações durante o dia; companyfacts.zip recompilado à noite | acesso sem chave descrito pela SEC | REST e arquivo bulk |
| Tesouro Transparente | [Conjunto oficial](https://www.tesourotransparente.gov.br/ckan/dataset/taxas-dos-titulos-ofertados-pelo-tesouro-direto) | CSV | dados desde janeiro/2002, atualização diária na ficha | dados abertos ODbL | download direto; não executei API de consulta |
| CoinGecko | [Guia oficial](https://www.coingecko.com/learn/download-bitcoin-historical-data) | JSON; exportação CSV | Demo: até 365 dias no endpoint descrito | Demo gratuito com chave; histórico maior depende de plano | REST |
| Binance Vision | [Repositório oficial](https://github.com/binance/binance-public-data) | ZIP de CSV, CHECKSUM | arquivos diários/mensais; cobertura varia por par | download público | distribuição HTTP; não é endpoint REST de consulta |

O formato das APIs ANBIMA está documentado na
[introdução oficial](https://developers.anbima.com.br/pt/documentacao/visao-geral/introducao-a-api/);
as condições de acesso, na [página do Feed](https://feed.anbima.com.br/anbima-feed/).
Não assinei serviço, usei chave ou validei licença de redistribuição. A página dinâmica
de IMA-B retornou “Aguarde...” no acesso direto; a indicação de cinco dias úteis veio do
resultado indexado da própria fonte. Não a usei para afirmar a janela das demais séries.

**IFData — contorno efetivamente executado:** a ferramenta web recusou XML com
`Unsupported content-type: application/xml`; o formato JSON também não abriu nela.
O primeiro urllib no sandbox retornou `WinError 10061`. A consulta autorizada fora dele,
com `urllib.request.urlopen(url, timeout=20)` e `json.load`, produziu:

```json
{"http":200,"n":6,"recursos":["_IfDataCadastro","_ListaDeRelatorio","_IfDataValores","ListaDeRelatorio","IfDataCadastro","IfDataValores"]}
```

n=uma resposta de catálogo, seis recursos; isso não valida os dados contábeis.
O código e a sintaxe da URL estão observados, sem necessidade de pedir inspeção manual ao dono.

**Outras fontes:** nenhuma integração adicional foi promovida a requisito. Fonte disponível
não é necessidade demonstrada. CoinGecko é agregador; Binance cobre a própria praça.
Isso precisa ser explícito se forem usadas como conferência ou insumo.

## 4. Roadmap priorizado

Esforço abaixo é tamanho qualitativo da intervenção observada, não estimativa inventada de horas.

| Prioridade | Item | Natureza / impacto | Esforço | Bloqueia / prova necessária |
|---|---|---|---|---|
| imediata | CX-04: recusar entradas não financeiras | correção; impedir carga inválida | localizada na conversão | três casos já falham antes e passam na proposta |
| seguinte | CX-05: corrigir objeto examinado | correção de guarda | uma atribuição + testes de mutação | dois mutantes já provados |
| seguinte | CX-06: interpretar constantes com AST | correção de guarda P2 | teste localizado | duas notações que escapavam + controle |
| antes de expor o motor | contrato de entrada e não retenção | execução das P-178/P-175, já registradas | depende de desenho e plataforma | valores-sentinela não aparecem em logs ou resposta indevida |
| conforme plano existente | adaptação da saída para a F0 | produto, não bug novo | não dimensionado | estado sintético gera decisão/recusa com procedência no esquema aprovado |
| conforme P-52 | decidir captura ANBIMA conforme termos | dado e decisão comercial | não dimensionado | captura idempotente; lacuna e dado vencido não viram zero |

### Otimizações avaliadas

- **Dependências:** nenhuma retirada ou troca por stdlib foi provada equivalente. NumPy e
  pandas participam dos cálculos registrados. Trocar versões por serem mais novas não é
  conserto demonstrado.
- **Deduplicação:** a busca por definições encontrou `simular_custo` em
  `alocacao/alocacao.py:461`, `simular` em `alocacao/reserva.py:40` e uma versão
  arquivada em `docs/historico/pesquisa-custos-2026-08/calc/motor.py:169`.
  Nome semelhante não demonstra fórmula duplicada. Não proponho fusão.
- **Suítes:** `testpaths` contém só `alocacao`, mas o orquestrador e o CI executam as
  cinco pastas explicitamente. Não tratar o campo isolado como prova de quatro suítes esquecidas.
- **Contexto:** `CLAUDE.md` tinha 432 linhas na base lida. O tamanho não demonstra custo
  evitável: não foi medido benefício de corte nem perda de instruções. Sem proposta de corte.
- **Estrutura:** nenhuma vantagem medida justifica mover módulos ou criar manifesto alternativo
  na raiz. Perfil, política, catálogo e estado público de exemplo já têm papéis distintos.

### Inovações: hipóteses com testes de aceitação, sem patch proposto

| Ideia | O que deve ser medido antes de existir como promessa | Teste de aceitação sugerido |
|---|---|---|
| Contrafactual automático / Real × Motor × Nada | comparação com os mesmos fluxos, datas, disponibilidade e custos | cenário sintético em que os três caminhos coincidem deve produzir igualdade; alterar só a ação realizada afeta só o caminho Real |
| IPA | definir com o dono o que significa aderir e o denominador; não confundir obediência e retorno | mês sem decisão deve ficar sem medida, não receber nota perfeita; decisões iguais recebem a mesma classificação |
| Trilha de decisão | a especificação T5 já pede motivo e hashes | política alterada depois não reescreve registro passado; evento aponta para a versão efetivamente usada |
| Simulador what-if | há custo de discordar; não presume necessidade de novo cenario.py | cenário não modifica o estado-base; cenário idêntico reproduz a saída-base |
| Painel de saúde | definir indicadores úteis; não inventar “quatro” sem contrato | ausência, atraso e falha de captura não podem produzir selo saudável |
| Exposição look-through | cobertura dos componentes e data comum | fundo com componente desconhecido mostra parcela desconhecida; não atribui exposição zero |

Esses testes são **especificações de aceitação não executadas**, não consertos provados
nem achados adicionais. A utilidade para o público e a privacidade são decisões do dono.
Não há benchmark financeiro medido que sustente promessas de ganho.

## 5. O que não fazer — e o que a doutrina de fato diz

- **Otimizador de carteira:** rejeição explícita em `CLAUDE.md:25-28`. Não substituir
  escolha declarada por um ótimo apresentado como verdade.
- **Promessa de previsão de retorno:** `politica.yaml:1813-1835` separa qualidade da empresa
  de retorno da ação; `docs/ux/mapa-de-telas-v1.md:43` também veda promessa de retorno.
  Isso não equivale a proibir todo teste estatístico pré-registrado.
- **“ML sobre fundamentos foi rejeitado”: não sustentado.** A P-122 e o pré-registro ML
  são evidência contrária a uma proibição geral. Não instalar ou mudar o experimento nesta
  auditoria; a doutrina exige pré-registro e validação, não uma rejeição inventada.
- **Interface gráfica pesada:** a v1 exclui gráficos em
  `docs/ux/mapa-de-telas-v1.md:164-166`, mas o mesmo documento projeta telas.
  Não transformar isso em “interface gráfica proibida”.
- **Comunidade:** comparação entre usuários fica fora da v1, pelo mesmo trecho;
  o registro de adesão é pessoal (`:135`). Uma proibição eterna de qualquer comunidade
  não foi demonstrada.
- **Integração com corretoras:** a P-128 registra autorização para pesquisar Open Finance,
  **sem integrar**. Preservar essa decisão; não afirmar que a pesquisa foi rejeitada.

## 6. Arquivos mais críticos

A evidência justifica **três**, não cinco arquivos com correção imediata:
`alocacao/estado_io.py:31`, `alocacao/test_usuario_novo.py:229` e
`alocacao/test_alocacao.py:327`, pelas provas CX-04 a CX-06.

`auditoria/chaves_orfas.py` e `alocacao/conftest.py` têm pendências já registradas
(P-173/P-174), mas esta rodada não produziu prova nova que justifique inflá-las como
novos achados. `auditoria/c02_corrida.py` ganhou a P-177 no checkout posterior;
também não a recadastrei.

## 7. Testes que faltam primeiro

| Teste | Estado da prova nesta auditoria |
|---|---|
| carga normal recusa aporte NaN | falhou antes; passou na proposta |
| carga normal recusa caixa infinito | falhou antes; passou na proposta |
| carga normal recusa despesa booleana | falhou antes; passou na proposta |
| guarda do modelo falha se sumirem todos os problemas ou só os dos campos | dois casos falharam antes; passaram na proposta |
| guarda P2 rejeita constante em decimal, expoente positivo e separador de dígitos | controle passou antes; dois bypasses falharam; três passaram na proposta |

O código executado desses testes e o diff das propostas são incorporados no apêndice,
para que o documento seja conferível sem depender desta conversa.

## 8. Candidatos descartados e limites que impediram promoção

| Candidato | Por que não virou achado novo |
|---|---|
| _registro depende da forma textual das anotações | já usa typing.get_type_hints; B-11 |
| reserva disponível ausente deveria bloquear sempre | a equivalência com nominal é decisão documentada; mudar sem ler J-01 reabriria semântica já definida |
| _conferir_empenho usa valor “corrompido” | não foi provada corrupção no caso normal; distinção entre ausência e empenho é explícita |
| fixtures de sessão não são vigiadas | B-12 já implementada; prova com subprocesso existe |
| caches devem ser limpos a cada teste | conftest.py:85-87 declara por que não; limpar pode esconder a classe S-02 |
| E03 só procura a palavra ativo | B-15 já substituiu a inspeção textual por cenários ligados/desligados |
| P72 negativo só confere lista de problemas | teste já exige EstadoInvalido com pytest.raises, B-14 |
| alias no AST permite carregar estado pessoal | o bypass citado foi fechado em B-13, com contraexemplos de alias/import estrela |
| nenhum detector de chave duplicada | implementação está em test_y01_yaml_duplicata.py; fusão documentada |
| chaves_orfas encontrou campos, portanto todos são defeitos | nomes variáveis, testemunhas e limitações do instrumento exigem leitura; P-173 registra uma delas |
| falta manifesto CVM | manifestos versionados existem e foram contados; não confundir existência com integridade real |
| faltam workflows automáticos | captura diária e testes semanais estão declarados em YAML |
| subprocess.run(pytest) é recursão da suíte inteira | chamadas em test_alocacao.py:2686,2720,2761 apontam a arquivos sintéticos temporários, sem copiar a própria suíte |
| primeiro aporte sempre SEM_POSICAO | verdadeiro na base antiga, implementado no checkout posterior; P-164 descartada como lacuna atual |
| precisamos de um cenario.py, aportes.yaml ou responder.py com esse nome | nome ausente não prova capacidade ausente; medir contrato e caminho do usuário |
| contagens de testes diferentes provam inconsistência | recorte, data, parametrização, skips e arquivos históricos diferem; não foi provada contradição comparável |
| versões mais novas provam dependência defeituosa | atualização é evento de ambiente; nenhum bug foi reproduzido por versão |
| repetir P-173/P-174/P-177 | sem acréscimo de prova nesta rodada, permanecem referências ao registro existente |

Não incluí seção de elogios. Os controles que derrubaram suspeitas estão acima.

## 9. Apêndice de descoberta, comandos e propostas


### 9.1 Doutrina aplicada

Fonte: `docs/doutrinas.md`, lida integralmente. P1: procedência por valor e recusa de
insumo bloqueado; P2: regra como dado; P3: portões com motivo, sem score opaco;
P4: pré-registro com impressão; P5: limites declarados; P6: ausência de critério não
justifica exclusão; P7: rotina não depende de alguém lembrar.

A premissa de “16 regras” do prompt está desatualizada frente ao texto lido:
`CLAUDE.md:284-296` contém as cinco perguntas e `:303-328` as regras adicionais
numeradas 12 a 18. O histórico explica os onze erros anteriores; não inventei regras
numeradas que o documento atual não enumera.

### 9.2 Estrutura e inventário

Comando-base: `git ls-files -z`, com exclusão explícita de
`data/`, `alocacao/dados/`, `alocacao/estado.yaml` e acervo bruto.
O `find.exe` disponível no Windows não é o `find` POSIX pedido.
Usei a árvore pública versionada e AST: **não é inventário completo do disco**.
A réplica contém 457 caminhos no índice medido (n=1 índice; lista obtida por esse comando).

| Categoria | Onde foi encontrada | Limite da observação |
|---|---|---|
| Pontos de entrada | tools/testar.py; scripts com guarda __main__; demo_aporte.py com execução de topo | detectar __main__ não encontra toda execução de topo |
| Coletores | fase0/capturar_cvm.py, capturar_cotahist.py, capturar_eventos_b3.py, capturar_nefin.py | presença/estrutura; sem disparar captura real |
| Parsers e transformação | fase0/calendario.py, refinar.py, ajustar.py | leituras localizadas e testes sintéticos |
| Motor | alocacao/alocacao.py, motor.py, estado_io.py, reserva.py, aporte.py | apenas caminhos declarados no alcance |
| Guardas e testes | auditoria/ e test_*.py das cinco suítes | lista completa de nomes abaixo; conteúdo não lido integralmente |
| Configuração | YAML de alocacao/; pyproject.toml; workflows | configurações públicas |
| Produto e documentação | docs/, pesquisa/, CLAUDE/PLANO/PENDENCIAS/ACHADOS | produto tem especificações; não equivale a protótipo validado |
| Acervo | apenas manifestos públicos em docs/acervo/ | bruto e diretório data/ excluídos |

Workflows lidos por `yaml.BaseLoader` para preservar a chave `on`:
captura `15 9 * * *`; testes `0 11 * * 1`; medir em push; mutação manual.
n=4 arquivos YAML. Essa configuração não prova que o último job agendado tenha executado.
`.gitignore:12,24,95-97` cobre data/, ZIPs de fontes e estado pessoal.
Os três testes de privacidade citados no pedido existem na lista e participaram do recorte
aplicável; não usei isso como licença para ler os arquivos protegidos.

### 9.3 Dependências

Manifesto: `pyproject.toml:71-115`.
Instaladas: `importlib.metadata.version(nome)`, n=13 declarações.
Versão publicada: consulta ao JSON público do PyPI; nos timeouts, página oficial do pacote.
A primeira consulta restrita retornou `WinError 10061`; na consulta autorizada houve
`TimeoutError: The read operation timed out` para parte dos pacotes. As páginas do PyPI
resolveram a consulta desses casos. São versões observadas durante esta auditoria,
não recomendação de atualização.

| Dependência | Declarada | Instalada | Publicada na consulta | Uso observado / alternativa stdlib |
|---|---|---|---|---|
| numpy | ==2.4.4 | 2.4.4 | [2.5.3](https://pypi.org/project/numpy/) | import numpy e cálculos numéricos; nenhuma equivalência com stdlib foi provada |
| pandas | ==3.0.2 | 3.0.2 | [3.0.6](https://pypi.org/project/pandas/) | import pandas em fatores/teste; reimplementar agrupamento exigiria nova medição |
| PyYAML | ==6.0.3 | 6.0.3 | [6.0.3](https://pypi.org/project/PyYAML/) | import yaml, não PyYAML; parser/anchors/merges sem substituição demonstrada |
| pytest | ==9.1.1 | 9.1.1 | [9.1.1](https://pypi.org/project/pytest/) | fixtures, parametrização e executor; unittest não é troca direta desses testes |
| ruff | ==0.16.9 | 0.16.9 | [0.16.10](https://pypi.org/project/ruff/) | CLI em tools/testar.py:89; ausência de import não é desuso |
| mypy | ==2.3.1 | 2.3.1 | [2.4.0](https://pypi.org/project/mypy/) | CLI em tools/testar.py:90; sem substituição equivalente provada |
| types-PyYAML | sem == | 6.0.12.20260906 | [6.0.12.20260906](https://pypi.org/project/types-PyYAML/) | stubs; não é dependência de import de execução |
| boto3 | ==1.43.102 | 1.43.101 | [1.43.108](https://pypi.org/project/boto3/) | import em fase0/armazem.py:269; urllib não substitui SDK S3 por simples remoção |
| pytest-xdist | ==3.8.0 | 3.8.0 | [3.8.0](https://pypi.org/project/pytest-xdist/) | plugin usado por -n / loadgroup; não depende de import direto |
| execnet | ==2.1.2 | 2.1.2 | [2.1.2](https://pypi.org/project/execnet/) | suporte do executor paralelo; nenhum import direto nos módulos varridos |
| pytest-cov | ==7.1.0 | 7.1.0 | [7.1.0](https://pypi.org/project/pytest-cov/) | plugin da medição de cobertura, fora desta rodada de cobertura |
| coverage | ==7.16.1 | 7.16.1 | [7.16.2](https://pypi.org/project/coverage/) | workflow testes.yml:139 usa CLI; sem import não significa sem consumidor |
| mutmut | ==3.8.0 | 3.8.0 | [3.8.0](https://pypi.org/project/mutmut/) | workflow manual e import em auditoria/mutmut_contagem.py; não executado nesta auditoria |

A divergência local de boto3 fica fora dos extras instalados pelo comando do recorte.
Ela limita qualquer conclusão sobre captura real, que não foi executada; não é prova de
bug financeiro. `types-PyYAML` não pinado não foi promovido a defeito sem impacto medido.
NumPy publicado na consulta exige Python >=3.12: não proponho adotá-lo em projeto restrito
a 3.11. Os pinos do projeto permanecem como foram encontrados.

### 9.4 YAML, campos e manifestos

Comando de carga: `yaml.safe_load((Path("alocacao") / nome).read_text(encoding="utf-8"))`;
inspeção de duplicatas com `_chaves_duplicadas(caminho)` de
`test_y01_yaml_duplicata.py`. Todos os sete YAML permitidos carregaram como dicionário;
a guarda retornou zero duplicatas em cada um (n=7 arquivos).
Isso mede o alcance daquela guarda, não toda possibilidade de colisão semântica de chaves.

Comando da inspeção de órfãos:
```powershell
py -3.11 auditoria/chaves_orfas.py alocacao alocacao/custos.yaml alocacao/politica.yaml alocacao/perfil.yaml alocacao/catalogo.yaml alocacao/teses.yaml alocacao/estado.exemplo.yaml alocacao/instituicoes.yaml --tambem fase0
```

Saída resumida, n=7 YAML: custos 6 órfãos/0 só teste; política 18/0; perfil 4/3;
catálogo 0/0; teses 0/0; estado.exemplo 0/0; instituições 3/22.
Total: 31 nomes candidatos a órfão e 25 candidatos lidos só por teste.
O instrumento reportou 1213 leituras de índice variável como pontos cegos, não como defeitos.
A P-173 impede promover indiscriminadamente esses totais: testes e colisões de nomes podem
alterar o reconhecimento. Não se atribuiu consequência financeira aos candidatos sem leitura.

Manifestos: `csv.DictReader(..., delimiter=";")` e verificação de formato por
`re.fullmatch("[0-9a-fA-F]{64}", sha256)`.
O primeiro rascunho do instrumento assumiu vírgula e leu o cabeçalho como uma só coluna;
foi corrigido antes de qualquer conclusão.

- `docs/acervo/b3/dt_captura=2026-09-24.csv`: 41 registros, 41 hashes com formato válido,
  n=41 linhas.
- `docs/acervo/cvm/dt_captura=2026-09-25.csv`: 62 registros, 62 hashes com formato válido,
  n=62 linhas.

São registros de snapshots, **não a contagem atual de ZIPs no computador**.
Não imprimi preços, volumes ou valores de negociação da B3 no relatório.
O leitor `fase0/calendario.py` usa schema e há testes P-99 de nomes históricos;
não executei a conferência do acervo de todos os anos.

### 9.5 Escada de erros do instrumento

Além dos erros de rede, instalação e permissão já transcritos:
- `rg alocacao/test_*.py` no Windows retornou `os error 123`; repetido com
  `rg ... alocacao -g 'test_*.py'`, com resultado.
- Leitura numerada por Python retornou `UnicodeEncodeError: 'charmap' codec can't encode`;
  repetida com `PYTHONIOENCODING=utf-8`.
- A primeira rodada de durações tentou gravar numa pasta temporária ainda inexistente:
  `DirectoryNotFound`. Os testes não chegaram a iniciar nessa tentativa; a pasta foi criada
  na réplica e a rodada efetiva é a transcrita.
- A busca por `docs/ux/F0-contrato.md` retornou `os error 2`; `rg --files docs/ux`
  identificou o nome real, `F0-contrato-de-saida.md`.
- A proposta inicial de AST e o erro de separador estão registrados no CX-06. Somente
  a proposta final, retestada, consta do diff.

Nenhum desses erros de ferramenta foi rotulado como defeito do projeto.

### 9.6 Contagem de imports e comparação dos achados no checkout posterior

Varredura AST de `git show HEAD:<arquivo>` sobre 175 módulos Python versionados nas cinco
pastas vivas, excluindo dados. Contagem de nós de import, não de usos em execução
(n=175 arquivos; inclui testes):

```text
numpy=15 pandas=2 yaml=58 pytest=76 boto3=1 mutmut=1
ruff=0 mypy=0 xdist=0 execnet=0 pytest_cov=0 coverage=0
test_*.py nas cinco pastas=100
```

O comando extraiu `ast.Import` e `ast.ImportFrom`, normalizando pelo primeiro segmento.
CLI, plugins e stubs são examinados separadamente; as linhas de uso estão na tabela de dependências.

Para o checkout posterior, `git diff --exit-code 97bdc56 HEAD -- alocacao/estado_io.py alocacao/test_usuario_novo.py`
retornou 0 (n=2 arquivos). Para não supor que o restante de test_alocacao.py também fosse
igual, comparei `ast.dump(node, include_attributes=False)` de cada função entre os commits:

```text
test_nenhum_literal_de_politica_fixo_no_modulo: linhas 311-328, ast_igual=true
test_o_modelo_nao_carrega_ate_alguem_preencher: linhas 222-233, ast_igual=true
_num: linhas 31-48, ast_igual=true
```

n=3 funções, sem reatribuir resultados de CI à árvore posterior.


### 9.7 Arquivos de teste encontrados na base

Comando: `git ls-files -z`, filtro por basename `test_*.py`. Nomes, nao contagem de casos parametrizados.

```text
alocacao/test_alocacao.py
alocacao/test_b11_registro_sem_future.py
alocacao/test_campos_mortos.py
alocacao/test_cenarios.py
alocacao/test_corretoras.py
alocacao/test_e02_registros.py
alocacao/test_e08_bloqueio_e_copia.py
alocacao/test_fatores.py
alocacao/test_impacto.py
alocacao/test_jcp.py
alocacao/test_limitacoes_tipo.py
alocacao/test_motor.py
alocacao/test_multiplicidade.py
alocacao/test_p141_paralelo.py
alocacao/test_p40_lint.py
alocacao/test_p67_segredo.py
alocacao/test_p71_p72_porta_de_entrada.py
alocacao/test_p77_duas_pontas.py
alocacao/test_p82_copia_do_projeto.py
alocacao/test_p98_acervo_fora_do_indice.py
alocacao/test_preregistro.py
alocacao/test_sleeve.py
alocacao/test_tese.py
alocacao/test_usuario_novo.py
alocacao/test_y01_yaml_duplicata.py
auditoria/test_achados_ancorados.py
auditoria/test_c02_bootstrap_sigma.py
auditoria/test_c02_contar_n.py
auditoria/test_c02_corrida.py
auditoria/test_c02_criterio_v2_poder.py
auditoria/test_c02_sorteio_d1.py
auditoria/test_chaves_orfas.py
auditoria/test_cobertura_csv.py
auditoria/test_codigos_de_marca.py
auditoria/test_codigos_preservados.py
auditoria/test_contraste_tokens.py
auditoria/test_direcoes_marca.py
auditoria/test_escada_contorno.py
auditoria/test_expira_proxima.py
auditoria/test_git01_branches_integradas.py
auditoria/test_guarda_segredos.py
auditoria/test_links_internos.py
auditoria/test_metricas_processo.py
auditoria/test_mutmut_contagem.py
auditoria/test_navegador_negado.py
auditoria/test_p88_block_bootstrap.py
auditoria/test_raiz_viva.py
auditoria/test_tags_citadas.py
auditoria/test_tamanho_do_contexto.py
auditoria/test_workflow_medir.py
auditoria/test_workflows.py
docs/historico/pesquisa-custos-2026-08/calc/test_motor.py
fase0/test_a12_chave_de_evento.py
fase0/test_acervo.py
fase0/test_acervo_de_teste.py
fase0/test_ajustar.py
fase0/test_ajustar_janela.py
fase0/test_armazem.py
fase0/test_calendario.py
fase0/test_calendario_p99.py
fase0/test_capturar_cotahist.py
fase0/test_capturar_cvm.py
fase0/test_capturar_cvm_armazem.py
fase0/test_capturar_eventos_b3.py
fase0/test_capturar_nefin.py
fase0/test_ci04_origem_da_captura.py
fase0/test_coletar_b3.py
fase0/test_conciliar_cotahist.py
fase0/test_conferir_reproducao.py
fase0/test_insumo_ml.py
fase0/test_manifesto_cvm.py
fase0/test_materializar_acervo.py
fase0/test_memo_acervo.py
fase0/test_moeda.py
fase0/test_nomear_extracoes.py
fase0/test_origem_bom.py
fase0/test_p113_preco_de_vespera.py
fase0/test_p114_raiz_do_cotahist.py
fase0/test_p120_extracoes_soltas.py
fase0/test_p121_pasta_nao_e_cotahist.py
fase0/test_p125_ano_do_cabecalho.py
fase0/test_p7_captura_declarada.py
fase0/test_publicar_cvm.py
fase0/test_refinar.py
fase0/test_sondar_cotahist.py
fase0/test_subir_acervo_local.py
fase0/test_universo_ml.py
fase0/test_workflow_captura.py
medicoes/test_p145_ponte_2013_2019.py
tools/test_analisar_sessoes.py
tools/test_analise_teste_marca.py
tools/test_codigos_visuais.py
tools/test_conteudo_estimulo.py
tools/test_estado.py
tools/test_pesquisa.py
tools/test_questionario_json.py
tools/test_questionario_teste_marca.py
tools/test_r3_dominante.py
tools/test_r3_universo.py
tools/test_servir_pesquisa.py
tools/test_testar.py
```

### 9.8 Duracoes por suite: transcricao

Uma rodada serial por pasta; replica 97bdc56, recorte `not slow and not privado and not acervo`, sem estado pessoal/acervo.

**alocacao**

```text
============================ slowest 10 durations =============================
2.95s call     alocacao/test_impacto.py::test_os_pontos_cegos_sao_reportados_e_nao_escondidos
2.23s call     alocacao/test_preregistro.py::test_P138_verificador_so_aceita_o_que_foi_EMPURRADO
1.81s call     alocacao/test_corretoras.py::test_robustez_e_reportada_com_honestidade
1.74s call     alocacao/test_corretoras.py::test_P90_zero_MEDIDO_e_zero_por_AUSENCIA_sao_distinguiveis
1.69s call     alocacao/test_corretoras.py::test_a_saida_do_ranking_e_DETERMINISTICA_entre_execucoes
1.51s call     alocacao/test_alocacao.py::test_R01_a_ordem_dos_portoes_era_um_DADO_que_so_aceitava_18_de_120_valores
1.38s call     alocacao/test_impacto.py::test_o_relatorio_de_alvo_inexistente_nao_afirma_que_nada_depende
1.27s call     alocacao/test_preregistro.py::test_P138_emenda_publicada_com_OUTRO_texto_nao_vale
1.07s call     alocacao/test_impacto.py::test_o_alcance_de_funcao_e_transitivo_e_nao_so_direto

(1 durations < 1s hidden.)
552 passed, 22 deselected in 48.87s
```

**fase0**

```text
============================ slowest 10 durations =============================
3.80s call     fase0/test_capturar_eventos_b3.py::test_sobe_por_chave_de_conteudo_em_b3_e_a_segunda_rodada_nao_sobe_nada
1.82s call     fase0/test_capturar_eventos_b3.py::test_sem_tradingname_e_falha
1.73s call     fase0/test_capturar_eventos_b3.py::test_ressalva_do_coletor_fica_no_registro_e_o_passo_segue_verde
1.73s call     fase0/test_capturar_eventos_b3.py::test_qualquer_dia_roda_fora_da_cadencia
1.46s call     fase0/test_capturar_eventos_b3.py::test_erro_ou_bloqueio_da_B3_e_falha_com_motivo_e_nao_silencio
1.33s call     fase0/test_capturar_eventos_b3.py::test_o_teto_recusa_com_linha_no_registro_e_passo_vermelho
1.18s call     fase0/test_capturar_eventos_b3.py::test_fora_da_cadencia_nada_e_pedido
1.18s call     fase0/test_capturar_eventos_b3.py::test_sem_cadencia_valida_na_politica_recusa[segunda-]
1.13s call     fase0/test_capturar_eventos_b3.py::test_sem_cadencia_valida_na_politica_recusa[None-x]
1.05s call     fase0/test_capturar_cvm_armazem.py::test_hash_coincide_vai_ao_registro_e_fecha_o_portao_na_rodada_seguinte
539 passed, 10 skipped, 41 deselected in 41.54s
```

**auditoria**

```text
============================ slowest 10 durations =============================
2.18s call     auditoria/test_c02_corrida.py::test_trava_aceita_o_commit_empurrado
1.57s call     auditoria/test_c02_corrida.py::test_sem_queda_reprova_k2_e_k3_por_ic_disjunto
1.44s call     auditoria/test_c02_corrida.py::test_queda_igual_ao_liquido_reprova_o_k2
1.36s call     auditoria/test_c02_corrida.py::test_main_grava_o_sha256_de_cada_insumo
1.35s setup    auditoria/test_c02_corrida.py::test_queda_igual_ao_bruto_passa_a_janela
1.30s call     auditoria/test_chaves_orfas.py::test_a_linha_de_base_nao_guarda_chave_ja_resolvida
1.29s call     auditoria/test_chaves_orfas.py::test_nenhuma_chave_orfa_NOVA
1.29s call     auditoria/test_tags_citadas.py::test_toda_tag_de_marco_e_anotada_e_o_sha256_bate_com_o_arquivo
1.13s call     auditoria/test_codigos_de_marca.py::test_os_documentos_nao_mudam_os_codigos_preservados

(1 durations < 1s hidden.)
638 passed, 1 skipped, 18 deselected in 47.14s
```

**tools**

```text
============================ slowest 10 durations =============================
3.86s call     tools/test_pesquisa.py::test_v_a_duracao_obedece_ao_json_servido
3.24s call     tools/test_pesquisa.py::test_v_imagem_visivel_antes_do_tempo_e_fora_depois
2.52s call     tools/test_pesquisa.py::test_v_percurso_inteiro_com_o_contador_simulado
2.07s call     tools/test_pesquisa.py::test_v_sem_contador_a_pagina_para_e_nao_sorteia
1.81s call     tools/test_pesquisa.py::test_v_a_versao_vem_do_contador

(5 durations < 1s hidden.)
141 passed, 1 skipped in 19.39s
```

**medicoes**

```text
============================ slowest 10 durations =============================

(10 durations < 1s hidden.)
5 passed in 0.07s
```

### 9.9 Testes adicionais executados

Os testes devem ser copiados para a pasta temporaria equivalente de uma copia limpa do commit medido. Antes de aplicar o diff, produzem as falhas transcritas. Depois, passam. Nao execute mutacoes no checkout do dono.

**.testar/provas/test_estado_invalido.py**

```python
import sys
from pathlib import Path
import pytest
import yaml
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "alocacao"))
import estado_io

@pytest.mark.parametrize("campo, valor", [("aporte_mensal", float("nan")), ("caixa", float("inf")), ("despesa_mensal", True)])
def test_carregar_recusa_numero_invalido(tmp_path, campo, valor):
    modelo = yaml.safe_load((Path(estado_io.__file__).parent / "estado.exemplo.yaml").read_text(encoding="utf-8"))
    modelo.update(despesa_mensal=3000, estabilidade_renda="media", horizonte_anos=30, aporte_mensal=500)
    modelo["meta"]["status"] = "REAL"
    modelo[campo] = valor
    arquivo = tmp_path / "sintetico.yaml"
    arquivo.write_text(yaml.safe_dump(modelo), encoding="utf-8")
    with pytest.raises(estado_io.EstadoInvalido, match=campo):
        estado_io.carregar(path=str(arquivo))

```

**.testar/provas/test_modelo_guarda.py**

```python
import sys
from pathlib import Path
from unittest.mock import patch
import pytest
import yaml
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "alocacao"))
import estado_io
import test_usuario_novo as T

@pytest.mark.parametrize("mutacao", ["nenhum_problema", "so_status"])
def test_guarda_rejeita_validador_sem_problemas_obrigatorios(mutacao):
    modelo = yaml.safe_load((Path(T.__file__).parent / "estado.exemplo.yaml").read_text(encoding="utf-8"))
    dados, _, avisos = estado_io.validar(modelo)
    problemas = [] if mutacao == "nenhum_problema" else ["meta.status: MODELO"]
    with patch.object(estado_io, "validar", return_value=(dados, problemas, avisos)):
        with pytest.raises(AssertionError):
            T.test_o_modelo_nao_carrega_ate_alguem_preencher()

```

**.testar/provas/test_literal_guarda.py**

```python
import io
import sys
from pathlib import Path
from unittest.mock import patch
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "alocacao"))
import test_alocacao as T

@pytest.mark.parametrize("literal", ["70.0", "7e+1", "7_0"])
def test_guarda_recusa_politica_fixa_em_notacoes_validas(literal):
    alvo = Path(T.__file__).parent / "alocacao.py"
    fonte = alvo.read_text(encoding="utf-8")
    trecho = 'if k_max is None: k_max = P["motor_aporte"]["k_max"]'
    assert fonte.count(trecho) == 1
    fonte = fonte.replace(trecho, "if k_max is None: k_max = " + literal)
    compile(fonte, str(alvo), "exec")
    abrir = open
    def abrir_mutante(path, *args, **kwargs):
        return io.StringIO(fonte) if Path(path) == alvo else abrir(path, *args, **kwargs)
    with patch("builtins.open", side_effect=abrir_mutante):
        with pytest.raises(AssertionError):
            T.test_nenhum_literal_de_politica_fixo_no_modulo()

```

### 9.10 Diff das propostas: somente na copia temporaria

Comando: `git diff -- alocacao/estado_io.py alocacao/test_usuario_novo.py alocacao/test_alocacao.py`. O diff nao foi aplicado no checkout do dono.

```diff
diff --git a/alocacao/estado_io.py b/alocacao/estado_io.py
index 56ebc58..8541171 100644
--- a/alocacao/estado_io.py
+++ b/alocacao/estado_io.py
@@ -15,6 +15,7 @@ o que bloqueia do que e aviso, e nao inventa valor nenhum.
 """
 from __future__ import annotations
 import dataclasses, os, re, sys, typing, datetime as dt
+import math
 import yaml
 
 AQUI = os.path.dirname(os.path.abspath(__file__))
@@ -28,21 +29,33 @@ NUMERICOS = ("despesa_mensal", "reserva_atual", "aporte_mensal", "caixa", "horiz
 class EstadoInvalido(Exception):
     pass
 
+def _numero_finito(v, campo, problemas):
+    n = float(v)
+    if not math.isfinite(n):
+        problemas.append(f"{campo}: numero tem de ser finito")
+        return None
+    return n
+
+
 def _num(v, campo, problemas):
     """Converte para float recusando as armadilhas de preenchimento manual."""
     if v is None:
         problemas.append(f"{campo}: nao preenchido"); return None
-    if isinstance(v, (int, float)): return float(v)
+    if isinstance(v, bool):
+        problemas.append(f"{campo}: booleano nao e numero")
+        return None
+    if isinstance(v, (int, float)): return _numero_finito(v, campo, problemas)
     if isinstance(v, str):
         s = v.strip()
         if re.fullmatch(r"-?\d{1,3}(\.\d{3})*,\d+", s) or re.fullmatch(r"-?\d+,\d+", s):
-            convertido = float(s.replace(".", "").replace(",", "."))
+            convertido = _numero_finito(s.replace(".", "").replace(",", "."), campo, problemas)
+            if convertido is None: return None
             problemas.append(
                 f"{campo}: '{v}' foi lido como TEXTO, nao numero — YAML usa PONTO como "
                 f"separador decimal. Escreva {convertido:.2f}. Interpretei como "
                 f"{convertido:.2f} para seguir, mas corrija o arquivo")
             return convertido
-        try: return float(s)
+        try: return _numero_finito(s, campo, problemas)
         except ValueError:
             problemas.append(f"{campo}: '{v}' nao e numero"); return None
     problemas.append(f"{campo}: tipo inesperado {type(v).__name__}"); return None
diff --git a/alocacao/test_alocacao.py b/alocacao/test_alocacao.py
index 3c9b670..307fcf0 100644
--- a/alocacao/test_alocacao.py
+++ b/alocacao/test_alocacao.py
@@ -312,19 +312,19 @@ def test_nenhum_literal_de_politica_fixo_no_modulo():
     """V-03, o caminho inverso do teste de cobertura: a cobertura garante que toda
     chave do YAML e lida; este garante que nao ha constante de politica fixa no
     Python. A lista de excecoes e explicita de proposito."""
-    import re
+    import ast
     fonte = open(os.path.join(AQUI, "alocacao.py"), encoding="utf-8").read()
-    corpo = fonte.split("# ══ PORTOES ══")[1]
-    corpo = re.sub(r'""".*?"""', "", corpo, flags=re.S)
-    corpo = re.sub(r"#.*", "", corpo)
-    corpo = re.sub(r'"[^"]*"|\'[^\']*\'', "", corpo)
+    corpo = fonte.split("# ══ PORTOES ══")[1].split("\n", 1)[1]
     PERMITIDOS = {
         "0", "1", "2", "12", "100",      # aritmetica, meses do ano, conversao para %
         "3", "4", "5",                   # indices de tupla e casas de arredondamento
         "1e-9", "1e-12", "1e-6",         # tolerancias de ponto flutuante
         "0.0", "1.0", "0.01", "365.25",  # identidades, centavo, dias do ano
     }
-    achados = set(re.findall(r"(?<![\w.])(\d+\.?\d*(?:e-?\d+)?)(?![\w.])", corpo)) - PERMITIDOS
+    permitidos = {float(v) for v in PERMITIDOS}
+    achados = {n.value for n in ast.walk(ast.parse(corpo))
+               if isinstance(n, ast.Constant) and type(n.value) in (int, float)
+               and n.value not in permitidos}
     assert not achados, f"literais numericos nao declarados no modulo: {sorted(achados)}"
 
 
diff --git a/alocacao/test_usuario_novo.py b/alocacao/test_usuario_novo.py
index 5cd773a..e8e8adb 100644
--- a/alocacao/test_usuario_novo.py
+++ b/alocacao/test_usuario_novo.py
@@ -226,7 +226,7 @@ def test_o_modelo_nao_carrega_ate_alguem_preencher():
     import yaml
     d = yaml.safe_load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                          "estado.exemplo.yaml"), encoding="utf-8"))
-    problemas, _avisos, _ = validar(d)
+    _dados, problemas, _avisos = validar(d)
     assert problemas, "o modelo em branco tem de ser recusado"
     for campo in CADASTRO_MINIMO:
         assert any(campo in p for p in problemas), \

```

Validacao adicional: `py -3.11 -m ruff check alocacao/estado_io.py alocacao/test_usuario_novo.py`: `All checks passed!`; apos CX-06, `py -3.11 -m ruff check alocacao/test_alocacao.py`: `All checks passed!`. `py -3.11 -m mypy alocacao --cache-dir .testar/mypy-prova`: `Success: no issues found in 44 source files`. O mypy avisou que corpos de funcoes sem anotacao nao sao verificados por padrao; os testes executados e a compilacao sao evidencia complementar, nao garantia de toda entrada.

## 10. Encerramento e bloco para conferência

O checkout do dono foi conferido por `git rev-parse HEAD` e `git status --porcelain`.
HEAD observado: `232ca4b882fb85cf7b8f07654db00cdfc1d5dc4b`.

Transcrição da saída de `git status --porcelain`: **vazia**.

```text
```

O que permanece sem exame: integridade do acervo real, histórico financeiro pessoal,
cobertura temporal completa das fontes, comportamento econômico de todo o motor,
implementações posteriores ao commit medido além das comparações declaradas,
e utilidade das inovações com usuários. Não há conclusão sobre esses objetos.

```yaml
auditoria:
  frente: "geral, conforme pedido posterior; guardas e testes como foco"
  commit: "97bdc5676a5e98eab9032884b53ee205cfd7c047"
  checkout_final: "232ca4b882fb85cf7b8f07654db00cdfc1d5dc4b"
  git_status_final: ""
  testar_py: "1875 passed, 12 skipped; n=5 suites; replica 97bdc56; recorte not slow and not privado and not acervo; uma execucao do orquestrador"
  provas_no_checkout_do_dono: false
  estado_pessoal_lido: false
  acervo_bruto_lido: false
  propostas_aplicadas_no_checkout_do_dono: false
achados:
  - id: CX-04
    tipo: erro
    severidade: S1
    severidade_pedido_geral: P1
    status: MEDIDO
    titulo: "Entrada aceita NaN, infinito e booleano como numero financeiro"
    arquivos: ["alocacao/estado_io.py:31-48"]
    comando: "py -3.11 -m pytest .testar/provas/test_estado_invalido.py -o addopts='' -q -p no:cacheprovider --tb=short"
    saida: "3 failed in 1.00s; DID NOT RAISE EstadoInvalido"
    n: 3
    padrao_f05: false
    ja_registrado: null
    consequencia: "NaN atravessa a carga e provoca ValueError no motor; booleano vira unidade e produz diretiva de reserva."
    conserto: "Recusar bool e centralizar verificacao de finitude; diff compilado e testado apenas na replica."
    teste_falha_antes: "Comando acima: aporte_mensal-nan, caixa-inf e despesa_mensal-True; DID NOT RAISE EstadoInvalido."
    teste_depois: "32 passed in 1.15s, verificacao direcionada conjunta de CX-04/CX-05; nao e suite completa."
    decisao_do_dono: false
    nao_coberto: "Todos os demais campos, intervalos economicos, carteira pessoal e acervo."
  - id: CX-05
    tipo: falha_silenciosa
    severidade: S2
    severidade_pedido_geral: P2
    status: MEDIDO
    titulo: "Guarda do modelo em branco testa o dicionario errado"
    arquivos: ["alocacao/test_usuario_novo.py:222-233"]
    comando: "py -3.11 -m pytest .testar/provas/test_modelo_guarda.py -o addopts='' -q -p no:cacheprovider --tb=short"
    saida: "2 failed in 0.28s; DID NOT RAISE AssertionError"
    n: 2
    padrao_f05: true
    ja_registrado: null
    consequencia: "O teste continua verde quando somem os problemas da validacao dos campos obrigatorios."
    conserto: "_dados, problemas, _avisos = validar(d)"
    teste_falha_antes: "Comando acima: nenhum_problema e so_status; DID NOT RAISE AssertionError."
    teste_depois: "20 passed in 0.44s; depois incluido nos 32 testes direcionados conjuntos."
    decisao_do_dono: false
    nao_coberto: "Capacidade dos outros testes da suite de detectar os mesmos mutantes."
  - id: CX-06
    tipo: falha_silenciosa
    severidade: S2
    severidade_pedido_geral: P2
    status: MEDIDO
    titulo: "Guarda de politica deixa passar notacoes validas de constante numerica"
    arquivos: ["alocacao/test_alocacao.py:311-328"]
    comando: "py -3.11 -m pytest .testar/provas/test_literal_guarda.py -o addopts='' -q -p no:cacheprovider --tb=short"
    saida: "2 failed, 1 passed in 1.38s; 7e+1 e 7_0: DID NOT RAISE AssertionError"
    n: 3
    padrao_f05: true
    ja_registrado: null
    antecedente: "V-03 e a classe original; os bypasses por notacao sao a prova acrescentada."
    consequencia: "A guarda anunciada contra politica fixa depende da grafia do numero e aceita k_max fixo."
    conserto: "AST das constantes numericas no mesmo recorte do modulo, preservando os valores permitidos; diff testado."
    teste_falha_antes: "Comando acima: 7e+1 e 7_0 passam pela guarda; 70.0 e recusado como controle."
    teste_depois: "4 passed in 0.76s, incluindo o teste original; Ruff All checks passed."
    decisao_do_dono: false
    nao_coberto: "Codigo fora do recorte do marcador, demais formas de constante e resposta da suite inteira ao mutante."
descartados:
  - candidato: "Dependencia de anotacao textual em _registro"
    motivo: "get_type_hints implementado; B-11."
  - candidato: "Fixtures de sessao nao vigiadas"
    motivo: "B-12 implementado, com teste de mutacao em subprocesso."
  - candidato: "E03 so mede a palavra ativo"
    motivo: "B-15 mede cenarios ligados/desligados."
  - candidato: "P72 nao verifica excecao"
    motivo: "B-14 ja exige EstadoInvalido."
  - candidato: "Alias AST do carregar"
    motivo: "B-13 cobre o bypass citado."
  - candidato: "Ausencia de detector de duplicatas"
    motivo: "Detector fundido em test_y01_yaml_duplicata.py."
  - candidato: "Ausencia de manifesto CVM"
    motivo: "Manifestos versionados lidos; integridade do bruto ficou fora."
  - candidato: "Recursao da suite inteira por subprocessos"
    motivo: "Chamadas inspecionadas rodam arquivos sinteticos isolados."
  - candidato: "Primeiro aporte sempre SEM_POSICAO"
    motivo: "P-164 implementada no checkout posterior; nao promover o comportamento da base antiga."
  - candidato: "P-173, P-174 e P-177 como achados novos"
    motivo: "Ja registradas, sem nova prova nesta rodada."
  - candidato: "Contagens de testes diferentes"
    motivo: "Nao foi demonstrada contradicao com mesmo commit, recorte e unidade."
  - candidato: "Atualizar ou eliminar dependencias"
    motivo: "Nenhum ganho ou equivalencia semantica foi provado."
```
