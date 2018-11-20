#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 00:24:49 2018

@author: wei
"""

        
if __name__=='__main__':
    import tkinter as tk
    from GUIObj import ORC_Figure, ORC_Status, scan_data, test_scan_data, SendData, timer
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
    data = SendData()
    
    frm_right_bottom_left = tk.Frame(frm_right_bottom)
    frm_right_bottom_left.pack(side='left')
    frm_right_bottom_right = tk.Frame(frm_right_bottom)
    frm_right_bottom_right.pack(side='right')    
    
    varScan = tk.StringVar()
    labelScan = tk.Label(frm_right_bottom_left, textvariable=varScan, bg='white', \
                 font=('Arial', 12), width=15, height=2)
    labelScan.pack()

    varmdotWater = tk.StringVar()
    labelmdotWater = tk.Label(frm_right_bottom_right, textvariable=varmdotWater, bg='white', \
                 font=('Arial', 12), width=15, height=2)
    labelmdotWater.pack()
    
    on_click_loop = False
    def btn_cmd_loop(func):
        global on_click_loop
        if on_click_loop == False:
            on_click_loop = True
            varScan.set('start2scan')
            func(data, SM_dia, TH_dia)
        else:
            on_click_loop = False
            varScan.set('stop2scan')

            
    def btn_cmd_one(func):
        func()
    
    def good():
        mdotWater = varmdotWater.get()
#        print(mdotWater, type(mdotWater))
        SM_dia.update_mdotWater(float(mdotWater))
        data.update_mdotWater(float(mdotWater))
        labelmdotWater.config(text=str(mdotWater))
        
            
    buttonScan = tk.Button(frm_right_bottom_left, text='click me', width=15, height=2, \
                  command=lambda: btn_cmd_loop(test_scan_data))
    buttonScan.pack()
    
    g = tk.Radiobutton(frm_right_bottom_right, text='熱水大流量',  variable=varmdotWater, value=0.29, \
                  command=good)
    g.pack()
    gg = tk.Radiobutton(frm_right_bottom_right, text='熱水中流量', variable=varmdotWater, value=0.23, \
                  command=good)
    gg.pack()
    ggg = tk.Radiobutton(frm_right_bottom_right, text='熱水小流量', variable=varmdotWater, value=0.17, \
                  command=good)
    ggg.pack()
#    kkk = tk.Button(frm_right_bottom, text='scan', width=15, height=2, \
#                  command=lambda: btn_cmd_loop(SM_dia.update_state))
#    kkk.pack()
#
#    
#    init_boundary = tk.Button(frm_right_bottom, text='init_boundary', width=15, height=2, \
#                  command=lambda: btn_cmd_one(TH_dia.set_window_boundary))
#    init_boundary.pack()
    
    
    window.mainloop()

    
    
    

    

