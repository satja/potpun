from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter.font import Font
from tkinter.scrolledtext import *
import file_menu
import edit_menu
import format_menu
import help_menu

root = Tk()

root.title("TextEditor-newfile")
root.geometry("300x250+300+300")
root.minsize(width=400, height=400)

text = ScrolledText(root, state='normal', height=400, width=400, wrap='word', pady=2, padx=3, undo=True)
text.grid(row=0, column=0, rowspan=10, sticky='nsew')
#text.pack(fill=Y, expand=1)
text.focus_set()

Label(root, text="0:").grid(row=0, column=1, sticky='nsew')
Label(root, text="1:").grid(row=1, column=1, sticky='nsew')
Label(root, text="2:").grid(row=2, column=1, sticky='nsew')
Label(root, text="3:").grid(row=3, column=1, sticky='nsew')
Label(root, text="3:").grid(row=4, column=1)
Label(root, text="4:").grid(row=5, column=1)
Label(root, text="5:").grid(row=6, column=1)
Label(root, text="7:").grid(row=7, column=1)
Label(root, text="6:").grid(row=8, column=1)
Label(root, text="8:").grid(row=9, column=1)
Label(root, text="9:").grid(row=10, column=1)

menubar = Menu(root)

file_menu.main(root, text, menubar)
edit_menu.main(root, text, menubar)
format_menu.main(root, text, menubar)
help_menu.main(root, text, menubar)
root.mainloop()
