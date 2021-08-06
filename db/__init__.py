#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  3 01:21:44 2021

@author: wei
"""

# from db.config import config
from log import logger
logger.info('load database')
from db._config import LABEL
from db._config import GUI
from db._config import LINE
from db._config import v34972A
from db._config import SENSOR
from db._config import SENSOR_SETTING
from db._config import FM
from db._config import FILE

logger.info('create realtime shell')
from db._realtime import shell
