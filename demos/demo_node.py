#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 23:01:09 2021

@author: wei
"""

# import sys
# sys.path.append('../')


#    # use Bar, C, KJ/Kg, ((KJ/Kg) * K), (Kg/m^3) to output Props list
#    def statusProps(self):
#        return [self.p, self.t, self.h/1000, self.s/1000, self.d, self.q, self.over]
if __name__ == '__main__':
    from thermo.node import Node
    from CoolProp.CoolProp import PropsSI
    # 配合課本或 NIST檢查
    # 20 KPa, 800C 查表得 v = 2.475 m^3/kg, h = 4159.2 KJ/kg, s = 9.2460 (KJ/kg)*K
    print("---test node---")
    node1 = Node(nid=1, fluid="Water")
    node1.p = 1.01325
    node1.t = 120
    node1.pt()
    print(node1)

    node2 = Node(nid=2, fluid="Water")
    node2.p = 1.01325
    node2.q = 0.5
    node2.pq()
    print(node2)

    # test PropsSI
    print("---test PropsSI---")
    print(PropsSI('T', 'P', 1.01325 * 1e5, 'Q', 0, 'Water') - 273)
    print(PropsSI('P', 'T', [25+273, 25+273], 'Q', [0, 1], "R245FA") / 1e5)
    print(PropsSI(
        ['H', 'S', 'D'],
        'P', [1.01325 * 1e5, 1.01325 * 1e5],
        'T', [20+273, 50+273],
        'Water')/1000)
