#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 23:19:47 2020

@author: wei
"""

from json import load
from PIL import Image
from PIL import ImageTk

''' resize function '''
def _resize(value):
    return int(value * config["GUI"]["scaling_factor"])

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

def _resize_LABEL_config():
    for key, GUI_attr in LABEL.items():
        GUI_attr["posx"] = _resize(GUI_attr["posx"])
        GUI_attr["posy"] = _resize(GUI_attr["posy"])

LABEL = _make_LABEL_config()
_resize_LABEL_config()

''' import GUI config '''

def _make_GUI_config():
    return config["GUI"]
def _resize_GUI_fontsize():
    GUI["fontsize"] = _resize(GUI["fontsize"])

GUI = _make_GUI_config()
_resize_GUI_fontsize()

''' import photo '''


GUI["image"] = Image.open(GUI["path"])
GUI["image"] = GUI["image"].resize(
    (_resize(GUI["image"].width), _resize(GUI["image"].height)), Image.ANTIALIAS)

def import_photo():
    return ImageTk.PhotoImage(GUI["image"])