from tkinter import *
from interfaces.CustomerTab import CustomerTab
from interfaces.ProductTab import ProductTab
from interfaces.MessageTab import MessageTab


class GUI:

    def __init__(self, data):
        self.tabs = []

        self.root = Tk()
        self.root.title('Cantina Maria Auxiliadora')
        self.root.geometry("1080x720")

        self.init_tabs()

        self.root.mainloop()

    def init_tabs(self):
        customerTab = CustomerTab(self.root, "Clientes", [])
        self.tabs.append(customerTab)

        productTab = ProductTab(self.root, "Productos")
        productTab.hide()
        self.tabs.append(productTab)

        messageTab = MessageTab(self.root, "Mensajes")
        messageTab.hide()
        self.tabs.append(messageTab)