from .indexador_secovi import IndexadorSecovi
from .indexador_mensal import IndexadorMensal


class IndexadorINCC(IndexadorMensal, IndexadorSecovi):
    """
    Classe responsável por recuperar valores mensais de INCC
    através do site da Secovi
    """

    def __init__(self):
        super().__init__(indexador="incc", codigo_indexador=59)
