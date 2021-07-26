#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 20:40:46 2018

@author: wei
"""
# import matplotlib.pyplot as plt

from matplotlib.figure import Figure
# import matplotlib.lines as lin
from matplotlib.lines import Line2D
from CoolProp.CoolProp import PropsSI
from numpy import linspace, array
# import numpy as np
from thermo.node import Node
from thermo.unit import T, pps


def calc_StatusofORC(nodes, point=None):
    t = []
    s = []
    for i in point:
        t.append(nodes[i].t)
        s.append(nodes[i].s)

    return s, t


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

    def test_iso_line(self, num=50):
        if self.iso_type == None:
            raise ValueError("This isoline cannot be calculated!")
        elif self.iso_type == "isop":
            self._Ih = linspace(self.Node_in._h, self.Node_out._h, num)
            self._Ipa = linspace(self.Node_in._p, self.Node_out._p, num)
            self._Ipi = self.Node_in._p
        elif self.iso_type == "isos":
            self._Ih = linspace(self.Node_in._h, self.Node_out._h, num)
            self._Isa = linspace(self.Node_in._s, self.Node_out._s, num)
            self._Isi = linspace(self.Node_in._s, self.Node_in._s, num)
            # print(self._Ih, self._Isa)
        # 待改良slice點得位置

    def iso_line(self, nodes, num=50):
        if self.iso_type == None:
            raise ValueError("This isoline cannot be calculated!")
        elif self.iso_type == "isop":
            self._Ih = linspace(nodes[self.Node_in]._h,
                                nodes[self.Node_out]._h, num)
            self._Ipa = linspace(
                nodes[self.Node_in]._p, nodes[self.Node_out]._p, num)
            self._Ipi = nodes[self.Node_in]._p
        elif self.iso_type == "isos":
            self._Ih = linspace(nodes[self.Node_in]._h,
                                nodes[self.Node_out]._h, num)
            self._Isa = linspace(
                nodes[self.Node_in]._s, nodes[self.Node_out]._s, num)
            self._Isi = linspace(
                nodes[self.Node_in]._s, nodes[self.Node_in]._s, num)
            # print(self._Ih, self._Isa)

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

        self._iso = Line2D(self.Isi, self.Iti, color="grey", lw=2.0)
#        plt.pause(0.00000001)

        self._act = Line2D(self.Isa, self.Ita, color="b", lw=2.0)
#        plt.pause(0.00000000001)
        return self._iso, self._act

    def calc_stateline_data(self):
        return [self.Isi, self.Iti], [self.Isa, self.Ita]

    def plot_process(self, nodes):
        self.iso_line(nodes)
        self.calc_iso()

        return self.calc_stateline()

    def plot_process_data(self, nodes):
        self.iso_line(nodes)
        self.calc_iso()

        return self.calc_stateline_data()


def set_windows_GUI():
    fig = Figure(figsize=(8, 6), dpi=100)
    dia = fig.add_subplot(1, 1, 1)
    xAxis = "s"
    yAxis = "T"
    title = {"T": "T, °C", "s": "s, (kJ/kg)*K"}
    dia.set_title("%s-%s Diagram" % (yAxis, xAxis))
    dia.set_xlabel(title[xAxis])
    dia.set_ylabel(title[yAxis])
    dia.set_ylim(10, 135)
    dia.set_xlim(1.05, 1.88)
    dia.grid()
    return dia, fig


def calc_SaturationofCurve(fluid="R245FA", num=50):
    tcrit = PropsSI("Tcrit", fluid) - 0.00007
    tmin = PropsSI("Tmin", fluid)
    T_array = linspace(tmin, tcrit, num)
    X_array = array([0, 1.0])

    ''' calc the right and left of Saturation Curve '''
    lines = []
    for x in X_array:
        S = array([PropsSI("S", "Q", x, "T", t, "R245FA") for t in T_array])
        # print(pps.J2KJ(S), T.K2C(T_array))
        line = Line2D(pps.J2KJ(S), T.K2C(T_array), color="r", lw=1.8)
        lines.append(line)
    # print(lines)
    return lines


def clear_plot(dia):
    times = range(len(dia.lines)-2)
    for i in times:
        dia.lines.pop()
