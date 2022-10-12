import io
import os.path
import time
import zipfile

import pandas as pd
import requests
from alive_progress import alive_bar

pd.set_option('display.max_columns', None)
start_time = time.time()

root = "https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/ITR/DADOS/"
list_date = [2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]


def save_file(df, type, date):
    path = f"../../../../dataset/{type}/{date}"

    if os.path.isdir(path) == False:  # vemos de este diretorio ja existe
        os.mkdir(path)

    df.to_csv(path + f"/{type}_{date}.csv", index=False)


def read_file(type, zip_files, date):
    arquivo = f'itr_cia_aberta_{type}_con_{date}.csv'

    zf = zip_files.open(arquivo)

    lines = zf.readlines()
    lines = [i.strip().decode('ISO-8859-1').split(';') for i in lines]
    df = pd.DataFrame(lines[1:], columns=lines[0])
    df = df[df['ORDEM_EXERC'] == 'ÚLTIMO']

    return df


def read_zip(date, bar):
    link = f'{root}itr_cia_aberta_{date}.zip'

    r = requests.get(link)
    zf = zipfile.ZipFile(io.BytesIO(r.content))

    list_demo = ['DRE', 'BPP', 'BPA']

    for demo in list_demo:
        print(f"Baixando {demo}")
        df = read_file(demo, zf, date)
        save_file(df, demo, date)


with alive_bar(len(list_date), bar='classic', force_tty=True, title=f'Download') as bar:
    for date in list_date:
        read_zip(date, bar)
        bar()
