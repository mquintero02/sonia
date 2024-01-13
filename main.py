from interfaces.Gui import Gui
from db import *

def main():

    data = read_customer()
    hData = read_history()

    data.sort(key=lambda x: x.name.lower(), reverse=False)
    
    gui = Gui(data, hData)
    gui.mainloop()

main()