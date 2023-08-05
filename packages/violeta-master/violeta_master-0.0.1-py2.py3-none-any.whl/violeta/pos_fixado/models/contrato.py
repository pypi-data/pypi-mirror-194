from datetime import date
from typing import List, Dict

from dataclasses import dataclass

from violeta.constantes import EnumTipoIndexador, EnumTipoAmortizacao, EnumTipoContagemDias
from violeta.date_utils import next_bizday, adjust_next_bizdays
from violeta.exceptions import PagamentoInvalidoError

from .pagamento import Pagamento
from .parcela import Parcela
from .valores_atraso import ValoresAtraso
from ..calculo import CalculoPosFixado


@dataclass
class Contrato:
    """
    Representação de um contrato pós-fixado
    """
    def __init__(self, valor_titulo: float, data_emissao: date, indice: EnumTipoIndexador,
                 tipo_amortizacao: EnumTipoAmortizacao, taxa_pre_anual: float, multa: float,
                 tipo_contagem_multa: EnumTipoContagemDias, mora: float, datas_parcelas: List[date],
                 data_referencia: date = None):
        self.valor_titulo = valor_titulo
        self.data_emissao = data_emissao
        self.indice = indice
        self.calculador = CalculoPosFixado(indice.value, EnumTipoContagemDias.uteis)
        self.tipo_amortizacao = tipo_amortizacao
        self.taxa_pre_anual = taxa_pre_anual
        self.multa = multa
        self.tipo_contagem_multa = tipo_contagem_multa
        self.mora = mora
        self.parcelas = self._generate_parcelas(valor_titulo, data_emissao, datas_parcelas, tipo_amortizacao)

        self.atualiza_parcelas(data_referencia)

    def _get_parcelas_anteriores(self, parcela_referencia: Parcela) -> List[Parcela]:
        parcelas_anteriores = []

        for pmt, parcela in self.parcelas.items():
            if pmt < parcela_referencia.pmt:
                parcelas_anteriores.append(parcela)

        return parcelas_anteriores

    def _get_amortizacao_total(self, parcela: Parcela) -> float:
        parcelas_anteriores = self._get_parcelas_anteriores(parcela)

        amortizacao_total = 0.0
        for parcela_anterior in parcelas_anteriores:
            amortizacao_total += parcela_anterior.amortizacao

        return amortizacao_total

    def atualiza_parcelas(self, data_referencia: date = None):
        if data_referencia is None:
            data_referencia = date.today()

        for parcela in self.parcelas.values():
            saldo_devedor = self.valor_titulo - self._get_amortizacao_total(parcela)
            parcela.atualiza_parcela(data_referencia, saldo_devedor, self.taxa_pre_anual, self.multa, self.mora, self.calculador)

    def adiciona_pagamento(self, pagamento: Pagamento):
        if pagamento.pmt not in self.parcelas.keys():
            raise PagamentoInvalidoError(f"Pagamento para pmt {pagamento.pmt} inexistente")

        parcela = self.parcelas[pagamento.pmt]

        if parcela.is_vencida(pagamento.data):
            juros_e_multa = self._calcula_juros_multa_atraso(parcela, data_atraso=pagamento.data)
            pagamento.adiciona_atraso(juros_e_multa, aplica_multa=parcela.cobrar_multa(pagamento.data))

        parcela.adiciona_pagamento(pagamento)

    def _calcula_juros_multa_atraso(self, parcela: Parcela, data_atraso: date) -> ValoresAtraso:
        valores_atraso = self.calculador.calcula_valor_atualizado(valor=parcela.valor_aberto,
                                                                  data_inicio=parcela.data_ajustada,
                                                                  data_final=data_atraso,
                                                                  taxa_pre_anual=self.taxa_pre_anual)
        return ValoresAtraso(juros_pre=valores_atraso.juros_pre,
                             juros_pos=valores_atraso.juros_pos,
                             mora=valores_atraso.valor * self.mora,
                             multa=parcela.valor_nominal * self.multa)

    def get_valor_devido(self) -> float:
        valor_devido = 0.0

        for parcela in self.parcelas.values():
            valor_devido += parcela.valor_aberto

        return valor_devido

    @staticmethod
    def _generate_parcelas(valor_titulo: float, data_emissao: date, datas_vencimento: List[date],
                           tipo_amortizacao: EnumTipoAmortizacao) -> Dict[int, Parcela]:
        if tipo_amortizacao == EnumTipoAmortizacao.sac:
            return Contrato._generate_parcelas_sac(valor_titulo, data_emissao, datas_vencimento)

        raise NotImplementedError("Apenas tabela de amortização SAC implementada")

    @staticmethod
    def _generate_parcelas_sac(valor_titulo: float, data_emissao: date, datas_vencimento: List[date]) -> Dict[
        int, Parcela]:
        quantidade_parcelas = len(datas_vencimento)
        amortizacao_por_parcela = round(valor_titulo / quantidade_parcelas, 2)

        data_inicio = data_emissao

        parcelas = {}
        for index, data in enumerate(datas_vencimento, start=1):
            data_vencimento = next_bizday(data)

            parcelas[index] = Parcela(
                pmt=index,
                data_inicio=adjust_next_bizdays(data_inicio),
                data_vencimento=data,
                data_ajustada=data_vencimento,
                amortizacao=amortizacao_por_parcela,
                valor_nominal=amortizacao_por_parcela,
                valor_aberto=amortizacao_por_parcela
            )

            data_inicio = data_vencimento

        return parcelas


if __name__ == "__main__":
    data_emissao = date(2022, 1, 13)

    datas_parcelas = [
        date(2022, 2, 12),
        date(2022, 3, 12),
        date(2022, 4, 12),
        date(2022, 5, 12),
        date(2022, 6, 12),
        date(2022, 7, 12),
        date(2022, 8, 12),
        date(2022, 9, 12),
        date(2022, 10, 12),
        date(2022, 11, 12),
        date(2022, 12, 12),
        date(2023, 1, 12),
        date(2023, 2, 12),
        date(2023, 3, 12),
        date(2023, 4, 12),
        date(2023, 5, 12),
        date(2023, 6, 12),
        date(2023, 7, 12)
    ]
    valor_titulo = 21_000_000.00
    taxa_pre_anual = 0.1
    mora = 0.01
    multa = 0.02

    data_referencia = date(2022, 6, 23)

    contrato = Contrato(valor_titulo, data_emissao, EnumTipoIndexador.cdi, EnumTipoAmortizacao.sac,
                        taxa_pre_anual, datas_parcelas=datas_parcelas, mora=mora, multa=multa,
                        tipo_contagem_multa=EnumTipoContagemDias.uteis, data_referencia=data_referencia)
    print(contrato)
    print(contrato.parcelas)

    data = date(2022, 5, 12)

    for i in range(1, 9):
        print(contrato.parcelas[i])

    contrato.adiciona_pagamento(Pagamento(data=date(2022, 2, 14), valor=1_513_853.73, pmt=1))
    contrato.adiciona_pagamento(Pagamento(data=date(2022, 3, 14), valor=1_447_023.42, pmt=2))
    contrato.adiciona_pagamento(Pagamento(data=date(2022, 4, 12), valor=1_487_743.82, pmt=3))
    contrato.adiciona_pagamento(Pagamento(data=date(2022, 5, 12), valor=1_458_212.16, pmt=4))
    contrato.adiciona_pagamento(Pagamento(data=date(2022, 6, 12), valor=1_475_300.73, pmt=5))

    print(contrato.get_valor_devido())
