#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 15:01:08 2018

@author: wei
"""

from threading import Timer
import tkinter as tk
import tkinter.font as tkfont
from PIL import ImageTk, Image

from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from ORC_plot import calc_SaturationofCurve, calc_StatusofORC
#import node
from ORC_plot import ProcessPlot
from ORC_sample import initNode, setAndCalcNode
import os
from openpyxl import Workbook, load_workbook
import datetime

from json import load
with open('config.json', 'r') as f:
    config = load(f)
    del f


def make_GUI_config():
    node_config = config["System"]["node"]
    attr_config = config["System"]["attribute"]

    GUI_config = {}
    for name in node_config:
        for attr, value in node_config[name].items():
            GUI_config[f"{name}_{attr}"] = value["GUI"]
    for name, value in attr_config.items():
        GUI_config[f"{name}"] = value["GUI"]

    return GUI_config



class P_and_I_Diagram(tk.Frame):
    offset_x = 50
    offset_y = 30

    def __init__(self, master=None):
        tk.Frame.__init__(self, master=None)

        self.canvasID = {}

        ''' load config'''
        self.photo_config = config["GUI"]
        self.GUI_config = make_GUI_config()
        self.font = self.photo_config["font"]
        self.scaling_factor = self.photo_config["scaling_factor"]
        self.fontsize = self.scaling(self.photo_config["fontsize"])

        ''' load img and create canvas'''
        # load the .gif image file, put gif file here
        # test gif, png and jpg, jpg can't use
        image = Image.open(self.photo_config["path"])
        w, h = self.scaling(image.width), self.scaling(image.height)
        image = image.resize((w, h), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(image)
        # create the canvas, size in pixels
        self.canvas = tk.Canvas(
            master, width=self.img.width(), height=self.img.height(), bg='white')
        self.canvas.pack(expand=1, fill=tk.BOTH)
        # put gif image on canvas
        # pic's upper left corner (NW) on the canvas is at x=50 y=10
        self.canvas.create_image(0, 0, image=self.img, anchor=tk.NW)

        ''''font'''
        self.fontprop = tkfont.Font(
            family=self.font, size=self.fontsize)  # bitstream charter or courier 10 pitch

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

    def create_img(self):
        pass
        
    def scaling(self, value):
        return int(value * self.scaling_factor)
    
    def create_text(self, posx, posy, text):
        return self.canvas.create_text(posx, posy, text=text, fill='blue', font=self.fontprop)

    def set_Labels(self):
        for k, v in self.GUI_config.items():
            v["posx"], v["posy"] = self.scaling(v["posx"]), self.scaling(v["posy"])
            # pass 
            if v["posx"] == 0 or v["posy"] == 0:
                continue
            label_name = k.split("_")[-1]
            # default unit
            if "T" in label_name:
                unit = "C"
            elif "P" in label_name:
                unit = "B"
            elif label_name in ["Win", "Wout", "Qin", "Qout"]:
                unit = "kW"
            elif label_name in ["Eff", "Ein", "Eout"]:
                unit = "%"
            elif label_name in ["mDot"]:
                unit = "kg/s"
            else:
                unit = "?"
            
            if unit in ["C", "B"]:
                self.create_text(v["posx"], v["posy"], text=f"{label_name:<7}{'':^5}{unit:>5}")
                self.canvasID[f"{k}"] = self.create_text(v["posx"], v["posy"], text=f"{'None':^6}")
            else:
                self.create_text(v["posx"], v["posy"], text=f"{label_name:<5}{' '*16:^5}{unit:>5}")
                self.canvasID[f"{k}"] = self.create_text(v["posx"], v["posy"], text=f"{'None':^6}")
    # def set_Labels(self):
    #     for k, v in self.GUI_config.items():
    #         name = k.split("_")[-1]
    #         unit = ""
    #         # print(name)
    #         if name == "mDot":
    #             unit = "kg/s"
    #         elif name in ["Win", "Wout", "Qin", "Qout"]:
    #             unit = "kW"
                
    #         if unit:
    #             self.create_text(v["posx"], v["posy"], text=f"{name:_<5}{'':_^5}{unit:_>5}")
    #             self.canvasID[f"{k}"] = self.create_text(v["posx"], v["posy"], text=f"{'None':_^5}")

    # def set_P_T_Labels(self):
    #     for name, pos in self.config_P_T_Labels.items():
    #         self.create_text(pos["posx"], pos["posy"], text='P')
    #         self.canvasID["{}_value_P".format(name)] = \
    #             self.create_text(pos["posx"]+self.offset_x,
    #                              pos["posy"], text='None')
    #         self.create_text(pos["posx"], pos["posy"]+self.offset_y, text='T')
    #         self.canvasID["{}_value_T".format(name)] = \
    #             self.create_text(pos["posx"]+self.offset_x,
    #                              pos["posy"]+self.offset_y, text='None')

    # def set_T_Labels(self):
    #     for name, pos in self.config_T_Labels.items():
    #         self.create_text(pos["posx"], pos["posy"], text='T')
    #         self.canvasID["{}_value_T".format(name)] = \
    #             self.create_text(pos["posx"]+self.offset_x,
    #                              pos["posy"], text='None')

    # def set_Labels(self):
    #     for name, pos in self.config_Labels.items():
    #         self.create_text(pos["posx"], pos["posy"], text="{} {} {}".format(
    #             name, " "*14, pos["unit"]))
    #         self.canvasID["{}_value".format(name)] = \
    #             self.create_text(pos["posx"]+10, pos["posy"], text='None')

    def update_canvas_value(self, itemID, vlaue):
        self.canvas.itemconfigure(itemID, text=str(vlaue))
        # return self.canvas.create_text(posx, posy, text=text, fill='blue', font=self.fontprop)
#     def update_state(self, num, data):
#         self.canvas.itemconfigure(self.state['node{}'.format(num)]['p'], text=str(round(data.p, 2)))
#         self.canvas.itemconfigure(self.state['node{}'.format(num)]['t'], text=str(round(data.t, 1)))

#     def update_stateHX(self, data):
#         self.canvas.itemconfigure(self.stateHX['heater']['ti'], text=str(round(data[0].t, 1)))
#         self.canvas.itemconfigure(self.stateHX['heater']['to'], text=str(round(data[1].t, 1)))
#         self.canvas.itemconfigure(self.stateHX['cooler']['ti'], text=str(round(data[3].t, 1)))
#         self.canvas.itemconfigure(self.stateHX['cooler']['to'], text=str(round(data[2].t, 1)))

#     def update_eff(self, eff_num):
#         self.canvas.itemconfigure(self.eff, text=str(round(eff_num, 2)))
#     def update_mdot(self, mdot_num):
#         self.canvas.itemconfigure(self.mdot, text=str(round(mdot_num, 4)))
#     def update_Win(self, Win_num):
#         self.canvas.itemconfigure(self.Win, text=str(round(Win_num, 3)))
#     def update_Qin(self, Qin_num):
#         self.canvas.itemconfigure(self.Qin, text=str(round(Qin_num, 2)))
#     def update_Wout(self, Wout_num):
#         self.canvas.itemconfigure(self.Wout, text=str(round(Wout_num, 3)))
#     def update_Qout(self, Qout_num):
#         self.canvas.itemconfigure(self.Qout, text=str(round(Qout_num, 2)))
#     def update_Eff(self, Eff_num):
#         self.canvas.itemconfigure(self.Eff, text=str(round(Eff_num, 2)))
#     def update_Effi(self, Effi_num):
#         self.canvas.itemconfigure(self.Effi, text=str(round(Effi_num, 2)))
#     def update_mdotWater(self, mdotWater_num):
#         self.mdotWater = mdotWater_num
    def update_data(self, nodesSys, nodesHX):
        for i in range(len(nodesSys)):
            self.update_state(i+1, nodesSys[i])

        self.update_stateHX(nodesHX)

        eff = ((nodesSys[2].h-nodesSys[3].h)/(nodesSys[2].h-nodesSys[1].h))*100

        mdot = self.mdotWater*4.2 * \
            (nodesHX[0].t-nodesHX[1].t)/(nodesSys[2].h-nodesSys[1].h)

        Win = mdot * (nodesSys[1].h - nodesSys[0].h)
        Qin = mdot * (nodesSys[2].h - nodesSys[1].h)
        Wout = mdot * (nodesSys[2].h - nodesSys[3].h)
        Qout = mdot * (nodesSys[3].h - nodesSys[0].h)

        self.update_eff(eff)
        self.update_mdot(mdot)
        self.update_Win(Win)
        self.update_Qin(Qin)
        self.update_Wout(Wout)
        self.update_Qout(Qout)
        self.update_Eff(eff)
#        self.update_Effi(Effi)


class ORC_Figure(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master=None)

        self._fig = Figure(figsize=(8, 6), dpi=100)
        self.canvas = FigureCanvasTkAgg(self._fig, master)

#        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)
        self.dia = self._fig.add_subplot(111)
        xAxis = "s"
        yAxis = "T"
        title = {"T": "T, °C", "s": "s, (kJ/kg)*K"}
        self.dia.set_title("%s-%s Diagram" % (yAxis, xAxis))
        self.dia.set_xlabel(title[xAxis])
        self.dia.set_ylabel(title[yAxis])
        self.set_window_boundary()
        self.openGrid()

        self.toolbar = NavigationToolbar2Tk(self.canvas, master)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.setThermoLine()
        self.addThermoLine()

    def set_window_boundary(self):
        self.dia.set_ylim(10, 150)
        self.dia.set_xlim(0.9, 1.9)

    def openGrid(self):
        self.dia.grid()

    def setThermoLine(self):
        self.lineOfSaturationCurve = calc_SaturationofCurve()

        self.lineStatePoint = Line2D(
            [], [], color='g', linestyle='None', marker='o')

        self.linePumpimg = Line2D([], [], color="g", lw=2.5)
        self.lineHeating = Line2D([], [], color="g", lw=2.5)
        self.lineWorking = Line2D([], [], color="g", lw=2.5)
        self.lineCooling = Line2D([], [], color="g", lw=2.5)

        self.linePumpimgISO = Line2D([], [], color="grey", lw=1.3)
        self.lineHeatingISO = Line2D([], [], color="grey", lw=1.3)
        self.lineWorkingISO = Line2D([], [], color="grey", lw=1.3)
        self.lineCoolingISO = Line2D([], [], color="grey", lw=1.3)

        self.lineHeater = Line2D([], [], color="r", lw=2.0)
        self.lineCooler = Line2D([], [], color="b", lw=2.0)

        self.thermoLine = [self.linePumpimg, self.lineHeating,
                           self.lineWorking, self.lineCooling]
        self.thermoLineISO = [
            self.linePumpimgISO, self.lineHeatingISO, self.lineWorkingISO, self.lineCoolingISO]
        self.heatExchangerLine = [self.lineHeater, self.lineCooler]

    def addThermoLine(self):
        for i in self.lineOfSaturationCurve:
            self.dia.add_line(i)

        self.dia.add_line(self.lineStatePoint)

        for i in self.thermoLine:
            self.dia.add_line(i)

        for i in self.thermoLineISO:
            self.dia.add_line(i)

        for i in self.heatExchangerLine:
            self.dia.add_line(i)

    def updata_StatePoint(self, data):
        self.lineStatePoint.set_xdata(data[0])
        self.lineStatePoint.set_ydata(data[1])

    def updata_thermoLine(self, data):
        for i in range(len(data)):
            self.thermoLine[i].set_xdata(data[i][1][0])
            self.thermoLine[i].set_ydata(data[i][1][1])

            self.thermoLineISO[i].set_xdata(data[i][0][0])
            self.thermoLineISO[i].set_ydata(data[i][0][1])

    def updata_heatExchangerLine(self, data):
        for i in range(len(data)):
            self.heatExchangerLine[i].set_xdata(data[i][0])
            self.heatExchangerLine[i].set_ydata(data[i][1])

    def update_data(self, nodesSys, nodesHX):
        #            ORC_status([nodes[i] for i in range(len(nodes))])
        state_data = calc_StatusofORC(nodesSys, [0, 1, 2, 3])

        process = [ProcessPlot(0, 1, 'isos'),
                   ProcessPlot(1, 2, 'isop'),
                   ProcessPlot(2, 3, 'isos'),
                   ProcessPlot(3, 0, 'isop')]
        thermoLine = [plot.plot_process_data(nodesSys) for plot in process]

        heatExchangerLine_data = [[[nodesHX[0].s, nodesHX[1].s], [nodesHX[0].t, nodesHX[1].t]],
                                  [[nodesHX[2].s, nodesHX[3].s], [nodesHX[2].t, nodesHX[3].t]]]

        self.updata_StatePoint(state_data)
        self.updata_thermoLine(thermoLine)
        self.updata_heatExchangerLine(heatExchangerLine_data)

        self.canvas.draw()


class Scan_button(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master=None)

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

        ''' init v34970a '''

    def update_diagram(self):
        print("update_diagram")

        def innerfunc(text):
            print(text)
            self.scan_data()
            self.update_P_and_I_Diagram()
            self.update_T_s_Diagram()
        # readings_PRESS = [1.8, 9, 8.3, 2.3, 1.9, 2]
        # readings_TEMP = [22, 25, 97, 64, 24, 68, 99, 89, 22, 24]

        # value = data.send(readings_TEMP, readings_PRESS)
        # print(value)
        # data.update(SM_dia, TH_dia)

        # innerfunc()

        def timer(func, second=2, *arg):
            func(*arg)
            t = Timer(second, timer, args=(func, 3, *arg))
            t.setDaemon(True)

            if t.daemon and self.is_click:
                t.start()
            else:
                return 0

        timer(innerfunc, 3, "**kw")

    def scan_data():
        print("scan_data")

    def update_P_and_I_Diagram(self):
        print("update P&ID")

    def update_T_s_Diagram(self):
        print("update T-s Diagram")


class SendData:
    def __init__(self):
        pumpi = {'name': 'pump_inlet',         'nid': 1}
        pumpo = {'name': 'pump_ioutlet',       'nid': 2}
        EXPi = {'name': 'expander_inlet',     'nid': 3}
        EXPo = {'name': 'expander_outlet',    'nid': 4}

        HI = {'name': 'heat_inlet',       'nid': 5}
        HO = {'name': 'heat_outlet',      'nid': 6}
        CI = {'name': 'condenser_inlet',  'nid': 7}
        CO = {'name': 'condenser_outlet', 'nid': 8}

# =========================================================
# define the  of all point & init all node
# =========================================================

        self.dev_list = [pumpi, pumpo, EXPi, EXPo]
        self.heatexchange_list = [HI, HO, CI, CO]
        self.mdotWater = None

    def send(self, readings_TEMP, readings_PRESS):
        for i in range(4):
            self.dev_list[i]['P'] = readings_PRESS[i]
            self.dev_list[i]['T'] = readings_TEMP[i]
            self.heatexchange_list[i]['T'] = readings_TEMP[i+6]

    #        global nodesSys
    #        global nodesHX

        self.nodesSys = initNode(self.dev_list)
        self.nodesHX = initNode(self.heatexchange_list)

        setAndCalcNode(self.nodesSys, self.dev_list)
        setAndCalcNode(self.nodesHX, self.heatexchange_list)
        self.nodesHX[0].s = self.nodesSys[2].s + 0.03
        self.nodesHX[1].s = self.nodesSys[0].s - 0.03
        self.nodesHX[2].s = self.nodesSys[0].s - 0.03
        self.nodesHX[3].s = self.nodesSys[2].s + 0.03
        value = [self.nodesSys[1].p-self.nodesSys[0].p, self.nodesSys[0].p, self.nodesSys[0].t, self.nodesSys[0].d, self.nodesSys[0].over, self.nodesSys[0].h,
                 self.nodesSys[1].p, self.nodesSys[1].t, self.nodesSys[1].tSat, self.nodesSys[1].h,
                 self.nodesSys[2].p-self.nodesSys[3].p, self.nodesSys[2].p, self.nodesSys[2].t, self.nodesSys[2].tSat, self.nodesSys[2].over, self.nodesSys[2].h,
                 self.nodesSys[3].p, self.nodesSys[3].t, self.nodesSys[3].tSat, self.nodesSys[3].h,
                 self.nodesHX[0].t, self.nodesHX[1].t, self.nodesHX[1].t -
                 self.nodesSys[2].tSat,
                 self.nodesHX[2].t, self.nodesHX[3].t, self.nodesHX[3].t -
                 self.nodesSys[3].tSat,
                 ((self.nodesSys[2].h-self.nodesSys[3].h) /
                  (self.nodesSys[2].h-self.nodesSys[1].h))*100,
                 self.mdotWater*4.2*(self.nodesHX[0].t-self.nodesHX[1].t)/(self.nodesSys[2].h-self.nodesSys[1].h)]

        return value

    def update(self, SM_dia, TH_dia):

        #
        #        global SM_dia
        #        global TH_dia

        SM_dia.update_data(self.nodesSys, self.nodesHX)
        TH_dia.update_data(self.nodesSys, self.nodesHX)

    def update_mdotWater(self, mdotWater):
        self.mdotWater = mdotWater


def mk_exclusivefile(path, filename):
    ''' 創見專屬資料夾

    說明: 在路徑 path 中, 創見名為 dirname 的資料夾
    -----
    ex:
        path = '/home/wei/data/python/photo'
        dirname = 'good'
        os.path.isdir(path + '/' + dirname) # False
        mk_exclusivedir(path, dirname)
        os.path.isdir(path + '/' + dirname) # True
    '''
    if not os.path.isdir(path):
        os.mkdir(path)
    os.chdir(path)
    if not os.path.isfile(filename):
        workBook = Workbook()
        workSheet = workBook.active
        workSheet['a1'] = '實驗名稱'
        workSheet['a2'] = '實驗日期'
        workSheet['b2'] = datetime.date.today()
        workSheet['a3'] = '實驗說明(描述)'
        workSheet.append(['scan', 'time(real)',
                          '壓差', 'inlet(P)', 'inlet(T)', '密度', '次冷', 'h1',
                          'outlet(P)', 'outlet(T)', '飽和溫度', 'h2',
                          '壓差', 'inlet(P)', 'inlet(T)', '飽和溫度', '過熱', 'h3',
                          'outlet(P)', 'outlet(T)', '飽和溫度', 'h4',
                          'inlet(T)', 'outlet(T)', '高溫壓迫',
                          'inlet(T)', 'outlet(T)', '低溫壓迫',
                          'ORC效率(%)', 'mdot(kg/s)', 'time(s)', '聚集', 'operate'])
        workBook.save(".\{}".format(filename))

    else:
        workBook = load_workbook('{}'.format(filename))
        workSheet = workBook.active

    return workBook, workSheet


#    if not os.path.isdir(dirname):
#        os.mkdir('{}'.format(dirname))
