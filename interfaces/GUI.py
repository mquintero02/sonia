from tkinter import *
from interfaces.CustomerTab import CustomerTab
from interfaces.ProductTab import ProductTab
from interfaces.MessageTab import MessageTab


class GUI:

    def __init__(self, data):
        self.data = data

        self.tabs = []

        self.root = Tk()
        self.root.title('Cantina Maria Auxiliadora')
        self.root.geometry("1080x720")
        self.root.resizable(0, 0)

        self.init_tabs()
        self.init_navBar()

        self.root.mainloop()

    def init_tabs(self):
        customerTab = CustomerTab(self.root, "Clientes", self.data)
        self.tabs.append(customerTab)

        productTab = ProductTab(self.root, "Productos")
        productTab.hide()
        self.tabs.append(productTab)

        messageTab = MessageTab(self.root, "Mensajes")
        messageTab.hide()
        self.tabs.append(messageTab)

    def init_navBar(self):
        navBar = Frame(self.root, background="blue")
        navBar.place(x=0, y=0, width=120, height=720)

        btnCustomer = Button(navBar, text="Clientes", font=("Arial", 18), background="aqua", borderwidth=1)
        btnCustomer.place(x=0, y=0, width=120, height=80)
        btnProduct = Button(navBar, text="Productos", font=("Arial", 18), background="aqua", borderwidth=1)
        btnProduct.place(x=0, y=80, width=120, height=80)
        btnMessage = Button(navBar, text="Mensajes", font=("Arial", 18), background="aqua", borderwidth=1)
        btnMessage.place(x=0, y=640, width=120, height=80)