from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QCheckBox, QPushButton, QHBoxLayout, QWidget, QRadioButton, \
    QButtonGroup, QSizePolicy

from dto.drawing_settings import DrawingSettings
from dto.simulation_settings import SimulationSettings
from widgets.inputs.float_value_input import FloatValueInput
from widgets.inputs.radio_buttons import RadioButtons


class SimulationSettingsBox(QGroupBox):
    settings_changed = pyqtSignal()

    def __init__(self):
        super(SimulationSettingsBox, self).__init__("Simulation settings")
        self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)

        layout = QVBoxLayout()
        layout.setSpacing(0)


        self.method_rb = RadioButtons("Method", ["variance", "regression", "analytic"])
        self.method_rb.value_changed.connect(self.settings_changed)
        layout.addWidget(self.method_rb)

        self.phase_increment_rb = RadioButtons("Phase increment", ["yes", "no"])
        self.phase_increment_rb.value_changed.connect(self.settings_changed)
        layout.addWidget(self.phase_increment_rb)


        self.wavelength_input = FloatValueInput('Wavelength', min_val=0.00000001, max_val=float("inf"), init_val=1.0, step=0.01)
        self.wavelength_input.value_changed.connect(self.settings_changed)
        layout.addWidget(self.wavelength_input)

        self.phase_err_input = FloatValueInput('Phase error coefficient', min_val=0, max_val=1, init_val=0, step=0.01)
        self.phase_err_input.value_changed.connect(self.settings_changed)
        layout.addWidget(self.phase_err_input)



        self.setLayout(layout)

    def get_settings(self):
        detection_method = self.method_rb.get_value()
        phase_increment = self.phase_increment_rb.get_value()
        wavelength = self.wavelength_input.get_value()
        phase_err = self.phase_err_input.get_value()

        return SimulationSettings(detection_method, phase_increment, wavelength, phase_err)
