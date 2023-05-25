from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QCheckBox, QSizePolicy

from dto.drawing_settings import DrawingSettings


class DrawingSettingsBox(QGroupBox):
    settings_changed = pyqtSignal()

    def __init__(self):
        super(DrawingSettingsBox, self).__init__("Drawing settings")
        self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)

        vbox = QVBoxLayout()
        vbox.setSpacing(0)

        self.show_names = QCheckBox('Show names')
        self.show_names.stateChanged.connect(self.settings_changed)
        self.show_names.setCheckState(Qt.CheckState.Checked)
        vbox.addWidget(self.show_names)

        self.show_grid = QCheckBox('Show grid')
        self.show_grid.stateChanged.connect(self.settings_changed)
        self.show_grid.setCheckState(Qt.CheckState.Checked)
        vbox.addWidget(self.show_grid)

        self.show_numbers = QCheckBox('Show axis coordinates')
        self.show_numbers.stateChanged.connect(self.settings_changed)
        self.show_numbers.setCheckState(Qt.CheckState.Checked)
        vbox.addWidget(self.show_numbers)

        self.show_helpers_lines = QCheckBox('Show calculation lines (if exist)')
        self.show_helpers_lines.stateChanged.connect(self.settings_changed)
        vbox.addWidget(self.show_helpers_lines)

        self.show_helpers_points = QCheckBox('Show calculation points (if exist)')
        self.show_helpers_points.stateChanged.connect(self.settings_changed)
        vbox.addWidget(self.show_helpers_points)

        self.show_helpers_circles = QCheckBox('Show calculation circles (if exist)')
        self.show_helpers_circles.stateChanged.connect(self.settings_changed)
        vbox.addWidget(self.show_helpers_circles)



        self.setLayout(vbox)

    def get_settings(self):
        show_names = self.show_names.checkState().value != 0
        show_grid = self.show_grid.checkState().value != 0
        show_numbers = self.show_numbers.checkState().value != 0
        show_helpers_lines = self.show_helpers_lines.checkState().value != 0
        show_helpers_points = self.show_helpers_points.checkState().value != 0
        show_helpers_circles = self.show_helpers_circles.checkState().value != 0


        return DrawingSettings(show_names, show_grid, show_numbers, show_helpers_lines, show_helpers_points, show_helpers_circles)
