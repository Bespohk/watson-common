# -*- coding: utf-8 -*-
# Support functions, classes
from datetime import datetime
from watson.common import json


def some_func():
    pass


DATA = {}


def date_serialize(value, format='%d/%m/%Y', timezone=None):
    return value.strftime(format)


def date_deserialize(value, format='%d/%m/%Y'):
    return datetime.strptime(value, format)


def data_list_serialize(value, **kwargs):
    return [
        json.serialize(v,
                       attributes=('name', 'date'),
                       strategies={'date': date_serialize}, **kwargs)
        for v in value]


def data_dict_serialize(value, **kwargs):
    return {
        k: json.serialize(v,
                          attributes=('name', 'date',),
                          strategies={'date': date_serialize}, **kwargs)
        for k, v in value.items()}


class MyObject(object):
    name = None
    date = None
    data_list = None
    data_dict = None
    private = None

    def __init__(self, name=None, date=None):
        self.name = name
        self.date = date
