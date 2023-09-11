import pickle
import json
import sys

# Load the pickled data
with open(f'{sys.argv[1]}.dat', 'rb') as f:
    words = pickle.load(f)
    suggestions = pickle.load(f)
    next_word = pickle.load(f)

# Convert the data to a dictionary
data = {
    'words': words,
    'suggestions': suggestions,
    'next_word': next_word
}

# Save the data as JSON
with open(f'{sys.argv[1]}.json', 'w') as f:
    json.dump(data, f)

print("Conversion complete!")
