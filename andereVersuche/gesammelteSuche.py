import json
import os

suchwoerter = ["Klima", "klima"]  # Die Wörter, nach denen du suchen möchtest
ergebnisse = {}  # Ein Dictionary, um die Ergebnisse zu speichern

# Pfade zu den JSON-Dateien
verzeichnis = "results"  # Das Verzeichnis, in dem die JSON-Dateien gespeichert sind
dateien = os.listdir(verzeichnis)

for datei in dateien:
    if datei.endswith(".json"):
        # Extrahiere den Schlüssel (party) aus dem Dateinamen
        suchschluessel = datei.split("_")[1]

        with open(os.path.join(verzeichnis, datei), 'r') as file:
            data = json.load(file)

            gefunden_in_datei = []  # Liste, um gefundene Wörter in dieser Datei zu speichern

            # Durchsuche die Wörter in der Liste unter dem angegebenen Schlüssel
            if suchschluessel in data:
                wortliste = data[suchschluessel]
                for wort in wortliste:
                    for suchwort in suchwoerter:
                        if suchwort in wort:
                            gefunden_in_datei.append(wort)

            # Füge die gefundenen Wörter zur Liste der Ergebnisse hinzu
            ergebnisse[suchschluessel] = gefunden_in_datei

# Speichere die Ergebnisse in einer JSON-Datei
with open("ergebnisse.json", "w", encoding="utf-8") as json_output:
    json.dump(ergebnisse, json_output, indent=4, ensure_ascii=False)
