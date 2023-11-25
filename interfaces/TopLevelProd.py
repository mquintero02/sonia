from tkinter import *

class TopLevelProd:

    def __init__(self, master, product):
        self.master = master
        self.product = product

        self.button = Button(master, text=product.name, command=lambda:self.init_widgets(), background='blue', width=250, height=2)

    def init_widgets(self):
        root = Toplevel(self.master)
        root.resizable(0, 0)
        root.geometry("480x720")

        Label(root, text=f'{self.product.name} {self.product.price}$', font=("Arial", 24)).place(x=10, y=10)
        Label(root, text=f'Tipo: {self.product.type}', font=("Arial", 24)).place(x=10, y=90)

        update = Button(root, text='Modificar', background='blue', padx=3, pady=3, font=('Arial', 18)).place(x=365, y=670)
        delete = Button(root, text='Eliminar', background='red', padx=3, pady=3, font=('Arial', 18)).place(x=0, y=670)
        root.mainloop()
        
        