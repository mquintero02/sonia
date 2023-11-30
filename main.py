from interfaces.Gui import Gui
from db import *

def main():

    data = read_customer()
    for i in data:
        print(i.name +' '+ i.lastName+ ' ' + i.ci + ' ' + i.phone)

    gui = Gui(data)
    gui.mainloop()

main()