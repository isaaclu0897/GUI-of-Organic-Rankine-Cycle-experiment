#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 23:26:54 2021

@author: wei
"""

# import unittest
# from unittest import TestCase
from numpy.testing import assert_almost_equal
# import unittest
# assertions = unittest.TestCase('__init__')
from thermo.node import Node
import pytest


''' online steam table
https://www.steamtablesonline.com/steam97web.aspx

coolprop default use IF95, so I change the fluid
http://www.coolprop.org/fluid_properties/IF97.html
'''

data = [
    (dict(fluid="IF97::Water", t=25, p=1.01325),  # 1.atm = 1.01325 bar, 25 c
     dict(h=104.9292946426, s=0.3672310160))
]


@pytest.mark.parametrize("n, e", data)
def test_node_pt(n, e):
    # print(n, e)
    node = Node()
    node.fluid = n["fluid"]
    node.t = n["t"]
    node.p = n["p"]
    node.pt()
    assert_almost_equal(node.h, e["h"], 10)
    assert_almost_equal(node.s, e["s"], 10)


