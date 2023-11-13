from interfaces.Tab import Tab
from tkinter import *

class CustomerTab(Tab):

    def __init__(self, master, tittle, data):
        super().__init__(master=master, title=tittle)
        self.data = data

        self.init_widgets()

    def init_widgets(self):
        canvas = Canvas(self.frame)
        canvas.config(background="blue")
        canvas.place(x=0, y=300, width=900, height=400) 

        ybar = Scrollbar(self.frame)
        ybar.config(command=canvas.yview)                   
        canvas.config(yscrollcommand=ybar.set)              
        ybar.place(x=900, y=300, width=30, height=400)

        #INGRESAR DATA PARA SABER EL TAMAGNO DE CANVAS
        canvas.config(scrollregion=(0,0,300, 1000))

        textName = Label(self.frame, text="Nombre:", font=('Arial', 12))
        textLastName = Label(self.frame, text="Apellido:",font=('Arial', 12))
        textCi = Label(self.frame, text="Cédula:",font=('Arial', 12))

        inputName = Entry(self.frame, font=('Arial', 12))
        inputLastName = Entry(self.frame, font=('Arial', 12))
        inputCi = Entry(self.frame, font=('Arial', 12))

        textName.place(x=10, y=230)
        textLastName.place(x=10, y=270)
        textCi.place(x=320, y=270)

        inputName.place(x=80, y=230)
        inputLastName.place(x=80, y=270)
        inputCi.place(x=380, y=270)

        btnNew = Button(self.frame, text="Añadir", font=('Arial', 18), background="#7CFF4F")
        btnNew.place(x=800, y=20, width=100, height=60)

        btnFilter = Button(self.frame, text="Filtrar", font=("Arial", 18), background="aqua")
        btnFilter.place(x=800, y=230, width=100, height=60)
