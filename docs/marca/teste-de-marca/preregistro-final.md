# Pré-registro do teste de marca — versão final 2 (P-162)

*27/09/2026, S5 v2. Escrito antes de qualquer estímulo ser mostrado a alguém e antes de existir
qualquer resposta, no repositório ou fora dele.*

**Status.** Vale como pré-registro **a partir do merge deste arquivo no `main`**, e só se o
merge vier antes do primeiro convite (a lição da P-116: critério gravado depois de olhar não é
critério). A impressão digital é o sha do merge. Os dez arquivos que ele congela têm o sha256
nas §3, §4 e §8. `tools/test_analise_teste_marca.py` reprova se um deles mudar sem que esta
página mude junto.

*Revisão de 02/10/2026, antes do merge (Claude Code, sessão local): as categorias
concorrentes do veto ficam fechadas no livro de códigos (ac-a, dele); o classificador do veto
entra no conjunto congelado (eram nove arquivos); o contrato de privacidade exige envio por
POST; e a limitação 4 ganha o painel do Firewall da Vercel. Nenhuma resposta existe.*

*Emenda de 02/10/2026, livro de códigos versão 2 (ad-a, ae-a e af-a, dele). Feita **antes da
primeira marca da R3 e antes do primeiro convite**: o commit das datas da janela não existe, e
nenhuma marca foi classificada. Entram quatro categorias concorrentes (consultoria CVM,
assessor, robô e planejador), a unidade que a R3 classifica (app ou site) e a amostra mínima
de 10 marcas por categoria. O que já estava no livro não mudou: variáveis, faixas, limites,
dominante, imitar, e a classificação de E, C e D.*

*Mudança de 02/10/2026, y-a (dele), que supera a y-b. Feita **antes do primeiro convite**: o
commit das datas da janela não existe. Voltam os textos que o ensaio de 27/09 tinha corrigido:
o filtro da v-a e a pergunta dos amigos da u-a; o convite e a tela de conclusão passam a dizer
o mesmo critério do filtro. Muda só o `questionario.yaml` (§4); a análise não lê o texto das
perguntas. Nenhuma resposta existe (§10).*

**Origem e o que este substitui.**
- [`preregistro-teste-de-marca-2026-09-20.md`](../preregistro-teste-de-marca-2026-09-20.md):
  o de 20/09, como declarado. sha256
  `fca34b86d5265c5c7687aae297043fa925cc76c4a13cba1282b95e68765ebcbc`, commit `2c2976b`.
