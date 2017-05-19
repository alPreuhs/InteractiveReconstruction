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
        self.offset = np.zeros(shape=(3, 2))
        self.offset[0, ...] = [-self.pix_Phantom.width() / 2, -self.pix_Phantom.height() * 3 / 4]
        self.gps_Phantom = QtWidgets.QGraphicsPixmapItem(self.pix_Phantom)
        self.gps_Phantom.setOffset(self.offset[0, 0], self.offset[0, 1])
        self.gps_Phantom.setPos(-  self.offset[0, 0], -self.offset[0, 1])
        self.gps_Phantom = QtWidgets.QGraphicsPixmapItem(self.pix_Phantom)
        self.gs_Phantom = QtWidgets.QGraphicsScene()
        self.gs_Phantom.clear()
        self.gs_Phantom.addItem(self.gps_Phantom)
        self.gV_Phantom.setScene(self.gs_Phantom)
        self.gV_Phantom.setStyleSheet("background:black")
        self.gs_Phantom.update()


    #slide bar with image movement
    #def Phantom_Slider_Moved(self):
       # self.hSlider_Phantom.valueChanged.connect(self.hslider_changed)


    #def hslider_changed(self):
        #hSlider_Phantom_value = self.hSlider_Phantom.value()



if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    wid_FanRecont = QtWidgets.QWidget()
    ui = fanbeam_main()
    ui.setupUi(wid_FanRecont)
    ui.PhantomSelect_click()
    #ui.Phantom_Slider_Moved()
    wid_FanRecont.show()
    sys.exit(app.exec_())
