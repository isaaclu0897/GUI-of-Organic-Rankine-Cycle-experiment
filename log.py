#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 23:39:41 2021

@author: wei
"""

import logging
import logging.config


LOGGING_CONFIG = {
    "version": 1,
    "formatters": {
        "detail": {
            'format': '%(asctime)s | %(name)s | %(module)s | %(filename)s | %(lineno)s | %(levelname)-8s | %(message)s',
        },
        "simple": {
            "format": "%(levelname)-8s | %(message)s",
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
            "level": "INFO",
            "formatter": "detail"
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "filename": "./log.txt",
            "formatter": "detail",
            "maxBytes": 1000000,  # 1 MB
            "backupCount": 5,
        },
        'time-rotating-file': {  # the name of handler
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'f3.log',  # the path of the log file
            'when': 'midnight',  # time interval
            'formatter': 'detail',  # use the above "simple" formatter
        },
    },
    "loggers": {
        "console_logger": {
            "handlers": ["console", "console_plain", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
    "disable_existing_loggers": False,
}

logging.config.dictConfig(LOGGING_CONFIG)

logger = logging.getLogger("console_logger")
logger.debug('debug message')
logger.info('info message')

for i in range(100000):
    logger.debug('debug message')
    logger.info('info message')

