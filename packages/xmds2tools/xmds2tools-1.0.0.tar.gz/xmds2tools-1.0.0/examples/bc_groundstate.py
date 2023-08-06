#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 11:24:48 2023

@author: CSChisholm
"""

#Using the reader module to load the .h5 file generate by the example in the
# xmds installation directory examples/bessel_cosine_groundstate.xmds

import numpy as np
import matplotlib.pyplot as plt
from xmds2tools import reader
from xmds2tools import bessel

plt.close('all')

data = reader.ReadH5('bc_groundstate.h5')
variables = reader.ParseXSIL('bc_groundstate.xsil')['Variables']

#Plot imaginary time evolution by integrating out spatial axes
plt.figure()
plt.subplot(1,2,1)
plt.pcolormesh(data['1']['z'],data['1']['t'],2*np.pi*bessel.BesselQuadratureN_array(data['1']['norm_dens'], variables['rOuter'], 1),shading='auto')
plt.xlabel('z')
plt.ylabel('t')
plt.colorbar()
plt.subplot(1,2,2)
plt.pcolormesh(data['1']['r'],data['1']['t'],2*np.diff(data['1']['z'])[0]*np.sum(data['1']['norm_dens'],axis=-1),shading='auto')
plt.xlabel('r')
plt.ylabel('t')
plt.colorbar()
plt.tight_layout()

#Plot last density
plt.figure()
plt.pcolormesh(data['1']['z'],data['1']['r'],data['1']['norm_dens'][-1],shading='auto')
plt.xlabel('z')
plt.ylabel('r')
plt.colorbar()

#Check normalisation, we get one here because the script normalises to Nparticles but the sampling group is divided by Ncalc
norm = 4*np.pi*np.diff(data['1']['z'])[0]*np.sum(bessel.BesselQuadratureN_array(data['1']['norm_dens'], variables['rOuter'], 1),axis=-1)
plt.figure()
plt.plot(data['1']['t'],norm)
plt.xlabel('t')
plt.ylabel('norm')