#-------------------------------------------------------------------------------
# Name:        PyAMS
# Author:      d.fathi
# Created:     20/03/2015
# Update:      07/02/2023
# Copyright:   (c) pyams 2023
# Web:         www.PyAMS.org
# Licence:     free  "GPLv3"
#-------------------------------------------------------------------------------

import math;

from sys import path;
import os;
dire =  os.path.dirname(__file__)
path+=[dire+"\src"];
path+=[dire+"\library"];
path+=[dire+"\library\Source"];
path+=[dire+"\library\Basic"];
path+=[dire+"\library\Semiconductor"];

#-------------------------------------------------------------------------------
# def floatToStr: convert float to string
#-------------------------------------------------------------------------------
def floatToStr(value):
    units={'f':1e-15,'p':1e-12,'n':1e-9,'µ':1e-6,'m':1e-3,' ':1.0,'k':1e+3,'M':1e+6,'T':1e+9}
    v=list(units.values())
    k=list(units.keys())
    sign=math.copysign(1, value)
    value=abs(value)
    for i in range(len(v)-1, 0, -1):
       if(value>=(v[i])):
        f=format(sign*value/v[i],'.2f')
        lf=len(f)
        if(f[lf-1]=='0'):
          f=f[:lf-1]
        lf=len(f)
        if(f[lf-1]=='0'):
          f=f[:lf-1]
          f=f[:lf-2]
        return f+k[i]
    return str(sign*value);



#-------------------------------------------------------------------------------
# def strToFloat: convert string to  float
#-------------------------------------------------------------------------------

def strToFloat(value):
    num=''
    uni=''
    units={'f':1e-15,'p':1e-12,'n':1e-9,'µ':1e-6,'u':1e-6,'m':1e-3,' ':1.0,'k':1e+3,'K':1e+3,'M':1e+6,'T':1e+9}
    m=1.0;
    value=value+' ';

    for i in range(len(value)):
        if value[i] in ['0','1','2','3','4','5','6','7','8','9','+','-','e','.']:
           num=num+value[i];
        else:
           uni=value[i];
           m=float(num);
           if uni in units:
             m=m*units[uni];
           break;
    return m;

def value(v):
    return strToFloat(v)

#-------------------------------------------------------------------------------
# class model: object of model
#-------------------------------------------------------------------------------


class model(object):
    def __init__(self):
        self.Values='';

    def getSignals(self):
        self.signals=[]
        a=dir(self);
        for i in range(0,len(a)):
          f=eval('self.'+a[i])
          if type(f).__name__=='signal':
            self.signals+=[eval('self.'+a[i])]
        return self.signals;

    def getParamaters(self):
        self.params=[]
        a=dir(self);
        for i in range(0,len(a)):
          f=eval('self.'+a[i])
          if type(f).__name__=='param':
            self.params+=[eval('self.'+a[i])]
        return self.params;

    def getParam(self,param=''):
        result=[]
        a=dir(self);
        for i in range(0,len(a)):
          f=eval('self.'+a[i])
          if type(f).__name__=='param':
           # if not(f.Local):
           result+=[{'name':a[i],'value':f.value,'unit':f.unit,'description':f.description}]
        d=param.split(' ')
        for i in range(len(d)):
           p=d[i].split('=')
           if(len(p)==2):
              for j in range(len(result)):
                if result[j]['name']==p[0]:
                    result[j]['value']=p[1]
        return result


    def setParam(self,param=''):
        s=[]
        param=param.split(' ')
        for i in range(len(param)):
           p=param[i].split('=')
           if(len(p)==2):
            s+=[{'name':p[0],'val':p[1]}]
        a=dir(self);
        for i in range(0,len(a)):
          f=eval('self.'+a[i])
          if type(f).__name__=='param':
            for j in range(len(s)):
                if (a[i]==s[j]['name']):
                    f+=value(s[j]['val'])


    def getIndex(self,node):
        n=len(self.signals)
        for i in range(n):
            if self.signals[i].Porta in node:
               self.signals[i].Indxa=node.index(self.signals[i].Porta)
            if self.signals[i].Portb in node:
               self.signals[i].Indxb=node.index(self.signals[i].Portb)



#-------------------------------------------------------------------------------
# class param: parameter object
#-------------------------------------------------------------------------------

