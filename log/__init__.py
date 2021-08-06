#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 23:39:41 2021

@author: wei
"""

import logging
import logging.config

import os.path
log_path = os.path.dirname(os.path.realpath(__file__))

LOGGING_CONFIG = {
    "version": 1,
    "formatters": {
        "detail": {
            'format': '%(asctime)s | %(module)s | %(filename)s %(lineno)s | %(levelname)-8s | %(message)s',
        },
        "simple": {
            "format": "%(levelname)-8s | %(module)s | %(filename)s %(lineno)s | %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
        },
        "console_plain": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "detail"
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "filename": f"{log_path}/app.log",
            "formatter": "detail",
            "maxBytes": 1000000,  # 1 MB
            "backupCount": 5,
        },
        "time-rotating-file": {  # the name of handler
            'class': 'logging.handlers.TimedRotatingFileHandler',
            "level": "DEBUG",
            'filename': f'{log_path}/app.log',  # the path of the log file
            'when': 'midnight',  # time interval
            'formatter': 'detail',  # use the above "simple" formatter
        },
    },
    "loggers": {
        "console_logger": {
            # "handlers": ["console", "console_plain", "time-rotating-file"],
            "handlers": ["console", "time-rotating-file"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
    # "disable_existing_loggers": False,
}

logging.config.dictConfig(LOGGING_CONFIG)

logger = logging.getLogger("console_logger")
# logger.debug('debug message')
# logger.info('info message')

# for i in range(10):
#     logger.debug('debug message')
#     logger.info('info message')

