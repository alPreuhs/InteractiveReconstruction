from __future__ import division
from __future__ import print_function
from Test.projector import radonRayDrivenApproach as rrd
from Test.projector import interpolation_Image as inter
import numpy as np
import cv2
import matplotlib.pyplot as plt
from Test.projector import plot_interp as pl
from PIL import Image,ImageChops

img = Image.open("circle.png")
arr = np.array(img)

'''
#Method 1
img = cv2.imread("circle.png",0)

#img1 = Image.new( img.mode, img.size)
#pixel_new = img1.load()

rows,cols = img.shape
print(cols)
offset_x = -188
offset_y = -188

for i in range(0,rows):
    for j in range(0,cols):
        row_new = offset_x + 1 * i
        cols_new = offset_y + 1 * j
        M = np.float32([[i, 0, row_new], [0, j, cols_new]])
        dst = cv2.warpAffine(img, M, (j, i))
arr = -np.array(dst)


img = cv2.imread("circle.png",0)
rows,cols = img.shape

M = np.float32([[377,0,25],[0,377,25]])
dst = cv2.warpAffine(img,M,(cols,rows))

arr2 = np.array(img)

img = Image.open("circle.png")
a = 377
b =0
c = -188.5 # +left/-right
d =0
e = 377
f = 188.5 # +up/-down
translate = img.transform(img.size, Image.AFFINE, (a, b, c, d, e, f))
arr = np.array(translate)
'''
#pl(image)
fanogram = rrd(img,inter(arr),500,50,20,500,1,377)
#fanogram = rrd(arr,inter(arr),1500,100,120,600,1,500)
#fan = rrd(inter(arr))
pl(img,fanogram)
#pl(img,fan)