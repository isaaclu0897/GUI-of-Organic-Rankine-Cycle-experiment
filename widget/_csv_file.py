#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  8 01:49:02 2021

@author: wei
"""

from pathlib import Path
from datetime import datetime as dt
import db._config as cfg
from db._realtime import shell
from csv import writer
from shutil import copyfile


class CsvFile:
    def __init__(self):
        self.header = cfg.FILE["header"]
        self.path = cfg.FILE["folder-path"]
        self.file_buffer_count = 0
        self.data_buffer_count = 0

        today = dt.now().date()
        self.lock_file = f"{self.path}/.{today}.lock"
        self.csv_file = f"{self.path}/{today}.csv"

        self.open_file()

    def open_file(self):
        ''' check file exist?
        if file is not exist,
        system will create file with header
        '''
        Path(self.path).mkdir(parents=True, exist_ok=True)
        if Path(self.lock_file).is_file():
            self.file = open(self.lock_file, 'a', newline="")
            self.writer = writer(self.file)
        else:
            ''' avoid user crash file
            Lock file, just GUI can used.
            Prevent user from crashing the system due to file modification.
            '''
            self.file = open(self.lock_file, 'a', newline="")
            self.writer = writer(self.file)
            print(self.header)
            self.writer.writerow(self.header)
            self.file.flush()

    def save_data(self):
        self.write_data(cfg.FILE["data_buffer"])
        self.transfer_file(cfg.FILE["file_buffer"])

    def write_data(self, buffer=0):
        self.writer.writerow(self.row_data())

        if self.data_buffer_count > buffer:
            self.file.flush()
            self.data_buffer_count = 0

        self.data_buffer_count += 1

    def row_data(self):
        def myround(num):
            length = len(str(num))
            if length - 1 > 4:
                n = 4 - len(str(num).split(".")[0])
                if n < 1:
                    return int(num)
                return round(num, n)
            else:
                return num
        row = []
        for value in cfg.FILE["data"]:
            if "shell" in value:
                v = myround(eval(value))

            elif "." in value:
                name, attr = value.split(".")
                v = myround(shell[f"{name}"][f"{attr}"])
            else:
                try:
                    if isinstance(shell[f"{value}"], float):
                        v = myround(shell[f"{value}"])  # timestamp
                    else:
                        v = shell[f"{value}"]  # f"{value}" in data count time
                except:
                    v = f"{value}"
                    # print(f"{value} can not convert")
            row.append(v)
        return row

    def transfer_file(self, buffer=5, close=False):
        ''' transfer lock file to experiment file
        When experiment is done,
        system will copy lock file into experiment file.
        '''
        if self.file_buffer_count > buffer or close:
            copyfile(self.lock_file, self.csv_file)
            self.file_buffer_count = 0
        self.file_buffer_count += 1

    def __del__(self):
        self.transfer_file(close=True)
