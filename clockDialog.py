# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'clock.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Clock")
        Dialog.resize(800, 480)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setStyleSheet("")
        self.labelTime = QtWidgets.QLabel(Dialog)
        self.labelTime.setGeometry(QtCore.QRect(190, 40, 441, 181))
        font = QtGui.QFont()
        font.setFamily("Droid Sans")
        font.setPointSize(120)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        self.labelTime.setFont(font)
        self.labelTime.setObjectName("labelTime")
        self.labelDate = QtWidgets.QLabel(Dialog)
        self.labelDate.setGeometry(QtCore.QRect(190, 220, 481, 51))
        font = QtGui.QFont()
        font.setFamily("Droid Sans")
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        self.labelDate.setFont(font)
        self.labelDate.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.labelDate.setAutoFillBackground(False)
        self.labelDate.setObjectName("labelDate")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.labelTime.setText(_translate("Dialog", "22:22"))
        self.labelDate.setText(_translate("Dialog", "-"))

