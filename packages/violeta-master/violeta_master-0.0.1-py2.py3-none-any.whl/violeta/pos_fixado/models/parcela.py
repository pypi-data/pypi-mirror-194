import datetime
from datetime import date
from typing import List

from dataclasses import dataclass, field

from violeta.date_utils import prev_bizday, adjust_next_bizdays

from .pagamento import Pagamento
from ..calculo import CalculoPosFixado


@dataclass
class Parcela:
    """Representação de uma parcela pos fixada"""
    pmt: int
    data_inicio: date
    data_vencimento: date
    data_ajustada: date
    amortizacao: float
    valor_nominal: float
    fechada: bool = False
    valor_aberto: float = 0.0
    juros_pre: float = 0.0
    juros_pos: float = 0.0
    fator_pre: float = 0.0
    fator_pos: float = 0.0
    atraso_multa: float = 0.0
    atraso_mora: float = 0.0
    atraso_juros_pre: float = 0.0
    atraso_juros_pos: float = 0.0
    pagamentos: List[Pagamento] = field(default_factory=list)

    def __repr__(self):
        return f"ParcelaPosFixada(pmt={self.pmt}, data_inicio={self.data_inicio}, " \
               f"data_vencimento={self.data_vencimento}, data_ajustada={self.data_ajustada}, " \
               f"amortizacao={self.amortizacao}, valor_nominal={self.valor_nominal}, valor_aberto={self.valor_aberto}," \
               f"juros_pre={self.juros_pre}, " \
               f"juros_pos={self.juros_pos}, fator_pre={self.fator_pre}, fator_pos={self.fator_pos}, " \
               f"atraso_multa={self.atraso_multa}, atraso_mora={self.atraso_mora}, " \
               f"atraso_juros_pre={self.atraso_juros_pre}, atraso_juros_pos={self.atraso_juros_pos})"

    def valor_pago(self) -> float:
        return self.valor_nominal - self.valor_aberto

    def is_vencida(self, data: date = None) -> bool:
        """Se a parcela já venceu"""
        if not data:
            data = date.today()

        return self.data_ajustada < data

    def is_corrente(self, data: date = None) -> bool:
        """Se é a parcela atual corrente"""
        if not data:
            data = date.today()

        return self.data_inicio < data <= self.data_ajustada

    def is_futura(self, data: date = None) -> bool:
        """Se é uma parcela futura, ainda não corrente"""
        if not data:
            data = date.today()

        return self.data_inicio >= data

    def atualiza_parcela(self, data_referencia: date, saldo_devedor: float, taxa_pre_anual: float, taxa_multa: float,
                         taxa_mora: float, calculador: CalculoPosFixado):
        if self.is_vencida(data_referencia):
            self._calcula_e_atualiza_parcela(data_inicio=self.data_inicio,
                                             data_final=self.data_ajustada,
                                             saldo_devedor=saldo_devedor,
                                             taxa_pre_anual=taxa_pre_anual,
                                             calculador=calculador)
            self._calcula_e_atualiza_parcela_atrasada(data_referencia=data_referencia,
                                                      taxa_pre_anual=taxa_pre_anual,
                                                      taxa_multa=taxa_multa,
                                                      taxa_mora=taxa_mora,
                                                      calculador=calculador)
        elif self.is_corrente(data_referencia):
            # ajuste porque não temos o índice disponível para o dia, sempre D-1
            data_calculo = data_referencia - datetime.timedelta(days=1)
            self._calcula_e_atualiza_parcela(data_inicio=self.data_inicio,
                                             data_final=data_calculo,
                                             saldo_devedor=saldo_devedor,
                                             taxa_pre_anual=taxa_pre_anual,
                                             calculador=calculador)
        elif self.is_futura(data_referencia):
            # não iremos calcular juros que ainda não incidiram na parcela
            return

    def _calcula_e_atualiza_parcela(self, data_inicio: date, data_final: date, saldo_devedor: float,
                                    taxa_pre_anual: float, calculador: CalculoPosFixado):
        amortizacoes = self._get_amortizacoes()
        valores_calculados = calculador.calcula_valor_atualizado(valor=saldo_devedor,
                                                                 data_inicio=data_inicio,
                                                                 data_final=data_final,
                                                                 taxa_pre_anual=taxa_pre_anual,
                                                                 amortizacoes=amortizacoes)
        self.valor_nominal = round(self.amortizacao + valores_calculados.juros_pre + valores_calculados.juros_pos, 2)
        self.valor_aberto = self.valor_nominal
        self.juros_pre = valores_calculados.juros_pre
        self.juros_pos = valores_calculados.juros_pos
        self.fator_pre = valores_calculados.fator_pre
        self.fator_pos = valores_calculados.fator_pos

    def _calcula_e_atualiza_parcela_atrasada(self, data_referencia: date, taxa_pre_anual: float, taxa_multa: float,
                                             taxa_mora: float, calculador: CalculoPosFixado):
        data_inicio = self._data_inicio_parcela_atrasada()
        data_final = prev_bizday(data_referencia)
        valores_atraso = calculador.calcula_valor_atualizado(valor=self.valor_aberto,
                                                             data_inicio=data_inicio,
                                                             data_final=data_final,
                                                             taxa_pre_anual=taxa_pre_anual)
        self.atraso_juros_pre = valores_atraso.juros_pre
        self.atraso_juros_pos = valores_atraso.juros_pos
        self.atraso_mora = valores_atraso.valor * taxa_mora
        self.atraso_multa = self.valor_nominal * taxa_multa

        self.valor_aberto += self.atraso_juros_pos + self.atraso_juros_pre + self.atraso_multa + self.atraso_mora

    def _data_inicio_parcela_atrasada(self) -> date:
        data_inicio = self.data_ajustada
        for pagamento in self.pagamentos:
            if pagamento.data > data_inicio:
                data_inicio = pagamento.data

        return adjust_next_bizdays(data_inicio)

    def _get_amortizacoes(self):
        amortizacoes = {}
        for pagamento in self.pagamentos:
            if pagamento.data in amortizacoes:
                amortizacoes[pagamento.data] += pagamento.valor
            else:
                amortizacoes[pagamento.data] = pagamento.valor

        return amortizacoes

    def cobrar_multa(self, data_referencia: date) -> bool:
        if not self.is_vencida(data_referencia):
            return False

        for pagamento in self.pagamentos:
            if pagamento.atraso_multa:
                return False
        return True

    def adiciona_pagamento(self, pagamento: Pagamento):
        self.valor_aberto -= pagamento.valor
        self.pagamentos.append(pagamento)
