from interfaces.Tab import Tab
from tkinter import *
from tkinter import ttk

class MainMenu(Tab):

    def __init__(self, master, tittle, data):
        super().__init__(master=master, title=tittle)
        
        self.data = data
        self.data.sort(key = lambda x: x.name)

        self.font_size_p = 24

        self.inputs = []
        self.buttons = []

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
        self.buttons.clear()
        canvasHeight = 0
        numberButtons = -1
        for i, c in enumerate(self.data):
            if self.inputs[0].get() in c.name and self.inputs[1].get() in c.lastName and self.inputs[2].get() in c.ci:
                numberButtons += 1
                # self.buttons.append(TopLevelCust(canvas, c))
                # canvas.create_window(40, 20+(canvasHeight), window=self.buttons[numberButtons].button)

                canvasHeight += 55

        canvas.config(scrollregion=(0,0,300, canvasHeight))
        return canvas

    def init_widgets(self):

        textName = Label(self.frame, text="Nombre:", font=('Arial', self.font_size_p))
        textLastName = Label(self.frame, text="Apellido:",font=('Arial', self.font_size_p))
        textCi = Label(self.frame, text="Cédula:",font=('Arial', self.font_size_p))

        inputName = Entry(self.frame, font=('Arial', self.font_size_p))
        inputLastName = Entry(self.frame, font=('Arial', self.font_size_p))
        inputCi = Entry(self.frame, font=('Arial', self.font_size_p))

        self.inputs.append(inputName)
        self.inputs.append(inputLastName)
        self.inputs.append(inputCi)

        textName.place(x=0, y=134)
        textLastName.place(x=0, y=210)
        textCi.place(x=0, y=286)

        inputName.place(x=138, y=134)
        inputLastName.place(x=138, y=210)
        inputCi.place(x=138, y=286)

        canvas = Canvas(self.frame)
        canvas.place(x=0, y=494, width=1440, height=466) 

        ybar = Scrollbar(self.frame)
        ybar.config(command=canvas.yview)                   
        canvas.config(yscrollcommand=ybar.set)              
        ybar.place(x=1410, y=494, width=30, height=466)

        canvas = self.set_buttons(canvas)

        btnFilter = Button(self.frame, text="Filtrar", font=("Arial", 24), background='aqua', highlightbackground = "black", command=lambda:self.set_buttons(canvas))
        btnFilter.place(x=146, y=366, width=164, height=83)

        orderList = ttk.Combobox(self.frame, state="readonly", values=['nombre', 'apellido', 'saldo'], font=("Arial", 24))
        orderList.place(x=790, y=200)

        btnOrder = Button(self.frame, text="Ordenar", font=("Arial", 24), background="aqua", command=lambda:self.reOrder(orderList.get()))
        btnOrder.place(x=1195, y=200, width=210, height=83)
        
        btnAdd = Button(self.frame, text="Añadir", font=("Arial", 24), background="#009846")
        btnAdd.place(x=1195, y=50, width=210, height=83)

        return canvas
