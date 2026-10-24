# P-18: o `SETOR_ATIV` do cadastro da CVM, contado no dado real

**Data:** 24/10/2026. **Régua:** 5-B.18 (a escada), 5-B.14 (todo número com o seu n).

## A escada, degrau a degrau

| degrau | o que se tentou | resultado |
|---|---|---|
| 1 · outra ferramenta | `curl -sS -m 90 -o cad.csv -w "http=%{http_code} bytes=%{size_download}\n" https://dados.cvm.gov.br/dados/CIA_ABERTA/CAD/DADOS/cad_cia_aberta.csv` | **`http=200 bytes=1494003`**, `sha256 39ac70276c513b835eb3d470e6e1f623e217e4220e9608592eaf601948556873` |
| 4a · workflow `medir/` | não foi preciso | o degrau 1 respondeu |

O sha256 é o do registro do acervo: `docs/acervo/cvm/capturas.csv` tem a captura de
`2026-10-24T13:20:32Z` do recurso `cad` com o mesmo prefixo. Nenhuma credencial foi usada.

## O que se mediu, em uma frase

Quantos valores distintos tem a coluna `SETOR_ATIV` no cadastro de companhias abertas da CVM da
data, em todas as linhas do arquivo (ativas, canceladas e suspensas).

**Resultado:** 2.678 linhas, **71 valores distintos** (um deles é o vazio, em 6 linhas), 2.567
`CD_CVM`; 107 `CD_CVM` aparecem em mais de uma linha e **nenhum** com setores diferentes. A lista
inteira, com a contagem de cada valor, está em `politica.yaml → bloco_C_solvencia.setor_ativ`
(`OBSERVADO`). Antes: "só dois exemplos foram vistos".

## O que a contagem NÃO decide (P5)

1. **Quais valores são instituição financeira ou seguradora.** A regra do YAML diz "instituição
   financeira ou seguradora", e a lista de 71 valores tem 2 que dizem banco ou seguradora
   (`Bancos`, `Seguradoras e Corretoras`: 139 linhas) e 14 financeiro-adjacentes ou vazios
   (securitização, factoring, crédito imobiliário, arrendamento mercantil, intermediação
   financeira, bolsa, a holding que o nome liga a eles, e o vazio: 276 linhas). Essa leitura é
   de Claude, de 24/10/2026, não dele. As duas vão para `RECUSA_REGIME` e `EXIGE_DOSSIE`; o
   regime delas é a P-31.
2. **A holding genérica.** "Emp. Adm. Participações" (156) e "Emp. Adm. Part. - Sem Setor
   Principal" (109) ficam em `GERAL` por não nomearem setor: o bloco aplicaria EBIT / despesa
   financeira a uma holding cujo demonstrativo pode ser dominado por equivalência patrimonial. É a
   escolha em aberto mais cara da lista.
3. **O tempo.** É o cadastro de HOJE, não *as-of*: empresa que mudou de setor entra no regime de
   hoje no passado. O registro diário do `cad` permite reconstruir a partir de 24/09/2026.
4. **Uma data só (n = 1 arquivo).** Valor novo no cadastro de amanhã derruba o leitor, de
   propósito (P1): `SetorForaDaEnumeracao` nomeia o valor e pede para contá-lo e declará-lo.
