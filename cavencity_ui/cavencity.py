import sys

from PyQt5.QtWidgets import QApplication

from model import Model
from ui_main import MainWindow

old_excepthook = sys.excepthook


def exception_hook(exctype, value, traceback):
    old_excepthook(exctype, value, traceback)
    sys.exit(1)


sys.excepthook = exception_hook

app = QApplication(sys.argv)

model = Model()

window = MainWindow(model)
window.show()

app.exec()
