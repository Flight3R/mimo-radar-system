from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QRadioButton, QLabel


class RadioButtons(QWidget):
    value_changed = pyqtSignal()

    def __init__(self, label_text, options):
        super().__init__()

        self.hbox = QHBoxLayout()
        self.hbox.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.hbox.setContentsMargins(0, 0, 4, 4)
        self.hbox.setSpacing(0)

        self.label = QLabel(label_text + ":  ")
        self.hbox.addWidget(self.label)

        self.buttons = []
        for option in options:
            button = QRadioButton(option)
            button.toggled.connect(self.value_changed)
            self.buttons.append(button)
            self.hbox.addWidget(button)

            if option == options[0]:
                button.setChecked(True)

        self.setLayout(self.hbox)


    def get_value(self):
        for button in self.buttons:
            if button.isChecked():
                return button.text()
        return None