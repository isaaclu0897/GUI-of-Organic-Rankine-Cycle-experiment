#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 00:24:49 2018

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
import node
from ORC_plot import ProcessPlot

class ORC_Status(tk.Frame):
    offset_x = 50
    offset_y = 30
    
    nodePosition = {"node1": {"x": 120, "y": 430},
                    "node2": {"x": 100, "y": 110},
                    "node3": {"x": 480, "y": 150},
                    "node4": {"x": 400, "y": 500}}
    
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
        # set label of pressure and temperature
        self.labelPAndTSet()
        # set value of pressure and temperature
        self.valuePAndTSet()
        
        
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
            
    
    def labelWork(self, posx, posy, text):
        self.canvas.create_text(posx, posy, text=text, fill = 'blue', font=self.fontprop)
    def labelWorkSet(self):
        self.labelWork(self.workPosition['x'], self.workPosition['y'], text = 'mdot{}kW'.format(' '*6))
        self.labelWork(self.workPosition['x'], self.workPosition['y']+self.offset_y, text = 'Win {}kW'.format(' '*6))
        self.labelWork(self.workPosition['x'], self.workPosition['y']+self.offset_y*2, text = 'Qin {}kW'.format(' '*6))
        self.labelWork(self.workPosition['x'], self.workPosition['y']+self.offset_y*3, text = 'Wout{}kW'.format(' '*6))
        self.labelWork(self.workPosition['x'], self.workPosition['y']+self.offset_y*4, text = 'Qout{}kW'.format(' '*6))
    def valueWorkSet(self, offestx=20):
        posx = self.workPosition['x'] + offestx
        self.mdot = self.canvas.create_text(posx, self.workPosition['y'],text = 'None', fill = 'blue', font=self.fontprop)
        self.Win = self.canvas.create_text(posx, self.workPosition['y']+self.offset_y, text = 'None', fill = 'blue', font=self.fontprop)
        self.Qin = self.canvas.create_text(posx, self.workPosition['y']+self.offset_y*2, text = 'None', fill = 'blue', font=self.fontprop)
        self.Wout = self.canvas.create_text(posx, self.workPosition['y']+self.offset_y*3, text = 'None', fill = 'blue', font=self.fontprop)
        self.Qout = self.canvas.create_text(posx, self.workPosition['y']+self.offset_y*4, text = 'None', fill = 'blue', font=self.fontprop)
    
    
    def update_state(self, num, data):
        self.canvas.itemconfigure(self.state['node'.format(num)]['p'], text=str(round(data.p, 2)))
        self.canvas.itemconfigure(self.state['node'.format(num)]['t'], text=str(round(data.t, 1)))
    def update_eff(self, eff_num):
        self.canvas.itemconfigure(self.eff, text=str(round(eff_num, 2)))
    def update_mdot(self, mdot_num):
        self.canvas.itemconfigure(self.mdot, text=str(round(mdot_num, 5)))
    def update_Qin(self, Qin_num):
        self.canvas.itemconfigure(self.Qin, text=str(round(Qin_num, 5)))
    def update_Wout(self, Wout_num):
        self.canvas.itemconfigure(self.Wout, text=str(round(Wout_num, 5)))


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
        self.dia.set_ylim(10, 150)
        self.dia.set_xlim(0.9, 1.9)
        self.dia.grid()
        
        self.toolbar = NavigationToolbar2Tk(self.canvas, master)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        [self.dia.add_line(i) for i in calc_SaturationofCurve()]
        self.state_point = Line2D([], [], color='g', linestyle='None', marker='o')
        self.line1 = Line2D([], [], color="g", lw=2.0)
        self.line2 = Line2D([], [], color="g", lw=2.0)
        self.line3 = Line2D([], [], color="g", lw=2.0)
        self.line4 = Line2D([], [], color="g", lw=2.0)
        
        self.heat = Line2D([], [], color="r", lw=2.0)
        self.cool = Line2D([], [], color="b", lw=2.0)
        
        self.dia.add_line(self.state_point)
        self.allofline = [self.line1, self.line2, self.line3, self.line4]
        self.hx = [self.heat, self.cool] 
        
        for i in self.allofline:
            self.dia.add_line(i)
        for i in self.hx:
            self.dia.add_line(i)
        
        
    def set_window_boundary(self):
        self.dia.set_ylim(10, 150)
        self.dia.set_xlim(0.9, 1.9)
        
    def updata_state_point(self, data):
        self.state_point.set_xdata(data[0])
        self.state_point.set_ydata(data[1])
        
    def updata_line(self, data):
        for i in range(len(data)):
            self.allofline[i].set_xdata(data[i][0])
            self.allofline[i].set_ydata(data[i][1])
    
    def updata_linehx(self, data):
        for i in range(len(data)):
            self.hx[i].set_xdata(data[i][0])
            self.hx[i].set_ydata(data[i][1])


