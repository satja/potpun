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


""" Happens when the text has changed (e.g. by entering a character).
"""
def on_change(event):
    global resetting_modified_flag
    global space_after_interpuction_inserted
    global space_after_word_inserted
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

    # Get previous and last (partially entered) word.
    word = text.get("insert -1c wordstart", "insert").strip()
    prev_word = text.get("insert -1c wordstart -2c wordstart",
            "insert -1c wordstart -1c").strip()

    # Is this interpunction?
    if any(word == c for c in '.!?:,;'):
        if auto_space_word.get() and space_after_word_inserted:
            text.delete("insert -2c", "insert -1c")
            space_after_word_inserted = False
        elif auto_space_interpunction.get() and not space_after_interpuction_inserted:
            text.insert(INSERT, ' ')
            space_after_interpuction_inserted = True
        if word == '.' or word == '?' or word == '!':
            if auto_capitalize.get():
                capitalize = True
        completions.clear()
        return

    if word:
        space_after_word_inserted = False
        space_after_interpuction_inserted = False

    # Fill suggestions for word completion.
    suggestions = ai.suggest(word, prev_word)
    completions.clear()
    max_width = 0
    num_suggestions = min(settings.NUM_SUGGESTIONS, len(suggestions))
    for i in range(num_suggestions):
        completion = suggestions[i][len(word):]
        completions.append(completion)
        labels[i].config(text=f'{word}{completion}')
        max_width = max(labels[i].winfo_width(), max_width)

    # Where to show suggestions?
    x, y, width, height = text.bbox(INSERT)
    max_width += settings.SUGGESTION_DISTANCE + height
    orig_x = x
    if x + max_width > root.winfo_width():
        x = root.winfo_width() - max_width
        y += height
    if y + num_suggestions * height > root.winfo_height():
        y = root.winfo_height() - num_suggestions * height
        if x < orig_x < x + max_width:
            x = orig_x - max_width

    for i in range(settings.NUM_SUGGESTIONS):
        if i < len(suggestions):
            nums[i].config(bg=settings.SUGGESTION_BACKGROUND, width=2)
            nums[i].place(x=x + settings.SUGGESTION_DISTANCE, y=y + i * height)
            labels[i].place(x=x + settings.SUGGESTION_DISTANCE + height, y=y + i * height)
        else:
            nums[i].place_forget()
            labels[i].place_forget()


""" Happens when any character is entered.
"""
def handle_input(event):
    global word_completed
    global space_after_word_inserted
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
                space_after_word_inserted = True
            for i in range(len(completions)):
                nums[i].place_forget()
                labels[i].place_forget()
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
    root.geometry("{}x{}".format(settings.DEFAULT_WIDTH, settings.DEFAULT_HEIGHT))
    root.minsize(width=settings.MIN_WIDTH, height=settings.MIN_HEIGHT)

    text = ScrolledText(root, state='normal', wrap='word', undo=True)
    text.focus_set()
    text.pack(fill='both', expand=True)
    text.bind("<Key>", handle_input)
    text.bind("<<Modified>>", on_change)

    nums = [Label(root, text=f"{settings.INDEX_TO_KEY[i]}")
            for i in range(settings.NUM_SUGGESTIONS)]
    labels = [Label(root, text="") for i in range(settings.NUM_SUGGESTIONS)]

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
    format_menu.main(root, text, nums, labels, menubar, config['USER'], settings.DEFAULT_CONFIG)
    help_menu.main(root, text, menubar)

    root.after(200, ai.load)
    root.protocol("WM_DELETE_WINDOW", on_closing)

    completions = []
    resetting_modified_flag = False
    word_completed = False
    space_after_interpuction_inserted = False
    capitalize = auto_capitalize.get()

    root.mainloop()
