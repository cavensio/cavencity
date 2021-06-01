from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QFormLayout, QGroupBox, QCheckBox, QVBoxLayout

from mcu_master_states import SlaveActualState
from ui.CaveCounter import CaveCounter
from ui.CaveSlider import CaveSlider
from ui.ui_utils import format_uptime


class CaveSlave(QGroupBox):
    fanLevelChanged = pyqtSignal(int)
    lightLevelChanged = pyqtSignal(int)

    def __init__(self, alias: str):
        super().__init__(alias)

        self._state_label = QLabel()
        self._uptime_label = QLabel()
        self._latency_label = QLabel()
        self._errors_label = QLabel()
        self._count_lcdnumber = CaveCounter()
        self._damper_checkbox = QCheckBox()

        self._fan_slider = CaveSlider('Fan speed')
        self._fan_slider.valueChanged.connect(self.fanLevelChanged)

        self._light_slider = CaveSlider('Light', max_value=100)
        self._light_slider.valueChanged.connect(self.lightLevelChanged)

        form = QFormLayout()
        form.addRow(QLabel('State:'), self._state_label)
        form.addRow(QLabel('Uptime:'), self._uptime_label)
        form.addRow(QLabel('Latency:'), self._latency_label)
        form.addRow(QLabel('Errors:'), self._errors_label)
        form.addRow(QLabel('Requests:'))
        form.addRow(self._count_lcdnumber)
        form.addRow(QLabel('Damper:'), self._damper_checkbox)

        hbox = QHBoxLayout()
        hbox.addWidget(self._fan_slider)
        hbox.addWidget(self._light_slider)

        vbox = QVBoxLayout()
        vbox.addLayout(form)
        vbox.addLayout(hbox)
        vbox.addStretch(1)
        self.setLayout(vbox)

    def updateState(self, actual_state: SlaveActualState):
        self._latency_label.setText(f'{actual_state.latency}μs')
        self._errors_label.setText(f'{actual_state.errors}')
        self._count_lcdnumber.setValue(actual_state.counter, actual_state.online)

        self._fan_slider.setActualValue(actual_state.fan_level)
        self._light_slider.setActualValue(actual_state.light_level)

        if actual_state.online:
            self._state_label.setText('Online')
            self._uptime_label.setText(format_uptime(actual_state.uptime))
        else:
            self._state_label.setText('Offline')
