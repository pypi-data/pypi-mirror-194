#-------------------------------------------------------------------------------
# Name:        Voltage divider
# Author:      D.fathi
# Created:     29/01/2023
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


#Step 2. Add the names of the models in the circle with the position of attachment
R1=Resistor("Vin","Vout");
R2=Resistor("Vout","0");
V1=DCVoltage("Vin","0");

#Step 3. Modifying parameters of the elements.
R1.R+=100;
R2.R+=100;
V1.Vdc+=15;


#Step 4. Importing command of analysis.
AppPyAMS.circuit(R1,R2,V1);
AppPyAMS.setOut("Vin","Vout");
AppPyAMS.analysis(mode="op");
AppPyAMS.run();

#Step 5. Print out
AppPyAMS.getOut("Vin");
AppPyAMS.getOut("Vout");
