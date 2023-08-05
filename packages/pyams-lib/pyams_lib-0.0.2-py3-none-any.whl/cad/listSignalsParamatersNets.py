#-------------------------------------------------------------------------------
# Name:        get list of signals, params and nodes from circuit
# Author:      d.fathi
# Created:     22/02/2023
# Update:      22/02/2023
# Copyright:   (c) pyams 2023
# Licence:     free  "GPLv3"
#-------------------------------------------------------------------------------


from PyQt5 import QtCore, QtGui, QtWidgets
from collections import deque
from PyQt5.QtCore import QProcess
import os
import data_rc

#-------------------------------------------------------------------------------
# class Ui_DialogListSignalsParamaters: intrface of dialog List of Signals
#                                         &Paramaters.
#-------------------------------------------------------------------------------

class Ui_DialogListSignalsParamaters(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(449, 510)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.treeView = QtWidgets.QTreeView(Dialog)
        self.treeView.setObjectName("treeView")
        self.verticalLayout.addWidget(self.treeView)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))

def getImage(value):
    if value['type']=='paramater':
        return ":image/paramsignals/param.png"
    elif (value['type']=='signal')and (value['description']=='voltage')and (value['dir']=='out'):
         return ":image/paramsignals/vout.png"
    elif (value['type']=='signal')and (value['description']=='voltage')and (value['dir']=='in'):
         return ":image/paramsignals/vin.png"
    elif (value['type']=='signal')and (value['dir']=='out'):
         return ":image/paramsignals/iout.png"
    elif (value['type']=='signal')and (value['dir']=='in'):
         return ":image/paramsignals/iin.png"
    elif (value['type']=='wire'):
         return ":image/paramsignals/node.png"

#-------------------------------------------------------------------------------
# class dialogListSignalsParamaters:  dialog List of Signals
#                                         & Paramaters.
#-------------------------------------------------------------------------------


class listSignalsParamatersNets:
    def __init__(self,test,result):
        self.test=test
        self.result=result
        self.w = QtWidgets.QDialog()

        self.path='';
        self.pathLib='';
        self.p = None
        self.start_process()
        self.err=False;



    def start_process(self):
            self.p = QProcess()  # Keep a reference to the QProcess (e.g. on self) while it's running.
            self.p.readyReadStandardOutput.connect(self.handle_stdout)
            self.p.readyReadStandardError.connect(self.handle_stderr)
            self.p.stateChanged.connect(self.handle_state)
            self.p.finished.connect(self.process_finished)  # Clean up once complete.
            self.p.start("python", [str(self.test)])



    def handle_stderr(self):
        data = self.p.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        '#-----------stderr-----------#'
        if not(self.err):
           self.text = QtWidgets.QTextEdit()
           self.layout = QtWidgets.QVBoxLayout(self.w)
           self.layout.addWidget(self.text)
        self.text.append(stderr)
        self.err=True


    def handle_stdout(self):
        data = self.p.readAllStandardOutput()
        '#-----------stdout-----------#'
        self.err=False


    def handle_state(self, state):
        states = {
            QProcess.NotRunning: 'Not running',
            QProcess.Starting: 'Starting',
            QProcess.Running: 'Running',
        }
        state_name = states[state]
        print(f"State changed: {state_name}")

    def process_finished(self):

       '#-----------Process finished-----------#'
       if not(self.err):
         try:
           with open(self.result, "r", encoding="utf-8") as file:
              lisval = file.readlines()[-1]
           import os
           os.remove(self.result)
           print(lisval)
           self.lisval=eval(lisval)
           self.ui = Ui_DialogListSignalsParamaters()
           self.ui.setupUi(self.w)
           self.model = QtGui.QStandardItemModel()
           self.model.setHorizontalHeaderLabels(['Name'])#, 'Type', 'Description'
      #  self.model.resizeSection(0, 42);
           self.ui.treeView.setModel(self.model)
           self.ui.treeView.header().resizeSection(0, 150);#setStyleSheet("QTreeView::item { width: 100px }")
           self.ui.treeView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
           self.ui.treeView.clicked.connect(self.treeClicked)
           self.importData(self.lisval)
           self.ui.treeView.expandAll()
           self.pos='None'
           self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False);
         except Exception as e: # work on python 3.x
            print('Error: '+ str(e));


    def treeClicked(self, index):
        row=index.row()
        column=index.column()
        data=index.data()
        if len(data.split('.'))>1:
           self.pos=data
           self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(True);
        else:
           self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False);

    def importData(self, data, root=None):
        self.model.setRowCount(0)
        if root is None:
            root = self.model.invisibleRootItem()
        seen = {}   # List of  QStandardItem
        values = deque(data)
        while values:
            value = values.popleft()
            if value['unique_id'] == 1:
                parent = root
            else:
                pid = value['parent_id']
                if pid not in seen:
                    values.append(value)
                    continue
                parent = seen[pid]
            unique_id = value['unique_id']
            parent.appendRow([
                QtGui.QStandardItem(QtGui.QIcon(getImage(value)),value['short_name'])
               # QStandardItem(value['type']),
               # QStandardItem(value['description'])
            ])
            seen[unique_id] = parent.child(parent.rowCount() - 1)
            #seen[unique_id].QStandardItem(QIcon("4.bmp"))

    def show(self):
        self.w.show()