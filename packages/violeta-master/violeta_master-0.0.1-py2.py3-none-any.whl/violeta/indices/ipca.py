from .indexador_secovi import IndexadorSecovi
from .indexador_mensal import IndexadorMensal


class IndexadorIPCA(IndexadorMensal, IndexadorSecovi):
    """
    Classe responsável por recuperar valores mensais de IPCA
    através do site da Secovi
    """

    def __init__(self):
        super().__init__(indexador="ipca", codigo_indexador=61)
