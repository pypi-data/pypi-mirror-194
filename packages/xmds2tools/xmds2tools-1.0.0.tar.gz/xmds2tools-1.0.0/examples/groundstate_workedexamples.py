#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 10:31:19 2023

@author: CSChisholm
"""

#Using the reader module to load the .h5 file generate by the worked example
# http://www.xmds.org/worked_examples.html#groundstatebec
#In the xmds installation directory, the code can be found in
# examples/groundstate_workedexamples.xmds

import numpy as np
import matplotlib.pyplot as plt
from xmds2tools import reader

plt.close('all')

data = reader.ReadH5('groundstate.h5')

#Plot imaginary time evolution
plt.figure()
plt.pcolormesh(data['1']['y'],data['1']['t'],data['1']['norm_dens'],shading='auto')
plt.xlabel('y')
plt.ylabel('t')
plt.colorbar()

#Check normalisation
norm = np.trapz(data['1']['norm_dens'],x=data['1']['y'],axis=1)

plt.figure()
plt.plot(data['2']['t'],data['2']['norm'],label='Sampling group')
plt.scatter(data['1']['t'],norm,label='Calculated')
plt.xlabel('t')
plt.ylabel('norm')
plt.legend()