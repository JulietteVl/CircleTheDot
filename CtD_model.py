import random

class Fuyard:
    def __init__(self,x:int,y:int):
        self.x = x
        self.y = y
    
    def move(self,w,h,l_cond):
        pass
    
    def __repr__(self):
        return f"Le fuyard est en (x={self.x:2d} ; y={self.y:2d})"
    
    


class Board:
    def __init__(self,w=10,h=10,nb_cond=6,fw=3,fh=3):
        self.width = w
        self.height = h
        self.l_cond = []
        self.nb_cond = nb_cond
        self.fuy_width = fw
        self.fuy_height = fh
        self.fuyard = Fuyard((random.randint(int(self.width/2-self.fuy_width/2), 
                                             int(self.width/2+self.fuy_width/2))),
                             (random.randint(int(self.height/2-self.fuy_height/2),
                                             int(self.height/2+self.fuy_height/2))))
        
        
    def cond(self,x,y):
        pos = x,y
        if pos not in self.l_cond:
            self.l_cond.append(pos)

class Game:
    def __init__(self):
        pass
    
    def saveGame(self):
        pass