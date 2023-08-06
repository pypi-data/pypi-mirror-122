#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import copy
import csv
from datetime import datetime
import argparse
from .lmd import *

__help__ = """
this is help
"""

def parse_ids(origs_dict, val):
    '''parse the id'''
    if not val:
        raise Exception('need id')

    ids =[i.strip() for i in str(val).split(ID_SPLIT_STR)]
    # 检查格式是否合理
    if len(ids) > 2:
        raise Exception("id format error: %s, just suport one '-'" % val)
    if len(ids) == 2:
        for i in ids:
            if not i.isdigit():
                raise Exception('id format error: %s' % i)
        ids = [str(i) for i in range(int(ids[0]), int(ids[1])+1)]

    # 检查是否存在
    for i in ids:
        if i == '0':
            continue

        if not origs_dict.get(i):
            raise Exception('not fount the id: %s' % i)

    return ids

def parse_v(v):
    if not v:
        raise Exception('v must have value')
    vs = [i.strip() for i in str(v).split(SPLIT_STR)]
    for i in vs:
        if not i:
            raise Exception('v format error: %s' % i)
    return vs

def check_deadline_format(deadline):
    '''检查合理性'''
    for i in DATE_FORMAT:
        try:
            deadline_date = datetime.strptime(deadline, i)
            return True
        except:
            continue
    return False

def parse_values(values):
    value_dict = dict()
    if not values:
        raise Exception('values must have value')
    value_list = [i.strip() for i in str(values).split(SPLIT_STR)]
    for value in value_list:
        kv = value.split('=')
        if len(kv) != 2:
            raise Exception('the value format error: %s' % value)
        if kv[0] not in UPDATE_FIELDS + UPDATE_FIELDS_ABB:
            raise Exception('update field must be one of (%s)' % str(UPDATE_FIELDS + UPDATE_FIELDS_ABB))
        if kv[0] == 'deadline' and not check_deadline_format(kv[1]):
            raise Exception('deadline must be one of format (%s)' % DATE_FORMAT)
        value_dict[kv[0]] = kv[1]
    return value_dict

def parse_where(where):
    where_dict = dict()
    if not where:
        return None
    where_list = [i.strip() for i in str(where).split(SPLIT_STR)]
    for w in where_list:
        kv = w.split('=')
        if len(kv) != 2:
            raise Exception('the where format error: %s' % w)
        if kv[0] not in WHERE_FIELDS + WHERE_FIELDS_ABB:
            raise Exception('where field must be one of (%s)' % str(WHERE_FIELDS + WHERE_FIELDS_ABB))
        if kv[0] == 'deadline' and not check_deadline_format(kv[1]):
            raise Exception('deadline must be one of format (%s)' % DATE_FORMAT)
        if kv[0] == 'status' or kv[0] == FIELDS_ABB[idx('status')]:
            status_to_code = {v:k for k,v in STATUS.items()}
            if status_to_code.get(kv[1]) is None:
                raise Exception('the status value is error')
            kv[1] = status_to_code.get(kv[1])
        where_dict[kv[0]] = kv[1]
    return where_dict

