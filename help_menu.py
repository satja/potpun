from tkinter import *
from tkinter.messagebox import *
import sys


class Help():
    def about(root):
        showinfo(title="About", message="Autocomplete editor by Adrian Satja Kurdija")


def main(root, text, menubar):
    help = Help()
    help_menu = Menu(menubar)
    help_menu.add_command(label="About", command=help.about)
    menubar.add_cascade(label="Help", menu=help_menu)

    root.config(menu=menubar)


if __name__ == "__main__":
    print("Please run 'main.py'")
