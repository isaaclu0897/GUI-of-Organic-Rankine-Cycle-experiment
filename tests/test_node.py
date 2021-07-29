#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 23:26:54 2021

@author: wei
"""

import unittest
from thermo.node import Node


class NodeTestCase(unittest.TestCase):
    ''' online steam table
    https://www.steamtablesonline.com/steam97web.aspx

    coolprop default use IF95, so I change the fluid
    http://www.coolprop.org/fluid_properties/IF97.html
    '''

    def setUp(self):
        self.node = Node()
        self.node.fluid = "IF97::Water"
        self.node.p = 1.01325   # 1.atm = 1.01325 bar
        self.node.t = 25        # 25 c
        self.node.pt()

    def test_node_enthalpy(self):
        self.assertAlmostEqual(self.node.h, 104.9292946426, 4)

    def test_node_entropy(self):
        self.assertAlmostEqual(self.node.s, 0.3672310160, 4)
