from interfaces.Tab import Tab
from tkinter import *
from tkinter import ttk

class CustomerTab(Tab):

    def __init__(self, master, tittle, data):
        super().__init__(master=master, title=tittle)
        self.data = data
        self.data.sort(key = lambda x: x.name)

        self.inputs = []

        self.canvas = self.init_widgets()

    def reOrder(self, attribute):
        if attribute == 'nombre' or attribute == "":
            self.data.sort(key = lambda x: x.name)
            self.set_buttons(self.canvas)
        elif attribute == 'apellido':
            self.data.sort(key = lambda x: x.lastName)
            self.set_buttons(self.canvas)
        elif attribute == 'saldo':
            self.data.sort(key = lambda x: x.balance)
            self.set_buttons(self.canvas)

    def set_buttons(self, canvas):
        canvas.delete('all')
        canvasHeight = 25
        for i, c in enumerate(self.data):
            if self.inputs[0].get() in c.name and self.inputs[1].get() in c.lastName and self.inputs[2].get() in c.ci:
                btn = Button(canvas, text=f"{c.name} {c.lastName}", justify=LEFT, font=("Arial", 13), borderwidth=1, background="blue")
                btn.config(width=250, height=2)
                canvas.create_window(40, 25+(canvasHeight), window=btn)
                canvasHeight += 40

        canvas.config(scrollregion=(0,0,300, canvasHeight))
        return canvas

    def init_widgets(self):

        textName = Label(self.frame, text="Nombre:", font=('Arial', 12))
        textLastName = Label(self.frame, text="Apellido:",font=('Arial', 12))
        textCi = Label(self.frame, text="Cédula:",font=('Arial', 12))

        inputName = Entry(self.frame, font=('Arial', 12))
        inputLastName = Entry(self.frame, font=('Arial', 12))
        inputCi = Entry(self.frame, font=('Arial', 12))

        self.inputs.append(inputName)
        self.inputs.append(inputLastName)
        self.inputs.append(inputCi)

        textName.place(x=10, y=230)
        textLastName.place(x=10, y=270)
        textCi.place(x=320, y=270)

        inputName.place(x=80, y=230)
        inputLastName.place(x=80, y=270)
        inputCi.place(x=380, y=270)

        canvas = Canvas(self.frame)
        canvas.place(x=10, y=300, width=900, height=400) 

        ybar = Scrollbar(self.frame)
        ybar.config(command=canvas.yview)                   
        canvas.config(yscrollcommand=ybar.set)              
        ybar.place(x=910, y=300, width=30, height=400)

        canvas = self.set_buttons(canvas)

        btnFilter = Button(self.frame, text="Filtrar", font=("Arial", 18), background="aqua", command=lambda:self.set_buttons(canvas))
        btnFilter.place(x=800, y=230, width=100, height=60)

        orderList = ttk.Combobox(self.frame, state="readonly", values=['nombre', 'apellido', 'saldo'])
        orderList.place(x=650, y=100)

        btnFilter = Button(self.frame, text="Ordenar", font=("Arial", 18), background="aqua", command=lambda:self.reOrder(orderList.get()))
        btnFilter.place(x=800, y=100, width=100, height=60)
        
        return canvas
