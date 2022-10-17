import numpy as np
import pandas as pd
from alive_progress import alive_bar

pd.set_option('display.max_columns', None)

df_dre = pd.read_csv("../../../dataset/DRE/2020/DRE_2020.csv")
acoes = pd.read_csv('../../../dataset/cadastral_acao.csv')
# acoes = acoes[acoes['setor'] == 'Financeiro e Outros']
df_dre = pd.merge(df_dre, acoes, left_on=['CNPJ_CIA'], right_on=['cnpj'])

dre = pd.pivot_table(df_dre, index=['CNPJ_CIA', 'DS_CONTA'], columns=['DT_INI_EXERC', 'DT_FIM_EXERC'],
                     values=['VL_CONTA'])

# Financeiro e Outros  X
# Consumo Cíclico OK
# Utilidade Pública OK
# Bens Industriais OK
# Materiais Básicos OK
# Consumo não Cíclico OK
# Saúde OK
# Tecnologia da Informação OK
# Petróleo. Gás e Biocombustíveis OK
# Comunicações OK


# print(dre.loc['28.195.667/0001-06'])
list_cnpj = list(set(df_dre['CNPJ_CIA'].values) - set(
    ['30.723.886/0001-62', '92.702.067/0001-96', '17.344.597/0001-94', '28.127.603/0001-78', '61.186.680/0001-74',
     '17.184.037/0001-10', '00.000.000/0001-91', '02.762.113/0001-50', '00.416.968/0001-01', '60.872.504/0001-23',
     '59.285.411/0001-13', '60.746.948/0001-12', '62.144.175/0001-20', '90.400.888/0001-42', '15.144.017/0001-90',
     '33.376.989/0001-91', '28.195.667/0001-06']))
# list_cnpj = list(set(df_dre['CNPJ_CIA'].values))
print(len(list_cnpj))


# list_cnpj = ['37.663.076/0001-07', '61.156.931/0001-78', '61.351.532/0001-68', '61.374.161/0001-30', '00.416.968/0001-01']
#
# Resultado Bruto => Lucro Bruto
# Receita de Venda de Bens e/ou Serviços => Receita Liquida
# (Lucro Bruto / Receita Liquida)*100
def calculate_margem_bruta(dre, cnpj):
    try:
        margem_bruta = (dre.loc[cnpj, :].loc['Resultado Bruto'].iloc[-1] /
                        dre.loc[cnpj, :].loc['Receita de Venda de Bens e/ou Serviços'].iloc[-1]) * 100
        return margem_bruta

    except:
        return 0


# Lucro/Prejuízo Consolidado do Período => Lucro Liquido
# Receita de Venda de Bens e/ou Serviços => Receita Liquida
# Lucro Liquido / Receita Liquida
def calculate_margem_liquida(dre, cnpj):
    if dre.loc[cnpj, :].loc['Receita de Venda de Bens e/ou Serviços'].iloc[-1] != 0:
        try:
            margem_liquida = (dre.loc[cnpj, :].loc['Lucro/Prejuízo Consolidado do Período'].iloc[-1] /
                              dre.loc[cnpj, :].loc['Receita de Venda de Bens e/ou Serviços'].iloc[-1]) * 100
            return margem_liquida

        except:
            return 0

    else:
        return 0


# Receita de Venda de Bens e/ou Serviços => Receita Liquida
# Custo dos Bens e/ou Serviços Vendidos => Custos
# Despesas com Vendas
# Despesas Gerais e Administrativas
# EBITDA = Receita de Venda de Bens e/ou Serviços + Custo dos Bens e/ou Serviços Vendidos + Despesas com Vendas + Despesas Gerais e Administrativas
def calculate_ebitda(dre, cnpj):
    try:
        ebitda = dre.loc[cnpj, :].loc['Receita de Venda de Bens e/ou Serviços'].iloc[-1] + \
                 dre.loc[cnpj, :].loc['Custo dos Bens e/ou Serviços Vendidos'].iloc[-1] + \
                 dre.loc[cnpj, :].loc['Despesas com Vendas'].iloc[-1] + \
                 dre.loc[cnpj, :].loc['Despesas Gerais e Administrativas'].iloc[-1]

        return ebitda

    except:
        return 0


# EBITDA
# Receita de Venda de Bens e/ou Serviços => Receita Liquida
# (EBITDA/Receita Liquida)*100
def calculate_margem_ebitda(dre, cnpj, ebitda):
    if dre.loc[cnpj, :].loc['Receita de Venda de Bens e/ou Serviços'].iloc[-1] != 0:
        try:
            margem_ebitda = (ebitda / dre.loc[cnpj, :].loc['Receita de Venda de Bens e/ou Serviços'].iloc[-1]) * 100
            return margem_ebitda

        except:
            return 0
    else:
        return 0


list_m_bruta = []
list_m_liq = []
list_m_ebitda = []

with alive_bar(len(list_cnpj), bar='classic', force_tty=True, title=f'Calculando') as bar:
    for cnpj in list_cnpj:
            print(cnpj)
            list_m_bruta.append(np.round(calculate_margem_bruta(dre, cnpj), 2))
            list_m_liq.append(np.round(calculate_margem_liquida(dre, cnpj), 2))

            ebitda = calculate_ebitda(dre, cnpj)
            list_m_ebitda.append(np.round(calculate_margem_ebitda(dre, cnpj, ebitda), 2))

df_lucratividade = pd.DataFrame({'cnpj': list_cnpj,
                                 'margem_bruta': list_m_bruta,
                                 'margem_liquida': list_m_liq,
                                 'margem_ebitda': list_m_ebitda})

df_lucratividade.to_csv("../../../dataset/indicadores_lucratividade/indicadores_lucratividade.csv", index=False)
