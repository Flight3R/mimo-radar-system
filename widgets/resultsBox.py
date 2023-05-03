from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QCheckBox, QPushButton

from dto.settings import Settings
from widgets.results.drawingSettings import DrawingSettings


class ResultsBox(QGroupBox):
    settings_changed = pyqtSignal()
    run_simulation = pyqtSignal()
    back_to_edit = pyqtSignal()

    def __init__(self):
        super(ResultsBox, self).__init__("Results")
        self.setMaximumWidth(400)

        vbox = QVBoxLayout()


        self.drawing_settings = DrawingSettings()
        self.drawing_settings.settings_changed.connect(self.settings_changed)
        vbox.addWidget(self.drawing_settings)

        self.run_button = QPushButton("Run simulation")
        self.run_button.setCheckable(True)
        self.run_button.clicked.connect(self.run_button_clicked)
        vbox.addWidget(self.run_button)

        self.setLayout(vbox)

    def run_button_clicked(self):
        if self.run_button.isChecked():
            self.run_simulation.emit()
            self.run_button.setText("Back to edit mode")
        else:
            self.back_to_edit.emit()
            self.run_button.setText("Run simulation")