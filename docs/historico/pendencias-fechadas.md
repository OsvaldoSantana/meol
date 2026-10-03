# Pendências fechadas — e o que saiu do `PENDENCIAS.md` em 26/09/2026

*Movido em 26/09/2026, sem edição de texto, do `PENDENCIAS.md` da raiz (commit `c85ce59`):
todo bloco de pendência fechada, a tabela `## Fechadas`, os marcos auditáveis, o achado U-01
que abria o arquivo e as notas antigas de "Ao voltar ao desktop". O arquivo vivo ficou só com
as abertas. Os links relativos foram reescritos para esta pasta.*

**Isto é registro, nunca instrução.** A tabela `## Fechadas` continua sendo o que se consulta
antes de abrir uma pendência nova.

---

# Pendências

Registro único e vivo. Atualizado a cada sessão, **antes** de encerrar.
Regra da casa: pendência sem dono e sem gatilho não é pendência, é desabafo.

**Estado em 06/09/2026 (2ª sessão do dia) · política 1.17.0 · custos 2.1 · perfil 1.0 · catálogo 1.0 · 269 testes**

**Classes:** 42 `BLOQUEIA_O_SISTEMA` · 10 `DECISAO_DE_DESENHO` · 3 `DADO_DE_UM_USUARIO`
(P-55 fechada no mesmo dia; P-57 a P-67 abertas)

---


## Achado U-01 — o roteiro misturava o sistema com a carteira de uma pessoa

**Correção do Osvaldo, 06/09/2026:**

> *"eu não ter reserva ou aporte ser uma barreira de desenvolvimento me parece estranho.
> imagina que fosse uma ferramenta para ser vendida: eu não teria informações sobre o
> aporte e a reserva do cliente porque ele não existiria. então o sistema tem que
> existir e funcionar independente do input do usuário."*

