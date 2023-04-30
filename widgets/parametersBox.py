from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QPushButton

from widgets.parameters.antennasList import AntennasList
from widgets.parameters.objectSettings import ObjectSettings
from widgets.parameters.transmittersList import TransmittersList


class ParametersBox(QGroupBox):
    value_changed = pyqtSignal()
    run_simulation = pyqtSignal()

    def __init__(self):
        super(ParametersBox, self).__init__("Parameters")
        self.setMaximumWidth(400)

        layout = QVBoxLayout()

        self.object_settings = ObjectSettings()
        self.object_settings.value_changed.connect(self.value_changed)
        layout.addWidget(self.object_settings)

        self.antennas_list = AntennasList()
        self.antennas_list.value_changed.connect(self.value_changed)
        layout.addWidget(self.antennas_list)

        self.transmitters_list = TransmittersList()
        self.transmitters_list.value_changed.connect(self.value_changed)
        layout.addWidget(self.transmitters_list)

        self.run_simulation_button = QPushButton("Run simulation")
        self.run_simulation_button.clicked.connect(self.run_simulation)
        layout.addWidget(self.run_simulation_button)

        self.setLayout(layout)

    def get_data(self):
        object = self.object_settings.get_object()
        antennas = self.antennas_list.get_items()
        transmitters = self.transmitters_list.get_items()

        return object, antennas, transmitters