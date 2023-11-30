from customtkinter import *

class CButton():

    def __init__(self, customer, master, root):
        self.button = CTkButton(master, text=customer, command=lambda:root.open_customer(customer))
