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
        l = 512;
        self.setSceneRect(0,0,l,l)
        
    def refresh(self):
        # Scene
        self.clear()

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
        
        # This is for player input
    
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
