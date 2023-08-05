import pandas as pd
import functools as func
import operator


class PDD:
    """
    DF com Matriz de rolagem
    chamar: PDD(faixa_pdd)(matriz)
    EX Faixa_pdd:
        {'0': 0, '1': 30, '2': 60, '3': 90, '4': 120, '5': 150, '6': 180}
    EX Matriz:
                0                1               2              3
        0	1.987038e+08	2.083425e+08	2.009372e+08	1.752676e+08
        1	2.785010e+07	1.740005e+07	1.501961e+07	2.211630e+07
        2	7.729672e+06	7.536564e+06	7.621408e+06	4.561096e+06
        3	5.212781e+06	6.864907e+06	6.573279e+06	6.353364e+06
        4	8.262887e+06	4.948561e+06	6.849818e+06	6.257886e+06
        5	5.077464e+06	7.902845e+06	4.870179e+06	6.394145e+06
        6	5.683260e+06	5.155184e+06	7.962849e+06	4.705649e+06
        7	5.407681e+07	6.911881e+07	7.356098e+07	8.130708e+07

    """

    def __init__(self, faixa_pdd={}):
        self.faixa_pdd = faixa_pdd

    def __call__(self, df):
        df = self.rolagem(df)
        df = self.pdd_rate(df)
        return df

    def rolagem(self, df):
        assert isinstance(df, pd.core.frame.DataFrame), "parametro nao e um DataFrame"
        dados = df.to_dict('r')
        rolagens = []
        for i, d in enumerate(dados):
            rolagem = {}
            if i == 0:
                continue
            for x, k in enumerate(d.keys()):
                if x < 1:
                    index_ant = k
                    continue
                calc = dados[i][k] / dados[i - 1][index_ant]
                calc = calc if calc < 1 else 1
                rolagem[k] = calc
                index_ant = k
            rolagens.append(rolagem)
        df_rolagem = pd.DataFrame(rolagens)
        df_rolagem['media'] = df_rolagem.apply(lambda x: sum(x) / len(x), axis=1)
        
        return df_rolagem

    def pdd_rate(self, df):
        assert isinstance(df, pd.core.frame.DataFrame), "parametro nao e um DataFrame"
        assert 'media' in df.columns.tolist(), "falta campo media"

        def produto(x, media):
            return func.reduce(operator.mul, [m for i, m in enumerate(media) if i >= x.name])

        df['pdd_rate'] = df.apply(lambda x: produto(x, df['media']), axis=1)
        return df

    def pdd_ativo(self, valor_presente: float, dias: int, df_rate):
        """
            Calcular pdd do ativo
            return (valor_pdd, faixa_pdd)
            EX:
                valor_presente : 27.00
                dias: 271
                df_rate:
                        pdd_rate
                    0	0.50
                    1	0.60
                    2	0.70
                    3	0.76
                    4	0.80
                    5	0.90
                    6	1.00
        """
        primeiro = list(self.faixa_pdd.keys())[0]
        for i, l in enumerate(self.faixa_pdd):
            faixa_atual = self.faixa_pdd[l]
            if i == 0 and dias >= self.faixa_pdd[l]:
                faixa = l
                valor_rate = valor_presente * df_rate['pdd_rate'][int(l)]
                break
            if l == primeiro:
                faixa_ant = faixa_atual
                continue
            elif dias <= faixa_ant and dias >= faixa_atual:
                faixa = l
                valor_rate = valor_presente * df_rate['pdd_rate'][int(l)]
                break
            else:
                faixa = (i + 1)
                valor_rate = valor_presente * df_rate['pdd_rate'][int(l)]

            faixa_ant = faixa_atual

        return round(valor_rate, 2), faixa
