from violeta.calc import valor_juros_moratorios, valor_multa_moratoria
from violeta.constantes import EnumTipoJuros, EnumTipoContagemDias

def test_juros_simples_moratorios_du_e_dc():
    """"
        segunda a sexta para juros simples, dias uteis e dias corridos mesmo periodo
    """
    VALOR_BASE = 1000
    DATA_INICIAL = '2020-08-03'
    DATA_FINAL = '2020-08-07'
    TAXA_AO_MES = 2
    VALOR_ESPERADO_JUROS_SIMPLES_DC = 3.81
    VALOR_ESPERADO_JUROS_SIMPLES_DU = 2.67

    valor_calculado = valor_juros_moratorios(VALOR_BASE,
                                             DATA_INICIAL,
                                             DATA_FINAL,
                                             EnumTipoContagemDias.uteis,
                                             TAXA_AO_MES,
                                             EnumTipoJuros.simples)

    assert valor_calculado == VALOR_ESPERADO_JUROS_SIMPLES_DC

    valor_calculado = valor_juros_moratorios(VALOR_BASE,
                                             DATA_INICIAL,
                                             DATA_FINAL,
                                             EnumTipoContagemDias.corridos,
                                             TAXA_AO_MES,
                                             EnumTipoJuros.simples)

    assert valor_calculado == VALOR_ESPERADO_JUROS_SIMPLES_DU


def test_juros_simples_moratorios_du_e_dc_zerados():
    """"
        segunda a sexta para juros simples, dias uteis e dias corridos mesmo periodo
    """
    VALOR_BASE = 1000
    DATA_INICIAL = '2020-08-03'
    DATA_FINAL = '2020-08-03'
    TAXA_AO_MES = 2
    VALOR_ESPERADO_JUROS_SIMPLES_DC = 0.00
    VALOR_ESPERADO_JUROS_SIMPLES_DU = 0.00

    valor_calculado = valor_juros_moratorios(VALOR_BASE,
                                             DATA_INICIAL,
                                             DATA_FINAL,
                                             EnumTipoContagemDias.uteis,
                                             TAXA_AO_MES,
                                             EnumTipoJuros.simples)

    assert valor_calculado == VALOR_ESPERADO_JUROS_SIMPLES_DC

    valor_calculado = valor_juros_moratorios(VALOR_BASE,
                                             DATA_INICIAL,
                                             DATA_FINAL,
                                             EnumTipoContagemDias.corridos,
                                             TAXA_AO_MES,
                                             EnumTipoJuros.simples)

    assert valor_calculado == VALOR_ESPERADO_JUROS_SIMPLES_DU

def test_juros_composto_moratorios_du_e_dc():
    """"
        segunda a sexta para juros composto, dias uteis e dias corridos mesmo periodo
    """
    VALOR_BASE = 1000
    DATA_INICIAL = '2020-08-03'
    DATA_FINAL = '2020-08-07'
    TAXA_AO_MES = 2
    VALOR_ESPERADO_JUROS_COMPOSTO_DC = 3.78
    VALOR_ESPERADO_JUROS_COMPOSTO_DU = 2.64

    valor_calculado = valor_juros_moratorios(VALOR_BASE,
                                             DATA_INICIAL,
                                             DATA_FINAL,
                                             EnumTipoContagemDias.uteis,
                                             TAXA_AO_MES,
                                             EnumTipoJuros.composto)

    assert valor_calculado == VALOR_ESPERADO_JUROS_COMPOSTO_DC

    valor_calculado = valor_juros_moratorios(VALOR_BASE,
                                             DATA_INICIAL,
                                             DATA_FINAL,
                                             EnumTipoContagemDias.corridos,
                                             TAXA_AO_MES,
                                             EnumTipoJuros.composto)

    assert valor_calculado == VALOR_ESPERADO_JUROS_COMPOSTO_DU


