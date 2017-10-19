from PyQt5 import QtCore
import subprocess
import time
import jpype



class back_project_thread(QtCore.QThread):

    back_project_finsihed  = QtCore.pyqtSignal(str)

    def init(self, use_cl, Backprojection, fanogram):
        self.use_cl = use_cl
        self.Backprojection = Backprojection
        self.fanogram = fanogram

    def get_backprojection(self):
        return self.back

    def run(self):
        jpype.attachThreadToJVM()
        time.sleep(5)
        if self.use_cl:
            self.back = self.Backprojection.backprojectPixelDrivenCL(self.fanogram)
        else:
            self.back = self.Backprojection.backprojectPixelDriven(self.fanogram)
        self.back_project_finsihed.emit('finished')