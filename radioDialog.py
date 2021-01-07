# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'radioDialogJUDYkv.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(800, 480)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setStyleSheet(u"")
        self.labelArtist = QLabel(Dialog)
        self.labelArtist.setObjectName(u"labelArtist")
        self.labelArtist.setGeometry(QRect(30, 20, 751, 51))
        font = QFont()
        font.setFamily(u"Droid Sans")
        font.setPointSize(32)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        self.labelArtist.setFont(font)
        self.labelArtist.setLayoutDirection(Qt.RightToLeft)
        self.labelArtist.setAutoFillBackground(False)
        self.labelTime = QLabel(Dialog)
        self.labelTime.setObjectName(u"labelTime")
        self.labelTime.setGeometry(QRect(300, 160, 441, 181))
        font1 = QFont()
        font1.setFamily(u"Droid Sans")
        font1.setPointSize(120)
        font1.setBold(True)
        font1.setWeight(75)
        font1.setKerning(True)
        self.labelTime.setFont(font1)
        self.labelSong = QLabel(Dialog)
        self.labelSong.setObjectName(u"labelSong")
        self.labelSong.setGeometry(QRect(30, 90, 751, 51))
        self.labelSong.setFont(font)
        self.labelPic = QLabel(Dialog)
        self.labelPic.setObjectName(u"labelPic")
        self.labelPic.setGeometry(QRect(30, 190, 59, 14))
        self.labelDate = QLabel(Dialog)
        self.labelDate.setObjectName(u"labelDate")
        self.labelDate.setGeometry(QRect(310, 330, 481, 51))
        font2 = QFont()
        font2.setFamily(u"Droid Sans")
        font2.setPointSize(30)
        font2.setBold(True)
        font2.setWeight(75)
        font2.setKerning(True)
        self.labelDate.setFont(font2)
        self.labelDate.setLayoutDirection(Qt.RightToLeft)
        self.labelDate.setAutoFillBackground(False)
        self.sliderVolume = QSlider(Dialog)
        self.sliderVolume.setObjectName(u"sliderVolume")
        self.sliderVolume.setGeometry(QRect(50, 370, 160, 16))
        self.sliderVolume.setMaximum(100)
        self.sliderVolume.setPageStep(5)
        self.sliderVolume.setOrientation(Qt.Horizontal)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.labelArtist.setText(QCoreApplication.translate("Dialog", u"-", None))
#if QT_CONFIG(whatsthis)
        self.labelTime.setWhatsThis(QCoreApplication.translate("Dialog", u"It's a clock", None))
#endif // QT_CONFIG(whatsthis)
        self.labelTime.setText(QCoreApplication.translate("Dialog", u"22:22", None))
        self.labelSong.setText(QCoreApplication.translate("Dialog", u"-", None))
#if QT_CONFIG(whatsthis)
        self.labelPic.setWhatsThis(QCoreApplication.translate("Dialog", u"Station Image", None))
#endif // QT_CONFIG(whatsthis)
        self.labelPic.setText(QCoreApplication.translate("Dialog", u"Pic", None))
        self.labelDate.setText(QCoreApplication.translate("Dialog", u"-", None))
#if QT_CONFIG(whatsthis)
        self.sliderVolume.setWhatsThis(QCoreApplication.translate("Dialog", u"Volume Slider", None))
#endif // QT_CONFIG(whatsthis)
    # retranslateUi
