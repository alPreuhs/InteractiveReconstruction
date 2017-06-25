from __future__ import division
from __future__ import print_function
from PIL import Image
from PyQt5 import QtCore, QtGui, QtWidgets
from fanGUI_Project import Ui_wid_FanRecont
from PhantomSelect_Window import selectPhantom
from PhantomSelect import Ui_Wid_PhantomSelect
import scipy.misc
import sys
import subprocess
import numpy as np
import scipy.ndimage
import warnings

__all__ = ["radon", "radon_fan_translation", "get_fan_coords",
           "get_det_coords"]



class fanbeam_main(Ui_wid_FanRecont):

    phantom_value = {}
    file_path = 'NULL'
    #def __init__(self, dialog):
     #   print("test")
        #Ui_wid_FanRecont.__init__(self)
        #self.setupUi(dialog)


    def get_det_coords(size, spacing):
        latmax = (size / 2 - .5) * spacing
        lat = np.linspace(-latmax, latmax, size, endpoint=True)
        return lat

    def get_fan_coords(size, spacing, distance, numang):
        latmax = (size / 2 - .5) * spacing
        angmax = abs(np.arctan2(latmax, distance))
        # equispaced angles
        angles = np.linspace(-angmax, angmax, numang, endpoint=True)

        latang = np.tan(angles) * distance
        latang[0] = -latmax
        latang[-1] = latmax
        return angles, latang

    def radon_fan_translation(arr, det_size, det_spacing=1, shift_size=1,
                              lS=1, lD=None, return_ang=False,
                              jmc=None, jmm=None):
        N = arr.shape[0]
        print(N)
        if lD is None:
            lD = N / 2
        lS = abs(lS)
        lDS = lS + lD

        numsteps = int(np.ceil((N + det_size) / shift_size))
        print(numsteps)

        if jmm is not None:
            jmm.value = numsteps + 2

        # First, create a zero-padded version of the input image such that
        # its center is the source - this is necessary because we can
        # only rotate through the center of the image.
        # arrc = np.pad(arr, ((0,0),(N+2*lS-1,0)), mode="constant")
        if lS <= N / 2:
            pad = 2 * lS
            arrc = np.pad(arr, ((0, 0), (pad, 0)), mode="constant")
            # The center is where either b/w 2 pixels or at one pixel,
            # as it is for the input image.
        else:
            pad = N / 2 + lS
            if pad % 1 == 0:  # even
                pad = int(pad)
                arrc = np.pad(arr, ((0, 0), (pad, 0)), mode="constant")
            else:
                pad = int(np.floor(pad))
                arrc = np.pad(arr, ((0, 0), (pad, 0)), mode="constant")
        axi = np.ones(det_size) * lDS

        if det_size % 2 == 0:
            even = True
        else:
            even = False

        if jmc is not None:
            jmc.value += 1

        lat = fanbeam_main.get_det_coords(det_size, det_spacing)
        print(lat)

        angles = np.arctan2(lat, axi)

        pad2 = det_size
        padset = np.pad(arrc, ((0, pad2), (0, 0)), mode="constant")
        A = angles.shape[0]
        lino = np.zeros((numsteps, A))

        if jmc is not None:
            jmc.value += 1

        for i in range(numsteps):
            padset = np.roll(padset, shift_size, axis=0)
            # cut out a det_size slice
            curobj = padset[N:]
            print(curobj)
            for j in range(A):
                ang = angles[j]
                rotated = scipy.ndimage.rotate(curobj, ang / np.pi * 180,
                                               order=3, reshape=False, mode="constant", cval=0)
                #print(rotated)
                if even:
                    warnings.warn("For even images the linogram is of " +
                                  "reduced resolution, because the center " +
                                  "of the image does not coincide with " +
                                  "a center of a pixel.")
                    centerid = int(len(rotated) / 2)
                    lino[i, j] = np.sum(rotated[centerid - 1:centerid + 1, :]) / 2
                    #print(lino)
                else:  # odd
                    centerid = int(np.floor(len(rotated) / 2))
                    lino[i, j] = np.sum(rotated[centerid, :])

            if jmc is not None:
                jmc.value += 1

        if return_ang:
            scipy.misc.imsave('outfile.jpg', lino)
            return lino, angles
        else:
            scipy.misc.imsave('outfile.jpg', lino)
            return lino

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
        img_Phantom = img_Phantom.scaled(377,377, aspectRatioMode=QtCore.Qt.KeepAspectRatio,transformMode=QtCore.Qt.SmoothTransformation)
        self.pix_Phantom = QtGui.QPixmap(img_Phantom)
        self.gps_Phantom_placeholder = QtWidgets.QGraphicsPixmapItem(self.pix_Phantom)
        self.gps_Phantom = QtWidgets.QGraphicsPixmapItem(self.pix_Phantom)
        #self.gps_Line = QtWidgets.QGraphicsLineItem()
        self.gs_Phantom = QtWidgets.QGraphicsScene()
        self.gs_Phantom.clear()
        self.gs_Phantom.addItem(self.gps_Phantom)
        self.Ecllipse = self.gs_Phantom.addEllipse(0,0,25,25,QtCore.Qt.white)
        self.Line1 = self.gs_Phantom.addLine(20, 20, 150, 375, QtCore.Qt.white)
        self.Line2 = self.gs_Phantom.addLine(20, 20, 375,150, QtCore.Qt.white)
        self.Line3 = self.gs_Phantom.addLine(150, 375, 375, 150, QtCore.Qt.white)
        self.gV_Phantom.setScene(self.gs_Phantom)
        self.gV_Phantom.setStyleSheet("background:black")
        self.gs_Phantom.update()
        print(self.phantom_value[self.file_path])
        self.temp = np.asarray(Image.open(self.phantom_value[self.file_path]), dtype="int32").reshape(377,377)
        #self.im = imread(self.phantom_value[self.file_path])
        #print(self.temp)

    #slide bar with image movement
    def Phantom_Slider_Moved(self):
        self.hSlider_Phantom.valueChanged.connect(self.hslider_changed)


    def hslider_changed(self):
        self.hSlider_Phantom_value = self.hSlider_Phantom.value()
        print(-self.hSlider_Phantom_value)
        self.rotation_triangle(-self.hSlider_Phantom_value)

    def rotation_triangle(self, val):
        self.Line1.setTransformOriginPoint(QtCore.QPointF(self.pix_Phantom.width() / 2, self.pix_Phantom.height()/2 ))
        self.Line2.setTransformOriginPoint(QtCore.QPointF(self.pix_Phantom.width() / 2, self.pix_Phantom.height()/2 ))
        self.Line3.setTransformOriginPoint(QtCore.QPointF(self.pix_Phantom.width() / 2, self.pix_Phantom.height()/2))
        self.Ecllipse.setTransformOriginPoint(QtCore.QPointF(self.pix_Phantom.width() / 2, self.pix_Phantom.height()/2 ))
        self.Line1.setRotation(val)
        self.Line2.setRotation(val)
        self.Line3.setRotation(val)
        self.Ecllipse.setRotation(val)
        fanbeam_main.radon_fan_translation(self.temp,377,1,1,1)





if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    wid_FanRecont = QtWidgets.QWidget()
    ui = fanbeam_main()
    ui.setupUi(wid_FanRecont)
    ui.PhantomSelect_click()
    ui.Phantom_Slider_Moved()
    wid_FanRecont.show()
    sys.exit(app.exec_())

















































































































































































































































