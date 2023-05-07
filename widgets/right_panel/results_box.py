from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QCheckBox, QPushButton, QSizePolicy

from dto.drawing_settings import DrawingSettings


class ResultsBox(QGroupBox):

    def __init__(self):
        super(ResultsBox, self).__init__("Results")
        self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)

        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        vbox.setSpacing(0)



        self.setLayout(vbox)

    def set_results(self):
        pass