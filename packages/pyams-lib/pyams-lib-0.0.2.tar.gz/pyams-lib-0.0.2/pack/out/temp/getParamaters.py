from sys import path;
path+=["../../"]
path+=["E:/project/PyAMS/library/Basic"];
path+=["E:/project/PyAMS/library/Source"];
path+=["E:/project/PyAMS/library/Semiconductor"];
from Resistor import Resistor
m=Resistor(2,3)
p=m.getParam("   R=1K");
file = open("E:/project/PyAMS/out/temp/Result_24_02_2023 18_23_02.txt", "w", encoding="utf-8")
file.write(str(p))
file.close();
