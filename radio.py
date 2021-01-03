from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QMessageBox
import clockDialog
import platform
import queue

import os.path
import clock
import mpd
import station
import labelClickable
import urllib
import time
import configparser



HOST = "localhost"
PORT = 6600



class radio():
    def __init__(self, gui, dia):
        self.gui = gui
        self.dia = dia
        self.menuActive = True
        
        if "arm" in platform.machine():
            print("ARM Detected, so probably Raspberry")
            import rpi_backlight as bl
            import lircradio
           
            # Backlight
            bl.set_brightness(100) # start up with full brightness
            
            # LIRC remote
            lircQueue = queue.Queue()
            
            self.LircObject = lircradio.LircInterface(lircQueue)
            self.LircObject.start()
            
            self.LircHandler = lircradio.LircHandler(lircQueue)
            self.lircTimer = QtCore.QTimer()
            self.lircTimer.timeout.connect(self.LircHandler.timerCall)
            self.lircTimer.start(1000)
            self.LircHandler.addCallback("ok", self.ok_clicked)
            self.LircHandler.addCallback("back", self.back_clicked)
            self.LircHandler.addCallback("up", self.up_clicked)
            self.LircHandler.addCallback("down", self.down_clicked)
            self.LircHandler.addCallback("left", self.left_clicked)
            self.LircHandler.addCallback("right", self.right_clicked)
            self.LircHandler.addCallback("power", self.power_clicked)
        else:
            print("No ARM, so no Raspberry")
            
        self.sDialog = station.SelectStation()
        dia.setStyleSheet("QWidget#Dialog {background-image: url(radio-cropped.png);}")
        #dia.setStyleSheet("QWidget#Dialog {background-color: black;}")
        self.cDialog = clock.Clock(self)
        
        self.infoTimer = QtCore.QTimer()
        self.infoTimer.timeout.connect(self.timercall)
        self.infoTimer.start(5000)
        
        font = QtGui.QFont()
        font.setFamily("Droid Sans")
        font.setPointSize(28)
        font.setBold(True)
        font.setWeight(75)
        
        self.labelStation = labelClickable.QLabelClickable(self.dia)
        self.labelStation.setFont(font)
        self.labelStation.setGeometry(28, 415, 750, 60)
        self.labelStation.setText("<font color='lightGray'> Back </font>")
        self.labelStation.clicked.connect(self.selectStation_clicked)
        self.showArtist("")
        self.showSong("")
        if os.path.isfile('config.cfg'):
            self.getLastPlayed()
        else:
            initConfig()

        self.showStation(self.last_name)
        self.showTime()
        self.showPicture(self.last_image)
        
        self.client = mpd.MPDClient()       # create client object
        self.client.timeout = 2             # network timeout in seconds (floats allowed), default: None
        self.client.idletimeout = None      # timeout for fetching the result of the idle command is handled seperately, default: None
        
        self.number = 0
        self.clear()
        self.addStation(self.lasturl)
        print("Starting")
        self.play(self.number)
        self.status = "playing"
        self.getShowInfo()
       
    def getLastPlayed(self):
        cfg = configparser.ConfigParser()
        cfg.read("config.cfg")
        self.lasturl = cfg.get("station", "last_url", raw=True)
        self.last_name = cfg.get("station", "last_name", raw=True)
        self.last_image = cfg.get("station", "last_image", raw=True)
 
        
    def setLastPlayed(self):  
        cfg = configparser.ConfigParser()
        cfg.add_section("station")
        cfg.set("station", "last_url",  self.lasturl)
        cfg.set("station", "last_name",  self.last_name)
        cfg.set("station", "last_image",  self.last_image)
        with open("config.cfg", "w", encoding='utf-8') as configfile:
            cfg.write(configfile)
    
    def initConfig():  
        cfg = configparser.ConfigParser()
        cfg.add_section("station")
        cfg.set("station", "last_url",  "https://streams.pinguinradio.com/PinguinClassics192.mp3")
        cfg.set("station", "last_name",  "A new config file has appeared. Please choose a station")
        cfg.set("station", "last_image",  "https://i.imgur.com/1zsbpOD.jpg")
        with open("config.cfg", "w", encoding='utf-8') as configfile:
            cfg.write(configfile)        
        
       
    def showClock(self):
        self.cDialog.show()
        
    
    def hideClock(self):
        self.cDialog.hide()
           
       
    def show(self):
        self.menuActive = True
        self.dia.show()  
        
    def hide(self):
        self.menuActive = False
        self.dia.hide()   
    
       
    def timercall(self):
        self.getShowInfo()
        self.showTime()
  
     
    def selectStation_clicked(self):
        self.sDialog.showSelectStation(self)
        self.hide()
  
    
    def connect(self):
        try:
            self.client.connect(HOST, PORT)
        except:
            print("could not connect")
            
                
    def disconnect(self): 
        try:       
            self.client.close()
            self.client.disconnect()
        except:
            print("could not disconnect")
        
    
    def addStation(self, station):
        self.lasturl = station
        self.connect()
        try:
            self.client.add(station)
        except mpd.CommandError:
            print("Station not added")
        self.disconnect()    
    
    
    def clear(self):
        self.connect()
        try:
            self.client.clear()
        except: 
            print("could not play")
        self.disconnect()    
    
    def playAfterSandby(self):
        self.clear()
        self.addStation(self.lasturl)
        time.sleep(0.5)
        self.play(0)
    
    
    def play(self, number):
        self.connect()
        try:
            self.client.play(number)
        except: 
            print("could not play")
        self.status = "playing"
        self.disconnect()    
    
    
    def playNew(self, url, name):
        self.last_name = name
        self.lasturl = url
        self.clear()
        self.addStation(url)
        self.showStation(name)
        time.sleep(0.5)
        self.connect()
        try:
            self.client.play(0)
        except: 
            print("could not play")
        self.status = "playing"
        self.disconnect()   
        self.setLastPlayed() 
            
                     
    def getInfo(self):
        self.connect()
        try:
            info = self.client.currentsong()
        except:
            return ""
        self.disconnect()
        return info


    def stop(self):
        self.connect()
        try:
            print("stopping")
            self.client.stop()
        except:
            pass
        self.status = "stopped"
    
       
    def getShowInfo(self):
        if self.status == "playing":
            info = self.getInfo()
            song = info.get("title")
            if song != None:
                song = song.split('-')
                self.showArtist(song[0])
                self.showSong(song[1])
               
        
    #################################################################################################
    
    def showStation(self, station):
        self.labelStation.setText("<font color='lightGray'>" + station + "</font>")
 
    
    def showSong(self, song):
        self.gui.labelSong.setText("<font color='white'>" + song + "</font>")
        
        
    def showArtist(self, artist):
        self.gui.labelArtist.setText("<font color='white'>" + artist + "</font>")
        
    
    def showTime(self):
        self.timeString = time.strftime('%H:%M', time.localtime())
        self.gui.labelTime.setText("<font color='white'>" +self.timeString+ "</font>")
        self.cDialog.clock.labelTime.setText("<font color='white'>" +self.timeString+ "</font>")
        self.dateString = time.strftime("%A %d %B", time.localtime())
        self.gui.labelDate.setText("<font color='white'>" +self.dateString+ "</font>")
        self.cDialog.clock.labelDate.setText("<font color='white'>" +self.dateString+ "</font>")
        

    def showPicture(self, url):
        try: 
            data = urllib.request.urlopen(url).read()
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(data)
            self.gui.labelPic.resize(200, 200)
            self.gui.labelPic.setPixmap(pixmap.scaled(self.gui.labelPic.size(), QtCore.Qt.IgnoreAspectRatio))
        except:
            pass   
        self.last_image = url     


    ###############################################################################
    # Remote control

    def ok_clicked(self):
        if self.menuActive:
            self.sDialog.showSelectStation(self)
            self.hide()
        else:
            self.sDialog.remoteCommand("ok")    
    
    def back_clicked(self):
        self.sDialog.remoteCommand("back")
        
    
    def up_clicked(self):
        self.sDialog.remoteCommand("up")
        
    
    def down_clicked(self):
        self.sDialog.remoteCommand("down")
    
    
    def left_clicked(self):
        self.sDialog.remoteCommand("left")
        
        
    def right_clicked(self):
        self.sDialog.remoteCommand("right")    
    
        
    def power_clicked(self):
        if self.menuActive == True:
            self.showClock()
            self.hide()
        else:
            self.cDialog.remoteCommand("power")
            self.sDialog.remoteCommand("power")
            
        
        
   