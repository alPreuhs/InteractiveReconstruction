from __future__ import division
from __future__ import print_function
from PIL import Image
from PyQt5 import QtCore, QtGui, QtWidgets
from Source.fanGUI_Project import Ui_ReconstructionGUI
from Source.PhantomSelect_Window import selectPhantom
from pyconrad import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from VideoCapture import Device
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


        ####Declare Variables
        self.slidercheck = 0
        self.maxslidercheck = 0
        self.Imagecapture_check = 0
        self.maxT = (float)(512)
        self.focalLength = (float)(500)
        self.gammaM = math.atan((self.maxT / 2.0 - 0.5) / self.focalLength)
        self.deltaT = (float)(1.0)
        self.numProj = 50

        self.maxBeta = math.pi + 2 * self.gammaM
        self.deltaBeta = (float)(self.maxBeta / self.numProj)
        self.connect_threads()
        self.imagecapture_click()
        self.PhantomSelect_click()
        self.Xray_Clicked()
        self.Reconst_Clicked()
        self.Parkerweight_Check()
        self.Ramlak_Check()
        self.deltabetaslider()
        self.deltaslidertext()
        self.maxbetaslider()
        self.maxslidertext()

    a=10

    def connect_threads(self):
        from Source.Threads.forward_projection_thread import forward_project_thread as fpt
        self.forward = fpt()
        #self.forward.finished.connect(self.on_fw_projection_finished)
        self.forward.forward_project_finsihed.connect(self.on_fw_projection_finished)

        from Source.Threads.back_projection_thread import back_project_thread as bpt
        self.backward = bpt()
        self.backward.back_project_finsihed.connect(self.on_bw_projection_finished)


    ##Logic for clicking the live image capture button
    def imagecapture_click(self):
        self.pB_videocapture.clicked.connect(self.imagecapture)

    ##Capturing the image
    def imagecapture(self):
        cam = Device()
        cam.saveSnapshot('image.png')
        self.load_image()

    def load_image(self):
        self.Imagecapture_check = 0
        self.img = Image.open('image.png').convert('LA')
        self.matrix = scipy.misc.fromimage(self.img,0)
        self.img.save('greyscale.png')
        print (self.matrix)
        img_Phantom = QtGui.QImage('greyscale.png')
        img_Phantom = img_Phantom.scaled(self.gV_Phantom.size(), aspectRatioMode=QtCore.Qt.KeepAspectRatioByExpanding,
                                         transformMode=QtCore.Qt.FastTransformation)
        self.pix_Phantom = QtGui.QPixmap(img_Phantom)
        self.gps_Phantom_placeholder = QtWidgets.QGraphicsPixmapItem(self.pix_Phantom)
        self.gps_Phantom = QtWidgets.QGraphicsPixmapItem(self.pix_Phantom)
        # self.gps_Line = QtWidgets.QGraphicsLineItem()
        self.gs_Phantom = QtWidgets.QGraphicsScene()
        self.gs_Phantom.clear()
        self.gs_Phantom.addItem(self.gps_Phantom)
        self.gV_Phantom.setScene(self.gs_Phantom)
        self.gV_Phantom.setStyleSheet("background:black")
        self.gs_Phantom.update()
        self.image = Image.open('greyscale.png')
        self.Imgcapture_FFT()

    def Imgcapture_FFT(self):
        self.ImgcaptureFFT = jvm['Grid2D'].from_numpy(np.array(self.matrix))
        grid2dcomplex = pyconrad.classes.stanford.rsl.conrad.data.numeric.Grid2DComplex(self.ImgcaptureFFT)
        grid2dcomplex.transformForward()
        grid2dcomplex.fftshift()
        grid2dcomplex.show("grid2complex display2")

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
        img_Phantom = img_Phantom.scaled(self.gV_Phantom.size(), aspectRatioMode=QtCore.Qt.KeepAspectRatioByExpanding,transformMode=QtCore.Qt.FastTransformation)
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
        if self.Imagecapture_check == 0 :
            self.image = Image.open(self.phantom_value[self.file_path])

        else :
            self.image = Image.open('greyscale.png')



    ####Fourier transform of the phantom
    def PhantomFFT(self):
        self.PhantomFFT_image = jvm['Grid2D'].from_numpy(np.array(self.image))
        grid2dcomplex = pyconrad.classes.stanford.rsl.conrad.data.numeric.Grid2DComplex(self.PhantomFFT_image)
        grid2dcomplex.transformForward()
        grid2dcomplex.fftshift()
        grid2dcomplex.show("grid2complex display2")

        ####convert complex grid 2d to grid 2d
        gridimage = grid2dcomplex.getMagnSubGrid(0, 0, grid2dcomplex.getHeight(), grid2dcomplex.getWidth())

        PhantomFFTarray = gridimage.as_numpy()
        low_values_indices = PhantomFFTarray < 0
        PhantomFFTarray[low_values_indices] = 0
        max_PhantomFFTarray = np.amax(PhantomFFTarray)
        print(max_PhantomFFTarray)


        self.gs_PhantomFFT = QtWidgets.QGraphicsScene()
        self.gs_PhantomFFT.addPixmap(QtGui.QPixmap.fromImage(qimage2ndarray.array2qimage(np.uint8(PhantomFFTarray/90)).scaled(self.gV_Phantom_FFT.size(),aspectRatioMode=QtCore.Qt.KeepAspectRatio,transformMode=QtCore.Qt.FastTransformation)))

        self.gV_Phantom_FFT.setScene(self.gs_PhantomFFT)
        self.gV_Phantom_FFT.fitInView(self.gs_PhantomFFT.sceneRect())
        self.gV_Phantom_FFT.setStyleSheet("background:black")
        self.gs_PhantomFFT.update()

    #Xray button click for forward projection
    def Xray_Clicked(self):
        self.pB_Xray.clicked.connect(self.forwardProj)


    ####forward projection
    def forwardProj(self):
        if self.slidercheck == 1 and self.maxslidercheck == 0:
            self.deltaBeta = (float)(self.maxBeta / self.numProjSlider)
        elif  self.slidercheck == 1 and self.maxslidercheck == 1:
            self.deltaBeta = (float)((math.radians(self.maxSlider)/ self.numProjSlider))
        elif self.slidercheck == 0 and self.maxslidercheck == 1:
            self.deltaBeta = (float)((math.radians(self.maxSlider) / self.numProj))
        else :
            self.deltaBeta = (float)(self.maxBeta / self.numProj)

        if self.maxslidercheck == 1 :
            self.maxBeta = math.radians(self.maxSlider)
          #  self.deltaBeta = (float)(self.maxBeta / self.numProj)
           # print(self.maxBeta)

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
        print("test")
        self.forward.run()

       # if self.use_cl:
        #    self.fanogram = ForwardProj.projectRayDrivenCL(Phantom)
       # else:
        #    self.fanogram = ForwardProj.projectRayDriven(Phantom)

    def on_fw_projection_finished(self):
        self.fanogram = self.forward.get_fanogram()
        self.Checkflag = 0
        self.fanogram_copy = jvm['Grid2D']
        self.fanogram_copy = self.fanogram.clone()
        self.fanogram_copy.show("Fanogram before filtering")


        #load the fanogram image
        fanogramarray = self.fanogram.as_numpy()
        self.gs_fanogram = QtWidgets.QGraphicsScene()
        pixmap =  QtGui.QPixmap.fromImage(qimage2ndarray.array2qimage(np.uint8(fanogramarray / 255)))
        pixmap = pixmap.scaled(self.gV_Sinogram.size(), aspectRatioMode=QtCore.Qt.KeepAspectRatio,
            transformMode=QtCore.Qt.FastTransformation)
        self.gs_fanogram.addPixmap(pixmap)
        self.gV_Sinogram.setScene(self.gs_fanogram)
        self.gV_Sinogram.setStyleSheet("background:black")
        self.gs_fanogram.update()
        self.fanFFT()

    def fanFFT(self):
        grid2dcomplex = pyconrad.classes.stanford.rsl.conrad.data.numeric.Grid2DComplex(self.fanogram)
        grid2dcomplex.transformForward()
        grid2dcomplex.fftshift()
        grid2dcomplex.show("grid2complex display")
        ####convert complex grid 2d to grid 2d
        print(grid2dcomplex.getHeight())

        gridimage = grid2dcomplex.getMagnSubGrid(0, 0, grid2dcomplex.getWidth(), grid2dcomplex.getHeight())
        fanFFTarray = gridimage.as_numpy()
        low_values_indices = fanFFTarray < 0
        fanFFTarray[low_values_indices] = 0

        self.gs_fanFFT = QtWidgets.QGraphicsScene()
        self.gs_fanFFT.addPixmap(QtGui.QPixmap.fromImage(qimage2ndarray.array2qimage(np.uint8(fanFFTarray/255)).scaled(self.gV_SinogramFFT.size(),
                                                                                       aspectRatioMode=QtCore.Qt.KeepAspectRatio,
                                                                                       transformMode=QtCore.Qt.SmoothTransformation)))
        self.gV_SinogramFFT.setScene(self.gs_fanFFT)
        self.gV_SinogramFFT.setStyleSheet("background:black")
        self.gs_fanFFT.update()


    def Parkerweight_Check(self):
        self.checkBox_ParkerWeigh.stateChanged.connect(self.weightcheck)

    def weightcheck(self):
        if self.checkBox_ParkerWeigh.isChecked():
            self.parkerweight()
            self.Checkflag = 1
        else:
            self.fanogram = self.fanogram_copy
            self.fanogram.show("uncheck")
            self.Checkflag = 0

    def parkerweight(self):
        #weight = pyconrad.classes.stanford.rsl.conrad.data.numeric.Grid2D(self.Phantomwidth, self.Phantomheight)
        weight = pyconrad.classes.stanford.rsl.tutorial.fan.redundancy.ParkerWeights(self.focalLength, self.maxT, self.deltaT, self.maxBeta,self.deltaBeta)
        pyconrad.classes.stanford.rsl.conrad.data.numeric.NumericPointwiseOperators.multiplyBy(self.fanogram, weight)
        weight.show()

    def Ramlak_Check(self):
        self.checkBox_RamLakFilter.stateChanged.connect(self.filtercheck)

    def filtercheck(self):
        if self.checkBox_RamLakFilter.isChecked():
            self.ramlakfilter()
            self.Checkflag = 1
        else:
            self.fanogram = self.fanogram_copy
            self.fanogram.show("uncheck")
            self.Checkflag = 0


    def ramlakfilter(self):
        sizeimage = self.fanogram.getSize()[1]
        ramlak = pyconrad.classes.stanford.rsl.tutorial.filters.RamLakKernel((int)(self.maxT / self.deltaT), self.deltaT)
        print(sizeimage)
        for theta in range(0, sizeimage):
            ramlak.applyToGrid(self.fanogram.getSubGrid(theta))
        self.fanogram.show("After filtering")

    def cosine_Check(self):
        self.checkBox_cosine.stateChanged.connect(self.cosinecheck)

    def cosinecheck(self):
        if self.checkBox_cosine.isChecked():
            self.cosinefilter()
            self.Checkflag = 1
        else:
            self.fanogram = self.fanogram_copy
            self.fanogram.show("uncheck")
            self.Checkflag = 0


    def cosinefilter(self):
        sizeimage = self.fanogram.getSize()[1]
        cosine = pyconrad.classes.stanford.rsl.tutorial.fan.CosineFilter(self.focalLength, self.maxT, self.deltaT)
        print(sizeimage)
        for theta in range(0, sizeimage):
            cosine.applyToGrid(self.fanogram.getSubGrid(theta))
        self.fanogram.show("After filtering")

    def deltabetaslider(self):
        self.hSlider_deltabeta.valueChanged.connect(self.deltabetaValue)

    def deltaslidertext(self):
        self.hSlider_deltabeta.valueChanged.connect(self.deltabetatext)

    def deltabetaValue(self):
        self.numProjSlider = self.hSlider_deltabeta.value()
        self.slidercheck = 1
        self.forwardProj()

    def deltabetatext(self):
        self.label_Hslidervalue.setAlignment((QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter))
        self.label_Hslidervalue.setText("Stepsize: {}/{}".format(self.hSlider_deltabeta.maximum(),self.numProjSlider))

    def maxbetaslider(self):
        self.vSlider_maxbeta.valueChanged.connect(self.maxbetaValue)

    def maxslidertext(self):
        self.vSlider_maxbeta.valueChanged.connect(self.maxbetatext)

    def maxbetaValue(self):
        self.maxSlider = self.vSlider_maxbeta.value()
        self.maxslidercheck = 1
        self.forwardProj()

    def maxbetatext(self):
        self.label_Vslidervalue.setAlignment((QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter))
        self.label_Vslidervalue.setText("Rotation Angle: {}/{}".format(self.vSlider_maxbeta.maximum(),self.maxSlider))

    ####Clicking the reconstruction button
    def Reconst_Clicked(self):
        self.pB_Reconstruction.clicked.connect(self.BackProj)


    ###Backprojection
    def BackProj(self):
        if self.slidercheck == 1 and self.maxslidercheck == 0:
            self.deltaBeta = (float)(self.maxBeta / self.numProjSlider)
        elif  self.slidercheck == 1 and self.maxslidercheck == 1:
            self.deltaBeta = (float)((math.radians(self.maxSlider)/ self.numProjSlider))
        elif self.slidercheck == 0 and self.maxslidercheck == 1:
            self.deltaBeta = (float)((math.radians(self.maxSlider) / self.numProj))
        else :
            self.deltaBeta = (float)(self.maxBeta / self.numProj)

        Backprojection = pyconrad.classes.stanford.rsl.tutorial.fan.FanBeamBackprojector2D(self.focalLength, self.deltaT, self.deltaBeta, self.Phantomwidth,
                                                                                  self.Phantomheight)
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
        if self.Checkflag == 0 :
           self.gs_backproj.addPixmap(QtGui.QPixmap.fromImage(qimage2ndarray.array2qimage(np.uint8(backarray/255)).scaled(self.gV_Backproj.size(),aspectRatioMode=QtCore.Qt.KeepAspectRatio,transformMode=QtCore.Qt.SmoothTransformation)))
        else :
           self.gs_backproj.addPixmap(QtGui.QPixmap.fromImage(qimage2ndarray.array2qimage(backarray).scaled(self.gV_Backproj.size(),aspectRatioMode=QtCore.Qt.KeepAspectRatio,transformMode=QtCore.Qt.SmoothTransformation)))
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
        ####convert complex grid 2d to grid 2d
        gridimage = grid2dcomplex.getMagnSubGrid(0, 0, grid2dcomplex.getHeight(), grid2dcomplex.getWidth())
        backFFTarray = gridimage.as_numpy()
        self.gs_backFFT = QtWidgets.QGraphicsScene()
        self.gs_backFFT.addPixmap(QtGui.QPixmap.fromImage(qimage2ndarray.array2qimage(np.uint8(backFFTarray/90)).scaled(self.gV_Backproj_FFT.size(),
                                                                                        aspectRatioMode=QtCore.Qt.KeepAspectRatio,
                                                                                        transformMode=QtCore.Qt.SmoothTransformation)))
        self.gV_Backproj_FFT.setScene(self.gs_PhantomFFT)
        self.gV_Backproj_FFT.setStyleSheet("background:black")
        self.gs_backFFT.update()

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