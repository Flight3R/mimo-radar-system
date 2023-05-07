from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QSpinBox, QLabel, QHBoxLayout


class ValueInput(QWidget):
    value_changed = pyqtSignal()

    def __init__(self, key, min_val=-100, max_val=100, init_val=0, parent=None):
        super().__init__(parent)

        self.spin = QSpinBox(self)
        self.spin.valueChanged.connect(self.value_changed)
        self.spin.setRange(min_val, max_val)
        self.spin.setValue(init_val)

        label = QLabel(key + ':', self)

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
