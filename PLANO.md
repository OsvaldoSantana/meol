# PLANO.md — destino, marcos e a ordem do que falta

*Reescrito em 03/10/2026 por decisão dele (dieta completa do processo). O anterior, inteiro e com
a lista do que ele afirmava errado, está em
[`docs/historico/plano-ate-2026-10-03.md`](docs/historico/plano-ate-2026-10-03.md).* Este arquivo
ganha de qualquer fila (`CLAUDE.md` §1). Se discordar do `PENDENCIAS.md` sobre o que vem
primeiro, um dos dois está com defeito, e corrige-se no mesmo dia.

## 1. Destino

> A cada aporte, o sistema diz **quanto** vai **para onde** (e, quando a régua existir, **para
> qual papel**), com **procedência em cada número**: de onde ele veio, quem escolheu a regra, e
> o que aconteceria se a escolha fosse outra.

**Limitação de hoje (P5):** decide classe e rota, ainda não papel. A régua de empresa depende do
dado da CVM lido (M2) e do backtest que ele destrava (M3). É lacuna com caminho, não recusa
(decisão dele de 18/09).

**Não é** otimizador (DeMiguel, Garlappi & Uppal, 2009) nem robô que opera: o sistema decide e
registra, e a ordem é dele.

## 2. Marcos, com o estado medido

**"Pronto" exige uso real por ele, do começo ao fim** (decisão de 03/10). Código com teste verde
é "código pronto", e o marco não fecha nisso.

| marco | o sistema passa a | estado em 03/10/2026 |
|---|---|---|
| **M1 · decidir o aporte** | dizer quanto entra, em qual classe e por qual rota, com custo, imposto e nove portões nomeados | **código pronto e porta de uso pronta, nunca usado.** Ele nunca usou o sistema e não o considera funcional. A porta existe desde 10/10: `alocacao/aporte_do_mes.py` lê o `estado.yaml` e devolve o quanto, o para onde e o porquê (P-181). Falta o uso real. Frente "primeiro uso", §4 |
| **M2 · decidir com dado próprio** | ler balanço do acervo próprio, sem terceiro nem tela | **em andamento.** CVM (DFP, ITR, CAD), COTAHIST e eventos da B3 no armazém; DFP/ITR já se leem *as-of* (`fase0/leitor_cvm.py`, 10/10); desde 16/10 também de 2010 em diante, pelo `DT_RECEB` (P-183), com 0,4% de documento-meses ocultos (P-184). Caminho crítico, §3 |
| **M3 · decidir o papel** | aplicar régua de empresa pré-registrada e medida, com o corte da família de testes | **bloqueado em M2.** M3 sem M2 é backtest sobre dado de outra pessoa (*look-ahead* contábil) |
| **M4 · fazer isso sozinho** | capturar sem ninguém lembrar e acusar a falha | **feito.** `captura_cvm.yml`, diário desde 24/09: CVM, COTAHIST (diário e anual mensal), NEFIN (desde 26/09, P-147 fechada), eventos da B3 às segundas (desde 28/09) e a conciliação mensal (setembro: 10 `CONFERE`, nenhuma falta). Parada levanta `CapturaParada`. Sobra a formalidade dos eventos em `regimes_de_captura` (P-150, reserva) |

**A série ajustada do COTAHIST não é marco.** O C-02 saiu `NAO_CONFIRMADA` em 2016–2020 (P-115,
opção A): K2 e K3 sem poder, e nenhuma janela do acervo dá ao K2 o n que ele pede (PO-01, PO-02).
Por decisão de 03/10 ela é **limitação declarada**, registrada em 24/10 (P-180 fechada:
`limitacoes_declaradas.serie_ajustada_do_cotahist_nao_confirmada`, `NAO_CONSERTADA`, política
1.43.0), e nenhuma conta a usa como confirmada. O oráculo externo (P-127) corre em paralelo, sem
bloquear nada.

## 3. Caminho crítico — o motor (decisão de 03/10)

**M2 pela CVM:** ponte → bitemporalidade → bloco C. Cada passo destrava o seguinte e nenhum
depende de dado de usuário.

