from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QCheckBox, QPushButton

from dto.settings import Settings


class DrawingSettings(QGroupBox):
    settings_changed = pyqtSignal()

    def __init__(self):
        super(DrawingSettings, self).__init__("Printing settings")

        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        vbox.setSpacing(0)


        self.show_names = QCheckBox('Show names')
        self.show_names.stateChanged.connect(self.settings_changed)
        vbox.addWidget(self.show_names)

        self.show_circles = QCheckBox('Show circles')
        self.show_circles.stateChanged.connect(self.settings_changed)
        vbox.addWidget(self.show_circles)

        self.show_lines = QCheckBox('Show lines')
        self.show_lines.stateChanged.connect(self.settings_changed)
        vbox.addWidget(self.show_lines)

        self.show_real_object = QCheckBox('Show real object')
        self.show_real_object.stateChanged.connect(self.settings_changed)
        vbox.addWidget(self.show_real_object)

        self.show_detected_object = QCheckBox('Show detected object')
        self.show_detected_object.stateChanged.connect(self.settings_changed)
        vbox.addWidget(self.show_detected_object)

        self.setLayout(vbox)

    def get_settings(self):
        show_names = self.show_names.checkState().value != 0
        show_circles = self.show_circles.checkState().value != 0
        show_lines = self.show_lines.checkState().value != 0
        show_real_object = self.show_real_object.checkState().value != 0
        show_detected_object = self.show_detected_object.checkState().value != 0

        return Settings(show_names, show_circles, show_lines, show_real_object, show_detected_object)
