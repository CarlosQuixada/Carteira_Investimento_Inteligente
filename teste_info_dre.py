import pandas as pd

pd.set_option('display.max_columns', None)

# cnpj = "61.532.644/0001-15"
cnpj = "00.000.000/0001-91"
# list_cnpj = ['30.723.886/0001-62', '92.702.067/0001-96', '17.344.597/0001-94', '28.127.603/0001-78',
#              '61.186.680/0001-74',
#              '17.184.037/0001-10', '00.000.000/0001-91', '02.762.113/0001-50', '00.416.968/0001-01',
#              '60.872.504/0001-23',
#              '59.285.411/0001-13', '60.746.948/0001-12', '62.144.175/0001-20', '90.400.888/0001-42',
#              '15.144.017/0001-90', '33.376.989/0001-91', '28.195.667/0001-06']
dre = pd.read_csv("dataset/DRE/2021/DRE_2021.csv")
#dre = dre[dre['CNPJ_CIA'] == cnpj]
#dre = dre[dre['CNPJ_CIA'].isin(list_cnpj)]

list_conta = list(set(dre['DS_CONTA'].values))

# dre = pd.pivot_table(dre, index=['CNPJ_CIA', 'DS_CONTA'], columns=['DT_INI_EXERC', 'DT_FIM_EXERC'],
#                      values=['VL_CONTA'])
print(list_conta)
#
# acoes = pd.read_csv('dataset/cadastral_acao.csv')
# acoes = acoes[acoes['cnpj'].isin(list_cnpj)]
# #print(acoes)