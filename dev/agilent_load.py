#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  8 19:31:54 2018

@author: wei
"""

from random import randint
import pyvisa as visa  # you need agilent io lib
# import config as cfg
from db._config import SENSOR, SENSOR_SETTING, v34972A
from db._realtime import shell


class V34972A:
    def __init__(self):
        rm = visa.ResourceManager()
        self.device = rm.open_resource(v34972A["USB_address"])

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


class test_device:
    def __init__(self):
        pass

    def query(self, query):
        value = "0"
        query = query.split(",")[-1]

        # print(query)
        if query == "(@101)":
            value = "23.1800"
        elif query == "(@102)":
            value = "24.8940"
        elif query == "(@103)":
            value = "80.3100"
            value = randint(80, 90)
        elif query == "(@104)":
            value = "70.0300"
        elif query == "(@105)":
            value = "62.5000"
            value = randint(58, 65)
        elif query == "(@106)":
            value = "22.5000"
        elif query == "(@107)":
            value = "100.5000"
        elif query == "(@108)":
            value = "90.5000"
        elif query == "(@109)":
            value = "22.5000"
        elif query == "(@110)":
            value = "24.5000"
        elif query == "(@201)":
            value = "2.07000"
        elif query == "(@202)":
            value = "5.03000"
        elif query == "(@203)":
            value = "4.96000"
        elif query == "(@204)":
            value = "2.03000"
        elif query == "(@205)":
            value = "2.03000"
        elif query == "(@206)":
            value = "1.97000"
        elif query == "(@301)":
            value = "2.5"
        return value

    def write(self, query):
        pass


class test_V34972A:

    def __init__(self):
        self.device = test_device()

    def scan(self):
        # print("scan_data")
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
            elif sensor_type in ["Ti", "To"]:
                
                if "setting" in items:
                    t_probe = items["setting"][0]
                    t_type = items["setting"][1]
                query = ':MEASure:TEMPerature? %s,%s,(%s)' % (
                    t_probe, t_type, ch)
                t = self.device.query(query)
                shell[f"{name}_{sensor_type}"] = float(t)
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
                p = self.device.query(query)
                # p = self.device.query(':READ?')
                shell[f"{name}"].p = float(p)
            else:
                v = self.device.query(f':READ?,({ch})')
                shell[f"{name}"] = float(v)
        return shell


if __name__ == "__main__":
    # rm = visa.ResourceManager()
    # usb_device = rm.open_resource('USB0::0x0957::0x2007::MY49017447::0::INSTR')
    # temps = usb_device.query(
    #     ':MEASure:TEMPerature? %s,%s,(%s)' % ('TCouple', 'T', "@101:110"))
    # usb_device.write(':CONFigure:VOLTage:DC %G,%G,(%s)' %
    #                  (10, 5.5, "@201:206"))
    # usb_device.write(':CALCulate:SCALe:GAIN %G,(%s)' % (2.1, "@201:206"))
    # usb_device.write(':CALCulate:SCALe:STATe %d,(%s)' % (1, "@201:206"))
    # pressS = usb_device.query(':READ?')
    # rm.close()

    # print(temps)
    # print(pressS)

    # device = V34972A()
    # device.scan()
    # print(data)

    device = test_V34972A()
    device.scan()
    print(shell)
