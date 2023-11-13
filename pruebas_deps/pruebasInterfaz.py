from tkinter import *

def pruebasInterfaz():

    root = Tk()
    root.title("Cantina Maria Auxiliadora")
    root.resizable(False, False)

    miFrame = Frame(root)
    miFrame.pack()
    miFrame.config(width=1080, height=720)

    navBar = Frame(miFrame)
    navBar.place(width=120, height=720, x=0, y=0)
    navBar.config(background="#0474e2")

    productsFrame = Frame(miFrame)
    productsFrame.place(width=960, height=720, x=120, y=0)
    productsFrame.config(background="#ffffff")

    pTittle = Label(productsFrame, text="Productos")
    pTittle.place(x=10, y=10)
    pTittle.config(font=('Arial', 40), background="#ffffff")

    btns = []
    canv = Canvas(productsFrame)
    canv.config(width=300, height=200)
    canv.place(x=0, y=400, width=900, height=320)             

    canv.config(scrollregion=(0,0,300, 1000))

    ybar = Scrollbar(productsFrame)
    ybar.config(command=canv.yview)                   
    ## connect the two widgets together
    canv.config(yscrollcommand=ybar.set)              
    ybar.place(x=900, y=400, width=20, height=250)   

# Add a Label widget to the child window
    h = 0
    for i in range(50):
        btn = Button(canv, text=f"{i}")
        btn.config(width=200, height=2)

        canv.create_window(30, 20+(40*i), window=btn)
        h += 40
    canv.config(scrollregion=(0,0,300, h))

    root.mainloop()

pruebasInterfaz()