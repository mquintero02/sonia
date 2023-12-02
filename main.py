from interfaces.Gui import Gui
from db import *

def main():

    data = read_customer()
    hData = read_history()
    for i in data:
        print(str(i.id) + ' ' +i.name +' '+ i.lastName+ ' ' + i.ci + ' ' + i.phone)

    gui = Gui(data, hData)
    gui.mainloop()

main()