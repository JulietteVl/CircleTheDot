import random

class Fugitive:
    def __init__(self,x:int,y:int):
        self.x = x
        self.y = y
    
    def move(self, board, level = 0):
        l_cond = board.l_cond
        if level ==0:
            choices = [(self.x,self.y+1),  #above
                       (self.x,self.y-1),   #below
                       (self.x+1,self.y),
                       (self.x-1,self.y)]
            if self.x%2 == 0:
                choices.append((self.x+1,self.y-1))
                choices.append((self.x-1,self.y-1))
            else:
                choices.append((self.x+1,self.y+1))
                choices.append((self.x-1,self.y+1))
            for c in choices.copy():
                if (c in board.l_cond):
                    choices.remove(c)
            if len(choices) == 0:
                return("stuck")
            pos = random.choice(choices)
            self.x = pos[0]
            self.y = pos[1]
            return("free")
    
    def __repr__(self):
        return f"The fugitive is at (x={self.x:2d} ; y={self.y:2d})"
    
    


class Board:
    def __init__(self,w=11,h=12,nb_cond=6,fw=3,fh=3):
        self.width = w
        self.height = h
        self.nb_cond = nb_cond
        self.l_cond = []
        self.fuy_width = fw
        self.fuy_height = fh
        self.fugitive = Fugitive((random.randint(int(self.width/2-self.fuy_width/2), 
                                             int(self.width/2+self.fuy_width/2))),
                             (random.randint(int(self.height/2-self.fuy_height/2),
                                             int(self.height/2+self.fuy_height/2))))
        while len(self.l_cond) != nb_cond:
            for i in range(nb_cond-len(self.l_cond)):
                pos = (random.randint(0,w-1),random.randint(0,h-1))
                if pos != (self.fugitive.x,self.fugitive.y):         # check that the fugitive is not on a condemned case.
                    self.l_cond.append((random.randint(0,w-1),random.randint(0,h-1)))
                    # condemn a case. one can use a tuple as a condemned case is not mutable. 
                    # It also enables me to use set, which can be used only on hashable elements.
            self.l_cond = list(set(self.l_cond))                # remove duplicates
        
    def cond(self,x,y):
        pos = x,y
        if pos not in self.l_cond:
            self.l_cond.append(pos)
            return 1
        return 0

class Game:
    def __init__(self):
        pass
    
    def saveGame(self):
        pass