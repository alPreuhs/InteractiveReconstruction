from PIL import Image
from PyQt5 import QtCore, QtGui, QtWidgets
from fanGUI_Project import Ui_ReconstructionGUI
from PhantomSelect_Window import selectPhantom
from pyconrad import *
from skimage.io import imread, imsave
from skimage.color import rgb2gray
import math
import numpy as np
import qimage2ndarray
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
        self.MainWindow = MainWindow

        #        self.MainWindow.connect(self.MainWindow, QtCore.PYQT_SIGNAL('resizeEvent()',self.test))
        ##somehow tracback is disabled by default,
        ##the following reactivats it
        def excepthook(type_, value, traceback_):
            traceback.print_exception(type_, value, traceback_)
            QtCore.qFatal('')

        sys.excepthook = excepthook

        self.gv_dict = {}
        Ui_ReconstructionGUI.__init__(self)
        self.setupUi(self.MainWindow)
        self.MainWindow.resized.connect(self.resizeEvent)
        self.MainWindow.dd.connect(self.asd)


        self.set_parameters()
        self.define_xray_projection()
        self.connect_threads()
        self.connect_buttons()
        self.connect_checkboxes()
        self.connect_slider()
        self.disable_sliders_on_start()

        self.gV_Phantom.photoClicked.connect(self.on_open_phantom)

        self.gV_Phantom_FFT.photoClicked.connect(self.on_open_phantom_fft)

        self.gV_Sinogram.photoClicked.connect(self.on_open_sinogram)

        self.gV_SinogramFFT.photoClicked.connect(self.on_open_sinogram_fft)

        self.gV_Backproj.photoClicked.connect(self.on_open_back)

        self.gV_Backproj_FFT.photoClicked.connect(self.on_open_back_fft)

    def on_open_phantom(self,point):
        if self.phantom_loaded:
            jvm['Grid2D'].from_numpy(self.phantom_grayscale).show();

    def on_open_phantom_fft(self, point):
        if self.phantom_fft_loaded:
            jvm['Grid2D'].from_numpy(self.phantom_fft).show();


    def on_open_sinogram(self, point):
        if self.sinogram_loaded:
            jvm['Grid2D'].from_numpy(self.fanogramarray).show();

    def on_open_sinogram_fft(self, point):
        if self.sino_fft_loaded:
            jvm['Grid2D'].from_numpy(self.fanFFTarray).show();

    def on_open_back(self, point):
        if self.back_loaded:
            jvm['Grid2D'].from_numpy(self.backarray).show();

    def on_open_back_fft(self, point):
        if self.back_fft_loaded:
            jvm['Grid2D'].from_numpy(self.backFFTarray).show();

    def asd(self):
        print('ebfsebfshbfjhsebfshe')

    def disable_sliders_on_start(self):
        self.pB_Xray.setDisabled(True)
        self.hScrollBar_deltabeta.setDisabled(True)
        self.hScrollBar_maxbeta.setDisabled(True)
        self.checkBox_cosine.setDisabled(True)
        self.checkBox_RamLakFilter.setDisabled(True)
        ###t missing....
        self.checkBox_ParkerWeigh.setDisabled(True)
        self.pB_Reconstruction.setDisabled(True)

    def connect_slider(self):
        ## delta beta slider
        self.hScrollBar_deltabeta.valueChanged.connect(self.deltabetaValue)
        self.hScrollBar_deltabeta.valueChanged.connect(self.deltabetatext)
        ## max beta slider
        self.hScrollBar_maxbeta.valueChanged.connect(self.maxbetaValue)
        self.hScrollBar_maxbeta.valueChanged.connect(self.maxbetatext)

    def connect_checkboxes(self):
        #parker weights
        self.checkBox_ParkerWeigh.stateChanged.connect(self.weightcheck)
        #ramLakFilter
        self.checkBox_RamLakFilter.stateChanged.connect(self.filtercheck)
        #cosine weight
        self.checkBox_cosine.stateChanged.connect(self.cosinecheck)

    def connect_buttons(self):
        ##capture image
        self.imagecapcheckflag = 1
        self.pB_videocapture.clicked.connect(self.imagecapture)
        ##Select Phantom
        self.pB_PhantomSelect.clicked.connect(self.selectphantom)
        ##X-ray
        self.pB_Xray.clicked.connect(self.forwardProj)
        ##reconstruction_clicked
        self.pB_Reconstruction.clicked.connect(self.BackProj)

    def define_xray_projection(self):
        self.maxT = (float)(1300)
        self.focalLength = (float)(2400)
        self.gammaM = math.atan((self.maxT / 2.0 - 0.5) / self.focalLength)
        self.deltaT = (float)(1.0)
        self.numProj = 1024
        self.maxBeta = math.pi + 2 * self.gammaM
        self.deltaBeta = (float)(self.maxBeta / self.numProj)

    def set_parameters(self):
        self.phantom_loaded = False
        self.phantom_fft_loaded = False
        self.sinogram_loaded = False
        self.sino_fft_loaded = False
        self.back_loaded = False
        self.back_fft_loaded = False
        self.slidercheck = 0
        self.imagecapcheckflag = 0
        self.ParkerCheckflag = 0
        self.ramlakCheckflag = 0
        self.cosineCheckflag = 0
        self.maxslidercheck = 0



    def connect_threads(self):
        from Source.Threads.forward_projection_thread import forward_project_thread as fpt
        self.forward = fpt()
        #self.forward.finished.connect(self.on_fw_projection_finished)
        self.forward.forward_project_finsihed.connect(self.on_fw_projection_finished)

        from Source.Threads.back_projection_thread import back_project_thread as bpt
        self.backward = bpt()
        self.backward.back_project_finsihed.connect(self.on_bw_projection_finished)

    def resizeEvent(self):
        #if self.pixmap_phantom:
       #     print('yes yes')
        print('on resize')
        if self.phantom_loaded:
            self.gV_Phantom.fitInView(self.gpi_phantom.boundingRect(), QtCore.Qt.KeepAspectRatio)
        if self.phantom_fft_loaded:
            self.gV_Phantom_FFT.fitInView(self.gpi_phantom_fft.boundingRect(), QtCore.Qt.KeepAspectRatio)
        if self.sinogram_loaded:
            self.gV_Sinogram.fitInView(self.gpi_sino.boundingRect(), QtCore.Qt.KeepAspectRatio)
        if self.sino_fft_loaded:
            self.gV_SinogramFFT.fitInView(self.gpi_sino_fft.boundingRect(), QtCore.Qt.KeepAspectRatio)
        if self.back_loaded:
            self.gV_Backproj.fitInView(self.gpi_back.boundingRect(), QtCore.Qt.KeepAspectRatio)
        if self.back_fft_loaded:
            self.gV_Backproj_FFT.fitInView(self.gpi_back_fft.boundingRect(), QtCore.Qt.KeepAspectRatio)



    def grayscale(self, img):
        arr = pygame.surfarray.array3d(img)
        # luminosity filter
        avgs = [[(r * 0.298 + g * 0.587 + b * 0.114) for (r, g, b) in col] for col in arr]
        #arr = np.array([[[avg,avg,avg] for avg in col] for col in avgs])
        return np.array(avgs)



    ##Capturing the image
    def imagecapture(self):
        pygame.camera.init()
        pygame.camera.list_cameras()
        cam = pygame.camera.Camera()
        cam.start()
        img = cam.get_image()
        self.phantom_grayscale = self.grayscale(pygame.transform.rotate(img, 90))
        self.load_image()




    def load_image(self):
        self.on_image_loaded()
        gray_t = self.phantom_grayscale.astype(np.int8)
        self.pixmap_phantom = 0
        self.load_phantom_in_gv(gray_t)
        self.Imgcapture_FFT()

    def Imgcapture_FFT(self):
        self.phantom_fft = jvm['Grid2D'].from_numpy(self.phantom_grayscale)
        grid2dcomplex = pyconrad.classes.stanford.rsl.conrad.data.numeric.Grid2DComplex(self.phantom_fft)
        grid2dcomplex.transformForward()
        grid2dcomplex.fftshift()
        gridimage = grid2dcomplex.getMagnSubGrid(0, 0, grid2dcomplex.getWidth(), grid2dcomplex.getHeight())
        self.phantom_fft = gridimage.as_numpy()

        self.phantom_fft /= np.median(self.phantom_fft)*50
        self.phantom_fft *= 255;
        phan_fft = self.phantom_fft.astype(np.uint8)

        ###HEEEEEEEEEEEEEREEEEEEEEEEEEEEEE
        #self.phantom_fft[self.phantom_fft < 0] = 0

        self.load_phantom_fft_in_gv(phan_fft)



    def on_image_loaded(self):
        self.pB_Xray.setDisabled(False)
        self.hScrollBar_deltabeta.setDisabled(False)
        self.hScrollBar_maxbeta.setDisabled(False)
        self.checkBox_cosine.setDisabled(False)
        self.checkBox_RamLakFilter.setDisabled(False)
        ###t missing....
        self.checkBox_ParkerWeigh.setDisabled(False)
        self.pB_Reconstruction.setDisabled(True)


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
        self.on_image_loaded()
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
        self.image = Image.open(self.phantom_value[self.file_path])





    ####Fourier transform of the phantom
    def PhantomFFT(self):
        self.PhantomFFT_image = jvm['Grid2D'].from_numpy(np.array(self.image))
        grid2dcomplex = pyconrad.classes.stanford.rsl.conrad.data.numeric.Grid2DComplex(self.PhantomFFT_image)
        grid2dcomplex.transformForward()
        grid2dcomplex.fftshift()


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



    ####forward projection
    def forwardProj(self):
        self.pB_Reconstruction.setDisabled(False)
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
        Phantom = jvm['Grid2D'].from_numpy(np.array(self.phantom_grayscale))
        self.Phantomwidth = Phantom.getWidth()
        self.Phantomheight = Phantom.getHeight()
        Phantom.setOrigin(JArray(JDouble)([-(self.Phantomwidth * Phantom.getSpacing()[0]) / 2, -(self.Phantomheight * Phantom.getSpacing()[1]) / 2]))
        Phantom.setSpacing(JArray(JDouble)([self.deltaT, self.deltaT]))




        ####Forward Projection
        ForwardProj = pyconrad.classes.stanford.rsl.tutorial.fan.FanBeamProjector2D(self.focalLength, self.maxBeta, self.deltaBeta, self.maxT, self.deltaT)
        self.forward.init(self.use_cl, ForwardProj, Phantom)
        self.forward.run()


    def on_fw_projection_finished(self):
        self.fanogram = self.forward.get_fanogram()
        self.fanogram_copy = jvm['Grid2D']
        self.fanogram_copy = self.fanogram.clone()
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




    ###Loading Fan Image aabb
    def fan_load(self):
        from PIL import Image, ImageOps, ImageFilter
        #load the fanogram image
        self.fanogramarray = self.fanogram.as_numpy()
        to_display = self.fanogramarray.copy()
        if to_display.min() < -100:
            to_display += 800
            to_display /= 1600

        else:
            to_display /= to_display.max()
        to_display *= 255



        scaled_fan = to_display.astype(np.uint8)

        self.load_sinogram_in_gv(scaled_fan)







    def fanFFT(self):
        grid2dcomplex = pyconrad.classes.stanford.rsl.conrad.data.numeric.Grid2DComplex(self.fanogram)
        grid2dcomplex.transformForward()
        grid2dcomplex.fftshift()
        ####convert complex grid 2d to grid 2d

        gridimage = grid2dcomplex.getMagnSubGrid(0, 0, grid2dcomplex.getWidth(), grid2dcomplex.getHeight())
        self.fanFFTarray = gridimage.as_numpy()
        #low_values_indices = fanFFTarray < 0
        #fanFFTarray[low_values_indices] = 0
        self.load_sino_fft_in_gv(self.fanFFTarray.astype(np.uint8))
        ###Loading FFT of FAN
        #self.gs_fanFFT = QtWidgets.QGraphicsScene()
        #self.gs_fanFFT.addPixmap(QtGui.QPixmap.fromImage(qimage2ndarray.array2qimage(np.uint8(fanFFTarray/255)).scaled(self.gV_SinogramFFT.size(),
