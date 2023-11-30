from customtkinter import *
from interfaces.CButton import CButton
from clases.Customer import Customer
from db import *

class Gui(CTk):

    def __init__(self, data):
        super().__init__()
        self.data = data
        self.geometry('720x720')
        self.resizable(0, 0)
        self.title('Cantina')

        self.titleFont = ('calibri', 32)
        self.buttonFont = ('calibri', 24)
        self.labelFont = ('calibri', 18)

        ww = 720
        wh = 720

        menuFrame = CTkFrame(self, width=720, height=720)
        menuFrame.pack()

        #TITULO DEL MAIN
        title = CTkLabel(menuFrame, text="Cantina María Auxiliadora", font=self.titleFont)
        title.place(x=10, y=10)

        #BOTON DE ANADIR
        btnNew = CTkButton(menuFrame, text="Añadir", fg_color='green', width=150, height=40, font=self.buttonFont,
                            command=self.addWindow)
        btnNew.place(x=ww-160, y=10)

        self.toplevel_window = None

    def open_customer(self, index):
        pass

    def add_data(self, name, lastName, ci, phoneExt, phoneNum):
        
        if name.get() != '' and lastName.get() != '' and ci.get().isnumeric() and len(phoneExt.get())==4 and phoneExt.get().isnumeric() and phoneNum.get().isnumeric():
            newCust = Customer(len(self.data)+1, name.get(), lastName.get(), ci.get(), f'+58{phoneExt.get()[1:]}{phoneNum.get()}', 0, 'Nunca')
            self.data.append(newCust)
            save_customer(self.data)
            print('guardado')

    def update_data(self, index, updatedCustomer):
        pass

    def addWindow(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = CTkToplevel(self)  # create window if its None or destroyed
            self.toplevel_window.attributes('-topmost', 'true')
            self.toplevel_window.geometry('480x480')

            name = StringVar(self.toplevel_window, '')
            lastName = StringVar(self.toplevel_window, '')
            ci = StringVar(self.toplevel_window, '')
            phoneExt =StringVar(self.toplevel_window, '')
            phoneNum = StringVar(self.toplevel_window, '')

            CTkLabel(self.toplevel_window, text='Nombre', font=self.labelFont, width=100, height=30).place(x=10, y=10)
            inputName = CTkEntry(self.toplevel_window, textvariable=name,  placeholder_text="Apellido", font=self.labelFont, width=300, height=30).place(x=120, y=10)
            CTkLabel(self.toplevel_window, text='Apellido', font=self.labelFont, width=100, height=30).place(x=10, y=50)
            inputLastName = CTkEntry(self.toplevel_window, textvariable=lastName, placeholder_text="Apellido", font=self.labelFont, width=300, height=30).place(x=120, y=50)
            CTkLabel(self.toplevel_window, text='Cédula', font=self.labelFont, width=100, height=30).place(x=10, y=90)
            inputCi = CTkEntry(self.toplevel_window, textvariable=ci,placeholder_text="Cédula", font=self.labelFont, width=300, height=30).place(x=120, y=90)
            CTkLabel(self.toplevel_window, text='Teléfono', font=self.labelFont, width=100, height=30).place(x=10, y=130)
            inputPhoneExt = CTkEntry(self.toplevel_window, textvariable=phoneExt, placeholder_text="04xx", font=self.labelFont, width=50, height=30).place(x=120, y=130)
            inputPhoneNum = CTkEntry(self.toplevel_window, textvariable=phoneNum, placeholder_text="1110000", font=self.labelFont, width=240, height=30).place(x=180, y=130)
        
            btnSaveNew = CTkButton(self.toplevel_window, text="Guardar", fg_color='green', width=150, height=40, font=self.buttonFont, command=lambda:self.add_data(name, lastName, ci, phoneExt, phoneNum)).place(x=165, y=200)
            btnCancel = CTkButton(self.toplevel_window, text="Cancelar", fg_color='red', width=120, height=40, font=self.buttonFont, command=lambda:self.toplevel_window.destroy()).place(x=10, y=430) #Customer(len(self.data)+1, inputName.get(), inputLastName.get(), inputCi.get(),f'+58{inputPhoneExt}{inputPhoneNum}', 0, 'Nunca')

        else:
            self.toplevel_window.deiconify()  #if window exists focus it
