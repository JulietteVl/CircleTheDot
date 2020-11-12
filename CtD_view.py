# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 14:08:06 2020

@author: julie
"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from CtD_controller import *

class Scene(QGraphicsScene):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.controller.add_client(self)
        self.l = 512;
        self.setSceneRect(0,0,self.l,self.l)
        
    def refresh(self):
        ## Scene
        
        # Background
        self.clear()
        pen = QPen(Qt.black)
        brush = QBrush(Qt.gray)
        self.fond = self.addRect(0,0,self.l,self.l,pen,brush)
        
        # Cells
        board = self.controller.myBoard
        w = board.width
        h = board.height
        self.cellSpace = self.l//(max(w,h)+1)
        self.cellSize = self.cellSpace - 5
        self.border = (self.l-self.cellSpace*(max(w,h)))//2
        cells = []
        for j in range(h):
            for i in range(w):
                 cells.append(self.addRect(0,0,self.cellSize,self.cellSize,pen,QBrush(Qt.white)))
                 cells[j*w+i].setPos(self.border+i*self.cellSpace,self.border+(2*j+i%2)*(self.cellSpace//2))
        
        # Condemned cells
        l_cond = board.l_cond
        cond_cells = [] # I'd rather simply repaint the cells but I don't know how to.
        for l,pos in enumerate(l_cond):
            i = pos[0]
            j = pos[1]
            cond_cells.append(self.addRect(0,0,self.cellSize,self.cellSize,pen,QBrush(Qt.red)))
            cond_cells[l].setPos(cells[j*w+i].scenePos())
        
        # fugitive
        fugitive = board.fugitive
        i = fugitive.x
        j = fugitive.y
        space = 2
        fugitiveGraphic = self.addEllipse(space,space,self.cellSize-2*space,self.cellSize-2*space,pen,QBrush(Qt.blue))
        fugitiveGraphic.setPos(cells[j*w+i].pos())

class View(QGraphicsView):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.controller.add_client(self)
        self.scene = Scene(self, controller)
        self.setScene(self.scene)

    def resizeEvent(self, event):
        self.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
    
    def refresh(self):
        pass
    
class Params(QWidget):
    def __init__(self, parent, controller):
        super().__init__()
        self.controller = controller
        self.controller.add_client(self)
        
        # Widgets
        self.start_button = QPushButton('Start')
        
        # Slots
        self.start_button.clicked.connect(self.on_start)
        
        # Layout
        vLayout = QVBoxLayout()
        vLayout.addWidget(self.start_button)
        vLayout.addStretch()
        
        self.setLayout(vLayout)
    
    def on_start(self):
        self.controller.start()
    
    def refresh(self):
        pass
    
class Widget(QWidget):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.controller.add_client(self)
        view = View(self, controller)
        params = Params(self, controller)
        layout = QHBoxLayout()
        layout.addWidget(params)
        layout.addWidget(view)
        self.setLayout(layout)
    
    def refresh(self):
        pass
    
class Window(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.controller.add_client(self)
        self.setWindowTitle("Circle the dot")
        mainwidget = Widget(self, controller)
        self.setCentralWidget(mainwidget)

#    def keyPressEvent(self, e):
#        self.controller.process_keypress(e.key())

    def refresh(self):
        pass
    
def main():
    app = QApplication([])
    controller = CtDController()
    win = Window(controller)
    win.show()
    app.exec()

if __name__ == "__main__":
    main()