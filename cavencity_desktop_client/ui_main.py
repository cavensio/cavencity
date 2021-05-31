from functools import partial

from PyQt5.QtCore import QTimer, pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMainWindow, QMenu, QStatusBar, QLabel, QHBoxLayout, QWidget, QMessageBox, \
    QFormLayout, QGroupBox, QCheckBox, QVBoxLayout

from mcu_master_states import MasterException
from model import Model
from ui_counter import CaveCounter
from ui_slave import CaveSlave
from ui_slider import CaveSlider
from ui_utils import format_uptime


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._model = Model()
        self.setWindowTitle('Cavencity')

        icon = QIcon('cavencity.ico')
        self.setWindowIcon(icon)

        self.setMinimumSize(400, 600)
        self.__create_com_port_menu()
        self.__create_status_bar()
        self.__misc()

        try:
            self._model.load()
            if self._model.master_port:
                self.__update_master_port_label()
            self.__start_thread()
        except MasterException as e:
            QMessageBox.warning(self, 'Master controller offline', e.message, buttons=QMessageBox.Ok)

    def __create_com_port_menu(self):
        self.com_port_menu = QMenu('&Master port', self)
        self.com_port_menu.aboutToShow.connect(self.__on_com_port_menu_about_to_show)

        self.menuBar().addMenu(self.com_port_menu)
        self.setStatusBar(QStatusBar(self))

    @pyqtSlot()
    def __on_com_port_menu_about_to_show(self):
        self.com_port_menu.clear()
        actions = []
        ports = self._model.list_ports()
        for port in ports:
            action = QAction(port.device, self)
            if port.device == self._model.master_port:
                action.setCheckable(True)
                action.setChecked(True)
            action.triggered.connect(partial(self.__on_master_port_selected, port.device))
            actions.append(action)
        if not ports:
            action = QAction('Empty', self)
            action.setEnabled(False)
            actions.append(action)

        self.com_port_menu.addActions(actions)

    @pyqtSlot(str)
    def __on_master_port_selected(self, port):
        self.statusBar().showMessage(f'{port} selected', 5000)
        self._model.master_port = port
        self.__update_master_port_label()

    def __create_status_bar(self):
        self._master_port_label = QLabel('Master port')

        self.statusBar().addPermanentWidget(self._master_port_label)
        self.__update_master_port_label()

    def __update_master_port_label(self):
        self._master_port_label.setText(f'Master port: {self._model.master_port}')

    def __create_master_panel(self) -> QGroupBox:
        self._master_state_label = QLabel('Online')
        self._master_uptime_label = QLabel()

        self._master_count_lcdnumber = CaveCounter()

        groupbox = QGroupBox('Master')
        form = QFormLayout()
        form.addRow(QLabel('State:'), self._master_state_label)
        form.addRow(QLabel('Uptime:'), self._master_uptime_label)
        form.addRow(QLabel('Latency:'))
        form.addRow(QLabel('Errors:'))
        form.addRow(QLabel('Requests:'))
        form.addRow(self._master_count_lcdnumber)
        form.addRow(QLabel('Backlight:'), QCheckBox())

        groupbox.setLayout(form)
        return groupbox

    @pyqtSlot(int)
    def __on_slave1_fan_level_changed(self, value: int):
        self._model.master_input_state.slave1_fan_level = value

    @pyqtSlot(int)
    def __on_slave1_light_changed(self, value: int):
        self._model.master_input_state.slave1_light_level = value

    @pyqtSlot(int)
    def __on_slave2_fan_level_changed(self, value: int):
        self._model.master_input_state.slave2_fan_level = value

    @pyqtSlot(int)
    def __on_slave2_light_changed(self, value: int):
        self._model.master_input_state.slave2_light_level = value

    def __misc(self):
        layout = QHBoxLayout()

        layout.addWidget(self.__create_master_panel())
        layout.addWidget(CaveSlave(self._model.slave1_alias))
        layout.addWidget(CaveSlave(self._model.slave2_alias))


        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def __start_thread(self):
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.__thread_tick)
        self.timer.start()

    def __thread_tick(self):
        self._model.tick()
        state = self._model.master_output_state

        self._master_uptime_label.setText(format_uptime(state.master_uptime))
        self._master_count_lcdnumber.setValue(state.master_counter)

        # self._slave1_count_lcdnumber.setValue(state.slave1_counter, state.slave1_online)
        # self._slave2_count_lcdnumber.setValue(state.slave2_counter, state.slave2_online)
        #
        # self._slave1_fan_slider.setActualValue(state.slave1_fan_level)
        # self._slave2_fan_slider.setActualValue(state.slave2_fan_level)
        #
        # self._slave1_latency_label.setText(f'{state.slave1_latency}μs')
        # self._slave2_latency_label.setText(f'{state.slave2_latency}μs')
        #
        # self._slave1_errors_label.setText(f'{state.slave1_errors}')
        # self._slave2_errors_label.setText(f'{state.slave2_errors}')
        #
        # if state.slave1_online:
        #     self._slave1_state_label.setText('Online')
        #     self._slave1_uptime_label.setText(format_uptime(state.slave1_uptime))
        # else:
        #     self._slave1_state_label.setText('Offline')
        #
        # if state.slave2_online:
        #     self._slave2_state_label.setText('Online')
        #     self._slave2_uptime_label.setText(format_uptime(state.slave2_uptime))
        # else:
        #     self._slave2_state_label.setText('Offline')
