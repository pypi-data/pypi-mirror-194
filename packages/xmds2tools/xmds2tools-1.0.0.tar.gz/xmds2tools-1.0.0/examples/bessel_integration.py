#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 11:45:44 2023

@author: CSChisholm
"""

#Using Bessel quadrature to integrate a Gaussian function

import numpy as np
import matplotlib.pyplot as plt
from xmds2tools import bessel

def Gauss(r,sigma):
    return np.multiply(2/(sigma**2),np.exp(-np.divide(np.power(r,2),sigma**2)))

plt.close('all')

sigma = 1 #Width of Gaussian
rOuter = 4*sigma #Set an upper integration bound four times the width of the Gaussian

#Plot the Gaussian
rr_Cart = np.linspace(0,rOuter,101)
rr_Bessel = bessel.BesselParameters(rOuter, 16, 0)[0]

plt.figure()
plt.plot(rr_Cart,Gauss(rr_Cart,sigma),label='Cartesian')
plt.scatter(rr_Bessel,Gauss(rr_Bessel,sigma),label='Bessel')
plt.xlabel('r')
plt.ylabel('G(r)')

#Compare number of points needed to calculate \int G(r)*rdr with Bessel quadrature and trapezium method
besselPoints = np.logspace(0,10,11,base=2,dtype=np.int64)
besselInt = np.array([bessel.BesselQuadrature(Gauss, rOuter, Ngrid=NN, args=(sigma,)) for NN in besselPoints])

trapzPoints = np.logspace(0,3,4,dtype=np.int64)
trapzInt = np.array([np.trapz(Gauss(np.linspace(0,rOuter,NN),sigma)*np.linspace(0,rOuter,NN),x=np.linspace(0,rOuter,NN)) for NN in trapzPoints])

plt.figure()
plt.plot(trapzPoints,trapzInt,label='Trapezium')
plt.plot(besselPoints,besselInt,label='Bessel')
plt.xlabel('Number of points')
plt.ylabel('$\int G(r)*r$d$r$')
plt.legend()
plt.xscale('log')