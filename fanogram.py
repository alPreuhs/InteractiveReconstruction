from __future__ import division
from __future__ import print_function
import numpy as np
from projector import radonRayDrivenApproach as rrd
from projector import interpolation_Image as inter
from projector import plot_interp as pl
from PIL import Image

image = np.asarray(Image.open("/Users/Janani/PycharmProjects/pythonqt/InteractiveReconstruction/circle.png"))

pl(image)
#fanogram = rrd(inter(image),231.2,105,0,318,1,377)
fan = rrd(inter(image))
pl(image,fan)