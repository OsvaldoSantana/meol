# Pendências ativas

**No máximo 20, lidas inteiras em toda sessão** (decisão dele, 03/10/2026). O resto do que está
aberto mora em [`docs/pendencias-reserva.md`](docs/pendencias-reserva.md), que se lê por busca.
O texto integral destas, até 03/10, com a história e as medições datadas, está em
`docs/historico/pendencias-ativas-ate-2026-10-03.md`; aqui fica só o que muda o que se faz.

- **Cada uma com dono, gatilho e classe** (`CLAUDE.md` §5-A.1). Sem os três, não entra.
- **Ativa é o que está no caminho do `PLANO.md`** ou com gatilho vencendo. Saiu do caminho, vai
  para a reserva; entrou, vem de lá. Com 20, uma sai antes de outra entrar.
- **Fechou?** Cabeçalho riscado, evidência, e o bloco vai para
  `docs/historico/pendencias-fechadas.md`, com a linha na tabela `## Fechadas`, no mesmo commit.
- **Decisões que esperam o Osvaldo:** `docs/decisoes/fila-do-osvaldo.md`.

Guarda: `auditoria/test_plano_e_pendencias.py` (teto de 20, os três campos, nenhum código nos
dois arquivos).

---

## P-145 · A ponte ticker → CD_CVM de 2013–2019 — o passo 1 do caminho crítico

**Dono:** Osvaldo (o envio ao R2) · Claude Code (a medição, depois) · **Gatilho:** agora; é a
cabeça do caminho crítico de 03/10 · **Classe:** `BLOQUEIA_O_SISTEMA`

A ponte de 2010–2012 fechou (P-143); a de 2013–2019 nunca foi medida. As duas escolhas da §2 são
dele e foram decididas em 25/09 (`t-2..t`, `≥ mediana` inclusiva; emenda 1, sha256
`71621ba64c899281`). A medição existe: `medicoes/p145_ponte_2013_2019.py` classifica cada
emissor em `MANUAL`, `LIGADO_NOME_CONFERE`, `LIGADO_NOME_DIVERGE`, `CNPJ_SEM_CVM` e
`AUSENTE_DO_ISIN`. Pelo `medir.yml` ela parou em 26/09 por falta do `isinp.zip` no armazém e do
token de leitura. **Na sessão local, falta só o envio** (corrigido em 04/10): o `isinp.zip` de
25/09 está no disco dele, mas o `acervo.abrir` só aceita versão que conste no registro ou no
inventário do armazém, e o inventário só se grava **depois** do envio (`subir_acervo_local.py`).
Rodado por ele em 04/10: `INSUMO AUSENTE ... 'isin/isinp.zip: nenhum registro nem inventario'`.
O plano do envio, no mesmo dia: 393 `SUBIR`, 0 `PARAR`, 0 `DESCONHECIDO` (1.583 MiB), com o
`isinp.zip` (`c4654dbd…`) entre eles. O token de leitura só é preciso para medir na nuvem.
Saída só com contagem, código e rótulo (P-136).

