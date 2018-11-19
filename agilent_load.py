#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  8 19:31:54 2018
 
@author: wei
"""
 
import visa
import node
from tabulate_text import ORC_status
from threading import Timer

# =============================================================================
# load the data
# =============================================================================

def timer(func, second=2, *arg):
    func(*arg)
    t = Timer(second, timer, args=(func, 3, *arg))
    t.setDaemon(True)
#    global readings_TEMP
#    global readings_PRESS
#    print(readings_TEMP, readings_PRESS)
    if t.daemon:
#        print('if')
        t.start()
    else:
#        print('else')
#        print(readings_TEMP, readings_PRESS)
#        del readings_TEMP, readings_PRESS
        return 0
    
def scan():
    probe_type_TEMP, type_TEMP, ch_TEMP = 'TCouple', 'T', '@201:210'
    range_PRESS,resolution_PRESS, ch_PRESS  = 10, 5.5, '@301:306'
    gain_PRESS, state_PRESS = 2.1, 1
    
    pumpi = {'name' : 'pump_inlet',         'nid' : 1}
    pumpo = {'name' : 'pump_ioutlet',       'nid' : 2}
    EXPi  = {'name' : 'expander_inlet',     'nid' : 3}
    EXPo  = {'name' : 'expander_outlet',    'nid' : 4}
    
#    offset_PRESS, label_PRESS = 0, 'BAR'
    rm = visa.ResourceManager()
    v34972A = rm.open_resource('USB0::0x0957::0x2007::MY49017447::0::INSTR')
#    idn_string = v34972A.query('*IDN?')
    def calc(readings_TEMP, readings_PRESS):
        global nodes
        dev_list = [pumpi, pumpo, EXPi, EXPo]
        for i in range(4):
            dev_list[i]['P'] = readings_PRESS[i]
            dev_list[i]['T'] = readings_TEMP[i]
        nodes = []
        for i in dev_list:
            nodes.append(node.Node(i['name'], i['nid']))
            
        for i, obj in enumerate(dev_list):
            nodes[i].set_tp(obj['T'], obj['P'])
            nodes[i].pt()
        
        ORC_status([nodes[i] for i in range(len(nodes))])

    def innerfunc():
        # scan temperature
        scans_TEMP = v34972A.query(':MEASure:TEMPerature? %s,%s,(%s)' % (probe_type_TEMP, type_TEMP, ch_TEMP))
        
        # scan pressure
        v34972A.write(':CONFigure:VOLTage:DC %G,%G,(%s)' % (range_PRESS,resolution_PRESS, ch_PRESS))
        v34972A.write(':CALCulate:SCALe:GAIN %G,(%s)' % (gain_PRESS, ch_PRESS))
        v34972A.write(':CALCulate:SCALe:STATe %d,(%s)' % (state_PRESS, ch_PRESS))
        scans_PRESS = v34972A.query(':READ?')
        
        # convert str to float
        global readings_TEMP
        global readings_PRESS
        readings_TEMP = [float(x) for x in scans_TEMP.split(',')]
        readings_PRESS = [float(x) for x in scans_PRESS.split(',')]
        calc(readings_TEMP, readings_PRESS)
    timer(innerfunc, 3)
            
#    rm.close()
        
if __name__=="__main__":
# =========================================================
# define the  of all point & init all node====================
# =============================================================================

    #CDSi  = {'name' : 'condenser_inlet',    'nid' : 5}
    #CDSo  = {'name' : 'condenser_outlet',   'nid' : 6}
    scan()
        









