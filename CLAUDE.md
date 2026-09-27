# CLAUDE.md

Instruções para qualquer sessão do Claude que trabalhe neste repositório. Leia inteiro, e as
doutrinas em `docs/doutrinas.md`, antes de tocar em código. Se algo aqui contradisser o que
você acha razoável, o arquivo ganha — ou você argumenta contra ele explicitamente, e a conversa
passa a ser sobre mudar o arquivo, não sobre ignorá-lo.

**Este arquivo só guarda o que muda o que alguém faz.** O porquê de cada regra (os incidentes,
as retratações, as rodadas datadas) mora em `docs/historico/claude-md-ate-2026-09.md`; o índice
está na §13. Regra nova entra aqui com uma linha de motivo; a história dela vai para o
histórico ou para o `ACHADOS.md`.

---

## 1. O que é este projeto

Um sistema pessoal de análise e aporte de investimentos, do Osvaldo (engenheiro civil, PJ sem
previdência, contrato único). É **inspirado no Bastter.com e existe para corrigi-lo**: o método
acerta na disciplina e erra ao apresentar como derivado o que é escolha, e como regra o que é
preferência. O objetivo é um método em que **toda decisão tenha procedência**: de onde veio o
número, quem escolheu a regra, e o que aconteceria se a escolha fosse outra.

- **Não é um otimizador.** DeMiguel, Garlappi & Uppal (2009): 14 modelos, nenhum bateu 1/N fora
  da amostra. Regra declarada e testável, nunca ótimo derivado.
- **Não é um backtest atrás de resultado.** As estratégias são pré-registradas, com ordem de
  execução, antes de qualquer dado ser tocado.

Onde o projeto está e a ordem do que falta: **`PLANO.md`** (ganha de qualquer fila escrita
aqui). O que está aberto: **`PENDENCIAS.md`**. As decisões que esperam o Osvaldo:
**`docs/decisoes/fila-do-osvaldo.md`**.

As instruções do Projeto no claude.ai são cópia de **`docs/ia/instrucoes-projeto-claude.md`**:
mudar uma exige mudar a outra no mesmo dia, com a linha no changelog de lá.

---

## 2. As sete doutrinas

Vivem em **`docs/doutrinas.md`**, fonte única (P2), leitura obrigatória em toda sessão
(`auditoria/tamanho_do_contexto.py` a conta como `SEMPRE`). Código que as viola está errado
mesmo que os testes passem. Índice: **P1** procedência por valor · **P2** regras como dados ·
**P3** portões, não pontuação · **P4** pré-registro com impressão digital · **P5** limitações
declaradas · **P6** ausência de critério não é critério de exclusão · **P7** rotina que depende
de alguém lembrar não é rotina.

---

## 3. Como rodar

**Python 3.11, e só 3.11** (`requires-python = "==3.11.*"`, P-15): 3.12 mudou a comparação de
`datetime.date`, e o projeto compara `expira` em quase todo `val()`. Reabrir a faixa só **com
medição**; um resultado de outro interpretador é número novo, não conferência de um antigo.

**Instalar — e NÃO é `pip install -e .`** (B-04: o build falha, o projeto não é pacote; o
`pyproject.toml` declara versões). O comando sai da própria lista:

```bash
python alocacao/ambiente.py --instalar   # imprime o pip install exato
```

**Dependências só no `pyproject.toml`, com pino `==`.** Não existe `requirements.txt` de
propósito (N-01: duas listas que concordam por acidente). Os grupos `lint`, `captura`,
`paralelo` e `metricas` ficam **fora** da impressão do ambiente, que lê só `dependencies` e
`dev`: executor de teste e ferramenta de lint não mudam número (P-141). Se o `ambiente.py`
disser que `numpy` ou `pandas` diferem, a suíte continua verde e isso está certo: o que deixa
de valer é a **reprodução** de um resultado pré-registrado, e quem carrega o aviso é o resultado
(`alfa_contra_fatores()["ambiente"]`).

