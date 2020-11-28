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


data = {}


class V34972A:
    # probe_type_TEMP, type_TEMP, ch_TEMP = 'TCouple', 'T', '@201:210'
    # range_PRESS, resolution_PRESS, ch_PRESS = 10, 5.5, '@301:306'
    # gain_PRESS, state_PRESS = 2.1, 1

    def __init__(self):
        rm = visa.ResourceManager()
        self.device = rm.open_resource(cfg.v34972A["USB_address"])

    def scan(self):
        for k, ch in cfg.SENSOR.items():
            name, sensor_type = k.split("_")
            if name not in nodes:
                nodes[f"{name}"] = node.Node()

            if "T" in sensor_type:
                query = ':MEASure:TEMPerature? %s,%s,(%s)' % (
                    'TCouple', 'T', ch)
                t = self.device.query(query)
                nodes[f"{name}"].t = float(t)
            elif "P" in sensor_type:
                query = ':CONFigure:VOLTage:DC %G,%G,(%s)' % (10, 5.5, ch)
                self.device.write(query)
                query = ':CALCulate:SCALe:GAIN %G,(%s)' % (2.1, ch)
                self.device.write(query)
                query = ':CALCulate:SCALe:STATe %d,(%s)' % (1, ch)
                self.device.write(query)
                p = self.device.query(':READ?')
                nodes[f"{name}"].p = float(p)
            else:
                pass


class test_device:
    def __init__(self):
        pass
    def query(self, query):
        value = "0"
        query = query.split(",")[-1]
        if query == "(@101)":
            value = "25.5000"
        elif query == "(@102)":
            value = "26.5000"
        elif query == "(@103)":
            value = "80.5000"
        elif query == "(@104)":
            value = "65.5000"
        elif query == "(@105)":
            value = "100.5000"
        elif query == "(@106)":
            value = "81.5000"
        elif query == "(@107)":
            value = "25.5000"
        elif query == "(@108)":
            value = "31.5000"
        
        return value
    def write(self, query):
        pass

class test_V34972A:
    # probe_type_TEMP, type_TEMP, ch_TEMP = 'TCouple', 'T', '@201:210'
    # range_PRESS, resolution_PRESS, ch_PRESS = 10, 5.5, '@301:306'
    # gain_PRESS, state_PRESS = 2.1, 1

    def __init__(self):
        pass
        # rm = visa.ResourceManager()
        self.device = test_device()

    def scan(self):
        for k, ch in cfg.SENSOR.items():
            name =  k.split("_")[0]
            sensor_type = k.split("_")[-1]
            if name not in nodes:
                nodes[f"{name}"] = node.Node()

            if "T" in sensor_type:
                query = ':MEASure:TEMPerature? %s,%s,(%s)' % (
                    'TCouple', 'T', ch)
                print(query)
                t = self.device.query(query)
                nodes[f"{name}"].t = float(t)
            elif "P" in sensor_type:
                query = ':CONFigure:VOLTage:DC %G,%G,(%s)' % (10, 5.5, ch)
                self.device.write(query)
                query = ':CALCulate:SCALe:GAIN %G,(%s)' % (2.1, ch)
                self.device.write(query)
                query = ':CALCulate:SCALe:STATe %d,(%s)' % (1, ch)
                self.device.write(query)
                p = self.device.query(':READ?')
                nodes[f"{name}"].p = float(p)
            else:
                pass


if __name__ == "__main__":
    # scan()
    dev = test_V34972A()
    dev.scan()
    # print(nodes)
