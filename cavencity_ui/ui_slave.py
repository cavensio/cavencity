from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QSlider, QProgressBar, QHBoxLayout, QFormLayout, \
    QLabel, QCheckBox, QLCDNumber


class Slave(QGroupBox):

    def __init__(self, title):
        super().__init__(title)

        speedSlider = QSlider()
        # speedSlider.setTickInterval(1)
        # speedSlider.setSingleStep(1)
        speedSlider.setSingleStep(1)
        speedSlider.setMaximum(5)

        speedStatus = QProgressBar()
        speedStatus.setOrientation(Qt.Vertical)

        hbox = QHBoxLayout()
        hbox.addWidget(speedSlider)
        hbox.addWidget(speedStatus)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addWidget(QLabel('Fan speed'))
        vbox.addLayout(hbox)

        self.uptime = QLCDNumber()
        self.uptime.setMinimumWidth(100)
        self.uptime.setFrameStyle(QLCDNumber.Flat)
        self.uptime.setSegmentStyle(QLCDNumber.Flat)
        palette = self.uptime.palette()

        # foreground color
        palette.setColor(palette.WindowText, QColor(80, 200, 80))
        # background color
        palette.setColor(palette.Background, QColor(0, 170, 255))
        # "light" border
        palette.setColor(palette.Light, QColor(255, 0, 0))
        # "dark" border
        palette.setColor(palette.Dark, QColor(0, 255, 0))

        # set the palette
        self.uptime.setPalette(palette)

        self.counter = QLabel()
        self.counter.setMinimumWidth(100)

        form = QFormLayout()
        form.addRow(QLabel('State:'), QLabel('Online'))
        form.addRow(QLabel('Uptime:'), self.uptime)
        form.addRow(QLabel('Counter:'), self.counter)
        form.addRow(QLabel('Damper:'), QCheckBox())
        # form.addRow(vbox)

        hbox = QHBoxLayout()
        hbox.addLayout(form)
        hbox.addLayout(vbox)

        self.setLayout(hbox)

    def update_state(self, online, uptime_seconds, reply_counter):
        pass

    def setUptime(self, seconds):
        if seconds >= 86400:
            uptime = '%sd %sh' % (int(seconds / 86400), int(seconds % 86400 / 3600))
        elif seconds >= 3600:
            uptime = '%sh %sm' % (int(seconds / 3600), int(seconds % 3600 / 60))
        elif seconds >= 60:
            uptime = '%sm %ss' % (int(seconds / 60), int(seconds % 60))
        else:
            uptime = '%ss' % seconds

        # print(seconds)
        # self.uptime.setText(uptime)
        self.uptime.display('%s' % int(seconds))

    def setCounter(self, counter):
        self.counter.setText('%s' % counter)
