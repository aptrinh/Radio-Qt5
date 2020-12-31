from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QIcon, QPixmap

import clockDialog
import labelClickable
import random
import platform
import time 



class Clock(QDialog):
    def __init__(self, radio):
        super().__init__()
        self.menuActive = False
        self.radio = radio
        self.clock = clockDialog.Ui_Dialog()
        self.clock.setupUi(self)
        self.setStyleSheet("QWidget#Clock {background-color: rgb(0, 0, 0);}")
        self.exitArea = self.createLabel(0, 0, 800, 480, "White", "", self.hide)
        random.seed()

    
    def show(self):
        self.menuActive = True
        if "arm" in platform.machine():
            import rpi_backlight as bl
            bl.set_brightness(15)
        ypos = random.randint(0, 220)
        self.clock.labelTime.setGeometry(QtCore.QRect(190, ypos, 441, 181))
        self.clock.labelDate.setGeometry(QtCore.QRect(190, ypos+180, 481, 51))
        self.radio.sDialog.hideSelectStation()
        self.radio.stop()
        super().show()
       

    def hide(self):
        self.menuActive = False
        if "arm" in platform.machine(): 
            import rpi_backlight as bl
            bl.set_brightness(100)
        self.radio.playAfterSandby()
        time.sleep(0.2)  
        super().hide()
        time.sleep(0.2)  
        self.radio.show() 

    
    
    def createLabel(self, xpos, ypos, x, y, color, text, connect):
        label_hdl = labelClickable.QLabelClickable(self)
        label_hdl.setGeometry(xpos, ypos, x, y)
        label_hdl.setText("<font color="+color+">"+text+"</font>")
        if connect != None:
            label_hdl.clicked.connect(connect)
            return label_hdl            

    def remoteCommand(self, command):
        if (self.menuActive == True) and (command == "power"):
            self.hide()