```bash
cd alocacao
python ambiente.py                 # confere o ambiente ANTES de acreditar num número
python -m pytest -q -m "not slow"  # durante a tarefa (§9)
ruff check . && mypy .             # ambos em ZERO (P-40)
python impacto.py <alvo>           # o que alcança uma constante, função ou campo
python demo_aporte.py              # motor de aporte
python cenarios.py                 # varredura de cenários
```

### As capturas — rodam sozinhas, no GitHub Actions

`.github/workflows/captura_cvm.yml`, todo dia às 09:15 UTC (o GitHub não garante o horário):
CVM (DFP, ITR, CAD), COTAHIST, NEFIN, a conciliação do COTAHIST e a release pública da CVM. O
regime de cada fonte é dado: `politica.yaml → regimes_de_captura`.

```bash
python fase0/capturar_cvm.py --armazem s3                      # o que o workflow roda
python fase0/capturar_cvm.py --armazem s3 --cache data/armazem # e guarda cópia local
py -3.11 fase0/capturar_cvm.py --dry-run                       # o que baixaria; não grava
```

| o quê | onde |
|---|---|
| o byte de cada versão | Cloudflare R2, `<fonte>/<recurso>/<arquivo>/<sha256>.<ext>` — nunca sobrescrito |
| o que mudou em cada rodada | `docs/acervo/<fonte>/capturas.csv`, commitado pelo `github-actions[bot]` |
| a prova de cada rodada, inalterados inclusive | R2, `logs/capturas/` e `logs/capturas_b3/` |
| o que a carga inicial subiu do disco dele | `docs/acervo/<fonte>/inventario-armazem.csv` |
| cópia local | `data/armazem/<chave>` (ignorado pelo git) |

- **COTAHIST:** diário a cada pregão; anual **uma vez por mês**, para conciliação; **nunca o
  anual todo dia** (85 MB × 250 pregões estoura o grátis). O `404` do diário é `ausente`, não
  erro: a B3 devolve o mesmo `404` para feriado e para dia não publicado, e quem distingue é a
  conciliação com o anual (P-137).
- **O armazém tem teto** (`politica.yaml → armazem`: aviso 7 GB, teto 9 GB), somado antes de
  cada envio. O R2 não tem limite de gasto; o teto é do código.
- **Só a CVM é pública** (release `cvm-acervo-<ano>`, `fase0/publicar_cvm.py`). Dado de mercado
  da B3 e os fatores do NEFIN **não se publicam** (termos lidos: P-136, LIC-01).
- **Credenciais só por variável de ambiente** (`R2_ACCOUNT_ID`, `R2_ACCESS_KEY_ID`,
  `R2_SECRET_ACCESS_KEY`, `R2_BUCKET`); no workflow, segredos do repositório. Nunca num
  arquivo, nunca num log. Criar conta ou mexer em credencial é dele.

**Abrir uma versão — nunca pelo caminho do disco**, que só tem o que esta máquina viu:

```python
import acervo                                                # fase0/acervo.py
acervo.abrir("dfp", "dfp_cia_aberta_2024.zip")               # a vigente
acervo.abrir("dfp", "dfp_cia_aberta_2024.zip", "0dd854dc")   # anterior, por prefixo de sha256
```

Procura no cache, no `data/bronze/` e no R2, e confere o sha256. Mais de 8 dias sem observação
levanta `CapturaParada`: o GitHub desliga cron de repositório parado há 60 dias **sem erro
nenhum**. `python fase0/acervo.py --frescor [--armazem s3]` mede à mão e sai 1 se algo parou.
Para os testes que leem acervo: `python fase0/materializar_acervo.py` põe no lugar as versões
fixadas pelos pré-registros.

---

## 4. Mapa dos arquivos

