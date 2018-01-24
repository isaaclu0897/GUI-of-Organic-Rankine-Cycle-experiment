#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 23:56:45 2018

@author: wei
"""

from tabulate import tabulate
if __name__ == '__main__':
#    明天來做texttacle 跟單位換算界面
    import node
#    from unit import P, T
    
    # define the status of all point
    
    pumpi_P, pumpi_T = 2.01, 21.86
    pumpo_P, pumpo_T = 6.44, 22.55
    HXo_P, HXo_T = 6.11, 88.31
    EVPi_P, EVPi_T = 6.27, 88.28
    EVPo_P, EVPo_T = 2.05, 64.03
    CDSi_P, CDSi_T  = 1.99, 59.68
    CDSo_P, CDSo_T = 1.98, 22.12
        
    # init all node
    nodes = []
    for i in range(7):
        nodes.append(node.Node())
    
    nodes[0].set_tp(pumpi_P, pumpi_T)
    nodes[1].set_tp(pumpo_T, pumpo_P)
    nodes[2].set_tp(HXo_T, HXo_P)
    nodes[3].set_tp(EVPi_T, EVPi_P)
    nodes[4].set_tp(EVPo_T, EVPo_P)
    nodes[5].set_tp(CDSi_T, CDSi_P)
    nodes[6].set_tp(CDSo_T, CDSo_P)
    
    table = []
    for i in range(7):
        nodes[i].pt()
#        nodes[i].show_ORCProps()
        table.append([nodes[i].p, round(nodes[i].t, 3), round(nodes[i].h/1000, 3), 
                      round(nodes[i].s/1000, 4), round(nodes[i].d, 3), nodes[i].q])
    headers=['node', 'p (bar)', 't (c)', 'h (KJ/Kg)',  's ((KJ/Kg) * K)', 'd (Kg/m^3)', 'q']
    print(tabulate(table, headers, showindex='always'))
        
    
