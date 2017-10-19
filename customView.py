from PyQt5 import QtCore, QtGui, QtWidgets

class CustomView(QtWidgets.QGraphicsView):
    photoClicked = QtCore.pyqtSignal(QtCore.QPoint)
    photoSaved = QtCore.pyqtSignal()

    def mouseDoubleClickEvent(self, event):
        self.photoClicked.emit(QtCore.QPoint(event.pos()))
        super(CustomView, self).mousePressEvent(event)

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        #if self.is
       # if self.underMouse():
           # if event.key() == QtCore.Qt.Key_S or event.key() == Q:
                self.photoSaved.emit()