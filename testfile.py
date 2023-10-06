import jsonlines
import nltk
nltk.data.path.append("/Users/hannahadam/PycharmProjects/pythonProject/HelloWorld/venv/nltk_data")
nltk.download('punkt')

'''
from collections import Counter

# Hier legen wir fest, welche Daten (Wahlperiode 19 oder 20) wir laden:
legislatur = 20

# Wir generieren eine leere Liste:
alleReden = []

# Wir öffnen den entsprechende File (Dateipfad anpassen!):
with jsonlines.open(f'/Users/hannahadam/Desktop/bundestag/data/speeches_{legislatur}.jsonl') as f:
    for line in f.iter():
        # Wir packen alles Zeile für Zeile zu unserer Liste:
        alleReden.append(line)

# Wir sortieren nach Datum:
alleReden.sort(key=lambda x: x['date'])

# Wir lassen uns zeigen, wie viele Reden enthalten sind.
print(f'Die Liste enthält {len(alleReden)} Reden')
# Neue Zeile auf der Konsole:
print(f'\n')


## Zunächst brauchen wir eine Funktion, die uns die Reden gibt, die ein bestimmtes Wort enthalten.
#  Funktion für Textsuche:
#  Gibt eine Untermenge an Reden zurück, die einen bestimmten String (Wort) enthalten.

def find_speeches_with_word(search_term, speeches):
    filtered_speeches = []
    for speech in speeches:
        if (search_term in speech['text']):
            filtered_speeches.append(speech)
    return filtered_speeches


## Probieren wir das mal aus.
#  Das ist unser Suchwort (oder String):
wort = 'letzte Generation'
# wort = 'Kapital'

#  Hier rufen wir die Suchfunktion auf und speichern die Untermenge der Reden.
untermenge = find_speeches_with_word(wort, alleReden)

# Wir lassen uns zeigen, wie viele Reden enthalten sind.
print(f'Diese Liste (Suche nach {wort}) enthält {len(untermenge)} Reden.')
# Neue Zeile auf der Konsole:
print(f'\n')


## Reden sind lang und die Worte tauchen in verschiedenen Kontexten auf.
#  Wir würden gerne alle Sätze sehen, in denen der Suchbegriff vorkommt.
#  Aber natürlich kommt unser Suchstring nur in Sätzen vor, die in de Untermenge an Reden sind.

def find_sentences_with_word(search_term, speeches):
    sents_with_words = []
    for speech in speeches:
        sent_list = nltk.sent_tokenize(speech['text'])
        for sent in sent_list:
            if search_term in sent:
                sents_with_words.append(sent)
    return sents_with_words


# Probieren wir diese Funktion einmal aus:
satz_liste = find_sentences_with_word(wort, untermenge)

# Wir lassen uns zeigen, wie viele Sätze in der Liste enthalten sind.
print(f'Diese Liste (Suche nach {wort}) enthält {len(satz_liste)} Sätze')
# Neue Zeile auf der Konsole:
print(f'\n')

# Wollen wir uns die alle anzeigen lassen? Ja oder Nein?
wir_wollen = False
if wir_wollen:
    for satz in satz_liste:
        print(satz)


## Nun wäre es doch spannend, die Reden einer Partei oder eines Politikers zu sehen.
#  Dazu entwickeln wir eine Funktion, die es erlaubt, in den anderen Felder (keys) zu suchen.
#  Funktion, mit der man eine Menge an Reden nach verschiedenen Kriterien filtern kann.
#  Es wird die entsprechende Untermenge zurückgegeben.
#  'what' enthält den Key, wo gesucht werden soll. Interessant vor allem: 'name' und 'party'

def filter_speeches_for(what, search_term, speeches):
    filtered_speeches = []
    for speech in speeches:
        if search_term in speech[what]:
            filtered_speeches.append(speech)

    filtered_speeches.sort(key=lambda x: x['date'])
    return filtered_speeches


# Beispiel: Für alle Reden von Olaf Scholz:
suche_nach = 'Olaf Scholz'
untermenge = filter_speeches_for('name', suche_nach, alleReden)
# Wir lassen uns zeigen, wie viele Reden enthalten sind.
print(f'Diese Liste (Suche nach {suche_nach}) enthält {len(untermenge)} Reden')
print(f'\n')

####
## Jetzt könnten wir die Sätze von Olaf Scholz mit einem bestimmten Wort anschauen.
#  Das ist unser Suchwort (oder String):
# wort = 'Klimawandel'
wort = 'Klimakrise'

#  Hier rufen wir die Suchfunktion auf und speichern die Untermenge der Reden.
untermenge = find_speeches_with_word(wort, alleReden)

# Wir suchen nach:
suche_nach = 'Olaf Scholz'
untermenge = filter_speeches_for('name', suche_nach, untermenge)
satz_liste = find_sentences_with_word(wort, untermenge)

print(f'In {len(untermenge)} Reden gibt es {len(satz_liste)} Sätze von {suche_nach}, die {wort} enthalten:')
print(f'\n')

# Die schauen wir uns an.
for sx, satz in enumerate(satz_liste):
    print(f' Satz {sx + 1}: {satz}')
    print(f'\n')

'''

