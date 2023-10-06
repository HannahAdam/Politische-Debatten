import json
import jsonlines

from collections import Counter     # um worte zu zählen
import matplotlib.pyplot as plt     # Für Visualisierung

legislatur = 20

alleReden = []
with jsonlines.open(f'/Users/hannahadam/Desktop/bundestag/data/speeches_{legislatur}.jsonl') as f:
    for line in f.iter():
    #for line in list(f):
        alleReden.append(line)

alleReden.sort(key = lambda x:x['date'])

# Wir lassen uns zeigen, wie viele Reden enthalten sind.
print(f'Die Liste enthält {len(alleReden)} Reden')
# Neue Zeile auf der Konsole:
print(f'\n')

################# FUNKTIONEN #####################

# Zunächst brauchen wir eine Funktion, die uns die Reden gibt, die ein bestimmtes Wort enthalten.
#  Funktion für Textsuche:
#  Gibt eine Untermenge an Reden zurück, die einen bestimmten String (Wort) enthalten.

def find_speeches_with_word(search_term, speeches):
    filtered_speeches = []
    for speech in speeches:
        if ( search_term in speech['text'] ):
            filtered_speeches.append(speech)
    return filtered_speeches

# Reden sind lang und die Worte tauchen in verschiedenen Kontexten auf.
#  Wir würden gerne alle Sätze sehen, in denen der Suchbegriff vorkommt.
#  Aber natürlich kommt unser Suchstring nur in Sätzen vor, die in de Untermenge an Reden sind.

def find_sentences_with_word(search_term, speeches):
    sents_with_word = []
    for speech in speeches:
        sent_list = nltk.sent_tokenize(speech['text'])
        for sent in sent_list:
            if search_term in sent:
                sents_with_word.append(sent)
    return sents_with_word


# Nun wäre es doch spannend, die Reden einer Partei oder eines Politikers zu sehen.
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

################ Anwendung ################

such_wort1 = 'Flüchtling'
such_wort2 = 'Geflüchtete'

#such_wort1 = 'Putin'
#such_wort2 = 'Selenskyj'

#such_wort1 = 'Krieg gegen die Ukraine'
#such_wort2 = 'Ukraine-Krieg'

parties = ['SPD', 'FDP', 'CDU', 'LINKE', 'GRÜNEN', 'AfD', 'unknown']  # sind die richtig geschrieben?

frequencies1 = []
for party in parties:
    untermenge = find_speeches_with_word(such_wort1, alleReden)
    untermenge = filter_speeches_for('party', party, untermenge)
    print(f'Die {party} hat {len(untermenge)} Reden mit "{such_wort1}" gehalten.')
    frequencies1.append(len(untermenge))

print('\n')
frequencies2 = []
for party in parties:
    untermenge = find_speeches_with_word(such_wort2, alleReden)
    untermenge = filter_speeches_for('party', party, untermenge)
    print(f'Die {party} hat {len(untermenge)} Reden mit "{such_wort2}" gehalten.')
    frequencies2.append(len(untermenge))

'''
# Wir wollen das Ergebnis natürlich auch visualisieren
# Das machen wir mit matplotlib.pyplot (ganz oben als plt importiert)

plt.bar(parties, frequencies1, label=f'{such_wort1}')
plt.bar(parties, frequencies2, bottom=frequencies1, label=f'{such_wort2}')
plt.title("Verteilung der Häufigkeiten")
plt.xlabel("Partei")
plt.ylabel("Anzahl der Reden")
plt.legend(loc="upper left")


plt.show()
'''
