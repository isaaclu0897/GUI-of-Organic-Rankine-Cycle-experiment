#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  8 19:31:54 2018
 
@author: wei
"""

import visa  # you need agilent io lib
import node
from tabulate_text import ORC_status
import config as cfg

# =============================================================================
# load the data
# =============================================================================


def scan():
    probe_type_TEMP, type_TEMP, ch_TEMP = 'TCouple', 'T', '@201:210'
    range_PRESS, resolution_PRESS, ch_PRESS = 10, 5.5, '@301:306'
    gain_PRESS, state_PRESS = 2.1, 1

    pumpi = {'name': 'pump_inlet',         'nid': 1}
    pumpo = {'name': 'pump_ioutlet',       'nid': 2}
    EXPi = {'name': 'expander_inlet',     'nid': 3}
    EXPo = {'name': 'expander_outlet',    'nid': 4}

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
        scans_TEMP = v34972A.query(':MEASure:TEMPerature? %s,%s,(%s)' % (
            probe_type_TEMP, type_TEMP, ch_TEMP))

        # scan pressure
        v34972A.write(':CONFigure:VOLTage:DC %G,%G,(%s)' %
                      (range_PRESS, resolution_PRESS, ch_PRESS))
        v34972A.write(':CALCulate:SCALe:GAIN %G,(%s)' % (gain_PRESS, ch_PRESS))
        v34972A.write(':CALCulate:SCALe:STATe %d,(%s)' %
                      (state_PRESS, ch_PRESS))
        scans_PRESS = v34972A.query(':READ?')

        # convert str to float
        global readings_TEMP
        global readings_PRESS
        readings_TEMP = [float(x) for x in scans_TEMP.split(',')]
        readings_PRESS = [float(x) for x in scans_PRESS.split(',')]
        calc(readings_TEMP, readings_PRESS)
#     timer(innerfunc, 3)

#    rm.close()

nodes = {}

class V34972A:
    probe_type_TEMP, type_TEMP, ch_TEMP = 'TCouple', 'T', '@201:210'
    range_PRESS, resolution_PRESS, ch_PRESS = 10, 5.5, '@301:306'
    gain_PRESS, state_PRESS = 2.1, 1

    def __init__(self):
        rm = visa.ResourceManager()
        self.device = rm.open_resource(cfg.v34972A["USB_address"])
        

    def scan(self):
        self.device.query(':MEASure:TEMPerature? %s,%s,(%s)' % (
            self.probe_type_TEMP, self.type_TEMP, self.ch_TEMP))

        self.device.write(':CONFigure:VOLTage:DC %G,%G,(%s)' % (
            self.range_PRESS, self.resolution_PRESS, self.ch_PRESS))
        self.device.write(':CALCulate:SCALe:GAIN %G,(%s)' %
                          (self.gain_PRESS, self.ch_PRESS))
        self.device.write(':CALCulate:SCALe:STATe %d,(%s)' %
                          (self.state_PRESS, self.ch_PRESS))


if __name__ == "__main__":
    # scan()
    pass
