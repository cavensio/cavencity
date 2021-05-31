from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLabel, QFormLayout, QGroupBox, QCheckBox

from mcu_master_states import MasterActualState
from CaveUi.CaveCounter import CaveCounter
from CaveUi.ui_utils import format_uptime


class CaveMaster(QGroupBox):
    backlightChanged = pyqtSignal(int)

    def __init__(self):
        super().__init__('Master')
        self.state_label = QLabel('Online')
        self.uptime_label = QLabel()
        self.count_lcdnumber = CaveCounter()

        form = QFormLayout()
        form.addRow(QLabel('State:'), self.state_label)
        form.addRow(QLabel('Uptime:'), self.uptime_label)
        form.addRow(QLabel('Latency:'))
        form.addRow(QLabel('Errors:'))
        form.addRow(QLabel('Requests:'))
        form.addRow(self.count_lcdnumber)
        form.addRow(QLabel('Backlight:'), QCheckBox())

        self.setLayout(form)

    def updateState(self, actual_state: MasterActualState):
        self.uptime_label.setText(format_uptime(actual_state.uptime))
        self.count_lcdnumber.setValue(actual_state.counter)
