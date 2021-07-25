#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 00:24:49 2018

@author: wei
"""


def main():
    '''layout'''
    from tkinter import Tk, Frame, Label
    from GUIObj import ORC_Figure, P_I_Diagram, Scan_button
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

    ''' right and left of right_bottom frame '''
    # frm_right_bottom_left = Frame(frm_right_bottom)
    # frm_right_bottom_left.pack(side='left')
    # tk.Label(frm_right_bottom_left, text='frame right bottom left').pack()
    
    ''' componement'''
        
    PID = P_I_Diagram(frm_left)
    Ts = ORC_Figure(frm_right_top)
    Scan_button(frm_right_bottom, PID.update, Ts.update)
    Label(frm_left, text="mDot").pack(side='right')
    Label(frm_left, text='developer:HW Lu, LAB:429, professor:TC Hung, agency:Taipei Tech University').pack(side='left')

    # frm_right_bottom_right = Frame(frm_right_bottom)
    # frm_right_bottom_right.pack(side='right')
    # tk.Label(frm_right_bottom_right, text='frame right bottom right').pack()

    window.bind("<Escape>", lambda x: window.destroy())


#     def btn_cmd_one(func):
#         func()

#     def good():
#         mdotWater = varmdotWater.get()
# #        print(mdotWater, type(mdotWater))
#         SM_dia.update_mdotWater(float(mdotWater))
#         data.update_mdotWater(float(mdotWater))
#         labelmdotWater.config(text=str(mdotWater))


#     g = tk.Radiobutton(frm_right_bottom_right, text='熱水大流量',  variable=varmdotWater, value=0.29, \
#                   command=good)
#     g.pack()
#     gg = tk.Radiobutton(frm_right_bottom_right, text='熱水中流量', variable=varmdotWater, value=0.23, \
#                   command=good)
#     gg.pack()
#     ggg = tk.Radiobutton(frm_right_bottom_right, text='熱水小流量', variable=varmdotWater, value=0.17, \
#                   command=good)
#     ggg.pack()

    window.mainloop()


if __name__ == '__main__':
    main()
