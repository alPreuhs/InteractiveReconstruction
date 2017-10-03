# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fanGUI_Project.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ReconstructionGUI(object):
    def setupUi(self, ReconstructionGUI):
        ReconstructionGUI.setObjectName("ReconstructionGUI")
        ReconstructionGUI.resize(932, 654)
        self.Reconstruction = QtWidgets.QWidget(ReconstructionGUI)
        self.Reconstruction.setObjectName("Reconstruction")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.Reconstruction)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_Phantom = QtWidgets.QLabel(self.Reconstruction)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_Phantom.setFont(font)
        self.label_Phantom.setObjectName("label_Phantom")
        self.gridLayout.addWidget(self.label_Phantom, 0, 1, 1, 1)
        self.label_Sino = QtWidgets.QLabel(self.Reconstruction)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_Sino.setFont(font)
        self.label_Sino.setObjectName("label_Sino")
        self.gridLayout.addWidget(self.label_Sino, 0, 4, 1, 1)
        self.label_Backproj = QtWidgets.QLabel(self.Reconstruction)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_Backproj.setFont(font)
        self.label_Backproj.setAutoFillBackground(True)
        self.label_Backproj.setObjectName("label_Backproj")
        self.gridLayout.addWidget(self.label_Backproj, 0, 7, 1, 1)
        self.pB_PhantomSelect = QtWidgets.QPushButton(self.Reconstruction)
        self.pB_PhantomSelect.setMaximumSize(QtCore.QSize(40, 500))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.pB_PhantomSelect.setFont(font)
        self.pB_PhantomSelect.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pB_PhantomSelect.setAutoDefault(False)
        self.pB_PhantomSelect.setObjectName("pB_PhantomSelect")
        self.gridLayout.addWidget(self.pB_PhantomSelect, 1, 0, 7, 1)
        self.vSlider_maxbeta = QtWidgets.QSlider(self.Reconstruction)
        self.vSlider_maxbeta.setOrientation(QtCore.Qt.Vertical)
        self.vSlider_maxbeta.setObjectName("vSlider_maxbeta")
        self.gridLayout.addWidget(self.vSlider_maxbeta, 1, 5, 1, 1)
        self.label_BackprojFFT = QtWidgets.QLabel(self.Reconstruction)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_BackprojFFT.setFont(font)
        self.label_BackprojFFT.setObjectName("label_BackprojFFT")
        self.gridLayout.addWidget(self.label_BackprojFFT, 6, 7, 1, 1)
        self.label_Sinogram = QtWidgets.QLabel(self.Reconstruction)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_Sinogram.setFont(font)
        self.label_Sinogram.setObjectName("label_Sinogram")
        self.gridLayout.addWidget(self.label_Sinogram, 6, 4, 1, 1)
        self.gV_Backproj_FFT = QtWidgets.QGraphicsView(self.Reconstruction)
        self.gV_Backproj_FFT.setObjectName("gV_Backproj_FFT")
        self.gridLayout.addWidget(self.gV_Backproj_FFT, 7, 7, 1, 1)
        self.label_PhantomFFT = QtWidgets.QLabel(self.Reconstruction)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_PhantomFFT.setFont(font)
        self.label_PhantomFFT.setObjectName("label_PhantomFFT")
        self.gridLayout.addWidget(self.label_PhantomFFT, 6, 1, 1, 1)
        self.gV_Backproj = QtWidgets.QGraphicsView(self.Reconstruction)
        self.gV_Backproj.setAutoFillBackground(False)
        self.gV_Backproj.setObjectName("gV_Backproj")
        self.gridLayout.addWidget(self.gV_Backproj, 1, 7, 1, 1)
        self.hSlider_deltabeta = QtWidgets.QSlider(self.Reconstruction)
        self.hSlider_deltabeta.setMaximum(180)
        self.hSlider_deltabeta.setOrientation(QtCore.Qt.Horizontal)
        self.hSlider_deltabeta.setObjectName("hSlider_deltabeta")
        self.gridLayout.addWidget(self.hSlider_deltabeta, 2, 4, 1, 1)
        self.gV_Phantom_FFT = QtWidgets.QGraphicsView(self.Reconstruction)
        self.gV_Phantom_FFT.setObjectName("gV_Phantom_FFT")
        self.gridLayout.addWidget(self.gV_Phantom_FFT, 7, 1, 1, 1)
        self.gV_SinogramFFT = QtWidgets.QGraphicsView(self.Reconstruction)
        self.gV_SinogramFFT.setObjectName("gV_SinogramFFT")
        self.gridLayout.addWidget(self.gV_SinogramFFT, 7, 4, 1, 1)
        self.gV_Phantom = QtWidgets.QGraphicsView(self.Reconstruction)
        self.gV_Phantom.setAutoFillBackground(False)
        self.gV_Phantom.setObjectName("gV_Phantom")
        self.gridLayout.addWidget(self.gV_Phantom, 1, 1, 1, 1)
        self.pB_Xray = QtWidgets.QPushButton(self.Reconstruction)
        self.pB_Xray.setMaximumSize(QtCore.QSize(40, 500))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.pB_Xray.setFont(font)
        self.pB_Xray.setObjectName("pB_Xray")
        self.gridLayout.addWidget(self.pB_Xray, 1, 2, 7, 1)
        self.pB_Reconstruction = QtWidgets.QPushButton(self.Reconstruction)
        self.pB_Reconstruction.setMaximumSize(QtCore.QSize(40, 500))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.pB_Reconstruction.setFont(font)
        self.pB_Reconstruction.setObjectName("pB_Reconstruction")
        self.gridLayout.addWidget(self.pB_Reconstruction, 1, 6, 7, 1)
        self.gV_Sinogram = QtWidgets.QGraphicsView(self.Reconstruction)
        self.gV_Sinogram.setAutoFillBackground(False)
        self.gV_Sinogram.setObjectName("gV_Sinogram")
        self.gridLayout.addWidget(self.gV_Sinogram, 1, 4, 1, 1)
        self.checkBox_ParkerWeigh = QtWidgets.QCheckBox(self.Reconstruction)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.checkBox_ParkerWeigh.setFont(font)
        self.checkBox_ParkerWeigh.setObjectName("checkBox_ParkerWeigh")
        self.gridLayout.addWidget(self.checkBox_ParkerWeigh, 4, 4, 1, 1)
        self.checkBox_RamLakFilter = QtWidgets.QCheckBox(self.Reconstruction)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.checkBox_RamLakFilter.setFont(font)
        self.checkBox_RamLakFilter.setObjectName("checkBox_RamLakFilter")
        self.gridLayout.addWidget(self.checkBox_RamLakFilter, 5, 4, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.gV_SinogramFFT.raise_()
        self.label_Sinogram.raise_()
        self.vSlider_maxbeta.raise_()
        self.hSlider_deltabeta.raise_()
        self.gV_Backproj.raise_()
        self.pB_Reconstruction.raise_()
        self.pB_Xray.raise_()
        self.pB_PhantomSelect.raise_()
        ReconstructionGUI.setCentralWidget(self.Reconstruction)
        self.menubar = QtWidgets.QMenuBar(ReconstructionGUI)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 932, 17))
        self.menubar.setObjectName("menubar")
        ReconstructionGUI.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ReconstructionGUI)
        self.statusbar.setObjectName("statusbar")
        ReconstructionGUI.setStatusBar(self.statusbar)

        self.retranslateUi(ReconstructionGUI)
        QtCore.QMetaObject.connectSlotsByName(ReconstructionGUI)

    def retranslateUi(self, ReconstructionGUI):
        _translate = QtCore.QCoreApplication.translate
        ReconstructionGUI.setWindowTitle(_translate("ReconstructionGUI", "Reconstruction"))
        self.label_Phantom.setText(_translate("ReconstructionGUI", "Phantom"))
        self.label_Sino.setText(_translate("ReconstructionGUI", "Sinogram"))
        self.label_Backproj.setText(_translate("ReconstructionGUI", "Back Projection"))
        self.pB_PhantomSelect.setText(_translate("ReconstructionGUI", "S\n"
"E\n"
"L\n"
"E\n"
"C\n"
"T\n"
"  \n"
"P\n"
"H\n"
"A\n"
"N\n"
"T\n"
"O\n"
"M"))
        self.label_BackprojFFT.setText(_translate("ReconstructionGUI", "Backprojection FFT"))
        self.label_Sinogram.setText(_translate("ReconstructionGUI", "Sinogram FFT"))
        self.label_PhantomFFT.setText(_translate("ReconstructionGUI", "Phantom FFT"))
        self.pB_Xray.setText(_translate("ReconstructionGUI", "X\n"
"\n"
"R\n"
"A\n"
"Y"))
        self.pB_Reconstruction.setText(_translate("ReconstructionGUI", "R\n"
"E\n"
"C\n"
"O\n"
"N\n"
"S\n"
"T\n"
"R\n"
"U\n"
"C\n"
"T\n"
"I\n"
"O\n"
"N"))
        self.checkBox_ParkerWeigh.setText(_translate("ReconstructionGUI", "Parker Weighting"))
        self.checkBox_RamLakFilter.setText(_translate("ReconstructionGUI", "RamLak Filtering"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ReconstructionGUI = QtWidgets.QMainWindow()
    ui = Ui_ReconstructionGUI()
    ui.setupUi(ReconstructionGUI)
    ReconstructionGUI.show()
    sys.exit(app.exec_())

