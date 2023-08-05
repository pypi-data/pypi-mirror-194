from datetime import date
from unittest.mock import call

import pytest

from violeta.constantes import EnumTipoContagemDias
from violeta.pos_fixado import CalculoPosFixado


def test_calculo_pos_fixado_cdi_calcula_valor_atualizado(mocker):
    data_inicio = date(2022, 1, 1)
    data_final = date(2022, 2, 1)
    valor = 1000.0
    taxa_pre = 0.0

    pos_fixado = CalculoPosFixado("cdi", EnumTipoContagemDias.uteis, defasagem_indice=0)
    pos_fixado.indice.get_taxa_diaria = mocker.Mock(return_value=0.00034749)

    valor_atualizado = pos_fixado.calcula_valor_atualizado(
        valor, data_inicio, data_final, taxa_pre
    )

    assert valor_atualizado.valor == 1007.67


def test_calculo_pos_fixado_cdi_calcula_valor_atualizado_com_defasagem():
    data_inicio = date(2022, 1, 14)
    data_final = date(2022, 2, 14)
    valor = 21_000_000.0
    taxa_pre = 0.1

    pos_fixado = CalculoPosFixado("cdi", EnumTipoContagemDias.uteis, defasagem_indice=5)

    valor_atualizado = pos_fixado.calcula_valor_atualizado(
        valor, data_inicio, data_final, taxa_pre
    )

    assert valor_atualizado.valor == 21_343_718.23
    assert valor_atualizado.fator_pre == 1.00835544
    assert valor_atualizado.fator_pos == 1.0079457


def test_calculo_pos_fixado_ipca_calcula_valor_atualizado_com_defasagem():
    data_inicio = date(2022, 1, 14)
    data_final = date(2022, 2, 14)
    valor = 21_000_000.0
    taxa_pre = 0.1

    pos_fixado = CalculoPosFixado(
        "ipca", EnumTipoContagemDias.uteis, defasagem_indice=5
    )

    valor_atualizado = pos_fixado.calcula_valor_atualizado(
        valor, data_inicio, data_final, taxa_pre
    )

    assert valor_atualizado.valor == 21_404_723.71
    assert valor_atualizado.fator_pre == 1.00835544
    assert valor_atualizado.fator_pos == 1.01082665


def test_calculo_pos_fixado_cdi_com_data_util_valida(mocker):
    data_inicio = date(2022, 1, 13)
    data_final = date(2022, 1, 17)
    valor = 1000.0
    taxa_pre = 0.0

    pos_fixado = CalculoPosFixado("cdi", EnumTipoContagemDias.uteis, defasagem_indice=2)
    pos_fixado.indice.get_taxa_diaria = mocker.Mock(return_value=0.00034749)

    pos_fixado.calcula_valor_atualizado(valor, data_inicio, data_final, taxa_pre)

    assert pos_fixado.indice.get_taxa_diaria.call_args_list == [
        call(date(2022, 1, 13), 2),
        call(date(2022, 1, 14), 2),
        call(date(2022, 1, 17), 2),
    ]


def test_calculo_pos_fixado_cdi_com_data_corrida_valida(mocker):
    data_inicio = date(2022, 1, 12)
    data_final = date(2022, 1, 15)
    valor = 1000.0
    taxa_pre = 0.0
    defasagem_final = 2

    pos_fixado = CalculoPosFixado(
        "cdi", EnumTipoContagemDias.corridos, defasagem_indice=2
    )
    pos_fixado.indice.get_taxa_diaria = mocker.Mock(return_value=0.00034749)

    pos_fixado.calcula_valor_atualizado(valor, data_inicio, data_final, taxa_pre)

    assert pos_fixado.indice.get_taxa_diaria.call_args_list == [
        call(date(2022, 1, 12), 2),
        call(date(2022, 1, 13), 2),
        call(date(2022, 1, 14), 2),
        call(date(2022, 1, 15), 2),
    ]


