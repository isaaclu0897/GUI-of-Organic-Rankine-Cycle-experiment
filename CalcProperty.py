#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 16:35:38 2018

@author: wei
"""

from node import Node

def calcm(mdot, Hi, Ho, T1, P1, T2, P2):
    inlet = Node()
    outlet = Node()
    inlet.set_tp(T1, P1); inlet.pt()
    outlet.set_tp(T2, P2); outlet.pt()
    return mdot*4.2*(Hi-Ho) / (outlet.h - inlet.h)

def calcw(mdot, T1, P1, T2, P2):
    inlet = Node()
    outlet = Node()
    inlet.set_tp(T1, P1); inlet.pt()
    outlet.set_tp(T2, P2); outlet.pt()
    return mdot*(inlet.h-outlet.h)
    