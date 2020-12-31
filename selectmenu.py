from PyQt5.QtWidgets import QDialog
from PyQt5 import QtCore, QtGui, QtWidgets

from functools import partial

import platform
import labelClickable


class selectMenu(QDialog):
    def __init__(self, dialog, items, nrDisplayItems, xpos, callBack):
        super().__init__()
        self.dialogParent = dialog
        self.callback = callBack
        self.displayedMenuItems = []
        self.labelHandler = []
        self.items = items
        self.nrDisplayItems = nrDisplayItems
        self.offset = 0
        self.length = 0
        self.xpos = xpos
        
        self.normalColor = "White"
        self.highlightColor = "Yellow" 
        
        self.font = QtGui.QFont()
        self.font.setFamily("Droid Sans")
        self.font.setPointSize(30)
        self.font.setBold(True)
        self.font.setWeight(75)
        self.createItemsMenu(self.items)
        self.highlightedItem = -1 
       
    def setItems(self, items):
        self.offset = 0
        self.highlightedItem = -1 
        self.items = items
        self.updateItemsMenu(self.items, self.offset) 
  
        
    def createLabel(self, x, y, color, text, connect):
        label_hdl = labelClickable.QLabelClickable(self.dialogParent)
        label_hdl.setFont(self.font)
        label_hdl.setGeometry(x, y, 500, 50)
        label_hdl.setText("<font color="+color+">"+text+"</font>")
        if connect != None:
            label_hdl.clicked.connect(connect)
            return label_hdl    
      
    def changeLabel(self, handle, color, text):
        handle.setText("<font color="+color+">"+text+"</font>")
          
        
    def itemCallback(self, item):
        if item < (len(self.items)):
            self.callback(item + self.offset)
        
    
    def createItemsMenu(self, items):
        self.upButton()
        self.downButton() 
        nrOfItems = len(items)
        self.displayedMenuItems = []
        self.labelHandler = []
        if nrOfItems > 6:
            self.downButton() 
            nrOfItems = 6
        y = 70
        for item in range(0, nrOfItems):
            self.displayedMenuItems.append(items[item].get("url"))
            self.labelHandler.append(self.createLabel(self.xpos, y, self.normalColor, 
                             items[item].get("name"), 
                             partial(self.itemCallback, item)))
            y += 55
        # fill out to 6 if needed    
        if  nrOfItems < 6:
            for item in range(nrOfItems, 6 ):
                self.displayedMenuItems.append("")
                self.labelHandler.append(self.createLabel(self.xpos, y, self.normalColor, 
                             "", partial(self.itemCallback, item)))
                y += 55
            
            
    
    def updateItemsMenu(self, items, offset): 
        y = 70
        nrOfItems = len(items)
        if nrOfItems < 6:
            endItem = nrOfItems
            self.offset = 0
        else:     
            endItem = offset + 6    
        index = 0
        for item in range(offset, endItem):
            if item >=0:
                self.displayedMenuItems[index] = items[item].get("url")
                if self.highlightedItem == item:
                    self.changeLabel(self.labelHandler[index], self.highlightColor, 
                                 items[item].get("name"))
                else:
                    self.changeLabel(self.labelHandler[index], self.normalColor, 
                                 items[item].get("name"))
                y += 55
                index += 1
        # fill out to 6 if needed    
        if  nrOfItems < 6:
            for item in range(nrOfItems, 6 ):
                self.displayedMenuItems[index] = ""
                self.changeLabel(self.labelHandler[index], self.normalColor, "")
                
                y += 55
                index+=1    
    
    
    def getCurrentItem(self):
        return self.highlightedItem            
    
    def highlight(self, item):
        self.highlightedItem = item
        self.updateItemsMenu(self.items, self.offset)
    
        
    def upButton(self):
        self.pushButton = QtWidgets.QPushButton(self.dialogParent)
        self.pushButton.setFont(self.font)
        self.pushButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButton.setStyleSheet("background-color: rgb(0, 0, 0); color: rgb(255, 255, 255);selection-color: rgb(0, 0, 0);")
        self.pushButton.setGeometry(QtCore.QRect(self.xpos, 10, 200, 50))
        self.pushButton.setObjectName("pushButton")  
        self.pushButton.pressed.connect(self.upPressed)   
        self.pushButton.setText("▲")  
    
    
    def upPressed(self):
        if self.offset > 0:
            self.offset-=1
        self.updateItemsMenu(self.items, self.offset)
    

    def downButton(self):
        self.pushButton = QtWidgets.QPushButton(self.dialogParent)
        self.pushButton.setFont(self.font)
        self.pushButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButton.setStyleSheet("background-color: rgb(0, 0, 0); color: rgb(255, 255, 255);selection-color: rgb(0, 0, 0);")
        self.pushButton.setGeometry(QtCore.QRect(self.xpos, 420, 200, 50))
        self.pushButton.setObjectName("pushButton")   
        self.pushButton.pressed.connect(self.downPressed)   
        self.pushButton.setText("▼")  
    
 
    def downPressed(self):
        if self.offset < (len(self.items)-6):
            self.offset+=1
        self.updateItemsMenu(self.items, self.offset)
    
    def remoteUp(self):
        if (self.highlightedItem > 0) and (self.highlightedItem > -1):
            self.highlightedItem -= 1
            if self.highlightedItem < self.offset:
                self.upPressed()
            else:
                self.updateItemsMenu(self.items, self.offset)

        
    def remoteDown(self):
        if (self.highlightedItem < len(self.items)-1) and (self.highlightedItem > -1):
            self.highlightedItem += 1
            if self.highlightedItem >= (self.offset + self.nrDisplayItems):
                self.downPressed()
            else:
                self.updateItemsMenu(self.items, self.offset)
                
    
    def remoteCommand(self, command):
        if command == "up":
            self.remoteUp()
        if command == "down":
            self.remoteDown()