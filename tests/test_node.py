#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 23:26:54 2021

@author: wei
"""

from numpy import testing
from thermo.node import Node
import pytest


''' online steam table
https://www.steamtablesonline.com/steam97web.aspx

coolprop default use IF95, so I change the fluid
http://www.coolprop.org/fluid_properties/IF97.html
'''

data = [
    (dict(fluid="IF97::Water", t=25, p=1.01325),  # 1.atm = 1.01325 bar, 25 c
     dict(d=997.0480319717, v=0.0010029607, h=104.9292946426, s=0.3672310160, q="subcool")),
    (dict(fluid="IF97::Water", t=120, p=1.01325),  # 1.atm = 1.01325 bar, 120 c
     dict(d=0.5651313042, v=0.0010029607, h=2716.4707336499, s=7.4612748541, q="superheat"))
]


@pytest.mark.parametrize("n, e", data)
def test_node_pt(n, e):
    # print(n, e)
    node = Node()
    node.fluid = n["fluid"]
    node.t = n["t"]
    node.p = n["p"]
    node.pt()
    # print(node.tSat, node.pSat)
    testing.assert_almost_equal(node.d, e["d"], 10)
    testing.assert_almost_equal(node.h, e["h"], 10)
    testing.assert_almost_equal(node.s, e["s"], 10)
    testing.assert_equal(node.q, e["q"])
