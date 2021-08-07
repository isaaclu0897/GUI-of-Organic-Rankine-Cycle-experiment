#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  8 19:31:54 2018

@author: wei
"""

import pyvisa  # you need agilent io lib
from db._config import SENSOR, SENSOR_SETTING, device
from db._realtime import shell


class V34972A:
    def __init__(self):
        rm = pyvisa.ResourceManager()
        self.device = rm.open_resource(device["address"])

    def scan(self):
        for ch, items in SENSOR.items():
            name = items["name"]
            sensor_type = items["type"]

            t_probe = SENSOR_SETTING["probe_type"]
            t_type = SENSOR_SETTING["type"]
            p_range = SENSOR_SETTING["range"]
            p_resolution = SENSOR_SETTING["resolution"]
            p_gain = SENSOR_SETTING["gain"]
            p_offset = SENSOR_SETTING["offset"]

            if "T" == sensor_type:
                if "setting" in items:
                    t_probe = items["setting"][0]
                    t_type = items["setting"][1]
                query = ':MEASure:TEMPerature? %s,%s,(%s)' % (
                    t_probe, t_type, ch)
                t = self.device.query(query)
                shell[f"{name}"].t = float(t)
            elif "P" == sensor_type:
                if "setting" in items:
                    p_range = items["setting"][0]
                    p_resolution = items["setting"][1]
                    p_gain = items["setting"][2]
                    p_offset = items["setting"][3]
                query = ':CONFigure:VOLTage:DC %G,%G,(%s)' % (
                    p_range, p_resolution, ch)
                self.device.write(query)
                query = ':CALCulate:SCALe:GAIN %G,(%s)' % (p_gain, ch)
                self.device.write(query)
                query = ':CALCulate:SCALe:STATe %d,(%s)' % (p_offset, ch)
                self.device.write(query)
                p = self.device.query(':READ?')
                shell[f"{name}"].p = float(p)
            elif sensor_type in ["Ti", "To"]:
                if "setting" in items:
                    t_probe = items["setting"][0]
                    t_type = items["setting"][1]
                query = ':MEASure:TEMPerature? %s,%s,(%s)' % (
                    t_probe, t_type, ch)
                t = self.device.query(query)
                shell[f"{name}_{sensor_type}"] = float(t)
            else:
                print(f"sensor {name} config error")

    ''' maybe need close? __del__'''
