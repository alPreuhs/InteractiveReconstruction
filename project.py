from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import numpy
from test import Ui_Dialog
from test1window import Ui_test1window
from project1 import testwindow

class FirstGuiProgram(Ui_Dialog):
    def __init__(self, dialog):
        Ui_Dialog.__init__(self)
        self.setupUi(dialog)

        #Logic for clicking the push button and getting new window
        self.pushButton.clicked.connect(self.myfunction)

        #Loading a image in the grapical view widget
        img_sinogram = QtGui.QImage('/Users/Janani/Downloads/phantom.png')
        img_sinogram = img_sinogram.scaled(191,231, aspectRatioMode=QtCore.Qt.KeepAspectRatio,transformMode=QtCore.Qt.SmoothTransformation)
        self.pix_sinogram = QtGui.QPixmap(img_sinogram)
        self.gps_sinogram_placeholder = QtWidgets.QGraphicsPixmapItem(self.pix_sinogram)
        #self.offset = numpy.zeros(shape=(3, 2))
        #self.offset[0, ...] = [-self.pix_sinogram.width() / 2, -self.pix_sinogram.height() * 3 / 4]
        self.gps_sinogram = QtWidgets.QGraphicsPixmapItem(self.pix_sinogram)
        #self.gps_sinogram.setOffset(self.offset[0, 0], self.offset[0, 1])
        #self.gps_sinogram.setPos(-  self.offset[0, 0], -self.offset[0, 1])

        self.gs_sinogram = QtWidgets.QGraphicsScene()

        self.gs_sinogram.addItem(self.gps_sinogram)

        self.GV_phantom.setScene(self.gs_sinogram)

        #slide bar with image movement
        #self.hSlider_1.valueChanged.connect(self.hslider_changed)

    def myfunction(self):
        self.project1_widget = QtWidgets.QWidget()
        self.project1_creator = testwindow(self.project1_widget)
        self.project1_widget.show()

    #def hslider_changed(self):



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QMainWindow()
    prog = FirstGuiProgram(dialog)
    dialog.show()
    sys.exit(app.exec_())
