# O texto integral das pendências ativas, até 03/10/2026

*Movido em 03/10/2026, sem edição de texto, do `PENDENCIAS.md` da raiz (`origin/main` em
`82600e2`), na divisão em ativas e reserva. As ativas foram reescritas curtas no arquivo vivo;
o texto inteiro, com a história, as medições datadas e os roteiros, é este. Vai junto a seção
"Ao voltar ao desktop" como estava (o roteiro do item 10 foi também para
`docs/marca/teste-de-marca/roteiro-no-ar.md`, onde vale como instrução). Os links relativos
foram reescritos para esta pasta.*

**Isto é registro, nunca instrução.** O que vale é a seção da pendência no `PENDENCIAS.md`.

---

## P-30 · `bloco_C_solvencia` — especificado em 05/09, nenhum módulo aplica

48 chaves escritas na mesma sessão em que a régua de solvência foi desenhada. Só
`test_alocacao.py` as menciona: os testes verificam que o **texto** existe, não que
algum comportamento derive dele. A régua de banco (P-16) depende dela.

---

## P-17 · C-04 e C-05 não foram lidos — ⚙ **exige o desktop**

O regime do bloco C está escrito, mas a lista de campos vive em
`docs/auditoria/escopo-campos-de-analise.md`, na sua máquina, e a ponte estava fora do ar.
C-01 a C-03 são conhecidos por referência cruzada dentro do próprio `politica.yaml`;
**C-04 e C-05 são citados como existentes e nunca nomeados ali.**

Não inventei os dois. Um bloco de exclusão com critério inventado excluiria empresa
por regra que ninguém escolheu — pior que bloco nenhum.

**Gatilho:** primeira sessão de desktop. Ler o arquivo e reconciliar.

---

## P-18 · `SETOR_ATIV` da CVM não foi contado

O bloco C recusa instituição financeira, e a identificação sai do campo `SETOR_ATIV`
do cadastro da CVM. O campo foi conferido, mas **só dois valores foram vistos** — a
enumeração nunca foi contada no dado real, como foi feito com `ORDEM_EXERC` e
`ESCALA_MOEDA`. Sem isso o corte automático não pode ser codificado.

**Gatilho:** antes de codificar a recusa. ⚙ exige o desktop.

---

## P-51 · `ORDEM_EXERC = PENÚLTIMO` contamina o backtest

**Classe:** `BLOQUEIA_O_SISTEMA`. **Dono:** Claude. **Gatilho:** ao escrever o parser da CVM.

O projeto contou as duas enumerações em 12,8 milhões de linhas e registrou as duas como
válidas. Elas são — mas **`PENÚLTIMO` é o ano anterior já reapresentado**. Usar a linha
`PENÚLTIMO` do arquivo de 2025 para saber o que se sabia em 2024 é look-ahead puro: é
justamente o número corrigido depois.

Regra que sai daqui: o parser usa **só `ÚLTIMO`, do arquivo daquele ano**. E a partição é
o **ano do arquivo**, não o ano do dado — o DFP de 2025 corrige 2023.

---

## P-53 · O acervo não pode depender de engine nenhum

**Classe:** `DECISAO_DE_DESENHO`. **Dono:** Claude. **Gatilho:** ao criar `data/bronze/`.

Recomendação da pesquisa: **Parquet imutável particionado por `dt_captura` como acervo, e
DuckDB como motor de consulta** — com o `.duckdb` sendo artefato reconstruível, nunca o
arquivo de registro. Segundo lugar: DuckLake (1.0 em abr/2026), com `AT (TIMESTAMP => …)`
nativo; perdeu por acoplar um acervo de década a um formato recente.

A consulta as-of e as sete armadilhas estão em
`docs/fontes/pesquisa-bases-e-apis-2026-09.md` §3. Duas que este projeto não sabia que
tinha, além da P-51: **`dt_captura` não é data de conhecimento do mercado** e **o
mapeamento ticker↔CNPJ↔CD_CVM também precisa ser bitemporal**, senão o join vaza futuro.

---

## P-58 a P-61 · Regimes de leitura de balanço — a pergunta que expôs o defeito

**Documento:** `docs/auditoria/regimes-de-leitura-de-balanco.md`. **Classe:** todas
`BLOQUEIA_O_SISTEMA`. **Gatilho:** depois da P-18 (contar `SETOR_ATIV`), que bloqueia as
quatro.

