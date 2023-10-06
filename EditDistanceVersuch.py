import json

party='AfD'
legislatur=19

with open(f'results/_{party}_{legislatur}.json', 'r') as file:
    data = json.load(file)

print(len(data[party]))

import editdistance
import networkx as nx

def get_edit_distance(word1, word2):
    return editdistance.eval(word1, word2)

words = data[party]
words=words[0:200]

word_network = nx.Graph()

for word in words:
    for other_word in words:
        if word != other_word:
            distance = get_edit_distance(word, other_word)
            similarity=1/(distance + 1)
            if similarity > 0.1:
                word_network.add_edge(word, other_word,weight=similarity)

print(word_network)

#visualisierung mit gephi
#littletool von github benutzen



