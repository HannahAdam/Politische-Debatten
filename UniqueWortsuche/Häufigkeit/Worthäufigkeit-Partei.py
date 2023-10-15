import json
import matplotlib.pyplot as plt

# Pfad zur JSON-Datei
dateipfad = "results/worte-final/klima-ergebnisse.json"

# Öffnen der JSON-Datei
with open(dateipfad, 'r', encoding='utf-8') as json_file:
    daten = json.load(json_file)

# Liste der Parteien
parteien = list(daten.keys())

# Erstellen Sie ein leeres Dictionary, um die Häufigkeiten nach Parteien zu zählen
partei_haeufigkeiten = {}

# Parteien, die ausgeschlossen werden sollen
ausgeschlossene_parteien = ["Bremen", "fraktionslos", "unknown"]

# Parteien, die nicht in der ausgeschlossenen Liste enthalten sind
nicht_ausgeschlossene_parteien = [partei for partei in parteien if partei not in ausgeschlossene_parteien]

# Farbcodes gemäß dem bereitgestellten Dictionary (ohne "Bremen", "fraktionslos" und "unknown")
colorcode1 = {
    'AfD': '#009ee0',
    'GRÜNE': '#46962b',
    'CDU_CSU': '#000000',
    'DIE LINKE': '#800080',
    'FDP': '#ffed00',
    'SPD': '#e3000f'
}

# Iterieren Sie durch die Parteien
for partei in nicht_ausgeschlossene_parteien:
    partei_haeufigkeiten[partei] = 0

    # Iterieren Sie durch die Wörter und zählen Sie die Vorkommen von "Regenbogen" in den Sätzen
    # Suchbegriffe hier manuell anpassen!
    for wort, legislatur_dict in daten[partei].items():
        for legislatur, saetze in legislatur_dict.items():
            for satz in saetze:
                if "Klima" in satz["satz"] or "klima" in satz["satz"]:
                    partei_haeufigkeiten[partei] += 1

# Anzeigen der Häufigkeiten nach Parteien
for partei, haeufigkeit in partei_haeufigkeiten.items():
    print(f'{partei}: {haeufigkeit} Mal das Wort "KLima" verwendet.')

# Visualisieren der Häufigkeiten nach Parteien (jede Partei in einer Farbe gemäß dem Dictionary)
parteien = list(partei_haeufigkeiten.keys())
haeufigkeiten = list(partei_haeufigkeiten.values())

# Ändern des Namens von "BÜNDNIS 90_DIE GRÜNEN" zu "GRÜNE"
parteien = [partei.replace("BÜNDNIS 90_DIE GRÜNEN", "GRÜNE") for partei in parteien]

farben_liste = [colorcode1.get(partei, 'gray') for partei in parteien]  # Verwenden Sie 'gray' für unbekannte Parteien

plt.bar(parteien, haeufigkeiten, color=farben_liste)
plt.xlabel('Partei')
plt.ylabel('Häufigkeit von "KLima"')
plt.title('Verwendung von "KLima" in Reden nach Partei')
plt.xticks(rotation=45)

# Aufruf von plt.tight_layout() vor dem Speichern des Bildes
plt.tight_layout()
plt.savefig('results/count-visual/Bilder/alle-klima-haeufigkeit.png')
plt.show()
