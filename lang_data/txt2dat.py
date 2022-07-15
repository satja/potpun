import pickle
import sys
from collections import defaultdict
import sys

sys.path.append('..')
import settings

language = sys.argv[1]

suggestions = defaultdict(list)
next_word = defaultdict(list)
words = []
word_to_index = dict()

# words
with open(sys.argv[1] + '.txt') as f:
    for line in f:
        if line.strip():
            word = line.split()[0]
            n = len(word)
            if n <= 2:
                continue
            word = word.lower()
            if word in word_to_index:
                continue
            word_index = len(words)
            word_to_index[word] = word_index
            words.append(word)
            for i in range(1, n):
                prefix = word[:i]
                if len(suggestions[prefix]) < settings.NUM_SUGGESTIONS:
                    suggestions[prefix].append(word_index)

with open('../dictionaries/' + sys.argv[1] + '.dat', 'wb') as f:
    pickle.dump(words, f)
    pickle.dump(suggestions, f)

# bigrams
bigrams = []
with open(sys.argv[1] + '_bigrams.txt') as f:
    for line in f:
        a, b, c = line.split()
        next_word[(a, b[0])].append(word_to_index[b])

with open('../dictionaries/' + sys.argv[1] + '_bigrams.dat', 'wb') as f:
    pickle.dump(next_word, f)
