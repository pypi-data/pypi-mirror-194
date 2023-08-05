from dataclasses import dataclass


@dataclass
class ValoresAtraso:
    """Representação de valores de um atraso"""
    juros_pre: float
    juros_pos: float
    multa: float = 0.0
    mora: float = 0.0

    def somatorio(self) -> float:
        return self.juros_pre + self.juros_pos + self.multa + self.mora
