import pygame
import pygame.camera

pygame.camera.init()
pygame.camera.list_cameras()

cam = pygame.camera.Camera()
cam.start()

img = cam.get_image()

pygame.image.save(img, r'C:\Users\z0038hzp.AD005\Desktop\camerashots\test.png')