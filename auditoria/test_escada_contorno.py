# -*- coding: utf-8 -*-
"""A guarda da escada de contorno (CLAUDE.md 5-B.18): NAO_CONFIRMADO por falta de acesso so
com `escada:` ou uma P-nnn na mesma linha. Ver auditoria/escada_contorno.py."""
from __future__ import annotations

import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import escada_contorno as EC  # noqa: E402

RAIZ = EC.RAIZ


def test_nenhuma_linha_nova_sem_escada_e_a_base_nao_tem_item_velho():
    novas, obsoletas = EC.varrer()
    assert novas == [], "NAO_CONFIRMADO por acesso sem escada (5-B.18):\n" + "\n".join(novas)
    assert obsoletas == [], "itens da linha de base que nao casam mais:\n" + "\n".join(obsoletas)


def test_mutacao_linha_nova_sem_escada_reprova():
    """A guarda falha quando deve: a frase de 06/09, escrita de novo, reprova."""
    assert EC.violacoes_no_texto("NAO_CONFIRMADO: o site bloqueia robo; visita manual\n")
    assert EC.violacoes_no_texto("| x | NAO CONFIRMADO (pagina devolveu HTTP 403) |\n")
    assert EC.violacoes_no_texto("N\u00c3O CONFIRMADO: sem acesso ao portal\n")


def test_escada_ou_pendencia_na_linha_passa():
    assert not EC.violacoes_no_texto(
        "NAO_CONFIRMADO, escada: 1 curl -> 403 (Akamai); 2 Wayback -> tunel caiu; 4 -> P-05\n")
    assert not EC.violacoes_no_texto("NAO_CONFIRMADO: o site bloqueia robo; roteiro na P-05\n")


def test_riscado_e_retratacao_e_nao_conta_nem_em_varias_linhas():
    texto = ("~~NAO_CONFIRMADO: `olinda` esta bloqueado por robots.txt --\n"
             "nao contornado. NAO_CONFIRMADO: robots~~ o resto da linha\n")
    assert EC.violacoes_no_texto(texto) == []
    assert EC.sem_riscado(texto).count("\n") == texto.count("\n")


def test_nao_confirmado_sem_motivo_de_acesso_nao_e_da_guarda():
    """A guarda e sobre ACESSO: NAO_CONFIRMADO por falta de leitura ou de dado nao reprova."""
    assert not EC.violacoes_no_texto("NAO_CONFIRMADO: ninguem mediu a compressao Parquet/CSV\n")


def _repo(tmp_path, texto):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / "nota.md").write_text(texto, encoding="utf-8")
    return str(tmp_path)


def test_mutacao_num_repositorio_uma_linha_nova_sem_escada_reprova(tmp_path):
    """Mutacao ponta a ponta: um .md ainda nao adicionado ao git ja entra na varredura."""
    raiz = _repo(tmp_path, "# nota\n\nNAO_CONFIRMADO: site do gestor bloqueia robo\n")
    novas, _ = EC.varrer(raiz, base={})
    assert novas == ["nota.md:3: NAO_CONFIRMADO: site do gestor bloqueia robo"]


def test_linha_de_base_casa_pelo_conteudo_e_item_velho_reprova(tmp_path):
    linha = "NAO_CONFIRMADO: site do gestor bloqueia robo"
    raiz = _repo(tmp_path, linha + "\n")
    base = {("nota.md", EC.chave(linha)): "motivo"}
    assert EC.varrer(raiz, base=base) == ([], [])
    # a linha foi consertada (ganhou escada): o item da base fica velho e reprova
    (tmp_path / "nota.md").write_text(linha + "; escada: 1 curl -> 200\n", encoding="utf-8")
    novas, velhas = EC.varrer(raiz, base=base)
    assert novas == [] and len(velhas) == 1


def test_linha_de_base_exige_motivo(tmp_path):
    p = tmp_path / "base.txt"
    p.write_text("docs/x.md | abcdef012345 |\n", encoding="utf-8")
    try:
        EC.ler_base(str(p))
    except ValueError:
        return
    raise AssertionError("item da base sem motivo foi aceito")


def test_os_casos_de_27_09_estao_reescritos_com_a_medicao_nova():
    """Os tres casos da regra 18: o texto antigo riscado e a medicao nova com o degrau."""
    def ler(rel):
        with open(os.path.join(RAIZ, *rel.split("/")), encoding="utf-8") as f:
            return f.read()
    pesquisa = ler("docs/fontes/pesquisa-bases-e-apis-2026-09.md")
    assert "~~NAO_CONFIRMADO: `olinda.bcb.gov.br` esta **bloqueado por robots.txt**" in pesquisa
    assert "escada: 1 curl no terminal \u2192 HTTP 200" in pesquisa
    assert ("~~NAO_CONFIRMADO: se `cad_fi` da CVM tem campo de taxa (dominio bloqueado);~~"
            in pesquisa)
    assert "**`TAXA_PERFM` na 22 e `TAXA_ADM` na 24**" in pesquisa
    mapa = [linha for linha in ler("docs/fontes/MAPA-CONSTANTES.md").splitlines()
            if linha.startswith("| `etf.BOVV11`")]
    assert len(mapa) == 1
    assert "~~site do gestor bloqueia rob\u00f4; visita manual~~" in mapa[0]
    assert "escada:" in mapa[0] and "P-05" in mapa[0]
