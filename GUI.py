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
        self.frame = Frame(self).pack()

    def add_label(self):
        Label(self.frame, text='frame').pack()


if __name__ == '__main__':

    # if (window.winfo_exists()): window.destroy()
    # from log import logger

    # logger.info('program starting!')
    # logger.info('load database')
    # logger.info('create realtime shell')
    # import db

    # logger.info('create layout')

    # '''layout'''
    from tkinter import Tk, Frame, Label

    window = Tk()

    app = App()
    app.add_label()
    # frame = Frame(app).pack()
    # Label(frame, text='frame').pack()

    # ''' left and right frame '''
    # frm_right = Frame(frame)
    # frm_right.pack(side='right')
    # Label(frm_right, text='frame right').pack()

    # frm_left = Frame(frame)
    # frm_left.pack(side='left')
    # Label(frm_left, text='frame left').pack()

    # ''' top and bottom of right frame '''
    # frm_right_top = Frame(frm_right)
    # frm_right_top.pack(side='top')
    # Label(frm_right_top, text='frame right top').pack()

    # frm_right_bottom = Frame(frm_right)
    # frm_right_bottom.pack(side='bottom')
    # Label(frm_right_bottom, text='frame right bottom').pack()

    # Label(frm_left, text='developer:HW Lu, LAB:429, professor:TC Hung, agency:Taipei Tech University').pack(
    #     side='bottom')

    # logger.info('add XXX in layout')
    # ''' componement'''
    # from GUIObj import ORC_Figure, P_I_Diagram, Scan_button, mDot_simulation
    # PID = P_I_Diagram(frm_left)
    # Ts = ORC_Figure(frm_right_top)
    # mDot_simulation(frm_left)
    # Scan_button(frm_right_bottom, PID.update, Ts.update)
    # # Scan_button(frm_right_bottom)

    window.bind("<Escape>", lambda x: window.destroy())

    window.mainloop()

    # logger.info('program finish.')
