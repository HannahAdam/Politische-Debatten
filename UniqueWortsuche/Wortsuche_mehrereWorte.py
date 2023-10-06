# Infos:

# Dieser Code dient dazu, die bereits generierten Wortlisten (UniqueWords) 
# nach mehrere Suchworten für eine Partei (siehe party), 
# in einer Legislaturperiode (siehe legislatur) zu durchsuchen. 
# Dieser Code speichert die gefundenen Begriffe (Bsp: Ad-hoc-Koalitionen), 
# die das Suchwort (Bsp: koalition) enthalten, in einer neuen Liste. 

# Hinweise: 

# Dateipfade müssen angepasst werden. 
# Suchwörter können geändert werden werden. 

# Damit die Dateien gespeichert werden können, 
# müssen die entsprechenden Ordner 
# results/wortsuche/{party}/{legislatur}/{suchwort}_{party}_{legislatur}
# angelegt sein. 
# Lege neben den gleichbleibenden Namen auch alle Ordner für die sich ändernden Angaben an 
# Ordner mit den Namen: AfD, CDU_CSU, DIE LINKE, BÜNDNIS 90_DIE GRÜNEN, SPD
# jeweils einen Ordner 19 und einen Ordner 20 



import json

party = 'AfD'
#party = 'CDU_CSU'
#party = 'DIE LINKE'
#party = 'BÜNDNIS 90_DIE GRÜNEN'
#party = 'SPD'

legislatur = 19
#legislatur = 20

with open(f'results/_{party}_{legislatur}.json', 'r') as file:
    data = json.load(file)


# Wir lassen uns zeigen, wie viele Worte in der Liste enthalten sind.
print(f'Die Liste der Partei {party} aus der Legislatur {legislatur} enthält {len(data[party])} Unique Words')

# Schlüssel, nach dem gesucht werden soll
suchschluessel = party

suchwoerter = ["fanatik","Fanatik"]  # Die Wörter, nach denen du suchen möchtest
anzahl_gefundener_woerter = {wort: 0 for wort in suchwoerter}  # Ein Wörterbuch, um die Anzahl der Vorkommen jedes Wortes zu speichern
gefundene_woerter = []

# Durchsuche die Wörter in der Liste unter dem angegebenen Schlüssel
if suchschluessel in data:
    wortliste = data[suchschluessel]
    for wort in wortliste:
        for suchwort in suchwoerter:
            if suchwort in wort:
                anzahl_gefundener_woerter[suchwort] += 1
                wort = wort.replace(u'\xa0', u' ')  # Ersetze unerwünschte Zeichen im Wort
                gefundene_woerter.append(wort)

# Zeige die Anzahl der Vorkommen jedes Wortes an
for wort, anzahl in anzahl_gefundener_woerter.items():
    if anzahl > 0:
        print(f"Das Wort '{wort}' wurde {anzahl} mal in der Liste der Partei {suchschluessel} aus der Legislatur {legislatur} gefunden.")

# Zeige die gefundenen Wörter selbst an
if gefundene_woerter:
    print("Gefundene Begriffe:")
    for wort in gefundene_woerter:
        print(wort)
else:
    print(f"Keines der gesuchten Wörter wurde in der Liste der Partei {suchschluessel} aus der Legislatur {legislatur} gefunden.")

# Ersetze unerwünschte Zeichen in den gefundenen Wörtern
gefundene_woerter = [wort.replace(u'\xa0', u' ') for wort in gefundene_woerter]
gefundene_woerter = [wort.replace(u'/', u'_') for wort in gefundene_woerter]

# Speichere die gefundenen Wörter in einer JSON-Datei
# Damit die JSON-Dateien gespeichert werden können, müssen die entsprechenden Ordner (siehe Pfad) angelegt sein
gefundene_woerter_dict = {"Gefundene Begriffe": gefundene_woerter}
with open(f"results/wortsuche/{party}/{legislatur}/{suchwort}_{party}_{legislatur}.json", "w", encoding="utf-8") as json_output:
    json.dump(gefundene_woerter_dict, json_output, indent=4, ensure_ascii=False)
