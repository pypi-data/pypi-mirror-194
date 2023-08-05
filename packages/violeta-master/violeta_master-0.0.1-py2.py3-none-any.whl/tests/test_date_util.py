import datetime as dt

import pytest

from violeta.date_utils import *
from violeta.constantes import EnumTipoContagemDias

DATE_STR = '2018-10-12'  # dia das criancas
DATE = dt.date(2018, 10, 12)
DATETIME = dt.datetime(2018, 10, 12)


def test_force_date():
    assert force_date(DATE_STR) == DATE
    assert force_date(DATE) == DATE
    assert force_date(DATETIME) == DATE


def test_force_datetime():
    assert force_datetime(DATE_STR) == DATETIME
    assert force_datetime(DATE) == DATETIME
    assert force_datetime(DATETIME) == DATETIME


def test_is_bizday():
    assert is_bizday('2018-10-12') is False  # dia das criancas
    assert is_bizday('2018-10-13') is False  # sabado
    assert is_bizday('2018-10-14') is False  # domingo
    assert is_bizday('2018-10-15') is True   # segunda

    assert is_bizday(DATE) is False
    assert is_bizday(DATETIME) is False

    assert is_bizday(dt.date(2018, 10, 15)) is True
    assert is_bizday(dt.datetime(2018, 10, 15)) is True


def test_bizdays_delta():
    assert bizdays_delta('2018-10-12', '2018-10-14') == 0
    assert bizdays_delta('2018-06-01', '2018-06-30') == 21  # testando um mes sem feriado


def test_diferenca_dias_uteis():
    assert diferenca_dias('2020-08-10', '2020-08-17', EnumTipoContagemDias.uteis) == 5
    assert diferenca_dias('2020-08-10', '2020-08-17', EnumTipoContagemDias.corridos) == 7


def test_adjust_next_bizdays():
    assert adjust_next_bizdays('2020-08-10') == dt.date(2020, 8, 11)
    assert adjust_next_bizdays('2020-08-7') == dt.date(2020, 8, 10)


def test_adjust_prev_bizdays():
    assert adjust_prev_bizdays('2020-08-10') == dt.date(2020, 8, 7)
    assert adjust_prev_bizdays('2020-08-11') == dt.date(2020, 8, 10)


def test_last_day_month():
    dia = last_day_month(dt.date(2020, 2, 5))
    assert dia == 28 or 29
    assert isinstance(dia, int)


@pytest.mark.parametrize('data_inicio, data_final, contagem, dias', [
                         (dt.date(2022, 1, 1), dt.date(2022, 2, 1), EnumTipoContagemDias.uteis, 22),
                         (dt.date(2022, 1, 1), dt.date(2022, 2, 1), EnumTipoContagemDias.corridos, 32)],
                         ids=["dias uteis", "dias corridos"])
def test_date_range(data_inicio, data_final, contagem, dias):
    dates = date_range(data_inicio, data_final, contagem)

    assert len(dates) == dias


@pytest.mark.parametrize('data, dias_uteis', [
    (dt.date(2022, 1, 1), 20),
    (dt.date(2022, 2, 4), 19),
    (dt.date(2022, 3, 8), 21),
    (dt.date(2022, 4, 8), 19),
], ids=['jan', 'fev', 'mar', 'abr'])
def test_bizdays_in_month(data, dias_uteis):
    assert bizdays_in_month(data) == dias_uteis
