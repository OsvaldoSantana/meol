# Pré-registro do teste de marca — versão final (P-162)

> **SUPERADO em 27/09/2026, sem ter sido usado: nenhum convite saiu.** Ele trocou o Google
> Forms por uma página própria (Vercel e Supabase, S6) e acrescentou o veto de distinção
> (fila, "Decisões dele, 27/09/2026, trazidas pelo prompt da S5 v2"). Vale
> [`docs/marca/teste-de-marca/preregistro-final.md`](teste-de-marca/preregistro-final.md).
> Este pré-registro fica como registro e não se edita. O sha256 do script que ele cita
> deixou de bater: o script mudou para a v2.

*27/09/2026, S5. Escrito antes de qualquer estímulo ser mostrado a alguém e antes de existir
qualquer resposta, no repositório ou fora dele.*

**Status.** Vale como pré-registro **a partir do merge deste arquivo no `main`**, e só se o
merge vier **antes** do primeiro convite (a lição da P-116: critério gravado depois de olhar
não é critério). A impressão digital é o sha do merge; os arquivos que ele congela têm o
sha256 na §3 e na §4, e `tools/test_analise_teste_marca.py` reprova se um deles mudar sem que
esta página mude junto.

**Origem.** [`preregistro-teste-de-marca-2026-09-20.md`](preregistro-teste-de-marca-2026-09-20.md),
como declarado em 20/09 e trazido ao repositório em 26/09 (commit `2c2976b`, sha256
`fca34b86d5265c5c7687aae297043fa925cc76c4a13cba1282b95e68765ebcbc`). Ele fica como está: é o
registro do que foi dito em 20/09. **Onde os dois divergem, vale este**, e a §1 diz cada
divergência e de quem é a decisão.

**Nome MEOL nos estímulos: decisão dele.**

---

## 1. O que mudou desde 20/09, e quem decidiu

Todas as decisões abaixo são dele, com a data e o código da fila
([`docs/decisoes/fila-do-osvaldo.md`](../decisoes/fila-do-osvaldo.md)). Nenhuma foi preenchida
por uma sessão.

| ponto | 20/09 | final | decisão |
|---|---|---|---|
| direções | A, B, C e D | **E, C e D** (A e B saem; E funde as duas) | 16b, 27/09 |
| H1 | "B e A superam D em confiável e honesto" | **"E supera D em confiável e em honesto"** | 16b |
| escala | pares opostos, sem número de pontos | **1 a 7** | 17a, 27/09 |
| "vence a maior média em confiável e em é para mim" | as duas escalas, sem dizer o que fazer se discordarem | **um índice por pessoa: a média de confiável e é para mim**; a regra roda sobre ele | q-a, 27/09 |
| "empate dentro da margem" | margem não definida | **empate quando o intervalo de 95% da diferença pareada (bootstrap) contém zero** | 17a |
| "não ficar abaixo da mediana em honesto" | mediana sem referente | **não ser a pior direção em honesto** | 17a |
| H2 | "D aumenta a sensação de parece golpe ou parece vendedor" | **D pior que E e pior que C**, com o intervalo pareado excluindo zero, em confiável ou em honesto | t-a, 27/09 |
| H3 | "faixa de incerteza ou rota bloqueada não reduz a confiança" | **rota bloqueada real, nas três direções** (j-A); cada pessoa vê as três bases e depois as três com rota bloqueada, **na mesma ordem**. O "ordem aleatória" da 17a não é possível com a base sempre antes: **a H3 é exploratória**, com esse viés declarado (§8) | 17a, j-A (27/09), prompt da S5 |
| H4 | "esse público aceita mais informação por tela do que um iniciante" | **fora do teste**: o filtro exclui iniciantes; vai para a P-156 | s-a, 27/09 |
| ordem das direções | aleatória | **seis versões do formulário**, uma por ordem, links em rodízio | g-B, 27/09 |
| tamanho da amostra | não definido | **quem aparecer numa janela de 21 dias corridos**; nunca encerrar olhando o resultado | h-A, 27/09 |
| estímulo | não definido | **imagem fixa**, fontes OFL embutidas | i-A, 27/09 |
| pessoas próximas | (a P-162 dizia: só pilotam) | **contam**, identificadas por pergunta; a análise sai com e sem elas, e **a sem elas decide** | amigos (27/09), r-a (27/09) |
| filtro | "aporta todo mês em renda variável há pelo menos 6 meses" | a mesma coisa sem jargão (§2) | v-a, 27/09 |
| recrutamento | rede do autor, comunidades, conhecidos de conhecidos | **rede pessoal e bola de neve, sem painel pago** | recrutamento, 27/09 |
| "seguro/arriscado", "sofisticado/simples" | escalas sobre o produto | **reescritas pelo visual**: insegurança ↔ segurança, popular ↔ de luxo | w-a, 27/09 |
| "honesto/vendedor", "confiável/parece golpe" | como estão | **mantidas**, com a ordem das palavras igual à da escala; o efeito de sugestão de "golpe" vira limitação | x-a, 27/09 |
| pergunta dos amigos | "você conhece quem criou este app?" | "Você conhece pessoalmente a pessoa que está fazendo esta pesquisa (é amigo, parente ou colega dela)?" | u-a, 27/09 |
| imagem de estilo de vida na D | prevista | **não entrou**: a D tem ilustração desenhada em código, provisória (P-168) | k-A, 27/09 |

