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





#Erstellen von shared unique words (suw) von Parteipaaren
'''
rows, cols = (len(uw_all), len(uw_all))
suw = [[0 for i in range(cols)] for j in range(rows)]
suw_words = [[0 for i in range(cols)] for j in range(rows)]
for ix,p1 in enumerate(uw_all.keys()):
    for jx,p2 in enumerate(uw_all.keys()):
        if jx > ix:
            print(p1,p2)
            tmp = return_unique_words([p1,p2],reden_gefiltert) - return_unique_words(p1,reden_gefiltert) - return_unique_words(p2,reden_gefiltert)
            suw_words[ix][jx] = tmp
            suw[ix][jx] = len(tmp)
            suw[jx][ix] = suw[ix][jx]

print(suw)

#0 SPD, 1 FDP, 2 CDU/CSU, 3 Linke, 4 Grüne, 5 AfD

#Die unique words eines bestimmten Parteienpaares lassen sich jetzt mit Angabe der Parteitabellenplatzzahlen öffnen.

#print(suw_words[0][1])

#print(uw_all.keys())
#0 SPD, 1 FDP, 2 CDU/CSU, 3 Linke, 4 Grüne, 5 AfD
'''

#wortlisten zu satzlisten erweitern
#unique words vergleichen von 19 und 20 (überschnitt?)
