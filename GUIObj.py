#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 15:01:08 2018

@author: wei
"""

# import tkinter
import tkinter as tk
import tkinter.font as tkfont

# import matplotlib
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

#import node
from node import Node
from ORC_plot import calc_SaturationofCurve
from ORC_plot import ProcessPlot
# from ORC_sample import initNode, setAndCalcNode
# import os
# import os
from pathlib import Path
# from openpyxl import Workbook, load_workbook
from datetime import datetime as dt
# import config
import config as cfg
import agilent_load as agilent
from realtime_data import data
# import gc
from csv import writer
from shutil import copyfile


class P_I_Diagram(tk.Frame):
    offset_x = 50
    offset_y = 30

    def __init__(self, master=None):
        tk.Frame.__init__(self, master=None)

        self.canvasID = {}

        ''' load img and create canvas '''
        self.photo = cfg.import_photo()
        self.canvas = tk.Canvas(master,
                                width=self.photo.width(),
                                height=self.photo.height(),
                                bg='white')
        self.canvas.pack(expand=1, fill=tk.BOTH)
        ''' put gif image on canvas
        pic's upper left corner (NW) on the canvas is at x=50 y=10
        '''
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        ''''font'''
        self.fontprop = tkfont.Font(
            size=cfg.GUI["fontsize"])  # bitstream charter or courier 10 pitch

        ''''set label'''
        self.set_Labels()

        # set label of efficiency
        # fontTitle = tkfont.Font(
        #     family='courier 10 pitch', size=30, weight='bold')
        # name = "429_ORC\nEff"
        # unit = "%"
        # self.canvas.create_text(280, 320, text="{} {} {}".format(
        #     name, " "*14, unit), fill='green', font=fontTitle)
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
                unit = "?"

            if unit in ["C", "B"]:
                self.create_text(v["posx"], v["posy"],
                                 f"{sensor_type:<7}{'':^5}{unit:>5}")
                self.canvasID[f"{k}"] = self.create_text(
                    v["posx"], v["posy"], f"{'None':^6}")
            else:
                self.create_text(v["posx"], v["posy"],
                                 f"{sensor_type:<5}{' '*16:^5}{unit:>5}")
                self.canvasID[f"{k}"] = self.create_text(
                    v["posx"], v["posy"], f"{'None':^6}")

    def update_value(self, name, value, n=1):
        itemID = self.canvasID[name]
        self.canvas.itemconfigure(itemID, text=str(round(value, n)))

    def update(self):
        # print("update P&ID")
        for name, value in data.items():
            if isinstance(value, Node):
                self.update_value(f"{name}_T", data[name].t)
                self.update_value(f"{name}_P", data[name].p)
            else:
                try:
                    self.update_value(name, value)
                except:
                    pass


class ORC_Figure(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master=None)

        self.lines = {}

        self._fig = Figure(
            figsize=(cfg.FIG["width"], cfg.FIG["height"]), dpi=100)
        self.canvas = FigureCanvasTkAgg(self._fig, master)
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.ax = self._fig.add_subplot(111)

        self.set_title_label()
        self.set_window_boundary()
        self.openGrid()

        self.toolbar = NavigationToolbar2Tk(self.canvas, master)
        self.toolbar.update()
        self.plot_Saturation_Curve()

        self.set_line()

    def set_title_label(self):
        xAxis = "s"
        yAxis = "T"
        title = {"T": "T, °C", "s": "s, (kJ/kg)*K"}
        self.ax.set_title("%s-%s Diagram" % (yAxis, xAxis))
        self.ax.set_xlabel(title[xAxis])
        self.ax.set_ylabel(title[yAxis])

    def set_window_boundary(self):
        self.ax.set_ylim(10, 150)
        self.ax.set_xlim(0.9, 1.9)

    def openGrid(self):
        self.ax.grid()

    def add_line(self, line=None, **kw):
        if line is None:
            line = Line2D([], [], **kw)

        return self.ax.add_line(line)

    def plot_Saturation_Curve(self):
        saturation_curve = calc_SaturationofCurve()
        self.lines["saturation_curve_left"] = self.add_line(
            saturation_curve[0])
        self.lines["saturation_curve_right"] = self.add_line(
            saturation_curve[1])

    def set_line(self):
        for name, attr in cfg.LINE.items():
            if attr["type"] == "o":
                self.lines[f"{name}"] = self.add_line(
                    linestyle='None', color="k", marker=".")
            elif attr["type"] == "s":
                self.lines[f"{name}"] = self.add_line(lw=1.3, color="g")
            elif attr["type"] == "p":
                self.lines[f"{name}"] = self.add_line(lw=1.3, color="g")
            elif attr["type"] == "l":
                if name == "heat":
                    self.lines[f"{name}"] = self.add_line(lw=2.0, color="r")
                elif name == "cool":
                    self.lines[f"{name}"] = self.add_line(lw=2.0, color="b")
            else:
                print(f"{name} config error")

    def update_line(self, line_name, line_type, points):
        s = []
        T = []
        if line_type == "o":
            for point_name in points:
                s.append(data[f"{point_name}"].s)
                T.append(data[f"{point_name}"].t)
        elif line_type == "s":
            process = ProcessPlot(
                data[f"{points[0]}"], data[f"{points[1]}"], 'isos')
            process.test_iso_line()
            process.calc_iso()
            s = process.Isa
            T = process.Ita
        elif line_type == "p":
            process = ProcessPlot(
                data[f"{points[0]}"], data[f"{points[1]}"], 'isop')
            process.test_iso_line()
            process.calc_iso()
            s = process.Isa
            T = process.Ita
        elif line_type == "l":
            s_list = []
            for node in data.values():
                if isinstance(node, Node):
                    s_list.append(node.s)
            if line_name == "heat":
                s.append([max(s_list), min(s_list)])
            elif line_name == "cool":
                s.append([min(s_list), max(s_list)])
            else:
                print("f{line_name} config warning")
            T.append([data[f"{points[0]}_Ti"], data[f"{points[1]}_To"]])

        self.lines[f"{line_name}"].set_data(s, T)

    def update(self):
        # print("update T-s Diagram")
        for name, attr in cfg.LINE.items():
            self.update_line(name, attr["type"], attr["point"])

        self.canvas.draw()


class Scan_button(tk.Frame):
    def __init__(self, master=None, *callbacks):
        tk.Frame.__init__(self, master=None)
        # gc.disable()
        self.update_funcs = []
        for func in callbacks:
            if callable(func):
                self.update_funcs.append(func)
            else:
                def func(): return print("this is not a func")
                self.update_funcs.append(func)

        self.is_click = False

        def btn_cmd_loop(func):
            if self.is_click:
                self.is_click = False
                varScan.set('stop2scan')
            else:
                self.is_click = True
                varScan.set('start2scan')
                func()

        varScan = tk.StringVar()
        varScan.set('stop2scan')

        labelScan = tk.Label(
            master,
            textvariable=varScan,
            bg='white',
            font=('Arial', 12),
            width=15, height=2)
        labelScan.pack()

        button = tk.Button(
            master,
            text='click me',
            width=15, height=2,
            command=lambda: btn_cmd_loop(self.update_diagram))
        button.pack()

        ''' init v34970A '''
        self.dev = agilent.test_V34972A()
        # self.dev = agilent.V34972A()
        ''' csv file '''
        self.file = csv_file()

    def call_update_funcs(self):
        for func in self.update_funcs:
            func()

    def update_diagram(self, count=0):
        if self.is_click:
            print("----" * 5)
            self.dev.scan()
            self.calc_nodes()
            self.file.save_data()
            ''' update functions
            update P&ID
            update T-s diagram
            '''
            self.call_update_funcs()
            self.after(300, self.update_diagram, count+1)

    def calc_nodes(self):
        # print("calc nodes and works")
        ''' calc nodes '''
        for name, value in data.items():
            if isinstance(value, Node):
                # print(name, data[name].p, data[name].t)
                data[name].pt()
        ''' calc WORK '''
        for name, node in cfg.FM.items():
            item0 = data[f"{node[0]}"]
            item1 = data[f"{node[1]}"]
            mDot = data["mDot"]
            data[f"{name}"] = (item1.h - item0.h) * mDot

        ''' calc efficiency '''
        data["Eff"] = ((data["Wout"] - data["Win"]) / data["Qin"]) * 100

        ''' other '''
        data["count"] = data["count"] + 1
        data["time"] = dt.now().time()
        data["timestamp"] = dt.now().timestamp()


class csv_file:
    def __init__(self):
        self.header = cfg.FILE["header"]
        self.path = cfg.FILE["folder-path"]
        self.file_buffer_count = 0
        self.data_buffer_count = 0
        today = dt.now().date()
        self.lock_file = f".{today}.lock"
        self.csv_file = f"{today}.csv"

        self.lock_path = f"{self.path}/{self.lock_file}"
        self.csv_path = f"{self.path}/{self.csv_file}"

        self.open_file()

    def open_file(self):
        ''' check file exist?
        if file is not exist,
        system will create file with header
        '''
        # check file path
        Path(self.path).mkdir(parents=True, exist_ok=True)
        if Path(self.lock_path).is_file():
            print("File exist")
            self.file = open(self.lock_path, 'a')
            self.writer = writer(self.file)
        else:
            ''' avoid users crash file
            Lock file just ORC GUI can used.
            Prevent users from crashing the system due to file modification.
            '''
            self.file = open(self.lock_path, 'a')
            self.writer = writer(self.file)
            self.writer.writerow(self.header)
            self.file.flush()

    def save_data(self):
        self.write_data(cfg.FILE["data_buffer"])
        self.transfer_file(cfg.FILE["file_buffer"])

    def write_data(self, buffer=0):
        self.writer.writerow(self.row_data())

        if self.data_buffer_count > buffer:
            self.file.flush()
            self.data_buffer_count = 0

        self.data_buffer_count += 1

    def row_data(self):
        def myround(num):
            length = len(str(num))
            if length - 1 > 4:
                n = 4 - len(str(num).split(".")[0])
                if n < 1:
                    return int(num)
                return round(num, n)
            else:
                return num
        row = []
        for value in cfg.FILE["data"]:
            if "`" in value:
                def oprater(one, two, op):

                    if op == "+":
                        value = one + two
                    elif op == "-":
                        value = one - two
                    elif op == "*":
                        value = one * two
                    elif op == "/":
                        value = one / two
                    else:
                        value = 9999
                    return value

                index = 0
                l = value.find("{", index)
                r = value.find("}", index)
                one = value[l+1:r]
                name, attr = one.split(".")
                one = myround(data[f"{name}"][f"{attr}"])

                index = r+1
                op = value[index]

                l = value.find("{", index)
                r = value.find("}", index)
                two = value[l+1:r]
                name, attr = two.split(".")
                two = myround(data[f"{name}"][f"{attr}"])

                v = myround(oprater(one, two, op))

            elif "." in value:
                name, attr = value.split(".")
                v = myround(data[f"{name}"][f"{attr}"])
            else:
                try:
                    if isinstance(data[f"{value}"], float):
                        v = myround(data[f"{value}"])
                    else:
                        v = data[f"{value}"]
                except:
                    v = f"{value}"
            row.append(v)
        return row

    def transfer_file(self, buffer=5, close=False):
        ''' transfer lock file to experiment file
        When experiment is done,
        system will copy lock file into experiment file.
        '''
        if self.file_buffer_count > buffer or close:
            copyfile(self.lock_path, self.csv_path)
            self.file_buffer_count = 0
        self.file_buffer_count += 1

    def __del__(self):
        print("delete")
        self.transfer_file(close=True)


if __name__ == "__main__":
    from GUI import main

    main()
