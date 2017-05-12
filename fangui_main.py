from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import numpy
from fanGUI_Project import Ui_wid_FanRecont
from PhantomSelect_Window import selectPhantom
from PhantomSelect import Ui_Wid_PhantomSelect

class fanbeam_main(Ui_wid_FanRecont):
    #Initialization function
    def __init__(self, dialog):
        Ui_wid_FanRecont.__init__(self)
        self.setupUi(dialog)
        #self.Phantom_load(selectPhantom())
        self.PhantomSelect_click()

    #Logic for clicking the push button and getting new window
    def PhantomSelect_click(self):
        self.pB_PhantomSelect.clicked.connect(self.selectphantom)

    # function for displaying the phantom selection window
    def selectphantom(self):
        self.selectPhan_Window = QtWidgets.QWidget()
        self.selectPhan_creator = selectPhantom(self.selectPhan_Window)
        self.selectPhan_Window.show()
        #self.Phantom_load(icon)


    #Function for loading the phantom
    #def Phantom_load(self,icon):
        #Loading a image in the grapical view widget
        #img_Phantom = QtGui.QImage('/Users/Janani/Downloads/phantom.png')
        #img_Phantom = QtGui.QIcon(icon)
        #img_Phantom = img_Phantom.scaled(377,217, aspectRatioMode=QtCore.Qt.KeepAspectRatio,transformMode=QtCore.Qt.SmoothTransformation)
        #self.pix_Phantom = QtGui.QPixmap(img_Phantom)
        #self.gps_Phantom_placeholder = QtWidgets.QGraphicsPixmapItem(self.pix_Phantom)
        #self.gps_Phantom = QtWidgets.QGraphicsPixmapItem(self.pix_Phantom)
        #self.gs_Phantom = QtWidgets.QGraphicsScene()
        #self.gs_Phantom.addItem(self.gps_Phantom)
        #self.gV_Phantom.setScene(icon)
        #self.gV_Phantom.setStyleSheet("background:black")

        #slide bar with image movement
        #self.hSlider_1.valueChanged.connect(self.hslider_changed)



    #def hslider_changed(self):



if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    wid_FanRecont = QtWidgets.QWidget()
    ui = fanbeam_main(wid_FanRecont)
    ui.setupUi(wid_FanRecont)
    wid_FanRecont.show()
    sys.exit(app.exec_())
