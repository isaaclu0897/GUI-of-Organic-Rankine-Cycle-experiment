#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  8 00:26:16 2021

@author: wei
"""

from tkinter import Frame, Canvas, font
from thermo.node import Node
from db._realtime import shell
import db._config as cfg

class PnID(Frame):
    offset_x = 50
    offset_y = 30

    def __init__(self, master=None):
        Frame.__init__(self, master=None)

        self.canvasID = {}

        ''' load img and create canvas '''
        self.photo = cfg.import_photo()
        self.canvas = Canvas(master,
                             width=self.photo.width(),
                             height=self.photo.height(),
                             bg='white')
        self.canvas.pack(expand=1, fill="both")
        ''' put gif image on canvas
        pic's upper left corner (NW) on the canvas is at x=50 y=10
        '''

        self.canvas.create_image(0, 0, image=self.photo, anchor="nw")

        ''''font'''
        self.fontprop = font.Font(
            size=cfg.GUI["fontsize"])  # bitstream charter or courier 10 pitch

        ''''set label'''
        self.set_Labels()

        # set label of efficiency
        fontTitle = font.Font(
            family='courier 10 pitch', size=30, weight='bold')
        self.canvas.create_text(200, 200, text="LAB429",
                                fill='green', font=fontTitle)
        # self.canvasID["{}_value".format(name)] = self.canvas.create_text(
        #     300, 350, text="None", fill='green', font=fontTitle)

    def create_text(self, x, y, t):
        return self.canvas.create_text(x, y, text=t, fill='blue', font=self.fontprop)

    def set_Labels(self):
        for k, v in cfg.LABEL.items():
            if v["posx"] == 0 or v["posy"] == 0:
                continue
            sensor_type = k.split("_")[-1]
            # default unit
            if "T" in sensor_type:
                unit = "C"
            elif "P" in sensor_type:
                unit = "B"
            elif sensor_type in ["Win", "Wout", "Qin", "Qout"]:
                unit = "kW"
            elif sensor_type in ["Eff", "Ein", "Eout"]:
                unit = "%"
            elif sensor_type in ["mDot"]:
                unit = "kg/s"
            else:
                unit = ""

            if unit in ["C", "B"]:
                self.create_text(v["posx"], v["posy"],
                                 f"{sensor_type:<7}{'':^5}{unit:>5}")
                self.canvasID[f"{k}"] = self.create_text(
                    v["posx"], v["posy"], f"{'None':^6}")
            else:
                self.create_text(v["posx"], v["posy"],
                                 f"{sensor_type:<5}{' '*20}{unit:>5}")
                self.canvasID[f"{k}"] = self.create_text(
                    v["posx"]+15, v["posy"], f"{'None'}")

    def update_value(self, name, text):
        itemID = self.canvasID[name]
        self.canvas.itemconfigure(itemID, text=text)

    def update(self):
        print("update P&ID")
        for name, value in shell.items():
            if isinstance(value, Node):
                self.update_value(f"{name}_T", round(shell[name].t, 1))
                self.update_value(f"{name}_P", round(shell[name].p, 1))
            elif isinstance(value, (int, float)):
                self.update_value(name, round(value, 1))
            else:
                try:
                    self.update_value(name, str(value).split(".")[0])
                except:
                    pass
