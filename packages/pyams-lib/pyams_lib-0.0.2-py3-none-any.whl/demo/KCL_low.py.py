#-------------------------------------------------------------------------------
# Name:        KCL Low
# Author:      D.fathi
# Created:     17/02/2023
# Copyright:   (c) PyAMS 2023
# Licence:     free  "GPLv3"
#-------------------------------------------------------------------------------


#Step 1. Import the library of analog elements (PyAMS models) that are used in the circuit.

from sys import path;
path+=["../"];
import PyAMS
from  Resistor  import  *
from  DCVoltage  import  *
from  DCCurrent import *
from  simu import AppPyAMS


#Step 2. Add the names of the models in the circle with the position of attachment

I1=DCCurrent("N02","0");
I2=DCCurrent("N03","N02");
R1=Resistor("N02","N01");
R2=Resistor("N01","0");
R3=Resistor("N03","N01");
R4=Resistor("N03","N04");
V1=DCVoltage("N04","0");


#Step 3. Modifying parameters of the elements.

I1.Idc+=1
I2.Idc+=1
R1.R+=1000
R2.R+=1000
R3.R+=1000
R4.R+=1000
V1.Vdc+=15


#Step 4. Importing command of analysis.
AppPyAMS.circuit(I1,I2,R1,R2,R3,R4,V1);
AppPyAMS.analysis(mode="op");
AppPyAMS.run();

#Step 5. Print out


print('-------in (Node = N01)----------')
print('I(R1)='+str(R1.I));
print('I(R2)='+str(R2.I));
print('I(R3)='+str(R3.I));


print('-------in (Node = N02)----------')
print('I(I1)='+str(I1.I));
print('I(I2)='+str(I2.I));
print('I(R1)='+str(R1.I));



