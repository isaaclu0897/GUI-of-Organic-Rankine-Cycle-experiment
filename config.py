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


def reload_config():
    pass

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

# %%


def _resize_FIG_size():
    FIG["width"] = _resize(FIG["width"])
    FIG["height"] = _resize(FIG["height"])


FIG = {"width": 8, "height": 6}
_resize_FIG_size()


def _make_LINE_config():
    return config["line"]


LINE = _make_LINE_config()

# %%


def _import_v34972A():
    return config["v34972A"]


v34972A = _import_v34972A()

# %%


def _make_SENSOR_config():
    ''' import sensor config '''
    node_config = config["System"]["node"]
    attr_config = config["System"]["attribute"]
    node_config_o = config["OtherSystem"]["node"]

    SENSOR_config = {}
    for name in node_config:
        for attr, value in node_config[name].items():
            if "sensor" in value:
                if isinstance(value["sensor"], list):
                    obj = value["sensor"]

                    SENSOR_config[obj[0]] = {
                        "name": name, "type": attr, "setting": obj[1:]	}
                else:
                    SENSOR_config[f"{value['sensor']}"] = {
                        "name": name, "type": attr	}
    for name in node_config_o:
        for attr, value in node_config_o[name].items():
            if "sensor" in value:
                SENSOR_config[f"{value['sensor']}"] = {
                    "name": name, "type": attr	}
    for name, value in attr_config.items():
        if "sensor" in value:
            SENSOR_config[f"{value['sensor']}"] = {"name": name, "type": name}

    return {k: SENSOR_config[k] for k in sorted(SENSOR_config)}


SENSOR = _make_SENSOR_config()


def _make_SENSOR_setting():
    return {
        "probe_type": "TCouple",
        "type": "T",
        "range": 10,
        "resolution": 5.5,
        "gain": 2.1,
        "offset": 1
    }


SENSOR_SETTING = _make_SENSOR_setting()
# %%


def _make_System_attr_formula():
    attr_config = config["System"]["attribute"]

    attr_formula = {}
    for name in attr_config:
        for attr, value in attr_config[name].items():

            if "in_out" in attr:
                #         # SENSOR_config[f"{name}_{attr}"] = value["sensor"]
                attr_formula[f"{name}"] = value

    return attr_formula


FM = _make_System_attr_formula()

# %%


def _make_experiment_file_config():

    FILE_config = config["experiment-file"]
    FILE_config["header"] = FILE_config["column"].keys()
    FILE_config["data"] = FILE_config["column"].values()
    return FILE_config


FILE = _make_experiment_file_config()
