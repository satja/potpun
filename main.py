from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
import configparser
import sys

import file_menu
import edit_menu
import format_menu
import help_menu
import language_menu
import suggest

DICTIONARY = 'dictionaries/croatian.txt'
TITLE = 'Nadopunitelj'
TEXT_WIDTH = 100
LABEL_WIDTH = 2
SUGGESTION_WIDTH = 15
LABEL_FONT = 'Courier 20'
DEFAULT_FONT = "Times New Roman"
DEFAULT_SIZE = 15

root = Tk()
root.tk.call('encoding', 'system', 'utf-8')
root.option_add("*font", "lucida 12")
root.title(TITLE + ' - Untitled')
root.geometry("{}x{}".format(300, root.winfo_height()))
root.minsize(width=600, height=600)

config = configparser.ConfigParser()
config.read('potpun.ini')
default_config = {
    'FontFamily': DEFAULT_FONT,
    'FontSize': str(DEFAULT_SIZE),
    'Background': 'white',
    'FontColor': 'black',
    'Language': 'croatian',
    }
if 'USER' not in config:
    config['USER'] = default_config

text = ScrolledText(root, width=TEXT_WIDTH, state='normal', wrap='word', undo=True)
text.focus_set()

nums = [Label(root, font=LABEL_FONT + ' bold', text=f"{i}", width=LABEL_WIDTH)\
        for i in range(10)]
for i, num in enumerate(nums):
    num.grid(row=i, column=1)

labels = [Label(root, text="", font=LABEL_FONT, width=SUGGESTION_WIDTH) for i in range(10)]
for i, l in enumerate(labels):
    l.grid(row=i, column=2)

text.grid(row=0, column=0, rowspan=10)

ai = suggest.AutoComplete(config['USER'])

menubar = Menu(root)
file_menu.main(root, text, menubar)
var = StringVar(None, config['USER']['Language'])
language_menu.main(root, text, menubar, config['USER'], ai, var)
edit_menu.main(root, text, menubar)
format_menu.main(root, text, menubar, config['USER'], default_config)
help_menu.main(root, text, menubar)

completions = []
resetting_modified_flag = False
autocompleted = False

def on_change(event):
    global resetting_modified_flag
    global autocompleted

    title = root.title()
    if title[0] != '*':
        root.title('*' + title)
    if resetting_modified_flag:
        resetting_modified_flag = False
        return

    resetting_modified_flag = True
    text.tk.call(text._w, 'edit', 'modified', 0)

    if autocompleted:
        autocompleted = False
        return

    word = text.get("insert -1c wordstart", "insert").strip()
    suggestions = ai.suggest(word)
    completions.clear()
    for i in range(10):
        nums[i].config(bg='#f0f0f0')
        if i < len(suggestions):
            completion = suggestions[i][len(word):]
            labels[i].config(text=f'{word}{completion}')
            completions.append(completion)
        else:
            labels[i].config(text='')

def handle_input(event):
    global autocompleted
    if not event.char:
        return
    if event.char in '0123456789':
        digit = int(event.char)
        if digit < len(completions):
            autocompleted = True
            text.insert(INSERT, completions[digit])
            for i in range(len(completions)):
                if i != digit:
                    labels[i].config(text='')
            nums[digit].config(bg='yellow')
            completions.clear()
        return 'break'

def configure(event):
    root.geometry("{}x{}".format(root.winfo_width(), event.height))

def on_closing():
    entry = askyesno(title="Quit", message="Are you sure you want to quit?")
    if entry == True:
        with open('potpun.ini', 'w') as f:
            config.write(f)
        root.destroy()

text.bind("<Key>", handle_input)
text.bind("<<Modified>>", on_change)
text.bind("<Configure>", configure)

root.protocol("WM_DELETE_WINDOW", on_closing)

root.after(200, ai.load)
root.mainloop()