> **Retratação, 04/10/2026.** A triagem de 03/10 escreveu aqui que "a sessão local roda sem
> esperar nenhum dos dois" passos dele. **Evidência que derruba:** a execução acima. **Causa
> raiz:** concluí pela existência do arquivo no disco e pela descrição do `acervo.abrir` ("procura
> no cache, no `data/bronze/` e no R2"), sem rodar o script e sem ler o `_escolher()`, que exige
> registro ou inventário antes de procurar o byte. É a §5-B.13 ao contrário: "dá para fazer X"
> escrito sem tentar X. **O que muda:** afirmação de que um passo roda sai com a execução ao lado.
**Fecha com:** cada emissor de 2013–2019 classificado, e os três últimos rótulos conferidos à mão.

## P-53b · A ponte ticker ↔ CNPJ ↔ CD_CVM também é bitemporal — a sobra da P-53

**Dono:** Claude Code · **Gatilho:** P-145 fechada · **Classe:** `BLOQUEIA_O_SISTEMA`

O leitor *as-of* (P-53, fechada em 10/10) responde por `CD_CVM` e não liga papel a empresa. O
join papel × `CD_CVM` precisa da ponte **no tempo**: um código de negociação de 2010 pode apontar
hoje para outra entidade (CV-06: `EMBR`, `JBSS`, `TRPL`, `PMAM`), e uma ponte de hoje aplicada
ao passado vaza futuro em silêncio. **Fecha com:** a ponte da P-145 consultada *as-of*, e um
teste em que um código reaproveitado liga o papel de 2010 ao emissor de 2010, não ao de hoje.

## P-184 · O valor da versão substituída, lido do ENET pelo `LINK_DOC`

**Dono:** Claude Code · **Gatilho:** antes de o backtest usar o modo `conhecimento="dt_receb"` do
leitor *as-of* numa estratégia que não tolere documento ausente · **Classe:** `BLOQUEIA_O_SISTEMA`

O modo `dt_receb` (P-183, fechada em 16/10) responde 2010–2026 sem *look-ahead*, mas esconde
**14.955 de 3.870.622 documento-meses (0,4%)**: os meses em que o mercado conhecia uma versão
que o demonstrativo não traz mais (`medicoes/resultados/p183_dt_receb.txt`; n = 40.905
documentos, 2.727 com mês oculto). O índice de cada ZIP dá um `LINK_DOC` por versão, e o ENET da
CVM serviu as versões substituídas pelo `https`, com o XML estruturado inteiro (`NumeroConta`,
`ValorConta1..12`), nos 2 documentos testados (DFP 2015 do CD_CVM 1023, ITR 31/03/2024 do
CD_CVM 14206). O pacote é cortado no PDF (curl 56 perto de 12–16 MB), que vem depois do XML, e
o servidor ignora `Range`. **Fecha com:** as versões substituídas dos 2.727 documentos baixadas
pela ordem do degrau 4 (4a, o workflow no servidor do GitHub, primeiro), o leitor do XML com teste
e com o mesmo leiaute de conta, o modo `dt_receb` devolvendo a versão que o mercado conhecia, e a
limitação passando a RESOLVIDA, ou a FISICA só pelas versões que nem o ENET guardar.

## P-30 · O bloco C sobre dado real — o passo 3 do caminho crítico

**Dono:** Claude Code · **Gatilho:** a bitemporalidade pronta (P-53, fechada em 10/10: o leitor responde desde 24/09/2026); para o histórico, o modo `dt_receb` (P-183, fechada em 16/10), com 0,4% de documento-meses ocultos até a P-184 · **Classe:**
`BLOQUEIA_O_SISTEMA` *(campos dados na triagem de 03/10/2026, P-171)*

**Parte 1 feita em 24/10/2026** (`politica.yaml` 1.44.0; `alocacao/bloco_c.py`, 37 testes sobre
acervo sintético): as cinco saídas do portão (decisão do arquiteto em
`docs/decisoes/2026-10-24-saidas-do-portao-bloco-c.md`), o bloco lendo tudo do YAML (cortes,
grades, ordem, 63a, contas do plano conferidas no DFP 2024 real), o documento visto só pelo leitor
(modo da captura e `dt_receb`), a contagem do 27c como função (`contar`) e como medição
(`medicoes/p30_contagem.py`, branch `medir/p30_contagem`). **Nenhum corte está ativo** e o bloco
**não está ligado** ao `alocar()` nem ao `motor_aporte()`. C-01, C-03 e C-05 calculam e marcam; o
C-02 é `NAO_IMPLEMENTADA` (P-185); o C-04 marca "não medido" (P-65). **Falta (parte 2):** a
contagem real rodada (precisa do token `R2_LEITURA_*`), a escolha dele vendo a contagem (P-17),
os setores financeiro-adjacentes e a holding genérica (265 linhas do cadastro, em `GERAL` por
escolha de Claude) olhados por ele, e ligar ao motor.

`bloco_C_solvencia` tinha 48 chaves escritas em 05/09 e nenhum módulo as aplicava: os testes
conferiam o texto, não o comportamento. É o primeiro portão que olha empresa, e é de **exclusão**
(`criterio_nao_e_previsao`). **Leva a 63a** (decisão dele, 26/09): cada métrica declara no YAML
se lê nível, tendência ou híbrido. Dependem dela P-17, P-18, P-58 a P-61 e P-64; o regime de
banco é a P-31, na reserva. **Fecha com:** o bloco rodando sobre o acervo, cada exclusão com o
motivo nomeado, e a 63a lida do YAML (esta última, feita em 24/10; falta o resto da parte 2).

## P-17 · C-04 e C-05 nomeados; o limiar do C-05 sai da contagem (27c)

**Dono:** Osvaldo (o limiar, bloco 27) · Claude Code (gravá-lo no YAML) · **Gatilho:** antes de
ligar o corte do C-05 no bloco C (P-30) · **Classe:** `DECISAO_DE_DESENHO` *(era
`BLOQUEIA_O_SISTEMA` até 10/10: a identidade caiu na leitura, e o bloco C roda sem o corte)*

**Feito em 10/10/2026** (`politica.yaml` 1.40.0, `bloco_C_solvencia.campos_C04_C05`, guarda
`alocacao/test_p17_c04_c05.py`): os dois lidos no escopo e reconciliados com o YAML.
**C-04**, moeda da dívida × moeda da receita: Fase B, nota de instrumentos financeiros;
`NAO_CONSERTADA` com `pendencia: P-65`, e até lá marca "C-04 não medido" e nunca exclui (P6).
**C-05**, caixa / dívida de curto prazo: Fase A, balanço estruturado; calcula e marca. O escopo
não dá limiar como regra: o "caixa < dívida CP" é o exemplo do bloco L, e a §7 dele diz que
nenhum limiar aparece no documento. Medido de passagem: o metadado do FRE estruturado da CVM não
tem campo de moeda (730 campos), então o "exige o FRE" da Fase B não resolve o C-04 pelo CSV.
**16/10/2026: ele respondeu 27c** (fila, bloco 27): o limiar sai da contagem do bloco C em 0,5 ·
1,0 · 1,5, só o número de empresas, e até lá o C-05 marca e não corta. **24/10/2026: ele estendeu o 27c a C-01, C-02 e C-03** (fila, bloco 27, pelo formulário no
claude.ai): os quatro marcam e não cortam até a contagem. A grade de cada um está em
`bloco_C_solvencia.metricas.C-0x.grade` (C-05: 0,5 · 1,0 · 1,5, dele; C-01, C-02 e C-03: três
pontos de Claude, cada um com fonte e "não é corte"), e a contagem existe como função e como
medição (P-30). O C-02 não entra na contagem enquanto a P-185 não escrever a fórmula.
**Fecha com:** a contagem
rodada na P-30, a escolha dele vendo ela, e o limiar gravado no `campos_C04_C05.C-05.limiar` (e
em `metricas.C-01` a `C-03`) com impressão digital.

## P-58 a P-61 · Regimes de leitura de balanço: o portão de regime tem 2 saídas e precisa de N

**Dono:** Claude Code (desenho) · Osvaldo (o que só ele responde, §6 do documento) ·
**Gatilho:** a P-18 fechada (24/10/2026) e a parte 1 da P-30 · **Classe:** `BLOQUEIA_O_SISTEMA`
*(dono dado na triagem de 03/10/2026, P-171)*

`docs/auditoria/regimes-de-leitura-de-balanco.md`. Um regime para banco e **um para "todo o
resto"**, que lê incorporadora e WEG com a mesma régua. **P-58**, as saídas (incorporação,
concessão, propriedade para renda, IFRS 16); **P-59**, o C-01 exclui empresa em fase de
investimento; **P-60**, ROIC contra custo da dívida não existe; **P-61**, capex de manutenção
contra expansão (limitação, viés contra quem cresce). A porta de entrada é a DFC, não a DRE.
Construção civil **não sai do universo** (P6). **Fecha com:** o portão com N saídas, cada uma
com regra no YAML, e as respostas dele registradas como decisão dele.

