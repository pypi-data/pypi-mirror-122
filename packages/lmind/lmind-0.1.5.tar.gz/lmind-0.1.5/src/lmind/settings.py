#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
class ENUMSBASE:
    @classmethod
    def values(cls):
        if hasattr(cls, '_values'):
            return getattr(cls, '_values')
        _values = [getattr(cls, i) for i in list(cls.__dict__.keys()) if str(i).isupper()]
        setattr(cls, '_values', _values)
        return _values
    @classmethod
    def keys(cls):
        if hasattr(cls, '_keys'):
            return getattr(cls, '_keys')
        _keys = [i for i in list(cls.__dict__.keys()) if str(i).isupper()]
        setattr(cls, '_keys', _keys)
        return _keys

ID_SPLIT_STR = '-'
SPLIT_STR = '&&'
CSV_PATH = os.path.dirname(os.path.abspath(__file__))
CSV_NAME = 'tasks.csv'
CONF_NAME = 'conf.csv'
TIME_FORMAT = '%Y-%m-%d'
DATE_FORMAT = ['%Y-%m-%d', '%Y%m%d', '%Y/%m/%d', '%Y.%m.%d']

class FS(ENUMSBASE):
    ID = 'id'
    PID = 'parent_id'
    NA = 'name'
    EXE = 'executor'
    DESC = 'description'
    DL = 'deadline'
    STA = 'status'
    DIS = 'display'
    FD = 'finish_date'
    CD = 'create_date'

class FSABB(ENUMSBASE):
    ID = 'id'
    PID = 'pid'
    NA = 'na'
    EXE = 'exe'
    DESC = 'desc'
    DL = 'dl'
    STA = 'sta'
    DIS = 'dis'
    FD = 'fd'
    CD = 'cd'

FIELDS = [FS.ID, FS.PID, FS.NA, FS.EXE, FS.DESC, FS.DL, FS.STA, FS.DIS, FS.FD, FS.CD] 
FIELDS_ABB = [FSABB.ID, FSABB.PID, FSABB.NA, FSABB.EXE, FSABB.DESC, FSABB.DL, FSABB.STA, FSABB.DIS, FSABB.FD, FSABB.CD]
FIELDS_IDX = {field:index for index, field in enumerate(FIELDS)}
FIELDS_IDX.update(
    {field:index for index, field in enumerate(FIELDS_ABB)}
)
SHOW_FIELDS = ['path', FS.NA, FS.EXE, FS.DL, FS.STA]
SHOW_FIELDS_ABB = [FSABB.ID] + [FIELDS_ABB[FIELDS_IDX[field]] for field in SHOW_FIELDS[1:]]
SHOW_ALL_FIELDS = ['path', FS.NA, FS.EXE, FS.DESC, FS.DL, FS.STA, FS.DIS, FS.FD, FS.CD]
SHOW_ALL_FIELDS_ABB = [FSABB.ID] + [FIELDS_ABB[FIELDS_IDX[field]] for field in SHOW_ALL_FIELDS[1:]]
UPDATE_FIELDS = [FS.NA, FS.EXE, FS.DESC, FS.DL]
UPDATE_FIELDS_ABB = [FIELDS_ABB[FIELDS_IDX[field]] for field in UPDATE_FIELDS]
WHERE_FIELDS = [FS.NA, FS.EXE, FS.DESC, FS.DL, FS.STA, FS.FD]
WHERE_FIELDS_ABB = [FIELDS_ABB[FIELDS_IDX[field]] for field in WHERE_FIELDS]
ORDER_FIELDS = [ FS.DL, FS.FD, FS.CD]
ORDER_FIELDS_ABB = [FIELDS_ABB[FIELDS_IDX[field]] for field in ORDER_FIELDS]
SEARCH_FIELDS = [FS.NA, FS.EXE, FS.DESC]
SEARCH_FIELDS_ABB = [FIELDS_ABB[FIELDS_IDX[field]] for field in SEARCH_FIELDS]

CONF_TYPE = ['show-info']