class param (object):
      def __init__(self,value=0.0, unit='', description=''):
          self.value=value
          self.unit=unit
          self.description=description

      def __name__(self):
          return 'param'
      def __Str__(self):
           return floatToStr(self.value)+self.unit

      def __float__(self):
        return self.value

      def setParam(self,value):
          self.value=value

      def __truediv__(self, other):
          return self.value/other
      def __rtruediv__(self, other):
          return other/self.value
      def __add__(self, other):
          return self.value+other
      def __radd__(self, other):
          return self.value+other
      def __sub__(self, other):
          return self.value-other
      def __rsub__(self, other):
          return -self.value+other
      def __mul__(self, other):
          return self.value*other
      def __rmul__(self, other):
          return self.value*other
      def __rpow__(self, other):
          return other**self.value
      def __pow____(self, other):
          return self.value**other
      def __neg__(self):
          return -self.value
      def __pos__(self):
          return self.value
      def __iadd__(self, other):
          if type(other).__name__ in ['signal','param']:
               self.value=other.value;
               return self
          self.value=other
          return self
      def __lt__(self, other):
          return self.value<other
      def __gt__(self, other):
          return self.value>other
      def __le__(self, other):
          return self.value<=other
      def __ge__(self, other):
          return self.value>=other
      def __ne__(self, other):
          return self.value!=other
      def __eq__(self, other):
          return self.value==other


#-------------------------------------------------------------------------------
# class signal: signal object
#-------------------------------------------------------------------------------

class signal(object):
      def __init__(self,direction,description,Porta='0', Portb='0'):
         self.dir =direction
         self.Porta = Porta
         self.Portb = Portb
         self.Indxa = 0
         self.Indxb = 0
         self.value=0.0
         self.pos=0
         self.adr=(0,0)
         self.abstol=description['abstol']
         self.chgtol=description['chgtol']
         self.discipline=description['discipline']
         self.type=description['signalType']
         self.nature=description['nature']
         self.unit=description['unit']
         self.I=0.0
         self.Name=' '

      def __name__(self):
         return 'signal'

      def getValue(self):
        return floatToStr(self.value)+self.unit

      def __str__(self):
         return floatToStr(self.value)+self.unit

      def __float__(self):
        return self.value

      def __truediv__(self, other):
          return self.value/other
      def __rtruediv__(self, other):
          return other/self.value
      def __add__(self, other):
          return self.value+other
      def __radd__(self, other):
          return self.value+other
      def __sub__(self, other):
          return self.value-other
      def __rsub__(self, other):
          return -self.value+other
      def __mul__(self, other):
          return self.value*other
      def __rmul__(self, other):
          return self.value*other
      def __rpow__(self, other):
          return other**self.value
      def __pow____(self, other):
          return self.value**other
      def __neg__(self):
          return -self.value
      def __pos__(self):
          return self.value
      def __iadd__(self, other):
          if type(other).__name__ in ['signal','param']:
               self.value=other.value;
               return self
          self.value=other
          return self
      def __lt__(self, other):
          return self.value<other
      def __gt__(self, other):
          return self.value>other
      def __le__(self, other):
          return self.value<=other
      def __ge__(self, other):
          return self.value>=other
      def __ne__(self, other):
          return self.value!=other
      def __eq__(self, other):
          return self.value==other

      def get_(self):
          return self.value
      def set_(self,value):
            self.value=value



#-------------------------------------------------------------------------------
# inf,gnd,version: List of constant
#-------------------------------------------------------------------------------

inf=1.0e+15
gnd='0'
version='0.0.2'


#-------------------------------------------------------------------------------
# time..temp: List of paramatres
#-------------------------------------------------------------------------------

time=param(0.0,'Sec','Time')
freq=param(0.0,'Hz','Freq')
tnom=param(300.0,'K','Temperature')
temp=param(27.0,'°C','Temperature')

temp.name='Temperature'
time.name='Time'
freq.name='Freq'


#-------------------------------------------------------------------------------
#Class analysis: used to convert the netlist or structur of circuit into
#                an array according to the type of analysis.
#-------------------------------------------------------------------------------

