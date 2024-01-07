from customtkinter import *
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
        self.custFrameTittle = StringVar(self.customerFrame, '')

        self.open_menu()

    def open_customer(self, customer):
        self.menuFrame.destroy()
        if self.customerFrame is None or not self.customerFrame.winfo_exists():
            self.hData = read_history()
            customerHData = self.hData[str(customer.id)]
            self.customerFrame = CTkFrame(self, width=720, height=720)
            self.customerFrame.pack()

            if customer.balance < -1:
                CTkLabel(self.customerFrame, text=f'Saldo: {customer.balance}$', fg_color='red', font=self.titleFont, width=370, height=40, corner_radius=5).place(x=310, y=20)
            elif customer.balance >1:
                CTkLabel(self.customerFrame, text=f'Saldo: {customer.balance}$', fg_color='green', font=self.titleFont, width=370, height=40, corner_radius=5).place(x=310, y=20)
            else:
                CTkLabel(self.customerFrame, text=f'Saldo: {customer.balance}$', fg_color='blue', font=self.titleFont, width=370, height=40, corner_radius=5).place(x=310, y=20)

            sf = CTkScrollableFrame(self.customerFrame, width=370, height=600, fg_color='yellow')
            sf.place(x=310, y=70)

            auxHData = list(reversed(customerHData))
            lColor = ''
            for c in auxHData:
                CTkLabel(sf, text=c.dateStr, font=self.labelFont, text_color='black').pack()
                if c.sent:
                    CTkLabel(sf, text="enviado", fg_color="#00FFFF", width=370, font=self.labelFont, text_color='black').pack()
                if c.resultBalance < -1:
                    lColor = '#ff735a'
                elif c.resultBalance > 1:
                    lColor = '#a9e159'
                else:
                    lColor = 'blue'
                for i in c.items:
                    CTkLabel(sf, text=f'{i["quantity"]} {i["name"]}: {i["price"]}$', text_color='black', anchor="w", width=370, font=self.labelFont).pack()

                CTkLabel(sf, fg_color=lColor, text=f"saldo: {c.resultBalance}$", font=self.labelFont, text_color='black',width=370, anchor=E).pack()
                CTkLabel(sf, text='------------------------------------------------------', font=self.labelFont, text_color='black').pack()

            btnBack = CTkButton(self.customerFrame, text="Regresar", width=100, height=40, font=self.buttonFont, command=self.open_menu).place(x=10, y=10)
            btnFiar = CTkButton(self.customerFrame, text="Fiar", width=100, height=40, font=self.buttonFont, command=lambda:self.fiar_window(customer), fg_color='orange', text_color='black').place(x=100, y=200)
            btnAbonar = CTkButton(self.customerFrame, text='Abonar', width=100, height=40, font=self.buttonFont, fg_color='green', command=lambda:self.abonar_window(customer)).place(x=100, y=260)
            btnMessage = CTkButton(self.customerFrame, text='Enviar\nPendientes', width=100, height=40, font=self.buttonFont, command=lambda:self.check_conection(customer)).place(x=100, y=360)
            btnDateMessage = CTkButton(self.customerFrame, text='Enviar\npor fecha', width=100, height=40, font=self.buttonFont, command=lambda:self.send_by_date_window(customer)).place(x=100, y=440)
            btnDetele = CTkButton(self.customerFrame, text='Eliminar', width=100, height=40, font=self.buttonFont, fg_color='red', command=lambda:self.delete_customer(customer)).place(x=10, y=670)
            btnModify = CTkButton(self.customerFrame, text='modificar', width=100, height=40, font=self.buttonFont, fg_color='blue', command=lambda:self.modify_window(customer)).place(x=180, y=10)
            
            self.custFrameTittle.set(f'{customer.name} {customer.lastName}\nCI: {customer.ci}\nTeléfono: {customer.phone}')
            self.customerFrameTitle = CTkLabel(self.customerFrame, text=self.custFrameTittle.get(), font=self.titleFont2, width=200).place(x=10, y=70)

    def delete_customer(self, customer):
        option = CTkMessagebox(message=f"¿Seguro que quieres eliminar a {customer.name} {customer.lastName}?",option_2="No", option_1="Si", font=self.labelFont)
        response = option.get()

        if response == "Si":
            self.data.remove(customer)
            self.hData.pop(str(customer.id))
            save_customer(self.data)
            save_history(self.hData)
            self.open_menu()

    def open_menu(self):
        if not self.customerFrame is None:
            self.customerFrame.destroy()
        if self.menuFrame is None or not self.menuFrame.winfo_exists():
            self.menuFrame = CTkFrame(self, width=720, height=720)
            self.menuFrame.pack()

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

    def filter(self, name, lastName, ci, sf):
        for c in sf.winfo_children():
            c.destroy()

        for c in self.data:
            if f"{name}".lower() in c.name.lower() and f"{lastName}".lower() in c.lastName.lower() and f"{ci}".lower() in c.ci.lower():
                CButton(c, sf, self).set_button()

    def refresh_menu(self):
        self.menuFrame.destroy()
        self.open_menu()

    def refresh_customer_window(self, customer):
        self.customerFrame.destroy()
        self.open_customer(customer)

    def add_data(self, name, lastName, ci, phoneExt, phoneNum):
        if name.get() != '' and lastName.get() != '' and ci.get().isnumeric() and len(phoneExt.get())==4 and phoneExt.get().isnumeric() and phoneNum.get().isnumeric():
                        
            newId = int(read_last_index()) + 1
            newCust = Customer(newId, name.get(), lastName.get(), ci.get(), f'+58{phoneExt.get()[1:]}{phoneNum.get()}', 0, 'Nunca')
            self.data.append(newCust)
            save_customer(self.data)
            save_last_index(newId)
            self.hData[str(newId)] = []
            save_history(self.hData)
            self.refresh_menu()
            self.toplevel_window.destroy()
        else:
            CTkMessagebox(message="Datos no válidos")

    def update_data(self, index, updatedCustomer):
        self.data[index] = updatedCustomer
        save_customer(self.data)

    def add_to_aux_list(self, product, quantity, price, sf):
        if product.get() != "" and quantity.get() != "" and quantity.get().isnumeric and price.get() != "" and price.get().isnumeric:
            self.auxList.append({'name': product.get(), 'quantity':quantity.get(), 'price':-float(price.get())*float(quantity.get())})
            CTkLabel(sf, text=f'{quantity.get()} {product.get()}: {-float(price.get())*float(quantity.get())}$', text_color='black', font=self.labelFont, anchor='w', width=440).pack()
            product.set('')
            quantity.set('')
            price.set('')
        else:
            CTkMessagebox(message="Datos no válidos")

    def add_to_aux_list_deposito(self, amount, sf):
        self.auxList.append({'name': 'Depósito', 'quantity':'1', 'price':amount.get()})
        CTkLabel(sf, text=f'{1} "Depósito": {amount.get()}$', text_color='black', font=self.labelFont, anchor='w', width=440).pack()
        amount.set('')

    def reset_aux_list(self):
        self.auxList.clear()

    def close_fiar_window(self):
        self.reset_aux_list()
        self.toplevel_window.destroy()

    def save_fiar(self, customer):
        amount = 0
        for i in self.auxList:
            amount += float(i['price'])

        index = self.data.index(customer)
        customer.balance += amount

        dateToCompare = datetime.now()
        dateDay = dateToCompare.weekday()

        if len(self.hData[str(customer.id)]) == 0:
            self.hData[str(customer.id)].append(
                Compra(self.auxList, dateToCompare, f'{self.weekDays[dateDay]} {dateToCompare.day}/{dateToCompare.month}/{dateToCompare.year}', customer.balance)
            )
        elif self.hData[str(customer.id)][-1].dateStr == f'{self.weekDays[dateDay]} {dateToCompare.day}/{dateToCompare.month}/{dateToCompare.year}':
            self.hData[str(customer.id)][-1].add_items(self.auxList, customer.balance)
        else:
            self.hData[str(customer.id)].append(
                Compra(self.auxList, dateToCompare, f'{self.weekDays[dateDay]} {dateToCompare.day}/{dateToCompare.month}/{dateToCompare.year}', customer.balance)
            )
        save_history(self.hData)
        self.update_data(index, customer)
        self.refresh_customer_window(customer)
        self.close_fiar_window()

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
            inputName = CTkEntry(self.toplevel_window, textvariable=name,  placeholder_text="Nombre", font=self.labelFont, width=300, height=30).place(x=120, y=10)
            CTkLabel(self.toplevel_window, text='Apellido', font=self.labelFont, width=100, height=30).place(x=10, y=50)
            inputLastName = CTkEntry(self.toplevel_window, textvariable=lastName, placeholder_text="Apellido", font=self.labelFont, width=300, height=30).place(x=120, y=50)
            CTkLabel(self.toplevel_window, text='Cédula', font=self.labelFont, width=100, height=30).place(x=10, y=90)
            inputCi = CTkEntry(self.toplevel_window, textvariable=ci,placeholder_text="Cédula", font=self.labelFont, width=300, height=30).place(x=120, y=90)
            CTkLabel(self.toplevel_window, text='Teléfono', font=self.labelFont, width=100, height=30).place(x=10, y=130)
            inputPhoneExt = CTkEntry(self.toplevel_window, textvariable=phoneExt, placeholder_text="04xx", font=self.labelFont, width=70, height=30).place(x=120, y=130)
            inputPhoneNum = CTkEntry(self.toplevel_window, textvariable=phoneNum, placeholder_text="1110000", font=self.labelFont, width=220, height=30).place(x=200, y=130)
        
            btnSaveNew = CTkButton(self.toplevel_window, text="Guardar", fg_color='green', width=150, height=40, font=self.buttonFont, command=lambda:self.add_data(name, lastName, ci, phoneExt, phoneNum)).place(x=165, y=200)
            btnCancel = CTkButton(self.toplevel_window, text="Cancelar", fg_color='red', width=120, height=40, font=self.buttonFont, command=lambda:self.toplevel_window.destroy()).place(x=10, y=430) #Customer(len(self.data)+1, inputName.get(), inputLastName.get(), inputCi.get(),f'+58{inputPhoneExt}{inputPhoneNum}', 0, 'Nunca')

        else:
            self.toplevel_window.deiconify()  #if window exists focus it
    
    def modify_window(self, customer):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = CTkToplevel(self)  # create window if its None or destroyed
            self.toplevel_window.attributes('-topmost', 'true')
            self.toplevel_window.geometry('480x480')

            index = self.data.index(customer)

            name = StringVar(self.toplevel_window, customer.name)
            lastName = StringVar(self.toplevel_window, customer.lastName)
            ci = StringVar(self.toplevel_window, customer.ci)
            phoneExt =StringVar(self.toplevel_window, f'0{customer.phone[3:6]}')
            phoneNum = StringVar(self.toplevel_window, f'{customer.phone[6:]}')

            CTkLabel(self.toplevel_window, text='Nombre', font=self.labelFont, width=100, height=30).place(x=10, y=10)
            inputName = CTkEntry(self.toplevel_window, textvariable=name,  placeholder_text="Nombre", font=self.labelFont, width=300, height=30).place(x=120, y=10)
            CTkLabel(self.toplevel_window, text='Apellido', font=self.labelFont, width=100, height=30).place(x=10, y=50)
            inputLastName = CTkEntry(self.toplevel_window, textvariable=lastName, placeholder_text="Apellido", font=self.labelFont, width=300, height=30).place(x=120, y=50)
            CTkLabel(self.toplevel_window, text='Cédula', font=self.labelFont, width=100, height=30).place(x=10, y=90)
            inputCi = CTkEntry(self.toplevel_window, textvariable=ci,placeholder_text="Cédula", font=self.labelFont, width=300, height=30).place(x=120, y=90)
            CTkLabel(self.toplevel_window, text='Teléfono', font=self.labelFont, width=100, height=30).place(x=10, y=130)
            inputPhoneExt = CTkEntry(self.toplevel_window, textvariable=phoneExt, placeholder_text="04xx", font=self.labelFont, width=70, height=30).place(x=120, y=130)
            inputPhoneNum = CTkEntry(self.toplevel_window, textvariable=phoneNum, placeholder_text="1110000", font=self.labelFont, width=220, height=30).place(x=200, y=130)
        
            btnSaveNew = CTkButton(self.toplevel_window, text="Guardar", fg_color='green', width=150, height=40, font=self.buttonFont, command=lambda:self.modify_data(customer, index, name, lastName, ci, phoneExt, phoneNum)).place(x=165, y=200)
            btnCancel = CTkButton(self.toplevel_window, text="Cancelar", fg_color='red', width=120, height=40, font=self.buttonFont, command=lambda:self.toplevel_window.destroy()).place(x=10, y=430) #Customer(len(self.data)+1, inputName.get(), inputLastName.get(), inputCi.get(),f'+58{inputPhoneExt}{inputPhoneNum}', 0, 'Nunca')

        else:
            self.toplevel_window.deiconify()  #if window exists focus it

    def modify_data(self, customer, index, name, lastName, ci, phoneExt, phoneNum):
        if name.get() != '' and lastName.get() != '' and ci.get().isnumeric() and len(phoneExt.get())==4 and phoneExt.get().isnumeric() and phoneNum.get().isnumeric():
            customer.name = name.get()
            customer.lastName = lastName.get()
            customer.ci = ci.get()
            customer.phone = f'+58{phoneExt.get()[1:]}{phoneNum.get()}'
            self.update_data(index, customer)
            self.refresh_customer_window(customer)
            self.toplevel_window.destroy()
        else:
            CTkMessagebox(message="Datos no válidos")

    def fiar_window(self, customer):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = CTkToplevel(self)  # create window if its None or destroyed
            self.toplevel_window.attributes('-topmost', 'true')
            self.toplevel_window.geometry('480x480')

            name = StringVar(self.toplevel_window, '')
            quantity = StringVar(self.toplevel_window, '')
            price = StringVar(self.toplevel_window, '')

            CTkLabel(self.toplevel_window, text='Producto', font=self.labelFont, width=100, height=30).place(x=10, y=10)
            inputName = CTkEntry(self.toplevel_window, textvariable=name,  placeholder_text="Producto", font=self.labelFont, width=300, height=30).place(x=120, y=10)
            CTkLabel(self.toplevel_window, text='Precio c/u', font=self.labelFont, width=100, height=30).place(x=10, y=50)
            inputPrice = CTkEntry(self.toplevel_window, textvariable=price,placeholder_text="Precio", font=self.labelFont, width=100, height=30).place(x=120, y=50)
            CTkLabel(self.toplevel_window, text='Cantidad', font=self.labelFont, width=100, height=30).place(x=220, y=50)
            inputQuantity = CTkEntry(self.toplevel_window, textvariable=quantity, placeholder_text="Cantidad", font=self.labelFont, width=100, height=30).place(x=320, y=50)

            sf = CTkScrollableFrame(self.toplevel_window, width=440, height=200, fg_color='yellow')
            sf.place(x=10, y=170)

            btnadd = CTkButton(self.toplevel_window, text="Añadir", fg_color='green', width=150, height=40, font=self.buttonFont, command=lambda:self.add_to_aux_list(name, quantity, price, sf)).place(x=165, y=110)
            btnSaveNew = CTkButton(self.toplevel_window, text="Guardar", fg_color='green', width=150, height=40, font=self.buttonFont, command=lambda:self.save_fiar(customer)).place(x=320, y=430)
            btnCancel = CTkButton(self.toplevel_window, text="Cancelar", fg_color='red', width=120, height=40, font=self.buttonFont, command=lambda:self.close_fiar_window()).place(x=10, y=430) #Customer(len(self.data)+1, inputName.get(), inputLastName.get(), inputCi.get(),f'+58{inputPhoneExt}{inputPhoneNum}', 0, 'Nunca')

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

        try:
            request = requests.get("https://google.com", timeout=5)
        except (requests.ConnectionError, requests.Timeout):
            CTkMessagebox(message="Sin conexión a internet")
            return
        else:
            print("Con conexión a internet.")

        history = list(reversed(self.hData[str(customer.id)]))

        for i, c in enumerate(history):
            if c.date >= date:
                c.sent = False
            else:
                break
        
        self.hData[str(customer.id)] = list(reversed(history))
        save_history(self.hData)

        self.send_message(customer)
        self.close_fiar_window()

    def prepare_week_message(self, customer):
        date = datetime.now()
        deltaTime = timedelta(weeks=1)
        auxDate = date - deltaTime

        try:
            request = requests.get("https://google.com", timeout=5)
        except (requests.ConnectionError, requests.Timeout):
            CTkMessagebox(message="Sin conexión a internet")
            return
        else:
            print("Con conexión a internet.")

        history = list(reversed(self.hData[str(customer.id)]))

        for i, c in enumerate(history):
            if c.date >= auxDate:
                c.sent = False
            else:
                break
        
        self.hData[str(customer.id)] = list(reversed(history))
        save_history(self.hData)

        self.send_message(customer)
        self.close_fiar_window()

    def abonar_window(self, customer):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = CTkToplevel(self)  # create window if its None or destroyed
            self.toplevel_window.attributes('-topmost', 'true')
            self.toplevel_window.geometry('480x480')

            amount = StringVar(self.toplevel_window, '')

            CTkLabel(self.toplevel_window, text='Depósito($)', font=self.labelFont, width=100, height=30).place(x=10, y=40)
            inputAmount = CTkEntry(self.toplevel_window, textvariable=amount,  placeholder_text="Depósito($)", font=self.labelFont, width=300, height=30).place(x=120, y=40)
            
            sf = CTkScrollableFrame(self.toplevel_window, width=440, height=200, fg_color='yellow')
            sf.place(x=10, y=170)

            btnadd = CTkButton(self.toplevel_window, text="Añadir", fg_color='green', width=150, height=40, font=self.buttonFont, command=lambda:self.add_to_aux_list_deposito(amount, sf)).place(x=165, y=110)
            btnSaveNew = CTkButton(self.toplevel_window, text="Guardar", fg_color='green', width=150, height=40, font=self.buttonFont, command=lambda:self.save_fiar(customer)).place(x=320, y=430)
            btnCancel = CTkButton(self.toplevel_window, text="Cancelar", fg_color='red', width=120, height=40, font=self.buttonFont, command=lambda:self.close_fiar_window()).place(x=10, y=430) #Customer(len(self.data)+1, inputName.get(), inputLastName.get(), inputCi.get(),f'+58{inputPhoneExt}{inputPhoneNum}', 0, 'Nunca')

        else:
            self.toplevel_window.deiconify()  #if window exists focus it

    def send_message(self, customer):

        message = "comienzo de mensaje de prueba\n\n"
        message2 = ""
        history = list(reversed(self.hData[str(customer.id)]))

        for i, c in enumerate(history):
            if c.sent:
                break
            else:
                message2 = c.toString() + message2
                c.sent = True
        
        self.hData[str(customer.id)] = list(reversed(history))
        save_history(self.hData)

        date = datetime.now()
        dateDay = date.weekday()
        customer.lastMessageDateStr = f'{self.weekDays[dateDay]} {date.day}/{date.month}/{date.year}'
        self.update_data(self.data.index(customer), customer)
        self.refresh_customer_window(customer)
        
        message = message + message2    

        pyperclip.copy(message)
