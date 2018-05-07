from PyQt5 import QtCore
import numpy as np
import cv2

import time

class image_capture_thread(QtCore.QThread):
    image_capture_finsihed  = QtCore.pyqtSignal(str)

    def __init__(self):
        QtCore.QThread.__init__(self)


        ###typically external cameras are listed last, thus this takes the last camera
        self.vc = cv2.VideoCapture(0)



    def scale_to_0_255(self,image):
        image += np.min(image)
        image /= np.max(image)
        image -= np.min(image)
        image *= 255.0/np.max(image)
        return image

    def get_photo(self):
        return self.phantom_grayscale



    def run(self):

        time.sleep(2)
        rval, frame = self.vc.read()
        rval, frame = self.vc.read()
        frame_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)





        self.phantom_grayscale = self.scale_to_0_255(frame_image.astype(np.float32))
        #self.phantom_grayscale = self.convert_pygame_to_grayscale(pygame.transform.rotate(img, 90))
        #print(' JOASJDOIAJSDJIO')
        self.image_capture_finsihed.emit('finished')