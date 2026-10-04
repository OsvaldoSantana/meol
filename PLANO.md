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
| **M1 · decidir o aporte** | dizer quanto entra, em qual classe e por qual rota, com custo, imposto e nove portões nomeados | **código pronto, nunca usado.** Ele nunca usou o sistema e não o considera funcional. E não há porta de uso: dos três módulos que leem o `estado.yaml` (`aporte.py`, `reserva.py`, `estado_io.py`), nenhum chama `alocar()` nem `motor_aporte()` (`grep`, 03/10). Frente "primeiro uso", §4 |
| **M2 · decidir com dado próprio** | ler balanço do acervo próprio, sem terceiro nem tela | **em andamento.** CVM (DFP, ITR, CAD), COTAHIST e eventos da B3 no armazém; nada disso é lido ainda como balanço. Caminho crítico, §3 |
| **M3 · decidir o papel** | aplicar régua de empresa pré-registrada e medida, com o corte da família de testes | **bloqueado em M2.** M3 sem M2 é backtest sobre dado de outra pessoa (*look-ahead* contábil) |
| **M4 · fazer isso sozinho** | capturar sem ninguém lembrar e acusar a falha | **feito.** `captura_cvm.yml`, diário desde 24/09: CVM, COTAHIST (diário e anual mensal), NEFIN (desde 26/09, P-147 fechada), eventos da B3 às segundas (desde 28/09) e a conciliação mensal (setembro: 10 `CONFERE`, nenhuma falta). Parada levanta `CapturaParada`. Sobra a formalidade dos eventos em `regimes_de_captura` (P-150, reserva) |

**A série ajustada do COTAHIST não é marco.** O C-02 saiu `NAO_CONFIRMADA` em 2016–2020 (P-115,
opção A): K2 e K3 sem poder, e nenhuma janela do acervo dá ao K2 o n que ele pede (PO-01, PO-02).
Por decisão de 03/10 ela vira **limitação declarada** (P-180), e o oráculo externo (P-127) corre
em paralelo, sem bloquear nada.

## 3. Caminho crítico — o motor (decisão de 03/10)

**M2 pela CVM:** ponte → bitemporalidade → bloco C. Cada passo destrava o seguinte e nenhum
depende de dado de usuário.

| # | passo | destrava | o que impede hoje |
|---|---|---|---|
| 1 | **Ponte ticker → CD_CVM de 2013–2019** (P-145). A medição existe: `medicoes/p145_ponte_2013_2019.py` | o universo com CD_CVM, sem o qual DFP/ITR não se liga a papel; e os 13 eventos sem ticker (P-93) | **nada na sessão local:** o `isinp.zip` de 25/09 está no disco dele, e o `acervo.abrir` lê de lá. Na nuvem, faltam dois passos dele (token R2 de leitura, `isinp.zip` no armazém) |
| 2 | **Bitemporalidade** `dt_captura` × `DT_REFER`: DFP/ITR lidos *as-of*, com duas regras já escritas: só `ÚLTIMO`, partição pelo ano do arquivo (P-51); Parquet imutável e consulta DuckDB, ponte também bitemporal (P-53) | o direito de dizer que o backtest não vaza futuro | o passo 1 |
| 3 | **Bloco C sobre dado real** (P-30): primeiro portão que olha empresa, e é de **exclusão**, não de ordenação. Vão junto: C-04 e C-05 (P-17, o escopo já está no repositório), a contagem de `SETOR_ATIV` (P-18), os regimes de leitura (P-58 a P-61), portão × dossiê (P-64) e, por métrica, nível, tendência ou híbrido (63a) | o M3 | o passo 2 |

**Decidida e fora do caminho de 03/10:** a P-65, segunda esteira (notas explicativas e IPE),
**65b, "construir já"**, de 26/09. Ficou oito dias sem nenhum PR (0 de 47, IP-01). Onde ela
entra é decisão dele (§6).

## 4. Frente "primeiro uso" (decisão de 03/10)

O M1 só fecha quando ele usar o sistema num aporte real, do começo ao fim, sem a sessão no meio.
Conta como sessão de motor no ritmo da §5.

1. **Uma porta de uso** (P-181): um comando que lê o `estado.yaml` e devolve o "quanto, para
   onde e por quê" do mês, com a procedência. Hoje não existe (§2).
2. **Ele usa** no aporte seguinte. Cada passo em que travar vira pendência com o nome do passo;
   o que ele não entender é defeito do sistema, não dele.
3. **P-179**, o investimento mínimo do Tesouro: o primeiro aporte (P-164, fechada em 03/10 com
   a regra **(c)** dele) pode mandar R$ 40 para o Tesouro Selic, e a casa recusar. O mínimo se lê
   na fonte antes de ele usar.

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
| 3 · mercado | **P-162**, teste de marca | pré-registro e página prontos; pôr no ar e o commit das datas são dele |
| 3 · mercado | **P-170**, rodada 3 de marcas (veto de distinção) | sorteio gravado; visitas a fazer. A direção só sai com ela fechada |
| 3 · mercado | P-153, P-154; posicionamento e tom | reserva; o tom depois da P-162 |
| 4 · UX | mapa v2 (P-160); esquema da F0; P-167 (WCAG); protótipo F1, F3, F6; P-156 | mapa depois da P-162; o veredito da F0 (item 20) está no PR #59, ainda aberto |
| 5 · brandbook | brandbook, P-168 | P-155, P-162 e P-156 fechadas |

**Portão que vale sempre:** P-158 (parecer jurídico) antes de qualquer usuário além dele ou de
texto comercial público.

## 6. Bloqueios e decisões abertas

**Bloqueios reais, três:**

1. **O M1 não tem porta de uso** (P-181). Sem ela, "primeiro uso" é impossível, não adiado.
2. **A bitemporalidade não existe em código** (passo 2 da §3).
3. **A ponte de 2013–2019 não foi medida** (P-145). Na sessão local, nada a impede.

**Decisões dele, abertas:**

| decisão | onde | o que muda |
|---|---|---|
| onde entra a P-65 (65b) no caminho de 03/10 | fila, bloco 23 | se a segunda esteira disputa vaga com a bitemporalidade, ou espera o bloco C |
| se o mínimo do Tesouro entra no "caber" do primeiro aporte | P-179 | ordem executável ou aviso na ordem |
| o `PLANO.md` continua na abertura | P-172, em 17/10 | abertura de ~21,0 mil tokens com ele, ~18,2 mil sem ele (medido em 03/10) |
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
