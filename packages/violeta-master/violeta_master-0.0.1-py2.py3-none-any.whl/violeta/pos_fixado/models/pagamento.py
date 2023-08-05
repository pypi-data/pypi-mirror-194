from datetime import date

from dataclasses import dataclass

from .valores_atraso import ValoresAtraso


@dataclass
class Pagamento:
    """Representação de um pagamento/liquidação"""
    valor: float
    data: date
    pmt: int
    atraso_multa: float = 0.0
    atraso_mora: float = 0.0
    atraso_juros_pre: float = 0.0
    atraso_juros_pos: float = 0.0

    def adiciona_atraso(self, valores_atraso: ValoresAtraso, aplica_multa: bool):
        if aplica_multa:
            self.atraso_multa = valores_atraso.multa
        self.atraso_mora = valores_atraso.mora
        self.atraso_juros_pre = valores_atraso.juros_pre
        self.atraso_juros_pos = valores_atraso.juros_pos
