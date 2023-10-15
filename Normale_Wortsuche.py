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
suchbegriffe = ['Klimaangst']

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
                    sents_with_words.append((term, sent, speech))
    return sents_with_words

# Probieren wir diese Funktion einmal aus:
satz_liste = find_sentences_with_words(suchbegriffe, untermenge)

# Wir lassen uns zeigen, wie viele Sätze in der Liste enthalten sind.
print(f'Diese Liste enthält {len(satz_liste)} Sätze:')
print(f'\n')

# Wollen wir uns die alle anzeigen lassen? Ja oder Nein?
wir_wollen = True
if wir_wollen:
    for term, satz, speech in satz_liste:
        print(f"Wort: {term}")
        print(f"Satz: {satz}")
        print(f"Name: {speech['name']}, Partei: {speech['party']}, Datum: {speech['date']}")
        print()