from clases.Compra import Compra

class Customer:

    def __init__(self, id, name, ci, phone, balance):
        self.id = id
        self.name = name
        self.ci = ci
        self.phone = phone
        self.balance = balance

        self.history = {}

    def add_history(self, date, dateStr, items, amount):
        self.balance += amount

        if dateStr in self.history:
            self.history[dateStr].add_items(items, amount)
        else:
            self.history[dateStr] = Compra(items, date, dateStr, amount)