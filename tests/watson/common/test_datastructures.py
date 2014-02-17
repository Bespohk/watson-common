# -*- coding: utf-8 -*-
from pytest import raises
from watson.common.datastructures import ImmutableDict, ImmutableMultiDict
from watson.common.datastructures import MultiDict, dict_deep_update
from copy import copy, deepcopy


class TestImmutableDict(object):

    def test_create(self):
        d = ImmutableDict({'test': 'blah', 'something': '2'})
        assert len(d) == 2

    def test_copy(self):
        d = ImmutableDict({'test': 'blah', 'something': '2'})
        c = copy(d)
        c['blah'] = 'blah'
        assert d != c

    def test_set_value(self):
        with raises(TypeError):
            d = ImmutableDict()
            d['something'] = 'test'

    def test_deep_copy(self):
        d = ImmutableDict({'test': 'blah', 'something': '2'})
        d2 = deepcopy(d)
        d3 = d.copy()
        assert d == d2
        assert d == d3

    def test_delete(self):
        with raises(TypeError):
            d = ImmutableDict({'test': 'blah', 'something': '2'})
            del d['test']

    def test_clear(self):
        with raises(TypeError):
            d = ImmutableDict({'test': 'blah', 'something': '2'})
            d.clear()


class TestImmutableMultiDict(object):

    def test_create(self):
        d = ImmutableMultiDict({'test': 'blah', 'something': '2'})
        assert len(d) == 2

    def test_set_value(self):
        with raises(TypeError):
            d = ImmutableMultiDict()
            d['something'] = 'test'

    def test_del_value(self):
        with raises(TypeError):
            d = ImmutableMultiDict()
            d['something'] = 'test'
            del d['something']

    def test_copy(self):
        d = ImmutableMultiDict({'test': 'blah', 'something': '2'})
        d2 = copy(d)
        d3 = d.copy()
        assert len(d) == len(d2)
        assert len(d) == len(d3)

    def test_deep_copy(self):
        d = ImmutableMultiDict({'test': 'blah', 'something': '2'})
        d2 = deepcopy(d)
        assert len(d) == len(d2)


class TestMultiDict(object):

    def test_add_key(self):
        d = MultiDict({'test': 'blah', 'something': '2'})
        d['test'] = 'something'
        d['another'] = ['b']
        d['another'] = 'c'
        assert len(d['test']) == 2
        assert len(d.get('test')) == 2
        assert d.get('something') == '2'

    def test_get_value(self):
        d = MultiDict()
        d['list'] = []
        assert d.get('empty') is None
        assert d.get('list') is not None


class TestFunctions(object):

    def test_dict_deep_update(self):
        d1 = {'a': {'b': 3}}
        d2 = {'a': {'b': 4}}
        merged = dict_deep_update(d1, d2)
        assert merged['a']['b'] == 4

    def test_complex_deep(self):
        d1 = {
            'a': {
                'b': {
                    'key': [
                        'a',
                        'b',
                        'c',
                        'd',
                    ]
                }
            }
        }
        d2 = {
            'a': {
                'b': {
                    'key': [
                        'e',
                        'f',
                        'g',
                    ]
                }
            }
        }
        merged = dict_deep_update(d1, d2)
        assert 'c' in merged['a']['b']['key']

    def test_dict_deep_update_not_dict(self):
        d1 = {'a': {'b': 3}}
        d2 = 'b'
        merged = dict_deep_update(d1, d2)
        assert merged == 'b'
