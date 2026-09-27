# Estímulos do teste de marca — direções E, C e D (P-163)

*S3 (27/09/2026) fez a primeira versão; a S4 (27/09/2026) a refez com as respostas de 27/09
dele (g-B a p-A, em `docs/decisoes/fila-do-osvaldo.md`). **Nada daqui foi mostrado a
ninguém.** Os PNG são candidatos a imagem final: o sha256 deles só entra no pré-registro
(P-162, S5) se ele os aprovar.*

| arquivo | o que é |
|---|---|
| `cenario.yaml` | o cenário sintético (quem já aporta), os rótulos genéricos por rota (l-B) e o motivo em linguagem comum da rota bloqueada (j-A). Dado, em ASCII |
| `conteudo.yaml` | **gerado** por `python tools/conteudo_estimulo.py` a partir do motor; `--conferir` reprova se alguém o editar à mão |
| `E.html`, `C.html`, `D.html` | a T1 em cada direção, com as versões **base** e **com rota bloqueada**, que diferem só no elemento `data-diferenca` |
| `png/<direção>-base.png`, `png/<direção>-rota-bloqueada.png` | as seis imagens fixas (i-A), 390 × 844 |

Os tokens (cores, fontes, pares de contraste) estão em `../tokens/direcoes.yaml`, e as
fontes OFL embutidas em `../tipografia/`.

## Como os PNG foram gerados, e como reproduzir o sha256

Com o Chromium sem interface **141.0.7390.37** (`headless_shell` do Playwright, na nuvem), a
partir desta pasta:

```bash
CH=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell
for d in E C D; do for v in base rota-bloqueada; do
  frag=""; [ $v = rota-bloqueada ] && frag="#tela-rota"
  $CH --no-sandbox --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
      --virtual-time-budget=5000 --window-size=390,844 \
      --screenshot=png/${d}-${v}.png "file://$PWD/$d.html$frag"
done; done
```

Duas rodadas seguidas deram os mesmos seis sha256 (n=6), medido em 27/09/2026. Outro
Chromium ou outra máquina podem dar outro byte com a mesma aparência: o que o pré-registro
congela é **o arquivo**, não o comando.

| PNG | sha256 |
|---|---|
| `png/E-base.png` | `302a50ab35a31e24166874f14dfebc4055bc794524c90a73a6894a7311be3665` |
| `png/E-rota-bloqueada.png` | `04fe0520a5c4e0e022927ec37cca779fc88c169844b8d0185ff9bcca6e678962` |
| `png/C-base.png` | `91b3f24e0eebd467306917b1c24df86ed6fdde4fe25ca9ac211abe4c76acd5b9` |
| `png/C-rota-bloqueada.png` | `da85f3eb295e16d43872f5521ec18a13682888291d7ab4aa4c2912389c908174` |
| `png/D-base.png` | `36a7c019c0410b1567e5dc17177473895deb5d90a175e630f58eace063115a83` |
| `png/D-rota-bloqueada.png` | `f0ad96161c829d4536cd083f08d99581fc54deaa7f32f904c264702bb9b64b73` |

## O que mudou da S3 para a S4, e por quê

| mudança | por quê |
|---|---|
| "PIBB11" virou "fundo de índice de ações brasileiras" | l-B: rótulo genérico; o ticker real não aparece (guarda: nenhum ticker do catálogo no texto) |
| "peso-alvo" virou "meta" | pedido do prompt da S4, no mesmo item do rótulo genérico |
| o estado "Completo" contrafactual saiu; o selo é "Parcial" nas duas versões, com a faixa do custo | a tarifa da B3 é `PARCIAL` no `custos.yaml`: nenhuma tela mostra estado que o motor não emite |
| a versão PARCIAL virou a versão **com rota bloqueada** | j-A: a H3 por rota bloqueada real. A rota é a primeira que o motor elimina, na ordem dos portões de universo (G5, o cofrinho de banco digital) |
| a linha "Destino" saiu do quadro | ela repetia a frase da decisão, e com o rótulo longo a versão com rota bloqueada não cabia em 844 px. O destino continua na frase |
| a C trocou o roxo por magenta (318°) | m-B: o roxo era o matiz do Nubank; lista conferida no YAML |
| a D ganhou um cartão metálico desenhado em SVG | k-A: ilustração provisória (P-168), sem marca, sem texto, sem gradiente |
| fontes do sistema viraram fontes OFL embutidas | i-A: a mesma tipografia para todos |
