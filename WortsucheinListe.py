import json

party='AfD'
legislatur=19

with open(f'results/_{party}_{legislatur}.json', 'r') as file:
    data = json.load(file)

# Wir lassen uns zeigen, wie viele Worte in der Liste enthalten sind.
print(f'Die Liste enthält {len(data[party])} Unique Words')

# Schlüssel, nach dem gesucht werden soll
suchschluessel = party

suchwort = ("Koalition")  # Das Wort, nach dem du suchen möchtest
gefundene_woerter = []
anzahl_gefundener_woerter = 0  # Zählvariable für die Anzahl der Übereinstimmungen

# Durchsuche die Wörter in der Liste unter dem angegebenen Schlüssel
if suchschluessel in data:
    wortliste = data[suchschluessel]
    for wort in wortliste:
        if suchwort in wort:
            gefundene_woerter.append(wort)
            anzahl_gefundener_woerter += 1

#wenn nur nach einem Suchwort durchsucht werden soll

if anzahl_gefundener_woerter > 0:
    print(f"Das Wort '{suchwort}' wurde {anzahl_gefundener_woerter} mal in der Liste der Partei {suchschluessel} aus der Legislatur {legislatur} gefunden.")
    for wort in gefundene_woerter:
        print(wort)
else:
    print(f"Das Wort '{suchwort}' wurde nicht in der Liste der Partei {suchschluessel} aus der Legislatur {legislatur} gefunden.")
