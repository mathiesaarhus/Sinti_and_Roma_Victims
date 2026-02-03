# Creating csv for personal information

import os
from bs4 import BeautifulSoup
import pandas

data = []

files = os.listdir('sinti_en_roma_namenlijst')
for file in files:
    text = open('sinti_en_roma_namenlijst/'+file,'r',encoding='utf-8').read()
    soup = BeautifulSoup(text,features="lxml")
    
    person_ID = file[:-5] 
    name = soup.find('h1', attrs={'c-warvictim-intro__title'}).text.strip()
    name = " ".join(name.split())

    #we tried finding info through soup but found that it was easier to get the whole line (line_info from "c-warvictim-intro__sub") and then split it into different elements we choose from
    life_info = soup.find(attrs={"c-warvictim-intro__sub"}).text.split(',')
    place_of_birth = life_info[0]
    place_of_birth = " ".join(place_of_birth.split()) 
    date_of_death = life_info[2]
    date_of_death = " ".join(date_of_death.split())
    place_of_death = life_info[-2].split('–')[-1]
    place_of_death = " ".join(place_of_death.split())
    date_of_birth = life_info[-2].split('–')[0]
    date_of_birth = " ".join(date_of_birth.split())
    data.append([person_ID, name, date_of_birth, date_of_death, place_of_birth, place_of_death])

df = pandas.DataFrame(data,columns = ['person_ID', 'name', 'date_of_birth', 'date_of_death', 'place_of_birth', 'place_of_death'])
df = df.replace('Extern Kommando Sangershausen', 'Sangerhausen') 
df = df.replace('Extern kommando Sangerhausen', 'Sangerhausen')
df = df.replace('Extern kommando Sangershausen', 'Sangerhausen')
df.to_csv('person_information.csv', index=False, encoding='utf-8')   

# %%

# Creating csv for directed relationships

import os
from bs4 import BeautifulSoup
import pandas

data = []

files = os.listdir('sinti_en_roma_namenlijst')
for file in files:
    text = open('sinti_en_roma_namenlijst/'+file,'r',encoding='utf-8').read()
    soup = BeautifulSoup(text, features="lxml")
    links = soup.findAll(attrs={'class': "c-card-family__title"})
    for link in links:
        url = link.find('a')
        url1 = url['href'] 
        pID2 = url1.split('/')[-2]
        if pID2 == "page":
            pID2 = "Unknown" 
        pID1 = file[:-5]        
        parent_url = url.parent.parent        
        detailed_relation = parent_url.find(attrs={'class': "c-card-family__relation"})
        try: 
            detailed_relation = " ".join(detailed_relation.text.split())
        except AttributeError: 
            pass
        if detailed_relation == "Survivor":
            detailed_relation = ""
        try:
            detailed_relation = detailed_relation.split(" ")[0] 
        except AttributeError:
            pass
        parent_parent_url = parent_url.parent
        try:
            general_relation = parent_parent_url.find('h3').text
        except AttributeError: 
            pass
        if general_relation == "Siblings":
            general_relation = "Sibling"
        if general_relation == "Children":
            general_relation = "Child"
        if general_relation == "Parents":
            general_relation = "Parent"
        if pID1 != pID2:
            data.append([pID1, pID2, general_relation,detailed_relation])

df = pandas.DataFrame(data,columns = ['pID1', 'pID2', 'general_relation','detailed_relation'])
df.to_csv('directed_relationships.csv', index=False, encoding='utf-8')         