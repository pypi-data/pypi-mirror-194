#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 22:51:49 2023

@author: CSChisholm

#Functions to implement Bessel transformations and radial derivatives as well
# as Bessel quadrature integration. Based on AU-CHEN LEE, D. BAILLIE, AND
# P. B. BLAKIE, PHYSICAL REVIEW RESEARCH 3, 013283 (2021). Sec. III.A.1
#The author's use case is working with XMDS2 (http://xmds.org) output data but
# these functions can be used for other purposes also.

"""

from typing import Tuple
import numpy as np
import scipy.special as sp
import types

def BesselParameters(RR: float, Ngrid: int, order: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, float]:
    '''Get Bessel grid points in position space and reciprocal space as well as
    weights for Bessel quadrature in positions space and reciprocal space
    See AU-CHEN LEE, D. BAILLIE, AND P. B. BLAKIE, PHYSICAL REVIEW RESEARCH 3, 013283 (2021)
    Sec. III.A.1
    
    RR: Outer radius of grid interval
    Ngrid: Number of grid points
    order: Order of Bessel function to use (most of the time, leave it as zero)
    
    return grid, weights, gridK, weightsK, KK'''
    zeros = sp.jn_zeros(order,Ngrid+1)
    #Formulate grid points
    KK = zeros[-1]/RR
    grid = np.divide(zeros[:-1],KK)
    #Calculate weights
    weights = np.divide(2/(KK**2),np.power(np.absolute(sp.jv(order+1,zeros[:-1])),2))
    #Grid and weights in k-space
    gridK = np.divide(zeros[:-1],RR)
    weightsK = np.divide(2/(RR**2),np.power(np.absolute(sp.jv(order+1,zeros[:-1])),2))
    return grid, weights, gridK, weightsK, KK

def BesselQuadrature(func: types.FunctionType, RR: float, Ngrid=8, order=0, args=None) -> float:
    '''Integrates \int_0^RR dr r*func(r) using Bessel quadrature on Ngrid sampling points
    See AU-CHEN LEE, D. BAILLIE, AND P. B. BLAKIE, PHYSICAL REVIEW RESEARCH 3, 013283 (2021)
    Sec. III.A.1
    
    func: function to integrate
    RR: Upper limit of integration (this method is valid for RR -> infinity but finite RR works if the function tends to zero at a small value of r)
    (optional) Ngrid: Number of grid points to use
    (optional) order: Order of Bessel function to use (most of the time, leave it as zero)
    (optional) args: additional arguments for func (iterable)    
    
    return besselquadrature'''
    grid, weights = BesselParameters(RR,Ngrid,order)[:2]
    if (args is not None):
        funcSamples = func(grid,*args)
    else:
        funcSamples = func(grid)
    return np.sum(np.multiply(weights,funcSamples))

def BesselQuadratureK(func: types.FunctionType, RR: float, Ngrid=8, order=0, args=None) -> float:
    '''Version of BesselQuadrature for reciprocal k-space
    Integrates \int_0^infinity dk k*func(k) using Bessel quadrature on Ngrid sampling points
    See AU-CHEN LEE, D. BAILLIE, AND P. B. BLAKIE, PHYSICAL REVIEW RESEARCH 3, 013283 (2021)
    Sec. III.A.1
    
    func: function to integrate
    RR: Outer radius of sampling region in real space (this method is valid for RR -> infinity but finite RR works if the function tends to zero at a small value of r)
    (optional) Ngrid: Number of grid points to use
    (optional) order: Order of Bessel function to use (most of the time, leave it as zero)
    (optional) args: additional arguments for func (iterable) 
    
    return besselquadrature'''
    grid, weights = BesselParameters(RR,Ngrid,order)[2:4]
    if (args is not None):
        funcSamples = func(grid,*args)
    else:
        funcSamples = func(grid)
    return np.sum(np.multiply(weights,funcSamples))

def BesselQuadratureN(funcSamples: np.ndarray, RR: float, order=0) -> float:
    '''Version of BesselQuadrature for presampled function
    
    funcSamples: Presampled function
    RR: Outer radius for sampling
    (optional) order: Order of Bessel function used for sampling
    
    return besselquadrature'''
    weights = BesselParameters(RR,len(funcSamples),order)[1]
    return np.sum(np.multiply(weights,funcSamples))

def BesselQuadratureN_array(funcSamples: np.ndarray, RR: float, axis: int, order=0) -> np.ndarray:
    '''Applies BesselQuadratureN to one axis of an N-dimensional array
    
    funcSamples: Presampled function
    RR: Outer radius for sampling
    axis: The axis to integrate
    (optional) order: Order of Bessel function used for sampling
    
    return besselquadrature'''
    gridshape = np.shape(funcSamples)
    weights = BesselParameters(RR,gridshape[axis],order)[1]
    axes = []
    for itr, axlen in enumerate(gridshape):
        if (itr==axis):
            axes.append(weights)
        else:
            axes.append(np.linspace(1,axlen,axlen))
    WEIGHTS = np.meshgrid(*axes,indexing='ij')[axis]
    return np.sum(np.multiply(WEIGHTS,funcSamples),axis=axis)

def BesselQuadratureKN(funcSamples: np.ndarray, RR: float, order=0) -> float:
    '''Version of BesselQuadratureK for presampled function
    
    funcSamples: Presampled function
    RR: Outer radius for sampling
    (optional) order: Order of Bessel function to used for sampling
    
    return besselquadrature'''
    weights = BesselParameters(RR,len(funcSamples),order)[3]
    return np.sum(np.multiply(weights,funcSamples))

def BesselQuadratureKN_array(funcSamples: np.ndarray, RR: float, axis: int, order=0) -> np.ndarray:
    '''Applies BesselQuadratureKN to one axis of an N-dimensional array
    
    funcSamples: Presampled function
    RR: Outer radius for sampling
    axis: The axis to integrate
    (optional) order: Order of Bessel function to used for sampling
    
    return besselquadrature'''
    gridshape = np.shape(funcSamples)
    weights = BesselParameters(RR,gridshape[axis],order)[3]
    axes = []
    for itr, axlen in enumerate(gridshape):
        if (itr==axis):
            axes.append(weights)
        else:
            axes.append(np.linspace(1,axlen,axlen))
    WEIGHTS = np.meshgrid(*axes,indexing='ij')[axis]
    return np.sum(np.multiply(WEIGHTS,funcSamples),axis=axis)

def BesselHankelMat(RR: float, Ngrid=8, order=0) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    '''Construct Hankel transform matrix (and inverse) for cylindrical Bessel transform
    The grid points in reciprocal space are also returned since the most likely
    use of this function is computing the transverse Laplacian.
    This is not an unlisted helper because another use is actually doing the Bessel transform.
    See AU-CHEN LEE, D. BAILLIE, AND P. B. BLAKIE, PHYSICAL REVIEW RESEARCH 3, 013283 (2021)
    Sec. III.A.1
    
    RR: Outer radius of spatial grid
    (optional) Ngrid: Number of grid points
    (optional) order: Order of Bessel transform
    
    return hankelmatrix, inversehankelmatrix, gridK, grid'''
    grid, weights, gridK, weightsK, KK = BesselParameters(RR,Ngrid,order)
    WEIGHTS = np.meshgrid(gridK,weights,indexing='ij')[1]
    hankelmat = np.multiply(WEIGHTS,sp.jv(order,np.outer(gridK,grid)))
    inversehankelmat = np.multiply((KK/RR)**2,hankelmat)
    return hankelmat, inversehankelmat, gridK, grid

def BesselTransverseLaplacian(func: types.FunctionType, RR: float, Ngrid=8, order=0, args=None) -> Tuple[np.ndarray, np.ndarray]:
    '''Calculate the transverse Lapalcian of func on a Bessel grid
    \nabla^2 \left(f(r) e^{i m \theta}\right) &= \left(\frac{\partial^2 f}{\partial r^2} +\frac{1}{r}\frac{\partial f}{\partial r} -\frac{m^2}{r^2} f \right) e^{i m \theta}
    
    func: function to integrate
    RR: Upper limit of integration (this method is valid for RR -> infinity but finite RR works if the function tends to zero at a small value of r)
    (optional) Ngrid: Number of grid points to use
    (optional) order: Order of Bessel function to use (most of the time, leave it as zero)
    (optional) args: additional arguments for func (iterable)   
    
    return grid, D2Tfunc(r)'''
    grid = BesselParameters(RR,Ngrid,order)[0]
    return grid, (BesselTransverseLaplacianMatrix(RR,Ngrid=Ngrid)@np.reshape(func(grid,*args),(Ngrid,1))).ravel()

def BesselTransverseLaplacianMatrix(RR: float, Ngrid=8, order=0) -> np.ndarray:
    '''Construct a matrix to represent the transverse Laplacian operator in cylindrical coordinates
    Reference: http://www.xmds.org/reference_elements.html#geometry-element
    \nabla^2 \left(f(r) e^{i m \theta}\right) &= \left(\frac{\partial^2 f}{\partial r^2} +\frac{1}{r}\frac{\partial f}{\partial r} -\frac{m^2}{r^2} f \right) e^{i m \theta} = \left\{\mathcal{H}^{-1}_m \left[(-k^2) F_m(k)\right](r) \right\} e^{i m \theta}
    
    RR: Outer radius of spatial grid
    (optional) Ngrid: number of grid points
    (optional) order: Order of Bessel transform
    
    return nablaT2'''
    hankelmat, inversehankelmat, gridK = BesselHankelMat(RR,Ngrid,order)[:3]
    return inversehankelmat@np.diag(-np.power(gridK,2))@hankelmat