Ele está certo, e **o sistema já funciona** — `test_usuario_novo.py` mede: patrimônio
zero, nada assinado, nada registrado, e a resposta vem completa e acionável (*"R$800/mês
para o Tesouro Reserva até R$10 mil, depois RDB; 23 meses até o alvo"*). Com a reserva
pronta, sai uma carteira de 7 rotas sem nada assinado.

**O defeito era do ROTEIRO, não do motor.** Eu vinha listando "aporte realizado = zero"
e "as duas teses não assinadas" como bloqueios de desenvolvimento. Não são: são o estado
de **um** usuário.

É o achado **L-01 num nível acima**. A L-01 separou `politica.yaml` (motor) de
`perfil.yaml` (usuário) na *configuração*. O *plano* nunca recebeu essa separação — e
por isso o caminho crítico tinha, no meio dele, coisas que só dizem respeito à carteira
do Osvaldo.

### As três classes, e a proporção é o achado

| classe | quantas | o que significa |
|---|---|---|
| **BLOQUEIA_O_SISTEMA** | 34 | o sistema não faz o trabalho dele. Prioridade real. |
| **DECISAO_DE_DESENHO** | 10 | precisa de *um* humano decidindo sobre o sistema — qualquer dono de produto responderia |
| **DADO_DE_UM_USUARIO** | **2** | P-01 e P-02. **Nunca** são bloqueio de desenvolvimento |

**Só duas de 46 são dado seu, e eu pus as duas no caminho crítico.** Toda pendência
nova nasce com a classe declarada; sem ela, não dá para saber se está no caminho
crítico ou na lista de outra pessoa.

---

> **As pendências fechadas migraram para `ACHADOS.md` em 06/09/2026.** Eram 39% deste
> arquivo — ~4 mil tokens de história de coisa já resolvida, relidos toda sessão. A
> tabela `## Fechadas` no fim continua aqui, porque ela é o que impede uma sessão nova
> de reabrir tarefa pronta; o que saiu foi a narrativa longa de cada uma.

---

## ~~P-45~~ · Migrar o trabalho de repositório para o Claude Code — **decisão sua** — **FECHADA em 26/09/2026**

O plano Pro inclui Claude Code no terminal, com **limite compartilhado** com o app. O
ritual de zip que fazemos toda sessão existe **só** porque seu computador fica
desligado; no Claude Code o arquivo é editado onde mora, e `git commit` é direto.

**A divisão proposta:** Claude Code para refatoração, teste, lint e git; este ambiente
para pesquisa, download da CVM/B3 e processamento pesado — que é do que a Fase 0
precisa.

**Gatilho:** terça, depois do push. Não antes — o primeiro passo é ter o repositório
no GitHub.

**FECHADA em 26/09/2026.** Revisão das pendências com dono Osvaldo, 26/09, na nuvem: conferida no repositório, vencida. O trabalho de repositório migrou: desde 16/09 as rodadas são feitas direto no repositório pelo Claude Code local (`CLAUDE.md`, *16/09/2026 — a segunda ponta encontrou a primeira*), e a divisão proposta aqui é a da §5-A e da §11.2. O ritual do zip acabou; os bilhetes vencidos estão em `docs/historico/entregas/`.

---

## ~~P-02~~ · Aporte realizado · `DADO_DE_UM_USUARIO` — **FECHADA em 26/09/2026**

Piso planejado R$500/mês; realizado hoje **zero**. É o único número do projeto que
nenhuma linha de código substitui. Enquanto for zero, a data da reserva completa
(**~mai/2031**, recalculada em 05/09) é projeção de um aporte que não começou.

E o achado M-01 põe isto em escala: o aporte é a alavanca de **33 meses**; o destino,
onde o sistema inteiro trabalha hoje, é a de **3**.

> **Não bloqueia desenvolvimento** (U-01). Um cliente novo de um produto tem aporte
> zero, e o sistema responde. `test_usuario_novo.py` garante isso.

**FECHADA em 26/09/2026.** Revisão das pendências com dono Osvaldo, 26/09, na nuvem: conferida no repositório, vencida. O realizado deixou de ser zero em **10/09/2026**: primeiro depósito de R$ 500 no cofrinho (`CLAUDE.md` §7, *o aporte deixou de ser zero*), classificado por ele como **aporte**, não reserva (U-02, 12/09). O valor de cada mês é dado do `estado.yaml`, que não entra no git; que o sistema dependa de alguém digitá-lo é a pergunta da P-128.

---

## ~~P-04~~ · `b3.quem_paga_custodia` fura a P1 — **decisão sua** — **FECHADA em 26/09/2026**

É `NAO_CONFIRMADO` e **não declara `bloqueia` nada**, ao contrário das outras
quatro. Insumo não confirmado que nenhum cálculo recusa não está protegido: não
bloqueia porque ninguém o lê, e se um dia alguém ler, lerá `None`.

Ou ele bloqueia algo e precisa dizer o quê, ou sai do `custos.yaml`.

**FECHADA em 26/09/2026.** Revisão das pendências com dono Osvaldo, 26/09, na nuvem: conferida no repositório, vencida. A pergunta era *"ou ele bloqueia algo e diz o quê, ou sai"*. Bloqueia e diz: `alocacao/custos.yaml → b3.quem_paga_custodia` declara `bloqueia: ["atribuicao_de_quem_paga_a_custodia"]`, e a `nota_do_bloqueio` (F-05) explica que o valor não entra em conta nenhuma — o motor supõe sempre que quem paga é o investidor, a hipótese conservadora — e que o bloqueado é uma **afirmação** ao usuário, não um cálculo.

---

## P-06 · ~~`Fonte: NAO_REGISTRADA` no layout do COTAHIST~~ **FECHADA em 19/09**

O `SeriesHistoricas_Layout.md` não registra de onde veio o PDF. Pesa porque o
achado central daquele arquivo é que as tabelas anexas da **revisão 02 (05/10/2020)**
estão desatualizadas — `TPMERC=021` e seis `CODBDI` aparecem em 2023 e não constam.
Sem a URL não dá para checar se existe revisão 03.

**Gatilho:** antes de escrever o parser do COTAHIST.

> **18/09/2026 — medido, e reclassifica a pendência.** As duas páginas públicas da série
> histórica foram lidas nesta data (a atual da B3 e o formulário no host legado) e
> **nenhuma linka documento de leiaute** — não é "eu não procurei a URL", é *a página
> onde ela deveria estar não a tem*. Transcrição em
> `docs/fontes/b3-series-historicas-cotahist.md` §5.
>
> **RETIRADO em 19/09, no dia seguinte.** O leiaute EXISTE e tem URL:
> `www.b3.com.br/data/files/33/67/B9/50/D84057102C784E47AC094EA8/SeriesHistoricas_Layout.pdf`
> — **revisão 02 de 05/10/2020**, a mesma que o projeto transcrevia. **Não há revisão 03**,
> que era a pergunta da pendência. Fonte em `docs/fontes/b3-cotahist-leiaute.md`.
>
> Ele está numa **terceira** página — *Cotações Históricas*, não *Séries Históricas*. Eu
> tinha lido duas e concluído sobre "a página onde ela deveria estar". §5-B.13 dois dias
> seguidos. **A pendência fecha, e o que sobra é a P-95:** o leiaute **não traz tabela de
> valores para `MODREF`** — não é tabela incompleta, é inexistente.
>
> ~~A P-06 deixa de ser *achar um link* e passa a ser *decidir o que fazer sem ele*, e a
> saída provável é limitação declarada:~~ o layout que o projeto usa é cópia sem fonte
> verificável, e a enumeração real tem de sair do **dado observado** com falha ruidosa
> fora dela — que é o que a P-95 já mandava, por outro motivo.

---

## ~~P-43~~ · Há um TERCEIRO catálogo — achado T-01 — **FECHADA em 24/09/2026: apagado**

`motor.montar_rotas` é paralelo ao `catalogo.yaml`: **22 rotas contra 25, com 13 nomes
que só existem lá**. A P-36 disse "os dois catálogos" e havia três. Nenhum módulo de
produção o chama — só o `test_motor.py`.

O ruff viu uma **variável** morta; o defeito era a **chamada**: `B3V = val(...)` era
cópia da função de baixo, e a chamada **abortaria** se o valor fosse `NAO_CONFIRMADO`,
dentro de uma função que promete *"capturar InsumoBloqueado como marcador em vez de
abortar"*. A linha saiu.

**O catálogo não foi apagado, e a decisão é sua.** Apagar código com teste próprio sem
medir o que os testes guardam é como se perde uma rede. As opções:

| | consequência |
|---|---|
| apagar `montar_rotas` + os testes dele | some a cobertura de K-06 e K-07 — precisa medir se `test_alocacao` já cobre |
| migrá-lo para YAML também | ele vira o catálogo da **camada de custo**, com procedência, e passa a poder discordar visivelmente do de alocação |
| deixar e declarar | duas fontes de verdade sobre os mesmos custos, sem nada as confrontando |

**Recomendo a segunda**, com um teste que confronte os dois onde eles se sobrepõem —
mas é decisão sua, e não é urgente.

> **RETRATAÇÃO — 24/09/2026.** A recomendação acima (*"migrá-lo para YAML também … com um
> teste que confronte os dois"*) estava errada, e a medição da sessão B a derrubou (B-16):
>
> - `motor.simular` e `montar_rotas` **só eram chamados por testes** — nenhum módulo de
>   produção, nenhum script (`impacto.py` e `grep` nas três pastas);
> - o `motor.simular` **não tem a custódia interna do F-01**: lê `adm_aa`, e a alocação lê
>   `interno_aa` (adm + custódia interna). Com o espelho honesto, 9 de 57 pares divergem —
>   `bova11` até **+17,4%**;
> - ou seja, **a divergência inteira estava no código morto**. Migrar e confrontar teria
>   construído um YAML e um teste para manter viva uma segunda simulação cujo único
>   comportamento distinto era um defeito já corrigido do outro lado.
>
> **A causa raiz do erro de método:** recomendei a opção que parecia mais rigorosa
> (*"passa a poder discordar visivelmente"*) sem medir se havia um consumidor para quem a
> discordância importasse. Confronto entre duas implementações só vale quando as duas
> servem a alguém; quando uma não serve a ninguém, confrontá-la é manter o A-07 com
> teste. **Decisão técnica delegada ao Claude em 24/09**, e tomada: apagar.

**Fechamento, 24/09/2026:**

1. **B-17 antes de apagar:** a única leitura de `b3.custodia_rv_interpretacao` estava no
   `motor.simular`. `simular_custo` passou a lê-la, e `custodia_rv_aa` recusa valor fora de
   `deducao`/`limiar` (um erro de digitação viraria `limiar` calado). Dois testes em
   `test_alocacao.py` (`test_B17_*`), **os dois reprovam por mutação** (leitura retirada).
2. **Cobertura medida antes de apagar os testes:** F-02/E-01 (rota bloqueada recusa) e aporte
   zero já estavam no `test_alocacao`; K-07 estava só para o BOVV11. **K-06 (perna de saída) e
   K-07 da Vest só existiam no `test_motor`** — trazidos como `test_K06_*` (atributo **e**
   simulação: zerar `saida_extra` tem de baixar o custo) e `test_K07_*`.
3. **Apagados:** `Rota`, `montar_rotas`, `custo_entrada_pct`, `custo_saida_pct` e `simular` do
   `motor.py`, e 7 testes do `test_motor.py`. **Perda declarada:** o cenário
   `custodia_absorvida` do K-04 não tem par na alocação; a absorção vive no ranking de
   corretoras (`corretoras.py`), e a nota do `custos.yaml` que apontava para o cenário foi
   corrigida. O alerta do K-08.3 (custo de entrada ≥ aporte) virou a **P-134**.
4. **Instantâneo dourado inalterado:** `simular_custo` + `arrasto_anualizado` +
   `custo_pct_aportado` em 25 rotas × 4 configurações (100 pares, 76 simulados, 24
   bloqueados), `sha256 afea5570…` antes e depois; `cenarios.py` (`393f4925…`) e
   `demo_aporte.py` (`fda2cedc…`) byte a byte idênticos. `alocacao`: 537 → **534 passed**
   (−7 apagados, +4 novos).

---

## ~~P-47~~ · Eventos societários da B3 — o insumo que faltava no plano inteiro — **FECHADA em 26/09/2026**

**Classe:** `BLOQUEIA_O_SISTEMA`. **Dono:** Osvaldo (rodar) + Claude (processar).
**Gatilho:** terça, 08/09 — antes de qualquer download da CVM.

Sem proventos, desdobramento, grupamento e bonificação, **uma série de preços não serve
para backtest**. A PETR desdobrou 100:1 em 25/04/2008 — confirmado em primeira mão no
endpoint da B3, com `factor: 100,00000000000` e `lastDatePrior: 25/04/2008`. O preço cai
99% num dia. COTAHIST cru lê isso como um crash de 99%.

**Não havia uma linha sobre isso em lugar nenhum do plano.** O blueprint listava COTAHIST
e CVM e parava aí. Um backtest rodado sobre esse acervo teria produzido números e eles
teriam parecido plausíveis.

A fonte existe, é gratuita e é programática, mas **não é documentada**:
`sistemaswebb3-listados.b3.com.br/listedCompaniesProxy/CompanyCall/GetListedSupplementCompany/{base64}`.
Sem contrato, sem SLA, sem espelho conhecido. Por isso **vem antes da CVM**: DFP/ITR são
ZIP estático em portal oficial; isto pode sumir sem aviso.

`fase0/coletar_b3.py` está escrito, compila e teve a lógica testada (a rede não — ver
P-49). Ele grava snapshot datado imutável, com sha256 e manifesto JSONL.

**A armadilha embutida, e ela é o F-02 de novo:** a chave é texto, e chave errada devolve
HTTP 200 com listas vazias, **em silêncio**. Gravar isso como "empresa sem eventos" é
escrever ausência de dado no lugar de dado. O coletor acusa em voz alta; o parser, quando
existir, precisa recusar.

**FECHADA em 26/09/2026.** Revisão das pendências com dono Osvaldo, 26/09, na nuvem: conferida no repositório, vencida. Rodou em 11/09: carteira do IBOV (76 ativos) e eventos de **74 de 74** emissoras, `dt_captura=2026-09-11`, com sha256 (`CLAUDE.md` §7, item 1; `PLANO.md` §2, *B3 — eventos societários: completo*), e o histórico longo por `--proventos-completos` (132 páginas). O processamento também existe: o silver em `fase0/refinar.py`, que recusa em voz alta valor fora da lista `OBSERVADO` (A-05), e a série ajustada em `fase0/ajustar.py` (C-02). **O que esta pendência não cobria e continua aberto:** a captura foi uma vez só — os eventos não estão no workflow diário nem no armazém. Vai para a **P-150**.

---

## ~~P-49~~ · `coletar_b3.py` nunca tocou a rede — e não pode tocar daqui — **FECHADA em 26/09/2026**

**Classe:** `BLOQUEIA_O_SISTEMA`. **Dono:** Osvaldo. **Gatilho:** terça, primeira coisa.

O script compila e a lógica pura foi testada (montagem do base64, derivação
`PETR4 → PETR`, recusa de sobrescrita). **O caminho de rede não rodou**, porque a máquina
de download é a dele — ver a correção da §11.2 do CLAUDE.md.

O que precisa ser conferido no primeiro uso:
- se `BPAC11 → BPAC`, `KLBN11 → KLBN`, `IGTI11 → IGTI` são de fato os códigos de
  emissora que o endpoint aceita. **Só `PETR` foi confirmado.** Unit e BDR podem ter
  outra regra, e a falha é silenciosa;
- se as 76 emissoras respondem, ou quantas voltam sem `tradingName`;
- se a pausa de 1,2 s é suficiente para não tomar bloqueio.

```powershell
cd C:\...astter
python fase0\coletar_b3.py --indice IBOV
python fase0\coletar_b3.py --eventos          # usa a carteira recém-capturada
```

**FECHADA em 26/09/2026.** Revisão das pendências com dono Osvaldo, 26/09, na nuvem: conferida no repositório, vencida. Tocou a rede em 11/09, na máquina dele: quebrou três vezes (A-00 a A-02, `CLAUDE.md` §5-A) e fechou em 74/74 em 12/09 pela cascata de nome do B-03 (`ACHADOS.md`, 12/09, marco 3). As três conferências pedidas foram respondidas pela corrida: a regra de emissora é posicional (A-01), e código que muda não traz o histórico junto (A-03, A-04).

---

## ~~P-54~~ · A rotina de snapshot da CVM é SEMANAL — e ainda não existe — **FECHADA em 26/09/2026**

**Classe:** `BLOQUEIA_O_SISTEMA`. **Dono:** Osvaldo (rodar) + Claude (escrever).
**Gatilho:** terça, junto do coletor da B3.

Confirmado na fonte em 06/09 (`docs/fontes/cvm-dfp-politica-atualizacao.md`, COMPLETO):
a CVM atualiza **semanalmente** os arquivos dos **últimos cinco anos**, com as
reapresentações. Os de 2010 a 2020 estão congelados.

**O que muda em relação ao que o projeto acreditava:**

| acreditava | é |
|---|---|
| o arquivo do ano corrente é reescrito | **os seis últimos** são, toda semana |
| o prazo vence em 31/12 | o prazo vence **toda semana** |
| são 1,5 GB correndo contra o tempo | são **6 arquivos**; os outros 11 podem esperar |

Última atualização registrada pela CVM: **31/08/2026, 08:01**. Entre ela e a terça
haverá pelo menos mais uma rodada — a primeira captura já nasce com uma semana perdida,
e isso não é recuperável.

O que falta: uma rotina que rode toda semana e grave
`data/bronze/cvm/dfp/dt_captura=AAAA-MM-DD/`, com sha256 e manifesto, **sem sobrescrever**.
O `coletar_b3.py` já tem a forma; falta o equivalente para a CVM, e ele pode reusar
`cvm_catalogo.py` para ler o `last_modified` de cada recurso e só baixar o que mudou.

**FECHADA em 26/09/2026.** Revisão das pendências com dono Osvaldo, 26/09, na nuvem: conferida no repositório, vencida. A rotina existe e é **diária**, não semanal: `.github/workflows/captura_cvm.yml`, decidida na P-57 e fechada em 25/09 — primeira execução agendada `36148547193`, sem ninguém disparar; registro em `docs/acervo/cvm/capturas.csv`, byte no R2 por sha256, nunca sobrescrito. Não precisa de ninguém para rodar.

---

## ~~P-55~~ · Política do ITR — **FECHADA em 06/09/2026, no mesmo dia**

Conferida na fonte (`docs/fontes/cvm-itr-politica-atualizacao.md`, COMPLETO). É
**idêntica** à do DFP: semanal, últimos cinco anos, histórico desde 2011.

Duas coisas vieram de brinde: os recursos do ITR **vêm rotulados por ano** (2021…2026),
o que converte a janela de inferência em observação; e o carimbo `31/08/2026 08:01` é
**o mesmo nos dois conjuntos, ao minuto** — é um único job semanal do portal, então uma
única rotina cobre os dois e um único `last_modified` decide se vale baixar.

---

## ~~P-57~~ · A captura semanal não pode depender do Osvaldo lembrar — achado W-01 — **FECHADA em 25/09/2026**

**Classe:** `BLOQUEIA_O_SISTEMA`. **Dono:** Claude. **Gatilho:** antes de considerar a
Fase 0 concluída.

**Correção dele, 06/09/2026.** Eu ofereci montar um lembrete semanal:

> *"o lembrete no caso seria exatamente para quê? uma das coisas do projeto é
> estabilidade, e um projeto escalável não deve depender de mim para funcionar."*

Está certo. Virou a **doutrina P7** do CLAUDE.md. E é a terceira vez que eu ponho ele no
caminho crítico de algo que é do sistema — U-01, P6, e agora esta.

### O problema real, sem disfarce

A captura precisa de três coisas ao mesmo tempo: **gatilho** (semanal), **rede**, e
**disco** que retenha os snapshots. A máquina dele fica desligada quase sempre; o Task
Scheduler do Windows não roda em máquina desligada, então ele não é solução — é o mesmo
lembrete com outro nome.

### A separação que torna o problema tratável

Os dois lados têm custo de armazenamento muito diferente, e tratá-los junto é o que faz
o problema parecer impossível:

| | tamanho | automatizável hoje |
|---|---|---|
| **eventos societários da B3 + carteira de índice** | JSON, poucos MB por captura | **sim** — cabe em repositório, cabe em runner gratuito |
| **metadado da CVM** (`last_modified` dos 2 conjuntos) | bytes | **sim** — e é o que decide se vale baixar |
| **os 6 ZIPs da CVM** | centenas de MB por captura | **não trivialmente** — é aqui que mora o custo |

> ⚠ **RETRATAÇÃO — 24/09/2026:** tratada como manual; um script na máquina dele resolve. A limitação era da ferramenta de quem respondia, não da tarefa. Hoje é `py -3.11 fase0/capturar_cvm.py` (CLAUDE.md §3, §5-B.17).

**Ou seja: a parte irreplicável e perecível é a barata.** O que é caro de guardar (os
ZIPs) é justamente o que dá para reconstruir parcialmente, porque a CVM mantém a versão
corrente; o que não dá para reconstruir de jeito nenhum (eventos societários, composição
de índice, e o *histórico* de `last_modified`) é pequeno.

### O que investigar antes de decidir

- **GitHub Actions com `schedule`** — cron semanal, sem máquina ligada. Cobre B3 e
  metadado da CVM com folga. Limites de minuto e de armazenamento em repositório
  privado: **NAO_CONFIRMADO**, precisa ser lido antes de prometer.
- Onde guardar os ZIPs quando o metadado acusar mudança, e por quanto tempo. Talvez a
  resposta honesta seja: **não guardar todos**, e declarar isso.
- Se o próprio `last_modified` capturado semanalmente já entrega parte do valor
  point-in-time sem guardar o conteúdo — ele diz *quando* mudou, mesmo sem dizer *o quê*.

### A resposta, pesquisada no mesmo dia

`docs/fontes/executor-da-rotina-semanal.md`. **GitHub Actions em repositório privado.**
14 GB de disco efêmero, 6 h por job, 2.000 min/mês (a rotina usa 100–200), banda não
tarifada, e **sem pausa por inatividade** — a regra dos 60 dias só vale para repo público.

**Supabase está descartado como executor**, e o motivo é preciso: projeto Free **pausa
após 1 semana de inatividade**, com restauração manual. Uma rotina semanal vive em cima
desse limiar — seria a P7 violada pela própria infraestrutura. Edge Function ainda por
cima limita a 150 s, 256 MB e upload de 50 MB.

**E o armazenamento deixou de ser problema:** guarda-se o **delta**, não o snapshot.
Poucas centenas de MB por ano em vez de dezenas de GB, versionado no próprio git.

**O que falta para fechar:** escrever o workflow, e a primeira execução real. Página de
limite lida não é rotina rodando — até lá, a limitação vai declarada.

**A armadilha a embutir no desenho:** 404 + unzip vazio = "nenhuma mudança", que é
indistinguível de "a CVM não mudou nada". `set -euo pipefail`, conferência de sha256, e
notificação em `if: failure()`. Ausência de mudança se **afirma**, não se infere.

**24/09/2026 — o comando existe; o executor não.** `fase0/capturar_cvm.py` (auditado do
`tools/baixar_cvm.py` que outra IA escreveu) captura todos os anos do índice com portão HEAD,
confere cada download (Content-Length + `testzip`), guarda a versão deslocada com a data da
versão e anota **toda** observação, `inalterado` inclusive, em `docs/acervo/cvm/capturas.csv`.
A armadilha acima está coberta: índice vazio sai com erro, e `inalterado` é linha escrita, não
ausência de linha. **Onde ele roda toda semana continua aberto e é decisão dele.** A
limitação `captura_da_cvm` segue declarada até a primeira execução sem mão humana. Cada
semana sem rodar é uma versão perdida (CV-01).

**24/09/2026 — DECIDIDA e construída: GitHub Actions + Cloudflare R2.** Decisão técnica
delegada ao Claude; desenho, alternativas descartadas, riscos e defesas em
**`docs/decisoes/P-57.md`**. Construído e testado sem rede (63 testes novos em `fase0/`: 340 → 403):

| peça | arquivo |
|---|---|
| armazém (nunca sobrescreve; confere sha256 na subida e na descida) | `fase0/armazem.py` |
| captura na nuvem (`--armazem s3`, `--cache`) | `fase0/capturar_cvm.py` |
| leitura e frescor (`abrir`, `frescor` > 8 dias → `CapturaParada`) | `fase0/acervo.py` |
| carga inicial (plano; `--aplicar`) | `fase0/subir_acervo_local.py` |
| executor diário | `.github/workflows/captura_cvm.yml` |

**Desvio do pedido, com o motivo:** o `inalterado` por *hash coincide* vai para o
`capturas.csv`, não para o log — é a única linha que leva o `Last-Modified` novo ao estado;
sem ela o portão baixaria o mesmo arquivo todo dia. Os `inalterado` do portão HEAD vão para
`logs/capturas/<AAAA-MM-DD>.csv` no armazém, como pedido.

**O que falta para fechar, em ordem** — ⚙ **os dois primeiros exigem o desktop**:
1. `py -3.11 -m pip install "boto3==1.43.101"` e, com as `R2_*` no ambiente,
   `py -3.11 fase0/subir_acervo_local.py --aplicar` (87 arquivos, 1.565 MiB no plano de 24/09).
   Commitar os dois `inventario-armazem.csv` que ele grava.
2. Disparar o workflow **Captura CVM** pela aba Actions (ou esperar o cron das 09:15 UTC) e
   conferir que ficou verde e que `logs/capturas/<dia>.csv` apareceu no bucket.
3. Com a primeira execução verde: tirar `captura_da_cvm_e_manual_e_o_dado_e_perecivel` de
   `limitacoes_declaradas` — e declarar o regime automático onde o
   `test_P7_todo_acervo_tem_regime_de_captura_declarado` o leia, senão ele reprova no mesmo
   minuto (é o desenho dele). Aí esta pendência fecha.

**24/09/2026 — o teto do armazém (pedido dele: cobrança zero).** O R2 não tem limite de
gasto, então o limite é do código: `politica.yaml → armazem.aviso_gb = 7`, `teto_gb = 9`
(1.27.0). `armazem.py` soma o bucket **antes de cada envio** — a soma, não um contador,
porque a carga inicial roda de outra máquina — e um `ArmazemS3` de `do_ambiente()` já nasce
limitado. Acima do aviso o workflow abre **uma** issue *"Armazem em X GB"* (atualiza a
aberta); um envio que levaria acima do teto é recusado, o registro ganha
`recusado_por_teto` e o job fica vermelho. O log da rodada é isento (KB, e é a prova da
recusa). 15 testes; a guarda reprova 4 deles quando removida (mutação). O que o teto não
cobre — token vazado — está em `limitacoes_declaradas.o_teto_do_armazem_e_do_codigo`.
Ocupação na carga inicial: **1,64 GB** (soma dos dois `inventario-armazem.csv`).

---


**25/09/2026 — FECHADA.** A execução `36148547193` (evento `schedule`, sem ninguém disparar) rodou os passos `captura` e `captura_b3` verdes, conferido passo a passo pela API do GitHub. O regime virou dado: `politica.yaml → regimes_de_captura` (1.31.0), lido por `manifesto_cvm.defeitos_de_regime()`, e as duas limitações ficaram `RESOLVIDA`. **O que não foi conferido daqui:** o `logs/capturas/<dia>.csv` no bucket (a sessão na nuvem não tem as credenciais do R2). E o cron das 09:15 UTC saiu às 14:35 UTC: o horário do agendamento não é garantido pelo GitHub.

## ~~P-62~~ · Repositório público — **DECIDIDO em 06/09**, com pré-requisito duro — **FECHADA em 26/09/2026**

**Classe:** `DECISAO_DE_DESENHO`. **Dono:** Osvaldo (decidiu) + Claude (executar).
**Gatilho:** antes do primeiro `git push`.

Ele disse não ter problema com repositório público. Isso **melhora** a automação: repo
público tem Actions sem consumo de cota e runner maior (4 vCPU/16 GB contra 2/8). A regra
dos 60 dias de auto-desativação do cron deixa de morder porque **o próprio workflow
commita o delta toda semana**, e commit é atividade.

**Mas há um pré-requisito que não é negociável:** `alocacao/estado.yaml` guarda a situação
financeira real dele — patrimônio, aporte, dívida. Em repositório público, isso **não
entra**, e a U-01 já provou que não precisa: `test_usuario_novo.py` mede que o sistema
funciona com estado vazio, e `estado.exemplo.yaml` existe para ocupar esse lugar.

A favor: nada foi empurrado ainda, então **não há histórico para reescrever** — a janela
limpa é agora. Se um commit com `estado.yaml` for para o GitHub público, a correção passa
a exigir reescrita de histórico, e a cópia já vazou.

**`perfil.yaml`: ele decidiu que pode ser público.** Perguntado na forma correta ("você
quer isso público, podendo não ter?"), respondeu que sim. Fica registrado como
`DECISAO_DO_USUARIO`, e sobrevive à carteira mudar.

**`estado.yaml` continua fora**, e isso não é preferência: é o único arquivo que carrega
patrimônio, aporte e dívida reais. O `.gitignore` precisa listá-lo **antes** do primeiro
`git add`, e o teste que guarda isso ainda não existe — ver P-67.

**FECHADA em 26/09/2026.** Revisão das pendências com dono Osvaldo, 26/09, na nuvem: conferida no repositório, vencida. O repositório é público e empurrado desde 18/09 (`b1d06f4..3ee5e97`, `CLAUDE.md`, terceira rodada de 18/09). **O pré-requisito falhou antes de a guarda existir:** o `estado.yaml` foi empurrado em 08/09, e isso está escrito no bloco *SEGREDO* do `.gitignore`. Hoje ele está fora (três padrões no `.gitignore`) e `alocacao/test_p67_segredo.py` mede o índice do git. O histórico público não foi reescrito, por decisão dele de 25/09 (`CLAUDE.md` §6, exceção à D-01).

---

## ~~P-68~~ · O primeiro aporte existe — e a pergunta certa não é quanto, é se está livre — **FECHADA em 26/09/2026**

**Classe:** `DADO_DE_UM_USUARIO`. **Dono:** Osvaldo. **Gatilho:** antes de rodar qualquer
projeção de Fase A com número real.

**10/09/2026: R$500 depositados**, no cofrinho do PicPay a 121% do CDI, obtido *"por
completar as missões"*.

O projeto já mediu esse produto, e o registro é desconfortável (`custos.yaml`, seção
`cofrinho`, achados J-01/J-02/K-01):

- o Turbinado a 121% que foi analisado em 05/09 vem com **mensalidade de R$287,88/ano** e
  exige **R$2.500 de gasto no cartão em 3 meses**;
- o diferencial de 121% para 102% vale **2,113% a.a. líquido de IR** — e, no teto,
  **PERDE R$76,60 por ano** contra o cofrinho comum;
- e o principal: **o cofrinho que rende mais é caução do limite do cartão.** Dinheiro
  empenhado **não é reserva** — é garantia. O `Estado` já separa `reserva_atual` de
  `reserva_disponivel` exatamente por isso.

### RESPONDIDA em 10/09 pela tela do app — e a resposta contraria o que ele disse

`docs/fontes/picpay-cofrinhos-2026-09-10.md`, status OBSERVADO.

Ele escreveu *"os 500 reais é livre"*. **A tela do produto diz o contrário**, em duas
marcações independentes: *"O saldo deste cofrinho está ativo como limite do seu cartão"*
e a etiqueta `LIMITE DO CARTÃO` na lista.

A distinção por trás disso é real: o cofrinho é **líquido** (resgata quando quiser) e
**empenhado** (resgatar derruba o limite) ao mesmo tempo. É exatamente por isso que o
`Estado` separa `reserva_atual` de `reserva_disponivel` desde o J-01.

**E apareceu o número que faltava:** total guardado **R$ 8.181,71** — R$500 no Turbinado
(121%) e **R$ 7.681,71 no Cofrinho do Cartão (120%)**, os dois etiquetados
`LIMITE DO CARTÃO`.

> **O M-01 estava certo pelo motivo certo.** Ele registrou que "~mar/2030" fora calculado
> com **R$7.671 de reserva inicial** e que isso estava errado *"porque a reserva é zero"*.
> O saldo hoje é **R$7.681,71**. **O número existia** — o que estava errado era chamá-lo
> de reserva. Agora há evidência, com etiqueta do próprio app.

**O que ainda falta, e é o único número que define a Fase A:** quanto do limite está
**comprometido** hoje. `reserva_disponivel = 8.181,71 − limite usado`. Com limite zerado,
a reserva é R$8.181,71 e a Fase A está muito à frente do que o projeto supõe; com o limite
todo usado, é **zero**, e o dinheiro garante dívida que já existe.

### Decisão dele em 11/09, e o registro guarda as duas coisas separadas

> *"considerar 500 reais livres — devo ter clicado na hora de depositar para usar como
> limite"*

**Registrado assim, e a separação é o ponto:**

| campo | valor | status |
|---|---|---|
| estado observado do Turbinado | `LIMITE DO CARTAO` | **OBSERVADO** — etiqueta do app, 10/09 |
| `reserva_disponivel` dos R$500 | 500 | **DECISAO_DO_USUARIO**, `NAO_CONFIRMADO` na fonte |

Não é firula de modelagem: as duas afirmações podem ser verdadeiras ao mesmo tempo — o
app mostra o estado de hoje, ele descreve a intenção e o que pretende desfazer. Misturá-las
num campo só apagaria qual das duas o sistema está usando.

**A conferência que fecha isso leva 30 segundos:** no cofrinho Turbinado há a linha *"O
saldo deste cofrinho está ativo como limite do seu cartão"* com uma seta. Entrar, desligar,
e tirar outra captura. Aí `reserva_disponivel = 500` vira **OBSERVADO** e a decisão some do
caminho — que é sempre o desfecho melhor.

> **O risco real, e ele é uma hipótese, não um fato:** na lista, **os dois** cofrinhos
> aparecem com a etiqueta `LIMITE DO CARTAO` — inclusive o de 120%. Pode ser que, no
> PicPay, **taxa alta e caução sejam o mesmo produto**, e que desligar o limite jogue o
> saldo para o cofrinho comum de 102%. Se for o caso, não existe "R$500 livre a 121%": há
> uma escolha.
>
> **E o preço dessa escolha é pequeno e já está medido:** 121% × 102% sobre R$500 é
> **R$13,20/ano bruto**. Treze reais por ano é o que custa ter esse dinheiro solto — e num
> projeto cuja Fase A depende de reserva de verdade, é barato. Mas é decisão dele, não
> minha, e depende de a hipótese se confirmar. `NAO_CONFIRMADO`.

**FECHADA em 26/09/2026.** Revisão das pendências com dono Osvaldo, 26/09, na nuvem: conferida no repositório, vencida. **O fechamento de 12/09 nunca chegou a este cabeçalho.** `CLAUDE.md` §7: *"P-68 FECHADA em 12/09"* — do Cofrinho do Cartão, R$ 4.202,12 estão disponíveis para retirada, e dá para desligar o limite sobre o Turbinado. A classificação é dele (U-02): o saldo do cartão **não** é reserva, e os R$ 500 são aporte. O cabeçalho ficou aberto catorze dias: é a fila desatualizada que a §5-A condena, e foi achada por esta revisão.

---

## ~~P-75~~ · O ambiente instalado diverge dos pinos, e o Python é outro — **FECHADA em 26/09/2026**

**Classe:** `BLOQUEIA_O_SISTEMA`. **Dono:** Osvaldo. **Gatilho:** antes de acreditar em
qualquer número produzido na máquina dele.

Instalado em 10/09: **numpy 2.5.3, pandas 3.0.5**, em **Python 3.13**.
Declarado no `pyproject.toml`: **numpy==2.4.4, pandas==3.0.2**, `requires-python ==3.11.*`.

**As três divergem, e as duas primeiras são as que MUDAM NÚMERO** — `alfa_contra_fatores`
resolve por `numpy.linalg.lstsq`, `mensal()` compõe por `pandas.groupby`.

Isto é o P-15 fazendo exatamente o trabalho dele: a divergência virou evento visível em
vez de número silenciosamente diferente. **A saída não é afrouxar o pino.** Ou se instala
o declarado, ou se muda o declarado **com medição** e registro em `REGISTRO-vN.md`.

Enquanto isso vale a regra já escrita no CLAUDE.md §3: a suíte continua verde e **isso
está certo** — o que deixa de valer não é o código, é a *reprodução* de um resultado
pré-registrado.

---



- livres → `reserva_atual = 500`, `reserva_disponivel = 500`. A Fase A começou.
- empenhados → `reserva_atual = 500`, `reserva_disponivel = 0`. **A reserva continua zero**,
  e o que existe é uma caução que rende.

E uma segunda, que pode **melhorar** o registro do projeto: se os 121% vieram de **missões**
e **não** de mensalidade, então a aritmética do K-01 não se aplica a este caso — o custo de
R$287,88/ano some, e o Turbinado deixa de perder para o cofrinho comum. **Seria a primeira
vez que um achado do projeto é derrubado por um fato novo em vez de por um erro.** Não
presumi: o K-01 fica como está até a captura do app confirmar.

**FECHADA em 26/09/2026.** Revisão das pendências com dono Osvaldo, 26/09, na nuvem: conferida no repositório, vencida. Mesma medição da P-73: em 12/09 o `ambiente.py`, no 3.11.9, com **numpy 2.4.4, pandas 3.0.2**, PyYAML 6.0.3 e pytest 9.1.1, disse *"O ambiente instalado E o registrado"* (`ACHADOS.md`, 12/09, marco 1). E a divergência não volta calada: o Dependabot ignora numpy e pandas desde 25/09 (P-148).

---

## ~~P-73~~ · A máquina roda Python 3.13 e o projeto exige 3.11 — **FECHADA em 26/09/2026**

**Classe:** `BLOQUEIA_O_SISTEMA`. **Dono:** Osvaldo. **Gatilho:** antes de acreditar em
qualquer número produzido lá.

`pyproject.toml` fecha em `requires-python = "==3.11.*"`, e a faixa é fechada **de
propósito**: 3.12 mudou o comportamento de comparação de `datetime.date` em alguns
caminhos, e o projeto compara `expira` em quase todo `val()`.

Isto é o P-15 fazendo o trabalho dele — a divergência virou um evento visível em vez de um
número silenciosamente diferente. **A saída não é reabrir a faixa por conveniência**: ou se
instala o 3.11, ou se reabre **com medição** e se registra em `REGISTRO-vN.md`.

Enquanto isso, um resultado produzido no 3.13 é **número novo**, não conferência de um
antigo.

**FECHADA em 26/09/2026.** Revisão das pendências com dono Osvaldo, 26/09, na nuvem: conferida no repositório, vencida. **Fechada em 12/09 no `ACHADOS.md` e nunca aqui.** Python 3.11.9 instalado em 11/09; o `ambiente.py` disse *"O ambiente instalado E o registrado"*, impressão `7565df1381e2c1ed` (`ACHADOS.md`, 12/09, marco 1: *"P-73 fechada"*; `CLAUDE.md` §3). O CI roda 3.11 também.

---

## ~~P-76~~ · A F-03 se declarou refutada com um insumo que não autoriza refutação — **FECHADA em 26/09/2026**

**Classe:** `DECISAO_DE_DESENHO`. **Dono:** Osvaldo decide a regra; Claude implementa.
**Gatilho:** quando o regulamento do IMAB11 for baixado (P-05/P-50) — ou antes, se
qualquer decisão sobre a rota de ETF de renda fixa for tomada.

Aberta ao fechar a P-69. A F-03 foi medida em 05/09 **à mão, com 0,25%** (está em
`politica.yaml → fora_de_escopo.ETF_renda_fixa`) e registrada como *"hipótese caiu,
Tesouro vence em todas as faixas"*. Mas o próprio insumo é `PARCIAL`, com
`bloqueia: comparacao_definitiva_imab11_vs_td_ipca`, e o `motivo` diz por quê: **a
página do gestor não diz se 0,25% é teto de regulamento ou taxa efetiva.**

Isso não é detalhe. Se 0,25% for o **teto**, a taxa cobrada pode ser menor que 0,20% —
e a comparação **inverte**. A conclusão saiu mais forte que o insumo que a sustenta: é a
P1 aplicada ao relato de uma medição, não ao dado.

**A decisão que falta:** uma conclusão medida herda o status do insumo mais fraco dela?
Se sim, a F-03 volta a "tendência medida, não refutação" até o regulamento chegar, e a
linha da F-03 em `## Fechadas` ganha a ressalva. Não mexi em nenhum dos dois registros.

**FECHADA em 26/09/2026.** Revisão das pendências com dono Osvaldo, 26/09, na nuvem: conferida no repositório, vencida. **Fechada em 13/09 no `ACHADOS.md` e nunca aqui** (`docs/auditoria/P76-P78-B04.md`). A regra saiu: uma conclusão **não herda** o status do insumo mais fraco — herda uma **medição de sensibilidade** (sobrevive à faixa → `COMPLETO` com a faixa; inverte dentro dela → `PARCIAL` com a fronteira). É a linha da P-76 no índice da `CLAUDE.md` §7. A F-03 foi remedida depois com a lâmina do gestor e o Tesouro IPCA+ vence em todas as faixas (índice, linha F-03).

---

---

## ~~P-80~~ · A rotina mede um terço do projeto — **FECHADA em 26/09/2026**

**Classe:** `DECISAO_DE_DESENHO`. **Dono:** Osvaldo decide; Claude implementa.
**Gatilho:** agora — as três suítes estão verdes ao mesmo tempo, e é a janela barata.

`pyproject.toml` declara `testpaths = ["alocacao"]`, e `test_p40_lint.py` roda
`ruff check .` com `cwd=alocacao/`. Consequência medida em 16/09: `py -3.11 -m pytest -q`
dava **verde** enquanto `pytest fase0` tinha **9 falhas** e `pytest auditoria` tinha
**2** — e `ruff` tinha **5 violações** em `fase0/refinar.py` que nenhum portão olhava.

Isto é a **P7 aplicada à própria rotina**: rodar as outras duas depende de alguém
lembrar, então não é rotina. E o preço já foi pago: o A-06 sobreviveu quatro dias e a
linha de base das órfãs apodreceu, as duas coisas dentro das pastas que o portão não vê.

**A mudança é de uma linha e meia,** e não a apliquei porque ela **redefine o que
"verde" significa** neste projeto — isso é decisão sua, não minha:

```toml
testpaths = ["alocacao", "auditoria", "fase0"]
```

e, no lado do lint, `ruff check .` a partir da RAIZ. Esse segundo pede uma decisão a
mais: a raiz tem **14 violações** em `docs/historico/pesquisa-custos-2026-08/calc/`, que é cópia
congelada de pesquisa. Ou ela entra em `[tool.ruff] exclude` com o motivo escrito ao
lado, ou o portão nasce com linha de base — e linha de base conhecida não é barreira
(é o próprio texto do `test_P40_ruff_esta_em_zero`).

**FECHADA em 26/09/2026.** Revisão das pendências com dono Osvaldo, 26/09, na nuvem: conferida no repositório, vencida. **Resolvida por outro caminho.** O defeito era a P7: `fase0` e `auditoria` só rodavam se alguém lembrasse. Desde 25/09 ninguém precisa lembrar: `.github/workflows/testes.yml` roda as **quatro** suítes (`alocacao fase0 auditoria tools`) e `ruff`/`mypy` nas quatro pastas em todo push e em todo PR (`CLAUDE.md` §12), e os PRs de 25/09 foram mesclados com ele verde. O `testpaths = ["alocacao"]` do `pyproject.toml` ficou como estava: `pytest -q` na raiz continua medindo um terço, mas deixou de ser o portão.

---

## ~~P-77~~ · Meia P-13 — **FECHADA 16/09/2026**, ver `## Fechadas`

**Classe:** `BLOQUEIA_O_SISTEMA`. **Dono:** Claude. **Gatilho:** antes de qualquer rota
com `aliquota_ganho` sair do bloqueio por insumo — hoje o FII está bloqueado, e é só
por isso que o número não sai errado.

Achado pela guarda de campos mortos (11/09). A P-13 trocou `isento_ir` por dois campos
porque o FII não cabia num booleano: rendimento isento, **ganho tributado a 20%**
(Lei 8.668/1993 art. 18). O catálogo preenche os dois, e três testes conferem o
valor de `aliquota_ganho`. **Nenhuma linha de produção o lê.** `retorno_liquido_aa`
calcula `ir = 0.0 if r.isento_ir else aliquota_ir_rf(...)`, e `isento_ir` devolve
`isento_ir_rendimento` — para o FII, IR zero sobre tudo. É exatamente o *"True
subestimava o imposto"* que o comentário da P-13 descreve como o erro que ela corrigiu.

Inventariado em `test_campos_mortos.py`; o teste do inventário quebra no dia em que ele
passar a ser lido, e a linha tem de sair.

---

## ~~P-78~~ · Dado de pesquisa coletado e nunca consumido — oito campos de `Instituicao` e um utilitário — **FECHADA em 26/09/2026**

**Classe:** `DECISAO_DE_DESENHO`. **Dono:** Osvaldo decide por campo; Claude executa.
**Gatilho:** a próxima vez que `corretoras.py` for tocado.

A guarda achou 10 além dos quatro da auditoria; um é a P-77. Os outros nove:

- `bc_procedentes`, `bc_clientes` — o numerador e o denominador do `bc_indice`, que é o
  que pontua. Guardar a origem de um número é procedência; a pergunta é se o lugar
  dela é o dataclass ou o `instituicoes.yaml`.
- `corretagem_fii`, `corretagem_etf_pct`, `exercicio_opcao_pct`, `mesa_minimo` — custo
  por operação coletado e fora de `pontuar()`, que só usa `corretagem_rv`. O
  `corretagem_etf_pct` é o 0,50% da XP em ETF: para quem compra ETF, é o custo que
  mais importa, e o ranking não o vê.
- `home_broker_web`, `exporta_csv` — a dimensão `facilidade`, que o `regras()` já
  recusa pontuar em voz alta. Decisão tomada; o campo pode ficar como dado exibido.
- `ambiente.PACOTE_PARA_IMPORT` — usado só pelo teste do P-15. **É ponto cego
  declarado da guarda**, não defeito do código: uso só em teste conta como morto de
  propósito (P-71), e para um utilitário isso pode ser rigor demais.

Nada foi removido: o LIMITE do prompt era parar acima de cinco e mostrar a lista.

**FECHADA em 26/09/2026.** Revisão das pendências com dono Osvaldo, 26/09, na nuvem: conferida no repositório, vencida. **Fechada em 13/09 no `ACHADOS.md` e nunca aqui** (`docs/auditoria/P76-P78-B04.md`). Os campos eram três naturezas: procedência (`bc_procedentes`, `bc_clientes`, reclassificados), ausência de critério declarada (`home_broker_web`, `exporta_csv`, que `regras()` recusa pontuar) e custo por operação fora do `pontuar()`. A terceira seguiu: o defeito fechou na P-83 e a decisão de peso é a **P-84**, que continua aberta.

---

## ~~P-79~~ · Três cópias do desembrulho — **FECHADA 16/09/2026** junto com o A-06

**Classe:** `DECISAO_DE_DESENHO`. **Dono:** Claude. **Gatilho:** a próxima vez que o
caminho `--eventos` do `coletar_b3.py` precisar mudar por outro motivo.

A esteira de proventos (11/09) precisou desembrulhar o acervo — string JSON contendo
lista (A-00, A-02) — e ganhou `desembrulhar()`. A mesma regra já vivia **inline** em
`coletar_eventos` e numa **cópia** em `test_coletar_b3.py` (`_normalizar`, com um teste
que confere o fonte). Três implementações da mesma conta é a N-01 na forma canônica.

Não unifiquei porque o LIMITE do prompt 5 proibia tocar o caminho `--eventos`: ele
funciona, e o acervo que ele produz não se recupera. Quando ele for tocado por outro
motivo, `coletar_eventos` passa a chamar `desembrulhar()` e o teste espelho morre.

---

---

## ~~P-87~~ · Existe uma SEGUNDA cópia do projeto na máquina, com `.git` próprio — **FECHADA em 26/09/2026**

**Dono:** Osvaldo · **Gatilho:** nenhum — antes do próximo pacote ou sessão de nuvem ·
**Classe:** `BLOQUEIA_O_SISTEMA`

O repositório vivo é `C:\Users\osvaldo.junior\Desktop\Bastter`. Existe **outro**, em
`C:\Users\osvaldo.junior\OneDrive - VOLGA …\Área de Trabalho\Bastter`, com `.git`
próprio cujo último `index` é de **09/09/2026**, `corretoras.py` de 18 KB contra os 28 KB
do vivo, e ainda com os cinco `*-patch.py` e a pasta `pacote_segunda/` que o P-82 removeu.

**Foi essa a pasta que a sessão da nuvem recebeu como pasta conectada em 18/09**, e eu
estive a um `device_commit_files` de escrever o trabalho de três dias dentro dela. O que
impediu foi conferir tamanho e `mtime` antes de gravar — não uma guarda.

> **É a armadilha do `docs/historico/pesquisa-custos-2026-08/calc/` e do `pacote_segunda/` num terceiro
> andar, e é o pior dos três:** os dois primeiros moram *dentro* do repositório e o
> `test_p82_copia_do_projeto.py` os mede pelo índice do git. Este mora **fora**, tem git
> próprio, e nenhum teste do projeto pode alcançá-lo — um teste mede o repositório em que
> roda, e o problema é justamente haver dois.

**Contexto, corrigido por ele em 18/09:** tirar o projeto do OneDrive **foi decisão
tomada e executada** — a pasta do servidor é o original abandonado, não um espelho vivo.
Isso explica a pasta e **não a torna inofensiva**: ela continua sendo um repositório
completo, com `.git` próprio, no caminho que a nuvem recebeu como pasta conectada.

**O que fazer (decisão dele, não minha):** ou a cópia do OneDrive é apagada, ou é renomeada
para algo que não se confunda (`Bastter-ARQUIVO-09set`), ou o `Desktop\Bastter` passa a ser
o único caminho aceito. Enquanto houver duas, toda sessão de nuvem precisa conferir qual
recebeu — e **P7: conferência que depende de alguém lembrar não é conferência.**

**FECHADA em 26/09/2026.** Revisão das pendências com dono Osvaldo, 26/09, na nuvem: conferida no repositório, vencida. A cópia do OneDrive foi **apagada por ele em 18/09** (`PLANO.md` §4, item 5, e §5, decisão A).

---

## ~~P-92~~ · O acervo tem UM ano de preço, e ele é a régua de todo o resto — **FECHADA em 26/09/2026**

**Dono:** Osvaldo (download) · **Gatilho:** antes de qualquer execução do pré-registro ·
**Classe:** `BLOQUEIA_O_SISTEMA` · ⚙ **exige o desktop**

`fase0/ajustar.py` existe e foi medido contra o mercado (`docs/auditoria/C02-O-DEGRAU-MEDIDO.md`):
a série ajustada de **2023** está de pé, com 293 datas-ex medidas e controle em 86.736
pares. O módulo não tem mais nada a fazer — **o que falta é preço.**

Um ano não é backtest. E há um segundo ganho, que é o mais barato do projeto hoje:

| ano | eventos de QUANTIDADE que ele corrobora |
|---|---|
| 2025 | 31 |
| 2021 | 19 |
| 2023 (no acervo) | **1** |

A leitura percentual do campo `factor` — a decisão do C-01 — tem hoje **uma** corroboração
de preço. Com 2021 e 2025 ela passa a ter **51**, e são os casos **grandes**, que o preço
resolve com folga. Baixar dois arquivos fecha uma questão metodológica *e* amplia a
cobertura da data ex, sem uma linha de código nova: o `calendario.py` e o `ajustar.py` leem
o que estiver na pasta.

**A regra que vale a pena carregar:** ordem por evento de quantidade, não por
proximidade — 2025 antes de 2024.

**FECHADA em 26/09/2026.** Revisão das pendências com dono Osvaldo, 26/09, na nuvem: conferida no repositório, vencida. O acervo tem os **41 anos**, 1986–2026, desde 18/09 (`CLAUDE.md`, terceira rodada de 18/09), o leitor enxerga todos desde 19/09 (P-99), e desde 24/09 eles estão no armazém: `docs/acervo/b3/inventario-armazem.csv` lista 41 `COTAHIST_A*.ZIP`, e o anual do ano corrente é recapturado todo mês pelo workflow (P-135). 2021–2025 deram ao C-01 **54** eventos de quantidade com preço em 21/09 (`PLANO.md`, passo 3).

---

## P-96 · ~~Ano fechado do COTAHIST muda?~~ **FECHADA em 18/09 — não muda, medido**

**Dono:** Osvaldo (download) · **Gatilho:** junto com o download dos quatro anos ·
**Classe:** `DECISAO_DE_DESENHO` · ⚙ **exige o desktop**

A limitação `captura_do_cotahist_passa_por_captcha` (política 1.21.0) diz que o custo do
portão manual é **um número fixo de cliques, uma vez** — e diz isso apoiada numa
suposição minha: *ano fechado não muda*. **A B3 não afirma isso em lugar nenhum**; as
duas páginas públicas não publicam política de atualização (lido em 18/09/2026).

> **18/09 — a medição aconteceu sozinha.** O download dos 41 anos rebaixou o
> `COTAHIST_A2023.ZIP` e ele veio com **70.216.090 bytes — exatamente o tamanho do que
> está no acervo desde 04/09.** Falta uma linha para fechar:
>
> ```powershell
> Get-FileHash "docs\fontes\series-historicas-cotahist\COTAHIST_A2023.ZIP" -Algorithm SHA256
> #   ad1603788d78aaa1de806498572277f1d9443f88ae116452751b5800cb23523e  -> congelado
> ```
>
> Tamanho igual é evidência forte e não é prova: dois arquivos do mesmo tamanho podem
> diferir. O hash decide.
>
> **FECHADA — o hash foi medido no arquivo rebaixado:**
>
> ```
> ad1603788d78aaa1de806498572277f1d9443f88ae116452751b5800cb23523e   rebaixado 18/09
> ad1603788d78aaa1de806498572277f1d9443f88ae116452751b5800cb23523e   acervo     04/09
> ```
>
> **Idênticos.** Ano fechado do COTAHIST é congelado — deixou de ser suposição minha e
> virou medição, com 14 dias de intervalo.

- **Igual** → congelado, medido em vez de suposto. A P7 encolhe para o ano corrente.
- **Diferente** → existe rotina periódica, ela é manual, e a limitação muda de peso.

E vale o aprendizado da CVM antes de concluir: **hash diferente não é reapresentação.**
`manifesto_cvm.py --comparar` separa `REORDENADO` de `REAPRESENTADO`; na CVM, comparar
por hash deu **100% de falso positivo** em 18/09.

---

## ~~P-97~~ · A procedência do `COTAHIST_A2023.ZIP` — **FECHADA em 23/09/2026**

**Decisão dele:** é duplicata e não importa de onde veio — **sai do acervo.** Das duas
saídas que a pendência oferecia (lembrar a origem, ou registrar origem desconhecida),
ele escolheu a terceira, que estava escrita no `docs/historico/entregas/SEGUNDA-21.md` e é melhor que as duas:
**arquivo sem procedência não ganha uma linha dizendo que não tem procedência — ele sai
de onde a procedência é obrigatória.**

**Nada único saiu do acervo, e isso foi medido antes de mover** (não depois):

| arquivo | sha256 | o gêmeo em `cotahist/` |
|---|---|---|
| `COTAHIST_A2023.ZIP` | `ad1603788d78aaa1…` | **idêntico** |
| `COTAHIST_A2023/COTAHIST_A2023.TXT` | `344a50f86548a4aa…` | **idêntico** |

O gêmeo tem origem declarada desde 18/09 (GET direto, `origem.csv`). O que saiu foi a
cópia sem procedência — e **movida, não apagada**: `data/quarentena/`, com um `LEIA.md`
que registra a decisão e as duas medições. Apagar é a operação sem volta, e a P-97
nunca pediu isso.

**A saída do manifesto, que era o critério:**

```
P-06: os 41 arquivos tem origem declarada.
```

**Guarda:** `fase0/test_p114_raiz_do_cotahist.py::test_P97_nao_sobrou_ZIP_sem_origem_no_acervo`
— o manifesto é um comando que alguém roda, e a P7 é explícita sobre isso. O teste prende
na suíte o que a linha acima afirma uma vez.

> **Ela não fechava sozinha, e é esse o achado.** Enquanto o avulso estava em
> `data/bronze/b3/`, a raiz padrão do `refinar.py` e do `ajustar.py` enxergava **ele** e
> devolvia 248 pregões — um acervo de um ano com cara de acervo inteiro (P-114). Tirar só
> o avulso deixaria a raiz antiga com zero COTAHIST; mudar só a raiz deixaria a duplicata
> sem procedência dentro do acervo. **As duas metades se escondiam uma à outra**, e por
> isso as duas decisões são do mesmo dia.

---

## P-99 · ~~O COTAHIST muda de convenção de nome~~ **CONSERTADA em 19/09, falta aplicar**

**Dono:** Osvaldo (copiar os arquivos) · **Gatilho:** segunda 21/09, passo 1 de
`docs/historico/entregas/SEGUNDA-21.md` · **Classe:** `BLOQUEIA_O_SISTEMA` · ⚙ **exige o desktop**

> **Consertada em 19/09, e eram TRÊS defeitos, não um.** Medido nos 9 ZIPs que estavam no
> container: **7 de 9 devolviam ZERO registros em silêncio**; `arquivos()` faria quinze anos
> disputarem a chave `COTAHIST`; e `pregoes()` **morria inteiro** num `BadZipFile` — o 2026
> truncado apagava o calendário do acervo todo.
>
> `fase0/calendario.py` + `fase0/test_calendario_p99.py` (24 testes). **Instantâneo dourado:
> 2023 em 248 pregões, sha256 `e4a9d81d…d551c`, idêntico ao de 18/09.**
>
> **Risco declarado:** eu não pude ver `test_calendario.py` nem `test_ajustar.py` — nunca
> passaram pelo container. Se algum falhar, é o contrato do `registros()`, que agora confere
> cabeçalho. Já reduzi: arquivo que começa direto em registro de cotação é aceito, e a
> primeira linha não se perde. Mas testei contra a minha suposição, não contra eles.

| faixa | nome dentro do ZIP |
|---|---|
| 1986–2000 | `COTAHIST.A1986` … `COTAHIST.A2000` — **ponto**, sem extensão |
| 2001 | `COTAHIST_A2001` — **sublinhado**, sem extensão |
| 2002–2025 | `COTAHIST_A2002.TXT` — sublinhado **e** `.TXT` |

> **18/09 — medido, e a notícia é boa: o problema é SÓ o nome.** Abri os três ZIPs e
> comparei o conteúdo. O layout é **idêntico** nos 41 anos — 245 posições, CRLF,
> `TIPREG=01`, `DATA` em 3–10, `CODNEG` em 13–24, `MOEDA` em 53–56:
>
> ```
> COTAHIST_A1986.ZIP -> 'COTAHIST.A1986'      245 pos.  '00COTAHIST.1986BOVESPA 19991210'
> COTAHIST_A2001.ZIP -> 'COTAHIST_A2001'      245 pos.  '00COTAHIST.2001BOVESPA 20060331'
> COTAHIST_A2023.ZIP -> 'COTAHIST_A2023.TXT'  245 pos.  '00COTAHIST.2023BOVESPA 20231228'
> ```
>
> **A correção certa não é uma lista de nomes** — seria o mesmo erro da P-98 e da P-82
> pela terceira vez. É ler o **membro único do ZIP** (`namelist()[0]`) e validar pelo
> conteúdo: cabeçalho `00COTAHIST.<ANO>` e registros de 245 posições. Nome é a
> propriedade que varia; o layout é a que identifica.

`fase0/calendario.py` varre ZIP **ou** TXT; `ajustar.py` lê o que estiver na pasta.
**Nenhum dos dois encontra os 16 primeiros**, e o modo de falha é o mais caro do
projeto: eles não quebram — **não veem o ano.** A série passaria a começar em 2002 sem
ninguém ter decidido isso, e nenhum teste de "veio número?" notaria.

A correção é a do A-05: enumeração vinda do **dado observado**, com falha ruidosa fora
dela. E um teste que liste os anos efetivamente lidos e compare com os anos presentes
na pasta — **contagem que decai**, não suposição.

---

## ~~P-100~~ · O `COTAHIST_A2026.ZIP` não era um ZIP completo — **FECHADA em 23/09/2026**

**Dono:** Osvaldo (rebaixar) · **Gatilho:** quando o ano corrente for necessário ·
**Classe:** `DECISAO_DE_DESENHO` · ⚙ **exige o desktop**

> **23/09 — FECHADA, medido na sessão local sobre o arquivo rebaixado.** Ele rebaixou em
> **21/09 às 11:59** e o arquivo veio íntegro. Duas medições independentes, a dele e a desta
> sessão, **concordam em todos os campos**:
>
> | | medido |
> |---|---|
> | bytes | **85.779.964** |
> | sha256 | `fb3546ed27cc8a138e93c141adce3e8dc684df219ebffa4d49bff5d557b3e5e3` |
> | ZIP | membro `COTAHIST_A2026.TXT`, 709.321.015 bytes, flag `0x808` (ainda streaming), `testzip` limpo |
> | header | `00COTAHIST.2026BOVESPA 20260918` |
> | trailer | `99COTAHIST.2026BOVESPA 20260918` + `TOTREG` **2.871.743** |
> | registros tipo `01` | **2.871.743** — bate com o `TOTREG`; o trailer **não** conta header e trailer (2.871.745 linhas) |
> | pregões | **179**, de **02/01 a 18/09/2026** |
>
> `origem.csv` com `acesso` 2026-09-21 e o rebaixamento escrito; manifesto regravado
> (`dt_captura=2026-09-23.csv`, o anterior preservado como `.bb47854ef9d2.csv` — só a linha
> de 2026 difere).
>
> **Retratação:** a P-100 **nunca devia ter bloqueado nada.** Um download cortado se conserta
> baixando de novo; eu o tratei como limitação e cortei o período da família ML em dez/2025.
> O arquivo bom estava no disco 44 h antes do commit que declarou o contrário. Citação,
> evidência e causa raiz no `CLAUDE.md` (bloco da P-100 na rodada de 18/09) — e a régua que
> sai daí é a **§5-B.16**.

> **21/09 — agora bloqueia a família ML.** O teste do `preregistro-ml-v1.md` vai de
> jan/2020 até o fim do COTAHIST; sem 2026 íntegro, ou o período termina em dez/2025 escrito
> no §2, ou a família espera este arquivo. Ver P-107.

38.328.935 bytes baixados; a extração falha com *"O registro Final de Diretório Central
não foi localizado"* — o fim do arquivo não chegou.

> **18/09 — medido o que o arquivo é.** Não é página de erro nem HTML: o cabeçalho é
> `PK\x03\x04`, com o membro `COTAHIST_A2026.TXT` declarado e **flag 0x0808** — bit 3
> ligado, isto é, **ZIP em streaming**, com os tamanhos num descritor no fim. É a forma
> de quem **gera o arquivo na hora**, coerente com o ano corrente ainda estar aberto. O
> download foi **cortado**, não recusado.
>
> Consequência para a rotina automática: um ZIP em streaming **não dá para validar pelo
> tamanho esperado**, porque não há tamanho esperado. O coletor tem de **abrir o ZIP e
> ler o membro até o fim** antes de aceitar o arquivo — conferir depois de gravar é
> conferir tarde.

**É a armadilha do `CLAUDE.md` §11.6, e desta vez ela gritou por sorte do formato:**
*"um download que devolve 404 mais um unzip vazio produzem 'nenhuma mudança',
indistinguível de 'a B3 não mudou nada'"*. Um ZIP truncado quebra alto; um TXT truncado
teria entrado calado. **Ausência de mudança precisa ser afirmada, nunca inferida da
ausência de erro** — e isso vale agora para o coletor que a rotina automática vai usar:
ele tem de conferir o ZIP antes de aceitar o arquivo, não depois.

---

## P-105 · ~~O leiaute do COTAHIST estava em Python~~ **FECHADA em 19/09 — defeito meu**

**Dono:** — · **Gatilho:** — · **Classe:** `BLOQUEIA_O_SISTEMA` · *(P2 violada)*

O `fase0/calendario.py` nasceu em 19/09 com `POS_DATA = (2, 10)`, `POS_MODREF = (52, 56)`,
`LARGURA = 245` e `MODREF_OBSERVADOS = (...)` **escritos em Python**, com a procedência num
comentário. São valores de **fonte externa** — o leiaute publicado pela B3 — e a P2 é
explícita: *"todo parâmetro vive em YAML versionado, nunca em código."*

**E eu os escrevi no mesmo dia em que auditei três planos de otimização por falta de
rigor.** A procedência ficou num comentário, que é o lugar onde ela não pode ser conferida
por teste nenhum.

**Fechada:** `docs/schemas/cotahist-v02.yaml` — revisão, URL, data de acesso e o status de
cada enumeração ao lado dos valores. O `calendario.py` lê de lá e **recusa rodar sem o
arquivo** (`LeiauteAusente`), sem fallback: um fallback silencioso reintroduziria o defeito
e **funcionaria**, que é o pior resultado possível.

E a conversão 1-baseada → Python mora num lugar só, porque ela é a fonte clássica de erro
de um: o documento diz 53–56, Python quer `[52:56]`.

> **A ideia não é minha.** Veio do **terceiro plano de otimização de tokens** que você mandou
> auditar — *"schema estruturado, Knowledge Registry"* —, e era o melhor item dos três. O
> ganho dele não é token: **é a P2.** Registro a origem porque conclusão sem procedência é o
> que este projeto persegue.

---

## P-106 · ~~`modref_de()` era lida só por teste~~ **FECHADA em 19/09 — P-77 recriada por mim**

**Dono:** — · **Gatilho:** — · **Classe:** `BLOQUEIA_O_SISTEMA`

`calendario.modref_de()` e `conferir_modref()` nasceram em 19/09 e **nenhum módulo do motor
as chamava** — só o teste. É a **P-77 na letra**: *campo que só o teste toca é campo que o
motor não usa*, e é categoria pior que órfã pura, porque tem testemunha — o teste prova o
esquema e ninguém prova o comportamento. Foi assim que a P-13 anunciou correção com a suíte
verde.

**Menos de 24 horas entre a P-77 estar escrita no `CLAUDE.md` e eu recriá-la.**

**Fechada:** `fase0/moeda.py` é o consumidor que faltava, e ele não é enfeite — é o
instrumento do C-03.

---

## ~~P-107~~ · O pré-registro de ML herdou `L = 3` de uma amostra quatro vezes maior — e não tem teste de poder — **FECHADA em 26/09/2026**

**Dono:** Osvaldo (decidir) · **Gatilho:** **antes do primeiro commit de
`preregistro-ml-v1.md`** — ele vale *"a partir do commit que o contém"*; depois disso, cada
correção é uma v2 · **Classe:** `DECISAO_DE_DESENHO`

Auditoria completa em `docs/auditoria/AUDITORIA-PREREGISTRO-ML-V1.md`. Medido com o instrumento
da P-88 sobre o NEFIN recortado a n = 80 (o tamanho do teste do ML, jan/2020 em diante):

| L | blocos | HML | SMB (controle) |
|---|---|---|---|
| 1 | 80 | 3,1045 | 4,1399 |
| **3** | **27** | 3,4598 (+11,4%) | 3,6704 (**−11,3%**) |

A faixa L = 2 a 8 da P-88 foi definida por **≥ 39 blocos** com n = 306. Com n = 80, `L = 3`
dá 27 — está **fora** da faixa pelo próprio critério que a definiu, e o controle mostra o
artefato: o corte **cai** 11% onde não há dependência. Anticonservador, na direção de
aceitar um modelo que não funciona.

**Recomendação (decisão sua):** corte operativo = **máximo entre L ∈ {1, 2, 3}**, com o motivo
escrito no §6; e um **nono teste** no §8 — poder com sinal plantado, reportado ao lado do
veredito (com c ≈ 3,1–4,1, o IC médio precisa ser ≥ 0,35–0,46 × sd para ser detectável).
Mais quatro menores na tabela §5 da auditoria. **P-100 passa a bloquear a família ML.**

**Também retratado aqui:** a minha recusa do ML em 19/09 (`AUDITORIA-PLANO-DE-TOKENS.md`
§4.5) citou DeMiguel fora do alcance dele.

**FECHADA em 26/09/2026.** Revisão das pendências com dono Osvaldo, 26/09, na nuvem: conferida no repositório, vencida. Decidida por ele antes do commit e aplicada: `docs/aprendizado/preregistro-ml-v1.md` e `-v2.md`, seção *Feitas por decisão dele (P-107)* — corte = **máximo entre L ∈ {1, 2, 3}** e o **nono teste**, poder com sinal plantado. A condição *"P-100 bloqueia a família"* também caiu: a P-100 fechou em 23/09.

---

## P-108 · ~~O `origem.csv` com BOM zerava a procedência em silêncio~~ **FECHADA em 21/09 — e o roteiro que causou era meu**

**Dono:** — · **Classe:** `BLOQUEIA_O_SISTEMA`

O `docs/historico/entregas/SEGUNDA-21.md` mandava criar o `origem.csv` com `Out-File -Encoding utf8`. No Windows
PowerShell 5.1 isso grava `EF BB BF` na frente — **medido no arquivo dele: 26 bytes, os três
primeiros o BOM**. O leitor abria com `utf-8`, a primeira coluna virava `'\ufeffcaminho'`,
e o filtro `r.get("caminho")` descartava **todas** as linhas sem erro nem aviso. Ele
declararia as 41 origens e o contador continuaria em 42. É o F-02 na camada do registro.

**Fechada:** `origem_declarada()` lê com `utf-8-sig`, e cabeçalho sem a coluna `caminho`
**levanta** em vez de zerar (*origem ilegível não é origem ausente*).
`fase0/test_origem_bom.py`, 5 testes, um deles reproduzindo o leitor antigo para provar que
o defeito existia. O `origem.csv` foi escrito com as 41 linhas, sem BOM, a partir do
manifesto dele de 21/09 e da `$baseUrl` do script de download que ele colou em 18/09.

---

## P-109 · ~~O `calendario.py` de 19/09 reprovava 19 testes que eu não rodei~~ **FECHADA em 21/09**

**Dono:** — · **Classe:** `BLOQUEIA_O_SISTEMA`

O `calendario.py` de 19/09 confere o header do COTAHIST (`00COTAHIST.AAAABOVESPA …`) — é o
que pegou a P-99. Os sintéticos do `test_ajustar.py` (sem header) e do `test_calendario.py`
(header `00` + oito zeros) não existem no acervo real, e **14 + 5 testes** reprovaram. Eu
tinha declarado em 19/09 que não rodara esses testes; não tinha tentado — o repositório é
público (§5-B.15).

**E o roteiro mentia sobre o código.** O `docs/historico/entregas/SEGUNDA-21.md` de 19/09 dizia que *"arquivo que
começa direto num registro de cotação é aceito, e a primeira linha não se perde"*. O
`registros()` entregue não faz isso: ele exige o header e levanta. É o defeito recorrente da
casa — *um arquivo declara um comportamento que o código não tem* —, escrito por mim no
roteiro do dia em que você ia confiar nele.

**Fechada** corrigindo o **sintético**, não o leitor: os dois `_cotahist()` agora escrevem o
header real. O `calendario` continua recusando arquivo sem header, com aviso em stderr —
recusar é o que protege a P-99. Medido sobre clone do `origin/main` + entrega.

---

## P-110 · ~~Treze `.md` da raiz sem papel, e o teto de órfãos medido na árvore errada~~ **FECHADA em 21/09**

**Dono:** — · **Classe:** `DECISAO_DE_DESENHO`

`test_todo_md_da_raiz_tem_PAPEL_declarado` reprovou no repositório real: `LEIA-AGORA.md`,
`LEIA-NA-SEGUNDA.md`, `LEIA-NA-TERCA.md`, dois de prompts, `RECRIAR-REPOSITORIO.md` e sete
laudos de agosto. **Fechada:** os treze classificados `SOB_DEMANDA`, cada um com o motivo,
lido o título de cada um. **Nenhum entra na leitura de sessão.**

O teto de 46 órfãos do `achados_ancorados.py` foi medido em 19/09 numa árvore **sem** o
`ACHADOS.md`. No repositório real, com o `ACHADOS.md` já colado, também dá **46 — mas com
outros 24 códigos** (os da árvore de entrega ganharam definição; entraram os `E-10`…`E-19`
do laudo consolidado, os `T-02`…`T-05` dos escopos, `D-2`…`D-7`). O teto continua valendo,
agora **por medição no lugar certo**, e a coincidência fica escrita aqui para ninguém ler
como calibração.

**Sobra (aberta, sem prazo):** os três `LEIA-*` são roteiros vencidos. Movê-los para
`docs/historico/` limpa a raiz; é decisão sua, porque são arquivos seus.

---

## P-111 · ~~`pytest.mark.slow` sem registro~~ **FECHADA em 21/09**

**Dono:** — · **Classe:** `DECISAO_DE_DESENHO`

Os testes da P-88 usam `@pytest.mark.slow` e eu não registrei a marca: três
`PytestUnknownMarkWarning` em toda execução de `auditoria`, visíveis no transcript do commit
`c6ccf2a`. Aviso que aparece sempre é aviso que se aprende a não ler — e o dia em que vier
um aviso de verdade ele entra no meio dos três de sempre. **Fechada:** `markers` no
`[tool.pytest.ini_options]` do `pyproject.toml`. **A impressão do ambiente não mudou**
(`7565df1381e2c1ed` antes e depois, medida): ela é calculada só sobre Python e versões.

**O `1 skipped` da `auditoria` na máquina dele não é defeito**, e fica escrito para não
virar dúvida: é `test_mutacao_a_razao_grosseira_e_a_do_tiktoken_concordam_em_ORDEM_DE_GRANDEZA`,
que pula quando o `tiktoken` não está instalado e diz isso na razão do skip
(`pytest auditoria -rs` mostra). O `tiktoken` é proxy opcional (§11.4), fora das dependências.

---

## ~~P-113~~ · O preço de véspera do COTAHIST — **FECHADA em 23/09/2026**

**Decisão dele:** o fechamento do COTAHIST substitui `closingPricePriorExDate` quando a B3
não o traz, com uma **coluna nova de origem** (`B3` / `COTAHIST` / `B3+COTAHIST`) e **a B3
ganhando quando existe**. Sem segundo leitor de COTAHIST (N-01).

**Feita pela P-116, e é a primeira do projeto:** os critérios foram escritos, commitados e
**empurrados** antes da corrida — `docs/auditoria/P113-CRITERIOS.md`, commit **`9a08a55`**. O hash
é a impressão digital; sem ele, *"pré-registrado"* não é verificável pela P4.

**E o pré-registro pagou na primeira vez que foi usado: quatro dos sete critérios
reprovaram.**

| | previsto | medido |
|---|---|---|
| eventos que ganham fator | 172 | **11** |
| séries `INCOMPLETO` | 18 | **74** |
| degraus contaminados | 8 | **138** |

**Os 161 que faltam são o achado A-13:** não eram fatores faltando, eram **o mesmo pagamento
chegando pela segunda porta**. As duas esteiras da B3 se sobrepõem na janela recente, e
`_chave_de_evento` não as colapsa porque `origem` entra nela de propósito (A-09). A cópia do
suplemento era inofensiva **por acidente** — vinha sem preço, logo sem fator. Dar preço a ela
subtrairia o provento **duas vezes**.

Provado pelo resíduo de 2025, onde a sobreposição mora: **t +0,39 colapsando, +6,31 sem
colapsar**. E a armadilha: **o agregado dos cinco anos melhorava enquanto o ano quebrava** —
o critério R3 que eu havia pré-registrado teria aprovado a versão errada. Quem pegou foi a
coluna de procedência que a decisão dele mandou criar.

**Resultado final:** 11 fatores novos, 162 proventos repetidos não aplicados, `AJUSTADO`
23 → **27**, `INCOMPLETO` 78 → **74**, degraus 1.586 → **1.593**. **2023 não se moveu — nem
um degrau**, e o instantâneo dourado do C-02 continua de pé (a minha previsão R6 dizia que
mudaria; errei na direção conservadora).

Laudo em `docs/auditoria/P113-MEDIDO.md`. Guarda: `fase0/test_p113_preco_de_vespera.py`, 17 testes.

**O que NÃO foi mudado, e continua dele:** `diagnostico()` conta `SEM_FATOR` (subscrição, que
por desenho não ajusta preço) como insumo ausente. Conferido e é verdade; hoje vale 1 série.
Reclassificar status publicado é decisão dele.

## ~~P-114~~ · A raiz padrão apontava para uma pasta sem o acervo — **FECHADA em 23/09/2026**

**Decisão dele:** a raiz padrão do `refinar.py` e do `ajustar.py` passa a ser
`data/bronze/b3/cotahist` — a pasta que **tem** o dado.

**E a correção não foi trocar uma constante**, porque no `refinar.py` o parâmetro servia a
**dois acervos**: `eventos/` e `proventos/` de um lado, o COTAHIST de onde sai o calendário
do outro. Apontar os dois para `cotahist/` consertaria o calendário e apagaria o acervo de
eventos. Agora são dois parâmetros:

| | padrão | o que mora lá |
|---|---|---|
| `--raiz` | `data/bronze/b3` | `eventos/`, `proventos/` |
| `--cotahist` | `data/bronze/b3/cotahist` | os 41 anos, de onde sai o **calendário** |

> **Um parâmetro que serve a dois acervos não é economia: é a garantia de que mover um
> quebra o outro em silêncio.** Foi exatamente o que aconteceu — os 41 anos entraram em
> `cotahist/` em 18/09 e o calendário continuou em 2023, sem erro e sem aviso.

**O que o defeito produzia não era ausência, era um recorte com cara de todo.** A raiz antiga
devolvia 248 pregões de 2023 e o relatório imprimia `acervo COTAHIST_A2023`. Passa em
qualquer teste de *"veio número?"*. E o `refinar.py` fechava a armadilha imprimindo que
*"cada ano de COTAHIST que entrar em `data/bronze/b3/` amplia a cobertura sozinho"* —
**falso para o disco como ele estava**: quem copiasse um ano para ali, seguindo a instrução
da própria ferramenta, não veria diferença nenhuma. A frase agora nomeia a pasta que o
módulo **leu de fato**.

**Medido — o silver regerado com o calendário dos 41 anos:**

| | com calendário de 2023 | com os 41 anos |
|---|---|---|
| cobertura | 2023-01-02 a 2023-12-28, 248 pregões | **1986-01-02 a 2026-09-18, 10.059 pregões** |
| `data_ex` `DERIVADA` | 383 | **9.271** |
| `FORA_DA_COBERTURA` | 8.889 | **1** |

A única linha que sobra é uma subscrição da PETR com último dia com direito em
**14/11/1974** — doze anos antes do início do acervo. Recusa correta, não buraco.

**Instantâneo dourado, e ele fechou nos três níveis exigidos:**

- `pregoes()` de 2023: **248 pregões**, `sha256 e4a9d81d…d551c` — inalterado;
- **silver:** as 383 datas ex já derivadas saíram **idênticas**, 8.888 ganharam, **0
  perderam**, e **nenhuma outra coluna mudou em nenhuma das 9.272 linhas**;
- **os dois CSVs, subconjunto de 2023:** byte a byte idênticos —
  `degrau_datas_ex` `875dd1ca…`, `precos_ajustados` `a2e437b5…`.

E a mudança de raiz **isolada** é inerte: com o silver antigo, a janela 2021–2025 saiu com os
mesmos `c248053b…` e `a08e4657…` de 21/09. As duas metades foram medidas separadas de
propósito — juntas, uma explicaria a outra.

**O arquivo de 11/09 não foi sobrescrito.** O silver regerado é
`eventos_silver_2026-09-11_cal-1986-2026.csv`, e os CSVs da janela ganharam o mesmo sufixo.
O que mudou na janela 2021–2025 está no A-12, e **não é efeito do calendário**: é o calendário
tendo revelado um defeito de chave que existia desde 18/09.

**Guarda:** `fase0/test_p114_raiz_do_cotahist.py`, 8 testes, 4 dos quais reprovam contra a
versão de 21/09 (prova por mutação). Os dois que valem medem **comportamento**: o COTAHIST
numa pasta sem evento nenhum tem de produzir data ex, e um COTAHIST na raiz de **eventos**
**não** pode virar calendário.

## ~~P-120~~ · O manifesto só vê `*.zip`, e há 6,0 GB de cópias extraídas no acervo sem registro — **FECHADA em 24/09/2026**

**Dono:** Osvaldo (decidiu) · **Gatilho:** — ·
**Classe:** `DECISAO_DE_DESENHO` · ⚙ **exige o desktop**

Medido em 23/09 em `data/bronze/b3/cotahist/`: **41 ZIPs, 790.736.674 bytes**, e ao lado
deles **41 arquivos extraídos, 5.993.738.309 bytes** (5,6 GiB) — 40 soltos na pasta (`.TXT`
de 2002 em diante; sem extensão de 1986 a 2001) e um dentro de `COTAHIST_A2026/`. O
`manifesto()` filtra por `*.zip`, então **88% dos bytes do acervo não têm sha256 nem
`dt_captura`**. Nenhum leitor os usa hoje — `calendario.arquivos()` prefere o ZIP —, mas
ninguém prova que são o que o ZIP contém, e um `.TXT` avulso de um ano sem ZIP seria lido.

Duas saídas, e as duas são legítimas:

| | o que custa | o que ganha |
|---|---|---|
| **registrar** — manifesto passa a hashear todo arquivo com cara de COTAHIST | ~6 GB de leitura por rodada (hoje ~0,8 GB) | procedência do que está no disco, seja o que for |
| **apagar** — o ZIP é a fonte, a extração é derivada e se refaz | nada; libera 6 GB | a regra *"no acervo só entra o que a fonte entregou"* fica verdadeira |

A minha leitura, e a decisão é sua: **apagar**. A extração é derivada (a P-96 mediu que ano
fechado não muda), e manifestar derivado é pagar 7× para provar o que o ZIP já prova.

> **23/09, tarde — as cópias foram RENOMEADAS (P-126), e isso não decide esta pendência.**
> Agora são 41 `COTAHIST_A<ANO>.TXT`, cada uma conferida por CRC-32 contra o membro do ZIP, e
> a pasta `COTAHIST_A2026/` não existe mais. Continuam sem sha256 nem `dt_captura` no
> manifesto: **apagar ou manifestar segue sendo decisão sua.**
>
> ⚠ **RETRATAÇÃO — 24/09/2026, sem apagar a nota acima.** O que ela diz, citado: *"cada uma
> conferida por CRC-32 contra o membro do ZIP"*. **Falso para 24 das 41.** Em 23/09 só as
> **17 renomeadas** passaram por `conferir()`; as 24 que já tinham o nome certo saíram
> `JA_CORRETO` pelo `continue` de `plano()`, **antes** da conferência (P-131). As **41** só
> foram conferidas em **24/09**, uma a uma, antes de apagar (fechamento abaixo, item 1).
> **Causa raiz:** eu li o nome do status como o que ele mediu — o contador dizia *"RECUSADO
> 0"* e eu escrevi *"todas conferidas"*, sem abrir o ramo que produzia o `JA_CORRETO`. É a
> §5-B.1: a frase do que a medição mediu era mais estreita que a conclusão. **Corrigido na
> ferramenta:** P-131 — `JA_CORRETO` agora também passa por `conferir()`.

### Fechamento, 24/09/2026 — **decisão dele: apagar**

**1. A conferência que eu ia usar não conferia.** O pedido era *"apague só o que a execução
sem `--aplicar` conferiu"*. Ela deu `JA_CORRETO=41, RECUSADO=0` — e em `plano()` o
`JA_CORRETO` faz `continue` **antes** de `conferir()`: cabeçalho, tamanho e CRC-32 só rodam
para quem vai ser renomeado. As 41 linhas diziam que o **nome** estava certo, não que o
**conteúdo** era o do ZIP. Conferi as 41 chamando a mesma `conferir()` do módulo, uma a uma:
**41 conferidas, 0 recusadas, 5.993.738.309 bytes**. Apaguei exatamente essa lista. O defeito
do `plano()` ficou registrado como **P-131**.

**2. Instantâneo antes e depois, idêntico** (método: `sha256(str(x).encode())`):

| | antes | depois |
|---|---|---|
| `pregoes()` de 2023 | 248, `e4a9d81d…d551c` | **248, `e4a9d81d…d551c`** |
| `pregoes()` total | 10.059, `2700aca0…de35d` | **10.059, `2700aca0…de35d`** |
| `arquivos()` | 41, `sorted(items)` → `7469fb94…` | **41, `7469fb94…`** |

O `0af9b2f5…` de `arquivos()` registrado na P-126 **não se reproduz** com nenhuma de dez
formas óbvias (itens, chaves, valores, basename, absoluto, barra normal, dict, json…): o
método não foi escrito. É um hash sem conta — a §11.4 em miniatura. Fica o `7469fb94…` com o
método ao lado. A pasta ficou com **41 `.ZIP` e nada mais**.

**3. A decisão não depende de memória (P7).** `manifesto_cvm.extracoes_soltas()` conta —
**sem hash** — todo arquivo sob a raiz que começa com `COTAHIST` e não é `.zip`, e o `main()`
imprime a contagem **sempre**, inclusive o zero (§5-B.14), com `AVISO P-120` em stderr como
última linha quando ela passa de zero. O critério é o prefixo e não `calendario.ano_de()`: o
alarme tem de ser mais largo que o leitor. `fase0/test_p120_extracoes_soltas.py`, 7 testes,
um deles contra o acervo real a cada rodada. **Prova por mutação:** devolver `[]` reprova 3;
tirar o filtro `.zip` reprova 6; hashear a cópia reprova 1; tirar o `print` reprova 2.

**4. O manifesto de 24/09** (`--manifesto data/bronze/b3`): **41 arquivos, 791 MB**,
*"P-06: os 41 arquivos tem origem declarada"*, **"P-120: 0 copia(s)"**. `caminho`, `bytes`
e `sha256` idênticos, nas 41 linhas, aos do retrato de 23/09.

## ~~P-121~~ · `calendario.arquivos()` aceitava pasta com nome de ano — **FECHADA em 23/09/2026**

**Dono:** Claude Code · **Gatilho:** — · **Classe:** `BLOQUEIA_O_SISTEMA`

O filtro era só o nome (`ano_de`). `COTAHIST_A2026/` — a extração dele — está no acervo
desde 21/09 e só não entrava porque `sorted()` a põe antes do `.ZIP` e o ZIP de mesmo ano a
sobrescreve: **certo por acidente**. Um ano com só a pasta devolveria um diretório como
arquivo de COTAHIST. Consertado com `os.path.isfile`; `fase0/test_p121_pasta_nao_e_cotahist.py`,
4 testes, **2 reprovam contra a versão anterior** (pasta sozinha; pasta `.ZIP` desbancando
um `.TXT` verdadeiro).

## ~~P-125~~ · `calendario.conferir_cabecalho` devolvia `'.202'` como ano de 2026 — **FECHADA em 23/09/2026**

**Dono:** Claude Code · **Gatilho:** — · **Classe:** `BLOQUEIA_O_SISTEMA`

O header é `00COTAHIST.AAAABOVESPA AAAAMMDD`: o ponto está na posição 10 (0-based) e o ano em
11–14. A fatia era `[10:14]` — pegava o ponto e perdia o último dígito. A docstring prometia o
ano e **ninguém lia o retorno** (`registros()` só usa a função para levantar), então nada
quebrava: a P-77/P-106 outra vez, declaração sem consumidor. O primeiro consumidor é o
`nomear_extracoes.py` (P-126), e com o defeito ele recusaria **todas** as 41 cópias. Conserto
`[11:15]`; `fase0/test_p125_ano_do_cabecalho.py`, 6 testes, **reprovam contra a versão
anterior** e passam na nova.

## ~~P-126~~ · As cópias extraídas do COTAHIST tinham três convenções de nome e uma pasta — **FECHADA em 23/09/2026**

**Dono:** Claude Code · **Gatilho:** — · **Classe:** `BLOQUEIA_O_SISTEMA`

`fase0/nomear_extracoes.py` (+ `test_nomear_extracoes.py`, 12 testes) veio da entrega de 23/09
e foi movido de `data/entrega-23-09/`. Ele só renomeia depois de conferir cabeçalho, tamanho e
CRC-32 contra o membro do ZIP do mesmo ano. Plano sem `--aplicar`, no acervo real:
**RENOMEAR 17** (15 `COTAHIST.A1986…A2000`, o `COTAHIST_A2001` e o
`COTAHIST_A2026/COTAHIST_A2026.TXT` saindo da pasta), **JA_CORRETO 24, RECUSADO 0**. Aplicado;
a segunda execução dá 41 `JA_CORRETO`, e a pasta tem 41 `.ZIP` + 41 `.TXT`, nada mais.
**Instantâneo dourado antes e depois, idêntico:** 2023 em **248** pregões `e4a9d81d…`; o
calendário inteiro em 10.059 pregões `2700aca0…`; `arquivos()` com 41 entradas `0af9b2f5…`.

> ⚠ **RETRATAÇÃO — 24/09/2026, sem apagar o parágrafo acima.** O que ele diz, citado:
> *"Ele só renomeia depois de conferir cabeçalho, tamanho e CRC-32"* e *"JA_CORRETO 24,
> RECUSADO 0"*. A primeira frase é verdade **para o que ele renomeia**; o *"24"* foi lido
> como *"24 conferidas e certas"*, e **não eram conferidas**: `plano()` fazia `continue` no
> `JA_CORRETO` antes de `conferir()`. `RECUSADO 0` media só as 17 renomeadas. As 41 foram
> conferidas em **24/09**, antes de apagar (P-120). Causa raiz e conserto: **P-131**.

> **Renomear NÃO decide a P-120.** As 41 cópias continuam no acervo sem sha256 nem
> `dt_captura`; a escolha entre **apagá-las** ou **manifestá-las** continua sendo dele. O que
> mudou é só que agora elas têm um nome só, e a pasta com nome de ano (a armadilha da P-121)
> deixou de existir.

## ~~P-135~~ · O COTAHIST ainda não é capturado na nuvem — **FECHADA em 25/09/2026**

**Dono:** Claude · **Gatilho:** depois da primeira execução verde da captura da CVM (P-57) ·
**Classe:** `BLOQUEIA_O_SISTEMA`

O executor da P-57 cobre só a CVM. O `COTAHIST_A<ANO>.ZIP` do ano corrente muda todo dia
útil e hoje só é baixado quando ele roda o laço na máquina. **Não é validação por imagem** —
o pedido de 24/09 mandava declarar isso, e o HEAD do mesmo dia respondeu `200`, com
`Content-Length`, `Last-Modified` e `ETag` (transcrito em `docs/decisoes/P-57.md` e em
`limitacoes_declaradas.captura_do_cotahist_ainda_nao_e_rotina.medido_2026_09_24`). É a
§5-B.13 de novo, e desta vez pega antes de entrar no arquivo.

**Pesquisa, e depois conserto:** (1) medir se a B3, atrás da Cloudflare, responde igual a um
IP de datacenter do GitHub — um `workflow_dispatch` com um HEAD resolve, e o erro, se houver,
se transcreve; (2) se responder, estender a captura (mesmo portão HEAD, mesma chave de
conteúdo `b3/cotahist/...`, mesma regra 2.5 — a P-100 mostrou que o ano corrente chega em
streaming); (3) se não responder, a limitação muda de texto para o erro medido, e o
`o_que_resolveria` passa a ser o que ele disser.

**24/09, 18:23Z — a sonda existe e mediu da máquina dele** (`fase0/sondar_cotahist.py`, HEAD
sem retentativa). **Da máquina, não do runner** — isso não fecha o passo (1):

| arquivo | status | Content-Length | Last-Modified |
|---|---|---|---|
| `COTAHIST_A2026.ZIP` | 200 | 84.469.516 | Wed, 23 Sep 2026 23:43:07 GMT |
| `COTAHIST_D23092026.ZIP` | 200 | 463.627 | Wed, 23 Sep 2026 23:41:41 GMT |
| `COTAHIST_D22092026.ZIP` | 200 | 465.043 | Wed, 23 Sep 2026 00:03:01 GMT |
| `COTAHIST_D21092026.ZIP` | 200 | 497.066 | Mon, 21 Sep 2026 23:34:01 GMT |
| `COTAHIST_D18092026.ZIP` | 200 | 652.381 | Fri, 18 Sep 2026 23:34:50 GMT |
| `COTAHIST_D17092026.ZIP` | 200 | 640.513 | Thu, 17 Sep 2026 23:33:28 GMT |

Achado lateral: **o arquivo diário existe e mede ~0,5 MB** — ~170× menor que o anual. A
sonda virou passo do `captura_cvm.yml` (`continue-on-error`: uma recusa é dado, não
defeito), e a resposta ao runner sai no resumo da próxima execução.

**24/09, 18:46Z — o runner respondeu, e respondeu igual.** Execução `36043565046`
(`workflow_dispatch`, `ubuntu-24.04`, verde): os seis HEAD deram `200`, com os **mesmos**
`Content-Length`, `Last-Modified` e `ETag` da tabela acima, `Server: cloudflare`. Passo (1)
fechado: a B3 não trata IP de datacenter do GitHub diferente da máquina dele.

E medido na máquina, antes de escrever o `404`: `D07092026` (feriado), `D20092026`
(domingo) e `D24092026` (ainda não publicado) respondem **o mesmo** `404`, `text/html`. O
404 não distingue os três — quem distingue é o anual (P-137).

**Passo (2) construído:** `fase0/capturar_cotahist.py` + 10 testes, no mesmo workflow
(passo `captura_b3`), pelo mesmo `Armazem`, portão HEAD, regra 2.5 e teto. Diário dos dias
úteis dos últimos 7 dias (o portão fecha os já capturados); anual `A<ano do mês que acabou>`
na primeira rodada de cada mês; 404 do diário → `ausente` no log, sem vermelho; 404 do anual
→ `erro`. O passo da sonda saiu do workflow (a captura registra o mesmo, e mais); o módulo
fica como instrumento manual. **Falta para fechar:** a primeira execução verde **com** o
passo `captura_b3` — até lá `captura_do_cotahist_ainda_nao_e_rotina` fica de pé.

**24/09, 19:01Z — verde, com o COTAHIST.** Execução `36045126980`: os 5 diários (17 a 23/09)
e o `COTAHIST_A2026.ZIP` (84.469.516 B, sha256 `4f2cf2aac107…`) subiram como `novo`; log em
`logs/capturas_b3/2026-09-24.csv`; o bot commitou o registro novo (`c2c0040`) — o `git
status` no lugar do `git diff` funcionou na primeira. **O que resta para fechar é o mesmo
passo 3 da P-57:** tirar `b3` de `captura_do_cotahist_ainda_nao_e_rotina` exige declarar o
regime automático onde o `test_P7_todo_acervo_tem_regime_de_captura_declarado` o leia —
e o desenho dessa declaração serve às duas fontes de uma vez.


**25/09/2026 — FECHADA.** A execução `36148547193` (evento `schedule`, sem ninguém disparar) rodou os passos `captura` e `captura_b3` verdes, conferido passo a passo pela API do GitHub. O regime virou dado: `politica.yaml → regimes_de_captura` (1.31.0), lido por `manifesto_cvm.defeitos_de_regime()`, e as duas limitações ficaram `RESOLVIDA`. **O que não foi conferido daqui:** o `logs/capturas/<dia>.csv` no bucket (a sessão na nuvem não tem as credenciais do R2). E o cron das 09:15 UTC saiu às 14:35 UTC: o horário do agendamento não é garantido pelo GitHub.

## ~~P-139~~ · O pré-registro v2 fixa o sha256 do ZIP, e o leitor não confere pin nenhum — **FECHADA em 24/09/2026**

**Dono:** Claude Code · **Gatilho:** antes de a primeira linha do código da família ML ler
COTAHIST · **Classe:** `BLOQUEIA_O_SISTEMA` · **Origem:** CH-01, 24/09/2026.

O `preregistro-ml-v2.md` §2 fixa `COTAHIST_A2026.ZIP` em `fb3546ed…`. Desde a captura de
24/09, `acervo.versoes("cotahist", "COTAHIST_A2026.ZIP")` marca **`4f2cf2aa…` como vigente**,
e o `calendario.arquivos()` lê o que houver em `data/bronze/b3/cotahist/` **sem conferir
hash nenhum** — nesta máquina é o `fb3546ed`; numa que abra a vigente pelo armazém, é o
`4f2cf2aa`. **Hoje o ML leria versões diferentes conforme a máquina.**

O que a medição garante: na janela do teste (02/01 a 31/08/2026) as duas versões têm **o
mesmo multiconjunto de registros** — impressão
`sha256(01 ordenados) = ab74104d4aec2da2…` nas duas. Então o número do ML só depende da
versão se o código depender da **ordem** das linhas (primeira ocorrência vence, `groupby`
sem ordenar, desempate por posição).

**O conserto, sem editar o pré-registro:** o leitor do ML abre por `acervo.abrir(...,
"fb3546ed")` — a versão fixada, não a vigente — e confere a impressão de conteúdo da janela;
uma impressão diferente levanta `InsumoBloqueado`. Se um dia o pré-registro for emendado, a
emenda deveria fixar a **impressão de conteúdo** (que sobrevive a uma regeração da B3) e não
o sha256 do ZIP (que não sobrevive) — mas isso é emenda, com a régua da P-138, e não se faz
por aqui.

### Fechamento, 24/09/2026

`fase0/insumo_ml.py` é o leitor da família ML. Para um ano fixado, `abrir_cotahist(ano)`:
- abre por `acervo.abrir(..., versao=<sha256 fixado>, conferir=True)`, e **nunca** cai para
  a vigente. Se a versão fixada não abre, levanta `InsumoBloqueado`;
- confere o tamanho e a **impressão de conteúdo** da janela: sha256 das linhas `01` até
  31/08/2026, ordenadas, com `registros` e `pregoes` ao lado. Se diferir, levanta
  `InsumoBloqueado`.

O pin é dado: `docs/aprendizado/preregistro-ml-v2.pins.yaml` **transcreve** o §2 do
pré-registro sem editá-lo, e um teste reprova se o sha256 ou os bytes deixarem de aparecer
no `.md` (N-01). A impressão é **medida** sobre o mesmo byte fixado, não é escolha nova.

**Medido sobre o arquivo real:** `py -3.11 fase0/insumo_ml.py` → `2026 FIXADO fb3546ed27cc`,
saída 0. A impressão reproduz a do CH-01 (`ab74104d…`, 2.632.789 registros, 166 pregões).

**Testes:** 11 em `fase0/test_insumo_ml.py`. Duas mutações foram reprovadas:
- o leitor abrindo a vigente → 5 testes falham;
- a impressão sem ordenar → 2 testes falham, um deles o do arquivo real.

**Ano sem pin (2010–2025):** o leitor devolve a vigente com `fixado=False` e o sha256 ao
lado, porque o pré-registro não fixou esses anos. Fixá-los é a **P-140**.

**Limite declarado (P5):** a impressão prova o mesmo **multiconjunto** de linhas. Um código
do ML que dependa da ordem das linhas pode dar número diferente com a mesma impressão, e
quem lê tem de ordenar.

## ~~P-140~~ · Fixar os bytes de 2010–2025 que a família ML vai ler — **FECHADA em 25/09/2026**

> **Fechada** (decisão técnica do Claude, 25/09, pela impressão de conteúdo). **Anos 2004 a
> 2025**, e não 2010: a maior janela de preço do §5.1 é a reversão, 36–60 meses (H-ML7).
> De jan/2010, 60 meses para trás é o fim de jan/2005, e o último negócio até essa data pode
> estar em dez/2004. Medido do texto do pré-registro por teste, que reprova se 2004 sair.
> **Hierarquia do pin:** impressão = principal; sha256 e bytes = observado, secundário.
> `abrir_cotahist` tenta o byte observado; sem ele, lê a vigente, e a impressão igual segue
> com `AvisoRecompressao`, diferente vira `InsumoBloqueado`. O teste da P-139 que proibia
> cair para a vigente foi **substituído** pelos dois casos, porque a regra mudou por decisão.
> **Nesta máquina:** medição dos 22 anos em **54,5 s**; conferência dos 23 pelo leitor em
> **53,7 s** (`test_REAL_todo_ano_fixado_confere_nesta_maquina`) e 61 s pelo comando; 23/23
> `FIXADO`, nenhum aviso. Os 22 sha256 medidos conferem com a vigente do inventário do acervo.

**Dono:** Osvaldo (decisão) · Claude Code (execução) · **Gatilho:** antes de a primeira
variável da ML-3 ser montada · **Classe:** `DECISAO_DE_DESENHO` · **Origem:** P-139.

O pré-registro v2 só fixou o 2026. Para os outros anos, `insumo_ml.abrir_cotahist` lê a
versão vigente e devolve o sha256 dela, com `fixado=False`: a procedência acompanha o
resultado, mas nada impede que a versão mude entre duas execuções. A P-96 mediu o 2023
congelado por 14 dias, e a CV-02 mostrou que *"congelado não é imutável"* na CVM.

**A pergunta:** fixar 2010–2025 no `pins.yaml`, com o sha256 do inventário e a impressão
medida, antes de o ML tocar o dado? O custo é uma leitura de ~15 × 700 MB. Não é emenda ao
pré-registro, porque registra quais bytes existem e não muda o desenho. Mas é acréscimo a
ele, e por isso a decisão é dele.

## ~~P-138~~ · Confirmar a régua de "variante" do pré-registro — contador como alarme — **FECHADA em 24/09/2026**

**Dono:** Osvaldo · **Gatilho:** antes da próxima emenda ou extensão de um pré-registro
(a P-132 é a candidata) · **Classe:** `DECISAO_DE_DESENHO` ·
**Origem:** item 6 do `DEPENDE-DE-VOCE.md` de 13/09 (hoje em
`docs/historico/entregas/`), conferido em 24/09 na limpeza da raiz.

A pergunta era: *"confirma o desenho?"* — especificação congelada, graus de liberdade
declarados, diário de execuções, e o **contador de variantes como alarme** (exige
justificativa escrita, **não** bloqueia), em `docs/auditoria/PRE-REGISTRO-MODELO-DE-DADOS.md`.
O desenho foi **implementado** em 18/09 (`alocacao/preregistro.py`) junto com as decisões
2, 3 e 4, que ele respondeu. **A resposta ao item 6 não está registrada em lugar nenhum** —
nem no `PENDENCIAS.md`, nem no `CLAUDE.md`, nem no laudo. Código construído sobre um desenho
que ninguém confirmou é a U-01 do avesso: aqui não é o dado dele no caminho crítico, é a
decisão dele fora do caminho.

A resposta é `confirmo` ou o que ele mudaria; a escolha que mais pesa é **alarme × bloqueio**
— a decisão 4 já fez divergência de veredito **bloquear**, e o contador ficou mais brando
que ela.

### Fechamento, 24/09/2026 — **decisão dele: bloqueio, e a única saída é uma emenda empurrada ao repositório**

O resto do desenho de 13/09 fica confirmado; o que mudou é o contador, de **alarme** para
**bloqueio**. `alocacao/preregistro.py`:
- `conferir_orcamento(P, estrategia)` conta ORIGINAL + VARIANTE da estratégia no diário
  contra o `variantes_permitidas` dela, mais as emendas **publicadas**. Acima disso levanta
  `OrcamentoEstourado`, e `operativo()` chama a conferência **antes** da decisão 4;
- `politica.yaml → pesquisa.orcamento` (`politica: BLOQUEIA`, `ramo_publicado: origin/main`)
  e `pesquisa.emendas` (vazia). Uma emenda tem estratégia, `variantes_adicionais` ≥ 1,
  `escrita_em` e justificativa de ≥ 120 caracteres;
- **"empurrada" é medida:** a emenda só destrava se existir, com o mesmo conteúdo, no
  `politica.yaml` de `origin/main` (`git show`). A conferência é por conteúdo, e não por um
  sha escrito na emenda, porque o commit que a publica ainda não existe quando ela é
  escrita. Emenda commitada e não empurrada **não** destrava; sem git ou sem o ramo, o
  portão **fecha** (P-102);
- **emendar encarece:** as variantes da emenda entram no `m_orcado` assim que escritas,
  publicadas ou não. Se não entrassem, estourar o orçamento sairia de graça.

**Testes:** 20 novos em `test_preregistro.py`. Os dois que bloqueiam **reprovam por
mutação** (a chamada de `operativo` trocada por `pass`); três rodam contra um git de verdade
com remoto nu (não empurrada → não vale; empurrada → vale; outro texto → não vale).
**Inerte hoje:** nenhuma estratégia passou do orçamento; `m_orcado` 13, `m_executado` 2,
R3/R4 reproduzem. `politica.yaml` 1.29.0.

**Limite declarado (P5):** o verificador lê a referência **local** do remoto, ou seja o que
esta máquina soube no último fetch ou push, e não vai à rede. Forjar essa referência com
`git update-ref` passa no portão; o push seguinte ou o histórico público entregam a
diferença.

## ~~P-134~~ · Custo de entrada maior que o aporte vira `min()` calado na alocação — achado B-16 — **FECHADA em 25/09/2026**

**Dono:** Claude Code · **Gatilho:** no próximo toque em `simular_custo` ou quando algum
chamador fora do pipeline usar `custo_pct_aportado`/`arrasto_anualizado` · **Classe:**
`BLOQUEIA_O_SISTEMA`

Divergência 4 do B-16 (sessão B, 24/09). `alocacao.simular_custo` faz
`c = min(e*aporte, aporte)`: quando o custo de entrada iguala ou passa o aporte, a rota
come o aporte inteiro **sem dizer nada**. O `motor.simular` alertava (K-08.3) — e saiu com a
P-43. No pipeline o G3 barra a rota antes, então hoje é inerte; quem chama as duas funções
direto recebe um número sem o aviso. O conserto é o mesmo desenho do G3: devolver a condição
em vez de engoli-la, com teste que reprove contra a versão atual.


**25/09/2026 — FECHADA.** `AporteConsumidoPelaEntrada`: a simulação recusa com nome. **E a
premissa "hoje é inerte" estava errada:** o `custo_pct_aportado` do alvo e o `custo_de_discordar`
simulam com o aporte **da rota** (`aporte × peso`), e a proposta do segundo não passa pelo G3.
Medido: só `acao_450` (R$ 4,50 a ordem) alcança, com aporte da rota ≤ R$ 4,50. E embaixo havia o
B-19 (aporte R$ 0 → NaN). Três testes; os caminhos que simulam aporte fracionado viram motivo
escrito, e a interação G3×G4 deixa a rota fora.

## ~~P-149~~ · `cenarios.py` cai no `main` — `fora_status` mudou de forma — **FECHADA em 25/09/2026**

**Dono:** Claude Code · **Gatilho:** no próximo toque em `cenarios.py` ou em `fase_universo` ·
**Classe:** `BLOQUEIA_O_SISTEMA` (o `CLAUDE.md` §3 manda rodar `python cenarios.py`)

Medido em 25/09 no `main`, antes da P-134: `for rt,e in u["fora_status"]` →
`TypeError: cannot unpack non-iterable RotaAloc object`. Desde a F-02 o G5 roda **antes** do G3,
sobre rotas nuas, e o `fora_status` passou a guardar rota, não par. O `cenarios.py` não foi junto,
e nenhum teste o roda — é a P-80 (a rotina mede um terço) na forma de um script de exemplo.
Conserto: ler o `fora_status` como rota, e um teste que rode o `main()` do `cenarios.py`.

**FECHADA no mesmo commit.** `alocacao/test_cenarios.py` roda o script e exige os seis
cenários; reprova no `main` de antes (conferido com o conserto guardado).

## ~~P-143~~ · A ponte ticker ↔ `CD_CVM` de 2010 a 2017 não existe no projeto — **FECHADA em 25/09/2026**

> **Fechada.** A ponte é o banco de ISIN da B3: o download estava no JS da página `isinPage/`, e o
> `404` de antes era o endereço suposto. O FCA antigo não tem ISIN (medido). O `EMISSOR.TXT`
> descreve o dono **atual** de cada código (CV-06): liga 136 dos 190 emissores do universo de
> 2010–2012, deixa 50 de fora e tem 4 códigos reaproveitados. **Ponte manual** para 42
> (`docs/aprendizado/ponte-emissor-cvm.yaml`), por sucessão conferida à mão, com os 42 pares
> CNPJ/CD_CVM conferidos no cadastro por teste. 6 ficaram sem ponte, declarados. **Mês da emenda
> 1: mar/2011** (95,8%), igual nas duas leituras de janela
> (`docs/aprendizado/preregistro-ml-v2-emenda-1-medicao.md`). Segue na **P-145**.

**Dono:** Claude Code (achar e medir a fonte) · **Gatilho:** antes de medir o mês da emenda 1 e
antes de qualquer variável da ML-3 · **Classe:** `BLOQUEIA_O_SISTEMA`

Achado CV-05. O FCA só traz `Codigo_Negociacao` a partir de 2018 (0 ações com código de 2010 a
2017). Sem ponte, o universo da §2 (identidade pelo `codeCVM`) não se monta no desenvolvimento,
e o mês da emenda 1 mediria a ponte e não o fundamento. **O mês não foi medido, de propósito.**
Candidatas, `NAO_CONFIRMADO`: cadastro de ISIN da B3 (emissores, código de 4 letras e CNPJ) e o
Formulário de Referência da CVM. O critério da fonte certa: cobrir **empresas deslistadas** antes
de 2018. Uma ponte só dos sobreviventes repete o viés que a §2 existe para evitar.

## ~~P-132~~ · Emenda ao pré-registro v2 (período de desenvolvimento) — **FECHADA em 25/09/2026**

**Dono:** Osvaldo (decisão) · **Gatilho:** antes da montagem da ML-1 e antes de qualquer
resultado; a emenda vai empurrada antes (P-116) · **Classe:** `DECISAO_DE_DESENHO`

> **Fechada:** decisão dele, opção (a), limiar 90%. Regra em
> `docs/aprendizado/preregistro-ml-v2-emenda-1.md`, empurrada em `00aa622` **antes** de qualquer
> medição (sha256 `1aac96023fdc0de9`; v2 intocada, `2e2c46d4de72057f`). **O mês que a regra
> produz não foi medido:** a ponte ticker ↔ `CD_CVM` não existe antes de 2018 (CV-05). Segue
> na **P-143**. O reconhecimento pela P-138 segue na **P-144**.

Achado CV-04. O `preregistro-ml-v2.md` §2 declara período desde jan/2010 *"com fundamentos DFP
desde 2010"*, e a regra `DT_RECEB` ≤ data de decisão deixa **0 empresas** com fundamento de
jan a dez/2010: o menor `DT_RECEB` do `dfp_2010` é **27/01/2011**, e não existe ITR de 2010.
Jan/2011 tem 3 empresas, fev/2011 82, **mar/2011 510**. As opções, sem recomendar: começar o
desenvolvimento quando o fundamento chega (e em que limiar de cobertura), ou manter jan/2010
declarando que os primeiros ~14 meses rodam só com variável de preço. **O `preregistro-ml-v2.md`
não foi tocado.**

## ~~P-131~~ · `nomear_extracoes.plano()` não confere o que já tem o nome certo — **FECHADA em 24/09/2026**

**Dono:** Claude Code · **Gatilho:** — · **Classe:** `BLOQUEIA_O_SISTEMA`

Achado ao fechar a P-120. `JA_CORRETO` sai pelo `continue` antes de `conferir()`: o status
diz *"o nome é o certo"* e é lido como *"a cópia é o conteúdo do ZIP"* — foi assim que o
pedido de 24/09 o leu, e foi assim que a P-126 contou *"24 já corretas"*. Uma cópia truncada
ou de outro ano com o nome certo sai `JA_CORRETO`. Inofensivo hoje (não há cópias), e
exatamente a forma do F-02: status que parece medição sem ter medido. Conserto: conferir
também o `JA_CORRETO` (e `RECUSADO` quando falhar), com teste que reprove contra a versão atual.

**Fechamento, 24/09:** o ramo `JA_CORRETO` de `plano()` chama `conferir()` e sai `RECUSADO`
com o motivo quando ela falha. Dois testes em `fase0/test_nomear_extracoes.py`: cópia de
nome certo e conteúdo **truncado** → `RECUSADO` por tamanho e `main()` sai 1 — **reprovou
contra a versão anterior** (saía `JA_CORRETO`) antes do conserto; e cópia de nome certo e
conteúdo do ZIP continua `JA_CORRETO`, para a conferência não virar recusa geral. `fase0`
verde, `ruff` e `mypy` em zero. Custo: a segunda execução passa a ler as cópias inteiras
para o CRC — é o preço de o status dizer o que mediu.

## ~~P-142~~ · Nove testes do C-02 contra o acervo real **nunca rodam**: a raiz aponta para a pasta errada — **FECHADA em 25/09/2026**

> **Fechada** (pedido dele, 25/09: o alvo do ML é o retorno do `ajustar.py`). Raiz apontada para
> `data/bronze/b3/cotahist/` **com `anos={2023}`**, que é a população para a qual os testes foram
> escritos (o acervo de 18/09 tinha um ano). **Os 9 rodaram e passaram**, sem tocar em nenhum
> número esperado: 454 papéis, 293 degraus, 352/352 preços de véspera, as duas mutações
> reprovando, FLRY 12/06 → 13/06. Em 9 s. Guarda da classe: `fase0/acervo_de_teste.py` →
> `exigir_acervo`, com a regra *sem `data/` pula; com `data/` e arquivo faltando, falha*. É usada
> por todos os `test_REAL_*` (4 arquivos) e achou um décimo skip calado:
> `test_REAL_2023_dentro_da_janela_*` pulava se o `degrau_datas_ex` não existisse.
> `test_acervo_de_teste.py` reprova arquivo com `test_REAL_*` que use `skipif`/`skip`
> (reprovou os 4 arquivos antes do conserto, e reprova a mutação).

**Dono:** Claude Code · **Gatilho:** a próxima tarefa que toque `ajustar.py` ou o C-02 ·
**Classe:** `BLOQUEIA_O_SISTEMA` (a guarda do C-02 em 2023 está desligada sem ninguém saber)

Achado lateral da P-141, na rodada de base de 25/09 (`-rs`). `fase0/test_ajustar.py`
(`RAIZ_ACERVO`, 8 testes `test_REAL_*`) e `fase0/test_calendario.py`
(`test_o_caso_REAL_do_FLRY_contra_o_acervo`) leem o COTAHIST em `data/bronze/b3/`, e ele mora
em `data/bronze/b3/cotahist/` desde a P-114. Resultado: **9 SKIPPED** em toda rodada, com a
mensagem *"nenhum COTAHIST no acervo -- ESTES TESTES NAO RODARAM"* — verdadeira e ninguém a lê.
É a P-114 (*raiz padrão na pasta errada produz recorte com cara de todo*) dentro dos testes: o
`test_ajustar_janela.py` e o `test_calendario_p99.py` já usam `.../cotahist`, e os dois antigos
ficaram para trás.

**Não consertado na P-141, de propósito:** apontar para a pasta certa **liga** 9 testes com
números de 18/09 que ninguém confere desde então; se reprovarem, é trabalho de C-02, não de
velocidade de suíte. O conserto é trocar a raiz e, se algum reprovar, medir antes de mexer no
número. **E a classe inteira pede guarda:** um `skip` com *"NAO RODARAM"* na máquina que **tem**
o acervo devia ser falha, não aviso.

---

## Marcos auditáveis — tags anotadas

*25/09/2026.* Cada pré-registro vale pelo commit em que foi empurrado (P-116). A tag dá nome a
esse commit, e a mensagem traz o arquivo e o sha256. Conferir:
`git show <tag>:<arquivo> | sha256sum`. `auditoria/test_tags_citadas.py` reprova tag citada
aqui que não exista, tag leve e sha256 que não bata.

| tag | commit | arquivo | sha256 |
|---|---|---|---|
| `prereg-ml-v1` | `45405a6` | `docs/aprendizado/preregistro-ml-v1.md` | `2b435316136d3029…` |
| `prereg-ml-v2` | `2c608c9` | `docs/aprendizado/preregistro-ml-v2.md` | `2e2c46d4de72057f…` |
| `prereg-ml-v2-emenda-1` | `00aa622` | `docs/aprendizado/preregistro-ml-v2-emenda-1.md` | `1aac96023fdc0de9…` |
| `prereg-ml-v2-esclarecimentos` | `2f939ae` | `docs/aprendizado/preregistro-ml-v2-emenda-1.md` | `71621ba64c899281…` |

**A última aponta para `2f939ae`, não para `53112d6`.** O prompt de 25/09 pedia `53112d6`, mas
a GIT-01 (P-145, acima) já tinha decidido que vale a primeira §6 publicada no `origin`, e é essa
versão que está no `main`. Uma tag em `53112d6` marcaria como auditável a versão declarada sem
validade. **Se ele quiser a outra, é uma tag nova e uma linha nova aqui, nunca mover esta.**

## ~~P-69 a P-72~~ · Auditoria externa (DeepSeek), conferida contra o código em 10/09 — **FECHADAS em 11/09/2026**

**Documento:** `docs/referencia/AUDITORIA-DEEPSEEK-CONFERIDA.md`. Auditoria de terceiro é **hipótese**, não
achado — cada item foi rodado antes de virar pendência. Os quatro críticos são verdadeiros.

| # | item | classe | veredito |
|---|---|---|---|
| ~~**P-69**~~ | `etf.IMAB11` duplicado em `custos.yaml` (achado **Y-01**) | `BLOQUEIA_O_SISTEMA` | **FECHADA 11/09/2026** — ver tabela `## Fechadas`; abriu a **P-76** |
| ~~**P-70**~~ | `HOJE = dt.date(2026,9,1)` fixo em `motor.py:20` | `BLOQUEIA_O_SISTEMA` | **FECHADA 11/09/2026** — ver tabela `## Fechadas` |
| ~~**P-71**~~ | `dividas`/`objetivos` voltam como `dict`, motor espera dataclass | `BLOQUEIA_O_SISTEMA` | **FECHADA 11/09/2026** — ver tabela `## Fechadas` |
| ~~**P-72**~~ | `aporte_mensal <= 0` bloqueia `carregar()` | `BLOQUEIA_O_SISTEMA` | **FECHADA 11/09/2026** — ver tabela `## Fechadas` |

### O que os quatro têm em comum, e isso vale mais que os quatro

**P-71 e P-72 moram na costura entre dois módulos que cada um testa sozinho.** Os testes do
G1 montam `Divida(...)` na mão; `test_usuario_novo.py` monta o cadastro em memória. Nenhum
passa por `estado_io.carregar()`. **269 testes, e a porta de entrada real do sistema não é
exercitada por nenhum.**

Isso não é um bug: é uma lacuna de cobertura com forma reconhecível. O próximo defeito real
provavelmente mora ali também.

**E morava — duas vezes.** O teste que fecha P-71/P-72 (`test_p71_p72_porta_de_entrada.py`)
escreve um estado sintético (`tmp_path`, nunca o real) com dívida, objetivo e
`aporte_mensal=0`, carrega pelo caminho real e roda `alocar()` até o fim. Ele bateu em
QUATRO exceções diferentes, cada uma só visível depois que a anterior foi corrigida:
`EstadoInvalido` (P-72) → `AttributeError` em `g1_divida` (P-71) → `TypeError:
Estado.__init__() got an unexpected keyword argument 'reserva_empenhada'` (achado lateral:
`d` carregava `reserva_empenhada` e `meses_cobertos`, nenhum campo de `Estado` — o primeiro
já apontado como campo morto pela própria auditoria externa, o segundo duplicava uma
`@property` que `Estado` já calcula) → `ValueError: pesos somam 0` (achado lateral em
`custo_entrada_fixo_pct`, que tratava `aporte==0` como custo infinito para QUALQUER rota,
inclusive as de tarifa zero). `Estado(**estado_io.carregar()[0])` nunca tinha sido
executado, nem uma vez, fora deste teste.

### Correção à auditoria, registrada porque o método exige

**A1 (bônus arredondado, `aporte.py:69`) é verdadeiro, mas a auditoria o descreve pela
metade.** Ela diz "projeção otimista". Medido: 5/ano → 6 disparos (**+20%**), 7/ano → 6
(**−14%**), 11/ano → 12 (**+9%**). **Erra nos dois sentidos.** Viés que troca de sinal
conforme o input é pior que viés constante: não dá para corrigir de cabeça.

### Onde a auditoria erra de forma que importa: a ordem

Ela propõe **quatro semanas de motor** e a Fase 0 depois. É a P-44 sendo violada por
escrito, e o **X-01** torna o argumento mais forte — o dado estruturado da CVM responde 3
dos 10 passos de uma leitura de incorporadora, e nenhuma refatoração do motor antecipa
essa descoberta. Some-se o prazo semanal declarado pela própria CVM.

**Ordem defendida:** P-69 a P-72 (horas, não semanas) → **Fase 0** → o resto **em paralelo**.

---

> **26/09/2026:** fechada no corpo em 11/09/2026 e com o cabeçalho aberto até hoje; riscada e movida para cá no corte do `PENDENCIAS.md`.

## ~~P-83~~ · Nove casas não pesquisadas carregavam custo ZERO — e a decisão 1 ia acordá-lo — **FECHADA em 16/09/2026**

**Classe:** `BLOQUEIA_O_SISTEMA`. **FECHADA em 16/09/2026** na parte que é defeito.
A dimensão do ranking, que é a decisão, **continua aberta** — ver P-84.

Fui implementar a sua decisão de 13/09 (*"custo por operação entra no ranking: **sim**"*)
e medi os campos antes de escrever a dimensão. A medição derrubou a premissa e achou
outra coisa.

### O que a medição mostrou

| campo | declaram | valores distintos |
|---|---|---|
| `corretagem_fii` | 11 / 24 | **um só: 0,0** |
| `exercicio_opcao_pct` | 4 / 24 | **um só: 0,005** |
| `mesa_minimo` | 4 / 24 | 20 · 25 · 50 — o único que varia |
| `corretagem_etf_pct` | 24 / 24 | 0,0 em 23, **0,005 na XP** |

**Dois dos três campos que você autorizou são constantes.** Uma dimensão construída
sobre eles adiciona peso ao ranking e **não muda ordenação nenhuma** — é um número que
parece medir. É a forma do `pl_medio_3a`.

### E o que estava embaixo, que é o achado

`corretagem_etf_pct: 0.0` e `corretagem_pct: 0.0` estavam escritos em **nove casas cuja
própria `fonte` diz, com estas palavras, "custos NÃO OBTIDOS"** — Clear, BTG, Bradesco,
Mirae, Órama, Guide, Necton, Vitreo, Avenue. O `corretagem_rv` delas é `null`, ou seja
*"não sei"*, e o campo vizinho traz zero.

**Zero é o melhor valor possível.** É o F-02 na letra — o mesmo defeito da BOVV11, cuja
taxa `NAO_CONFIRMADO` virava `adm_aa = 0.0` e a punha como a rota mais barata do
catálogo. Não mordeu até hoje por um acidente: **os campos eram mortos.** A sua decisão
de pôr o custo por operação no ranking é exatamente o que os acordaria, e nove casas não
pesquisadas estreariam com custo zero de graça.

**E o zero tinha um segundo andar:** `corretagem_pct: float = 0.0` era o *default do
dataclass*. Limpar só o YAML deixaria o zero morando um nível acima, pronto para voltar
na primeira casa que não declarasse o campo.

### O que foi corrigido

Os 18 zeros viraram `null`; os dois defaults viraram `None`; e `pontuar()` passou a tirar
a dimensão quando **qualquer** das duas parcelas é desconhecida — meio custo conhecido não
é um custo, e somar a metade que se sabe com um zero inventado dá um número otimista por
construção.

**Instantâneo dourado: o ranking saiu byte a byte idêntico** (`ee59cd02…`). A correção é
inteiramente inerte hoje, que é exatamente o ponto — os zeros estavam dormindo.

Três guardas, as três provadas por mutação: nenhuma casa `NAO_CONFIRMADO` pode carregar
número de custo (guarda de **classe**, não dos dois campos); o default do dataclass não
pode voltar a ser zero; meio custo não pontua.

---

> **26/09/2026:** fechada no corpo em 16/09/2026 e com o cabeçalho aberto até hoje; riscada e movida para cá no corte do `PENDENCIAS.md`.

## ~~P-85~~ · O relatório do ranking mudava de texto entre execuções — **FECHADA em 16/09/2026**

**Classe:** `BLOQUEIA_O_SISTEMA`. **FECHADA em 16/09/2026.**

Peguei tentando usar a saída do `corretoras.py` como instantâneo dourado — que é
justamente para o que ela não servia. A linha *"vencedores distintos: N — <lista>"*
juntava um `set`, e `set` de string não tem ordem **entre processos**.

**O `refinar.py` já tinha aprendido a lição e escrito o motivo** — *"Ordem ESTÁVEL. Sem
isso o instantâneo dourado acusa diferença a cada rodada e para de servir como rede"* — e
ela não atravessou de módulo para módulo. É o A-07 (funções irmãs) com o irmão sendo um
**módulo**: regra aplicada num lugar só.

A guarda roda o relatório em **subprocesso**, com `PYTHONHASHSEED` diferente — dentro de
um processo só a ordem do `set` é estável e o defeito não aparece.

---

---

> **26/09/2026:** fechada no corpo em 16/09/2026 e com o cabeçalho aberto até hoje; riscada e movida para cá no corte do `PENDENCIAS.md`.

## ~~P-86~~ · O `chaves_orfas.py` escondia 42 de 67 chaves, e emudecia por escolha de nome — **FECHADA em 16/09/2026**

**Classe:** `BLOQUEIA_O_SISTEMA`. **FECHADA em 16/09/2026.**

A ferramenta deduplicava por **nome de folha**: a segunda ocorrência de qualquer nome no
mesmo arquivo **sumia do relatório** — nem órfã, nem lida, invisível. `bc_procedentes`
aparecia para o Itaú e calava para as outras oito casas; `variantes_permitidas` aparecia
numa estratégia e sumia em sete.

**Peguei sem procurar**, e é isso que torna o defeito caro: batizei uma chave nova
(`custo_por_operacao.e_uma_decisao_nao_uma_omissao`) com o mesmo nome de folha de uma
existente, e a **existente desapareceu da auditoria**. Uma guarda que emudece porque
alguém escolheu um nome é pior que guarda nenhuma — e o sintoma é a linha de base
**encolher**, que é a direção que parece progresso.

Corrigido para dedupe por caminho: **17 órfãs + 8 lidas-só-por-teste viraram 35 + 32.**

### Zero espécies novas, e é isso que permitiu fechar barato

As 42 escondidas são **nove espécies**, e todas já tinham o porquê escrito na linha de
base — para *uma* instância. A linha de base declarava uma e cobria N em silêncio.
Listá-las uma a uma seria copiar o mesmo motivo 42 vezes, então entrou `ESPECIES`, com
glob e o motivo escrito na espécie (precedente na casa: `test_alocacao.py` já usa
`corretora.*.e_uma_decisao_nao_uma_omissao`).

E a guarda nova **me pegou na mesma rodada**: pus `instituicoes.*.facilidade.exporta_csv`
por simetria, e o teste de *"espécie declarada que não casa com órfã nenhuma"* reprovou —
nenhuma casa declara esse campo.

`test_a_ferramenta_NAO_deduplica_por_nome_de_folha` é a guarda da guarda, com prova por
mutação.

---

> **26/09/2026:** fechada no corpo em 16/09/2026 e com o cabeçalho aberto até hoje; riscada e movida para cá no corte do `PENDENCIAS.md`.

## ~~P-118~~ · `politica.yaml` cita a P-96 como aberta, e ela fechou em 18/09 — **FECHADA em 23/09/2026**

**Dono:** Claude Code · **Gatilho:** no próximo bump de `politica.yaml` · **Classe:**
`DECISAO_DE_DESENHO`

`limitacoes_declaradas.captura_do_cotahist_ainda_nao_e_rotina.direcao_do_vies` diz
*"identico em tamanho ao capturado em 04/09. **Confirmar por sha256 fecha a P-96**"*. O
sha256 **foi** confirmado — a P-96 está na tabela de fechadas desde 18/09 (`ad1603788d78aaa1…`
dos dois lados, 14 dias de intervalo), e em 23/09 a medição foi repetida ao mover a duplicata.

É uma linha que manda fazer o que já foi feito. Inofensiva hoje e exatamente a forma de
defeito que o projeto persegue: **declaração que o próprio repositório já contradiz.** Trocar
"confirmar fecha" por "confirmado em 18/09 e em 23/09" é uma linha — mas mexer em
`limitacoes_declaradas` pede bump de versão, e não havia outro motivo para bumpar nesta
rodada.

> **23/09 — FECHADA no bump 1.23.0**, junto com o portão da §5-B.16. A linha agora diz
> *"confirmado em 18/09 e em 23/09"*. E o portão achou mais duas da mesma forma —
> `ordem_dos_portoes_nao_e_dado` (P-07) e `isento_ir_e_booleano_e_o_fii_nao_e` (P-13),
> ambas consertadas em 05/09 —, marcadas `RESOLVIDA`.

> **26/09/2026:** fechada no corpo em 23/09/2026 e com o cabeçalho aberto até hoje; riscada e movida para cá no corte do `PENDENCIAS.md`.


## ~~P-151~~ · O job `completo` do *Testes* fica vermelho sempre que houver branch de sessão aberta — **FECHADA em 26/09/2026**

**Dono:** Claude Code · **Gatilho:** antes da rodada agendada de segunda, 28/09, 11:00 UTC, ou
na primeira em que uma branch de sessão estiver à frente do `main` · **Classe:**
`BLOQUEIA_O_SISTEMA` (um portão que acende sem defeito esconde o que acende com defeito)

Medido em 26/09 pela nuvem, lendo o log: a única execução do job `completo` pedida pela P-146
(*Testes #16*, `36178274615`, disparo manual de 25/09 19:12Z) saiu **vermelha por um teste só**,
`auditoria/test_git01_branches_integradas.py::test_git01_toda_branch_do_origin_esta_no_head`,
com `['origin/claude/ecstatic-planck-wgbd03', 'origin/wip/sessao-b']`. Todo o resto passou: 555
em `alocacao`, 470 em `fase0` (39 pulados por falta de acervo local), 73 em `auditoria`, 6 em
`tools`; `ruff` e `mypy` em zero; armazém com 0 faltas.

**A causa:** os dois jobs fazem `fetch-depth: 0` (para as tags), então enxergam todas as
branches do `origin`. A guarda do GIT-01 foi escrita para a **sessão** (*"leia antes de
trabalhar"*); no runner, uma branch de PR aberto é o estado normal, não outra sessão fazendo a
tarefa. O GIT-02 já tirou o Dependabot pelo mesmo motivo. Com o semanal vermelho por isso, um
vermelho de verdade passa sem ninguém olhar (A-08: alarme que dispara sempre é alarme desligado).

**Hoje (26/09, 10:30Z) nenhuma branch fora do Dependabot está à frente do `main`**, então a rodada
de segunda passa se nada abrir até lá. **Proposta:** a guarda pula quando `GITHUB_ACTIONS` está
definido, com um controle que prove que fora do CI ela ainda reprova. A pergunta da guarda é de
sessão, e o CI já tem a sua: o PR roda contra o `main` de verdade.

**FECHADA em 26/09/2026.** A guarda do GIT-01 pula quando `GITHUB_ACTIONS=true` (`auditoria/test_git01_branches_integradas.py::no_ci`), porque no runner branch aberta de PR ou de medição é o estado normal. Controle: `test_P151_so_o_CI_pula_e_fora_dele_a_guarda_ainda_reprova`, que **não** pula no CI, prova que só o valor exato do runner pula e que, fora dele, uma ref em `refs/remotes/origin/` fora do HEAD ainda é acusada. Medido nos dois modos: sem a variável, 5 passam; com `GITHUB_ACTIONS=true`, a guarda pula e o controle passa.

## ~~P-124~~ · A custódia do Tesouro é descontada por mês, e a B3 cobra por semestre — **FECHADA em 26/09/2026**

**Dono:** Osvaldo (decidir) · **Gatilho:** nenhum · **Classe:** `DECISAO_DE_DESENHO`

Também declarada sem pendência. Ordem de grandeza: centavos por ano a R$ 500/mês, e erra
**contra** o Tesouro. A decisão é se a aproximação fica (escrita como escolha) ou se o motor
passa a descontar por netting pro rata. Entrada `periodicidade_da_custodia_do_tesouro`.

> **Decisão dele, 26/09/2026: `124a`** (recomendada) — a custódia mensal fica, escrita como escolha. Registro em `docs/decisoes/fila-do-osvaldo.md`.

**FECHADA em 26/09/2026.** Decisão dele (`124a`): a aproximação mensal fica, **escrita como escolha**. A entrada `limitacoes_declaradas.periodicidade_da_custodia_do_tesouro` ficou `RESOLVIDA` com o motivo (erra centavos por ano, contra o Tesouro, sem mudar ordenação), e a escolha está escrita no ponto do motor que a aplica (`alocacao.py`, `simular_custo`, bloco `custodia_td`). Política 1.33.0.

## ~~P-84~~ · A dimensão de custo por operação — o que a decisão 1 ainda precisa — **FECHADA em 26/09/2026**

**Classe:** `DECISAO_DE_DESENHO`. **Dono:** Osvaldo. **Gatilho:** agora; nada trava.

Com a P-83 corrigida, sobra a pergunta de desenho, e ela é sua porque envolve **peso**,
que é política declarada:

- `corretagem_fii` e `exercicio_opcao_pct` são **constantes**. O projeto já tem o
  mecanismo certo para isso e o precedente escrito: `reclame_aqui` é **exibido e nunca
  pontuado** (`politica.yaml → pontua: false, exibe: true`). Eles saem de campo morto sem
  fingir que discriminam.
- `mesa_minimo` varia (20/25/50) mas só 4 de 24 declaram, e **não dá para separar "não
  tem mesa" de "não pesquisei"**. Pontuá-lo penalizaria 20 casas pela ausência de um
  produto, não pela falta de transparência.
- `corretagem_etf_pct` é o único com cobertura real depois da P-83 (15 casas) e com um
  valor que separa: **os 0,50% da XP em ETF.** É também o que mais importa para quem
  compra ETF — e ele **não estava** nos três que você autorizou.

**A pergunta:** a corretagem de ETF entra como segunda parcela da dimensão `corretagem`
que já existe (sem inventar peso novo), ou como dimensão própria com peso declarado por
você no `politica.yaml`?

> **Decisão dele, 26/09/2026: `84a`** (recomendada) — a corretagem de ETF entra como segunda parcela da dimensão `corretagem`; `corretagem_fii` e `exercicio_opcao_pct` viram "exibe, não pontua". Registro em `docs/decisoes/fila-do-osvaldo.md`.

**FECHADA em 26/09/2026.** Decisão dele (`84a`), e **já estava implementada desde 16/09**: `corretoras.py` pontua a dimensão `corretagem` pelo pior caso entre ação e ETF (`max(custo_acao, corretagem_etf_pct)`), sem peso novo, e `custo_por_operacao.exibidos` lista `corretagem_fii`, `exercicio_opcao_pct` e `mesa_minimo` como exibidos e nunca pontuados. Teste: `test_P84_o_PIOR_CASO_entre_acao_e_ETF_e_o_que_pontua`. A pendência ficou dez dias aberta com a resposta no código — reincidência da fila desatualizada, em `eventos.csv`.

## ~~P-81~~ · O `chaves_orfas.py` não separa decisão registrada de parâmetro órfão — **FECHADA em 26/09/2026**

**Classe:** `DECISAO_DE_DESENHO`. **Dono:** Claude, com sua confirmação.
**Gatilho:** a próxima vez que a linha de base crescer.

Reconferindo a linha de base em 16/09, dez chaves entraram de uma vez — e não porque
alguém escreveu chave nova: o instrumento passou a contar **"LIDA SÓ POR TESTE"** como
órfã. A mudança é deliberada e vem da P-77 (*campo que só o teste toca é campo que o
motor não usa*).

Mas as dez **não são da mesma espécie**, e a diferença decide o que fazer com cada uma:

- **parâmetro órfão** — `portoes.G3_atrito.ativo` prometia comportamento e não
  entregava. É defeito, e foi o E-03.
- **decisão registrada** — `corretora.promocional.e_uma_decisao_nao_uma_omissao: true`
  não promete comportamento nenhum: ela **registra um julgamento**, e o teste a lê para
  fixar o registro. Isso é procedência, não dívida.

Cinco das dez são do segundo tipo. Hoje elas convivem na mesma lista, e uma lista que
mistura duas espécies faz a próxima pessoa tratar procedência como dívida — ou, pior,
tratar dívida como procedência. O instrumento precisa de um terceiro rótulo, ou o YAML
precisa de uma convenção que ele reconheça.

> **Decisão dele, 26/09/2026: `81a`** (recomendada) — o YAML declara a chave de registro, e o instrumento lê. Registro em `docs/decisoes/fila-do-osvaldo.md`.

**FECHADA em 26/09/2026.** Decisão dele (`81a`): o YAML declara, o instrumento lê. `_registros: [nome]` ao lado da chave marca registro de julgamento; `auditoria/chaves_orfas.py` (`registros()`) tira essas chaves das órfãs e as lista à parte (`DECISAO REGISTRADA`), e recusa declaração que aponte para chave inexistente. Dez chaves marcadas no `politica.yaml`; saíram da linha de base as cinco da P-81 e as duas espécies (`*.tem_piso_legal`, `corretora.*.e_uma_decisao_nao_uma_omissao`). Teste com mutação: `test_P81_decisao_registrada_sai_das_orfas_e_aparece_a_parte`.

## ~~P-12~~ · `DATADO` cobra liquidez onde deveria cobrar vencimento — **decisão sua** — **FECHADA em 26/09/2026**

Achado H-01, ao catalogar LCI/LCA. A função `DATADO` exige `exige_liquidez_dias: 30`.
Isso trata um problema de **duração** com critério de **liquidez**.

Simulei a chegada da carência sem tocar no YAML: com 270 dias a rota perde **todas**
as funções; com 90, idem; com 30, só sobra `DATADO`. Uma LCI isenta de IR, coberta
pelo FGC e que **vence exatamente na data do objetivo** seria eliminada por uma
iliquidez que o objetivo não precisa.

A regra correta seria "vence até a data do objetivo **ou** é líquida em 30 dias" — o
mesmo padrão que o G8/CARREGO já usa para `PROTECAO_REAL`. Não mudei porque afrouxar
`exige_liquidez_dias` sozinho deixa entrar também coisa ilíquida que não vence em data
nenhuma; a mudança precisa vir com o casamento de vencimento junto.

**Efeito hoje: zero** — LCI/LCA estão bloqueadas no G5 e o G6 nem as vê. Morde no dia
em que a carência for confirmada. Há um teste que falha se alguém mexer no `DATADO`
sem atualizar este registro.

> **Decisão dele, 26/09/2026: `12a`** (recomendada) — DATADO aceita "vence até a data do objetivo **ou** líquida em 30 dias", junto com o casamento de vencimento. Registro em `docs/decisoes/fila-do-osvaldo.md`.

**FECHADA em 26/09/2026.** Decisão dele (`12a`), com o casamento de vencimento junto. `funcoes.DATADO.liquidez_ou_vencimento_casado: true`: o G6 não reprova a rota ilíquida que tem vencimento conhecido, e `casa_duracao` exige que ela vença até o **menor** prazo dos objetivos (V-07). **A armadilha que a medição achou:** `duracao_anos` é duração de JURO (0,0 na LCI pós-fixada), não prazo até o vencimento — casar por ela deixaria passar a LCI de 9999 dias. Nasceu o campo `vencimento_anos`, vazio em todo o catálogo: sem ele a rota ilíquida continua fora (P1), e nenhuma alocação mudou (instantâneos verdes). Limitação `datado_cobra_liquidez_onde_deveria_cobrar_vencimento` `RESOLVIDA`; política 1.33.0; `test_P12_DATADO_aceita_vencimento_casado_no_lugar_da_liquidez`, com três mutações.

## ~~P-117~~ · O silver passou a ter dois arquivos para a mesma captura, e quem escolhe é o `sorted()` — **FECHADA em 26/09/2026**

**Dono:** Osvaldo decide · **Gatilho:** antes da próxima corrida do `refinar.py` ·
**Classe:** `DECISAO_DE_DESENHO`

A P-114 criou `eventos_silver_2026-09-11_cal-1986-2026.csv` ao lado de
`eventos_silver_2026-09-11.csv` — por instrução dele, para não sobrescrever o de 11/09. São
**duas tabelas da mesma captura**, diferindo só no calendário que derivou a `data_ex`.

`ajustar.ultimo_silver()` escolhe **o último em ordem alfabética**, e por sorte isso é o
arquivo com o calendário largo. **Sorte não é regra.** Um `eventos_silver_2026-09-11_antigo.csv`
inverteria a escolha sem que nada reclamasse, e a corrida seguinte mediria a série com 383
datas ex em vez de 9.271 — sem erro, sem aviso, e com número plausível na saída.

**A raiz do problema é o nome:** o silver é função de **dois** insumos (a captura e o
calendário) e o nome só carregava um. A decisão é qual das três:

1. o `refinar.py` passa a nomear a saída com os dois insumos (`_cal-<ini>-<fim>`), sempre —
   é o mais honesto e mexe em testes que hoje esperam o nome curto;
2. `ultimo_silver()` ganha regra explícita (maior cobertura para a captura mais recente) e
   um teste — mais barato, mantém a convenção;
3. o silver de 11/09 é aposentado e fica um arquivo só — mais simples, e perde o lado a
   lado que a P-114 usou como instantâneo dourado.

**Hoje a corrida imprime qual silver leu**, então nada está oculto — mas *"está escrito na
saída"* é a defesa que a P7 recusa: depende de alguém ler.

> **Decisão dele, 26/09/2026: `117a`** (recomendada) — o nome do silver passa a carregar os dois insumos (captura + calendário), sempre. Registro em `docs/decisoes/fila-do-osvaldo.md`.

**FECHADA em 26/09/2026.** Decisão dele (`117a`). `refinar.nome_do_silver` grava `eventos_silver_<captura>_cal-<AAAAMMDD>-<AAAAMMDD>.csv` (ou `_cal-nenhum`), sempre: datas completas, porque dois calendários que terminam em dias diferentes do mesmo ano colidiriam. `ajustar.ultimo_silver` deixa o `sorted()` e passa a ter regra escrita: a captura mais nova; dentro dela, o maior calendário lido do nome (o legado `_cal-1986-2026` do P-114 é lido como ano inteiro); o nome sem calendário só vale se for o único; empate levanta `SilverAmbiguo`. O caso da P-117 (um `_antigo` que o `sorted()` poria por último) está no teste e não inverte mais a escolha. Os silvers já gravados no disco dele continuam legíveis.

## ~~P-152~~ · O G8 tem de honrar o `REGRA_DECIDIDA` que o validador anuncia (G-07) — **FECHADA em 26/09/2026**

**Dono:** Osvaldo (decidir) · Claude Code (implementar) · **Gatilho:** antes de gravar a
assinatura do `td_ipca` (P-01) · **Classe:** `DECISAO_DE_DESENHO`

O defeito é do motor, não do registro: `g8_compromisso_de_carrego` libera peso a qualquer
carrego válido, e `validar_carrego` anuncia que em `REGRA_DECIDIDA` ele não libera. **Proposta:**
o G8 passa a mandar o carrego em `REGRA_DECIDIDA` para `sem_compromisso`, com o motivo *"regras
seladas, posição não existe; libera no dia da compra"*, e um teste que aloca com o registro
assinado e exige `protecao_real = 0` — reprovando na versão de hoje. É apertar o portão para
ele fazer o que declara; como a instrução de 26/09 foi *"sem mexer nos portões"*, a decisão é
dele. Alternativa: gravar o `td_ipca` só no dia da compra, já em `COMPROMISSO_ATIVO`, e o
defeito fica sem efeito até lá.

**FECHADA em 26/09/2026.** Decisão dele (26/09, sessão G-07): *"G-07 é defeito, não política"* — a regra está escrita no validador e no `CLAUDE.md`, e o portão a ignorava. `g8_compromisso_de_carrego` agora lê o estado (`_estado_do_carrego`, com o mesmo default do validador) e manda `REGRA_DECIDIDA` para `sem_carrego` com a pendência "na compra, preencher C02 e C04 e mudar para COMPROMISSO_ATIVO". **Teste que falha na versão anterior:** `test_G07_regra_decidida_nao_libera_peso_no_g8` (2 de 3 reprovam no G8 antigo). **Instantâneo dourado** (9 cenários, `alocar()` inteiro, campo a campo): só mudam os 3 cenários com o registro assinado em memória — `td_ipca` 15% → 0, `protecao_real` 0,15 → 0, `lastro` +15 p.p. para `td_selic`, uma pendência `G8_carrego:td_ipca` a mais, o alerta de PROTECAO_REAL sem rota viável. Sem assinatura (o `teses.yaml` do repositório) e em `COMPROMISSO_ATIVO`: **zero diferenças**.

## ~~P-01~~ · Assinatura dos dois registros · `DADO_DE_UM_USUARIO` — **FECHADA em 26/09/2026**

Os dois rascunhos estão prontos em `alocacao/teses.yaml` e passam em todas as
verificações de conteúdo. Faltam três edições, e nenhuma delas eu posso fazer.

**HASH11** — apagar `exemplo: true` e colar `impressao: 31a31607f3c60e62`.
**Tesouro IPCA+** — apagar `exemplo: true`, trocar `C06_reconhecimento` para `true`
e colar `impressao: 942c75bae248327b`.

> Antes de assinar o HASH11, responda a pergunta anterior: **você quer a posição?**
> Ela reprova ou é inaplicável em todos os portões do catálogo buy & hold, custa
> 1,30% a.a. e a perda máxima aceita é 100%. "Não compro" é uma resolução completa
> e custa zero. Assinar o rascunho porque ele está pronto é o erro que o
> pré-registro existe para impedir.

**Gatilho:** nenhum. Depende só de você decidir.

> **Não bloqueia desenvolvimento** (U-01). O sistema aloca sem nenhuma tese assinada —
> as rotas que exigem registro viram pendência com o motivo escrito, e as outras
> recebem peso. Isto bloqueia **a sua carteira**, não o projeto.

> **Decisão dele, 26/09/2026: `01b`** (**diverge da recomendada (01a)**) — **assinar as duas teses** (HASH11 e Tesouro IPCA+), com impressão digital, sem mexer nos portões; o texto final vai a ele antes de gravar. Registro em `docs/decisoes/fila-do-osvaldo.md`.

> **26/09/2026 — assinatura preparada, NÃO gravada; e ela achou dois defeitos.**
> 1. `python tese.py`, o comando que calcula a impressão, **caía** com `KeyError: 'compromissos'`
>    desde a L-01. Consertado (`main()` usa `carregar_politica`), com teste que falha na versão
>    anterior. As impressões batem com as escritas aqui: `hash11` **`31a31607f3c60e62`**,
>    `td_ipca` **`942c75bae248327b`**.
> 2. **G-07:** assinado em `REGRA_DECIDIDA`, o `td_ipca` **recebe 15% em PROTECAO_REAL** no
>    cenário sintético — o G8 não lê o estado, embora o validador diga que não libera peso.
>    Conserto na **P-152** — feito em 26/09, decisão dele: *"G-07 é defeito, não política"*.
>
> **Medido, o que assinar muda** (cenário sintético `test_alocacao.BASE`, registros assinados em
> memória): `aposta` 0 → **3%** (`hash11`), `protecao_real` 0 → **15%** (`td_ipca`, pelo G-07),
> `lastro` 35% → 19%, `rv` 65% → 63%. O texto final das duas foi mostrado a ele no chat; a
> gravação espera o OK dele e a decisão da P-152.
>
> **26/09/2026 — G-07 consertado (P-152 fechada).** O G8 agora lê o estado: assinado em
> `REGRA_DECIDIDA`, o `td_ipca` fica em **0%** até a compra, e o efeito da assinatura passa a
> ser só o do `hash11`. A gravação espera o **"assino"** dele sobre o texto final.
>
> **26/09/2026 — respostas dele ao texto.** HASH11: sai a regra de desuso do K02 e sai o
> K04(c); o resto fica. Tesouro IPCA+: o C03 mantém "9 meses" fixo, com um **alarme**. O alarme
> está no motor (`pendencias_de_premissa`): lê os meses do texto assinado do C03 e, se a meta da
> reserva que o G2 calcula (6 × estabilidade + 0,5 por dependente, com teto) não for esses
> meses, abre a pendência *"tese td_ipca desatualizada, reassinar?"*. A meta não é um campo do
> `perfil.yaml`, é conta (política × EST01 × dependentes do estado), e o alarme usa a mesma conta.
> Impressões dos textos finais: `hash11` **`ea8c8769bbf021e2`** (nova), `td_ipca`
> **`942c75bae248327b`** (texto inalterado). A gravação espera o **"assino"**.

**FECHADA em 26/09/2026.** Assinada por ele no chat em 26/09/2026 ("Assinar"), sobre o texto final mostrado antes de gravar. Mudanças dele no texto: no HASH11, sai a regra de desuso do K02 e sai o K04(c); no Tesouro IPCA+, o C03 mantém "9 meses" fixo, com o alarme `pendencias_de_premissa` (PR #22). Impressões gravadas: `hash11` **`ea8c8769bbf021e2`**, `td_ipca` **`942c75bae248327b`** (texto inalterado). O `td_ipca` fica em `REGRA_DECIDIDA`: válido, sem peso até a compra (G-07, PR #21). **Efeito medido** (cenário sintético, estabilidade baixa, reserva cheia): aposta 0 → 3% (`hash11`), RV 56% → 54,32%, lastro 44% → 42,68%, `td_ipca` 0%, sem pendência de reassinar. Os dois testes que exigiam "só modelos no repositório" viraram `test_repositorio_assinado_libera_so_o_que_a_assinatura_diz`, que fixa as impressões e o estado.

## ~~P-159~~ · Ler a Resolução CVM 19/2021 na fonte primária e confirmar ou retirar a tese de independência — **FECHADA em 26/09/2026**

**Dono:** sessão de pesquisa (nuvem), com a transcrição em `docs/fontes/` · **Gatilho:** antes
da P-158 e antes de qualquer texto público que prometa independência · **Classe:**
`DECISAO_DE_DESENHO`

A pesquisa de fundação apoia a tese de independência ("não distribui produto, não recebe
comissão, não aceita anúncio") e a leitura de que "padrão é recomendação" num **achado de 20/09
sobre a CVM 19 que só existe no chat**: não está no `ACHADOS.md` nem em `docs/fontes/`. Em
26/09 toda afirmação que se apoia nele passou a `NAO_CONFIRMADO` (nota N-CVM nos documentos de
`docs/marca/`). O que fecha: o texto da resolução transcrito da fonte primária, com os
dispositivos que se aplicam, e a tese **confirmada** (as notas N-CVM saem, com a citação) ou
**retirada** (a promessa sai da fundação de marca, como retratação, não apagada).

**FECHADA em 26/09/2026.** A Resolução CVM 19/2021 foi lida na fonte primária (site da CVM, texto consolidado até a 179/2023) e transcrita em `docs/fontes/cvm-resolucao-19-consolidada.md`, com URL, data de acesso e sha256 do PDF e do DOCX. **Confirmadas com escopo:** o padrão individualizado é recomendação (art. 1º, § 1º, I e II) e a atividade é privativa de consultor (art. 2º), para o MEOL oferecido a terceiros; a vedação de garantir rentabilidade (art. 18, III). **Retirada:** "não distribuir, não receber comissão e não aceitar anúncio" como critério da CVM — a norma permite distribuir com segregação (art. 18, I e § 2º) e não fala de anúncio; as três ficam como escolha do MEOL. Retratação em `eventos.csv`. O enquadramento do MEOL segue na P-158. Não é parecer.

## ~~P-147~~ · A captura do NEFIN ainda não rodou no executor — **FECHADA em 27/09/2026**

**Dono:** o workflow (ninguém dispara) · **Gatilho:** o cron diário das 09:15 UTC, ou um *Run
workflow* da *Captura CVM* · **Classe:** `BLOQUEIA_O_SISTEMA` (o CSV saiu do git e só volta
ao runner pelo armazém)

O CSV do NEFIN saiu do git em 25/09 (LIC-01). `fase0/capturar_nefin.py` rodou uma vez, na
máquina dele, e subiu a versão fixada ao R2 (`novo`, `619991c2192c…`). O passo `captura_nefin`
entrou no `captura_cvm.yml`. **Fecha quando** o passo sair verde no executor. Nesse dia, apagar
`limitacoes_declaradas.captura_do_nefin_ainda_nao_rodou_no_executor`, e o `test_P7` cobra que o
regime seja declarado onde ele lê.

**FECHADA em 27/09/2026.** A execução agendada `36246158435` do `captura_cvm.yml` (schedule, 26/09, 13:44Z) rodou o passo `captura_nefin` verde; o passo "Falhar se a captura falhou" foi pulado, então o código foi 0. O NEFIN entrou em `regimes_de_captura` (política 1.36.0), e a limitação ficou `RESOLVIDA`. `test_P147_nefin_roda_sozinho_e_nao_e_mais_limitacao` reprova a volta.

## ~~P-155~~ · Ler a WCAG na fonte: contraste, alvo de toque e daltonismo · era P-WCAG — **FECHADA em 27/09/2026**

**Dono:** sessão de pesquisa (nuvem) · **Gatilho:** antes do brandbook e da primeira tela
desenhada · **Classe:** `DECISAO_DE_DESENHO`

O capítulo de acessibilidade do Pix é recomendação e não cobre contraste, tamanho de alvo nem
daltonismo ([Pix v7.4](../marca/pesquisa-pix-e-pendencias-2026-09.md), §1.1). Os requisitos
de interface declaram a lacuna (§5, item 2). O que fecha: a WCAG lida na fonte, com os critérios
que viram requisito novo (RI-22 em diante) e a verificação de cada um.

**FECHADA em 27/09/2026.** A WCAG 2.2 foi lida na recomendação do W3C (REC de 12/12/2024, acesso em 27/09/2026 04:54 UTC) e nas páginas Understanding dos 13 critérios candidatos, e transcrita em `docs/fontes/wcag-22-w3c.md`, com URL, Last-Modified e sha256 de cada página e a licença de documentos do W3C lida. Número, nível e limiar de cada critério foram conferidos no HTML da recomendação. Viraram os **RI-22 a RI-34** (`docs/marca/requisitos-interface-v1.md`, v1.1, tema E), cada um com a verificação: o teste de contraste dos tokens (P-163), o teste de navegador da etapa 4 ou revisão. O RI-34 (autenticação) não se aplica à v1, sem login, e passa a valer com a P-165. O que a WCAG não resolve para este público (alfabetismo, jargão) ficou como limitação 6 do documento, apontando para os RI-01 e RI-03 e para a P-156. Não é auditoria de acessibilidade; a lei brasileira não foi lida.

## ~~P-163~~ · Direções visuais como estímulo: a T1 desenhada em cada direção — **FECHADA em 27/09/2026**

**Dono:** Claude Code (nuvem) · Osvaldo (aprova antes do teste) · **Gatilho:** P-155
fechada (**feito em 27/09**) e bloco 16 da fila respondido · **Classe:** `DECISAO_DE_DESENHO`

Uma tela T1 estática por direção, com **o mesmo texto e os mesmos números** (só o visual
muda), números vindos de uma rodada do motor sobre cenário sintético, tokens em
`docs/marca/tokens/` e contraste verificado por teste no CI. O controle D precisa ser uma
ostentação **competente**, no nível do mercado; uma caricatura tornaria a H2 trivial.

> **27/09/2026 — estímulos feitos; a pendência fica aberta até ele aprovar.** Direções E, C e D
> (resposta 16b), cada uma em `docs/marca/direcoes/<direção>.html` com os estados normal e
> PARCIAL, PNG 390×844 em `docs/marca/direcoes/png/`. Números do motor sobre cenário sintético
> (`python tools/conteudo_estimulo.py`, `conteudo.yaml`); tokens em
> `docs/marca/tokens/direcoes.yaml`, 44 pares, nenhum abaixo do limiar
> (`auditoria/test_contraste_tokens.py`, com a execução vermelha registrada no PR); o
> conteúdo idêntico, as cores só do YAML, nenhum recurso remoto e o formato do real guardados
> por `auditoria/test_direcoes_marca.py`. **O que ele revisa:** se o D é ostentação
> competente (critério: parece cartão ou private premium de mercado, não paródia) e se as
> três se distinguem à primeira vista.
>
> **Diferenças em relação ao pré-registro de 20/09, para o texto final da P-162:** (1) o D
> ficou **sem a imagem de estilo de vida**, porque a S3 proibiu foto; (2) a "linguagem leve" da
> C não entrou, porque o texto é idêntico nas três; (3) o estado normal mostra o custo da
> compra como se a tarifa da B3 fosse `COMPLETO`, o que é contrafactual de propósito, para a
> H3; (4) a "data de referência" é o dia da rodada, porque o motor não emite o mês de
> referência (F0).
>
> **Perguntas para ele, que o teste precisa antes de rodar (nenhuma foi decidida aqui):**
> - **Ordem de apresentação:** cada pessoa vê as três direções em ordem aleatória, ou em
>   ordem balanceada (quadrado latino, 3 ordens × igual número de pessoas)? A balanceada
>   controla melhor o efeito de ordem com amostra pequena; a aleatória é mais simples.
> - **Tamanho de amostra:** quantas pessoas, e com que critério? Sem esse número, a regra 17a
>   (bootstrap pareado) pode dar "empate" só por falta de gente.
> - **Estímulo como imagem fixa ou como página:** as fontes são as do sistema, e cada aparelho
>   mostra outra tipografia (Didot e Iowan no iPhone; Roboto e Noto Serif no Android; DejaVu
>   no PNG daqui). Mostrar a página ao vivo põe o aparelho de cada pessoa no meio da
>   comparação. **Recomendação: imagem fixa**, renderizada uma vez com fontes livres (OFL)
>   embutidas, para todos verem a mesma coisa; os PNG de hoje servem para layout e cor, não
>   para tipografia.
> - **H3 no desenho 17a:** ver a mesma direção com e sem a faixa é uma tela a mais por direção
>   (seis no total). Vale para as três direções ou só para a vencedora?
>
> **27/09/2026, S4 — as quatro perguntas foram respondidas (g-B, h-A, i-A, j-A; fila), e os
> estímulos refeitos.** Rótulo genérico no lugar do ticker (l-B), nenhum estado
> contrafactual (selo `PARCIAL` nas duas versões, que é o status do insumo), as versões
> **base** e **com rota bloqueada** (j-A: a primeira rota que o motor elimina, pela ordem
> dos portões), a C em magenta (m-B), a D com a ilustração provisória (k-A, P-168) e as
> fontes OFL embutidas (i-A). Os seis PNG, com sha256, estão em
> `docs/marca/direcoes/README.md`. **Continua aberta até ele aprovar esses seis PNG**; a
> aprovação vai para a fila e é pré-condição da S5.

**FECHADA em 27/09/2026.** Os estímulos das direções E, C e D (resposta 16b), nas versões base e com rota bloqueada (j-A), foram refeitos na S4 com as respostas g-B a p-A (PR #38, commit `2625cc7`) e **aprovados por ele** em 27/09/2026 (`docs/decisoes/fila-do-osvaldo.md`, "Aprovação dele, 27/09/2026: os seis PNG da S4"), com o sha256 de cada um dos seis PNG gravado ao lado. Guardas: `auditoria/test_contraste_tokens.py` e `auditoria/test_direcoes_marca.py`, cada uma provada por mutação. O que segue: o pré-registro final (P-162, S5), que congela esses seis sha256. A ilustração da D continua provisória (P-168).

## ~~P-165~~ · Onde o motor roda para o usuário: a resposta "servidor" contra a P-157 — **FECHADA em 03/10/2026**

**Dono:** Osvaldo · **Gatilho:** antes do mapa v2 (etapa 4) · **Classe:**
`DECISAO_DE_DESENHO`

Em 26/09 ele respondeu "servidor". Isso colide com a P-157 ("o dado fica no aparelho") e
com o mapa (O1 e §5). As três vias estão no bloco 18 da fila: no aparelho; servidor com
banco de dados; **servidor sem estado** (calcula e devolve sem gravar). Não afeta a v1,
que é sintética. Com servidor, entram na conta a LGPD (quem guarda o quê, por quanto
tempo), o custo fixo e a autenticação (WCAG 3.3.8).

**FECHADA em 03/10/2026.** Decisão dele pelo formulário do Projeto no claude.ai: **B′, servidor
sem estado** (A e B recusadas). O desenho, o porquê e as três consequências estão em
[`docs/decisoes/P-165-onde-o-motor-roda.md`](../decisoes/P-165-onde-o-motor-roda.md); a resposta, no
bloco 18 da [fila](../decisoes/fila-do-osvaldo.md). A P-157 fica de pé. A consequência (b) virou
a P-175; a (a) é da P-158 e a (c) é da leitura do item 20.

## ~~P-115~~ · O critério do degrau precisa ser re-pré-registrado antes da próxima janela — **FECHADA em 03/10/2026**

**Dono:** Osvaldo decide · **Gatilho:** antes de medir qualquer janela nova (2016–2020, ou o
acervo inteiro) · **Classe:** `DECISAO_DE_DESENHO`

O critério do C-02 reprovou em 4 de 5 anos (`docs/auditoria/C02-JANELA-2021-2025.md`) e o nulo
estava errado: o dia ex ajustado tem o retorno do mercado, e o dividendo tira do preço 1,16×
o que paga. O critério corrigido — dias **limpos**, **descontado o mercado** do dia, razão
queda/provento **por tipo** — foi desenhado **depois** de ver 2021–2025, então só vale como
pré-registro para dado que ainda não foi medido.

**E só vale se for commitado e empurrado ANTES de rodar sobre 2016–2020.** Commit local não
basta: o que torna o "antes" verificável (P4) é o histórico **público** datado — o verificador
externo do laudo `docs/auditoria/PREREGISTRO-EVIDENCIA.md`. Sem o push anterior à corrida, o
critério corrigido repete o defeito da P-116.

> **Decisão dele, 26/09/2026: `115a`** (recomendada) — empurrar o critério corrigido do degrau como pré-registro antes de medir 2016–2020. O Claude Code redige; ele responde "pode empurrar" antes de qualquer medição. Registro em `docs/decisoes/fila-do-osvaldo.md`.

> **26/09/2026, revisão 4 (no rascunho do PR #27, §9):** "pode empurrar" dado, com merge
> condicionado. **Antes do merge, a janela é escolhida pelo n de JCPs, sem ler preço.** As
> candidatas são 2016–2020, 2015–2020, 2014–2020 e 2013–2020. Vale a menor com
> **n_JCP ≥ 1.648**; se nenhuma atender, fica 2016–2020 com o `NAO_CONFIRMADO` provável
> declarado. Quem conta é o `auditoria/c02_contar_n.py` (só no branch do #27 até o merge),
> que lê do silver só `cod`, `type_stock`, `tipo` e as duas datas. **A ordem da sessão local:**
> 1. silver com calendário desde **2013-01-01**;
> 2. contar;
> 3. gravar contagem, janela e sha256 num commit só;
> 4. sortear e empurrar o D1;
> 5. merge.
>
> ~~**Aberta, e decidir antes de segunda:** o n do silver é teto do n do K2. A calibração pela
> razão de 2021–2025 está na fila (`n-a` ou `n-b`).~~ **Decidida em 26/09: `n-c`.** O n passa a
> ser a unidade dos 819, medida por presença no COTAHIST e sem preço. A calibração é condição:
> sobre 2021–2025 tem de dar 819, senão o script para e mostra a diferença. E há quarentena do
> retorno do dia ex em 2013–2020 até o merge. Texto na §9 do #27 (`d7811fd`); decisão em
> `docs/decisoes/fila-do-osvaldo.md`. **Na segunda**, se a calibração parar, a janela não cresce,
> e a diferença vai para ele antes de qualquer outro passo. **27/09, tolerância de 2% só para
> cima:** 819 segue; de 820 a 835 segue, com o n × 819 ÷ n_cal arredondado para baixo; fora
> disso, para (§9 do #27, `239acf1`).
>
> **02/10/2026, sessão local — a contagem deu `PARADO`.** A calibração em 2021–2025 contou
> **807**, quando a faixa aceita vai de 819 a 835: diferença de **−12**, abaixo da faixa. A
> §9 do #27 diz que contar a menos é sinal de unidade errada. Pelo passo 3, nada se gravou
> além da diferença:
> - sem janela escolhida;
> - sem sha256 na §2;
> - sem D1 sorteado.
>
> **Nenhum preço de 2013–2020 foi aberto.** O silver
> (`eventos_silver_2026-09-11_cal-19860102-20260918.csv`, sha256 `ec6b50da…98143`, igual em
> duas gerações) e os COTAHIST de 2013 a 2025, conferidos contra os pinos, estão na §9.
>
> **Em aberto:** o −12 é do contador ou da referência? Os 819 foram medidos em setembro, com o
> silver e o código de então. Separar os dois exige rodar o `ajustar.medir` em 2021–2025 com
> este silver; isso lê preço só de 2021–2025, fora da quarentena.
>
> **03/10/2026 — o −12 é da referência** (§9 do pré-registro): o `ajustar.medir` de hoje dá
> **807** em 2021–2025; os 819 de setembro não valem mais. Revisão 5: calibração 807, σ 0,0482,
> limiar **1.693** (`2638de1`). A contagem deu 2016–2020 = **555**, nenhuma candidata atende, e a
> janela é **2016–2020** com o `NAO_CONFIRMADO` provável do K2 declarado (`60a40f2`). O D1 está
> sorteado e empurrado (`73ee120`, semente 20260927, 30 posições). Esses quatro commits saíram
> em Sonnet; a auditoria do claude.ai em Opus conferiu constantes, ordem e semente, sem
> reexecutar (`eventos.csv`). **Limitação declarada (§9):** o 0,0482 é σ por ponto; o K2 é
> julgado pela §3.1 (por pregão, semente 20260926). A janela só seria outra com o σ por pregão
> de 2021–2025 entre 0,0276 e 0,0342, e ele não foi medido. **Próximo passo do D1:** a
> transcrição dos documentos (§3.1, passo 2), antes da corrida.
>
> **03/10/2026 — D1 transcrito: `PASSA`** (`docs/fontes/jcp-amostra-2016-2020.md`). As posições
> 1 a 10 têm documento no RAD e as 10 são `BRUTO`; nenhuma foi pulada. As posições 5 (GGBR3) e
> 10 (TOTS3) não rotulavam o valor: depois da escada, a decisão dele virou a **emenda E-D1a**
> ("sujeito a retenção de IR" = bruto; o 20-F em HTML vale como prova), empurrada antes da
> classificação (`95042ca`). A emenda veio depois de abrir os documentos, e isso está declarado
> na §3.1, com o que cada saída daria: só a leitura estrita leva a `NAO_CONFIRMADO`. O RAD corta downloads (`curl: (18)`); a guarda de
> integridade reprova as 5 cópias cortadas, e as 10 provas repetiram o sha256 em duas rodadas.
> **Aberto:** os PDFs no armazém (§3.1), que a nuvem não alcança: sessão local, em "Ao voltar
> ao desktop".
>
> **03/10/2026 — o script da corrida existe** (`auditoria/c02_corrida.py`, §3.1 passo 3). Antes
> dele, a decisão dele virou a **emenda E-K** (§4.4): o texto literal da §4.1 fazia o K6 falhar
> por construção. O script:
> - recalcula o D1 da transcrição;
> - grava o sha256 do silver e de cada COTAHIST;
> - **recusa ler preço de 2013–2020 se o commit não estiver no `origin`** (P7).
>
> 43 testes com dado sintético; 22 mutações reintroduzidas, 22 pegas. Não rodou sobre dado real.
> **Próximo passo:** ⚙ **exige o desktop.** A sessão local roda
> `py -3.11 auditoria/c02_corrida.py <silver>` sobre o silver da §2 (sha256 `ec6b50da…98143`),
> depois do merge, e commita o JSON do resultado.

**FECHADA em 03/10/2026.** Decisão dele no claude.ai: **opção A**, fechar com o C-02 como saiu.
A corrida de 2016–2020 deu **`NAO_CONFIRMADA`**. K2 (JCP) e K3 (dividendo) ficaram
`NAO_CONFIRMADO` por σ̂ acima do σ_max. K1, K5, a completude e o K6 deram `PASSA`, e não houve
nenhum `REPROVA`. **Evidência:**
- o PR **#57**, mergeado em `c4fec69`;
- o commit do resultado, **`b331172`**, rodado sobre `506678e`;
- o JSON `docs/auditoria/C02-JANELA-2016-2020-resultado.json`, com sha256 do blob
  **`73e43fba73cd07dc38e16415772d670a9d887674fc93dec6aba699bb5487defd`**.

O resultado, a decisão e a hipótese exploratória do JCP líquido (marcada como não resultado)
estão na §7 do pré-registro. O teste `xfail(strict=True)` da §7 é o
`auditoria/test_c02_janela_2016_2020.py`. A falta de poder é o achado **PO-01**. Ficaram
abertas a **P-176** (o padrão 1, 2, 3, 4, 5 no K5 e na completude) e a **P-177** (a corrida
não recusa insumo com sha256 diferente). Os PDFs do D1 no armazém seguem como item 11 de
"Ao voltar ao desktop": não bloqueavam a corrida e não bloqueiam o fechamento.

## Fechadas

| # | o que era | fechada em |
|---|---|---|
| **P-115** | o critério do degrau re-pré-registrado antes da próxima janela (C-02 v2) | 03/10 — opção A: `NAO_CONFIRMADA` em 2016–2020 como saiu (#57, `b331172`); PO-01, P-176, P-177 |
| **P-165** | onde o motor roda para o usuário | 03/10 — B′, servidor sem estado; consequências na P-175 |
| **P-163** | as direções visuais como estímulo, a T1 em cada direção | 27/09 — S4 (PR #38) aprovada por ele; seis PNG com sha256 na fila |
| **P-155** | ler a WCAG na fonte: contraste, alvo de toque e daltonismo (era P-WCAG) | 27/09 — WCAG 2.2 transcrita; RI-22 a RI-34 com verificação |
| **P-147** | a captura do NEFIN não tinha rodado no executor | 27/09 — execução agendada `36246158435`, passo `captura_nefin` verde |
| **P-159** | ler a Resolução CVM 19/2021 e confirmar ou retirar a tese de independência | 26/09 — duas teses confirmadas com escopo, uma retirada |
| **P-01** | assinar os dois registros (HASH11 e Tesouro IPCA+) | 26/09 — hash11 ea8c8769bbf021e2, td_ipca 942c75bae248327b; td_ipca sem peso até a compra |
| **P-152** | G8 tem de honrar REGRA_DECIDIDA (G-07) | 26/09 — G8 lê o estado; td_ipca 15% → 0% assinado em REGRA_DECIDIDA |
| **P-117** | o silver tinha dois arquivos para a mesma captura e quem escolhia era o sorted() | 26/09 — 117a: nome com captura e calendário; escolha por regra, empate levanta |
| **P-12** | DATADO cobrava liquidez onde deveria cobrar vencimento (H-01) | 26/09 — 12a: vencimento casado via campo novo `vencimento_anos`; política 1.33.0 |
| **P-81** | o chaves_orfas.py não separava decisão registrada de parâmetro órfão | 26/09 — 81a: `_registros` no YAML, lido pelo instrumento |
| **P-84** | a corretagem de ETF no ranking de corretoras | 26/09 — 84a: já implementada em 16/09 (pior caso ação × ETF); pendência estava desatualizada |
| **P-124** | custódia do Tesouro mensal no motor e semestral na B3 | 26/09 — 124a: fica mensal, como escolha declarada (política 1.33.0) |
| **P-151** | o semanal ficava vermelho por branch de sessão aberta (GIT-01 no CI) | 26/09 — a guarda pula no CI; o controle que roda no CI prova que fora dele ela reprova |
| **P-118** | `politica.yaml` citava a P-96 como aberta | 23/09 — fechada no corpo; cabeçalho riscado em 26/09 |
| **P-45** | migrar o trabalho de repositório para o Claude Code | 26/09 — vencida: 16/09 — em uso desde então (`CLAUDE.md`, rodada de 16/09) |
| **P-02** | aporte realizado era zero | 26/09 — vencida: 10/09 — primeiro depósito; classificado como aporte (U-02) |
| **P-04** | `b3.quem_paga_custodia` não bloqueava nada | 26/09 — vencida: F-05 — o bloqueio foi nomeado no `custos.yaml` |
| **P-47** | eventos societários da B3 não existiam no plano | 26/09 — vencida: 11/09 — 74/74 emissoras, silver e série ajustada; a rotina que falta é a P-150 |
| **P-49** | `coletar_b3.py` nunca tinha tocado a rede | 26/09 — vencida: 11–12/09 — rodou; 74/74 (A-00 a A-04, B-03) |
| **P-54** | a rotina semanal da CVM não existia | 26/09 — vencida: 25/09 — superada pela captura diária da P-57 |
| **P-62** | repositório público, com `estado.yaml` fora | 26/09 — vencida: 18/09 — público; `estado.yaml` fora e guardado por `test_p67_segredo.py` |
| **P-68** | o primeiro aporte estava livre ou empenhado? | 26/09 — vencida: 12/09 — quanto sai medido; a classificação é dele (U-02). Cabeçalho corrigido em 26/09 |
| **P-75** | numpy e pandas divergiam dos pinos | 26/09 — vencida: 12/09 — pinos instalados; `ambiente.py` igual ao registrado |
| **P-73** | a máquina rodava Python 3.13 | 26/09 — vencida: 12/09 — 3.11.9; `ambiente.py` igual ao registrado |
| **P-76** | a F-03 se declarou refutada com insumo `PARCIAL` | 26/09 — vencida: 13/09 — o status de uma conclusão é medição de sensibilidade, não herança |
| **P-80** | a rotina media um terço do projeto | 26/09 — vencida: 25/09 — o CI roda as quatro suítes e o lint em todo push; `testpaths` intocado |
| **P-78** | oito campos de `Instituicao` coletados e nunca lidos | 26/09 — vencida: 13/09 — três naturezas; o que sobra é a P-84 |
| **P-87** | segunda cópia do projeto na máquina | 26/09 — vencida: 18/09 — apagada por ele |
| **P-92** | o acervo tinha um ano de preço | 26/09 — vencida: 18/09 — 41 anos; no armazém desde 24/09 |
| **P-107** | o pré-registro de ML herdou `L = 3` e não tinha teste de poder | 26/09 — vencida: 23/09 — máximo entre L ∈ {1,2,3} e o nono teste, no v1 e no v2 |
| **P-149** | `cenarios.py` caía no `main` (`fora_status` virou lista de rotas) | 25/09 — lê rota nua; `test_cenarios.py` roda o script |
| **P-134** | custo de entrada maior que o aporte virava `min()` calado | 25/09 — `AporteConsumidoPelaEntrada`; não era inerte (aporte da rota e proposta); achado B-19 (aporte R$ 0 → NaN) |
| **P-57** | a captura da CVM dependia de alguém lembrar (W-01) | 25/09 — execução agendada `36148547193` verde; regime em `politica.yaml → regimes_de_captura.cvm`; limitação `RESOLVIDA` |
| **P-135** | o COTAHIST não era capturado na nuvem | 25/09 — mesma execução, passo `captura_b3`; `regimes_de_captura.b3`; limitação `RESOLVIDA`. Conciliação segue na P-137 |
| **P-148** | o Dependabot proporia `numpy` e `pandas` toda semana, e aceitar muda o número pré-registrado (P-15) | 25/09 — **decisão dele, opção (b):** `ignore` das duas no `.github/dependabot.yml`, derivado de `pyproject → tool.meol.dependencias.numericas`; `test_P148_…` reprova divergência nos dois sentidos (mutação: sem o `pandas`, reprova). Saída escrita no arquivo: pré-registro ML executado ou aviso de segurança. Os PRs `numpy-2.4.6` e `pandas-3.0.6` fecham |
| **P-143** | sem ponte ticker ↔ `CD_CVM` antes de 2018, o universo do ML e o mês da emenda 1 não se mediam (CV-05) | 25/09 — banco de ISIN da B3 (achado no JS da página) + ponte manual de 42 emissores conferida à mão (CV-06). **Mês da emenda: mar/2011**, 95,8%, igual nas duas janelas. Resto na P-145 |
| **P-140** | o pré-registro ML só fixava 2026; os outros anos saíam da versão vigente, sem pin | 25/09 — **2004–2025** fixados pela impressão de conteúdo (2004 derivado da janela de 60 meses do §5.1, com teste). Impressão = pino principal; sha256 = observado. Mesma impressão com sha diferente → aviso e segue; impressão diferente → `InsumoBloqueado`. 23/23 conferem nesta máquina em 53,7 s |
| **P-142** | 9 testes do C-02 contra o acervo real pulavam em toda rodada: raiz em `data/bronze/b3`, e o COTAHIST em `.../cotahist` desde a P-114 | 25/09 — raiz certa com `anos={2023}`; **os 9 passaram sem mudar número**. `exigir_acervo`: sem `data/` pula, com `data/` e arquivo faltando falha; guarda reprova `skipif` em arquivo com `test_REAL_*` |
| **P-132** | o pré-registro v2 promete fundamento desde jan/2010, e o primeiro `DT_RECEB` é 27/01/2011 (CV-04) | 25/09 — **decisão dele, opção (a):** emenda 1 (início do desenvolvimento = primeiro mês com ≥ 90% do universo coberto), empurrada em `00aa622` antes de medir. O FCA passou a ser capturado (17 anos, 6,6 MB). O mês **não** foi medido: o FCA não tem ticker antes de 2018 (CV-05) → **P-143**; a P-138 não enxerga emenda de desenho → **P-144** |
| **P-141** | o pytest foi **58% do tempo** dos pedidos de 21–24/09 (268 de 458 min; `tools/analisar_sessoes.py`); o `fase0` sequencial media **537 s**, a 63 s do teto de 10 min do Bash, e 3 rodadas morreram nele sem resultado | 25/09 — **medido antes e depois, mesma máquina:** completa sequencial **34 + 538 + 35 = 607 s** → completa `-n auto --dist loadgroup` **11 + 103 + 21 + 3 (tools) = 138 s**; ciclo `-m "not slow"` **30 + 7 + 8 + 1 = 46 s**. Memo de sessão por sha256 (`fase0/memo_acervo.py`): os dois pares que liam o mesmo acervo, **338 → 202 s** sequenciais (o segundo de cada par: 95 → 1,2 s e 64 → 1,1 s). Fixtures de módulo (`med`, `jan`, `real`) em `xdist_group`, senão cada trabalhador refaz 45–62 s. `pytest-xdist==3.8.0` no grupo **`paralelo`, não no `dev`**: o `dev` entra na impressão `7565df…` gravada em 4 resultados (`test_p141_paralelo.py`, com mutação). Único teste com caminho fixo (`_pyproject_frouxo.toml`) foi para `tmp_path`. 3 guardas novas, as 3 reprovam por mutação. Protocolo na §9 do `CLAUDE.md`. **Achado lateral: P-142** |
| **P-43** | um terceiro catálogo (`motor.montar_rotas`) e uma segunda simulação (`motor.simular`) só chamados por testes, divergindo até 17,4% da de produção (B-16) | 24/09 — **apagados** (decisão técnica delegada). Antes: `simular_custo` passou a ler `custodia_rv_interpretacao` (B-17), K-06 e K-07 da Vest trazidos para o `test_alocacao`. Instantâneo dourado idêntico. Retratação da recomendação *"migrar e confrontar"* na própria P-43 |
| **Limpeza CVM** | acervo com 4 `(1).zip` duplicados, 2 `(1).zip` que eram a **única** cópia da versão de 13/09 de 2024, 6 pastas extraídas e uma página da B3 salva por engano em `itr/` | 24/09 — **aprovado por ele.** `capturar_cvm.py --arrumar limpeza`: 4 duplicatas apagadas (sha256 idêntico), os 2 de 2024 viraram `_snapshots/*__v20260913__*`, as 6 pastas saíram depois de todo CSV bater em CRC-32 e tamanho com um membro (cada uma é inteira igual a um ZIP que fica; as de 2024 à versão `v20260830`), e a página foi apagada à mão. Manifesto: 49 → **45 arquivos**, 918 → 849 MB. **Tropeço no caminho, meu:** na primeira aplicação o Windows negou o `rmdir` de pasta `ReadOnly` depois de o `rmtree` apagar os 18 CSVs de `dfp_2012`. O `\| tail` escondeu o código de saída, e a cadeia `&&` seguiu até o manifesto. Conserto: `_tirar_somente_leitura` no `rmtree`, com teste que reprova sem ele |
| **P-139** | o pré-registro v2 fixava `fb3546ed…` e nenhum leitor conferia: o acervo marcava `4f2cf2aa…` como vigente, e o ML leria uma versão diferente conforme a máquina (CH-01) | 24/09 — `fase0/insumo_ml.py` abre a versão fixada e confere a impressão de conteúdo da janela; pin em `docs/aprendizado/preregistro-ml-v2.pins.yaml`, amarrado ao `.md` por teste. Arquivo real: `2026 FIXADO`. 11 testes, 2 mutações reprovadas. Abriu a **P-140** |
| **P-138** | o contador de variantes do pré-registro era desenhado como **alarme** (exige justificativa, não trava), mais brando que a decisão 4, e a resposta dele ao item 6 de 13/09 não estava registrada | 24/09 — **decisão dele: bloqueio; a única saída é emenda empurrada ao repositório.** `preregistro.conferir_orcamento` antes da decisão 4; emenda conferida por conteúdo contra `origin/main`; emenda entra no `m_orcado`. 20 testes, os de bloqueio reprovam por mutação. Inerte hoje (13/2) |
| **P-131** | `JA_CORRETO` saía de `plano()` antes de `conferir()` — nome certo lido como conteúdo certo, e foi assim que a P-126 contou *"24 já corretas"* e a P-120 escreveu *"cada uma conferida por CRC-32"* | 24/09 — `JA_CORRETO` passa por `conferir()` e sai `RECUSADO` se falhar; teste com cópia de nome certo e conteúdo truncado **reprova contra a versão anterior**. Retratações na P-120 e na P-126, sem apagar |
| **P-120** | o manifesto só via `*.zip` e 41 cópias extraídas (5,99 GB, 88% dos bytes) estavam no acervo sem sha256 | 24/09 — **decisão dele: apagar.** 41 conferidas uma a uma por `conferir()` (cabeçalho, tamanho, CRC-32) e apagadas; `pregoes()` idêntico (2023 248 `e4a9d81d…`, total 10.059 `2700aca0…`, `arquivos()` 41 `7469fb94…`). O manifesto conta o que sobrar sem hash (`extracoes_soltas`, 7 testes, 4 mutações): **41 arquivos, todos com origem, contagem 0**. Abriu a **P-131** |
| **P-125** | `conferir_cabecalho` devolvia `'.202'` como ano — fatia `[10:14]` pegando o ponto de `COTAHIST.`; ninguém lia o retorno | 23/09 — `[11:15]`; `fase0/test_p125_ano_do_cabecalho.py`, **6 de 6 reprovam por mutação** (fatia antiga reintroduzida). Achado lateral: as posições do header moram em Python (P-130) |
| **P-126** | cópias extraídas com três convenções de nome e uma pasta com nome de ano | 23/09 — `fase0/nomear_extracoes.py`: 17 renomeadas, 24 já corretas, 0 recusadas; instantâneo de `pregoes()` idêntico (2023 em 248 `e4a9d81d…`). **Não decide a P-120**. ⚠ **Retratado em 24/09:** as *"24 já corretas"* tinham o **nome** certo e **não foram conferidas** — só as 17 renomeadas passaram por `conferir()`; as 41 foram conferidas em 24/09, antes de apagar (P-131) |
| **P-100** | o `COTAHIST_A2026.ZIP` de 18/09 chegou truncado (38.328.935 bytes, sem diretório central), e eu **declarei 2026 indisponível** em vez de pedir outro download — o período da família ML foi cortado em dez/2025 por isso | 23/09 — rebaixado por ele em 21/09 11:59, **íntegro**: 85.779.964 bytes, `fb3546ed27cc…`, trailer `TOTREG` 2.871.743 = registros `01` contados, **179 pregões de 02/01 a 18/09/2026**. Duas medições independentes concordam. `origem.csv` e manifesto atualizados. **Retratação** no `CLAUDE.md`: o arquivo foi descartado em vez de consertado — nasce a §5-B.16 |
| **P-114** | a raiz padrão do `refinar.py` e do `ajustar.py` era `data/bronze/b3`, e `calendario.arquivos()` não é recursivo: os 41 anos moram em `cotahist/` e o padrão enxergava **um** — o avulso de 04/09. O relatório dizia `acervo COTAHIST_A2023` e ninguém perguntava | 23/09 — **decisão dele**: a raiz vira `data/bronze/b3/cotahist`. No `refinar.py` isso exigiu **separar dois parâmetros** (`--raiz` de eventos, `--cotahist` do calendário), porque um servia aos dois acervos. Calendário de 248 → **10.059 pregões**; `data_ex` derivada de 383 → **9.271**. Instantâneo dourado fecha nos três níveis: 2023 em 248 pregões `e4a9d81d…`, silver com **0 colunas alteradas** e **0 data ex perdidas**, e os dois CSVs de 2023 byte a byte idênticos. 8 testes, 4 reprovam contra a versão anterior |
| **P-97** | o `COTAHIST_A2023.ZIP` de 04/09 estava no acervo **sem origem**, e o manifesto contava `1 de 42` | 23/09 — **decisão dele**: é duplicata, sai do acervo. Medido **antes** de mover: ZIP e TXT extraído são byte a byte idênticos aos de `cotahist/`, que **têm** origem declarada. Movido para `data/quarentena/` com `LEIA.md`, não apagado. Manifesto: **`P-06: os 41 arquivos tem origem declarada`**. Guarda na suíte, porque manifesto é comando que alguém roda (P7) |
| **P-113** | 173 proventos sem `closingPricePriorExDate` deixavam 78 séries `INCOMPLETO`; a decisão era se o COTAHIST pode substituir a fonte | 23/09 — **decisão dele**: pode, com coluna de origem e a B3 ganhando. **Primeiro pré-registro do projeto com impressão digital** (critérios empurrados em `9a08a55` antes da corrida, P-116) — e **quatro dos sete critérios reprovaram**. 11 fatores novos em vez de 172; `INCOMPLETO` 78 → 74; degraus 1.586 → 1.593; 2023 inalterado. `docs/auditoria/P113-MEDIDO.md`, 17 testes |
| **A-13** | os 161 restantes não eram fator faltando: eram **o mesmo pagamento chegando pelas duas esteiras** da B3, que `_chave_de_evento` não colapsa porque `origem` entra nela de propósito (A-09). A cópia do suplemento era inerte só por não ter preço — dar preço a ela subtrairia o provento **duas vezes** | 23/09 — `_provento()` identifica o **pagamento**, sem a porta de entrada. Provado pelo resíduo de 2025: **t +0,39 colapsando, +6,31 sem**. E a armadilha registrada: **o agregado melhorava enquanto o ano quebrava**, então o critério R3 pré-registrado teria aprovado a versão errada. Quem pegou foi a coluna de procedência |
| **A-12** | `_chave_de_evento` montava a identidade do evento com `data_ex`, que é **derivado** e estava vazio em 8.889 das 9.272 linhas — e **128 eventos reais** colapsavam como "duplicata exata" | 23/09 — chave passa a usar `ultimo_dia_com_direito`, o campo **observado**, preenchido em 9.272 de 9.272. Contagem: 334 → **206**, e 206 **nos dois silvers** — deixa de depender do calendário. Achado só apareceu porque a P-114 moveu o número; com o calendário largo a chave antiga também daria 206 e o defeito **se auto-encobriria**. 8 testes |
| PLANO passo 3 | a série ajustada cobria só 2023, com duas bordas, e o C-01 tinha **um** caso de preço | 21/09 — `ajustar.py --anos 2021-2025` + `fase0/test_ajustar_janela.py`. Controle fecha nos cinco anos (632.384 pares, pior 1e-27); **C-01 com 54 eventos de quantidade**, 49 encolhem, os dois primeiros grupamentos com preço (MGLU3 +896% → −0,38%; HAPV3 +1378% → −1,46%); as duas bordas de 2023 fecharam. O critério por ano **reprovou em 4 de 5** e fica em `xfail` estrito (P-115). Achados A-10 e A-11. Ver `docs/auditoria/C02-JANELA-2021-2025.md` |
| C-01, a corroboração de preço | a regra do `factor` tinha sido fechada pela **distribuição**, com UM caso de preço, e a data ex derivada também tinha UM. A série de preços ajustada não existia | 18/09 — `fase0/ajustar.py` + `fase0/test_ajustar.py` (32 testes, 8 contra o acervo). **O degrau do dia ex cai de −1,6263% (t = −9,88) para −0,0360% (t = −0,29) em 293 datas-ex**, com controle em 86.736 pares de pregões sem evento (pior divergência 1e-27, arredondamento de `Decimal`). Duas mutações presas na suíte: data ex deslocada deixa o degrau **inteiro** e cria um **falso** na véspera (+1,91%, t = +11,20); fator invertido **dobra** o degrau (−3,16%). Ver `docs/auditoria/C02-O-DEGRAU-MEDIDO.md` |
| — | `calendario.py` era o único leitor de COTAHIST; o segundo (`ajustar.py`) ia redigitar a descoberta de arquivo e a posição da data | 18/09 — extraídos `arquivos()`, `registros()` e `data_de()`. Um fato, um dono. Instantâneo dourado de `pregoes()` antes e depois: **248 pregões, `sha256 e4a9d81d…` idêntico** |
| manifesto da CVM | gravado em `data/bronze/cvm/manifesto/` — dentro do caminho que o `.gitignore` ignora na linha 12. **Não entrou no commit `64a5c97`**, e o `CVM-PRIMEIRO-RETRATO.md` afirmava que entrava | 18/09 — destino padrão passou a ser `docs/acervo/cvm/`, achado pela raiz do repositório; `gravar()` **recusa** qualquer caminho sob `data/`. 3 testes, um provado por mutação. Encontrado lendo a lista de `create mode` do commit dele e não achando o manifesto lá |
| P-87 | uma segunda cópia do projeto na máquina, no OneDrive, com `.git` próprio parado em 09/09 — e foi a pasta que a sessão de nuvem recebeu conectada | 18/09 — **apagada por ele.** `Desktop\Bastter` é o caminho único |
| passo 1 do `PLANO.md` | CVM não baixada — o bloqueio de que os outros três marcos dependiam | 18/09 — **33 ZIPs**, DFP 2010–2026 e ITR 2011–2026, em `data\bronze\cvm\`. Acervo completo, cauda congelada incluída. Falta o manifesto (`fase0/manifesto_cvm.py --manifesto`), e sem ele o acervo é um conjunto de arquivos, não um retrato datado |
| decisão 2 de 13/09 | o corte do backtest era **1,96 por omissão** — e 1,96 é a NORMAL, num teste com 301 graus de liberdade | 18/09 — `alocacao/multiplicidade.py`: t de Student implementada em casa (sem acrescentar scipy, que mudaria a impressão do ambiente e tornaria todo resultado registrado um número novo), Bonferroni, Bonferroni sobre marginal medida e Romano-Wolf com bootstrap **conjunto**. 69 testes, com oráculo externo: tabela publicada de Student, identidade de ida-e-volta, e amostragem pelo numpy |
| decisão 3 de 13/09 | o `m` era afirmado por quem registra, e o `pesquisa_id` era renomeável | 18/09 — `alocacao/preregistro.py`: `m_executado` sai do **diário**, `m_orcado` da **soma** dos `variantes_permitidas`, `pesquisa_id` do sha256 da fonte + regra de amostra. Renomear não reinicia contador; trocar a série levanta `FonteTrocada` |
| decisão 4 de 13/09 | divergência de veredito não tinha regra, e "preservar tudo" viraria "escolha o que preferir" | 18/09 — portão em `preregistro.operativo()`, sobre **vereditos divergentes venham de onde vierem**, não só R1×Rn. Primeiro caso no mesmo dia: o HML diverge entre os dois lados do `m`. Operativo = **orçado**. `leitura` com menos de 120 caracteres não destrava |
| P-29 | `estrategias_pre_registradas` declarada ESPECIFICACAO — escrito e não ligado a nada | 18/09 — reclassificada para **REGISTRO** (67 das suas chaves são testemunho e nunca serão lidas; inventariá-las como dívida seria registrar 67 promessas falsas). O papel de ESPECIFICACAO virou **número**: `m_orcado − m_executado` = **11** testes pré-registrados que nunca foram ao dado, com teste que o prende |
| — | `politica.yaml` sem bump desde 16/09 | 18/09 — **1.19.0 → 1.20.0**, changelog com o corte medido e a retificação do HML |
| — | `ruff` acusava 1 erro em `auditoria/pares_irmaos.py` (E501), fora do portão da P-40 | 18/09 — corrigido; `ruff check alocacao fase0 auditoria` passa limpo. Um passo da **P-80**, que continua aberta (o `testpaths` ainda cobre um terço) |
| P-84 | a decisão dele de 13/09 — custo por operação no ranking — sem implementação | 16/09 — `corretagem_etf_pct` entrou como **segunda parcela** da dimensão `corretagem` (pior caso entre ação e ETF), sem inventar peso. Os outros três são **exibidos e nunca pontuados** (`politica.yaml → corretora.custo_por_operacao`), porque medidos são constantes entre quem os declara. **A tabela do ranking não mudou**, e o motivo está preso num teste: a única casa com ETF ≠ 0 é a XP, cuja dimensão já estava `None` pelo E-08 |
| P-86 | o `chaves_orfas.py` deduplicava por NOME DE FOLHA e escondia **42 de 67** chaves — a segunda ocorrência de um nome sumia do relatório | 16/09 — dedupe por caminho; linha de base recortada por **espécie** (glob + motivo), porque as 42 são nove espécies já declaradas para uma instância. Guarda da guarda com prova por mutação |
| — | `politica.yaml` sem bump de versão desde 11/09 (passo 9 do protocolo, sete commits) | 16/09 — **1.18.0 → 1.19.0**, com o changelog registrando a decisão do custo por operação e a lacuna acumulada |
| P-83 | nove casas com `procedencia: NAO_CONFIRMADO` — cuja própria fonte diz *"custos NÃO OBTIDOS"* — carregavam `corretagem_pct: 0.0` e `corretagem_etf_pct: 0.0`, e o default do dataclass também era `0.0` | 16/09 — 18 zeros viraram `null`, os dois defaults viraram `None`, e `pontuar()` tira a dimensão quando qualquer parcela é desconhecida. **Ranking byte a byte idêntico** (`ee59cd02…`): a correção é inerte hoje, e é esse o ponto — os zeros estavam dormindo até a decisão 1 acordá-los. 3 guardas provadas por mutação |
| P-85 | a saída do `corretoras.py` mudava de TEXTO entre execuções (um `set` impresso sem ordenar) e não servia como instantâneo dourado | 16/09 — ordenado; guarda roda o relatório em subprocesso com `PYTHONHASHSEED` diferente. O `refinar.py` já tinha a lição escrita e ela não atravessou de módulo para módulo |
| C-01 | `factor` dos eventos de quantidade: percentual ou multiplicador? As duas leituras produzem número e diferem por até 50x; 180 das 738 linhas do silver ficavam sem fator | 16/09 — **medido pela DISTRIBUIÇÃO**, não por um caso: os 65 desdobramentos usam 11 valores distintos que, lidos como percentual, caem em cima de razões canônicas (100→2x, 400→5x, 9900→100x). E a regra é **dupla**: no GRUPAMENTO `factor` já é o multiplicador, e é < 1. FACTOR_AMBIGUO 180 → CALCULADO 178 + FACTOR_FORA_DA_REGRA 2 (as incorporações). Instantâneo dourado: nenhuma coluna herdada mudou de valor |
| — | a coluna `data_ex` do silver guardava `lastDatePrior`, que é o **último dia COM direito** — o degrau de preço cai no pregão seguinte, e quem ajustasse por ela deslocaria tudo em um pregão | 16/09 — renomeada para `ultimo_dia_com_direito`; entraram `data_ex` derivada e `data_ex_status`. `fase0/calendario.py` tira o calendário do próprio COTAHIST do acervo (**dia com negociação é pregão**) e **recusa** fora da cobertura em vez de chutar dia útil — Carnaval e feriado estadual não estão em regra genérica nenhuma. Hoje: 1 derivada, 737 `FORA_DA_COBERTURA`; a cobertura cresce sozinha a cada ano de COTAHIST |
| P-82 | `git add -A` levou `pacote_segunda/pacote_segunda/` junto, e o git registrou as deleções como **rename para dentro da cópia** — o repositório passou a guardar uma cópia congelada de si mesmo, com um segundo `CLAUDE.md`, e a suíte continuou verde porque nenhum portão olha para fora de `alocacao/` | 16/09 — cópia removida e `test_p82_copia_do_projeto.py` mede o **índice**, não o disco. A regra já existia no `.gitignore` e era uma lista de nomes de pasta a lembrar; agora é medição |
| A-06 | `desembrulhar` não existia em `coletar_b3.py` — a lógica estava EMBUTIDA em `coletar_eventos`, e `refinar.py` importava um nome que só existia em cópia de teste | 16/09 — extraída, devolve `(dados, n_registros)` (A-07), e `coletar_eventos` a CHAMA. **Instantâneo dourado sobre os 74 arquivos do acervo real: `2127cad3…` idêntico antes e depois.** `pytest fase0` 9 falhas → 0, e `refinar.py` rodou até o fim pela primeira vez: 738 linhas |
| P-79 | três cópias da normalização (embutida, `desembrulhar`, `_normalizar` no teste) | 16/09 — uma só. O teste que comparava o TEXTO DO FONTE das duas primeiras saiu: comparar fonte é o instrumento que sobra quando não dá para comparar comportamento, e não dar era **consequência** da duplicata |
| P-77 | `aliquota_ganho` declarado e nunca lido pelo motor | 16/09 — `regime_tributario` lê; a linha saiu do `INVENTARIO` de `test_campos_mortos.py`, acusada pelo próprio teste do inventário |
| — | `alocacao.py:PONTAS_DIVERGENTES` | 16/09 — **removida**. Constante decorativa que eu criei no P-77 e nunca referenciei; os motivos são frases inteiras. A guarda de campos mortos pegou o meu próprio lixo um commit depois de nascer |
| — | DUAS guardas para o mesmo defeito Y-01/E-09 (`test_y01_yaml_duplicata.py` e `test_chaves_duplicadas.py` + `auditoria/chaves_duplicadas.py`), escritas em paralelo no mesmo fim de semana — o N-01 dentro da própria suíte | 16/09 — **fundidas**. Ficou a que usa `yaml.compose` e já estava no `testpaths`; da outra vieram os três testes que ela não tinha: a prova de que a guarda PEGA, o caso do merge, e o caso concreto do IMAB11. Fechou também a falha do P-15, sem precisar afrouxar o P-15 |
| — | `test_E08b_a_referencia_HERDA_o_relogio` adiantava o relógio escrevendo em `motor.HOJE` — **apoiava-se no defeito que a P-70 removeu** | 16/09 — **o teste estava errado, não o P-70**. Agora troca o `val` que `corretoras` usa por um espião que injeta `hoje`: prova que o aviso saiu POR ALI, não só que alguém avisou |
| — | `tributacao.ir_jcp_fonte` COMPLETO sem `fonte` no nível do nó | 16/09 — `fonte` escrita **e** a guarda `test_toda_constante_tem_procedencia` aprendeu a olhar dentro da série: se ALGUMA faixa declara fonte, todas precisam. Série meio declarada é pior que série não declarada, porque quem lê supõe que a faixa calada herda a de cima — e aqui herdar é o erro, a faixa de 18% vem de uma MP que caducou |
| — | os cinco `*-patch.py` ainda no repositório, 5 violações de ruff | 16/09 — apagados. Remendo de uma vez não é ferramenta; deixá-lo convida a rodá-lo de novo |
| — | `conferir-pacote.ps1` não rodou: política de execução + travessão `—` lido como CP1252, onde `0x94` é aspa tipográfica de fechamento e o parser do PowerShell a trata como delimitador de string | 16/09 — apagado, sem substituto. **O remédio não é um `.ps1` melhor**: `py -3.11` já funciona, não tem política de execução e aceita `encoding` explícito. E, sem zip, o script não tem função. Regra, se algum dia voltar a existir um `.ps1`: **7-bit ASCII, sem exceção** |
| — | linha de base das órfãs apodrecida (10 novas, 2 já resolvidas na lista) | 16/09 — reconferida **na máquina real**, com o porquê ao lado de cada uma; `corretagem_fii` e `exercicio_opcao_pct` saíram porque o código passa a lê-las. Abriu a P-81 |
| — | isenção de FII: 50 ou 100 cotistas | 04/09 — **100**, duas leis independentes |
| — | enumerações ORDEM_EXERC / ESCALA_MOEDA / MOEDA | 04/09 — `OBSERVADO`, 12,8M linhas |
| — | layout do COTAHIST conferido contra dado real | 04/09 — + fechamento ao byte em 05/09 |
| — | custódia interna dos ETF iShares não modelada (F-01) | 04/09 |
| — | rota bloqueada simulava com custo zero (F-02) | 04/09 |
| — | CRLF mudava o sha256 da série do NEFIN (F-04) | 04/09 |
| — | `.md` → constante do `custos.yaml` sem mapa | 05/09 — `MAPA-CONSTANTES.md` |
| 20 | regime de análise para bancos | 05/09 — **especificado**, 5 métricas, só Basileia com piso legal |
| — | LCI/LCA e FII fora do catálogo | 05/09 — viraram rotas, bloqueadas com motivo |
| P-03 | 6 citações apontando para trecho não transcrito | 05/09 — 5 transcritas, 1 corrigida |
| F-05 | `bloqueia` era prosa: nenhuma linha de código o lia | 05/09 — viaja na exceção + 3 testes |
| F-03 | IMAB11 como concorrente do Tesouro IPCA+ | 05/09 — **hipótese caiu**: 0,25% > 0,20%, Tesouro vence em todas as faixas |
| L-01 | escolhas do usuário misturadas com o motor | 05/09 — `perfil.yaml` + 3 testes de fronteira |
| J-03 | troca depósito/limite calculada em 14,5:1 | 05/09 — **refutada**: é 1:1 mais bônus |
| J-02 | reserva é colateral da própria fatura do cartão | 05/09 — registrado; motor já zerava por outro caminho |
| K-03 | isenção do Turbinado parecia gratuita | 05/09 — é paga em gasto no cartão e chave Pix |
| K-01 | Turbinado parecia melhor sem olhar a mensalidade | 05/09 — empate acima do teto: nunca se paga pagando |
| J-01 | reserva contada pela nominal, não pela disponível | 05/09 — `reserva_efetiva`; meses caíram de 1,9 para 0,0 |
| — | `opcoes` excluída por resposta factual | 05/09 — **revertida**, virou P-20 |
| P-16 | bloco C: nível ou tendência | 05/09 — **híbrido**, e admite empresa sem dado |
| P-14 | banco no universo | 05/09 — **construir a fonte do BCB**; banco não sai |
| P-07 | ordem dos portões no código, não no YAML | 05/09 — dado + achado I-01 |
| P-13 | `isento_ir` booleano não expressava o FII | 05/09 — dois campos |
| — | bloco C sem regime de exclusão | 05/09 — **regime especificado**, com a lacuna C-04/C-05 declarada |
| — | schema não sabia expressar "regra decidida, papel não comprado" (G-01) | 05/09 |
| H3 | `tamanho_smb_v1` — prêmio de tamanho no Brasil | 05/09 — **nula sobrevive**, t=0,28, P(rejeitar)=3% |
| P-24 | rota com teto de saldo não modelada | 05/09 — `teto_de_saldo` + G2 devolve composição |
| K-02 | teto do produto ignorado pelo G2 | 05/09 — era pior: prometia retorno sobre dinheiro recusado |
| O-01 | retorno médio no alvo inteiro escondia a isenção do Tesouro | 05/09 — critério virou marginal |
| N-01 | seção `corretora` declarava 3 regras que só o Python decidia | 05/09 — lidas do YAML + 5 testes |
| P-28 | guarda de cobertura media o próprio escopo | 05/09 — 19 seções, 11 módulos, regime declarado |
| P-33 | `aporte_extraordinario.registro` na dívida | 05/09 — **falso positivo**, é prosa |
| P-15 | ambiente de execução não registrado | 05/09 — `pyproject.toml` + `ambiente.py`, 8 testes |
| P-36 | catálogos eram dado de pesquisa dentro de código | 05/09 — 2 YAML, migração com **zero diferenças** |
| Q-01 | insumo bloqueado derrubava o catálogo inteiro | 05/09 — bloqueia a rota, nunca o catálogo |
| Q-02 | `confirmacao` era uma letra para cinco fontes | 05/09 — procedência por grupo, letra derivada |
| P-37 | `alocar()` com 300 linhas | 05/09 — 6 passos, **zero desvio** em 38 cenários |
| R-01 | ordem dos portões só aceitava 18 de 120 valores | 05/09 — contrato `consome`/`produz` declarado |
| P-38 | `deepcopy` por disciplina, não por garantia | 06/09 — `conftest.py` + guarda que nomeia o culpado |
| S-01 | 37% do motor era re-hashear o `custos.yaml` | 06/09 — memoizado por mtime |
| S-02 | cache de arrasto ignorava o `C` recebido | 06/09 — **testes que alteravam custo testavam nada** |
| P-39 | não havia mapa de dependências | 06/09 — `impacto.py`, com os pontos cegos declarados |
| P-40 | sem lint nem type-checker | 06/09 — ruff e mypy em **zero**, com cada dispensa justificada |
| T-01 | linha morta cuja chamada contradizia a docstring | 06/09 — removida; revelou o **terceiro catálogo** |
| — | cofrinho do PicPay fora do catálogo | 05/09 — 2 rotas; a dele entra **sem** LIQUIDEZ |
| P-70 | `HOJE` fixo em `motor.py`, resolvido no import — aviso de expiração mudo desde 02/09 | 11/09 — `val()` recebe `hoje` opcional, resolvido em `dt.date.today()` NO MOMENTO DA CHAMADA; 2 testes injetam data (nunca o relógio real). **Segunda metade, no mesmo dia:** 4 de 43 `expira` estavam ENTRE ASPAS — texto, e `val()` só avisa em `dt.date`. Duas eram `cdi_aa` e `selic_aa`, reconferidas em 05/09 e reescritas com aspas: o mecanismo que o `CLAUDE.md` cita como prova estava mudo para elas. Aspas removidas (mesma data, não é renovação) + `test_P70_toda_expira_e_data_e_nunca_texto` |
| P-71 | `dividas`/`objetivos` voltavam como `dict`, motor espera dataclass | 11/09 — `estado_io.validar()` converte para `Divida`/`Objetivo` na carga; `test_p71_p72_porta_de_entrada.py` é o primeiro teste que passa por `estado_io.carregar()` de verdade. **Segunda metade, no mesmo dia:** a conversão era `classe(**x)` cru e aceitava o que o módulo existe para recusar — `taxa_am: "14,5"` entrava como TEXTO sem problema (e estourava no G1), campo faltando virava `TypeError`, chave errada sumia. E `match_empregador`/`match_verificado`, pedidos pelo `estado.exemplo.yaml`, **nunca eram lidos**. Agora cada registro passa pelo `_num()`, e os dois de match chegam ao `Estado`; 5 testes, todos falhavam antes |
| P-72 | `aporte_mensal <= 0` bloqueava `carregar()`, contradizendo a U-01 | 11/09 — só NEGATIVO bloqueia; zero vira AVISO |
| — | achado lateral: `Estado(**estado_io.carregar()[0])` nunca funcionou — `d` carregava `reserva_empenhada`/`meses_cobertos`, nenhum campo de `Estado` | 11/09 — os dois removidos de `d` (eram campo morto e formula duplicada; a validação de `reserva_empenhada` continua) |
| — | achado lateral: `custo_entrada_fixo_pct` tratava `aporte==0` como custo infinito para toda rota, mesmo as de tarifa zero — zerava o universo e violava `_conferir_invariantes` | 11/09 — `r.corr_fix == 0` agora é custo zero para qualquer aporte; sem mudança para aporte>0 |
| P-69 | `etf.IMAB11` duas vezes no `custos.yaml` — o PyYAML ficava com o placeholder `null` e a entrada de 05/09 estava morta (Y-01) | 11/09 — entradas **fundidas** (valor/fonte de 05/09, base legal e `bloqueia` da outra); `test_y01_yaml_duplicata.py` varre os seis YAML pela árvore de nós. A F-03 foi medida à mão com 0,25%, nunca por `val()` — não foi contaminada. Abriu a P-76 |
| — | guarda de campos mortos do lado Python (auditoria de 10/09: o P-28 protegia só o YAML) | 11/09 — `campos_mortos.py` (AST; referência = `Attribute`, `keyword`, `Name` ou chave de `Dict`, só em produção) + `test_campos_mortos.py` com inventário que não apodrece e os pontos cegos declarados. Achou 10 além dos quatro — P-77 e P-78 |
| — | `Aporte.status_do_variavel` | 11/09 — **removido**. Ninguém o preenchia e ninguém o lia: um status que parece gate e não é. A desconfiança do extraordinário já está no desenho (piso × extraordinário) |
| — | `tese.DIFERIDOS_K` | 11/09 — **removido**. O G-01 nasceu do C02, que depende do juro travado na compra; o K02 não depende de compra. Diferir a tese selaria na impressão um texto vazio |
| — | `estado_io.reserva_empenhada` | 11/09 — **usado**, como conferência: se declarado, tem de bater com `reserva_atual − reserva_disponivel`, no padrão de `reserva_por_rota`. O motor segue usando só `reserva_disponivel` |
| — | `corretora.promocional` (P-32) | 11/09 — **usado**: `regras()` recusa peso ≠ 0, como faz com `reclame_aqui` e `facilidade` |
| B-02 | 3 de 74 emissoras com `totalRecords: 0` na esteira de proventos (ABEV, CURY, KLBN) | 11/09 — **não era truncamento** (o código supunha; a hipótese foi medida e caiu): a tabela de proventos guarda o nome **sem** o sufixo `S/A`. O coletor tenta o nome como veio e, **só depois de um zero**, sem o sufixo; a forma usada vai para o manifesto. As 71 gravadas não foram tocadas; recoletar as 3 é decisão do Osvaldo |
| B-03 | CURY falhou nas duas formas do B-02 | 11/09 — `'CURY S.A.'` → 20: o sufixo não some, é **reescrito** (barra vira ponto). As bases divergem sem regra, então virou **cascata**: como veio → sem sufixo → `S.A.` → `SA`, só avançando depois de zero; a trilha inteira vai para o manifesto. 73 de 74 gravadas; recoletar a CURY é decisão do Osvaldo |

---

## P-102 · ~~Uma guarda acessória derrubou o manifesto~~ **CONSERTADA, falta aplicar**

**Dono:** Osvaldo (aplicar os arquivos) · **Gatilho:** **antes de qualquer outro commit** ·
**Classe:** `BLOQUEIA_O_SISTEMA` · ⚙ **exige o desktop**

Liguei `acervos_sem_regime()` ao `main()` do `manifesto_cvm.py` sem guarda. Em `tmp_path` o
`raiz_do_repositorio` acha o `pyproject.toml` que o próprio teste cria, a política não existe
ali, e o `FileNotFoundError` subiu — derrubando **três testes do `test_manifesto_cvm.py` que
não tinham nada a ver com P7 nenhuma**. Eles foram commitados e **empurrados vermelhos, no
primeiro push da história do repositório** (`3ee5e97`).

**Dois erros meus, e o segundo vale mais:** rodei só o meu teste novo, não a suíte de `fase0`
(passo 5 do §9, *"pytest, o júri"*, pulado na mesma resposta em que citei o protocolo); e uma
guarda **acessória** derrubou o **trabalho principal** — o comando grava o retrato de
procedência, conferir a P7 é um extra que eu pendurei nele.

**A correção fica entre dois extremos:** `PoliticaAusente` **levanta** na função (engolir
seria o E-02 — arquivo ausente virando *"nada declarado"*) e o `main()` **avisa que a
conferência não rodou** e deixa o retrato de pé. *"Conferi e está certo"* e *"não consegui
conferir"* não podem ter a mesma saída.

**Medido com o PC desligado**, reconstruindo os três testes a partir do diff:

```
1 test_sem_origem_declarada_o_manifesto_CONTA_em_vez_de_calar   VERDE
2 test_com_origem_declarada_o_numero_CAI                       VERDE
3 test_a_origem_NAO_e_reescrita_pelo_manifesto                 VERDE
4 politica ausente LEVANTA (nao vira "nada declarado")          VERDE
```

**O que NÃO foi medido (P5):** a suíte `fase0` inteira. O container não tem `ajustar.py`,
`test_ajustar.py`, `test_calendario.py` nem o `coletar_b3.py` atual — o mirror é parcial.
O que está provado é a causa raiz, que era **uma** e local ao `main()`. **Rodar a suíte na
máquina é o que fecha.**

---

## Ao voltar ao desktop — as notas anteriores a 26/09

> **25/09/2026, noite — substitui a nota de 24/09 abaixo: a P-57 e a P-135 FECHARAM** (execução
> agendada `36148547193`). O que fica para a sessão local, em ordem:
>
> 1. ~~P-136 — ler os termos da B3 e a licença da CVM~~ **lidos às 20:02 UTC**, pela nuvem,
>    depois de ele liberar os hosts. Sobram duas decisões dele, escritas na P-136.
> 2. **P-147 — conferir o NEFIN no executor** depois do cron de 26/09. O agendamento de 09:15
>    UTC saiu às 14:35 UTC em 25/09: olhar à noite, não de manhã. Não exige desktop.
> 3. **`macro.poupanca_am` vence em 28/09.**

> **24/09/2026 — o que vem primeiro agora é a P-57, e são dois passos dele** (a ordem e os
> comandos estão na própria P-57): a **carga inicial** para o R2
> (`subir_acervo_local.py --aplicar`, com as `R2_*` no ambiente) e a **primeira execução**
> do workflow *Captura CVM*. O roteiro abaixo é de 19/09 e está cumprido nos passos 1–4.

> # ▶ O roteiro completo está em **`docs/historico/entregas/SEGUNDA-21.md`**.
>
> *Reescrito em 19/09. Ele é autossuficiente: abrir e seguir de cima para baixo. Esta seção
> só resume, para não haver duas listas discordando — foi assim que a versão de 06/09 ficou
> doze dias mandando criar um repositório que já existia.*

**Em uma linha:** copiar 7 arquivos do chat → as três suítes verdes → commit e push →
`ajustar.py` sobre 2021–2025 no Claude Code.

| passo | o que | tempo |
|---|---|---|
| 1 | copiar os 7 arquivos do chat (lista em `docs/historico/entregas/SEGUNDA-21.md`) | 5 min |
| 2 | **as três suítes verdes** — `origin/main` está VERMELHO (P-102) | 5 min |
| 3 | commit + push | 2 min |
| 4 | ~~**`ajustar.py` sobre 2021–2025 contíguos**~~ **FEITO em 21/09** — `docs/auditoria/C02-JANELA-2021-2025.md` | — |

**Duas coisas com data:** `macro.poupanca_am` vence **28/09**; e a CVM reescreve DFP/ITR
toda semana — cada semana sem captura é uma rodada de reapresentações que **não volta**.

**Uma coisa que eu não fiz:** não atualizei o `ACHADOS.md` — ele nunca passou pelo
container, e manter atualizado um arquivo que eu não li seria escrever sobre o que suponho
que ele diz. O bloco pronto está em `ACHADOS-19-09-PARA-COLAR.md`.
