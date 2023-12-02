from datetime import datetime

class Compra:

    def __init__(self, items, date):
        self.items = items
        self.date = date
        self.dateStr = f'{date.day}/{date.month}/{date.year}'
        self.sent = False
        