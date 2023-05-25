import string
from threading import Thread

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QDialog, QLabel, QVBoxLayout, QProgressBar

from backend.api import create_heatmap
from dto.antenna import Antenna
from dto.simulation_settings import SimulationSettings
from dto.transmitter import Transmitter


class HeatmapWindow(QDialog):
    update_progressbar = pyqtSignal([int, int])
    finish_progressbar = pyqtSignal(str)

    def __init__(self, antennas: list[Antenna], transmitter: list[Transmitter],
                 simulation_settings: SimulationSettings, edge_length: float, resolution: float):
        super(HeatmapWindow, self).__init__()
        self.update_progressbar.connect(self.progressbar_step)
        self.finish_progressbar.connect(self.progressbar_end)

        self.setWindowTitle("Heatmap")

        self.setLayout(QVBoxLayout())

        self.label = QLabel("Generating heatmap")
        self.layout().addWidget(self.label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedWidth(300)
        self.layout().addWidget(self.progress_bar)

        thread = Thread(target=create_heatmap,
                        args=(antennas, transmitter, simulation_settings, edge_length, resolution, self.update_progressbar, self.finish_progressbar))
        thread.start()

    def progressbar_step(self, complexity, iterator):
        self.setWindowTitle(f'Heatmap complexity={complexity}')
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(complexity)
        self.progress_bar.setValue(iterator)
        self.label.setText("Generating layout" + str((iterator % 3 + 1) * "."))

    def progressbar_end(self, filename):
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.layout().removeWidget(self.progress_bar)
        self.progress_bar.deleteLater()

        self.label.setText("")
        self.label.setPixmap(QPixmap(filename))
