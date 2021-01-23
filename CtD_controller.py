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
            self.refresh_all("Invalid parameters.\n") 
            return 0
        self.myBoard = CtD.Board(self.w, self.h, self.nb_cond, self.fw, self.fh)
        self.refresh_all('Let the game begin.\n')
    
    def load_game(self,file):
        # give to the controller all the characteristics to reconstitute a game
        try:
            # This format is better than for an actual application
            self.start()
            
            f = open(file,'rb')
            [self.mode, self.best_score, self.nbTurns, self.w, self.h, self.nb_cond, 
             self.level, self.myBoard.fugitive.x, self.myBoard.fugitive.y, self.myBoard.l_cond] = pickle.load(f)
            
            self.refresh_all("Game loaded\n")
            f.close()
        except:
            try:
                # text format makes testing easier
                f = open(file,'r')
                params = [f.readline().split()[1]]
                for i in range(8):
                    params.append(int(f.readline().split()[1]))
                [self.mode, self.best_score, self.nbTurns, self.w, self.h, self.nb_cond, 
                 self.level, self.myBoard.fugitive.x, self.myBoard.fugitive.y] = params
                self.myBoard.l_cond = []
                for i in range(self.nb_cond):
                    cell = f.readline().split()
                    self.myBoard.l_cond.append((int(cell[0]),int(cell[1])))
        
                if self.myBoard.fugitive.x<self.w and self.myBoard.fugitive.y<self.h:
                    self.refresh_all("Game loaded.\n")
                else:
                    self.refresh_all("The file submitted is invalid. We advise you to delete it.")
                f.close()
            except:
                self.refresh_all('Game could not be loaded. New game has been loaded instead.\n')
    
    def save_game(self, file):
        # save in a file all the characteristics to reconstitute a game
        try:
            nb_cond = len(self.myBoard.l_cond)
            
            # This format is better than for an actual application
            f = open(file[0],'wb')
            params = [self.mode, self.best_score, self.nbTurns, self.w, self.h, nb_cond,
                      self.level, self.myBoard.fugitive.x, self.myBoard.fugitive.y, self.myBoard.l_cond]
            pickle.dump(params,f,pickle.HIGHEST_PROTOCOL)
            f.close()
            
            # text format makes testing easier
            f = open('{}.txt'.format(file[0]),'w')
            param_names = ["mode", "best_score", "nb_turns", 'width', 'heigth', 
                           'nb_condemned_cells', 'level', 'fugitive_x_position', 
                           'fugitive_y_position']
            params = [self.mode, self.best_score, self.nbTurns, self.w, self.h, 
                      nb_cond, self.level, self.myBoard.fugitive.x, self.myBoard.fugitive.y]
            
            for i, param in enumerate(params):
                f.write('{}: {}\n'.format(param_names[i], param))
            for l_cond in self.myBoard.l_cond:
                f.write('{} {}\n'.format(l_cond[0], l_cond[1]))
            f.close()
            self.refresh_all("The game has been saved")
        except:
            self.refresh_all('Game could not be saved\n')
            
        
    
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
        print("Fugitive level",self.level,self.state)