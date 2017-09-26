from __future__ import division
from __future__ import print_function
import numpy as np
import math
from PIL import Image,ImageChops
from pyconrad import *

jvm = PyConrad()
jvm.setup()
jvm.add_import('edu.stanford.rsl.conrad.data.numeric')
jvm.add_import('edu.stanford.rsl.tutorial.phantoms')
jvm.add_import('edu.stanford.rsl.conrad.phantom')

#Pyconrad
pyconrad = PyConrad()
pyconrad.setup()
pyconrad.start_conrad()

####Declaration of variables
#gammaM = 11.768288932020647*2*math.pi/180
#maxT = (float)(500)
#deltaT = (float)(1.0)
#focalLength = (float)((maxT/2.0-0.5)*deltaT/math.tan(gammaM))
#maxBeta = (float)(285.95* math.pi/180)
#deltaBeta = (float)(maxBeta / 132)
maxT = (float)(600)
focalLength = (float)(500)
gammaM = math.atan((maxT/2.0-0.5 ) / focalLength)
deltaT = (float)(1.0)
numProj = 500
maxBeta = math.pi +  2*gammaM;
deltaBeta = (float)(maxBeta/numProj )
rayfil = (int) (maxT / deltaT)


####Input image
img = Image.open("phantom.png")
Phantom = jvm['Grid2D'].from_numpy(np.array(img))
Phantom.setOrigin(JArray(JDouble)([-(377 * Phantom.getSpacing()[0]) / 2, -(377 * Phantom.getSpacing()[1]) / 2 ]))
Phantom.setSpacing(JArray(JDouble)([deltaT , deltaT]))
Phantom.show()

# Phantom = pyconrad.classes.stanford.rsl.conrad.data.numeric.Grid2D.from_numpy(np.array(img))
#Phantom.setSpacing(deltaT , deltaT )
#Phantom.setOrigin(-(377 * Phantom.getSpacing()[0]) / 2, -(377 * Phantom.getSpacing()[1]) / 2  )

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

###Ramlak filtering
sizeimage =  fanogram.getSize()
ramlak = pyconrad.classes.stanford.rsl.tutorial.filters.RamLakKernel((int) (maxT / deltaT), deltaT)
print(sizeimage)

for theta in range(0,500):
    ramlak.applyToGrid(fanogram.getSubGrid(theta))
fanogram.show("After filtering")

#####Backward Projection
Test1 = pyconrad.classes.stanford.rsl.tutorial.fan.FanBeamBackprojector2D(focalLength,
					deltaT, deltaBeta, 377, 377)
baclpro = Test1.initSinogramParams(fanogram)
back = Test1.backprojectRayDriven(fanogram)
back.show("back projection")

