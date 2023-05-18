import sys

from PyQt6.QtWidgets import *

from backend.api import detect, PositionIsNoneError
from dto.object import Object
from widgets.canvas_panel.canvas_panel import CanvasPanel
from widgets.left_panel.left_panel import LeftPanel
from widgets.right_panel.heatmap_window import HeatmapWindow
from widgets.right_panel.right_panel import RightPanel


def set_enabled_childrens(container, value):
    for child in container.children():
        if isinstance(child, QWidget):
            child.setEnabled(value)
            set_enabled_childrens(child, value)


class MainWindow(QMainWindow):
    detected_position = None

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("MIMO object radar simulator")
        self.resize(1200, 700)

        layout = QHBoxLayout()

        self.left_panel = LeftPanel()
        self.left_panel.value_changed.connect(self.repaint_canvas)
        layout.addWidget(self.left_panel)
        layout.setStretchFactor(self.left_panel, 3)

        self.canvas_panel = CanvasPanel(self.left_panel.update_position)
        layout.addWidget(self.canvas_panel)
        layout.setStretchFactor(self.canvas_panel, 4)

        self.right_panel = RightPanel()
        self.right_panel.drawing_settings_changed.connect(self.repaint_canvas)
        self.right_panel.run_simulation.connect(self.run_simulation)
        self.right_panel.back_to_edit.connect(self.back_to_edit)
        self.right_panel.generate_heatmap.connect(self.generate_heatmap)
        layout.addWidget(self.right_panel)
        layout.setStretchFactor(self.right_panel, 3)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.repaint_canvas()

    def repaint_canvas(self):
        real_object, antennas, transmitters = self.left_panel.get_data()
        detected_object = Object("detected object", real_object.name + "'", self.detected_position)
        settings = self.right_panel.drawing_settings.get_settings()
        self.canvas_panel.repaint_canvas(real_object, detected_object, antennas, transmitters, settings)

    def set_enable_settings(self, value):
        set_enabled_childrens(self.left_panel, value)
        set_enabled_childrens(self.right_panel.simulation_settings, value)
        self.canvas_panel.set_points_movable(value)

    def back_to_edit(self):
        self.set_enable_settings(True)
        self.detected_position = None
        self.repaint_canvas()
        self.right_panel.results.clear()

    def run_simulation(self):
        object, antennas, transmitters = self.left_panel.get_data()
        simulation_settings = self.right_panel.simulation_settings.get_settings()

        try:
            self.detected_position = detect(object, antennas, transmitters, simulation_settings)
            self.right_panel.results.set_results(object.position, self.detected_position)
            self.repaint_canvas()
            self.set_enable_settings(False)
        except PositionIsNoneError:
            self.right_panel.results.show_error("No object was detected")
        except Exception as e:
            self.right_panel.results.show_error("Some error occurred")
            raise e

    def generate_heatmap(self):
        object, antennas, transmitters = self.left_panel.get_data()
        simulation_settings = self.right_panel.simulation_settings.get_settings()
        edge_length, resolution = self.right_panel.heatmap_box.get_settings()

        heatmap_window = HeatmapWindow(antennas, transmitters, simulation_settings, edge_length, resolution)
        heatmap_window.exec()


app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()
