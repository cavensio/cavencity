from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QProgressBar, QSlider, QVBoxLayout, QLabel, QFrame


class CaveSlider(QWidget):
    valueChanged = pyqtSignal(int)

    def __init__(self, label: str, max_value: int = 5):
        super().__init__()
        self._target_value: int = 0
        self._actual_value: int = 0

        slider = QSlider()
        # slider.setSingleStep(1)
        # slider.setPageStep(1)
        slider.setMaximum(max_value)
        slider.setTickInterval(1)
        slider.setTickPosition(QSlider.TicksBothSides)
        slider.setFixedHeight(200)
        slider.setFixedWidth(25)
        slider.valueChanged.connect(self.valueChanged)
        self._slider = slider

        status = QProgressBar()
        status.setFixedHeight(200)
        status.setFixedWidth(25)
        status.setMaximum(max_value)
        status.setTextVisible(False)
        status.setOrientation(Qt.Vertical)
        self._status = status

        hbox = QHBoxLayout()
        hbox.addWidget(slider)
        hbox.addWidget(status)

        label = QLabel(label)
        label.setAlignment(Qt.AlignCenter)
        vbox = QVBoxLayout()
        vbox.addWidget(label)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def setActualValue(self, value) -> None:
        if value != self._actual_value:
            self._status.setValue(value)
