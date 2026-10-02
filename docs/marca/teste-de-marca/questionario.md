# Teste de marca — o questionário (versão de leitura)

*GERADO de `questionario.yaml` por `tools/questionario_teste_marca.py`. Não edite: `--conferir` reprova. Quem vale é o YAML, cujo sha256 está no pré-registro final.*

Versão 2, 2026-09-27.

## 1. O convite (mensagem, fora da página)

> Oi! Estou fazendo uma pesquisa curta, de uns 8 minutos, sobre como as pessoas percebem telas de aplicativos de investimento. É para quem, há pelo menos 6 meses, coloca dinheiro todo mês em ações, fundos de índice (ETF) ou fundos imobiliários. Ela não pede dinheiro, cadastro, nome nem e-mail. O link abre a página da pesquisa: {link}

## 2. Consentimento

> Concordo em participar: a pesquisa não pede nome nem e-mail, as notas são analisadas em conjunto, e se eu parar no meio nada do que respondi é guardado.

Opções: `Concordo` · `Não concordo`. "Não concordo" leva à saída.

## 3. Filtro de entrada

> Há pelo menos 6 meses, você coloca dinheiro todo mês em ações, fundos de índice (ETF) ou fundos imobiliários?

Opções: `Sim` · `Não`. "Não" leva à saída.

## 4. A pergunta dos amigos

> Você conhece pessoalmente a pessoa que está fazendo esta pesquisa (é amigo, parente ou colega dela)?

Opções: `Sim` · `Não`. Todos seguem; a análise sai com e sem quem responde "Sim", e a sem eles decide (r-a).

## 5. As 6 telas

Antes de cada imagem, a instrução:

> Você vai ver 6 telas de um aplicativo de investimento. Quando tocar em "Ver a tela", ela aparece por 5 segundos e some sozinha; não dá para voltar a ela. Depois vêm as perguntas. Olhe a imagem inteira, sem tentar ler cada palavra. As telas são exemplos inventados: os valores e o investimento não são recomendação para você. Algumas telas se parecem ou se repetem com pequenas mudanças, de propósito: dê as notas pelo que vir agora.

Antes das telas 2 em diante, a instrução curta (aqui, a da tela 2):

> Tela 2 de 6: toque em "Ver a tela"; ela fica 5 segundos.

A imagem aparece quando a pessoa toca em "Ver a tela", fica **5 segundos**, some, e só então vêm as perguntas; não há como voltar a ela, e ela cabe inteira na tela, sem rolar. As telas 1 a 3 são as três direções na versão base; as 4 a 6, as mesmas três, na mesma ordem, com a rota bloqueada.

1. **Aberta** (`lembra`, não obrigatória): O que você lembra desta tela? Escreva com as suas palavras.
2. **Cinco escalas de 1 a 7, obrigatórias**, sob a frase "Responda pelo que a tela passa, não pelo investimento que ela mostra.", nesta ordem; o 1 fica à esquerda, o 7 à direita, e o meio não tem rótulo:

| id | pergunta | polo do 1 | polo do 7 |
|---|---|---|---|
| `seguro` | Pelo jeito da tela (cores, letras, formas), esta tela passa insegurança ou segurança? | Insegurança | Segurança |
| `para_mim` | Pelo visual, esta tela parece feita para alguém como você? | Não é para mim | É para mim |
| `honesto` | Esta tela parece querer te vender algo ou parece honesta? | Quer me vender algo | Honesta |
| `confiavel` | Esta tela parece golpe ou parece confiável? | Parece golpe | Confiável |
| `luxo` | O visual desta tela lembra mais um app popular ou um app de luxo? | Popular | De luxo |

## 6. A pronúncia do nome

> Nas telas apareceu o nome do app, MEOL. Como você o falaria em voz alta? Escreva o som, do seu jeito.

## 7. As mensagens finais

- **Quem respondeu tudo:** Obrigado! A sua resposta foi registrada. Se conhecer alguém que também coloque dinheiro todo mês em ações, fundos de índice (ETF) ou fundos imobiliários, pode repassar o link.
- **Quem não concordou:** Tudo bem, obrigado pelo seu tempo! Só ficou registrado que você preferiu não participar.
- **Quem não passou no filtro:** Obrigado pelo seu tempo! Esta pesquisa procura um perfil específico.

## 8. As seis ordens

Atribuição: versao = (contador_de_aberturas mod 6) + 1; o contador comeca em 0 e soma 1 a cada abertura, conclua ou nao.

| versão | telas 1 a 3 (base) e 4 a 6 (com rota bloqueada) |
|---|---|
| 1 | E, C, D |
| 2 | E, D, C |
| 3 | C, E, D |
| 4 | C, D, E |
| 5 | D, E, C |
| 6 | D, C, E |

## 9. O contrato da exportação (a página da S6 grava assim)

Arquivo `data/teste-marca/respostas.csv` (fora do git), utf-8, separador `,`, uma linha por **abertura** da página. As respostas só são gravadas no envio final: quem para no meio deixa só a versão e o dia da abertura, com `concluida_em` vazio. Quem sai pelo consentimento ou pelo filtro conclui ali, e só a resposta que o tirou fica gravada. Datas: AAAA-MM-DD, no fuso de Brasilia, sem hora. Colunas, nesta ordem:

- fixas: `id_resposta`, `versao`, `aberta_em`, `concluida_em`, `consentimento`, `filtro`, `amigo`;
- por tela: t{k}_{id}, para k de 1 a 6 e id em lembranca.id e escalas[].id;
- finais: `pronuncia`.

Nada de IP, nome ou e-mail. Exigências de privacidade para a página (ver `docs/fontes/vercel-supabase-metadados-de-acesso.md`):

- o navegador nunca chama o Supabase; a gravação passa por uma função no servidor da Vercel;
- a função não repassa ao Supabase os cabeçalhos do cliente (x-forwarded-for, x-real-ip, user-agent);
- o link é o mesmo para todos, sem identificador na URL nem na query;
- Web Analytics e Speed Insights da Vercel desligados; nenhum cookie; nenhum script de terceiros;
- a função não escreve resposta nem cabeçalho no log (console.log);
- o envio é POST, com as respostas no corpo; nenhuma resposta vai na URL nem na query;
- a tabela não tem IP, nome, e-mail, user agent nem hora.

## 10. A janela

21 dias corridos, no fuso `America/Sao_Paulo`; conta o instante `concluida_em`. As datas absolutas entram num commit próprio, antes do primeiro convite.
