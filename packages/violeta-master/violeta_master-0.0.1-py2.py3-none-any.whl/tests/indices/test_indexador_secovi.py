import json
from datetime import date
from decimal import Decimal
from unittest import mock

import pytest

from violeta.exceptions import DataInvalidaError
from violeta.indices.indexador import Indexador
from violeta.indices.indexador_secovi import IndexadorSecovi


@pytest.fixture
def index_value():
    indice = 6412.880
    taxa_indice = 0.00470007
    variacao = 0.47
    data = date(2022, 5, 22)

    return {
        "indice": indice,
        "variacao": variacao,
        "variacao_calculada": taxa_indice,
        "ano": data.year,
        "mes": data.month
    }


@pytest.fixture
def indice():
    return 'ipca'


@pytest.fixture
def codigo():
    return 61


def test_indexador_secovi_success(indice):
    indexador = Indexador(indice)

    assert isinstance(indexador.indexador, IndexadorSecovi)


def test_indexador_secovi_get_index_values(indice, codigo, index_value):
    indexador = IndexadorSecovi(indice, codigo)
    indices_data = json.dumps({"2022": {"MAI": index_value}})

    with mock.patch('violeta.indices.indexador_base.open', mock.mock_open(read_data=indices_data)):
        data = date(2022, 5, 22)
        indice = indexador.get_index_values(data)

        assert indice == index_value


def test_indexador_secovi_get_index_values_retrieve_data(mocker, indice, codigo, index_value):
    indexador = IndexadorSecovi(indice, codigo)
    indices_data = {"2022": {"MAI": index_value}}
    mock_response = mocker.MagicMock()
    mock_response.content = b'<html></html>'

    with mock.patch('violeta.indices.indexador_base.open', create=True) as mock_open:
        mock_context = mocker.MagicMock()
        mock_context.__exit__.return_value = False
        mock_open.side_effect = [FileNotFoundError, mock_context]

        with mock.patch.object(indexador, '_retrieve_index_data', return_value=indices_data) as retrive_index_data:
            data = date(2022, 5, 22)
            indice = indexador.get_index_values(data)

            assert indice == index_value
            retrive_index_data.assert_called()


def test_indexador_secovi_get_index_values_bad_date(indice, codigo, index_value):
    indexador = IndexadorSecovi(indice, codigo)
    indices_data = json.dumps({"2022": {"MAI": index_value, "JUN": 1}})

    with mock.patch('violeta.indices.indexador_base.open', mock.mock_open(read_data=indices_data)):
        with pytest.raises(DataInvalidaError):
            data_no_futuro = date(2022, 6, 1)
            indexador.get_index_values(data_no_futuro)


def test_indexador_secovi_consultar(indice, codigo, index_value):
    indexador = IndexadorSecovi(indice, codigo)
    indices_data = json.dumps({"2022": {"MAI": index_value}})
    
    mock.patch.object(indexador, '_get_file', return_value=indices_data)

    data = date(2022, 5, 22)
    valor = indexador._consultar(data)

    assert valor == index_value


@pytest.mark.parametrize('mes_str, mes_int', [("jan", 1), ("fev", 2), ("mar", 3), ("abr", 4), ("mai", 5), ("jun", 6), 
                                              ("jul", 7), ("ago", 8), ("set", 9), ("out", 10), ("nov", 11), ("dez", 12)])
def test_indexador_secovi_int_to_month(indice, codigo, mes_str, mes_int):
    indexador = IndexadorSecovi(indice, codigo)

    result = indexador._int_to_month(mes_int)

    assert result == mes_str


@pytest.mark.parametrize('mes_str, mes_int', [("jan", 1), ("fev", 2), ("mar", 3), ("abr", 4), ("mai", 5), ("jun", 6), 
                                              ("jul", 7), ("ago", 8), ("set", 9), ("out", 10), ("nov", 11), ("dez", 12)])
def test_indexador_secovi_month_to_int(indice, codigo, mes_str, mes_int):
    indexador = IndexadorSecovi(indice, codigo)

    result = indexador._month_to_int(mes_str)

    assert result == mes_int


@pytest.mark.parametrize('valor_str, valor_decimal', [("-1,05%", Decimal('-1.05')), ("0,47%", Decimal('0.47')), ("6315,880", Decimal('6315.880'))])
def test_indexador_secovi_string_to_decimal(indice, codigo, valor_str, valor_decimal):
    indexador = IndexadorSecovi(indice, codigo)

    result = indexador._string_to_decimal(valor_str)

    assert result == valor_decimal


def test_indexador_secovi_set_url_consulta(indice, codigo):
    indexador = IndexadorSecovi(indice, codigo)

    assert indexador._url == "http://indiceseconomicos.secovi.com.br/indicadormensal.php?idindicador=61"
