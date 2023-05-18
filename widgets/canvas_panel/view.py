from PyQt6.QtGui import QColor, QPen, QColorConstants, QFont, QFontMetrics
from PyQt6.QtWidgets import QGraphicsView

from globalDef import sandbox_size

font = QFont("Arial", 10)


class View(QGraphicsView):
    settings = None

    def __init__(self, parent=None):
        super().__init__(parent)

    def drawBackground(self, painter, rect):
        painter.fillRect(rect, QColorConstants.White)

        if self.settings.show_grid:
            painter.setPen(QPen(QColor(200, 200, 200), 1))
            for i in range(-sandbox_size, sandbox_size + 1, 100):
                painter.drawLine(i, -sandbox_size, i, sandbox_size)
                painter.drawLine(-sandbox_size, i, sandbox_size, i)

            painter.setPen(QPen(QColor(0, 0, 0), 1))
            painter.drawLine(-sandbox_size, 0, sandbox_size, 0)
            painter.drawLine(0, -sandbox_size, 0, sandbox_size)

        if self.settings.show_numbers:
            painter.setPen(QPen(QColorConstants.Black, 1))
            for i in range(-sandbox_size, sandbox_size + 1, 100):
                name = str(i)
                name_rect = QFontMetrics(painter.font()).boundingRect(name)

                painter.drawText(i - int(name_rect.width() / 2), name_rect.height() + 1, str(i))
                painter.drawText(0 - int(name_rect.width() / 2), i + name_rect.height() + 1, str(i))
