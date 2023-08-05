import logging
import sys
from datetime import date, timedelta
from types import SimpleNamespace
from typing import Dict

from violeta.constantes import EnumTipoContagemDias
from violeta.date_utils import date_range, prev_bizday, is_bizday
from violeta.indices.indexador import Indexador, IndexadorCDI


class CalculoPosFixado:
    def __init__(self, indice: str, tipo_contagem: EnumTipoContagemDias, defasagem_indice: int = None, variacao_positiva: bool = False):
        """
        Construtor para cálculo de valores pós-fixados

        :param str indice: indice a ser usado para cálculo. ex.: cdi, ipca, igpm
        :param EnumTipoContagemDias tipo_contagem: define se usaremos dias corridos ou uteis para composição de juros
        :param int defasagem_indice: opcional. Defasagem em mêses de indices mensais
        :param bool variacao_positiva: opcional. Define se será aceita a aplicação de taxa de juros negativo no cálculo
        """
        self.indice = Indexador(indice)
        self.tipo_contagem = tipo_contagem
        self.defasagem_indice = defasagem_indice if defasagem_indice is not None else 0
        self.variacao_positiva = variacao_positiva

    def _get_taxa_pos(self, data_juros):
        taxa_pos = self.indice.get_taxa_diaria(data_juros, self.defasagem_indice)
        
        return 0 if taxa_pos < 0 and self.variacao_positiva else taxa_pos

    def calcula_valor_atualizado(self, valor: float, data_inicio: date, data_final: date, taxa_pre_anual: float,
                                 amortizacoes: Dict[date, float] = None) -> SimpleNamespace:
        """
        Calcula o valor atualizado com base no indice, taxa pre e datas

        O cálculo é feito com variação diária. Não é calculado o fator acumulado das taxas para evitar discrepâncias
        nos valores discriminados esperados de juros pré e pós-fixados. Entretanto, o valor final somado é o mesmo
        que se utilizado o fator acumulado

        :param float valor: valor inicial a ser corrigido
        :param date data_inicio: data inicio inclusiva de composição dos juros
        :param date data_final: data final inclusiva de composição dos juros
        :param float taxa_pre_anual: taxa pre fixada(spread) anualizada
        :param dict amortizacoes: opcional. Adiciona amortizações ao longo do prazo
        """
        range_datas_juros = date_range(data_inicio, data_final, self.tipo_contagem)

        fator_pre_acumulado = fator_pos_acumulado = 1
        juros_pre_acumulado = juros_pos_acumulado = 0

        for data_juros in range_datas_juros:
            taxa_pre = self._convert_to_taxa_diaria(taxa_pre_anual)
            juros_pre = valor * taxa_pre
            valor_com_juros_pre = valor + juros_pre

            taxa_pos = self._get_taxa_pos(data_juros)

            juros_pos = valor_com_juros_pre * taxa_pos
            valor_com_juros_pos = valor_com_juros_pre + juros_pos

            valor = valor_com_juros_pos

            if amortizacoes and data_juros in amortizacoes:
                valor -= amortizacoes[data_juros]

            # acumula valores apenas para referência
            fator_pre_acumulado *= 1 + taxa_pre
            fator_pos_acumulado *= 1 + taxa_pos
            juros_pre_acumulado += juros_pre
            juros_pos_acumulado += juros_pos
            logging.debug(f"{data_juros} {valor} {taxa_pos} {fator_pos_acumulado} {taxa_pre} {fator_pre_acumulado}")

        return SimpleNamespace(**{
            "valor": round(valor, 2),
            "juros_pre": round(juros_pre_acumulado, 2),
            "juros_pos": round(juros_pos_acumulado, 2),
            "fator_pre": round(fator_pre_acumulado, 8),
            "fator_pos": round(fator_pos_acumulado, 8)
        })

    @staticmethod
    def _convert_to_taxa_diaria(taxa_anual: float) -> float:
        base_du_ano = 252
        return (1 + taxa_anual) ** (1 / base_du_ano) - 1


if __name__ == "__main__":
    data_inicio = date(2022, 1, 14)
    data_final = date(2022, 2, 14)

    valor = 21_000_000.0
    taxa_pre = 0.1

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    root.addHandler(handler)

    def exemplo_cdi():
        print('CDI')
        fixado = CalculoPosFixado('cdi', EnumTipoContagemDias.uteis, defasagem_indice=2)

        valor_atualizado = fixado.calcula_valor_atualizado(valor, data_inicio, data_final, taxa_pre)
        print(valor_atualizado)

    def exemplo_ipca():
        print('IPCA')
        fixado = CalculoPosFixado('ipca', EnumTipoContagemDias.uteis, defasagem_indice=2)

        valor_atualizado = fixado.calcula_valor_atualizado(valor, data_inicio, data_final, taxa_pre)
        print(valor_atualizado)

    # exemplo_ipca()
