import matplotlib.pyplot as plt
import json

# Laden der JSON-Datei mit den Daten
with open('results/count-visual/top5_haeufige_klima.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Extrahieren der Daten nur für die AfD
afd_data = data.get('AfD', {})

# Überprüfen, ob Daten für die AfD vorhanden sind
if afd_data:
    # Extrahieren der Wörter und ihrer Häufigkeit
    words = list(afd_data.keys())
    frequency = list(afd_data.values())

    # Erstellen des Bar-Charts
    plt.figure(figsize=(10, 6))
    plt.bar(words, frequency, color='#009ee0')
    plt.xlabel('Pseudo-Wörter')
    plt.ylabel('Häufigkeit')
    plt.title('Häufigkeit der Klima-Wörter in AfD-Reden')
    plt.xticks(rotation=45)

    # Speichern des Bar-Charts als Bild
    plt.tight_layout()
    plt.savefig('results/count-visual/Bilder/afd_klima_wort_haeufigkeit.png')

    # Anzeigen des Bar-Charts
    plt.show()
else:
    print("Keine Daten für die AfD gefunden.")