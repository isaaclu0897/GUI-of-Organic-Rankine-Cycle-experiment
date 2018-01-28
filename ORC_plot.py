#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 20:40:46 2018

@author: wei
"""
import matplotlib.pyplot as plt 
from CoolProp.CoolProp import PropsSI 
import numpy as np 
from node import Node
from unit import P, T, pps
class ProcessPlot(Node):
    
    def __init__(self, Node_in, Node_out, iso_type=None, name=None, nid=None):
        super(ProcessPlot, self).__init__(name, nid)
        self.Node_in = Node_in
        self.Node_out = Node_out
        self.iso_type = iso_type

    def iso_line(self, nodes, num=100):
        if self.iso_type == None:
            raise ValueError("This isoline cannot be calculated!")
        elif self.iso_type == 'isop':
            self.h = np.linspace(nodes[self.Node_in].h, nodes[self.Node_out].h, num)
            self.pa = np.linspace(nodes[self.Node_in].p, nodes[self.Node_out].p, num)
            self.pi = nodes[self.Node_in].p
        elif self.iso_type == 'isos':
            self.h = np.linspace(nodes[self.Node_in].h, nodes[self.Node_out].h, num)
            self.sa = np.linspace(nodes[self.Node_in].s, nodes[self.Node_out].s, num)
            self.si = np.linspace(nodes[self.Node_in].s, nodes[self.Node_in].s, num)
            
    def calc_iso(self):
        if self.iso_type == 'isop':
            self._x = P.Bar2Pa(self.pa)
            self._y = P.Bar2Pa(self.pi)
            
            self.ta = PropsSI('T', 'P', self._x, 'H', self.h, self.fluid)
            self.sa = PropsSI('S', 'P', self._x, 'H', self.h, self.fluid)
            self.ti = PropsSI('T', 'P', self._y, 'H', self.h, self.fluid)
            self.si = PropsSI('S', 'P', self._y, 'H', self.h, self.fluid)

        elif self.iso_type == 'isos':            
            self.ta = PropsSI('T', 'S', self.sa, 'H', self.h, self.fluid)
            self.ti = PropsSI('T', 'S', self.si, 'H', self.h, self.fluid)

    def plot_iso(self):
        plt.plot(pps.J2KJ(self.si), T.K2C(self.ti), 'grey')
        plt.plot(pps.J2KJ(self.sa), T.K2C(self.ta), 'b')
        
if __name__=='__main__':
    
    
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
    Ti = np.linspace(tmin, tcrit, 50) 
    
    for x in np.array([0, 1.0]): 
        S = np.array([PropsSI("S", "Q", x, "T", t, 'REFPROP::R245FA') for t in Ti]) 
        plt.plot(S / 1000, Ti - 273.15, 'r', lw=2.0) 
    
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
        nodes.append(Node(i['name'], i['nid'])) 
         
    for i, obj in enumerate(dev_list): 
        nodes[i].set_tp(obj['T'], obj['P']) 
        nodes[i].pt() 
    
    t = [] 
    s = [] 
    for i in range(7): 
        t.append(nodes[i].t) 
        s.append(nodes[i].s / 1000)
    
    plt.plot(s, t, 'o')
    
    plot1 = ProcessPlot(0, 1, 'isos')
    plot1.iso_line(nodes)
    plot1.calc_iso()
    plot1.plot_iso()      

    plot1 = ProcessPlot(1, 2, 'isop')
    plot1.iso_line(nodes)
    plot1.calc_iso()
    plot1.plot_iso()
    
    plot1 = ProcessPlot(2, 3, 'isop')
    plot1.iso_line(nodes)
    plot1.calc_iso()
    plot1.plot_iso()

    plot1 = ProcessPlot(3, 4, 'isos')
    plot1.iso_line(nodes)
    plot1.calc_iso()
    plot1.plot_iso()  
    
    plot1 = ProcessPlot(4, 5, 'isop')
    plot1.iso_line(nodes)
    plot1.calc_iso()
    plot1.plot_iso()    
    
    plot1 = ProcessPlot(5, 6, 'isop')
    plot1.iso_line(nodes)
    plot1.calc_iso()
    plot1.plot_iso()
    
    plot1 = ProcessPlot(6, 0, 'isop')
    plot1.iso_line(nodes)
    plot1.calc_iso()
    plot1.plot_iso()   




