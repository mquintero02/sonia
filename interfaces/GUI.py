from customtkinter import *
from tkinter import *
from CTkMessagebox import CTkMessagebox
import requests
from interfaces.CButton import CButton
from clases.Customer import Customer
from clases.Compra import Compra
from db import *
from datetime import datetime, timedelta
import pyperclip

class Gui(CTk):

    def __init__(self, data, hData):
        super().__init__()
        self.data = data
        self.hData = hData
        self.geometry('720x720')
        self.resizable(0, 0)
        self.title('Cantina')
     
        self.toplevel_window = None

        self.titleFont = ('calibri', 32)
        self.titleFont2 = ('calibri', 26)
        self.buttonFont = ('calibri', 24)
        self.labelFont = ('calibri', 20)

        self.ww = 720
        self.wh = 720

        self.auxList = []
        self.weekDays = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

        #FRAME DE ENTRADA----------------------------------------------------------------------------

        self.menuFrame = None

        #FRAME DE COMPRADORES-------------------------------------------------------------------------------

        self.customerFrame = None

        self.open_menu()

    #FUNCIONES DE VENTANAS PRINCIPALES-----------------------------------------

    def open_menu(self):
        if not self.customerFrame is None:
            self.customerFrame.destroy()
        if self.menuFrame is None or not self.menuFrame.winfo_exists():
            self.menuFrame = CTkFrame(self, width=720, height=720)
            self.menuFrame.pack()

            self.data.sort(key=lambda x: x.name.lower(), reverse=False)

            #TITULO DEL MAIN
            title = CTkLabel(self.menuFrame, text="Cantina María Auxiliadora", font=self.titleFont)
            title.place(x=10, y=10)

            #BOTON DE ANADIR
            btnNew = CTkButton(self.menuFrame, text="Añadir", fg_color='green', width=150, height=40, font=self.buttonFont,
                                command=self.addWindow)
            btnNew.place(x=self.ww-160, y=10)

            #SCROLLFRAME
            sf = CTkScrollableFrame(self.menuFrame, width=690, height=360)
            sf.place(x=0, y=360)

            for c in self.data:
                CButton(c, sf, self).set_button()

            #FILTROS
            filterName = CTkEntry(self.menuFrame, placeholder_text="Nombre", font=self.labelFont)
            filterName.place(x=10, y=150)

            filterLastName = CTkEntry(self.menuFrame, placeholder_text="Apellido", font=self.labelFont)
            filterLastName.place(x=10, y=200)

            filterCi = CTkEntry(self.menuFrame, placeholder_text="Cédula", font=self.labelFont)
            filterCi.place(x=10, y=250)

            btnfilter = CTkButton(self.menuFrame, text="Filtrar", width=140, height=40, font=self.buttonFont,
                                command=lambda:self.filter(filterName.get(), filterLastName.get(), filterCi.get(), sf))
            btnfilter.place(x=10, y=300)

            btnResetFilter =CTkButton(self.menuFrame, text="Eliminar filtro", width=150, height=40, font=self.buttonFont,
                                command=lambda:self.filter("", "", "", sf))
            btnResetFilter.place(x=180, y=300)

    def refresh_menu(self):
        self.menuFrame.destroy()
        self.open_menu()

    def open_customer(self, customer):
        self.menuFrame.destroy()
        if self.customerFrame is None or not self.customerFrame.winfo_exists():
            customerHData = list(customer.history)
            self.customerFrame = CTkFrame(self, width=720, height=720)
            self.customerFrame.pack()

            self.customerFrameTitle = CTkLabel(self.customerFrame, text=f'{customer.name}\nCI: {customer.ci}\nTeléfono: {customer.phone}', font=self.titleFont2, width=200).place(x=10, y=70)
            
            if customer.balance < 0:
                CTkLabel(self.customerFrame, text=f'Saldo: {customer.balance}$', fg_color='red', font=self.titleFont, width=370, height=40, corner_radius=5).place(x=310, y=20)
            elif customer.balance > 0:
                CTkLabel(self.customerFrame, text=f'Saldo: {customer.balance}$', fg_color='green', font=self.titleFont, width=370, height=40, corner_radius=5).place(x=310, y=20)
            else:
                CTkLabel(self.customerFrame, text=f'Saldo: {customer.balance}$', fg_color='blue', font=self.titleFont, width=370, height=40, corner_radius=5).place(x=310, y=20)

            sf = CTkScrollableFrame(self.customerFrame, width=370, height=600, fg_color='yellow')
            sf.place(x=310, y=70)

            for k in list(reversed(customerHData)):
                CTkLabel(sf, text=k, font=self.labelFont, text_color='black').pack()
                CTkLabel(sf, text=customer.history[k].items, font=self.labelFont, text_color='black', width=360, anchor=W).pack()
                CTkLabel(sf, text=f'Total: {customer.history[k].resultBalance}$', font=self.labelFont, text_color='black', width=360, anchor=E).pack()

            btnBack = CTkButton(self.customerFrame, text="Regresar", width=100, height=40, font=self.buttonFont, command=self.open_menu).place(x=10, y=10)
            btnFiar = CTkButton(self.customerFrame, text="Fiar", width=100, height=40, font=self.buttonFont, command=lambda:self.fiar_window(customer), fg_color='orange', text_color='black').place(x=20, y=200)
            btnAbonar = CTkButton(self.customerFrame, text='Abonar', width=100, height=40, font=self.buttonFont, fg_color='green', command=lambda:self.abonar_window(customer)).place(x=20, y=260)
            btnMessage = CTkButton(self.customerFrame, text='Enviar\nPendientes', width=100, height=40, font=self.buttonFont, command=lambda:self.send_message(customer)).place(x=100, y=360)
            btnDateMessage = CTkButton(self.customerFrame, text='Enviar\npor fecha', width=100, height=40, font=self.buttonFont, command=lambda:self.send_by_date_window(customer)).place(x=100, y=440)
            btnDetele = CTkButton(self.customerFrame, text='Eliminar', width=100, height=40, font=self.buttonFont, fg_color='red', command=lambda:self.delete_customer(customer)).place(x=10, y=670)
            btnModify = CTkButton(self.customerFrame, text='Modificar', width=100, height=40, font=self.buttonFont, fg_color='blue', command=lambda:self.modify_window(customer)).place(x=180, y=10)
            btnCorrection = CTkButton(self.customerFrame, text='Corregir\nSaldo', width=100, height=40, font=self.buttonFont, fg_color='blue', command=lambda:self.correction_window(customer)).place(x=180, y=200)
            
    def refresh_customer_window(self, customer):
        self.customerFrame.destroy()
        self.open_customer(customer)

    #FUNCIONES DE VENTANAS PRINCIPALES-----------------------------------------

    #FUNCIONES DE MANEJO A BASE DE DATOS---------------------------------------

    def add_data(self, name, ci, phoneNum):
        if name.get() != '' and ci.get().isnumeric() and phoneNum.get().isnumeric():
                        
            newId = int(read_last_index()) + 1
            newCust = Customer(newId, name.get(), ci.get(), f'{phoneNum.get()}', 0)
            self.data.append(newCust)
            save_customer(self.data)
            save_last_index(newId)
            self.refresh_menu()
            self.toplevel_window.destroy()
        else:
            CTkMessagebox(message="Datos no válidos")

    def add_to_aux_list(self, product, quantity, price, sf):
        try:
            if product.get() != "" and quantity.get() != "" and quantity.get().isnumeric() and price.get() != "":
                self.auxList.append({'name': product.get(), 'quantity':quantity.get(), 'price':-float(price.get())*float(quantity.get())})
                CTkLabel(sf, text=f'{quantity.get()} {product.get()}: {-float(price.get())*float(quantity.get())}$', text_color='black', font=self.labelFont, anchor='w', width=440).pack()
                product.set('')
                quantity.set('')
                price.set('')
            else:
                CTkMessagebox(message="Datos no válidos")
        except:
            CTkMessagebox(message="Datos no válidos")

    def add_to_aux_list_deposito(self, amount, sf):
        try:
            self.auxList.append({'name': 'Depósito', 'quantity':'1', 'price':amount.get()})
            CTkLabel(sf, text=f'{1} "Depósito": {amount.get()}$', text_color='black', font=self.labelFont, anchor='w', width=440).pack()
            amount.set('')
        except:
            CTkMessagebox(message="Datos no válidos")

    def add_to_aux_list_correction(self, amount, customer):
        try:
            actualBalance = -(customer.balance - float(amount.get()))
            self.auxList.append({'name': 'Corrección de saldo', 'quantity':'1', 'price':actualBalance})
            amount.set('')
            self.save_fiar(customer)
        except:
            CTkMessagebox(message="Datos no válidos")

    def save_fiar(self, customer, amount, items):
        try:
            amount = float(amount)
        except:
            CTkMessagebox(message="Datos no válidos")
            return

        if items != "Depósito":
            amount = -amount
        else:
            items = f'Depósito: {amount}$'

        if items != '':
            index = self.data.index(customer)

            date = datetime.now()
            dateDay = date.weekday()

            dateStr = f'{self.weekDays[dateDay]} {date.day}/{date.month}/{date.year}'

            customer.add_history(date, dateStr, items, amount)

            self.update_data(index, customer)
            self.refresh_customer_window(customer)
            print(customer.history)
            self.close_fiar_window()
        else:
            CTkMessagebox(message="Datos no válidos")

    def update_data(self, index, updatedCustomer):
        self.data[index] = updatedCustomer
        save_customer(self.data)

    def modify_data(self, customer, index, name, ci, phoneNum):
        if name.get() != '' and ci.get().isnumeric() and phoneNum.get().isnumeric():
            customer.name = name.get()
            customer.ci = ci.get()
            customer.phone = f'{phoneNum.get()}'
            self.update_data(index, customer)
            self.refresh_customer_window(customer)
            self.toplevel_window.destroy()
        else:
            CTkMessagebox(message="Datos no válidos")

    def delete_customer(self, customer):
        option = CTkMessagebox(message=f"¿Seguro que quieres eliminar a {customer.name} {customer.lastName}?",option_2="No", option_1="Si", font=self.labelFont)
        response = option.get()

        if response == "Si":
            self.data.remove(customer)
            save_customer(self.data)
            self.open_menu()

    def reset_aux_list(self):
        self.auxList.clear()

    #FUNCIONES DE MANEJO A BASE DE DATOS---------------------------------------

    #MANIPULAR LISTA DE CLIENTES----------------------------------------------
    
    def filter(self, name, lastName, ci, sf):
        for c in sf.winfo_children():
            c.destroy()

        for c in self.data:
            if f"{name}".lower() in c.name.lower() and f"{lastName}".lower() in c.lastName.lower() and f"{ci}".lower() in c.ci.lower():
                CButton(c, sf, self).set_button()    

     #MANIPULAR LISTA DE CLIENTES----------------------------------------------

    #MANIPULAR LISTA DE CLIENTES----------------------------------------------

    #MENSAJERIA------------------------------------------------------------------
    def check_conection(self, customer):
        try:
            request = requests.get("https://google.com", timeout=5)
        except (requests.ConnectionError, requests.Timeout):
            CTkMessagebox(message="Sin conexión a internet")
            return
        else:
            print("Con conexión a internet.")
        self.send_message(customer)

    def prepare_message(self, customer, day, month, year):
        try:
            date = datetime(int(year), int(month), int(day))
        except:
            CTkMessagebox(message="Datos no válidos")
            return

        history = list(customer.history)

        for k in list(reversed(history)):
            if customer.history[k].date >= date:
                customer.history[k].sent = False
            else:
                break

        self.send_message(customer)
        self.close_fiar_window()

    def prepare_week_message(self, customer):
        date = datetime.now()
        deltaTime = timedelta(weeks=1)
        auxDate = date - deltaTime

        history = list(customer.history)

        for k in list(reversed(history)):
            if customer.history[k].date >= auxDate:
                customer.history[k].sent = False
            else:
                break

        self.send_message(customer)
        self.close_fiar_window()

    def send_message(self, customer):
        message = "Buen día, este es el reporte de su cuenta en la Cantina del Colegio María Auxiliadora\n"
        message2 = ""
        history = list(customer.history)

        if customer.balance < 0:
            message += f"Posee una deuda de: {customer.balance}$"
        elif customer.balance > 0:
            message += f"Posee un saldo a favor de: {customer.balance}$"
        else:
            message += f"Su saldo es de 0$"

        message += "\n\n"

        for k in list(reversed(history)):
            if customer.history[k].sent:
                break
            else:
                message += customer.history[k].toString()
                customer.history[k].sent = True
        
        self.update_data(self.data.index(customer), customer)
        self.refresh_customer_window(customer)   

        pyperclip.copy(message)
    
    #MENSAJERIA------------------------------------------------------------------

    #VENTANAS SECUNDARIAS--------------------------------------------------------
    #CLIENTES
    def addWindow(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = CTkToplevel(self)  # create window if its None or destroyed
            self.toplevel_window.attributes('-topmost', 'true')
            self.toplevel_window.geometry('480x480')

            name = StringVar(self.toplevel_window, '')
            ci = StringVar(self.toplevel_window, '')
            phoneNum = StringVar(self.toplevel_window, '')

            CTkLabel(self.toplevel_window, text='Nombre', font=self.labelFont, width=100, height=30).place(x=10, y=10)
            inputName = CTkEntry(self.toplevel_window, textvariable=name,  placeholder_text="Nombre", font=self.labelFont, width=300, height=30).place(x=120, y=10)
            CTkLabel(self.toplevel_window, text='CI', font=self.labelFont, width=100, height=30).place(x=10, y=50)
            inputCi = CTkEntry(self.toplevel_window, textvariable=ci,placeholder_text="Cédula", font=self.labelFont, width=300, height=30).place(x=120, y=50)
            CTkLabel(self.toplevel_window, text='Teléfono', font=self.labelFont, width=100, height=30).place(x=10, y=130)
            inputPhoneNum = CTkEntry(self.toplevel_window, textvariable=phoneNum, placeholder_text="04xx1111111", font=self.labelFont, width=300, height=30).place(x=120, y=130)
        
            btnSaveNew = CTkButton(self.toplevel_window, text="Guardar", fg_color='green', width=150, height=40, font=self.buttonFont, command=lambda:self.add_data(name, ci, phoneNum)).place(x=165, y=200)
            btnCancel = CTkButton(self.toplevel_window, text="Cancelar", fg_color='red', width=120, height=40, font=self.buttonFont, command=lambda:self.toplevel_window.destroy()).place(x=10, y=430) #Customer(len(self.data)+1, inputName.get(), inputLastName.get(), inputCi.get(),f'+58{inputPhoneExt}{inputPhoneNum}', 0, 'Nunca')

        else:
            self.toplevel_window.deiconify()  #if window exists focus it

    def fiar_window(self, customer):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = CTkToplevel(self)  # create window if its None or destroyed
            self.toplevel_window.attributes('-topmost', 'true')
            self.toplevel_window.geometry('480x380')

            amount = StringVar(self.toplevel_window, '')

            inputText = Text(self.toplevel_window, background="yellow", font=self.labelFont)
            inputText.place(x=20, y=10, width=440, height=200)

            CTkLabel(self.toplevel_window, text='Monto c/u', font=self.labelFont, width=100, height=30).place(x=10, y=250)
            inputPrice = CTkEntry(self.toplevel_window, textvariable=amount,placeholder_text="Precio", font=self.labelFont, width=100, height=30).place(x=120, y=250)

            btnSaveNew = CTkButton(self.toplevel_window, text="Guardar", fg_color='green', width=150, height=40, font=self.buttonFont, command=lambda:self.save_fiar(customer, amount.get(), inputText.get('0.0', 'end'))).place(x=320, y=330)
            btnCancel = CTkButton(self.toplevel_window, text="Cancelar", fg_color='red', width=120, height=40, font=self.buttonFont, command=lambda:self.close_fiar_window()).place(x=10, y=330) #Customer(len(self.data)+1, inputName.get(), inputLastName.get(), inputCi.get(),f'+58{inputPhoneExt}{inputPhoneNum}', 0, 'Nunca')

        else:
            self.toplevel_window.deiconify()  #if window exists focus it

    def abonar_window(self, customer):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = CTkToplevel(self)  # create window if its None or destroyed
            self.toplevel_window.attributes('-topmost', 'true')
            self.toplevel_window.geometry('480x180')

            amount = StringVar(self.toplevel_window, '')

            CTkLabel(self.toplevel_window, text='Depósito($)', font=self.labelFont, width=100, height=30).place(x=10, y=40)
            inputAmount = CTkEntry(self.toplevel_window, textvariable=amount,  placeholder_text="Depósito($)", font=self.labelFont, width=300, height=30).place(x=120, y=40)

            btnSaveNew = CTkButton(self.toplevel_window, text="Guardar", fg_color='green', width=150, height=40, font=self.buttonFont, command=lambda:self.save_fiar(customer, amount.get(), 'Depósito')).place(x=320, y=130)
            btnCancel = CTkButton(self.toplevel_window, text="Cancelar", fg_color='red', width=120, height=40, font=self.buttonFont, command=lambda:self.close_fiar_window()).place(x=10, y=130) #Customer(len(self.data)+1, inputName.get(), inputLastName.get(), inputCi.get(),f'+58{inputPhoneExt}{inputPhoneNum}', 0, 'Nunca')

        else:
            self.toplevel_window.deiconify()  #if window exists focus it

    def close_fiar_window(self):
        self.reset_aux_list()
        self.toplevel_window.destroy()

    def correction_window(self, customer):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = CTkToplevel(self)  # create window if its None or destroyed
            self.toplevel_window.attributes('-topmost', 'true')
            self.toplevel_window.geometry('480x240')

            amount = StringVar(self.toplevel_window, '')

            CTkLabel(self.toplevel_window, text='Saldo corregido: ', font=self.labelFont, width=100, height=30).place(x=10, y=40)
            inputAmount = CTkEntry(self.toplevel_window, textvariable=amount,  placeholder_text="saldo", font=self.labelFont, width=300, height=30).place(x=150, y=40)

            btnSaveNew = CTkButton(self.toplevel_window, text="Guardar", fg_color='green', width=150, height=40, font=self.buttonFont, command=lambda:self.add_to_aux_list_correction(amount, customer)).place(x=320, y=130)
            btnCancel = CTkButton(self.toplevel_window, text="Cancelar", fg_color='red', width=120, height=40, font=self.buttonFont, command=lambda:self.close_fiar_window()).place(x=10, y=130) #Customer(len(self.data)+1, inputName.get(), inputLastName.get(), inputCi.get(),f'+58{inputPhoneExt}{inputPhoneNum}', 0, 'Nunca')

        else:
            self.toplevel_window.deiconify()

    def modify_window(self, customer):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = CTkToplevel(self)  # create window if its None or destroyed
            self.toplevel_window.attributes('-topmost', 'true')
            self.toplevel_window.geometry('480x480')

            index = self.data.index(customer)

            name = StringVar(self.toplevel_window, customer.name)
            ci = StringVar(self.toplevel_window, customer.ci)
            phoneNum = StringVar(self.toplevel_window, f'{customer.phone}')

            CTkLabel(self.toplevel_window, text='Nombre', font=self.labelFont, width=100, height=30).place(x=10, y=10)
            inputName = CTkEntry(self.toplevel_window, textvariable=name,  placeholder_text="Nombre", font=self.labelFont, width=300, height=30).place(x=120, y=10)
            CTkLabel(self.toplevel_window, text='Cédula', font=self.labelFont, width=100, height=30).place(x=10, y=90)
            inputCi = CTkEntry(self.toplevel_window, textvariable=ci,placeholder_text="Cédula", font=self.labelFont, width=300, height=30).place(x=120, y=90)
            CTkLabel(self.toplevel_window, text='Teléfono', font=self.labelFont, width=100, height=30).place(x=10, y=130)
            inputPhoneNum = CTkEntry(self.toplevel_window, textvariable=phoneNum, placeholder_text="04xx1111111", font=self.labelFont, width=300, height=30).place(x=120, y=130)
        
            btnSaveNew = CTkButton(self.toplevel_window, text="Guardar", fg_color='green', width=150, height=40, font=self.buttonFont, command=lambda:self.modify_data(customer, index, name, ci, phoneNum)).place(x=165, y=200)
            btnCancel = CTkButton(self.toplevel_window, text="Cancelar", fg_color='red', width=120, height=40, font=self.buttonFont, command=lambda:self.toplevel_window.destroy()).place(x=10, y=430) #Customer(len(self.data)+1, inputName.get(), inputLastName.get(), inputCi.get(),f'+58{inputPhoneExt}{inputPhoneNum}', 0, 'Nunca')

        else:
            self.toplevel_window.deiconify()  #if window exists focus it

    def send_by_date_window(self, customer):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = CTkToplevel(self)  # create window if its None or destroyed
            self.toplevel_window.attributes('-topmost', 'true')
            self.toplevel_window.geometry('480x480')

            day = StringVar(self.toplevel_window, 1)
            month = StringVar(self.toplevel_window, datetime.now().month)
            year = StringVar(self.toplevel_window, datetime.now().year)

            CTkLabel(self.toplevel_window, text='Día', font=self.labelFont, width=100, height=30).place(x=10, y=40)
            inputDay = CTkEntry(self.toplevel_window, textvariable=day,  placeholder_text="dd", font=self.labelFont, width=100, height=30).place(x=120, y=40)
            CTkLabel(self.toplevel_window, text='Mes', font=self.labelFont, width=100, height=30).place(x=10, y=80)
            inputMonth = CTkEntry(self.toplevel_window, textvariable=month,  placeholder_text="mm", font=self.labelFont, width=100, height=30).place(x=120, y=80)
            CTkLabel(self.toplevel_window, text='Año', font=self.labelFont, width=100, height=30).place(x=10, y=120)
            inputYear = CTkEntry(self.toplevel_window, textvariable=year,  placeholder_text="yyyy", font=self.labelFont, width=100, height=30).place(x=120, y=120)

            btnSendByDate = CTkButton(self.toplevel_window, text="Enviar", fg_color='blue', width=120, height=40, font=self.buttonFont, command=lambda:self.prepare_message(customer, day.get(), month.get(), year.get())).place(x=280, y=80)
            btnSendLastWeek = CTkButton(self.toplevel_window, text="Enviar\núltima semana", fg_color='blue', width=120, height=40, font=self.buttonFont, command=lambda:self.prepare_week_message(customer)).place(x=10, y=230)

            btnCancel = CTkButton(self.toplevel_window, text="Cancelar", fg_color='red', width=120, height=40, font=self.buttonFont, command=lambda:self.close_fiar_window()).place(x=10, y=430) #Customer(len(self.data)+1, inputName.get(), inputLastName.get(), inputCi.get(),f'+58{inputPhoneExt}{inputPhoneNum}', 0, 'Nunca')

        else:
            self.toplevel_window.deiconify()  #if window exists focus it