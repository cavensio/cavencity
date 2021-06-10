from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLabel, QFormLayout, QGroupBox, QCheckBox

from mcu_master_states import MasterActualState
from ui.CaveCounter import CaveCounter
from ui.ui_utils import format_uptime, format_micros


class CaveMaster(QGroupBox):
    backlightChanged = pyqtSignal(int)

    def __init__(self):
        super().__init__('Master')
        self._state_label = QLabel()
        self._uptime_label = QLabel()
        self._count_lcdnumber = CaveCounter()
        self._latency_label = QLabel()

        form = QFormLayout()
        form.addRow(QLabel('State:'), self._state_label)
        form.addRow(QLabel('Uptime:'), self._uptime_label)
        form.addRow(QLabel('Latency:'), self._latency_label)
        form.addRow(QLabel('Errors:'))
        form.addRow(QLabel('Requests:'))
        form.addRow(self._count_lcdnumber)
        form.addRow(QLabel('Backlight:'), QCheckBox())

        self.setLayout(form)

    def update_state(self, actual_state: MasterActualState):
        if actual_state.online:
            self._state_label.setText('Online')
            self._uptime_label.setText(format_uptime(actual_state.uptime))
        else:
            self._state_label.setText('Offline')

        self._count_lcdnumber.set_value(actual_state.counter)
        self._latency_label.setText(format_micros(actual_state.latency))
