from flask import send_file
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pandas as pd
import requests

def ranking():
   # get hmtl file containing Nadal's ranking data from atptour
    site = 'https://www.atptour.com/en/players/rafael-nadal/n409/rankings-history'
    data = BeautifulSoup(requests.get(site).content,'html.parser')
    tables = data.find_all('table')
    
    # convert the html file to DataFrame tables
    ranking = pd.read_html(str(tables[1]))[0]
    
    # process the data
    ranking['Week'] = range(len(ranking),0,-1)
    ranking['Quarter'] = ranking['Week']/12
    ranking.drop(['Doubles','Date'],axis=1,inplace=True)
    # select rankings at the start of each quarter
    ranking = ranking.head(900)[-1::-12]

    ranking['Singles'] = pd.to_numeric(ranking['Singles'])
    
    # plot ranking vs quarter
    ax = ranking.plot(x='Quarter',y='Singles',kind='scatter', \
             title='Rafael Nadal\'s history of ATP ranking', \
             color='seagreen', figsize = (10,8))

    ax.set_xlabel('Quarter No. since Pro')
    ax.set_ylabel('ATP Singles Ranking')
    
    # save plot
    plt.savefig('Nadal Ranking.png')
    
    return send_file('Nadal Ranking.png', mimetype = 'image/png') 
