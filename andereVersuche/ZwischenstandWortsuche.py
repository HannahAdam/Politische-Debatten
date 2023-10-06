import json

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

        reden_gefiltert[rede['party']].extend(rede['text_lem'])

    # Initialisieren eines leeren Trefferdictionaries
    treffer = {}

    # Durchsuchen der Reden nach den Suchwörtern
    for partei, reden in reden_gefiltert.items():
        treffer[partei] = {}
        for wort in suchwoerter_dict.get(partei, []):
            treffer[partei][wort] = reden.count(wort)

    return treffer

# Liste der Legislaturperioden
legislatur_perioden = [19, 20]

# Verwenden Sie den absoluten Dateipfad zur "['Pseudo', 'pseudo']ergebnisse.json"-Datei
absoluter_dateipfad_suchwoerter = f'/Users/hannahadam/PycharmProjects/pythonProject/HelloWorld/results/vergleich/Pseudo-pseudo-ergebnisse.json'

# Laden der Suchwörter aus der JSON-Datei
with open(absoluter_dateipfad_suchwoerter, 'r', encoding='utf-8') as json_file:
    suchwoerter_dict = json.load(json_file)

# Initialisieren eines leeren Trefferdictionaries für beide Perioden kombiniert
gesamt_treffer = {}

# Durchsuchen der Reden für beide Perioden
for legislatur in legislatur_perioden:
    treffer = suche_in_reden(legislatur, suchwoerter_dict)

    # Fügen Sie die Treffer für diese Legislatur zur Gesamttrefferliste hinzu
    for partei, worttreffer in treffer.items():
        if partei not in gesamt_treffer:
            gesamt_treffer[partei] = {}
        for wort, anzahl in worttreffer.items():
            if wort not in gesamt_treffer[partei]:
                gesamt_treffer[partei][wort] = 0
            gesamt_treffer[partei][wort] += anzahl

# Überprüfen Sie, ob für jedes Wort mindestens ein Treffer gefunden wurde
alle_woerter_gefunden = all(all(anzahl > 0 for anzahl in worttreffer.values()) for worttreffer in gesamt_treffer.values())

if alle_woerter_gefunden:
    print("Für jedes Wort wurde mindestens ein Treffer gefunden.")
else:
    print("Es wurden nicht für jedes Wort mindestens ein Treffer gefunden.")

# Ergebnisse anzeigen
for partei, worttreffer in gesamt_treffer.items():
    print(f"{partei}:")
    for wort, anzahl in worttreffer.items():
        print(f"    {wort}: {anzahl} Treffer")
