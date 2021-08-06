#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 00:24:49 2018

@author: wei
"""

# import tkinter as tk
from tkinter import Tk, Frame, Label


class App(Frame):
    def __init__(self, master=None):
        super().__init__(master=None)

        self.initUI()

    def initUI(self):
        self.master.title("ORC Realtime System")
        
        main = Frame(self.master)
        main.pack()
        footer = Frame(self.master)
        footer.pack()
        
        Label(footer, text='developer:HW Lu, laboratory:429, professor:TC Hung, agency:National Taipei Technology University').pack()
        
        self.frame_left = Frame(main)
        self.frame_left.pack(side="left")
        
        frame_right = Frame(main)
        frame_right.pack(side="right")
        
        self.frame_ts = Frame(frame_right)
        self.frame_ts.pack(side="top")
        
        self.frame_right = Frame(frame_right)
        self.frame_right.pack(side="bottom")
        

    def add_label(self):
        Label(self.frame_left, text='frame_left').pack()
        Label(self.frame_ts, text='frame_ts').pack()
        Label(self.frame_right, text='frame_right').pack()
        


if __name__ == '__main__':

    from log import logger

    logger.info('program starting!')
    logger.info('load database')
    logger.info('create realtime shell')
    import db

    logger.info('create layout')

    # '''layout'''
    from tkinter import Tk, Frame, Label

    window = Tk()

    app = App()
    app.add_label()

    logger.info('add XXX in layout')
    # ''' componement'''
    from GUIObj import ORC_Figure, P_I_Diagram, Scan_button, mDot_simulation
    PID = P_I_Diagram(app.frame_left)
    mDot_simulation(app.frame_left)
    Ts = ORC_Figure(app.frame_ts)
    Scan_button(app.frame_right, PID.update, Ts.update)

    window.bind("<Escape>", lambda x: window.destroy())

    window.mainloop()

    logger.info('program finish.')