| # | passo | destrava | o que impede hoje |
|---|---|---|---|
| 1 | **Ponte ticker → CD_CVM de 2013–2019** (P-145). A medição existe: `medicoes/p145_ponte_2013_2019.py` | o universo com CD_CVM, sem o qual DFP/ITR não se liga a papel; e os 13 eventos sem ticker (P-93) | **um passo dele:** o envio ao R2 (`subir_acervo_local.py --aplicar`), que grava o inventário do `isinp.zip`; sem ele o `acervo.abrir` recusa o arquivo do disco (rodado em 04/10). Na nuvem, falta também o token de leitura |
| 2 | **Bitemporalidade** `dt_captura` × `DT_REFER`: DFP/ITR lidos *as-of* (`fase0/leitor_cvm.py`, 10/10): só `ÚLTIMO`, partição pelo ano do arquivo (P-51), versão vigente na `dt_captura` (P-53), sem pacote novo. Começou antes da P-145 por decisão de 10/10 (`docs/decisoes/2026-10-10-leitor-asof-cvm.md`): DFP/ITR são chaveados por `CD_CVM`, e a ponte só entra no join com o papel | o direito de dizer que o backtest não vaza futuro | **o leitor responde desde 24/09/2026 pela captura e, desde 16/10, de 2010 em diante pelo `DT_RECEB` da versão presente (P-183, `conhecimento="dt_receb"`)**, com 14.955 de 3.870.622 documento-meses ocultos (0,4%) até ler a versão substituída no ENET (P-184); para ligar papel, a ponte bitemporal (P-53b), que espera o passo 1 |
| 3 | **Bloco C sobre dado real** (P-30): primeiro portão que olha empresa, e é de **exclusão**, não de ordenação. Vão junto: C-04 e C-05 (P-17: nomeados em 10/10; o C-05 calcula e marca, e o limiar sai da contagem, 27c de 16/10; o C-04 espera a P-65), a contagem de `SETOR_ATIV` (P-18), os regimes de leitura (P-58 a P-61), portão × dossiê (P-64) e, por métrica, nível, tendência ou híbrido (63a). **Feito em 24/10 (parte 1):** `alocacao/bloco_c.py` com as cinco saídas do portão (P-64, fechada), a 63a e a enumeração do `SETOR_ATIV` (P-18, fechada) lidas do YAML, e a contagem do 27c como função; C-01 a C-03 seguem o 27c (decisão dele de 24/10). **Nenhum corte está ativo e o bloco não está ligado ao motor** | o M3 | não é mais o passo 2: o bloco C é por `CD_CVM`, o leitor *as-of* existe (passo 2) e a ponte só entra no join com o papel (P-53b). Falta: a contagem real rodada (precisa do token de leitura `R2_LEITURA_*`), a escolha dele vendo a contagem (P-17), a fórmula do C-02 (P-185) e ligar ao motor (parte 2) |

**Depois do passo 3 (23a, decisão dele de 10/10):** a P-65, segunda esteira (notas explicativas
e IPE), **65b**, de 26/09, só extração determinística. Entra quando o bloco C rodar, porque o
consumidor dela é o dossiê (P-64), que lê a lista curta do bloco C. O C-04 (moeda da dívida)
espera por ela.

## 4. Frente "primeiro uso" (decisão de 03/10)

O M1 só fecha quando ele usar o sistema num aporte real, do começo ao fim, sem a sessão no meio.
Conta como sessão de motor no ritmo da §5.

1. **Uma porta de uso** (P-181): **feita em 10/10.** `py -3.11 alocacao/aporte_do_mes.py` lê o
   `estado.yaml` e devolve o "quanto, para onde e por quê" do mês, com a procedência de cada
   número e o portão que eliminou cada rota. Sem o preço de uma rota em lote, recusa e pede.
2. **Ele usa** no aporte seguinte, pelo roteiro [`docs/uso/aporte-do-mes.md`](docs/uso/aporte-do-mes.md)
   (dez passos). Cada passo em que travar vira pendência com o nome do passo; o que ele não
   entender é defeito do sistema, não dele.
3. **P-179**, o investimento mínimo do Tesouro: **decidida em 04/10 (entra no "caber", como
   lote) e feita em 10/10.** O lote do Tesouro é 0,01 título, lido na fonte primária; com o PU do
   Selic em ~R$ 20 mil, R$ 40 não compram e o aporte cede à próxima rota. Falta o PU do dia
   chegar sem ninguém digitar e o nome que a tela mostra (P-179).

