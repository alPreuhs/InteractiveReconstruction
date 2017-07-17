from __future__ import division
from __future__ import print_function
import numpy as np
from projector import radonRayDrivenApproach as rrd
from projector import interpolation_Image as inter
from projector import plot_interp as pl
from skimage.color import rgb2gray
from PIL import Image
import matplotlib.image as mpimg
from skimage.color import rgb2gray

img = Image.open("/Users/Janani/PycharmProjects/pythonqt/InteractiveReconstruction/circle.png")
#img = mpimg.imread("/Users/Janani/Desktop/09.png")


arr = np.array(img)


#pl(image)
fanogram = rrd(arr,231.2,105,10,318,1,377)
#fan = rrd(inter(arr))
pl(img,fanogram)
#pl(img,fan)