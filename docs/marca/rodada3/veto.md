# R3: a tabela do veto (direcao x codigo dominante de cada categoria)

*GERADO por `python tools/r3_dominante.py` a partir de `classificacao.csv`; nao editar a mao. O codigo e fundo/matiz/familia do titulo/raio (as quatro centrais, aa-a). Categoria com menos de 5 marcas classificadas nao tem dominante e nao veta. "imita" = a direcao partilha os quatro valores centrais com um dominante (livro de codigos). A vencedora so sai depois da janela; o veto se le na linha dela.*

| categoria | n (so app) | codigo dominante | E | C | D | so app: E | C | D |
|---|---|---|---|---|---|---|---|---|
| banco_tradicional | 10 (8) | sem dominante | - | - | - | - | - | - |
| banco_digital | 10 (7) | sem dominante | - | - | - | - | - | - |
| corretora | 10 (1) | sem dominante | - | - | - | - | - | - |
| gestora_e_private | 14 (1) | sem dominante | - | - | - | - | - | - |
| pagamentos | 11 (9) | sem dominante | - | - | - | - | - | - |
| consolidador | 0 (0) | sem dominante | - | - | - | - | - | - |
| casa_de_analise_e_educacao | 10 (3) | sem dominante | - | - | - | - | - | - |
| consultoria_cvm | 10 (0) | sem dominante | - | - | - | - | - | - |
| assessor | 10 (0) | sem dominante | - | - | - | - | - | - |
| robo | 0 (0) | sem dominante | - | - | - | - | - | - |
| planejador | 0 (0) | sem dominante | - | - | - | - | - | - |

**Arquivamento:** 85 linha(s) classificada(s) com `PENDENTE_LOCAL`. A R3 so fecha com zero (tools/r3_arquivar.py, na maquina dele).
