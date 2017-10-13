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
        ReconstructionGUI.resize(1005, 852)
        self.Reconstruction = QtWidgets.QWidget(ReconstructionGUI)
        self.Reconstruction.setObjectName("Reconstruction")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.Reconstruction)
        self.gridLayout_2.setObjectName("gridLayout_2")
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
        self.gridLayout.addWidget(self.label_Sino, 0, 3, 1, 1)
        self.label_Backproj = QtWidgets.QLabel(self.Reconstruction)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_Backproj.setFont(font)
        self.label_Backproj.setAutoFillBackground(True)
        self.label_Backproj.setObjectName("label_Backproj")
        self.gridLayout.addWidget(self.label_Backproj, 0, 5, 1, 1)
        self.pB_videocapture = QtWidgets.QPushButton(self.Reconstruction)
        self.pB_videocapture.setMaximumSize(QtCore.QSize(40, 450))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pB_videocapture.setFont(font)
        self.pB_videocapture.setObjectName("pB_videocapture")
        self.gridLayout.addWidget(self.pB_videocapture, 1, 0, 6, 1)
        self.gV_Phantom = QtWidgets.QGraphicsView(self.Reconstruction)
        self.gV_Phantom.setAutoFillBackground(False)
        self.gV_Phantom.setObjectName("gV_Phantom")
        self.gridLayout.addWidget(self.gV_Phantom, 1, 1, 1, 1)
        self.pB_Xray = QtWidgets.QPushButton(self.Reconstruction)
        self.pB_Xray.setMaximumSize(QtCore.QSize(40, 700))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pB_Xray.setFont(font)
        self.pB_Xray.setObjectName("pB_Xray")
        self.gridLayout.addWidget(self.pB_Xray, 1, 2, 10, 1)
        self.gV_Sinogram = QtWidgets.QGraphicsView(self.Reconstruction)
        self.gV_Sinogram.setAutoFillBackground(False)
        self.gV_Sinogram.setObjectName("gV_Sinogram")
        self.gridLayout.addWidget(self.gV_Sinogram, 1, 3, 1, 1)
        self.pB_Reconstruction = QtWidgets.QPushButton(self.Reconstruction)
        self.pB_Reconstruction.setMaximumSize(QtCore.QSize(40, 700))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pB_Reconstruction.setFont(font)
        self.pB_Reconstruction.setObjectName("pB_Reconstruction")
        self.gridLayout.addWidget(self.pB_Reconstruction, 1, 4, 10, 1)
        self.gV_Backproj = QtWidgets.QGraphicsView(self.Reconstruction)
        self.gV_Backproj.setAutoFillBackground(False)
        self.gV_Backproj.setObjectName("gV_Backproj")
        self.gridLayout.addWidget(self.gV_Backproj, 1, 5, 1, 1)
        self.label_delta = QtWidgets.QLabel(self.Reconstruction)
        self.label_delta.setObjectName("label_delta")
        self.gridLayout.addWidget(self.label_delta, 2, 3, 1, 1)
        self.hScrollBar_deltabeta = QtWidgets.QScrollBar(self.Reconstruction)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.hScrollBar_deltabeta.setPalette(palette)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.hScrollBar_deltabeta.setFont(font)
        self.hScrollBar_deltabeta.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.hScrollBar_deltabeta.setMinimum(1)
        self.hScrollBar_deltabeta.setMaximum(1024)
        self.hScrollBar_deltabeta.setOrientation(QtCore.Qt.Horizontal)
        self.hScrollBar_deltabeta.setObjectName("hScrollBar_deltabeta")
        self.gridLayout.addWidget(self.hScrollBar_deltabeta, 3, 3, 1, 1)
        self.label_max = QtWidgets.QLabel(self.Reconstruction)
        self.label_max.setMaximumSize(QtCore.QSize(352, 16777215))
        self.label_max.setObjectName("label_max")
        self.gridLayout.addWidget(self.label_max, 4, 3, 1, 1)
        self.hScrollBar_maxbeta = QtWidgets.QScrollBar(self.Reconstruction)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.hScrollBar_maxbeta.setPalette(palette)
        self.hScrollBar_maxbeta.setMinimum(1)
        self.hScrollBar_maxbeta.setMaximum(360)
        self.hScrollBar_maxbeta.setOrientation(QtCore.Qt.Horizontal)
        self.hScrollBar_maxbeta.setObjectName("hScrollBar_maxbeta")
        self.gridLayout.addWidget(self.hScrollBar_maxbeta, 5, 3, 1, 1)
        self.checkBox_ParkerWeigh = QtWidgets.QCheckBox(self.Reconstruction)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.checkBox_ParkerWeigh.setFont(font)
        self.checkBox_ParkerWeigh.setObjectName("checkBox_ParkerWeigh")
        self.gridLayout.addWidget(self.checkBox_ParkerWeigh, 6, 3, 1, 1)
        self.checkBox_cosine = QtWidgets.QCheckBox(self.Reconstruction)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.checkBox_cosine.setFont(font)
        self.checkBox_cosine.setObjectName("checkBox_cosine")
        self.gridLayout.addWidget(self.checkBox_cosine, 7, 3, 1, 1)
        self.checkBox_RamLakFilter = QtWidgets.QCheckBox(self.Reconstruction)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.checkBox_RamLakFilter.setFont(font)
        self.checkBox_RamLakFilter.setObjectName("checkBox_RamLakFilter")
        self.gridLayout.addWidget(self.checkBox_RamLakFilter, 8, 3, 1, 1)
        self.pB_PhantomSelect = QtWidgets.QPushButton(self.Reconstruction)
        self.pB_PhantomSelect.setMaximumSize(QtCore.QSize(40, 400))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pB_PhantomSelect.setFont(font)
        self.pB_PhantomSelect.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pB_PhantomSelect.setAutoDefault(False)
        self.pB_PhantomSelect.setObjectName("pB_PhantomSelect")
        self.gridLayout.addWidget(self.pB_PhantomSelect, 9, 0, 2, 1)
        self.label_PhantomFFT = QtWidgets.QLabel(self.Reconstruction)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_PhantomFFT.setFont(font)
        self.label_PhantomFFT.setObjectName("label_PhantomFFT")
        self.gridLayout.addWidget(self.label_PhantomFFT, 9, 1, 1, 1)
        self.label_Sinogram = QtWidgets.QLabel(self.Reconstruction)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_Sinogram.setFont(font)
        self.label_Sinogram.setObjectName("label_Sinogram")
        self.gridLayout.addWidget(self.label_Sinogram, 9, 3, 1, 1)
        self.label_BackprojFFT = QtWidgets.QLabel(self.Reconstruction)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_BackprojFFT.setFont(font)
        self.label_BackprojFFT.setObjectName("label_BackprojFFT")
        self.gridLayout.addWidget(self.label_BackprojFFT, 9, 5, 1, 1)
        self.gV_Phantom_FFT = QtWidgets.QGraphicsView(self.Reconstruction)
        self.gV_Phantom_FFT.setObjectName("gV_Phantom_FFT")
        self.gridLayout.addWidget(self.gV_Phantom_FFT, 10, 1, 1, 1)
        self.gV_SinogramFFT = QtWidgets.QGraphicsView(self.Reconstruction)
        self.gV_SinogramFFT.setObjectName("gV_SinogramFFT")
        self.gridLayout.addWidget(self.gV_SinogramFFT, 10, 3, 1, 1)
        self.gV_Backproj_FFT = QtWidgets.QGraphicsView(self.Reconstruction)
        self.gV_Backproj_FFT.setFocusPolicy(QtCore.Qt.NoFocus)
        self.gV_Backproj_FFT.setAutoFillBackground(False)
        self.gV_Backproj_FFT.setObjectName("gV_Backproj_FFT")
        self.gridLayout.addWidget(self.gV_Backproj_FFT, 10, 5, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        ReconstructionGUI.setCentralWidget(self.Reconstruction)
        self.menubar = QtWidgets.QMenuBar(ReconstructionGUI)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1005, 17))
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
        self.label_delta.setText(_translate("ReconstructionGUI", "<html><head/><body><p>Sample Density</p></body></html>"))
        self.label_max.setText(_translate("ReconstructionGUI", "<html><head/><body><p>Rotation Angle</p></body></html>"))
        self.checkBox_ParkerWeigh.setText(_translate("ReconstructionGUI", "Parker Weighting"))
        self.checkBox_cosine.setText(_translate("ReconstructionGUI", "Cosine Filter"))
        self.checkBox_RamLakFilter.setText(_translate("ReconstructionGUI", "RamLak Filter"))
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
        self.label_PhantomFFT.setText(_translate("ReconstructionGUI", "Phantom FFT"))
        self.label_Sinogram.setText(_translate("ReconstructionGUI", "Sinogram FFT"))
        self.label_BackprojFFT.setText(_translate("ReconstructionGUI", "Backprojection FFT"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ReconstructionGUI = QtWidgets.QMainWindow()
    ui = Ui_ReconstructionGUI()
    ui.setupUi(ReconstructionGUI)
    ReconstructionGUI.show()
    sys.exit(app.exec_())

