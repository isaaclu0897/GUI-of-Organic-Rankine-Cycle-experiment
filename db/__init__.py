#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  3 01:21:44 2021

@author: wei
"""

print("db __init__.py")
import db._config

cfg = {}
rt = {}

def init():
    cfg["ccc"] = 1
    cfg = db.config._import_config()

print("db __init__.py")
