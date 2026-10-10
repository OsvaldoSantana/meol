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

## P-51 · Só `ÚLTIMO`, e a partição é o ano do arquivo — regra do leitor da CVM

**Dono:** Claude · **Gatilho:** ao escrever o leitor de DFP/ITR (passo 2 do caminho crítico) ·
**Classe:** `BLOQUEIA_O_SISTEMA`

`PENÚLTIMO` é o ano anterior já reapresentado: usar a linha `PENÚLTIMO` do arquivo de 2025 para
saber o que se sabia em 2024 é *look-ahead*. O leitor usa **só `ÚLTIMO`, do arquivo daquele
ano**, e particiona pelo **ano do arquivo**, não do dado (o DFP de 2025 corrige 2023).
**Fecha com:** o leitor e um teste que falha se uma linha `PENÚLTIMO` entrar na série.

## P-53 · O acervo lido não depende de engine, e a ponte também é bitemporal

**Dono:** Claude · **Gatilho:** ao escrever a bitemporalidade (passo 2) · **Classe:**
`DECISAO_DE_DESENHO`

Recomendação da pesquisa (`docs/fontes/pesquisa-bases-e-apis-2026-09.md` §3): **Parquet
imutável particionado por `dt_captura`, DuckDB como consulta**, e o `.duckdb` sempre
reconstruível, nunca registro. Duas armadilhas que entram no desenho: `dt_captura` não é data de
conhecimento do mercado, e **o mapeamento ticker ↔ CNPJ ↔ CD_CVM também precisa ser
bitemporal**, senão o join vaza futuro. Hoje o byte de cada versão já está no armazém por sha256
(M4); o que falta é a camada de leitura. **Fecha com:** a consulta *as-of* sobre DFP/ITR e um
teste com duas versões do mesmo `DT_REFER` capturadas em dias diferentes.

## P-30 · O bloco C sobre dado real — o passo 3 do caminho crítico

**Dono:** Claude Code · **Gatilho:** a bitemporalidade pronta (P-53) · **Classe:**
`BLOQUEIA_O_SISTEMA` *(campos dados na triagem de 03/10/2026, P-171)*

`bloco_C_solvencia` tem 48 chaves escritas em 05/09, e nenhum módulo as aplica: os testes
conferem o texto, não o comportamento. É o primeiro portão que olha empresa, e é de **exclusão**
(`criterio_nao_e_previsao`). **Leva a 63a** (decisão dele, 26/09): cada métrica declara no YAML
se lê nível, tendência ou híbrido. Dependem dela P-17, P-18, P-58 a P-61 e P-64; o regime de
banco é a P-31, na reserva. **Fecha com:** o bloco rodando sobre o acervo, cada exclusão com o
motivo nomeado, e a 63a lida do YAML.

## P-17 · C-04 e C-05 nunca foram nomeados — o escopo já está no repositório

**Dono:** Claude Code · **Gatilho:** antes de codificar o bloco C (P-30) · **Classe:**
`BLOQUEIA_O_SISTEMA` *(campos dados na triagem de 03/10/2026, P-171)*

O `politica.yaml` cita C-04 e C-05 como existentes e nunca os nomeia. A lista vive em
`docs/auditoria/escopo-campos-de-analise.md`, que **já está no repositório** (conferido em
03/10): o "exige o desktop" de antes não vale mais. Bloco de exclusão com critério inventado
excluiria por regra que ninguém escolheu. **Fecha com:** os dois lidos e reconciliados com o YAML.

## P-18 · `SETOR_ATIV` da CVM nunca foi contado

**Dono:** Claude Code (sessão local, ou `medir/`) · **Gatilho:** antes de codificar a separação
de instituição financeira no bloco C · **Classe:** `BLOQUEIA_O_SISTEMA` *(campos dados na
triagem de 03/10/2026, P-171)*

O bloco C manda banco para regime próprio, e a identificação sai do `SETOR_ATIV` do cadastro.
Só dois valores foram vistos; a enumeração nunca foi contada no dado real, como `ORDEM_EXERC` e
`ESCALA_MOEDA` foram. **Fecha com:** a enumeração `OBSERVADO` no YAML, e o leitor falhando
ruidosamente fora dela (P1).

## P-58 a P-61 · Regimes de leitura de balanço: o portão de regime tem 2 saídas e precisa de N

**Dono:** Claude Code (desenho) · Osvaldo (o que só ele responde, §6 do documento) ·
**Gatilho:** depois da P-18 · **Classe:** `BLOQUEIA_O_SISTEMA` *(dono dado na triagem de
03/10/2026, P-171)*

`docs/auditoria/regimes-de-leitura-de-balanco.md`. Um regime para banco e **um para "todo o
resto"**, que lê incorporadora e WEG com a mesma régua. **P-58**, as saídas (incorporação,
concessão, propriedade para renda, IFRS 16); **P-59**, o C-01 exclui empresa em fase de
investimento; **P-60**, ROIC contra custo da dívida não existe; **P-61**, capex de manutenção
contra expansão (limitação, viés contra quem cresce). A porta de entrada é a DFC, não a DRE.
Construção civil **não sai do universo** (P6). **Fecha com:** o portão com N saídas, cada uma
com regra no YAML, e as respostas dele registradas como decisão dele.

