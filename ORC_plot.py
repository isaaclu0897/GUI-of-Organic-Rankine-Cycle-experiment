#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 20:40:46 2018

@author: wei
"""
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import matplotlib.lines as lin
from CoolProp.CoolProp import PropsSI 
import numpy as np 
from node import Node
from unit import P, T, pps

#def plot_StatusofORC(nodes):
#    t = []; s = []
#    for i in range(len(nodes)): 
#        t.append(nodes[i].t) 
#        s.append(nodes[i].s)
#    
#    plt.plot(s, t, 'bo')
# test 選點打印
def calc_StatusofORC(nodes, point=None):
    t = []; s = []
    for i in point: 
        t.append(nodes[i].t) 
        s.append(nodes[i].s)
    
    return lin.Line2D(s, t, color='b', linestyle='None', marker='o')
        
class ProcessPlot(Node):
    
    def __init__(self, Node_in, Node_out, iso_type=None, name=None, nid=None):
        super(ProcessPlot, self).__init__(name, nid)
        self.Node_in = Node_in
        self.Node_out = Node_out
        ''' test 改良繼承node寫法（好處：看起來更像物件）
        self._node_in = nodes[Node_in]
        self._node_out = nodes[Node_out]
        '''
        self.iso_type = iso_type
#        print(self._p, self._h, self.name, self.nid)
#        print(nodes[self.Node_in]._h, nodes[self.Node_in]._p)
#        print(np.linspace(nodes[self.Node_in]._h, nodes[self.Node_out]._h, 50))
#        print(self.iso_type)
        
        # 待改良slice點得位置
    def iso_line(self, nodes, num=50):
        if self.iso_type == None:
            raise ValueError("This isoline cannot be calculated!")
        elif self.iso_type == "isop":
            self._Ih = np.linspace(nodes[self.Node_in]._h, nodes[self.Node_out]._h, num)
            self._Ipa = np.linspace(nodes[self.Node_in]._p, nodes[self.Node_out]._p, num)
            self._Ipi = nodes[self.Node_in]._p
        elif self.iso_type == "isos":
            self._Ih = np.linspace(nodes[self.Node_in]._h, nodes[self.Node_out]._h, num)
            self._Isa = np.linspace(nodes[self.Node_in]._s, nodes[self.Node_out]._s, num)
            self._Isi = np.linspace(nodes[self.Node_in]._s, nodes[self.Node_in]._s, num)
            
    def calc_iso(self):
        if self.iso_type == "isop":      
            self._Ita = PropsSI("T", "P", self._Ipa, "H", self._Ih, self.fluid)
            self._Isa = PropsSI("S", "P", self._Ipa, "H", self._Ih, self.fluid)
            self._Iti = PropsSI("T", "P", self._Ipi, "H", self._Ih, self.fluid)
            self._Isi = PropsSI("S", "P", self._Ipi, "H", self._Ih, self.fluid)

        elif self.iso_type == "isos":            
            self._Ita = PropsSI("T", "S", self._Isa, "H", self._Ih, self.fluid)
            self._Iti = PropsSI("T", "S", self._Isi, "H", self._Ih, self.fluid)
    
    @property
    def Isi(self):
        return self._Isi / 1000
    @property
    def Isa(self):
        return self._Isa / 1000
    @property
    def Iti(self):
        return self._Iti - 273.15
    @property
    def Ita(self):
        return self._Ita - 273.15
    def calc_stateline(self):
#        self.Isi = self._Isi / 1000
#        self.Isa = self._Isa / 1000
#        self.Iti = self._Iti - 273.15
#        self.Ita = self._Ita - 273.15

        self._iso = lin.Line2D(self.Isi, self.Iti, color="grey", lw=2.0)
#        plt.pause(0.00000001) 

        self._act = lin.Line2D(self.Isa, self.Ita, color="b", lw=2.0)
#        plt.pause(0.00000000001)
        return self._iso, self._act
    
    def plot_process(self, nodes):
        self.iso_line(nodes)
        self.calc_iso()
        self.calc_stateline()
        return self._iso, self._act
        
def set_windows():
    fig = plt.figure()
    dia =  fig.add_subplot(1,1,1)
    xAxis = "s" 
    yAxis = "T" 
    title = {"T": "T, °C", "s": "s, (kJ/kg)*K"} 
    dia.set_title("%s-%s Diagram" %(yAxis, xAxis))
    dia.set_xlabel(title[xAxis])
    dia.set_ylabel(title[yAxis])
    dia.set_ylim(10, 135)
    dia.set_xlim(1.05, 1.88)
    dia.grid()
    return dia
def set_windows_GUI():
    fig = Figure(figsize=(8,6), dpi=100)
    dia = fig.add_subplot(1,1,1)
    xAxis = "s" 
    yAxis = "T" 
    title = {"T": "T, °C", "s": "s, (kJ/kg)*K"} 
    dia.set_title("%s-%s Diagram" %(yAxis, xAxis))
    dia.set_xlabel(title[xAxis])
    dia.set_ylabel(title[yAxis])
    dia.set_ylim(10, 135)
    dia.set_xlim(1.05, 1.88)
    dia.grid()
    return dia, fig
    

def calc_SaturationofCurve(fluid="REFPROP::R245FA", num=50):
    tcrit = PropsSI("Tcrit", fluid) - 0.00007
    tmin = PropsSI("Tmin", fluid) 
    T_array = np.linspace(tmin, tcrit, num) 
    X_array = np.array([0, 1.0])
    
    line = []
    for x in X_array: 
        S = np.array([PropsSI("S", "Q", x, "T", t, "REFPROP::R245FA") for t in T_array]) 
        line.append(lin.Line2D(pps.J2KJ(S), T.K2C(T_array), color="r", lw=2.0))
    return line


def clear_plot(dia):
    times = range(len(dia.lines)-2)
    for i in times:
        dia.lines.pop()
        
if __name__=="__main__":
    from ORC_sample import data
    from node import Node

    # set label 
    dia = set_windows()
    # plot Saturation of Curve
    sat_line = calc_SaturationofCurve()
    dia.add_line(sat_line[0])
    dia.add_line(sat_line[1])

    
    # import data
    dev_list = [pumpi, pumpo, EVPo, EXPi, EXPo, CDSi, CDSo] = data()

    # init node
    nodes = [Node(i["name"], i["nid"]) for i in dev_list]
    for i, obj in enumerate(dev_list):
        nodes[i].set_tp(obj["T"], obj["P"])
        nodes[i].pt()
    
    
    # plot status of ORC
#    plot_StatusofORC(nodes)
    state_point = calc_StatusofORC(nodes, [1, 2, 3, 4])
    dia.add_line(state_point)
    """ example
    ProcessPlot(0, 1, 'isos').plot_process
    a=ProcessPlot(3, 4, 'isos')
    a.iso_line(nodes)
    a.calc_iso()
    a.plot_iso()
    plot process of ORC
    """
    process = [ProcessPlot(0, 1, 'isos'),
               ProcessPlot(1, 2, 'isop'),
               ProcessPlot(2, 3, 'isop'),
               ProcessPlot(3, 4, 'isos'),
               ProcessPlot(4, 5, 'isop'),
               ProcessPlot(5, 6, 'isop'),
               ProcessPlot(6, 0, 'isop')]
    good = [plot.plot_process(nodes) for plot in process]
    
    for i in good:
        dia.add_line(i[0])
        dia.add_line(i[1])

    plt.show()
