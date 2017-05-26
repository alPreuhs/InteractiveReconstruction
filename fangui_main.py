from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import subprocess
import numpy as np
from fanGUI_Project import Ui_wid_FanRecont
from PhantomSelect_Window import selectPhantom
from PhantomSelect import Ui_Wid_PhantomSelect

class fanbeam_main(Ui_wid_FanRecont):

    phantom_value = {}
    file_path = 'NULL'
    #def __init__(self, dialog):
     #   print("test")
        #Ui_wid_FanRecont.__init__(self)
        #self.setupUi(dialog)


    #Logic for clicking the push button and getting new window
    def PhantomSelect_click(self):
        self.pB_PhantomSelect.clicked.connect(self.selectphantom)

    # function for displaying the phantom selection window
    def selectphantom(self):
        self.selectPhan_Window = QtWidgets.QWidget()
        self.selectPhan_creator = selectPhantom(self.selectPhan_Window)
        self.selectPhan_creator.ListWid_SelectPhantom.itemClicked.connect(self.getPhantom)
        self.phantom_value =  self.selectPhan_creator.listwidload()
        self.selectPhan_Window.show()

    def getPhantom(self):
        self.file_path = self.selectPhan_creator.ListWid_SelectPhantom.currentIndex().data()
        self.Phantom_load()
        self.selectPhan_Window.close()

    #Function for loading the phantom
    def Phantom_load(self):
        img_Phantom = QtGui.QImage(self.phantom_value[self.file_path])
        img_Phantom = img_Phantom.scaled(377,217, aspectRatioMode=QtCore.Qt.KeepAspectRatio,transformMode=QtCore.Qt.SmoothTransformation)
        self.pix_Phantom = QtGui.QPixmap(img_Phantom)
        self.gps_Phantom_placeholder = QtWidgets.QGraphicsPixmapItem(self.pix_Phantom)
        self.gps_Phantom = QtWidgets.QGraphicsPixmapItem(self.pix_Phantom)
        #self.gps_Line = QtWidgets.QGraphicsLineItem()
        self.gs_Phantom = QtWidgets.QGraphicsScene()
        self.gs_Phantom.clear()
        self.gs_Phantom.addItem(self.gps_Phantom)
        self.Line1 = self.gs_Phantom.addLine(0, 0, 65, 216, QtCore.Qt.white)
        self.Line2 = self.gs_Phantom.addLine(0, 0, 245, 45, QtCore.Qt.white)
        self.Line3 = self.gs_Phantom.addLine(65, 216, 245, 45, QtCore.Qt.white)
        self.gV_Phantom.setScene(self.gs_Phantom)
        self.gV_Phantom.setStyleSheet("background:black")
        self.gs_Phantom.update()


    #slide bar with image movement
    def Phantom_Slider_Moved(self):
        self.hSlider_Phantom.valueChanged.connect(self.hslider_changed)


    def hslider_changed(self):
        self.hSlider_Phantom_value = self.hSlider_Phantom.value()
        print(-self.hSlider_Phantom_value)
        self.rotation_triangle()

    def rotation_triangle(self):
        #self.offset = np.zeros(shape=(3, 2))
        #self.offset[0, ...] = [-self.pix_Phantom.width() / 2, -self.pix_Phantom.height()  / 2]
        #self.Line1.setPos(-self.offset[0, 0], -self.offset[0, 1])
        #self.Line2.setPos(-self.offset[0, 0], -self.offset[0, 1])
        #self.Line3.setPos(-self.offset[0, 0], -self.offset[0, 1])
        self.Line1.setTransformOriginPoint(self.Line1.mapFromScene(QtCore.QPointF(self.pix_Phantom.width() / 2, self.pix_Phantom.height()/2 )))
        self.Line2.setTransformOriginPoint(self.Line2.mapFromScene(QtCore.QPointF(self.pix_Phantom.width() / 2, self.pix_Phantom.height()/2 )))
        self.Line3.setTransformOriginPoint(self.Line3.mapFromScene(QtCore.QPointF(self.pix_Phantom.width() / 2, self.pix_Phantom.height()/2)))
        self.Line1.setRotation(-self.hSlider_Phantom_value)
        self.Line2.setRotation(-self.hSlider_Phantom_value)
        self.Line3.setRotation(-self.hSlider_Phantom_value)

if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    wid_FanRecont = QtWidgets.QWidget()
    ui = fanbeam_main()
    ui.setupUi(wid_FanRecont)
    ui.PhantomSelect_click()
    ui.Phantom_Slider_Moved()
    #ui.rotation_triangle()
    wid_FanRecont.show()
    sys.exit(app.exec_())
