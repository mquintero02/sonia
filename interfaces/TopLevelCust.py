from tkinter import *

class TopLevelCust:

    def __init__(self, master, customer):
        self.master = master
        self.customer = customer

        self.button = Button(master, text=customer.name, command=lambda:self.init_widgets())

    def init_widgets(self):
        root = Toplevel(self.master)
        root.resizable(0, 0)
        root.geometry("480x720")
        
        Label(root, text=self.customer.name, font=("Arial", 24)).place(x=10, y=10)
        Label(root, text=self.customer.name, font=("Arial", 24)).place(x=10, y=50)

        root.mainloop()