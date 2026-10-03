# -*- coding: utf-8 -*-
"""Os documentos de marca e de UX nao falam a lingua dos achados.

POR QUE (decisao dele, 26/09/2026). A pesquisa de marca trouxe um livro de codigos com
prefixo C (numeros 01 a 29) e requisitos de interface com prefixo R (01 a 21). O projeto ja
tinha C-01 (fator), C-02 (ajuste de proventos), C-03 (moeda) e R-01 (ordem dos portoes). Com
os documentos como chegaram, "C-02"
passava a significar duas coisas, e os instrumentos (`achados_ancorados`, `codigos_preservados`)
os contariam como achados -- 32 codigos novos presos na linha de base, sem ninguem ver: as
suites passavam. A decisao foi renomear SO nesses documentos, C-xx -> MC-xx e R-xx -> RI-xx.

O QUE MEDE (P5): (1) nenhum codigo de `docs/marca/` e `docs/ux/` e tambem citado no
`ACHADOS.md`, fora as citacoes deliberadas de achados do projeto, listadas com o motivo;
(2) o conjunto do `codigos_preservados` e o mesmo com e sem essas pastas. NAO mede se um
MC-xx ou RI-xx citado tem definicao -- isso e da propria numeracao dos documentos.
"""
from __future__ import annotations

import io
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)
import achados_ancorados as A  # noqa: E402
import codigos_preservados as CP  # noqa: E402

PASTAS = ("docs/marca/", "docs/ux/")

# Achados DO PROJETO que os documentos citam com o mesmo sentido -- citacao, nao colisao.
CITACOES_DE_ACHADO = {
    "F-02": "ausencia virando numero; o RI-10 e o F-02 na interface",
    "U-01": "um cliente novo teria isso? -- a regra de nao bloquear por dado de usuario",
    "A-03": "o codigo da emissora muda e a historia nao vem junto (troca de ticker)",
    "X-01": "o dado estruturado nao alcanca a decisao (o dossie fica fora da v1)",
    "D-01": "numero sobre o dinheiro dele so em estado.yaml; citado na nota dos prints",
    "P-116": "pre-registro vale pelo que foi empurrado primeiro; citado no pre-registro do "
             "teste de marca de 20/09 (27/09/2026)",
    "P-115": "o criterio do degrau (C-02 v2); o mapa de telas a cita como o caminho critico, e o "
             "PO-01 e o GIT-03 citam a corrida que a fechou (03/10/2026)",
    "P-165": "onde o motor roda (servidor sem estado); o mapa de telas a cita, e o GIT-03 cita a "
             "sessao que a fechava (03/10/2026)",
}


def _documentos(raiz=RAIZ):
    out = []
    for pasta in PASTAS:
        base = os.path.join(raiz, pasta)
        if os.path.isdir(base):
            out += [os.path.join(base, f) for f in sorted(os.listdir(base)) if f.endswith(".md")]
    return out


def _codigos_do_texto(s):
    return {c for c in (f"{m.group(1)}-{m.group(2)}" for m in A.REF.finditer(s))
            if A.conta_como_codigo(c)}


def colisoes(raiz=RAIZ):
    """{codigo: [documento]} dos codigos das pastas de marca/UX que o ACHADOS.md tambem cita."""
    with io.open(os.path.join(raiz, "ACHADOS.md"), encoding="utf-8") as f:
        do_projeto = _codigos_do_texto(f.read())
    out: dict[str, list[str]] = {}
    for caminho in _documentos(raiz):
        with io.open(caminho, encoding="utf-8") as f:
            for c in _codigos_do_texto(f.read()) & do_projeto:
                if c not in CITACOES_DE_ACHADO:
                    out.setdefault(c, []).append(os.path.relpath(caminho, raiz))
    return out


def acrescimos(raiz=RAIZ):
    """Os codigos que o `codigos_preservados` so conta POR CAUSA das pastas de marca/UX."""
    return sorted(set(CP.codigos(raiz)) - set(CP.codigos(raiz, excluir=PASTAS)))


def test_os_documentos_existem():
    """Vacuidade: sem os documentos, os dois testes abaixo passariam sem medir nada."""
    nomes = {os.path.relpath(p, RAIZ).replace("\\", "/") for p in _documentos()}
    assert {"docs/marca/requisitos-interface-v1.md", "docs/ux/mapa-de-telas-v1.md"} <= nomes


def test_nenhum_codigo_de_marca_colide_com_um_achado():
    assert colisoes() == {}


def test_os_documentos_nao_mudam_os_codigos_preservados():
    assert acrescimos() == []


def test_mutacao_um_C_de_marca_de_volta_reprova(tmp_path):
    """A guarda falha quando deveria (regua 5-B, pergunta 4): um documento com o `C-02` da
    rodada 2 como chegou colide com o achado do ajuste de proventos."""
    # Os codigos da mutacao sao montados, nao escritos: escritos por extenso, este proprio
    # arquivo os poria no `codigos_preservados` -- o defeito que o teste existe para pegar.
    c02, c24 = "C" + "-02", "C" + "-24"
    (tmp_path / "docs" / "marca").mkdir(parents=True)
    (tmp_path / "ACHADOS.md").write_text(f"## {c02} · ajuste de proventos\n", encoding="utf-8")
    doc = tmp_path / "docs" / "marca" / "x.md"
    doc.write_text(f"| **{c02}** | maximo condicionado |\n| **{c24}** | celebridade |\n",
                   encoding="utf-8")
    assert colisoes(str(tmp_path)) == {c02: [os.path.join("docs", "marca", "x.md")]}
    assert acrescimos(str(tmp_path)) == [c24], "o primeiro ja existe fora; o segundo so ali"
    doc.write_text("| **MC-02** | maximo condicionado |\n| **MC-24** | celebridade |\n",
                   encoding="utf-8")
    assert colisoes(str(tmp_path)) == {} and acrescimos(str(tmp_path)) == []


def test_os_prefixos_de_outro_dominio_nao_escondem_achado():
    """A exclusao e por PREFIXO inteiro: `MC-02` fica de fora, `C-02` continua contando."""
    assert not A.conta_como_codigo("MC-02") and not A.conta_como_codigo("RI-10")
    assert A.conta_como_codigo("C-02") and A.conta_como_codigo("R-01")


def test_nenhum_titulo_de_achado_usa_prefixo_de_outro_dominio():
    """A exclusao de MC/RI e por prefixo, e por isso tem um custo: um achado do projeto que
    nascesse com titulo `## MC-01` ou `## RI-02` sumiria calado dos dois instrumentos -- nem
    orfao no `achados_ancorados`, nem preservado no `codigos_preservados`. O ACHADOS.md nao
    pode usar esses prefixos em titulo."""
    with io.open(os.path.join(RAIZ, "ACHADOS.md"), encoding="utf-8") as f:
        assert A.titulos_em_outro_dominio(f.read()) == []


def test_mutacao_titulo_MC_no_ACHADOS_reprova(tmp_path):
    achados = tmp_path / "ACHADOS.md"
    achados.write_text("## A-01 · um achado\n\n## " + "MC" + "-01 · um achado com prefixo "
                       "de marca\n\n> ### RI-" + "02 · em citacao tambem\n", encoding="utf-8")
    assert A.titulos_em_outro_dominio(achados.read_text(encoding="utf-8")) == ["MC-01",
                                                                             "RI-02"]
