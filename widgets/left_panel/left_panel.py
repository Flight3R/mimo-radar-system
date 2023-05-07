from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QGroupBox, QVBoxLayout

from widgets.left_panel.antennas_list import AntennasList
from widgets.left_panel.object_settings import ObjectSettings
from widgets.left_panel.transmitters_list import TransmittersList


class LeftPanel(QGroupBox):
    value_changed = pyqtSignal()

    def __init__(self):
        super(LeftPanel, self).__init__("Objects")
        self.setMinimumWidth(300)
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

    def update_position(self, index, position):
        if "object" in index:
            self.object_settings.update_position(position)
        elif "antenna" in index:
            self.antennas_list.update_position(index, position)
        elif "transmitter" in index:
            self.transmitters_list.update_position(index, position)

