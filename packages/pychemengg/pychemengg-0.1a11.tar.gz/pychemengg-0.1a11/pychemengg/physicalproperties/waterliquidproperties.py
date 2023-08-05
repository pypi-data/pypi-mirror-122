# -*- coding: utf-8 -*-

# This file is part of pyChemEngg python package.
 
# PyChemEngg: A python-based framework to promote problem solving and critical
# thinking in chemical engineering.

# Copyright (c) 2021 Harvinder Singh Gill <profhsgill@gmail.com>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Module to compute physical properties of liquid water.

"""
import numpy as np
import os

def _loadwater_data():
    __location__ = os.path.realpath(
                        os.path.join(os.getcwd(), os.path.dirname(__file__)))
    water = []
    file_to_open = "data_waterproperties.txt"
    with open(os.path.join(__location__, file_to_open),"r") as water_file:
        for line in water_file:
            water.append([float(eval(x)) if x != "nan" else np.nan for x in line.strip().split()])
    water_file.close()
    water_data = np.array(water)
    return water_data

def density(T=None):
    r""" Provides density of liquid water at a temperature T.
    
    
    Parameters
    ----------
    T : `int or float`
        Temperature in 'Celsius' at which density is required.


    Returns
    -------
    density : `int or float`
       Density (kg/m3) at temperature T .
   
    
    Notes
    -----
    Look up table adapted from ref [1].
    
    Linear interpolation is performed when the temperature lies
    between tabulated entries.

    
    Examples
    --------
    First import the module **waterliquidproperties**.
       
    >>> from pychemengg.physicalproperties import waterliquidproperties as wlp 
    >>> wlp.density(T=32.5)
    995.0

    
    References
    ----------
    [1] Yunus A. Cengel and Afshin J. Ghajar, "Heat And Mass Transfer
    Fundamentals and Applications", 6th Edition. New York, McGraw Hill
    Education, 2020.
    
    """
    water_data = _loadwater_data()
    return np.interp(T, water_data[:,0], water_data[:,2])

def viscosity(T=None):
    r""" Provides viscosity of liquid water at a temperature T.
    
    
    Parameters
    ----------
    T : `int or float`
        Temperature in 'Celsius' at which viscosity is required.


    Returns
    -------
    Viscosity: `int or float`
        Dynamic viscosity (kg/ms) at temperature T.
   
    
    Notes
    -----
    Look up table adapted from ref [1].
    
    Linear interpolation is performed when the temperature lies
    between tabulated entries.

    
    Examples
    --------
    First import the module **waterliquidproperties**.
       
    >>> from pychemengg.physicalproperties import waterliquidproperties as wlp 
    >>> wlp.viscosity(T=50)
    0.0005470000000000001

    
    References
    ----------
    [1] Yunus A. Cengel and Afshin J. Ghajar, "Heat And Mass Transfer
    Fundamentals and Applications", 6th Edition. New York, McGraw Hill
    Education, 2020.
    """
    water_data = _loadwater_data()
    return np.interp(T, water_data[:,0], water_data[:,9])

def specificheat(T=None):
    r""" Provides specific heat of liquid water at a temperature T.
    
    
    Parameters
    ----------
    T : `int or float`
        Temperature in 'Celsius' at which specific heat is required.


    Returns
    -------
    specific heat : `int or float`
        Specific heat (J/kg K) at temperature T.
   
    
    Notes
    -----
    Look up table adapted from ref [1].
    
    Linear interpolation is performed when the temperature lies
    between tabulated entries.

    
    Examples
    --------
    First import the module **waterliquidproperties**.
       
    >>> from pychemengg.physicalproperties import waterliquidproperties as wlp 
    >>> wlp.specificheat(T=32.5)
    4178

    
    References
    ----------
    [1] Yunus A. Cengel and Afshin J. Ghajar, "Heat And Mass Transfer
    Fundamentals and Applications", 6th Edition. New York, McGraw Hill
    Education, 2020.
    
    """
    water_data = _loadwater_data()
    return np.interp(T, water_data[:,0], water_data[:,5])

def thermalconductivity(T=None):
    r""" Provides thermal conductivity of liquid water at a temperature T.
    
    
    Parameters
    ----------
    T : `int or float`
        Temperature in 'Celsius' at which thermal conductivity is required.


    Returns
    -------
    Thermal conductivity : `int or float`
        Thermal conductivity (W/mK) at temperature T.
   
    
    Notes
    -----
    Look up table adapted from ref [1].
    
    Linear interpolation is performed when the temperature lies
    between tabulated entries.

    
    Examples
    --------
    First import the module **waterliquidproperties**.
       
    >>> from pychemengg.physicalproperties import waterliquidproperties as wlp 
    >>> wlp.thermalconductivity(T=42.5)
    0.634

    
    References
    ----------
    [1] Yunus A. Cengel and Afshin J. Ghajar, "Heat And Mass Transfer
    Fundamentals and Applications", 6th Edition. New York, McGraw Hill
    Education, 2020.
    
    """
    water_data = _loadwater_data()
    return np.interp(T, water_data[:,0], water_data[:,7])

def heatofvaporization(T=None):
    r""" Provides heat of vaporization of liquid water at a temperature T.
    
    
    Parameters
    ----------
    T : `int or float`
        Temperature in 'Celsius' at which heat of vaporization is required.


    Returns
    -------
    Heat of vaporization : `int or float`
        Heat of vaporization (J/kg) at temperature T.
   
    
    Notes
    -----
    Look up table adapted from ref [1].
    
    Linear interpolation is performed when the temperature lies
    between tabulated entries.

    
    Examples
    --------
    First import the module **waterliquidproperties**.
       
    >>> from pychemengg.physicalproperties import waterliquidproperties as wlp 
    >>> wlp.heatofvaporization(T=68)
    2338800.0
    
    
    References
    ----------
    [1] Yunus A. Cengel and Afshin J. Ghajar, "Heat And Mass Transfer
    Fundamentals and Applications", 6th Edition. New York, McGraw Hill
    Education, 2020.
    
    """
    water_data = _loadwater_data()
    return np.interp(T, water_data[:,0], water_data[:,4])*1e3

def prandtlnumber(T=None):
    r""" Provides Prandtl number of liquid water at a temperature T
    
    
    Parameters
    ----------
    T : `int or float`
        Temperature in 'Celsius' at which Prandtl number is required.


    Returns
    -------
    Prandtl number: `int or float`
        Prandtl number at temperature T.
   
    
    Notes
    -----
    Look up table adapted from ref [1].
    
    Linear interpolation is performed when the temperature lies
    between tabulated entries.

    
    Examples
    --------
    First import the module **waterliquidproperties**.
       
    >>> from pychemengg.physicalproperties import waterliquidproperties as wlp 
    >>> wlp.prandtlnumber(T=42.5)
    0.7248

    
    References
    ----------
    [1] Yunus A. Cengel and Afshin J. Ghajar, "Heat And Mass Transfer
    Fundamentals and Applications", 6th Edition. New York, McGraw Hill
    Education, 2020.
    """
    water_data = _loadwater_data()
    return np.interp(T, water_data[:,0], water_data[:,11])

def volumeexpansioncoefficient(T=None):
    r""" Provides volume expansion coefficient of liquid water at a temperature T
    
    
    Parameters
    ----------
    T : `int or float`
        Temperature in 'Celsius' at which volume expansion coefficient is required.


    Returns
    -------
    Volume expansion coefficient : `int or float`
        Volume expansion coefficient (1/K) at temperature T.
   
    
    Notes
    -----
    Look up table adapted from ref [1].
    
    Linear interpolation is performed when the temperature lies
    between tabulated entries.

    
    Examples
    --------
    First import the module **waterliquidproperties**.
       
    >>> from pychemengg.physicalproperties import waterliquidproperties as wlp 
    >>> wlp.volumeexpansioncoefficient (T=42.5)
    0.000396

    
    References
    ----------
    [1] Yunus A. Cengel and Afshin J. Ghajar, "Heat And Mass Transfer
    Fundamentals and Applications", 6th Edition. New York, McGraw Hill
    Education, 2020.
    """
    water_data = _loadwater_data()
    return np.interp(T, water_data[:,0], water_data[:,13])

Cp = specificheat(T=18)
# col_0 = 'Temp (C)';
# col_1 = 'Saturation pressure (kPa)';
# col_2 = 'Density (liquid, kg/m3)';
# col_3 = 'Density (vapor, kg/m3)';
# col_4 = 'Enthaly/Heat of vaporization/condensation  kJ/kg';
# col_5 = 'Specific heat (liquid) J/kg K';
# col_6 = 'Specific heat (vapor) J/kg K';
# col_7 = 'Thermal cond (liquid) W/mK';
# col_8 = 'Thermal cond (vapor) W/mK';
# col_9 = 'Dynamic viscosity (liquid) kg/m s';
# col_10 = 'Dynamic viscosity (vapor) kg/m s';
# col_11 = 'Prandtl Number (liquid)';
# col_12 = 'Prandtl Number (vapor)';
# col_13 = 'Volume expansion coefficient (liquid), beta 1/K';