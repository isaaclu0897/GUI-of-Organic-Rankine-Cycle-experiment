#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 23:56:45 2018

@author: wei
"""

from tabulate import tabulate
from ORC_sample import data

def ORC_status(objlist, headers=['nodeID', 'name', 'p (bar)', 't (c)', 'h (KJ/Kg)',
                                 's ((KJ/Kg)*K)', 'd (Kg/m^3)', 'q', 'over']):
    table = []
    for nodei in objlist:
        table.append([nodei.name, nodei.nid, nodei.p, round(nodei.t, 3), round(nodei.h, 3),\
                      round(nodei.s, 4), round(nodei.d, 2), nodei.q, round(nodei.over, 1)])
    
    print(tabulate(table, headers))
    
if __name__ == '__main__':
    import node
    
    # define the  of all point
    dev_list = [pumpi, pumpo, EVPo, EXPi, EXPo, CDSi, CDSo] = data()
    
    # init all node
    nodes = []
    for i in dev_list:
        nodes.append(node.Node(i['name'], i['nid']))
    
    # set & calc Prop of point 
    for i, obj in enumerate(dev_list):
        nodes[i].set_tp(obj['T'], obj['P'])
        nodes[i].pt()

    # print pretty ORC_status table
    ORC_status([nodes[i] for i in range(7)])        # method 1
    ORC_status([nodes[0], nodes[2], nodes[5]])      # method 2
     
