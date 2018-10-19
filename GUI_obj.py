#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 00:24:49 2018

@author: wei
"""

"""
=================
Animated subplots
=================

This example uses subclassing, but there is no reason that the proper function
couldn't be set up and then use FuncAnimation. The code is long, but not
really complex. The length is due solely to the fact that there are a total of
9 lines that need to be changed for the animation as well as 3 subplots that
need initial set up.

"""
import tkinter as tk
import tkinter.font as tkfont
#import numpy as np
#import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
from ORC_plot import calc_SaturationofCurve

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
        self.dia.set_ylim(10, 160)
        self.dia.set_xlim(0.9, 2)
        self.dia.grid()
        
        self.toolbar =NavigationToolbar2Tk(self.canvas, master)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        [self.dia.add_line(i) for i in calc_SaturationofCurve()]
    
    def good():
        pass
#        self.line2 = Line2D([], [], color='blue', marker='o')
#        self.line2a = Line2D([], [], color='blue', marker='o')
#        self.line2e = Line2D([], [], color='blue', marker='o')
#        self.dia.add_line(self.line2)
#        self.dia.add_line(self.line2a)
#        self.dia.add_line(self.line2e)
###
###
###
#        self.line3 = Line2D([], [], color='green')
#        self.line3a = Line2D([], [], color='green', linewidth=2)
#        self.line3e = Line2D([], [], color='green', marker='o', markeredgecolor='r')
#        self.dia.add_line(self.line3)
#        self.dia.add_line(self.line3a)
#        self.dia.add_line(self.line3e)
#       
#        self.canvas.show()
#
#        animation.TimedAnimation.__init__(self, self.fig, interval=50, blit=True)
#
#    def _draw_frame(self, framedata):
#        i = framedata
#        head = i - 1
#        head_slice = (self.t > self.t[i] - 1.0) & (self.t < self.t[i])
#
#        self.line1.set_data(self.x[:i], self.y[:i])
#        self.line1a.set_data(self.x[head_slice], self.y[head_slice])
#        self.line1e.set_data(self.x[head], self.y[head])
#
#        self.line2.set_data(self.y[:i], self.z[:i])
#        self.line2a.set_data(self.y[head_slice], self.z[head_slice])
#        self.line2e.set_data(self.y[head], self.z[head])
#
#        self.line3.set_data(self.x[:i], self.z[:i])
#        self.line3a.set_data(self.x[head_slice], self.z[head_slice])
#        self.line3e.set_data(self.x[head], self.z[head])
#
#        self._drawn_artists = [self.line1, self.line1a, self.line1e,
#                               self.line2, self.line2a, self.line2e,
#                               self.line3, self.line3a, self.line3e]

        

        
        
if __name__=='__main__':
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
    
    a = ORC_Figure(frm_right)
#    ORC_Status(frm_left)
#    a.dia.add_line(Line2D([0, 100], [0, 100], color='blue', marker='o'))
    
    window.mainloop()
