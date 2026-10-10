# R3: a tabela do veto (direcao x codigo dominante de cada categoria)

*GERADO por `python tools/r3_dominante.py` a partir de `classificacao.csv`; nao editar a mao. O codigo e fundo/matiz/familia do titulo/raio (as quatro centrais, aa-a). Categoria com menos de 5 marcas classificadas nao tem dominante e nao veta. "imita" = a direcao partilha os quatro valores centrais com um dominante (livro de codigos). A vencedora so sai depois da janela; o veto se le na linha dela.*

| categoria | n (so app) | codigo dominante | E | C | D | so app: E | C | D |
|---|---|---|---|---|---|---|---|---|
| banco_tradicional | 6 (5) | claro/celeste/sem_serifa/grande | - | - | - | - | - | - |
| banco_digital | 3 (2) | sem dominante | - | - | - | - | - | - |
| corretora | 2 (1) | sem dominante | - | - | - | - | - | - |
| gestora_e_private | 12 (1) | sem dominante | - | - | - | - | - | - |
| pagamentos | 1 (1) | sem dominante | - | - | - | - | - | - |
| consolidador | 0 (0) | sem dominante | - | - | - | - | - | - |
| casa_de_analise_e_educacao | 0 (0) | sem dominante | - | - | - | - | - | - |
| consultoria_cvm | 10 (0) | sem dominante | - | - | - | - | - | - |
| assessor | 10 (0) | sem dominante | - | - | - | - | - | - |
| robo | 0 (0) | sem dominante | - | - | - | - | - | - |
| planejador | 0 (0) | sem dominante | - | - | - | - | - | - |

**Arquivamento:** 44 linha(s) classificada(s) com `PENDENTE_LOCAL`. A R3 so fecha com zero (tools/r3_arquivar.py, na maquina dele).
