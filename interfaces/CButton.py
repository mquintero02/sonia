from customtkinter import *

class CButton():

    def __init__(self, customer, master, root):
        self.button = CTkButton(master, text=customer.name, command=lambda:root.open_customer(customer), width=720, height=40, corner_radius=0, font=('calibri', 24))
        if customer.balance <= -1:
            self.button.configure(fg_color = 'red')
        elif customer.balance >= 1:
            self.button.configure(fg_color = 'green')
            
    def set_button(self):
        self.button.pack()