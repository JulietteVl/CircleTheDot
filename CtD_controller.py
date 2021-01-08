#import numpy as np
from PyQt5.QtCore import *
import CtD_model as CtD
import pickle
from math import floor
from numpy import sqrt
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
        self.mode = 'chaser'
        self.best_score = 0
        self.nbTurns = 0
        self.w = 11
        self.h = 12
        self.nb_cond = 6
        self.fw = 3
        self.fh = 3
        self.state = 'escaping' #
        self.level = 0
    
    def start(self):
        self.state = 'escaping'
        if self.nb_cond+1>self.w*self.h:
            print("invalid values") 
            return 0
        self.myBoard = CtD.Board(self.w, self.h, self.nb_cond, self.fw, self.fh)#floor(sqrt(self.w)), floor(sqrt(self.h)))
#        self.fugitive = CtD.Fugitive((random.randint(int(self.w/2-self.fw/2), 
#                                                     int(self.w/2+self.fw/2))),
#                                     (random.randint(int(self.h/2-self.fh/2),
#                                                     int(self.h/2+self.fh/2))))
        self.refresh_all('')
    
    def load_game(self,file):
        f = open(file,'rb')
        [self.mode, self.best_score, self.nbTurns, self.w, self.h, self.nb_cond, self.fw, self.fh, self.level, x, y, l_cond] = pickle.load(f)
        self.start()
        self.myBoard.fugitive.x = x
        self.myBoard.fugitive.y = y
        self.myBoard.l_cond = l_cond
        self.refresh_all("")
    
    def save_game(self, file):
        try:
            f = open(file[0],'wb')
            params = [self.mode, self.best_score, self.nbTurns, self.w, self.h, self.nb_cond, self.fw, self.fh,self.level, self.myBoard.fugitive.x, self.myBoard.fugitive.y,self.myBoard.l_cond]
            pickle.dump(params,f,pickle.HIGHEST_PROTOCOL)
        except:
            print('Game could not be saved')
    
    def choose_level(self, level: int):
        self.level = level
    
    def condemn(self,i,j):
        condemned = self.myBoard.cond(i,j)
        if condemned:
            self.next()
    
    def next(self):
        #self.refresh_all('')
        #wait(0.5)
        if self.level == 0:
            self.state = self.myBoard.fugitive.move(self.myBoard)
        elif self.level == 1:
            self.state = self.myBoard.fugitive.move_moy(self.myBoard)
        else: #self.level == 2
            self.state = self.myBoard.fugitive.move_hard(self.myBoard)
        self.refresh_all('')
        print(self.level,self.state)