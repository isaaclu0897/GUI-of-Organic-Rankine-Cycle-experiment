#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 23:56:45 2018

@author: wei
"""

from tabulate import tabulate

def ORC_status(objlist, headers=['node', 'p (bar)', 't (c)','h (KJ/Kg)',\
                                 's ((KJ/Kg) * K)', 'd (Kg/m^3)', 'q']):
    table = []
    for nodei in objlist:
        table.append([nodei.p, round(nodei.t, 3), round(nodei.h/1000, 3), 
                  round(nodei.s/1000, 4), round(nodei.d, 3), nodei.q])
    
    print(tabulate(table, headers, showindex='always'))
    
if __name__ == '__main__':
    import node

    # init all node
    nodes = []
    for i in range(7):
        nodes.append(node.Node())
    
    nodes[0].set_tp(2.01, 21.86)
    nodes[1].set_tp(6.44, 22.55)
    nodes[2].set_tp(6.11, 88.31)
    nodes[3].set_tp(6.27, 88.28)
    nodes[4].set_tp(2.05, 64.03)
    nodes[5].set_tp(1.99, 59.68)
    nodes[6].set_tp(1.98, 22.12)

    for i in range(7):
        nodes[i].pt()    
    
    table = []
    for nodei in [nodes[i] for i in range(7)]:
        table.append([nodei.p, round(nodei.t, 3), round(nodei.h/1000, 3), 
                  round(nodei.s/1000, 4), round(nodei.d, 3), nodei.q])
    headers=['node', 'p (bar)', 't (c)','h (KJ/Kg)', 's ((KJ/Kg) * K)', 'd (Kg/m^3)', 'q']
    print(tabulate(table, headers, showindex='always'))
    
 
