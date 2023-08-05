import datetime as dt

from dateutil.relativedelta import relativedelta
from violeta.date_utils import bizdays_in_month


class IndexadorMensal:
    '''
    Essa classe possui um único método get_daily_value que retornar a taxa diaria com defasagem em meses, get_daily_value recebe os seguintes paramêtros


    data: dt.date = Data base onde vai ser aplicado o período de defasagem
    defasagem: int = Quantidade de Meses em defasagem
    '''

    def get_daily_value(self, data: dt.date, defasagem: int = 0) -> float:
        if not hasattr(self, 'get_index_values'):
            raise NotImplementedError

        data_com_defasagem = data + relativedelta(months=-defasagem)
        dias_no_mes = bizdays_in_month(data_com_defasagem)
        taxa_mensal = self.get_index_values(data_com_defasagem)["variacao_calculada"]

        return taxa_mensal / dias_no_mes
