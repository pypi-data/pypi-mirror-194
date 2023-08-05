from datetime import date

import pytest

from violeta.indices.indexador_diario import IndexadorDiario
from violeta.indices.cdi import IndexadorCDI


data = date(2022, 1, 20)
periodo_defasagem = 15


def test_indexador_diario_not_implemented_error():
    indexador_diario = IndexadorDiario()
    with pytest.raises(NotImplementedError):
        indexador_diario.get_daily_value(data)


def test_indexador_diario_cdi_get_daily_value_success():
    indexador_diario = IndexadorCDI()
    assert indexador_diario.get_daily_value(data, periodo_defasagem) == 0.00034749
