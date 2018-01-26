#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Real system
 
 the diagram of our ORC as

    ┌─── Node 1 ─── Evaparator ─── Node 2 ──┐
    │                                       │ 
    │                                       │ 
    │                                    Node 3
    │                                       │
    │                                       │
  Pump                                   Expander  
    │                                       │
    │                                       │
 Node 0                                  Node 4
    │                                       │ 
    │                                       │
    └─── Node 6 ───  Condenser ─── Node 5 ──┘  

 each on status of point as
 
	      Node 0	   Node 1	   Node 2 	Node 3  	Node 4 	 Node 5 	Node 6
	      pump in	pump out	HX out	   EVP in	   EVP out	 CDS in	   CDS out
T (C)	   21.86	   22.55	   88.31   88.28	    64.03	  59.68	   22.12
P (bar)	   2.01	       6.44	   6.11	    6.27	   2.05	     1.99	   1.98
 
 we can use the CoolProp & REFPROP to find the status of point,
 just for use with node.py

 @ author: wei
 @ e-mail: t104306033@ntut.org.tw
"""
    
if __name__ == '__main__':
    import node
    from tabulate import tabulate
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
    table = []
    for nodei in [nodes[i] for i in range(7)]:
        table.append([nodei.nid, nodei.name, nodei.p, round(nodei.t, 3), round(nodei.h/1000, 3), 
                  round(nodei.s/1000, 4), round(nodei.d, 3), nodei.q])
    headers=['nodeID', 'name', 'p (bar)', 't (c)','h (KJ/Kg)', 's ((KJ/Kg) * K)', 'd (Kg/m^3)', 'q']
    print(tabulate(table, headers))

        
    
        