## P-185 · A fórmula do C-02 (dívida líquida / EBITDA): o escopo diz "Padrão"

**Dono:** Osvaldo (decide a fórmula do EBITDA e da dívida líquida) · Claude Code (escreve no YAML e
implementa) · **Gatilho:** antes de a contagem do 27c incluir o C-02 · **Classe:**
`DECISAO_DE_DESENHO`

O escopo (`docs/auditoria/escopo-campos-de-analise.md`, §4) traz "Padrão" na coluna da fórmula do
C-02, e a §1 do mesmo documento exige fórmula explícita. EBITDA não é conta do plano da CVM: a
depreciação e a amortização não têm `CD_CONTA` único, e as variantes (impairment, equivalência
patrimonial, itens não recorrentes) mudam o número. Em 24/10/2026 o bloco C marcou o C-02
`NAO_IMPLEMENTADA` (`metricas.C-02`) em vez de escolher uma. A dívida líquida tem a mesma questão
da composição do caixa (`operandos.caixa`). **Fecha com:** a fórmula escrita no YAML, com as
contas, implementada com teste, e o C-02 entrando na contagem.

## P-65 · A segunda esteira: notas explicativas e IPE — decidida (65b), entra depois do bloco C (23a)

**Dono:** Claude Code (construir) · **Gatilho:** o bloco C rodando sobre o acervo (P-30) —
resposta 23a dele, 10/10/2026 · **Classe:** `BLOQUEIA_O_SISTEMA`

