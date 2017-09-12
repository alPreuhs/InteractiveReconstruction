from __future__ import division
from __future__ import print_function
from Test.projector import radonRayDrivenApproach as rrd
from Test.projector import interpolation_Image as inter
from pyconrad import PyConrad, ImageUtil, java_float_dtype
import numpy as np
import math

import matplotlib.pyplot as plt
from Test.projector import plot_interp as pl
from PIL import Image,ImageChops

#Pyconrad
pyconrad = PyConrad()
pyconrad.setup()
pyconrad.start_conrad()

####Declaration of variables
gammaM = 11.768288932020647*math.pi/180
maxT = (float)(500)
deltaT = (float)(1.0)
focalLength = (float)((maxT/2.0-0.5)*deltaT/math.tan(gammaM))
maxBeta = (float)(285.95* math.pi/180)
deltaBeta = (float)(maxBeta / 132)
rayfil = (int) (maxT / deltaT)

####Input image
img = Image.open("phantom.png")
Phantom = pyconrad.classes.stanford.rsl.conrad.data.numeric.Grid2D.from_numpy(np.array(img))

#####Forward Projection
Test = pyconrad.classes.stanford.rsl.tutorial.fan.FanBeamProjector2D(focalLength, maxBeta, deltaBeta, maxT, deltaT)
fanogram = Test.projectRayDriven(Phantom)
fanogram.show("Fanogram before filtering")

####Filtering

######Adding redundancy weighting
weight = pyconrad.classes.stanford.rsl.conrad.data.numeric.Grid2D(377,377)
weight = pyconrad.classes.stanford.rsl.tutorial.fan.redundancy.ParkerWeights(focalLength, maxT, deltaT, maxBeta, deltaBeta)
pyconrad.classes.stanford.rsl.conrad.data.numeric.NumericPointwiseOperators.multiplyBy(fanogram, weight)
weight.show("Weight")

###Ray by ray filtering
sizeimage =  fanogram.getSize()
rbrfil = pyconrad.classes.stanford.rsl.tutorial.filters.RayByRayFiltering(rayfil , deltaT, 0.5,0.000200, 1., 1000000.0, 6, 405)
print(sizeimage)

for theta in range(0,132):
    rbrfil.applyToGrid(fanogram.getSubGrid(theta))
fanogram.show("After filtering")

#####Backward Projection
Test1 = pyconrad.classes.stanford.rsl.tutorial.fan.FanBeamBackprojector2D(focalLength,
					deltaT, deltaBeta, 377, 377)
baclpro = Test1.initSinogramParams(fanogram)
back = Test1.backprojectRayDriven(fanogram)
back.show("back projection")


#pl(image)
#fanogram = rrd(img,inter(arr),500,50,20,500,1,377)
#fanogram = rrd(arr,inter(arr),1500,100,120,600,1,500)
#fan = rrd(inter(arr))
#pl(img,fanogram)
#pl(img,fan)