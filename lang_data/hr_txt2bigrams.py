from collections import Counter
from sys import argv, exit, stderr

c = Counter()

for i in range(1, 15):
    print(i, file=stderr)
    tmp = Counter()
    with open(f'tekst{i}.txt') as f:
        for line in f:
            prev_word = None
            for word in line.split():
                if not word.isalpha():
                    prev_word = None
                    continue
                if prev_word:
                    tmp[(prev_word, word.lower())] += 1
                prev_word = word.lower()
    for bigram, cnt in tmp.items():
        if cnt > 1:
            c[bigram] += cnt

for (a, b), val in c.most_common():
    if val > 10:
        print(a, b, val)
    else:
        break
