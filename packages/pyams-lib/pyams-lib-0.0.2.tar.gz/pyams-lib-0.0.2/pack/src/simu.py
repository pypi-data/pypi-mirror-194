#-------------------------------------------------------------------------------
# Name:        simulation
# Author:      d.fathi
# Created:     20/06/2017
# Update:      06/10/2021
# Copyright:   (c) pyams
# Web:         www.PyAMS.org
# Licence:     free  "GPLv3"
#-------------------------------------------------------------------------------


from PyAMS import  analysis,getStepTime
from newton import solven
from option import simulationOption
from standardFunction import controlStepTime
import PyAMS
import time


#-------------------------------------------------------------------------------
# def addRefToModel: add reference to signals and parameters
#-------------------------------------------------------------------------------
def addRefToModel(R,M):
    M.name=R
    a=dir(M)
    for i in range(len(a)):
      f=eval('M.'+a[i])
      if type(f).__name__=='signal':
        f.name=R+'.'+a[i];
      if type(f).__name__=='param':
        f.name=R+'.'+a[i];

#-------------------------------------------------------------------------------
# class simu: circuit simulation
#-------------------------------------------------------------------------------
class simu:
    def __init__(self,app,cir,output,method,Option={}):
      getStepTime.__init__();
      simulationOption.setOption(Option)
      simulationOption.Run=False;
      self.n=0;
      self.method=method
      self.output=output
      self.GetResult=False;
      self.SweepUsed=False;
      self.SweepName='';
      self.SweepPos=0;
      self.SweepList=[]
      self.cir=cir
      self.method=method
      self.ProgressPosition=0
      self.LenSweepList=1;
      self.UsedTimeInter=False;
      self.stop=False;
      self.app=app;
      if 'sweep' in method:
          self.Sweep=method['sweep']
          self.SweepUsed=True;
          self.SweepPos=0;
          self.SweepParam=self.Sweep['param'];
          self.SweepList=self.Sweep['list'];
          self.LenSweepList=len(self.SweepList)
          self.SweepParam+=self.SweepList[0];
          self.SweepName=self.Sweep['param'].name+'='+str(self.SweepList[0])+self.Sweep['param'].Unit;
      self.StartSimu();

    def StartSimu(self):

      if  self.method['mode']=='tran':

          PyAMS.time+=0.0
          self.Timestart=self.method['start'];
          self.Timestep=self.method['step'];
          self.Timestop=self.method['stop'];
          self.param=PyAMS.time;
          self.a=analysis(self.cir,self.method)
          self.leng=[self.a.len,self.a.les];
          simulationOption.SetTimeStep(self.Timestep)
          self.analyse_tr();

      if self.method['mode']=='int':
          Time+=0.0
          self.Timestart=self.method['start'];
          self.Timestep=self.method['step'];
          self.Timestop=self.method['stop'];
          self.UsedTimeInter=True;
          self.param=Time;
          self.a=analysis(self.cir,self.method)
          self.leng=[self.a.len,self.a.les];
          simulationOption.SetTimeStep(self.Timestep)
          self.analyse_InteractiveSimulation();


      if self. method['mode']=='dc':
              PyAMS.time+=0.0
              self.DCstart=self.method['start'];
              self.DCstep=self.method['step'];
              self.DCstop=self.method['stop'];
              self.param=self.method['param'];
              self.dcVal=0;
              self.a=analysis(self.cir,self.method)
              self.leng=[self.a.len,self.a.les];
              self.analyse_dc();

      if self. method['mode']=='ac':
              PyAMS.Time+=0.0
              self.ACstart=self.method['start'];
              a=pow(10.0,1/self.method['nstep']);
              self.ACstep=pow(10.0,a);
              self.ACstop=self.method['stop'];
              if 'interval' in self.method:
                if self.method['interval'] =='oct':
                    self.ACstep=pow(8.0,1/self.method['nstep']);
                elif self.method['interval'] =='lin':
                    self.ACstep=(self.ACstop-self.ACstart)/self.method['nstep'];

              self.a=analysis(self.cir,self.method)
              self.leng=[self.a.len,self.a.les];
              self.analyse_ac();



      if self.method['mode']=='op':
              PyAMS.time+=0.0
              self.method['mode']='op'
              self.a=analysis(self.cir,self.method)
              self.leng=[self.a.len,self.a.les];
              self.analyse_op();
