# -*- coding: utf-8 -*-
"""O universo e a ordem canonica do D1, e o sorteio e fixo para a semente declarada."""
import datetime as dt
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c02_sorteio_d1 as S  # noqa: E402


def _r(tipo, ex, tk, valor, status="DERIVADA"):
    return dict(tipo=tipo, data_ex=ex, _ticker=tk, valor=valor, data_ex_status=status)


CASADOS = [
    _r("JRS CAP PROPRIO", "2016-05-02", "BBB3", "0.10"),
    _r("JRS CAP PROPRIO", "2016-05-02", "AAA3", "0.20"),
    _r("JRS CAP PROPRIO", "2016-05-02", "AAA3", "0.15"),     # mesmo par, outro valor: fica 0.15
    _r("JRS CAP PROPRIO", "2015-12-30", "CCC3", "0.10"),     # antes da janela
    _r("JRS CAP PROPRIO", "2021-01-04", "CCC3", "0.10"),     # depois da janela
    _r("DIVIDENDO", "2017-01-02", "DDD3", "0.10"),           # tipo errado
    _r("JRS CAP PROPRIO", "2018-01-02", "EEE3", "0"),        # valor nao positivo
    _r("JRS CAP PROPRIO", "2018-01-03", "FFF3", "0.05", status="SEM_DATA"),
    _r("JRS CAP PROPRIO", "2020-12-31", "GGG3", "0.30"),     # ultimo dia da janela
]


def test_universo_filtra_ordena_e_conta_o_par_uma_vez():
    linhas, multi = S.universo(CASADOS)
    assert linhas == [(dt.date(2016, 5, 2), "AAA3", "0.15"), (dt.date(2016, 5, 2), "BBB3", "0.10"),
                      (dt.date(2020, 12, 31), "GGG3", "0.30")]
    assert multi == 1


def test_semente_e_posicoes_declaradas():
    assert S.SEMENTE == 20260927 and S.POSICOES == 30


def test_sorteio_e_a_permutacao_do_numpy_com_a_semente_e_e_repetivel():
    linhas = [(dt.date(2016, 1, 4) + dt.timedelta(days=i), f"T{i:03d}3", "0.1")
              for i in range(100)]
    a = S.sortear(linhas)
    assert a == S.sortear(linhas) and len(a) == 30
    perm = np.random.default_rng(20260927).permutation(100)
    assert [x[1] for x in a] == [int(i) for i in perm[:30]]
    assert [x[1] for x in S.sortear(linhas, semente=1)] != [x[1] for x in a]
