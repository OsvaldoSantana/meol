# Teste de marca — o questionário, com o texto exato de cada tela

> **SUPERADO em 27/09/2026, sem ter sido usado: nenhum convite saiu.** Ele trocou o Google
> Forms por uma página própria (Vercel e Supabase, S6) e acrescentou o veto de distinção
> (fila, "Decisões dele, 27/09/2026, trazidas pelo prompt da S5 v2"). Vale
> [`docs/marca/teste-de-marca/preregistro-final.md`](teste-de-marca/preregistro-final.md).
> Este questionário fica como registro e não se edita; o vigente é
> [`teste-de-marca/questionario.yaml`](teste-de-marca/questionario.yaml).

*27/09/2026, S5. Parte do pré-registro final (`preregistro-teste-de-marca-final.md`), que
grava o sha256 deste arquivo. **Mudar uma vírgula depois do merge é questionário novo**, e o
pré-registro deixa de cobri-lo. A seção 9 diz o que mudou por causa do ensaio.*

O formulário é um Google Forms, montado seis vezes (uma por ordem das direções, seção 8).
Configuração obrigatória em todas as seis versões:

- **não coletar e-mail** e não pedir login (Configurações → Respostas);
- **fuso horário do formulário: (GMT-03:00) Brasília**, porque a janela de coleta é em
  horário de Brasília (h-A);
- toda pergunta marcada como **obrigatória**, menos as abertas ("o que você lembra" e a de
  pronúncia);
- **uma seção por imagem e uma seção por bloco de perguntas**, para a imagem sumir quando a
  pessoa avança para as perguntas;
- **os títulos das perguntas exatamente como estão aqui**: o script de análise acha cada
  coluna pelo título.

---

## 1. O convite (mensagem, fora do formulário)

Enviado por mensagem, com o link da versão da vez (rodízio, seção 8). Sem promessa de
produto e sem nome de investimento (P-158):

> Oi! Estou fazendo uma pesquisa curta, de uns 8 minutos, sobre como as pessoas percebem
> telas de aplicativos de investimento. É para quem coloca dinheiro todo mês em ações, fundos
> de índice (ETF) ou fundos imobiliários. Não é venda: não tem nada sendo oferecido e não pede
> nome, e-mail nem nenhum dado pessoal. O link abre um formulário do Google: [link]

## 2. Consentimento (seção 1 do formulário)

**Título da seção:** Pesquisa sobre telas de investimento

**Texto:**
> Esta é uma pesquisa independente, feita por uma pessoa, não por uma empresa. As respostas
> são anônimas: o formulário não guarda nome nem e-mail. Você pode parar a qualquer momento, e
> nada é cobrado nem instalado. As notas são somadas com as de todas as pessoas; as respostas
> escritas são lidas, sem saber de quem são.

**Pergunta (múltipla escolha, obrigatória):**
- Título: `Concordo em participar`
- Opções: `Concordo` · `Não concordo`
- "Não concordo" leva à seção de saída (seção 7b).

## 3. Filtro de entrada (seção 2)

**Pergunta (múltipla escolha, obrigatória):**
- Título: `Há pelo menos 6 meses, você coloca dinheiro todo mês em ações, fundos de índice (ETF) ou fundos imobiliários?`
- Opções: `Sim` · `Não`
- "Não" leva à seção de saída (seção 7b).

## 4. A pergunta dos amigos (seção 3)

**Pergunta (múltipla escolha, obrigatória):**
- Título: `Você conhece pessoalmente a pessoa que está fazendo esta pesquisa (é amigo, parente ou colega dela)?`
- Opções: `Sim` · `Não`

Todas as respostas seguem, com "sim" ou "não". A análise sai com e sem quem respondeu
"sim"; **a sem eles decide** (r-a).

## 5. As seis telas (seções 4 a 15, duas por tela)

A ordem das imagens depende da versão (seção 8): as telas 1, 2 e 3 são as três direções na
versão **base**, e as telas 4, 5 e 6 são as mesmas três direções, **na mesma ordem**, na
versão **com rota bloqueada** (j-A).

