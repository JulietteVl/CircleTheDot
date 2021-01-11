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
        # create an instance of board, which contains an instance of the fugitive
        self.state = 'escaping'
        if self.nb_cond+1>self.w*self.h:
            print("invalid values") 
            return 0
        self.myBoard = CtD.Board(self.w, self.h, self.nb_cond, self.fw, self.fh)
        self.refresh_all('')
    
    def load_game(self,file):
        # give to the controller all the characteristics to reconstitute a game
        f = open(file,'rb')
        try:
            [self.mode, self.best_score, self.nbTurns, self.w, self.h, self.nb_cond, self.level, x, y, l_cond] = pickle.load(f)
            self.start()
            self.myBoard.fugitive.x = x
            self.myBoard.fugitive.y = y
            self.myBoard.l_cond = l_cond
            self.refresh_all("")
        except:
            pass
        f.close()
    
    def save_game(self, file):
        # save in a file all the characteristics to reconstitute a game
        try:
            f = open(file[0],'wb')
            params = [self.mode, self.best_score, self.nbTurns, self.w, self.h, self.nb_cond,self.level, self.myBoard.fugitive.x, self.myBoard.fugitive.y,self.myBoard.l_cond]
            pickle.dump(params,f,pickle.HIGHEST_PROTOCOL)
            f.close()
        except:
            print('Game could not be saved')
        f = open('{}.txt'.format(file[0]),'w')
        param_names = ["mode", "best_score", "nb_turns", 'width', 'heigth', 'nb_condemned_cells', 'level', 'fugitive_x_position', 'fugitive_y_position']
        params = [self.mode, self.best_score, self.nbTurns, self.w, self.h, self.nb_cond, self.level, self.myBoard.fugitive.x, self.myBoard.fugitive.y]
        params = list(map(str, params))
        for i, param in enumerate(params):
            f.write('{}: {}\n'.format(param_names[i], param))
        f.writelines(list(map(str, self.myBoard.l_cond)))
        f.close()
    
    def choose_level(self, level: int):
        # process level chosen
        self.level = level
    
    def condemn(self,i,j):
        # mark a case (i,j) as condemned
        condemned = self.myBoard.cond(i,j)
        if condemned:
            self.next()
    
    def next(self):
        # Move the fugitive. The strategy depend on the level of the game.
        #wait(0.5)
        if self.level == 0:
            self.state = self.myBoard.fugitive.move(self.myBoard)
        elif self.level == 1:
            self.state = self.myBoard.fugitive.move_moy(self.myBoard)
        else: #self.level == 2
            self.state = self.myBoard.fugitive.move_hard(self.myBoard)
        self.refresh_all('')
        print(self.level,self.state)