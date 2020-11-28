#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 23:19:47 2020

@author: wei
"""

from json import load
from PIL import Image
from PIL import ImageTk


def _resize(value):
    ''' resize function '''
    return int(value * config["GUI"]["scaling_factor"])


# %%


def _import_config():
    ''' import config '''
    with open('config.json', 'r') as f:
        config = load(f)
        del f
    return config


config = _import_config()
# %%


def _make_LABEL_config():
    ''' import label config '''
    node_config = config["System"]["node"]
    attr_config = config["System"]["attribute"]
    node_config_o = config["OtherSystem"]["node"]

    LABEL_config = {}
    for name in node_config:
        for attr, value in node_config[name].items():
            if "GUI" in value:
                LABEL_config[f"{name}_{attr}"] = value["GUI"]
    for name in node_config_o:
        for attr, value in node_config_o[name].items():
            if "GUI" in value:
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
# %%


def _make_GUI_config():
    ''' import GUI config '''
    return config["GUI"]


def _resize_GUI_fontsize():
    GUI["fontsize"] = _resize(GUI["fontsize"])


GUI = _make_GUI_config()
_resize_GUI_fontsize()


GUI["image"] = Image.open(GUI["path"])
GUI["image"] = GUI["image"].resize(
    (_resize(GUI["image"].width), _resize(GUI["image"].height)), Image.ANTIALIAS)


def import_photo():
    ''' import photo
    load the .gif image file, put gif file here
    test gif, png and jpg, jpg can't use
    '''
    return ImageTk.PhotoImage(GUI["image"])

#%%

def _import_v34970A():
    return config["v34970A"]

v34970A = _import_v34970A()

#%%

def _make_SENSOR_config():
    ''' import sensor config '''
    node_config = config["System"]["node"]
    attr_config = config["System"]["attribute"]
    node_config_o = config["OtherSystem"]["node"]

    SENSOR_config = {}
    for name in node_config:
        for attr, value in node_config[name].items():
            if "sensor" in value:
                # SENSOR_config[f"{name}_{attr}"] = value["sensor"]
                SENSOR_config[f"{value['sensor']}"] = {"name" : name,"type" : attr	}
    for name in node_config_o:
        for attr, value in node_config_o[name].items():
            if "sensor" in value:
                # SENSOR_config[f"{name}_{attr}"] = value["sensor"]
                SENSOR_config[f"{value['sensor']}"] = {"name" : name,"type" : attr	}
    for name, value in attr_config.items():
        if "sensor" in value:
            # SENSOR_config[f"{name}"] = value["sensor"]
            SENSOR_config[f"{value['sensor']}"] = {"name" : name,"type" : name	}

    return SENSOR_config 

SENSOR = _make_SENSOR_config()

#%%

# def _make_NODE_config():
#     return config["System"]["node"]

# NODE = _make_NODE_config()