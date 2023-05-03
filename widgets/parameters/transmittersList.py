from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QScrollArea, QLineEdit

from globalDef import global_small_spacing, global_big_spacing
from dto.transmitter import Transmitter
from widgets.parameters.inputs.coordinateInput import CoordinateInput
from widgets.parameters.inputs.keyValueInput import KeyValueInput


class TransmittersList(QWidget):
    value_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.items_counter = 1
        self.items = []

        self.vbox = QVBoxLayout()
        self.add_button = QPushButton('Add transmitter')
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
        name = 'Transmitter {}'.format(self.items_counter)

        item = QWidget(self)
        vbox = QVBoxLayout()
        vbox.setSpacing(0)

        index = QLineEdit("transmitter_" + str(self.items_counter))
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
        dipole_number = KeyValueInput("Power", min_val=0, max_val=100, init_val=20)
        dipole_number.value_changed.connect(self.value_changed)
        vbox.addWidget(dipole_number)

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
        transmitters = []
        for item in self.items:
            index = item.layout().itemAt(0).widget().text()
            name = item.layout().itemAt(1).widget().layout().itemAt(0).widget().text()
            power = item.layout().itemAt(2).widget().get_value()
            coordinate = item.layout().itemAt(3).widget().get_value()

            transmitters.append(Transmitter(index, name, coordinate, power))

        return transmitters

    def update_coordinates(self, index, coordinates):
        filtered = list(filter(lambda item: item.layout().itemAt(0).widget().text() == index, self.items))
        assert len(filtered) == 1

        filtered[0].layout().itemAt(3).widget().set_value(coordinates)


