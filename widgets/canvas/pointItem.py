from PyQt6.QtCore import QRectF
from PyQt6.QtGui import QColorConstants, QPen, QColor, QBrush, QFontMetrics, QFont
from PyQt6.QtWidgets import QGraphicsItem

from dto.position import Position


class PointItem(QGraphicsItem):
    def __init__(self, index, position, name, show_name, item_moved_event, color=QColorConstants.Blue, size=14, parent=None):
        super().__init__(parent)
        self.index = index
        self.show_name = show_name
        self.size = size
        self.position = position
        self.name = name
        self.color = color
        self.font = QFont("Arial", 12)
        self.name_rect = QFontMetrics(self.font).boundingRect(self.name)
        self.name_x_offset = - int(self.name_rect.width() / 2)
        self.name_y_offset = int(1.6 * self.size)

        self.item_moved_event = item_moved_event
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)

    def paint(self, painter, option, widget=None):
        painter.setPen(QPen(QColor("black")))
        painter.setBrush(QBrush(QColor(self.color)))
        painter.drawEllipse(
            QRectF(self.position.x - self.size / 2, self.position.y - self.size / 2, self.size, self.size))
        if self.show_name:
            painter.setFont(self.font)
            painter.drawText(self.position.x + self.name_x_offset, self.position.y + self.name_y_offset,
                             self.name)

    def boundingRect(self):
        if self.show_name:
            return QRectF(
                min(self.position.x - self.size / 2, self.position.x - self.size / 2 + self.name_x_offset),
                min(self.position.y - self.size / 2, self.position.y - self.size / 2 + self.name_y_offset),
                max(self.size + self.name_x_offset + self.name_rect.width(), self.size + self.name_rect.width()) + 5,
                max(self.size + self.name_y_offset + self.name_rect.height(), self.size + self.name_rect.height()) + 5)
        else:
            return QRectF(self.position.x - self.size / 2, self.position.y - self.size / 2, self.size, self.size)

    def get_position(self):
        return Position(self.position.x + self.x(), self.position.y + self.y())

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.update()
        self.item_moved_event(self.index, self.get_position())