class analysis:
      def __init__(self,circuit,method,output=[]):
           self.c=circuit
           self.output=output
           self.out=[]
           self.nodes=['0']
           self.Lin=[]
           self.Lout=[]
           self.fout=[]
           self.LIV=[]
           self.len=0
           self.x=[]
           self.signals=[]
           self.ListStart=[]
           self.VectsDesc=[]
           self.start=True;
           global  List,Val
           List=[]
           Val=[]

           l=len(self.c)
           i=0

           while i<l:
                     d=self.c[i]
                     a=dir(d)
                     if ('sub' in a):
                       r=d.sub()
                       #AddRefToSub(d)
                       if not(len(r)==0):
                         # self.c.remove(self.c[i])
                          for j in range(len(r)):
                              self.c.append(r[j])
                     l=len(self.c)
                     i=i+1

           l=len(self.c)
           i=0
           while i<l:
                #try:
                     d=self.c[i]
                     a=dir(d)
                     if ('start' in a):
                        self.ListStart+=[d]
                     i=i+1#except:
                    # i=i+1

           l=len(self.c)
           i=0
           '''
           while i < l:
                     d=self.c[i]
                     d.analog()
                     i=i+1
           '''


           l=len(self.c)
           i=0
           while i<=l:
                try:
                     d=self.c[i]
                     a=dir(d);
                     if 'output' in a:
                       self.fout.append(d)
                     i=i+1;
                except:
                     i=i+1


           self.List=[]
           self.Val=[]
           self.adr= id(self)/800

           def  addToList(list,val,dir_,nature,a, b='0'):
            #  if not (dir_,pf,a, b) in List:
                list+=[(dir_,nature,a, b)]
                val+=[0]
                return len(list)-1

           for i in range(len(self.c)):
                L=dir(self.c[i])
                try:
                 for j in range(len(L)):
                     # if L[j]=='__doc__':
                     #      break;
                      f=eval('self.c['+str(i)+'].'+L[j])
                      if type(f).__name__=='signal':
                           f.pos=addToList(self.List,self.Val,f.dir,f.nature,f.Porta,f.Portb)
                           f.adr=(self.adr,f.pos)
                           self.signals+=[f]
                except:
                    pass


           for i in range(len(self.List)):
                v=self.List[i]
                if not v[2] in self.nodes:
                     self.nodes+=[v[2]]
                if not v[3] in self.nodes:
                     self.nodes+=[v[3]]
           for i in range(len(self.List)):
                v=self.List[i]
                if v[0]=='in':
                     self.Lin+=[(v[1]=='potential',self.nodes.index(v[2]),self.nodes.index(v[3]),i)]
                else:
                     self.Lout+=[(v[1]=='potential',self.nodes.index(v[2]),self.nodes.index(v[3]),i)]


           for i in range(len(self.Lin)):
                vin=self.Lin[i]
                inList=False
                if not(vin[0]):
                     addlen=len(self.nodes)-1
                     for j in range(len(self.Lout)):
                          vout=self.Lout[j]
                          if vout[0]:
                               addlen=addlen+1
                               t=vin[3]
                               if (vout[1]==vin[1]) and (vout[2]==vin[2]):
                                    self.Lin[i]=(False,addlen,-1,vin[3])
                                    #print(str(t)+':'+str(self.ListSignal[t].pos))
                                    inList=True
                                    break
                               elif (vout[1]==vin[2]) and (vout[2]==vin[1]):
                                    self.Lin[i]=(False,addlen,1,vin[3])
                                    #print(str(t)+':'+str(self.ListSignal[t].pos))
                                    inList=True
                                    break
                     if not(inList):
                          addlen=addlen+1
                          self.Val+=[0]
                          self.Lout+=[(True,vin[1],vin[2],len(self.Val)-1)]
                          self.Lin[i]=(False,addlen,1,vin[3])



           self.len=len(self.nodes)-1
           self.les=0

           self.nde=self.len
           for i in range(len(self.Lout)):
               v=self.Lout[i]
               if v[0]:
                    self.LIV+=[(self.len-1,v[3])]
                    self.les+=1

           self.mlen=self.len+self.les+1

           for i in range(self.mlen):
                self.x+=[0]

           #print ('Numbre of signals:       ',len(self.ListSignal))
           #print ('Numbre of nodes:         ',  self.len-self.les)
           #print ('Numbre of source out:    ',self.les)

           i=0
           l=len(self.c)
           global getStepTime;
           while i<=l:
                try:
                     d=self.c[i]
                     a=d.period()
                     getStepTime.addPer(a);
                     i=i+1;
                except:
                     i=i+1


      def getoutput_(self,out_):

                 if type(out_)==str:
                    j=self.nodes.index(out_)
                    return self.x[j-1]
                 elif  type(out_).__name__=='signal':
                    return self.Val[out_.pos]
                 elif  type(out_).__name__=='param':
                    return out_.Val
                 else:
                    return 0

      def getunits_(self,out_):
                 if type(out_)==str:
                    j=self.nodes.index(out_)
                    return 'V'
                 elif  type(out_).__name__=='signal':
                    return out_.Unit
                 elif  type(out_).__name__=='param':
                    return out_.Unit
                 else:
                    return 0

      def getlen(self):
         self.len=len(self.nodes)-1
         self.les=0;
         for i in range(len(self.Lout)):
               p,n1,n2,k=self.Lout[i]
              # f=self.ListSignal[k]
               if p:
                  self.les=self.les+1
         self.mlen=self.len+self.les+1
         return [self.mlen,self.len,self.les]


      def set(self,x):
           x[0]=0;

           for i in range(len(self.LIV)):
                p,s=self.LIV[i]
                if(s<len(self.signals)):
                  self.signals[s].I=x[p]

           for i in range(len(self.Lin)):
               p,n1,n2,v=self.Lin[i]
               if p:
                    self.Val[v]=x[n1]-x[n2]
               else:
                    self.Val[v]=x[n1]

           for i in range(len(self.signals)):
                self.signals[i].value=self.Val[self.signals[i].pos]


           for i in range(len(self.c)):
               self.c[i].analog()

           for i in range(len(self.signals)):
                self.Val[self.signals[i].pos]=self.signals[i].value



      def favel(self,x):

           x.insert(0,0)
          # x=ndarray.tolist(x);
           self.set(x)
           addlen=len(self.nodes)-1
           y=[]
           for i in range(self.mlen):
                y+=[0]
           for i in range(len(self.Lout)):
               p,n1,n2,k=self.Lout[i]
               v=self.Val[k]
               if p:
                      addlen+=1
                      y[addlen]+=x[n1]-x[n2]-v
                      y[n1]+=x[addlen]
                      y[n2]-=x[addlen]
               else:
                    y[n1]+=v
                    y[n2]-=v


           y.pop(0)
           x.pop(0)
           self.x=x;
           #for i in range(len(self.ListSignal)):
            #     print(str(i)+':'+str(self.ListSignal[i].pf)+'='+str(self.ListSignal[i].Val))
           #print(self.Val)
           return y



