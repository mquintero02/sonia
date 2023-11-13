from tkinter import *

class Tab:

    def __init__(self, master, title):
        self.frame = Frame(master)
        self.frame.place(width=960, height=720, x=120, y=0)

        self.title = Label(self.frame, text=title)
        self.title.place(x=10, y=10)
        self.title.config(font=("Arial", 40))

    def hide(self):
        self.frame.place_forget()

    def show(self):
        self.frame.place(width=960, height=720, x=120, y=0)