```
alocacao/
  motor.py         val(), InsumoBloqueado. A porta de entrada de todo insumo: ler
                   custos.yaml sem passar por val() fura a P1
  custos.yaml      constantes com procedencia por valor (e `expira`)
  politica.yaml    o MOTOR: funcoes, portoes, doutrinas, regimes, pre-registro,
                   limitacoes_declaradas. Vale independente de quem usa
  perfil.yaml      UM usuario: `compromissos` e `decisoes`. Segundo usuario = segundo
                   arquivo, nunca edicao no politica.yaml (L-01)
  alocacao.py      catalogo de rotas, portoes G0-G8, motor de aporte
  tese.py / teses.yaml   registros K e C: REGRA_DECIDIDA (G8 nao libera peso) e
                   COMPROMISSO_ATIVO (G-01)
  estado.yaml      situacao financeira real -- PRIVADO, fora do git (test_p67_segredo)
  estado_io.py     validacao do estado
  reserva.py, aporte.py, sleeve.py, cenarios.py, corretoras.py, fatores.py
  multiplicidade.py, preregistro.py   Romano-Wolf, o `m` dos dois lados
  dados/nefin_factors.csv   FORA DO GIT (termos do NEFIN); o materializador o poe no lugar
fase0/
  calendario.py    calendario de pregoes e UNICO leitor de COTAHIST; acha o membro do ZIP
                   pelo CONTEUDO (P-99) e le o leiaute do YAML (P-105)
  moeda.py         as fronteiras de MODREF, medidas e NAO aplicadas (C-03)
  refinar.py       o silver de eventos societarios
  ajustar.py       a serie de precos ajustada por proventos (C-02)
  capturar_cvm.py, capturar_cotahist.py, capturar_nefin.py   as capturas (P-57)
  conciliar_cotahist.py   diarios x anual do mes (P-137)
  publicar_cvm.py  a release publica da CVM; recusa o que nao e CVM antes do primeiro envio
  armazem.py       chave = conteudo, nunca sobrescreve, confere sha256 nas duas pontas
  acervo.py        a porta de LEITURA: abrir() e frescor()
  materializar_acervo.py   poe no lugar as versoes fixadas pelos pre-registros
  insumo_ml.py     o COTAHIST FIXADO pelo pre-registro ML, nunca o vigente (P-139)
  manifesto_cvm.py sha256 + dt_captura; comparar() separa REORDENADO de REAPRESENTADO
  subir_acervo_local.py   carga inicial do disco dele para o R2
auditoria/         os INSTRUMENTOS; os laudos moram em docs/auditoria/
  chaves_orfas.py, chaves_duplicadas.py   o YAML que ninguem le, e o que ele engole
  tamanho_do_contexto.py   quanto custa ler este projeto
  achados_ancorados.py     todo achado citado tem onde ser lido
  codigos_preservados.py   nenhum codigo (P-, A-, 5-B.n) some do repositorio
  escada_contorno.py       NAO_CONFIRMADO por falta de acesso so com a escada (5-B.18)
medicoes/          scripts de medicao sobre o acervo; push em `medir/<nome>` roda
                   `<nome>.py` no Actions, com o token de LEITURA (5-A.11); saida em resultados/
tools/analisar_sessoes.py  tempo e tokens das sessoes, na maquina dele
docs/
  doutrinas.md     as sete doutrinas
  decisoes/        decisoes com desenho e alternativas; fila-do-osvaldo.md
  fontes/          fonte primaria transcrita, com indice
  schemas/         LEIAUTE COMO DADO (cotahist-v02.yaml)
  acervo/          manifesto e registro de cada captura; origem.csv declara DE ONDE veio
  auditoria/       laudos, escopos e medicoes
  metricas/        o que e medido, eventos.csv, o antes e depois de cada corte
  historico/       REGISTRO, nunca instrucao: este arquivo ate 26/09, as pendencias
                   fechadas, os bilhetes vencidos, a pesquisa de agosto
  referencia/      laudos e desenhos que sairam da raiz
.github/workflows/ testes.yml (portao), captura_cvm.yml (capturas), medir.yml, mutacao.yml
```

