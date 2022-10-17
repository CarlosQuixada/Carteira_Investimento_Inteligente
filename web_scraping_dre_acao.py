import pandas as pd
import requests
from alive_progress import alive_bar


def get_range_date(acao):
    url = f"https://statusinvest.com.br/acao/getdre?code={acao}&type=1&futureData=false"
    resp = dict(requests.get(url).json())
    list_anos = list(resp['data']['years'])
    return list_anos[0], list_anos[-1]


def get_dre_data(acao, min_ano, max_ano):
    url = f"https://statusinvest.com.br/acao/getdre?code={acao}&type=1&futureData=false&range.min={min_ano}&range.max={max_ano}"
    resp = dict(requests.get(url).json())

    return resp


def get_trimestres(resp):
    list_trimestre = []
    list_ano = []

    for ind, row in enumerate(resp['data']['grid'][0]['columns']):
        if ind != 0:
            if row['name'] == "DATA":
                value = str(row['value']).split('T')
                list_trimestre.append(value[0])
                list_ano.append(value[1])

    return list_trimestre, list_ano


def get_values(resp, trimestres, anos):
    list_key = []
    list_dre = []
    list_value = []
    list_trim_final = []
    list_ano_final = []

    for ind, row in enumerate(resp['data']['grid']):
        if ind != 0:
            list_key.extend([row['gridLineModel']['key']] * len(row['gridLineModel']['values']))
            list_dre.extend([row['gridLineModel']['name']] * len(row['gridLineModel']['values']))
            list_value.extend(row['gridLineModel']['values'])
            list_trim_final.extend(trimestres)
            list_ano_final.extend(anos)

    return list_key, list_dre, list_value, list_trim_final, list_ano_final


df_acoes = pd.read_csv('dataset/cadastral_acao_filter.csv')
list_acoes = list(sorted(set(df_acoes['acao'].values)))

list_dfs = []
with alive_bar(len(list_acoes), bar='classic', force_tty=True, title=f'Download') as bar:
    for acao in list_acoes:
        bar()
        min_ano, max_ano = get_range_date(acao)
        resp = get_dre_data(acao, min_ano, max_ano)

        trimestres, anos = get_trimestres(resp)
        list_key, list_dre, list_value, list_trim_final, list_ano_final = get_values(resp, trimestres, anos)

        df = pd.DataFrame({'acao': [acao] * len(list_key),
                           'trimestre': list_trim_final,
                           'ano': list_ano_final,
                           'key': list_key,
                           'dre': list_dre,
                           'value': list_value})

        list_dfs.append(df)

df_dre_trim = pd.concat(list_dfs, ignore_index=True)
print(df_dre_trim)
df_dre_trim.to_csv('dataset/DRE/trimestral/dre_filter.csv', index=False)
