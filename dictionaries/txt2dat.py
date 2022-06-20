""" Converts a .txt file (i.e. croatian.txt, english.txt), with words sorted by
    frequencies, into a binary file (i.e. croatian.dat, english.dat).
"""

import pickle
import sys

with open(sys.argv[1] + '.txt') as f:
    words = [line.split()[0] for line in f if line.strip()]

with open(sys.argv[1] + '.dat', 'wb') as f:
    pickle.dump(words, f)
