from PyQt5 import QtCore
import numpy as np
import pygame
import pygame.camera


import time

class image_capture_thread(QtCore.QThread):
    image_capture_finsihed  = QtCore.pyqtSignal(str)

    def __init__(self):
        QtCore.QThread.__init__(self)

        pygame.camera.init()
        self.cam = pygame.camera.Camera()


    def scale_to_0_255(self,image):
        image += np.min(image)
        image /= np.max(image)
        image -= np.min(image)
        image *= 255.0/np.max(image)
        return image

    def get_photo(self):
        return self.phantom_grayscale


    def convert_pygame_to_grayscale(self, img):
        arr = pygame.surfarray.array3d(img)
        avgs = [[(r * 0.298 + g * 0.587 + b * 0.114) for (r, g, b) in col] for col in arr]
        return np.array(avgs)

    def run(self):
        time.sleep(2)
        self.cam.start()
        img = self.cam.get_image()

        self.cam.stop()
        print('this takes looooooooooong')
        data = pygame.surfarray.array2d(pygame.transform.rotate(img, 90))
        self.phantom_grayscale = self.scale_to_0_255(data.astype(np.float32))
        print('faster ??')

        #self.phantom_grayscale = self.convert_pygame_to_grayscale(pygame.transform.rotate(img, 90))
        #print(' JOASJDOIAJSDJIO')
        self.image_capture_finsihed.emit('finished')