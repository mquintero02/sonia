from datetime import datetime

class Compra:

    def __init__(self, items, date, dateStr, resultBalance):
        self.items = items
        self.date = date
        self.dateStr = dateStr
        self.sent = False
        self.resultBalance = resultBalance
        
    def toString(self):
        message = f"{self.dateStr}\n{self.items}\nTotal: {self.resultBalance}\n"
        return message
    
    def add_items(self, items, amount):
        self.resultBalance += amount
        self.items = f'{self.items}\n{items}'
