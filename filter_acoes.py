import pandas as pd
import re


def split_codigo(acao):
    match = re.match(r"([a-z]+)([0-9]+)", acao, re.I)
    items = match.groups()

    return items


def filter_indice(df):
    indices = list(df['indice'].values)

    if '11' in indices:
        return '11'

    elif '4' in indices:
        return '4'

    else:
        return '3'


df_acoes = pd.read_csv('dataset/cadastral_acao.csv')
list_acoes = list(df_acoes['acao'].values)

list_itens = [split_codigo(acao) for acao in list_acoes]

list_cod = []
list_ind = []
for value in list_itens:
    list_cod.append(value[0])
    list_ind.append(value[1])

df_split = pd.DataFrame({"codigo": list_cod,
                         "indice": list_ind})

list_ind_filter = [filter_indice(df_split[df_split['codigo'] == codigo]) for codigo in
                   list(sorted(set(df_split['codigo'].values)))]

df_filter = pd.DataFrame({'codigo': list(sorted(set(df_split['codigo'].values))),
                          'indice': list_ind_filter})

df_filter['acao'] = df_filter.apply(lambda x: f"{x['codigo']}{x['indice']}", axis=1)

df_filter_final = pd.merge(df_acoes, df_filter, left_on=['acao'], right_on=['acao'])
df_filter_final.to_csv("dataset/cadastral_acao_filter.csv", index=False)
print(df_filter_final)