---

## 5. Convenções

- **Código e YAML em ASCII.** Comentários, docstrings e valores de `.py` e `.yaml` sem acento.
  Markdown usa acento normal. Não "conserte".
- **Comentário explica o porquê**, nomeando o achado que motivou a linha:
  `# A-02: custo percentual nao dilui`. Comentário que parafraseia o código é ruído.
- **Um achado, um teste que falha na versão anterior.** Teste que passaria antes e depois não
  documenta nada: o do F-01 compara duas simulações, porque um campo declarado e nunca lido
  passaria num teste de atributo.
- **Commit: título até 72 caracteres, corpo com o porquê** e o que a mudança mediu (decisão
  dele, 25/09). O histórico anterior não se reescreve: os marcos valem pelo sha.
- **Achado novo** segue a skill `bastter-achado`; mudança em `alocacao/` segue
  `bastter-mudanca`.

---

## 5-A. Regras permanentes de sessão

Decididas por ele; valem em toda sessão sem ele precisar pedir.

1. **Registrar as pendências** em `PENDENCIAS.md` **antes de encerrar**. Cada uma com **dono**,
   **gatilho** e **classe** — sem os três é desabafo. Classes: `BLOQUEIA_O_SISTEMA` (caminho
   crítico) · `DECISAO_DE_DESENHO` (um humano decide sobre o sistema) · `DADO_DE_UM_USUARIO` (o
   estado de uma carteira; **nunca** bloqueia desenvolvimento). Antes de chamar algo de
   bloqueio: *um cliente novo desta ferramenta teria isso?* (U-01). Pendência fechada vai para
   `docs/historico/pendencias-fechadas.md`, com a evidência, e **o cabeçalho é riscado no mesmo
   commit** (fila desatualizada já reabriu tarefa pronta três vezes).
2. **Teste em toda etapa, sem exceção.** Arquivo novo em `fase0/` ou `alocacao/` nasce com
   `test_<nome>.py` ao lado, script utilitário inclusive: o `coletar_b3.py` quebrou três vezes
   seguidas em funções puras que ficaram sem teste.
3. **Escalável, auditável, manutenível — nesta ordem de conferência.** Funciona com 400
   empresas e dois usuários? De onde veio o número? A próxima sessão entende e o teste pega a
   volta? Isso proíbe: script de uma vez só, número no código em vez do YAML, correção sem teste.
4. **Achado retirado fica como retratação, nunca some**: o achado citado, a evidência que o
   derruba, a causa raiz do erro de método e o que mudou no processo. Tamanho em troca de não
   repetir — e o que cresce demais se **move** para o histórico, nunca se apaga
   (`auditoria/codigos_preservados.py` reprova código que sumir).
5. **Terminar indicando *o* próximo passo**, escolhido e justificado: o que vem primeiro, por
   que, o que destrava, o que o impede. Marque o que exige o desktop. O próximo passo **não pode
   ser de engenharia duas vezes seguidas** — engenharia entra quando destrava, não quando é o
   que sobrou de mais fácil (skill `bastter-proximo-passo`).
6. **Bilhete de entrega não vai para a raiz.** O prompt vive no chat; o registro vive em
   `CLAUDE.md`, `PENDENCIAS.md` e `PLANO.md`. Quem pode morar na raiz é dado
   (`auditoria/raiz_viva.yaml`, guardado por `test_raiz_viva.py`).
7. **Credencial fora do fluxo do git não se extrai para chamar API**, e **sessão logada de
   navegador é credencial**: não se usa para agir em conta nenhuma. Disparar workflow, criar
   issue, mexer em segredo: ou pede a ele, ou usa o `gh`/conector que ele autorizou para aquilo.
   A única via automática é a da regra 11 (medição), e ela não abre exceção a esta.
   `.claude/settings.json` nega as ferramentas do Chrome, e `test_navegador_negado.py` reprova
   se a negação sair.
