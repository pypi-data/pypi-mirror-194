class VioletaException(Exception):
    def __init__(self, msg=None):
        self.msg = msg


class CalculoPosFixadoError(VioletaException):
    message = "Erro ao realizar cálculo pós-fixado"

    def __init__(self, custom_message, *args, **kwargs):
        self.custom_message = custom_message
        super().__init__(*args, **kwargs)

    def __str__(self):
        return f"{self.msg or self.message}. Erro: {self.custom_message}"


class DataInvalidaError(CalculoPosFixadoError):
    message = "Data inválida para cálculo"


class IndexadorInvalidoError(CalculoPosFixadoError):
    message = "Indexador inexistente para cálculo"


class IntegracaoExternaError(CalculoPosFixadoError):
    message = "Falha ao recuperar dados externos"


class PagamentoInvalidoError(CalculoPosFixadoError):
    message = "Pagamento inválido para ser processado"
