from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
import traceback
import sys
from os.path import basename

TITLE = 'Nadopunitelj'

class File():
    def newFile(self):
        entry = askyesno(title=TITLE, message="Save changes?")
        if entry == True:
            self.saveFile()
        self.filename = None
        self.root.title(TITLE + ' - Untitled')
        self.text.delete(0.0, END)

    def saveFile(self, *args):
        if not self.filename:
            return self.saveAs()
        t = self.text.get(0.0, END)
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                f.write(t)
            self.root.title(f"{TITLE} - {basename(self.filename)}")
        except Exception as e:
            traceback.print_exc()
            showerror(title="Oops!", message="Unable to save file...\n\n" + e)

    def saveAs(self):
        f = asksaveasfile(mode='w', defaultextension='.txt')
        if hasattr(f, 'name'):
            self.filename = f.name
            self.saveFile()

    def openFile(self, *args):
        f = askopenfile(mode='r')
        if not hasattr(f, 'name'):
            return
        self.filename = f.name
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                t = f.read()
            self.root.title(f"{TITLE} - {basename(self.filename)}")
            self.text.delete(0.0, END)
            self.text.insert(0.0, t)
        except Exception as e:    
            traceback.print_exc()
            showerror(title="Oops!", message="Unable to open file...\n\n" + e)

    def quit(self):
        entry = askyesno(title="Quit", message="Are you sure you want to quit?")
        if entry == True:
            self.root.destroy()

    def __init__(self, text, root):
        self.filename = None
        self.text = text
        self.root = root


def main(root, text, menubar):
    filemenu = Menu(menubar)
    objFile = File(text, root)
    filemenu.add_command(label="New", command=objFile.newFile)
    filemenu.add_command(label="Open", command=objFile.openFile, accelerator='Ctrl+O')
    filemenu.add_command(label="Save", command=objFile.saveFile, accelerator="Ctrl+S")
    filemenu.add_command(label="Save As...", command=objFile.saveAs)
    filemenu.add_separator()
    filemenu.add_command(label="Quit", command=objFile.quit)
    menubar.add_cascade(label="File", menu=filemenu)
    root.config(menu=menubar)

    root.bind_all("<Control-s>", objFile.saveFile)
    root.bind_all("<Control-o>", objFile.openFile)


if __name__ == "__main__":
    print("Please run 'main.py'")
