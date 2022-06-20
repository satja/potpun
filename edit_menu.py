from tkinter import *
from tkinter.simpledialog import *
from tkinter.filedialog import *
from tkinter.messagebox import *


class Edit():
    def popup(self, event):
        self.rightClick.post(event.x_root, event.y_root)

    def copy(self, *args):
        sel = self.text.selection_get()
        self.root.clipboard_clear()
        self.root.clipboard_append(sel)
        self.root.update()

    def cut(self, *args):
        sel = self.text.selection_get()
        self.text.delete(SEL_FIRST, SEL_LAST)
        self.root.clipboard_clear()
        self.root.clipboard_append(sel)
        self.root.update()

    def paste(self, *args):
        self.text.insert(INSERT, self.root.clipboard_get())

    def select_all(self, *args):
        self.text.tag_add(SEL, "1.0", END)
        self.text.mark_set(0.0, END)
        self.text.see(INSERT)

    def copy_all(self, *args):
        self.select_all()
        self.copy()

    def undo(self, *args):
        self.text.edit_undo()

    def redo(self, *args):
        self.text.edit_redo()

    def find(self, *args):
        self.text.tag_remove('found', '1.0', END)
        target = askstring('Find', 'Search String:')

        if target:
            idx = '1.0'
            while 1:
                idx = self.text.search(target, idx, nocase=1, stopindex=END)
                if not idx: break
                lastidx = '%s+%dc' % (idx, len(target))
                self.text.tag_add('found', idx, lastidx)
                idx = lastidx
            self.text.tag_config('found', foreground='white', background='blue')

    def __init__(self, text, root):
        self.text = text
        self.root = root
        self.rightClick = Menu(root)


def main(root, text, menubar):

    obj_edit = Edit(text, root)

    editmenu = Menu(menubar)
    editmenu.add_command(label="Copy", command=obj_edit.copy, accelerator="Ctrl+C")
    editmenu.add_command(label="Cut", command=obj_edit.cut, accelerator="Ctrl+X")
    editmenu.add_command(label="Paste", command=obj_edit.paste, accelerator="Ctrl+V")
    editmenu.add_command(label="Undo", command=obj_edit.undo, accelerator="Ctrl+Z")
    editmenu.add_command(label="Redo", command=obj_edit.redo, accelerator="Ctrl+Y")
    editmenu.add_command(label="Find", command=obj_edit.find, accelerator="Ctrl+F")
    editmenu.add_separator()
    editmenu.add_command(label="Select All", command=obj_edit.select_all, accelerator="Ctrl+A")
    editmenu.add_command(label="Copy All", command=obj_edit.copy_all)
    menubar.add_cascade(label="Edit", menu=editmenu)

    root.bind_all("<Control-z>", obj_edit.undo)
    root.bind_all("<Control-y>", obj_edit.redo)
    root.bind_all("<Control-f>", obj_edit.find)
    root.bind_all("<Control-a>", obj_edit.select_all)

    obj_edit.rightClick.add_command(label="Copy", command=obj_edit.copy)
    obj_edit.rightClick.add_command(label="Cut", command=obj_edit.cut)
    obj_edit.rightClick.add_command(label="Paste", command=obj_edit.paste)
    obj_edit.rightClick.add_separator()
    obj_edit.rightClick.add_command(label="Select All", command=obj_edit.select_all)
    obj_edit.rightClick.bind("<Control-q>", obj_edit.select_all)

    text.bind("<Button-3>", obj_edit.popup)

    root.config(menu=menubar)


if __name__ == "__main__":
    print("Please run 'main.py'")
