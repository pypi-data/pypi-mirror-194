from .indexador_secovi import IndexadorSecovi
from .indexador_mensal import IndexadorMensal


class IndexadorIGPM(IndexadorMensal, IndexadorSecovi):
    """
    Classe responsável por recuperar valores mensais de IGPM
    através do site da Secovi
    """

    def __init__(self):
        super().__init__(indexador="igpm", codigo_indexador=58)
