from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QIcon, QPixmap

import labelClickable
import stationDialog
import selectmenu
import json
import tunein
import urllib
import soma
import platform
import local

selectXpos = 250
normalcolor = "#b1b1b1"
highlight = "White" 

class SelectStation(QDialog):
    def __init__(self):
        super().__init__()
        self.menuActive = None
        self.selectStation = stationDialog.Ui_SelectDialog()
        self.selectStation.setupUi(self)
        self.setStyleSheet("QWidget#SelectDialog {background-image: url(radio-cropped.png);}")
        self.createLabel(15, 15, normalcolor, "Back", self.backButton_clicked)
        self.fav_label = self.createLabel(15, 65, highlight, "Favorites", self.favorites_clicked)
        self.pinguin_label = self.createLabel(15, 115, normalcolor, "Pinguin", self.pinguin_clicked)
        self.tuneIn_label = self.createLabel(15, 165, normalcolor,"TuneIn", self.tuneIn_clicked)
        self.somafm_label = self.createLabel(15, 215, normalcolor,"SomaFm", self.somafm_clicked)
        self.local_label = self.createLabel(15, 265, normalcolor, "Local File", self.local_clicked)
        self.readFavorites()
        self.readPinguin()
        self.items = self.favorites
        self.tuneIn = tunein.openRadio()
        self.sMenu = selectmenu.selectMenu(self, self.items, 6, selectXpos, self.itemSelected)
        self.menu = "Favorites"     
        self.playing_name = ""
        self.playing_url = ""
        self.playing_image = ""
        
        
        self.pow_button = self.createIconLabel(20, 415, normalcolor, "", self.powerButton_clicked)
        pixmap = QtGui.QPixmap("./assets/power.png")
        #self.pow_button.resize(50, 50)
        self.pow_button.setPixmap(pixmap.scaled(self.pow_button.size(), QtCore.Qt.IgnoreAspectRatio))
        
        self.favmin_button = self.createIconLabel(85, 414, normalcolor, "", self.deleteFavorite_clicked)
        pixmap = QtGui.QPixmap("./assets/minus.png")
        #self.set_button.resize(50, 50)
        self.favmin_button.setPixmap(pixmap.scaled(self.favmin_button.size(), QtCore.Qt.IgnoreAspectRatio))
    
        self.favplus_button = self.createIconLabel(150, 414, normalcolor, "", self. addFavorite_clicked)
        pixmap = QtGui.QPixmap("./assets/plus.png")
        #self.fav_button.resize(50, 50)
        self.favplus_button.setPixmap(pixmap.scaled(self.favplus_button.size(), QtCore.Qt.IgnoreAspectRatio))
        
         
    def powerButton_clicked(self):
        self.radio.showClock()
        
        
    def readFavorites(self):
        try:
            with open("favorites.json") as json_data:
                self.favorites = json.load(json_data)
        except Exception as msg:
            print("file problem:" + str(msg))
        return           

    def readPinguin(self):
        try:
            with open("pinguin.json") as json_data:
                self.pinguin = json.load(json_data)
        except Exception as msg:
            print("file problem:" + str(msg))
        return     


    def writeFavorites(self):
        try:
            with open("favorites.json", "w") as json_data:
                json.dump(self.favorites, json_data, indent=4)
        except Exception as msg:
            print("file problem:" + str(msg))
        return      


    def show(self):
        self.favorites_clicked()
        self.menuActive = "left"
        super().show()

        
    def itemSelected(self, item):
        if self.items[item].get("type") == "audio":
            print("Item selected: " + str(item))
            if self.menu == "tuneIn":
                url = self.tuneIn.getStreamUrl(self.items[item].get("url")).splitlines()[0]
            else:
                url = self.items[item].get("url")
            if (".pls" in url) or (".m3u" in url):
                try:
                    req = urllib.request.urlopen(url)
                    file = req.read()
                    url = plparser.parse(filename=url, filedata=file).Tracks[0].File
                except Exception as msg:
                    print(msg)    
            self.playing_name = self.items[item].get("name")  
            self.playing_url = url
            self.playing_image = self.items[item].get("image")
            if self.playing_image != None:
                self.radio.showPicture(self.playing_image)
            self.radio.playNew(url,self.playing_name)
            self.radio.showArtist("")
            self.radio.showSong("")
            self.radio.show()    
            self.hide()
        else:
            self.items = self.tuneIn.getNextLayer(self.items[item].get("url"))
            self.sMenu.setItems(self.items)
            if self.menuActive == "right":
                self.sMenu.highlight(0)
                
         
        
    def createLabel(self, x, y, color, text, connect):
        font = QtGui.QFont()
        font.setFamily("Droid Sans")
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(75)
        label_hdl = labelClickable.QLabelClickable(self)
        label_hdl.setFont(font)
        label_hdl.setGeometry(x, y, 300, 50)
        label_hdl.setText("<font color="+color+">"+text+"</font>")
        if connect != None:
            label_hdl.clicked.connect(connect)
        return label_hdl    
 
    def createIconLabel(self, x, y, color, text, connect):
        font = QtGui.QFont()
        font.setFamily("Droid Sans")
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(75)
        label_hdl = labelClickable.QLabelClickable(self)
        label_hdl.setFont(font)
        label_hdl.setGeometry(x, y, 48, 48)
        label_hdl.setText("<font color="+color+">"+text+"</font>")
        if connect != None:
            label_hdl.clicked.connect(connect)
        return label_hdl    
 
 
      
    def changeLabel(self, handle, color, text):
        handle.setText("<font color="+color+">"+text+"</font>")
    
        
    def showSelectStation(self, radio):
        self.items = self.favorites
        self.radio = radio
        self.sMenu.setItems(self.items)
        self.show()
 
        
    def hideSelectStation(self):
        self.menuActive = None
        #self.radio.show()
        self.hide()
        

    def backButton_clicked(self):
        self.menuActive = None
        self.radio.show()
        self.hide()    


    def favorites_clicked(self):
        self.changeLabel(self.fav_label, highlight, "Favorites")
        self.changeLabel(self.pinguin_label, normalcolor, "Pinguin")
        self.changeLabel(self.tuneIn_label, normalcolor, "TuneIn") 
        self.changeLabel(self.somafm_label, normalcolor, "SomaFm") 
        self.items = self.favorites
        self.menu = "Favorites"
        self.sMenu.setItems(self.items)
    
    
    def pinguin_clicked(self):
        self.changeLabel(self.fav_label, normalcolor, "Favorites")
        self.changeLabel(self.pinguin_label, highlight, "Pinguin")
        self.changeLabel(self.tuneIn_label, normalcolor, "TuneIn") 
        self.changeLabel(self.somafm_label, normalcolor, "SomaFm") 
        self.items = self.pinguin
        self.menu = "Pinguin"
        self.sMenu.setItems(self.items)
    
    
     
    def tuneIn_clicked(self):
        self.changeLabel(self.fav_label, normalcolor, "Favorites") 
        self.changeLabel(self.pinguin_label, normalcolor, "Pinguin")
        self.changeLabel(self.tuneIn_label, highlight, "TuneIn")  
        self.changeLabel(self.somafm_label, normalcolor, "SomaFm") 
        self.items = self.tuneIn.getOverview()
        self.menu = "tuneIn"
        self.sMenu.setItems(self.items)
    
            
    def somafm_clicked(self):
        self.changeLabel(self.fav_label, normalcolor, "Favorites")  
        self.changeLabel(self.pinguin_label, normalcolor, "Pinguin")
        self.changeLabel(self.tuneIn_label, normalcolor, "TuneIn") 
        self.changeLabel(self.somafm_label, highlight, "SomaFm")
        self.items = soma.get_stations()
        self.menu = "Somafm"
        self.sMenu.setItems(self.items)
        
    def local_clicked(self):
        self.changeLabel(self.fav_label, normalcolor, "Favorites")  
        self.changeLabel(self.pinguin_label, normalcolor, "Pinguin")
        self.changeLabel(self.tuneIn_label, normalcolor, "TuneIn") 
        self.changeLabel(self.somafm_label, normalcolor, "SomaFm")
        self.changeLabel(self.local_label, highlight, "Local File")
        self.items = local.get_stations()
        self.menu = "Local File"
        self.sMenu.setItems(self.items)

    def addFavorite_clicked(self):
        for item in self.favorites:
            if (item.get("url") == self.playing_url) or  (self.playing_url == ""):
                return #already i playlist
            
        self.favorites.append({"name":self.playing_name, 
                              "url":self.playing_url,
                              "image":self.playing_image,
                              "type": "audio" }) 
        self.writeFavorites()
        self.radio.show()
        self.hide()  
        
    
    def deleteFavorite_clicked(self):
        for index in range(0, len(self.favorites)):
            item = self.favorites[index]
            if item.get("url") == self.playing_url:
                self.favorites.pop(index)
        self.writeFavorites()
        self.radio.show()
        self.hide()   
        
    
    def remoteCommand(self, command):
        # send command to selectmenu
        self.sMenu.remoteCommand(command)
        
        # handle commands if this menu is active
        if (self.menuActive != None):
            if  command == "power":
                self.radio.showClock()
            elif command == "down":
                self.remoteDown()
            elif command == "up":
                self.remoteUp()
            elif (command == "ok") or (command == "right"):
                self.remoteOK()
            elif (command == "back") or (command == "left"):
                self.menuActive = None
                self.radio.show()
                self.hide()        
            
        
    def remoteDown(self):
        if self.menuActive == "left":
            if self.menu == "Favorites":
                self.pinguin_clicked()
            elif self.menu == "Pinguin":
                self.tuneIn_clicked()    
            elif self.menu == "tuneIn":     
                self.somafm_clicked()
        
        
    def remoteUp(self):
        if self.menuActive == "left":
            if self.menu == "Pinguin":
                self.favorites_clicked()    
            elif self.menu == "tuneIn":     
                self.pinguin_clicked()
            elif self.menu == "Somafm":
                self.tuneIn_clicked()    
            
            
    def remoteOK(self):
        if self.menuActive == "left":
            self.menuActive = "right"
            self.sMenu.highlight(0)
        elif self.menuActive == "right":
            self.itemSelected(self.sMenu.getCurrentItem())
            
            
         
        
        
