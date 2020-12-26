import random

class Fugitive:
    def __init__(self,x:int,y:int):
        self.x = x
        self.y = y
    
    def move(self, board, level = 0):
        l_cond = board.l_cond
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
    
    def move_moy(self, board, level = 0 ):
        paths = []
        current_path = []
        
        for p in range(250):
            state = "escaping"
            current_path.clear()
            cx = self.x
            cy = self.y
            while state == "escaping" and len(current_path) < 20:
                l_cond = board.l_cond
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
                return("free")
            self.x,self.y = best[0]
                    
    def move_hard(self, board, level = 0):
        if (self.x<1) or (self.y<1) or (self.x>=board.width-1) or (self.y>=board.height-1):
           return("free")
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
                    elif (c in p):
                        choices.remove(c)
                if not choices:
                    return(self.move(board))
                else:
                    paths.remove(p)
                    for c in choices:
                        if (c[0]<0) or (c[1]<0) or (c[0]>=board.width) or (c[1]>=board.height):
                            state = "free"
                            self.x,self.y = p[1]
                        else:
                            p.append(c)
                            paths.append(p.copy())
                            p.remove(c)
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
