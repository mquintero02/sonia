from datetime import datetime

class Compra:

    def __init__(self, items, date, resultBalance):
        self.items = items
        self.date = date
        self.dateStr = f'{date.strftime("%A")} {date.day}/{date.month}/{date.year}'
        self.sent = False
        self.resultBalance = resultBalance
        
    def toString(self):
        message = ''
        for i in self.items:
            message += f'({i["quantity"]}) {i["name"]}: {i["price"]}$\n'
        message += '\n'

        return message