## 5. Ritmo e a fila do rosto

**Duas sessões de motor para uma de rosto** (decisão de 03/10). Motor é a §3 e a §4; rosto é
marca, UX e pesquisa com pessoas. **Registro vai dentro do PR que o gera**, nunca em PR próprio.
O ritmo se confere ao escolher o próximo passo (skill `bastter-proximo-passo`), contando os PRs
mergeados pela etiqueta: **sem guarda automática ainda**, e isso fica declarado aqui.

A ordem do rosto é dele ([`docs/decisoes/rosto-v1.md`](docs/decisoes/rosto-v1.md)): pesquisa →
design → mercado → UX → brandbook. A v1 é estímulo e protótipo sobre dado sintético.

| etapa | item | estado ou portão |
|---|---|---|
| 2 · design | P-166, anterioridade da marca e do domínio | aberta, na reserva |
| 3 · mercado | **P-162**, teste de marca | pré-registro e página prontos; plano da Vercel decidido (24b, 04/10); pôr no ar, o commit das datas e o convite são dele, pelo [roteiro](docs/marca/teste-de-marca/roteiro-no-ar.md) |
| 3 · mercado | **P-170**, rodada 3 de marcas (veto de distinção) | livro v3 (ag-b, 04/10); 85 classificadas em 11/10, as 10 em oito categorias, **nenhum dominante**; faltam o degrau 4 (83 linhas), o Wayback e a decisão sobre as três categorias sem universo (fila 27). A direção só sai com ela fechada |
| 3 · mercado | P-153, P-154; posicionamento e tom | reserva; o tom depois da P-162 |
| 4 · UX | mapa v2 (P-160); esquema da F0; P-167 (WCAG); protótipo F1, F3, F6; P-156 | mapa depois da P-162; o veredito da F0 (item 20) entrou no `main` pelo PR #59, em 03/10 |
| 5 · brandbook | brandbook, P-168 | P-155, P-162 e P-156 fechadas |

**Portão que vale sempre:** P-158 (parecer jurídico) antes de qualquer usuário além dele ou de
texto comercial público.

## 6. Bloqueios e decisões abertas

**Bloqueios reais, dois** (a porta de uso do M1 caiu em 10/10 com a P-181; o leitor *as-of* existe
desde 10/10, e o que falta nele é o histórico):

1. ~~**O leitor *as-of* não responde antes de 24/09/2026** (P-183)~~: responde desde 16/10, pelo
   `DT_RECEB`. O que sobra são 0,4% de documento-meses em que o mercado conhecia uma versão que o
   arquivo não traz mais; o valor dela está no ENET (P-184).
2. **A ponte de 2013–2019 não foi medida** (P-145). Falta o envio ao R2, que é dele.

**Decisões dele, abertas:**

| decisão | onde | o que muda |
|---|---|---|
| o limiar do C-05, **depois da contagem** | 27c (16/10): o bloco C conta quantas empresas sairiam em 0,5 · 1,0 · 1,5, sem nomes | o número que ele grava com impressão digital antes de qualquer backtest |
| parecer jurídico | P-158 | qualquer usuário além dele |

## 7. As pendências

Em 03/10: **76 abertas**, 16 ativas no [`PENDENCIAS.md`](PENDENCIAS.md) (teto 20, lidas em toda
sessão) e 60 em [`docs/pendencias-reserva.md`](docs/pendencias-reserva.md) (por busca). Doze
fecharam na triagem, com a evidência em `docs/historico/pendencias-fechadas.md`. O número do dia
sai do `docs/estado.md`, não daqui.

## 8. Como este arquivo se mantém honesto

1. **Estado medido, com o comando ao lado.** "Pronto" é usado por ele (§2), e "rodando" é a
   execução com número.
2. **Passo feito sai da §3 com a data**, e a narrativa vai para `ACHADOS.md` ou para o histórico.
   Este arquivo não guarda história.
3. **Até ~150 linhas.** Passou disso, está guardando o que não é plano.
4. **Afirmação sobre fonte só com a entrada de `limitacoes_declaradas` lida**, inclusive as
   `RETIRADA` (§5-B.13). O plano anterior repetiu por duas semanas uma limitação retirada no dia
   em que foi escrita; `auditoria/test_plano_e_pendencias.py` prende esse caso.
