from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QScrollArea, QLineEdit

from global_def import global_small_spacing, global_big_spacing
from dto.antenna import Antenna
from widgets.inputs.position_input import PositionInput
from widgets.inputs.float_value_input import FloatValueInput
from widgets.inputs.value_input import ValueInput


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

        self.add_item(x_init=-50, y_init=0, dipole_number_init=3)
        self.add_item(x_init=50, y_init=0, dipole_number_init=3)

    def add_item(self, dipole_number_init=3, dipole_spread_init=5, x_init=0, y_init=0):
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
        dipole_number = ValueInput("Dipole number", min_val=1, max_val=10, init_val=dipole_number_init)
        dipole_number.value_changed.connect(self.value_changed)
        vbox.addWidget(dipole_number)

        dipole_spread = FloatValueInput("Dipole spread", min_val=0.01, max_val=float("inf"), init_val=dipole_spread_init, step=0.1)
        dipole_spread.value_changed.connect(self.value_changed)
        vbox.addWidget(dipole_spread)

        position = PositionInput(x_init=x_init, y_init=y_init)
        position.value_changed.connect(self.value_changed)
        vbox.addWidget(position)


        vbox.addStretch()
        vbox.setSpacing(global_small_spacing)
        item.setLayout(vbox)
        self.vbox.insertWidget(self.vbox.count() - 1, item)

        self.items.append(item)
        self.items_counter += 1
        self.value_changed.emit()

    def remove_item(self, item):
        if self.number_of_items() <= 2:
            return

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
            position = item.layout().itemAt(4).widget().get_value()

            antennas.append(Antenna(index, name, position, dipole_number, dipole_distance))

        return antennas

    def update_position(self, index, position):
        filtered = list(filter(lambda item: item.layout().itemAt(0).widget().text() == index, self.items))
        assert len(filtered) == 1

        filtered[0].layout().itemAt(4).widget().set_value(position)

    def number_of_items(self):
        return len(self.items)