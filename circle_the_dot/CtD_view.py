"""
The view manages the user interface.

Classes:
    Scene
    View
    Message box
    Params
    Widget
    Window

Function:
    main

License:
    MIT License
    
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
    THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
    DEALINGS IN THE SOFTWARE.
"""

import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from CtD_controller import *


class Scene(QGraphicsScene):
    """Represent the board and the fugitive."""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.controller.add_client(self)
        self.parent = parent
        self.l = 512
        self.setSceneRect(0, 0, self.l, self.l)

        # See if packages can be imported to adapt behavior:
        try:
            from tinydb import TinyDB, Query
            self.tinyInitialized = 1
        except Exception:
            self.tinyInitialized = 0

    def refresh(self):
        """Update the scene."""
        # Scene
        if self.controller.valid:
            # Background
            self.clear()
            pen = QPen(Qt.black)
            brush = QBrush(Qt.gray)
            self.fond = self.addRect(0, 0, self.l, self.l, pen, brush)

            # Cells
            w = self.controller.myBoard.width
            h = self.controller.myBoard.height
            self.cellSpace = self.l // (max(w, h) + 1)
            self.cellSize = self.cellSpace - 5
            self.border = (self.l - self.cellSpace * (max(w, h))) // 2
            cells = []
            for j in range(h):
                for i in range(w):
                    cells.append(
                        self.addRect(0, 0, self.cellSize, self.cellSize, pen,
                                     QBrush(Qt.white)))
                    cells[j * w + i].setPos(
                        self.border + i * self.cellSpace,
                        self.border + (2 * j + i % 2) * (self.cellSpace // 2)
                        )

            # Condemned cells
            l_cond = self.controller.myBoard.l_cond
            cond_cells = []
            for k, pos in enumerate(l_cond):
                i = pos[0]
                j = pos[1]
                cond_cells.append(
                    self.addRect(0, 0, self.cellSize, self.cellSize,
                                 pen, QBrush(Qt.red))
                    )
                cond_cells[k].setPos(cells[j * w + i].scenePos())

            # fugitive
            fugitive = self.controller.myBoard.fugitive
            i = fugitive.x
            j = fugitive.y
            space = 2
            if i < w and j < h:
                fugitiveGraphic = self.addEllipse(
                    space, space, self.cellSize - 2 * space,
                    self.cellSize - 2 * space, pen, QBrush(Qt.blue))
                fugitiveGraphic.setPos(cells[j * w + i].pos())

            temp = self.controller.state.split()

            # Win
            if temp[0] == 'stuck':
                if not self.tinyInitialized:
                    best = False
                elif self.controller.best_score is None:
                    best = True
                else:
                    best = self.controller.nbTurns < self.controller.best_score
                self.game_win(best)

            # Loose
            elif temp[0] == 'free':
                self.game_over()

        else:
            pass

    def mousePressEvent(self, e):
        """Send user click information to the controller."""
        w = self.controller.w
        h = self.controller.h
        x = e.scenePos().x()
        y = e.scenePos().y()
        try:
            i = int((x - self.border) / self.cellSpace)
            j = int((y - self.border / 2) / self.cellSpace - (i) % 2 / 2)     # Hexagonal
            if i >= 0 and i < w and j >= 0 and j < h:
                self.controller.condemn(i, j)
        except Exception:
            pass

    def game_win(self, best):
        """Display appropriate information when the player wins."""
        self.clear()
        pen = QPen(Qt.black)
        brush = QBrush(Qt.gray)
        self.fond = self.addRect(0, 0, self.l, self.l, pen, brush)
        font = QFont('Arial', 24, QFont.Bold)
        if best:
            self.gbTxt = self.addText('BEST SCORE !', font)
            self.gbTxt.setDefaultTextColor(Qt.black)
            self.gbTxt.setPos(6 * self.l / 20, 9 * self.l / 20)
            self.controller.save_score()
        else:
            self.gwTxt = self.addText('YOU WON !', font)
            self.gwTxt.setDefaultTextColor(Qt.black)
            self.gwTxt.setPos(7 * self.l / 20, 9 * self.l / 20)

    def game_over(self):
        """Display appropriate message when player looses."""
        self.clear()
        pen = QPen(Qt.black)
        brush = QBrush(Qt.gray)
        self.fond = self.addRect(0, 0, self.l, self.l, pen, brush)
        font = QFont('Arial', 24, QFont.Bold)
        self.goTxt = self.addText('GAME OVER !', font)
        self.goTxt.setDefaultTextColor(Qt.black)
        self.goTxt.setPos(6 * self.l / 20, 9 * self.l / 20)


class View(QGraphicsView):
    """Control the window size."""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.controller.add_client(self)
        self.scene = Scene(self, controller)
        self.setScene(self.scene)

    def resizeEvent(self, event):
        """Resize the window."""
        self.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

    def refresh(self):
        """Update the object."""
        pass


class message_box(QTextEdit):
    """Writable box."""

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.controller.add_client(self)
        self.setReadOnly(True)

    def refresh(self):
        """Update the object."""
        message = self.controller.message
        if message:
            self.append(message)


class Params(QWidget):
    """Manages the layout of the parameters (everything but the board)."""

    def __init__(self, parent, controller):
        super().__init__()
        self.controller = controller
        self.controller.add_client(self)

        # Widgets
        self.start_button = QPushButton('New game')
        self.gridWidth_box = QSpinBox()
        self.gridHeight_box = QSpinBox()
        self.gridInit_boxes = QSpinBox()
        self.level_box = QComboBox()
        self.searchPath_button = QPushButton("Browse")
        self.save_button = QPushButton("Save game")
        self.b_score_lay = QLabel(f'Best score : {self.controller.best_score}')
        self.score_lay = QLabel('Moves : ' + str(self.controller.nbTurns))
        self.log_box = message_box(self.controller)     # Message box

        # Default value
        self.gridWidth_box.setValue(11)
        self.gridWidth_box.setMinimum(3)
        self.gridHeight_box.setValue(12)
        self.gridHeight_box.setMinimum(3)
        self.gridInit_boxes.setValue(6)
        self.level_box.addItems(['1 (blind)', '2', '3'])
        self.log_box.clear()
        self.log_box.append("Welcome to Circle the dot!\n")

        # Slots
        self.searchPath_button.clicked.connect(self.on_load)
        self.start_button.clicked.connect(self.on_start)
        self.save_button.clicked.connect(self.on_save)
        self.level_box.currentTextChanged.connect(self.change_level)

        # Layout
        self.formLayout = QFormLayout()
        self.formLayout.addRow('Grid Width', self.gridWidth_box)
        self.formLayout.addRow('Grid Height', self.gridHeight_box)
        self.formLayout.addRow('Initial red boxes', self.gridInit_boxes)
        self.formLayout.addRow('Fugitive level', self.level_box)

        self.formLayout2 = QFormLayout()
        self.formLayout2.addRow('Load game', self.searchPath_button)

        vLayout = QVBoxLayout()
        vLayout.addLayout(self.formLayout)
        vLayout.addWidget(self.start_button)
        vLayout.addLayout(self.formLayout2)
        vLayout.addWidget(self.save_button)
        vLayout.addStretch()
        vLayout.addWidget(self.b_score_lay)
        vLayout.addWidget(self.score_lay)
        vLayout.addWidget(self.log_box)

        self.setLayout(vLayout)

    def on_start(self):
        """Initialise parameters."""
        self.controller.w = self.gridWidth_box.value()
        self.controller.h = self.gridHeight_box.value()
        self.controller.nb_cond = self.gridInit_boxes.value()
        self.controller.start()

    def on_load(self):
        """Update parameters when loading a game."""
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Load game", "", "All Files (*);;Python Files (*.py)",
            options=options
            )
        try:
            name = os.path.basename(fileName)
            self.searchPath_button.setText(name)
        except Exception:
            self.log_box.append('There was an error with the file submitted')
            return(0)
        try:
            self.controller.load_game(fileName)
        except Exception:
            self.log_box.append(
                "the file submitted does not have the expected layout")

    def on_save(self):
        """Trigger parameters' backup."""
        try:
            fileName = QFileDialog.getSaveFileName(self, "Select checkpoint",
                                                   "", "All Files(*)")
            self.controller.save_game(fileName)
        except Exception:
            self.log_box.append(
                "Game could not be saved. Please create a game.\n")

    def change_level(self):
        """Trigger level change."""
        print("Level changed to", int(self.level_box.currentIndex()) + 1)
        self.controller.choose_level(int(self.level_box.currentIndex()))

    def refresh(self):
        """Update object."""
        self.gridWidth_box.setValue(self.controller.w)
        self.gridHeight_box.setValue(self.controller.h)
        self.gridInit_boxes.setValue(self.controller.nb_cond)
        self.level_box.setCurrentIndex(self.controller.level)
        self.b_score_lay.setText(f'Best score : {self.controller.best_score}')
        self.score_lay.setText('Moves : ' + str(self.controller.nbTurns))


class Widget(QWidget):
    """Manages the layout of the objects defined in previous classes."""

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
        """Update object."""
        pass


class Window(QMainWindow):
    """Main window: Widget plus title."""

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.controller.add_client(self)
        self.setWindowTitle("Circle the dot")
        mainwidget = Widget(self, controller)
        self.setCentralWidget(mainwidget)

    def refresh(self):
        """Update object."""
        pass


def main():
    """Instanciate necessary classes and display application."""
    app = QApplication([])
    controller = CtDController()
    win = Window(controller)
    win.show()
    app.exec()


if __name__ == "__main__":
    main()
