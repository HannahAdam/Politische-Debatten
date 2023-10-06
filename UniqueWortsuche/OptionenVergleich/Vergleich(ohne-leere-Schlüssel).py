# Info:

# Dieser Code ist eine Variation von der python file "VergleichSuche.py"
# Anders ist: Hier werden die leeren Schlüssel nicht aufgelistet. 
# Stattdessen gibt es einen Infotext darüber, dass die Suche dennoch für alle Parteien durchgeführt wurde.
# Wenn die Partei nicht aufgelistet ist, wurde das Suchwort in ihren Reden nicht verwendet

import json
import os

suchwoerter = ["Hyster", "hyster"]  # Die Wörter, nach denen du suchen möchtest
ergebnisse = {}  # Ein Dictionary, um die Ergebnisse zu speichern

# Pfade zu den JSON-Dateien
verzeichnis = "results"  # Das Verzeichnis, in dem die JSON-Dateien gespeichert sind
dateien = os.listdir(verzeichnis)

# Alle verfügbaren Schlüssel initialisieren
verfuegbare_schluessel = set()

for datei in dateien:
    if datei.endswith(".json"):
        # Extrahiere den Schlüssel (party) aus dem Dateinamen
        datei_teile = datei.split("_")
        if len(datei_teile) >= 3:
            suchschluessel = "_".join(datei_teile[1:-1])  # Alle Teile außer dem ersten und letzten
        else:
            # Der Dateiname hat nicht das erwartete Format
            continue

        # Entferne Leerzeichen am Anfang und Ende des Schlüssels
        suchschluessel = suchschluessel.strip()

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
            if gefunden_in_datei:
                if suchschluessel in ergebnisse:
                    ergebnisse[suchschluessel].extend(gefunden_in_datei)
                else:
                    ergebnisse[suchschluessel] = gefunden_in_datei

            # Füge den Schlüssel zur Liste der verfügbaren Schlüssel hinzu
            verfuegbare_schluessel.add(suchschluessel)


# Speichern Sie das Ergebnis in einer JSON-Datei
with open(f"results/vergleich/{suchwoerter}ergebnisse.json", "w", encoding="utf-8") as json_output:
    # Schreiben Sie die Information am Anfang des Dokuments
    json_output.write('{In dieser Datei werden nur die Parteien aufgelistet, bei welchen das Suchwort gefunden wurde. Die Suche wurde dennoch bei allen Parteien durchgeführt. Wenn die Partei nicht aufgelistet ist, wurde das Suchwort in ihren Reden nicht verwendet.}\n\n')

    # Schreiben Sie den Rest des JSON-Daten ohne die Information
    json.dump(ergebnisse, json_output, indent=4, ensure_ascii=False)
