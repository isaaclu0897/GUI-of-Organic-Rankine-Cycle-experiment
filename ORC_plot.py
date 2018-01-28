#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 20:40:46 2018

@author: wei
"""

import matplotlib.pyplot as plt 
from CoolProp.CoolProp import PropsSI 
import numpy as np 
import node 

# set label 
xAxis = "s" 
yAxis = "T" 
title = {"T": "T, °C", "s": "s, kJ/kgK"} 
plt.title("%s-%s Diagram" % (yAxis, xAxis)) 
plt.xlabel(title[xAxis]) 
plt.ylabel(title[yAxis]) 
plt.ylim(15, 90)
plt.xlim(1.05, 1.88)
plt.grid() 



tcrit = PropsSI('Tcrit', 'REFPROP::R245FA') - 0.00007 
tmin = PropsSI('Tmin', 'REFPROP::R245FA') 
T = np.linspace(tmin, tcrit, 50) 

for x in np.array([0, 1.0]): 
    S = np.array([PropsSI("S", "Q", x, "T", t, 'REFPROP::R245FA') for t in T]) 
    plt.plot(S / 1000, T - 273.15, 'r', lw=2.0) 

pumpi = {'name' : 'pump_inlet', 
         'nid' : 1, 
         'P' : 2.01, 
         'T' : 21.86} 
pumpo = {'name' : 'pump_ioutlet', 
         'nid' : 2, 
         'P' : 6.44, 
         'T' : 22.55} 
EVPo = {'name' : 'evaparator_outlet', 
        'nid' : 3, 
        'P' : 6.11, 
        'T' : 88.31} 
EXPi = {'name' : 'expander_inlet', 
        'nid' : 4, 
        'P' : 6.27, 
        'T' : 88.28} 
EXPo = {'name' : 'expander_outlet', 
        'nid' : 5, 
        'P' : 2.05, 
        'T' : 64.03} 
CDSi = {'name' : 'condenser_inlet', 
        'nid' : 6, 
        'P' : 1.99, 
        'T' : 56.68} 
CDSo = {'name' : 'condenser_outlet', 
        'nid' : 7, 
        'P' : 1.98, 
        'T' : 22.12} 

dev_list = [pumpi, pumpo, EVPo, EXPi, EXPo, CDSi, CDSo] 

nodes = [] 
for i in dev_list: 
    nodes.append(node.Node(i['name'], i['nid'])) 
     
for i, obj in enumerate(dev_list): 
    nodes[i].set_tp(obj['T'], obj['P']) 
    nodes[i].pt() 

t = [] 
s = [] 
for i in range(7): 
    t.append(nodes[i].t) 
    s.append(nodes[i].s / 1000) 

plt.plot(s, t, 'o')

# plot 6 bar iso_p
h = np.linspace(nodes[1].h, nodes[2].h, 50)
p = nodes[1].p
t = PropsSI('T', 'P', p * 100000, 'H', h, 'REFPROP::R245FA')
s = PropsSI('S', 'P', p * 100000, 'H', h, 'REFPROP::R245FA')
plt.plot(s/1000, t -273.15, 'b')
# plot 2 bar iso_p
h = np.linspace(nodes[5].h, nodes[6].h, 50)
p = nodes[5].p
t = PropsSI('T', 'P', p * 100000, 'H', h, 'REFPROP::R245FA')
s = PropsSI('S', 'P', p * 100000, 'H', h, 'REFPROP::R245FA')
plt.plot(s/1000, t -273.15, 'b')
# plot expander in out
h = np.linspace(nodes[3].h, nodes[4].h, 50)
t = PropsSI('T', 'S', nodes[3].s, 'H', h, 'REFPROP::R245FA')
s = PropsSI('S', 'T', t, 'H', h, 'REFPROP::R245FA')
plt.plot(s/1000, t - 273.15)
# plot pump in out
h = np.linspace(nodes[0].h, nodes[1].h, 50)
t = PropsSI('T', 'S', nodes[0].s, 'H', h, 'REFPROP::R245FA')
s = PropsSI('S', 'T', t, 'H', h, 'REFPROP::R245FA')
plt.plot(s/1000, t - 273.15)