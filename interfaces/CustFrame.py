from tkinter import *
from datetime import datetime


class CustFrame:

    def __init__(self, master, customer, root, mainFrane):

        self.date = datetime.now()

        self.master = master
        self.root = root
        self.customer = customer
        self.mainFrame = mainFrane

        self.currentCard = customer.history

        self.frame = Frame(root)
        self.button = Button(master,text=f"{self.customer.name.upper()}", command=lambda:self.init_widgets(), background='aqua', width=390, height=3, font=("Arial", 12))
        self.header = Label(self.frame, font=('Arial', 32), justify=LEFT, padx=5, pady=5,
                        text=f"{self.customer.name.capitalize()} {self.customer.lastName.capitalize()}\nCI:{self.customer.ci}\nTeléfono{self.customer.phone}")
        self.header.place(x=40, y=80)

        self.frameAbonar = Frame(self.frame, background="blue")
        self.abonar_widgets()

        self.frameFiar = Frame(self.frame, background="orange")
        self.fiar_widgets()

        self.frameBase = Frame(self.frame, background="green")
        self.frameBase.place(x=0, y=300, width=600, height=640)

        self.balanceArea = Label(self.frame, text=f"{self.customer.balance} $", font=('Arial', 32), background="green")
        self.balanceArea.place(x=720, y=110, width=653, height=50)

        self.yellowCard = Listbox(self.frame, background='#FDFF88', font=("Arial", 18))
        self.yellowCard.place(x=720, y=167, width=653, height=760)
        self.frame.bind_all("<MouseWheel>", self.mousewheel)

        self.set_list_box()

    def set_list_box(self):
        self.yellowCard.delete(0,END)

        for h in self.currentCard:
            if h != {}:
                self.yellowCard.insert(END, h['date'])
                for i in h['p']:
                    self.yellowCard.insert(END, f"      {i['quantity']} {i['product']}: {i['price']} $")

    def save(self, resets, num, cancel):

        for i in resets:
            i.delete(0, END)
        if self.currentCard[0]['p'] != [] and not cancel:
            self.customer.history.append({'date': self.currentCard[0]['date'], 'p': self.currentCard[0]['p']})
        if num == 0:
            self.quit_fiar()
        elif num == 1:
            self.quit_abonar()

    def addToCard(self, info):
        ticket = []
        for i in info:
            if i.get() == '':
                return
            else:
                ticket.append(i.get())
                i.delete(0, END)
        if len(ticket) == 3:
            try:
                self.currentCard[0]['p'].append({'quantity':int( ticket[2]), 'price': -float(ticket[1])*float(ticket[2]), 'product': ticket[0]})
            except:
                return
        elif len(ticket) ==  1:
            try:
                self.currentCard[0]['p'].append({'quantity': 1, 'price': float(ticket[0]), 'product': 'Abono'})
            except:
                return
        
        self.set_list_box()

    def abonar(self):
        self.currentCard = [{"date": f'{self.date.day}/{self.date.month}/{self.date.year}  {self.date.hour}:{self.date.minute}', 'p': []}]
        self.set_list_box()
        self.frameBase.place_forget()
        self.frameAbonar.place(x=0, y=300, width=600, height=640)

    def quit_abonar(self):
        self.currentCard = self.customer.history
        self.set_list_box()
        self.frameAbonar.place_forget()
        self.frameBase.place(x=0, y=300, width=600, height=640)

    def fiar(self):
        self.currentCard = [{"date": f'{self.date.day}/{self.date.month}/{self.date.year}  {self.date.hour}:{self.date.minute}', 'p': []}]
        self.set_list_box()
        self.frameBase.place_forget()
        self.frameFiar.place(x=0, y=300, width=600, height=640)

    def quit_fiar(self):
        self.currentCard = self.customer.history
        self.set_list_box()
        self.frameFiar.place_forget()
        self.frameBase.place(x=0, y=300, width=600, height=640)

    def mousewheel(self, event):
        self.yellowCard.yview_scroll(-1 * int(event.delta / 120), "units")

    def abonar_widgets(self):
        textAbono = Label(self.frameAbonar, text="Abonar:", font=('Arial', 24))
        inputAbono = Entry(self.frameAbonar, font=('Arial', 24))

        textAbono.place(x=10, y=34)
        inputAbono.place(x=158, y=34)

        btnAddAbono = Button(self.frameAbonar, text="Añadir", font=('Arial', 24), command=lambda:self.addToCard([inputAbono]))
        btnAddAbono.place(x=200, y=100)

        btnSave = Button(self.frameAbonar, text = 'Guardar', font=('Arial', 24), command=lambda: self.save([inputAbono], 1, False))
        btnSave.place(x=430, y=500)

        btnCancel = Button(self.frameAbonar, text = 'Cancelar', font=('Arial', 14), background='red', command=lambda: self.save([inputAbono], 0, True))
        btnCancel.place(x=20, y=520)


    def fiar_widgets(self):
        textProduct = Label(self.frameFiar, text="Producto:", font=('Arial', 24))
        textPrice = Label(self.frameFiar, text="Precio:",font=('Arial', 24))
        textQuantity = Label(self.frameFiar, text="Cantidad",font=('Arial', 24))

        inputProduct = Entry(self.frameFiar, font=('Arial', 24))
        inputPrice = Entry(self.frameFiar, font=('Arial', 24))
        inputQuantity = Entry(self.frameFiar, font=('Arial', 24))

        textProduct.place(x=10, y=34)
        textPrice.place(x=10, y=110)
        textQuantity.place(x=10, y=186)

        inputProduct.place(x=158, y=34)
        inputPrice.place(x=158, y=110)
        inputQuantity.place(x=158, y=186)

        btnAddProduct = Button(self.frameFiar, text="Añadir", font=('Arial', 24), command=lambda:self.addToCard([inputProduct, inputPrice, inputQuantity]))
        btnAddProduct.place(x=200, y=270)

        btnSave = Button(self.frameFiar, text = 'Guardar', font=('Arial', 24), command=lambda: self.save([inputProduct, inputPrice, inputQuantity], 0, False))
        btnSave.place(x=430, y=500)

        btnCancel = Button(self.frameFiar, text = 'Cancelar', font=('Arial', 14), background='red', command=lambda: self.save([inputProduct, inputPrice, inputQuantity], 0, True))
        btnCancel.place(x=20, y=520)



    def init_widgets(self):
        self.mainFrame.place_forget()
        self.frame.place(x=0, y=0, width=1440, height=960)

        btnBack = Button(self.frame, text="Regresar", font=("Arial", 24), command=self.quit)
        btnBack.place(x=10, y=10)

        btnAbonar = Button(self.frameBase, text="Abonar", font=("Arial", 24), command=self.abonar)
        btnAbonar.place(x=39, y=70)
        
        btnFiar = Button(self.frameBase, text="Fiar", font=("Arial", 24), command=self.fiar)
        btnFiar.place(x=39, y=170)
        
        btnMessage = Button(self.frameBase, text="Mensaje", font=("Arial", 24))
        btnMessage.place(x=39, y=270)

        btnDelete = Button(self.frameBase, text="Eliminar", font=("Arial", 18))
        btnDelete.place(x=20, y=570)
        
    def quit(self):
        self.quit_abonar()
        self.frame.place_forget()
        self.mainFrame.place(x=0, y=0, width=1440, height=960)