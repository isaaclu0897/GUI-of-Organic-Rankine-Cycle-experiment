#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 23:03:37 2018

@author: wei
"""
import tkinter as tk
import tkinter.font as tkfont
#import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
#matplotlib.use('TkAgg')

from CoolProp.CoolProp import PropsSI
import numpy as np
from unit import  T, pps
from node import Node
from ORC_sample import data
from ORC_plot import ProcessPlot, set_windows_GUI, calc_SaturationofCurve, calc_StatusofORC
#import matplotlib.pyplot as plt 



window = tk.Tk()

window.title("Lab429, ORC for 500W, author:wei")
w = tk.Label(window, text='this is ORC_GUI')
#w.config(height=10, size=20)
w.pack()

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
#tk.Label(frm_left, text='frame left').pack(side='top')
# create the canvas, size in pixels
canvas = tk.Canvas(master=frm_left, width = 1024, height = 724, bg = 'white')
# pack the canvas into a frame/form

# load the .gif image file, put gif file here
gif1 = tk.PhotoImage(file = './fig/500w_P&ID.png') # test gif, png and jpg, jpg can't use
# put gif image on canvas
# pic's upper left corner (NW) on the canvas is at x=50 y=10
canvas.create_image(0, 0, image = gif1, anchor = tk.NW)
k = 30
fontprop = tkfont.Font(family='courier 10 pitch', size=30)# bitstream charter or courier 10 pitch
fonteff = tkfont.Font(family='courier 10 pitch', size=50, weight='bold')# bitstream charter or courier 10 pitch

canvas.create_text(100,110, text = 'P', fill = 'blue', font=fontprop)  
canvas.create_text(100,110+k,text = 'T', fill = 'blue', font=fontprop)  

canvas.create_text(280,320, text = '429_ORC\neff: 3 %', fill = 'blue', font=fonteff)

canvas.pack(expand = 1, fill = tk.BOTH) #???
#tk.Label(frm_left, text=txt, bg=bg, font=font).pack(side='top')

frm_right = tk.Frame(frm)
frm_right.pack(side='right')
#tk.Label(frm_right, text='frame right').pack()

# set figure


# set label 
dia, fig = set_windows_GUI()
# plot Saturation of Curve
sat_line = calc_SaturationofCurve()
dia.add_line(sat_line[0])
dia.add_line(sat_line[1])
#
#
## import data
#dev_list = [pumpi, pumpo, EVPo, EXPi, EXPo, CDSi, CDSo] = data()
#
## init node
#nodes = [Node(i["name"], i["nid"]) for i in dev_list]
#for i, obj in enumerate(dev_list):
#    nodes[i].set_tp(obj["T"], obj["P"])
#    nodes[i].pt()


# plot status of ORC
#    plot_StatusofORC(nodes)
state_point = calc_StatusofORC(nodes, [1, 2, 3, 4])
dia.add_line(state_point)
""" example
ProcessPlot(0, 1, 'isos').plot_process
a=ProcessPlot(3, 4, 'isos')
a.iso_line(nodes)
a.calc_iso()
a.plot_iso()
plot process of ORC
"""
#process = [ProcessPlot(0, 1, 'isos'),
#           ProcessPlot(1, 2, 'isop'),
#           ProcessPlot(2, 3, 'isop'),
#           ProcessPlot(3, 4, 'isos'),
#           ProcessPlot(4, 5, 'isop'),
#           ProcessPlot(5, 6, 'isop'),
#           ProcessPlot(6, 0, 'isop')]
#good = [plot.plot_process(nodes) for plot in process]
#
#for i in good:
#    dia.add_line(i[0])
#    dia.add_line(i[1])
#
#plt.show()


# push figure to tkinter window
canvas = FigureCanvasTkAgg(fig, master=frm_right)
#canvas.show()


canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1) # side=tk.BOTTOM
#canvas.get_tk_widget().grid(row=0, columnspan=3)
#window.mainloop()
##%%


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

# define keyboard event
def on_key_event(event):
    print('you pressed %s'% event.key)
    key_press_handler(event, canvas, toolbar)
canvas.mpl_connect('key_press_event', on_key_event)


window.mainloop()
##%
#"""
## test to Put a gif image on a canvas with tkinter
#import tkinter as tk
#
## create the canvas, size in pixels
#canvas = tk.Canvas(width = 1024, height = 724, bg = 'white')
## pack the canvas into a frame/form
## load the .gif image file, put gif file here
#gif1 = tk.PhotoImage(file = '500w_P&ID.png') # test gif, png and jpg, jpg can't use
## put gif image on canvas
## pic's upper left corner (NW) on the canvas is at x=50 y=10
#canvas.create_image(0, 0, image = gif1, anchor = tk.NW)
#canvas.pack(expand = tk.YES, fill = tk.BOTH) #???
#
#tk.mainloop()
#"""
##%
#"""
## try to put jpg image on canvas
#import tkinter as tk 
#from PIL import Image, ImageTk  
# 
#canvas = tk.Canvas(width = 1800, height = 1000, bg = 'black')     
#image = Image.open("500w_P&ID.jpg")  
#jpg = ImageTk.PhotoImage(image)  
#  
#canvas.create_image(300,50,image = jpg, anchor=tk.NW)    
#canvas.create_text(350,120, text = 'Use Canvas', fill = 'gray')
#canvas.create_text(300,75, text = 'Use Canvas', fill = 'blue')  
#canvas.pack()
#tk.mainloop()  
#"""