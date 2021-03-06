from tkinter import *
from tkinter.messagebox import *
import sys


def main(root, text, menubar, config, ai, language_var,
        auto_capitalize, auto_space_word, auto_space_interpunction):
    def set_english():
        config['language'] = 'english'
        ai.load('english')

    def set_croatian():
        config['language'] = 'croatian'
        ai.load('croatian')

    def update_config():
        config['AutoCapitalize'] = str(auto_capitalize.get())
        config['SpaceAfterWord'] = str(auto_space_word.get())
        config['SpaceAfterInterpunction'] = str(auto_space_interpunction.get())

    language_menu = Menu(menubar)

    language_menu.add_radiobutton(label='Croatian', value='croatian',
            command=set_croatian, variable=language_var)
    language_menu.add_radiobutton(label='English', value='english',
            command=set_english, variable=language_var)

    language_menu.add_separator()

    language_menu.add_checkbutton(label='Auto Capitalize', onvalue=1, offvalue=0,
            variable=auto_capitalize, command=update_config)
    language_menu.add_checkbutton(label='Space After Interpunction', onvalue=1, offvalue=0,
            variable=auto_space_interpunction, command=update_config)
    language_menu.add_checkbutton(label='Space After Completion', onvalue=1, offvalue=0,
            variable=auto_space_word, command=update_config)

    menubar.add_cascade(label="Language", menu=language_menu)
    root.config(menu=menubar)


if __name__ == "__main__":
    print("Please run 'main.py'")
