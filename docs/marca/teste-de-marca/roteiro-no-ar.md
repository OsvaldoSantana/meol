# Pôr a página do teste de marca no ar (P-162)

*Escrito em 02/10/2026 (S6), movido sem edição do `PENDENCIAS.md` em 03/10. **Revisto em
04/10/2026, sessão na nuvem (rosto):** o passo 0 foi decidido por ele (fila, bloco 24: **24b**);
o passo 5 mandava conferir o sha256 de antes da y-a (`73936c74…`, retratação abaixo); e os
passos 8 e 9, o commit das datas e o convite, viraram tutorial. O que a página faz está em
[`pesquisa/README.md`](../../../pesquisa/README.md). As contas e as chaves são dele: **nenhuma
chave vai para o chat nem para o repositório** (§5-A.7).*

> **Retratação, 04/10/2026.** O passo 5 dizia que o `questionario_sha256` da resposta de teste
> é `73936c74…`. **Evidência que derruba:** a y-a (`6cb42c5`, 02/10) trocou o `questionario.yaml`
> e o sha256 passou a `02773d8b…` (pré-registro final, §4 e §10); o `pesquisa/questionario.json`
> já carrega o novo. **Causa raiz:** o roteiro nasceu no S6 (`047f6f4`) com o sha256 da hora, e
> a y-a, no mesmo dia, mudou o arquivo sem procurar quem citava o valor antigo. **O que muda:**
> `tools/test_roteiro_no_ar.py` reprova se o roteiro citar um prefixo que não seja o do
> questionário de hoje.

**Tempo:** os passos 1 a 5 levam cerca de 40 minutos e dão para fazer pelo celular. O 6 exige o
desktop. A ordem não se troca: **nenhum convite sai antes do passo 8 estar no `main`.**

---

## 0. O plano da Vercel — decidido: Hobby (24b)

Decisão dele em 04/10/2026, com a leitura escrita na fila (bloco 24). Se a Vercel pausar o
deploy durante a janela, isso é desvio do pré-registro e vai para o relatório com as datas; a
janela não se estende.

## 1. Criar o projeto no Supabase

1. Entre em **supabase.com** → *Dashboard* → **New project**.
2. *Name*: `meol-pesquisa` (qualquer nome serve). *Region*: **South America (São Paulo)**.
   *Plan*: **Free**.
3. *Database Password*: gere e guarde no seu gerenciador de senhas. Ela não volta para nenhum
   lugar deste roteiro.
4. **Create new project.** Espere o painel sair de "Setting up project" (1 a 2 minutos).

## 2. Criar as tabelas e provar que o público não lê nada

1. Menu da esquerda → **SQL Editor** → **New query**.
2. Abra no GitHub o arquivo
   [`pesquisa/supabase/esquema.sql`](../../../pesquisa/supabase/esquema.sql) → botão **Raw** →
   selecione tudo e copie. Cole no editor do Supabase → **Run**.
   **Deve aparecer:** "Success. No rows returned".
3. **New query** de novo. Faça o mesmo com
   [`pesquisa/supabase/teste_politicas.sql`](../../../pesquisa/supabase/teste_politicas.sql) →
   **Run**. **Tem de terminar sem erro.** Se aparecer uma mensagem com **"FALHA: …"**, o
   público pode mais do que deve: **pare** e traga a mensagem para a sessão. O teste desfaz o que
   fez (`rollback`).

## 3. Copiar as duas chaves (só as públicas)

1. No topo do projeto, botão **Connect** (ou *Project Settings → API Keys*).
2. Copie a **Project URL** (começa com `https://` e termina em `.supabase.co`).
3. Copie a **Publishable key** (começa com `sb_publishable_`).
4. **Nunca a secret key** (`sb_secret_…`): ela passa por cima das regras de acesso. A chave
   `anon` antiga (um texto longo que começa com `eyJ`) também funciona, mas o Supabase a
   descontinua até o fim de 2026.

## 4. Publicar na Vercel

