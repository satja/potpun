from tkinter import *
from tkinter.font import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
import file_menu
import edit_menu
import format_menu
import help_menu
import suggest

DICTIONARY = 'dictionaries/croatian.txt'
TEXT_WIDTH = 50
TEXT_FONT = ('Times New Roman', 15)
LABEL_WIDTH = 2
SUGGESTION_WIDTH = 15
LABEL_FONT = 'Courier 20'

root = Tk()
root.option_add("*font", "lucida 12")
root.title("Upotpuni me")
#root.geometry("300x250+300+300")
root.minsize(width=400, height=400)

text = ScrolledText(root, width=TEXT_WIDTH, state='normal', wrap='word', undo=True)
text.focus_set()

nums = [Label(root, font=LABEL_FONT + ' bold', text=f"{i}", width=LABEL_WIDTH)\
        for i in range(10)]
for i, num in enumerate(nums):
    num.grid(row=i, column=1)

labels = [Label(root, text="", font=LABEL_FONT, width=SUGGESTION_WIDTH) for i in range(10)]
for i, l in enumerate(labels):
    l.grid(row=i, column=2)

text.grid(row=0, column=0, rowspan=10)

menubar = Menu(root)

file_menu.main(root, text, menubar)
edit_menu.main(root, text, menubar)
format_menu.main(root, text, menubar)
help_menu.main(root, text, menubar)

ai = suggest.AutoComplete(DICTIONARY)
completions = []

resetting_modified_flag = False
autocompleted = False

def on_change(event):
    global resetting_modified_flag
    global autocompleted

    if resetting_modified_flag: return
    resetting_modified_flag = True
    try:
        text.tk.call(text._w, 'edit', 'modified', 0)
    finally:
        resetting_modified_flag = False

    if autocompleted:
        autocompleted = False
        return

    word = text.get("insert -1c wordstart", "insert").strip()
    suggestions = ai.suggest(word)
    completions.clear()
    for i in range(10):
        nums[i].config(bg='#f0f0f0')
        if i < len(suggestions):
            completion = suggestions[i][len(word):]
            labels[i].config(text=f'{word}{completion}')
            completions.append(completion)
        else:
            labels[i].config(text='')

def handle_input(event):
    global autocompleted
    if not event.char:
        return
    if event.char in '0123456789':
        digit = int(event.char)
        if digit < len(completions):
            autocompleted = True
            text.insert(INSERT, completions[digit])
            for i in range(len(completions)):
                if i != digit:
                    labels[i].config(text='')
            nums[digit].config(bg='yellow')
            completions.clear()
        return 'break'

text.bind("<Key>", handle_input)
text.bind("<<Modified>>", on_change)

text.configure(font=TEXT_FONT)
root.mainloop()
