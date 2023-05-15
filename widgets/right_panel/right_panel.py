from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QPushButton, QWidget

from widgets.right_panel.drawing_settings_box import DrawingSettingsBox
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


        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignmentFlag.AlignTop)
        vbox.setContentsMargins(0, 0, 0, 0)

        self.simulation_settings = SimulationSettingsBox()
        vbox.addWidget(self.simulation_settings)

        self.drawing_settings = DrawingSettingsBox()
        self.drawing_settings.settings_changed.connect(self.drawing_settings_changed)
        vbox.addWidget(self.drawing_settings)

        self.run_button = QPushButton("Run simulation")
        self.run_button.setCheckable(True)
        self.run_button.clicked.connect(self.run_button_clicked)
        vbox.addWidget(self.run_button)

        self.generate_heatmap_button = QPushButton("Generate heatmap")
        self.generate_heatmap_button.clicked.connect(self.generate_heatmap)
        vbox.addWidget(self.generate_heatmap_button)

        self.results = ResultsBox()
        vbox.addWidget(self.results)

        self.setLayout(vbox)

    def run_button_clicked(self):
        if self.run_button.isChecked():
            self.run_simulation.emit()
            self.run_button.setText("Back to edit mode")
        else:
            self.back_to_edit.emit()
            self.run_button.setText("Run simulation")