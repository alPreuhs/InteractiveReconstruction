from PyQt5 import QtCore
import subprocess
from pyconrad import *
import numpy as np
import jpype
import time

class forward_project_thread(QtCore.QThread):
    forward_project_finsihed = QtCore.pyqtSignal(str)

    def init(self, use_cl, ForwardProj, Phantom):
        self.use_cl = use_cl
        self.ForwardProj = ForwardProj
        self.Phantom = Phantom

    def get_fanogram(self):
        return self.fanogram

    def run(self):
        jpype.attachThreadToJVM()
        if self.use_cl:
            self.fanogram = self.ForwardProj.projectRayDrivenCL(self.Phantom.grid)
        else:
            self.fanogram = self.ForwardProj.projectRayDriven(self.Phantom)
       # time.sleep(5)
        jpype.detachThreadFromJVM()
        self.forward_project_finsihed.emit('finished')