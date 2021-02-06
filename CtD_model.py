import random
from math import sqrt

class Fugitive:
    def __init__(self,x:int,y:int): #,level:int
        self.x = x
        self.y = y
    
    def get_choices(self, board, cx, cy):
        # the 6 adjacent cases, excluding the condemned ones
        choices = [(cx,cy+1),   #above
                   (cx,cy-1),   #below
                   (cx+1,cy),
                   (cx-1,cy)]
        if cx%2 == 0:
            choices.append((cx+1,cy-1))
            choices.append((cx-1,cy-1))
        else:
            choices.append((cx+1,cy+1))
            choices.append((cx-1,cy+1))
        for c in choices.copy():
            if (c in board.l_cond):
                choices.remove(c)
        
        return choices
    
    def move(self, board):
        # random choice. The fugitive is blind.
        choices = self.get_choices(board, self.x,self.y)
        if len(choices) == 0:
            return("stuck 0")
        
        pos = random.choice(choices)
        if (pos[0]<0) or (pos[1]<0) or (pos[0]>=board.width) or (pos[1]>=board.height):
            return("free 0")
        self.x = pos[0]
        self.y = pos[1]
        return("escaping 0")
    
    def move_moy(self, board):
        # The fugitive makes a significant number of random guesses, 
        # saves the not to long ones and make the first step of the shortest.
        paths = []
        
        for p in range(board.height*board.width//10):
            state = "escaping"
            current_path = []
            cx = self.x
            cy = self.y
            while state == "escaping" and len(current_path) < 2*sqrt(board.height*board.width):
                choices = self.get_choices(board, cx,cy)
                for c in choices.copy():
                    if (c in current_path):
                        choices.remove(c)
                if len(choices) == 0:
                    state = "stuck"
                else :
                    pos = random.choice(choices)
                    if (pos[0]<0) or (pos[1]<0) or (pos[0]>=board.width) or (pos[1]>=board.height):
                        state = "free"
                    else :
                        state = "escaping"
                    cx = pos[0]
                    cy = pos[1]
                    cp = cx,cy
                    current_path.append(cp)
                    
            if state == "free":                
                paths.append(current_path)
                
        if not paths:
            return(self.move(board))
        else:
            paths.sort(key=len)
            best = paths[0]
            cx,cy = best[0]
            if (cx<0) or (cy<0) or (cx>=board.width) or (cy>=board.height):
                return("free 1")
            self.x,self.y = best[0]
            return("escaping 1")
                    
    def move_hard(self, board):
        # The fugitive considers all the possible path and make the first step to the shortest.
        if (self.x<1) or (self.y<1) or (self.x>=board.width-1) or (self.y>=board.height-1):
           return("free 2")
        paths = []
        cp = []
        t = self.x,self.y
        cp.append(t)
        paths.append(cp)
        state = "escaping"
        while state == "escaping":
            for p in paths.copy():
                ct = p[len(p)-1]
                cx,cy = ct
                choices = self.get_choices(board,cx,cy)
                for c in choices.copy():
                    if (c in p):
                        choices.remove(c)
                paths.remove(p)
                if choices:
                    for c in choices:
                        if (c[0]<0) or (c[1]<0) or (c[0]>=board.width) or (c[1]>=board.height):
                            state = "free"
                            self.x,self.y = p[1]
                            return("escaping 2")
                        else:
                            p.append(c)
                            paths.append(p.copy())
                            p.remove(c)
                elif paths == []:
                    return(self.move(board))
        return("escaping 2")                      
        
    
    def __repr__(self):
        return f"The fugitive is at (x={self.x:2d}; y={self.y:2d})"
    
    


class Board:
    def __init__(self, w, h, nb_cond, fw, fh):
        self.width = w
        self.height = h
        self.nb_cond = nb_cond
        self.l_cond = []
        self.fuy_width = fw
        self.fuy_height = fh
        
        # avoid being outside of the grid:
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
            
    def __repr__(self):
        return(f"Width {self.width}\nHeight {self.height}\nCondemned cells {self.l_cond}")
        
    def cond(self,x,y):
        pos = x,y
        if (pos not in self.l_cond) and (pos != (self.fugitive.x, self.fugitive.y)):
            self.l_cond.append(pos)
            return 1
        return 0

if __name__ == "__main__":
    myBoard = Board(10,5,6,3,3)
    print(myBoard)
    print(myBoard.fugitive)