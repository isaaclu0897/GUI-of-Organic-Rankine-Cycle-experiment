#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 23:56:45 2018

@author: wei
"""

from tabulate import tabulate

def ORC_status(objlist, headers=['nodeID', 'name', 'p (bar)', 't (c)', 'h (KJ/Kg)', \
                                 's ((KJ/Kg) * K)', 'd (Kg/m^3)', 'q']):
    table = []
    for nodei in objlist:
        table.append([nodei.nid, nodei.name, nodei.p, round(nodei.t, 3),  \
                      round(nodei.h/1000, 3), round(nodei.s/1000, 4), round(nodei.d, 3), nodei.q])
    
    print(tabulate(table, headers))
    
if __name__ == '__main__':
    import node
    
    # define the  of all point
    pumpi = {'name' : 'pump_inlet',
             'nid' : 1,
             'P' : 2.01,
             'T' : 21.86}
    pumpo = {'name' : 'pump_ioutlet',
             'nid' : 2,
             'P' : 6.44,
             'T' : 22.55}
    EVPo = {'name' : 'evaparator_outlet',
            'nid' : 3,
            'P' : 6.11,
            'T' : 8.31}
    EXPi = {'name' : 'expander_inlet',
            'nid' : 4,
            'P' : 6.27,
            'T' : 8.28}
    EXPo = {'name' : 'expander_outlet',
            'nid' : 5,
            'P' : 2.05,
            'T' : 64.03}
    CDSi = {'name' : 'condenser_inlet',
            'nid' : 6,
            'P' : 1.99,
            'T' : 56.68}
    CDSo = {'name' : 'condenser_outlet',
            'nid' : 7,
            'P' : 1.98,
            'T' : 22.12}
    
    dev_list = [pumpi, pumpo, EVPo, EXPi, EXPo, CDSi, CDSo]
    
    # init all node
    nodes = []
    for i in dev_list:
        nodes.append(node.Node(i['name'], i['nid']))
#        print(i)
    
    # set & calc Prop of point 
    for i, obj in enumerate(dev_list):
        nodes[i].set_tp(obj['T'], obj['P'])
        nodes[i].pt()
   
#    for i in range(7):
#        print(nodes[i])

    # print pretty ORC_status table
    ORC_status([nodes[i] for i in range(7)])        # method 1
    ORC_status([nodes[0], nodes[2], nodes[5]])      # method 2
    
 
