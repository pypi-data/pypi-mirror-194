#-------------------------------------------------------------------------------
# Name:        puls voltage Source
# Author:      d.fathi
# Created:     22/02/2023
# Modified:    22/02/2023
# Copyright:   (c) PyAMS
# Licence:     free  "GPLv3"
#-------------------------------------------------------------------------------

from PyAMS import model,signal,param
from electrical import voltage
from standardFunction import puls


#Source for square voltage-----------------------------------------------------
class PulsVoltage(model):
     def __init__(self, p, n):
         #Signal  declaration--------------------------------------------------
         self.V= signal('out',voltage,p,n)

         #Parameters declarations----------------------------------------------
         self.Va=param(1.0,'V','Amplitude of square wave voltage  ')
         self.T=param(0.1,'Sec','Period')
         self.Voff=param(0.0,'V','Offset voltage')

     def analog(self):
         self.V+=puls(self.Va,self.T)+self.Voff