8. **Registrar o que fazer ao voltar ao desktop**: seção `## Ao voltar ao desktop` no fim do
   `PENDENCIAS.md`. Tarefa que precisa de PowerShell, download ou do dado bruto dele é da sessão
   local — diga isso em vez de simular; contagem inventada é o pior resultado possível aqui.
9. **Duas ferramentas, não substitutas.** A sessão local (Claude Code na máquina dele) tem o
   disco, o acervo bruto e o `git` dele. A da nuvem tem rede limitada e não vê o disco dele:
   antes de declarar algo manual, pergunte se um script na máquina dele faz (§5-B.17).
10. **Leitura larga vai para subagente**, com a proibição de inventar URL, número e versão e a
    ordem de marcar `NAO_CONFIRMADO` no prompt dele. Trabalho que decide o projeto fica na sessão.
11. **Medir sobre o acervo é empurrar uma branch `medir/<nome>`** com `medicoes/<nome>.py` — o
    `.github/workflows/medir.yml` roda o script com o token do R2 **somente leitura** e commita a
    saída na própria branch. **Esse push é o fluxo normal do agente, não uso de credencial
    dele**: o agente não vê, não extrai e não escolhe credencial nenhuma; quem as usa é o
    workflow, com os segredos `R2_LEITURA_*` que ele criou para isso. E por isso **não é
    brecha para a regra 7**, em três cercas: o workflow só tem `contents: write`; o token não
    apaga nem escreve no armazém; e `auditoria/test_workflow_medir.py` reprova permissão a mais,
    segredo fora do passo que mede, ou token de escrita. Qualquer coisa que **não** seja medir
    (disparar outro workflow, mexer em segredo, escrever no armazém) continua na regra 7: pede.
    A saída vai para o repositório público: **nada de preço, volume ou dado de negociação da B3**
    nela (P-136) — só contagem, código e rótulo.

---

## 5-B. A régua da medição

> **Em todos os erros que ela registra, a medição estava certa. Errada era a pergunta que se
> achou que ela tinha respondido.** Medir → ler a vizinhança → concluir. O passo do meio é o
> que se pula.

**Cinco perguntas antes de promover uma medição a achado:**

1. **Escreva em uma frase o que a medição mediu.** Se a frase for mais estreita que a conclusão,
   reescreva a conclusão.
2. **Que parte do sistema ficou fora do instrumento?** Regra em YAML (varrer só `.py` é medir
   metade — E-05), leitura por chave variável, módulo que o filtro excluiu, teste contado como
   motor.
3. **Abra os arquivos em volta antes de escrever.** Medir levanta o candidato; quem o promove a
   achado é a leitura.
4. **A guarda falha quando deveria?** Prove por **mutação** (reintroduza o defeito), por **duas
   execuções** (idempotência) ou **adiantando o relógio** (`val(..., hoje=2027-01-01)`).
5. **Numa fonte, a cláusula citada cobre o item de que se fala?** "Fonte primária ganha" só
   depois de verificar qual dispositivo a cláusula alcança.

**Declare o alcance do instrumento:** ferramenta que anuncia o próprio limite é ferramenta; a
que só imprime achados é opinião com sotaque de máquina.

**E as regras que a régua ganhou depois:**

- **12 · Arquivo que duas mãos editam não se entrega inteiro.** `CLAUDE.md`, `PENDENCIAS.md` e
  `politica.yaml` se editam por trecho ancorado, sobre a versão do `origin`. Entregar o arquivo
  inteiro é decidir sozinho que a sua cópia é a verdade.
- **13 · "Não dá para fazer X" só se escreve depois de tentar X e falhar, com o erro
  transcrito.** Sem isso, escreve-se "não sei se dá" — e mede-se. Antes de afirmar uma
  limitação de uma fonte, **ler as entradas dela em `limitacoes_declaradas`, inclusive as
  `RETIRADA`**.
- **14 · Todo número de controle sai com o seu n.** `1,0000 (n=1)` e `1,0000 (n=339)` são a
  mesma string e conclusões opostas.
