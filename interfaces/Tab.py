from tkinter import *

class Tab:

    def __init__(self, master, title):
        self.master = master
        self.frame = Frame(master, background='white')
        self.frame.place(width=1440, height=960, x=0, y=0)

        self.title = Label(self.frame, text=title, background='white')
        self.title.place(x=10, y=10)
        self.title.config(font=("", 64))

    def hide(self):
        self.frame.place_forget()

    def show(self):
        self.frame.place(width=960, height=720, x=120, y=0)