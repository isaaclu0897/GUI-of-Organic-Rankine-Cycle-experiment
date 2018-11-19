#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 15:01:08 2018

@author: wei
"""

import tkinter as tk
import tkinter.font as tkfont
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from ORC_plot import calc_SaturationofCurve, calc_StatusofORC
from threading import Timer
#import visa
#import node
from ORC_plot import ProcessPlot
from ORC_sample import initNode, setAndCalcNode

class ORC_Status(tk.Frame):
    offset_x = 50
    offset_y = 30
    
    nodePosition = {"node1": {"x": 120, "y": 430},
                    "node2": {"x": 100, "y": 110},
                    "node3": {"x": 480, "y": 150},
                    "node4": {"x": 400, "y": 500}}
    heatExchangerPosition = {"heater": {"x": 500, "y": 50},
                             "cooler": {"x": 500, "y": 615}}
    
    workPosition = {'x': 90,
                    'y': 500}
    #        posx = 220
    #        posy = 220
    
    def __init__(self, master=None):
        tk.Frame.__init__(self, master=None)
        
        # create the canvas, size in pixels
        self.canvas = tk.Canvas(master, width = 900, height = 800, bg = 'white')
        # load the .gif image file, put gif file here
        self.gif1 = tk.PhotoImage(file = './fig/500w_P&ID_4x3.png') # test gif, png and jpg, jpg can't use
        # put gif image on canvas
        # pic's upper left corner (NW) on the canvas is at x=50 y=10
        self.canvas.create_image(0, 0, image=self.gif1, anchor=tk.NW)
        self.canvas.pack(expand = 1, fill = tk.BOTH)
        
        self.fontprop = tkfont.Font(family='courier 10 pitch', size=18)# bitstream charter or courier 10 pitch
        self.fonteff = tkfont.Font(family='courier 10 pitch', size=30, weight='bold')# bitstream charter or courier 10 pitch
        
        self.state = {'node1': {"p": None, "t": None},# can not use state1 = state2 = state3 = state4 = {}, because id will same
                      'node2': {"p": None, "t": None},
                      'node3': {"p": None, "t": None},
                      'node4': {"p": None, "t": None}}
        self.stateHX = {'heater': {'ti': None, 'to': None}, 
                        'cooler': {'ti': None, 'to': None}}
        # set label of pressure and temperature
        self.labelPAndTSet()
        # set value of pressure and temperature
        self.valuePAndTSet()
        
        self.labelHeatExchangerSet()
        self.valueHeatExchangerSet()
        
        # set label of work
        self.labelWorkSet()
        # set value of work
        self.valueWorkSet()
        
        # set label of efficiency
        self.canvas.create_text(280,320, text = '429_ORC\neff:       %', fill = 'blue', font=self.fonteff)
        
        self.eff = self.canvas.create_text(300, 350,text = "None", fill = 'blue', font=self.fonteff)
    
    
    def labelPAndT(self, posx, posy):
        self.canvas.create_text(posx, posy, text='P', fill='blue', font=self.fontprop)  
        self.canvas.create_text(posx, posy+self.offset_y, text='T', fill='blue', font=self.fontprop)
    def labelPAndTSet(self):
        for pos in self.nodePosition.values():
            self.labelPAndT(pos["x"], pos["y"])
    def valuePAndT(self, node, posx, posy, offestx=20):
        self.state[node]['p'] = self.canvas.create_text(posx+self.offset_x, posy, text = 'None', fill = 'blue', font=self.fontprop)
        self.state[node]['t'] = self.canvas.create_text(posx+self.offset_x, posy+self.offset_y,text = 'None', fill = 'blue', font=self.fontprop)
    def valuePAndTSet(self):
        for node, pos in self.nodePosition.items():
            self.valuePAndT(node, pos['x'], pos['y'])
    
    def labelHeatExchanger(self, posx, posy):
        self.canvas.create_text(posx, posy, text='To', fill='blue', font=self.fontprop)  
        self.canvas.create_text(posx, posy+self.offset_y, text='Ti', fill='blue', font=self.fontprop)
    def labelHeatExchangerSet(self):
        for pos in self.heatExchangerPosition.values():
            self.labelHeatExchanger(pos["x"], pos["y"])
    def valueHeatExchanger(self, node, posx, posy, offestx=20):
        self.stateHX[node]['ti'] = self.canvas.create_text(posx+self.offset_x, posy, text = 'None', fill = 'blue', font=self.fontprop)
        self.stateHX[node]['to'] = self.canvas.create_text(posx+self.offset_x, posy+self.offset_y,text = 'None', fill = 'blue', font=self.fontprop)
    def valueHeatExchangerSet(self):
        for node, pos in self.heatExchangerPosition.items():
            self.valueHeatExchanger(node, pos['x'], pos['y'])
            
    
    def labelWork(self, posx, posy, text):
        self.canvas.create_text(posx, posy, text=text, fill = 'blue', font=self.fontprop)
    def labelWorkSet(self):
        self.labelWork(self.workPosition['x'], self.workPosition['y'], text = 'mdot{}kW'.format(' '*6))
        self.labelWork(self.workPosition['x'], self.workPosition['y']+self.offset_y, text = 'Win {}kW'.format(' '*6))
        self.labelWork(self.workPosition['x'], self.workPosition['y']+self.offset_y*2, text = 'Qin {}kW'.format(' '*6))
        self.labelWork(self.workPosition['x'], self.workPosition['y']+self.offset_y*3, text = 'Wout{}kW'.format(' '*6))
        self.labelWork(self.workPosition['x'], self.workPosition['y']+self.offset_y*4, text = 'Qout{}kW'.format(' '*6))
        self.labelWork(self.workPosition['x'], self.workPosition['y']+self.offset_y*5, text = 'Eff{}%'.format(' '*6))
        self.labelWork(self.workPosition['x'], self.workPosition['y']+self.offset_y*6, text = 'Effi{}%'.format(' '*6))
    def valueWorkSet(self, offestx=20):
        posx = self.workPosition['x'] + offestx
        self.mdot = self.canvas.create_text(posx, self.workPosition['y'],text = 'None', fill = 'blue', font=self.fontprop)
        self.Win = self.canvas.create_text(posx, self.workPosition['y']+self.offset_y, text = 'None', fill = 'blue', font=self.fontprop)
        self.Qin = self.canvas.create_text(posx, self.workPosition['y']+self.offset_y*2, text = 'None', fill = 'blue', font=self.fontprop)
        self.Wout = self.canvas.create_text(posx, self.workPosition['y']+self.offset_y*3, text = 'None', fill = 'blue', font=self.fontprop)
        self.Qout = self.canvas.create_text(posx, self.workPosition['y']+self.offset_y*4, text = 'None', fill = 'blue', font=self.fontprop)
        self.Eff = self.canvas.create_text(posx, self.workPosition['y']+self.offset_y*5, text = 'None', fill = 'blue', font=self.fontprop)
        self.Effi = self.canvas.create_text(posx, self.workPosition['y']+self.offset_y*6, text = 'None', fill = 'blue', font=self.fontprop)
    
    def update_state(self, num, data):
        self.canvas.itemconfigure(self.state['node{}'.format(num)]['p'], text=str(round(data.p, 2)))
        self.canvas.itemconfigure(self.state['node{}'.format(num)]['t'], text=str(round(data.t, 1)))
    
    def update_stateHX(self, data):
        self.canvas.itemconfigure(self.stateHX['heater']['ti'], text=str(round(data[0].t, 1)))
        self.canvas.itemconfigure(self.stateHX['heater']['to'], text=str(round(data[1].t, 1)))
        self.canvas.itemconfigure(self.stateHX['cooler']['ti'], text=str(round(data[3].t, 1)))
        self.canvas.itemconfigure(self.stateHX['cooler']['to'], text=str(round(data[2].t, 1)))        
        
    def update_eff(self, eff_num):
        self.canvas.itemconfigure(self.eff, text=str(round(eff_num, 2)))
    def update_mdot(self, mdot_num):
        self.canvas.itemconfigure(self.mdot, text=str(round(mdot_num, 4)))
    def update_Win(self, Win_num):
        self.canvas.itemconfigure(self.Win, text=str(round(Win_num, 3)))
    def update_Qin(self, Qin_num):
        self.canvas.itemconfigure(self.Qin, text=str(round(Qin_num, 2)))
    def update_Wout(self, Wout_num):
        self.canvas.itemconfigure(self.Wout, text=str(round(Wout_num, 3)))
    def update_Qout(self, Qout_num):
        self.canvas.itemconfigure(self.Qout, text=str(round(Qout_num, 2)))
    def update_Eff(self, Eff_num):
        self.canvas.itemconfigure(self.Eff, text=str(round(Eff_num, 2)))
    def update_Effi(self, Effi_num):
        self.canvas.itemconfigure(self.Effi, text=str(round(Effi_num, 2)))
    def update_mdotWater(self, mdotWater_num):
        self.mdotWater = mdotWater_num
    def update_data(self, nodesSys, nodesHX):
        for i in range(len(nodesSys)):
            self.update_state(i+1, nodesSys[i])
            

        self.update_stateHX(nodesHX)

        eff = ((nodesSys[2].h-nodesSys[3].h)/(nodesSys[2].h-nodesSys[1].h))*100

        mdot = self.mdotWater*4.2*(nodesHX[0].t-nodesHX[1].t)/(nodesSys[2].h-nodesSys[1].h)
        
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
        
        self._fig = Figure(figsize=(8,6), dpi=100)
        self.canvas = FigureCanvasTkAgg(self._fig, master)
        
#        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)
        self.dia = self._fig.add_subplot(111)
        xAxis = "s" 
        yAxis = "T" 
        title = {"T": "T, °C", "s": "s, (kJ/kg)*K"} 
        self.dia.set_title("%s-%s Diagram" %(yAxis, xAxis))
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
        self.lineOfSaturationCurve  = calc_SaturationofCurve()
        
        self.lineStatePoint = Line2D([], [], color='g', linestyle='None', marker='o')
        
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
        
        self.thermoLine = [self.linePumpimg, self.lineHeating, self.lineWorking, self.lineCooling]
        self.thermoLineISO = [self.linePumpimgISO, self.lineHeatingISO, self.lineWorkingISO, self.lineCoolingISO]
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
        

def scan_data(on_click_loop, SM_dia, TH_dia):
# =============================================================================
# load the data
# =============================================================================
    probe_type_TEMP, type_TEMP, ch_TEMP = 'TCouple', 'T', '@201:210'
    range_PRESS,resolution_PRESS, ch_PRESS  = 10, 5.5, '@301:306'
    gain_PRESS, state_PRESS = 2.1, 1
#    offset_PRESS, label_PRESS = 0, 'BAR'

    
    rm = visa.ResourceManager()
    v34972A = rm.open_resource('USB0::0x0957::0x2007::MY49017447::0::INSTR') 
#        idn_string = v34972A.query('*IDN?')

    data = SendData()
        

    def innerfunc(on_click_loop, SM_dia, TH_dia):
        # scan temperature
        scans_TEMP = v34972A.query(':MEASure:TEMPerature? %s,%s,(%s)' % (probe_type_TEMP, type_TEMP, ch_TEMP))
        
        # scan pressure
        v34972A.write(':CONFigure:VOLTage:DC %G,%G,(%s)' % (range_PRESS,resolution_PRESS, ch_PRESS))
        v34972A.write(':CALCulate:SCALe:GAIN %G,(%s)' % (gain_PRESS, ch_PRESS))
        v34972A.write(':CALCulate:SCALe:STATe %d,(%s)' % (state_PRESS, ch_PRESS))
        scans_PRESS = v34972A.query(':READ?')
        
        # convert str to float
        readings_TEMP = [float(x) for x in scans_TEMP.split(',')]
        readings_PRESS = [float(x) for x in scans_PRESS.split(',')]
        
#        print(readings_TEMP, readings_PRESS)
        readings_PRESS = [1.8, 8.8, 8.6, 1.9, 1.9, 2]
        readings_TEMP = [22, 25, 97, 64, 24, 68, 99, 89, 22, 24]
        
        data.send(readings_TEMP, readings_PRESS)
        data.update(SM_dia, TH_dia)

    timer(innerfunc, 3, on_click_loop, SM_dia, TH_dia)

def test_scan_data(SM_dia, TH_dia):

    data = SendData()

    def innerfunc(SM_dia, TH_dia):
        readings_PRESS = [1.8, 9, 8.3, 2.3, 1.9, 2]
        readings_TEMP = [22, 25, 97, 64, 24, 68, 99, 89, 22, 24]
        
        
        data.send(readings_TEMP, readings_PRESS)
        data.update(SM_dia, TH_dia)
    
    innerfunc(SM_dia, TH_dia)



    
class SendData:
    def __init__(self):
        pumpi = {'name' : 'pump_inlet',         'nid' : 1}
        pumpo = {'name' : 'pump_ioutlet',       'nid' : 2}
        EXPi  = {'name' : 'expander_inlet',     'nid' : 3}
        EXPo  = {'name' : 'expander_outlet',    'nid' : 4}
        
        HI = {'name' : 'heat_inlet',       'nid' : 5}
        HO = {'name' : 'heat_outlet',      'nid' : 6}
        CI = {'name' : 'condenser_inlet',  'nid' : 7}
        CO = {'name' : 'condenser_outlet', 'nid' : 8}
        
# =========================================================
# define the  of all point & init all node
# =========================================================

        self.dev_list = [pumpi, pumpo, EXPi, EXPo]
        self.heatexchange_list = [HI, HO, CI, CO]
    
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
            
        
    def update(self, SM_dia, TH_dia):

#        
#        global SM_dia
#        global TH_dia
        
        SM_dia.update_data(self.nodesSys, self.nodesHX)
        TH_dia.update_data(self.nodesSys, self.nodesHX)


def timer(func, second=2, *arg):
    func(*arg)
    t = Timer(second, timer, args=(func, 3, *arg))
    t.setDaemon(True)
    
    on_click_loop = arg[0]
    
    if t.daemon and on_click_loop:
        t.start()
    else:
#        del readings_TEMP, readings_PRESS
        return 0