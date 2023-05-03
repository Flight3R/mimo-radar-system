from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QPushButton, QHBoxLayout

from widgets.parameters.antennasList import AntennasList
from widgets.parameters.objectSettings import ObjectSettings
from widgets.parameters.transmittersList import TransmittersList


class ParametersBox(QGroupBox):
    value_changed = pyqtSignal()

    def __init__(self):
        super(ParametersBox, self).__init__("Parameters")
        self.setMaximumWidth(400)

        vbox = QVBoxLayout()

        self.object_settings = ObjectSettings()
        self.object_settings.value_changed.connect(self.value_changed)
        vbox.addWidget(self.object_settings)

        self.antennas_list = AntennasList()
        self.antennas_list.value_changed.connect(self.value_changed)
        vbox.addWidget(self.antennas_list)

        self.transmitters_list = TransmittersList()
        self.transmitters_list.value_changed.connect(self.value_changed)
        vbox.addWidget(self.transmitters_list)

        self.setLayout(vbox)

    def get_data(self):
        object = self.object_settings.get_object()
        antennas = self.antennas_list.get_items()
        transmitters = self.transmitters_list.get_items()

        return object, antennas, transmitters

    def update_position(self, index, coordinates):
        if "object" in index:
            self.object_settings.update_coordinates(coordinates)
        elif "antenna" in index:
            self.antennas_list.update_coordinates(index, coordinates)
        elif "transmitter" in index:
            self.transmitters_list.update_coordinates(index, coordinates)

