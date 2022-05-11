from tkinter import *
from tkinter.messagebox import *
import sys


def main(root, text, menubar, config, ai, var):
    def setEnglish():
        config['language'] = 'english'
        ai.load('english')

    def setCroatian():
        config['language'] = 'croatian'
        ai.load('croatian')

    languageMenu = Menu(menubar)
    languageMenu.add_radiobutton(label='Croatian', value='croatian', command=setCroatian,
            variable=var)
    languageMenu.add_radiobutton(label='English', value='english', command=setEnglish,
            variable=var)
    menubar.add_cascade(label="Language", menu=languageMenu)
    root.config(menu=menubar)


if __name__ == "__main__":
    print("Please run 'main.py'")
