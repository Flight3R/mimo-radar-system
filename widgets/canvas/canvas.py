from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPen, QColorConstants, QBrush, QFont
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, QGraphicsTextItem

from globalDef import sandbox_size

font = QFont("Arial", 10)


class Canvas(QGraphicsView):
    settings = True

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setScene(QGraphicsScene(self))

    def drawBackground(self, painter, rect):
        painter.fillRect(rect, QColorConstants.White)

        painter.setPen(QPen(QColor(200, 200, 200), 1))
        for i in range(-sandbox_size, sandbox_size + 1, 20):
            painter.drawLine(i, -sandbox_size, i, sandbox_size)
            painter.drawLine(-sandbox_size, i, sandbox_size, i)

        painter.setPen(QPen(QColor(0, 0, 0), 1))
        painter.drawLine(-sandbox_size, 0, sandbox_size, 0)
        painter.drawLine(0, -sandbox_size, 0, sandbox_size)


    def repaint_canvas(self, object, antennas, transmitters, settings):
        self.settings = settings

        self.scene().clear()
        self.paint_object(object)

        for antenna in antennas:
            self.paint_antenna(antenna)

        for transmitter in transmitters:
            self.paint_transmitter(transmitter)

    def paint_object(self, object):
        self.paint_circle(object.coordinates, "red")
        self.paint_name(object.coordinates, object.name)

    def paint_transmitter(self, transmitter):
        self.paint_circle(transmitter.coordinates, "blue")
        self.paint_name(transmitter.coordinates, transmitter.name)

    def paint_antenna(self, antenna):
        self.paint_circle(antenna.coordinates, "green")
        self.paint_name(antenna.coordinates, antenna.name)

    def paint_name(self, coordinates, name):
        if self.settings.show_names:
            name = QGraphicsTextItem(name)
            name.setFont(font)
            name.setDefaultTextColor(QColor("black"))
            name.setPos(coordinates.x, coordinates.y)
            self.scene().addItem(name)

    def paint_circle(self, coordinates, color="blue", size=10):
        circle = QGraphicsEllipseItem(coordinates.x - size / 2, coordinates.y - size / 2, size, size)
        circle.setPen(QPen(QColor("black")))
        circle.setBrush(QBrush(QColor(color)))
        self.scene().addItem(circle)