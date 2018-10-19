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
import visa
import node

class ORC_Status(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master=None)
        
        # create the canvas, size in pixels
        self.canvas = tk.Canvas(master, width = 1024, height = 724, bg = 'white')
        # load the .gif image file, put gif file here
        self.gif1 = tk.PhotoImage(file = './fig/500w_P&ID.png') # test gif, png and jpg, jpg can't use
        print(self.gif1)
        # put gif image on canvas
        # pic's upper left corner (NW) on the canvas is at x=50 y=10
        self.canvas.create_image(0, 0, image=self.gif1, anchor=tk.NW)
        
        k = 30
        fontprop = tkfont.Font(family='courier 10 pitch', size=30)# bitstream charter or courier 10 pitch
        fonteff = tkfont.Font(family='courier 10 pitch', size=50, weight='bold')# bitstream charter or courier 10 pitch
        
        self.canvas.create_text(100,110, text = 'P', fill = 'blue', font=fontprop)  
        self.canvas.create_text(100,110+k,text = 'T', fill = 'blue', font=fontprop)  
        
        self.canvas.create_text(280,320, text = '429_ORC\neff: 3 %', fill = 'blue', font=fonteff)
        
        self.canvas.pack(expand = 1, fill = tk.BOTH) #???
        
        #tk.Label(frm_left, text=txt, bg=bg, font=font).pack(side='top')


class ORC_Figure(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master=None)
        
        self.fig = Figure(figsize=(8,6), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master)
        
#        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)
        self.dia = self.fig.add_subplot(111)
        xAxis = "s" 
        yAxis = "T" 
        title = {"T": "T, °C", "s": "s, (kJ/kg)*K"} 
        self.dia.set_title("%s-%s Diagram" %(yAxis, xAxis))
        self.dia.set_xlabel(title[xAxis])
        self.dia.set_ylabel(title[yAxis])
        self.dia.set_ylim(10, 150)
        self.dia.set_xlim(0.9, 1.9)
        self.dia.grid()
        
        self.toolbar =NavigationToolbar2Tk(self.canvas, master)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        [self.dia.add_line(i) for i in calc_SaturationofCurve()]
        self.state_point = Line2D([], [], color='b', linestyle='None', marker='o')
        self.dia.add_line(self.state_point)
    

def scan_data():
    rm = visa.ResourceManager()
    v34972A = rm.open_resource('USB0::0x0957::0x2007::MY49017447::0::INSTR') 
#        idn_string = v34972A.query('*IDN?')

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
        
# =========================================================
# define the  of all point & init all node
# =========================================================
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
#            ORC_status([nodes[i] for i in range(len(nodes))])
        xdata, ydata = calc_StatusofORC(nodes, [0, 1, 2, 3])

        global a
        a.state_point.set_xdata(xdata)
        a.state_point.set_ydata(ydata)
        print(a.dia.lines)
        
        a.canvas.draw()
    timer(innerfunc, 3,)

def timer(func, second=2, *arg):
    func(*arg)
    t = Timer(second, timer, args=(func, 3, *arg))
    t.setDaemon(True)

    if t.daemon:
        t.start()
    else:
#        print('else')
#        print(readings_TEMP, readings_PRESS)
        del readings_TEMP, readings_PRESS
        return 0

            

    
        
        
if __name__=='__main__':
    # =============================================================================
    # load the data
    # =============================================================================
    probe_type_TEMP, type_TEMP, ch_TEMP = 'TCouple', 'T', '@201:210'
    range_PRESS,resolution_PRESS, ch_PRESS  = 10, 5.5, '@301:306'
    gain_PRESS, offset_PRESS, label_PRESS, state_PRESS = 2.1, 0, 'BAR', 1
    pumpi = {'name' : 'pump_inlet',         'nid' : 1}
    pumpo = {'name' : 'pump_ioutlet',       'nid' : 2}
    EXPi  = {'name' : 'expander_inlet',     'nid' : 3}
    EXPo  = {'name' : 'expander_outlet',    'nid' : 4}
#    CDSi  = {'name' : 'condenser_inlet',    'nid' : 5}
#    CDSo  = {'name' : 'condenser_outlet',   'nid' : 6}
    
    window = tk.Tk()
    window.title("Lab429, ORC for 500W, author:wei")
    w = tk.Label(window, text='this is ORC_GUI').pack()
    
    frame = tk.Frame(window).pack()
    
    frm_right = tk.Frame(frame)
    frm_right.pack(side='right')              
    tk.Label(frm_right, text='frame right').pack()

    frm_left = tk.Frame(frame)
    frm_left.pack(side='left')
    tk.Label(frm_left, text='frame left').pack()
    
    #    ORC_Status(frm_left)
    a = ORC_Figure(frm_right)
    
    
    var = tk.StringVar()
    l = tk.Label(window, textvariable=var, bg='green', font=('Arial', 12), width=15, height=2)
#    #l = tk.Label(window, text='OMG! this is TK!', bg='green', font=('Arial', 12), width=15, height=2)
    l.pack()
    on_hit = False
    def hit_me():
        global on_hit
        if on_hit == False:
            on_hit = True
            var.set('start2scan')
            scan_data()
            
    b = tk.Button(window, text='hit me', width=15, height=2, command=hit_me)
    b.pack()
    
    
    window.mainloop()

    
    
    

    

