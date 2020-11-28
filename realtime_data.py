#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 01:11:35 2020

@author: wei
"""

import node
import config as cfg

data = {}

def _make_system_nodes_shell():
    for i, name in enumerate(cfg.config["System"]["node"], 1):
        data[f"{name}"] = node.Node(name, i)

_make_system_nodes_shell()

def _make_system_attr_shell():
    for name in cfg.config["System"]["attribute"]:
        data[f"{name}"] = 0

_make_system_attr_shell()

def _make_other_system_nodes_shell():
    for name in cfg.config["OtherSystem"]["node"]:
        for attr in cfg.config["OtherSystem"]["node"][f"{name}"]:
            data[f"{name}"] = {f"{attr}":0}

_make_other_system_nodes_shell()
