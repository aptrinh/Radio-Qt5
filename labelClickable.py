from PyQt5.QtCore import pyqtSignal, QTimer
from PyQt5.QtWidgets import QApplication, QLabel



class QLabelClickable(QLabel):
    clicked = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super(QLabelClickable, self).__init__(parent)
        
        

    def mousePressEvent(self, event):
        self.lastEvent = "Click"
    
    def mouseReleaseEvent(self, event):
        if self.lastEvent == "Click":
            QTimer.singleShot(QApplication.instance().doubleClickInterval(),
                              self.performSingleClickAction)
        else:
            self.clicked.emit(self.lastEvent)
    
    def mouseDoubleClickEvent(self, event):
        self.lastEvent = "Double Click"
    
    def performSingleClickAction(self):
        if self.lastEvent == "Click":
            self.clicked.emit(self.lastEvent)
            