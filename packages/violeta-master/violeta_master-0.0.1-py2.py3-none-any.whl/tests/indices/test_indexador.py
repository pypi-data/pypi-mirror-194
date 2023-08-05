import pytest
import datetime as dt

from violeta.exceptions import IndexadorInvalidoError
from violeta.indices.indexador import Indexador


@pytest.fixture()
def index_value(taxa_indice=0.07, variacao=0.13, data=dt.date(2021, 1, 10)):
    return {
        "indice": taxa_indice,
        "variacao": variacao,
        "variacao_calculada": (taxa_indice / taxa_indice) - 1,
        "ano": data.year,
        "mes": data.month,
        "dia": data.day,
    }


@pytest.mark.parametrize('indice', ['ipca', 'incc', 'igpm', 'cdi'])
def test_indexador_success(indice):
    indexador = Indexador(indice)
    assert isinstance(indexador, Indexador)


def test_indexador_failure():
    indice_desconhecido = 'ABC'

    with pytest.raises(IndexadorInvalidoError):
        Indexador(indice_desconhecido)


@pytest.mark.parametrize('indice', ['ipca', 'incc', 'igpm', 'cdi'])
def test_indexador_get_valor(mocker, indice, index_value):
    indexador = Indexador(indice)

    mock_indexador = mocker.MagicMock()
    mock_indexador.get_index_values.return_value = index_value
    indexador.indexador = mock_indexador

    data = dt.date(2022, 2, 22)
    assert indexador.get_valor(data) == index_value
