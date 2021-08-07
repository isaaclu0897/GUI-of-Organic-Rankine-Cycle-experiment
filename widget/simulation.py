#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  8 00:46:46 2021

@author: wei
"""

from tkinter import Frame, Button, Entry
from db._realtime import shell


class MDot(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master=None)

        def confirm():
            mDot = float(mDot_entry.get())
            shell["mDot"] = mDot

        button = Button(
            master,
            text='confirm',
            command=confirm)
        button.pack(side="right")

        mDot_entry = Entry(master, width=10)
        mDot_entry.pack(side="right")
