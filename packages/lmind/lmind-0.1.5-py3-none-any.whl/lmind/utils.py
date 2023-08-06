#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import copy
import sys
import csv
from .settings import *
from .constants import *

idx = lambda x:FIELDS_IDX.get(x)
plen = lambda x:len(x)
# plen = lambda x:len(x.encode('utf8'))

def get_file_path():
    if CSV_PATH:
        if not os.path.exists(CSV_PATH):
            os.makedirs(CSV_PATH)
        file_path = os.path.join(CSV_PATH, CSV_NAME)
    else:
        file_path = CSV_NAME
    if not os.path.isfile(file_path):
        os.mknod(file_path)
    return file_path

def read_csv():
    file_path = get_file_path()
    with open(file_path, 'r') as f:
        datas = csv.reader(f)
        return list(datas)

def write_csv(datas):
    file_path = get_file_path()
    with open(file_path, 'w') as f:
        writer = csv.writer(f)
        for i in datas:
            writer.writerow(i)

def del_csv():
    file_path = get_file_path()
    os.remove(file_path)

def read_conf_file():
    conf_file_path=os.path.join(CSV_PATH, CONF_NAME)
    if not os.path.isfile(conf_file_path):
        return None
    with open(conf_file_path, 'r') as f:
        datas = csv.reader(f)
        return list(datas)

def write_conf_file(conf_datas):
    conf_file_path =os.path.join(CSV_PATH, CONF_NAME)
    with open(conf_file_path, 'w') as f:
        writer = csv.writer(f)
        for i in conf_datas:
            writer.writerow(i)

def find_by(datas, **where):
    res = []
    for data in datas:
        for field in where.keys():
            if field in SEARCH_FIELDS + SEARCH_FIELDS_ABB:
                if str(data[idx(field)]).find(where[field]) == -1:
                    break
            else:
                if data[idx(field)] != where[field]:
                    break
        else:
            res.append(data)
    return res

def format_show(data, fields):
    res = []
    for field in fields:
        if field == 'path':
            res.append(data[idx('id')])
        elif field == 'status':
            res.append(STATUS[data[idx(field)]])
        else:
            res.append(data[idx(field)])
    return res

