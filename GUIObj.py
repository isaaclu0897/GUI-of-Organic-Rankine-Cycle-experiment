#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 15:01:08 2018

@author: wei
"""

from tkinter import Frame, Canvas, StringVar, Label, Button, font, Entry

from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from thermo.node import Node
from thermo.plot import calc_SaturationofCurve, ProcessPlot

from pathlib import Path
from datetime import datetime as dt
import db._config as cfg
import dev
from db._realtime import shell
from csv import writer
from shutil import copyfile
from threading import Thread
import db

def thread_func(func, *args):
    # print("thread")
    t = Thread(target=func, args=args, name=f"{func.__name__}")
    t.setDaemon(True)
    t.start()


class P_I_Diagram(Frame):
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


class ORC_Figure(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master=None)

        self.lines = {}

        self._fig = Figure(
            figsize=(cfg.FIG["width"], cfg.FIG["height"]), dpi=100)
        self.canvas = FigureCanvasTkAgg(self._fig, master)
        self.canvas._tkcanvas.pack(side="top", fill="both", expand=1)

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
                s.append(shell[f"{point_name}"].s)
                T.append(shell[f"{point_name}"].t)
        elif line_type == "s":
            process = ProcessPlot(
                shell[f"{points[0]}"], shell[f"{points[1]}"], 'isos')
            process.test_iso_line()
            process.calc_iso()
            s = process.Isa
            T = process.Ita
        elif line_type == "p":
            process = ProcessPlot(
                shell[f"{points[0]}"], shell[f"{points[1]}"], 'isop')
            process.test_iso_line()
            process.calc_iso()
            s = process.Isa
            T = process.Ita
        elif line_type == "l":
            s_list = []
            for node in shell.values():
                if isinstance(node, Node):
                    s_list.append(node.s)
            if line_name == "heat":
                s.append([max(s_list), min(s_list)])
            elif line_name == "cool":
                s.append([min(s_list), max(s_list)])
            else:
                print("f{line_name} config warning")
            T.append([shell[f"{points[0]}_Ti"], shell[f"{points[1]}_To"]])
        self.lines[f"{line_name}"].set_data(s, T)
        # print(self.lines[f"{line_name}"])

    def update(self):
        print("update T-s Diagram")
        for name, attr in cfg.LINE.items():
            self.update_line(name, attr["type"], attr["point"])
        self.canvas.draw_idle()


class Scan_button(Frame):
    def __init__(self, master=None, *callbacks):
        Frame.__init__(self, master=None)
        self.update_funcs = []
        for func in callbacks:
            if callable(func):
                self.update_funcs.append(func)
            else:
                def func(): print("this is not a func")
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

        varScan = StringVar()
        varScan.set('stop2scan')

        labelScan = Label(
            master,
            textvariable=varScan,
            bg='white',
            font=('Arial', 12),
            width=15, height=2)
        labelScan.pack()

        button = Button(
            master,
            text='click me',
            width=15, height=2,
            command=lambda: btn_cmd_loop(self.th_update))
        button.pack()

        ''' init v34970A '''
        print(db.device)
        if db.device["mode"] == "test":
            self.dev = dev.TEST()
        elif db.device["mode"] == "V34972A":
            self.dev = dev.V34972A()
        else:
            raise "ConfigError(device['mode']), please use manual/V34972A/DAQ970A"
        ''' csv file '''
        self.file = csv_file()

    def call_update_funcs(self):
        print(self.update_funcs)
        for func in self.update_funcs:
            func()

    def th_update(self):
        thread_func(self.update_diagram)

    def update_diagram(self):
        if self.is_click:
            self.after(500, self.th_update)
            print(1)
            self.dev.scan()
            print(2)
            self.calc_nodes()
            print(3)
            self.file.save_data()
            ''' update functions
            update P&ID
            update T-s diagram
            '''
            self.call_update_funcs()

    def calc_nodes(self):
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


class mDot_simulation(Frame):
    def __init__(self, master=None, *callbacks):
        Frame.__init__(self, master=None)

        def confirm():
            mDot = float(mDot_entry.get())
            shell["mDot"] = mDot

        button = Button(
            master,
            text='confirm',
            command=confirm)
        button.pack(side="right")

        mDot_entry = Entry(master, width=10)
        mDot_entry.pack(side="right")


class csv_file:
    def __init__(self):
        self.header = cfg.FILE["header"]
        self.path = cfg.FILE["folder-path"]
        self.file_buffer_count = 0
        self.data_buffer_count = 0

        today = dt.now().date()
        self.lock_file = f"{self.path}/.{today}.lock"
        self.csv_file = f"{self.path}/{today}.csv"

        self.open_file()

    def open_file(self):
        ''' check file exist?
        if file is not exist,
        system will create file with header
        '''
        Path(self.path).mkdir(parents=True, exist_ok=True)
        if Path(self.lock_file).is_file():
            self.file = open(self.lock_file, 'a', newline="")
            self.writer = writer(self.file)
        else:
            ''' avoid user crash file
            Lock file, just GUI can used.
            Prevent user from crashing the system due to file modification.
            '''
            self.file = open(self.lock_file, 'a', newline="")
            self.writer = writer(self.file)
            print(self.header)
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
            if "shell" in value:
                v = myround(eval(value))

            elif "." in value:
                name, attr = value.split(".")
                v = myround(shell[f"{name}"][f"{attr}"])
            else:
                try:
                    if isinstance(shell[f"{value}"], float):
                        v = myround(shell[f"{value}"])  # timestamp
                    else:
                        v = shell[f"{value}"]  # f"{value}" in data count time
                except:
                    v = f"{value}"
                    # print(f"{value} can not convert")
            row.append(v)
        return row

    def transfer_file(self, buffer=5, close=False):
        ''' transfer lock file to experiment file
        When experiment is done,
        system will copy lock file into experiment file.
        '''
        if self.file_buffer_count > buffer or close:
            copyfile(self.lock_file, self.csv_file)
            self.file_buffer_count = 0
        self.file_buffer_count += 1

    def __del__(self):
        self.transfer_file(close=True)

