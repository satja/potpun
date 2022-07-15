""" A script for parsing croatian words with frequencies
    using the 'hrLex_v1.3' file from:

    Ljubešić, Nikola, 2019, Inflectional lexicon hrLex 1.3,
    Slovenian language resource repository CLARIN.SI, ISSN 2820-4042,
    http://hdl.handle.net/11356/1232.
"""

from collections import defaultdict
freqs = defaultdict(float)
with open('hrLex_v1.3') as f:
    for line in f:
        string = line.split()
        word = string[0]
        freq = float(string[-1])
        freqs[word] += freq
for word, freq in sorted(freqs.items(), key=lambda par: -par[1]):
    if freq <= 1e-5:
        break
    print(word, "{:.6f}".format(freq))
