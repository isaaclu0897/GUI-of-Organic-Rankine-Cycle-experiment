#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 01:11:35 2020

@author: wei
"""

from thermo.node import Node
from db._config import config

shell = {}

def _make_system_nodes_shell():
    for i, name in enumerate(config["System"]["node"], 1):
        shell[f"{name}"] = Node(name, i)

_make_system_nodes_shell()

def _make_system_attr_shell():
    for name in config["System"]["attribute"]:
        shell[f"{name}"] = 0

_make_system_attr_shell()

def _make_other_system_nodes_shell():
    for name in config["OtherSystem"]["node"]:
        for attr in config["OtherSystem"]["node"][f"{name}"]:
            shell[f"{name}_{attr}"] = 0

_make_other_system_nodes_shell()

def _make_other_field():
    shell["count"] = 0
    shell["time"] = 0
    shell["ts"] = 0

_make_other_field()

if __name__ == "__main__":
    print(shell)