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
    
    def pq(self):
        ''' change default unit
        
        the coolprop default unit is Pa & K, but I Accustomed to use Bar & C
        '''
        self.h = PropsSI("H", "P", P.Bar2Pa(self.p), "Q", self.q, self.fluid)
        self.s = PropsSI("S", "P", P.Bar2Pa(self.p), "Q", self.q, self.fluid)
        self.d = PropsSI("D", "P", P.Bar2Pa(self.p), "Q", self.q, self.fluid)
        self.t = PropsSI("T", "P", P.Bar2Pa(self.p), "Q", self.q, self.fluid)
        self.over = self.t - T.K2C(PropsSI("T", "P", P.Bar2Pa(self.p), "Q", 0.5, self.fluid))

            
    # set Props of P & T
    def set_tp(self, Temperature, Presspsure):
        self.p = Presspsure
        self.t = Temperature

    # print all of Props of the node
    def __str__(self):
        result = '{:^12}, {:^5}, {:^10.4f}, {:^12.5f}, {:^12.2f}, {:^12.2f}, {:^12.2f}, {:^12}, {:^12}' \
        .format(self.name, self.nid, self.p, self.t, self.h/1000, self.s/1000, self.d, self.q, self.over)
        return result
    
#    # use Bar, C, KJ/Kg, ((KJ/Kg) * K), (Kg/m^3) to output Props list
#    def statusProps(self):
#        return [self.p, self.t, self.h/1000, self.s/1000, self.d, self.q, self.over]

class Node2(object):
    
    # define the Props of the node
    def __init__(self, name, nid, fluid="REFPROP::R245FA"):
        self.fluid = fluid
        self.name = name
        self.nid = nid
        self._p = None
        self._t = None
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
    def t(self):
        return T.K2C(self._t)
    @t.setter
    def t(self, value):
        self._t = T.C2K(value)
        return self._t
    @property
    def h(self):
        return self._h / 1000
#    @h.setter
#    def h(self, value):
#        self._h = value * 1000
#        return self._h
    @property
    def s(self):
        return self._s / 1000
#    @s.setter
#    def s(self, value):
#        self._s = value * 1000
#        return self._s
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
        self._h = PropsSI("H", "P", self._p, "T", self._t, self.fluid)
        self._s = PropsSI("S", "P", self._p, "T", self._t, self.fluid)
        self._d = PropsSI("D", "P", self._p, "T", self._t, self.fluid)
        self.q = PropsSI("Q", "P", self._p, "T", self._t, self.fluid)
        self.over = self.t - T.K2C(PropsSI("T", "P", self._p, "Q", 0.5, self.fluid))

        if self.q < 0:
            self.q = 'subcool'
        elif 0 <= self.q <= 1:
            self.q = self.q
            self.over = self.t - T.K2C(PropsSI("T", "P", self._p, "Q", 1, self.fluid))
        else:
            self.q = 'supderheat'
    
    def pq(self):
        ''' change default unit
        
        the coolprop default unit is Pa & K, but I Accustomed to use Bar & C
        '''
        self.h = PropsSI("H", "P", self._p, "Q", self.q, self.fluid)
        self.s = PropsSI("S", "P", self._p, "Q", self.q, self.fluid)
        self.d = PropsSI("D", "P", self._p, "Q", self.q, self.fluid)
        self.t = PropsSI("T", "P", self._p, "Q", self.q, self.fluid)
        self.over = self.t - T.K2C(PropsSI("T", "P", self._p, "Q", 0.5, self.fluid))

            
    # set Props of P & T
    def set_tp(self, Temperature, Presspsure):
        self.p = Presspsure
        self.t = Temperature

    # print all of Props of the node
    def __str__(self):
        result = '{:^12}, {:^5}, {:^10.4f}, {:^12.5f}, {:^12.2f}, {:^12.2f}, {:^12.2f}, {:^12}, {:^12}' \
        .format(self.name, self.nid, self.p, self.t, self.h, self.s, self.d, self.q, self.over)
        return result
    
#    # use Bar, C, KJ/Kg, ((KJ/Kg) * K), (Kg/m^3) to output Props list
#    def statusProps(self):
#        return [self.p, self.t, self.h/1000, self.s/1000, self.d, self.q, self.over]
    
#   test
if __name__ == '__main__':
    from time import time
    # 配合課本或 NIST檢查
    # 20 KPa, 800C 查表得 v = 2.475 m^3/kg, h = 4159.2 KJ/kg, s = 9.2460 (KJ/kg)*K
    '''
    nodes = Node('point1', 1, "REFPROP::Water")
    nodes.p = 1.01325
    nodes.t = 100
    nodes.pt()
    msg = nodes.__str__()
    print(nodes, '\n')
    print('{:^12}, {:^5}, {:^10}, {:^12}, {:^12}, {:^12}, {:^12}, {:^12}, {:^12}\n' \
          .format('name', 'nodeid', 'p (bar)', 't (c)', 'h (KJ/Kg)',  's ((KJ/Kg) * K)', 'd (Kg/m^3)', 'q', 'over'), msg)
    '''
    ccc = 0

    for i in range(3):
        con = 0
        a = []
        b = []
        for i in range(100):
            t1 = time()

            for i in range(5):    
                node = Node('point1', 1)
                node.p = 2.01
                node.t = 21.86
                node.pt()
                node2 = Node('point2', 2)
                node2.p = 12.01
                node2.t = 221.86
                node2.pt()

    #            print(node, node2)
            s1 = time()-t1
            t2 = time()
            for i in range(5):    
                node = Node2('point1', 1)
                node.p = 2.01
                node.t = 21.86
                node.pt()
                node2 = Node2('point2', 2)
                node2.p = 12.01
                node2.t = 221.86
                node.pt()
            
    #            print(node, node2)
            s2 = time()-t2
            a.append(s1)
            b.append(s2)
            if s1 > s2:
                con += 1
#            print(s1,s2)
        
        if con >= 50:
            ccc += 1
        print(con)
        a = sum(a)
        b = sum(b)
        print(a, b)
    print(ccc)
    