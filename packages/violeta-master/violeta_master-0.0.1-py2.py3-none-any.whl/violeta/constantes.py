from enum import Enum


class EnumTipoContagemDias(Enum):
    uteis = 21
    corridos = 30


class EnumTipoJuros(Enum):
    simples = 'simples'
    composto = 'composto'


class EnumTipoIndexador(Enum):
    ipca = 'ipca'
    igpm = 'igpm'
    incc = 'incc'
    cdi = 'cdi'


class EnumTipoAmortizacao(Enum):
    sac = 'sac'
    price = 'price'
