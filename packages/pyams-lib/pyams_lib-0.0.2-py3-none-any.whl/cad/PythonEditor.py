#-------------------------------------------------------------------------------
# Name:        Python Editor
# Author:      D.fathi
# Created:     08/06/2022
# Update:      19/08/2022
# Copyright:   (c) PyAMS 2022
# Licence:     free
#-------------------------------------------------------------------------------

import sys


from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from dialogs import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QPushButton,QLineEdit,QDialogButtonBox,QLabel
from PyQt5.QtCore import QTimer
import syntax_pars
import os




class openCode:
    ARROW_MARKER_NUM = 8
    def __init__(self,file):
        self.file=file
        self.w = QtWidgets.QDialog()
        self.editor=QtWidgets.QPlainTextEdit()
        self.editor.setStyleSheet("""QPlainTextEdit{
                                 font-family:'Consolas';
	                             color: #ccc;
	                             background-color: #2b2b2b;}""")

        self.highlight = syntax_pars.PythonHighlighter(self.editor.document())
        self.w.resize(950, 640)
        self.layout = QtWidgets.QVBoxLayout(self.w)
        self.layout.addWidget(self.editor);
        self.editor.toPlainText().encode("utf-8")
        self.w.closeEvent=self.closeEvent
        self.modified=False



        file_exists = os.path.exists(file)
        if(file_exists):
           infile = open(file, 'r', encoding="utf-8")
           self.editor.setPlainText(infile.read())


        btns = QDialogButtonBox()
        btns.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.layout.addWidget(btns)

        btns.accepted.connect(self.w.accept)
        btns.rejected.connect(self.w.reject)
        btns.button(QDialogButtonBox.Ok).setText("Save file")
        self.editor.modificationChanged.connect(self.isModified)

    def isModified(self, have_change):
        self.modified=have_change



    def save(self):
        #file = open(self.file,'w',encoding='utf-8')
        text = self.editor.toPlainText()
        with open(self.file, 'w',encoding='utf-8') as f:
            f.write(text)

    def closeEvent(self, event):
        if self.modified:
            ret = QMessageBox.question(None, 'MessageBox', "Do you want to save your changes? ", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
            if ret == QMessageBox.Yes:
                self.save();
                event.accept();
            elif ret == QMessageBox.No:
               event.accept();
            else:
               event.ignore()

        else:
            event.accept();




def showCode(self,modelName,directory):
    file=self.setWin.path+'/'+directory+'/'+modelName+'.py'
    dialog =openCode(file);
    dialog.w.setWindowTitle("Model:  "+file);
    dialog.w.setWindowIcon(self.setWin.setIcon);
    if dialog.w.exec():
        dialog.save()

def showCodeBySymEd(self):
    file=self.setWin.filename
    if file=='NewFile.sym':
         QMessageBox.about(None, 'Model not exist','Save your new symbol');
    else:
        root, ext = os.path.splitext(file)
        file=root+'.py'
        dialog =openCode(file);
        dialog.w.setWindowTitle("Model:  "+file);
        dialog.w.setWindowIcon(self.setWin.setIcon);
        if dialog.w.exec():
             dialog.save()








def showCode(self,modelName,directory):
    file=self.setWin.path+'/'+directory+'/'+modelName+'.py'
    dialog =openCode(file);
    dialog.w.setWindowTitle("Model:  "+file);
    dialog.w.setWindowIcon(self.setWin.setIcon);
    if dialog.w.exec():
        dialog.save()

def showCodeBySymEd(self):
    file=self.setWin.filename
    if file=='NewFile.sym':
         QMessageBox.about(None, 'Model not exist','Save your new symbol');
    else:
        root, ext = os.path.splitext(file)
        file=root+'.py'
        dialog =openCode(file);
        dialog.w.setWindowTitle("Model:  "+file);
        dialog.w.setWindowIcon(self.setWin.setIcon);
        if dialog.w.exec():
             dialog.save()





if __name__ == "__main__":
    file="E:/project/PyAMS/symbols/Basic/Resistor.py"
    import sys
    app =  QtWidgets.QApplication(sys.argv)
    window = openCode(file)


    if window.w.exec():
        window.save()
