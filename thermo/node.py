# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 23:18:15 2018

@author: wei
"""
from CoolProp.CoolProp import PropsSI
from json import dumps
from thermo.unit import T, P
from log import logger

logger.info('node!')

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


class Node:
    ''' define the Props of the node
    '''

    def __init__(self, name="", nid="", fluid="R245FA"):
        self.fluid = fluid
        self.name = name
        self.nid = nid
        self._p = 0
        self._pSat = 0
        self._t = 0
        self._tSat = 0
        self._h = 0
        self._s = 0
        self._d = 0
        self._q = 0
        self._over = 0

    ''' use setter and getter?
    def __setattr__(self, name, value):
        self.__dict__[name] = value
    def __getattr__(self, name):
        return self.name
    '''

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

    @property
    def over(self):
        return self._over

    @over.setter
    def over(self, value):
        self._over = value * 1000
        return self._over

#    @d.setter
#    def d(self, value):
#        self._d = value * 1000
#        return self._d

    @property
    def q(self):
        if self._q > 1:
            value = "superheat"
        elif self._q < 0:
            value = "subcool"
        else:
            value = self._q
        return value

    @q.setter
    def q(self, value):
        if value > 1:
            self._q = 2
        elif value < 0:
            self._q = -1
        else:
            self._q = value
        return self._q

    def __getitem__(self, name):

        if name == "p":
            value = self.p
        elif name == "pSat":
            value = self.pSat
        elif name == "t":
            value = self.t
        elif name == "tSat":
            value = self.tSat
        elif name == "h":
            value = self.h
        elif name == "s":
            value = self.s
        elif name == "d":
            value = self.d
        elif name == "q":
            value = self.q
        elif name == "over":
            value = self.over
        else:
            value = "error"

        return value

    def __get__(self, name):
        print(name)
    # def __dict__(self):
    #     return "a"
    # use pt() to clac Props of the node

    def pt(self):
        ''' change default unit

        the coolprop default unit is Pa & K, but I Accustomed to use Bar & C
        '''
        self._h, self._s, self._d = PropsSI(
            ["H", "S", "D"], "P", self._p, "T", self._t, self.fluid
        )

        # assume that Q is equal to 0
        self._pSat = PropsSI("P", "Q", 0, "T", self._t, self.fluid)
        self._tSat = PropsSI("T", "Q", 0, "P", self._p, self.fluid)

        self._over = self.t - self.tSat

        if self._over <= 0:
            self._q = -1
        else:
            self._q = 2

    def pq(self):
        ''' change default unit

        the coolprop default unit is Pa & K, but I Accustomed to use Bar & C
        '''

        self._h, self._s, self._d, self._t = \
            PropsSI(["H", "S", "D", "T"], "P",
                    self._p, "Q", self._q, self.fluid)

        self._tSat = PropsSI("T", "P", self._p, "Q", 0.5, self.fluid)
        self._pSat = PropsSI("P", "T", self._t, "Q", 0.5, self.fluid)

        self._over = self.t - self.tSat

    def ps(self):
        ''' change default unit

        the coolprop default unit is Pa & K, but I Accustomed to use Bar & C
        '''

        self._t, self._h, self._d, self._q = PropsSI(
            ["T", "H", "D", "Q"], "P", self._p, "S", self._s, self.fluid
        )

        # assume that Q is equal to 0
        self._pSat = PropsSI("P", "Q", 0, "T", self._t, self.fluid)
        self._tSat = PropsSI("T", "Q", 0, "P", self._p, self.fluid)

        self.over = self.t - self.tSat
        if self._over <= 0:
            self._q = -1
        else:
            self._q = 2

    # set Props of P & T
    def set_tp(self, temperature, presspsure):
        self.p = presspsure
        self.t = temperature

    # print all of Props of the node
    def __str__(self):
        result = '{:^12}, {:^5}, {:^12.2f}, {:^12.2f}, {:^12.2f}, {:^12.2f}, {:^12.2f}, {:^12}, {:^12.2f}' \
            .format(self.name, self.nid, self.p, self.t, self.h, self.s, self.d, self.q, self._over)
        return result

    def __repr__(self):
        node_info = {
            "fluid": self.fluid,
            "name": self.name,
            "nodeID": self.nid,
            "pressure": self.p,
            "pressure(Sat)": self.pSat,
            "temperature": self.t,
            "temperature(Sat)": self.tSat,
            "enthalpy(h)": self.h,
            "entropy(s)": self.s,
            "density": self.d,
            "quality": self.q,
            "over": self._over
        }

        return dumps(node_info, indent=4)