#                                                                                       aspectRatioMode=QtCore.Qt.KeepAspectRatio,
    #                                                                                   transformMode=QtCore.Qt.SmoothTransformation)))
        #self.gV_SinogramFFT.setScene(self.gs_fanFFT)
        #self.gV_SinogramFFT.setStyleSheet("background:black")
        #self.gs_fanFFT.update()



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


    def filtercheck(self):
        if self.checkBox_RamLakFilter.isChecked():
            self.ramlakfilter()
            self.fan_load()
            self.ramlakCheckflag = 1
        else:
            self.fanogram = self.fanogram_copy

            self.ramlakCheckflag = 0
            self.fan_load()


    def ramlakfilter(self):
        sizeimage = self.fanogram.getSize()[1]
        ramlak = pyconrad.classes.stanford.rsl.tutorial.filters.RamLakKernel((int)(self.maxT / self.deltaT), self.deltaT)
        print(sizeimage)
        for theta in range(0, sizeimage):
            ramlak.applyToGrid(self.fanogram.getSubGrid(theta))
        self.fanogram_ramlak = jvm['Grid2D']
        self.fanogram_ramlak = self.fanogram


    def cosinecheck(self):
        if self.checkBox_cosine.isChecked():
            self.cosinefilter()
            self.cosineCheckflag = 1
            self.fan_load()
        else:
            self.fanogram = self.fanogram_copy
            self.cosineCheckflag = 0
            self.fan_load()


    def cosinefilter(self):
        sizeimage = self.fanogram.getSize()[1]
        cosine = pyconrad.classes.stanford.rsl.tutorial.fan.CosineFilter(self.focalLength, self.maxT, self.deltaT)
        print(sizeimage)
        for theta in range(0, sizeimage):
            cosine.applyToGrid(self.fanogram.getSubGrid(theta))
        self.fanogram_cosine = jvm['Grid2D']
        self.fanogram_cosine = self.fanogram



    def deltabetaValue(self):
        self.numProjSlider = self.hScrollBar_deltabeta.value()
        self.slidercheck = 1

    def deltabetatext(self):
        #self.label_delta.setAlignment((QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter))
        self.label_delta.setText("Sampling density: {}/{}".format(self.hScrollBar_deltabeta.maximum(),self.numProjSlider))


    def maxbetaValue(self):
        self.maxSlider = self.hScrollBar_maxbeta.value()
        self.maxslidercheck = 1

    def maxbetatext(self):
        #self.label_max.setAlignment((QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter))
        self.label_delta_2.setText("Rotation Angle: {}/{}".format(self.hScrollBar_maxbeta.maximum(),self.maxSlider))



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
        back = self.backward.get_backprojection()
        self.backarray = back.as_numpy()

        to_display = self.backarray.copy()

        to_display[to_display < 0] = 0
        to_display /= np.max(to_display)
        to_display *= 255


        self.load_reco_in_gv(to_display.astype(np.uint8))
       # low_values_indices = backarray < 0

       # backarray[low_values_indices] = 0

        ##Loading Backprojection aabb
        #self.gs_backproj = QtWidgets.QGraphicsScene()
       # if self.ParkerCheckflag == 0 or self.cosineCheckflag == 0 or self.ramlakCheckflag == 0 :
       #    self.gs_backproj.addPixmap(QtGui.QPixmap.fromImage(qimage2ndarray.array2qimage(np.uint16(backarray/300)).scaled(self.gV_Backproj.size(),aspectRatioMode=QtCore.Qt.KeepAspectRatio,transformMode=QtCore.Qt.SmoothTransformation)))
       # elif self.imagecapcheckflag == 1:
        #   self.gs_backproj.addPixmap(QtGui.QPixmap.fromImage(qimage2ndarray.array2qimage(backarray/255).scaled(self.gV_Backproj.size(),aspectRatioMode=QtCore.Qt.KeepAspectRatio,transformMode=QtCore.Qt.SmoothTransformation)))
        #else :
         #  self.gs_backproj.addPixmap(QtGui.QPixmap.fromImage(qimage2ndarray.array2qimage(backarray).scaled(self.gV_Backproj.size(),aspectRatioMode=QtCore.Qt.KeepAspectRatio,transformMode=QtCore.Qt.SmoothTransformation)))
        #self.gV_Backproj.setScene(self.gs_backproj)
        #self.gV_Backproj.setStyleSheet("background:black")
        #self.gs_backproj.update()

        self.backFFT(back)

    ####Fourier transform of the phantom
    def backFFT(self, back):
        grid2dcomplex = pyconrad.classes.stanford.rsl.conrad.data.numeric.Grid2DComplex(back)
        grid2dcomplex.transformForward()
        grid2dcomplex.fftshift()
        ####convert complex grid 2d to grid 2d
        gridimage = grid2dcomplex.getMagnSubGrid(0, 0, grid2dcomplex.getWidth(), grid2dcomplex.getHeight())
        self.backFFTarray = gridimage.as_numpy()

        back_fft = gridimage.as_numpy()

        back_fft /= np.median(back_fft) * 50
        back_fft *= 255;
        self.load_reco_fft_in_gv(back_fft.astype(np.uint8))


    def load_phantom_in_gv(self, image):
        img_Phantom = QtGui.QImage(image.data, image.shape[1], image.shape[0],
                                   QtGui.QImage.Format_Grayscale8)
        pix_ImgPhantom = QtGui.QPixmap(img_Phantom)
        self.gpi_phantom = QtWidgets.QGraphicsPixmapItem(pix_ImgPhantom)
        gs_ImgPhantom = QtWidgets.QGraphicsScene()
        # self.gs_ImgPhantom.clear()
        gs_ImgPhantom.addItem(self.gpi_phantom)
        self.gV_Phantom.setScene(gs_ImgPhantom)
        self.gV_Phantom.setStyleSheet("background:black")
        self.phantom_loaded = True
        self.resizeEvent()


    def load_phantom_fft_in_gv(self, image):
        img_fft = QtGui.QImage(image.data, image.shape[1], image.shape[0],
                                   QtGui.QImage.Format_Grayscale8)
        pix_ImgPhantomfft = QtGui.QPixmap(img_fft)
        self.gpi_phantom_fft = QtWidgets.QGraphicsPixmapItem(pix_ImgPhantomfft)
        gs_ImgPhantom = QtWidgets.QGraphicsScene()
        # self.gs_ImgPhantom.clear()
        gs_ImgPhantom.addItem(self.gpi_phantom_fft)
        self.gV_Phantom_FFT.setScene(gs_ImgPhantom)
        self.gV_Phantom_FFT.setStyleSheet("background:black")
        self.phantom_fft_loaded = True
        self.resizeEvent()

    def load_sinogram_in_gv(self, image):
        img_sino = QtGui.QImage(image.data, image.shape[1], image.shape[0],
                               QtGui.QImage.Format_Grayscale8)
        pix_ImgSino = QtGui.QPixmap(img_sino)
        self.gpi_sino = QtWidgets.QGraphicsPixmapItem(pix_ImgSino)
        gs_ImgSino = QtWidgets.QGraphicsScene()
        gs_ImgSino.addItem(self.gpi_sino)
        self.gV_Sinogram.setStyleSheet("background:black")
        self.gV_Sinogram.setScene(gs_ImgSino)
        self.sinogram_loaded = True
        self.resizeEvent()
        self.fanFFT()

    def load_sino_fft_in_gv(self, image):
        img_fft = QtGui.QImage(image.data, image.shape[1], image.shape[0],
                               QtGui.QImage.Format_Grayscale8)
        pix_ImgPhantomfft = QtGui.QPixmap(img_fft)
        self.gpi_sino_fft = QtWidgets.QGraphicsPixmapItem(pix_ImgPhantomfft)
        gs_ImgPhantom = QtWidgets.QGraphicsScene()
        # self.gs_ImgPhantom.clear()
        gs_ImgPhantom.addItem(self.gpi_sino_fft)
        self.gV_SinogramFFT.setScene(gs_ImgPhantom)
        self.gV_SinogramFFT.setStyleSheet("background:black")
        self.sino_fft_loaded = True
        self.resizeEvent()


    def load_reco_in_gv(self, image):
        img_fft = QtGui.QImage(image.data, image.shape[1], image.shape[0],
                               QtGui.QImage.Format_Grayscale8)
        pix_ImgPhantomfft = QtGui.QPixmap(img_fft)
        self.gpi_back = QtWidgets.QGraphicsPixmapItem(pix_ImgPhantomfft)
        gs_ImgPhantom = QtWidgets.QGraphicsScene()
        # self.gs_ImgPhantom.clear()
        gs_ImgPhantom.addItem(self.gpi_back)
        self.gV_Backproj.setScene(gs_ImgPhantom)
        self.gV_Backproj.setStyleSheet("background:black")
        self.back_loaded = True
        self.resizeEvent()




    def load_reco_fft_in_gv(self, image):
        img_fft = QtGui.QImage(image.data, image.shape[1], image.shape[0],
                               QtGui.QImage.Format_Grayscale8)
        pix_ImgPhantomfft = QtGui.QPixmap(img_fft)
        self.gpi_back_fft = QtWidgets.QGraphicsPixmapItem(pix_ImgPhantomfft)
        gs_ImgPhantom = QtWidgets.QGraphicsScene()
        # self.gs_ImgPhantom.clear()
        gs_ImgPhantom.addItem(self.gpi_back_fft)
        self.gV_Backproj_FFT.setScene(gs_ImgPhantom)
        self.gV_Backproj_FFT.setStyleSheet("background:black")
        self.back_fft_loaded = True
        self.resizeEvent()



    def image_histogram_equalization(self, image, number_bins=256):
        # from http://www.janeriksolem.net/2009/06/histogram-equalization-with-python-and.html

        # get image histogram
        image_histogram, bins = np.histogram(image.flatten(), number_bins, normed=True)
        cdf = image_histogram.cumsum()  # cumulative distribution function
        cdf = 255 * cdf / cdf[-1]  # normalize

        # use linear interpolation of cdf to find new pixel values
        image_equalized = np.interp(image.flatten(), bins[:-1], cdf)

        return image_equalized.reshape(image.shape)






class Window(QtWidgets.QMainWindow):
    resized = QtCore.pyqtSignal()
    dd = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        super(Window, self).__init__(parent=parent)
    ###We need to map the show event onto the resized signal,
    ### such that the respective MPR are initialized to a good size
    def showEvent(self, event):
        self.dd.emit()
        self.resized.emit()
        return super(Window, self).showEvent(event)

    def resizeEvent(self, event):
        self.resized.emit()
        return super(Window, self).resizeEvent(event)


if __name__ == '__main__':


    app = QtWidgets.QApplication(sys.argv)
    wid_FanRecont = Window()
    ui = fanbeam_main(wid_FanRecont)
    wid_FanRecont.show()
    sys.exit(app.exec_())

