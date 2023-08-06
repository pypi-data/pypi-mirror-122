#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from .settings import FIELDS, TIME_FORMAT

class Task():
    id = '0'
    parent_id = '0'
    name = ''
    executor = ''
    description = ''
    deadline = ''
    status = '1'
    display = '1'
    finish_date = ''
    create_date = datetime.now().strftime(TIME_FORMAT)

    def to_list(self):
        return [getattr(self, i) for i in FIELDS]
