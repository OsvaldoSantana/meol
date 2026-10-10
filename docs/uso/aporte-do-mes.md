# O aporte do mês, do começo ao fim

*Roteiro do primeiro uso real do M1 (P-181, [`PLANO.md`](../../PLANO.md) §4). Escrito em
10/10/2026. Você roda sozinho, no seu computador, sem nenhuma sessão do Claude no meio. **Cada
passo em que você travar é defeito do sistema, não seu**: anote o número do passo e o que
apareceu na tela (último bloco deste arquivo), e isso vira pendência com o nome do passo.*

O comando lê o seu `alocacao/estado.yaml`, que é privado e fica só no seu computador (P-67). Nada
do que ele mostra vai para o repositório.

---

## Antes de começar (uma vez)

**1. Abra o PowerShell na pasta do projeto.**
No Explorador de Arquivos, abra `Desktop\Bastter`. Clique na barra de endereço, apague o que
estiver lá, digite `powershell` e aperte Enter. Deve abrir uma janela azul ou preta terminando em:

```
PS C:\Users\osvaldo.junior\Desktop\Bastter>
```

**2. Traga a versão nova do projeto.**

```powershell
git switch main
git pull
```

Deve aparecer `Already on 'main'` (ou `Switched to branch 'main'`) e, no fim do `pull`, a lista de
arquivos que mudaram, entre eles `alocacao/aporte_do_mes.py`. Se aparecer `error: Your local
changes ... would be overwritten`, pare e anote o passo 2.

**3. Confira o Python.**

```powershell
py -3.11 --version
```

Deve aparecer `Python 3.11.` seguido de um número. Qualquer outra versão: anote o passo 3.

**4. Confira as dependências.**

```powershell
py -3.11 alocacao/ambiente.py --instalar
```

Ele imprime uma linha que começa com `python -m pip install` e lista quatro pacotes com a versão
(`PyYAML==...`, `numpy==...`, `pandas==...`, `pytest==...`). Copie essa linha, cole no PowerShell,
**troque o `python` do começo por `py -3.11`** (para instalar no Python certo) e aperte Enter. Deve
terminar em `Successfully installed` ou em `Requirement already satisfied`.

---

## Todo mês

**5. Atualize o seu `estado.yaml`.**

```powershell
notepad alocacao\estado.yaml
```

Confira, com os números de hoje:

| campo | o que é |
|---|---|
| `aporte_mensal` | quanto você guarda num mês sem bônus |
| `despesa_mensal` | quanto você gasta por mês |
| `reserva_atual` e `reserva_por_rota` | a reserva de emergência, e onde ela está |
| `posicoes` | quanto você já tem em cada investimento (rota → valor em reais) |
| `caixa` | dinheiro parado, sem destino |
| `meta.status` | tem de ser `REAL` |
| `meta.preenchido_em` | a data de hoje, no formato `2026-10-10`, sem aspas |

Número com **ponto** decimal (`1500.50`), nunca vírgula. Não escreva `yes`, `no`, `sim` ou `não`
num campo de número: o sistema recusa (CX-04). Salve e feche o Bloco de Notas.

**6. Peça a resposta do mês.**

```powershell
py -3.11 alocacao/aporte_do_mes.py
```

Ele demora alguns segundos, porque baixa o preço do Tesouro Selic do site do Tesouro. Uma de três
coisas aparece:

- **`APORTE DE ... -- R$ ...`** seguido de `O QUE FAZER`: é a resposta. Vá para o passo 8.
- **`Antes de responder, o seu estado.yaml precisa de ajuste:`** seguido de uma lista: cada linha
  diz o campo e o problema. Corrija no passo 5 e rode de novo. Se uma linha não fizer sentido,
  anote o passo 6 e copie a linha.
- **`Para dizer quanto comprar, falta o preco de hoje de: ...`**: vá para o passo 7.

**7. Informe o preço que ele pediu (se pediu).**
Abra a sua corretora, procure cada ativo que a mensagem nomeou (o código entre parênteses, como
`pibb11`) e anote o preço de agora. Rode de novo com um `--preco` para cada um, com vírgula:

```powershell
py -3.11 alocacao/aporte_do_mes.py --preco pibb11=30,12
```

No Tesouro, informe o preço de **1 título** (o PU), não o do mínimo. Num mês com bônus, acrescente
o valor deste mês: `--aporte 1.500`. A carteira-alvo continua calculada sobre o aporte normal.

**8. Leia a resposta, de cima para baixo.**

| bloco | o que diz |
|---|---|
| `O QUE FAZER` | quanto, em quê, e quanto fica no caixa |
| `POR QUE` | a regra que levou a isso, em uma ou duas frases |
| `QUEM FICOU DE FORA, E POR QUE` | cada investimento que não entrou, com o portão que o tirou |
| `O QUE O SISTEMA PEDE DE VOCE` | decisões suas que estão pendentes |
| `DE ONDE VEIO CADA NUMERO` | a origem de cada número: o seu arquivo, o preço com data, a versão das regras |

O texto sai sem acento, de propósito por enquanto: os arquivos de regra do projeto são ASCII.

**9. Execute na corretora, se concordar.** A ordem é sua: o sistema não compra nem vende nada, e
isto não é recomendação de investimento. Se a corretora recusar a ordem (valor mínimo, quantidade,
horário), **não force**: anote o passo 9 e a mensagem da corretora.

**10. Depois de comprar, volte ao passo 5** e atualize `posicoes` e `caixa` com o que de fato
aconteceu. É isso que faz a resposta do mês seguinte partir do lugar certo.

---

## Onde travei

Copie este bloco, preencha e mande para o Claude no Projeto. Cada linha vira uma pendência com o
nome do passo.

```
Passo:          (o número)
O que eu fiz:   (o comando ou o clique)
O que apareceu: (copie a mensagem inteira, ou descreva a tela)
O que eu esperava:
```

Não cole números do seu `estado.yaml` aqui se não quiser: o nome do campo basta.