#---------------------------------------------------------------------------
    def analyse_ac(self):
        self.analyse_op();
        self.a.getImpdence();
        self.ACVal=self.ACstart
        self.stop=False;
        def update():
            self.a.favelac(self.ACVal)
            SaveInData(self.a,self.SweepPos);
            self.ProgressPosition=self.ACVal*100/self.ACstop;
            if self.ACstop  < self.ACVal:
              self.StopAnalyse()
            self.ACVal+=self.ACstep;
        self.update=update


    def analyse_op(self):
          self.x=[]
          n,vlen,vles=self.a.getlen()
          simulationOption.len=vlen;
          simulationOption.les=vles;
          simulationOption.size=n;

          for i in range(n-1):
             self.x+=[0.0]

          self.y=self.a.favel;
          self.stop=False;
          def update():
            if not(solven(self.x,self.y)):
                hsolven(self.x,self.y);
            self.app.saveData();
            self.stop=True
          self.update=update


#---------------------------------------------------------------------------
    def updaet_analyses(self):
              PyAMS.Time+=0.0
              self.a=analysis(self.cir,self.method)
              self.leng=[self.a.len,self.a.les];

    def analyse_tr(self):
          self.x=[]
          n,vlen,vles=self.a.getlen()
          simulationOption.len=vlen;
          simulationOption.les=vles;
          simulationOption.size=n;

          for i in range(n-1):
             self.x+=[0.0]

          self.y=self.a.favel;
          self.param.value=0.0
          self.stop=False;
          simulationOption.start=True
          if simulationOption.ldt>0:
             simulationOption.TimeStep=getStepTime.GetStepTime(simulationOption.TimeStep)



          def update():
           # SimulationOption.TimeStep=0.00001;
            self.n=self.n+1
            PyAMS.time.value=simulationOption.t1
            UsedTime=getStepTime.ControlPer();
            simulationOption.t1=PyAMS.time.value
            self.x,s=solven(self.x,self.y)

            Time_Selection=controlStepTime(UsedTime)
            simulationOption.GetStep=simulationOption.t1-simulationOption.t0
            if Time_Selection or simulationOption.Start:
                self.app.saveData();
            simulationOption.Start=False;
            self.ProgressPosition=((self.SweepPos+1)/self.LenSweepList)*self.param.value*100/self.Timestop;

            if self.Timestop  < self.param.value:
               self.stop=True;

          self.update=update

    def analyse_InteractiveSimulation(self):
          self.x=[]
          for i in range(self.a.len):
             self.x+=[0.0]
          self.y=self.a.favel;
          self.param.Val=0.0
          self.stop=False;
          SimulationOption.Start=True
          if SimulationOption.ldt>0:
             SimulationOption.TimeStep=GetStepTime.GetStepTime(SimulationOption.TimeStep)



          def update():
            self.UsedResult=False;
            Time.Val=SimulationOption.t1
            UsedTime=GetStepTime.ControlPer();
            self.x,s=solven(self.x,self.y)
            Time_Selection=ControlStepTime(UsedTime)
            SimulationOption.GetStep=SimulationOption.t1-SimulationOption.t0
            if Time_Selection or SimulationOption.Start:
                self.UsedResult=True;
            SimulationOption.Start=False;
          self.update=update


    def analyse_dc(self):
          self.x=[]
          n,vlen,vles=self.a.getlen()
          simulationOption.len=vlen;
          simulationOption.les=vles;
          simulationOption.size=n;

          for i in range(n-1):
             self.x+=[0.0]

          self.y=self.a.favel;
          self.DCVal_=self.DCstart
          self.stop=False;
          def update():
            self.param.Val=self.DCVal_
            self.dcVal=self.DCVal_
            if not(solven(self.x,self.y)):
                hsolven(self.x,self.y);
            self.app.saveData();
            self.ProgressPosition=max(self.ProgressPosition,((self.SweepPos+1)/self.LenSweepList)*self.DCVal_*100/self.DCstop);
            if self.DCstop  < self.DCVal_:
               self.StopAnalyse();
               #self.stop=True
            else:
               self.DCVal_+=self.DCstep;
          self.update=update






    def StopAnalyse(self):
        if not(self.SweepUsed):
           self.stop=True
        else:
         self.app.saveDataBySweepPos(self.SweepPos)
         self.SweepPos=self.SweepPos+1
         if len(self.SweepList) > self.SweepPos:
          self.SweepParam+=self.SweepList[self.SweepPos];
          self.SweepName=self.Sweep['param'].name+'='+str(self.SweepList[self.SweepPos])+self.Sweep['param'].Unit;
          self.StartSimu();
         else:
              self.stop=True
        if self.stop:
            self.EndTime= time.time()
        #-------------




