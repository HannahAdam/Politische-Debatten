import json
import jsonlines
import nltk
import re
from collections import Counter

# Hier legen wir fest, welche Daten (Wahlperioden 19 und 20) wir laden möchten:
legislaturen = [19, 20]

# Wir generieren eine leere Liste:
alleReden = []

# Für jede Legislaturperiode die entsprechende Datei öffnen und die Daten in die Liste hinzufügen:
for legislatur in legislaturen:
    with jsonlines.open(f'/Users/hannahadam/Desktop/bundestag/data/speeches_{legislatur}.jsonl') as f:
        for line in f.iter():
            alleReden.append(line)

# Wir sortieren nach Datum:
alleReden.sort(key=lambda x: x['date'])

# Wir lassen uns zeigen, wie viele Reden enthalten sind.
print(f'Die Liste enthält {len(alleReden)} Reden')
# Neue Zeile auf der Konsole:
print(f'\n')

# Liste der Suchbegriffe
suchbegriffe = ['Anti-ismus', 'Anti-AfD-Einheitsblock', 'Anti-AfD-Prinzip','Anti-Deutschland-Koalition', 'Antikernkraftwahn']

def find_speeches_with_words(search_terms, speeches):
    filtered_speeches = []
    for speech in speeches:
        for term in search_terms:
            if (term in speech['text']):
                filtered_speeches.append(speech)
                break  # Um doppelte Einträge zu vermeiden, brechen wir die Schleife ab, sobald ein Suchbegriff gefunden wurde
    return filtered_speeches

# Hier rufen wir die Suchfunktion auf und speichern die Untermenge der Reden.
untermenge = find_speeches_with_words(suchbegriffe, alleReden)

# Reden sind lang und die Worte tauchen in verschiedenen Kontexten auf.
# Wir würden gerne alle Sätze sehen, in denen die Suchbegriffe vorkommen.
# Aber natürlich kommen die Suchbegriffe nur in Sätzen vor, die in der Untermenge an Reden sind.

def find_sentences_with_words(search_terms, speeches):
    sents_with_words = []
    for speech in speeches:
        sent_list = nltk.sent_tokenize(speech['text'])
        for sent in sent_list:
            for term in search_terms:
                if re.search(rf'\b{term}\b', sent, flags=re.IGNORECASE):
                    sents_with_words.append({"Wort": term, "Satz": sent, "Name": speech['name'], "Partei": speech['party'], "Datum": speech['date']})
    return sents_with_words

# Probieren wir diese Funktion einmal aus:
satz_liste = find_sentences_with_words(suchbegriffe, untermenge)

# Dateipfad und Dateiname, in dem die Ergebnisse gespeichert werden sollen
output_file_path = "results/wortsuche-einzeln/anti-ergebnisse.json"

# Speichern Sie das gesamte Ergebnis in einer JSON-Datei
with open(output_file_path, "w", encoding="utf-8") as json_output:
    json.dump(satz_liste, json_output, indent=4, ensure_ascii=False)

print(f"Die Ergebnisse wurden in '{output_file_path}' gespeichert.")
