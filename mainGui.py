import sys

from PyQt6.QtWidgets import *

from widgets.canvasBox import CanvasBox
from widgets.parametersBox import ParametersBox
from widgets.resultsBox import ResultsBox


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("MIMO object radar simulator")
        self.resize(1200, 700)

        layout = QHBoxLayout()

        self.parameters_box = ParametersBox()
        self.parameters_box.value_changed.connect(self.repaint_canvas)
        self.parameters_box.run_simulation.connect(self.run_simulation)
        layout.addWidget(self.parameters_box)
        layout.setStretchFactor(self.parameters_box, 3)

        self.canvas_box = CanvasBox()
        layout.addWidget(self.canvas_box)
        layout.setStretchFactor(self.canvas_box, 4)

        self.results_box = ResultsBox()
        self.results_box.value_changed.connect(self.repaint_canvas)
        layout.addWidget(self.results_box)
        layout.setStretchFactor(self.results_box, 3)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def repaint_canvas(self):
        object, antennas, transmitters = self.parameters_box.get_data()
        settings = self.results_box.get_settings()

        self.canvas_box.canvas.repaint_canvas(object, antennas, transmitters, settings)

    def run_simulation(self):
        self.set_enabled_childrens(self.parameters_box, False)

    def set_enabled_childrens(self, container, value):
        for child in container.children():
            if isinstance(child, QWidget):
                child.setEnabled(False)
                self.set_enabled_childrens(child, value)




app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()
