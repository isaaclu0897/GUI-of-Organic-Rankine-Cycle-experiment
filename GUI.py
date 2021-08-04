#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 00:24:49 2018

@author: wei
"""

    

def main():
    '''layout'''
    from tkinter import Tk, Frame, Label
    from GUIObj import ORC_Figure, P_I_Diagram, Scan_button, mDot_simulation
    window = Tk()
    window.title("ORC Realtime System")

    frame = Frame(window).pack()
    Label(frame, text='frame').pack()

    ''' left and right frame '''
    frm_right = Frame(frame)
    frm_right.pack(side='right')
    Label(frm_right, text='frame right').pack()

    frm_left = Frame(frame)
    frm_left.pack(side='left')
    Label(frm_left, text='frame left').pack()

    ''' top and bottom of right frame '''
    frm_right_top = Frame(frm_right)
    frm_right_top.pack(side='top')
    Label(frm_right_top, text='frame right top').pack()

    frm_right_bottom = Frame(frm_right)
    frm_right_bottom.pack(side='bottom')
    Label(frm_right_bottom, text='frame right bottom').pack()

    ''' componement'''

    PID = P_I_Diagram(frm_left)
    # Label(frm_left, text="mDot").pack(side='right')
    Label(frm_left, text='developer:HW Lu, LAB:429, professor:TC Hung, agency:Taipei Tech University').pack(side='left')
    mDot_simulation(frm_left)

    Ts = ORC_Figure(frm_right_top)
    Scan_button(frm_right_bottom, PID.update, Ts.update)

    window.bind("<Escape>", lambda x: window.destroy())

    window.mainloop()


if __name__ == '__main__':
    from log import logger
    
    logger.info('program starting!')
    logger.info('load database')
    logger.info('create realtime shell')
    logger.info('create layout')
    logger.info('add XXX in layout')
    import db
    
    '''layout'''
    from tkinter import Tk, Frame, Label
    from GUIObj import ORC_Figure, P_I_Diagram, Scan_button, mDot_simulation
    window = Tk()
    window.title("ORC Realtime System")

    frame = Frame(window).pack()
    Label(frame, text='frame').pack()

    ''' left and right frame '''
    frm_right = Frame(frame)
    frm_right.pack(side='right')
    Label(frm_right, text='frame right').pack()

    frm_left = Frame(frame)
    frm_left.pack(side='left')
    Label(frm_left, text='frame left').pack()

    ''' top and bottom of right frame '''
    frm_right_top = Frame(frm_right)
    frm_right_top.pack(side='top')
    Label(frm_right_top, text='frame right top').pack()

    frm_right_bottom = Frame(frm_right)
    frm_right_bottom.pack(side='bottom')
    Label(frm_right_bottom, text='frame right bottom').pack()

    ''' componement'''

    PID = P_I_Diagram(frm_left)
    # Label(frm_left, text="mDot").pack(side='right')
    Label(frm_left, text='developer:HW Lu, LAB:429, professor:TC Hung, agency:Taipei Tech University').pack(side='left')
    mDot_simulation(frm_left)

    Ts = ORC_Figure(frm_right_top)
    Scan_button(frm_right_bottom, PID.update, Ts.update)

    window.bind("<Escape>", lambda x: window.destroy())

    window.mainloop()
    
    logger.info('program finish.')
