from functools import partial

from PyQt5.QtCore import QTimer, pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMainWindow, QMenu, QStatusBar, QLabel, QHBoxLayout, QWidget, QMessageBox

from ui.CaveMaster import CaveMaster
from mcu_master_states import MasterException
from model import Model
from ui.CaveSlave import CaveSlave


class CaveMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._model = Model()
        self.setWindowTitle('Cavencity')

        icon = QIcon('../cavencity.ico')
        self.setWindowIcon(icon)

        self.setMinimumSize(400, 600)
        self._create_com_port_menu()
        self._create_status_bar()
        self._create_master_slave_panels()

        try:
            self._model.load()
            if self._model.master_port:
                self._update_master_port_label()
            self._start_thread()
        except MasterException as e:
            QMessageBox.warning(self, 'Master controller offline', e.message, buttons=QMessageBox.Ok)

    def _create_com_port_menu(self):
        self.com_port_menu = QMenu('&Master port', self)
        self.com_port_menu.aboutToShow.connect(self._on_com_port_menu_about_to_show)

        self.menuBar().addMenu(self.com_port_menu)
        self.setStatusBar(QStatusBar(self))

    @pyqtSlot()
    def _on_com_port_menu_about_to_show(self):
        self.com_port_menu.clear()
        actions = []
        ports = self._model.list_ports()
        for port in ports:
            action = QAction(port.device, self)
            if port.device == self._model.master_port:
                action.setCheckable(True)
                action.setChecked(True)
            action.triggered.connect(partial(self._on_master_port_selected, port.device))
            actions.append(action)
        if not ports:
            action = QAction('Empty', self)
            action.setEnabled(False)
            actions.append(action)

        self.com_port_menu.addActions(actions)

    @pyqtSlot(str)
    def _on_master_port_selected(self, port):
        self.statusBar().showMessage(f'{port} selected', 5000)
        self._model.master_port = port
        self._update_master_port_label()

    def _create_status_bar(self):
        self._master_port_label = QLabel('Master port')

        self.statusBar().addPermanentWidget(self._master_port_label)
        self._update_master_port_label()

    def _update_master_port_label(self):
        self._master_port_label.setText(f'Master port: {self._model.master_port}')

    @pyqtSlot(int)
    def _on_slave1_fan_level_changed(self, value: int):
        self._model.target_state.slaveStates[0].fan_level = value

    @pyqtSlot(int)
    def _on_slave1_light_changed(self, value: int):
        self._model.target_state.slaveStates[0].light_level = value

    @pyqtSlot(int)
    def _on_slave2_fan_level_changed(self, value: int):
        self._model.target_state.slaveStates[1].fan_level = value

    @pyqtSlot(int)
    def _on_slave2_light_changed(self, value: int):
        self._model.target_state.slaveStates[1].light_level = value

    def _create_master_slave_panels(self):
        layout = QHBoxLayout()
        self.cave_master = CaveMaster()
        self.cave_slave1 = CaveSlave(self._model.slave1_alias)
        self.cave_slave2 = CaveSlave(self._model.slave2_alias)

        self.cave_slave1.fanLevelChanged.connect(self._on_slave1_fan_level_changed)
        self.cave_slave2.fanLevelChanged.connect(self._on_slave2_fan_level_changed)

        self.cave_slave1.lightLevelChanged.connect(self._on_slave1_light_changed)
        self.cave_slave2.lightLevelChanged.connect(self._on_slave2_light_changed)

        layout.addWidget(self.cave_master)
        layout.addWidget(self.cave_slave1)
        layout.addWidget(self.cave_slave2)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def _start_thread(self):
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self._thread_tick)
        self.timer.start()

    def _thread_tick(self):
        self._model.tick()
        self.cave_master.update_state(self._model.actual_state.masterState)
        self.cave_slave1.update_date(self._model.actual_state.slaveStates[0])
        self.cave_slave2.update_date(self._model.actual_state.slaveStates[1])
