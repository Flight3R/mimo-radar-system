from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPalette, QColorConstants
from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QSizePolicy, QLabel, QPushButton

from globalDef import sandbox_size
from widgets.inputs.float_value_input import FloatValueInput
from widgets.inputs.value_input import ValueInput


class HeatmapBox(QGroupBox):
    def __init__(self):
        super(HeatmapBox, self).__init__("Heatmap")
        layout = QVBoxLayout()
        layout.setSpacing(0)

        self.edge_length = ValueInput('Edge length', min_val=1, max_val=sandbox_size, init_val=200)
        layout.addWidget(self.edge_length)

        self.resolution = ValueInput('Resolution', min_val=1, max_val=100, init_val=20)
        layout.addWidget(self.resolution)

        self.setLayout(layout)

    def get_settings(self):
        edge_length = self.edge_length.get_value()
        resolution = self.resolution.get_value()

        return edge_length, resolution

