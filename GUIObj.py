#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 15:01:08 2018

@author: wei
"""

from tkinter import Frame, StringVar, Label, Button


from threading import Thread


def thread_func(func, *args):
    # print("thread")
    t = Thread(target=func, args=args, name=f"{func.__name__}")
    t.setDaemon(True)
    t.start()


class Scan_button(Frame):
    def __init__(self, master=None, *callbacks):
        Frame.__init__(self, master=None)

        # add callbacks funs into list
        self.update_funcs = []
        for func in callbacks:
            if callable(func):
                self.update_funcs.append(func)
            else:
                def func(): print("this is not a func")
                self.update_funcs.append(func)

        self.is_click = False

        def btn_cmd_loop(func):
            if self.is_click:
                self.is_click = False
                varScan.set('stop2scan')
            else:
                self.is_click = True
                varScan.set('start2scan')
                func()

        varScan = StringVar()
        varScan.set('stop2scan')

        labelScan = Label(
            master,
            textvariable=varScan,
            bg='white',
            font=('Arial', 12),
            width=15, height=2)
        labelScan.pack()

        button = Button(
            master,
            text='click me',
            width=15, height=2,
            command=lambda: btn_cmd_loop(self.th_update))
        button.pack()

    def call_update_funcs(self):
        for func in self.update_funcs:
            func()

    def th_update(self):
        thread_func(self.update)

    def update(self):
        if self.is_click:
            self.after(500, self.th_update)
            ''' update functions
            scan device 
            calc nodes
            update P&ID
            update T-s diagram
            '''
            self.call_update_funcs()
            # self.file.save_data()