1. **vercel.com** → **Add New… → Project** → importe o repositório `OsvaldoSantana/meol`.
2. **Root Directory:** clique em *Edit* e escolha **`pesquisa`**.
3. **Framework Preset: Other.** Sem *Build Command* e sem *Output Directory*.
4. **Environment Variables**, duas:
   - `SUPABASE_URL` = a Project URL do passo 3;
   - `SUPABASE_ANON_KEY` = a Publishable key do passo 3.

   Cole direto no painel da Vercel; não passe por chat, e-mail nem bloco de notas sincronizado.
5. **Deploy.** Espere "Congratulations". Anote a URL de produção (algo como
   `https://meol-pesquisa.vercel.app`; o nome exato é o que a Vercel der).
6. **Não ligue** *Web Analytics* nem *Speed Insights* (aba *Analytics* do projeto). Eles vêm
   desligados, e o contrato de privacidade os quer desligados.

## 5. Conferir no ar, com uma resposta de teste

1. Abra `<sua URL>/README.md` e `<sua URL>/supabase/esquema.sql`. **Os dois têm de dar 404.**
   O `.vercelignore` os tira do ar, e este passo é a prova.
2. Abra `<sua URL>` e **responda a pesquisa uma vez, até o fim**.
3. No Supabase → **Table Editor**:
   - `aberturas` tem **1 linha**;
   - `respostas` tem **1 linha**, e a coluna `questionario_sha256` começa com **`02773d8b`**
     (o do pré-registro final, §4). Se começar com outra coisa, **pare**: a página no ar não é a
     do `main`.

## 6. ⚙ No desktop: conferir o cabeçalho da exportação real

1. No Supabase → **SQL Editor** → **New query** → cole
   [`pesquisa/supabase/exportar.sql`](../../../pesquisa/supabase/exportar.sql) → **Run**.
2. Botão **Export → Download CSV**. Salve como `data/teste-marca/respostas.csv`, dentro da
   pasta do repositório (a pasta `data/` é ignorada pelo git: a resposta nunca vai para o
   GitHub).
3. No terminal, na pasta do repositório:

   ```powershell
   py -3.11 tools/analise_teste_marca.py --conferir-cabecalho
   ```

   **Tem de aparecer `ok`.** Se não aparecer, **pare**: o cabeçalho da exportação real é o
   último ponto que nenhum teste viu, e a análise do dia 21 dependeria dele.

## 7. Apagar a resposta de teste

1. No Supabase → **SQL Editor** → **New query** → cole e **Run**:

   ```sql
   delete from public.respostas; delete from public.aberturas;
   update public.contador_de_aberturas set aberturas = 0;
   ```

2. **Table Editor:** as duas tabelas vazias.
3. Apague o `data/teste-marca/respostas.csv` do teste.

O contador volta a 0 porque as aberturas de teste não são da janela (ab-a). **Depois do
primeiro convite, nada mais se apaga.**

## 8. O commit das datas da janela (pré-registro final, §6)

**Escolha o dia 1:** é o dia em que você vai mandar o **primeiro** convite. O dia 21 é o dia 1
mais 20 dias (21 dias corridos, contando os dois, em Brasília).

| dia 1 | dia 21 | | dia 1 | dia 21 |
|---|---|---|---|---|
| 2026-10-05 (seg) | 2026-10-25 | | 2026-10-10 (sáb) | 2026-10-30 |
| 2026-10-06 (ter) | 2026-10-26 | | 2026-10-11 (dom) | 2026-10-31 |
| 2026-10-07 (qua) | 2026-10-27 | | 2026-10-12 (seg) | 2026-11-01 |
| 2026-10-08 (qui) | 2026-10-28 | | 2026-10-13 (ter) | 2026-11-02 |
| 2026-10-09 (sex) | 2026-10-29 | | 2026-10-14 (qua) | 2026-11-03 |

**Pelo GitHub, no celular ou no computador:**

