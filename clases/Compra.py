from datetime import datetime

class Compra:

    def __init__(self, items, date, dateStr, resultBalance):
        self.items = items
        self.date = date
        self.dateStr = dateStr
        self.sent = False
        self.resultBalance = resultBalance
        
    def toString(self):
        message = ''
        message += f"{self.dateStr}\n"
        for i in self.items:
            message += f'{i["quantity"]} {i["name"]}: {i["price"]}$\n'
        message += '\n'
        message += f"Saldo resultate: {self.resultBalance}\n\n"

        return message
    
    def add_items(self, auxList, newBalance):
        for i in auxList:
            self.items.append(i)
        
        self.resultBalance = newBalance
        self.sent = False
