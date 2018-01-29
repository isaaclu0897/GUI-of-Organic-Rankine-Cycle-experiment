#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 00:07:47 2018

@author: wei
"""

import csv
from node import Node
from tabulate_text import ORC_status
import time
import matplotlib.pyplot as plt 
from CoolProp.CoolProp import PropsSI 
import numpy as np
from ORC_plot import ProcessPlot


filename = 'Data 8199 2391 1_9_2018 08_48_19.csv'
#with open(filename, 'r') as f:
with open(filename, 'r', newline='', encoding='utf-16') as f:
    
    reader = csv.reader(f, delimiter=',')
    table = []
    for row in reader:
        table.append(row)
#    for i in range(50):
#        print(table[i])

    
    for i in range(50):
#        print(table[i][0])
        if table[i][0] == 'Scan':
#            print(table[i][0])
            x = i
#    print(x)
    header_index = table[x]
#    print(header_index)
    
    table_new = []
#    for x in range(x, reader.line_num - 1): 
    for x in range(260, 500):
        table_new.append(table[x + 1])
    
    dev_list = ['<pump inlet>', '<pump outlet>', '<HX outlet>', '<expander inlet>'
                , '<expander outlet>', '<condenser inlet>' , '<condenser outlet>']
    for indexe, i in enumerate(table_new):
        print(indexe)
        pumpi = {'name' : 'pump_inlet',
#                 'nid' : 1,
                 'P' : i[24],
                 'T' : i[2]}
        pumpo = {'name' : 'pump_ioutlet',
#                 'nid' : 2,
                 'P' : i[26],
                 'T' : i[4]}
        EVPo = {'name' : 'evaparator_outlet',
#                'nid' : 3,
                'P' : i[28],
                'T' : i[6]}
        EXPi = {'name' : 'expander_inlet',
#                'nid' : 4,
                'P' : i[30],
                'T' : i[8]}
        EXPo = {'name' : 'expander_outlet',
#                'nid' : 5,
                'P' : i[32],
                'T' : i[10]}
        CDSi = {'name' : 'condenser_inlet',
#                'nid' : 6,
                'P' : i[34],
                'T' : i[12]}
        CDSo = {'name' : 'condenser_outlet',
#                'nid' : 7,
                'P' : i[36],
                'T' : i[14]}
        dev_list = [pumpi, pumpo, EVPo, EXPi, EXPo, CDSi, CDSo]
        nodes = []
        for index, j in enumerate(dev_list):
#            print(index, j)
            nodes.append(Node(j['name'], index))
        for index, j in enumerate(dev_list):
            nodes[index].set_tp(float(j['T']), float(j['P']))
            nodes[index].pt()
        ORC_status([nodes[a] for a in range(7)])
#        time.sleep(1e-10)
        
        # set label 
        plt.clf()
        xAxis = "s" 
        yAxis = "T" 
        title = {"T": "T, °C", "s": "s, kJ/kgK"} 
        plt.title("%s-%s Diagram" % (yAxis, xAxis)) 
        plt.xlabel(title[xAxis]) 
        plt.ylabel(title[yAxis]) 
        plt.ylim(0, 125)
        plt.xlim(0.8, 2)
        plt.grid()
        

#        time.sleep(5)
        
        tcrit = PropsSI('Tcrit', 'REFPROP::R245FA') - 0.00007 
        tmin = PropsSI('Tmin', 'REFPROP::R245FA') 
        Ti = np.linspace(tmin, tcrit, 50)
#        time.sleep(0.5)
        
        t = [] 
        s = [] 
        for i in range(7): 
            t.append(nodes[i].t) 
            s.append(nodes[i].s / 1000)
        
        for x in np.array([0, 1.0]): 
            S = np.array([PropsSI("S", "Q", x, "T", t, 'REFPROP::R245FA') for t in Ti]) 
            plt.plot(S / 1000, Ti - 273.15, 'r', lw=2.0) 
#            plt.pause(0.05)
#        plt.pause(0.00000000000005)

        plt.plot(s, t, 'o')
#        plt.pause(0.05) 
    
        plot1 = ProcessPlot(0, 1, 'isos')
        plot1.iso_line(nodes)
        plot1.calc_iso()
        plot1.plot_iso()      
        
        plot1 = ProcessPlot(1, 2, 'isop')
        plot1.iso_line(nodes)
        plot1.calc_iso()
        plot1.plot_iso()
        
        plot1 = ProcessPlot(2, 3, 'isop')
        plot1.iso_line(nodes)
        plot1.calc_iso()
        plot1.plot_iso()
        
        plot1 = ProcessPlot(3, 4, 'isos')
        plot1.iso_line(nodes)
        plot1.calc_iso()
        plot1.plot_iso()  
        
        plot1 = ProcessPlot(4, 5, 'isop')
        plot1.iso_line(nodes)
        plot1.calc_iso()
        plot1.plot_iso()    
        
        plot1 = ProcessPlot(5, 6, 'isop')
        plot1.iso_line(nodes)
        plot1.calc_iso()
        plot1.plot_iso()
        
        plot1 = ProcessPlot(6, 0, 'isop')
        plot1.iso_line(nodes)
        plot1.calc_iso()
        plot1.plot_iso()   
        plt.pause(0.00005)
        

        #        [nodes[k] for k in range(7)]
#        print(i)
    
    
#    table_new.reverse()
#    for i in table_new:
#        print(i)
    

#    reader = csv.DictReader(f)
#    table = []
#    for row in reader:
#        table.append(row)
#        print(row.values())
        
#    for i in range(150):
#        print(table[i])
        
    