- [`preregistro-teste-de-marca-final.md`](../preregistro-teste-de-marca-final.md): a versão 1
  (PR #39, merge `3e89a46`), com o Google Forms. **Fica superada por esta, sem ter sido usada:**
  nenhum convite saiu. Ele trocou o instrumento por uma página própria e acrescentou o veto de
  distinção (fila, 27/09).

Os dois ficam como registro. **Onde divergem desta, vale esta.**

**Nome MEOL nos estímulos: decisão dele.**

---

## 1. As decisões, e de quem é cada uma

Todas são dele e estão na fila ([`docs/decisoes/fila-do-osvaldo.md`](../../decisoes/fila-do-osvaldo.md)).
Nenhuma foi preenchida por uma sessão. A coluna "20/09" diz o que mudou desde a origem.

| ponto | 20/09 | agora | decisão |
|---|---|---|---|
| direções | A, B, C e D | **E, C e D** | 16b |
| H1 | "B e A superam D em confiável e honesto" | **"E supera D em confiável e em honesto"** | 16b |
| escala | sem número de pontos | **1 a 7**, com os polos escritos | 17a |
| a regra, em duas escalas | "maior média em confiável e em é para mim" | **um índice por pessoa:** a média de confiável e é para mim | q-a |
| empate | "dentro da margem", sem margem | **o intervalo de 95% da diferença pareada (bootstrap) contém zero** | 17a |
| honesto | "não ficar abaixo da mediana" | **não ser a pior direção em honesto** | 17a |
| H2 | "D aumenta a sensação de golpe ou de vendedor" | **D pior que E e pior que C**, com o intervalo pareado excluindo zero, em confiável ou em honesto | t-a |
| H3 | "faixa ou rota bloqueada não reduz a confiança" | **rota bloqueada real, nas três direções**; base sempre antes, na mesma ordem: **exploratória** | 17a, j-A |
| H4 | "aceita mais informação que um iniciante" | **fora do teste** (o filtro exclui iniciantes); vai para a P-156 | s-a |
| q-a a t-a | — | **continuam valendo** nesta versão | z-a |
| instrumento | — | **página própria no Vercel, respostas no Supabase**, sem IP, sem nome, sem e-mail; construída na S6 | instrumento (27/09) |
| ordem das direções | aleatória | **seis ordens balanceadas; a versão sai de um contador de ABERTURAS no banco (mod 6)**, não do link | g-B revista, ab-a |
| tamanho da amostra | — | **quem aparecer numa janela de 21 dias corridos**; nunca encerrar olhando o resultado | h-A |
| estímulo | — | **imagem fixa**: os seis PNG aprovados, pelo sha256 | i-A |
| amigos | (a P-162 dizia: só pilotam) | **contam**, pela pergunta "Você conhece pessoalmente a pessoa que está fazendo esta pesquisa (é amigo, parente ou colega dela)?"; a análise sai com e sem eles, e **a sem eles decide** | amigos, r-a, u-a, y-a |
| filtro | "aporta todo mês em renda variável há pelo menos 6 meses" | **sem jargão:** "Há pelo menos 6 meses, você coloca dinheiro todo mês em ações, fundos de índice (ETF) ou fundos imobiliários?"; o convite e a tela de conclusão dizem o mesmo critério | v-a, y-a |
| u-a e v-a | — | ~~**superadas pela y-b**: voltaram os textos de 20/09, e o defeito que o ensaio tinha achado vira limitação (§9)~~ **restauradas pela y-a, 02/10/2026** | y-a |
| **y-a** (02/10) | — | **supera a y-b:** voltam os textos da u-a e da v-a. A y-b veio de um prompt que citava os textos de 20/09 como decisão; o texto antigo dos amigos contamina a análise sem amigos, que é a que decide (r-a), e o filtro usava jargão. Saem as limitações 6 (em parte) e 7 (§9) | y-a |
| recrutamento | rede do autor, comunidades, conhecidos de conhecidos | **rede pessoal e bola de neve, sem painel pago** | recrutamento |
| escalas seguro e luxo | "seguro/arriscado", "sofisticado/simples" | **pelo visual:** insegurança ↔ segurança; popular ↔ de luxo | w-a |
| escalas honesto e confiável | "honesto/vendedor", "confiável/parece golpe" | **mantidas**, com a ordem das palavras igual à da escala | x-a |
| imagem de estilo de vida na D | prevista | ilustração desenhada em código, **provisória** (P-168) | k-A |
| **veto de distinção** | — | se a vencedora pela 17a **imitar** o código dominante de uma categoria auditada na R3, a escolha volta para ele; **a direção só sai com a R3 fechada** (§8) | veto (27/09), aa-a |
| categorias do veto | — | **fechadas no livro de códigos, não na R3:** banco tradicional, banco digital, corretora, gestora e private, pagamentos, consolidador, casa de análise e educação; as referências de sentimento ficam fora do veto (§8) | ac-a (02/10) |
| mais quatro categorias, a unidade e a amostra da R3 | — | **consultoria CVM, assessor, robô e planejador** entram no veto, com uma precedência para quem cabe em duas; a R3 classifica **o app** (primeira captura de interface da App Store) ou, **sem app, o site** em 390 px, com o dominante também só com as de app; **pelo menos 10 marcas sorteadas por categoria** (§8) | ad-a, ae-a, af-a (02/10) |

**O que não entra.** A H-A1, que a P-162 dizia que "pode entrar como exploratória", fica de
fora: nenhuma decisão dele a incluiu, e a n-A juntou as perguntas sobre o público na P-154.

## 2. Público, filtro, recrutamento, amigos

- **Filtro**, antes de qualquer tela: *"Há pelo menos 6 meses, você coloca dinheiro todo mês em ações, fundos de índice (ETF) ou fundos imobiliários?"* Quem responde
  "Não" sai. O convite e a tela de conclusão dizem o mesmo critério (v-a, y-a).
- **Recrutamento:** rede pessoal dele e bola de neve, sem painel pago, sem anúncio e sem
  comunidade aberta.
- **Amigos:** depois do filtro vem *"Você conhece pessoalmente a pessoa que está fazendo esta pesquisa (é amigo, parente ou colega dela)?"* (u-a, y-a).
  Quem responde "Sim" segue e conta. A análise sai duas vezes: **sem eles, que decide** (r-a), e com todos, como
  sensibilidade.
- **Consentimento:** é a primeira pergunta. "Não concordo" sai sem ver nenhuma tela; fica
  gravado só que a pessoa não quis participar, com a versão e o dia (§4).

## 3. Os estímulos (i-A)

A T1 ("aporte do mês") nas direções **E** (instrumento de precisão), **C** (digital amigável) e
**D** (ostentação, o controle), cada uma em versão **base** e **com rota bloqueada**. Os números
saem do motor sobre um cenário sintético ([`../direcoes/README.md`](../direcoes/README.md)). São
imagens fixas de 390 × 844, **aprovadas por ele em 27/09/2026** (fila). Mudar um byte é imagem
nova, nova aprovação e novo pré-registro.

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
| `docs/marca/teste-de-marca/questionario.yaml` | **o questionário como dado:** os textos de cada tela, a duração da exposição, as escalas e os polos, as seis ordens, o contrato da exportação, as exigências de privacidade e a janela. A página da S6 e o script leem este arquivo | `02773d8b9b71945e3a463e55ed10696f0d63eb7ddf4780e0fcc9520631f38091` |
| `tools/analise_teste_marca.py` | a análise inteira: leitura pelo contrato, filtros, janela, regra, hipóteses, abandono por versão e saída | `2c43c9b9f59b19ab7f4784edad8a8b99a8a5b65ef3c1ca836c7f47b996b6caef` |

A versão de leitura, [`questionario.md`](questionario.md), é **gerada** do YAML por
`tools/questionario_teste_marca.py`, e o `--conferir` reprova se ela divergir. Ela não tem
sha256 próprio, porque não é fonte.

**A página (S6) segue o YAML.**
- **Exposição:** a imagem aparece quando a pessoa toca em "Ver a tela". Fica
  `telas.exposicao_segundos` (5) segundos, some, e não volta. Cabe inteira na tela, sem rolar.
- **Respostas:** as escalas são obrigatórias, e as respostas só são gravadas no envio final.
  Quem sai pelo consentimento ou pelo filtro conclui ali, e só a resposta que o tirou fica
  gravada.
- **O que fica gravado:** uma linha por abertura, com a versão e só o dia (AAAA-MM-DD, em
  Brasília), sem hora.
- **Privacidade:** o navegador nunca chama o Supabase; a gravação passa por uma função da
  Vercel que não repassa os cabeçalhos do cliente. O link é o mesmo para todos. Analytics e
  Speed Insights ficam desligados, e nenhuma resposta vai para o log. O envio é **POST**, com
  as respostas no corpo: o log de runtime da Vercel guarda sozinho os parâmetros da URL
  (revisão de 02/10).

**O ensaio.** Um subagente respondeu a versão 5 como quatro investidores leigos, olhando os
seis PNG. Nada do ensaio é dado. Ele achou 19 problemas.
- **Corrigidos (redação desta sessão):**
  - o consentimento prometia anonimato absoluto e omitia o que fica guardado se a pessoa
    parar;
  - uma só mensagem de saída valia para dois motivos;
  - o "Não é venda" do convite soava como golpe;
  - a instrução não dizia que a imagem some, não volta e pede um toque;
  - "como se fosse a primeira vez" pedia o impossível;
  - a instrução inteira se repetia seis vezes;
  - "desenho" e "este app" na escala `seguro`;
  - as escalas não tinham uma frase-cabeça;
  - o exemplo "XP / xis-pê" ensinava a soletrar;
  - a saída do filtro ensinava a resposta;
  - não estava declarado que as escalas são obrigatórias, nem que a imagem cabe sem rolar.
- **Mudanças no contrato:** as respostas só são gravadas no fim, e as datas são só o dia. Com
  convite pessoal, a hora exata deixaria ligar uma resposta a quem abriu o link.
- **Viraram limitação** os achados sobre textos decididos por ele e sobre as imagens (§9).

## 5. O desenho

- **Seis versões** (g-B), idênticas em tudo menos a ordem das imagens:

  | versão | telas 1 a 3 (base) e 4 a 6 (com rota bloqueada) |
  |---|---|
  | 1 | E, C, D |
  | 2 | E, D, C |
  | 3 | C, E, D |
  | 4 | C, D, E |
  | 5 | D, E, C |
  | 6 | D, C, E |

- **Atribuição (g-B revista, ab-a):** `versão = (contador de aberturas mod 6) + 1`. O contador
  fica no banco, começa em 0 e soma 1 a cada abertura, conclua a pessoa ou não. O link não
  escolhe a versão.
- **Cada pessoa vê as seis telas.** Para cada uma: a exposição; uma pergunta aberta ("o que
  você lembra", o teste de 5 segundos de 20/09); e cinco escalas de 1 a 7 (`seguro`,
  `para_mim`, `honesto`, `confiavel`, `luxo`; o 7 é sempre o polo do nome). No fim, a
  pronúncia do nome.

## 6. A janela (h-A)

- **21 dias corridos**, do dia do primeiro convite até o fim do 21º dia, **em Brasília**.
  Conta o **dia da conclusão** (`concluida_em`). Quem abre dentro da janela e envia depois
  fica fora.
- Resposta fora da janela é **guardada** e **não entra** na análise; o script a conta como
  `fora_da_janela`.
- **As datas absolutas** entram num **commit próprio, empurrado antes do primeiro convite**,
  que muda só estas duas linhas:
  - dia 1 (primeiro convite): **a preencher no commit das datas**
  - dia 21 (último dia): **a preencher no commit das datas**
- **Nunca encerrar olhando o resultado.** O script **recusa** a análise até o fim do dia 21
  em Brasília. Antes disso, só roda `--conferir-cabecalho`, que não calcula nada.
- **Sem tamanho mínimo nem alvo** (h-A). Com pouca gente, o intervalo fica largo e a regra
  tende ao empate. Isso é consequência aceita, não motivo para estender a janela.

## 7. A análise (o que `tools/analise_teste_marca.py` faz, e só isso)

```
python tools/analise_teste_marca.py --inicio AAAA-MM-DD   # o dia 1; só depois do dia 21
```

**Quem entra.** Uma linha da exportação conta se a pessoa concluiu, marcou "sim" no
consentimento e no filtro, e concluiu dentro da janela. O script recusa um CSV que esteja no
repositório sem ser ignorado pelo git, e recusa cabeçalho fora do contrato.

**A amostra que decide** é a de quem respondeu "não" à pergunta dos amigos (r-a). A com todos
sai com as mesmas contas, como sensibilidade.

**A regra (17a + q-a), sobre as três telas base:**

1. Por pessoa e por direção, **índice** = (`confiavel` + `para_mim`) / 2.
2. Sai da disputa a direção com a **pior média em `honesto`**. Se duas empatarem exatamente
   na pior média, as duas saem; se as três empatarem, nenhuma é elegível, e o resultado é
   empate.
3. Entre as que ficam, a de **maior média de índice** vence **se o intervalo de 95% da
   diferença pareada para a segunda não contém zero**. Se contém, é **EMPATE**, e a escolha é
   dele, com critério escrito antes de escolher. Se só uma fica, ela vence sem comparação.
4. Com menos de 2 pessoas, não há intervalo: sai `SEM_DADOS`, e a regra não escolhe nada.

**O intervalo:** bootstrap pareado por pessoa, percentil, **10.000 reamostragens, semente
20260927**, nível 95%. Toda comparação usa a mesma semente. Nada disso tem opção de linha de
comando. O nível vem da 17a. A semente e o número de reamostragens foram fixados pela S5 e
estão declarados aqui.

**As hipóteses**, relatadas ao lado, sem mudar a regra:
- **H1** (16b): E − D em `confiavel` e em `honesto`, nas bases. **Confirmada** se os dois
  intervalos ficam acima de zero.
- **H2** (t-a): E − D e C − D, em `confiavel` e em `honesto`. **Confirmada** se, em pelo
  menos uma escala, os dois intervalos ficam acima de zero.
- **H3** (j-A), **exploratória**: rota bloqueada − base em `confiavel`, por direção. Saem
  "reduz", "aumenta" ou "sem evidência de redução".
- **H4:** fora do teste (s-a), na P-156.

Não há correção de multiplicidade entre H1, H2 e H3. `seguro` e `luxo` são descritivas.

**O que sai:** só agregado.
- aberturas, abandonos e descartes por motivo;
- **aberturas e abandonos por versão** (ab-a);
- válidas, no total e por versão;
- n de amigos;
- médias, diferenças e intervalos, com o n de cada amostra.

Nunca sai uma linha de resposta. O script não lê a pergunta aberta nem a de pronúncia. As
duas são lidas por ele, fora do repositório, como material exploratório. Não mudam a regra, e
nenhuma frase de participante entra no repositório.

## 8. O veto de distinção (decisão dele, 27/09; aa-a)

| arquivo | o que é | sha256 |
|---|---|---|
| `docs/marca/teste-de-marca/codigos-visuais.yaml` | o livro de códigos: seis variáveis com valores fechados, a regra de medida de cada uma, as categorias concorrentes, a definição de código dominante e de imitar | `1d32a59442693be97c6cc9628f422bb0509007fb9a205d1286365f1e1a14719b` |
| `tools/codigos_visuais.py` | o classificador e o veto, os mesmos para as direções e para as marcas da R3. Congelado desde 02/10: sem ele no conjunto, o cálculo do veto podia mudar depois de a R3 começar sem que nada reprovasse | `7bf3129599fffaea6b883d6e1512c47eeabe96fa8c7e6ed63fb38083711f7188` |

**As variáveis.**

| variável | central | valores | regra |
|---|---|---|---|
| fundo | sim | claro, escuro | luminância relativa da cor de maior área; claro se for maior que 0,179, o ponto em que texto preto e texto branco contrastam igual |
| matiz | sim | neutro e 12 faixas de 30° | a cor do botão principal (borda, se for vazado); neutro se a saturação HSL for menor que 0,15 |
| família do título | sim | serifa, sem serifa, monoespaçada | a fonte do **texto de maior corpo** da tela, fora o logotipo |
| raio | sim | reto, pequeno, grande | o raio do botão principal: até 2 px é reto; de 3 a 8 px, pequeno; de 9 px em diante, grande |
| densidade | não | baixa, média, alta | blocos de informação sem rolar: até 8, baixa; de 9 a 15, média; 16 ou mais, alta |
| botão | não | cheio, vazado | se o botão tem fundo próprio |

**As categorias concorrentes (ac-a, 02/10).** Fechadas aqui, e não na R3, porque a
classificação de E, C e D já está pública neste arquivo: quem escolhesse as categorias depois
poderia escolher o veto. Cada marca entra em **uma** categoria, a do app que se classifica.
Os exemplos vêm das rodadas 1 e 2 e só mostram a fronteira; **não são a lista de marcas da
R3**.

| categoria | o que entra | exemplos |
|---|---|---|
| `banco_tradicional` | banco de varejo com agência | Itaú, Bradesco, Banco do Brasil, Santander, Caixa |
| `banco_digital` | banco sem agência, de app; o investimento dentro do app do banco conta aqui | Nubank, Inter, C6, Neon |
| `corretora` | corretora ou banco de investimento com app próprio de investimento para pessoa física | XP, Rico, Clear, Toro, BTG Pactual, Genial |
| `gestora_e_private` | gestora de recursos ou private banking | Verde, Dynamo, SPX, Itaú Private |
| `pagamentos` | carteira ou conta de pagamento | PicPay, Mercado Pago, PagBank |
| `consolidador` | app de acompanhamento de carteira | Gorila, Kinvo |
| `casa_de_analise_e_educacao` | casa de análise ou marca de educação financeira | Empiricus, Suno, Me Poupe!, Primo Rico |
| `consultoria_cvm` *(ad-a)* | consultoria de valores mobiliários registrada na CVM (Resolução CVM 19), pessoa jurídica: **a categoria do próprio MEOL** | — |
| `assessor` *(ad-a)* | assessoria de investimento registrada na CVM (o antigo agente autônomo) | — |
| `robo` *(ad-a)* | robô de investimento: a pessoa responde um perfil e o app monta e rebalanceia a carteira | — |
| `planejador` *(ad-a)* | planejador financeiro pessoal com marca própria | — |

**Precedência (ad-a).** Marca que cabe em duas categorias fica com a primeira desta ordem:
robô, consultoria CVM, planejador, assessor, consolidador, corretora, gestora e private, casa
de análise e educação, pagamentos, banco digital, banco tradicional.

**A unidade na R3 (ae-a).** Com app: a primeira captura da App Store do Brasil que mostra a
interface, recortada na tela do aparelho, em 390 px. Sem app: a página inicial do site oficial
em 390 px, sem rolar. Cada marca registra qual foi usada; o dominante sai também **só com as de
app**, como sensibilidade, e o veto usa todas. A tela depois do login fica fora do alcance de
quem audita.

**A amostra (af-a).** A R3 sorteia pelo menos **10 marcas por categoria** para a classificação
visual, independentemente da saturação dos códigos MC, que é textual.

As **referências de sentimento** (rodada 2: SBB, Volvo) podem ser auditadas na R3 com a
categoria `referencia_de_sentimento`: entram classificadas e não acionam o veto. **Marca com
qualquer outra categoria reprova o classificador** (`veto()` levanta erro), para que nenhuma
marca entre ou saia do veto por um nome escrito na hora.

**A regra.**
- **Código dominante de uma categoria:** a combinação das **quatro variáveis centrais**
  presente em pelo menos metade das marcas classificadas, com **n ≥ 5** marcas. Com duas
  combinações na metade exata, as duas são dominantes.
- **Imitar:** a direção partilha os quatro valores centrais com um código dominante.
- **Se a vencedora pela 17a imitar**, a escolha volta para ele, com critério escrito.
- Categoria sem código dominante, ou com menos de 5 marcas, não aciona o veto.
- **A escolha da direção só sai com a R3 fechada.**

**A classificação de E, C e D, feita agora, antes de a R3 começar:**

| direção | fundo | matiz | família do título | raio | densidade (blocos) | botão |
|---|---|---|---|---|---|---|
| E | claro | laranja (37,5°) | serifa | reto (2 px) | média (12) | vazado |
| C | claro | rosa (317,9°) | sem serifa | grande (pílula) | média (12) | cheio |
| D | escuro | laranja (41,0°) | serifa | reto (0 px) | média (13) | cheio |

Três leituras para quem for aplicar o veto:
- **O título da E é com serifa.** O h1 da decisão herda a Source Serif do corpo; o token
  chamado `titulo` vale só para os rótulos em caixa alta.
- **A C está a 2,9° da fronteira** entre rosa e magenta (315°). Uma categoria de código
  magenta não a pega; uma de código rosa, sim.
- **E e D partilham matiz, família e raio**, e diferem só no fundo.

**Nada do livro se ajusta depois de a R3 começar.** Os limites de densidade foram escritos
depois de contar E, C e D e antes de qualquer marca; a densidade não entra no veto.

## 9. Limitações declaradas

**As que o prompt pediu:**
1. **Amostra de conveniência.** O resultado escolhe entre direções para quem respondeu. Não
   descreve o investidor brasileiro, nem a fatia que o MEOL quer atender.
2. **H3 exploratória, com ordem fixa.** A rota bloqueada vem sempre depois da base: a
   diferença mistura o efeito da rota com o de rever a tela e com o cansaço.
3. **Amigos com viés de agradar.** Por isso a análise dupla, e a sem eles decide.
4. **A plataforma registra metadados por conta própria** (lido na documentação em 27/09, em
   [`docs/fontes/vercel-supabase-metadados-de-acesso.md`](../../fontes/vercel-supabase-metadados-de-acesso.md)):
   - **CONFIRMADO:** a Vercel coleta o IP do visitante e a cidade e o país derivados dele, e
     guarda o log de runtime, com user agent e caminho, por **1 hora** no plano Hobby.
   - **CONFIRMADO:** o IP "para DDoS" ela coleta mesmo se o dono o esconder, por um prazo que
     não publica.
   - **CONFIRMADO:** o DPA da Vercel não cobre o Hobby.
   - **CONFIRMADO:** o Supabase guarda no log do gateway, por **1 dia** no Free, o IP, o user
     agent e a geolocalização até o CEP **de quem o chama**. Por isso o contrato proíbe o
     navegador de chamá-lo.
   - **CONFIRMADO (02/10):** o painel do Firewall da Vercel agrupa o tráfego por IP de
     origem e por user agent, numa janela de até 24 horas. `NAO_CONFIRMADO`: se esse painel
     existe no plano Hobby.
   - `NAO_CONFIRMADO`: se dá para desligar os logs, o prazo do IP de DDoS e a região física
     dos logs.
   - A tabela da pesquisa não tem IP. A plataforma tem.
5. **O resultado escolhe entre direções e não descreve o investidor brasileiro.**

**As dos textos decididos (w-a, x-a), que o ensaio apontou.** As 6 e 7 vinham da y-b; a
y-a (02/10/2026) devolveu os textos da v-a e da u-a, e elas saem. O texto fica riscado, como
registro.

6. ~~**Filtro com jargão.** "Aporta" e "renda variável" podem não ser entendidos, e quem só
   aplica no Tesouro pode marcar "sim".~~ *Sai pela y-a: o filtro nomeia ações, ETF e fundos
   imobiliários.* **Fica:** "todo mês" é absoluto, e quem pulou um mês decide sozinho se
   arredonda.
7. ~~**A pergunta dos amigos vem antes de qualquer tela.** "Este app" ainda não se refere a
   nada, e quem conhece o autor pode responder "não". A amostra que decide pode ter amigos.~~
   *Sai pela y-a: a pergunta nomeia a pessoa que faz a pesquisa, e não um app.*
8. **"Segurança"** pode ser lida como risco do investimento, não da tela. **"Popular"** pode
   ser lido como "famoso". As duas escalas são descritivas e não entram na regra.
9. **`para_mim` e `honesto` sofrem o conteúdo, que é o mesmo nas três direções:** R$ 800 e
   "aporte". Isso afeta o nível das notas mais que a comparação. A frase-cabeça das escalas
   reduz o efeito, mas não o elimina.
10. **"Parece golpe"** planta a suspeita, repetida seis vezes (x-a).

**As das imagens, que estão congeladas:**

11. "Cofrinho de banco digital: bloqueado" pode ser lido como "sua conta foi bloqueada", e
    isso pesa na H3. Na D, a caixa da rota bloqueada tem pouco contraste e pode não ser vista
    em 5 segundos.
12. O aviso da tarifa da B3 e o selo "Parcial" parecem erro. Estão nas três direções.
13. O cartão da D parece oferta de cartão de crédito.
14. "M E O L" aparece espaçado na E e na D, e a pronúncia pode depender da última direção
    vista.
15. A C lembra um app de banco digital, o que pode puxar `para_mim` por familiaridade.

**As do instrumento e da análise:**

16. **Rodízio por contador de aberturas.** Quem abandona gasta uma versão, e quem reabre o
    link abre de novo. O relatório traz aberturas e abandonos por versão e não pondera.
17. **Respostas duplicadas não são detectáveis.** Sem e-mail nem IP na tabela, a mesma pessoa
    pode responder duas vezes.
18. **Bootstrap percentil com amostra pequena** dá intervalo mais estreito do que deveria. Com
    poucas pessoas, a regra pode declarar vencedora com evidência mais fraca do que os 95%
    sugerem. Cada intervalo sai com o n ao lado.
19. **Os 5 segundos são de tela, não de atenção.** A página esconde a imagem, mas não sabe se a
    pessoa olhou.
20. **O livro de códigos mede o que o classificador declara.** A família da fonte vem do
    genérico do CSS nas direções e do olho de quem classifica nas marcas da R3. E a fronteira
    de matiz da C fica a 2,9°.
21. **Uma categoria por marca** (ac-a). Marca com mais de um negócio (o Itaú do varejo e o
    Itaú Private; o Nubank e o Nu Invest dentro dele) entra pela categoria do app que se
    classifica, e a escolha do app é de quem classifica na R3. Crédito (Serasa) não está na
    lista nem fora do veto: uma marca só de crédito não tem categoria no livro, e o
    classificador a recusa se ela aparecer no arquivo do veto.
22. **A unidade da R3 não é a das direções** (ae-a). E, C e D são a tela do app inteira; as
    marcas são a captura de marketing da App Store, escolhida pela marca, ou o site, que é
    página de venda e não tela de uso. O dominante só com as de app mede o tamanho dessa
    diferença; não a elimina.

## 10. Mudanças depois do merge

- **Antes do primeiro convite:** qualquer mudança num dos dez arquivos é pré-registro novo.
  Esta página muda no mesmo commit, com o motivo, e o teste de sha256 reprova se não mudar.
- **Depois do primeiro convite:** nada muda. Defeito achado durante a coleta vai para o
  relatório como **desvio do pré-registro**.
- **O livro de códigos não muda depois de a R3 classificar a primeira marca**, mesmo antes do
  primeiro convite.
- **O relatório** dá o resultado sem amigos, o resultado com todos, se os dois divergem, e o
  veto aplicado à vencedora com a R3 fechada.
- **02/10/2026, y-a (dele), antes do primeiro convite.** O `questionario.yaml` mudou: filtro
  da v-a, pergunta dos amigos da u-a, e o convite e a tela de conclusão com o critério do
  filtro. sha256 de `73936c74…757a` para `02773d8b…8091` (§4). O `questionario.md` e o
  `pesquisa/questionario.json` foram regenerados pelos geradores, com `--conferir`. Os ids,
  as opções e as saídas não mudaram, e a análise não lê o texto das perguntas, então o
  `tools/analise_teste_marca.py` e o seu sha256 ficam.

## 11. Privacidade

A página não pede nome, e-mail nem login. A tabela não guarda IP, user agent nem hora (§4). A
exportação fica em `data/teste-marca/`, que o git ignora. O script recusa ler um CSV que o git
não ignore, e o teste reprova se uma exportação aparecer no repositório. No repositório entra
só o agregado.

## 12. Até o primeiro convite, em ordem

1. Merge deste pré-registro no `main` (ele).
2. A página, na S6, pelo `questionario.yaml` e pelas exigências da §4, e o merge dela no
   `main`.
3. Uma resposta de teste e `--conferir-cabecalho` sobre a exportação real da página.
4. Commit das datas da janela (§6), empurrado.
5. Primeiro convite.
