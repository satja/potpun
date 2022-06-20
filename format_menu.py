from tkinter import *
from tkinter.font import Font, families
from tkinter.colorchooser import askcolor
from tkinter.scrolledtext import *

import time
import sys


class Format():
    def __init__(self, text, config, default_config):
        self.text = text
        self.config = config
        self.default_config = default_config
        self.font = Font(family=config['FontFamily'], size=config['FontSize'])
        text.configure(font=self.font, bg=config['Background'], fg=config['FontColor'])

    def change_bg(self):
        (triple, hexstr) = askcolor()
        if hexstr:
            self.text.config(bg=hexstr)
            self.config['Background'] = hexstr

    def change_fg(self):
        (triple, hexstr) = askcolor()
        if hexstr:
            self.text.config(fg=hexstr)
            self.config['FontColor'] = hexstr

    def change_font(self, option):
        self.font.configure(family=option)
        self.config['FontFamily'] = option

    def change_size(self, value):
        self.font.configure(size=value)
        self.config['FontSize'] = str(value)

    def default(self):
        self.config.update(self.default_config)
        self.text.config(bg=self.config['Background'])
        self.text.config(fg=self.config['FontColor'])
        self.font.configure(family=self.config['FontFamily'], size=self.config['FontSize'])


def main(root, text, menubar, config, default_config):
    obj_format = Format(text, config, default_config)
    fontoptions = families(root)

    format_menu = Menu(menubar)

    fsubmenu = Menu(format_menu, tearoff=0)
    ssubmenu = Menu(format_menu, tearoff=0)

    for option in fontoptions:
        fsubmenu.add_command(label=option, command=lambda option=option:
            obj_format.change_font(option))
    for value in range(1, 31):
        ssubmenu.add_command(label=str(value), command=lambda value=value:
            obj_format.change_size(value))

    format_menu.add_command(label="Change Background", command=obj_format.change_bg)
    format_menu.add_command(label="Change Font Color", command=obj_format.change_fg)
    format_menu.add_cascade(label="Font", menu=fsubmenu)
    format_menu.add_cascade(label="Size", menu=ssubmenu)
    format_menu.add_separator()
    format_menu.add_command(label="Reset Default", command=obj_format.default)
    menubar.add_cascade(label="Format", menu=format_menu)

    root.grid_columnconfigure(0, weight=1)
    root.resizable(True, True)

    root.config(menu=menubar)


if __name__ == "__main":
    print("Please run 'main.py'")
