from PyQt6.QtGui import QPalette, QColor, QPainter, QPen
from PyQt6.QtWidgets import QWidget, QGroupBox, QGraphicsView, QGraphicsScene, QVBoxLayout

from widgets.canvas.canvas import Canvas


class CanvasBox(QGroupBox):

    def __init__(self):
        super(CanvasBox, self).__init__("Canvas")
        self.setMinimumSize(400, 400)
        layout = QVBoxLayout()
        self.canvas = Canvas()
        layout.addWidget(self.canvas)

        self.setLayout(layout)
