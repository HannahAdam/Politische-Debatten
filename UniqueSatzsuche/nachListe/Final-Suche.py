# Info: 

# Dieser Code dient dazu, die vollständigen Satze zu den einzigartigen Worten zu finden.

# Das ist wichtig, um die gefundenen Begriffen in einen Kontext zu setzten. 
# Dieser Teil ist deshalb relevant, weil er explizit zeigt, wie die verschiedenen Parteien Sprache 
# (insbesondere Wortzusammensetzungen) verwenden. 

# Hinweis:

# Der Dateipfad zu den Listen (absoluter_dateipfad_suchwoerter =) muss manuell angepasst werden, 
# je nach dem für welche Liste ist ganzen Sätze gefunden werden sollen. 

# Die Listen müssen außerdem manuell umbenannt werden. 
# Das muss sein, weil die Namen, welche durch das erstellen generiert wurden, nicht gelesen werden können.
# Beispiel: Den Dateinamen ['Zwang', 'zwang']ergebnisse.json  zu  Zwang-zwang-ergebnisse.json  umbenennen.

# Der Name für die neue Datei muss auch manuell angepasst werden (bei # Speichern Sie das gesamte Ergebnis in einer JSON-Datei), 
# sonst würde eine, vorher mit dem Code erstellte, Datei überschrieben werden. 
# Beispiel: schein-ergebnisse.json -> zwang-ergebnisse.json


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

        reden_gefiltert[rede['party']].append(rede)

    # Initialisieren eines leeren Trefferdictionaries
    treffer = {}

    # Durchsuchen der Reden nach den Suchwörtern und Sammeln der Sätze mit den gesuchten Wörtern
    for partei, reden in reden_gefiltert.items():
        treffer[partei] = {}

        for wort in suchwoerter_dict.get(partei, []):
            treffer[partei][wort] = []

            for rede in reden:
                saetze = nltk.sent_tokenize(rede['text'])
                for satz in saetze:
                    if re.search(rf'\b{wort}\b', satz, flags=re.IGNORECASE):
                        treffer[partei][wort].append({'name': rede['name'], 'party': rede['party'], 'satz': satz})

    return treffer

def sammle_und_speichere_ergebnisse():
    # Verwenden Sie den absoluten Dateipfad, z.B. zur "Pseudo-pseudo-ergebnisse.json"-Datei
    absoluter_dateipfad_suchwoerter = '/Users/hannahadam/PycharmProjects/pythonProject/HelloWorld/results/vergleich/Schein-schein-ergebnisse.json'

    # Laden der Suchwörter aus der JSON-Datei
    with open(absoluter_dateipfad_suchwoerter, 'r', encoding='utf-8') as json_file:
        suchwoerter_dict = json.load(json_file)

    treffer_legislatur_19 = suche_in_reden(19, suchwoerter_dict)
    treffer_legislatur_20 = suche_in_reden(20, suchwoerter_dict)

    # Ergebnisse sammeln
    ergebnisse = {}

    for partei in treffer_legislatur_19.keys():
        ergebnisse[partei] = {}
        for wort in suchwoerter_dict.get(partei, []):
            saetze_19 = treffer_legislatur_19[partei].get(wort, [])
            saetze_20 = treffer_legislatur_20[partei].get(wort, [])

            # Überprüfen, ob es Ergebnisse in Legislatur 19 gibt
            if saetze_19:
                # Wenn es Ergebnisse in Legislatur 20 gibt, fügen Sie sie hinzu
                if saetze_20:
                    ergebnisse[partei][wort] = {
                        'Legislatur 19': saetze_19,
                        'Legislatur 20': saetze_20
                    }
                else:
                    ergebnisse[partei][wort] = {'Legislatur 19': saetze_19}
            # Wenn es Ergebnisse in Legislatur 20 gibt, fügen Sie sie hinzu
            elif saetze_20:
                ergebnisse[partei][wort] = {'Legislatur 20': saetze_20}

    # Speichern Sie das gesamte Ergebnis in einer JSON-Datei
    with open(f"results/worte-final/schein-ergebnisse.json", "w", encoding="utf-8") as json_output:
        json.dump(ergebnisse, json_output, indent=4, ensure_ascii=False)


# Aufruf der Funktion, um die Ergebnisse zu sammeln und in einer Datei zu speichern
sammle_und_speichere_ergebnisse()
