#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 23:18:15 2018

@author: wei
"""
from CoolProp.CoolProp import PropsSI
from unit import P, T
from json import dumps

# I don't want to use refprop.
# def fixpath():
#     """ set different path of OS """
#     from platform import system
#     if system() == 'Linux':
#         path = r'/opt/refprop'
#     else:
#         path = r'C:\Program Files (x86)\REFPROP'
#     import CoolProp.CoolProp as CP;CP.set_config_string(CP.ALTERNATIVE_REFPROP_PATH, path)
#     # CP.get_global_param_string("REFPROP_version")
# fixpath()
class Node(object):
    
    # define the Props of the node
    def __init__(self, name=None, nid=None, fluid="R245FA"):
        self.fluid = fluid
        self.name = name
        self.nid = nid
        self._p = 0
        self._pSat = None
        self._t = 0
        self._tSat = 0
        self._h = None
        self._s = None
        self._d = None
        self._q = None
        self._over = None
    @property
    def p(self):
        return P.Pa2Bar(self._p)
    @p.setter
    def p(self, value):
        self._p = P.Bar2Pa(value)
        return self._p
    @property
    def pSat(self):
        return P.Pa2Bar(self._pSat)
    @pSat.setter
    def pSat(self, value):
        self._pSat = P.Bar2Pa(value)
        return self._pSat
    @property
    def t(self):
        return T.K2C(self._t)
    @t.setter
    def t(self, value):
        self._t = T.C2K(value)
        return self._t
    @property
    def tSat(self):
        return T.K2C(self._tSat)
    @tSat.setter
    def tSat(self, value):
        self._tSat = T.C2K(value)
        return self._t
    @property
    def h(self):
        return self._h / 1000
    @h.setter
    def h(self, value):
        self._h = value * 1000
        return self._h
    @property
    def s(self):
        return self._s / 1000
    @s.setter
    def s(self, value):
        self._s = value * 1000
        return self._s
    @property
    def d(self):
        return self._d
#    @d.setter
#    def d(self, value):
#        self._d = value * 1000
#        return self._d
     
    # use pt() to clac Props of the node
    def pt(self):
        ''' change default unit
        
        the coolprop default unit is Pa & K, but I Accustomed to use Bar & C
        '''
        self._h, self._s, self._d = PropsSI(["H", "S", "D"], "P", self._p, "T", self._t, self.fluid)

        # assume that Q is equal to 0
        self._pSat, self._tSat = PropsSI(["P", "T"], "Q", 0, "T", self._t, self.fluid)

        self._over = self.t - self.tSat
        
        if self._over <= 0:
            self.q = 'subcool'
        else:
            self.q = 'supderheat'


    def pq(self):
        ''' change default unit
        
        the coolprop default unit is Pa & K, but I Accustomed to use Bar & C
        '''

        self._h, self._s, self._d, self._t = PropsSI(["H", "S", "D", "T"], "P", self._p, "Q", self.q, self.fluid)
        
        self._tSat, self._pSat = PropsSI(["T", "P"], "P", self._p, "Q", 0.5, self.fluid)

        self._over = self.t - self.tSat
            

            
    # set Props of P & T
    def set_tp(self, Temperature, Presspsure):
        self.p = Presspsure
        self.t = Temperature

    def __repr__(self):
        nodeInfo = {
            "fluid" : self.fluid,
            "name" : self.name,
            "nodeID" : self.nid,
            "pressure" : self.p,
            "pressure(Sat)" : self.pSat,
            "temperature" : self.t,
            "temperature(Sat)" : self.tSat,
            "enthalpy(h)" : self.h,
            "entropy(s)" : self.s,
            "density" : self.d,
            "quality" : self.q,
            "over" : self._over
        }

        return dumps(nodeInfo, indent=4)
    
#    # use Bar, C, KJ/Kg, ((KJ/Kg) * K), (Kg/m^3) to output Props list
#    def statusProps(self):
#        return [self.p, self.t, self.h/1000, self.s/1000, self.d, self.q, self.over]
    
#   
if __name__ == '__main__':
    # 配合課本或 NIST檢查
    # 20 KPa, 800C 查表得 v = 2.475 m^3/kg, h = 4159.2 KJ/kg, s = 9.2460 (KJ/kg)*K
    node1 = Node(None, 1, "Water")
    node1.p = 1.01325
    node1.t = 100
    node1.pt()

    node2 = Node(None, 2, "Water")
    node2.p = 1.01325
    node2.q = 0.5
    node2.pq()
    print("---test node---")
    print(node1)
    print(node2)
    
    # test PropsSI
    import numpy as np
    from CoolProp.CoolProp import PropsSI
    print("---test PropsSI---")
    print(PropsSI('T','P', 1.01325 * 1e5,'Q',0,'Water') - 273)
    print(PropsSI('P','T',[25+273, 25+273],'Q',[0,1], "R245FA") / 1e5)
    print(PropsSI(['H', 'S', 'D'],'P',[1.01325 * 1e5, 1.01325 * 1e5],'T',[20+273,50+273],'Water')/1000)


    import CoolProp
    from CoolProp.Plots import PropertyPlot
    ts_plot = PropertyPlot('Water', 'Ts')
    ts_plot.calc_isolines(CoolProp.iQ, num=11)
    ts_plot.title(r'$T,s$ Graph for Water')
    ts_plot.xlabel(r'$s$ [kJ/kg K]')
    ts_plot.ylabel(r'$T$ [K]')
    ts_plot.grid()
    ts_plot.show()
