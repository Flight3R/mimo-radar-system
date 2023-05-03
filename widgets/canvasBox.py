from PyQt6.QtGui import QPalette, QColor, QPainter, QPen, QColorConstants
from PyQt6.QtWidgets import QWidget, QGroupBox, QGraphicsView, QGraphicsScene, QVBoxLayout

from globalDef import sandbox_size

from widgets.canvas.graphicsView import GraphicsView
from widgets.canvas.pointItem import PointItem


class CanvasBox(QGroupBox):
    def __init__(self):
        super(CanvasBox, self).__init__("Canvas")
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(-sandbox_size, -sandbox_size, 2*sandbox_size, 2*sandbox_size)

        self.view = GraphicsView(self.scene)

        layout = QVBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)

    def repaint_canvas(self, object, antennas, transmitters, settings):
        self.scene.clear()

        self.scene.addItem(PointItem(object.coordinates, object.name, settings.show_names, QColorConstants.Red))

        for antenna in antennas:
            self.scene.addItem(PointItem(antenna.coordinates, antenna.name, settings.show_names, QColorConstants.Blue))

        for transmitter in transmitters:
            self.scene.addItem(PointItem(transmitter.coordinates, transmitter.name, settings.show_names, QColorConstants.Green))