def parse_order(order):
    order_dict = dict()
    if not order:
        return None
    order_list = [i.strip() for i in str(order).split(SPLIT_STR)]
    for o in order_list:
        kv = o.split('=')
        if len(kv) != 2:
            raise Exception('the order format error: %s' % o)
        if kv[0] not in ORDER_FIELDS + ORDER_FIELDS_ABB:
            raise Exception('order field must be one of (%s)' % str(ORDER_FIELDS + ORDER_FIELDS_ABB))
        if kv[1] not in ['asc', 'desc']:
            raise Exception('the value of order must be one of [asc, desc]')
        order_dict[kv[0]] = kv[1]
    return order_dict


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-show', '-s', nargs='?', 
                        help="""
                        Show project or tasks.\n
                        usage: lmd -show [id]\n
                        usage: lmd -show
                        """, 
                        const='0', default=None, required=False)
    parser.add_argument('--all', nargs='?', 
                        help="""
                        Used with '-show' to show all content of task.\n 
                        Used with '-delete' to delete all tasks.\n
                        usage: lmd -show [id] --all\n
                        usage: lmd -delete --all\n
                        """, 
                        const=True, default=False, required=False)
    parser.add_argument('--where', nargs=1, 
                        help="""
                        Used with '-show' to filter the result.\n
                        usage: lmd -show [id] --where 'executor=[executor]&&description=[description]'\n
                        usage: lmd -show [id] --where 'exe=[executor]&&desc=[description]'\n
                        fields includ name(na),executor(exe),description(desc),deadline(dl),status(sta)
                        """, 
                        default=None, required=False)
    parser.add_argument('-create', '-c', nargs=1, 
                        help="""
                        Create a new project.\n
                        usage: lmd -create [project-name]
                        """, 
                        default=None, required=False)
    parser.add_argument('-add', '-a', nargs=2, 
                        help="""
                        Add tasks to a task or project.\n
                        usage: lmd -add [id] '[task-name]&&[task-name]'
                        """, 
                        default=None, required=False)
    parser.add_argument('-remove', '-rm', nargs=1, 
                        help="""
                        Make task or tasks not display when execute '-show' command.\n
                        usage: lmd -remove [id]([id]-[id])
                        """, 
                        default=None, required=False)
    parser.add_argument('-back', '-bk', nargs=1, 
                        help="""
                        Make task or tasks display when execute '-show' command.\n
                        usage: lmd -back [id]([id]-[id])
                        """, 
                        default=None, required=False)
    parser.add_argument('-delete', '-d', nargs='?', 
                        help="""
                        Delete and never find it back.\n
                        usage: lmd -delete [id]([id]-[id])
                        """, 
                        const=True, default=None, required=False)
    parser.add_argument('-move', '-mv', nargs=2, 
                        help="""
                        Move from one task to another task.\n
                        usage: lmd -move [id]([id]-[id]) [father-id]
                        """, 
                        default=None, required=False)
    parser.add_argument('-update', '-u', nargs=2, 
                        help="""
                        Update the fields of tasks.\n
                        usage: lmd -update [id]([id]-[id]) \
                        'executor=[executor]&&description=[description]&&deadline=[deadline]'
                        """, 
                        default=None, required=False)
    parser.add_argument('-name', '-{0}'.format(FIELDS_ABB[idx('name')]), nargs=2, 
                        help="""
                        Change the name of tasks.\n
                        usage: lmd -name [id]([id]-[id]) [task-name]
                        """, 
                        default=None, required=False)
    #  parser.add_argument('-status',
    #                      '-{0}'.format(FIELDS_ABB[idx('status')]),
    #                      nargs=2,
    #                      help="""
    #                      Change the status of tasks.\n
    #                      usage: lmd -status [id] [status]
    #                      """,
    #                      default=None, required=False)
    parser.add_argument('-executor', 
                        '-{0}'.format(FIELDS_ABB[idx('executor')]), 
                        nargs=2, 
                        help="""
                        Change the executor of tasks.\n
                        usage: lmd -executor [id]([id]-[id]) [executor]
                        """, 
                        default=None, required=False)
    parser.add_argument('-description', 
                        '-{0}'.format(FIELDS_ABB[idx('description')]), 
                        nargs=2, 
                        help="""
                        Change the description of tasks.\n 
                        usage: lmd -description [id]([id]-[id]) [description]
                        """, 
                        default=None, required=False)
    parser.add_argument('-deadline', 
                        '-{0}'.format(FIELDS_ABB[idx('deadline')]), 
                        nargs=2, 
                        help="""
                        Change the deadline of tasks.\n
                        usage: lmd -deadline [id]([id]-[id]) [description]
                        """, 
                        default=None, required=False)
    parser.add_argument('-work', nargs=1, 
                        help="""
                        Turn tasks's status to working.\n
                        usage: lmd -work [id]([id]-[id])
                        """, 
                        default=None, required=False)
    parser.add_argument('-done', nargs=1, 
                        help="""
                        Turn tasks's status to finish.\n
                        usage: lmd -done [id]([id]-[id])
                        """, 
                        default=None, required=False)
    parser.add_argument('-cancel', nargs=1, 
                        help="""
                        Turn tasks's status to canceled.\n
                        usage: lmd -cancel [id]([id]-[id])
                        """, 
                        default=None, required=False)
    parser.add_argument('-stop', nargs=1, 
                        help="""
                        Turn tasks's status to stopped.\n
                        usage: lmd -stop [id]([id]-[id])
                        """, 
                        default=None, required=False)
    parser.add_argument('-conf', nargs=2, 
                        help="""
                        show-info: config the fields that will display at command '-show'.\n
                        usage: lmd -conf show-info 'path&&name&&executor&&deadline'
                        """, 
                        default=None, required=False)
    
    # parser.add_argument('-find_by', help="""find""", default=None, required=False)
    # parser.add_argument('--order_by', help="""order""", default=None, required=False)

    args = parser.parse_args()
    origs = read_csv()
    origs_dict = {i[idx('id')]:i for i in origs}

    if args.show:
        ids = parse_ids(origs_dict, args.show)
        where_dict = parse_where(args.where and args.where[0])
        show(origs, origs_dict, ids, args.all, where_dict)
    elif args.create:
        create(origs, args.create[0])
    elif args.add:
        ids = parse_ids(origs_dict, args.add[0])
        if len(ids) > 1:
            raise Exception('the number of id must be one!')
        vs = parse_v(args.add[1])
        add_tasks(origs, ids[0], vs)
    elif args.remove:
        ids = parse_ids(origs_dict, args.remove[0])
        rm_tasks(origs, origs_dict, ids)
    elif args.back:
        ids = parse_ids(origs_dict, args.back[0])
        bk_tasks(origs, origs_dict, ids)
    elif args.delete:
        if args.all:
            if args.delete != True:
                raise Exception("'-delete' can't pass value if '--all' exist ")
            del_tasks(origs, origs_dict, '0', args.all)
        else:
            if args.delete == True:
                raise Exception("'-delete' must pass a value if '--all' not exist ")
            ids = parse_ids(origs_dict, args.delete)
            del_tasks(origs, origs_dict, ids, args.all)
    elif args.move:
        ids = parse_ids(origs_dict, args.move[0])
        target_ids = parse_ids(origs_dict, args.move[1])
        if len(target_ids) > 1:
            raise Exception('the father id must be one id')
        mv_tasks(origs_dict, ids, target_ids[0])
    elif args.update:
        ids = parse_ids(origs_dict, args.update[0])
        value_dict = parse_values(args.update[1])
        update_tasks(origs, origs_dict, ids, value_dict)
    #  elif args.find_by:
    #      ids = parse_ids(origs_dict, args.find_by[0])
    #      where_dict = parse_where(args.where and args.where[0])
    #      order_by = parse_order(args.order_by)
    #      if order_by and len(order_by) > 1:
    #          raise Exception('the order_by just support one value')
    #      find(origs, ids, where, order_by)
    elif args.name:
        ids = parse_ids(origs_dict, args.name[0])
        vs = parse_v(args.name[1])
        if len(vs) > 1:
            raise Exception('the v value must be one!')
        update_tasks(origs, origs_dict, ids, dict(name=vs[0]))
    #  elif args.status:
    #      ids = parse_ids(origs_dict, args.status[0])
    #      vs = parse_v(args.status[1])
    #      if len(vs) > 1:
    #          raise Exception('the v value must be one!')
    #      update_tasks(origs, origs_dict, ids, dict(status=vs[0]))
    elif args.executor:
        ids = parse_ids(origs_dict, args.executor[0])
        vs = parse_v(args.executor[1])
        if len(vs) > 1:
            raise Exception('the v value must be one!')
        update_tasks(origs, origs_dict, ids, dict(executor=vs[0]))
    elif args.description:
        ids = parse_ids(origs_dict, args.description[0])
        vs = parse_v(args.description[1])
        if len(vs) > 1:
            raise Exception('the v value must be one!')
        update_tasks(origs, origs_dict, ids, dict(description=vs[0]))
    elif args.deadline:
        ids = parse_ids(origs_dict, args.deadline[0])
        vs = parse_v(args.deadline[1])
        if len(vs) > 1:
            raise Exception('the v value must be one!')
        update_tasks(origs, origs_dict, ids, dict(deadline=vs[0]))
    elif args.work:
        ids = parse_ids(origs_dict, args.work[0])
        update_tasks(origs, origs_dict, ids, dict(status=WORKING))
    elif args.done:
        ids = parse_ids(origs_dict, args.done[0])
        update_tasks(origs, origs_dict, ids, dict(status=DONE))
    elif args.cancel:
        ids = parse_ids(origs_dict, args.cancel[0])
        update_tasks(origs, origs_dict, ids, dict(status=CANCELED))
    elif args.stop:
        ids = parse_ids(origs_dict, args.stop[0])
        update_tasks(origs, origs_dict, ids, dict(status=STOPPED))
    elif args.conf:
        if args.conf[0] not in CONF_TYPE:
            raise Exception('conf type error! just suport(%s)', CONF_TYPE)
        if args.conf[0] == 'show-info':
            if args.conf[1]:
                vs = parse_v(args.conf[1])
                for v in vs:
                    if v not in SHOW_ALL_FIELDS:
                        raise Exception('not suport this field:%s, \
                                        the fields must pick up from [%s]' % (v, SHOW_ALL_FIELDS))
                conf_show_fields(vs)
            else:
                conf_show_fields()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
