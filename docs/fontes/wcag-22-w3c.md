# WCAG 2.2 — os critérios que viram requisito de interface do MEOL

**Fonte primária, lida no site do W3C. Acesso: 27/09/2026, 04:54 UTC.**
**Status: `PARCIAL`**: foram transcritos os 13 critérios de sucesso candidatos da P-155 (mais o
2.5.5, citado como alternativa não adotada) e as definições que eles usam. Os outros critérios
da WCAG 2.2 não foram transcritos; os que ficaram de fora e parecem tocar o MEOL estão listados
no fim, sem leitura.

> **Isto não é auditoria de acessibilidade nem parecer.** É a transcrição do texto normativo,
> para que cada limiar do `docs/marca/requisitos-interface-v1.md` aponte para o critério que o
> define. A lei brasileira de acessibilidade não foi lida aqui.

## De onde veio

| documento | URL | Last-Modified | sha256 do HTML baixado |
|---|---|---|---|
| WCAG 2.2, W3C Recommendation de 12/12/2024 (no cabeçalho dela, "This version: https://www.w3.org/TR/2024/REC-WCAG22-20241212/" e "Latest published version: https://www.w3.org/TR/WCAG22/") | https://www.w3.org/TR/WCAG22/ | 12/12/2024 10:36:22 GMT | `6e3c5fe397257cae509a2fb4752b73062cf8cbeb92c2cec618989b17e4cf7057` |
| Understanding 1.4.3 | https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html | 03/09/2026 15:17:59 GMT | `3352aaf477e9739155628467c4b62997e18ea4cab917c0eb4fc4fb39c5238a2e` |
| Understanding 1.4.11 | https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html | idem | `237cd64c8439ddbca50694708b5d24718a5b2ed74bb4eee90d02cf7707fd0674` |
| Understanding 1.4.1 | https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html | idem | `a9bab2b8f419ee379b1ab37985d70b03bd6568952251d2f8a55036198990c9e8` |
| Understanding 1.4.4 | https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html | idem | `38c890a4e70ec24fee98480e08218503bc458e41f38d3ce85f20e86d984e6c0c` |
| Understanding 1.4.10 | https://www.w3.org/WAI/WCAG22/Understanding/reflow.html | idem | `d322027ca3f1f43f516687120442c60f02ee3f82b09cb26933c9ee7abfeabb33` |
| Understanding 1.4.12 | https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html | idem | `48d38892c50739b98b6d7c4d54b83d15152e9c9dbba2a550bc5dec5bead38df2` |
| Understanding 1.3.4 | https://www.w3.org/WAI/WCAG22/Understanding/orientation.html | idem | `93e67978e3b5c7c7a3e289ae539553e8fe5e35a5c4eba4c2abc5e370e6b10755` |
| Understanding 2.4.7 | https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html | idem | `80ec2e7fc5cd2aaa3ab9379dbceab3192b7873434ca03c2a66a7da4eeed18c3a` |
| Understanding 2.4.11 | https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html | idem | `9515bdd0faab14d62528c5b1af1ea03383409c651b551c4e9b708c6f5bc8b607` |
| Understanding 2.5.8 | https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html | idem | `361694575d2a4ca5834de57dbc44b24c27ecc67956625703a140b9f1d79c62d4` |
| Understanding 3.2.6 | https://www.w3.org/WAI/WCAG22/Understanding/consistent-help.html | idem | `446fbc385d6c6494368d0389318db29f1f25f54603e69665ad9d9db151ab0238` |
| Understanding 3.3.7 | https://www.w3.org/WAI/WCAG22/Understanding/redundant-entry.html | idem | `d945ac6dea17b9b57ce2d530a1381e935fa231059b10c2edf9219c4dd3cd6706` |
| Understanding 3.3.8 | https://www.w3.org/WAI/WCAG22/Understanding/accessible-authentication-minimum.html | idem | `3c6496948b93fda1f7e45b0094853bf39141c01f615c340367dda5cee6871629` |
| licença de documentos do W3C (a URL da recomendação redireciona, 301, para a versão de 2023) | https://www.w3.org/copyright/document-license-2023/ | — | `4bc849ad8fc856e93478400332f409d209bdb7ab3ec0f346e88e9c23b6d2b9ae` |