def scan_data():
# =============================================================================
# load the data
# =============================================================================
    probe_type_TEMP, type_TEMP, ch_TEMP = 'TCouple', 'T', '@201:210'
    range_PRESS,resolution_PRESS, ch_PRESS  = 10, 5.5, '@301:306'
    gain_PRESS, state_PRESS = 2.1, 1
#    offset_PRESS, label_PRESS = 0, 'BAR'
    
    pumpi = {'name' : 'pump_inlet',         'nid' : 1}
    pumpo = {'name' : 'pump_ioutlet',       'nid' : 2}
    EXPi  = {'name' : 'expander_inlet',     'nid' : 3}
    EXPo  = {'name' : 'expander_outlet',    'nid' : 4}
    
    HI = {'name' : 'heat_inlet',       'nid' : 5}
    HO = {'name' : 'heat_outlet',      'nid' : 6}
    CI = {'name' : 'condenser_inlet',  'nid' : 7}
    CO = {'name' : 'condenser_outlet', 'nid' : 8}
    
    rm = visa.ResourceManager()
    v34972A = rm.open_resource('USB0::0x0957::0x2007::MY49017447::0::INSTR') 
#        idn_string = v34972A.query('*IDN?')
    
    def calc(readings_TEMP, readings_PRESS):
# =========================================================
# define the  of all point & init all node
# =========================================================
        dev_list = [pumpi, pumpo, EXPi, EXPo]
        HX = [HI, HO, CI, CO]
        for i in range(4):
            dev_list[i]['P'] = readings_PRESS[i]
            dev_list[i]['T'] = readings_TEMP[i]
        for i in range(4):
            HX[i]['T'] = readings_TEMP[i+6]

        global nodes
        nodes = []
        for i in dev_list:
            nodes.append(node.Node(i['name'], i['nid']))
            
        for i, obj in enumerate(dev_list):
            nodes[i].set_tp(obj['T'], obj['P'])
            nodes[i].pt()
        global nodes_HX
        nodes_HX = []
        for i in HX:
            nodes_HX.append(node.Node(i['name'], i['nid']))
        for i, obj in enumerate(HX):
            nodes_HX[i].t = obj['T']
        nodes_HX[0].s = nodes[2].s + 0.03
        nodes_HX[1].s = nodes[0].s - 0.03 
        nodes_HX[2].s = nodes[0].s - 0.03 
        nodes_HX[3].s = nodes[2].s + 0.03
        
        
        
        def left(nodes):
            
            global SM_dia
            for i in range(len(nodes)):
                SM_dia.update_state(i, nodes[i])
            eff = ((nodes[2].h-nodes[3].h)/(nodes[2].h-nodes[1].h))*100
            SM_dia.update_eff(eff)
            mdot = 0.23*4.2*(nodes_HX[0].t-nodes_HX[1].t)/(nodes[2].h-nodes[1].h)
            SM_dia.update_mdot(mdot)
            Qin = mdot * (nodes[2].h - nodes[1].h)
            Wout = mdot * (nodes[2].h - nodes[3].h)
            SM_dia.update_Qin(Qin)
            SM_dia.update_Wout(Wout)
            
        def right(nodes):
