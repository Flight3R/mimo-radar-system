from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QPushButton, QWidget, QMainWindow, QLabel, QDialog

from widgets.right_panel.drawing_settings_box import DrawingSettingsBox
from widgets.right_panel.heatmap_box import HeatmapBox
from widgets.right_panel.heatmap_window import HeatmapWindow
from widgets.right_panel.results_box import ResultsBox
from widgets.right_panel.simulation_settings_box import SimulationSettingsBox


class RightPanel(QWidget):
    drawing_settings_changed = pyqtSignal()
    run_simulation = pyqtSignal()
    generate_heatmap = pyqtSignal()
    back_to_edit = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setMinimumWidth(300)
        self.setMaximumWidth(400)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)


        self.drawing_settings = DrawingSettingsBox()
        self.drawing_settings.settings_changed.connect(self.drawing_settings_changed)
        layout.addWidget(self.drawing_settings)

        self.simulation_settings = SimulationSettingsBox()
        layout.addWidget(self.simulation_settings)

        self.run_button = QPushButton("Run simulation")
        self.run_button.setCheckable(True)
        self.run_button.clicked.connect(self.run_button_clicked)
        layout.addWidget(self.run_button)

        self.results = ResultsBox()
        layout.addWidget(self.results)

        self.heatmap_box = HeatmapBox()
        layout.addWidget(self.heatmap_box)

        self.generate_heatmap_button = QPushButton("Generate heatmap")
        self.generate_heatmap_button.clicked.connect(self.generate_heatmap)
        layout.addWidget(self.generate_heatmap_button)


        self.setLayout(layout)

    def run_button_clicked(self):
        if self.run_button.isChecked():
            self.run_simulation.emit()
            self.run_button.setText("Back to edit mode")
        else:
            self.back_to_edit.emit()
            self.run_button.setText("Run simulation")

