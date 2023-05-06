from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QSpinBox, QLabel, QHBoxLayout

from globalDef import global_big_spacing, sandbox_size
from dto.position import Position


class PositionInput(QWidget):
    value_changed = pyqtSignal()

    def __init__(self, x_min=-sandbox_size, x_max=sandbox_size, y_min=-sandbox_size, y_max=sandbox_size, x_init=0, y_init=0, parent=None):
        super().__init__(parent)
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

        self.x_spin = QSpinBox(self)
        self.x_spin.valueChanged.connect(self.value_changed)
        self.x_spin.setRange(self.x_min, self.x_max)
        self.x_spin.setValue(x_init)

        self.y_spin = QSpinBox(self)
        self.y_spin.valueChanged.connect(self.value_changed)
        self.y_spin.setRange(self.y_min, self.y_max)
        self.y_spin.setValue(y_init)

        x_label = QLabel('X:', self)
        y_label = QLabel('Y:', self)

        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.addWidget(x_label)
        hbox.addWidget(self.x_spin)
        hbox.addWidget(y_label)
        hbox.addWidget(self.y_spin)
        hbox.setSpacing(global_big_spacing)
        hbox.addStretch()

        self.setLayout(hbox)

    def get_value(self):
        x = self.x_spin.value()
        y = self.y_spin.value()
        return Position(x, y)

    def set_value(self, position):
        self.x_spin.setValue(position.x)
        self.y_spin.setValue(position.y)
