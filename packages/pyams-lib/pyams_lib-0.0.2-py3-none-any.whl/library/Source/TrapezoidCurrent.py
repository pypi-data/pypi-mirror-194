#-------------------------------------------------------------------------------
# Name:        Trapezoid current Source
# Author:      D.Fathi
# Created:     14/03/2017
# Modified:    10/04/2020
# Copyright:   (c) PyAMS
# Licence:     free  "GPLv3"
#-------------------------------------------------------------------------------

from PyAMS import model,signal,param
from electrical import current
from StandardFunction import trap


#Source for Trapezoid current---------------------------------------------------
class TrapezoidCurrent(model):
     def __init__(self, a, b):
         #Signal  declaration---------------------------------------------------
         self.I = signal('out',current,a,b)

         #Parameters declarations-----------------------------------------------
         self.I0=param(1.0,'A','Initial current ')
         self.I1=param(1.0,'A','Peak current ')
         self.Td=param(0,'Sec','Initial delay time')
         self.Tr=param(0,'Sec','Rise time')
         self.Tw=param(0.05,'Sec','Pulse-width')
         self.Tf=param(0,'Sec','Fall time')
         self.T=param(0.1,'Sec','Period of wave')
         self.Ioff=param(0.0,'A','Offset current')

     def analog(self):
         self.I+=trap(self.I1,self.I0,self.Td,self.Tr, self.Tw,self.Tf,self.T)+self.Ioff

