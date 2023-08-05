import json
from unittest import mock

import pytest
import datetime as dt

from violeta.exceptions import DataInvalidaError, IntegracaoExternaError
from violeta.indices.indexador_banco_central import IndexadorBancoCentral


def index_value(taxa_indice=0.075139, variacao=0.13, data=dt.date(2022, 2, 22)):
    return {
        "indice": taxa_indice,
        "variacao": variacao,
        "variacao_calculada": taxa_indice,
        "ano": data.year,
        "mes": data.month,
        "dia": data.day,
    }


indices = [("cdi", 12)]


@pytest.mark.parametrize("indice,codigo", indices)
def test_indexador_banco_central_success(indice, codigo):
    indexador = IndexadorBancoCentral(indice, codigo)

    assert isinstance(indexador, IndexadorBancoCentral)


@pytest.mark.parametrize("indice,codigo", indices)
def test_indexador_banco_central_get_index_values(indice, codigo):
    indexador = IndexadorBancoCentral(indice, codigo)
    expected_index = index_value(variacao=0.075139)
    indices_data = json.dumps({"2022-02-22": expected_index})

    with mock.patch(
        "violeta.indices.indexador_base.open", mock.mock_open(read_data=indices_data)
    ):
        data = dt.date(2022, 2, 22)
        indice = indexador.get_index_values(data)

        assert indice == expected_index


@pytest.mark.parametrize("indice,codigo", indices)
def test_indexador_banco_central_get_index_values_retrieve_data(mocker, indice, codigo):
    indexador = IndexadorBancoCentral(indice, codigo)
    indices_data = [{"data": "22/02/2022", "valor": "0.075139"}]
    mock_response = mocker.MagicMock()
    mock_response.json.return_value = indices_data

    with mock.patch("violeta.indices.indexador_base.open", create=True) as mock_open:
        mock_context = mocker.MagicMock()
        mock_context.__enter__.return_value = mocker.MagicMock()
        mock_context.__exit__.return_value = False
        mock_open.side_effect = [FileNotFoundError, mock_context]

        with mock.patch("requests.get", return_value=mock_response) as request:
            data = dt.date(2022, 2, 22)
            indice = indexador.get_index_values(data)

            assert indice == index_value(variacao=0.075139)
            request.assert_called()


@pytest.mark.parametrize("indice,codigo", indices)
def test_indexador_banco_central_get_index_values_failed_retrieval(
    mocker, indice, codigo
):
    indexador = IndexadorBancoCentral(indice, codigo)

    mocker.patch("violeta.indices.indexador_base.open", side_effect=FileNotFoundError)

    with pytest.raises(IntegracaoExternaError):
        with mock.patch("requests.get", return_value=False):
            data = dt.date(2022, 2, 22)
            indexador.get_index_values(data)


@pytest.mark.parametrize("indice,codigo", indices)
def test_indexador_banco_central_get_index_values_bad_date(indice, codigo):
    indexador = IndexadorBancoCentral(indice, codigo)
    indices_data = b"""[{'data': '22/02/2022', 'valor': '0.075139'}]"""
    mock.patch("builtins.open", mock.mock_open(read_data=indices_data))

    with pytest.raises(DataInvalidaError):
        data_no_futuro = dt.date(2030, 1, 1)
        indexador.get_index_values(data_no_futuro)


@pytest.mark.parametrize("indice,codigo", indices)
def test_indexador_banco_central_invalid_data_response(indice, codigo):
    indexador_bc = IndexadorBancoCentral(indexador='cdi', codigo_indexador=999999999)
    with pytest.raises(IntegracaoExternaError):
        indexador_bc._retrieve_index_data()
