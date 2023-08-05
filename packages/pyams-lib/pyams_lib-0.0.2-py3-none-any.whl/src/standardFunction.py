#-------------------------------------------------------------------------------
# Name:        Standard Function
# Author:      d.fathi
# Created:     13/04/2020
# Copyright:   (c) PyAMS 2020
# Licence:     CC-BY-SA
#-------------------------------------------------------------------------------

from PyAMS import time,getStepTime,temp,tnom
from option import simulationOption
from math import sqrt,exp


def acSim(mag,phase):
    if ModAnaly.getSource:
        return 1
    return 0
    #return   mag*(cos(phase)+sin(phase)*(1j))

def toKelvin(degree):
    return degree+275

def temperature():
    return 273.15+Temp;

def vth(T=tnom):
    #thermal voltage
    return 8.6173303e-5*(T+273)


def qtemp(TC1,TC2):
    return (1+TC1*(Temp-Tnom)+TC2*(Temp-Tnom)*(Temp-Tnom))



def  explim(a):
     if a>=200.0:
          return (a-199.0)*exp(200.0)
     return exp(a)


#Computer Aided Engineering for Integrated Circuits
#ECE 570

ITL4=0;
ListSignalDdt=[];

dt1=1e-12;
Err=1e-18;
dt0=1e-7
dtr=0.0
h=[0.0,0.0,0.0,0.0]



def ddt(Signal,InitialValue=0.0):



    try:
        dt=abs(simulationOption.t1-simulationOption.t0);#;

        if dt >0.0:
            #Method Integration Trapezoidal order 2
            if simulationOption.Trapezoidal:
                Signal.V1=Signal.Val;
                Signal.dVr=(Signal.V1-Signal.V0)/dt
                Signal.dV=2*Signal.dVr-Signal.dV0

        return Signal.dV
    except:
        global ListSignalDdt
        ListSignalDdt+=[Signal]
        simulationOption.ldt=len(ListSignalDdt)
        if  (type(InitialValue)==int) or  (type(InitialValue)==float) :
            Signal.V0=InitialValue
        else:
            Signal.V0=InitialValue.Val
        Signal.V1=0.0
        Signal.dV0=0.0
        Signal.DD1=[0.0,0.0]
        Signal.DD2=[0.0,0.0]
        Signal.DD3=[0.0,0.0]
        Signal.dt=[0.0,0.0,0.0]
        Signal.dV=0.0
        Signal.dVr=0.0
        if dt >0.0:
             Signal.dVr=(Signal.V1-Signal.V0)/dt
             Signal.dV=2*Signal.dVr-Signal.dV0
        return Signal.dV



def controlStepTime(UsedTime):

        if (simulationOption.ldt==0):
            simulationOption.t0=time.value;
            simulationOption.t1=simulationOption.t1+simulationOption.TimeStep;
            return True

        global ListSignalDdt,dt0,dt1,h,ITL4,Err,dtr


        if simulationOption.t1==0.0:
           dt1=simulationOption.TimeStep
           dtr=min(1e-12,  simulationOption.TimeStep/100);
           simulationOption.t0=time.Val;
           simulationOption.t1=min(1e-12,simulationOption.TimeStep/100);
           simulationOption.UsedThise=True
           print('ust1=',simulationOption.t1)
           return True;

        '''
        if UsedTime:


            for i in range(len(ListSignalDdt)):
              Signal=ListSignalDdt[i]
              Signal.DD1[0]=Signal.DD1[1]
              Signal.DD2[0]=Signal.DD2[1]
              Signal.dV0=Signal.dV
              Signal.V0=Signal.V1

            h[0]=h[1]
            h[1]=h[2]
            dtr=min(h);
            if(dtr < Err):
                dtr=SimulationOption.TimeStep/1e+6;

            SimulationOption.t0=Time.Val;
            SimulationOption.t1=SimulationOption.t1+dtr;
            Time_Selection=True
            return True


        '''



        dt=simulationOption.t1-simulationOption.t0;


        if dt <=Err:
            if(dtr > Err):
              dt=dtr
            else:
              dt=SimulationOption.TimeStep/1e+8


        LTE=[dt]

        h[2]=dt
        t1=h[2]+h[1]
        t2=h[2]+h[1]+h[0]
       # print('t1',t1)

        for i in range(len(ListSignalDdt)):
          Signal=ListSignalDdt[i]
          Signal.DD1[1]=Signal.dVr


          if t1 > Err:
            Signal.DD2[1]=(Signal.DD1[1]-Signal.DD1[0])/t1
            Signal.DD3[1]=(Signal.DD2[1]-Signal.DD2[0])/t2
            if (h[2]>Err):
             Ex=simulationOption.RELTOL*max(abs(Signal.V0),abs(Signal.V1),Signal.Chgtol)/h[2]
             Edx=(Signal.Abstol+simulationOption.RELTOL*max(abs(Signal.dV),abs(Signal.dV0)))
             EB=max(Ex,Edx)
             er=sqrt(EB/max(Signal.Abstol,abs(Signal.DD3[1])/12))
             if (er>0.0):
                  LTE+=[er]


        DH=min(LTE);
        #print(LTE)
        #print('DH=',DH)
        #print('0.9*dt=',0.9*dt)

        Time_Selection=False;
        if (0.9*dt>DH):
            simulationOption.t1=simulationOption.t0+DH
            Time_Selection=True;
            ITL4=ITL4+1
            if(ITL4>simulationOption.ITL4):
                ITL4=0;
                Time_Selection=True;
        else:
            if ITL4 > 10:
              print(ITL4)
            dtr=dt;
            dt=min(2*dt,simulationOption.TimeStep)
            Time_Selection=True;
            #print(dt)
            ITL4=0;




        if Time_Selection or UsedTime:

            for i in range(len(ListSignalDdt)):
              Signal=ListSignalDdt[i]
              Signal.DD1[0]=Signal.DD1[1]
              Signal.DD2[0]=Signal.DD2[1]
              Signal.dV0=Signal.dV
              Signal.V0=Signal.V1

            h[0]=h[1]
            h[1]=h[2]


            simulationOption.t0=time.Val
            simulationOption.t1=simulationOption.t1+dt;
            Time_Selection=True


        return Time_Selection;





def trap(V1,V2,Td,Tr,Pw,Tf,T):
        global getStepTime,time
        b=(V1,V2,Td,Tr,Pw,Tf,T)
        v=getStepTime.indexTrap(b)
        [S,T,a,b,c]=getStepTime.List[v]
        len_=len(b)
        y2=0.0
        for i in range(len_-1):
            y1,x1=c[i],a[i]
            y2,x2=c[i+1],a[i+1]
            u1,u2=b[i],b[i+1]
            if u2:
              if x1==x2:
                if u1:
                    return V1
                else:
                    return V2
              else:
                   a_=(y1-y2)/(x1-x2)
                   b_=y1-a_*x1
                   return a_*time+b_
        return y2

def puls(Va,T):
    dT=T/1e+7;
    return trap(Va,0,dT,dT,T/2,dT,T)


def realTime():
     global time
     return time;

