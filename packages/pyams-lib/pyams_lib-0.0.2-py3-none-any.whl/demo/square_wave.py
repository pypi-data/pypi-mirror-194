#-------------------------------------------------------------------------------
# Name:        Square wave
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
from SquareVoltage import SquareVoltage
from Resistor import Resistor


#Step 2. Add the names of the models in the circle with the position of attachment.
V1=SquareVoltage("Vin","0");
R1=Resistor("Vin","Vout");
R2=Resistor("Vout","0");


#Step 3. Modifying parameters of the elements.
V1.Va+=10
V1.T+=1
R1.R+=1000
R2.R+=1000


#Step 4. Importing command of analysis.
AppPyAMS.setOut("Vin","Vout")
AppPyAMS.circuit(V1,R1,R2);
AppPyAMS.analysis(mode="tran",start=0.0,stop=4,step=0.01);
AppPyAMS.run();



#Step 5. Plotting result
import matplotlib.pyplot as plt
Time = AppPyAMS.getOut(time)
Vin = AppPyAMS.getOut("Vin")
Vout = AppPyAMS.getOut("Vout")

import matplotlib
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot(Time, Vin, label="Vin")
ax.plot(Time, Vout, label="Vout")

ax.set(xlabel='Time [Sec]', ylabel='[Volt]', title='About as  sin wave circuit')
ax.grid()
ax.legend()
plt.show()

ax.grid()
plt.show()

