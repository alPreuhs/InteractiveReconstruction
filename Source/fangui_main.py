from __future__ import division
from __future__ import print_function
from PIL import Image
from scipy.interpolate import RectBivariateSpline
from numpy import ones,vstack
from numpy.linalg import lstsq
from PyQt5 import QtCore, QtGui, QtWidgets
from Source.fanGUI_Project import Ui_wid_FanRecont
from numpy import linalg as LA
from Source.PhantomSelect_Window import selectPhantom
from sklearn import preprocessing
from sympy import Point3D, Line3D
import math
import numpy as np
import matplotlib.pylab as plt



class fanbeam_main(Ui_wid_FanRecont):

    phantom_value = {}
    file_path = 'NULL'
    #def __init__(self, dialog):
     #   print("test")
        #Ui_wid_FanRecont.__init__(self)
        #self.setupUi(dialog)

    def interpolation_Image(self,image):
        x = np.arange(image.shape[0])
        y = np.arange(image.shape[1])
        z = image
        img_interp_spline = RectBivariateSpline(x=x, y=y, z=image,bbox=[None, None, None, None],kx=3, ky=3,s=0  )
        return img_interp_spline



    def radonRayDrivenApproach(self,img_interp_spline,dSI,dDI,val,detectorSize,detectorSpacing,numProj):
        #rrd(img_interp_spline,dSI,dDI,val,detectorSize,detectorSpacing,numProj)

        fan_img = Image.new('RGB', (377, 377), "black")  # create a new black image
        pixels = fan_img.load()
        detectorSizeIndex = (detectorSize / detectorSpacing)
        gammaM = math.atan((detectorSize / 2.0 - 0.5) / dSI)
        angRange = val + 2 * gammaM
        angStepSize = angRange / numProj
        samplingRate = 3.0
        maxbetaindex = angRange / angStepSize
        # print(maxbetaindex)
        for i in np.arange(0, 10):
            # print(val)
            beta = val * i
            print(beta)
            cosBeta = math.cos(beta)
            sinBeta = math.sin(beta)
            source_x = dSI * (cosBeta)
            source_y = dSI * sinBeta
            PP_Point_x = -detectorSize / 2 * sinBeta
            PP_Point_y = detectorSize / 2 * (cosBeta)
            PP = (PP_Point_x, PP_Point_y)
            source = (source_x, source_y)
            PP_vector = np.array(PP) * (-cosBeta) + np.array(PP) * (-sinBeta)
            dirDetector = (PP) / np.linalg.norm(PP)
            #    print("dirDetector   ",dirDetector)
            for t in range(0, int(detectorSizeIndex)):
                stepsDirection = 0.5 * detectorSpacing + t * detectorSpacing
                #        print("stepsDirection   ",stepsDirection)
                P = np.array(PP) + (dirDetector * stepsDirection)
                points = (source, P)
                distance = math.hypot(PP_Point_x - source_x, PP_Point_y - source_y)
                #        print("distance  " , distance)
                x_coords, y_coords = zip(*points)
                A = vstack([x_coords, ones(len(x_coords))]).T
                m, c = lstsq(A, y_coords)[0]
                straightline = "{m}x + {c}".format(m=m, c=c)
                #        print (straightline)
                increment = 1.0 / distance * samplingRate
                sum = 0.0
                for Linet in np.arange(0.0, distance * samplingRate):
                    current = np.array(source) + increment * Linet
                    #           print("current    ", current)
                    phantomWidth = 377
                    phantomHeight = 377
                    if ((phantomWidth) <= ((current.item(0)) + 1)) or ((phantomHeight) <= ((current.item(1)) + 1)) \
                            or ((current.item(0)) < 0) or ((current.item(1)) < 0):
                        continue
                    # sum += img_interp_spline(current.item(0), current.item(1))
                    sum += interpolate.interp1d(source_x + 0.5, source_y + 0.5)
                sum /= samplingRate
                print("sum    ", sum)
                pixels = (i, t, sum)
        return fan_img

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
        self.image = np.asarray(Image.open(self.phantom_value[self.file_path]), dtype="int32")




    #slide bar with image movement
    def Phantom_Slider_Moved(self):
        self.hSlider_Phantom.valueChanged.connect(self.hslider_changed)


    def hslider_changed(self):
        self.hSlider_Phantom_value = self.hSlider_Phantom.value()
        self.rotation_triangle(self.hSlider_Phantom_value)

    def rotation_triangle(self, val):
        self.Line1.setTransformOriginPoint(QtCore.QPointF(self.pix_Phantom.width() / 2, self.pix_Phantom.height()/2 ))
        self.Line2.setTransformOriginPoint(QtCore.QPointF(self.pix_Phantom.width() / 2, self.pix_Phantom.height()/2 ))
        self.Line3.setTransformOriginPoint(QtCore.QPointF(self.pix_Phantom.width() / 2, self.pix_Phantom.height()/2))
        self.Ecllipse.setTransformOriginPoint(QtCore.QPointF(self.pix_Phantom.width() / 2, self.pix_Phantom.height()/2 ))
        self.Line1.setRotation(val)
        self.Line2.setRotation(val)
        self.Line3.setRotation(val)
        self.Ecllipse.setRotation(val)
        fanbeam_main.radonRayDrivenApproach(self,fanbeam_main.interpolation_Image(self,self.image),231.2,105,val,318,1,377)





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

















































































































































































































































