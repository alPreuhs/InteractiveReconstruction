from PyQt5 import QtCore
import subprocess

class forward_project_thread(QtCore.QThread):

    forward_project_finsihed  = QtCore.pyqtSignal(str)

    def init(self, use_cl, ForwardProj, Phantom):
        self.use_cl = use_cl
        self.ForwardProj = ForwardProj
        self.Phantom = Phantom

    def get_fanogram(self):
        return self.fanogram

    def run(self):
        a = 10

        if self.use_cl:
            self.fanogram = self.ForwardProj.projectRayDrivenCL(self.Phantom)
        else:
            self.fanogram = self.ForwardProj.projectRayDriven(self.Phantom)

        self.forward_project_finsihed.emit('finished')