#--------------------------------------------------------------------------------------------
global listNewNode;
listNewNode=[]

def newNode():
        NodeName='SN00'

        i=1
        while i>=1:
            if not(NodeName+str(i) in listNewNode):
                listNewNode.append(NodeName+str(i))
                return NodeName+str(i)
            i=i+1


#-------------------------------------------------------------------------------
#class getStepTime: used to find step time from models
#-------------------------------------------------------------------------------


class getStepTime:
    def __init__(self):
        self.List=[]
        self.ndivPer=36;
        self.ListTrap=[]
        self.ListTrapPos=[]

    def indexTrap(self,v):
        try:
          i=self.ListTrap.index(v)
          return self.ListTrapPos[i]
        except:
          self.ListTrap+=[v]
          (V2,V1,Td,Tr,Pw,Tf,T)=v
          a=[0.0,Td+0.0,Td+Tr+0.0,Td+Tr+Pw+0.0,Td+Tr+Pw+Tf+0.0,Td+Tr+Pw+Tf+0.0,T+0.0]
          b=[True,True,True,True,True,True,True]
          c=[V1,V1,V2,V2,V1,V1,V1]
          self.List+=[['trap',T+0.0,a,b,c]]
          Pos=len(self.List)-1;
          self.ListTrapPos+=[Pos]
          return Pos

    def addPer(self,Values):
        len_=len(Values)
        for i in range(len_):
         T= Values[i][0]+(Values[i][1]*Values[i][0]/360)
         a=[]
         b=[]
         for r in range(self.ndivPer):
            a+=[r*T/self.ndivPer]
            b+=[True]
         self.List+=[['pr',T,a,b]]

    def  IncPer(self):
        len_=len(self.List)
        for i in range(len_):
            d=self.List[i]
            T=d[1]
            a=d[2]
            b=d[3]
            lenb=len(b)
            R=True
            for r in range(lenb):
                R=R and not(b[r])
            if R:
                for r in range(lenb):
                    a[r]=a[r]+T
                    b[r]=True

    def  GetStepTime(self,MinTime):
        len_=len(self.List)
        for i in range(len_):
            d=self.List[i]
            T=d[1]/(2*self.ndivPer)
            if (MinTime > T) and (T!=0.0):
                MinTime=T
        print ('MinStepTime=',MinTime);
        return MinTime

    def ControlPer(self):
        self.IncPer()
        global time
        TimeVal=0.0
        UsedTime=False;
        ResultPer=(TimeVal,-1,-1)
        len_=len(self.List)
        for i in range(len_):
            d=self.List[i]
            a=d[2]
            b=d[3]
            lenb=len(b)
            for r in range(lenb):
                if b[r]:
                  if time.value >= a[r]:
                    time.value = a[r]
                    ResultPer=(a[r],i,r)

        if(ResultPer[1]!=-1):
          UsedTime=True;
          (t,i,r)=ResultPer
          time.Val=t
          d=self.List[i]
          a=d[2]
          b=d[3]
          b[r]=False;
        return UsedTime;

getStepTime=getStepTime()



