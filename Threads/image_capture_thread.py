from PyQt5 import QtCore
import numpy as np
import pygame
import pygame.camera


class image_capture_thread(QtCore.QThread):
    image_capture_finsihed  = QtCore.pyqtSignal(str)

    def get_photo(self):
        return self.phantom_grayscale


    def convert_pygame_to_grayscale(self, img):
        arr = pygame.surfarray.array3d(img)
        avgs = [[(r * 0.298 + g * 0.587 + b * 0.114) for (r, g, b) in col] for col in arr]
        return np.array(avgs)

    def run(self):
        pygame.camera.init()
        cam = pygame.camera.Camera()
        cam.start()
        img = cam.get_image()
        self.phantom_grayscale = self.convert_pygame_to_grayscale(pygame.transform.rotate(img, 90))
        self.image_capture_finsihed.emit('finished')