import numpy as np
from scipy.optimize import newton, brentq
from .date_utils import bizdays_delta, force_datetime, dt, diferenca_dias
from decimal import Decimal, getcontext
from violeta.constantes import EnumTipoContagemDias, EnumTipoJuros
from violeta.date_utils import force_date

getcontext().prec = 9

_BASE_DU = 252

def tir(valor_desembolsado, data_desembolso, dts_pagamentos, vls_pagamentos,
        dias_uteis=True, mes_base=None):
    """
    Taxa Interna de Retorno
    """

    def _calcula_tir(taxa, pagamentos, dias_corridos, valor_desembolsado, mes_base):
        _tx = (1 + taxa / 100) ** (1 / mes_base) - 1

        parciais = [pmt / ((1 + _tx) ** du) for du, pmt in zip(dias_corridos, pagamentos)]
        estimativa_pv = np.sum(parciais)
        desired_zero = abs(valor_desembolsado - estimativa_pv)
        return desired_zero

    # usa o Internal Rate of Return (IRR) para estimar o x0
    x0 = 100 * np.irr([-1 * valor_desembolsado, *vls_pagamentos])

    if not dias_uteis:
        return x0

    dias_corridos = [bizdays_delta(data_desembolso, data) for data in dts_pagamentos]

    if not mes_base:
        mes_base = 21

    approx = newton(_calcula_tir, x0=x0, args=(
        vls_pagamentos, dias_corridos, valor_desembolsado, mes_base))

    return approx


def vp(parcela, taxa_mensal, data_desembolso, data_pgto, mes_base='util'):
    """
    Valor Presente
    da uma aproximacao bem ruim -- os centavos nao batem OU testei com exemplos errados
    """
    from functools import partial

    mes = {'util': 21, 'corrido': 30}
    assert mes_base in mes.keys(), 'mes_base invalido'

    try:
        data_pgto = force_datetime(data_pgto)
    except TypeError:
        # assumindo q dtata_pgto eh uma collection de datas. se nao for vai estourar um erro lindo de ver
        _vp = partial(vp, parcela, taxa_mensal, data_desembolso, mes_base=mes_base)
        return [_vp(d) for d in data_pgto]

    if mes_base == 'util':
        dias = bizdays_delta(data_desembolso, data_pgto)
    else:
        dias = (force_datetime(data_pgto) - data_desembolso).days

    x = (1 + taxa_mensal) ** (dias / mes[mes_base])  # <<<< vou acessar chave de dic com colchete SIM

    return parcela / x


def xnpv(rate, values, dates):
    if rate <= -1.0:
        return float('inf')
    d0 = dates[0]
    return round(sum([vi / (1.0 + rate)**(bizdays_delta(d0, di) / _BASE_DU) for vi, di in zip(values, dates)]), 8)


def xirr(values, dates):
    """
    taxa interna de retorno (goal seek)
    """
    try:
        return newton(lambda r: xnpv(r, values, dates), 0.0)
    except RuntimeError:
        return brentq(lambda r: xnpv(r, values, dates), -1.0, 1e10)


def xvp(parcela, taxa, data, hoje):
    """
    valor presente
    """
    du = bizdays_delta(hoje, data)
    p = parcela / ((1 + taxa) ** (du / _BASE_DU))
    return p


def xvf(parcela, taxa, data, hoje):
    """
    valor futuro
    """
    du = bizdays_delta(hoje, data)
    p = parcela * ((1 + taxa) ** (du / _BASE_DU))
    return p


def taxa_pre_anual(valor_nominal: float, valor_presente: float, data_base: dt.date, data_vencimento: dt.date, du_base=252) -> float:
    """
    taxa pre anual
    """
    du = bizdays_delta(data_base, data_vencimento)
    taxa = ((float(valor_nominal) / float(valor_presente)) ** (du_base / du)) - 1
    return taxa


def fator_taxa_pre_acumulado(spread: float, data_aquisicao: dt.date, data_ref: dt.date) -> Decimal:
    du = bizdays_delta(data_aquisicao, data_ref)
    return Decimal((1 + float(spread)) ** (du / _BASE_DU))


def fator_taxa_pre_descontado(spread: float, data_ref: dt.date, data_vencimento: dt.date) -> Decimal:
    du = bizdays_delta(data_ref, data_vencimento)
    return Decimal((1 + float(spread)) ** (du / _BASE_DU))


def _valor_juros_moratorios_simples(valor_base: float,
                                    dias_atraso: int,
                                    quantidade_dias_mes: int,
                                    taxa_ao_mes: float):
    return round(valor_base * dias_atraso * (taxa_ao_mes / 100 / quantidade_dias_mes), 2)


def _valor_juros_moratorios_composto(valor_base: float,
                                     dias_atraso: int,
                                     quantidade_dias_mes: int,
                                     taxa_ao_mes: float):
    total = round(valor_base * ((100 + taxa_ao_mes) / 100) ** (dias_atraso / quantidade_dias_mes), 2)
    return round(total - valor_base, 2)


def _forca_datas(data_inicial, data_atual):
    data_inicial = force_date(data_inicial)
    data_atual = force_date(data_atual)
    return data_inicial, data_atual


def _datas_validas(data_inicial, data_atual, dias_carencia, tipo_contagem_dias):
    data_inicial, data_atual = _forca_datas(data_inicial, data_atual)
    if data_inicial < data_atual:
        dias_atraso = diferenca_dias(data_inicial, data_atual, tipo_contagem_dias)
        if dias_atraso > dias_carencia:
            return True, dias_atraso
    return False, 0


def valor_juros_moratorios(valor_base: float,
                           data_inicial,
                           data_atual,
                           tipo_contagem_dias: EnumTipoContagemDias,
                           taxa_ao_mes: float,
                           tipo_juros: EnumTipoJuros,
                           juros_aberto: float = 0.0,
                           dias_carencia: int = 0):
    datas_validas, dias_atraso = _datas_validas(data_inicial, data_atual, dias_carencia, tipo_contagem_dias)
    if datas_validas:
        if tipo_juros == EnumTipoJuros.simples:
            return _valor_juros_moratorios_simples(valor_base, dias_atraso, tipo_contagem_dias.value, taxa_ao_mes)
        elif tipo_juros == EnumTipoJuros.composto:
            return _valor_juros_moratorios_composto(valor_base + juros_aberto, dias_atraso, tipo_contagem_dias.value, taxa_ao_mes)
    return 0.00


def valor_multa_moratoria(valor_base: float,
                          data_inicial,
                          data_atual,
                          tipo_contagem_dias: EnumTipoContagemDias,
                          percentual_multa: float,
                          dias_carencia: int = 0):
    datas_validas, _ = _datas_validas(data_inicial, data_atual, dias_carencia, tipo_contagem_dias)
    if datas_validas:
        return round(valor_base * percentual_multa / 100, 2)
    return 0.0
