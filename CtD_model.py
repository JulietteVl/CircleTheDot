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
            if (pos[0]<0) or (pos[1]<0) or (pos[0]>=board.width) or (pos[1]>=board.height):
                return("free")
            self.x = pos[0]
            self.y = pos[1]
            return("escaping")
    
    def __repr__(self):
        return f"The fugitive is at (x={self.x:2d} ; y={self.y:2d})"
    
    


class Board:
    def __init__(self, w, h, nb_cond, fw, fh):
        self.width = w
        self.height = h
        self.nb_cond = nb_cond
        self.l_cond = []
        self.fuy_width = fw
        self.fuy_height = fh
        
        
        self.fugitive = Fugitive((random.randint(max(int(self.width/2-self.fuy_width/2),0), 
                                                 min(int(self.width/2+self.fuy_width/2),self.width-1))),
                                 (random.randint(max(int(self.height/2-self.fuy_height/2),0),
                                                 min(int(self.height/2+self.fuy_height/2),self.height-1))))
        choices = []
        for i in range(self.width):
            for j in range(self.height):
                choices.append((i,j))
        choices.remove((self.fugitive.x,self.fugitive.y))
        for l in range(nb_cond):
            self.l_cond.append(random.choice(choices))
            choices.remove(self.l_cond[l])
        
    def cond(self,x,y):
        pos = x,y
        if (pos not in self.l_cond) and (pos != (self.fugitive.x, self.fugitive.y)):
            self.l_cond.append(pos)
            return 1
        return 0

class Game:
    def __init__(self):
        pass
    
    def saveGame(self):
        pass