#-------------------------------------------------------------------------------
# Name:        KVL Low
# Author:      D.fathi
# Created:     17/02/2023
# Copyright:   (c) PyAMS 2023
# Licence:     free  "GPLv3"
#-------------------------------------------------------------------------------


#Step 1. Import the library of analog elements (PyAMS models) that are used in the circuit.

import PyAMS
from PyAMS import time;
from simu import AppPyAMS;
from Resistor import Resistor
from DCVoltage import DCVoltage


#Step 2. Add the names of the models in the circle with the position of attachment
R1=Resistor("N01","0");
R2=Resistor("N04","N01");
V1=DCVoltage("N01","0");
V2=DCVoltage("N04","0");


#Step 3. Modifying parameters of the elements.
R1.R+=100e+3;
R2.R+=100e+3;
V1.Vdc+=15;
V2.Vdc+=15;

#Step 4. Importing command of analysis.
AppPyAMS.circuit(R1,R2,V1,V2);
AppPyAMS.analysis(mode="op");
AppPyAMS.run();



#Step 5. Print out.
print('-------in loop 1----------')
print('V(R1)='+str(R1.V));
print('V(V1)='+str(V1.V));


print('-------in loop 2----------')
print('V(R1)='+str(R1.V));
print('V(R2)='+str(R2.V));
print('V(V2)='+str(V2.V));