#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 07:24:12 2018

@author: wei
"""

class P():
    
    def Pa2Bar(p):
        return p / 1e5
    
    def Pa2KPa(P):
        return P / 1e3
    
    
    def Bar2Pa(P):
        return P * 1e5
    
    def KPa2Pa(P):
        return P * 1e3

class T():
    
    def C2K(T):
        return T + 273.15

    
    def K2C(T):
        return T - 273.15