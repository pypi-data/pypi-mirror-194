from datetime import date
from math import isclose

import pytest

from violeta.indices.indexador_mensal import IndexadorMensal
from violeta.indices.ipca import IndexadorIPCA
from violeta.indices.igpm import IndexadorIGPM
from violeta.indices.incc import IndexadorINCC


data = date(2022, 1, 20)
periodo_defasagem = 10


def test_indexador_mensal_not_implemented_error():
    indexador_mensal = IndexadorMensal()
    with pytest.raises(NotImplementedError):
        indexador_mensal.get_daily_value(data, periodo_defasagem)


def test_indexador_mensal_ipca_get_daily_value_success():
    indexador_mensal = IndexadorIPCA()
    assert isclose(
        indexador_mensal.get_daily_value(data, periodo_defasagem),
        0.00042,
        abs_tol=0.00001,
    )


def test_indexador_mensal_igpm_get_daily_value_success():
    indexador_mensal = IndexadorIGPM()
    assert isclose(
        indexador_mensal.get_daily_value(data, periodo_defasagem),
        0.00133,
        abs_tol=0.0001,
    )


def test_indexador_mensal_incc_get_daily_value_success():
    indexador_mensal = IndexadorINCC()
    assert isclose(
        indexador_mensal.get_daily_value(data, periodo_defasagem),
        0.00059,
        abs_tol=0.00001,
    )
