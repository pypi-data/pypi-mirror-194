from datetime import date
from violeta.date_utils import datas_vencimento, force_date
from violeta.calc import xirr, xvp


class Parcelas:
    """
    Classe helper para gerar pmts com data de vcto ajustada, calcular TIR e valor de aquisicao

    OBS: parcelas vencidas (legado) retornam com VP = 0
    """

    def __init__(self, *, valor_aquisicao, quantidade_parcela,
                 valor_parcela, primeiro_vencimento,
                 data_desembolso=None, data_originacao=None, periodo='m', data_emissao=False):

        self.data_desembolso = force_date(data_desembolso) if data_desembolso else date.today()
        self.data_originacao = force_date(data_originacao) if data_originacao else data_desembolso
        self.valor_parcela = valor_parcela
        self.valor_aquisicao = valor_aquisicao
        self.quantidade_parcela = quantidade_parcela
        self.primeiro_vencimento = force_date(primeiro_vencimento)
        self.periodo = periodo
        self.day_vencimento = self.primeiro_vencimento.day
        self.data_emissao = force_date(data_emissao) if data_emissao else data_emissao

    def gerar_fluxo(self, pmt_calcula_vp=0, vencidos=False, primeira_parcela=1):
        pmts = self.gerar_parcelas(self.primeiro_vencimento, self.quantidade_parcela, self.valor_parcela,
                                   self.periodo, self.data_emissao, primeira_parcela)
        taxa = self.get_taxa(pmts, self.valor_aquisicao, self.data_desembolso, pmt_calcula_vp, vencidos)
        pmts_vp, vp_cal = self.cal_vp(pmts, taxa, self.data_desembolso, pmt_calcula_vp, vencidos, self.data_originacao)
        return {"taxa": taxa, "vp_calculado": round(vp_cal, 2), "parcelas": pmts_vp}

    @classmethod
    def gerar_parcelas(cls, primeiro_vcto, qtde_parcelas, valor_parcela, periodo, data_emissao=False, primeira_parcela=1):
        valor = round(valor_parcela, 2)
        vctos = datas_vencimento(primeiro_vcto, periodo, qtde_parcelas, data_emissao)
        return [dict(pmt=primeira_parcela + i, valor_parcela=valor, **vctos[i]) for i in range(qtde_parcelas)]

    @staticmethod
    def cal_vp(pmts, taxa, data_desembolso, pmt_calcula_vp=0, vencidos=False, data_originacao=False):
        vp_total = 0
        if pmt_calcula_vp:
            pmt_qtd = round(len(pmts) - pmt_calcula_vp)
        else:
            pmt_qtd = pmt_calcula_vp

        for i, pmt in enumerate(pmts):
            data_vcto = pmt.get('data_ajustada')

            if data_vcto <= data_desembolso or i < pmt_qtd:
                vp_cal = 0 if not vencidos or i < pmt_qtd else pmt.get('valor_parcela')
                valor_emissao = 0
            else:
                vp_cal = round(xvp(pmt.get('valor_parcela'), taxa, pmt.get('data_ajustada'), data_desembolso), 2)
                data_originacao = data_originacao if data_originacao else data_desembolso
                valor_emissao = xvp(pmt.get('valor_parcela'), taxa, pmt.get('data_ajustada'), data_originacao)

            vp_total = vp_total + vp_cal
            pmts[i]['valor_presente'] = vp_cal
            pmts[i]['valor_aquisicao'] = vp_cal
            pmts[i]['valor_emissao'] = round(valor_emissao, 2)

        return pmts, vp_total

    @staticmethod
    def get_taxa(pmts, valor_aquisicao, data_desembolso, pmt_calcula_vp=0, vencidos=False):
        valor_aquisicao = valor_aquisicao * -1
        lista_datas = [data_desembolso]
        lista_parcelas = [valor_aquisicao]

        if pmt_calcula_vp:
            pmt_qtd = round(len(pmts) - pmt_calcula_vp)
        else:
            pmt_qtd = pmt_calcula_vp

        for i, pmt in enumerate(pmts):
            if pmt_qtd > i:
                continue
            if pmt.get('data_ajustada') > data_desembolso:
                lista_datas.append(pmt.get('data_ajustada'))
                lista_parcelas.append(pmt.get('valor_parcela'))

        Xirr_ = xirr(lista_parcelas, lista_datas)

        return Xirr_

    @staticmethod
    def ajuste_parcelas(vp, vp_cal, pmts):
        resto = round(vp - vp_cal, 2)
        range_ = int(abs(round(vp - vp_cal, 2)) * 100)
        if range_ > 10:
            return pmts
        i = 0
        count_par = len(pmts) - 1
        par = count_par
        ajuste = 0.01
        if resto < 0:
            ajuste = ajuste * -1
        while i < range_:
            pmts[par]['valor_presente'] = round(pmts[par]['valor_presente'] + ajuste, 2)
            pmts[par]['valor_aquisicao'] = round(pmts[par]['valor_aquisicao'] + ajuste, 2)
            par -= 1
            par = 0 if par > (count_par * -1) else par
            i += 1

        return pmts


if __name__ == "__main__":
    par = Parcelas(**{
        "valor_aquisicao": 935.50,
        "quantidade_parcela": 12,
        "valor_parcela": 131.54,
        "primeiro_vencimento": '2019-05-03',
        "data_desembolso": '2019-05-01',
        "data_originacao": '2019-05-01',
    })
    fluxo = par.gerar_fluxo()
    fluxo['parcelas'][0]['valor_presente'] = fluxo['parcelas'][0]['valor_presente'] - 0.09
    sum_par = sum(x['valor_presente'] for x in fluxo['parcelas'])
    fluxo['parcelas'] = par.ajuste_parcelas(935.23, sum_par, fluxo['parcelas'])
    sum_par_ = sum(x['valor_presente'] for x in fluxo['parcelas'])
    print(sum_par_)
