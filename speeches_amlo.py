import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import requests
from bs4 import BeautifulSoup as bs

df = pd.read_csv('./output/fechas_links_amlo.csv')    
cuantos = len(df.index)

speech = []
counter = 0
for url in df["Links"]:
    req = requests.get(url)
    if req.status_code!= 200:
        print("Error: ", req.status_code)
        break
    soup = bs(req.text,"lxml")
    entrada = soup.find_all("div", class_ = "entry-content")
    speech.append(entrada)
    counter +=1
    print(counter,"Discurso de ", cuantos)

df["Discurso"] = speech
print(df)
df.to_csv('./output/speeches_amlo.csv', index=True)    
