from collections import Counter
from sys import argv, exit, stderr

c = Counter()
tmp = Counter()
it = 0

with open('en_corpus.txt') as f:
    for line in f:
        prev_word = None
        for word in line.split():
            if not word.isalpha():
                prev_word = None
                continue
            word = word.strip(',.;!?-:"').strip("'").lower()
            if prev_word:
                tmp[(prev_word, word)] += 1
            prev_word = word
        it += 1
        if it % (10 * 10**6) == 0:
            print(it, file=stderr)
            for bigram, cnt in tmp.items():
                if cnt > 1:
                    c[bigram] += cnt
            tmp.clear()

for (a, b), val in c.most_common():
    if val > 4:
        print(a, b, val)
    else:
        break
