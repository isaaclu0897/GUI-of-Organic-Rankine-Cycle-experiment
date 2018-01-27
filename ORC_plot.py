#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 20:40:46 2018

@author: wei
"""

import matplotlib.pyplot as plt
from CoolProp.CoolProp import PropsSI
import numpy as np

# set label
xAxis = "s"
yAxis = "T"
title = {"T": "T, °C", "s": "s, kJ/kgK"}
plt.title("%s-%s Diagram" % (yAxis, xAxis))
plt.xlabel(title[xAxis])
plt.ylabel(title[yAxis])
plt.grid()



tcrit = PropsSI('Tcrit', 'REFPROP::R245FA') - 0.00007
tmax = PropsSI('Tmax', 'REFPROP::R245FA') 
tmin = PropsSI('Tmin', 'REFPROP::R245FA')
T = np.linspace(tmin, tcrit, 1000)

for x in np.array([0, 1.0]):
    S = np.array([PropsSI("S", "Q", x, "T", t, 'REFPROP::R245FA') for t in T]) / 1000
    plt.plot(S, T - 273.15, 'r', lw=2.0)