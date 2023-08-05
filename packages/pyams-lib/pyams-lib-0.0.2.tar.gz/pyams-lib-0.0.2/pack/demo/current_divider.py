#-------------------------------------------------------------------------------
# Name:        Current divider
# Author:      D.fathi
# Created:     02/02/2023
# Copyright:   (c) PyAMS 2023
# Licence:      free  "GPLv3"
#-------------------------------------------------------------------------------


#Step 1. Import the library of analog elements (PyAMS models) that are used in the circuit.

from sys import path;
path+=["../"];


import PyAMS
from  Resistor  import  *;
from  DCCurrent  import  *;

from simu import AppPyAMS


#Step 2. Add the names of the models in the circle with the position of attachment
R1=Resistor("0","n");
R2=Resistor("0","n");
R3=Resistor("0","n");
R4=Resistor("0","n");
I1=DCCurrent("n","0");

#Step 3. Modifying parameters of the elements.
R1.R+=1000;
R2.R+=1000;
R3.R+=1000;
R4.R+=1000;
I1.Idc+=0.1;


#Step 4. Importing command of analysis.
AppPyAMS.circuit(I1,R1,R2,R3,R4);
AppPyAMS.setOut(R4.I);
AppPyAMS.analysis(mode="op");
AppPyAMS.run();

#Step 5. Print out
print('I(R4)='+str(R4.I))