1. Abra `github.com/OsvaldoSantana/meol/blob/main/docs/marca/teste-de-marca/preregistro-final.md`.
2. Toque no **lápis** (*Edit this file*).
3. Procure a §6, "A janela". Há duas linhas que terminam em
   `**a preencher no commit das datas**`. Troque **só o que está entre os asteriscos**:

   ```text
     - dia 1 (primeiro convite): **2026-10-08**
     - dia 21 (último dia): **2026-10-28**
   ```

   (com as suas datas, no formato `AAAA-MM-DD`; nada mais muda no arquivo).
4. **Commit changes…** → marque **Create a new branch for this commit and start a pull
   request** → nome da branch: `p162-datas-da-janela` → **Propose changes**.
5. Título do PR, exatamente neste formato (o CI reprova sem a etiqueta):

   ```text
   [modelo=desconhecido classe=pre-registro] P-162: datas da janela (dia 1 = 2026-10-08)
   ```

   `desconhecido` porque a edição é sua, e a tabela de modelos não tem valor para pessoa.
6. **Create pull request.** Espere o **Testes** ficar verde (uns 5 minutos).
   `tools/test_roteiro_no_ar.py` reprova se o dia 21 não for o dia 1 + 20, ou se a data não
   estiver em `AAAA-MM-DD`.
7. **Merge pull request** → **Confirm merge.**

**Se o dia 1 escorregar** (você não conseguir mandar o convite no dia escrito): **não mande
em outro dia.** Repita os passos 1 a 7 com as datas novas antes de qualquer convite. Depois do
primeiro convite, as datas não mudam mais.

## 9. O primeiro convite, no dia 1

**O texto é o do pré-registro** (`questionario.yaml → convite.texto`, congelado pelo sha256).
Mande **exatamente este**, trocando só `{link}` pela URL de produção do passo 4:

```text
Oi! Estou fazendo uma pesquisa curta, de uns 8 minutos, sobre como as pessoas percebem telas de aplicativos de investimento. É para quem, há pelo menos 6 meses, coloca dinheiro todo mês em ações, fundos de índice (ETF) ou fundos imobiliários. Ela não pede dinheiro, cadastro, nome nem e-mail. O link abre a página da pesquisa: {link}
```

1. **Quem recebe:** a sua rede pessoal, em mensagem individual (WhatsApp, por exemplo). Sem
   anúncio, sem painel pago e sem grupo ou comunidade aberta (recrutamento, §2).
2. **O mesmo link para todos.** Nada de `?nome=` nem link encurtado com rastreio: a página não
   pode saber quem abriu.
3. **Bola de neve:** o texto congelado não pede para repassar. Se alguém perguntar se pode
   mandar a outra pessoa, a resposta é sim, com o mesmo texto. Não escreva uma segunda mensagem
   pedindo repasse: texto novo de recrutamento não está no pré-registro.
4. **Sem promessa de produto.** Não diga o que o MEOL é, que vai lançar, nem peça opinião sobre
   investimento. Se perguntarem, "é uma pesquisa sobre como as pessoas percebem telas de
   aplicativos" basta, e é o que o pré-registro cobre (o portão da P-158 vale para texto
   comercial).
5. **Durante os 21 dias, não olhe as notas.** O Table Editor mostra respostas; contar linhas
   para saber quantos responderam pode, abrir as colunas das escalas não. O script recusa a
   análise antes do fim do dia 21, e quem decide quando parar é a data, não o resultado (h-A).

## 10. Depois do dia 21

1. ⚙ No desktop, a exportação de novo (passo 6, itens 1 e 2).
2. `py -3.11 tools/analise_teste_marca.py --inicio <o dia 1>`.
3. **Só o agregado entra no repositório:** contagens, médias, intervalos e o n de cada amostra.
   Nenhuma linha de resposta e nenhuma frase de participante. As perguntas abertas (o que a
   pessoa lembra e a pronúncia) são lidas por você, fora do repositório.
4. A direção só sai com a R3 fechada (P-170): o veto se aplica à vencedora.