**Pergunta do Osvaldo, 06/09/2026:** como o sistema lida com empresa que lucrou menos por
reinvestir, com dívida feita para capex, e com setores que funcionam com dívida alta —
construção civil, porque se realiza imóvel com financiamento.

**Resposta honesta: não estava desenhado.** E a pergunta expôs um defeito do projeto, não
uma lacuna de escopo.

O `bloco_C_solvencia` já escreve que dívida líquida/EBITDA aplicado a um banco *"devolve
um número, e esse é o perigo: métrica que não se aplica mas não falha é o modo de falha do
F-02"*. **O projeto reconheceu esse modo de falha para banco e não o generalizou.** Existe
um regime para instituição financeira e **um único regime para "todo o resto"** — que lê
uma incorporadora e uma WEG com a mesma régua.

| | |
|---|---|
| **P-58** | o portão de regime tem 2 saídas e precisa de N. Candidatos: incorporação, utilities/concessões, propriedades para renda, arrendamento pesado (IFRS 16) |
| **P-59** | **C-01 (cobertura de juros) exclui empresa em fase de investimento** — EBIT deprimido por depreciação nova E despesa financeira alta pela dívida do capex: as duas pontas pioram pelo mesmo motivo, que pode ser saudável. E cai no portão de **exclusão**, o pior lugar |
| **P-60** | **ROIC vs custo da dívida** não existe no sistema, e é o único critério que separa dívida que cria valor de dívida que destrói |
| **P-61** | capex de **manutenção** vs **expansão**: a CVM não separa, e a heurística "manutenção ≈ depreciação" é conhecidamente errada em empresa que cresce. **Limitação declarada**, com direção de viés: **o sistema subestima quem investe para crescer** |

**A correção que a pergunta dele também recebeu:** capex **não passa pela DRE**. O que
derruba o lucro são três causas distintas — depreciação do capex passado, juros da dívida
do capex, e opex não capitalizado — e elas têm leitura **oposta**. Consequência de
desenho: **a porta de entrada é a DFC, não a DRE.**

**P6 aplicada:** construção civil **não sai do universo**. A saída fácil seria excluir por
falta de régua, e foi exatamente essa a correção que criou a P6 — no caso do banco. Se eu
excluir agora, é a quarta vez.

**O que só ele responde** (§6 do documento): dívida SFH vs corporativa, receita a
apropriar, permuta, distratos, e qual número um planejador olha primeiro. Ele é engenheiro
civil e analista de planejamento; isso é procedência melhor que artigo, **desde que
registrada como decisão dele**.

---

## P-64 · Portão × dossiê — uma camada de desenho que o projeto não tem

**Classe:** `BLOQUEIA_O_SISTEMA`. **Dono:** Claude. **Gatilho:** antes de implementar
qualquer regime.

Ele respondeu como analista lendo **uma** empresa. O sistema precisa varrer **centenas**.
Uma sequência manual de dez passos não é portão.

| | o que é | quando roda | fonte |
|---|---|---|---|
| **portão** | automático, todo o universo | sempre | dado estruturado |
| **dossiê** | leitura manual guiada, empresa a empresa | só na lista curta | notas, release, IPE |

Para incorporação **o portão não pode ser o regime** — o dado não existe (X-01). O portão só
pode dizer: *"esta empresa é do regime INCORPORACAO, exige dossiê, e até ter um permanece no
universo sem peso atribuído por este bloco."*

Coerente com P6 (nada sai), P1 (nada é inventado) e A05 (o sistema não nomeia empresa). E
transforma o painel de cinco camadas dele **no roteiro do dossiê** — que é o que ele é.

**Vale para todo regime, não só incorporação.**

---

## P-65 · Extração de nota explicativa e de IPE — a segunda esteira, nunca orçada

**Classe:** `BLOQUEIA_O_SISTEMA`. **Dono:** Claude. **Gatilho:** depois da Fase 0 rodar.

**Achado X-01.** Dos dez passos da sequência dele, **3 são obtíveis** no dado estruturado
(FCO, margem bruta, caixa) e **7 não são**. E os 3 obtíveis são os que ele não colocaria em
primeiro lugar.

O caminho existe: a página do conjunto DFP publica *"os endereços para download dos
Formulários DFP entregues"* (documento completo do Empresas.NET), e o **IPE** carrega
releases de resultados. Mas é **extração de documento**, não leitura de CSV — ordem de
grandeza diferente do que o projeto orçou.

