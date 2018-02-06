#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 23:03:37 2018

@author: wei
"""

import tkinter as Tk
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
matplotlib.use('TkAgg')

from CoolProp.CoolProp import PropsSI
import numpy as np
from unit import  T, pps
from node import Node
from ORC_sample import data
from ORC_plot import ProcessPlot
from matplotlib.gridspec import GridSpec

window = Tk.Tk()
window.title("matplotlib into TK")

# set figure
fig = Figure(figsize=(16,9), dpi=100)

gs = GridSpec(16, 9)
dia = fig.add_subplot(gs[0:11, 5:], facecolor='w') # projection='polar'
'''
b = fig.add_subplot(gs[0, 0])
r = [1, 2, 3]
t = [5, 5, 7]
b.plot(r, t)
b = fig.add_subplot(gs[1, :-1])
b.plot(r, t)
b = fig.add_subplot(gs[:, 1])
'''

xAxis = "s" 
yAxis = "T" 
title = {"T": "T, °C", "s": "s, (kJ/kg)*K"} 

dia.set_title("%s-%s Diagram" %(yAxis, xAxis))
dia.set_xlabel(title[xAxis])
dia.set_ylabel(title[yAxis])
#    plt.ylim(15, 90)
#    plt.xlim(1.05, 1.88)
dia.set_ylim(10, 135)
dia.set_xlim(1.05, 1.88)
dia.grid()

# plot figure
fluid = 'REFPROP::R245FA'
num = 50
tcrit = PropsSI("Tcrit", fluid) - 0.00007 
tmin = PropsSI("Tmin", fluid) 
T_array = np.linspace(tmin, tcrit, num) 
X_array = np.array([0, 1.0])

for x in X_array:
    S = np.array([PropsSI("S", "Q", x, "T", t, "REFPROP::R245FA") for t in T_array]) 
    
    dia.plot(pps.J2KJ(S), T.K2C(T_array), "r", lw=2.0)

# import data
dev_list = [pumpi, pumpo, EVPo, EXPi, EXPo, CDSi, CDSo] = data()
dev = {'pumpi' : pumpi,
       'pumpo' : pumpo,
       'EVPo' : EVPo, 
       'EXPi' : EXPi, 
       'EXPo' : EXPo, 
       'CDSi' : CDSi, 
       'CDSo' : CDSo}

# init node
nodes = [Node(i["name"], i["nid"]) for i in dev_list]
for i, obj in enumerate(dev_list):
    nodes[i].set_tp(obj["T"], obj["P"]) 
    nodes[i].pt()

# plot status of ORC
t = []; s = []
for i in range(len(nodes)): 
    t.append(nodes[i].t) 
    s.append(pps.J2KJ(nodes[i].s))

dia.plot(s, t, 'bo')

process = [ProcessPlot(0, 1, 'isos'),
           ProcessPlot(1, 2, 'isop'),
           ProcessPlot(2, 3, 'isop'),
           ProcessPlot(3, 4, 'isos'),
           ProcessPlot(4, 5, 'isop'),
           ProcessPlot(5, 6, 'isop'),
           ProcessPlot(6, 0, 'isop')]
for b in process:
    b.iso_line(nodes)
    b.calc_iso()
    
    dia.plot(pps.J2KJ(b.sa), T.K2C(b.ta), "b")

# push figure to tkinter window
canvas =FigureCanvasTkAgg(fig, master=window)
canvas.show()
canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
#canvas.get_tk_widget().grid(row=0, columnspan=3)

# push tool of matplotlib into tkinter window
toolbar =NavigationToolbar2TkAgg(canvas, window)
toolbar.update()
canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

# define keyboard event
def on_key_event(event):
    print('you pressed %s'% event.key)
    key_press_handler(event, canvas, toolbar)
canvas.mpl_connect('key_press_event', on_key_event)

# define quit button, quit & kill the window
def _quit():
    window.quit()
    window.destroy()
button =Tk.Button(master=window, text='Quit', command=_quit)
button.pack(side=Tk.BOTTOM)

window.mainloop()
