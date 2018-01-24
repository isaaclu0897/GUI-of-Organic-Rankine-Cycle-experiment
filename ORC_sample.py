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
#    明天來做texttacle 跟單位換算界面
    import node
#    from unit import P, T
    
    # define the status of all point
    
    pumpi_P = 2.01
    pumpi_T = 21.86
    
    pumpo_P = 6.44
    pumpo_T = 22.55
    
    HXo_P = 6.11
    HXo_T = 88.31
    
    EVPi_P = 6.27
    EVPi_T = 88.28
    
    EVPo_P = 2.05
    EVPo_T = 64.03
    
    CDSi_P = 1.99
    CDSi_T = 59.68
    
    CDSo_P = 1.98
    CDSo_T = 22.12
    '''
    pumpi_P = P.Bar2Pa(2.01)
    pumpi_T = T.C2K(21.86)
    
    pumpo_P = P.Bar2Pa(6.44)
    pumpo_T = T.C2K(22.55)
    
    HXo_P = P.Bar2Pa(6.11)
    HXo_T = T.C2K(88.31)
    
    EVPi_P = P.Bar2Pa(6.27)
    EVPi_T = T.C2K(88.28)
    
    EVPo_P = P.Bar2Pa(2.05)
    EVPo_T = T.C2K(64.03)
    
    CDSi_P = P.Bar2Pa(1.99)
    CDSi_T = T.C2K(59.68)
    
    CDSo_P = P.Bar2Pa(1.98)
    CDSo_T = T.C2K(22.12)
    '''
        
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
    
    for i in range(7):
        nodes[i].pt()
        nodes[i].show_ORCProps()
        
        
    
        




