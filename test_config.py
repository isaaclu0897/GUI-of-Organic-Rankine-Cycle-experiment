#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 23:24:33 2020

@author: wei
"""

import config as cfg

print("\n----- LABEL -----")
print(cfg.LABEL)

print("\n----- GUI -----")
print(cfg.GUI)

print("\n----- font -----")
def list_font():
    import tkinter as tk
    import tkinter.font as tkFont
    tk.Tk()
    return list(tkFont.families())
print(list_font())
