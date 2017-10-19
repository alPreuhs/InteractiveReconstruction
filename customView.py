from PyQt5 import QtCore, QtGui, QtWidgets

class CustomView(QtWidgets.QGraphicsView):
    photoClicked = QtCore.pyqtSignal(QtCore.QPoint)
    def mouseDoubleClickEvent(self, event):
        self.photoClicked.emit(QtCore.QPoint(event.pos()))
        super(CustomView, self).mousePressEvent(event)