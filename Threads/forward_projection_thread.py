from PyQt5 import QtCore
import subprocess
from pyconrad import *

class forward_project_thread(QtCore.QThread):




    def __init__(self,  use_cl, phantom, focalLength, maxBeta, deltaBeta, maxT, deltaT):
        forward_project_finsihed = QtCore.pyqtSignal(str)
        self.pyconrad_instance = PyConrad()
        self.pyconrad_instance.add_import('edu.stanford.rsl.conrad.data.numeric')

        self.Phantom = self.pyconrad_instance['Grid2D'].from_numpy(phantom)
        QtCore.QThread.__init__(self)
        self.use_cl = use_cl
        self.fan_beam_projection = self.pyconrad_instance.classes.stanford.rsl.tutorial.fan.FanBeamProjector2D(focalLength, maxBeta, deltaBeta, maxT, deltaT)

    #def initttt(self, use_cl, ForwardProj, Phantom):
    #    self.use_cl = use_cl
    #    self.ForwardProj = ForwardProj
    #    self.Phantom = Phantom

    def get_fanogram(self):
        return self.fanogram

    def run(self):
        print('greeetings from thread')
        if self.use_cl:
            self.fanogram = self.fan_beam_projection.projectRayDrivenCL(self.Phantom)
        else:
            self.fanogram = self.fan_beam_projection.projectRayDriven(self.Phantom)

        self.forward_project_finsihed.emit('finished')