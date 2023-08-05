# -*- coding: utf-8 -*-
import json
from typing import Iterable

import grequests

import constants

api_address = 'https://wxfwdt.hit.edu.cn/app/bkskbcx/kbcxapp/getBkszkb'


def get_week_courses_req(uid: str, weekday: int):
    r = grequests.post(url=api_address, data={
        'info': json.dumps({
            'gxh': uid,
            'zc': str(weekday),
            'xnxq': constants.semester,
        })
    })
    # interest = r.json()['module']['data']
    return r


def from_iterable(it: Iterable, weekday):
    reqs = [get_week_courses_req(hit_id, weekday) for hit_id in it]
    res = grequests.map(reqs)
    for i in res:
        yield i
