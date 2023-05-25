from PyQt6.QtGui import QColorConstants, QColor, QPen, QPainter, QFontMetrics
from PyQt6.QtWidgets import QGroupBox, QGraphicsView, QGraphicsScene, QVBoxLayout, QGraphicsItem

from global_def import sandbox_size
from widgets.canvas_panel.view import View
from widgets.canvas_panel.point_item import PointItem


class CanvasPanel(QGroupBox):
    def __init__(self, item_moved):
        super(CanvasPanel, self).__init__("Canvas")
        self.item_moved = item_moved
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(-sandbox_size, -sandbox_size, 2 * sandbox_size, 2 * sandbox_size)

        self.view = View(self.scene)
        self.view.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)

        layout = QVBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)

    def repaint_canvas(self, real_object, detected_object, antennas, transmitters, settings, helpers):
        self.view.settings = settings
        self.view.helpers = helpers
        self.scene.clear()
        self.scene.update()

        self.scene.addItem(PointItem(real_object.index, real_object.position, real_object.name, settings.show_names, self.item_moved, QColorConstants.Red))

        if detected_object.position is not None:
            self.scene.addItem(PointItem(detected_object.index, detected_object.position, detected_object.name, settings.show_names, self.item_moved, QColor(255, 120, 120)))

        for antenna in antennas:
            self.scene.addItem(PointItem(antenna.index, antenna.position, antenna.name, settings.show_names, self.item_moved, QColorConstants.Blue))

        for transmitter in transmitters:
            self.scene.addItem(PointItem(transmitter.index, transmitter.position, transmitter.name, settings.show_names, self.item_moved, QColorConstants.Green))



    def set_points_movable(self, value):
        for item in self.scene.items():
            item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, value)

