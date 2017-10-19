from PIL import Image, ImageEnhance, ImageFilter
from PyQt5 import QtCore, QtGui, QtWidgets
from fanGUI_Project import Ui_ReconstructionGUI
from PhantomSelect_Window import selectPhantom
from pyconrad import *
import math
import numpy as np
import sys



class fanbeam_main(Ui_ReconstructionGUI):
    use_cl = True


    phantom_value = {}
    file_path = 'NULL'


    def __init__(self, MainWindow):
        self.MainWindow = MainWindow
        self.start_pyconrad()

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



        self.set_parameters()
        self.define_xray_projection()
        self.connect_threads()
        self.connect_buttons()
        self.connect_checkboxes()
        self.connect_slider()
        self.disable_sliders_on_start()
        self.connect_graphics_view()
        self.set_max_beta_text()

        self.gV_Phantom
        self.bt_start_simulation.clicked.connect(self.on_init_simulation)
        self.bt_stop_simulation.clicked.connect(self.on_stop_simulation)

    def start_pyconrad(self):
        self.pyconrad_instance = PyConrad()
        self.pyconrad_instance.add_import('edu.stanford.rsl.conrad.data.numeric')
        self.pyconrad_instance.setup()
        self.pyconrad_instance.start_conrad()



    def on_stop_simulation(self):
        self.on_simulation = False
        self.bt_stop_simulation.setDisabled(True)
        self.bt_start_simulation.setDisabled(False)


    def on_init_simulation(self):
        self.bt_start_simulation.setDisabled(True)
        self.bt_stop_simulation.setDisabled(False)
        self.on_simulation = True
        self.current = 1
        self.end = 360
        self.dt = 5

        self.current -= self.dt
        self.start_simulation()



    def start_simulation(self):
       # time.sleep(5)
        self.current += self.dt

        if self.current <= self.end:
            self.hScrollBar_maxbeta.setValue(self.current)
            self.pB_Xray.click()
        else:
            self.hScrollBar_maxbeta.setValue(self.end)
            self.on_simulation = False
            self.pB_Xray.click()
    


    def connect_graphics_view(self):
        self.gV_Phantom.photoClicked.connect(self.on_open_phantom)
        self.gV_Phantom_FFT.photoClicked.connect(self.on_open_phantom_fft)
        self.gV_Sinogram.photoClicked.connect(self.on_open_sinogram)
        self.gV_SinogramFFT.photoClicked.connect(self.on_open_sinogram_fft)
        self.gV_Backproj.photoClicked.connect(self.on_open_back)
        self.gV_Backproj_FFT.photoClicked.connect(self.on_open_back_fft)

        self.gV_Backproj_FFT.photoSaved.connect(self.on_save_back_fft2)
        self.gV_Phantom.photoSaved.connect(self.on_save_phantom)
        self.gV_Phantom_FFT.photoSaved.connect(self.on_save_phantom_fft)
        self.gV_Sinogram.photoSaved.connect(self.on_save_sinogram)
        self.gV_SinogramFFT.photoSaved.connect(self.on_save_sinogram_fft)
        self.gV_Backproj.photoSaved.connect(self.on_save_back)






    def on_open_phantom(self,point):
        if self.phantom_loaded:
            self.pyconrad_instance['Grid2D'].from_numpy(self.phantom_grayscale).show("Phantom");
    def on_open_phantom_fft(self, point):
        if self.phantom_fft_loaded:
            self.pyconrad_instance['Grid2D'].from_numpy(self.phantom_fft).show("FFT des Phantoms");
    def on_open_sinogram(self, point):
        if self.sinogram_loaded:
            self.pyconrad_instance['Grid2D'].from_numpy(self.fanogramarray).show("Fanogram");

    def on_open_sinogram_fft(self, point):
        if self.sino_fft_loaded:
            self.pyconrad_instance['Grid2D'].from_numpy(self.fanFFTarray).show("FFT des Fanograms");
    def on_open_back(self, point):
        if self.back_loaded:
            self.pyconrad_instance['Grid2D'].from_numpy(self.backarray).show("Rekonstruktion");
    def on_open_back_fft(self, point):
        if self.back_fft_loaded:
            self.pyconrad_instance['Grid2D'].from_numpy(self.backFFTarray).show("FFT der Rekonstruktion");




    def on_save_phantom(self):
        if self.phantom_loaded:
            Image.fromarray(self.scaled_phantom.astype(np.uint8)).save(r'photos/Phantom.png')

    def on_save_phantom_fft(self):
        if self.phantom_fft_loaded:
            Image.fromarray(self.scaled_phantom_fft).save(r'photos/Phantom_FFT.png')

    def on_save_sinogram(self):
        if self.sinogram_loaded:
            Image.fromarray(self.scaled_sinogram).save(r'photos/Fanogram.png')

    def on_save_sinogram_fft(self):
        if self.sino_fft_loaded:
            Image.fromarray(self.scaled_sinogram_fft).save(r'photos/Fanogram_FFT.png')

    def on_save_back(self):
        if self.back_loaded:
            Image.fromarray(self.scaled_reco).save(r'photos/Rekonstruktion.png')

    def on_save_back_fft2(self):
        print('try do reco fft')
        if self.back_fft_loaded:
            Image.fromarray(self.scaled_reco_fft).save(r'photos/Rekonstruktion_FFT.png')




    def disable_sliders_on_start(self):
        self.pB_Xray.setDisabled(True)
        self.hScrollBar_deltabeta.setDisabled(True)
        self.hScrollBar_maxbeta.setDisabled(True)
        self.checkBox_cosine.setDisabled(True)
        self.checkBox_RamLakFilter.setDisabled(True)
        ###t missing....
        self.checkBox_ParkerWeigh.setDisabled(True)
        self.pB_Reconstruction.setDisabled(True)
        self.bt_stop_simulation.setDisabled(True)
        self.bt_start_simulation.setDisabled(True)

    def connect_slider(self):
        ## delta beta slider
        self.hScrollBar_deltabeta.valueChanged.connect(self.deltabetaValue)
        ## max beta slider
        self.hScrollBar_maxbeta.valueChanged.connect(self.on_max_beta_value_changed)
        self.hScrollBar_maxbeta.valueChanged.connect(self.set_max_beta_text)

    def connect_checkboxes(self):
        #parker weights
        self.checkBox_ParkerWeigh.stateChanged.connect(self.parker_weight_check)
        #ramLakFilter
        self.checkBox_RamLakFilter.stateChanged.connect(self.ram_Lak_filter_check)
        #cosine weight
        self.checkBox_cosine.stateChanged.connect(self.cosine_filtere_check)

    def connect_buttons(self):
        ##capture image
        self.pB_videocapture.clicked.connect(self.on_live_image_clicked)
        ##Select Phantom
        self.pB_PhantomSelect.clicked.connect(self.on_select_phantom_clicked)
        ##X-ray
        self.pB_Xray.clicked.connect(self.on_roentgen_clicked)
        ##reconstruction_clicked
        self.pB_Reconstruction.clicked.connect(self.on_reconstruction_clicked)

    def define_xray_projection(self):
        self.maxT = (float)(1300)
        self.focalLength = (float)(2400)
        self.gammaM = math.atan((self.maxT / 2.0 - 0.5) / self.focalLength)
        self.deltaT = (float)(1.0)
        self.numProj = 1024
        self.maxBeta = math.pi + 2 * self.gammaM
        self.deltaBeta = (float)(self.maxBeta / self.numProj)

    def set_parameters(self):
        self.on_simulation = False
        self.phantom_loaded = False
        self.phantom_fft_loaded = False
        self.sinogram_loaded = False
        self.sino_fft_loaded = False
        self.back_loaded = False
        self.back_fft_loaded = False


    def connect_threads(self):
        from Threads.forward_projection_thread import forward_project_thread as fpt
        self.fan_projector_thread = fpt()
        self.fan_projector_thread.forward_project_finsihed.connect(self.on_fw_projection_finished)

        from Threads.back_projection_thread import back_project_thread as bpt
        self.backprojector_thread = bpt()
        self.backprojector_thread.back_project_finsihed.connect(self.on_bw_projection_finished)

        from Threads.image_capture_thread import image_capture_thread as ict
        self.image_capture_thread = ict()
        self.image_capture_thread.image_capture_finsihed.connect(self.on_photo_finished)

    def resizeEvent(self):
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



    ##Capturing the image
    def on_live_image_clicked(self):
        self.pB_videocapture.setDisabled(True)
        self.pB_PhantomSelect.setDisabled(True)
        print('start thread')
        self.load_phantom_in_gv_from_string(r'resource_photos/laecheln.png')
        self.image_capture_thread.start()


    def on_photo_finished(self):
        print('finished thread')
        self.phantom_grayscale = self.image_capture_thread.get_photo()
        self.on_load_phantom()
        self.pB_videocapture.setDisabled(False)
        self.pB_PhantomSelect.setDisabled(False)


    def on_load_phantom(self):
        #self.checkBox_cosine.setChecked(False)
        #self.checkBox_ParkerWeigh.setChecked(False)
        #self.checkBox_RamLakFilter.setChecked(False)

        self.on_image_loaded()
        gray_t = self.phantom_grayscale.astype(np.int8)
        self.pixmap_phantom = 0
        self.load_phantom_in_gv(gray_t)
        self.generate_fft_of_phantom()

    def generate_fft_of_phantom(self):
        ###need self.phantom_fft as we might open it somewhen with imageJ
        self.phantom_grid = self.pyconrad_instance['Grid2D'].from_numpy(self.phantom_grayscale)
        phantom_fft = self.pyconrad_instance.classes.stanford.rsl.conrad.data.numeric.Grid2DComplex(self.phantom_grid)
        phantom_fft.transformForward()
        phantom_fft.fftshift()
        phantom_fft_magnitude = phantom_fft.getMagnSubGrid(0, 0, phantom_fft.getWidth(), phantom_fft.getHeight())
        self.phantom_fft = phantom_fft_magnitude.as_numpy()
        to_display = self.fft_scaling(self.phantom_fft.copy())
        self.load_phantom_fft_in_gv(to_display)


    def on_image_loaded(self):
        self.pB_Xray.setDisabled(False)
        self.hScrollBar_deltabeta.setDisabled(False)
        self.hScrollBar_maxbeta.setDisabled(False)
        self.checkBox_cosine.setDisabled(False)
        self.checkBox_RamLakFilter.setDisabled(False)
        ###t missing....
        self.checkBox_ParkerWeigh.setDisabled(False)
        self.pB_Reconstruction.setDisabled(True)
        self.bt_start_simulation.setDisabled(False)


    # function for displaying the phantom selection window
    def on_select_phantom_clicked(self):
        self.pB_videocapture.setDisabled(True)
        self.pB_PhantomSelect.setDisabled(True)
        self.selectPhan_Window = QtWidgets.QWidget()
        self.selectPhan_creator = selectPhantom(self.selectPhan_Window)
        self.selectPhan_creator.ListWid_SelectPhantom.itemClicked.connect(self.getPhantom)
        self.selectPhan_creator.pushButton.clicked.connect(self.phantom_window_closed)
        self.phantom_value =  self.selectPhan_creator.listwidload()
        self.selectPhan_Window.setWindowFlags(QtCore.Qt.WindowTitleHint)
        self.selectPhan_Window.show()


    def phantom_window_closed(self):
        self.pB_videocapture.setDisabled(False)
        self.pB_PhantomSelect.setDisabled(False)
        self.selectPhan_Window.close()

    def getPhantom(self):
        self.file_path = self.selectPhan_creator.ListWid_SelectPhantom.currentIndex().data()
        self.phantom_grayscale = np.array(Image.open(self.phantom_value[self.file_path]))
        self.selectPhan_Window.close()
        self.on_load_phantom()
        self.on_image_loaded()
        self.pB_videocapture.setDisabled(False)
        self.pB_PhantomSelect.setDisabled(False)



    ####forward projection
    def on_roentgen_clicked(self):
        self.pB_Xray.setDisabled(True)
        print('i do roentgen')
        self.pB_Reconstruction.setDisabled(False)
        ####Forward Projection
        ForwardProj = self.pyconrad_instance.classes.stanford.rsl.tutorial.fan.FanBeamProjector2D(self.focalLength, self.maxBeta, self.deltaBeta, self.maxT, self.deltaT)
        self.fan_projector_thread.init(self.use_cl, ForwardProj, self.phantom_grid)
        self.fan_projector_thread.start()




    def on_fw_projection_finished(self):
        self.fanogram = self.fan_projector_thread.get_fanogram()
      #  self.fanogram = self.a.get_fanogram()
        self.load_fan_in_view(self.fanogram)
        self.fanFFT()
        ###if we are not in simulation mode, we want to
        ###display any combination fast, therefore we
        ###precompute it
        ##########################
        ###in demo mode, we only compute the needed
        ###filtering
        if not self.on_simulation:
            ## creates a self.fanogram_parker
            self.parkerweight()
            ## creates a self.fanogram_cosine_filtered
            self.cosinefilter()
            ## creates  self.fanogram_ramlak
            self.ramlakfilter()
            ## creates a self.fanogram_ramlak_cosine
            self.ramlak_cosine()
            ## creates a self.fanogram_full_filtered
            self.ramlak_cosine_parker()
            ## creates a self.fanogram_ramlak_parker
            self.ramlak_parker()
            ## creates a self.fanogram_cosine_parker
            self.cosine_parker()
            self.select_filtered_image()
        else:
            pw = self.checkBox_ParkerWeigh.isChecked()
            rl = self.checkBox_RamLakFilter.isChecked()
            cf = self.checkBox_cosine.isChecked()
            if pw and not rl and not cf:
                self.parkerweight()
                self.load_fan_in_view(self.fanogram_parker)
            elif rl and not pw and not cf:
                self.ramlakfilter()
                self.load_fan_in_view(self.fanogram_ramlak)
            elif cf and not pw and not rl:
                self.cosinefilter()
                self.load_fan_in_view(self.fanogram_cosine_filtered)
            elif pw and rl and not cf:
                self.ramlak_parker()
                self.load_fan_in_view(self.fanogram_ramlak_parker)
            elif pw and rl and cf:
                self.ramlak_cosine_parker()
                self.load_fan_in_view(self.fanogram_full_filtered)
            elif cf and rl and not pw:
                self.ramlak_cosine()
                self.load_fan_in_view(self.fanogram_ramlak_cosine)
            elif pw and cf and not rl:
                self.cosine_parker()
                self.load_fan_in_view(self.fanogram_cosine_parker)
            elif not pw and not cf and not rl:
                self.load_fan_in_view(self.fanogram)

        self.pB_Xray.setDisabled(False)
        if(self.on_simulation):
            self.pB_Reconstruction.click()



    def cosine_parker(self):
        self.fanogram_cosine_parker = self.pyconrad_instance.classes.stanford.rsl.conrad.data.numeric.NumericPointwiseOperators.multipliedBy(
        self.fanogram_cosine_filtered, self.parker_weight)

    def ramlak_parker(self):
        self.fanogram_ramlak_parker = self.pyconrad_instance.classes.stanford.rsl.conrad.data.numeric.NumericPointwiseOperators.multipliedBy(
            self.fanogram_ramlak, self.parker_weight)


    def ramlak_cosine_parker(self):
        self.fanogram_full_filtered = self.pyconrad_instance.classes.stanford.rsl.conrad.data.numeric.NumericPointwiseOperators.multipliedBy(
            self.fanogram_ramlak_cosine, self.parker_weight)


    def ramlak_cosine(self):
        sizeimage = self.fanogram.getSize()[1]
        cosine = self.pyconrad_instance.classes.stanford.rsl.tutorial.fan.CosineFilter(self.focalLength, self.maxT, self.deltaT)
        ramlak = self.pyconrad_instance.classes.stanford.rsl.tutorial.filters.RamLakKernel((int)(self.maxT / self.deltaT),
                                                                                      self.deltaT)
        self.fanogram_ramlak_cosine = self.fanogram.clone()
        for theta in range(0, sizeimage):
            ramlak.applyToGrid(self.fanogram_ramlak_cosine.getSubGrid(theta))
            cosine.applyToGrid(self.fanogram_ramlak_cosine.getSubGrid(theta))


    ###Loading Fan Image
    def load_fan_in_view(self, image):
        from PIL import Image, ImageOps, ImageFilter
        #load the fanogram image
        self.current_fanogram = image.clone()
        self.fanogramarray = image.as_numpy()

        to_display = self.fanogramarray.copy()
        if to_display.min() < -100:
            #to_display = self.scale_to_0_255(to_display)
            to_display += 800
            to_display /= 1600
            to_display *= 255
            im = Image.fromarray(to_display.astype(np.uint8))
            contrast = ImageEnhance.Contrast(im)
            contrasted_image = contrast.enhance(2)
            to_display = np.array(contrasted_image.filter(ImageFilter.GaussianBlur(2)))
        else:
            to_display /= to_display.max()
            to_display *= 255


        scaled_fan = to_display.astype(np.uint8)
        self.load_sino_in_gv(scaled_fan)



    def fanFFT(self):
        grid2dcomplex = self.pyconrad_instance.classes.stanford.rsl.conrad.data.numeric.Grid2DComplex(self.fanogram)
        grid2dcomplex.transformForward()
        grid2dcomplex.fftshift()
        ####convert complex grid 2d to grid 2d

        gridimage = grid2dcomplex.getMagnSubGrid(0, 0, grid2dcomplex.getWidth(), grid2dcomplex.getHeight())
        self.fanFFTarray = gridimage.as_numpy()
        fan_fft = self.fanFFTarray.copy()
        fan_fft = self.fft_scaling(fan_fft)
        self.load_sino_fft_in_gv(fan_fft.astype(np.uint8))


    def fft_scaling(self, image, blurring_radius = 1):
        image_tmp = np.abs(image)
        image_tmp += 1
        image_tmp = np.log(image_tmp)
        image_tmp = self.scale_to_0_255(image_tmp)
        im = Image.fromarray(image_tmp.astype(np.uint8))
        contrast = ImageEnhance.Contrast(im)
        contrasted_image = contrast.enhance(2)
        to_ret = contrasted_image.filter(ImageFilter.GaussianBlur(blurring_radius))
        return np.array(to_ret)

    def scale_to_0_255(self,image):
        image += np.min(image)
        image /= np.max(image)
        image -= np.min(image)
        image *= 255.0/np.max(image)
        return image


    def parkerweight(self):
        self.parker_weight = self.pyconrad_instance.classes.stanford.rsl.tutorial.fan.redundancy.ParkerWeights(self.focalLength, self.maxT, self.deltaT, self.maxBeta, self.deltaBeta)
        self.fanogram_parker = self.pyconrad_instance.classes.stanford.rsl.conrad.data.numeric.NumericPointwiseOperators.multipliedBy(self.fanogram, self.parker_weight)


    def parker_weight_check(self):
        self.select_filtered_image()

    def ram_Lak_filter_check(self):
        self.select_filtered_image()

    def cosine_filtere_check(self):
        self.select_filtered_image()

    def select_filtered_image(self):
        pw = self.checkBox_ParkerWeigh.isChecked()
        # ramLakFilter
        rl = self.checkBox_RamLakFilter.isChecked()
        # cosine weight
        cf = self.checkBox_cosine.isChecked()

        if pw and not rl and not cf:
            self.load_fan_in_view(self.fanogram_parker)
            print('parker_checked')

        elif rl and not pw and not cf:
            self.load_fan_in_view(self.fanogram_ramlak)
            print('ramlak checked')

        elif cf and not pw and not rl:
            self.load_fan_in_view(self.fanogram_cosine_filtered)
            print('cosine checked')

        elif pw and rl and not cf:
            self.load_fan_in_view(self.fanogram_ramlak_parker)
            print('parker and ramlak')

        elif pw and rl and cf:
            self.load_fan_in_view(self.fanogram_full_filtered)
            print(' all filteres checked')

        elif cf and rl and not pw:
            self.load_fan_in_view(self.fanogram_ramlak_cosine)
            print('cosien and ramlak')

        elif pw and cf and not rl:
            self.load_fan_in_view(self.fanogram_cosine_parker)
            print('parker and cosine')

        elif not pw and not cf and not rl:
            self.load_fan_in_view(self.fanogram)

            print('nothing checked')
        print('')



    def ramlakfilter(self):
        sizeimage = self.fanogram.getSize()[1]
        ramlak = self.pyconrad_instance.classes.stanford.rsl.tutorial.filters.RamLakKernel((int)(self.maxT / self.deltaT), self.deltaT)
        self.fanogram_ramlak = self.fanogram.clone()
        for theta in range(0, sizeimage):
            ramlak.applyToGrid(self.fanogram_ramlak.getSubGrid(theta))





    def cosinefilter(self):
        sizeimage = self.fanogram.getSize()[1]
        cosine = self.pyconrad_instance.classes.stanford.rsl.tutorial.fan.CosineFilter(self.focalLength, self.maxT, self.deltaT)
        self.fanogram_cosine_filtered = self.fanogram.clone()
        for theta in range(0, sizeimage):
            cosine.applyToGrid(self.fanogram_cosine_filtered.getSubGrid(theta))



    def deltabetaValue(self):
        ##goes from 1 to 1024
        self.numProj =self.hScrollBar_deltabeta.value()
        self.deltaBeta = self.maxBeta / self.numProj


    def on_max_beta_value_changed(self):
        self.maxBeta = math.radians(self.hScrollBar_maxbeta.value())
        self.deltaBeta = self.maxBeta / self.numProj


    def set_max_beta_text(self):
        self.label_delta_2.setText("Maximale Angulation: {}/{}".format(self.hScrollBar_maxbeta.maximum(),int(math.degrees(self.maxBeta))))



    ###Backprojection
    def on_reconstruction_clicked(self):
        self.pB_Reconstruction.setDisabled(True)
        height = self.phantom_grayscale.shape[0]
        width = self.phantom_grayscale.shape[1]
        fan_beam_backprojector = self.pyconrad_instance.classes.stanford.rsl.tutorial.fan.FanBeamBackprojector2D(self.focalLength, self.deltaT, self.deltaBeta, width, height)
        self.backprojector_thread.init(self.use_cl, fan_beam_backprojector, self.current_fanogram)
        self.backprojector_thread.start()


    def on_bw_projection_finished(self):
        back = self.backprojector_thread.get_backprojection()
        self.backarray = back.as_numpy()
        to_display = self.backarray.copy()
        to_display = self.scale_to_0_255(to_display)
        self.load_reco_in_gv(to_display.astype(np.uint8))
        self.backFFT(back)
        self.pB_Reconstruction.setDisabled(False)
        if self.on_simulation:
            self.start_simulation()

    ####Fourier transform of the phantom
    def backFFT(self, back):
        grid2dcomplex = self.pyconrad_instance.classes.stanford.rsl.conrad.data.numeric.Grid2DComplex(back)
        grid2dcomplex.transformForward()
        grid2dcomplex.fftshift()
        ####convert complex grid 2d to grid 2d
        gridimage = grid2dcomplex.getMagnSubGrid(0, 0, grid2dcomplex.getWidth(), grid2dcomplex.getHeight())
        self.backFFTarray = gridimage.as_numpy()
        back_fft= self.fft_scaling(self.backFFTarray.copy())
        self.load_reco_fft_in_gv(back_fft.astype(np.uint8))



    def load_phantom_in_gv(self, image):
        img_Phantom = QtGui.QImage(image.data, image.shape[1], image.shape[0],
                                   QtGui.QImage.Format_Grayscale8)
        pix_ImgPhantom = QtGui.QPixmap(img_Phantom)
        self.gpi_phantom = QtWidgets.QGraphicsPixmapItem(pix_ImgPhantom)
        gs_ImgPhantom = QtWidgets.QGraphicsScene()
        gs_ImgPhantom.addItem(self.gpi_phantom)
        self.gV_Phantom.setScene(gs_ImgPhantom)
        self.gV_Phantom.setStyleSheet("background:black")
        self.phantom_loaded = True
        self.scaled_phantom = image
        self.resizeEvent()

    def load_phantom_in_gv_from_string(self, fn):
        img_Phantom = QtGui.QImage(fn)
        pix_ImgPhantom = QtGui.QPixmap(img_Phantom)
        self.gpi_phantom = QtWidgets.QGraphicsPixmapItem(pix_ImgPhantom)
        gs_ImgPhantom = QtWidgets.QGraphicsScene()
        gs_ImgPhantom.addItem(self.gpi_phantom)
        self.gV_Phantom.setScene(gs_ImgPhantom)
        self.gV_Phantom.setStyleSheet("background:black")
        self.phantom_loaded = True
        self.resizeEvent()


    def load_phantom_fft_in_gv_from_string(self, fn, load_fft = True):
        print('loading from string')
        img_fft = QtGui.QImage(fn)
        pix_ImgPhantomfft = QtGui.QPixmap(img_fft)
        self.gpi_phantom_fft = QtWidgets.QGraphicsPixmapItem(pix_ImgPhantomfft)
        gs_ImgPhantom = QtWidgets.QGraphicsScene()
        gs_ImgPhantom.addItem(self.gpi_phantom_fft)
        self.gV_Phantom_FFT.setScene(gs_ImgPhantom)
        self.gV_Phantom_FFT.setStyleSheet("background:black")
        self.phantom_fft_loaded = True
        self.resizeEvent()


    def load_phantom_fft_in_gv(self, image):
        img_fft = QtGui.QImage(image.data, image.shape[1], image.shape[0],
                                   QtGui.QImage.Format_Grayscale8)
        pix_ImgPhantomfft = QtGui.QPixmap(img_fft)
        self.gpi_phantom_fft = QtWidgets.QGraphicsPixmapItem(pix_ImgPhantomfft)
        gs_ImgPhantom = QtWidgets.QGraphicsScene()
        gs_ImgPhantom.addItem(self.gpi_phantom_fft)
        self.gV_Phantom_FFT.setScene(gs_ImgPhantom)
        self.gV_Phantom_FFT.setStyleSheet("background:black")
        self.phantom_fft_loaded = True
        self.scaled_phantom_fft = image
        self.resizeEvent()

    def load_sino_in_gv(self, image):
        img_sino = QtGui.QImage(image.data, image.shape[1], image.shape[0],
                               QtGui.QImage.Format_Grayscale8)
        pix_ImgSino = QtGui.QPixmap(img_sino)
        self.gpi_sino = QtWidgets.QGraphicsPixmapItem(pix_ImgSino)
        gs_ImgSino = QtWidgets.QGraphicsScene()
        gs_ImgSino.addItem(self.gpi_sino)
        self.gV_Sinogram.setStyleSheet("background:black")
        self.gV_Sinogram.setScene(gs_ImgSino)
        self.sinogram_loaded = True
        self.scaled_sinogram = image
        self.resizeEvent()


    def load_sino_fft_in_gv(self, image):
        img_fft = QtGui.QImage(image.data, image.shape[1], image.shape[0],
                               QtGui.QImage.Format_Grayscale8)
        pix_ImgPhantomfft = QtGui.QPixmap(img_fft)
        self.gpi_sino_fft = QtWidgets.QGraphicsPixmapItem(pix_ImgPhantomfft)
        gs_ImgPhantom = QtWidgets.QGraphicsScene()
        gs_ImgPhantom.addItem(self.gpi_sino_fft)
        self.gV_SinogramFFT.setScene(gs_ImgPhantom)
        self.gV_SinogramFFT.setStyleSheet("background:black")
        self.sino_fft_loaded = True
        self.scaled_sinogram_fft = image
        self.resizeEvent()


    def load_reco_in_gv(self, image):
        img_fft = QtGui.QImage(image.data, image.shape[1], image.shape[0],
                               QtGui.QImage.Format_Grayscale8)
        pix_ImgPhantomfft = QtGui.QPixmap(img_fft)
        self.gpi_back = QtWidgets.QGraphicsPixmapItem(pix_ImgPhantomfft)
        gs_ImgPhantom = QtWidgets.QGraphicsScene()
        gs_ImgPhantom.addItem(self.gpi_back)
        self.gV_Backproj.setScene(gs_ImgPhantom)
        self.gV_Backproj.setStyleSheet("background:black")
        self.back_loaded = True
        self.scaled_reco = image
        self.resizeEvent()




    def load_reco_fft_in_gv(self, image):
        img_fft = QtGui.QImage(image.data, image.shape[1], image.shape[0],
                               QtGui.QImage.Format_Grayscale8)
        pix_ImgPhantomfft = QtGui.QPixmap(img_fft)
        self.gpi_back_fft = QtWidgets.QGraphicsPixmapItem(pix_ImgPhantomfft)
        gs_ImgPhantom = QtWidgets.QGraphicsScene()
        gs_ImgPhantom.addItem(self.gpi_back_fft)
        self.gV_Backproj_FFT.setScene(gs_ImgPhantom)
        self.gV_Backproj_FFT.setStyleSheet("background:black")
        self.back_fft_loaded = True
        self.scaled_reco_fft = image
        self.resizeEvent()



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

