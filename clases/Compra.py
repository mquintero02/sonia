from datetime import datetime

class Compra:

    def __init__(self, items, date):
        self.items = items
        self.date = date
        self.dateStr = f'{date.day}/{date.month}/{date.year}'
        self.sent = False
        
    def toString(self):
        message = f'{self.dateStr}\n'
        for i in self.items:
            message += f'({i["quantity"]}) {i["name"]}: {i["price"]}$\n'
        message += '\n'

        return message