**O que não entra, e por quê.** A H-A1 (a fatia insegura), que a P-162 dizia que "pode entrar
como exploratória", **não entra**: nenhuma decisão dele a incluiu, e a n-A juntou as
perguntas sobre o público (H-A1 e H-A2) na P-154. Se ele quiser a H-A1 aqui, é antes do
merge, e o questionário e o script mudam junto.

## 2. Público, filtro e recrutamento

- **Público:** quem já coloca dinheiro todo mês em renda variável. **Filtro**, antes de
  qualquer tela: *"Há pelo menos 6 meses, você coloca dinheiro todo mês em ações, fundos de
  índice (ETF) ou fundos imobiliários?"* Quem responde "Não" sai. O convite diz o mesmo
  critério (v-a).
- **Recrutamento:** rede pessoal dele e bola de neve (quem respondeu repassa). Sem painel
  pago, sem anúncio, sem comunidade aberta.
- **Amigos:** a pergunta u-a vem logo depois do filtro. Quem responde "Sim" segue e conta.
  A análise sai duas vezes: **sem quem respondeu "Sim", e essa decide** (r-a); e com todos,
  como sensibilidade. As duas vão para o relatório.
- **Consentimento:** a primeira pergunta. "Não concordo" sai sem ver nenhuma tela.

## 3. Os estímulos

A T1 ("aporte do mês") nas direções **E** (instrumento de precisão), **C** (digital amigável)
e **D** (ostentação, o controle), cada uma em duas versões: **base** e **com rota bloqueada**
(j-A: a primeira rota que o motor elimina pela ordem dos portões de universo, com o motivo em
linguagem comum). Os números saem do motor, sobre um cenário sintético
([`direcoes/README.md`](direcoes/README.md)). Imagens fixas de 390 × 844 (i-A), **aprovadas
por ele em 27/09/2026** (fila, "Aprovação dele, 27/09/2026: os seis PNG da S4"). Mudar um
byte é imagem nova, nova aprovação e novo pré-registro.

