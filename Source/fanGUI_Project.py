# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fanGUI_Project.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class PhotoViewer(QtWidgets.QGraphicsView):
    photoClicked = QtCore.pyqtSignal(QtCore.QPoint)
    def mouseDoubleClickEvent(self, event):
        self.photoClicked.emit(QtCore.QPoint(event.pos()))
        super(PhotoViewer, self).mousePressEvent(event)

class Ui_ReconstructionGUI(object):
    def setupUi(self, ReconstructionGUI):
        ReconstructionGUI.setObjectName("ReconstructionGUI")
        ReconstructionGUI.resize(1120, 753)
        ReconstructionGUI.setMaximumSize(QtCore.QSize(16777215, 16666666))
        self.Reconstruction = QtWidgets.QWidget(ReconstructionGUI)
        self.Reconstruction.setObjectName("Reconstruction")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.Reconstruction)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.groupBox = QtWidgets.QGroupBox(self.Reconstruction)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.frame_10 = QtWidgets.QFrame(self.groupBox)
        self.frame_10.setMinimumSize(QtCore.QSize(300, 0))
        self.frame_10.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_10.setObjectName("frame_10")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.frame_10)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_delta_2 = QtWidgets.QLabel(self.frame_10)
        self.label_delta_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_delta_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_delta_2.setObjectName("label_delta_2")
        self.verticalLayout_6.addWidget(self.label_delta_2)
        self.hScrollBar_maxbeta = QtWidgets.QScrollBar(self.frame_10)
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
        self.verticalLayout_6.addWidget(self.hScrollBar_maxbeta)
        self.horizontalLayout_3.addWidget(self.frame_10)
        self.frame_9 = QtWidgets.QFrame(self.groupBox)
        self.frame_9.setMinimumSize(QtCore.QSize(300, 0))
        self.frame_9.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_9.setObjectName("frame_9")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_9)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_delta = QtWidgets.QLabel(self.frame_9)
        self.label_delta.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_delta.setAlignment(QtCore.Qt.AlignCenter)
        self.label_delta.setObjectName("label_delta")
        self.verticalLayout_5.addWidget(self.label_delta)
        self.hScrollBar_deltabeta = QtWidgets.QScrollBar(self.frame_9)
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
        self.verticalLayout_5.addWidget(self.hScrollBar_deltabeta)
        self.horizontalLayout_3.addWidget(self.frame_9)
        self.checkBox_RamLakFilter = QtWidgets.QCheckBox(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.checkBox_RamLakFilter.setFont(font)
        self.checkBox_RamLakFilter.setObjectName("checkBox_RamLakFilter")
        self.horizontalLayout_3.addWidget(self.checkBox_RamLakFilter)
        self.checkBox_ParkerWeigh = QtWidgets.QCheckBox(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.checkBox_ParkerWeigh.setFont(font)
        self.checkBox_ParkerWeigh.setObjectName("checkBox_ParkerWeigh")
        self.horizontalLayout_3.addWidget(self.checkBox_ParkerWeigh)
        self.checkBox_cosine = QtWidgets.QCheckBox(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.checkBox_cosine.setFont(font)
        self.checkBox_cosine.setObjectName("checkBox_cosine")
        self.horizontalLayout_3.addWidget(self.checkBox_cosine)
        self.verticalLayout_7.addWidget(self.groupBox)
        self.frame_7 = QtWidgets.QFrame(self.Reconstruction)
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_7)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frame_5 = QtWidgets.QFrame(self.frame_7)
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_5)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.gV_Phantom = PhotoViewer(self.frame_5)
        self.gV_Phantom.setAutoFillBackground(False)
        self.gV_Phantom.setObjectName("gV_Phantom")
        self.verticalLayout_3.addWidget(self.gV_Phantom)
        self.gV_Phantom_FFT = PhotoViewer(self.frame_5)
        self.gV_Phantom_FFT.setObjectName("gV_Phantom_FFT")
        self.verticalLayout_3.addWidget(self.gV_Phantom_FFT)
        self.gridLayout_2.addWidget(self.frame_5, 0, 1, 1, 1)
        self.frame_2 = QtWidgets.QFrame(self.frame_7)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gV_Sinogram = PhotoViewer(self.frame_2)
        self.gV_Sinogram.setAutoFillBackground(False)
        self.gV_Sinogram.setObjectName("gV_Sinogram")
        self.verticalLayout_2.addWidget(self.gV_Sinogram)
        self.gV_SinogramFFT = PhotoViewer(self.frame_2)
        self.gV_SinogramFFT.setObjectName("gV_SinogramFFT")
        self.verticalLayout_2.addWidget(self.gV_SinogramFFT)
        self.gridLayout_2.addWidget(self.frame_2, 0, 3, 1, 1)
        self.frame_4 = QtWidgets.QFrame(self.frame_7)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_4)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pB_Xray = QtWidgets.QPushButton(self.frame_4)
        self.pB_Xray.setMaximumSize(QtCore.QSize(40, 700))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pB_Xray.setFont(font)
        self.pB_Xray.setObjectName("pB_Xray")
        self.horizontalLayout_2.addWidget(self.pB_Xray)
        self.gridLayout_2.addWidget(self.frame_4, 0, 2, 1, 1)
        self.frame = QtWidgets.QFrame(self.frame_7)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gV_Backproj = PhotoViewer(self.frame)
        self.gV_Backproj.setAutoFillBackground(False)
        self.gV_Backproj.setObjectName("gV_Backproj")
        self.verticalLayout.addWidget(self.gV_Backproj)
        self.gV_Backproj_FFT = PhotoViewer(self.frame)
        self.gV_Backproj_FFT.setFocusPolicy(QtCore.Qt.NoFocus)
        self.gV_Backproj_FFT.setAutoFillBackground(False)
        self.gV_Backproj_FFT.setObjectName("gV_Backproj_FFT")
        self.verticalLayout.addWidget(self.gV_Backproj_FFT)
        self.gV_Backproj.raise_()
        self.gV_Backproj_FFT.raise_()
        self.gV_Backproj.raise_()
        self.gV_Backproj_FFT.raise_()
        self.gV_Backproj.raise_()
        self.gridLayout_2.addWidget(self.frame, 0, 5, 1, 1)
        self.frame_3 = QtWidgets.QFrame(self.frame_7)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pB_Reconstruction = QtWidgets.QPushButton(self.frame_3)
        self.pB_Reconstruction.setMaximumSize(QtCore.QSize(40, 700))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pB_Reconstruction.setFont(font)
        self.pB_Reconstruction.setObjectName("pB_Reconstruction")
        self.horizontalLayout.addWidget(self.pB_Reconstruction)
        self.gridLayout_2.addWidget(self.frame_3, 0, 4, 1, 1)
        self.frame_6 = QtWidgets.QFrame(self.frame_7)
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_6)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.pB_videocapture = QtWidgets.QPushButton(self.frame_6)
        self.pB_videocapture.setMaximumSize(QtCore.QSize(40, 450))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pB_videocapture.setFont(font)
        self.pB_videocapture.setObjectName("pB_videocapture")
        self.verticalLayout_4.addWidget(self.pB_videocapture)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_4.addItem(spacerItem)
        self.pB_PhantomSelect = QtWidgets.QPushButton(self.frame_6)
        self.pB_PhantomSelect.setMaximumSize(QtCore.QSize(40, 400))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pB_PhantomSelect.setFont(font)
        self.pB_PhantomSelect.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pB_PhantomSelect.setAutoDefault(False)
        self.pB_PhantomSelect.setObjectName("pB_PhantomSelect")
        self.verticalLayout_4.addWidget(self.pB_PhantomSelect)
        self.gridLayout_2.addWidget(self.frame_6, 0, 0, 1, 1)
        self.verticalLayout_7.addWidget(self.frame_7)
        ReconstructionGUI.setCentralWidget(self.Reconstruction)
        self.menubar = QtWidgets.QMenuBar(ReconstructionGUI)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1120, 26))
        self.menubar.setObjectName("menubar")
        ReconstructionGUI.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ReconstructionGUI)
        self.statusbar.setObjectName("statusbar")
        ReconstructionGUI.setStatusBar(self.statusbar)

        self.retranslateUi(ReconstructionGUI)
        QtCore.QMetaObject.connectSlotsByName(ReconstructionGUI)

    def retranslateUi(self, ReconstructionGUI):
        _translate = QtCore.QCoreApplication.translate
        ReconstructionGUI.setWindowTitle(_translate("ReconstructionGUI", "Interaktive Rekonstruktion"))
        self.groupBox.setTitle(_translate("ReconstructionGUI", "Konfiguriere Röntgen System"))
        self.label_delta_2.setText(_translate("ReconstructionGUI", "<html><head/><body><p>Maximale Angulation</p></body></html>"))
        self.label_delta.setText(_translate("ReconstructionGUI", "<html><head/><body><p>Winkelabgstand zwischen Projektionen</p></body></html>"))
        self.checkBox_RamLakFilter.setText(_translate("ReconstructionGUI", "RamLak Filter"))
        self.checkBox_ParkerWeigh.setText(_translate("ReconstructionGUI", "Parker Gewicht"))
        self.checkBox_cosine.setText(_translate("ReconstructionGUI", "Kosinus Filter"))
        self.pB_Xray.setText(_translate("ReconstructionGUI", "R\n"
"Ö\n"
"N\n"
"T\n"
"G\n"
"E\n"
"N"))
        self.pB_Reconstruction.setText(_translate("ReconstructionGUI", "R\n"
"E\n"
"K\n"
"O\n"
"N\n"
"S\n"
"T\n"
"R\n"
"U\n"
"I\n"
"E\n"
"R\n"
"E\n"
"N"))
        self.pB_videocapture.setText(_translate("ReconstructionGUI", "L\n"
"I\n"
"V\n"
"E\n"
"\n"
"P\n"
"H\n"
"O\n"
"T\n"
"O"))
        self.pB_PhantomSelect.setText(_translate("ReconstructionGUI", "P\n"
"H\n"
"A\n"
"N\n"
"T\n"
"O\n"
"M"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ReconstructionGUI = QtWidgets.QMainWindow()
    ui = Ui_ReconstructionGUI()
    ui.setupUi(ReconstructionGUI)
    ReconstructionGUI.show()
    sys.exit(app.exec_())

