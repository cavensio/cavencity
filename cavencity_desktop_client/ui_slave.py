from PyQt5.QtWidgets import QLabel, QHBoxLayout, QFormLayout, QGroupBox, QCheckBox, QVBoxLayout

from ui_counter import CaveCounter
from ui_slider import CaveSlider


class CaveSlave(QGroupBox):
    def __init__(self, alias: str):
        super().__init__(alias)

        self.state_label = QLabel()
        self.uptime_label = QLabel()
        self.latency_label = QLabel()
        self.errors_label = QLabel()
        self.count_lcdnumber = CaveCounter()
        self.damper_checkbox = QCheckBox()

        self.fan_slider = CaveSlider('Fan speed')
        # fan_slider.valueChanged.connect(self.__on_slave1_fan_level_changed)
        self.light_slider = CaveSlider('Light', max_value=100)
        # light_slider.valueChanged.connect(self.__on_slave1_light_changed)

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

        def updateState(self):
            pass
