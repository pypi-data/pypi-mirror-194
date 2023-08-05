import datetime as dt

from violeta.date_utils import prev_bizday, is_bizday


class IndexadorDiario():

    '''
    Essa classe possui um único método get_daily_value que retornar a taxa diaria com defasagem em dias, get_daily_value recebe os seguintes paramêtros


    data: dt.date = Data base onde vai ser aplicado o período de defasagem
    defasagem: int = Quantidade de dias em defasagem
    '''

    def get_daily_value(self, data: dt.date, defasagem: int = 0) -> float:
        if not hasattr(self, 'get_index_values'):
            raise NotImplementedError
        
        data_com_defasagem = data - dt.timedelta(days=defasagem)
        if not is_bizday(data_com_defasagem):
            data_com_defasagem = prev_bizday(data_com_defasagem)

        return round(self.get_index_values(data_com_defasagem)["indice"] / 100, 8)
