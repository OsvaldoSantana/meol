---
name: bastter-contorno
description: A escada de contorno do projeto Bastter — o que tentar antes de escrever "bloqueado", "403" ou "não confirmado por falta de acesso", e como transcrever cada degrau. Use quando uma página, API, arquivo ou pacote recusar a sua ferramenta.
---

# Subir a escada antes de escrever "não dá" — projeto Bastter

Esta skill existe porque "tentei, deu 403, parei" cumpria a letra das regras 13 e 17 do
`CLAUDE.md` §5-B e deixava o dado de fora. Em 27/09/2026, três `NAO_CONFIRMADO` do
repositório caíram no **primeiro degrau**, com um comando de terminal cada. A regra é a 18
da §5-B; a guarda é `auditoria/test_escada_contorno.py`.

## A pergunta antes de tudo

> **O limite é da minha ferramenta ou do mundo?**

- **Da ferramenta:** a ferramenta web de quem responde recusa por política (`ROBOTS_DISALLOWED`,
  `PERMISSIONS_ERROR`, `EGRESS_BLOCKED`); o site bloqueia IP de datacenter (403 do Akamai); o
  túnel do proxy da sessão cai. **Outro caminho existe.** Suba a escada.
- **Do mundo:** a fonte não publica o dado; o arquivo não existe; o campo não está no leiaute.
  Isso é `FISICA` (§5-B.16), e só se afirma **depois** de ler a fonte pelo caminho que
  funciona.

Um erro de ferramenta escrito como fato do mundo encerra a investigação, e é por isso que ele
custa mais que o erro em si.

## A escada

| degrau | o que tentar | exemplos |
|---|---|---|
| **1 · outra ferramenta** | a mesma fonte por outro cliente ou outro formato | `curl` no terminal no lugar da busca web; `git clone` no lugar da página do GitHub; a **API** no lugar da página (OData, JSON do PyPI); `curl -r 0-4095` para ler só o cabeçalho de um CSV grande; o CSV no lugar do painel |
| **2 · outra cópia** | o mesmo documento guardado em outro lugar | Wayback Machine (`archive.org/wayback/available?url=`); espelho oficial; portal de dados abertos que republica o arquivo |
| **3 · outra fonte primária** | o mesmo **dado** publicado por outro dono | CVM no lugar do site do gestor; o regulamento no lugar da lâmina; o Banco Central no lugar do agregador |
| **4 · outro executor** | alguém que alcança o que esta sessão não alcança | sessão local na máquina dele (IP residencial, disco); workflow `medir/` (§5-A.11, só para medir); script que ele roda com um comando |
| **5 · `NAO_CONFIRMADO`** | só agora, e com a escada na linha | `escada: 1 curl → 403 (Akamai); 2 Wayback → túnel caiu; 3 CVM → sem campo; 4 → P-05` |

**Transcreva cada degrau com o erro exato** (código HTTP, servidor, mensagem), a data e o
comando. "Bloqueado" sem o erro não é medição (§5-B.13). O degrau 4 vira roteiro para quem o
executa, nunca "visita manual" (§5-B.17).

## Os casos que criaram a regra (medidos em 27/09/2026)

**1 · `olinda.bcb.gov.br` "bloqueado por robots.txt"** (`docs/fontes/pesquisa-bases-e-apis-2026-09.md`).
Degrau 1 resolveu: `curl` na API PTAX (`CotacaoDolarDia(dataCotacao=@dataCotacao)?@dataCotacao='09-25-2026'&$format=json`)
respondeu **HTTP 200** com `cotacaoCompra`, `cotacaoVenda`, `dataHoraCotacao`. O
`robots.txt` do olinda respondeu **HTTP 502** (página de erro, sem regra legível). O
`ROBOTS_DISALLOWED` era a política da ferramenta de busca, não uma recusa do servidor. De
brinde, a "sintaxe de parâmetro do OData, não verificada" ficou verificada pelo mesmo comando.

**2 · "se `cad_fi` da CVM tem campo de taxa (domínio bloqueado)"** (mesmo arquivo). Degrau 1
resolveu a pergunta: `curl -r 0-4095` no `cad_fi.csv` deu **HTTP 206** e o cabeçalho de 41
colunas, com `TAXA_PERFM` (22) e `TAXA_ADM` (24). **E a régua §5-B.1 pegou o passo seguinte:**
lido o arquivo inteiro, `TAXA_ADM` está preenchida em 15.117 de 46.806 linhas, e só **1**
delas está `EM FUNCIONAMENTO NORMAL`. Depois da RCVM 175 o `cad_fi` guarda taxa de fundo
antigo; "tem a coluna" não quer dizer "é fonte da taxa de hoje". Subir a escada não dispensa
ler a vizinhança.

**3 · `etf.BOVV11`, "site do gestor bloqueia robô; visita manual"** (`docs/fontes/MAPA-CONSTANTES.md`).
A escada inteira, e ela **não** resolveu da nuvem:
- degrau 1: `curl` em `itnow.com.br` → **403** do `AkamaiGHost` (a WAF do site, não o proxy);
- degrau 2: a Wayback tem a página (`20260513194558`, status 200 pela API), mas o
  `web.archive.org` fecha o túnel desta sessão (`ws_closed_mid_exchange`, 4 de 4 tentativas);
- degrau 3: CVM — o `registro_fundo_classe` acha o fundo (It Now Ibovespa, CNPJ
  21.407.758/0001-19, FIIM, em funcionamento) e **não tem campo de taxa**; o `extrato_fi`
  cobre só classes FIF (6.565 de 6.565); o `cad_fi` só o tem cancelado; o FundosNet devolve
  0 documentos para o CNPJ (controle com um FII: devolve);
- degrau 4: sessão local, com o roteiro na **P-05**. Continua `NAO_CONFIRMADO`, agora com a
  escada e a pendência na linha.

**4 · O `tabpfn` "recusado pelo PyPI por robots.txt"** (P-122, laudo do pré-registro ML).
Degrau 1: `curl https://pypi.org/pypi/tabpfn/json` → **HTTP 200**; a 9.0.0 exige
`torch>=2.5`. A pergunta "se o TabPFN trouxer torch" tinha resposta a um comando.

**5 · A rodada do claude.ai de 27/09.** A ferramenta web deu `PERMISSIONS_ERROR` no GitHub; o
`git clone` pelo terminal funcionou. Mesmo repositório, outra ferramenta.

## O que a escada não autoriza

- **Credencial, sessão logada ou navegador dele** (§5-A.7). Degrau 4 é pedir, não usar.
- **Contornar um termo de uso ou um CAPTCHA.** A escada troca de ferramenta, de cópia ou de
  fonte; não finge ser humano. Se a fonte proíbe (a B3, P-136), o limite é do mundo.
- **Inventar URL.** Endpoint só entra depois de achado (na página, no JS da própria página, na
  documentação); URL "provável" que dá 404 não é degrau.

## Onde escrever

| o quê | onde |
|---|---|
| a linha corrigida | no próprio arquivo, com o texto antigo riscado (§5-A.4), a medição nova, a data e o degrau |
| o `NAO_CONFIRMADO` que sobrou | com `escada:` e a `P-nnn` na mesma linha |
| a reincidência | `docs/metricas/eventos.csv`, código `5-B.17` |
