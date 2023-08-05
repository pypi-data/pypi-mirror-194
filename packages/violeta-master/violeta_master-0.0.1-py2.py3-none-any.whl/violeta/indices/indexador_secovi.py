import re
import requests
import datetime as dt
import pandas as pd

from decimal import Decimal
from bs4 import BeautifulSoup

from violeta.exceptions import DataInvalidaError
from .indexador_base import IndexadorBase

_MES = {
    "jan": 1,
    "fev": 2,
    "mar": 3,
    "abr": 4,
    "mai": 5,
    "jun": 6,
    "jul": 7,
    "ago": 8,
    "set": 9,
    "out": 10,
    "nov": 11,
    "dez": 12,
}


class IndexadorSecovi(IndexadorBase):
    """
    Responsável por recuperar dados através do site da SECOVI
    Possui apenas dados de índices mensais
    """

    _url = "http://indiceseconomicos.secovi.com.br/indicadormensal.php"

    def __init__(self, indexador: str, codigo_indexador: int):
        super().__init__(indexador)
        self.indexador = indexador
        self.codigo_indexador = codigo_indexador
        self._set_url_consulta()

    def _set_url_consulta(self):
        self._url = f"{self._url}?idindicador={self.codigo_indexador}"

    def _string_to_decimal(self, valor: str):
        try:
            x = re.search(r"([\-]*\d+[,|\.]\d*)", valor)
            return Decimal(valor[x.start() : x.end()].replace(",", "."))
        except Exception:
            valor = None
        return valor

    def _month_to_int(self, mes_string: str) -> int:
        return _MES[mes_string.lower()]

    def _int_to_month(self, mes: int) -> str:
        for m in _MES:
            if _MES[m] is mes:
                return m

    def _retrieve_index_data(self) -> dict:
        resp = requests.get(self._url)
        soup = BeautifulSoup(resp.content, "html.parser")
        tds = soup.find_all("td")
        dados = {}
        indice_ant = 1
        for i, td in enumerate(tds):
            valor = td.text
            if valor.find("Ano:") > -1:
                ano = valor.replace("Ano: ", "")
                dados[ano] = {}

            class_value = td.get("class") if td.get("class") else []
            if "borderLeft" in class_value:
                indice = Decimal(tds[i + 1].text.replace(".", "").replace(",", "."))
                dados[ano][valor] = {
                    "indice": indice,
                    "variacao": self._string_to_decimal(tds[i + 2].text),
                    "variacao_calculada": (indice / indice_ant) - 1,
                    "ano": int(ano),
                    "mes": self._month_to_int(valor),
                }
                indice_ant = indice
        return dados

    def _consultar(self, data_ref: dt.date) -> dict:
        dados = self._get_file()
        df = pd.DataFrame(dados)
        mes = self._int_to_month(data_ref.month)
        ano = data_ref.year
        valor = df.filter(like=mes.upper(), axis=0)[str(ano)][-1]
        return valor

    def get_index_values(self, data_ref: dt.date) -> dict:
        valor = self._consultar(data_ref)
        if not isinstance(valor, dict):
            self._update_file()
            valor = self._consultar(data_ref)

        if data_ref <= dt.date.today() and valor is None:
            self._update_file()
            valor = self._consultar(data_ref)

        if not isinstance(valor, dict):
            raise DataInvalidaError(
                f"Nao foi encontrado indice {self.indexador} para {data_ref}"
            )
        return valor
