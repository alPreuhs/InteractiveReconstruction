from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from test import Ui_Dialog
from test1window import Ui_test1window

class testwindow(Ui_test1window):
    def __init__(self, dialog):
        Ui_test1window.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(dialog)
        #testing

class FirstGuiProgram(Ui_Dialog):
    def __init__(self, dialog):
        Ui_Dialog.__init__(self)
        self.setupUi(dialog)
        self.pushButton.clicked.connect(self.myfunction)

    def myfunction(self):
        window = testwindow(self)
        window.show()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    prog = FirstGuiProgram(dialog)
    dialog.show()
    sys.exit(app.exec_())
