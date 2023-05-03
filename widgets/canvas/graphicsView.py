from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPen, QColorConstants, QBrush, QFont
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, QGraphicsTextItem

from globalDef import sandbox_size

font = QFont("Arial", 10)


class GraphicsView(QGraphicsView):
    settings = True

    def __init__(self, parent=None):
        super().__init__(parent)


    def drawBackground(self, painter, rect):
        painter.fillRect(rect, QColorConstants.White)

        painter.setPen(QPen(QColor(200, 200, 200), 1))
        for i in range(-sandbox_size, sandbox_size + 1, 50):
            painter.drawLine(i, -sandbox_size, i, sandbox_size)
            painter.drawLine(-sandbox_size, i, sandbox_size, i)

        painter.setPen(QPen(QColor(0, 0, 0), 1))
        painter.drawLine(-sandbox_size, 0, sandbox_size, 0)
        painter.drawLine(0, -sandbox_size, 0, sandbox_size)

