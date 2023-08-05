result="E:/project/PyAMS/out/temp/Result_24_02_2023 18_16_01.txt"
net=['Vin', 'N02', 'Vout']
#------------------------------------------------------------------
from sys import path;
path+=["../../"]
path+=["E:/project/PyAMS/library"];
path+=["E:/project/PyAMS/library/Basic"];
path+=["E:/project/PyAMS/library/Source"];
path+=["E:/project/PyAMS/library/Semiconductor"];
import PyAMS
from PyAMS import time;
from simu import AppPyAMS;
from VCVS import VCVS
from Resistor import Resistor
from SinVoltage import SinVoltage
#------------------------------------------------------------------
C1=VCVS("Vin","0","Vout","0");
R1=Resistor("N02","Vin");
V1=SinVoltage("N02","0");
R2=Resistor("Vout","0");
#------------------------------------------------------------------
C1.setParam("  G=5");
R1.setParam("  R=1K");
V1.setParam("  Va=10V Fr=2Hz");
R2.setParam("  R=1K");
#------------------------------------------------------------------

AppPyAMS.circuit({"C1":C1,"R1":R1,"V1":V1,"R2":R2});

id=1;
data=[{'unique_id': 1, 'parent_id': 0, 'short_name': '', 'type': ' ', 'description': ' '}];
v=list(AppPyAMS.elements.values())
k=list(AppPyAMS.elements.keys())


id=id+1;
r=id;

data += [{'unique_id': id, 'parent_id': 1, 'short_name': 'Wire', 'type': ' ', 'description': ' '}]
for j in range(len(net)):
    id=id+1;
    data += [{'unique_id': id, 'parent_id': r, 'short_name':net[j]+'.V', 'type': 'wire', 'description': ''}]


for i in range(len(v)):
    signals=v[i].getSignals();
    params=v[i].getParamaters();
    id=id+1;
    r=id
    data += [{'unique_id': id, 'parent_id': 1, 'short_name': k[i], 'type': ' ', 'description': ' '}]
    for j in range(len(signals)):
          id=id+1;
          data += [{'unique_id': id, 'parent_id': r, 'short_name': signals[j].name, 'type': 'signal', 'description': signals[j].type, 'dir': signals[j].dir}]
    for j in range(len(params)):
          id=id+1;
          data += [{'unique_id': id, 'parent_id': r, 'short_name': params[j].name, 'type': 'paramater', 'description': ''}]


file = open(result, "w", encoding="utf-8")
file.write(str(data))
file.close();