| arquivo | sha256 |
|---|---|
| `docs/marca/direcoes/png/E-base.png` | `302a50ab35a31e24166874f14dfebc4055bc794524c90a73a6894a7311be3665` |
| `docs/marca/direcoes/png/E-rota-bloqueada.png` | `04fe0520a5c4e0e022927ec37cca779fc88c169844b8d0185ff9bcca6e678962` |
| `docs/marca/direcoes/png/C-base.png` | `91b3f24e0eebd467306917b1c24df86ed6fdde4fe25ca9ac211abe4c76acd5b9` |
| `docs/marca/direcoes/png/C-rota-bloqueada.png` | `da85f3eb295e16d43872f5521ec18a13682888291d7ab4aa4c2912389c908174` |
| `docs/marca/direcoes/png/D-base.png` | `36a7c019c0410b1567e5dc17177473895deb5d90a175e630f58eace063115a83` |
| `docs/marca/direcoes/png/D-rota-bloqueada.png` | `f0ad96161c829d4536cd083f08d99581fc54deaa7f32f904c264702bb9b64b73` |

## 4. O instrumento e a análise, congelados

| arquivo | o que é | sha256 |
|---|---|---|
| [`docs/marca/teste-de-marca-questionario.md`](teste-de-marca-questionario.md) | o texto exato de cada tela do formulário, a configuração do Forms, as seis versões e o ensaio | `998f0931118fd1765712702e75619850f98e7430c1ecb0fc8fd7bcc3471da666` |
| [`tools/analise_teste_marca.py`](../../tools/analise_teste_marca.py) | a análise inteira: leitura, filtros, janela, regra, hipóteses e saída | `88fd3210f66107c37954c3fc9718d65b9d76f2fd32df1d71c101f0f7906682cd` |

**O ensaio** (seção 9 do questionário): um subagente respondeu o questionário três vezes,
como três investidores leigos, para achar defeito no instrumento. Nada do ensaio é dado. Os
achados que mexiam em texto decidido por ele foram a ele (u-a, v-a, w-a, x-a); os de redação
foram corrigidos pela S5; os que estão nas imagens congeladas viraram limitação (§8).

## 5. O desenho

- **Seis versões** do formulário, uma por ordem das três direções (g-B), idênticas em tudo
  menos a ordem das imagens:

  | versão | telas 1 a 3 (base) e 4 a 6 (com rota bloqueada) |
  |---|---|
  | 1 | E, C, D |
  | 2 | E, D, C |
  | 3 | C, E, D |
  | 4 | C, D, E |
  | 5 | D, E, C |
  | 6 | D, C, E |

- **Rodízio:** o primeiro convidado recebe a versão 1, o segundo a 2, e assim por diante,
  voltando à 1 depois da 6. A versão fica registrada pelo arquivo de exportação
  (`data/teste-marca/versao-N.csv`). O repasse leva o link de quem repassou.
- **Cada pessoa vê as seis telas**, uma por seção, e responde sobre cada uma antes da
  seguinte: uma pergunta aberta ("o que você lembra", o teste de 5 segundos de 20/09) e cinco
  escalas de 1 a 7 (`seguro`, `para_mim`, `honesto`, `confiavel`, `luxo`; 7 é sempre o polo do
  nome). No fim, a pergunta de pronúncia do nome.

## 6. A coleta e a janela (h-A)

- **Janela:** 21 dias corridos, de 00:00 do dia do primeiro convite até 23:59:59 do 21º dia,
  **horário de Brasília** (o fuso do formulário). Resposta fora da janela é **guardada** no
  CSV e **não entra** na análise; o script a conta como `fora_da_janela`.
- **As datas absolutas** entram num **commit próprio, empurrado antes do primeiro convite**,
  que muda só as duas linhas abaixo:
  - dia 1 (o primeiro convite): **a preencher no commit das datas**
  - dia 21 (último dia, até 23:59 de Brasília): **a preencher no commit das datas**
- **Nunca encerrar olhando o resultado.** A coleta não termina antes do dia 21 porque "já dá",
  nem se estende porque "está quase". O script não roda sobre respostas antes do fim da
  janela; o que ele pode fazer antes é `--conferir-cabecalho`, que não calcula nada.
- **Sem tamanho mínimo nem alvo:** é a amostra de quem aparecer (h-A). Com pouca gente, o
  intervalo fica largo e a regra tende ao empate; isso é consequência aceita, não motivo para
  estender a janela.

## 7. A análise (o que `tools/analise_teste_marca.py` faz, e só isso)