#-------------------------------------------------------------------------------
# class AppPyAMS: Application  PyAMS for: In and out data
#-------------------------------------------------------------------------------

class appPyAMS:

    def __init__(self,UsedPyAMSSoft=True):
        self.UsedPyAMSSoft=UsedPyAMSSoft
        self.cir=[]
        self.option={}
        self.Result_=[]
        self.LenOut=0
        self.SweepMethod=''
        self.OutPut=[]
        self.data=[];
        self.usedaX=False;
        self.usedSweep=False;
        self.lenSweep=0;
        self.cad=False
        self.outPuts=[]


    def circuit(self,*elements):
        n=len(elements);
        self.cir=[]
        self.elements={}
        self.sweepListData={}
        if n==1:
            self.elements=elements[0];
        elif n>1:
            for i in range(n):
                k='E'+str(i+1);
                self.elements[k]=elements[i];


        a=list(self.elements.values())
        k=list(self.elements.keys())
        for i in range(0,len(a)):
            addRefToModel(k[i],a[i])
            self.cir+=[a[i]]


    def setOut(self,*outPuts):
            self.outPuts=outPuts;
            for i in range(len(self.outPuts)):
              t=self.outPuts[i]

    def getOp(self):
        self.Result_=[]
        for i in range(len(self.outPuts)):
            if(type(self.outPuts[i])==str):
                t=self.sium.a.getoutput_(self.outPuts[i])
                self.Result_+=[PyAMS.floatToStr(t)+'V']
            else:
                self.Result_+=[self.outPuts[i].__str__()]
        return self.Result_;


    def getDescBar(self):
        print(self.sium.method['mode'])
        if self.sium.method['mode']=='dc':
            print(self.sium.param.Val)

            return self.sium.param.name+'='+PyAMS.floatToStr(self.sium.param.Val)+self.sium.param.Unit;
        else:
            return 'Time='+PyAMS.time.__Str__();

    def getDataPlot(self):
        self.Result_=[]
        for i in range(len(self.outPuts)):
            t=self.outPuts[i]
            if (type(t)==str):
              self.Result_+=[self.sium.a.getoutput_(t)]
            else:
              self.Result_+=[self.outPuts[i].value]
             # print(self.outPuts[i].Val)
        if(self.usedaX):
           self.Result_+=[self.aX.Val]
        elif self.sium.method['mode']=='dc':
            self.Result_+=[self.sium.dcVal];
        else:
            self.Result_+=[PyAMS.time.value];


        return self.Result_;

    def saveData(self):
        if self.execute:
          r=self.getDataPlot();
          if len(self.data)==0:
            for i in range(len(r)):
                self.data+=[[r[i]]];
          else:
            for i in range(len(r)):
                self.data[i]+=[r[i]];



    def saveDataBySweepPos(self,SweepPos):
        self.sweepListData[SweepPos]=self.data.copy()
        self.data=[]


    def getOutSweep(self,t,pos):
        self.data=self.sweepListData[pos]
        leg=' Sun='+str(self.SweepMethod['list'][pos])+self.SweepMethod['param'].Unit #self.SweepMethod['param'].name
        for i in range(len(self.outPuts)):
            if t==self.outPuts[i]:
                return self.data[i],leg

    def getOut(self,t):
        for i in range(len(self.outPuts)):
            if t==self.outPuts[i]:
                if self.analysis['mode']=="op":
                    print(t+'='+PyAMS.floatToStr(self.data[i][0])+'V')
                return self.data[i]

        if self.sium.method['mode']=='dc':
            #self.Result_+=[self.sium.dcVal];
            pass;
        else:
            if(t==PyAMS.time):
                i=len(self.data)-1;
                return self.data[i];



    def getUnit(self):
        a=self.outPuts;
        self.Units=[]
        for i in range(0,len(a)):
         self.Units+=[self.sium.a.getunits_(a[i])]

        if(self.usedaX):
            self.Units+=[self.aX.Unit]
        else:
           self.Units+=[self.sium.param.Unit]
        return self.Units

    def sweep(self,**SweepMethod):
            self.SweepMethod=SweepMethod
            print(self.SweepMethod['param'])
            print(self.SweepMethod['list'])
            self.usedSweep=True;
            self.lenSweep=len(self.SweepMethod['list'])

    def getSweepListStr(self):
        self.result=[]
        for i in range(self.lenSweep):
            leg=self.SweepMethod['param'].name+'='+str(self.SweepMethod['list'][i])+self.SweepMethod['param'].Unit
            self.result+=[leg]
        return self.result



    def analysis(self,**analysisMethod):
            self.analysis=analysisMethod

    def setOption(self,option):
            self.option=option

    def addSecondSweep(self,secondSweep,values):
        pass


    def run(self,execute=True):
        self.data=[]
        if self.SweepMethod !='':
           self.analysis['sweep']=self.SweepMethod
        self.sium=simu(self,self.cir,self.outPuts,self.analysis,self.option)
        self.sium.stop=False;
        self.execute=execute
        self.sium.ProgressPosition=0;
        self.feavl=self.sium.update
        self.startTime = time.time()

        if execute:
          import sys
          fill = '█'
          j=1;
          while not(self.sium.stop):
              self.feavl()
              i=int(self.sium.ProgressPosition)
              if(i>0):
                if not(self.cad):
                  sys.stdout.write('\r')
                  sys.stdout.write("Progress: %-99s %d%%" % (fill*i, i))
                  sys.stdout.flush()
                else:
                  sys.stderr.write('\r')
                  sys.stderr.write('Total complete: ' +str(i)+'%')



          self.endTime= time.time()
          print("\n ---------------------------------------------------------------------------------------------")
          print("\n Elapsed (with compilation and simulation) = %s" % (self.endTime - self.startTime))
          print("\n ---------------------------------------------------------------------------------------------")

          #print("Length ="+str(self.sium.n))
          #SaveDataInSignalParam()

    def setPageWeb(self,page):
        self.sium.a.pageWeb(page)
    def update(self):
         self.feavl();
         self.sium.a.printout();

    def getValTran(self,l):
        '''
        t=[]
        for i in range(len(l)):
            r=l[i]+'.Val';
            t+=[eval(r)];
        '''
        return [self.cir['V1'].V.Val];



    def data(self,name):
        if type(name)==str:
          return getData(name)
        else:
          return getData(name.name)


    def unit(self,name):
        if type(name)==str:
          return 'V'
        else:
          return name.Unit


    def plot(self,xout,yout,name):
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        fig.suptitle('Panel ')
        legend=[]
        if self.usedSweep:
            for i in range(self.lenSweep):
                x,labelx= self.getOutSweep(xout,i)
                y,labely= self.getOutSweep(yout,i)
                ax.plot(x,y,label = labely)

            '''
            for i in range(self.lenSweep):
                x,labelx= self.getOutSweep(xout,i)
                y,labely= self.getOutSweep(yout,i)
                for t in range(len(y)):
                  y[t]=y[t]+v
                ax.plot(x,y,linestyle='dashed',label = 'Data '+labely)
            '''
            ax.legend()
          #  legend+=[labely]
           # ax.legend(legend)

        else:
          x= self.getOut(xout)
          y= self.getOut(yout)
          ax.plot(x,y)

        #ax.set(xlabel=xout.name+'('+xout.Unit+')', ylabel=yout.name+'('+yout.Unit+')', title=' ')
        ax.set(xlabel='Voltage V('+xout.Unit+')', ylabel=name+'('+yout.Unit+')', title='T=25°C')
        ax.grid()

        plt.show()




    def dataAmplitude(self,name):
        if type(name)==str:
          a=getData(name)
        else:
          a=getData(name.name)
        d=[abs(number) for number in a]
        return d

    def datadB(self,name):
        from math import log10
        if type(name)==str:
          a=getData(name)
        else:
          a=getData(name.name)
        d=[20*log10(abs(number)) for number in a]
        return d

    def dataPhase(self,name):
        from math import atan,pi
        from cmath import phase
        if type(name)==str:
          a=getData(name)
        else:
          a=getData(name.name)
        d=[phase(num)*180/pi for num in a]
        return d

global AppPyAMS
AppPyAMS=appPyAMS()

