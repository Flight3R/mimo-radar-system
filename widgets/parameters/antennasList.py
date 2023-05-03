from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QScrollArea, QLineEdit

from globalDef import global_small_spacing, global_big_spacing
from dto.antenna import Antenna
from widgets.inputs.coordinateInput import CoordinateInput
from widgets.inputs.keyValueInput import KeyValueInput


class AntennasList(QWidget):
    value_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.items_counter = 1
        self.items = []

        self.vbox = QVBoxLayout()
        self.add_button = QPushButton('Add antenna')
        self.add_button.clicked.connect(self.add_item)

        hbox = QHBoxLayout()
        hbox.addWidget(self.add_button)
        hbox.addStretch()

        self.vbox.addLayout(hbox)
        self.vbox.addStretch()
        self.vbox.setSpacing(global_big_spacing)

        widget = QWidget()
        widget.setLayout(self.vbox)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(widget)

        main_vbox = QVBoxLayout(self)
        main_vbox.addWidget(scroll_area)

    def add_item(self):
        name = 'Antenna {}'.format(self.items_counter)

        item = QWidget(self)
        vbox = QVBoxLayout()
        vbox.setSpacing(0)

        index = QLineEdit("antenna_" + str(self.items_counter))
        index.setVisible(False)
        vbox.addWidget(index)

        # label & remove button
        labelWidget = QWidget()
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        label = QLineEdit(name)
        label.textChanged.connect(self.value_changed)
        hbox.addWidget(label)

        remove_button = QPushButton('Remove', item)
        remove_button.clicked.connect(lambda: self.remove_item(item))
        hbox.addWidget(remove_button)
        labelWidget.setLayout(hbox)
        vbox.addWidget(labelWidget)

        # other parameters
        dipole_number = KeyValueInput("Dipole number", min_val=0, max_val=4, init_val=2)
        dipole_number.value_changed.connect(self.value_changed)
        vbox.addWidget(dipole_number)

        dipole_spread = KeyValueInput("Dipole spread", min_val=0, max_val=5, init_val=1)
        dipole_spread.value_changed.connect(self.value_changed)
        vbox.addWidget(dipole_spread)

        coordinates = CoordinateInput()
        coordinates.value_changed.connect(self.value_changed)
        vbox.addWidget(coordinates)


        vbox.addStretch()
        vbox.setSpacing(global_small_spacing)
        item.setLayout(vbox)
        self.vbox.insertWidget(self.vbox.count() - 1, item)

        self.items.append(item)
        self.items_counter += 1
        self.value_changed.emit()

    def remove_item(self, item):
        self.vbox.removeWidget(item)
        item.deleteLater()
        self.items.remove(item)
        self.value_changed.emit()


    def get_items(self):
        antennas = []
        for item in self.items:
            index = item.layout().itemAt(0).widget().text()
            name = item.layout().itemAt(1).widget().layout().itemAt(0).widget().text()
            dipole_number = item.layout().itemAt(2).widget().get_value()
            dipole_distance = item.layout().itemAt(3).widget().get_value()
            coordinate = item.layout().itemAt(4).widget().get_value()

            antennas.append(Antenna(index, name, coordinate, dipole_number, dipole_distance))

        return antennas

    def update_coordinates(self, index, coordinates):
        filtered = list(filter(lambda item: item.layout().itemAt(0).widget().text() == index, self.items))
        assert len(filtered) == 1

        filtered[0].layout().itemAt(4).widget().set_value(coordinates)




