#-------------------------------------------------------------------------------
# Name:        Square current Source
# Author:      d.fathi
# Created:     22/02/2023
# Modified:    22/02/2023
# Copyright:   (c) PyAMS
# Licence:     free  "GPLv3"
#-------------------------------------------------------------------------------

from PyAMS import model,signal,param
from electrical import current
from StandardFunction import puls


#Source for square current------------------------------------------------------
class PulsCurrent(model):
     def __init__(self, p, n):
         #Signal  declaration---------------------------------------------------
         self.I = signal('out',current,p,n)

         #Parameters declarations-----------------------------------------------
         self.Ia=param(1.0,'A','Amplitude of square wave current  ')
         self.T=param(0.1,'Sec','Period')
         self.Ioff=param(0.0,'A','Offset current')

     def analog(self):
         self.I+=puls(self.Ia,self.T)+self.Ioff

