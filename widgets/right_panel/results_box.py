import math

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColorConstants
from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QSizePolicy, QLabel


def distance(p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    return math.sqrt(dx * dx + dy * dy)


class ResultsBox(QGroupBox):
    def __init__(self):
        super(ResultsBox, self).__init__("Results")
        self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.layout.setSpacing(0)

        self.setLayout(self.layout)

    def set_results(self, real_position, detected_position):

        real_position_text = QLabel(f"Object position: X={real_position.x}, Y={real_position.y}")
        self.layout.addWidget(real_position_text)

        detected_position_text = QLabel(f"Obtained position: X={detected_position.x}, Y={detected_position.y}")
        self.layout.addWidget(detected_position_text)

        error_text = QLabel(f"Position error: {distance(detected_position, real_position)}")
        self.layout.addWidget(error_text)

    def show_error(self, error):
        error = QLabel(error)

        palette = error.palette()
        palette.setColor(QPalette.ColorRole.WindowText, QColorConstants.Red)
        error.setPalette(palette)
        self.layout.addWidget(error)

    def clear(self):
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