```
python tools/analise_teste_marca.py --inicio AAAA-MM-DD   # o dia 1 do commit das datas
```

**Quem entra.** De cada `data/teste-marca/versao-N.csv`: quem marcou "Concordo", respondeu
"Sim" no filtro e tem o carimbo dentro da janela. O script recusa CSV que esteja no
repositório sem ser ignorado pelo git.

**A amostra que decide** é a de quem respondeu "Não" à pergunta dos amigos (r-a). A com
todos sai com as mesmas contas, rotulada como sensibilidade.

**A regra (17a + q-a), sobre as três telas base:**

1. Por pessoa e por direção, o **índice** = (`confiavel` + `para_mim`) / 2.
2. Sai da disputa a direção com a **pior média em `honesto`**. Se duas empatarem exatamente na
   pior média, as duas saem (as duas são "a pior"); se as três empatarem, nenhuma é elegível e
   o resultado é empate.
3. Entre as que ficam, a de **maior média de índice** vence **se o intervalo de 95% da
   diferença pareada de índice para a segunda não contém zero**. Se contém, é **EMPATE**, e a
   escolha passa a ser dele, com o critério escrito antes de escolher (20/09). Se só uma fica,
   ela vence sem comparação.
4. Com menos de 2 pessoas na amostra, não há intervalo: sai `SEM_DADOS`, e a regra não
   escolhe nada.

**O intervalo:** bootstrap pareado por pessoa, percentil, **10.000 reamostragens, semente
20260927**, nível 95%. Toda comparação usa a mesma semente, e portanto as mesmas reamostragens
de pessoas. Nada disso tem opção de linha de comando.

**As hipóteses**, relatadas ao lado da regra e sem mudar a regra:

- **H1** (16b), sobre as bases: E − D em `confiavel` e E − D em `honesto`. **Confirmada** se
  os dois intervalos ficam acima de zero.
- **H2** (t-a), sobre as bases: em `confiavel` e em `honesto`, E − D e C − D. **Confirmada** se,
  em pelo menos uma das duas escalas, os dois intervalos ficam acima de zero.
- **H3** (j-A), **exploratória**: para cada direção, com rota bloqueada − base em `confiavel`
  (a escala que nomeia a confiança de que a H3 de 20/09 fala). Lida como "reduz" (intervalo
  abaixo de zero), "aumenta" (acima) ou "sem evidência de redução" (contém zero). A suspeita
  de 20/09, "nesse público, aumenta", fica como suspeita.
- **H4**: fora do teste (s-a), na P-156.

Sem correção de multiplicidade entre H1, H2 e H3: a decisão é uma regra só, e as hipóteses
são relatadas como tais. `seguro` e `luxo` são descritivas: saem nas médias do relatório e não
entram em regra nem hipótese.

**O que sai:** só agregado. Linhas lidas e descartes por motivo, n válido, n de amigos, n por
versão do formulário, médias, diferenças e intervalos. Nunca uma linha de resposta.

**O que o script não lê:** a pergunta aberta e a de pronúncia. As duas são lidas por ele,
fora do repositório, como material **exploratório**: não mudam a regra nem as hipóteses, e
nenhuma frase de participante entra no repositório (só, se ele quiser, a contagem por tema).

## 8. Limitações declaradas

**As que o plano já previa:**

1. **Amostra de conveniência.** Rede pessoal e bola de neve: o resultado **escolhe entre
   direções para quem respondeu**; não descreve o investidor brasileiro, nem a fatia que o
   MEOL quer atender.
2. **Os 5 segundos são por honra.** O Forms não cronometra nem esconde a imagem depois de 5
   segundos; a pessoa pode olhar quanto quiser. O "o que você lembra" mede lembrança livre,
   não um teste de 5 segundos controlado.
3. **Rodízio imperfeito.** O repasse leva o link de quem repassou, e as versões ficam
   desiguais. O script imprime o n por versão e **não pondera** o desequilíbrio.