**A investigar antes de prometer:** formato dos formulários do Empresas.NET; se as notas
vêm em XML estruturado ou em texto livre; volume do IPE; e se existe alguma padronização
que torne a extração determinística em vez de heurística. **Se for heurística, ela produz
número sem procedência — e aí a P1 manda não fazer.**

> **Decisão dele, 26/09/2026: `65b`** (**diverge da recomendada (65a)**) — a segunda esteira entra **já como construção**, com a condição dele: só extração **determinística** — todo número carrega o trecho, a posição e o sha256 do arquivo de origem, e número sem trecho é recusado (P1). Começa medindo o formato. Registro em `docs/decisoes/fila-do-osvaldo.md`.

---

## P-127 · Oráculo externo do preço ajustado — **decisão sua**

**Dono:** Osvaldo (decidir) · **Gatilho:** antes de usar a série ajustada na ML-3 ·
**Classe:** `DECISAO_DE_DESENHO`

Ideia 4a de `docs/pesquisa/analise-pesquisa-apis-2026-09-23.md`. O C-02 valida o
`ajustar.py` contra ele mesmo; o instrumento que pegou o A-13 foi **duas fontes independentes
comparadas**. Um agregador de preço ajustado (plano gratuito) serviria de **controle** numa
amostra — mesmo papel, mesmo período, medir a divergência — e **nunca de feed** (rebaixaria a
P1). Exige pré-registro (P-116): o critério de "concordam" empurrado antes de olhar. A decisão
é se vale o custo, e qual fornecedor (os nomes são dos relatórios, `NAO_CONFIRMADO`).

> **Decisão dele, 26/09/2026: `127a`** (recomendada) — oráculo externo como **controle** numa amostra, depois da P-115, com o critério de "concordam" gravado antes de olhar e os termos do fornecedor lidos na fonte. Registro em `docs/decisoes/fila-do-osvaldo.md`.

---

## P-145 · A ponte e o universo do ML depois de 2012, e duas escolhas que a §2 não fez

**Dono:** Claude Code (medir) · ~~Osvaldo (as duas escolhas)~~ decididas por ele em 25/09 ·
**Gatilho:** antes da primeira
variável da ML-3 · **Classe:** `DECISAO_DE_DESENHO`

A P-143 fechou a ponte para **2010–2012** (a janela da emenda). O desenvolvimento vai até 2019:
os emissores do universo de 2013–2019 ainda não passaram pela conferência da CV-06, e a ponte
manual cresce com eles. Há também duas escolhas da §2 que mudam o universo e que a medição da
emenda não precisou fazer, porque o mês saiu igual nas duas:
1. *"3 meses anteriores"*: t-2..t ou t-3..t-1;
2. *"percentil ≥ 50"*: aplicado aqui como `≥ mediana` dos que passaram no filtro de pregões.

