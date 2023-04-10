## AMLO_Transcripts
## Codigo para parsear y scrapear la página de amlo y bajar sus scripts
## Y con ellos hacer un df con los textos enteros y fechas para después analizarlos

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

url = "https://lopezobrador.org.mx/transcripciones/" # homepage url
req = requests.get(url) # request
html_text = req.text # Get page
soup = bs(html_text,  "lxml") # parse in bs fashion
## Finding span object in entries which contains hyperlinks to other pages to acces ADN dates -----
amlo_ed = soup.find_all("span", class_ = "entry-date")
# must parse each entry for href and content
links = []
fechas = []
for entradas in amlo_ed:
    link = entradas.find("a")["href"] # gets flippin thing
    fecha = entradas.text # gets content of tag
    links.append(link)
    fechas.append(fecha)

## Now run it for the fucking bulk of the 311 pages lmfao jesus im a beast
# Make list to parse
base_url = "https://lopezobrador.org.mx/transcripciones/page/"
url_list = []
for i in range(2,312,1):
    urlt = base_url+str(i)+"/"
    url_list.append(urlt)
iterations = 0
# parse the whole thing
for url in url_list:
    req = requests.get(url) # request
    if req.status_code != 200:
        print("Error, status code: ",req.status_code)
        break
    soup = bs(req.text,  "lxml") # parse in bs fashion
    amlo_ed = soup.find_all("span", class_ = "entry-date")
    iterations +=1
    for entradas in amlo_ed:
        link = entradas.find("a")["href"] # gets flippin thing
        fecha = entradas.text # gets content of tag
        links.append(link)
        fechas.append(fecha)
    print(iterations, " iterations done")


df = pd.DataFrame({"Fechas": fechas, "Links": links})
print(df)
df.to_csv('./output/fechas_links_amlo.csv', index=True)    

speech = []
counter = 0
for url in df["Links"]:
    req = requests.get(url)
    soup = bs(req)
    entrada = soup.find_all("div", class_ = "entry-content")
    speech.append(entrada)
    counter +=1
    print(counter,"Discurso de ", len(df.index))

df["Discurso"] = speech

df.to_csv('./output/speeches_amlo.csv', index=True)    























