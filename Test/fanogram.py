from __future__ import division
from __future__ import print_function
import numpy as np
from Test.projector import radonRayDrivenApproach as rrd
from Test.projector import interpolation_Image as inter
import numpy as np
import matplotlib.pyplot as plt

from skimage.io import imread
from skimage import data_dir
from skimage.transform import radon, rescale
from Test.projector import plot_interp as pl
from PIL import Image

'''
image = imread("/Users/Janani/PycharmProjects/python_newproject/InteractiveReconstruction/Test/eclipse.png")
fig, (ax1, ax2) = plt.subplots(1, 2)

ax1.set_title("Original")
ax1.imshow(image)

#theta = np.linspace(0., 180., max(image.shape), endpoint=False)
theta = np.linspace(0., 180., max(image.shape), endpoint=False)
sinogram = radon(image, theta=theta, circle=True)
ax2.set_title("Radon transform\n(Sinogram)")
ax2.set_xlabel("Projection angle (deg)")
ax2.set_ylabel("Projection position (pixels)")
ax2.imshow(sinogram,
           extent=(0, 180, 0, sinogram.shape[0]), aspect='auto')

fig.tight_layout()
plt.show()


'''
img = Image.open("/Users/Janani/PycharmProjects/pythonqt/InteractiveReconstruction/Test/circle.png")
#img = mpimg.imread("/Users/Janani/Desktop/09.png")


arr = np.array(img)


#pl(image)
fanogram = rrd(arr,inter(arr),232,105,120,577,1,377)
#fanogram = rrd(arr,inter(arr),1500,100,120,600,1,500)
#fan = rrd(inter(arr))
pl(img,fanogram)
#pl(img,fan)f