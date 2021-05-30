import sys

from PyQt5.QtWidgets import QApplication

from ui_main import MainWindow

old_excepthook = sys.excepthook


def exception_hook(exctype, value, traceback):
    old_excepthook(exctype, value, traceback)
    sys.exit(1)

sys.excepthook = exception_hook

try:
    from PyQt5.QtWinExtras import QtWin

    app_id = 'cavensio.cavencity'
    QtWin.setCurrentProcessExplicitAppUserModelID(app_id)
except ImportError:
    pass

app = QApplication(sys.argv)
with open('cavencio.qss') as f:
    app.setStyleSheet(f.read())

window = MainWindow()
window.show()

app.exec()
