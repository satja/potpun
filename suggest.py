from collections import defaultdict

class AutoComplete:
    def __init__(self, words_file):
        self.suggestions = defaultdict(list)
        self.words = []
        word_set = set()
        with open(words_file) as f:
            for line in f:
                word, freq = line.split()
                n = len(word)
                if n <= 2:
                    continue
                word = word.lower()
                if word in word_set:
                    continue
                word_set.add(word)
                word_index = len(self.words)
                self.words.append(word)
                for i in range(1, n):
                    prefix = word[:i]
                    if len(self.suggestions[prefix]) < 10:
                        self.suggestions[prefix].append(word_index)

    def suggest(self, word):
        return [self.words[index] for index in self.suggestions[word.lower()]]
