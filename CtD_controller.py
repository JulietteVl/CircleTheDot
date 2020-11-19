from PyQt5.QtCore import *
import CtD_model as CtD
#import random

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
        self.state = 0 #
    
    def start(self):
        if self.nb_cond+1>self.w*self.h:
            print("invalid values") 
            return 0
        self.myBoard = CtD.Board(self.w, self.h, self.nb_cond, self.fw, self.fh)
#        self.fugitive = CtD.Fugitive((random.randint(int(self.w/2-self.fw/2), 
#                                                     int(self.w/2+self.fw/2))),
#                                     (random.randint(int(self.h/2-self.fh/2),
#                                                     int(self.h/2+self.fh/2))))
        self.refresh_all('')
    
    def condemn(self,i,j):
        condemned = self.myBoard.cond(i,j)
        if condemned:
            self.next()
    
    def next(self):
        #self.refresh_all('')
        #wait(0.5)
        state = self.myBoard.fugitive.move(self.myBoard)
        self.refresh_all('')
        print(state)
        