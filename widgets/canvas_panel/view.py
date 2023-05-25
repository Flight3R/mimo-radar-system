from PyQt6.QtCore import QPoint, QLine
from PyQt6.QtGui import QColor, QPen, QColorConstants, QFont, QFontMetrics, QPainter
from PyQt6.QtWidgets import QGraphicsView

from dto.drawing_settings import DrawingSettings
from dto.helpers import Helpers
from global_def import sandbox_size

font = QFont("Arial", 10)


class View(QGraphicsView):
    settings: DrawingSettings = None
    helpers: Helpers = None


    def __init__(self, parent=None):
        super().__init__(parent)

    def drawBackground(self, painter, rect):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(rect, QColorConstants.White)

        if self.settings.show_grid:
            painter.setPen(QPen(QColor(200, 200, 200), 1))
            for i in range(-sandbox_size, sandbox_size + 1, 100):
                painter.drawLine(i, -sandbox_size, i, sandbox_size)
                painter.drawLine(-sandbox_size, i, sandbox_size, i)

            painter.setPen(QPen(QColorConstants.Black, 1))
            painter.drawLine(-sandbox_size, 0, sandbox_size, 0)
            painter.drawLine(0, -sandbox_size, 0, sandbox_size)

        if self.settings.show_numbers:
            painter.setPen(QPen(QColorConstants.Black, 1))
            for i in range(-sandbox_size, sandbox_size + 1, 100):
                name = str(i)
                name_rect = QFontMetrics(painter.font()).boundingRect(name)

                painter.drawText(i - int(name_rect.width() / 2), name_rect.height() + 1, str(i))
                painter.drawText(0 - int(name_rect.width() / 2), i + name_rect.height() + 1, str(i))


        if self.helpers.regression_lines is not None and self.settings.show_helpers_lines:
            painter.setPen(QPen(QColorConstants.Black, 1))
            for line in self.helpers.regression_lines:
                start_x = -sandbox_size
                end_x = sandbox_size
                start_y = int(line[0] * start_x + line[1])
                end_y = int(line[0] * end_x + line[1])

                painter.drawLine(start_x, start_y, end_x, end_y)

        if self.helpers.all_points is not None and self.settings.show_helpers_points:
            painter.setPen(QPen(QColorConstants.Black, 1))
            for point in self.helpers.all_points:
                painter.drawEllipse(QPoint(int(point.x), int(point.y)), 1, 1)

        if self.helpers.all_circles is not None and self.settings.show_helpers_circles:
            painter.setPen(QPen(QColorConstants.Black, 1))
            for circle in self.helpers.all_circles:
                radius = int(circle[2])
                painter.drawEllipse(QPoint(int(circle[0]), int(circle[1])), radius, radius)
