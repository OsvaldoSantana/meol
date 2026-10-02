# Tipografia dos estímulos do teste de marca — fontes livres embutidas

*27/09/2026, S4. Resposta i-A dele: o estímulo é imagem fixa, gerada com fontes livres
(OFL) embutidas. Assim todo participante vê a mesma tipografia, qualquer que seja o aparelho
(P-163).*

**Todas as famílias abaixo são SIL Open Font License 1.1.** A licença de cada uma está no
`OFL.txt` da pasta dela, copiado sem edição do `LICENSE` do pacote de origem. Duas notas:
- o `LICENSE` do Source Sans 3 e do Source Serif 4 abre com "Google Inc.": é o cabeçalho
  do Fontsource, e o texto que segue é a OFL 1.1;
- a Playfair Display declara nome de fonte reservado. Os arquivos aqui não foram
  modificados; renomear ou alterar exigiria ler a cláusula antes.

**De onde vieram.** Dos pacotes `@fontsource/<família>` 5.3.0 do registro do npm,
baixados em 27/09/2026 às 11:5x UTC. O sha512 de cada pacote bateu com o `integrity` que o
registro declara. Só o subconjunto `latin` (que cobre os acentos do português) e só os pesos
usados foram copiados. A rede da nuvem não alcançou o repositório do Google Fonts no
GitHub (acesso negado à API para repositórios fora da sessão); o npm alcançou.

| família | direção | uso | arquivo | sha256 |
|---|---|---|---|---|
| Source Sans 3 | E | títulos, rótulos e navegação | `source-sans-3/source-sans-3-latin-400-normal.woff2` | `0f73f35e08cde0a2f10c109c6e01d71459d97e4099ecd9a50f1b6c0209e4de2b` |
| Source Sans 3 | E | títulos em negrito | `source-sans-3/source-sans-3-latin-600-normal.woff2` | `14527d193b0e30bc32ef931549a246cdfd286573bb12869b7e052b8101a39d38` |
| Source Serif 4 | E | texto corrido e números | `source-serif-4/source-serif-4-latin-400-normal.woff2` | `02194deb92d3975dd30e11a3824a1f1db32b48c93654e60560cb81ce8e7b5f95` |
| Nunito | C | tudo | `nunito/nunito-latin-500-normal.woff2` | `23ae3083dbdaeabf3b9969a3947ddf5d5614683516e28ffa110ca4eb6192a9ff` |
| Nunito | C | tudo | `nunito/nunito-latin-600-normal.woff2` | `45f437de32ff5973eb5616b43c1308bf9fe897442f3d78a603c4cd0a06d66573` |
| Nunito | C | tudo | `nunito/nunito-latin-700-normal.woff2` | `fa89300b9bbb3bd0f60d6991aa055965d98e2ccca27bf8688fe0c39cdc796846` |
| Nunito | C | tudo | `nunito/nunito-latin-800-normal.woff2` | `2363d3ed037283ebb961e8c4b4917e40a8bc8853cf9965cf1ea7b4daa1df630a` |
| Playfair Display | D | títulos, nome e números | `playfair-display/playfair-display-latin-400-normal.woff2` | `1fe9ad5d8b2ebd8ecb8fbd05bed1e3fdfa52dae3f1a04e1c219918442fe9394d` |
| Montserrat | D | texto corrido e caixa alta | `montserrat/montserrat-latin-400-normal.woff2` | `e66bcd2761ab6924b25ce70dafe10e57a39193c4fea1516730bd9cb5240af6c8` |
| Montserrat | D | botão principal | `montserrat/montserrat-latin-700-normal.woff2` | `f9d9e65b15372cebcafc3acd1e664a564c5c4b23278de4d5760de9a13c530371` |

**Por que estas.** A E pede serifa no texto corrido com algarismos alinhados e títulos
sem serifa em caixa alta: Source Serif 4 e Source Sans 3, que foram desenhadas como par.
A IBM Plex ficou de fora de propósito: é a tipografia do Quanto-e-Onde, que ele não
aproveitou (resposta d, `docs/decisoes/rosto-v1.md`). A C pede cantos arredondados, e a
Nunito tem terminais arredondados. A D pede serifa de alto contraste, e a Playfair Display é
didone.

**Guarda:** `auditoria/test_direcoes_marca.py` reprova `url()` que não aponte para um
arquivo desta pasta, e reprova família em `@font-face` sem o `OFL.txt` ao lado.
