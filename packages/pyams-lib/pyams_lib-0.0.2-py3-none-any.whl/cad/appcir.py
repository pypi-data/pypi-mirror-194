#-------------------------------------------------------------------------------
# Name:        convert schema of circuit to PyAMS netlist
# Author:      d.fathi
# Created:     17/09/2021
# Copyright:   (c) pyams 2023
# Web:         www.PyAMS.org
# Licence:     free  "GPLv3"
#-------------------------------------------------------------------------------
from libraryManagement import openLib


#-------------------------------------------------------------------------------
# def pyamscircuit: convert schema of circuit to PyAMS netlist
#-------------------------------------------------------------------------------
def pyamscircuit(result,getdata,self):
    netList=result[3]
    option=str(result[4]);


    data=[]
    libs=['from sys import path;'];
    libs+=['path+=["../../"]'];
    libs+=['path+=["'+self.path+'"];'];
    dirs=openLib(self.path)['libs'];
    for i in range(len(dirs)):
        pos=self.path+'/'+dirs[i];
        libs+=['path+=["'+pos+'"];'];

    libs+=["import PyAMS"];
    libs+=['from PyAMS import time;']
    libs+=['from simu import AppPyAMS;']

    cir=[];
    parms=[];
    elems=[];

    for i in range(len(netList)):
        pins='","'.join(netList[i]['pins']);
        pins='("'+pins+'");';

        elems+=[netList[i]['ref']+'='+netList[i]['modelname']+pins]
        cir+=['"'+netList[i]['ref']+'":'+netList[i]['ref']]

        s='from '+netList[i]['modelname']+' import '+netList[i]['modelname'];
        if not(s in libs):
            libs+=[s]

        p=netList[i]['params'];
        parms+=[netList[i]['ref']+'.setParam("'+p+'");'];
        #for k in range(len(p)):
         #   x = p[k].split('=');
          #  parms+=[netList[i]['ref']+'.'+x[0]+'+='+'strToFloat("'+x[1]+'");'];


    if(getdata):
       temp=result[0];
       probe=','.join(temp);
    else:
       temp=result[1];
       probe=','.join(temp);




    data+=[];
    data+=[];
    data+=["#------------------------------------------------------------------"];
    for i in range(len(libs)):
        data+=[libs[i]]

    data+=[];
    data+=[];
    data+=["#------------------------------------------------------------------"];
    for i in range(len(elems)):
        data+=[elems[i]]

    data+=["#------------------------------------------------------------------"];
    for i in range(len(parms)):
        data+=[parms[i]]

    data+=[];
    data+=[];
    data+=["#------------------------------------------------------------------"];

    data+=['AppPyAMS.cad=True'];
    data+=['AppPyAMS.circuit({'+','.join(cir)+'});'];
    return data


def getNameFileResult():
    from datetime import datetime
    # datetime object containing current date and time
    now = datetime.now()
    return  now.strftime("Result_%d_%m_%Y %H_%M_%S.txt")

#-------------------------------------------------------------------------------
# def analysis:  Analysis
#-------------------------------------------------------------------------------

def analysis(self,result):
    data=pyamscircuit(result,False,self);
    analy=result[5];
    result=self.ppDir+'/'+getNameFileResult();
    test=self.ppDir+"/out/testBench.py"
    print(test)
    file =open(test, "w", encoding="utf-8")
    for element in data:
        file.write(element + "\n")
    file.write(analy[1])
    file.close();

    title='Analysis';
    from processInterface import processAnalysis
    dialog=processAnalysis(self,test,title,result);
    dialog.w.exec_()




def setDataAnalysis(l,win):
    test.AppPyAMS.update();
    win.lbl3.setText(test.AppPyAMS.getDescBar());
    a=test.AppPyAMS.getDataPlot()
    a+=[0]
    return a;

def setCommand(s):
    s='test.'+s;
    eval(s);

#-------------------------------------------------------------------------------
# def getListSignalsNodeParams: get list of signals from symboles in circuit.
#-------------------------------------------------------------------------------


def modifiedParams(self,modelName,pins,params):
    result=self.ppDir+'/out/temp/'+getNameFileResult();
    code=self.ppDir+"/out/temp/getParamaters.py";
    libs=['from sys import path;'];
    libs+=['path+=["../../"]'];
    dirs=openLib(self.path)['libs'];
    for i in range(len(dirs)):
        pos=self.path+'/'+dirs[i];
        libs+=['path+=["'+pos+'"];'];
    libs+=['from '+modelName+' import '+modelName];
    libs+=['m='+modelName+'('+pins+')'];
    libs+=['p=m.getParam("'+str(params)+'");']
    libs+=['file = open("'+str(result)+'", "w", encoding="utf-8")']
    libs+=['file.write(str(p))']
    libs+=['file.close();']

    file = open(code, "w", encoding="utf-8")
    for element in libs:
        file.write(element + "\n")
    file.close();

    from listParams import listParams
    dialog =listParams(code,result);
    dialog.w.setWindowTitle("Paramatres of:  "+modelName);
    dialog.w.setWindowIcon(self.setIcon);
    if dialog.w.exec_():
        a=dialog.getModified();
        self.ui.m_webview.page().runJavaScript("ioSetModifedParams('"+a+"');");

#-------------------------------------------------------------------------------
# def getListSignalsNodeParams: get list of signals from symboles in circuit.
#-------------------------------------------------------------------------------

def getListSignalsNodeParams(self,result):

    fout=self.ppDir+'/out/temp/'+getNameFileResult();
    code=self.ppDir+"/out/temp/test.py";
    data=pyamscircuit(result,False,self);
    n=len(data)
    data[n-2]='';

    py_file = open(self.ppDir+"/cad/getpsn.py", "r")
    content_list = py_file.readlines()

    file = open(code, "w", encoding="utf-8")
    file.write('result="'+str(fout)+'"\n')
    file.write('net='+str(result[2])+'\n')
    for element in data:
        file.write(element + "\n")
    for element in content_list:
        file.write(element)
    file.close();
    from listSignalsParamatersNets import listSignalsParamatersNets
    dialog =listSignalsParamatersNets(code,fout);
    dialog.w.setWindowTitle("Lists of signals paramatres and nodes");
    dialog.w.setWindowIcon(self.setIcon);
    if dialog.w.exec_():
        self.ui.m_webview.page().runJavaScript("ioSetPosProbe('"+dialog.pos+"');");


