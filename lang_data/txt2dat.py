import numpy as np
import pickle
import sys
from collections import defaultdict

sys.path.append('..')
import settings

language = sys.argv[1]

word_set = set()
word_list = []
word_to_index = dict()
suggestions = defaultdict(list)
next_word = defaultdict(list)

with open(f'{language}.txt') as f:
    for line in f:
        word = line.split()[0].lower()
        word_set.add(word)
        n = len(word)
        if n <= 2:
            continue
        if word in word_to_index:
            continue
        word_index = len(word_list)
        word_to_index[word] = word_index
        word_list.append(word)
        for i in range(1, n):
            prefix = word[:i]
            if len(suggestions[prefix]) < settings.NUM_SUGGESTIONS:
                suggestions[prefix].append(word_index)

with open(f'{language}_bigrams.txt') as f:
    for line in f:
        a, b, _ = line.split()
        if len(b) > 2 and a in word_set and b in word_set:
            next_word[a + b[0]].append(word_to_index[b])

with open(f'../dictionaries/{language}.dat', 'wb') as f:
    pickle.dump(word_list, f)
    pickle.dump(suggestions, f)
    pickle.dump(next_word, f)