Achado X-01: dos dez passos da leitura dele, 3 saem do dado estruturado e 7 não. **Decisão dele,
26/09: 65b, construir já**, só com extração **determinística** (todo número com trecho, posição
e sha256 da origem; número sem trecho é recusado, P1), começando por medir o formato do
Empresas.NET. **Nenhum PR em oito dias** (0 de 47, de #13 a #59): é o achado IP-01. **Onde ela
entra, decidido em 10/10 (fila, bloco 23, 23a): depois do bloco C**, porque o consumidor dela é
o dossiê (P-64), que lê a lista curta que o bloco C produz. A 65b muda de quando, não de se nem
de condição. O C-04 (moeda da dívida) espera por ela: `politica.yaml →
bloco_C_solvencia.campos_C04_C05.C-04`, `pendencia: P-65`. **Fecha com:** o formato medido e a
primeira extração com procedência, na posição que ele deu (23a).

## P-127 · Oráculo externo do preço ajustado — em paralelo, sem bloquear

**Dono:** Claude (pesquisa e pré-registro) · Osvaldo (fornecedor, se tiver custo) · **Gatilho:**
qualquer sessão de motor com folga; nunca na frente da §3 do `PLANO.md` · **Classe:**
`DECISAO_DE_DESENHO`

**127a, decisão dele de 26/09:** um agregador de preço ajustado como **controle** numa amostra,
nunca como feed (rebaixaria a P1). O critério de "concordam" gravado e empurrado antes de olhar
(P4, P-116); os termos do fornecedor lidos na fonte; os nomes dos relatórios estão
`NAO_CONFIRMADO`. **Decisão de 03/10:** corre em paralelo e não bloqueia o caminho crítico.
**Fecha com:** a divergência medida numa amostra pré-registrada, que vira o `o_que_resolveria`
da P-180.

## P-181 · O M1 nunca foi usado: a porta de uso e o primeiro uso real, do começo ao fim

**Dono:** Claude Code (a porta e o roteiro) · Osvaldo (usar) · **Gatilho:** agora; o aporte
seguinte dele é o teste · **Classe:** `BLOQUEIA_O_SISTEMA`

Decisão dele, 03/10/2026: ele nunca usou o sistema e não o considera funcional, e **"pronto"
passa a exigir uso real por ele, do começo ao fim**. Medido na triagem (`grep`, 03/10): dos três
módulos que leem o `estado.yaml` (`aporte.py`, `reserva.py`, `estado_io.py`), **nenhum chama
`alocar()` nem `motor_aporte()`**; o `demo_aporte.py` usa um `Estado` escrito no código. Não há
como ele pedir "o que faço com o aporte deste mês". O que fecha, em ordem: (1) um comando que lê
o `estado.yaml` e devolve quanto, para onde e por quê, com a procedência e os portões que
eliminaram cada rota, nascido com teste sobre um estado sintético; (2) ele usa num aporte real,
sem a sessão no meio; (3) cada passo em que travou vira pendência com o nome do passo.
Nenhum número dele entra no repositório (o `estado.yaml` é privado, P-67).

**(1) feito em 10/10/2026:** `alocacao/aporte_do_mes.py`, testado sobre estados sintéticos em
`alocacao/test_aporte_do_mes.py`. Lê o `estado.yaml` pela mesma porta (`estado_io.validar`, com
o CX-04), roda `alocar()` e `motor_aporte()`, e responde em três blocos: o que fazer, por quê
(com cada rota de fora e o portão que a tirou) e de onde veio cada número. O PU do Tesouro Selic
vem do CSV do Tesouro Transparente, com data e sha256; preço de ETF a pessoa informa
(`--preco`). Sem o preço de uma rota em lote que o motor consultou, o comando recusa e pede
esse preço (P-182). O roteiro do uso, passo a passo, é
[`docs/uso/aporte-do-mes.md`](docs/uso/aporte-do-mes.md). **Falta (2) e (3).**

## P-179 · O catálogo não conhece o investimento mínimo do Tesouro, e o primeiro aporte pode sair inexecutável

**Dono:** Osvaldo (decide se o mínimo entra no "caber") · Claude (lê a fonte e modela) ·
**Gatilho:** antes de o protótipo F1 mostrar uma ordem de primeiro aporte · **Classe:**
`DECISAO_DE_DESENHO`

*Ativa pela frente "primeiro uso" (P-181, `PLANO.md` §4): o primeiro aporte real dele pode
cair nela antes de qualquer protótipo.*

Visto ao lado da P-164 (03/10); não é achado: nenhum arquivo afirma que o mínimo é modelado. O "caber" do primeiro aporte usa as verificações que o motor
já tem, por decisão dele: lote inteiro e G3. A `td_selic` tem `negocia_em_lote: false` e
nenhum piso no `catalogo.yaml`, então para ela o lote é qualquer valor positivo. No
instantâneo dourado da P-164, um aporte de **R$ 40** com patrimônio zero vira uma ordem de
R$ 40 em Tesouro Selic (n=6 cenários, com e sem rotas). O Tesouro Direto tem investimento
mínimo por título: o valor exato e a regra (fração do título com piso em reais) estão
`NAO_CONFIRMADO` aqui, e quem confirma é a leitura da fonte primária do Tesouro Nacional, não a
memória de quem escreve. Se o mínimo for maior que o aporte, a ordem não se executa, e a tela
diria "compre" onde a casa recusa.

Junto, e menor: o nome da rota é **"Tesouro Selic acima de R$10k"**, e é ele que o `porque` do
primeiro aporte mostra para um aporte de R$ 500. O nome descreve o regime de custo da rota, e
o leigo o lê como condição de entrada.

**Decidida em 04/10/2026, pelo formulário: o mínimo entra no "caber", como lote** (fila, bloco
26). Lido na fonte primária em 10/10 (tesourodireto.com.br, "Regras e regulamento", item 9): as
aplicações tradicionais são múltiplas de **0,01 título**. Feito: `td_selic` e `td_ipca` com
`negocia_em_lote: true` e `lote_fracao: 0.01` no `catalogo.yaml`, e `preco_do_lote()` converte o
PU do dia no preço de um lote (`alocacao/test_p179_minimo_do_tesouro.py`: R$ 40 não compram
Tesouro Selic; R$ 500 compram 0,02 título e o resto vai para o caixa). O `td_reserva` ficou sem
lote: a regra dele não foi lida (`NAO_CONFIRMADO` na procedência).

**O que falta para fechar:** (1) o PU do dia chegar ao motor com data e hash, sem ninguém
digitar: a porta de uso (P-181) o lê do CSV do Tesouro Transparente; a forma P7 é a captura
diária; (2) o nome que a tela mostra para a `td_selic` ("acima de R$10k" é o regime de custo,
e o leigo lê como condição de entrada); (3) a regra de mínimo do Tesouro Reserva, lida na fonte.

## P-162 · Teste de marca das direções visuais (H1 a H3)

**Dono:** Osvaldo (pôr no ar, recrutar) · Claude (análise) · **Gatilho:** a página no ar e o
commit das datas da janela · **Classe:** `DECISAO_DE_DESENHO`

Etapa 3 do rosto. O pré-registro que vale é o
[final 2](docs/marca/teste-de-marca/preregistro-final.md), com o questionário, o livro de
códigos e a análise congelados pelo sha256 (a v1, com Google Forms, ficou superada sem uso). A
página está em `pesquisa/`, sem deploy e sem resposta real. **O que falta é dele:** o roteiro em
[`docs/marca/teste-de-marca/roteiro-no-ar.md`](docs/marca/teste-de-marca/roteiro-no-ar.md),
depois o commit das datas, e só então o primeiro convite. A direção só sai com a R3 fechada
(P-170). A H4 foi para a P-156. **04/10:** o passo 0 (plano da Vercel) foi decidido por ele,
**24b** (Hobby, com a leitura escrita na fila); o roteiro virou tutorial numerado, com o commit
das datas e o texto do convite, e o sha256 que o passo 5 manda conferir foi corrigido para o da
y-a (`02773d8b…`; retratação no roteiro). **Fecha com:** o relatório da análise, depois do dia 21.

## P-170 · A rodada 3 de marcas (R3), visual, para o veto de distinção

**Dono:** Claude (visitar e classificar) · Osvaldo (o veto, se disparar) · **Gatilho:** corre em
paralelo à coleta da P-162; as visitas já podem começar (o sorteio está no `main`, #45) ·
**Classe:** `DECISAO_DE_DESENHO`

Livro de códigos v3 (onze categorias, 10 marcas sorteadas por categoria, semente 20261002; a v3 é a ag-b, de 04/10, a luminosidade do matiz),
plano em [`docs/marca/rodada3/`](docs/marca/rodada3/plano.yaml), andamento em
`docs/marca/pesquisa-marcas-rodada3-2026-09.md` §5. **11/10:** 413 marcas lidas, 85 classificadas,
as 10 da af-a em oito categorias (os universos de bancos, pagamentos e casas de análise saíram de
cadastro oficial, §2) e **nenhum código dominante em categoria nenhuma** (`rodada3/veto.md`);
robô, consolidador e planejador **sem universo**, com a escada transcrita (§2.1; decisão dele, fila
28). ~~Falta o que a nuvem não alcança: 83 linhas `AGUARDA DEGRAU 4` [...], na máquina dele.~~
**16/10 (sessão local, §3.3 da pesquisa):** as 83, e mais 6 que a guarda nova achou sem o status,
saíram pela loja (ae-a: 60 das 89 marcas tinham app) e pelo degrau 4 em ordem (4a o servidor do
GitHub, 4b o `br-sp`, que não existe, 4c esta sessão); **nenhuma linha espera a máquina dele**
(guarda `auditoria/test_degrau4.py`). A amostra se refez pela ordem do sorteio (plano v3): 10 em
cada categoria de cadastro, consolidador 5 e robô 1 pelo quadro da loja (fila 28), e **nenhum
código dominante** em categoria nenhuma (`rodada3/veto.md`). ~~Falta o Wayback das 86 classificadas~~
**19/10/2026: 80 de 86 com link do Wayback**, pelo degrau 4 em ordem (`arquivar_r3.yml` no servidor
do GitHub: 25 no run 38944870464 e 1 no 39246785988; esta sessão, 4c: 54). As 6 que faltam (WCIA,
Agibank, Desmistificando, C6, Crefisa, Rendimento) recusaram do lado do Save Page Now (conexão
recusada, 520, 429), não do site, e cada uma leva a escada e o próximo executor (uma nova rodada
do 4c fora do limite de frequência). Falta também o planejador (fila 28c, dele). Só página
pública; nada de sessão logada (§5-A.7); recusa sobe a escada (§5-B.18). **Fecha com:** o
arquivamento, uma linha por marca (categoria, captura com fonte e data, medidas do `classificar()`)
e o `veto()` aplicado à direção vencedora. **E, no mesmo commit do fechamento,** sai o
`instrumento_r3` do `pyproject.toml` e o `ignore` do `playwright` no `dependabot.yml`
(`docs/decisoes/R3-instrumento-playwright.md`).

---

## Ao voltar ao desktop

*Encurtada em 03/10/2026: só o que está vivo. A versão anterior, inteira, está no histórico das
ativas.*

**Da sessão local (sem ele):**

1. **P-145, depois do item 4:** `py -3.11 medicoes/p145_ponte_2013_2019.py` e o PR com os
   inventários que o envio gravou. É o passo 1 do caminho crítico.
2. ~~**P-170, as 83 linhas paradas da R3**~~ (16/10: resolvidas pela loja e pela escada em
   ordem; §3.3 da pesquisa). ~~**O Wayback das 86**~~ (19/10: 80 de 86 pelo `arquivar_r3.yml` e
   pelo 4c; as 6 que faltam levam a escada e o próximo executor no CSV). As capturas das 85 de 10 e
   11/10 (12 MB, enviadas por arquivo em 11/10) continuam sem descompactar nesta máquina; as de
   16/10 estão em `data/r3/capturas/` do worktree `Bastter-p170-appstore` (fora do git).
3. **P-05 e P-169, o degrau 4 da escada:** `curl` de IP residencial no site do BOVV11 e nas
   páginas dos 11 bancos da regra m-B (os roteiros estão no texto das duas, na reserva).

**Dele:**

4. **O envio ao R2, que destrava a P-145 e a parte 1 da P-150:** com as `R2_*` no ambiente,
   `py -3.11 fase0/subir_acervo_local.py --aplicar`. O plano de 04/10 deu 393 `SUBIR`, 0
   `PARAR`, 0 `DESCONHECIDO` (1.583 MiB), com o `isinp.zip` e os eventos de 11/09. Depois, os
   `inventario-armazem.csv` que ele gravar vão para um commit (a sessão faz).
5. **P-115, os PDFs do D1 no armazém:** baixar as 10 provas pelas URLs de
   `docs/fontes/jcp-amostra-2016-2020.md`, conferir cada sha256 contra a tabela e subir; do 20-F
   da Gerdau, o documento arquivado (sha256 `20f8599e…b512`).
6. **Token do R2 somente leitura** e os quatro segredos `R2_LEITURA_*` (fila, "Conferência de
   um minuto"): destrava toda medição na nuvem. A P-145 na sessão local não precisa dele.
7. **P-162, a página no ar:** `docs/marca/teste-de-marca/roteiro-no-ar.md`. Nada exige o desktop
   além do passo 6.
8. ~~**Instruções do Projeto no claude.ai:** colar a versão 4 de
   `docs/ia/instrucoes-projeto-claude.md`~~ **Feito; conferido em 16/10/2026:** o texto que ele
   colou na sessão é idêntico, linha a linha, à seção copiável da versão 4 (a ordem dos
   executores na escada).
9. **Fila 28c, o planejador da R3 (sem prazo):** abrir a busca da Planejar (certificação CFP) num
   navegador e exportar a lista uma vez; a sessão monta o universo a partir dela. O reCAPTCHA de
   caixa de seleção não se contorna (pesquisa da R3, §2.1).