- **Os endereços não foram montados:** os 13 links "Understanding" e o da licença foram tirados
  do próprio HTML da recomendação, que liga cada critério à sua página.
- **Número e nível** de cada critério foram lidos no HTML da recomendação (`<h4>` e
  `conformance-level` da seção de cada um), não nas páginas Understanding.
- **robots.txt** (`https://www.w3.org/robots.txt`, sha256
  `f3947d244239d90298c7c3323a6d83042bb4f38c821f1bdefa449e7dfd9e2976`): bloqueia `/TR/?` e
  `/WAI/search/?` (consultas), não `/TR/WCAG22/` nem `/WAI/WCAG22/Understanding/`.
- **As páginas Understanding são material de apoio, não norma.** O que é exigido está na
  recomendação; o que vem das Understanding é marcado como tal.

## A licença, e por que o que está aqui é trecho

A licença de documentos do W3C (em vigor desde 01/01/2023) permite copiar e distribuir o
documento "or portions thereof" desde que cada cópia traga três coisas: o link para o documento
original, a nota de copyright original e o status do documento. E veda publicar obra derivada
"for use as a technical specification". Por isso esta página transcreve **só** o texto dos
critérios usados, com as três coisas abaixo, e os requisitos do MEOL citam o critério em vez de
reescrevê-lo.

- **Documento original:** Web Content Accessibility Guidelines (WCAG) 2.2,
  https://www.w3.org/TR/WCAG22/
- **Nota de copyright do original:** "Copyright © 2020-2024 World Wide Web Consortium. W3C®
  liability, trademark and document use rules apply."
