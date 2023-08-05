import datetime as dt

from violeta.exceptions import IndexadorInvalidoError

from .cdi import IndexadorCDI
from .igpm import IndexadorIGPM
from .incc import IndexadorINCC
from .ipca import IndexadorIPCA


class Indexador:
    """
    Responsável por criar o objeto apropriado baseado no indexador pedido
    """

    indexadores = {
        "ipca": IndexadorIPCA,
        "igpm": IndexadorIGPM,
        "incc": IndexadorINCC,
        "cdi": IndexadorCDI,
    }

    def __init__(self, indexador: str):
        if indexador not in self.indexadores:
            raise IndexadorInvalidoError(f"Indexador desconhecido {indexador}")
        self.indexador = self.indexadores[indexador]()

    def get_valor(self, data_ref: dt.date) -> dict:
        return self.indexador.get_index_values(data_ref)

    def get_taxa_diaria(self, data: dt.date, meses_defasagem: int = 0) -> float:
        return self.indexador.get_daily_value(data, meses_defasagem)
