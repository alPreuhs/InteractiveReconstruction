from __future__ import division
from __future__ import print_function
import numpy as np
from Test.projector import radonRayDrivenApproach as rrd
from Test.projector import interpolation_Image as inter
from Test.projector import plot_interp as pl
from PIL import Image


img = Image.open("/Users/Janani/PycharmProjects/pythonqt/InteractiveReconstruction/Test/circle.png")
#img = mpimg.imread("/Users/Janani/Desktop/09.png")


arr = np.array(img)


#pl(image)
fanogram = rrd(arr,inter(arr),231.2,105,120,318,1,377)
#fan = rrd(inter(arr))
pl(img,fanogram)
#pl(img,fan)f