- **Status:** W3C Recommendation, 12 December 2024 ("This document was published by the
  Accessibility Guidelines Working Group as a Recommendation using the Recommendation track").

## Os critérios, literais

Texto normativo copiado do HTML da recomendação. Os títulos das exceções estão em negrito como
na fonte.

### 1.4.3 Contrast (Minimum) · nível AA

> The visual presentation of text and images of text has a contrast ratio of at least 4.5:1,
> except for the following:
> **Large Text** — Large-scale text and images of large-scale text have a contrast ratio of at
> least 3:1;
> **Incidental** — Text or images of text that are part of an inactive user interface
> component, that are pure decoration, that are not visible to anyone, or that are part of a
> picture that contains significant other visual content, have no contrast requirement.
> **Logotypes** — Text that is part of a logo or brand name has no contrast requirement.

### 1.4.11 Non-text Contrast · nível AA

> The visual presentation of the following have a contrast ratio of at least 3:1 against
> adjacent color(s):
> **User Interface Components** — Visual information required to identify user interface
> components and states, except for inactive components or where the appearance of the
> component is determined by the user agent and not modified by the author;
> **Graphical Objects** — Parts of graphics required to understand the content, except when a
> particular presentation of graphics is essential to the information being conveyed.

### 1.4.1 Use of Color · nível A

> Color is not used as the only visual means of conveying information, indicating an action,
> prompting a response, or distinguishing a visual element.

### 1.4.4 Resize Text · nível AA

> Except for captions and images of text, text can be resized without assistive technology up
> to 200 percent without loss of content or functionality.

### 1.4.10 Reflow · nível AA

> Content can be presented without loss of information or functionality, and without requiring
> scrolling in two dimensions for:
> - Vertical scrolling content at a width equivalent to 320 CSS pixels;
> - Horizontal scrolling content at a height equivalent to 256 CSS pixels.
>
> Except for parts of the content which require two-dimensional layout for usage or meaning.

Nota 2 do critério, que decide a tabela do funil da T3: "Examples of content which requires
two-dimensional layout are images required for understanding (such as maps and diagrams),
video, games, presentations, data tables (not individual cells), and interfaces where it is
necessary to keep toolbars in view while manipulating content."

### 1.4.12 Text Spacing · nível AA

> In content implemented using markup languages that support the following text style
> properties, no loss of content or functionality occurs by setting all of the following and by
> changing no other style property:
> - Line height (line spacing) to at least 1.5 times the font size;
> - Spacing following paragraphs to at least 2 times the font size;
> - Letter spacing (tracking) to at least 0.12 times the font size;
> - Word spacing to at least 0.16 times the font size.

Nota 1 do critério: "Content is not required to use these text spacing values. The requirement
is to ensure that when a user overrides the authored text spacing, content or functionality is
not lost."

### 1.3.4 Orientation · nível AA

> Content does not restrict its view and operation to a single display orientation, such as
> portrait or landscape, unless a specific display orientation is essential.

### 2.4.7 Focus Visible · nível AA

> Any keyboard operable user interface has a mode of operation where the keyboard focus
> indicator is visible.

### 2.4.11 Focus Not Obscured (Minimum) · nível AA · novo na 2.2

> When a user interface component receives keyboard focus, the component is not entirely hidden
> due to author-created content.

### 2.5.8 Target Size (Minimum) · nível AA · novo na 2.2

> The size of the target for pointer inputs is at least 24 by 24 CSS pixels, except when:
> **Spacing** — Undersized targets (those less than 24 by 24 CSS pixels) are positioned so that
> if a 24 CSS pixel diameter circle is centered on the bounding box of each, the circles do not
> intersect another target or the circle for another undersized target;
> **Equivalent** — The function can be achieved through a different control on the same page
> that meets this criterion;
> **Inline** — The target is in a sentence or its size is otherwise constrained by the
> line-height of non-target text;
> **User Agent Control** — The size of the target is determined by the user agent and is not
> modified by the author;
> **Essential** — A particular presentation of the target is essential or is legally required
> for the information being conveyed.

**Não adotado, citado para registrar a alternativa — 2.5.5 Target Size (Enhanced) · nível
AAA:** "The size of the target for pointer inputs is at least 44 by 44 CSS pixels except
when: [...]". A conformidade AA não o exige.

### 3.2.6 Consistent Help · nível A · novo na 2.2

> If a web page contains any of the following help mechanisms, and those mechanisms are
> repeated on multiple web pages within a set of web pages, they occur in the same order
> relative to other page content, unless a change is initiated by the user:
> - Human contact details;
> - Human contact mechanism;
> - Self-help option;
> - A fully automated contact mechanism.

### 3.3.7 Redundant Entry · nível A · novo na 2.2

> Information previously entered by or provided to the user that is required to be entered
> again in the same process is either:
> - auto-populated, or
> - available for the user to select.
>
> Except when:
> - re-entering the information is essential,
> - the information is required to ensure the security of the content, or
> - previously entered information is no longer valid.

### 3.3.8 Accessible Authentication (Minimum) · nível AA · novo na 2.2

> A cognitive function test (such as remembering a password or solving a puzzle) is not
> required for any step in an authentication process unless that step provides at least one of
> the following:
> **Alternative** — Another authentication method that does not rely on a cognitive function
> test.
> **Mechanism** — A mechanism is available to assist the user in completing the cognitive
> function test.
> **Object Recognition** — The cognitive function test is to recognize objects.
> **Personal Content** — The cognitive function test is to identify non-text content the user
> provided to the website.

Nota 2 do critério: "Examples of mechanisms that satisfy this criterion include: support for
password entry by password managers to reduce memory need, and copy and paste to reduce the
cognitive burden of re-typing."

## As definições que os critérios usam

- **contrast ratio:** "(L1 + 0.05) / (L2 + 0.05), where L1 is the relative luminance of the
  lighter of the colors, and L2 is the relative luminance of the darker of the colors." Nota 1:
  "Contrast ratios can range from 1 to 21 (commonly written 1:1 to 21:1)." Nota 4: "It is a
  failure if no background color is specified when the text color is specified [...]. For the
  same reason, it is a failure if no text color is specified when a background color is
  specified."
- **relative luminance** (sRGB): "L = 0.2126 * R + 0.7152 * G + 0.0722 * B", com cada canal
  "if RsRGB <= 0.04045 then R = RsRGB/12.92 else R = ((RsRGB+0.055)/1.055) ^ 2.4" e
  "RsRGB = R8bit/255". Nota 2: "Before May 2021 the value of 0.04045 in the definition was
  different (0.03928). [...] It has no practical effect on the calculations".
- **large scale (text):** "with at least 18 point or 14 point bold or font size that would
  yield equivalent size for Chinese, Japanese and Korean (CJK) fonts". Nota 2: "Font size is
  the size when the content is delivered. It does not include resizing that may be done by a
  user."
- **CSS pixel:** "visual angle of about 0.0213 degrees [...] This unit is density-independent,
  and distinct from actual hardware pixels present in a display."
- **target:** "region of the display that will accept a pointer action, such as the
  interactive area of a user interface component".
- **user interface component:** "a part of the content that is perceived by users as a single
  control for a distinct function".
- **cognitive function test:** "A task that requires the user to remember, manipulate, or
  transcribe information." Entre os exemplos: "memorization, such as remembering a username,
  password [...]", "transcription, such as typing in characters", "performance of
  calculations".
- **essential:** "if removed, would fundamentally change the information or functionality of
  the content, and information and functionality cannot be achieved in another way that would
  conform".

## Das páginas Understanding — apoio, não norma

Lidas por um subagente sobre o texto baixado, com a ordem de não inventar e de marcar
`NAO_CONFIRMADO` o que não estivesse na página; cada trecho abaixo foi conferido de novo nesta
sessão contra o arquivo, na linha citada. As Understanding são de 03/09/2026 (Last-Modified).

| critério | o que a página diz, literal | por que importa ao MEOL |
|---|---|---|
| 1.4.3 | "When comparing the computed contrast ratio to the Success Criterion ratio, the computed values should not be rounded (e.g., 4.499:1 would not meet the 4.5:1 threshold)." | o teste de contraste dos tokens compara sem arredondar |
| 1.4.3 | "The ratio between sizes in points and CSS pixels is 1pt = 1.333px, therefore 14pt and 18pt are equivalent to approximately 18.5px and 24px." | "texto grande" nos tokens: 24 CSS px, ou 18,5 CSS px em negrito, **aproximados** pela própria página |
| 1.4.11 | "the computed values should not be rounded (e.g. 2.999:1 would not meet the 3:1 threshold)." | idem, para componente e gráfico |
| 1.4.1 | "if content relies on the user's ability to accurately perceive or differentiate a particular color an additional visual indicator will be required regardless of the contrast ratio between those colors. For example, knowing whether an outline is green for valid or red for invalid." | os estados `COMPLETO`, `PARCIAL` e recusa precisam de rótulo, qualquer que seja o contraste entre as cores deles |
| 3.2.6 | "This is distinct from interface-level help, such as contextual help, features like spell checkers, and instructional text in a form." | a gaveta do porquê (T3) é ajuda contextual e fica fora do 3.2.6; o canal de contato (RI-21) fica dentro |
| 3.3.7 | "This success criterion does not add a requirement to store information between sessions." | o que a pessoa informou num mês não precisa vir preenchido no mês seguinte por força do 3.3.7 |
| 2.5.8 | "The requirement does however apply to targets in any new content that appears on top of other content." | os botões da gaveta do porquê, que abre por cima, entram no RI-31 |
| 3.3.8 | "A service that requires manual transcription of a verification code is not compliant." | código por SMS ou e-mail só vale se puder ser colado |
| 3.3.8 | "authentication methods provided by the user's operating system (such as Windows Hello, or Touch ID/Face ID on macOS and iOS) – are not a cognitive function test." | a biometria do aparelho é caminho aceito, se a P-165 trouxer login |
| 3.3.8 | "such techniques do not fully support the cognitive accessibility community and should be avoided if possible." | dito das exceções de reconhecimento de objeto e de conteúdo pessoal, **não** da WCAG inteira |

**Procurado e não encontrado nas 13 páginas (`NAO_CONFIRMADO`):** nenhuma fala de aplicativo
nativo ("native" e "WCAG2ICT" não aparecem); nenhuma diz que a WCAG deixa de cobrir
necessidades de letramento ("literacy" não aparece). A conclusão sobre letramento, abaixo, vem
da leitura dos critérios AAA, não de uma frase do W3C.

## Linguagem e letramento: o que a WCAG tem, e em que nível

Lidos na recomendação para escrever a limitação 6 dos requisitos sem afirmar uma ausência que
não foi conferida (CLAUDE.md §5-B.13):

- **3.1.3 Unusual Words · nível AAA:** "A mechanism is available for identifying specific
  definitions of words or phrases used in an unusual or restricted way, including idioms and
  jargon."
- **3.1.5 Reading Level · nível AAA:** "When text requires reading ability more advanced than
  the lower secondary education level after removal of proper names and titles, supplemental
  content, or a version that does not require reading ability more advanced than the lower
  secondary education level, is available." Definição de *lower secondary education level*:
  "the two or three year period of education that begins after completion of six years of
  school and ends nine years after the beginning of primary education".

**Leitura:** a WCAG trata de jargão e de nível de leitura, mas **só no AAA**, que a meta AA do
MEOL não inclui. E a régua do 3.1.5 é a escolaridade de nove anos, não a leitura medida de quem
usa. O RI-03 (definição no ponto de uso) faz o que o 3.1.3 pede; o RI-01 vai além do 3.1.5 ao
limitar a camada 1 a uma frase curta. Nenhum dos três prova que a pessoa entendeu: isso é do
teste com pessoas (P-156).

## Fora desta leitura

Critérios da WCAG 2.2 que parecem tocar o MEOL e **não foram lidos** (só o título e o nível,
tirados do HTML da recomendação). Nenhum requisito se apoia neles:

| critério | nível | por que parece tocar o MEOL |
|---|---|---|
| **3.3.4 Error Prevention (Legal, Financial, Data)** | AA | **o mais próximo de um produto financeiro**; o "executei" da T1b e o desfazer antes de gravar |
| 1.3.2 Meaningful Sequence | A | a ordem de leitura decisão → porquê → procedência (a "seleção de prioridades" do Pix) |
| 1.3.1 Info and Relationships | A | a tabela do funil e os rótulos dos números |
| 1.1.1 Non-text Content | A | ícones de estado e o gráfico da reserva |
| 1.4.13 Content on Hover or Focus | AA | a gaveta do porquê |
| 2.1.1 Keyboard | A | pré-condição dos RI-29 e RI-30 |
| 2.4.3 Focus Order | A | a gaveta que abre por cima e fecha no mesmo lugar |
| 2.4.6 Headings and Labels | AA | as três camadas |
| 3.3.1 Error Identification | A | o RI-17 (recusa com o motivo) |
| 3.3.2 Labels or Instructions | A | o cadastro O2 a O4 |
| 3.3.3 Error Suggestion | AA | a recusa que diz o que destrava (F6) |
| 4.1.2 Name, Role, Value | A | todo controle do protótipo |
| 4.1.3 Status Messages | AA | a confirmação da T1b |
