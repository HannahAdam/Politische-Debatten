import json

party='AfD'
legislatur=19

with open(f'results/_{party}_{legislatur}.json', 'r') as file:
    data = json.load(file)

print(len(data[party]))

from gensim.models import KeyedVectors

# Laden des vortrainierten Word2Vec-Modells
model_path = 'path_to_pretrained_model.bin'  # Pfade anpassen
word2vec_model = KeyedVectors.load_word2vec_format(model_path, binary=True)

import networkx as nx

words = ['apple', 'banana', 'cat', 'dog', 'elephant']
word_network = nx.Graph()

# Hinzufügen von ähnlichen Nachbarn zu jedem Wort
for word in words:
    neighbors = word2vec_model.most_similar(positive=[word], topn=5)
    neighbors = [neighbor[0] for neighbor in neighbors]
    word_network.add_edges_from([(word, neighbor) for neighbor in neighbors])


#word_network = {}

#for word in data:
   # neighbors = []
  #  for other_word in data:
  #      if word != other_word and other_word.startswith(word[-1]):
   #         neighbors.append(other_word)
   # word_network[word] = neighbors

#for word, neighbors in word_network.items():
     #   print(f"{word}: {', '.join(neighbors)}")

