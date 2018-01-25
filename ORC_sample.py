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
    └─── Node 0 ───  Condenser ─── Node 5 ──┘  

 each on status of point as
 
	      Node 0	   Node 1	   Node 2 	Node 3  	Node 4 	Node 5 	Node 6
	      pump in	pump out	HX out	   EVP in	   EVP out	CDS in	   CDS out
T (C)	   21.86	   22.55	   88.31	   88.28	   64.03	   59.68	   22.12
P (bar)	2.01	   6.44	   6.11	   6.27	   2.05	   1.99	   1.98
 
 we can use the CoolProp & REFPROP to find the status of point,
 just for use with node.py

 @ author: wei
 @ e-mail: t104306033@ntut.org.tw
"""
    
if __name__ == '__main__':
    import node
    import tabulate_text
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
    
    nodes[0].set_tp(pumpi_T, pumpi_P)
    nodes[1].set_tp(pumpo_T, pumpo_P)
    nodes[2].set_tp(HXo_T, HXo_P)
    nodes[3].set_tp(EVPi_T, EVPi_P)
    nodes[4].set_tp(EVPo_T, EVPo_P)
    nodes[5].set_tp(CDSi_T, CDSi_P)
    nodes[6].set_tp(CDSo_T, CDSo_P)
    
    # calc the Props of point
    for i in range(7):
        nodes[i].pt() 
    
    # print pretty ORC_status table
    tabulate_text.ORC_status([nodes[i] for i in range(7)])
        
        
    
        