#            ORC_status([nodes[i] for i in range(len(nodes))])
            state_data = calc_StatusofORC(nodes, [0, 1, 2, 3])
            process = [ProcessPlot(0, 1, 'isos'),
                       ProcessPlot(1, 2, 'isop'),
                       ProcessPlot(2, 3, 'isos'),
                       ProcessPlot(3, 0, 'isop')]
            
            line_data = [plot.plot_process_data(nodes) for plot in process]
            line_datahx = [[[nodes_HX[0].s, nodes_HX[1].s], [nodes_HX[0].t, nodes_HX[1].t]], [[nodes_HX[2].s, nodes_HX[3].s], [nodes_HX[2].t, nodes_HX[3].t]]]
            global TH_dia
            TH_dia.updata_state_point(state_data)
            TH_dia.updata_line(line_data)
            TH_dia.updata_linehx(line_datahx)
            

            TH_dia.canvas.draw()
            
        left(nodes)
        right(nodes)

        

    def innerfunc():
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
        calc(readings_TEMP, readings_PRESS)
    

    timer(innerfunc, 3,)



def timer(func, second=2, *arg):
    func(*arg)
    t = Timer(second, timer, args=(func, 3, *arg))
    t.setDaemon(True)
    
    global on_click_loop
#    print(t.daemon, on_click_loop)
    if t.daemon and on_click_loop:
        t.start()
    else:
#        del readings_TEMP, readings_PRESS
        return 0

            
#def smliu_scan_data():
#    print('load data')
#
#    def innerfunc():
#        global x
#        
#        print('get and update the data', x)
#        
#    timer(innerfunc, 3,)
    
        
        
if __name__=='__main__':
    window = tk.Tk()
    window.title("Lab429, ORC for 500W, author:wei")
    w = tk.Label(window, text='this is ORC_GUI').pack()
    
    frame = tk.Frame(window).pack()
    
    
    # left and right frame
    frm_right = tk.Frame(frame)
    frm_right.pack(side='right')
#    tk.Label(frm_right, text='frame right').pack()

    frm_left = tk.Frame(frame)
    frm_left.pack(side='left')
#    tk.Label(frm_left, text='frame left').pack()
    
    
    # top and bottom of right frame
    frm_right_top = tk.Frame(frm_right)
    frm_right_top.pack(side='top')
#    tk.Label(frm_right_top, text='frame right top').pack()
    frm_right_bottom = tk.Frame(frm_right)
    frm_right_bottom.pack(side='bottom')
#    tk.Label(frm_right_bottom, text='frame right bottom').pack()
    
    
    SM_dia = ORC_Status(frm_left)
    TH_dia = ORC_Figure(frm_right_top)

#    x = 0
    
    
    var = tk.StringVar()
    l = tk.Label(frm_right_bottom, textvariable=var, bg='white', \
                 font=('Arial', 12), width=15, height=2)
    l.pack()
    
    on_click_loop = False
    def btn_cmd_loop(func):
        global on_click_loop
        if on_click_loop == False:
            on_click_loop = True
            var.set('start2scan')
            func()
        else:
            on_click_loop = False
            var.set('stop2scan')
            
    def btn_cmd_one(func):
        func()
        
        
            
    b = tk.Button(frm_right_bottom, text='click me', width=15, height=2, \
                  command=lambda: btn_cmd_loop(scan_data))
    b.pack()
    
#    kkk = tk.Button(frm_right_bottom, text='scan', width=15, height=2, \
#                  command=lambda: btn_cmd_loop(SM_dia.update_state))
#    kkk.pack()
#
#    
#    init_boundary = tk.Button(frm_right_bottom, text='init_boundary', width=15, height=2, \
#                  command=lambda: btn_cmd_one(TH_dia.set_window_boundary))
#    init_boundary.pack()
    
    
    window.mainloop()

    
    
    

    