### Seção da imagem (uma por tela, k = 1 a 6)

- **Título da seção:** `Tela k de 6`
- **Texto:**
  > Olhe a imagem inteira por uns 5 segundos, sem ler cada palavra. As telas são exemplos
  > inventados: os valores e o investimento não são recomendação para você. Algumas telas se
  > parecem; responda sobre cada uma como se fosse a primeira vez que a vê. Depois clique em
  > Próxima e responda sem voltar.
- **Imagem:** o PNG da vez, sem legenda e sem nome de arquivo à mostra.

### Seção das perguntas (logo depois, k = 1 a 6)

- **Título da seção:** `Sobre a tela k`

1. **Pergunta aberta (parágrafo, não obrigatória).**
   - Título: `[Tela k] O que você lembra desta tela? Escreva com as suas palavras.`
2. **Cinco escalas lineares de 1 a 7, obrigatórias**, nesta ordem. Em todas, o **1** fica à
   esquerda, o **7** à direita, e o número 4 não tem rótulo. **A ordem das palavras no título
   é a mesma da escala** (o que vem primeiro no título fica no 1).

| título exato | rótulo do 1 | rótulo do 7 | nome na análise |
|---|---|---|---|
| `[Tela k] Pelo jeito da tela (cores, letras, desenho), este app passa insegurança ou segurança?` | `Insegurança` | `Segurança` | `seguro` |
| `[Tela k] Pelo visual, esta tela parece feita para alguém como você?` | `Não é para mim` | `É para mim` | `para_mim` |
| `[Tela k] Esta tela parece querer te vender algo ou parece honesta?` | `Quer me vender algo` | `Honesta` | `honesto` |
| `[Tela k] Esta tela parece golpe ou parece confiável?` | `Parece golpe` | `Confiável` | `confiavel` |
| `[Tela k] O visual desta tela lembra mais um app popular ou um app de luxo?` | `Popular` | `De luxo` | `luxo` |

Em todas as escalas, **7 é o polo que o nome na análise diz**. A de luxo não é avaliativa
(mais luxo não é "melhor"). A regra de decisão usa `confiavel`, `para_mim` e `honesto`; a
H2 usa `confiavel` e `honesto`; `seguro` e `luxo` são descritivas.

## 6. A pronúncia do nome (seção 16)

**Pergunta aberta (resposta curta, não obrigatória).**
- Título: `Como VOCÊ falaria em voz alta o nome MEOL? Escreva o som, do seu jeito (por exemplo, para "XP" alguém escreveria "xis-pê").`

## 7. As seções finais

**7a. Para quem respondeu tudo:**
> Obrigado! A sua resposta foi registrada. Se conhecer alguém que também coloque dinheiro
> todo mês em ações, fundos de índice ou fundos imobiliários, pode repassar o link.

**7b. Para quem não concordou ou não passou no filtro:**
> Obrigado pelo seu tempo! Esta pesquisa é só para quem coloca dinheiro todo mês em ações,
> fundos de índice ou fundos imobiliários há pelo menos 6 meses.

## 8. As seis versões: uma por ordem das direções (g-B)

Cada versão é **um formulário separado**, idêntico aos outros em tudo menos a ordem das
imagens. O rodízio envia a versão 1 ao primeiro convidado, a 2 ao segundo, e assim por
diante, voltando à 1 depois da 6. O repasse na bola de neve leva o link de quem repassou, e
isso desequilibra o rodízio: fica declarado, e o script imprime quantas respostas cada versão
teve.

| versão | telas 1, 2, 3 (base) | telas 4, 5, 6 (com rota bloqueada) |
|---|---|---|
| 1 | E, C, D | E, C, D |
| 2 | E, D, C | E, D, C |
| 3 | C, E, D | C, E, D |
| 4 | C, D, E | C, D, E |
| 5 | D, E, C | D, E, C |
| 6 | D, C, E | D, C, E |

