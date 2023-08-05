#------------------------------------------------------------------
from sys import path;
path+=["../../"]
path+=["E:/project/pypi_0.0.2/pack/library"];
path+=["E:/project/pypi_0.0.2/pack/library/Basic"];
path+=["E:/project/pypi_0.0.2/pack/library/Source"];
path+=["E:/project/pypi_0.0.2/pack/library/Semiconductor"];
import PyAMS
from PyAMS import time;
from simu import AppPyAMS;
from Resistor import Resistor
from SinVoltage import SinVoltage
#------------------------------------------------------------------
R1=Resistor("N03","N01");
R2=Resistor("N01","0");
V1=SinVoltage("N03","0");
#------------------------------------------------------------------
R1.setParam("  R=1K");
R2.setParam("  R=1K");
V1.setParam("  Va=20V Fr=10Hz");
#------------------------------------------------------------------
AppPyAMS.cad=True
AppPyAMS.circuit({"R1":R1,"R2":R2,"V1":V1});
AppPyAMS.setOut("N01","N03")
AppPyAMS.analysis(mode="tran",start=0.0,stop=2,step=1);
AppPyAMS.run();

import matplotlib.pyplot as plt
Time = AppPyAMS.getOut(time)
Vin = AppPyAMS.getOut("N01")
Vout = AppPyAMS.getOut("N03")

import matplotlib
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot(Time, Vin, label="Vin")
ax.plot(Time, Vout, label="Vout")

ax.set(xlabel='Time [Sec]', ylabel='[Volt]', title='About as  sin wave circuit')
ax.grid()
ax.legend()
plt.show()

image_format = 'svg' # e.g .png, .svg, etc.
image_name = 'myimage.svg'
fig.savefig(image_name, format=image_format, dpi=1200)