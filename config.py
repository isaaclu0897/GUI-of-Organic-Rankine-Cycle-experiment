#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 23:19:47 2020

@author: wei
"""

from json import load
from PIL import ImageTk, Image


class DictX(dict):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as k:
            raise AttributeError(k)

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError as k:
            raise AttributeError(k)

def dictx(func):
    def warp():
        return DictX(func())
    return warp

@dictx
def _import_config():
    with open('config.json', 'r') as f:
        config = load(f)
        del f
    return config

config = _import_config()

''' --- '''

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

GUI = DictX(config["GUI"])

image = Image.open(GUI["path"])

# w, h = self.scaling(image.width), self.scaling(image.height)
# image = image.resize((w, h), Image.ANTIALIAS)
# self.img = ImageTk.PhotoImage(image)

#     def scaling(self, value):
#         return int(value * self.scaling_factor)