4. **H3 exploratória, com ordem fixa.** A versão com rota bloqueada vem sempre depois da base:
   a diferença mistura o efeito da rota bloqueada com o de ver a mesma tela pela segunda vez e
   com o cansaço.
5. **Amigos com viés de agradar.** Por isso a análise dupla, e por isso a sem amigos decide.
   A pergunta depende de a pessoa se declarar; quem chegou por repasse e conhece o autor de
   vista pode responder qualquer das duas.
6. **O resultado escolhe entre direções e não descreve o investidor brasileiro.**

**As que o ensaio achou nas imagens, que estão congeladas:**

7. "Cofrinho de banco digital: bloqueado" pode ser lido como "sua conta foi bloqueada", o
   texto típico de golpe: puxa `confiavel` para baixo por um motivo que não é a marca, na H3.
8. O aviso da tarifa da B3 e o selo "Parcial" foram lidos como erro. Estão nas três
   direções: afetam o nível das notas, não a comparação entre elas.
9. O cartão da D foi lido como oferta de cartão de crédito, o que tende a puxar "quer me
   vender algo": o efeito do objeto "cartão" não se separa do efeito da estética.
10. O nome aparece como "MEOL" na C e espaçado ("M E O L") na E e na D: a pronúncia pode
    depender da última direção vista.
11. A C lembrou a uma persona "o app do meu banco": pode puxar `para_mim` por familiaridade.

**As do instrumento e da análise:**

12. **"Parece golpe" sugere suspeita** (x-a): a palavra planta a ideia antes de a pessoa tê-la.
    Atinge as três direções igualmente na pergunta, não necessariamente na resposta.
13. **Filtro e pergunta dos amigos são autodeclarados**, e o formulário não impede a mesma
    pessoa de responder duas vezes (sem e-mail não há como detectar).
14. **Bootstrap percentil com amostra pequena** tende a dar intervalo mais estreito do que
    deveria: com poucas pessoas, a regra pode declarar vencedora com evidência mais fraca do
    que os 95% sugerem. Foi a escolha dele (17a com h-A), e o relatório traz o n ao lado de
    cada intervalo (§5-B.14).
15. **O formato do carimbo de data do Forms em português é `NAO_CONFIRMADO`.** O script aceita
    três formatos e para com erro em qualquer outro; o roteiro do desktop confere com uma
    resposta de teste antes do primeiro convite (`--conferir-cabecalho`).
16. **A escala `para_mim` pergunta pelo visual**, não pelo produto: "é para mim" mede se a
    estética fala com a pessoa, não se ela usaria o MEOL.

## 9. Mudanças depois do merge

- **Antes do primeiro convite:** qualquer mudança no questionário, no script ou num PNG é um
  novo pré-registro: esta página muda no mesmo commit, com o motivo, e o teste de sha256
  reprova se não mudar.
- **Depois do primeiro convite:** nada muda. Um defeito achado durante a coleta vai para o
  relatório como **desvio do pré-registro**, com o que aconteceu e o que teria sido diferente;
  a análise roda como está gravada.
- **O relatório** diz o resultado da amostra sem amigos, o da amostra com todos, e se os dois
  divergem. Divergência não muda a decisão (r-a); fica escrita.

## 10. Privacidade

Respostas anônimas: sem nome, sem e-mail, sem login. Os CSV ficam em `data/teste-marca/`,
ignorado pelo git (o script recusa ler um CSV que o git não ignore, e
`tools/test_analise_teste_marca.py` reprova se um `versao-N.csv` aparecer no repositório).
No repositório entra só o agregado.

## 11. Até o primeiro convite, em ordem

1. Merge deste pré-registro no `main` (ele).
2. Montar o formulário, duplicar seis vezes e conferir cada versão contra o questionário;
   resposta de teste com "Não concordo" e `--conferir-cabecalho` (ele, no desktop; roteiro em
   `PENDENCIAS.md`, "Ao voltar ao desktop").
3. Commit das datas da janela (§6), empurrado.
4. Primeiro convite.
