#import codecs
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from alive_progress import alive_bar


#response = codecs.open("../../../../dataset/cadastral_acao_test.html", 'r', 'utf-8')
#html_doc = response.read()
#soup = BeautifulSoup(html_doc, 'html.parser')

def get_page_stock(stock):
    url = f"https://statusinvest.com.br/acoes/{stock}"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    return soup

def get_cnpj(soup):
    cnpj = soup.find(class_="d-block fs-4 fw-100 lh-4").string
    return cnpj

def get_atuacao(soup):
    card_atuacao = soup.find(class_="top-info top-info-1 top-info-sm-2 top-info-md-n sm d-flex justify-between")

    # Setor Atuação ======
    setor_atuacao = card_atuacao.find(class_="info pr-md-2").find("strong").string

    # Subsetor Atuação =====
    subsetor_atuacao = card_atuacao.find(class_="info pl-md-2 pr-md-2").find("strong").string

    # Segmento de Atuação =====
    segmento_atuacao = card_atuacao.find(class_="info pl-md-2").find("strong").string

    return setor_atuacao, subsetor_atuacao, segmento_atuacao



df_stocks = pd.read_csv("../../../../dataset/statusinvest-busca-avancada.csv", sep=';')
list_stocks = [str(value).lower() for value in df_stocks['TICKER'].values]

list_cnpj = []
list_setor = []
list_subsetor = []
list_segmento = []

#for stock in tqdm(list_stocks):

with alive_bar(len(list_stocks), bar='classic', force_tty=True, title=f'Processando') as bar:
    for stock in list_stocks:
        soup = get_page_stock(stock)
        list_cnpj.append(get_cnpj(soup))
        setor_atuacao, subsetor_atuacao, segmento_atuacao = get_atuacao(soup)
        list_setor.append(setor_atuacao)
        list_subsetor.append(subsetor_atuacao)
        list_segmento.append(segmento_atuacao)
        bar()



df_final = pd.DataFrame({"acao":list_stocks,
                         "cnpj":list_cnpj,
                         "setor":list_setor,
                         "subsetor":list_subsetor,
                         "segmento":list_segmento})

print(df_final)

df_final.to_csv("../../../../dataset/cadastral_acao.csv", index=False)