## P-64 · Portão × dossiê — a camada de desenho que o bloco C precisa

**Dono:** Claude · **Gatilho:** antes de implementar qualquer regime (P-58) · **Classe:**
`BLOQUEIA_O_SISTEMA`

O portão é automático, sobre todo o universo, e só com dado estruturado. O dossiê é leitura
guiada, empresa a empresa, só na lista curta. Onde o dado não existe (incorporação, X-01), o
portão só diz *"regime X, exige dossiê; até lá fica no universo sem peso deste bloco"*. Vale para
todo regime. Os cortes de distrato (P-66, na reserva) entram junto. **Fecha com:** a saída
`EXIGE_DOSSIE` no portão, com o motivo, e um teste que prova que ela não tira ninguém do universo.

## P-65 · A segunda esteira: notas explicativas e IPE — decidida (65b) e sem lugar no caminho

**Dono:** Claude Code (construir) · Osvaldo (onde ela entra, fila, bloco 23) · **Gatilho:** a
resposta dele ao bloco 23 · **Classe:** `BLOQUEIA_O_SISTEMA`

Achado X-01: dos dez passos da leitura dele, 3 saem do dado estruturado e 7 não. **Decisão dele,
26/09: 65b, construir já**, só com extração **determinística** (todo número com trecho, posição
e sha256 da origem; número sem trecho é recusado, P1), começando por medir o formato do
Empresas.NET. **Nenhum PR em oito dias** (0 de 47, de #13 a #59): é o achado IP-01. O caminho
crítico de 03/10 não a nomeia, e escolher entre os dois não é da sessão. **Fecha com:** o formato
medido e a primeira extração com procedência, na posição que ele der.

## P-180 · A série ajustada do COTAHIST vira limitação declarada

**Dono:** Claude Code · **Gatilho:** a próxima sessão de motor, antes de qualquer conta que use
a série · **Classe:** `BLOQUEIA_O_SISTEMA`

Decisão dele, 03/10/2026, depois da P-115 `NAO_CONFIRMADA` (opção A). A série segue no acervo e
no código; o que muda é o status: nenhuma conta a usa como confirmada. A entrada vai para
`politica.yaml → limitacoes_declaradas`, pelo protocolo de mudança (versão e changelog). O que
ela diz: o C-02 não confirmou o ajuste em 2016–2020 (K2 e K3 sem poder; PO-01, PO-02); a direção
do viés é desconhecida; o que resolveria é um controle independente (a P-127). Os consertos de
série que estão na reserva (P-93, P-94, P-101, P-112) ficam lá, ligados a ela.
**Fecha com:** a entrada no YAML, `NAO_CONSERTADA` com `pendencia: P-127`, e o
`test_limitacoes_tipo.py` verde.

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
`docs/marca/pesquisa-marcas-rodada3-2026-09.md` §5. **04/10:** 51 visitadas, 34 classificadas
(consultoria CVM e assessor com as 10), nenhum código dominante ainda; corretora e gestora
dependem do degrau 4 (bloqueio para o IP da nuvem, §3.1 de lá), as 34 aguardam o Wayback
(`tools/r3_arquivar.py`, na máquina dele), e sete categorias seguem sem universo. Só página
pública; nada de sessão logada (§5-A.7); recusa sobe a escada (§5-B.18). **Fecha com:** uma linha
por marca (categoria, captura com fonte e data, medidas do `classificar()`) e o `veto()` aplicado
à direção vencedora.

## P-172 · O PLANO.md na abertura volta à decisão em 17/10

**Dono:** Osvaldo (decidir) · Claude Code (levar os números) · **Gatilho:** 17/10/2026, com duas
semanas de dado da regra de volta · **Classe:** `DECISAO_DE_DESENHO`

Resposta 22a de 03/10: o `PLANO.md` segue na abertura. Na mesma data ele foi reescrito curto
(dieta de 03/10), e a pergunta de 17/10 fica menor. A sessão de 17/10 leva: a tabela da regra de
volta (`python auditoria/metricas_processo.py --prs prs.json`, com `gh pr list --state merged
--base main --json number,title,mergedAt,author`) e os semanais de 05/10 e 12/10; o tamanho da
abertura (`python auditoria/tamanho_do_contexto.py`); e se o piso da 21d ficou alto demais para o
`registro` (limiar 0,21 com referência 1/7).

---

## Ao voltar ao desktop

*Encurtada em 03/10/2026: só o que está vivo. A versão anterior, inteira, está no histórico das
ativas.*

**Da sessão local (sem ele):**

1. **P-145, depois do item 4:** `py -3.11 medicoes/p145_ponte_2013_2019.py` e o PR com os
   inventários que o envio gravou. É o passo 1 do caminho crítico.
2. **P-170, o degrau 4 da R3:** a lista da §3.1 de `docs/marca/pesquisa-marcas-rodada3-2026-09.md`
   (capturas que a nuvem não abre e o resto da ordem de corretora), depois
   `py -3.11 tools/r3_arquivar.py` e `python tools/r3_dominante.py`. As capturas da nuvem estão
   em `data/r3/capturas/` da pasta dele (copiadas pela sessão de 04/10).
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
8. **Instruções do Projeto no claude.ai:** colar a versão 2 de
   `docs/ia/instrucoes-projeto-claude.md` (a escada de contorno), se ainda não foi colada.
