# R3: a tabela do veto (direcao x codigo dominante de cada categoria)

*GERADO por `python tools/r3_dominante.py` a partir de `classificacao.csv`; nao editar a mao. O codigo e fundo/matiz/familia do titulo/raio (as quatro centrais, aa-a). Categoria com menos de 5 marcas classificadas nao tem dominante e nao veta. "imita" = a direcao partilha os quatro valores centrais com um dominante (livro de codigos). A vencedora so sai depois da janela; o veto se le na linha dela.*

| categoria | n (so app) | codigo dominante | E | C | D | so app: E | C | D |
|---|---|---|---|---|---|---|---|---|
| banco_tradicional | 10 (9) | sem dominante | - | - | - | - | - | - |
| banco_digital | 10 (8) | sem dominante | - | - | - | - | - | - |
| corretora | 10 (4) | sem dominante | - | - | - | - | - | - |
| gestora_e_private | 10 (1) | sem dominante | - | - | - | - | - | - |
| pagamentos | 10 (9) | sem dominante | - | - | - | - | - | - |
| consolidador | 5 (5) | sem dominante | - | - | - | - | - | - |
| casa_de_analise_e_educacao | 10 (3) | sem dominante | - | - | - | - | - | - |
| consultoria_cvm | 10 (0) | sem dominante | - | - | - | - | - | - |
| assessor | 10 (0) | sem dominante | - | - | - | - | - | - |
| robo | 1 (1) | sem dominante | - | - | - | - | - | - |
| planejador | 0 (0) | sem dominante | - | - | - | - | - | - |

**Arquivamento:** 6 linha(s) classificada(s) com `PENDENTE_LOCAL`. A R3 so fecha com zero, ou com cada uma levando a escada e o proximo executor (tools/r3_arquivar.py pelo degrau 4 em ordem, 4a o workflow arquivar_r3.yml no servidor do GitHub; CLAUDE.md 5-B.18).
