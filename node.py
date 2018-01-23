#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 23:18:15 2018

@author: wei
"""

from CoolProp.CoolProp import PropsSI

class Node(object):
    
    # define the Props of the node
    def __init__(self, fluid="REFPROP::Water"):
        self.fluid = fluid
        self.p = None
        self.t = None
        self.h = None
        self.s = None
        self.d = None
        self.q = None
     
    # use pt() to clac Props of the node
    def pt(self):
        self.h = PropsSI("H", "P", self.p, "T", self.t, self.fluid)
        self.s = PropsSI("S", "P", self.p, "T", self.t, self.fluid)
        self.d = PropsSI("D", "P", self.p, "T", self.t, self.fluid)
        self.q = PropsSI("Q", "P", self.p, "T", self.t, self.fluid)
        if self.q < 0:
            self.q = 'subcool'
        elif 0 <= self.q <= 1:
            self.q = self.q
        else:
            self.q = 'supderheat'

    
    # print all of Props of the node
    def __str__(self):
        result = '{:^16.2f}, {:^16.2f}, {:^16.2f}, {:^16.2f}, {:^16.2f}, {:^16}' \
        .format(self.p, self.t, self.h, self.s, self.d, self.q)
        return result
    
#   testk
if __name__ == '__main__':
    # 配合課本或 NIST檢查
    # 20 KPa, 800C 查表得 v = 2.475 m^3/kg, h = 4159.2 KJ/kg, s = 9.2460 (KJ/kg)*K
    nodes = Node()
    nodes.p = 20000
    nodes.t = 273.15 + 800
    nodes.pt()
    msg = nodes.__str__()
    print(' {:^16}, {:^16}, {:^16}, {:^16}, {:^16}, {:^16}\n' \
          .format('p (Pa)', 't (K)', 'h (J/Kg)',  's ((J/Kg) * K)', 'd (Kg/m^3)', 'q'), msg)
    