import os.path
import sys
from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
import traceback

import settings


class File():
    def new_file(self):
        entry = askyesno(title=settings.TITLE, message="Save changes?")
        if entry == True:
            self.save_file()
        self.filename = None
        self.root.title(settings.TITLE + ' - Untitled')
        self.text.delete(0.0, END)

    def save_file(self, *args):
        if not self.filename:
            return self.save_as()
        t = self.text.get(0.0, END)
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                f.write(t)
            self.root.title(f"{settings.TITLE} - {os.path.basename(self.filename)}")
        except Exception as e:
            traceback.print_exc()
            showerror(title="Oops!", message="Unable to save file...\n\n" + e)

    def save_as(self):
        f = asksaveasfile(mode='w', defaultextension='.txt')
        if hasattr(f, 'name'):
            self.filename = f.name
            self.save_file()

    def open_file(self, *args):
        f = askopenfile(mode='r')
        if not hasattr(f, 'name'):
            return
        self.filename = f.name
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                t = f.read()
            self.root.title(f"{settings.TITLE} - {os.path.basename(self.filename)}")
            self.text.delete(0.0, END)
            self.text.insert(0.0, t)
        except Exception as e:    
            traceback.print_exc()
            showerror(title="Oops!", message="Unable to open file...\n\n" + e)

    def quit(self):
        entry = askyesno(title="Quit", message="Are you sure you want to quit?")
        if entry == True:
            with open(settings.CONFIG_FILE, 'w') as f:
                self.config.write(f)
            self.root.destroy()

    def __init__(self, text, root, config):
        self.filename = None
        self.text = text
        self.root = root
        self.config = config


def main(root, text, menubar, config):
    filemenu = Menu(menubar)
    obj_file = File(text, root, config)
    filemenu.add_command(label="New", command=obj_file.new_file)
    filemenu.add_command(label="Open", command=obj_file.open_file, accelerator='Ctrl+O')
    filemenu.add_command(label="Save", command=obj_file.save_file, accelerator="Ctrl+S")
    filemenu.add_command(label="Save As...", command=obj_file.save_as)
    filemenu.add_separator()
    filemenu.add_command(label="Quit", command=obj_file.quit)
    menubar.add_cascade(label="File", menu=filemenu)
    root.config(menu=menubar)

    root.bind_all("<Control-s>", obj_file.save_file)
    root.bind_all("<Control-o>", obj_file.open_file)


if __name__ == "__main__":
    print("Please run 'main.py'")
