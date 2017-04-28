# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(912, 517)
        self.GV_phantom = QtWidgets.QGraphicsView(Dialog)
        self.GV_phantom.setGeometry(QtCore.QRect(200, 50, 256, 192))
        self.GV_phantom.setObjectName("GV_phantom")
        self.vSlider_1 = QtWidgets.QSlider(Dialog)
        self.vSlider_1.setGeometry(QtCore.QRect(460, 60, 21, 191))
        self.vSlider_1.setOrientation(QtCore.Qt.Vertical)
        self.vSlider_1.setObjectName("vSlider_1")
        self.hSlider_1 = QtWidgets.QSlider(Dialog)
        self.hSlider_1.setGeometry(QtCore.QRect(200, 250, 261, 22))
        self.hSlider_1.setOrientation(QtCore.Qt.Horizontal)
        self.hSlider_1.setObjectName("hSlider_1")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(230, 20, 161, 20))
        self.label.setObjectName("label")
        self.sinogram = QtWidgets.QGraphicsView(Dialog)
        self.sinogram.setGeometry(QtCore.QRect(490, 50, 221, 192))
        self.sinogram.setObjectName("sinogram")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(570, 20, 59, 16))
        self.label_2.setObjectName("label_2")
        self.graphicsView = QtWidgets.QGraphicsView(Dialog)
        self.graphicsView.setGeometry(QtCore.QRect(360, 300, 256, 192))
        self.graphicsView.setObjectName("graphicsView")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(440, 270, 111, 16))
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(20, 130, 113, 41))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Dialog)
        self.hSlider_1.valueChanged['int'].connect(self.GV_phantom.invalidateScene)
        self.vSlider_1.sliderMoved['int'].connect(self.GV_phantom.invalidateScene)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "                 Phantom"))
        self.label_2.setText(_translate("Dialog", "Sinogram"))
        self.label_3.setText(_translate("Dialog", "Backprojection"))
        self.pushButton.setText(_translate("Dialog", "Select "))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