As imagens são os seis PNG aprovados em 27/09/2026, com os sha256 gravados no pré-registro:
a direção X na versão base é `docs/marca/direcoes/png/X-base.png`, e na versão com rota
bloqueada é `docs/marca/direcoes/png/X-rota-bloqueada.png`.

**A versão fica registrada em cada resposta** pelo arquivo: a exportação de cada formulário
é salva como `data/teste-marca/versao-N.csv` (fora do git), e o script marca cada linha com
o N do arquivo.

## 9. O ensaio, e o que mudou por causa dele

Em 27/09/2026 um subagente respondeu a versão 3 três vezes, como três investidores leigos
(um que investe pelo app de um banco grande e lê pouco; um de 55 anos, desconfiado, que saiu
da poupança há um ano; um de 25 anos que investe por fintech e lê correndo), olhando os seis
PNG. **Nada do ensaio é dado, e nada dele entra na análise.** Ele achou 16 problemas; o que
mudou:

| achado do ensaio | mudança | de quem |
|---|---|---|
| a pergunta dos amigos fala de um app e de um criador que ninguém nomeou | pergunta sobre a pessoa que faz a pesquisa | ele (u-a) |
| o filtro usa jargão ("aporta", "renda variável") | filtro em linguagem comum; o convite diz o mesmo critério | ele (v-a) |
| "segura ou arriscada" mistura tela com produto; "sofisticada ou simples" tem sentidos opostos | escalas reescritas pelo visual | ele (w-a) |
| "honesta ou vendedora" e "parece golpe" | construtos mantidos, rótulos claros; sugestão de "golpe" declarada | ele (x-a) |
| em 4 das 5 escalas, a ordem das palavras era o contrário da escala | a ordem do título segue a escala | redação |
| nada avisava que as telas 4 a 6 repetem as 1 a 3 | "algumas telas se parecem; responda como se fosse a primeira vez" | redação |
| o convite nega venda e a tela manda aportar | "as telas são exemplos inventados; não são recomendação para você" | redação |
| "role para baixo" não é como o Forms navega; "com calma" contradiz "5 segundos" | "clique em Próxima"; "sem ler cada palavra" | redação |
| "Este app é para alguém como você?" troca tela por app e mede o valor, não o visual | "Pelo visual, esta tela parece feita para alguém como você?" | redação |
| a pronúncia dependia de lembrar o nome | o nome aparece no próprio texto, com um exemplo | redação |
| a mesma mensagem final para quem respondeu e para quem saiu | duas seções finais | redação |
| o consentimento dizia "só o resultado somado" e as respostas abertas são lidas | o texto diz que as respostas escritas são lidas, sem saber de quem | redação (corrige erro da S5) |
| o convite com link e pedido de repasse lembra golpe de mensagem | o convite diz que o link é do Google; o repasse foi para a seção final | redação |

**O que o ensaio achou nas imagens, que estão congeladas (aprovadas em 27/09) e não mudaram:**
vão como limitação para o pré-registro final.
- "Cofrinho de banco digital: bloqueado" pode ser lido como "sua conta foi bloqueada", o
  texto típico de golpe; isso puxa "golpe" para baixo por um motivo que não é a marca, **na
  H3**, que já é exploratória.
- "A tarifa da B3 tem duas fontes que ainda não batem" e o selo "Parcial" foram lidos como
  aviso de erro; como estão nas três direções, afetam o nível, não a comparação entre elas.
- O cartão dourado da D foi lido como oferta de cartão de crédito, o que tende a puxar
  "quer me vender algo": é parte do que a D testa (a ostentação), mas o efeito do objeto
  "cartão" não se separa do efeito da estética.
- O nome aparece como "MEOL" na C e "M E O L" espaçado na E e na D; a pronúncia pode
  depender da última direção vista.
- A C lembrou a uma persona "o app do meu banco"; isso pode puxar "é para mim" por
  familiaridade.
