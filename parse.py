# A script for parsing croatian words with frequencies using a file from:
#
# Ljubešić, Nikola, 2019, Inflectional lexicon hrLex 1.3, Slovenian language resource repository CLARIN.SI, ISSN 2820-4042, http://hdl.handle.net/11356/1232.

from collections import defaultdict
freqs = defaultdict(float)
with open('hrLex_v1.3') as f:
    for line in f:
        niz = line.split()
        rijec = niz[0]
        frek = float(niz[-1])
        freqs[rijec] += frek
for rijec, frek in sorted(freqs.items(), key=lambda par: -par[1]):
    if frek <= 1e-4:
        break
    print(rijec, "{:.6f}".format(frek))
