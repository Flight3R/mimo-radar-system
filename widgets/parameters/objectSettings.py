from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit

from globalDef import global_small_spacing
from dto.object import Object
from widgets.parameters.inputs.positionInput import PositionInput
from widgets.parameters.inputs.valueInput import ValueInput


class ObjectSettings(QWidget):
    value_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        layout.setSpacing(global_small_spacing)

        self.label = QLineEdit("Object")
        self.label.textChanged.connect(self.value_changed)
        layout.addWidget(self.label)

        self.position_input = PositionInput()
        self.position_input.value_changed.connect(self.value_changed)
        layout.addWidget(self.position_input)

        self.reflection_input = ValueInput("Reflection coefficient")
        self.reflection_input.value_changed.connect(self.value_changed)
        layout.addWidget(self.reflection_input)

        self.setLayout(layout)

    def get_object(self):
        name = self.label.text()
        position = self.position_input.get_value()
        reflection = self.reflection_input.get_value()

        return Object("object", name, position, reflection)

    def update_position(self, position):
        self.position_input.set_value(position)