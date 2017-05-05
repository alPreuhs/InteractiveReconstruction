from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from test import Ui_Dialog
from test1window import Ui_test1window

class testwindow(Ui_test1window):
    def __init__(self, widget):
        Ui_test1window.__init__(self)
        self.setupUi(widget)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QMainWindow()
    prog = testwindow(dialog)
    dialog.show()
    sys.exit(app.exec_())
