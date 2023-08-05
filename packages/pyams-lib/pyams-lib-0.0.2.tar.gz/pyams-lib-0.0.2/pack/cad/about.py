#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      D.fathi
#
# Created:     02/09/2022
# Copyright:   (c) D.fathi 2022
# Licence:     <your licence>
#-------------------------------------------------------------------------------


from PyQt5 import QtCore, QtGui, QtWidgets
from collections import deque
import os
import data_rc
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QMainWindow, QApplication

#-------------------------------------------------------------------------------
# class ui_about:  interface of dialog about.
#-------------------------------------------------------------------------------

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("About")
        Dialog.setEnabled(True)
        Dialog.resize(712, 275)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/image/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setSizeGripEnabled(False)
        Dialog.setModal(False)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setStyleSheet("")
        self.label.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.label.setText("")
        self.label.setTextFormat(QtCore.Qt.PlainText)
        self.label.setPixmap(QtGui.QPixmap(":/image/logo.png"))
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setToolTip("")
        self.label_2.setToolTipDuration(-1)
        self.label_2.setAutoFillBackground(False)
        self.label_2.setStyleSheet("")
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept) # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("About", "About"))
        self.label_2.setText(_translate("About", "<html><head/><body><p align=\"center\"><span style=\" font-family:\'monospace\'; font-size:10pt; font-weight:600; color:#000000;\">PyAMS:Python for Analog and Mixed Signals</span></p><p align=\"center\"><span style=\" font-family:\'monospace\'; font-size:10pt; font-weight:600; color:#000000;\">Version 0.0.1 </span></p><p align=\"center\"><a href=\"http://www.pyams.org\"><span style=\" font-size:10pt; text-decoration: underline; color:#0000ff;\">www.pyams.org</span></a></p><p align=\"center\"><span style=\" font-family:\'monospace\'; font-size:10pt; font-weight:600; color:#000000;\">(c) 2021-2023</span></p></body></html>"))


#-------------------------------------------------------------------------------
# class about:  about dialog.
#-------------------------------------------------------------------------------

class about:
    def __init__(self):
        self.w = QtWidgets.QDialog()

        self.path='';
        self.pathLib='';

        self.ui = Ui_Dialog()
        self.ui.setupUi(self.w)


    def show(self):
        self.w.show()

if __name__ == '__main__':
     import sys
     app = QApplication(sys.argv)
     window = about()
     window.show()
     app.exec_()
