from tkinter import *

class CustFrame:

    def __init__(self, master, customer, root, mainFrane):
        self.master = master
        self.root = root
        self.customer = customer
        self.mainFrame = mainFrane

        self.frame = Frame(root)
        self.button = Button(master,text=f"{self.customer.name.upper()}", command=lambda:self.init_widgets(), background='aqua', width=390, height=3, font=("Arial", 12))
    
    def init_widgets(self):
        self.mainFrame.place_forget()
        self.frame.place(x=0, y=0, width=1440, height=960)
        self.frame.config(background='green')

        self.name = Label(self.frame, font=('Arial', 32), justify=LEFT, padx=5, pady=5,
                        text=f"{self.customer.name.capitalize()} {self.customer.lastName.capitalize()}\nCI:{self.customer.ci}\nTeléfono{self.customer.phone}")
        self.name.place(x=0, y=0)
        
    def quit(self):
        self.frame.place_forget()
        self.mainFrame.place(x=0, y=0, width=1440, height=960)