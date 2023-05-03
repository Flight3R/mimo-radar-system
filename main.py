import sys

from PyQt6.QtWidgets import *

from widgets.canvasBox import CanvasBox
from widgets.parametersBox import ParametersBox
from widgets.resultsBox import ResultsBox


def set_enabled_childrens(container, value):
    for child in container.children():
        if isinstance(child, QWidget):
            child.setEnabled(value)
            set_enabled_childrens(child, value)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("MIMO object radar simulator")
        self.resize(1200, 700)

        layout = QHBoxLayout()

        self.parameters_box = ParametersBox()
        self.parameters_box.value_changed.connect(self.repaint_canvas)
        layout.addWidget(self.parameters_box)
        layout.setStretchFactor(self.parameters_box, 3)

        self.canvas_box = CanvasBox(self.parameters_box.update_position)
        layout.addWidget(self.canvas_box)
        layout.setStretchFactor(self.canvas_box, 4)

        self.results_box = ResultsBox()
        self.results_box.settings_changed.connect(self.repaint_canvas)
        self.results_box.run_simulation.connect(self.run_simulation)
        self.results_box.back_to_edit.connect(self.back_to_edit)
        layout.addWidget(self.results_box)
        layout.setStretchFactor(self.results_box, 3)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.repaint_canvas()

    def repaint_canvas(self):
        object, antennas, transmitters = self.parameters_box.get_data()
        settings = self.results_box.drawing_settings.get_settings()
        self.canvas_box.repaint_canvas(object, antennas, transmitters, settings)

    def run_simulation(self):
        set_enabled_childrens(self.parameters_box, False)
        set_enabled_childrens(self.canvas_box, False)

    def back_to_edit(self):
        set_enabled_childrens(self.parameters_box, True)
        set_enabled_childrens(self.canvas_box, True)


app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()
