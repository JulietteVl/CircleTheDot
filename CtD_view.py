# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 14:08:06 2020

@author: julie
"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from controller import *

class GameScene(QGraphicsScene):
        def __init__(self, parent, controler):
        super().__init__(parent)
        self.controler = controler
        self.controler.add_client(self)
        l = 512;
        self.setSceneRect(0,0,l,l)
