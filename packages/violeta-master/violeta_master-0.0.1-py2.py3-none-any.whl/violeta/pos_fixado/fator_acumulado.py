import datetime as dt
import pandas as pd
from decimal import Decimal, getcontext
from dateutil.relativedelta import relativedelta

from violeta.date_utils import bizdays_delta, prev_bizday, next_bizday, is_bizday, last_day_month
from violeta.exceptions import DataInvalidaError
from violeta.indices.indexador import Indexador

getcontext().prec = 9


class FatorAcumuladoIndexador:
    DEFASAGEM_CALIBRE = 2

    def __init__(
            self,
            indexador: str,
            data_aquisicao: dt.date,
            data_vencimento: dt.date,
            data_ref: dt.date = None,
            variacao_positiva=True,
            defasagem=2
    ):
        if not is_bizday(data_ref):
            raise DataInvalidaError(f'Data {data_ref} invalida para precificação 252')

        self.data_ref = data_ref
        self.indexador = indexador
        self.defasagem = defasagem
        self.indice = Indexador(self.indexador)
        self.variacao_positiva = variacao_positiva
        self.data_aquisicao = data_aquisicao
        self.dia_aniversario = data_vencimento.day

    def _gerar_matriz(self) -> pd.DataFrame:
        datas_matriz = pd.period_range(start=self.data_aquisicao, end=self.data_ref, freq='D')
        amostra = []
        for p in datas_matriz:
            data = p.to_timestamp().date()
            if not is_bizday(data):
                continue

            amostra.append(CalcularAniversarioDias(data, self.data_aquisicao, self.dia_aniversario).__dict__)

        return pd.DataFrame(amostra)

    def _calcular_matriz(self) -> pd.DataFrame:
        def _cal_taxa(x, df, variacao) -> Decimal:
            taxa = round(self.get_taxa_indice(x['DATA_ANIVERSARIO']), 8)
            return max(taxa, 0) if variacao else taxa

        def fator(x):
            DU = 1 if x.DU > 0 else 0
            return (1 + x['TAXA']) ** Decimal(DU / x['DU_TOTAL'])

        df = self._gerar_matriz()
        df['TAXA'] = df.apply(lambda x: _cal_taxa(x, df, self.variacao_positiva), axis=1)
        df['FATOR'] = df.apply(lambda x: fator(x), axis=1)
        df['FATOR_ACUMULADO'] = df['FATOR'].cumprod()
        return df

    def get_taxa_indice(self, data_referencia: dt.date) -> Decimal:
        defasagem = self.defasagem - self.DEFASAGEM_CALIBRE
        data_referencia = prev_bizday(dt.date(data_referencia.year, data_referencia.month, 1) + relativedelta(days=-1))
        data_referencia = data_referencia + relativedelta(months=-defasagem)
        return Decimal(self.indice.get_valor(data_referencia)['variacao_calculada'])

    def fator_acumulado(self) -> Decimal:
        df = self._calcular_matriz()
        return round(df.iloc[-1, :]['FATOR_ACUMULADO'], 8)


class CalcularAniversarioDias():
    def __init__(self, data_ref: dt.date, data_cessao: dt.date, day_niver: dt.date):
        self.DATA_REF = data_ref
        self.data_cessao = data_cessao
        self.day_niver = day_niver
        self.DATA_ANIVERSARIO = self._niver_ant()
        self.DATA_REF_BASE = data_ref
        self.DATA_PROX_ANIVERSARIO = self._niver_prox()
        self.DATA_DU_BASE = self._get_du_base()
        self.DU = self._get_du()
        self.DU_TOTAL = self._get_du_total()
        self.DATA_VIRADA = next_bizday(self.DATA_ANIVERSARIO)

    def _niver_prox(self) -> dt.date:
        return self._ajuste_data_valida(self.DATA_ANIVERSARIO + relativedelta(months=+1))

    def _get_du_base(self) -> dt.date:
        return self.data_cessao if self.DATA_ANIVERSARIO < self.data_cessao else self.DATA_ANIVERSARIO

    def _get_du(self) -> int:
        return bizdays_delta(self.DATA_DU_BASE, self.DATA_REF_BASE)

    def _get_du_total(self) -> int:
        return bizdays_delta(self.DATA_ANIVERSARIO, self.DATA_PROX_ANIVERSARIO)

    def _ajuste_data_valida(self, data_ref: dt.date) -> dt.date:
        data = data_ref.replace(day=last_day_month(data_ref))
        data = data_ref.replace(day=self.day_niver) if data.day > self.day_niver else data
        return next_bizday(data)

    def _niver_ant(self) -> dt.date:
        data = self._ajuste_data_valida(self.DATA_REF)
        if self.DATA_REF.day <= data.day:
            data = self.DATA_REF.replace(day=1) + relativedelta(days=-1)
            if self.day_niver < data.day:
                data = data.replace(day=self.day_niver)

        return next_bizday(data)
