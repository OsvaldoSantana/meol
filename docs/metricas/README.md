# Métricas — o que é medido, onde, quando, e o que não é

*Criado em 25/09/2026. Os números moram nos arquivos desta pasta e nas saídas dos comandos
abaixo. Nenhum deles é copiado para o `CLAUDE.md` (§8: número que envelhece se lê da fonte).*

## O que é medido

| medida | onde | quando | quem roda |
|---|---|---|---|
| três suítes **sem** `slow`, ruff, mypy | `.github/workflows/testes.yml`, job `rapido` | a cada push em `main` | GitHub, sozinho |
| suíte **completa**, com `slow`, lendo o acervo do armazém | `testes.yml`, job `completo` | segunda 08:00 (Brasília) e manual | GitHub, sozinho |
| cobertura de linhas por módulo | `docs/metricas/cobertura.csv` (commit do bot só se mudar) | semanal | GitHub, sozinho |
| constante com `expira` em até 7 dias | uma issue "Constantes vencendo" (a aberta é atualizada) | semanal | GitHub, sozinho |
| o que o registro diz existir e o armazém não entrega | lista de faltas no log do job; job vermelho | semanal | GitHub, sozinho |
| mutação (mutmut) em `ajustar.py`, `estado_io.py`, `alocacao.py`, `insumo_ml.py` | `.github/workflows/mutacao.yml`, artefato `mutmut-resultados` | **manual, uma vez** | ele dispara |
| erros do processo: achado, retratação, reincidência | `docs/metricas/eventos.csv` | a cada achado, no mesmo commit | quem registra |
| resumo semanal do processo | `python auditoria/metricas_processo.py` | quando se quer ler | à mão |
| regra de volta dos modelos: eventos por PR mergeado, por classe, contra a referência de 25/09 a 02/10 | `metricas_processo.py --prs`, no resumo do job `completo`; classe que volta abre UMA issue | semanal | GitHub, sozinho |
| o que toda sessão lê, antes e depois de cada corte | `docs/metricas/contexto-de-sessao.md`, por `auditoria/tamanho_do_contexto.py` | a cada corte | quem corta |
| tempo e tokens por pedido das sessões | `py -3.11 tools/analisar_sessoes.py` → `data/analise-sessoes/` | quando se quer ler | à mão, na máquina dele |

**Job vermelho vira e-mail** pela notificação padrão do GitHub: falha de workflow avisa quem
disparou (push) e o dono do repositório (agendado).

## Como se lê

- **Cobertura é medida, não meta.** Não há piso. Ela conta linha **executada**, não linha
  **verificada**: um teste que roda o código sem afirmar nada sobe o número. Quem mede a
  verificação é a mutação. `auditoria/cobertura_csv.py` lista os módulos de produção abaixo de
  50% só para serem lidos.
- **Subprocesso conta.** `[tool.coverage.run] patch = ["subprocess"]` no `pyproject.toml`. Sem
  isso, `auditoria/chaves_orfas.py` media 0% e mede 96%, porque as guardas dele rodam em
  subprocesso.
- **Mutante sobrevivente é achado candidato.** Um mutante equivalente, que não muda o
  comportamento, também sobrevive. Quem o promove a achado é a leitura (régua §5-B, pergunta 3).
- **`eventos.csv`:** `desconhecido` quer dizer "o registro não diz", e nunca é vazio.
  `mesmo-commit` em `commit_corrigiu` é o commit que acrescentou a linha: um commit não sabe o
  próprio hash, e `git log -S "<codigo>" -- docs/metricas/eventos.csv` o encontra. `aberto` =
  ainda não corrigido. O resumo
  semanal mostra quantos `quem_achou` são `desconhecido` ao lado da fração do Osvaldo, porque
  "0% de 26" com 11 desconhecidos não é "0%".

## O que NÃO é medido

- **Os testes do silver no job semanal.** O silver (`data/silver/`) e os eventos da B3 não estão
  no armazém. No GitHub esses testes pulam, e o `-rs` do log diz quais. Eles só rodam na máquina
  dele, onde o silver existe.
- **Tempo e tokens das sessões no GitHub.** `tools/analisar_sessoes.py` lê `~/.claude/projects`,
  que só existe na máquina dele. No job essa seção não existe, e o resumo diz que não mediu.
- **O `eventos.csv` antes de 16/09.** O preenchimento para trás cobre o que estava datado nos
  três registros desde 16/09. Antes disso, nada foi preenchido.
- **Autor e descobridor de boa parte dos eventos.** Quando o texto não diz, fica `desconhecido`.
  Os campos não foram inferidos.
- **Qualidade de uma retratação.** A contagem diz quantas houve, não se a causa raiz foi a certa.
- **A mutação ainda não rodou.** O workflow existe; o primeiro disparo é dele (o `gh` não está
  instalado nesta máquina, e a §5-A manda pedir). A configuração `[tool.mutmut]` é
  `NAO_CONFIRMADO` até essa execução.
