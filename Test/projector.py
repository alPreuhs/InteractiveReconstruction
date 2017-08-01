
from __future__ import division
from __future__ import print_function
from PIL import Image
from numpy import ones,vstack
from numpy.linalg import lstsq
from scipy.interpolate import RectBivariateSpline
from scipy.interpolate import interp1d
from scipy import interpolate
import numpy as np
import matplotlib.pyplot as plt

from skimage.io import imread
from skimage import data_dir
from skimage.transform import radon, rescale
import math

import matplotlib.pylab as plt
import numpy as np
import sys


def interpolation_Image(arr):
    x = np.arange(arr.shape[0])
    y = np.arange(arr.shape[1])
    z = arr
    img_interp_spline = RectBivariateSpline(x=x, y=y, z=arr, bbox=[None, None, None, None], kx=3, ky=3, s=0)
    return img_interp_spline


def radonRayDrivenApproach( arr,img_interp_spline,dSI, dDI, val, detectorSize, detectorSpacing, numProj):
        source_pos_x_list = []
        source_pos_y_list = []

        piercing_x = []
        piercing_y = []
        #Defining the fanogram image
        fanogram = Image.new('RGB', (377, 377))  # create a new black image
        pixels = fanogram.load()

        detectorSizeIndex = (detectorSize / detectorSpacing)
        gammaM = math.atan((detectorSize / 2.0 - 0.5) / dSI)
        angRange = val + 2 * gammaM
        angStepSize = angRange / numProj
        samplingRate = 3.0
        maxbetaindex = angRange / angStepSize
        #print(maxbetaindex)

        #iterate over the rotation angle
        for i in np.arange(0, 10):
            #print(val)
            beta = angStepSize * i+math.pi/2
            #beta = val * i+math.pi/2
            #print(beta)
            cosBeta = math.cos(beta)
            sinBeta = math.sin(beta)

            #Compute source and detector points
            source_x = dSI * (-cosBeta)
            source_y = dSI * sinBeta
            PP_Point_x = dDI * cosBeta
            PP_Point_y = dDI  * (-sinBeta)
            PP = (PP_Point_x, PP_Point_y)
            source = (source_x, source_y)
            point = (cosBeta,sinBeta)

            source_pos_x_list.append(source_x)
            source_pos_y_list.append(source_y)
            piercing_x.append(PP_Point_x)
            piercing_y.append(PP_Point_y)

            #Unit vector along the detector
            PP_vector = np.array(PP)
            #print(PP_vector.size)
            PP_vector = PP + point * (-1)
            dirDetector = (PP_vector) / np.linalg.norm(PP_vector)
            #print(dirDetector)


            #iterate over detector elements
            for t in range(0, int(detectorSizeIndex)):
                #calculate detector bin positions
                stepsDirection = 0.5 * detectorSpacing + t * detectorSpacing
                P = PP + (dirDetector * stepsDirection)

                #Straight line equation between souce and the detector bin
                points = (source, P)
                distance = math.hypot(PP_Point_x - source_x, PP_Point_y - source_y)
                #print("distance  " , distance)
                x_coords, y_coords = zip(*points)
                A = vstack([x_coords, ones(len(x_coords))]).T
                m, c = lstsq(A, y_coords)[0]
                straightline = "{m}x + {c}".format(m=m, c=c)
                #print("straightline  ", straightline)

                #Normalised increment step
                increment = 1.0 / distance
                sum = 0.0
                #print("increment      ",increment)

                #integral along the line
                for Linet in np.arange(0, distance):
                    current = source + increment * Linet
                    #current = np.array(current)
                    #print("current      ", current)
                    #sum = interpolate.Rbf(current.item(0),current.item(1),arr,function='linear')
                    # sum += img_interp_spline(current.item(0),current.item(1),arr)
                    #sum += interp1d(current.item(0),current.item(1),"linear")
                #print("sum    ", sum)
                fanogram = img_interp_spline(i, t)
        # plt.plot(source_pos_x_list, source_pos_y_list)
        # plt.show()
        plt.plot(piercing_x, piercing_y)
        plt.show()


        return fanogram





def plot_interp(image, img_):
    fig, axes = plt.subplots(1, 3)
    for ax, (im, text) in zip(axes, ((image, 'original'), (img_, 'interpolated'))):
        ax.imshow(im, cmap='gray')
        ax.title.set_text(text)
        ax.axis('off')

    plt.tight_layout(pad=0)
    plt.show()

'''
def radonRayDrivenApproach(img_interp_spline):
    for i in np.arange(0, 100):
        for j in np.arange(0, 100):
            img_ = img_interp_spline(i+0.5, j+0.5)
            print(img_)
            return img_
'''
        
