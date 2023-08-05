import datetime as dt
from violeta.fluxo_parcelas import Parcelas
from math import isclose

# dados de teste
DADOS_TITULO = dict(
    valor_aquisicao=2538.23,
    valor_parcela=461.21,
    data_originacao=dt.date(2019, 2, 13),
    primeiro_vencimento=dt.date(2019, 3, 5),
    quantidade_parcela=12,
)


VP_list = [423.66, 362.58, 316.97, 271.27, 233.81, 201.52, 171.25, 146.56,
            126.32, 108.88, 94.51, 80.89]

TIR_ANUAL = 4.9493

# VP na curva
VPSUM_14_02_19 = 2538.23
VPSUM_10_03_19 = 2368.09


def test_vp_data_originacao():
    parc = Parcelas(
        data_desembolso=dt.date(2019, 2, 14),
        **DADOS_TITULO
    )
    fluxo = parc.gerar_fluxo()

    assert isclose(TIR_ANUAL, fluxo['taxa'], abs_tol=1e-4)

    for i, pmt in enumerate(fluxo['parcelas']):
        assert isclose(VP_list[i], pmt['valor_presente'])

    assert isclose(DADOS_TITULO['valor_aquisicao'], fluxo['vp_calculado'], abs_tol=1e-1)


def test_vp_curva():
    parc = Parcelas(
        data_desembolso=dt.date(2019, 2, 14),
        **DADOS_TITULO
    )
    fluxo = parc.gerar_fluxo()

    assert isclose(TIR_ANUAL, fluxo['taxa'], abs_tol=1e-4)
    assert isclose(VPSUM_14_02_19, fluxo['vp_calculado'], abs_tol=1e-1)
