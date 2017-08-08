
from __future__ import division
from __future__ import print_function
from PIL import Image
from numpy.linalg import lstsq
from scipy.interpolate import RectBivariateSpline
from scipy.interpolate import interp1d
from scipy import interpolate
import numpy as np
import matplotlib.pyplot as plt
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


def radonRayDrivenApproach(img,img_interp_spline,dSI, dDI, val, detectorSize, detectorSpacing, numProj):
        #debugging arrays for showing the source positions
        source_pos_x_list = []
        source_pos_y_list = []
        # debugging arrays for showing the piercing positions
        piercing_x = []
        piercing_y = []
        
        #Defining the fanogram image
        fanogram = Image.new(img.mode, (377,377))  # create a new black image

        ##calculate index for detector pixels
        detectorSizeIndex = (detectorSize / detectorSpacing) 
        ## calculate fan angle
        gammaM = math.atan((detectorSize / 2.0 - 0.5) / dSI)
        ## calculate scanning range which is 180+fan angle (short scan)
        angRange = val + 2 * gammaM        
        ## calculate angular step size
        angStepSize = angRange / numProj

        #iterate over the rotation angle
        for angle_index in np.arange(0, 10):

            # calculate actual angle which are distributed equally over short scan range + 180 degree shift...
            beta = angStepSize * angle_index+math.pi/2

            # calculate cos/sin
            cosBeta = math.cos(beta)
            sinBeta = math.sin(beta)

            #compute source position
            source_x = dSI * (-cosBeta)
            source_y = dSI * sinBeta
            source_position = (source_x, source_y)
            #compute piercing point
            PP_Point_x = dDI * cosBeta
            PP_Point_y = dDI  * (-sinBeta)
            PP = (PP_Point_x, PP_Point_y)

            #calculate direction orthogonal to central ray -> pointing parallel to detector 
            ortho_direction = -np.array([sinBeta, cosBeta])
            
            ### add values for debugging 
            source_pos_x_list.append(source_x)
            source_pos_y_list.append(source_y)
            piercing_x.append(PP_Point_x)
            piercing_y.append(PP_Point_y)

            #iterate over detector elements
            for t in range(0, int(detectorSizeIndex)):

                ##shift detector indices
                t -= detectorSizeIndex*0.5

                ## calculate world point for current pixel
                pixel_position = PP + (t * detectorSpacing * ortho_direction)
            
                ## calculate distence between source position and detector pixel
                distance = np.linalg.norm(pixel_position - np.array(source_position))

                #Define increment step
                increment = 0.5
                sum = 0.0
                #print("increment      ",increment)
                #integral along the line
                
                #Define maximal distance index
                max_distance_index = int(distance/increment)
                for line_index in np.arange(0, max_distance_index):
                    current = source_position + increment * line_index
                    current = np.array(current)
                    height , width = img.size
                    X_Image = current.item(0) + height / 2
                    Y_Image = current.item(1) + width / 2

                    #print("current      ", current)
                    #sum = interpolate.Rbf(current.item(0),current.item(1),arr,function='linear')
                    fanogram = RectBivariateSpline((X_Image,Y_Image,img)
                    #sum += interp1d(current.item(0),current.item(1),"linear")
                    #pixels[angle_index, t] = (angle_index, t, sum)
                #print("sum    ", sum)

        # plt.plot(source_pos_x_list, source_pos_y_list)
        # plt.show()
        plt.plot(piercing_x, piercing_y, 'bo')
        plt.plot(source_pos_x_list, source_pos_y_list, 'rx')
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
        
