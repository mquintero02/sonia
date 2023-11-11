from tkinter import *

def main():

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
    productsFrame.config(background="#9dd3ff")

    pTittle = Label(productsFrame, text="Productos")
    pTittle.place(x=0, y=0)
    pTittle.config(background="#9dd3ff", font=('Arial', 40))


    root.mainloop()

main()