- **15 · "Passed" só se escreve da rodada completa sobre o repositório real** (clone do
  `origin/main` com a entrega aplicada). Número de árvore parcial leva o nome da árvore ao lado.
- **16 · Ausência de dado por problema técnico é pendência de conserto, nunca limitação.**
  Pergunte de quem é o limite: do mundo → `FISICA`; consertável → `NAO_CONSERTADA`, com
  `o_que_resolveria` e `pendencia` aberta (`alocacao/test_limitacoes_tipo.py`).
- **17 · Limitação da ferramenta de quem responde não é limitação da tarefa.** Escreva com o
  sujeito — *"a sessão na nuvem não alcança"* — e o passo seguinte é o roteiro para a sessão
  local, não trabalho manual para ele.
- **18 · Antes de marcar `NAO_CONFIRMADO` por falta de acesso, sobe-se a escada**, e cada
  degrau tentado fica transcrito com o erro: **(1)** outra ferramenta (curl no terminal,
  `git clone`, a API em vez da página, outro formato do mesmo dado); **(2)** outra cópia
  (Wayback Machine, espelho oficial, portal de dados abertos); **(3)** outra fonte primária
  com o mesmo dado; **(4)** outro executor (sessão local, workflow `medir/`, script na máquina
  dele); **(5)** só então `NAO_CONFIRMADO`, com os degraus na linha (`escada:`) e uma `P-nnn`
  de conserto. Motivo: a 13 e a 17 se cumpriam com "tentei, deu 403, parei"; em 27/09, três
  "bloqueados" caíram no degrau 1 (skill `bastter-contorno`; guarda
  `auditoria/test_escada_contorno.py`).

A tabela dos onze erros de 11 a 13/09 e a narrativa de cada regra estão no histórico (§13).

---

## 6. Como trabalhar com o Osvaldo

- **Mostre onde ele está errado.** Concordar por educação é a pior entrega possível.
- **Não concorde com o Bastter por afinidade.** O projeto existe porque o método tem defeitos.
- **Traga o que ele não sabe que existe.** O achado lateral vale mais que a confirmação.
- **Análise profunda, nunca superficial**, e sem reexplicar o que já está escrito aqui (plano
  limitado).
- **Pergunte quando o caminho bifurca de verdade**, não por cortesia. **Pergunte o número
  inteiro antes de calcular uma razão**: dado parcial já sustentou conclusão que o completo
  derrubou três vezes.
- **Não confunda o que ele faz com o que ele quer.** A carteira dele é um cofrinho; "você opera
  X?" tem sempre a mesma resposta, e nenhuma é preferência. Pergunte por decisão (P6).
- **Número que descreve o dinheiro dele entra em `estado.yaml` e em lugar nenhum mais** — nem
  como ilustração, nem como argumento. O que é reserva, aporte ou caução é **decisão declarada
  dele**, não leitura do extrato (U-02). Achado de desenho que precisa do saldo de alguém para
  parecer grave não é achado de desenho.
- **D-01 e a exceção de 25/09:** os valores **já publicados** ficam, e o histórico do git não é
  reescrito. Todo valor **novo** sobre o dinheiro dele passa pela D-01 inteira, inclusive o
  gatilho de revisitar se o patrimônio crescer ou mudar de natureza.
- **O processo é orgânico e sem pressa.** Não force conclusão.

---

## 8. Números que envelhecem

**Não os repita de memória — leia do YAML.** Constante datada tem `expira` como **data** (não
texto entre aspas: YAML entre aspas é string e o aviso fica mudo — B-01, guardado por
`test_P70_…`); `motor.val()` avisa em stderr quando passa. Lei usa `expira: null` + `revisar_se`.
Constante que cita documento e artigo carrega `trecho_conferido`, e `false` reprova a suíte. As
que vencem em 7 dias viram issue no semanal (`auditoria/expira_proxima.py`).

