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
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.pB_videocapture = QtWidgets.QPushButton(self.Reconstruction)
        self.pB_videocapture.setMaximumSize(QtCore.QSize(40, 500))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pB_videocapture.setFont(font)
        self.pB_videocapture.setObjectName("pB_videocapture")
        self.gridLayout.addWidget(self.pB_videocapture, 4, 0, 1, 1)
        self.checkBox_cosine = QtWidgets.QCheckBox(self.Reconstruction)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.checkBox_cosine.setFont(font)
        self.checkBox_cosine.setObjectName("checkBox_cosine")
        self.gridLayout.addWidget(self.checkBox_cosine, 8, 4, 1, 1)
        self.gV_Backproj = QtWidgets.QGraphicsView(self.Reconstruction)
        self.gV_Backproj.setAutoFillBackground(False)
        self.gV_Backproj.setObjectName("gV_Backproj")
        self.gridLayout.addWidget(self.gV_Backproj, 4, 7, 1, 1)
        self.label_Phantom = QtWidgets.QLabel(self.Reconstruction)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_Phantom.setFont(font)
        self.label_Phantom.setObjectName("label_Phantom")
        self.gridLayout.addWidget(self.label_Phantom, 1, 1, 1, 1)
        self.label_Sinogram = QtWidgets.QLabel(self.Reconstruction)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_Sinogram.setFont(font)
        self.label_Sinogram.setObjectName("label_Sinogram")
        self.gridLayout.addWidget(self.label_Sinogram, 10, 4, 1, 1)
        self.label_BackprojFFT = QtWidgets.QLabel(self.Reconstruction)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_BackprojFFT.setFont(font)
        self.label_BackprojFFT.setObjectName("label_BackprojFFT")
        self.gridLayout.addWidget(self.label_BackprojFFT, 10, 7, 1, 1)
        self.label_Backproj = QtWidgets.QLabel(self.Reconstruction)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_Backproj.setFont(font)
        self.label_Backproj.setAutoFillBackground(True)
        self.label_Backproj.setObjectName("label_Backproj")
        self.gridLayout.addWidget(self.label_Backproj, 1, 7, 1, 1)
        self.label_PhantomFFT = QtWidgets.QLabel(self.Reconstruction)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_PhantomFFT.setFont(font)
        self.label_PhantomFFT.setObjectName("label_PhantomFFT")
        self.gridLayout.addWidget(self.label_PhantomFFT, 10, 1, 1, 1)
        self.gV_Backproj_FFT = QtWidgets.QGraphicsView(self.Reconstruction)
        self.gV_Backproj_FFT.setObjectName("gV_Backproj_FFT")
        self.gridLayout.addWidget(self.gV_Backproj_FFT, 11, 7, 1, 1)
        self.gV_Phantom = QtWidgets.QGraphicsView(self.Reconstruction)
        self.gV_Phantom.setAutoFillBackground(False)
        self.gV_Phantom.setObjectName("gV_Phantom")
        self.gridLayout.addWidget(self.gV_Phantom, 4, 1, 1, 1)
        self.gV_SinogramFFT = QtWidgets.QGraphicsView(self.Reconstruction)
        self.gV_SinogramFFT.setObjectName("gV_SinogramFFT")
        self.gridLayout.addWidget(self.gV_SinogramFFT, 11, 4, 1, 1)
        self.gV_Sinogram = QtWidgets.QGraphicsView(self.Reconstruction)
        self.gV_Sinogram.setAutoFillBackground(False)
        self.gV_Sinogram.setObjectName("gV_Sinogram")
        self.gridLayout.addWidget(self.gV_Sinogram, 4, 4, 1, 1)
        self.gV_Phantom_FFT = QtWidgets.QGraphicsView(self.Reconstruction)
        self.gV_Phantom_FFT.setObjectName("gV_Phantom_FFT")
        self.gridLayout.addWidget(self.gV_Phantom_FFT, 11, 1, 1, 1)
        self.pB_Xray = QtWidgets.QPushButton(self.Reconstruction)
        self.pB_Xray.setMaximumSize(QtCore.QSize(40, 500))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pB_Xray.setFont(font)
        self.pB_Xray.setObjectName("pB_Xray")
        self.gridLayout.addWidget(self.pB_Xray, 4, 2, 8, 1)
        self.pB_Reconstruction = QtWidgets.QPushButton(self.Reconstruction)
        self.pB_Reconstruction.setMaximumSize(QtCore.QSize(40, 500))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pB_Reconstruction.setFont(font)
        self.pB_Reconstruction.setObjectName("pB_Reconstruction")
        self.gridLayout.addWidget(self.pB_Reconstruction, 4, 6, 8, 1)
        self.checkBox_ParkerWeigh = QtWidgets.QCheckBox(self.Reconstruction)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.checkBox_ParkerWeigh.setFont(font)
        self.checkBox_ParkerWeigh.setObjectName("checkBox_ParkerWeigh")
        self.gridLayout.addWidget(self.checkBox_ParkerWeigh, 7, 4, 1, 1)
        self.checkBox_RamLakFilter = QtWidgets.QCheckBox(self.Reconstruction)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.checkBox_RamLakFilter.setFont(font)
        self.checkBox_RamLakFilter.setObjectName("checkBox_RamLakFilter")
        self.gridLayout.addWidget(self.checkBox_RamLakFilter, 9, 4, 1, 1)
        self.pB_PhantomSelect = QtWidgets.QPushButton(self.Reconstruction)
        self.pB_PhantomSelect.setMaximumSize(QtCore.QSize(40, 500))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pB_PhantomSelect.setFont(font)
        self.pB_PhantomSelect.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pB_PhantomSelect.setAutoDefault(False)
        self.pB_PhantomSelect.setObjectName("pB_PhantomSelect")
        self.gridLayout.addWidget(self.pB_PhantomSelect, 9, 0, 3, 1)
        self.label_Sino = QtWidgets.QLabel(self.Reconstruction)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_Sino.setFont(font)
        self.label_Sino.setObjectName("label_Sino")
        self.gridLayout.addWidget(self.label_Sino, 1, 4, 1, 1)
        self.label_Hslidervalue = QtWidgets.QLabel(self.Reconstruction)
        self.label_Hslidervalue.setObjectName("label_Hslidervalue")
        self.gridLayout.addWidget(self.label_Hslidervalue, 6, 4, 1, 1)
        self.vSlider_maxbeta = QtWidgets.QSlider(self.Reconstruction)
        self.vSlider_maxbeta.setMinimum(1)
        self.vSlider_maxbeta.setMaximum(360)
        self.vSlider_maxbeta.setOrientation(QtCore.Qt.Vertical)
        self.vSlider_maxbeta.setObjectName("vSlider_maxbeta")
        self.gridLayout.addWidget(self.vSlider_maxbeta, 4, 5, 1, 1)
        self.hSlider_deltabeta = QtWidgets.QSlider(self.Reconstruction)
        self.hSlider_deltabeta.setMinimum(1)
        self.hSlider_deltabeta.setMaximum(1024)
        self.hSlider_deltabeta.setOrientation(QtCore.Qt.Horizontal)
        self.hSlider_deltabeta.setObjectName("hSlider_deltabeta")
        self.gridLayout.addWidget(self.hSlider_deltabeta, 5, 4, 1, 1)
        self.label_Vslidervalue = QtWidgets.QLabel(self.Reconstruction)
        self.label_Vslidervalue.setObjectName("label_Vslidervalue")
        self.gridLayout.addWidget(self.label_Vslidervalue, 2, 4, 1, 3)
        self.verticalLayout.addLayout(self.gridLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)
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
        self.pB_videocapture.setText(_translate("ReconstructionGUI", "L\n"
"I\n"
"V\n"
"E\n"
"\n"
"I\n"
"M\n"
"A\n"
"G\n"
"E\n"
"\n"
"C\n"
"A\n"
"P\n"
"T\n"
"U\n"
"R\n"
"E"))
        self.checkBox_cosine.setText(_translate("ReconstructionGUI", "Cosine Weigting"))
        self.label_Phantom.setText(_translate("ReconstructionGUI", "Phantom"))
        self.label_Sinogram.setText(_translate("ReconstructionGUI", "Sinogram FFT"))
        self.label_BackprojFFT.setText(_translate("ReconstructionGUI", "Backprojection FFT"))
        self.label_Backproj.setText(_translate("ReconstructionGUI", "Back Projection"))
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
        self.label_Sino.setText(_translate("ReconstructionGUI", "Sinogram"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ReconstructionGUI = QtWidgets.QMainWindow()
    ui = Ui_ReconstructionGUI()
    ui.setupUi(ReconstructionGUI)
    ReconstructionGUI.show()
    sys.exit(app.exec_())

