#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 23:19:47 2020

@author: wei
"""

from json import load
from PIL import ImageTk, Image
import tkinter as tk
tk.Tk() # avoid [Too early to create image]

''' import config '''


def _import_config():
    with open('config.json', 'r') as f:
        config = load(f)
        del f
    return config


config = _import_config()

''' import label config '''


def _make_LABEL_config():
    node_config = config["System"]["node"]
    attr_config = config["System"]["attribute"]

    LABEL_config = {}
    for name in node_config:
        for attr, value in node_config[name].items():
            LABEL_config[f"{name}_{attr}"] = value["GUI"]
    for name, value in attr_config.items():
        LABEL_config[f"{name}"] = value["GUI"]

    return LABEL_config


LABEL = _make_LABEL_config()

''' import GUI config '''


def _make_GUI_config():
    return config["GUI"]


GUI = _make_GUI_config()

''' import photo '''


def _resize(value):
    return int(value * GUI["scaling_factor"])


GUI["_image"] = Image.open(GUI["path"])
GUI["_image"] = GUI["_image"].resize(
    (_resize(GUI["_image"].width), _resize(GUI["_image"].height)), Image.ANTIALIAS)
GUI["photo"] = ImageTk.PhotoImage(GUI["_image"])

