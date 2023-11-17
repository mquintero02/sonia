from interfaces.GUI import GUI
from clases.Customer import Customer
from clases.Product import Product

from random import randrange

def main():

    customerData=[
        Customer(0, "juan", "a", "123", "1234", "1234", 0, ""),
        Customer(1, "pedro", "a", "123", "1234", "1234", 0, ""),
        Customer(2, "julio", "a", "123", "1234", "1234", 10, ""),
        Customer(3, "carlos", "a", "123", "1234", "1234", 0, ""),
        Customer(4, "maria", "a", "123", "1234", "1234", 20, ""),
        Customer(4, "andrea", "a", "123", "1234", "1234", 0, ""),
        Customer(4, "leonardo", "b", "123", "1234", "1234", -40, ""),
        Customer(4, "mario", "a", "123", "1234", "1234", 1, ""),
        Customer(4, "luis", "a", "123", "1234", "1234", 2, ""),
        Customer(4, "carlos", "a", "123", "1234", "1234", 0, ""),
        Customer(4, "pedro", "cd", "123", "1234", "1234", 0, ""),
        Customer(4, "antonio", "a", "123", "1234", "1234", 0, ""),
        Customer(4, "alexandra", "z", "123", "1234", "1234", 0, ""),
        Customer(4, "abril", "a", "123", "1234", "1234", 0, ""),
    ]
    productData = [
        Product(1, "producto", 3, "tipo"),
        Product(1, "producto", 3, "tipo"),
        Product(1, "producto", 3, "tipo"),
        Product(1, "producto", 3, "tipo"),
        Product(1, "producto", 3, "tipo"),
        Product(1, "producto", 3, "tipo"),
        Product(1, "producto", 3, "tipo"),
        Product(1, "producto", 3, "tipo"),
        Product(1, "producto", 3, "tipo"),
        Product(1, "producto", 3, "tipo"),
        Product(1, "producto", 3, "tipo"),
    ]
    for i, j in enumerate(productData):
        j.id = i
        j.price = randrange(1, 10)

    historyData = []

    gui = GUI(customerData, productData, historyData)

main()