---

## 9. O protocolo de mudança — antes de editar qualquer coisa

| # | passo |
|---|---|
| 1 | `python impacto.py <alvo>` — o que alcança o que você vai mexer |
| 2 | ler os **pontos cegos** do relatório (chave dinâmica não aparece no mapa) |
| 3 | mudança de contrato ou refatoração? **instantâneo dourado antes** — não é opcional |
| 4 | editar |
| 5 | `pytest -m "not slow"` **da suíte tocada** durante a tarefa; a completa, uma vez, antes do commit |
| 6 | `ruff check . && mypy .` — ambos em zero |
| 7 | comparar o instantâneo — **campo a campo, não só os números** |
| 8 | registrar em `PENDENCIAS.md` e, se for achado, em `ACHADOS.md` e `docs/metricas/eventos.csv` |
| 9 | subir a versão do `politica.yaml` + changelog, se ele mudou |

**Enquanto a suíte roda, não se edita:** o verde vale para a árvore que existia quando ela
começou.

**Duas rodadas, dois papéis (P-141).** Durante a tarefa, só a suíte tocada, sem `slow`. Uma vez,
com a árvore parada, antes do commit:

```bash
for s in alocacao fase0 auditoria tools medicoes; do py -3.11 -m pytest $s -n auto --dist loadgroup -p no:cacheprovider; done
```

- **`--dist loadgroup` não é opcional:** o memo de sessão e a fixture de módulo são por
  processo; sem o grupo, a leitura dupla do acervo volta calada (`fase0/test_memo_acervo.py`).
- **Nenhuma rodada encosta no teto de 10 min do Bash.** Acima de 8 min, em segundo plano, sem
  editar nada enquanto roda.
- Na nuvem, sem acervo nem `estado.yaml`: `-m "not acervo and not privado"`, e o número vai com
  esse recorte escrito ao lado (§5-B.15).

---

## 12. Métricas

O que é medido, onde, com que frequência e o que **não** é: **`docs/metricas/README.md`**.
Nenhum número dela é copiado para cá — lê-se da fonte.

- **Portões sem ninguém lembrar (P7):** `.github/workflows/testes.yml`. Todo push e PR roda as
  quatro suítes sem `slow`, mais ruff e mypy; o semanal roda a completa contra o armazém, a
  cobertura e a issue de `expira`. `privado` fica fora do CI por nome.
- **Todo achado, retratação ou reincidência novo ganha a sua linha em
  `docs/metricas/eventos.csv` no mesmo commit.** Campo que o texto não diz fica `desconhecido`,
  nunca inferido. Evento sem código reprova (`auditoria/metricas_processo.py`).
- **O tamanho do que toda sessão lê** é comando, não frase: `python
  auditoria/tamanho_do_contexto.py`. O antes e depois de cada corte fica em `docs/metricas/`.
- **Tempo e tokens das sessões:** `py -3.11 tools/analisar_sessoes.py`, só na máquina dele.

---

## 13. Onde a história ficou

| o quê | onde |
|---|---|
| este arquivo até 26/09, inteiro: as §7, §10, §11 e as rodadas datadas de 16 a 19/09 | `docs/historico/claude-md-ate-2026-09.md` |
| o índice de achados (uma linha por achado, com a regra que ele deixou) | idem, §7 |
| as retratações da régua §5-B (os onze erros, as linhas 12 a 17 com a narrativa) | idem, §5-B |
| as retratações do tamanho do contexto e do tempo das sessões | idem, §11.4 e §11.5 |
| as críticas dele que mudaram o sistema, a U-02, a M-01 | idem, §6 e §7 |
| os achados, com medição e teste | `ACHADOS.md` — leia os da área antes de tocar nela |
| as pendências fechadas, com a evidência | `docs/historico/pendencias-fechadas.md` |
| os bilhetes de entrega vencidos | `docs/historico/entregas/` |
| as decisões com desenho e alternativas | `docs/decisoes/` |
