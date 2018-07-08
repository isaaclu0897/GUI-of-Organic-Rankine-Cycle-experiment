#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 20:43:53 2018

@author: wei
"""

from CoolProp.CoolProp import PropsSI
from unit import P, T, pps

class Node(object):
    
    # define the Props of the node
    def __init__(self, name=None, nid=None, fluid="REFPROP::R245FA"):
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
    def ps(self):
        ''' change default unit
        
        the coolprop default unit is Pa & K, but I Accustomed to use Bar & C
        '''
        self.t = PropsSI("T", "P", P.Bar2Pa(self.p), "S", (self.s), self.fluid)
        self.h = PropsSI("H", "P", P.Bar2Pa(self.p), "S", (self.s), self.fluid)
        self.d = PropsSI("D", "P", P.Bar2Pa(self.p), "S", (self.s), self.fluid)
        self.q = PropsSI("Q", "P", P.Bar2Pa(self.p), "S", (self.s), self.fluid)
        self.over = self.t - (PropsSI("T", "P", P.Bar2Pa(self.p), "Q", 0.5, self.fluid))

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
        result = '{:^12}, {:^5}, {:^12.2f}, {:^12.2f}, {:^12.2f}, {:^12.2f}, {:^12.2f}, {:^12}, {:^12.2f}' \
        .format(self.name, self.nid, self.p, self.t, self.h/1000, self.s/1000, self.d, self.q, self.over)
        return result
    def status(self):
        result = '{:^12.2f}, {:^12.2f}, {:^12.2f}, {:^12.2f}, {:^12.2f}, {:^12}, {:^12.2f}' \
        .format(self.p, self.t, self.h/1000, self.s/1000, self.d, self.q, self.over)
        return result




def main(tl, th, delta_subcool, delta_supheat, out, wan=False):
    if wan == True:
        print('小萬')
    tl = tl
    th = th
    delta_supheat = delta_supheat
    delta_subcool = delta_subcool
    
    pl = PropsSI('P', 'T', (tl + delta_subcool) + 273.15, 'Q', 0, 'REFPROP::R245FA') / 1e5
    if wan == True:
        ph = pl + 5
    else:
        ph = PropsSI('P', 'T', (th - delta_supheat) + 273.15, 'Q', 0, 'REFPROP::R245FA') / 1e5
    
    points = [None, 'pump_in', 'pump_out', 'exp_in', 'exp_out']
    point = []
    for index, pointss in enumerate(points, start=0):
        point.append(Node(pointss, index))
        
    point[1].set_tp(tl, pl)
    point[1].pt()
    
    point[2].p = ph
    point[2].s = point[1].s
    point[2].ps()
    
    point[3].set_tp(th, ph)
    point[3].pt()
    
    point[4].p = pl
    point[4].s = point[3].s
    point[4].ps()
    
    for i in range(1, 5):
        print(point[i])
    
    expact_output = out # 500w
    mdot = round(expact_output / (point[3].h-point[4].h), 5) # kg/s
    mdot_lpm = round((mdot * 60000 / point[2].d), 4)
    
    print('期望輸出: {}w,\t質量流率: {}kg/s,\t質量流率: {}LPM'.format(expact_output, mdot, mdot_lpm))

if __name__=='__main__':
    main(29, 90, 8, 8, 500,True)
    main(15.5, 90, 8, 8, 500, True)
    main(30, 100, 8, 8, 600)
    main(15, 100, 8, 8, 300)