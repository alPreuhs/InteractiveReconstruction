from __future__ import division
from __future__ import print_function
from PIL import Image
from PyQt5 import QtCore, QtGui, QtWidgets
from Source.fanGUI_Project import Ui_ReconstructionGUI
from Source.PhantomSelect_Window import selectPhantom
from pyconrad import *
from skimage.io import imread, imsave
from skimage.color import rgb2gray, rgb2grey
from VideoCapture import Device
import math
import numpy as np
import qimage2ndarray
import scipy.misc
import sys
import pygame
import pygame.camera


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
        self.imagecapcheckflag  = 0
        self.ParkerCheckflag = 0
        self.ramlakCheckflag = 0
        self.cosineCheckflag = 0
        self.maxslidercheck = 0
        self.Imagecapture_check = 0
        self.maxT = (float)(1300)
        self.focalLength = (float)(2400)
        self.gammaM = math.atan((self.maxT / 2.0 - 0.5) / self.focalLength)
        self.deltaT = (float)(1.0)
        self.numProj = 1024

        self.maxBeta = math.pi + 2 * self.gammaM
        self.deltaBeta = (float)(self.maxBeta / self.numProj)
        self.connect_threads()
        self.imagecapture_click()
        self.PhantomSelect_click()
        self.Xray_Clicked()
        self.Reconst_Clicked()
        self.Parkerweight_Check()
        self.Ramlak_Check()
        self.cosine_Check()
        self.deltabetascroll()
        self.deltascrolltext()
        self.maxbetascroll()
        self.maxscrolltext()

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
        self.imagecapcheckflag = 1
        self.pB_videocapture.clicked.connect(self.imagecapture)

    ##Capturing the image
    def imagecapture(self):
        pygame.camera.init()
        pygame.camera.list_cameras()
        cam = pygame.camera.Camera()
        cam.start()
        img = cam.get_image()
        pygame.image.save(img, r'image.png')
        self.load_image()

    def load_image(self):
        self.Imagecapture_check = 1
        self.img = imread('image.png')
        img_gray = rgb2gray(self.img)
        imsave("greyscale.png", img_gray)
        img_Phantom = QtGui.QImage('greyscale.png')
        img_Phantom = img_Phantom.scaled(self.gV_Phantom.size(), aspectRatioMode=QtCore.Qt.KeepAspectRatioByExpanding,
                                         transformMode=QtCore.Qt.FastTransformation)
        self.pix_ImgPhantom = QtGui.QPixmap(img_Phantom)
        self.gps_ImgPhantom_placeholder = QtWidgets.QGraphicsPixmapItem(self.pix_ImgPhantom)
        self.gps_ImgPhantom = QtWidgets.QGraphicsPixmapItem(self.pix_ImgPhantom)
        self.gs_ImgPhantom = QtWidgets.QGraphicsScene()
        self.gs_ImgPhantom.clear()
        self.gs_ImgPhantom.addItem(self.gps_ImgPhantom)
        self.gV_Phantom.setScene(self.gs_ImgPhantom)
        self.gV_Phantom.setStyleSheet("background:black")
        self.gs_ImgPhantom.update()
        self.imagegray = Image.open('greyscale.png')
        #if self.Imagecapture_check == 1 :
        self.image = self.imagegray
        self.Imgcapture_FFT()

    def Imgcapture_FFT(self):
        self.ImgcaptureFFT = jvm['Grid2D'].from_numpy(np.array(self.imagegray))
        grid2dcomplex = pyconrad.classes.stanford.rsl.conrad.data.numeric.Grid2DComplex(self.ImgcaptureFFT)
        grid2dcomplex.transformForward()
        grid2dcomplex.fftshift()
        grid2dcomplex.show("grid2complex display2")
        gridimage = grid2dcomplex.getMagnSubGrid(0, 0, grid2dcomplex.getWidth(), grid2dcomplex.getHeight())
        self.ImgcaptureFFT = gridimage.as_numpy()
        max_PhantomFFTarray = np.max(self.ImgcaptureFFT)
        self.ImgcaptureFFT[self.ImgcaptureFFT < 0] = 0
        self.gs_PhantomFFT = QtWidgets.QGraphicsScene()
        self.gs_PhantomFFT.addPixmap(QtGui.QPixmap.fromImage(qimage2ndarray.array2qimage(np.uint16(self.ImgcaptureFFT/255)).scaled(self.gV_Phantom_FFT.size(),
                                                                               aspectRatioMode=QtCore.Qt.KeepAspectRatio,
                                                                               transformMode=QtCore.Qt.FastTransformation)))

        self.gV_Phantom_FFT.setScene(self.gs_PhantomFFT)
        self.gV_Phantom_FFT.fitInView(self.gs_PhantomFFT.sceneRect())
        self.gV_Phantom_FFT.setStyleSheet("background:black")
        self.gs_PhantomFFT.update()

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
        self.gs_Phantom = QtWidgets.QGraphicsScene()
        self.gs_Phantom.clear()
        self.gs_Phantom.addItem(self.gps_Phantom)
        self.gV_Phantom.setScene(self.gs_Phantom)
        self.gV_Phantom.setStyleSheet("background:black")
        self.gs_Phantom.update()
        #if self.Imagecapture_check == 0 :
        self.image = Image.open(self.phantom_value[self.file_path])

       #else :
            #self.image = self.imagegray



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
        max_PhantomFFTarray = np.max(PhantomFFTarray)
        PhantomFFTarray[PhantomFFTarray<0] = 0

        print(max_PhantomFFTarray)

        self.gs_PhantomFFT = QtWidgets.QGraphicsScene()
        self.gs_PhantomFFT.addPixmap(QtGui.QPixmap.fromImage(qimage2ndarray.array2qimage(np.uint16(PhantomFFTarray/255)).scaled(self.gV_Phantom_FFT.size(),aspectRatioMode=QtCore.Qt.KeepAspectRatio,transformMode=QtCore.Qt.FastTransformation)))

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
        self.fanogram_copy = jvm['Grid2D']
        self.fanogram_copy = self.fanogram.clone()
        self.fanogram_copy.show("Fanogram before filtering")
        if self.ParkerCheckflag == 1:
            self.parkerweight()
            self.fanogram = self.fanogram_parkerweig
        if self.cosineCheckflag == 1:
            self.cosinefilter()
            self.fanogram = self.fanogram_cosine
        if self.ramlakCheckflag == 1:
            self.ramlakfilter()
            self.fanogram = self.fanogram_ramlak

        self.fan_load()


    def fan_load(self):

        #load the fanogram image
        fanogramarray = self.fanogram.as_numpy()
        self.gs_fanogram = QtWidgets.QGraphicsScene()
        pixmap =  QtGui.QPixmap.fromImage(qimage2ndarray.array2qimage(np.uint16(fanogramarray / 200)))
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
            self.ParkerCheckflag = 1
        else:
            self.fanogram = self.fanogram_copy
            self.fanogram.show("uncheck")
            self.ParkerCheckflag = 0
            self.fan_load()

    def parkerweight(self):
        #weight = pyconrad.classes.stanford.rsl.conrad.data.numeric.Grid2D(self.Phantomwidth, self.Phantomheight)
        weight = pyconrad.classes.stanford.rsl.tutorial.fan.redundancy.ParkerWeights(self.focalLength, self.maxT, self.deltaT, self.maxBeta,self.deltaBeta)
        pyconrad.classes.stanford.rsl.conrad.data.numeric.NumericPointwiseOperators.multiplyBy(self.fanogram, weight)
        self.fanogram_parkerweig = jvm['Grid2D']
        self.fanogram_parkerweig = self.fanogram
        self.fan_load()
        weight.show()

    def Ramlak_Check(self):
        self.checkBox_RamLakFilter.stateChanged.connect(self.filtercheck)

    def filtercheck(self):
        if self.checkBox_RamLakFilter.isChecked():
            self.ramlakfilter()
            self.fan_load()
            self.ramlakCheckflag = 1
        else:
            self.fanogram = self.fanogram_copy
            self.fanogram.show("uncheck")
            self.ramlakCheckflag = 0
            self.fan_load()


    def ramlakfilter(self):
        sizeimage = self.fanogram.getSize()[1]
        ramlak = pyconrad.classes.stanford.rsl.tutorial.filters.RamLakKernel((int)(self.maxT / self.deltaT), self.deltaT)
        print(sizeimage)
        for theta in range(0, sizeimage):
            ramlak.applyToGrid(self.fanogram.getSubGrid(theta))
        self.fanogram.show("After  ramlak filtering")
        self.fanogram_ramlak = jvm['Grid2D']
        self.fanogram_ramlak = self.fanogram

    def cosine_Check(self):
        self.checkBox_cosine.stateChanged.connect(self.cosinecheck)

    def cosinecheck(self):
        if self.checkBox_cosine.isChecked():
            self.cosinefilter()
            self.cosineCheckflag = 1
            self.fan_load()
        else:
            self.fanogram = self.fanogram_copy
            self.fanogram.show("uncheck")
            self.cosineCheckflag = 0
            self.fan_load()


    def cosinefilter(self):
        sizeimage = self.fanogram.getSize()[1]
        cosine = pyconrad.classes.stanford.rsl.tutorial.fan.CosineFilter(self.focalLength, self.maxT, self.deltaT)
        print(sizeimage)
        for theta in range(0, sizeimage):
            cosine.applyToGrid(self.fanogram.getSubGrid(theta))
        self.fanogram.show("After cosine filtering")
        self.fanogram_cosine = jvm['Grid2D']
        self.fanogram_cosine = self.fanogram

    def deltabetascroll(self):
        self.hScrollBar_deltabeta.valueChanged.connect(self.deltabetaValue)

    def deltascrolltext(self):
        self.hScrollBar_deltabeta.valueChanged.connect(self.deltabetatext)

    def deltabetaValue(self):
        self.numProjSlider = self.hScrollBar_deltabeta.value()
        self.slidercheck = 1

    def deltabetatext(self):
        #self.label_delta.setAlignment((QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter))
        self.label_delta.setText("Sampling density: {}/{}".format(self.hScrollBar_deltabeta.maximum(),self.numProjSlider))

    def maxbetascroll(self):
        self.hScrollBar_maxbeta.valueChanged.connect(self.maxbetaValue)

    def maxscrolltext(self):
        self.hScrollBar_maxbeta.valueChanged.connect(self.maxbetatext)

    def maxbetaValue(self):
        self.maxSlider = self.hScrollBar_maxbeta.value()
        self.maxslidercheck = 1

    def maxbetatext(self):
        #self.label_max.setAlignment((QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter))
        self.label_max.setText("Rotation Angle: {}/{}".format(self.hScrollBar_maxbeta.maximum(),self.maxSlider))

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
        print("test")
        ######Display the backprojected image
        backarray = self.back.as_numpy()
        low_values_indices = backarray < 0

        backarray[low_values_indices] = 0


        self.gs_backproj = QtWidgets.QGraphicsScene()
        if self.ParkerCheckflag == 0 or self.cosineCheckflag == 0 or self.ramlakCheckflag == 0 :
           self.gs_backproj.addPixmap(QtGui.QPixmap.fromImage(qimage2ndarray.array2qimage(np.uint16(backarray/300)).scaled(self.gV_Backproj.size(),aspectRatioMode=QtCore.Qt.KeepAspectRatio,transformMode=QtCore.Qt.SmoothTransformation)))
        elif self.imagecapcheckflag == 1:
           self.gs_backproj.addPixmap(QtGui.QPixmap.fromImage(qimage2ndarray.array2qimage(backarray/255).scaled(self.gV_Backproj.size(),aspectRatioMode=QtCore.Qt.KeepAspectRatio,transformMode=QtCore.Qt.SmoothTransformation)))
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
        grid2dcomplex.show("grid2complex back display")
        ####convert complex grid 2d to grid 2d
        gridimage = grid2dcomplex.getMagnSubGrid(0, 0, grid2dcomplex.getWidth(), grid2dcomplex.getHeight())
        backFFTarray = gridimage.as_numpy()
        backFFTarray[backFFTarray<0] = 0
        max_backFFTarray = np.max(backFFTarray)
        self.gs_backFFT = QtWidgets.QGraphicsScene()
        self.gs_backFFT.addPixmap(QtGui.QPixmap.fromImage(qimage2ndarray.array2qimage(np.uint16(backFFTarray*255))))
        self.gV_Backproj_FFT.setScene(self.gs_PhantomFFT)
        self.gV_Backproj_FFT.setStyleSheet("background:black")
        self.gs_backFFT.update()

if __name__ == '__main__':


    app = QtWidgets.QApplication(sys.argv)
    wid_FanRecont = QtWidgets.QMainWindow()
    ui = fanbeam_main(wid_FanRecont)
    wid_FanRecont.show()
    sys.exit(app.exec_())

