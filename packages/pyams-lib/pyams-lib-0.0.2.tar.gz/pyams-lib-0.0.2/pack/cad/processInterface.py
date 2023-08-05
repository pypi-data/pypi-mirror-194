#-------------------------------------------------------------------------------
# Name:        runInterface
# Purpose:
# Author:      D.fathi
# Created:     09/10/2022
# Copyright:   (c) D.fathi 2022
# Licence:     <your licence>
#-------------------------------------------------------------------------------


import sys
import time
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget, QPushButton,QDialog, QProgressBar, QVBoxLayout, QApplication, QPlainTextEdit
from PyQt5.QtCore import QProcess
import re

# A regular expression, to extract the % complete.
progress_re = re.compile("Total complete: (\d+)%")

def simple_percent_parser(output):
    """
    Matches lines using the progress_re regex,
    returning a single integer for the % progress.
    """
    m = progress_re.search(output)
    if m:
        pc_complete = m.group(1)
        return int(pc_complete)



class processAnalysis:
    def __init__(self,main,test,title,result):
        self.w = QDialog()
        self.w.resize(600,400)
        self.main=main;
        self.w.setWindowTitle(title)
        self.w.setWindowIcon(main.setIcon);
        self.p = None
        self.result=result
        self.test=test
        self.main=main

        self.btn = QPushButton("Execute")
        self.btn.pressed.connect(self.start_process)
        self.text = QPlainTextEdit()
        self.text.setReadOnly(True)
        self.progress = QProgressBar(self.w)
        self.progress.setValue(0)

        l = QVBoxLayout()
        l.addWidget(self.btn)
        l.addWidget(self.text)
        l.addWidget(self.progress)
        self.w.setLayout(l)

       # self.w.setCentralWidget(w)

    def message(self, s):
        self.text.appendPlainText(s)

    def start_process(self):
        if self.p is None:  # No process running.
            self.message("Executing process")
            self.p = QProcess()  # Keep a reference to the QProcess (e.g. on self) while it's running.
            self.p.readyReadStandardOutput.connect(self.handle_stdout)
            self.p.readyReadStandardError.connect(self.handle_stderr)
            self.p.stateChanged.connect(self.handle_state)
            self.p.finished.connect(self.process_finished)  # Clean up once complete.
            self.p.start("python", [str(self.test)])




    def handle_stderr(self):
        data = self.p.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        # Extract progress if it is in the data.
        progress = simple_percent_parser(stderr)
        if progress:
            self.progress.setValue(progress)
        else:
            self.message(stderr)



    def handle_stdout(self):
        data = self.p.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        self.message(stdout)

    def handle_state(self, state):
        states = {
            QProcess.NotRunning: 'Not running',
            QProcess.Starting: 'Starting',
            QProcess.Running: 'Running',
        }
        state_name = states[state]
        self.message(f"State changed: {state_name}")

    def process_finished(self):
        self.message("Process finished.")
        self.p = None
        self.progress.setValue(100)
        try:
           with open(self.result, "r") as file:
              last_line = file.readlines()[-1]
           self.main.ui.m_webview.page().runJavaScript("setDataPlot(["+last_line+"]);");
           self.btn.setText("Close")
           self.btn.pressed.connect(self.close)
           #print(last_line)
           import os
           os.remove(self.result)
        except:
           pass

    def close(self):
        self.w.close();



    def show(self):
        self.w.show()


