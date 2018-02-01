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

def plot_StatusofORC(nodes):
    t = []; s = []
    for i in range(len(nodes)): 
        t.append(nodes[i].t) 
        s.append(pps.J2KJ(nodes[i].s))
    
    plt.plot(s, t, 'bo')
        
class ProcessPlot(Node):
    
    def __init__(self, Node_in, Node_out, iso_type=None, name=None, nid=None):
        super(ProcessPlot, self).__init__(name, nid)
        self.Node_in = Node_in
        self.Node_out = Node_out
        self.iso_type = iso_type

    def iso_line(self, nodes, num=100):
        if self.iso_type == None:
            raise ValueError("This isoline cannot be calculated!")
        elif self.iso_type == "isop":
            self.h = np.linspace(nodes[self.Node_in].h, nodes[self.Node_out].h, num)
            self.pa = np.linspace(nodes[self.Node_in].p, nodes[self.Node_out].p, num)
            self.pi = nodes[self.Node_in].p
        elif self.iso_type == "isos":
            self.h = np.linspace(nodes[self.Node_in].h, nodes[self.Node_out].h, num)
            self.sa = np.linspace(nodes[self.Node_in].s, nodes[self.Node_out].s, num)
            self.si = np.linspace(nodes[self.Node_in].s, nodes[self.Node_in].s, num)
            
    def calc_iso(self):
        if self.iso_type == "isop":
            self._x = P.Bar2Pa(self.pa)
            self._y = P.Bar2Pa(self.pi)
            
            self.ta = PropsSI("T", "P", self._x, "H", self.h, self.fluid)
            self.sa = PropsSI("S", "P", self._x, "H", self.h, self.fluid)
            self.ti = PropsSI("T", "P", self._y, "H", self.h, self.fluid)
            self.si = PropsSI("S", "P", self._y, "H", self.h, self.fluid)

        elif self.iso_type == "isos":            
            self.ta = PropsSI("T", "S", self.sa, "H", self.h, self.fluid)
            self.ti = PropsSI("T", "S", self.si, "H", self.h, self.fluid)

    def plot_iso(self):
        plt.plot(pps.J2KJ(self.si), T.K2C(self.ti), "grey")
#        plt.pause(0.00000001) 

        plt.plot(pps.J2KJ(self.sa), T.K2C(self.ta), "b")
#        plt.pause(0.00000000001) 
    
    def plot_process(self, nodes):
        self.iso_line(nodes)
        self.calc_iso()
        self.plot_iso()
        
def set_windows():
    plt.clf()
    xAxis = "s" 
    yAxis = "T" 
    title = {"T": "T, °C", "s": "s, (kJ/kg)*K"} 
    plt.title("%s-%s Diagram" % (yAxis, xAxis))
    plt.xlabel(title[xAxis]) 
    plt.ylabel(title[yAxis]) 
#    plt.ylim(15, 90)
#    plt.xlim(1.05, 1.88)
    plt.ylim(10, 135)
    plt.xlim(1.05, 1.88)
    plt.grid()
    plt.show()
    
def plot_SaturationofCurve(fluid="REFPROP::R245FA", num=50):
    tcrit = PropsSI("Tcrit", fluid) - 0.00007 
    tmin = PropsSI("Tmin", fluid) 
    T_array = np.linspace(tmin, tcrit, num) 
    X_array = np.array([0, 1.0])
    
    for x in X_array: 
        S = np.array([PropsSI("S", "Q", x, "T", t, "REFPROP::R245FA") for t in T_array]) 
        plt.plot(pps.J2KJ(S), T.K2C(T_array), "r", lw=2.0)
        
if __name__=="__main__":
    from ORC_sample import data
    from node import Node

    # set label 
    set_windows()
    
    # plot Saturation of Curve
    plot_SaturationofCurve(fluid="REFPROP::R245FA", num=50)
    
#    # set label 
#    xAxis = "s" 
#    yAxis = "T" 
#    title = {"T": "T, °C", "s": "s, kJ/kgK"} 
#    plt.title("%s-%s Diagram" % (yAxis, xAxis))
#    plt.xlabel(title[xAxis]) 
#    plt.ylabel(title[yAxis]) 
##    plt.ylim(15, 90)
##    plt.xlim(1.05, 1.88)
#    plt.grid()
#    plt.show()
#
#    plot Saturation of Curve
#    tcrit = PropsSI('Tcrit', 'REFPROP::R245FA') - 0.00007 
#    tmin = PropsSI('Tmin', 'REFPROP::R245FA') 
#    Ti = np.linspace(tmin, tcrit, 50) 
#    
#    for x in np.array([0, 1.0]): 
#        S = np.array([PropsSI("S", "Q", x, "T", t, 'REFPROP::R245FA') for t in Ti]) 
#        plt.plot(S / 1000, Ti - 273.15, 'r', lw=2.0)
##        plt.pause(0.5) 
    
    # import data
    dev_list = [pumpi, pumpo, EVPo, EXPi, EXPo, CDSi, CDSo] = data()
    dev = {'pumpi' : pumpi,
           'pumpo' : pumpo,
           'EVPo' : EVPo, 
           'EXPi' : EXPi, 
           'EXPo' : EXPo, 
           'CDSi' : CDSi, 
           'CDSo' : CDSo}

    # init node
    nodes = [Node(i["name"], i["nid"]) for i in dev_list]
    for i, obj in enumerate(dev_list):
        nodes[i].set_tp(obj["T"], obj["P"]) 
        nodes[i].pt()
    
    
    # plot status of ORC
    plot_status = plot_StatusofORC(nodes)
    
    # plot process of ORC
    process = [ProcessPlot(0, 1, 'isos'),
               ProcessPlot(1, 2, 'isop'),
               ProcessPlot(2, 3, 'isop'),
               ProcessPlot(3, 4, 'isos'),
               ProcessPlot(4, 5, 'isop'),
               ProcessPlot(5, 6, 'isop'),
               ProcessPlot(6, 0, 'isop')]
    [plot.plot_process(nodes) for plot in process]


