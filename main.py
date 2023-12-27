from interfaces.Gui import Gui
from db import *

def main():

    data = read_customer()
    hData = read_history()
    
    gui = Gui(data, hData)
    gui.mainloop()

main()