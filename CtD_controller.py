from PyQt5.QtCore import *
import CtD_model as CtD

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

class CtDController(BaseController):
    def __init__(self):
        super().__init__()
        self.w = 11
        self.h = 12
        self.nb_cond = 6
        self.fw = 3
        self.fh = 3
    
    def start(self):
        self.myBoard = CtD.Board(self.w, self.h, self.nb_cond, self.fw, self.fh)
        self.refresh_all('')