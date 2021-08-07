#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 00:24:49 2018

@author: wei
"""

from log import logger
from tkinter import Tk, Frame, Label
from db._realtime import shell
from thermo.node import Node
import db._config as cfg
from datetime import datetime as dt


class App(Frame):
    def __init__(self, master=None):
        super().__init__(master=None)

        self.initUI()

    def initUI(self):
        self.master.title("ORC Realtime System")

        main = Frame(self.master)
        main.pack()
        footer = Frame(self.master)
        footer.pack()

        Label(footer, text='developer:HW Lu, laboratory:429, professor:TC Hung, agency:National Taipei Technology University').pack()

        self.frame_left = Frame(main)
        self.frame_left.pack(side="left")

        frame_right = Frame(main)
        frame_right.pack(side="right")

        self.frame_ts = Frame(frame_right)
        self.frame_ts.pack(side="top")

        self.frame_right = Frame(frame_right)
        self.frame_right.pack(side="bottom")

    def add_label(self):
        Label(self.frame_left, text='frame_left').pack()
        Label(self.frame_ts, text='frame_ts').pack()
        Label(self.frame_right, text='frame_right').pack()


def calc_nodes():
    ''' calc nodes '''
    for name, value in shell.items():
        if isinstance(value, Node):
            shell[name].pt()
    ''' calc WORK '''
    for name, node in cfg.FM.items():
        item0 = shell[f"{node[0]}"]
        item1 = shell[f"{node[1]}"]
        mDot = shell["mDot"]
        shell[f"{name}"] = (item1.h - item0.h) * mDot

    ''' calc efficiency '''
    shell["Eff"] = ((shell["Wout"] - shell["Win"]) / shell["Qin"]) * 100

    ''' other '''
    shell["count"] = shell["count"] + 1
    shell["time"] = dt.now().time()
    shell["ts"] = dt.now().timestamp()
    print(f"{shell['count']}----" * 5)


if __name__ == '__main__':

    logger.info('program starting!')

    import db
    import dev
    from GUIObj import Scan_button
    import widget
    import widget.simulation as sim

    if db.device["mode"] == "test":
        device = dev.TEST()
    elif db.device["mode"] == "V34972A":
        device = dev.V34972A()
    else:
        raise "ConfigError(device['mode']), please use manual/V34972A/DAQ970A"

    logger.info('init UI')

    window = Tk()
    app = App()
    # app.add_label()

    logger.info('add componement in layout')

    PnID = widget.PnID(app.frame_left)
    sim.MDot(app.frame_left)
    TnSD = widget.TnSD(app.frame_ts)
    Scan_button(app.frame_right, device.scan, calc_nodes, PnID.update, TnSD.update)

    window.bind("<Escape>", lambda x: window.destroy())

    window.mainloop()

    logger.info('program finish.')
