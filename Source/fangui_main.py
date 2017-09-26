from __future__ import division
from __future__ import print_function
from PIL import Image
from PyQt5 import QtCore, QtGui, QtWidgets
from Source.fanGUI_Project import Ui_ReconstructionGUI
from Source.PhantomSelect_Window import selectPhantom
from pyconrad import *
import math
import numpy as np
import qimage2ndarray
import scipy.misc
import sys



jvm = PyConrad()
jvm.setup()
jvm.add_import('edu.stanford.rsl.conrad.data.numeric')
jvm.add_import('edu.stanford.rsl.tutorial.phantoms')
jvm.add_import('edu.stanford.rsl.conrad.phantom')

#Pyconrad
pyconrad = PyConrad()
pyconrad.setup()
pyconrad.start_conrad()


class fanbeam_main(Ui_ReconstructionGUI):
    use_cl = True

    phantom_value = {}
    file_path = 'NULL'


    def __init__(self, MainWindow):

        Ui_ReconstructionGUI.__init__(self)
        self.setupUi(MainWindow)


        self.connect_threads()
        self.PhantomSelect_click()
        self.Xray_Clicked()
        self.Reconst_Clicked()
        self.Parkerweight_Check()
        self.Ramlak_Check()

    a=10

    def connect_threads(self):
        from Source.Threads.forward_projection_thread import forward_project_thread as fpt
        self.forward = fpt()
        #self.forward.finished.connect(self.on_fw_projection_finished)
        self.forward.forward_project_finsihed.connect(self.on_fw_projection_finished)

        from Source.Threads.back_projection_thread import back_project_thread as bpt
        self.backward = bpt()
        self.backward.back_project_finsihed.connect(self.on_bw_projection_finished)
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
        self.PhantomFFT()
        self.selectPhan_Window.close()

    #Function for loading the phantom
    def Phantom_load(self):
        img_Phantom = QtGui.QImage(self.phantom_value[self.file_path])
        img_Phantom = img_Phantom.scaled(self.gV_Phantom.size(), aspectRatioMode=QtCore.Qt.KeepAspectRatio,transformMode=QtCore.Qt.SmoothTransformation)
        self.pix_Phantom = QtGui.QPixmap(img_Phantom)
        self.gps_Phantom_placeholder = QtWidgets.QGraphicsPixmapItem(self.pix_Phantom)
        self.gps_Phantom = QtWidgets.QGraphicsPixmapItem(self.pix_Phantom)
        #self.gps_Line = QtWidgets.QGraphicsLineItem()
        self.gs_Phantom = QtWidgets.QGraphicsScene()
        self.gs_Phantom.clear()
        self.gs_Phantom.addItem(self.gps_Phantom)
        #self.Ecllipse = self.gs_Phantom.addEllipse(0,0,25,25,QtCore.Qt.white)
        #self.Line1 = self.gs_Phantom.addLine(20, 20, 150, 375, QtCore.Qt.white)
        #self.Line2 = self.gs_Phantom.addLine(20, 20, 375,150, QtCore.Qt.white)
        #self.Line3 = self.gs_Phantom.addLine(150, 375, 375, 150, QtCore.Qt.white)
        self.gV_Phantom.setScene(self.gs_Phantom)
        self.gV_Phantom.setStyleSheet("background:black")
        self.gs_Phantom.update()
        self.image = Image.open(self.phantom_value[self.file_path])

    ####Fourier transform of the phantom
    def PhantomFFT(self):
        self.PhantomFFT_image = jvm['Grid2D'].from_numpy(np.array(self.image))
        grid2dcomplex = pyconrad.classes.stanford.rsl.conrad.data.numeric.Grid2DComplex(self.PhantomFFT_image)
        grid2dcomplex.transformForward()
        grid2dcomplex.fftshift()
        grid2dcomplex.show("grid2complex display2")

        #PhantomFFTarray = grid2dcomplex.as_numpy()
        #self.gs_PhantomFFT = QtWidgets.QGraphicsScene()
        #self.gs_PhantomFFT.addPixmap(QtGui.QPixmap.fromImage(qimage2ndarray.array2qimage(PhantomFFTarray)).scaled(self.gV_Phantom_FFT.size(),
        #                                                                                                     aspectRatioMode=QtCore.Qt.KeepAspectRatio,
        #                                                                                                    transformMode=QtCore.Qt.SmoothTransformation))
        #self.gV_Phantom_FFT.setScene(self.gs_PhantomFFT)

    #Xray button click for forward projection
    def Xray_Clicked(self):
        self.pB_Xray.clicked.connect(self.forwardProj)


    ####forward projection
    def forwardProj(self):

        ####Declare Variables
        self.maxT = (float)(600)
        self.focalLength = (float)(500)
        self.gammaM = math.atan((self.maxT / 2.0 - 0.5) / self.focalLength)
        self.deltaT = (float)(1.0)
        self.numProj = 500
        self.maxBeta = math.pi + 2 * self.gammaM
        self.deltaBeta = (float)(self.maxBeta / self.numProj)


        ####convert the input Phantom to array and set origin and spacing
        Phantom = jvm['Grid2D'].from_numpy(np.array(self.image))
        self.Phantomwidth = Phantom.getWidth()
        self.Phantomheight = Phantom.getHeight()
        Phantom.setOrigin(JArray(JDouble)([-(self.Phantomwidth * Phantom.getSpacing()[0]) / 2, -(self.Phantomheight * Phantom.getSpacing()[1]) / 2]))
        Phantom.setSpacing(JArray(JDouble)([self.deltaT, self.deltaT]))
        Phantom.show("Phantom")


        ####Forward Projection
        ForwardProj = pyconrad.classes.stanford.rsl.tutorial.fan.FanBeamProjector2D(self.focalLength, self.maxBeta, self.deltaBeta, self.maxT, self.deltaT)




        self.forward.init(self.use_cl, ForwardProj, Phantom)

        print('befor')
        self.forward.run()
        print('agert')
       # if self.use_cl:
        #    self.fanogram = ForwardProj.projectRayDrivenCL(Phantom)
       # else:
        #    self.fanogram = ForwardProj.projectRayDriven(Phantom)

    def on_fw_projection_finished(self):
        print('here')
        self.fanogram = self.forward.get_fanogram()
        self.fanogram_copy = self.fanogram
        self.fanogram.show("Fanogram before filtering")


        #load the fanogram image
        fanogramarray = self.fanogram.as_numpy()
        self.gs_fanogram = QtWidgets.QGraphicsScene()
        self.gs_fanogram.addPixmap(QtGui.QPixmap.fromImage(qimage2ndarray.array2qimage(fanogramarray)).scaled(self.gV_Sinogram.size(),aspectRatioMode=QtCore.Qt.KeepAspectRatio,transformMode=QtCore.Qt.SmoothTransformation))
        self.gV_Sinogram.setScene(self.gs_fanogram)
        self.gV_Sinogram.setStyleSheet("background:black")
        self.gs_fanogram.update()


    def Parkerweight_Check(self):
        self.checkBox_ParkerWeigh.stateChanged.connect(self.weightcheck)

    def weightcheck(self):
        if self.checkBox_ParkerWeigh.isChecked():
            self.parkerweight()
        else:
            self.fanogram = self.fanogram_copy

            self.fanogram.show()
            print("inside parker")

    def parkerweight(self):
        weight = pyconrad.classes.stanford.rsl.conrad.data.numeric.Grid2D(self.Phantomwidth, self.Phantomheight)
        weight = pyconrad.classes.stanford.rsl.tutorial.fan.redundancy.ParkerWeights(self.focalLength, self.maxT, self.deltaT, self.maxBeta,self.deltaBeta)
        pyconrad.classes.stanford.rsl.conrad.data.numeric.NumericPointwiseOperators.multiplyBy(self.fanogram, weight)
        weight.show()

    def Ramlak_Check(self):
        self.checkBox_RamLakFilter.stateChanged.connect(self.filtercheck)

    def filtercheck(self):
        if self.checkBox_RamLakFilter.isChecked():
            self.ramlakfilter()
        else:
            self.fanogram = self.fanogram_copy
            print("inside ramlak")

    def ramlakfilter(self):
        sizeimage = self.fanogram.getSize()
        ramlak = pyconrad.classes.stanford.rsl.tutorial.filters.RamLakKernel((int)(self.maxT / self.deltaT), self.deltaT)

        for theta in range(0, 500):
            ramlak.applyToGrid(self.fanogram.getSubGrid(theta))
        self.fanogram.show("After filtering")

    ####Clicking the reconstruction button
    def Reconst_Clicked(self):
        self.pB_Reconstruction.clicked.connect(self.BackProj)


    ###Backprojection
    def BackProj(self):

        Backprojection = pyconrad.classes.stanford.rsl.tutorial.fan.FanBeamBackprojector2D(self.focalLength, self.deltaT, self.deltaBeta, self.Phantomwidth,
                                                                                  self.Phantomheight)
        #baclpro = Test1.initSinogramParams(fanogram)
        self.backward.init(self.use_cl, Backprojection, self.fanogram)
        self.backward.run()
        #if self.use_cl:
        #    self.back = Backprojection.backprojectPixelDrivenCL(self.fanogram)
        #else:
        #    self.back = Backprojection.backprojectPixelDriven(self.fanogram)

    def on_bw_projection_finished(self):
        self.back = self.backward.get_backprojection()

        self.back.show("back projection")


        ######Display the backprojected image
        backarray = self.back.as_numpy()
        self.gs_backproj = QtWidgets.QGraphicsScene()
        self.gs_backproj.addPixmap(QtGui.QPixmap.fromImage(qimage2ndarray.array2qimage(backarray)).scaled(self.gV_Backproj.size(),aspectRatioMode=QtCore.Qt.KeepAspectRatio,transformMode=QtCore.Qt.SmoothTransformation))
        self.gV_Backproj.setScene(self.gs_backproj)
        self.gV_Backproj.setStyleSheet("background:black")
        self.gs_backproj.update()

        self.backFFT()

    ####Fourier transform of the phantom
    def backFFT(self):
        grid2dcomplex = pyconrad.classes.stanford.rsl.conrad.data.numeric.Grid2DComplex(self.back)
        grid2dcomplex.transformForward()
        grid2dcomplex.fftshift()
        grid2dcomplex.show("grid2complex display")

        #PhantomFFTarray = grid2dcomplex.as_numpy()
        #self.gs_PhantomFFT = QtWidgets.QGraphicsScene()
        #self.gs_PhantomFFT.addPixmap(
         #   QtGui.QPixmap.fromImage(qimage2ndarray.array2qimage(PhantomFFTarray)).scaled(self.gV_Phantom_FFT.size(),
          #                                                                               aspectRatioMode=QtCore.Qt.KeepAspectRatio,
           #                                                                              transformMode=QtCore.Qt.SmoothTransformation))
        #self.gV_Phantom_FFT.setScene(self.gs_PhantomFFT)

if __name__ == '__main__':


    app = QtWidgets.QApplication(sys.argv)
    wid_FanRecont = QtWidgets.QMainWindow()
    ui = fanbeam_main(wid_FanRecont)





    wid_FanRecont.show()
    sys.exit(app.exec_())

'''
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
        fanbeam_main.forwardProj(self)
'''