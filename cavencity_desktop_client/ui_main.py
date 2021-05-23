from functools import partial

from PyQt5.QtWidgets import QAction, QMainWindow, QMenu, QStatusBar, QLabel, QHBoxLayout, QWidget
from PyQt5.QtGui import QIcon
from model import Model
from ui_slave import Slave

try:
    from PyQt5.QtWinExtras import QtWin

    app_id = 'cavensio.cavencity'
    QtWin.setCurrentProcessExplicitAppUserModelID(app_id)
except ImportError:
    pass


class MainWindow(QMainWindow):
    def __init__(self, model: Model):
        super().__init__()
        self.model = model
        self.setWindowTitle('Cavencity')

        icon = QIcon('cavencity.ico')
        self.setWindowIcon(icon)

        self.setMinimumSize(800, 600)

        self.selected_com_port = None
        self.__create_com_port_menu()
        self.__create_status_bar()
        self.__misc()

    def __create_com_port_menu(self):
        self.com_port_menu = QMenu('&Master port', self)
        self.com_port_menu.aboutToShow.connect(self.__populate_com_port_menu)
        self.menuBar().addMenu(self.com_port_menu)
        self.setStatusBar(QStatusBar(self))

    def __populate_com_port_menu(self):
        self.com_port_menu.clear()
        actions = []
        ports = self.model.list_ports()
        for port in ports:
            action = QAction(port.device, self)
            if port.device == self.model.master_port:
                action.setCheckable(True)
                action.setChecked(True)
            action.triggered.connect(partial(self.__select_com_port, port.device))
            actions.append(action)
        if not ports:
            action = QAction('Empty', self)
            action.setEnabled(False)
            actions.append(action)

        self.com_port_menu.addActions(actions)

    def __select_com_port(self, port):
        self.selected_com_port = port
        self.statusBar().showMessage(f'{port} selected', 5000)
        self.model.master_port = port
        self.__update_master_port_label()

    def __create_status_bar(self):
        self.selected_com_port_label = QLabel()
        self.statusBar().addPermanentWidget(self.selected_com_port_label)
        self.__update_master_port_label()

    def __update_master_port_label(self):
        self.selected_com_port_label.setText(f'Master port: {self.model.master_port}')

    def __misc(self):
        layout = QHBoxLayout()
        # layout.setContentsMargins(0, 0, 0, 0)
        # layout.setSpacing(0)

        # layout.addWidget(Dummy('green'))
        slave1 = Slave(self.model.slave1_alias)
        self.slave2 = Slave(self.model.slave2_alias)
        layout.addWidget(slave1)
        layout.addWidget(self.slave2)

        slave1.setDisabled(True)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def onMyToolBarButtonClick(self, s):
        print("click", s)

    def recurring_timer(self):
        global counter
        print(counter)
        # print(e)
        counter += 1
        self.slave2.setUptime(int(time.time() - startTime))
        self.slave2.setCounter(counter)
