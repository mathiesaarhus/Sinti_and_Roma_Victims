# -*- coding: utf-8 -*-

import urllib
import time

urls = "https://www.joodsmonument.nl/en/page/344139/sinti-en-roma-namenlijst/"

user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
headers = {'User-Agent': user_agent}

try:
    name = urls.split('/')[-2]
    request = urllib.request.Request( urls, None, headers )
    response = urllib.request.urlopen( request )
    with open(name+".html", 'w',encoding="utf-8") as f:
        f.write(str(response.read().decode('utf-8')))
    time.sleep(1)
except urllib.error.HTTPError as e:
    print(e)
        

import urllib
from bs4 import BeautifulSoup
import os

os.makedirs("sinti_en_roma_namenlijst", exist_ok=True)

page = open('sinti-en-roma-namenlijst.html', 'r', encoding='utf-8').read()
soup = BeautifulSoup(page, features="lxml")

links = soup.find_all(attrs={'class': "c-btn-cover"})

for link in links:
    name = link.text.strip().replace(' Name','')
    try:
        print("Getting page for:",name)
        url = 'https://www.joodsmonument.nl'+link['href']
        urllib.request.urlretrieve(url,"sinti_en_roma_namenlijst/"+url.split("/")[-2]+".html") 
        time.sleep(1)    
    except OSError:
        print("title not valid")
    except KeyError:
        print("No page available for:",name)