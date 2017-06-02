# -*- coding: utf-8 -*-
from datetime import datetime
import json as stdlib_json
from tests.watson.common import support
from watson.common import json


class TestSerialize(object):

    def test_basic(self):
        obj = support.MyObject('test')
        d = json.serialize(obj, ('name',))
        assert d == {'name': 'test'}

    def test_complex(self):
        obj = support.MyObject('test', date=datetime.now())
        d = json.serialize(obj, ('name', 'date'),
                           strategies={'date': support.date_serialize})
        assert isinstance(d['date'], str)

    def test_list(self):
        obj = support.MyObject('test', date=datetime.now())
        obj.data_list = [
            support.MyObject('testing', date=datetime.now()),
            support.MyObject('again', date=datetime.now())
        ]
        d = json.serialize(obj, ('name', 'date', 'data_list'),
                           strategies={
            'data_list': support.data_list_serialize,
            'date': support.date_serialize})
        assert isinstance(d['dataList'][0]['date'], str)

    def test_dict(self):
        obj = support.MyObject('test', date=datetime.now())
        obj.data_dict = {
            'test': support.MyObject('testing', date=datetime.now()),
        }
        d = json.serialize(obj,
                           ('name', 'date', 'data_dict'),
                           strategies={'data_dict': support.data_dict_serialize,
                                       'date': support.date_serialize})
        assert isinstance(d['dataDict']['test']['date'], str)

    def test_none_attribute(self):
        obj = support.MyObject('test')
        d = json.serialize(obj,
                           ('name', 'date'),
                           strategies={'date': support.date_serialize})
        assert 'date' not in d


class TestDeserialize(object):

    def test_basic(self):
        d = {'name': 'test'}
        obj = json.deserialize(d, class_=support.MyObject,
                               attributes=('name',))
        assert isinstance(obj, support.MyObject)
        assert obj.name == 'test'
        assert not obj.date

    def test_complex(self):
        d = {'name': 'test', 'date': '1/1/2014'}
        obj = json.deserialize(d, class_=support.MyObject,
                               attributes=('name', 'date'),
                               strategies={'date': support.date_deserialize})
        assert isinstance(obj.date, datetime)

    def test_none_attribute(self):
        d = {'name': 'test'}
        obj = json.deserialize(d, class_=support.MyObject,
                               attributes=('name', 'date'))
        assert not obj.date

    def test_deserialize_camel_to_snake(self):
        d = {'name': 'test', 'dateTime': 'now'}
        obj = json.deserialize(
            d, class_=support.MyObject, attributes=('name', 'date_time'))
        assert obj.date_time == 'now'
        assert obj.name == 'test'


class TestEncoder(object):

    def test_encode_dict(self):
        data = {
            'some_attribute': 'value',
            'nested': {
                'some_attribute': 'value'
            },
            'nested_list': [
                {'some_attribute': 'test'},
                'test'
            ]
        }
        encoder = json.JSONEncoder()
        snake_case = encoder.encode(data, camelcase=False)
        camel_case = encoder.encode(data)
        assert 'some_attribute' in snake_case
        assert 'someAttribute' in camel_case

    def test_encode_class(self):
        obj = support.MyObject(name='Test')
        serialized = stdlib_json.dumps(obj, cls=json.JSONEncoder)
        assert serialized == '{}'
        encoder = json.JSONEncoder()
        serialized = encoder.encode(
            obj,
            mapping={
                support.MyObject: {
                    'attributes': ('name',)
                }
            })
        assert serialized == '{"name": "Test"}'

    def test_encode_class_nested(self):
        nested = support.NestedObject(support.MyObject(name='Test'))
        encoder = json.JSONEncoder()
        serialized = encoder.encode(
            nested,
            mapping={
                support.NestedObject: {
                    'attributes': ('nested',)
                },
                support.MyObject: {
                    'attributes': ('name',)
                }
            })
        assert serialized == '{"nested": {"name": "Test"}}'

    def test_encode_types(self):
        obj = [{'date': datetime.now()}]
        encoder = json.JSONEncoder()
        serialized = encoder.encode(obj, mapping={
            datetime: support.date_serialize
        })
        assert '"date":' in serialized and '/' in serialized