def test_juros_composto_com_juros_aberto_moratorios_du_e_dc():
    """"
        segunda a sexta para juros composto, dias uteis e dias corridos mesmo periodo
    """
    VALOR_BASE = 1000
    DATA_INICIAL = '2020-08-03'
    DATA_FINAL = '2020-08-07'
    TAXA_AO_MES = 2
    VALOR_ESPERADO_JUROS_COMPOSTO_DC = 4.16
    VALOR_ESPERADO_JUROS_COMPOSTO_DU = 2.91

    valor_calculado = valor_juros_moratorios(VALOR_BASE,
                                             DATA_INICIAL,
                                             DATA_FINAL,
                                             EnumTipoContagemDias.uteis,
                                             TAXA_AO_MES,
                                             EnumTipoJuros.composto,
                                             100.0)

    assert valor_calculado == VALOR_ESPERADO_JUROS_COMPOSTO_DC

    valor_calculado = valor_juros_moratorios(VALOR_BASE,
                                             DATA_INICIAL,
                                             DATA_FINAL,
                                             EnumTipoContagemDias.corridos,
                                             TAXA_AO_MES,
                                             EnumTipoJuros.composto,
                                             100.0)

    assert valor_calculado == VALOR_ESPERADO_JUROS_COMPOSTO_DU


def test_juros_composto_moratorios_du_e_dc_zerados():
    """"
        segunda a sexta para juros composto, dias uteis e dias corridos mesmo periodo
    """
    VALOR_BASE = 1000
    DATA_INICIAL = '2020-08-03'
    DATA_FINAL = '2020-08-03'
    TAXA_AO_MES = 2
    VALOR_ESPERADO_JUROS_COMPOSTO_DC = 0.00
    VALOR_ESPERADO_JUROS_COMPOSTO_DU = 0.00

    valor_calculado = valor_juros_moratorios(VALOR_BASE,
                                             DATA_INICIAL,
                                             DATA_FINAL,
                                             EnumTipoContagemDias.uteis,
                                             TAXA_AO_MES,
                                             EnumTipoJuros.composto)

    assert valor_calculado == VALOR_ESPERADO_JUROS_COMPOSTO_DC

    valor_calculado = valor_juros_moratorios(VALOR_BASE,
                                             DATA_INICIAL,
                                             DATA_FINAL,
                                             EnumTipoContagemDias.corridos,
                                             TAXA_AO_MES,
                                             EnumTipoJuros.composto)

    assert valor_calculado == VALOR_ESPERADO_JUROS_COMPOSTO_DU

def test_juros_composto_moratorios_du_e_dc_pagamento_antecipado():
    """"
        segunda a sexta para juros composto, dias uteis e dias corridos mesmo periodo
    """
    VALOR_BASE = 1000
    DATA_INICIAL = '2020-08-04'
    DATA_FINAL = '2020-08-03'
    TAXA_AO_MES = 2
    VALOR_ESPERADO_JUROS_COMPOSTO_DC = 0.00
    VALOR_ESPERADO_JUROS_COMPOSTO_DU = 0.00

    valor_calculado = valor_juros_moratorios(VALOR_BASE,
                                             DATA_INICIAL,
                                             DATA_FINAL,
                                             EnumTipoContagemDias.uteis,
                                             TAXA_AO_MES,
                                             EnumTipoJuros.composto)

    assert valor_calculado == VALOR_ESPERADO_JUROS_COMPOSTO_DC

    valor_calculado = valor_juros_moratorios(VALOR_BASE,
                                             DATA_INICIAL,
                                             DATA_FINAL,
                                             EnumTipoContagemDias.corridos,
                                             TAXA_AO_MES,
                                             EnumTipoJuros.composto)

    assert valor_calculado == VALOR_ESPERADO_JUROS_COMPOSTO_DU


def test_juros_simples_moratorios_du_e_dc_pagamento_antecipado():
    """"
        segunda a sexta para juros simples, dias uteis e dias corridos mesmo periodo
    """
    VALOR_BASE = 1000
    DATA_INICIAL = '2020-08-04'
    DATA_FINAL = '2020-08-03'
    TAXA_AO_MES = 2
    VALOR_ESPERADO_JUROS_SIMPLES_DC = 0.00
    VALOR_ESPERADO_JUROS_SIMPLES_DU = 0.00

    valor_calculado = valor_juros_moratorios(VALOR_BASE,
                                             DATA_INICIAL,
                                             DATA_FINAL,
                                             EnumTipoContagemDias.uteis,
                                             TAXA_AO_MES,
                                             EnumTipoJuros.simples)

    assert valor_calculado == VALOR_ESPERADO_JUROS_SIMPLES_DC

    valor_calculado = valor_juros_moratorios(VALOR_BASE,
                                             DATA_INICIAL,
                                             DATA_FINAL,
                                             EnumTipoContagemDias.corridos,
                                             TAXA_AO_MES,
                                             EnumTipoJuros.simples)

    assert valor_calculado == VALOR_ESPERADO_JUROS_SIMPLES_DU