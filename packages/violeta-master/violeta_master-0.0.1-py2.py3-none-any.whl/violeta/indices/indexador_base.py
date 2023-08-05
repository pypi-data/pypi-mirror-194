import datetime as dt, tempfile
from functools import lru_cache

import simplejson as json

from violeta import PACKAGE_DIR


class IndexadorBase:
    """
    Responsável por unificar método de persistência dos indexadores.
    Fica a cargo de cada índice implementar como e onde recuperar os dados atualizados
    """

    _dir = f"{PACKAGE_DIR}/docs/"

    def __init__(self, indexador: str):
        self.indexador = indexador
        self._filename = f"{self._dir}{self.indexador}.json"

    def get_index_values(self, data_ref: dt.date) -> dict:
        raise NotImplementedError

    def get_daily_value(self, data: dt.date, meses_defasagem: int) -> dict:
        raise NotImplementedError

    def _retrieve_index_data(self) -> dict:
        raise NotImplementedError

    def _update_file(self) -> str:
        dados = json.dumps(self._retrieve_index_data())
        if self._get_file.cache_info() is not None:
            self._get_file.cache_clear()

        with tempfile.TemporaryFile(
            mode="w",
            dir=self._dir,
            prefix=self.indexador,
            suffix=".json",
        ) as fp:
            fp.write(dados)
        return dados

    @lru_cache(maxsize=32)
    def _get_file(self) -> dict:
        try:
            with open(self._filename, "r") as f:
                dados = f.read()
        except FileNotFoundError:
            dados = self._update_file()

        return json.loads(dados)
