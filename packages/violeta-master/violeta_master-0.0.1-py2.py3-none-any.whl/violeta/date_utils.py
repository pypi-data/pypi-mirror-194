import datetime
import os
from typing import List

import bizdays as _bizdays
import calendar
import datetime as dt
import pandas as pd

from dateutil.parser import parse as _parser
from dateutil.relativedelta import relativedelta

from .constantes import EnumTipoContagemDias
from .exceptions import DataInvalidaError

PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))


def feriados_anbima():
    ANBIMA_PATH = os.path.join(PACKAGE_DIR, 'data', 'ANBIMA.txt')
    with open(ANBIMA_PATH) as anbima:
        holidays = [d.strip() for d in anbima.readlines()]
    return holidays


_cal = _bizdays.Calendar(feriados_anbima(), ['Sunday', 'Saturday'])


def next_bizday(date):
    return _cal.adjust_next(force_date(date))


def prev_bizday(date):
    return _cal.adjust_previous(force_date(date))


def adjust_next_bizdays(date):
    date = force_date(date)
    return next_bizday(date + relativedelta(days=+1))


def adjust_prev_bizdays(date):
    date = force_date(date)
    return prev_bizday(date + relativedelta(days=-1))


def dateparser(d, fmt='%d/%m/%Y'):
    if d is None:
        return None
    elif isinstance(d, str):
        return dt.datetime.strptime(d, fmt).date()

    elif isinstance(d, dt.datetime):
        return d.date()
    elif isinstance(d, dt.date):
        return d
    raise ValueError('formato invalido')


def _date2str(date: dt.date):
    try:
        return force_date(date).strftime('%Y-%m-%d')
    except AttributeError:
        return date


def force_date(date, raise_exc=True):
    if isinstance(date, dt.datetime):
        return date.date()
    elif isinstance(date, dt.date):
        return date
    try:
        return _parser(date).date()
    except Exception:
        if raise_exc:
            raise


def force_datetime(datetime, raise_exc=True):
    if isinstance(datetime, dt.datetime):
        return datetime

    elif isinstance(datetime, dt.date):
        return dt.datetime.combine(datetime, dt.datetime.min.time())

    try:
        return _parser(datetime)
    except Exception:
        if raise_exc:
            raise


def is_bizday(date):
    return _cal.isbizday(_date2str(date))


def bizdays_delta(start, end):
    """
    :param start: objeto date ou string iso de data (YYYY-MM-DD)
    :param end: objeto date ou string iso de data (YYYY-MM-DD)
    :return numero de dias uteis entre a data "start" e "end"
    """
    d1 = force_date(start)
    d2 = next_bizday(force_date(end))

    return _cal.bizdays(d1, d2)


def diferenca_dias_corridos(data_inicio, data_fim):
    inicio = force_date(data_inicio)
    fim = force_date(data_fim)
    return (fim - inicio).days


def diferenca_dias(data_inicial, data_final, tipo_contagem_dias: EnumTipoContagemDias):
    if tipo_contagem_dias == EnumTipoContagemDias.uteis:
        return bizdays_delta(data_inicial, data_final)
    return diferenca_dias_corridos(data_inicial, data_final)


def bizdays_range(*args, **kwargs):
    """
    wrapper da funcao date_range do pandas
    (https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.date_range.html)

    aceita os mesmos argumentos da funcao e retorna um generator que exclui nao-workdays do daterange
    """
    import pandas as pd

    dt_range = pd.date_range(*args, **kwargs)

    for timestamp in dt_range:
        if is_bizday(timestamp.date()):
            yield timestamp


def datas_vencimento(primeiro_vcto, periodo, qtde, data_emissao=False):
    delta = {"s": {"weeks": 1},
             "m": {"months": 1},
             "d": {"days": 1},
             }[periodo]
    delta = relativedelta(**delta)

    # considerando a data de emissao para gerar o fluxo
    if data_emissao:
        vctos = [data_emissao + i * delta for i in range(qtde + 1)]
        vctos.pop(0)
    else:
        vctos = [primeiro_vcto + i * delta for i in range(qtde)]
    ajust = [next_bizday(v) for v in vctos]
    return [dict(data_vencimento=v, data_ajustada=vu) for v, vu in zip(vctos, ajust)]


def last_day_month(date):
    return calendar.monthrange(date.year, date.month)[1]


def date_range(primeiro_dia: datetime.date, ultimo_dia: datetime.date, tipo_contagem: EnumTipoContagemDias) -> List[dt.date]:
    """
    Retorna uma lista de datas conforme o período passado

    :param date primeiro_dia: primeira data inclusiva do range
    :param date ultimo_dia: ultima data inclusiva do range
    :param EnumTipoContagemDias tipo_contagem: define se os dias serão corridos ou úteis

    :raises DataInvalidaError: caso alguma data seja incompativel para criar o range
    """
    if primeiro_dia > ultimo_dia:
        raise DataInvalidaError("primeiro_dia precisa ser menor que ultimo_dia")

    dias_corridos = pd.date_range(start=primeiro_dia, end=ultimo_dia).to_pydatetime().tolist()

    if tipo_contagem == EnumTipoContagemDias.uteis:
        return [dia.date() for dia in dias_corridos if is_bizday(dia)]

    return [dia.date() for dia in dias_corridos]


def bizdays_in_month(date: datetime.date) -> int:
    """
    Retorna quantos dias úteis existem no mês da data passada

    :param datetime.date date: data cujo mês queremos a quantidade de dias uteis
    """
    first_day = datetime.date(date.year, date.month, 1)
    last_day_inclusive = datetime.date(date.year, date.month, last_day_month(date))

    return bizdays_delta(first_day, last_day_inclusive)
