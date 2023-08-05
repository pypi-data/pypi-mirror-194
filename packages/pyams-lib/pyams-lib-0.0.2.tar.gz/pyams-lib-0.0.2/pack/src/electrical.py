#-------------------------------------------------------------------------------
# Name:        electrical (voltage and current)
# Author:      d.fathi
# Created:     31/03/2020
# Modified:    07/02/2023
# Copyright:   (c) PyAMS 2023
# Licence:     free  "GPLv3"
#-------------------------------------------------------------------------------




voltage={'discipline':'electrical',
         'nature':'potential',
         'abstol': 1e-8,
         'chgtol':1e-14,
         'signalType':'voltage',
         'unit':'V'
         }



current={'discipline':'electrical',
         'nature':'flow',
         'abstol': 1e-8,
         'chgtol':1e-14,
         'signalType':'current',
         'unit':'A'
         }


