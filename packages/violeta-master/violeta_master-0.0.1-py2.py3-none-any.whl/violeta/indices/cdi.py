from .indexador_banco_central import IndexadorBancoCentral
from .indexador_diario import IndexadorDiario


class IndexadorCDI(IndexadorDiario, IndexadorBancoCentral):
    """
    Classe responsável por recuperar valores diários de CDI
    através da API do Banco Central
    """

    def __init__(self):
        super().__init__(indexador="cdi", codigo_indexador=12)