> **As duas escolhas foram decididas por ele em 25/09:** `t-2..t` e `≥ mediana` (inclusiva). Estão
> em `preregistro-ml-v2-emenda-1.md` §6 "Esclarecimentos", empurrada em `2f939ae` **antes** de
> qualquer número desta pendência (P-116). **sha256 publicado: `71621ba64c899281`.** O texto do
> commit `2f939ae` cita `380d747051f5e9b5`, o sha de um rascunho anterior à última correção de
> redação; o commit não foi reescrito, e o sha que vale é o do arquivo no `origin`. Falta a
> ponte de 2013–2019 e a captura do ISIN.
> **Houve uma segunda publicação da mesma §6, e ela não vale.** Uma sessão local, sem ver esta
> branch, empurrou ao `main` em `53112d6` (16:54Z) um texto de mesma substância e outra redação
> (sha256 `7fc09d780c5012ac`). O merge de 25/09 ficou com a versão de `2f939ae`, a primeira no
> `origin`; `53112d6` fica no histórico como registro. Achado GIT-01.
> **26/09/2026 — quarentena da P-115 (§9 do critério v2, no #27).** Até o merge e a medição
> do #27, nenhuma medição lê o **retorno do dia ex** em 2013–2020, esta inclusive. Conferido no
> mesmo dia: o `universo_ml.py`, que esta medição usa, lê do COTAHIST CODBDI, TPMERC, CODNEG,
> **VOLTOT** e CODISI, e nenhum campo de preço. Volume não é retorno, e a P-145 roda dentro da
> quarentena **como está**. Se ela passar a abrir preço, espera.

**E a captura do banco de ISIN não é rotina** (P7): foi uma vez, 25/09, `isinp.zip` sha256
`c4654dbd…`. Para 2010–2017 isso basta (o passado não muda), mas a ponte de um ano novo precisa
de captura, ou de limitação declarada.

> **26/09/2026 — a medição existe e roda sem o desktop; falta insumo e token, os dois dele.**
> `medicoes/p145_ponte_2013_2019.py`, pelo `.github/workflows/medir.yml` (CLAUDE.md §5-A.11), na
> branch `medir/p145_ponte_2013_2019`, com as duas leituras fixadas (`t-2..t`, `≥ mediana`
> inclusiva). Classifica cada emissor de 2013–2019 em `MANUAL`, `LIGADO_NOME_CONFERE`,
> `LIGADO_NOME_DIVERGE`, `CNPJ_SEM_CVM` (a forma dos 4 reaproveitados da CV-06) e
> `AUSENTE_DO_ISIN`, e lista os três últimos para a conferência à mão.
>
> **Resultado da primeira execução** (`36246813373`, 13:56Z): parou em *Conferir insumos*, sem
> segredo nenhum no ambiente — `isin/isinp.zip: nenhum registro nem inventario`. Medido também
> aqui, pelo mesmo comando: é o **único** insumo ausente; os oito COTAHIST fixados (2012–2019),
> o cadastro, os DFP de 2010–2019 e os ITR de 2011–2019 o acervo conhece. **Nenhum número da
> ponte existe ainda.** Para rodar faltam dois passos dele, na ordem:
> 1. ⚙ **desktop:** `py -3.11 fase0/subir_acervo_local.py --aplicar` — agora cobre o banco de
>    ISIN e sobe o `isinp.zip` de 25/09 (sha256 `c4654dbd…`) com o inventário;
> 2. **Cloudflare + GitHub:** um token do R2 **somente leitura** e os quatro segredos
>    `R2_LEITURA_ACCOUNT_ID`, `R2_LEITURA_ACCESS_KEY_ID`, `R2_LEITURA_SECRET_ACCESS_KEY`,
>    `R2_LEITURA_BUCKET`.
>
> Depois, a sessão empurra de novo a branch e o resultado volta commitado nela.

---

## P-162 · Teste de marca das direções visuais (H1 a H4)

**Dono:** Osvaldo (recrutamento e custo) · Claude (estímulos, questionário, análise) ·
**Gatilho:** quando a P-163 estiver pronta **e** o pré-registro final estiver empurrado ·
**Classe:** `DECISAO_DE_DESENHO`

É a etapa 3 (mercado) da fila do rosto (`docs/decisoes/rosto-v1.md`). O pré-registro de
20/09 está em `docs/marca/preregistro-teste-de-marca-2026-09-20.md`, sem impressão digital
e com três lacunas que ele fecha nos blocos 16 e 17 da fila: a direção E fora da H1, a
margem de empate da regra de decisão, e o desenho do teste da H3. *(27/09: fechadas pelas
respostas 16b e 17a; entram no pré-registro final, ainda não gravado.)* *(27/09, S4: g-B, h-A, i-A,
j-A, amigos e recrutamento também respondidos; a S5 grava o pré-registro final depois de ele
aprovar os PNG da S4.)* ~~Filtro de entrada:
aporta todo mês em renda variável há pelo menos 6 meses. Pessoas próximas do autor servem
para **pilotar** o questionário, não para contar como resposta. A medição da H-A1 pode
entrar como exploratória, declarada como **não sendo prevalência** (a prevalência é da
P-154).~~ *(27/09, S5: o filtro foi reescrito sem jargão (v-a); as pessoas próximas **contam**,
com a análise dupla em que a sem elas decide (amigos, r-a); a H-A1 não entra, porque nenhuma
decisão dele a incluiu e a n-A a juntou com a H-A2 na P-154.)*

> **27/09/2026, S5 — o pré-registro final está gravado:**
> [`docs/marca/preregistro-teste-de-marca-final.md`](../marca/preregistro-teste-de-marca-final.md),
> com o [questionário](../marca/teste-de-marca-questionario.md) e a análise
> (`tools/analise_teste_marca.py`) congelados pelo sha256, e os seis PNG aprovados. A H4 foi
> para a P-156 (s-a).
>
> **Primeiro convite só depois do merge deste pré-registro no main e do commit com as datas
> da janela.**
>
> ~~O que falta, em ordem, é dele: o merge; montar os seis formulários e conferi-los (roteiro em
> "Ao voltar ao desktop", item 8); o commit das datas; o primeiro convite.~~ A pendência fecha
> com o relatório da análise, depois do dia 21.

> **27/09/2026, S5 v2 — a versão 1 acima fica SUPERADA, sem ter sido usada** (nenhum convite
> saiu). Ele trocou o Google Forms por uma **página própria** (Vercel e Supabase, construída na
> S6) e acrescentou o **veto de distinção** contra a rodada 3 de marcas (R3). O pré-registro que
> vale é [`docs/marca/teste-de-marca/preregistro-final.md`](../marca/teste-de-marca/preregistro-final.md),
> com o [questionário como dado](../marca/teste-de-marca/questionario.yaml), o
> [livro de códigos visuais](../marca/teste-de-marca/codigos-visuais.yaml) com E, C e D já
> classificadas, e a análise, congelados pelo sha256. Respostas dele na fila: ~~y-b (voltam os
> textos de 20/09 do filtro e dos amigos)~~, z-a, aa-a e ab-a. **02/10/2026, y-a:** supera a
> y-b; voltam os textos do ensaio (u-a e v-a), e o `questionario.yaml` ganha sha256 novo, antes
> do primeiro convite.
>
> **Primeiro convite só depois do merge deste pré-registro e da página (S6) no main, e do
> commit com as datas da janela.**
>
> **A escolha da direção só sai com a R3 fechada** (veto de distinção).
>
> **02/10/2026, revisão antes do merge (Claude Code, sessão local):** as categorias do veto
> ficaram fechadas no livro de códigos (ac-a, dele: as sete financeiras; as referências de
> sentimento fora). O classificador `tools/codigos_visuais.py` entrou no conjunto congelado
> (dez arquivos); o contrato da página exige envio por POST; e a limitação 4 ganhou o painel
> do Firewall da Vercel. A R3 virou a P-170.
>
> **02/10/2026, S6 — a página da pesquisa está em `pesquisa/`** (sem deploy; nenhuma resposta
> real existe). Pôr no ar é dele: roteiro em "Ao voltar ao desktop", item 10. **Primeiro
> convite só depois do merge da S6, do roteiro do item 10 e do commit com as datas da janela.**

---

## P-164 · Primeiro aporte com patrimônio zero (`SEM_POSICAO`)

**Dono:** Osvaldo (a regra) · Claude Code (implementar) · **Gatilho:** P-115 fechada ·
**Classe:** `DECISAO_DE_DESENHO` (vira engenharia quando ele responder o bloco 19)

`motor_aporte()` devolve `SEM_POSICAO` com patrimônio zero, e quem tem a reserva cheia e
nada investido fica sem "quanto e onde" (F0-contrato §2 e §3, item 2). Lido no código em
26/09: com `V = 0`, a fórmula das ordens já põe o aporte nas `k_max` rotas de maior peso;
o guarda existe por causa das divisões por `V` (`peso_atual`, `deficit_rel`). O
`test_depois_da_reserva_o_sistema_aloca_sem_nada_assinado` confere o alvo, não as ordens.
O teste que prende o conserto tem de **falhar na versão atual**: patrimônio zero e reserva
cheia recebem ordens com rota e valor.

---

## P-170 · A rodada 3 de marcas (R3), visual, para o veto de distinção

**Dono:** Claude (auditar e classificar) · Osvaldo (o veto, se disparar) · **Gatilho:** o
merge do pré-registro final 2 do teste de marca (P-162), que fecha o livro de códigos; corre
em paralelo à coleta · **Classe:** `DECISAO_DE_DESENHO`

A escolha da direção do teste de marca só sai com a R3 fechada (veto de distinção, decisão
dele de 27/09). Até 02/10 a R3 não existia no repositório: a rodada 2 a deixou como "P-B5b",
**textual**, e a 2 não registrou nenhum código visual. A R3 é outra coisa: **visual**,
classificando a tela de cada marca pelo
[livro de códigos](../marca/teste-de-marca/codigos-visuais.yaml), com o classificador
`tools/codigos_visuais.py`, nas sete categorias fechadas pela ac-a (02/10).

O que fecha: um arquivo de marcas classificadas, uma linha por marca, com a categoria, a
captura usada (fonte e data) e as medidas que o `classificar()` recebe; pelo menos 5 marcas
por categoria que se queira capaz de vetar (com menos, a categoria não tem código dominante);
e o `veto()` aplicado à direção vencedora quando a análise sair. **Antes da primeira marca:**
a lista de marcas por categoria, escrita e empurrada, pela mesma razão da ac-a. As capturas
são de página pública (loja de apps, site); a §5-A.7 vale: nada de sessão logada, e acesso
recusado sobe a escada (§5-B.18) antes de virar `NAO_CONFIRMADO`.

> **02/10/2026, sessão 1 da R3 (sessão local):** antes da primeira marca, ele emendou o livro de
> códigos (versão 2; ad-a, ae-a e af-a na fila): quatro categorias novas (consultoria CVM,
> assessor, robô, planejador), a unidade (app ou site) e 10 marcas sorteadas por categoria. O
> plano e o sorteio estão gravados ([`docs/marca/rodada3/`](../marca/rodada3/plano.yaml);
> semente 20261002): consultoria 528, assessor 148, corretora 138 e gestora 1.195 no universo.
> **Nenhuma marca visitada.** O andamento mora em
> [`docs/marca/pesquisa-marcas-rodada3-2026-09.md`](../marca/pesquisa-marcas-rodada3-2026-09.md),
> §5. **As visitas só começam depois do merge** que grava a emenda e o sorteio.

---

## P-172 · O PLANO.md na abertura volta à decisão em 17/10, com a regra de volta medida

**Dono:** Osvaldo (decidir) · Claude Code (levar os números) · **Gatilho:** 17/10/2026, com duas
semanas de dado da regra de volta · **Classe:** `DECISAO_DE_DESENHO`

Resposta **22a** de 03/10 (fila, bloco 22): o `PLANO.md` segue na abertura, e a decisão volta a
ele quando a regra de volta dos modelos (21d) tiver duas semanas de dado. Um corte de cada vez:
tirar o `PLANO.md` e trocar de modelo ao mesmo tempo deixaria sem saber qual dos dois causou um
erro novo.

**O que a sessão de 17/10 leva:**
1. a tabela da regra de volta, de `python auditoria/metricas_processo.py --prs prs.json` com a
   lista de `gh pr list --state merged --base main --json number,title,mergedAt,author`, e o
   resumo dos semanais de 05/10 e 12/10;
2. o tamanho da abertura, de `python auditoria/tamanho_do_contexto.py`;
3. ~~a pergunta da referência zero~~ **respondida em 03/10:** a referência virou
   (eventos + 1) / (PRs + 1) e a volta exige pelo menos 2 eventos da classe na janela (fila,
   ajuste da 21d). Resta olhar, com dois semanais de dado, se o piso ficou alto demais para o
   `registro` (limiar 0,21 com referência 1/7).

---

## Ao voltar ao desktop

> **26/09/2026, nuvem — substitui a nota de 25/09 abaixo.** A revisão das pendências dele fechou
> 16 vencidas; o que é decisão dele está em **`docs/decisoes/fila-do-osvaldo.md`**, 15 blocos
> para responder pelo celular. Em ordem:
>
> 1. **As respostas da fila** viram o trabalho da sessão seguinte, a começar pela 1 (P-115) e
>    pela 2 (P-117), que vêm antes de qualquer janela nova da série ajustada.
> 2. ~~**P-151 antes de segunda, 28/09, 11:00 UTC.**~~ **Fechada em 26/09** (a guarda do GIT-01 pula no CI).
> 3. **P-150 — subir ao R2 o acervo de eventos de 11/09.** ⚙ **exige o desktop**. O script
>    cobre as pastas desde 26/09. Primeiro `py -3.11 fase0/subir_acervo_local.py` (só o plano):
>    conferir que os eventos aparecem como `SUBIR` em `b3/indice_carteira|eventos_suplemento|
>    proventos/…` e que não há `PARAR`. Um `DESCONHECIDO` em pasta de eventos se lê antes de
>    seguir. Depois, com as `R2_*` no ambiente, `--aplicar`, e commitar
>    `docs/acervo/b3_eventos/inventario-armazem.csv`. E conferir o cron de segunda, 28/09.
> 4. ~~**P-147 (NEFIN) e a release `cvm-acervo-2026`:** conferir depois do cron de 26/09. Não
>    exige desktop.~~ **Conferido em 27/09, na nuvem:** o cron `36246158435` (26/09)
>    rodou o `captura_nefin` verde (P-147 fechada) e publicou a release `cvm-acervo-2026`
>    (13:46Z). Nada a fazer no desktop.
> 5. ~~`macro.poupanca_am` vence em 28/09~~ — renovada em 25/09; vence em **24/10**.
> 6. **P-145 — dois passos dele destravam a medição na nuvem:** ⚙ **desktop:**
>    `py -3.11 fase0/subir_acervo_local.py --aplicar` (sobe o `isinp.zip`); e, de qualquer
>    lugar, o token do R2 **somente leitura** com os quatro segredos `R2_LEITURA_*`.
> 7. **27/09/2026 — a fila do rosto.** Os blocos 16 a 20 da fila
>    (`docs/decisoes/fila-do-osvaldo.md`) esperam o Osvaldo; os 16 e 17 destravam a P-162, e
>    nenhum exige o desktop. *(27/09: 16b e 17a respondidos; seguem 18, 19 e 20.)* **A P-115 continua na frente**: a fila do rosto não disputa com
>    ela (`docs/decisoes/rosto-v1.md`).
> 8. ~~**27/09/2026 — P-162, os seis formulários do teste de marca.**~~ **Superado pela S5 v2
>    (27/09):** o instrumento é uma página própria, feita na S6, e não um formulário. O que
>    fica dele: uma resposta de teste e o `py -3.11 tools/analise_teste_marca.py
>    --conferir-cabecalho` sobre a exportação real da página, antes do commit das datas (§12 do
>    pré-registro). O roteiro antigo, riscado:
>    ~~(navegador logado na conta Google dele; a sessão na nuvem não usa sessão de navegador,~~
>    ~~§5-A.7). Só **depois do merge** do pré-registro final. Tudo sai de~~
>    ~~`docs/marca/teste-de-marca-questionario.md`:~~
>    ~~1. **Montar um formulário** no Google Forms, seção por seção, com o texto exato do~~
>    ~~questionário: sem coletar e-mail, fuso (GMT-03:00) Brasília, perguntas obrigatórias~~
>    ~~(menos as duas abertas), uma seção por imagem e uma por bloco de perguntas, e os~~
>    ~~títulos copiados letra a letra (o script acha cada coluna pelo título). As imagens~~
>    ~~são os PNG de `docs/marca/direcoes/png/`, na ordem da versão 1 (E, C, D).~~
>    ~~2. **Duplicar seis vezes** (Forms → Fazer uma cópia) e, em cada cópia, trocar a ordem~~
>    ~~das imagens pela tabela da seção 8 do questionário. Nomear cada uma "versão N".~~
>    ~~3. **Conferir cada versão contra o questionário:** a ordem das seis imagens, os~~
>    ~~títulos, os rótulos do 1 e do 7, os desvios de seção do consentimento e do filtro.~~
>    ~~4. **Uma resposta de teste por versão, com "Não concordo"**, exportar as respostas de~~
>    ~~cada uma (Respostas → Planilhas → Baixar CSV) como `data/teste-marca/versao-N.csv` e~~
>    ~~rodar `py -3.11 tools/analise_teste_marca.py --conferir-cabecalho`: tem de dar `ok`~~
>    ~~nas seis e ler o carimbo. Se o carimbo não for lido, **parar**: o formato do Forms é~~
>    ~~`NAO_CONFIRMADO` e mudar o script é pré-registro novo, antes do convite.~~
>    ~~5. **Commit das datas da janela**: preencher as duas linhas da §6 do pré-registro final~~
>    ~~(dia 1 e dia 21) e empurrar. **Antes** do primeiro convite.~~
>    ~~6. **Primeiro convite**, com o link da versão 1; o seguinte com a 2, e assim em rodízio.~~
>    ~~Os CSV ficam em `data/teste-marca/` (ignorado pelo git) e em nenhum outro lugar do~~
>    ~~repositório. A análise roda depois de 23:59 do dia 21:~~
>    ~~`py -3.11 tools/analise_teste_marca.py --inicio <dia 1>` (antes disso ela recusa).~~
> 9. **27/09/2026 — o degrau 4 da escada de contorno (§5-B.18).** ⚙ **exige o desktop** (IP
>    residencial; a nuvem levou 403 do Akamai e o túnel do `web.archive.org` caiu). Dois
>    roteiros, sem navegador e sem sessão logada: o do **BOVV11** está na P-05 (três `curl`
>    e a transcrição do trecho da taxa total); o dos **11 bancos da regra m-B** está na P-169
>    (a cor declarada no HTML ou no CSS de cada página inicial). **Não exige o desktop:**
>    colar a versão 2 de `docs/ia/instrucoes-projeto-claude.md` nas instruções do Projeto no
>    claude.ai, que passam a ter a escada.
> 10. **02/10/2026 — P-162, pôr a página da pesquisa no ar (S6).** Só **depois do merge** do PR
>    da S6. Dá para fazer **no celular ou no computador**; nada exige o desktop, menos o passo 6
>    (rodar a análise no `data/` dele). As contas e as chaves são dele: **nenhuma chave vai para o
>    chat nem para o repositório** (§5-A.7). O que a página faz está em `pesquisa/README.md`.
>    0. **Decidir o plano da Vercel.** O Hobby (grátis) é "restricted to non-commercial personal
>       use only", e uso comercial é qualquer deploy "used for the purpose of financial gain of
>       **anyone** involved" (`vercel.com/docs/limits/fair-use-guidelines`, lido em 02/10). A
>       página não cobra, não anuncia e não vende, mas testa a marca de um produto possível. Se
>       é uso comercial, é decisão dele: Hobby, Pro, ou perguntar ao suporte da Vercel.
>    1. **Supabase, plano Free:** criar o projeto (*New project*), região **South America (São
>       Paulo)**. A senha do banco fica no gerenciador de senhas dele.
>    2. **SQL Editor → New query:** colar `pesquisa/supabase/esquema.sql` inteiro e rodar
>       (*Run*). Depois, numa query nova, colar `pesquisa/supabase/teste_politicas.sql` e
>       rodar. **Tem de terminar sem erro.** Um erro com "FALHA: …" quer dizer que o anon pode
>       mais do que deve: **parar** e trazer a mensagem. O teste desfaz o que fez (`rollback`).
>    3. **As duas chaves:** no botão *Connect* do projeto (ou *Settings → API Keys*), copiar a
>       **Project URL** e a **Publishable key** (`sb_publishable_…`). **Nunca a secret key**
>       (`sb_secret_…`), que passa por cima do RLS. A chave `anon` antiga (um texto longo que
>       começa com `eyJ`) também funciona, mas o Supabase a descontinua até o fim de 2026.
>    4. **Vercel:** *Add New → Project*, importar este repositório; **Root Directory:
>       `pesquisa`**; *Framework Preset*: **Other**, sem comando de build. Em *Environment
>       Variables*, criar `SUPABASE_URL` (a Project URL) e `SUPABASE_ANON_KEY` (a Publishable
>       key), coladas direto no painel da Vercel. *Deploy*. **Não ligar** Web Analytics nem
>       Speed Insights: eles vêm desligados, e o contrato os quer desligados.
>    5. **Conferir no ar**, na URL de produção:
>       - `<url>/README.md` e `<url>/supabase/esquema.sql` dão **404**. O `.vercelignore` os
>         tira do ar; a documentação da Vercel não diz com todas as letras que isso vale para
>         deploy pelo Git, então a prova é este passo;
>       - **responder a pesquisa uma vez, até o fim**;
>       - no Supabase, *Table Editor*: `aberturas` tem 1 linha e `respostas` tem 1 linha, e o
>         `questionario_sha256` dela é o do pré-registro (`73936c74…`).
>    6. ⚙ **No desktop:** rodar `pesquisa/supabase/exportar.sql` no SQL Editor, baixar o
>       resultado em CSV como `data/teste-marca/respostas.csv` e rodar
>       `py -3.11 tools/analise_teste_marca.py --conferir-cabecalho`. Tem de dar `ok`. Se não
>       der, **parar**: o cabeçalho da exportação real é o último ponto que nenhum teste viu.
>    7. **Apagar a resposta de teste** (SQL Editor). É o mesmo comando para o teste do passo 5 e
>       para qualquer outro antes do convite:
>       `delete from public.respostas; delete from public.aberturas;
>       update public.contador_de_aberturas set aberturas = 0;`
>       E apagar o `data/teste-marca/respostas.csv` do teste. O contador volta a 0 porque as
>       aberturas de teste não são da janela (ab-a).
>    8. Daí em diante, a ordem é a do pré-registro (§12): **o commit das datas da janela,
>       empurrado, e só então o primeiro convite.** Depois do primeiro convite, nada se apaga.
>
> 11. **03/10/2026 — P-115, os PDFs do D1 no armazém.** ⚙ **exige o desktop** (o R2 só se
>     escreve de lá). Baixar as 10 provas pelas URLs de `docs/fontes/jcp-amostra-2016-2020.md`,
>     conferir cada sha256 contra a tabela antes de subir e subir com a chave = conteúdo. Do
>     20-F da Gerdau, sobe o documento arquivado (sha256 `20f8599e…b512`). Não bloqueia a
>     corrida: a §3.1 exige as quatro provas por evento, e o armazém guarda a cópia.
