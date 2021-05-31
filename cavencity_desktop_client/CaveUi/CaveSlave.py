from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QFormLayout, QGroupBox, QCheckBox, QVBoxLayout

from mcu_master_states import SlaveActualState
from CaveUi.CaveCounter import CaveCounter
from CaveUi.CaveSlider import CaveSlider
from CaveUi.ui_utils import format_uptime


class CaveSlave(QGroupBox):
    fanLevelChanged = pyqtSignal(int)
    lightLevelChanged = pyqtSignal(int)

    def __init__(self, alias: str):
        super().__init__(alias)

        self.state_label = QLabel()
        self.uptime_label = QLabel()
        self.latency_label = QLabel()
        self.errors_label = QLabel()
        self.count_lcdnumber = CaveCounter()
        self.damper_checkbox = QCheckBox()

        self.fan_slider = CaveSlider('Fan speed')
        self.fan_slider.valueChanged.connect(self.fanLevelChanged)

        self.light_slider = CaveSlider('Light', max_value=100)
        self.light_slider.valueChanged.connect(self.lightLevelChanged)

        form = QFormLayout()
        form.addRow(QLabel('State:'), self.state_label)
        form.addRow(QLabel('Uptime:'), self.uptime_label)
        form.addRow(QLabel('Latency:'), self.latency_label)
        form.addRow(QLabel('Errors:'), self.errors_label)
        form.addRow(QLabel('Requests:'))
        form.addRow(self.count_lcdnumber)
        form.addRow(QLabel('Damper:'), self.damper_checkbox)

        hbox = QHBoxLayout()
        hbox.addWidget(self.fan_slider)
        hbox.addWidget(self.light_slider)

        vbox = QVBoxLayout()
        vbox.addLayout(form)
        vbox.addLayout(hbox)
        vbox.addStretch(1)
        self.setLayout(vbox)

    def updateState(self, actual_state: SlaveActualState):
        self.latency_label.setText(f'{actual_state.latency}μs')
        self.errors_label.setText(f'{actual_state.errors}')
        self.count_lcdnumber.setValue(actual_state.counter, actual_state.online)

        self.fan_slider.setActualValue(actual_state.fan_level)
        self.light_slider.setActualValue(actual_state.light_level)

        if actual_state.online:
            self.state_label.setText('Online')
            self.uptime_label.setText(format_uptime(actual_state.uptime))
        else:
            self.state_label.setText('Offline')
