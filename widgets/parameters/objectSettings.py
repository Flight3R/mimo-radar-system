from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QGroupBox, QVBoxLayout, QLineEdit

from globalDef import global_big_spacing, global_small_spacing
from dto.object import Object
from widgets.inputs.coordinateInput import CoordinateInput
from widgets.inputs.keyValueInput import KeyValueInput


class ObjectSettings(QWidget):
    value_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        layout.setSpacing(global_small_spacing)

        self.label = QLineEdit("Object")
        self.label.textChanged.connect(self.value_changed)
        layout.addWidget(self.label)

        self.coordinate_input = CoordinateInput()
        self.coordinate_input.value_changed.connect(self.value_changed)
        layout.addWidget(self.coordinate_input)

        self.reflection_input = KeyValueInput("Reflection coefficient")
        self.reflection_input.value_changed.connect(self.value_changed)
        layout.addWidget(self.reflection_input)

        self.setLayout(layout)

    def get_object(self):
        name = self.label.text()
        coordinates = self.coordinate_input.get_value()
        reflection = self.reflection_input.get_value()

        return Object("object", name, coordinates, reflection)

    def update_coordinates(self, coordinates):
        self.coordinate_input.set_value(coordinates)