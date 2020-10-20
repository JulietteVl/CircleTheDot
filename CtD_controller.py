from PyQt5.QtCore import *
from CtD_model import *

class BaseController:
    def __init__(self):
        self.clients = list()
        self.message = ""

    def add_client(self, client):
        self.clients.append(client)

    def refresh_all(self, message):
        self.message = message
        for client in self.clients:
            client.refresh()

class CtDcontroller(BaseController):
    def __init__(self):
        super().__init__()
