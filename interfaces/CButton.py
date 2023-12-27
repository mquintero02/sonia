from customtkinter import *

class CButton():

    def __init__(self, customer, master, root):
        self.customer = customer

        self.button = CTkButton(master, text=f"CI: {customer.ci}    {customer.name} {customer.lastName}", command=lambda:root.open_customer(customer), width=720, height=50, corner_radius=0, font=('calibri', 24), anchor=W, border_color='black', border_width=1)
        if customer.balance <= -1:
            self.button.configure(fg_color = 'red')
        elif customer.balance >= 1:
            self.button.configure(fg_color = 'green')

        CTkLabel(self.button, text=f"{customer.balance}$", width=100, height=50, font=('calibri', 24), anchor=E).place(x=590, y=0)
  
    def set_button(self):
        self.button.pack()