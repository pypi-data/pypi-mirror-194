#-------------------------------------------------------------------------------
# Name:        Trapezoid voltage Source
# Author:      D.Fathi
# Created:     14/03/2017
# Modified:    08/04/2020
# Copyright:   (c) PyAMS
# Licence:     free  "GPLv3"
#-------------------------------------------------------------------------------

from PyAMS import model,signal,param
from electrical import voltage
from StandardFunction import trap


#Source for Trapezoid voltage---------------------------------------------------
class TrapezoidVoltage(model):
     def __init__(self, a, b):
         #Signal  declaration---------------------------------------------------
         self.V = signal('out',voltage,a,b)

         #Parameters declarations-----------------------------------------------
         self.V0=param(1.0,'V','Initial voltage ')
         self.V1=param(1.0,'V','Peak voltage ')
         self.Td=param(0,'Sec','Initial delay time')
         self.Tr=param(0,'Sec','Rise time')
         self.Tw=param(0.05,'Sec','Pulse-width')
         self.Tf=param(0,'Sec','Fall time')
         self.T=param(0.1,'Sec','Period of wave')
         self.Voff=param(0.0,'V','Offset voltage')

     def analog(self):
         self.V+=trap(self.V1,self.V0,self.Td,self.Tr, self.Tw,self.Tf,self.T)+self.Voff

