from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
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
        try:
            t = self.text.get(0.0, END)
            f = open(self.filename, 'w')
            f.write(t)
            f.close()
            self.root.title(f"{TITLE} - {basename(self.filename)}")
        except:
            self.saveAs()

    def saveAs(self):
        f = asksaveasfile(mode='w', defaultextension='.txt')
        t = self.text.get(0.0, END)
        try:
            f.write(t.rstrip())
            self.filename = f.name
            self.root.title(f"{TITLE} - {basename(self.filename)}")
        except:
            showerror(title="Oops!", message="Unable to save file...")

    def openFile(self, *args):
        f = askopenfile(mode='r')
        self.filename = f.name
        self.root.title(f"{TITLE} - {basename(self.filename)}")
        t = f.read()
        self.text.delete(0.0, END)
        self.text.insert(0.0, t)

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
