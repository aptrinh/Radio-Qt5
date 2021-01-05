from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QIcon, QPixmap

import os.path
import labelClickable
import stationDialog
import selectmenu
import json
import tunein
import urllib
import soma
import platform
import local
import re

selectXpos = 250
normalcolor = "#f9e0c3"
highlight = "#DAF7A6" 

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
        self.savedLocal_label = self.createLabel(15, 325, normalcolor, "Last Local", self.savedLocal_clicked)
        if os.path.isfile('favorites.json'):
            self.readFavorites()
        else:
            self.initFavorites()
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
        
    def initFavorites(self):
        favorites =[]
        with open("favorites.json", "w") as json_data:
            favorites.append({"name":"FM WING", 
                    "url": "http://mtist.as.smartstream.ne.jp/30044/livestream/playlist.m3u8",
                    "image":"https://i.imgur.com/1zsbpOD.jpg",
                    "type": "audio" })
            json.dump(favorites, json_data, indent=4)
        json_data.close()

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
                print("tunein streamURL = ", url)
            else:
                url = self.items[item].get("url")
            # ------PARSE BEGINS------
            if (".pls" in url):
                try:
                    print(".pls detected")
                    req = urllib.request.urlopen(url)
                    file = req.read()
                    decodedFile = file.decode() # From bytes to str
                    #print ("Pre-parsed URL", decodedFile)
                    #print ("file is type", type(decodedFile))
                    pattern = re.compile("ht.+(?=\r)")
                    url = pattern.findall(decodedFile)[0] # Get only the first url of the list
                    print("Parsed URL: ", url)                    
                except Exception as msg:
                    print(msg)
            if (".m3u" in url and not (".m3u8" in url)):
                try:
                    print(".m3u detected")
                    req = urllib.request.urlopen(url)
                    file = req.read()
                    decodedFile = file.decode() # From bytes to str
                    #print ("Pre-parsed URL", decodedFile)
                    #print ("file is type", type(decodedFile))
                    pattern = re.compile("ht.+")
                    url = pattern.findall(decodedFile)[0] # Get only the first url of the list
                    print("Parsed URL: ", url)                    
                except Exception as msg:
                    print(msg)
            # ------PARSE ENDS------
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
        self.changeLabel(self.local_label, normalcolor, "Local File")
        self.items = self.favorites
        self.menu = "Favorites"
        self.sMenu.setItems(self.items)
    
    
    def pinguin_clicked(self):
        self.changeLabel(self.fav_label, normalcolor, "Favorites")
        self.changeLabel(self.pinguin_label, highlight, "Pinguin")
        self.changeLabel(self.tuneIn_label, normalcolor, "TuneIn") 
        self.changeLabel(self.somafm_label, normalcolor, "SomaFm") 
        self.changeLabel(self.local_label, normalcolor, "Local File")
        self.items = self.pinguin
        self.menu = "Pinguin"
        self.sMenu.setItems(self.items)
    
    
     
    def tuneIn_clicked(self):
        self.changeLabel(self.fav_label, normalcolor, "Favorites") 
        self.changeLabel(self.pinguin_label, normalcolor, "Pinguin")
        self.changeLabel(self.tuneIn_label, highlight, "TuneIn")  
        self.changeLabel(self.somafm_label, normalcolor, "SomaFm") 
        self.changeLabel(self.local_label, normalcolor, "Local File")
        self.items = self.tuneIn.getOverview()
        self.menu = "tuneIn"
        self.sMenu.setItems(self.items)
    
            
    def somafm_clicked(self):
        self.changeLabel(self.fav_label, normalcolor, "Favorites")  
        self.changeLabel(self.pinguin_label, normalcolor, "Pinguin")
        self.changeLabel(self.tuneIn_label, normalcolor, "TuneIn") 
        self.changeLabel(self.somafm_label, highlight, "SomaFm")
        self.changeLabel(self.local_label, normalcolor, "Local File")
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
        if self.items != None:
            self.menu = "Local File"
            self.sMenu.setItems(self.items)
        else:
            print("No file selected")
            self.radio.showArtist("No file selected. Try again")
            self.menuActive = None
            self.radio.show()
            self.hide()

    def savedLocal_clicked(self):
        self.changeLabel(self.fav_label, normalcolor, "Favorites")  
        self.changeLabel(self.pinguin_label, normalcolor, "Pinguin")
        self.changeLabel(self.tuneIn_label, normalcolor, "TuneIn") 
        self.changeLabel(self.somafm_label, normalcolor, "SomaFm")
        self.changeLabel(self.local_label, normalcolor, "Local File")
        self.items = local.get_savedLocal()
        if self.items != None:
            self.menu = "Last Local"
            self.sMenu.setItems(self.items)
        else:
            print("This file is empty/No file")
            self.radio.showArtist("Empty File")
            self.menuActive = None
            self.radio.show()
            self.hide()


    def addFavorite_clicked(self):
        for item in self.favorites:
            if (item.get("url") == self.playing_url) or  (self.playing_url == ""):
                return #already in playlist
            
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
            
            
         
        
        
