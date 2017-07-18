from PyQt5 import QtCore, QtGui, QtWidgets
__all__ = [QtCore, QtGui, QtWidgets]
import sys
from PhantomSelect import Ui_Wid_PhantomSelect
from fanGUI_Project import Ui_wid_FanRecont
#from fangui_main import fanbeam_main
import os

class selectPhantom(Ui_Wid_PhantomSelect):

    #Initialisation
    def __init__(self, widget):
        Ui_Wid_PhantomSelect.__init__(self)
        self.setupUi(widget)
        self.listwidload

    #Loading the listwidget with images of phantom

    def listwidload(self):
        i = 1
        j = 1
        files = []
        for file in os.listdir("/Users/Janani/PycharmProjects/pythonqt/InteractiveReconstruction/Resources"):
            if file.endswith(".png"):
               files.append(os.path.join(os.getcwd(), file))

        Phantom_Path = {}
        for x in files:
            Phantom_Path["Phantom"+str(i)]  = x
            #print (Phantom_Path["Phantom"+str(i)])
            i=i+1


        for x in files:
            item = QtWidgets.QListWidgetItem()
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(x), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            #Name = "Phantom"+str(i)
            #i=i+1
            item.setIcon(icon)
            item.setText("Phantom"+str(j))
            j+=1
            self.ListWid_SelectPhantom.setSelectionMode( QtWidgets.QAbstractItemView.ExtendedSelection )
            self.ListWid_SelectPhantom.addItem(item)
            self.ListWid_SelectPhantom.setIconSize(QtCore.QSize(200,200))

        return Phantom_Path

if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    wid_PhanWindow = QtWidgets.QWidget()
    ui = selectPhantom(wid_PhanWindow )
    ui.setupUi(wid_PhanWindow)
    wid_PhanWindow.show()
    sys.exit(app.exec_())
