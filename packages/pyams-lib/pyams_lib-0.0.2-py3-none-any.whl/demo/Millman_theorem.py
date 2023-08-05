#-------------------------------------------------------------------------------
# Name:        Millman’s theorem
# Author:      d.fathi
# Created:     24/02/2023
# Copyright:   (c) PyAMS 2023
# Licence:     free  "GPLv3"
#-------------------------------------------------------------------------------


#Step 1. Import the library of analog elements (PyAMS models) that are used in the circuit.
from sys import path;
path+=["../"];

import PyAMS

from  Resistor  import  *;
from  DCVoltage  import  *;
from  simu import AppPyAMS

number_of_branches=3;
R=[]
V=[]

for i in range(1,number_of_branches+1):
  #Step 2. Add the names of the models in the circle with the position of attachment
  R+=[Resistor("Vout",str(i))];
  V+=[DCVoltage(str(i),"0")];


  #Step 3. Modifying parameters of the elements.
  R[i-1].R+=1000*i;
  V[i-1].Vdc+=i;


#Step 4. Importing command of analysis.
AppPyAMS.circuit(*R,*V);
AppPyAMS.setOut("Vout");
AppPyAMS.analysis(mode="op");
AppPyAMS.run();

#Step 5. Print out
AppPyAMS.getOut("Vout");
