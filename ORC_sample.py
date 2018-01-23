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
def Bar2Pa(P):
    return P * 1e5

def C2K(T):
    return T + 273.15
    
if __name__ == '__main__':
    import node
    
    # define the status of all point
    pumpi_P = Bar2Pa(2.01)
    pumpi_T = C2K(21.86)
    
    pumpo_P = Bar2Pa(6.44)
    pumpo_T = C2K(22.55)
    
    HXo_P = Bar2Pa(6.11)
    HXo_T = C2K(88.31)
    
    EVPi_P = Bar2Pa(6.27)
    EVPi_T = C2K(88.28)
    
    EVPo_P = Bar2Pa(2.05)
    EVPo_T = C2K(64.03)
    
    CDSi_P = Bar2Pa(1.99)
    CDSi_T = C2K(59.68)
    
    CDSo_P = Bar2Pa(1.98)
    CDSo_T = C2K(22.12)
        
    # init all node
    nodes = []
    for i in range(7):
        nodes.append(node.Node())
    
    nodes[0].p = pumpi_P
    nodes[0].t = pumpi_T
    nodes[1].p = pumpo_P
    nodes[1].t = pumpi_T
    nodes[2].p = HXo_P
    nodes[2].t = HXo_T
    nodes[3].p = EVPi_P
    nodes[3].t = EVPi_T
    nodes[4].p = EVPo_P
    nodes[4].t = EVPo_T
    nodes[5].p = CDSi_P
    nodes[5].t = CDSi_T
    nodes[6].p = CDSo_P
    nodes[6].t = CDSo_T
    
    for i in range(7):
        nodes[i].pt()
        msg = nodes[i].__str__()
        print(' {:^16}, {:^16}, {:^16}, {:^16}, {:^16}, {:^16}\n' \
              .format('p (Pa)', 't (K)', 'h (J/Kg)',  's ((J/Kg) * K)', 'd (Kg/m^3)', 'q'), msg)
        print()




