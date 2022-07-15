import sys

language = sys.argv[1]

with open(f'{language}.txt') as f:
    words = set([line.split()[0].lower() for line in f])

with open(f'{language}_bigrams_unfiltered.txt') as f:
    for line in f:
        a, b, c = line.split()
        if a in words and b in words and len(b) > 2:
            print(a, b, c)
