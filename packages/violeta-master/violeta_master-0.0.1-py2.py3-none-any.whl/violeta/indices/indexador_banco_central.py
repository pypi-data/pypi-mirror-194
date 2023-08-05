import datetime as dt

import requests

from violeta.exceptions import IntegracaoExternaError, DataInvalidaError
from .indexador_base import IndexadorBase


class IndexadorBancoCentral(IndexadorBase):
    """
    Responsável por recuperar dados de índices através da API do Banco Central
    """

    _url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs"

    def __init__(self, indexador: str, codigo_indexador: int):
        super().__init__(indexador)
        self.indexador = indexador
        self.codigo_indexador = codigo_indexador
        self._set_url_consulta()
        self._timeout_seconds = 10

    def _set_url_consulta(self):
        self._url = f"{self._url}.{self.codigo_indexador}/dados"

    def _retrieve_index_data(self) -> dict:
        response = requests.get(
            self._url, params={"formato": "json"}, timeout=self._timeout_seconds
        )
        if not response:
            raise IntegracaoExternaError(response)

        try:
            indices = response.json()
        except:
            raise IntegracaoExternaError(
                "O formato dos dados retornado pela API do Banco Central é inválido"
            )

        return self._build_persistence_dict(indices)

    def _build_persistence_dict(self, indices: dict) -> dict:
        indices_por_data = {}

        indice_anterior = 1.0
        for indice in indices:
            data_indice = dt.datetime.strptime(indice["data"], "%d/%m/%Y").date()
            taxa_indice_diaria = float(indice["valor"])

            indices_por_data[data_indice.isoformat()] = {
                "indice": taxa_indice_diaria,
                "variacao": taxa_indice_diaria / indice_anterior,
                "variacao_calculada": taxa_indice_diaria,  ## não é necessário calcular, já que esse índice é diario
                "ano": data_indice.year,
                "mes": data_indice.month,
                "dia": data_indice.day,
            }

            indice_anterior = taxa_indice_diaria

        return indices_por_data

    def get_index_values(self, data: dt.date) -> dict:
        valor = self._get_index_from_file(data)

        if data <= dt.date.today() and valor is None:
            self._update_file()
            valor = self._get_index_from_file(data)

        if valor is None:
            raise DataInvalidaError(
                f"Nao foi encontrado indice {self.indexador} para {data}"
            )

        return valor

    def _get_index_from_file(self, data: dt.date) -> dict:
        dados = self._get_file()
        return dados.get(data.isoformat(), None)
