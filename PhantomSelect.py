# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PhantomSelect.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Wid_PhantomSelect(object):
    def setupUi(self, Wid_PhantomSelect):
        Wid_PhantomSelect.setObjectName("Wid_PhantomSelect")
        Wid_PhantomSelect.resize(647, 580)
        Wid_PhantomSelect.setToolTipDuration(-1)
        self.gridLayout = QtWidgets.QGridLayout(Wid_PhantomSelect)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton = QtWidgets.QPushButton(Wid_PhantomSelect)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 1, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.frame_SelectPhantom = QtWidgets.QFrame(Wid_PhantomSelect)
        self.frame_SelectPhantom.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_SelectPhantom.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_SelectPhantom.setObjectName("frame_SelectPhantom")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_SelectPhantom)
        self.verticalLayout.setObjectName("verticalLayout")
        self.ListWid_SelectPhantom = QtWidgets.QListWidget(self.frame_SelectPhantom)
        self.ListWid_SelectPhantom.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.ListWid_SelectPhantom.setObjectName("ListWid_SelectPhantom")
        self.verticalLayout.addWidget(self.ListWid_SelectPhantom)
        self.gridLayout.addWidget(self.frame_SelectPhantom, 0, 0, 1, 2)

        self.retranslateUi(Wid_PhantomSelect)
        QtCore.QMetaObject.connectSlotsByName(Wid_PhantomSelect)

    def retranslateUi(self, Wid_PhantomSelect):
        _translate = QtCore.QCoreApplication.translate
        Wid_PhantomSelect.setWindowTitle(_translate("Wid_PhantomSelect", "Phantom Selection Window"))
        self.pushButton.setText(_translate("Wid_PhantomSelect", "Schließen"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Wid_PhantomSelect = QtWidgets.QWidget()
    ui = Ui_Wid_PhantomSelect()
    ui.setupUi(Wid_PhantomSelect)
    Wid_PhantomSelect.show()
    sys.exit(app.exec_())

