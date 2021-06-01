import sys

from PyQt5.QtWidgets import QApplication

from ui import CaveMainWindow

old_excepthook = sys.excepthook


def exception_hook(exctype, value, traceback):
    old_excepthook(exctype, value, traceback)
    sys.exit(1)


sys.excepthook = exception_hook

try:
    from PyQt5.QtWinExtras import QtWin

    QtWin().setCurrentProcessExplicitAppUserModelID(id='cavensio.cavencity')
except ImportError:
    pass

app = QApplication(sys.argv)
with open('cavencio.qss') as f:
    app.setStyleSheet(f.read())

window = CaveMainWindow()
window.show()

app.exec()
