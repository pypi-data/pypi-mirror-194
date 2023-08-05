import pandas as pd
import pytest
from math import isclose

from violeta.date_utils import dt
from violeta.exceptions import IndexadorInvalidoError
from violeta.pos_fixado.fator_acumulado import FatorAcumuladoIndexador, CalcularAniversarioDias

INDEXADORES = ['igpm', 'ipca', 'cdi']
INDEXADORES_NAO_IMPLEMENTADOS = ['selic', 'di', 'pre']
DATA_REF = dt.date(2020, 1, 15)
DATA_AQUISICAO = dt.date(2020, 1, 13)
DATA_VENCIMENTO = dt.date(2022, 8, 13)
VARIACAO_POSITIVA = True
DEFASAGEM = 2


def instancia_fator(indexador: str, data_ref=DATA_REF, defasagem=DEFASAGEM):
    FATOR = FatorAcumuladoIndexador(
        indexador,
        DATA_AQUISICAO,
        DATA_VENCIMENTO,
        data_ref,
        VARIACAO_POSITIVA,
        defasagem
    )
    return FATOR


@pytest.mark.parametrize("indexador", INDEXADORES_NAO_IMPLEMENTADOS, ids=INDEXADORES_NAO_IMPLEMENTADOS)
def test_indexador_nao_implementado(indexador):
    with pytest.raises(IndexadorInvalidoError):
        instancia_fator(indexador=indexador)


@pytest.mark.parametrize("indexador", INDEXADORES, ids=INDEXADORES)
def test_dia_aniversario(indexador):
    FATOR = instancia_fator(indexador=indexador)
    assert DATA_VENCIMENTO.day == FATOR.dia_aniversario


@pytest.mark.parametrize("indexador", INDEXADORES, ids=INDEXADORES)
def test_matriz_datas(indexador):
    COLUNA_OBRIGATORIA = ['DATA_ANIVERSARIO', 'DATA_DU_BASE', 'DATA_PROX_ANIVERSARIO', 'DATA_REF',
                          'DATA_REF_BASE', 'DATA_VIRADA', 'DU', 'DU_TOTAL', 'data_cessao',
                          'day_niver']
    FATOR = instancia_fator(indexador=indexador)
    matriz = FATOR._gerar_matriz()
    falta_colunas = set(COLUNA_OBRIGATORIA) - set(matriz.columns)
    assert not falta_colunas
    assert isinstance(matriz, pd.DataFrame)
    assert matriz['DU'][0] == 0


@pytest.mark.parametrize("indexador", INDEXADORES, ids=INDEXADORES)
def test_calculo_fator_acumulado(indexador):
    COLUNA_OBRIGATORIA = ['TAXA', 'FATOR', 'FATOR_ACUMULADO']
    FATOR = instancia_fator(indexador=indexador)
    matriz = FATOR._calcular_matriz()
    falta_colunas = set(COLUNA_OBRIGATORIA) - set(matriz.columns)
    assert not falta_colunas
    assert matriz['FATOR'][0] == 1
    assert matriz['FATOR_ACUMULADO'][0] == 1
    assert matriz.iloc[-1, :]['FATOR_ACUMULADO'] > matriz['FATOR_ACUMULADO'][0]


@pytest.mark.parametrize("indexador,taxa_defasagem2,taxa_defasagem3,taxa_defasagem4", 
                        [('igpm', 0.012440599999999999575, -0.00040643299999999998, 0.004770049999999), 
                        ('ipca', 0.0006997500, 0.0025002700, 0.0020995300)], 
                        ids=['ipgm', 'ipca'])
def test_taxa_indice(indexador, taxa_defasagem2, taxa_defasagem3, taxa_defasagem4):
    FATOR = instancia_fator(indexador=indexador)
    taxa_indice = FATOR.get_taxa_indice(dt.date(2020, 4, 15))
    assert isclose(taxa_indice, taxa_defasagem2, abs_tol=0.000001)
    FATOR = instancia_fator(indexador=indexador, defasagem=3)
    taxa_indice = FATOR.get_taxa_indice(dt.date(2020, 4, 15))
    assert isclose(taxa_indice, taxa_defasagem3, abs_tol=0.000001)
    FATOR = instancia_fator(indexador=indexador, defasagem=4)
    taxa_indice = FATOR.get_taxa_indice(dt.date(2020, 4, 15))
    assert isclose(taxa_indice, taxa_defasagem4, abs_tol=0.000001)


@pytest.mark.parametrize("indexador, fator_15012020, fator_15042020, fator_05052020", 
                        [('igpm', 1.00180185, 1.02705730, 1.03470462), ('ipca', 1.00099483, 1.01622962, 1.01665628)], 
                        ids=['ipgm', 'ipca'])
def test_get_fator_acumulado(indexador, fator_15012020, fator_15042020, fator_05052020):
    FATOR = instancia_fator(indexador=indexador)
    valor_fator = FATOR.fator_acumulado()
    assert isclose(valor_fator, fator_15012020)
    FATOR = instancia_fator(indexador=indexador, data_ref=dt.date(2020, 4, 15))
    valor_fator = FATOR.fator_acumulado()
    assert isclose(valor_fator, fator_15042020)
    FATOR = instancia_fator(indexador=indexador, data_ref=dt.date(2020, 5, 5))
    valor_fator = FATOR.fator_acumulado()
    assert isclose(valor_fator, fator_05052020)


def test_data_aniversario():
    data_ref = dt.date(2020, 1, 15)
    data_cessao = dt.date(2020, 1, 13)
    dia_aniversario = 13
    cal = CalcularAniversarioDias(data_ref, data_cessao, dia_aniversario)
    assert cal.DATA_ANIVERSARIO == dt.date(2020, 1, 13)
    assert cal.DATA_PROX_ANIVERSARIO == dt.date(2020, 2, 13)
    assert cal.DU == 2
    assert cal.DU_TOTAL == 23

    data_ref = dt.date(2020, 1, 8)
    data_cessao = dt.date(2020, 1, 2)
    dia_aniversario = 13
    cal = CalcularAniversarioDias(data_ref, data_cessao, dia_aniversario)
    assert cal.DATA_ANIVERSARIO == dt.date(2019, 12, 13)
    assert cal.DATA_PROX_ANIVERSARIO == dt.date(2020, 1, 13)
    assert cal.DU == 4
    assert cal.DU_TOTAL == 19
