from interfaces.Tab import Tab
from interfaces.TopLevelProd import TopLevelProd

from tkinter import *
from tkinter import ttk

class ProductTab(Tab):

    def __init__(self, master, title, data):
        super().__init__(master=master, title=title)
        self.data = data

        self.data.sort(key = lambda x: x.name)

        self.inputs = []
        self.buttons = []

        self.canvas = self.init_widgets()

    def reOrder(self, attribute):
        if attribute == 'nombre' or attribute == "":
            self.data.sort(key = lambda x: x.name)
            self.set_buttons(self.canvas)
        elif attribute == 'precio':
            self.data.sort(key = lambda x: x.price)
            self.set_buttons(self.canvas)

    def set_buttons(self, canvas):
        canvas.delete('all')
        canvasHeight = 25
        self.buttons.clear()
        for i, p in enumerate(self.data):
            if self.inputs[0].get() in p.name and (self.inputs[2].get() in p.type or self.inputs[2].get()=="todos"):
                self.buttons.append(TopLevelProd(canvas, p))
                canvas.create_window(40, 25+(canvasHeight), window=self.buttons[i].button)
                canvasHeight += 40

        canvas.config(scrollregion=(0,0,300, canvasHeight))
        return canvas

    def init_widgets(self):

        textName = Label(self.frame, text="Nombre:", font=('Arial', 12))
        textPrice = Label(self.frame, text="precio:",font=('Arial', 12))
        textType = Label(self.frame, text="tipo:",font=('Arial', 12))

        inputName = Entry(self.frame, font=('Arial', 12))
        inputPrice = Entry(self.frame, font=('Arial', 12))
        inputType = ttk.Combobox(self.frame, font=('Arial', 12), values=["bebidas", "comidas", "almuerzos", "todos"], state="readonly")

        self.inputs.append(inputName)
        self.inputs.append(inputPrice)
        self.inputs.append(inputType)

        textName.place(x=10, y=230)
        textPrice.place(x=10, y=270)
        textType.place(x=320, y=230)

        inputName.place(x=80, y=230)
        inputPrice.place(x=80, y=270)
        inputType.place(x=380, y=230)

        canvas = Canvas(self.frame)
        canvas.place(x=10, y=300, width=900, height=400) 

        ybar = Scrollbar(self.frame)
        ybar.config(command=canvas.yview)                   
        canvas.config(yscrollcommand=ybar.set)              
        ybar.place(x=910, y=300, width=30, height=400)

        canvas = self.set_buttons(canvas)

        btnNew = Button(self.frame, text="Añadir", font=('Arial', 18), background="#7CFF4F")
        btnNew.place(x=800, y=20, width=100, height=60)

        btnFilter = Button(self.frame, text="Filtrar", font=("Arial", 18), background="aqua", command=lambda:self.set_buttons(canvas))
        btnFilter.place(x=800, y=230, width=100, height=60)

        orderList = ttk.Combobox(self.frame, state="readonly", values=['nombre', 'precio'])
        orderList.place(x=650, y=100)

        btnFilter = Button(self.frame, text="Ordenar", font=("Arial", 18), background="aqua", command=lambda:self.reOrder(orderList.get()))
        btnFilter.place(x=800, y=100, width=100, height=60)
        
        return canvas

    