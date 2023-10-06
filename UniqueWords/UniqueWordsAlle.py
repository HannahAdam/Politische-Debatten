# Infos: 

# Dieser Code dient dazu, die Worte in Listen zu speichern, welche nur von einer Partei benutzt werden. 
# Deshalb werden diese Worte als Unique Words; einzigartige Worte, bezeichnet. 


# Hinweise: 

# Die hier generierten Listen werden bereits im Ordner results zur Verfügung gestellt. 
# Diese Listen werden in anderen meiner Codes geladen und weiter verwendet, dabei muss der Ablageort auf deinem Computer stimmen. 
# In der neuen Datei stehen die Wortlisten immer unter einem Schlüsel (key); dem Namen der Partei. 
# Wenn du einen eigenen Code benutzt, um die hier erstellten Listen zu benutzen, beachte den Namen: _{key}_{legislatur} -> Unterstriche im Namen können in der weiteren Verwendung zu Problemen führen.  


import jsonlines
import json
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from PIL import Image
import numpy as np
from collections import Counter
import networkx as nx

#Importieren der lemmatisierten Reden

def laden_alleReden(legislatur):
    with open(f'/Users/hannahadam/Desktop/bundestag/data_preprocessed/speeches_{legislatur}_preprocessed.json', 'r') as fp:
        data = json.load(fp)

    return data.copy()

legislatur = 19
alleReden = laden_alleReden(legislatur)

#print(alleReden[0])

#Reden nach Parteien sortieren und zu Parteitexten zusammenfügen

reden_gefiltert = {'CDU_CSU': [],
                   'SPD': [],
                   'AfD': [],
                   'FDP': [],
                   'BÜNDNIS 90_DIE GRÜNEN': [],
                   'DIE LINKE': [],
                   'fraktionslos': [],
                   'Bremen': [],
                   'unknown': []
                   }

for rede in alleReden:
    rede['party'] = rede['party'].replace(u'\xa0', u' ')
    rede['party'] = rede['party'].replace(u'/', u'_')
    if rede['party'] == 'Bündnis 90_Die Grünen':
        rede['party'] = 'BÜNDNIS 90_DIE GRÜNEN'
    if rede['party'] == 'Fraktionslos':
        rede['party'] = 'fraktionslos'


    reden_gefiltert[rede['party']].extend(rede['text_lem'])

#Erstellen von unique words (uw) von Einzelparteien und Parteipaaren

def return_unique_words(partylist, word_dict):
    andereworte = set()
    parteienworte = set()
    for key in word_dict.keys():
        if key not in partylist:
            andereworte = andereworte | set(word_dict[key])
        else:
            parteienworte = parteienworte | set(word_dict[key])

    unique_words = parteienworte - andereworte

    return unique_words

#Unique words nach Parteien in Form von Keys sortiert

uw_all = {'SPD': return_unique_words('SPD',reden_gefiltert),
'FDP': return_unique_words('FDP',reden_gefiltert),
'CDU_CSU': return_unique_words('CDU_CSU',reden_gefiltert),
'DIE LINKE': return_unique_words('DIE LINKE',reden_gefiltert),
'BÜNDNIS 90_DIE GRÜNEN': return_unique_words('BÜNDNIS 90_DIE GRÜNEN',reden_gefiltert),
'AfD': return_unique_words('AfD',reden_gefiltert)
}

print(uw_all['BÜNDNIS 90_DIE GRÜNEN'])

len(uw_all['BÜNDNIS 90_DIE GRÜNEN'])

#Speichern

uw_all_lists = {}
for key,value in uw_all.items():
    #uw_all_lists.update({ key : list(uw_all[key]) })
    with open(f'results/_{key}_{legislatur}.json', 'w', encoding='UTF8') as fp:
        json.dump({key : list(value)}, fp, sort_keys=True, indent=4, ensure_ascii=False)


