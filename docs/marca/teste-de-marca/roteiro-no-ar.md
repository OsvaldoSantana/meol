# Pôr a página do teste de marca no ar (P-162)

*Movido em 03/10/2026, sem edição, do item 10 de "Ao voltar ao desktop" do `PENDENCIAS.md`
(escrito em 02/10/2026, na S6), quando a seção foi encurtada. É roteiro, e por isso mora aqui e
não no histórico.*

10. **02/10/2026 — P-162, pôr a página da pesquisa no ar (S6).** Só **depois do merge** do PR
   da S6. Dá para fazer **no celular ou no computador**; nada exige o desktop, menos o passo 6
   (rodar a análise no `data/` dele). As contas e as chaves são dele: **nenhuma chave vai para o
   chat nem para o repositório** (§5-A.7). O que a página faz está em `pesquisa/README.md`.
   0. **Decidir o plano da Vercel.** O Hobby (grátis) é "restricted to non-commercial personal
      use only", e uso comercial é qualquer deploy "used for the purpose of financial gain of
      **anyone** involved" (`vercel.com/docs/limits/fair-use-guidelines`, lido em 02/10). A
      página não cobra, não anuncia e não vende, mas testa a marca de um produto possível. Se
      é uso comercial, é decisão dele: Hobby, Pro, ou perguntar ao suporte da Vercel.
   1. **Supabase, plano Free:** criar o projeto (*New project*), região **South America (São
      Paulo)**. A senha do banco fica no gerenciador de senhas dele.
   2. **SQL Editor → New query:** colar `pesquisa/supabase/esquema.sql` inteiro e rodar
      (*Run*). Depois, numa query nova, colar `pesquisa/supabase/teste_politicas.sql` e
      rodar. **Tem de terminar sem erro.** Um erro com "FALHA: …" quer dizer que o anon pode
      mais do que deve: **parar** e trazer a mensagem. O teste desfaz o que fez (`rollback`).
   3. **As duas chaves:** no botão *Connect* do projeto (ou *Settings → API Keys*), copiar a
      **Project URL** e a **Publishable key** (`sb_publishable_…`). **Nunca a secret key**
      (`sb_secret_…`), que passa por cima do RLS. A chave `anon` antiga (um texto longo que
      começa com `eyJ`) também funciona, mas o Supabase a descontinua até o fim de 2026.
   4. **Vercel:** *Add New → Project*, importar este repositório; **Root Directory:
      `pesquisa`**; *Framework Preset*: **Other**, sem comando de build. Em *Environment
      Variables*, criar `SUPABASE_URL` (a Project URL) e `SUPABASE_ANON_KEY` (a Publishable
      key), coladas direto no painel da Vercel. *Deploy*. **Não ligar** Web Analytics nem
      Speed Insights: eles vêm desligados, e o contrato os quer desligados.
   5. **Conferir no ar**, na URL de produção:
      - `<url>/README.md` e `<url>/supabase/esquema.sql` dão **404**. O `.vercelignore` os
        tira do ar; a documentação da Vercel não diz com todas as letras que isso vale para
        deploy pelo Git, então a prova é este passo;
      - **responder a pesquisa uma vez, até o fim**;
      - no Supabase, *Table Editor*: `aberturas` tem 1 linha e `respostas` tem 1 linha, e o
        `questionario_sha256` dela é o do pré-registro (`73936c74…`).
   6. ⚙ **No desktop:** rodar `pesquisa/supabase/exportar.sql` no SQL Editor, baixar o
      resultado em CSV como `data/teste-marca/respostas.csv` e rodar
      `py -3.11 tools/analise_teste_marca.py --conferir-cabecalho`. Tem de dar `ok`. Se não
      der, **parar**: o cabeçalho da exportação real é o último ponto que nenhum teste viu.
   7. **Apagar a resposta de teste** (SQL Editor). É o mesmo comando para o teste do passo 5 e
      para qualquer outro antes do convite:
      `delete from public.respostas; delete from public.aberturas;
      update public.contador_de_aberturas set aberturas = 0;`
      E apagar o `data/teste-marca/respostas.csv` do teste. O contador volta a 0 porque as
      aberturas de teste não são da janela (ab-a).
   8. Daí em diante, a ordem é a do pré-registro (§12): **o commit das datas da janela,
      empurrado, e só então o primeiro convite.** Depois do primeiro convite, nada se apaga.

