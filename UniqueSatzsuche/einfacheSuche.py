import json
import re
import nltk

def suche_in_reden(legislatur, suchwoerter_dict):
    # Laden der Reden aus der JSON-Datei
    dateipfad_reden = f'/Users/hannahadam/Desktop/bundestag/data_preprocessed/speeches_{legislatur}_preprocessed.json'

    with open(dateipfad_reden, 'r', encoding='utf-8') as json_file:
        alleReden = json.load(json_file)

    # Reden nach Parteien sortieren und zu Parteitexten zusammenfügen
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

        reden_gefiltert[rede['party']].append(rede['text'])

    # Initialisieren eines leeren Trefferdictionaries
    treffer = {}

    # Durchsuchen der Reden nach den Suchwörtern und Sammeln der Sätze mit den gesuchten Wörtern
    for partei, reden in reden_gefiltert.items():
        treffer[partei] = {}

        # Aufteilen der Texte in Sätze
        saetze = nltk.sent_tokenize(" ".join(reden))
        #saetze = nltk.sent_tokenize(reden)

        for wort in suchwoerter_dict.get(partei, []):
            treffer[partei][wort] = []


            # Durchsuchen der Sätze nach den gesuchten Wörtern
            for satz in saetze:
                if re.search(rf'\b{wort}\b', satz, flags=re.IGNORECASE):
                    treffer[partei][wort].append(satz)

    return treffer

legislatur = 19

# Verwenden Sie den absoluten Dateipfad zur "['Pseudo', 'pseudo']ergebnisse.json"-Datei
absoluter_dateipfad_suchwoerter = '/Users/hannahadam/PycharmProjects/pythonProject/HelloWorld/results/vergleich/Pseudo-pseudo-ergebnisse.json'

# Laden der Suchwörter aus der JSON-Datei
with open(absoluter_dateipfad_suchwoerter, 'r', encoding='utf-8') as json_file:
    suchwoerter_dict = json.load(json_file)

treffer = suche_in_reden(legislatur, suchwoerter_dict)

# Ergebnisse anzeigen
for partei, worttreffer in treffer.items():
    print(f"{partei}:")
    for wort, saetze in worttreffer.items():
        print(f"    {wort}:")
        for satz in saetze:
            print(f"        {satz}")
