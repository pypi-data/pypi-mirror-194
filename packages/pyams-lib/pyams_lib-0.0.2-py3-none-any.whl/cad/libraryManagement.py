#-------------------------------------------------------------------------------
# Name:        Library management (to organize symbols)
# Author:      d.fathi
# Created:     20/06/2021
# Update:      30/10/2022
# Copyright:   (c) pyams
# Web:         www.Pv.PyAMS.org
# Licence:     free
#-------------------------------------------------------------------------------


from PyQt5 import QtCore, QtGui, QtWidgets
from collections import deque
import os


#-------------------------------------------------------------------------------
# class Ui_DialogOrganLibrary: interface of management type ui
#-------------------------------------------------------------------------------
class Ui_DialogOrganLibrary(object):
    def setupUi(self, DialogOrganLibrary):
        DialogOrganLibrary.setObjectName("DialogOrganLibrary")
        DialogOrganLibrary.resize(662, 375)
        self.gridLayout = QtWidgets.QGridLayout(DialogOrganLibrary)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_2 = QtWidgets.QLabel(DialogOrganLibrary)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_4.addWidget(self.label_2)
        self.listWidgetLibrary = QtWidgets.QListWidget(DialogOrganLibrary)
        self.listWidgetLibrary.setObjectName("listWidgetLibrary")
        self.verticalLayout_4.addWidget(self.listWidgetLibrary)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.pButtonUpDir = QtWidgets.QPushButton(DialogOrganLibrary)
        self.pButtonUpDir.setObjectName("pButtonUpDir")
        self.verticalLayout_2.addWidget(self.pButtonUpDir)
        self.pButtonDownDir = QtWidgets.QPushButton(DialogOrganLibrary)
        self.pButtonDownDir.setObjectName("pButtonDownDir")
        self.verticalLayout_2.addWidget(self.pButtonDownDir)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_3 = QtWidgets.QLabel(DialogOrganLibrary)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_5.addWidget(self.label_3)
        self.listWidgetSym = QtWidgets.QListWidget(DialogOrganLibrary)
        self.listWidgetSym.setObjectName("listWidgetSym")
        self.verticalLayout_5.addWidget(self.listWidgetSym)
        self.horizontalLayout.addLayout(self.verticalLayout_5)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem3)
        self.pButtonUpSym = QtWidgets.QPushButton(DialogOrganLibrary)
        self.pButtonUpSym.setObjectName("pButtonUpSym")
        self.verticalLayout_6.addWidget(self.pButtonUpSym)
        self.pButtonDownSym = QtWidgets.QPushButton(DialogOrganLibrary)
        self.pButtonDownSym.setObjectName("pButtonDownSym")
        self.verticalLayout_6.addWidget(self.pButtonDownSym)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem4)
        self.horizontalLayout.addLayout(self.verticalLayout_6)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(DialogOrganLibrary)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(DialogOrganLibrary)
        self.buttonBox.accepted.connect(DialogOrganLibrary.accept) # type: ignore
        self.buttonBox.rejected.connect(DialogOrganLibrary.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(DialogOrganLibrary)

    def retranslateUi(self, DialogOrganLibrary):
        _translate = QtCore.QCoreApplication.translate
        DialogOrganLibrary.setWindowTitle(_translate("DialogOrganLibrary", "Organizing and modifying the library"))
        self.label_2.setText(_translate("DialogOrganLibrary", "Library"))
        self.pButtonUpDir.setText(_translate("DialogOrganLibrary", "Up"))
        self.pButtonDownDir.setText(_translate("DialogOrganLibrary", "Down"))
        self.label_3.setText(_translate("DialogOrganLibrary", "Symbols"))
        self.pButtonUpSym.setText(_translate("DialogOrganLibrary", "Up"))
        self.pButtonDownSym.setText(_translate("DialogOrganLibrary", "Down"))



#-------------------------------------------------------------------------------
# get symbols from library
#-------------------------------------------------------------------------------
def getSymbolsFromLib(path,symDir,items):
    symDir=path+'/'+symDir
    exists = os.path.exists(symDir)
    if(exists):
      s=[]
      for i in range(len(items)):
         f = open(symDir+'/'+items[i], "r")
         d=items[i].split('.')
         s+=[{'sym':f.read(),'name':d[0]}]
         f.close()
      return s;
    else:
        return []

#-------------------------------------------------------------------------------
# get list of directory
#-------------------------------------------------------------------------------
def dirList(directory):
    a=[]
    rootdir = directory
    for file in os.listdir(directory):
       d = os.path.join(rootdir, file)
       if os.path.isdir(d):
         if(d.find("__pycache__")==-1):
          a+=[d]
          s=dirList(d);
          if len(s)!=0:
           a+=s;
    return a;


#-------------------------------------------------------------------------------
# get list of files
#-------------------------------------------------------------------------------
def getFiles(symDir):
    s=[]
    try:
        import glob
        os.chdir(symDir)
        items=[]
        for file in glob.glob("*.sym"):
            items.append(file)
        for i in range(len(items)):
          f = open(symDir+'/'+items[i], "r")
          s+=[f.read()]
          f.close()
        return s;
    except:
        return s;

#-------------------------------------------------------------------------------
# get names of files type '.sym'
#-------------------------------------------------------------------------------

def getNameFilesSym(symDir):
    items=[]
    try:
        import glob
        os.chdir(symDir)
        items=[]
        for file in glob.glob("*.sym"):
            items.append(file)
        return  items;
    except:
        return  items;


#-------------------------------------------------------------------------------
# save and open librarary file
#-------------------------------------------------------------------------------

def saveLib(setDir,library):
    f=open(setDir+'/library.txt', 'w')
    f.write(str(library))
    f.close()


def openLib(setDir):
    f = open(setDir+'/library.txt', "r")
    s=f.read()
    f.close()

    res = []
    for path in os.listdir(setDir):
      if not(os.path.isfile(os.path.join(setDir, path))):
        res.append(path)

    import ast
    libs=ast.literal_eval(s)
    libsDir=libs['libs']
    updateLibs=[]
    for i in range(len(libsDir)):
        if(libsDir[i] in res):
            updateLibs+=[libsDir[i]]
    for i in range(len(res)):
        if not(res[i] in updateLibs):
            updateLibs+=[res[i]]

    libs['libs']=updateLibs;
    for i in range(len(updateLibs)):
        if updateLibs[i] in libs:
           l=libs[updateLibs[i]]
           t=getNameFilesSym(setDir+'/'+updateLibs[i])

           j=0;
           while j < len(l):
             if not(l[j] in t):
               l.remove(l[j]);
               j=0;
             else:
               j=j+1;

           j=0;
           while j < len(t):
             if not(t[j] in l):
                l+=[t[j]];
             j=j+1;
           libs[updateLibs[i]]=l
        else:
            libs[updateLibs[i]]=getNameFilesSym(setDir+'/'+updateLibs[i])

    f=open(setDir+'/library.txt', 'w')
    f.write(str(libs))
    f.close()

    return libs




#-------------------------------------------------------------------------------
#  interface of management type dialog
#-------------------------------------------------------------------------------

class libraryManagement:
    def __init__(self):
        self.w = QtWidgets.QDialog()
        self.ui = Ui_DialogOrganLibrary()
        self.ui.setupUi(self.w)
        self.setButtonConnections()
        self.updateButtonStatus()
        self.libs=[]

    def getDirctory(self,pos):
        self.posDir=pos;
        self.libs=openLib(pos)
        self.listDirSym=self.libs['libs']

        for i in range(len(self.listDirSym)):
           self.ui.listWidgetLibrary.addItem(self.listDirSym[i])

    def setButtonConnections(self):
        self.ui.listWidgetLibrary.itemSelectionChanged.connect(self.updateButtonStatus)
        self.ui.listWidgetSym.itemSelectionChanged.connect(self.updateButtonSymStatus)
        self.ui.pButtonUpDir.clicked.connect(self.buttonUpClicked)
        self.ui.pButtonDownDir.clicked.connect(self.buttonDownClicked)
        self.ui.pButtonUpSym.clicked.connect(self.buttonUpSymClicked)
        self.ui.pButtonDownSym.clicked.connect(self.buttonDownSymClicked)


    def buttonAddClicked(self):
        folderpath = str(QtWidgets.QFileDialog.getExistingDirectory(None, 'Select Folder'))
        if folderpath:
            r=folderpath.replace(self.posDir,"");
            std=len(r)!=len(folderpath)
            used=True;
            a=os.path.split(folderpath);
            for i in range(len(self.libs)):
                if (a[1]==self.libs[i]['name']) and (r==self.libs[i]['destination']) :
                    used=False;

            if(a[1]==''):
                used=False;

            if used:
               self.libs+=[{'name':a[1], 'std':std, 'destination':r}]
               self.ui.listWidgetLibrary.addItem(a[1])


    def buttonRemoveClicked(self):
        row = self.ui.listWidgetLibrary.currentRow()
        rowItem = self.ui.listWidgetLibrary.takeItem(row)
        del self.libs[row]

    def buttonUpClicked(self):
        rowIndex = self.ui.listWidgetLibrary.currentRow()
        currentItem = self.ui.listWidgetLibrary.takeItem(rowIndex)
        a=self.listDirSym[rowIndex]
        self.listDirSym[rowIndex]=self.listDirSym[rowIndex-1]
        self.listDirSym[rowIndex-1]=a
        self.ui.listWidgetLibrary.insertItem(rowIndex - 1, currentItem)
        self.ui.listWidgetLibrary.setCurrentRow(rowIndex - 1)




    def buttonDownClicked(self):
        rowIndex = self.ui.listWidgetLibrary.currentRow()
        currentItem = self.ui.listWidgetLibrary.takeItem(rowIndex)
        a=self.listDirSym[rowIndex]
        self.listDirSym[rowIndex]=self.listDirSym[rowIndex+1]
        self.listDirSym[rowIndex+1]=a

        self.ui.listWidgetLibrary.insertItem(rowIndex + 1, currentItem)
        self.ui.listWidgetLibrary.setCurrentRow(rowIndex + 1)







    def buttonUpSymClicked(self):
        rowIndex = self.ui.listWidgetSym.currentRow()
        currentItem = self.ui.listWidgetSym.takeItem(rowIndex)
        self.ui.listWidgetSym.insertItem(rowIndex - 1, currentItem)
        self.ui.listWidgetSym.setCurrentRow(rowIndex - 1)
        self.libs[self.nameDirSym]=[str(self.ui.listWidgetSym.item(i).text()) for i in range(self.ui.listWidgetSym.count())]




    def buttonDownSymClicked(self):
        rowIndex = self.ui.listWidgetSym.currentRow()
        currentItem = self.ui.listWidgetSym.takeItem(rowIndex)
        self.ui.listWidgetSym.insertItem(rowIndex + 1, currentItem)
        self.ui.listWidgetSym.setCurrentRow(rowIndex + 1)
        self.libs[self.nameDirSym]=[str(self.ui.listWidgetSym.item(i).text()) for i in range(self.ui.listWidgetSym.count())]


    def saveLib(self):
      saveLib(self.posDir,self.libs);

    def updateButtonStatus(self):
        if bool(self.ui.listWidgetLibrary.selectedItems()):
           index=self.ui.listWidgetLibrary.currentRow()
           self.getFiles(index)
        self.ui.pButtonUpDir.setDisabled(not bool(self.ui.listWidgetLibrary.selectedItems()) or self.ui.listWidgetLibrary.currentRow() == 0)
        self.ui.pButtonDownDir.setDisabled(not bool(self.ui.listWidgetLibrary.selectedItems()) or self.ui.listWidgetLibrary.currentRow() == self.ui.listWidgetLibrary.count() - 1)


    def updateButtonSymStatus(self):
        self.ui.pButtonUpSym.setDisabled(not bool(self.ui.listWidgetSym.selectedItems()) or self.ui.listWidgetSym.currentRow() == 0)
        self.ui.pButtonDownSym.setDisabled(not bool(self.ui.listWidgetSym.selectedItems()) or self.ui.listWidgetSym.currentRow() == self.ui.listWidgetSym.count() - 1)


    def getFiles(self,index):
        import glob, os
        self.nameDirSym=self.listDirSym[index]
        d=self.libs[self.nameDirSym];
        self.ui.listWidgetSym.clear();
        for i in range(len(d)):
            self.ui.listWidgetSym.addItem(d[i])


    def show(self):
        self.w.show()




#-------------------------------------------------------------------------------
# __main__: test Dialog
#-------------------------------------------------------------------------------
if __name__ == "__main__":
     import sys
     app = QtWidgets.QApplication(sys.argv)
     window = libraryManagement()
     window.show()
     app.exec_()
