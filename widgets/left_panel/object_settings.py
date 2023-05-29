from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit

from dto.object import Object
from global_def import global_small_spacing
from widgets.inputs.position_input import PositionInput


class ObjectSettings(QWidget):
    value_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        layout.setSpacing(global_small_spacing)

        self.label = QLineEdit("Object")
        self.label.textChanged.connect(self.value_changed)
        layout.addWidget(self.label)

        self.position_input = PositionInput(x_init=25, y_init=200)
        self.position_input.value_changed.connect(self.value_changed)
        layout.addWidget(self.position_input)

        self.setLayout(layout)

    def get_object(self):
        name = self.label.text()
        position = self.position_input.get_value()

        return Object("object", name, position)

    def update_position(self, position):
        self.position_input.set_value(position)
