#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 23:18:15 2018

@author: wei
"""

from CoolProp.CoolProp import PropsSI
from unit import P, T

class Node(object):
    
    # define the Props of the node
    def __init__(self, name, nid, fluid="REFPROP::R245FA"):
        self.fluid = fluid
        self.name = name
        self.nid = nid
        self.p = None
        self.t = None
        self.h = None
        self.s = None
        self.d = None
        self.q = None
        self.over = None
     
    # use pt() to clac Props of the node
    def pt(self):
        ''' change default unit
        
        the coolprop default unit is Pa & K, but I Accustomed to use Bar & C
        '''
        self.h = PropsSI("H", "P", P.Bar2Pa(self.p), "T", T.C2K(self.t), self.fluid)
        self.s = PropsSI("S", "P", P.Bar2Pa(self.p), "T", T.C2K(self.t), self.fluid)
        self.d = PropsSI("D", "P", P.Bar2Pa(self.p), "T", T.C2K(self.t), self.fluid)
        self.q = PropsSI("Q", "P", P.Bar2Pa(self.p), "T", T.C2K(self.t), self.fluid)
        self.over = self.t - T.K2C(PropsSI("T", "P", P.Bar2Pa(self.p), "Q", 0.5, self.fluid))

        if self.q < 0:
            self.q = 'subcool'
        elif 0 <= self.q <= 1:
            self.q = self.q
            self.over = self.t - T.K2C(PropsSI("T", "P", P.Bar2Pa(self.p), "Q", 1, self.fluid))
        else:
            self.q = 'supderheat'
    # set Props of P & T
    def set_tp(self, Temperature, Presspsure):
        self.p = Presspsure
        self.t = Temperature

    # print all of Props of the node
    def __str__(self):
        result = '{:^12}, {:^5}, {:^12.2f}, {:^12.2f}, {:^12.2f}, {:^12.2f}, {:^12.2f}, {:^12}, {:^12}' \
        .format(self.name, self.nid, self.p, self.t, self.h/1000, self.s/1000, self.d, self.q, self.over)
        return result
    
    # use Bar, C, KJ/Kg, ((KJ/Kg) * K), (Kg/m^3) to output Props list
    def statusProps(self):
        return [self.p, self.t, self.h/1000, self.s/1000, self.d, self.q, self.over]
    
    ''' use tabulate with replace show_ORCProps
    
    def show_ORCProps(self):
        try:
            self.h = pps.Kilo(self.h)
            self.s = pps.Kilo(self.s)
            msg = self.p, self.t, self.h, self.s, self.d, self.q
            p, t, h, s, d, q = msg
            print(' {:^16}, {:^16}, {:^16}, {:^16}, {:^16}, {:^16}' \
              .format('p (Pa)', 't (K)', 'h (J/Kg)',  's ((J/Kg) * K)', 'd (Kg/m^3)', 'q'))
            print('{:^16.4f}, {:^16.4f}, {:^16.2f}, {:^16.4f}, {:^16.2f}, {:^16}' \
              .format(p, t, h, s, d, q))
            print()
        finally:
            self.h = pps.Millim(self.h)
            self.s = pps.Millim(self.s)
    '''
    
#   test
if __name__ == '__main__':
    # 配合課本或 NIST檢查
    # 20 KPa, 800C 查表得 v = 2.475 m^3/kg, h = 4159.2 KJ/kg, s = 9.2460 (KJ/kg)*K
    nodes = Node('point1', 1, "REFPROP::Water")
    nodes.p = 1.01325
    nodes.t = 120
    nodes.pt()
    msg = nodes.__str__()
    print(nodes, '\n')
    print('{:^12}, {:^5}, {:^10}, {:^12}, {:^12}, {:^12}, {:^12}, {:^12}, {:^12}\n' \
          .format('name', 'nodeid', 'p (bar)', 't (c)', 'h (KJ/Kg)',  's ((KJ/Kg) * K)', 'd (Kg/m^3)', 'q', 'over'), msg)
    