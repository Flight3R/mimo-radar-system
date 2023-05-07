from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QCheckBox, QPushButton, QSizePolicy

from dto.drawing_settings import DrawingSettings


class DrawingSettingsBox(QGroupBox):
    settings_changed = pyqtSignal()

    def __init__(self):
        super(DrawingSettingsBox, self).__init__("Printing settings")
        self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)

        vbox = QVBoxLayout()
        vbox.setSpacing(0)

        self.show_names = QCheckBox('Show names')
        self.show_names.stateChanged.connect(self.settings_changed)
        self.show_names.setCheckState(Qt.CheckState.Checked)
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

        return DrawingSettings(show_names, show_circles, show_lines, show_real_object, show_detected_object)
