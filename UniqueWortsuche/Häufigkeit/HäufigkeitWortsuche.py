import json
import re
from collections import Counter
import nltk

def suche_und_zaehle_haeufigkeit(legislatur, suchwoerter_dict):
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

        reden_gefiltert[rede['party']].append(rede)

    # Durchsuchen der Reden nach den Suchwörtern und Zählen der Treffer
    treffer_haeufigkeit = {}

    for partei, reden in reden_gefiltert.items():
        # Die folgenden Zeilen entfernen Parteien ohne Treffer
        if not suchwoerter_dict.get(partei):
            continue

        treffer_haeufigkeit[partei] = Counter()

        for wort in suchwoerter_dict.get(partei, []):
            for rede in reden:
                saetze = nltk.sent_tokenize(rede['text'])
                for satz in saetze:
                    if re.search(rf'\b{wort}\b', satz, flags=re.IGNORECASE):
                        treffer_haeufigkeit[partei][wort] += 1

    return treffer_haeufigkeit

def finde_top5_haeufige_worte():
    # Verwenden Sie den absoluten Dateipfad zur "Pseudo-pseudo-ergebnisse.json"-Datei
    absoluter_dateipfad_suchwoerter = '/Users/hannahadam/PycharmProjects/pythonProject/HelloWorld/results/vergleich/Klima-klima-ergebnisse.json'

    # Laden der Suchwörter aus der JSON-Datei
    with open(absoluter_dateipfad_suchwoerter, 'r', encoding='utf-8') as json_file:
        suchwoerter_dict = json.load(json_file)

    treffer_haeufigkeit_legislatur_19 = suche_und_zaehle_haeufigkeit(19, suchwoerter_dict)
    treffer_haeufigkeit_legislatur_20 = suche_und_zaehle_haeufigkeit(20, suchwoerter_dict)

    # Ergebnisse sammeln und die fünf häufigsten Wörter pro Partei über beide Legislaturperioden finden
    ergebnisse_top5 = {}

    for partei in treffer_haeufigkeit_legislatur_19.keys():
        # Die folgenden Zeilen entfernen Parteien ohne Treffer
        if not suchwoerter_dict.get(partei):
            continue

        ergebnisse_top5[partei] = {}
        alle_haeufigkeiten = treffer_haeufigkeit_legislatur_19[partei] + treffer_haeufigkeit_legislatur_20[partei]
        top5_haeufige_worte = alle_haeufigkeiten.most_common(5)
        ergebnisse_top5[partei] = dict(top5_haeufige_worte)

    # Speichern Sie die fünf häufigsten Wörter pro Partei in einer JSON-Datei
    with open(f"results/count-visual/top5_haeufige_klima.json", "w", encoding="utf-8") as json_output:
        json.dump(ergebnisse_top5, json_output, indent=4, ensure_ascii=False)

# Aufruf der Funktion, um die fünf häufigsten Wörter pro Partei zu finden und in einer Datei zu speichern
finde_top5_haeufige_worte()
