from tkinter import *
from tkinter import ttk
from interfaces.CustFrame import CustFrame

class GUI:

    def __init__(self, data):
        self.data = data
        self.font_size_p = 24
        self.buttons = []

        self.root = Tk()
        self.root.title('Cantina Maria Auxiliadora')
        self.root.geometry("1440x960")
        self.root.resizable(0, 0)

        self.mainFrame = Frame(self.root, background='blue')
        self.mainFrame.place(x=0, y=0, width=1440, height=960)

        self.canvas = Canvas(self.mainFrame, bd=0, highlightthickness=0)
        self.canvas.place(x=0, y=494, width=1440, height=466) 

        self.init_widgets()

        for j, i in enumerate(data):
            self.buttons.append(CustFrame(self.canvas, i, self.root, self.mainFrame))

        self.set_buttons()

        self.mainFrame.mainloop()

    def p(self, num):
        print(num)

    def set_buttons(self):
        self.canvas.delete('all')
        canvasHeight = 10

        for b in self.buttons:
            self.canvas.create_window(40, 20+(canvasHeight), window=b.button)
            canvasHeight += 65

        self.canvas.config(scrollregion=(0,0,300, canvasHeight))

    def init_widgets(self):

        textName = Label(self.mainFrame, text="Nombre:", font=('Arial', self.font_size_p))
        textLastName = Label(self.mainFrame, text="Apellido:",font=('Arial', self.font_size_p))
        textCi = Label(self.mainFrame, text="Cédula:",font=('Arial', self.font_size_p))

        inputName = Entry(self.mainFrame, font=('Arial', self.font_size_p))
        inputLastName = Entry(self.mainFrame, font=('Arial', self.font_size_p))
        inputCi = Entry(self.mainFrame, font=('Arial', self.font_size_p))

        textName.place(x=0, y=134)
        textLastName.place(x=0, y=210)
        textCi.place(x=0, y=286)

        inputName.place(x=138, y=134)
        inputLastName.place(x=138, y=210)
        inputCi.place(x=138, y=286)

        ybar = Scrollbar(self.mainFrame)
        ybar.config(command=self.canvas.yview)                   
        self.canvas.config(yscrollcommand=ybar.set)              
        ybar.place(x=1410, y=494, width=30, height=466)

        btnFilter = Button(self.mainFrame, text="Filtrar", font=("Arial", 24), background='aqua', highlightbackground = "black", command=lambda:self.set_buttons(canvas))
        btnFilter.place(x=146, y=366, width=164, height=83)

        orderList = ttk.Combobox(self.mainFrame, state="readonly", values=['nombre', 'apellido', 'saldo'], font=("Arial", 24))
        orderList.place(x=790, y=200)

        btnOrder = Button(self.mainFrame, text="Ordenar", font=("Arial", 24), background="aqua", command=lambda:self.reOrder(orderList.get()))
        btnOrder.place(x=1195, y=200, width=210, height=83)
        
        btnAdd = Button(self.mainFrame, text="Añadir", font=("Arial", 24), background="#009846")
        btnAdd.place(x=1195, y=50, width=210, height=83)