from interfaces.GUI import GUI
from clases.Customer import Customer
from db import *
import os


def main():

    data=[
        Customer(0, "juan", "a", "123", "1234", "1234", 0, "", [{'date': '01/01/2023', 'p':[{'quantity':2, 'price':3, 'product':'pizza'}]}]),
        Customer(1, "pedro", "a", "123", "1234", "1234", 0, "", [{}]),
        Customer(2, "julio", "a", "123", "1234", "1234", 10, "", [{}]),
        Customer(3, "carlos", "a", "123", "1234", "1234", 0, "", [{}]),
        Customer(4, "maria", "a", "123", "1234", "1234", 20, "", [{}]),
    ]

    gui = GUI(data)

main()