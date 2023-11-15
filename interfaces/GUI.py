from tkinter import *
from interfaces.CustomerTab import CustomerTab
from interfaces.ProductTab import ProductTab
from interfaces.MessageTab import MessageTab


class GUI:

    def __init__(self, customerData, productData, messageData):
        self.customerData = customerData
        self.productData = productData
        self.messageData = messageData

        self.tabs = []

        self.root = Tk()
        self.root.title('Cantina Maria Auxiliadora')
        self.root.geometry("1080x720")
        self.root.resizable(0, 0)

        self.init_tabs()
        self.init_navBar()

        self.root.mainloop()

    def show_tab(self, tabNum):
        for t in self.tabs:
            if self.tabs.index(t) == tabNum:
                t.show()
            else:
                t.hide()

    def init_tabs(self):
        customerTab = CustomerTab(self.root, "Clientes", self.customerData)
        self.tabs.append(customerTab)

        productTab = ProductTab(self.root, "Productos", self.productData)
        productTab.hide()
        self.tabs.append(productTab)

        messageTab = MessageTab(self.root, "Mensajes", self.messageData)
        messageTab.hide()
        self.tabs.append(messageTab)

    def init_navBar(self):
        navBar = Frame(self.root, background="blue")
        navBar.place(x=0, y=0, width=120, height=720)

        btnCustomer = Button(navBar, text="Clientes", font=("Arial", 18), background="aqua", borderwidth=1, command=lambda:self.show_tab(0))
        btnCustomer.place(x=0, y=0, width=120, height=80)
        btnProduct = Button(navBar, text="Productos", font=("Arial", 18), background="aqua", borderwidth=1, command=lambda:self.show_tab(1))
        btnProduct.place(x=0, y=80, width=120, height=80)
        btnMessage = Button(navBar, text="Mensajes", font=("Arial", 18), background="aqua", borderwidth=1, command=lambda:self.show_tab(2))
        btnMessage.place(x=0, y=640, width=120, height=80)