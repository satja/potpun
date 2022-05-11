from collections import defaultdict
import tkinter as tk

class AutoComplete:
    def __init__(self, config):
        self.language = config['Language']

    def _load(self):
        words_file = f'dictionaries/{self.language}.txt'
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
        self.loading.destroy()

    def load(self, language=None):
        if language:
            self.language = language
        self.loading = tk.Toplevel()
        self.loading.geometry("300x100")
        self.loading.title("Loading")
        label = tk.Label(self.loading, text="Loading dictionary...")
        label.pack()
        self.loading.after(200, self._load)

    def suggest(self, word):
        return [self.words[index] for index in self.suggestions[word.lower()]]
