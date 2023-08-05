#-------------------------------------------------------------------------------
# Name:        sin wave
# Author:      d.fathi
# Created:     05/02/2023
# Copyright:   (c) PyAMS 2023
# Licence:      free  "GPLv3"
#-------------------------------------------------------------------------------


#Step 1. Import the library of analog elements (PyAMS models) that are used in the circuit.

from sys import path;
path+=["../"];

import PyAMS
from PyAMS import time
from simu import AppPyAMS
from SinVoltage import SinVoltage
from Resistor import Resistor


#Step 2. Add the names of the models in the circle with the position of attachment.
V1=SinVoltage("Vout1","0");
R1=Resistor("Vout1","0");

V2=SinVoltage("Vout2","0");
R2=Resistor("Vout2","0");

V3=SinVoltage("Vout3","0");
R3=Resistor("Vout3","0");



#Step 3. Modifying parameters of the elements.
V1.Va+=1
V1.Fr+=1
V1.Ph+=0
R1.R+=100

V2.Va+=1
V2.Fr+=1
V2.Ph+=120
R2.R+=100

V3.Va+=1
V3.Fr+=1
V3.Ph+=240
R3.R+=100



#Step 4. Importing command of analysis.
AppPyAMS.setOut("Vout1","Vout2","Vout3")
AppPyAMS.circuit(V1,V2,V3,R1,R2,R3);
AppPyAMS.analysis(mode="tran",start=0.0,stop=2,step=1);
AppPyAMS.run();



#Step 5. Plotting result
import matplotlib.pyplot as plt
Time = AppPyAMS.getOut(time)
Vout1 = AppPyAMS.getOut("Vout1")
Vout2 = AppPyAMS.getOut("Vout2")
Vout3 = AppPyAMS.getOut("Vout3")

import matplotlib
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot(Time, Vout1, label="Vout1")
ax.plot(Time, Vout2, label="Vout2")
ax.plot(Time, Vout3, label="Vout3")

ax.set(xlabel='Time [Sec]', ylabel='[Volt]', title='About as  sin wave circuit')
ax.grid()
ax.legend()
plt.show()
image_format = 'svg' # e.g .png, .svg, etc.
image_name = 'myimage.svg'

fig.savefig(image_name, format=image_format, dpi=1200)
