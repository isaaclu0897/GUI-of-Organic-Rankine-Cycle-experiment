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

data = [("IF97::Water", 25, 1.01325), ("IF97::Water", 25, 1.01325),
        ("IF97::Water", 30, 1.01325), ("IF97::Water", 30, 1.01325)]

@pytest.mark.parametrize("fluid, t, p", data)
def test_node_pt(fluid, t, p):
    print(fluid, t, p)
    node = Node()
    node.fluid = fluid
    node.t = t
    node.p = p
    node.pt()
    assert_almost_equal(node.h, 104.9292946426, 10)
    


# @pytest.fixture(
#     scope="class",
#     params=params,
# )
# def n(request):
#     print('setup once per each param', request.param)
#     return request.param


# class NodeTestCase(unittest.TestCase):
#     ''' online steam table
#     https://www.steamtablesonline.com/steam97web.aspx

#     coolprop default use IF95, so I change the fluid
#     http://www.coolprop.org/fluid_properties/IF97.html
#     '''
#     # must be test water r245fa
#     def setUp(self):
#         print(1)
#     #     self.node = Node()
#     #     self.node.fluid = "IF97::Water"
#     #     print(self.node.s, self.node.h)
#     #     self.node.p = 1.01325   # 1.atm = 1.01325 bar
#     #     self.node.t = 25        # 25 c
#     #     self.node.pt()
#     def tearDown(self):
#         print(2)

#     def test_node_enthalpy(self, n):
#         print(3, "a=", n)
#         pass
#         # self.assertAlmostEqual(self.node.h, 104.9292946426, 10)
#         # self.assertAlmostEqual(self.node.h, 104.9292946426, 20)

#     def test_node_entropy(self):
#         print(4)
#         pass
#         # self.assertAlmostEqual(self.node.s, 0.3672310160, 10)
#         # self.assertAlmostEqual(self.node.s, 0.3672310160, 10)
#     # @pytest.mark.parametrize("a", [1, 2, 3, 4])
