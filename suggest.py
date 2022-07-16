from collections import defaultdict
from time import sleep
import tkinter as tk
from tkinter import ttk
from threading import Thread
import pickle

import settings


class AutoComplete:
    def __init__(self, config):
        self.language = config['Language']

    def _load(self):
        filename = f'{settings.DICT_FOLDER}/{self.language}.dat'
        with open(filename, 'rb') as f:
            self.words = pickle.load(f)
            self.suggestions = pickle.load(f)
            self.next_word = pickle.load(f)
        self.loading.destroy()

    def load(self, language=None):
        if language:
            self.language = language
        self.loading = tk.Toplevel()
        self.loading.geometry("300x60")
        self.loading.title("Loading")
        label = tk.Label(self.loading, text="Loading dictionary...")
        label.pack()
        pb = ttk.Progressbar(
            self.loading,
            orient='horizontal',
            mode='indeterminate',
            length=280
        )
        pb.pack()
        pb.start()
        t = Thread(target=self._load, args=())
        self.loading.after(200, t.start)

    def suggest(self, prefix, prev_word=None):
        if not prefix:
            return []
        prev_word = prev_word.lower()
        prefix = prefix.lower()
        suggestions = []
        for index in self.next_word.get(prev_word + prefix[0], []):
            word = self.words[index]
            if word.startswith(prefix):
                suggestions.append(word)
                if len(suggestions) == settings.NUM_SUGGESTIONS:
                    return suggestions
        for index in self.suggestions[prefix]:
            word = self.words[index]
            if word not in suggestions:
                suggestions.append(word)
                if len(suggestions) == settings.NUM_SUGGESTIONS:
                    return suggestions
        return suggestions