def test_calculo_pos_fixado_cdi_calcula_valor_atualizado_com_taxa_pre():
    data_inicio = date(2022, 1, 14)
    data_final = date(2022, 2, 13)
    valor = 21_000_000.0
    taxa_pre = 0.1

    pos_fixado = CalculoPosFixado("cdi", EnumTipoContagemDias.uteis, defasagem_indice=0)

    valor_atualizado = pos_fixado.calcula_valor_atualizado(
        valor, data_inicio, data_final, taxa_pre
    )

    assert valor_atualizado.valor == 21_330_546.71


def test_calculo_pos_fixado_cdi_calcula_valor_atualizado_com_variacao_entre_meses():
    data_inicio = date(2022, 1, 14)
    data_final = date(2022, 3, 21)
    valor = 21_000_000.0
    taxa_pre = 0.1

    pos_fixado = CalculoPosFixado("cdi", EnumTipoContagemDias.uteis, defasagem_indice=0)

    valor_atualizado = pos_fixado.calcula_valor_atualizado(
        valor, data_inicio, data_final, taxa_pre
    )

    assert valor_atualizado.valor == 21_735_846.12


def test_calculo_pos_fixado_cdi_calcula_valor_atualizado_com_amortizacoes():
    data_inicio = date(2022, 1, 14)
    data_final = date(2022, 3, 3)
    valor = 21_000_000.0
    taxa_pre = 0.1

    pos_fixado = CalculoPosFixado("cdi", EnumTipoContagemDias.uteis, defasagem_indice=0)

    pagamentos = {date(2022, 2, 14): 1_513_853.73}

    valor_atualizado = pos_fixado.calcula_valor_atualizado(
        valor, data_inicio, data_final, taxa_pre, amortizacoes=pagamentos
    )

    assert valor_atualizado.valor == 20_004_194.60


def test_calculo_pos_fixado_ipca_calcula_valor_atualizado():
    data_inicio = date(2022, 1, 14)
    data_final = date(2022, 2, 14)
    valor = 21_000_000.0
    taxa_pre = 0.1

    pos_fixado = CalculoPosFixado(
        "ipca", EnumTipoContagemDias.uteis, defasagem_indice=2
    )

    valor_atualizado = pos_fixado.calcula_valor_atualizado(
        valor, data_inicio, data_final, taxa_pre
    )

    assert valor_atualizado.valor == 21_373_664.74


def test_calculo_pos_fixado_ipca_calcula_valor_atualizado_fixo(mocker):
    data_inicio = date(2022, 1, 1)
    data_final = date(2022, 2, 1)
    valor = 1000.0
    taxa_pre = 0.0

    pos_fixado = CalculoPosFixado(
        "ipca", EnumTipoContagemDias.uteis, defasagem_indice=0
    )
    pos_fixado.indice.get_taxa_diaria = mocker.Mock(return_value=0.0002700145)

    valor_atualizado = pos_fixado.calcula_valor_atualizado(
        valor, data_inicio, data_final, taxa_pre
    )

    assert valor_atualizado.valor == 1005.96


def test_calculo_pos_fixado_ipca_calcula_valor_atualizado_variacao_positiva_false(mocker):
    data_inicio = date(2022, 1, 1)
    data_final = date(2022, 2, 1)
    valor = 1000.0
    taxa_pre = 0.0

    pos_fixado = CalculoPosFixado('ipca', EnumTipoContagemDias.uteis, defasagem_indice=0, variacao_positiva=False)
    pos_fixado.indice.get_taxa_diaria = mocker.Mock(return_value=-0.0002700145)

    valor_atualizado = pos_fixado.calcula_valor_atualizado(valor, data_inicio, data_final, taxa_pre)

    assert valor_atualizado.valor == 994.08


def test_calculo_pos_fixado_ipca_calcula_valor_atualizado_variacao_positiva_true(mocker):
    data_inicio = date(2022, 1, 1)
    data_final = date(2022, 2, 1)
    valor = 1000.0
    taxa_pre = 0.0

    pos_fixado = CalculoPosFixado('ipca', EnumTipoContagemDias.uteis, defasagem_indice=0, variacao_positiva=True)
    pos_fixado.indice.get_taxa_diaria = mocker.Mock(return_value=-0.0002700145)

    valor_atualizado = pos_fixado.calcula_valor_atualizado(valor, data_inicio, data_final, taxa_pre)

    assert valor_atualizado.valor == 1000.0
