from unittest import mock

import pytest
import datetime as dt

from violeta.indices.indexador_base import IndexadorBase


indices = ['ipca', 'incc', 'igpm', 'cdi']


@pytest.mark.parametrize('indice', indices)
def test_indexador_base_get_index_values(indice):
    indexador = IndexadorBase(indice)
    data = dt.date(2022, 2, 22)

    with pytest.raises(NotImplementedError):
        indexador.get_index_values(data)


@pytest.mark.parametrize('indice', indices)
def test_indexador_base_get_index_values(indice):
    indexador = IndexadorBase(indice)

    with pytest.raises(NotImplementedError):
        indexador._retrieve_index_data()


@pytest.mark.parametrize('indice', indices)
def test_indexador_base__update_file(indice):
    indexador = IndexadorBase(indice)

    with pytest.raises(NotImplementedError):
        indexador._update_file()


@pytest.mark.parametrize('indice', indices)
def test_indexador_base__update_file(indice):
    indexador = IndexadorBase(indice)
    file_data = '{"some": "json_data"}'

    with mock.patch('builtins.open', mock.mock_open(read_data=file_data)):
        dados = indexador._get_file()

        assert dados == {'some': 'json_data'}
