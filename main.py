# Você pode encontrar o tutorial onde esse código foi aplicado no seguinte link:
# https://tpaivalucas.medium.com/uma-introdu%C3%A7%C3%A3o-pr%C3%A1tica-ao-webscraping-com-python-a7edfb699847


from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime
from datetime import timedelta
import requests

days_back = 30
date = datetime.now() - timedelta(days=days_back) # Define a data limite para consulta.

dataframe = list()

for x in range(days_back):    
    url = (
        "https://www.buser.com.br/onibus/rio-de-janeiro-rj/sao-paulo-sp?ida="
        + "{}-{}-{}".format(date.year, date.month, date.day)  #Formata o final da URL com a data já incrementada pelo loop.
    )
    html = requests.get(url).content
    soup = BeautifulSoup(html, "html.parser")
    list_of_travels = soup.find_all(        
        "div", class_="bu-viagem bg-white text-grey pt-1 pb-0"  # Limita a busca à todas as divs com classe correspondente
    )

    for travel in list_of_travels:  # Executa a instrução para cada um dos itens da lista formada pelo BS4

        travel_data = {
            "data": "{}/{}/{}".format(date.day, date.month, date.year),
            "empresa": travel.find("p", class_="mb-0").text,
            "horario": travel.find("p", class_="viagem-data-hora text-black").text,
            "embarque": travel.find(
                "p", class_="text-black viagem-data-local ved-embarque"
            ).text,
            "desembarque": travel.find("p", class_="text-black viagem-data-local").text,
            "valor": travel.find("span", class_="h3 text-dark viagem-preco-buser").text,
        }

        dataframe.append(travel_data)

    date = date + timedelta(days=1) #Adiciona um dia à data até chegarmos à data atual, onde finalizamos o laço.
    time.sleep(0.5)

pd_data = pd.DataFrame(dataframe)
pd_data.to_excel("output.xlsx")   # Cria um dataframe e exporta em formato .xlsx
