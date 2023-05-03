from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QPalette, QColor, QPainter, QPen, QColorConstants
from PyQt6.QtWidgets import QWidget, QGroupBox, QGraphicsView, QGraphicsScene, QVBoxLayout

from globalDef import sandbox_size

from widgets.canvas.graphicsView import GraphicsView
from widgets.canvas.pointItem import PointItem


class CanvasBox(QGroupBox):
    def __init__(self, item_moved):
        super(CanvasBox, self).__init__("Canvas")
        self.item_moved = item_moved
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(-sandbox_size, -sandbox_size, 2*sandbox_size, 2*sandbox_size)

        self.view = GraphicsView(self.scene)

        layout = QVBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)


    def repaint_canvas(self, object, antennas, transmitters, settings):
        self.scene.clear()

        object_item = PointItem(object.index, object.coordinates, object.name,
                                settings.show_names, self.item_moved, QColorConstants.Red)
        self.scene.addItem(object_item)

        for antenna in antennas:
            antenna_item = PointItem(antenna.index, antenna.coordinates, antenna.name,
                                     settings.show_names, self.item_moved, QColorConstants.Blue)
            self.scene.addItem(antenna_item)

        for transmitter in transmitters:
            transmitter_item = PointItem(transmitter.index, transmitter.coordinates, transmitter.name,
                                         settings.show_names, self.item_moved, QColorConstants.Green)
            self.scene.addItem(transmitter_item)


