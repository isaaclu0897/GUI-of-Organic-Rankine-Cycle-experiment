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
        # "console_plain": {
        #     "class": "logging.StreamHandler",
        #     "level": "INFO",
        #     "formatter": "plain"
        # },
        # "file": {
        #     "class": "logging.FileHandler",
        #     "level": "INFO",
        #     "filename": "./log.txt",
        #     "formatter": "detail",
        # }
    },
    "loggers": {
        "console_logger": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        # "console_plain_logger": {
        #     "handlers": ["console_plain"],
        #     "level": "INFO",
        #     "propagate": False,
        # },
        # "file_logger": {
        #     "handlers": ["file"],
        #     "level": "INFO",
        #     "propagate": False,
        # }
    },
    # "disable_existing_loggers": False,
}

# 執行測試
logging.config.dictConfig(LOGGING_CONFIG)

logger = logging.getLogger("console_logger")
logger.debug('debug message')
logger.info('info message')
logger.warning('warning message')
logger.error('error message')
logger.critical('critical message')

# logger2 = logging.getLogger("console_plain")
# logger2.debug('debug message')
# logger2.info('info message')
# logger2.warning('warning message')
# logger2.error('error message')
# logger2.critical('critical message')

# logger3 = logging.getLogger("file")
# logger3.debug('debug message')
# logger3.info('info message')
# logger3.warning('warning message')
# logger3.error('error message')
# logger3.critical('critical message')
