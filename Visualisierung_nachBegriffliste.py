import json
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Verwenden Sie den absoluten Dateipfad zum Beispiel zur "Pseudo-pseudo-ergebnisse.json"-Datei
# Hinweis: Der Dateiname muss angepasst werden, weil in python Anführungsstriche im Namen zu Problemen führen.
# Deshalb muss zum Beispiel die Datei ['Beweis', 'beweis']ergebnisse.json stattdessen in Beweis-beweis-ergebnisse.json umbenannt werden.

absoluter_dateipfad_suchwoerter = '/Users/hannahadam/PycharmProjects/pythonProject/HelloWorld/results/vergleich/Beweis-beweis-ergebnisse.json'

# Laden der Suchwörter aus der JSON-Datei
with open(absoluter_dateipfad_suchwoerter, 'r', encoding='utf-8') as json_file:
    suchwoerter_dict = json.load(json_file)

# Extrahiere die Suchwörter aus dem JSON-Objekt
dokument_begriffe = []
for partei, begriffe in suchwoerter_dict.items():
    dokument_begriffe.extend(begriffe)

# Füge die Dokumentbegriffe zum Text hinzu:
text = " ".join(dokument_begriffe)

# Erzeuge die Word Cloud
wordcloud = WordCloud(background_color="white").generate(text)

# Ermittle den häufigsten Begriff in der Word Cloud
häufigster_begriff = wordcloud.process_text(text).items()
häufigster_begriff = max(häufigster_begriff, key=lambda x: x[1])[0]

# Zeige die Word Cloud an
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")  # Deaktiviere die Achsenanzeige

# Speichern Sie die Word Cloud als Bild mit dem häufigsten Begriff im Dateinamen
wordcloud.to_file(f"results/vergleich/visual/{häufigster_begriff}_wordcloud.png")

# Anzeige der Word Cloud (optional)
plt.show()