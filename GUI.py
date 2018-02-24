#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 23:03:37 2018

@author: wei
"""
import tkinter as tk
#import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
#from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
#matplotlib.use('TkAgg')

from CoolProp.CoolProp import PropsSI
import numpy as np
from unit import  T, pps
from node import Node
from ORC_sample import data
from ORC_plot import ProcessPlot
#from matplotlib.gridspec import GridSpec

window = tk.Tk()
window.title("matplotlib into tk")
tk.Label(window, text='this is ORC_GUI, window top').pack()

frm = tk.Frame(window)
frm.pack()
#tk.Label(frm, text='frame top').pack()
#
#txt = '''  nodeID  name                 p (bar)    t (c)    h (KJ/Kg)    s ((KJ/Kg)*K)    d (Kg/m^3)  q             over
#--------  -----------------  ---------  -------  -----------  ---------------  ------------  ----------  ------
#       1  pump_inlet              2.01    21.86      228.331           1.0994      1347.24   subcool      -11.6
#       2  pump_ioutlet            6.44    22.55      229.373           1.1018      1346.72   subcool      -49.5
#       3  evaparator_outlet       6.11    88.31      475.503           1.8317        30.912  supderheat    18.2
#       4  expander_inlet          6.27    88.28      475.138           1.8293        31.856  supderheat    17.2
#       5  expander_outlet         2.05    64.03      458.841           1.8464        10.309  supderheat    30
#       6  condenser_inlet         1.99    56.68      451.762           1.8269        10.268  supderheat    23.5
#       7  condenser_outlet        1.98    22.12      228.673           1.1005      1346.53   subcool      -10.9'''
#bg='white',     # 背景颜色
#font=('Helvetica', 12)     # 字体和字体大小


frm_left = tk.Frame(frm)
frm_left.pack(side='left')
tk.Label(frm_left, text='frame left').pack(side='top')
# create the canvas, size in pixels
canvas = tk.Canvas(master=frm_left, width = 1024, height = 724, bg = 'white')
# pack the canvas into a frame/form

# load the .gif image file, put gif file here
gif1 = tk.PhotoImage(file = '500w_P&ID.png') # test gif, png and jpg, jpg can't use
# put gif image on canvas
# pic's upper left corner (NW) on the canvas is at x=50 y=10
canvas.create_image(0, 0, image = gif1, anchor = tk.NW)
canvas.create_text(100,110, text = '1_T', fill = 'blue', font=("Arial", 12))  
canvas.create_text(100,126,text = '1_P', fill = 'blue', font=("times new roman", 12))  
canvas.pack(expand = 1, fill = tk.BOTH) #???
#tk.Label(frm_left, text=txt, bg=bg, font=font).pack(side='top')

frm_right = tk.Frame(frm)
frm_right.pack(side='right')
tk.Label(frm_right, text='frame right').pack()

# set figure
fig = Figure(figsize=(8,6), dpi=100)

#gs = GridSpec(4, 3)
#dia = fig.add_subplot(gs[0:3, :], facecolor='w') # projection='polar'
dia = fig.add_subplot(111)
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
canvas = FigureCanvasTkAgg(fig, master=frm_right)
canvas.show()
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1) # side=tk.BOTTOM
#canvas.get_tk_widget().grid(row=0, columnspan=3)

# define quit button, quit & kill the window
def _quit():
    window.quit()
    window.destroy()
button =tk.Button(master=frm_right, text='Quit', command=_quit)
button.pack(side=tk.RIGHT)


# push tool of matplotlib into tkinter window
toolbar =NavigationToolbar2TkAgg(canvas, frm_right)
toolbar.update()
canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

'''
# define keyboard event
def on_key_event(event):
    print('you pressed %s'% event.key)
    key_press_handler(event, canvas, toolbar)
canvas.mpl_connect('key_press_event', on_key_event)
'''


window.mainloop()
#%%
"""
# test to Put a gif image on a canvas with tkinter
import tkinter as tk

# create the canvas, size in pixels
canvas = tk.Canvas(width = 1024, height = 724, bg = 'white')
# pack the canvas into a frame/form
# load the .gif image file, put gif file here
gif1 = tk.PhotoImage(file = '500w_P&ID.png') # test gif, png and jpg, jpg can't use
# put gif image on canvas
# pic's upper left corner (NW) on the canvas is at x=50 y=10
canvas.create_image(0, 0, image = gif1, anchor = tk.NW)
canvas.pack(expand = tk.YES, fill = tk.BOTH) #???

tk.mainloop()
"""
#%%
"""
# try to put jpg image on canvas
import tkinter as tk 
from PIL import Image, ImageTk  
 
canvas = tk.Canvas(width = 1800, height = 1000, bg = 'black')     
image = Image.open("500w_P&ID.jpg")  
jpg = ImageTk.PhotoImage(image)  
  
canvas.create_image(300,50,image = jpg, anchor=tk.NW)    
canvas.create_text(350,120, text = 'Use Canvas', fill = 'gray')
canvas.create_text(300,75, text = 'Use Canvas', fill = 'blue')  
canvas.pack()
tk.mainloop()  
"""