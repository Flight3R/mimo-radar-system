from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QSpinBox, QLabel, QHBoxLayout, QVBoxLayout, QDoubleSpinBox

from globalDef import global_small_spacing


class FloatValueInput(QWidget):
    value_changed = pyqtSignal()

    def __init__(self, name, min_val=-100, max_val=100, init_val=0, step=0.1, parent=None):
        super().__init__(parent)

        self.spin = QDoubleSpinBox(self)
        self.spin.valueChanged.connect(self.value_changed)
        self.spin.setRange(min_val, max_val)
        self.spin.setSingleStep(step)
        self.spin.setValue(init_val)

        label = QLabel(name + ':', self)

        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.addWidget(label)
        hbox.addWidget(self.spin)
        hbox.addStretch()

        self.setLayout(hbox)

    def get_value(self):
        return self.spin.value()

    def set_value(self, x):
        self.spin.setValue(x)
