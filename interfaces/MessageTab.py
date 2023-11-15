from interfaces.Tab import Tab

class MessageTab(Tab):

    def __init__(self, master, title, data):
        super().__init__(master=master, title=title)
        self.data = data
    