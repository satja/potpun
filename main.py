import configparser
import sys
from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *

import edit_menu
import file_menu
import format_menu
import help_menu
import language_menu
import settings
import suggest


""" Restores user menu choices.
"""
def load_config():
    config = configparser.ConfigParser()
    config.read(settings.CONFIG_FILE)
    if 'USER' not in config or\
            any(key not in config['USER'] for key in settings.DEFAULT_CONFIG):
        config['USER'] = settings.DEFAULT_CONFIG
    return config


""" Adjusts the window in case of font/size change.
"""
def configure(event):
    root.geometry("{}x{}".format(root.winfo_width(), event.height))


""" Happens when the text has changed (e.g. by entering a character).
"""
def on_change(event):
    global resetting_modified_flag
    global word_completed
    global capitalize

    # Add * to the title to suggest "unsaved".
    title = root.title()
    if title[0] != '*':
        root.title('*' + title)

    if resetting_modified_flag:
        resetting_modified_flag = False
        return
    resetting_modified_flag = True
    text.tk.call(text._w, 'edit', 'modified', 0)

    if word_completed:
        word_completed = False
        return

    # Get last (partially entered) word.
    word = text.get("insert -1c wordstart", "insert").strip()

    # Is this interpunction?
    if any(word == c for c in '.!?:,;'):
        if auto_space_interpunction.get():
            text.insert(INSERT, ' ')
        if word == '.' or word == '?' or word == '!':
            if auto_capitalize.get():
                capitalize = True
        completions.clear()
        return

    # Fill suggestions for word completion.
    suggestions = ai.suggest(word)
    completions.clear()
    for i in range(settings.NUM_SUGGESTIONS):
        nums[i].config(bg=settings.SUGGESTION_KEY_BACKGROUND)
        if i < len(suggestions):
            completion = suggestions[i][len(word):]
            labels[i].config(text=f'{word}{completion}')
            completions.append(completion)
        else:
            labels[i].config(text='')


""" Happens when any character is entered.
"""
def handle_input(event):
    global word_completed
    global capitalize

    if not event.char:
        return

    # Handle diacritics in Croatian language.
    if event.keysym == '??':
        char = None
        if event.keycode == 219:
            char = u"\u0161"
        if event.keycode == 221:
            char = u"\u0111"
        if event.keycode == 186:
            char = u"\u010D"
        if event.keycode == 222:
            char = u"\u0107"
        if event.keycode == 220:
            char = u"\u017e"
        if char:
            if event.state > 8 or capitalize:
                char = char.upper()
                capitalize = False
            text.insert(INSERT, char)
            return 'break'

    # Handle selection of the suggested word.
    if completions and event.char in '0123456789':
        index = settings.KEY_TO_INDEX[int(event.char)]
        if index < len(completions):
            word_completed = True
            text.insert(INSERT, completions[index])
            if auto_space_word.get():
                text.insert(INSERT, ' ')
            for i in range(len(completions)):
                if i != index:
                    labels[i].config(text='')
            nums[index].config(bg=settings.SUGGESTION_SELECTED_BACKGROUND)
            completions.clear()
        return 'break'

    # Auto capitalize the beginning of a sentence.
    if event.char.isalpha() and capitalize:
        text.insert(INSERT, event.char.upper())
        capitalize = False
        return 'break'


def on_closing():
    entry = askyesno(title="Quit", message="Are you sure you want to quit?")
    if entry == True:
        with open(settings.CONFIG_FILE, 'w') as f:
            config.write(f)
        root.destroy()


if __name__ == "__main__":
    config = load_config()

    root = Tk()
    root.tk.call('encoding', 'system', 'utf-8')
    root.option_add("*font", settings.ROOT_FONT)
    root.title(settings.TITLE + ' - Untitled')
    root.geometry("{}x{}".format(settings.DEFAULT_WIDTH, root.winfo_height()))
    root.minsize(width=settings.MIN_WIDTH, height=settings.MIN_HEIGHT)

    text = ScrolledText(root, width=settings.TEXT_WIDTH,
            state='normal', wrap='word', undo=True)
    text.focus_set()
    text.grid(row=0, column=0, rowspan=settings.NUM_SUGGESTIONS)
    text.bind("<Configure>", configure)
    text.bind("<Key>", handle_input)
    text.bind("<<Modified>>", on_change)

    nums = [Label(root, font=settings.LABEL_FONT + ' bold',
            text=f"{settings.INDEX_TO_KEY[i]}", width=settings.LABEL_WIDTH)
            for i in range(settings.NUM_SUGGESTIONS)]
    for i, num in enumerate(nums):
        num.grid(row=i, column=1)

    labels = [Label(root, text="", font=settings.LABEL_FONT,
            width=settings.SUGGESTION_WIDTH) for i in range(settings.NUM_SUGGESTIONS)]
    for i, l in enumerate(labels):
        l.grid(row=i, column=2)

    ai = suggest.AutoComplete(config['USER'])
    language_var = StringVar(None, config['USER']['Language'])
    auto_capitalize = BooleanVar(value=config['USER']['AutoCapitalize'])
    auto_space_word = BooleanVar(value=config['USER']['SpaceAfterWord'])
    auto_space_interpunction = BooleanVar(value=config['USER']['SpaceAfterInterpunction'])

    menubar = Menu(root)
    file_menu.main(root, text, menubar, config)
    language_menu.main(root, text, menubar, config['USER'], ai, language_var,
            auto_capitalize, auto_space_word, auto_space_interpunction)
    edit_menu.main(root, text, menubar)
    format_menu.main(root, text, menubar, config['USER'], settings.DEFAULT_CONFIG)
    help_menu.main(root, text, menubar)

    root.after(200, ai.load)
    root.protocol("WM_DELETE_WINDOW", on_closing)

    completions = []
    resetting_modified_flag = False
    word_completed = False
    capitalize = auto_capitalize.get()

    root.mainloop()
