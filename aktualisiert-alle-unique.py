import jsonlines
import json
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from PIL import Image
import numpy as np
from collections import Counter
import networkx as nx
import os

#Importieren der lemmatisierten Reden

def laden_alleReden(legislatur):
    with open(f'/Users/hannahadam/Desktop/bundestag/data_preprocessed/speeches_{legislatur}_preprocessed.json', 'r') as fp:
        data = json.load(fp)

    return data.copy()

legislatur = 20
alleReden = laden_alleReden(legislatur)

#print(alleReden[0])

#Reden nach Parteien sortieren und zu Parteitexten zusammenfügen

reden_gefiltert = {'CDU_CSU': [],
                   'SPD': [],
                   'AfD': [],
                   'FDP': [],
                   'BÜNDNIS 90_DIE GRÜNEN': [],  # Parteiname mit Leerzeichen
                   'DIE LINKE': [],
                   'fraktionslos': [],
                   'Bremen': [],
                   'unknown': []
                   }

for rede in alleReden:
    rede['party'] = rede['party'].replace(u'\xa0', u' ')
    rede['party'] = rede['party'].replace(u'/', u'_')
    if rede['party'] == 'Bündnis 90_Die Grünen':
        rede['party'] = 'BÜNDNIS 90_DIE GRÜNEN'  # Parteiname mit Leerzeichen
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
'BÜNDNIS 90_DIE GRÜNEN': return_unique_words('BÜNDNIS 90_DIE GRÜNEN',reden_gefiltert),  # Parteiname mit Leerzeichen
'AfD': return_unique_words('AfD',reden_gefiltert)
}

# Anpassung des Dateinamens für die JSON-Datei
angepasster_dateiname = "DIE LINKE"  # Verwende den gleichen Schlüssel wie in den Daten

print(uw_all[angepasster_dateiname])

len(uw_all[angepasster_dateiname])

# Speicherpfad für die JSON-Dateien
speicherpfad = "results"

# Überprüfe, ob der Speicherpfad vorhanden ist, andernfalls erstelle ihn
if not os.path.exists(speicherpfad):
    os.makedirs(speicherpfad)

# Speichere die Unique Words in JSON-Dateien mit angepasstem Dateinamen
# Hier wird der Schlüssel im JSON-Objekt angepasst
angepasster_dateiname_speichern = "DIE_LINKE"  # Anpassung für die Speicherung

dateiname = f"_{angepasster_dateiname_speichern}_{legislatur}.json".replace(" ", "_")

# Erstelle den vollen Pfad zur JSON-Datei
dateipfad = os.path.join(speicherpfad, dateiname)

# Speichere die Unique Words in der JSON-Datei
with open(dateipfad, 'w', encoding='UTF8') as fp:
    json.dump({angepasster_dateiname_speichern: list(uw_all[angepasster_dateiname])}, fp, sort_keys=True, indent=4, ensure_ascii=False)